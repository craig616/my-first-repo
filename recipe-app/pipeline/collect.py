#!/usr/bin/env python3
"""Collect Instagram recipe posts into media/<code>/ (resumable, polite).

Usage (run with .venv/bin/python):
  collect.py CODE [CODE ...]       collect these posts
  collect.py --next N              take the next N un-collected posts from state.csv (N <= 50)
  collect.py --hero CODE N         pick _candidates/cN.jpg as hero.jpg, remove _candidates,
                                   copy a 720px thumbnail into the vault _thumbs folder
  collect.py --comments CODE       fetch the creator's own comments (one extra IG request)
  collect.py --set CODE k=v ...    update state.csv / media/INDEX.csv (recipe_id, note_file, title, ...)
  collect.py --reindex             rebuild state flags from what is on disk (no network)

Every step skips work already on disk.  Any rate-limit / login-required / 429
response stops ALL Instagram requests at once (exit code 3).  Limits: 50 posts
per run, 2 runs per day (pipeline/runs.csv).
"""
import csv, json, os, random, re, shutil, subprocess, sys, time, datetime, glob

ROOT = os.path.expanduser('~/Documents/Recipes')
MEDIA = f'{ROOT}/media'
PIPE = f'{ROOT}/pipeline'
STATE = f'{PIPE}/state.csv'
INDEX = f'{MEDIA}/INDEX.csv'
RUNS = f'{PIPE}/runs.csv'
ARCHIVE = f'{PIPE}/downloaded-video.txt'
VAULT_THUMBS = os.path.expanduser('~/Documents/Obsidian Vault/Me/Personal/Recipes/_thumbs')
FFMPEG = '/opt/homebrew/bin/ffmpeg'
FFPROBE = '/opt/homebrew/bin/ffprobe'
YTDLP = f'{ROOT}/.venv/bin/yt-dlp'
MAX_PER_RUN, MAX_RUNS_PER_DAY = 50, 2

NEW_COLS = ['recipe_id', 'note_file', 'has_speech', 'web_url', 'needs_comments',
            'video_ok', 'transcript_ok', 'frames_ok', 'hero_ok', 'size_mb']
INDEX_COLS = ['code', 'recipe_id', 'note_file', 'creator', 'title']
STOP_PATTERNS = re.compile(r'rate.?limit|login required|log in|HTTP Error 429|\bstatus(?:_code)?\W{0,3}429\b|too many requests|'
                           r'checkpoint|challenge_required|feedback_required', re.I)


class StopInstagram(Exception):
    pass


# ---------------------------------------------------------------- state
def load_state():
    with open(STATE, newline='') as f:
        r = csv.DictReader(f)
        cols = list(r.fieldnames)
        rows = list(r)
    for c in NEW_COLS:
        if c not in cols:
            cols.append(c)
    for row in rows:
        for c in cols:
            row.setdefault(c, '')
    return cols, rows


def save_state(cols, rows):
    tmp = STATE + '.tmp'
    with open(tmp, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, STATE)


def load_index():
    if not os.path.exists(INDEX):
        return {}
    with open(INDEX, newline='') as f:
        return {r['code']: r for r in csv.DictReader(f)}


def save_index(idx):
    with open(INDEX, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=INDEX_COLS)
        w.writeheader()
        for code in sorted(idx):
            w.writerow({c: idx[code].get(c, '') for c in INDEX_COLS})


def folder_mb(code):
    total = 0
    for dp, _, fs in os.walk(f'{MEDIA}/{code}'):
        total += sum(os.path.getsize(os.path.join(dp, f)) for f in fs)
    return round(total / 1e6, 2)


def refresh(code, cols, rows, idx):
    """Recompute flags from disk for one code and update state + index."""
    d = f'{MEDIA}/{code}'
    row = next(r for r in rows if r['code'] == code)
    exists = lambda n: os.path.exists(f'{d}/{n}')
    row['video_ok'] = 'yes' if (exists('video.mp4') and exists('info.json')) or \
        glob.glob(f'{d}/carousel_01.*') else row['video_ok']
    if exists('transcript.txt'):
        row['transcript_ok'] = 'yes'
        txt = open(f'{d}/transcript.txt', encoding='utf-8').read().strip()
        row['has_speech'] = 'no' if txt == '(no speech)' else 'yes'
    if glob.glob(f'{d}/carousel_01.*'):
        row['has_speech'] = row['has_speech'] or 'no'
        row['transcript_ok'] = row['transcript_ok'] or 'n/a'
        row['frames_ok'] = row['frames_ok'] or 'n/a'
    row['frames_ok'] = 'yes' if exists('frames.jpg') else row['frames_ok']
    row['hero_ok'] = 'yes' if exists('hero.jpg') else row['hero_ok']
    if exists('comments.json') or exists('web.md'):
        pass
    row['size_mb'] = str(folder_mb(code))
    if row['stage'] == 'noted':
        pass
    elif row['video_ok'] == 'yes' and exists('hero.jpg') and (exists('transcript.txt') or glob.glob(f'{d}/carousel_01.*')):
        row['stage'] = 'collected'
    elif os.path.isdir(d) and (exists('video.mp4') or exists('audio.m4a')):
        row['stage'] = 'partial'
    i = idx.setdefault(code, {'code': code})
    i['creator'] = row['creator']
    i.setdefault('title', row['title_guess'])
    if row.get('recipe_id'):
        i['recipe_id'] = row['recipe_id']
    if row.get('note_file'):
        i['note_file'] = row['note_file']
    if not i.get('title'):
        i['title'] = row['title_guess']
    save_state(cols, rows)
    save_index(idx)


# ---------------------------------------------------------------- helpers
def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def duration(path):
    r = sh([FFPROBE, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path])
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def has_audio(path):
    r = sh([FFPROBE, '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_name',
            '-of', 'csv=p=0', path])
    return bool(r.stdout.strip())


def check_stop(text):
    if STOP_PATTERNS.search(text or ''):
        raise StopInstagram(text.strip()[-600:])


# ---------------------------------------------------------------- steps
def step_video(code, row):
    d = f'{MEDIA}/{code}'
    if os.path.exists(f'{d}/video.mp4') and os.path.exists(f'{d}/info.json'):
        return False
    if row['media_type'] == 'carousel':
        return step_carousel(code)
    os.makedirs(d, exist_ok=True)
    # remove the code from the archive if files are missing, so yt-dlp does not skip it
    if os.path.exists(ARCHIVE):
        lines = [l for l in open(ARCHIVE) if l.strip() != f'instagram {code}']
        open(ARCHIVE, 'w').writelines(lines)
    cmd = [YTDLP, '--cookies-from-browser', 'chrome',
           '-f', 'bv*[height<=720]+ba/b[height<=720]/b', '--merge-output-format', 'mp4',
           '--embed-metadata', '--write-info-json', '--write-thumbnail', '--convert-thumbnails', 'jpg',
           '--sleep-requests', '3', '--sleep-interval', '20', '--max-sleep-interval', '60',
           '--download-archive', ARCHIVE, '--no-playlist', '--retries', '0', '--extractor-retries', '0',
           '--ffmpeg-location', '/opt/homebrew/bin',
           '-o', f'{d}/video.%(ext)s', f'https://www.instagram.com/p/{code}/']
    r = sh(cmd)
    out = (r.stderr or '') + (r.stdout or '')
    check_stop(out)
    if r.returncode != 0:
        print(f'  yt-dlp failed for {code} (exit {r.returncode}): {out.strip()[-400:]}')
        return True
    for src, dst in (('video.info.json', 'info.json'), ('video.jpg', 'cover.jpg')):
        if os.path.exists(f'{d}/{src}'):
            os.replace(f'{d}/{src}', f'{d}/{dst}')
    return True


def _cookie_session():
    import requests
    from yt_dlp.cookies import extract_cookies_from_browser
    jar = extract_cookies_from_browser('chrome')
    s = requests.Session()
    for c in jar:
        if 'instagram.com' in c.domain:
            s.cookies.set(c.name, c.value, domain=c.domain)
    csrf = s.cookies.get('csrftoken', domain='.instagram.com') or s.cookies.get('csrftoken')
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36',
        'X-IG-App-ID': '936619743392459', 'X-Requested-With': 'XMLHttpRequest',
        'X-ASBD-ID': '129477', 'X-CSRFToken': csrf or '',
        'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.instagram.com/'})
    return s


def media_id(code):
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    n = 0
    for ch in code:
        n = n * 64 + alpha.index(ch)
    return str(n)


def api_get(url, session):
    r = session.get(url, timeout=30)
    if r.status_code in (429, 401, 403) or r.status_code >= 400 and 'login' in r.text.lower():
        raise StopInstagram(f'HTTP {r.status_code}: {r.text[:300]}')
    check_stop(r.text[:500] if r.status_code != 200 else '')
    r.raise_for_status()
    return r.json()


def step_carousel(code):
    """Carousel: one web-API request for the media info, then download every image."""
    d = f'{MEDIA}/{code}'
    os.makedirs(d, exist_ok=True)
    if glob.glob(f'{d}/carousel_01.*') and os.path.exists(f'{d}/info.json'):
        return False
    s = _cookie_session()
    data = api_get(f'https://www.instagram.com/api/v1/media/{media_id(code)}/info/', s)
    item = data['items'][0]
    json.dump(data, open(f'{d}/info.json', 'w'), ensure_ascii=False, indent=1)
    kids = item.get('carousel_media') or [item]
    import requests
    for n, k in enumerate(kids, 1):
        cands = k['image_versions2']['candidates']
        best = max(cands, key=lambda c: c['width'])
        img = requests.get(best['url'], timeout=60)   # CDN, not an Instagram API call
        open(f'{d}/carousel_{n:02d}.jpg', 'wb').write(img.content)
        if k.get('video_versions'):   # carousel video items: CDN download, saved beside the still
            vb = max(k['video_versions'], key=lambda v: v.get('height', 0) if v.get('height', 0) <= 720 else 0)
            vid = requests.get(vb['url'], timeout=120)
            open(f'{d}/carousel_{n:02d}.mp4', 'wb').write(vid.content)
    shutil.copy(f'{d}/carousel_01.jpg', f'{d}/cover.jpg')
    return True


def step_audio(code):
    d = f'{MEDIA}/{code}'
    if os.path.exists(f'{d}/audio.m4a') or not os.path.exists(f'{d}/video.mp4'):
        return
    if not has_audio(f'{d}/video.mp4'):
        print('  no audio stream')
        return
    sh([FFMPEG, '-loglevel', 'error', '-y', '-i', f'{d}/video.mp4', '-vn', '-c:a', 'copy', f'{d}/audio.m4a'])


_model = None


def step_transcript(code):
    d = f'{MEDIA}/{code}'
    tp = f'{d}/transcript.txt'
    if os.path.exists(tp):
        return
    if not os.path.exists(f'{d}/audio.m4a'):
        if os.path.exists(f'{d}/video.mp4'):
            open(tp, 'w').write('(no speech)\n')   # video without audio track
        return
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel('small', device='cpu', compute_type='int8')
    segs, info = _model.transcribe(f'{d}/audio.m4a', vad_filter=True)
    segs = list(segs)
    lines = [f'[{s.start:.1f}-{s.end:.1f}] {s.text.strip()}' for s in segs]
    body = '\n'.join(lines)
    plain = re.sub(r'\[[^\]]*\]', '', body).strip()
    nsp = sum(s.no_speech_prob for s in segs) / len(segs) if segs else 1.0
    # Keep the raw transcript; the model judges speech vs lyrics/filler when writing the note.
    open(tp, 'w', encoding='utf-8').write(f'# lang={info.language} avg_no_speech_prob={nsp:.2f}\n' + (body or '(no audio detected)') + '\n')
    print(f'  transcript: lang={info.language}, {len(plain)} chars')


def step_frames(code):
    d = f'{MEDIA}/{code}'
    v = f'{d}/video.mp4'
    if not os.path.exists(v):
        return
    dur = duration(v)
    if not os.path.exists(f'{d}/frames.jpg'):
        step = min(4.0, max(2.0, dur / 24))
        n = int(dur / step) + 1
        cols = 6
        rows = max(1, -(-n // cols))
        sh([FFMPEG, '-loglevel', 'error', '-y', '-i', v, '-vf',
            f'fps=1/{step:.2f},scale=240:-2,tile={cols}x{rows}', '-frames:v', '1', '-q:v', '3',
            f'{d}/frames.jpg'])
    if not os.path.exists(f'{d}/hero.jpg') and not os.path.isdir(f'{d}/_candidates'):
        c = f'{d}/_candidates'
        os.makedirs(c)
        start = dur * 0.75
        for i in range(6):
            t = start + (dur * 0.24) * i / 5
            sh([FFMPEG, '-loglevel', 'error', '-y', '-ss', f'{t:.2f}', '-i', v, '-frames:v', '1',
                '-q:v', '2', f'{c}/c{i + 1}.jpg'])
        sh([FFMPEG, '-loglevel', 'error', '-y', '-framerate', '1', '-i', f'{c}/c%d.jpg', '-vf',
            'scale=320:-2,tile=3x2', '-frames:v', '1', '-q:v', '3', f'{c}/sheet.jpg'])


def set_hero(code, n):
    d = f'{MEDIA}/{code}'
    src = f'{d}/_candidates/c{n}.jpg' if n not in ('cover', 'carousel') else f'{d}/cover.jpg'
    if not os.path.exists(src):
        sys.exit(f'no such frame {src}')
    shutil.copy(src, f'{d}/hero.jpg')
    shutil.rmtree(f'{d}/_candidates', ignore_errors=True)
    os.makedirs(VAULT_THUMBS, exist_ok=True)
    out = f'{VAULT_THUMBS}/{code}.jpg'
    shutil.copy(f'{d}/hero.jpg', out)
    sh(['sips', '-Z', '720', out])
    cols, rows = load_state()
    idx = load_index()
    refresh(code, cols, rows, idx)
    print(f'hero set for {code} from {os.path.basename(src)}; thumbnail {out}')


def fetch_comments(code):
    d = f'{MEDIA}/{code}'
    if os.path.exists(f'{d}/comments.json'):
        print('comments.json already present')
        return
    cols, rows = load_state()
    row = next(r for r in rows if r['code'] == code)
    creator = row['creator'].lstrip('@')
    s = _cookie_session()
    data = api_get(f'https://www.instagram.com/api/v1/media/{media_id(code)}/comments/'
                   f'?can_support_threading=true&permalink_enabled=false', s)
    allc = list(data.get('pinned_comments') or []) + list(data.get('comments', []))
    mine = [c for c in allc if c.get('user', {}).get('username') == creator]
    json.dump({'creator': creator, 'total_seen': len(allc), 'commenters_seen': [c.get('user', {}).get('username') for c in allc],
               'response_keys': sorted(data.keys()), 'comments': mine},
              open(f'{d}/comments.json', 'w'), ensure_ascii=False, indent=1)
    row['needs_comments'] = 'done'
    idx = load_index()
    refresh(code, cols, rows, idx)
    print(f'{code}: {len(mine)} creator comments of {len(data.get("comments", []))} seen')


# ---------------------------------------------------------------- run control
def runs_today():
    if not os.path.exists(RUNS):
        return 0
    today = datetime.date.today().isoformat()
    return sum(1 for l in open(RUNS) if l.startswith(today))


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    os.makedirs(MEDIA, exist_ok=True)
    if argv[0] == '--hero':
        set_hero(argv[1], argv[2] if argv[2] in ('cover', 'carousel') else int(argv[2]))
        return 0
    if argv[0] == '--comments':
        try:
            fetch_comments(argv[1])
        except StopInstagram as e:
            print('STOP: Instagram refused:', e)
            return 3
        return 0
    cols, rows = load_state()
    idx = load_index()
    if argv[0] == '--set':
        code = argv[1]
        row = next(r for r in rows if r['code'] == code)
        i = idx.setdefault(code, {'code': code})
        for kv in argv[2:]:
            k, v = kv.split('=', 1)
            if k in INDEX_COLS:
                i[k] = v
            if k in cols:
                row[k] = v
        refresh(code, cols, rows, idx)
        return 0
    if argv[0] == '--reindex':
        for r in rows:
            if os.path.isdir(f'{MEDIA}/{r["code"]}'):
                refresh(r['code'], cols, rows, idx)
        return 0
    if argv[0] == '--next':
        n = min(int(argv[1]), MAX_PER_RUN)
        codes = [r['code'] for r in rows
                 if r['triage'] != 'not_recipe' and r['stage'] == 'triaged' and r['video_ok'] != 'yes'][:n]
    else:
        codes = argv[:MAX_PER_RUN]
    byc = {r['code']: r for r in rows}
    missing = [c for c in codes if c not in byc]
    if missing:
        sys.exit(f'not in state.csv: {missing}')
    need_net = [c for c in codes if not (os.path.exists(f'{MEDIA}/{c}/video.mp4') and
                                         os.path.exists(f'{MEDIA}/{c}/info.json'))
                and not (glob.glob(f'{MEDIA}/{c}/carousel_01.*') and os.path.exists(f'{MEDIA}/{c}/info.json'))]
    if need_net:
        if runs_today() >= MAX_RUNS_PER_DAY:
            sys.exit(f'already {MAX_RUNS_PER_DAY} Instagram runs today; try tomorrow')
        with open(RUNS, 'a') as f:
            f.write(f'{datetime.datetime.now().isoformat(timespec="seconds")},{len(need_net)}\n')
    stopped = None
    first_net = True
    for code in codes:
        row = byc[code]
        print(f'== {code} {row["creator"]} ({row["media_type"]})')
        if code in need_net and stopped is None:
            if not first_net:
                time.sleep(random.uniform(20, 60))
            first_net = False
            try:
                step_video(code, row)
            except StopInstagram as e:
                stopped = str(e)
                print('STOP: Instagram refused:', e)
        step_audio(code)
        step_transcript(code)
        step_frames(code)
        refresh(code, cols, rows, idx)
        print(f'  done: {folder_mb(code)} MB')
        if stopped:
            break
    return 3 if stopped else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
