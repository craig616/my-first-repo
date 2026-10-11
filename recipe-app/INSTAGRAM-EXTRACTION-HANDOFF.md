# Handoff: turning a saved Instagram collection into a searchable library (creative inspiration)

This is for a new Claude Code session. It describes the process that turned Craig's 533 saved food Reels into a structured archive with media. Everything here was proven on that project; the inspiration-specific parts are marked **[adapt]**.

The working reference implementation is `~/Documents/Recipes/pipeline/collect.py`. Read it before writing anything new: copy it and change the paths and outputs rather than starting from scratch.

---

## 1. Goal and principles

Take one saved Instagram collection (for example "Inspiration", "Type", "Motion") and produce:
1. **An archive:** every post's media on disk, in a folder named after its shortcode. Posts disappear, so this pass is the record.
2. **A structured note per post** that can be searched, filtered and later imported into an app.
3. **A state file** so any session can stop and resume.

Principles that held up:
- **Content first, then structure, then UI.** Get the archive and the labels right before building anything to browse them.
- **Be polite: it's Craig's personal account.** Small batches, long sleeps, stop at the first rate-limit signal.
- **Every step is resumable and skips work already on disk.** One process at a time.
- **The script collects; the model interprets.** Downloading, transcribing and frame-grabbing are scripted. Choosing the key image, reading on-screen text and writing the note are done by the model, looking at the files.
- **Be honest about gaps.** Anything guessed goes in a "To check" section, not into the facts.

---

## 2. Tools (already installed on this Mac)

| Tool | Use |
|---|---|
| `~/Documents/Recipes/.venv` | Python with `yt-dlp`, `faster-whisper`, `requests`. Reuse it, or make a new venv with the same three packages. |
| venv yt-dlp | Instagram downloads (`--cookies-from-browser chrome`) |
| `/opt/homebrew/bin/yt-dlp` | Newer Homebrew build. Use it for YouTube, which broke on the older venv copy. |
| `/opt/homebrew/bin/ffmpeg`, `ffprobe` | Audio extraction, contact sheets, frame grabs |
| faster-whisper `small`, `int8`, `vad_filter=True` | Transcripts (the model is cached locally) |
| `sips -Z 720` | Small thumbnails for Obsidian |
| puppeteer-core + Chrome | Rendering and checking any HTML you build (in the scratchpad `uxtest/node_modules`) |

Auth is always the **logged-in Chrome session's cookies**. Craig must be logged in to Instagram in Chrome. There are no passwords and no tokens in files.

---

## 3. The pipeline

### Phase 0: List the collection (one-off, a few requests)
1. Craig opens the collection in Chrome. The URL looks like `instagram.com/<username>/saved/<name>/<collection_id>/`. **The number is the collection ID.**
2. Page through the private web API with the Chrome cookies:
   - `GET https://www.instagram.com/api/v1/feed/collection/<collection_id>/posts/`
   - then `?max_id=<next_max_id>` until `more_available` is false
   - Sleep 3–6 s between pages and stop at about 40 pages. Each page holds about 20–30 posts.
3. Use the headers and cookie session from `_cookie_session()` in `collect.py`: `X-IG-App-ID: 936619743392459`, `X-Requested-With: XMLHttpRequest`, `X-ASBD-ID: 129477`, `X-CSRFToken` from the `csrftoken` cookie, and `Sec-Fetch-*` set to same-origin / cors / empty.
4. For each item (`it.get('media', it)`), save: `code`, URL, `user.username`, `media_type` (1 image, 2 video, 8 carousel), `product_type` (`clips` = Reel), `video_duration`, `taken_at`, `caption.text`, and `carousel_media_count`.
5. Write `source/<collection>.json`, plus a human CSV index (n, url, creator, type, duration, posted, first caption line) and a plain URL list.

Minimal pager (adapt from `collect.py`):
```python
s = _cookie_session(); items = []; maxid = None
for page in range(40):
    r = s.get(f'https://www.instagram.com/api/v1/feed/collection/{CID}/posts/', params={'max_id': maxid} if maxid else {}, timeout=30)
    if r.status_code in (401, 403, 429): raise SystemExit(f'STOP {r.status_code}')
    d = r.json()
    for it in d.get('items', []):
        m = it.get('media', it)
        items.append({'code': m['code'], 'user': m['user']['username'], 'media_type': m['media_type'],
                      'product': m.get('product_type'), 'duration': m.get('video_duration'),
                      'taken_at': m.get('taken_at'), 'caption': (m.get('caption') or {}).get('text', ''),
                      'carousel_count': m.get('carousel_media_count')})
    if not d.get('more_available'): break
    maxid = d.get('next_max_id'); time.sleep(random.uniform(3, 6))
```

### Phase 1: Triage (model only, no network)
Read every caption and sort each post into a class, recorded in `pipeline/state.csv` (one row per post: `code, url, creator, media_type, duration_s, lang, triage, title_guess, stage, notes` plus progress flags).
- In the food project the classes were: `recipe_full`, `recipe_partial`, `recipe_spoken`, `not_recipe`, `carousel`.
- **[adapt]** For inspiration, classify by what matters is in the post. Suggested classes:
  - `visual`: the image or video *is* the point
  - `process`: a technique or how-to, often spoken
  - `reference_link`: points to a portfolio, site or shop
  - `talk`: an idea or opinion, mostly speech
  - `not_relevant`
- The class decides which steps run. Transcripts matter for `process` and `talk`; frames and key images matter for `visual`.

### Phase 2: Collect (script, polite, resumable)
`collect.py --next N` (N ≤ 50), or with a list of codes. For each post it writes `media/<code>/`:

| File | What |
|---|---|
| `video.mp4` | 720p max, with metadata embedded |
| `info.json` | yt-dlp metadata (creator, date, music, etc.) |
| `cover.jpg` | Instagram's cover |
| `audio.m4a` | extracted locally with `ffmpeg -vn -c:a copy` (no extra request) |
| `transcript.txt` | `# lang=xx avg_no_speech_prob=0.nn`, then `[start-end] text` lines. **Never overwritten.** |
| `frames.jpg` | contact sheet, 1 frame every 2–4 s, 6 columns, 240 px wide |
| `_candidates/c1..c6.jpg` + `sheet.jpg` | candidate key frames; deleted once the key image is chosen |
| `hero.jpg` | the chosen key image (see Phase 3) |
| `carousel_01.jpg`… / `carousel_NN.mp4` | carousels: every item, at full resolution, from the CDN |
| `comments.json` | only when the caption says "see comments": the creator's own comments |

yt-dlp command (copy exactly):
```
yt-dlp --cookies-from-browser chrome -f "bv*[height<=720]+ba/b[height<=720]/b" --merge-output-format mp4
  --embed-metadata --write-info-json --write-thumbnail --convert-thumbnails jpg
  --sleep-requests 3 --sleep-interval 20 --max-sleep-interval 60
  --download-archive pipeline/downloaded-video.txt --no-playlist --retries 0 --extractor-retries 0
  -o "media/<code>/video.%(ext)s" https://www.instagram.com/p/<code>/
```
Carousels and single images: one `GET /api/v1/media/<media_id>/info/` (convert the shortcode to a media ID with the base64 alphabet in `media_id()`), then download each `image_versions2` candidate (the widest) and any `video_versions` from the CDN.

**[adapt] Key images for inspiration:**
- Video: grab candidate frames **across the whole clip**, not only the last 25%. For food the finished dish comes at the end; for inspiration the best frame can be anywhere.
- Use about 12 candidates evenly spaced, and let the model pick 1–3.
- For carousels, every slide is kept and the model picks the lead image.
- Keep originals at full resolution, because creative references are used for zooming and cropping. Make a 720px copy only for Obsidian.

### Phase 3: Interpret (model, per post, batches of about 25, subagents of about 5)
For each collected post, the model:
1. **Picks the key image** by looking at `_candidates/sheet.jpg` (or the carousel). Avoid frames with burned-in captions, UI or watermarks when a clean one exists. `collect.py --hero CODE N` promotes it and writes the thumbnail.
2. **Reads on-screen text** from `frames.jpg` when there's no speech. About a third of Reels were music-only.
3. **Judges the transcript:** Whisper transcribes song lyrics and invents filler ("You") on music. Under about 20 characters, or obviously lyrics, means **no speech**. Record `has_speech`.
4. **Follows links** only when the caption points to one (portfolio, studio site, shop). Make at most about 3 polite fetches, never get round a paywall, and skip and note it if the content isn't found.
5. **Writes the note** (format below), then `collect.py --set CODE note_file=… title=…`.

Duplicates (the same work saved twice, or a repost) become **one note with several `sources`**. The media stays in each code's own folder.

### Phase 4: Index and browse
`media/INDEX.csv` maps `code → note id, note file, creator, title`. Obsidian is the interim database, read through frontmatter and Bases or Dataview. Build an app only after the labels have proved useful.

---

## 4. IDs and layout (keep them stable; an app may import them later)
- `code` = Instagram shortcode. It's the permanent key for a post and its folder.
- `id` = a slug for the *note* (unique; add `-2` and so on if needed). One note can have several sources (`ig:<code>`, `web:<url>`).
- One folder per post (`media/<code>/`) with fixed filenames, so nothing needs a lookup table.
- `pipeline/state.csv` is the single source of truth for progress. Write it atomically (to a temp file, then replace).
- Commands: `--next N` · `CODE…` · `--hero CODE N|cover|carousel` · `--comments CODE` · `--set CODE k=v…` · `--reindex` (rebuild the flags from disk, no network).

---

## 5. [adapt] Note format for inspiration
Filename: `<Short descriptive title>.md`. Frontmatter (keep the field names stable):

```yaml
---
id: risograph-gradient-poster-series
title: Risograph gradient poster series
status: ok                     # ok | needs_checking
sources: [ig:DcBld-hI3ef]
source_url: https://www.instagram.com/p/DcBld-hI3ef/
creator: "@studioname"
creator_name: Studio Name
creator_url: https://www.instagram.com/studioname/
creator_site:                  # portfolio or studio site, if found
posted: 2026-08-14
media: "~/<INSPO_ROOT>/media/DcBld-hI3ef/"
thumbnail: "[[_thumbs/DcBld-hI3ef.jpg]]"
kind: visual                   # visual | process | reference_link | talk
format: [poster]               # poster, identity, packaging, editorial, type specimen, motion, UI, illustration, photography, 3D, spatial, campaign, social
discipline: [graphic design, print]
technique: [risograph, gradient]   # how it was made, in plain words
typography: [condensed sans, all caps]   # describe it; name the typeface only if the creator does
palette: ["#f2c75c", "#1b2a4a", "#e8e4de"]   # 3–6 sampled hex values from the key image
palette_words: [warm, high contrast]
composition: [grid, big type, lots of white space]
mood: [playful, bold]          # 1–3 words for how it feels
use_for: [landing pages, campaign key visual]   # where Craig might use the idea
client_or_brand:               # only if stated
has_speech: false
sources_used: [caption, frames]     # + transcript | comments | web
added: 2026-10-05
---

# Risograph gradient poster series

<2–3 plain sentences: what it is, what's distinctive, why it's worth keeping>

## What to take from it
- <specific, reusable observations: a grid move, a colour pairing, a motion timing, a type treatment>

## Technique
<for process posts: the steps, tools and settings, from the transcript, frames or caption>

## To check
- <anything guessed: typeface identification, colours from a compressed frame, the client>

## Source
Work by [Studio Name (@studioname)](https://www.instagram.com/studioname/) · [Original post](https://www.instagram.com/p/DcBld-hI3ef/)

> [!quote]- Original caption
> <verbatim>

> [!note]- Transcript
> <verbatim with timestamps, or "(no speech)">
```

The palette can be scripted (sample the key image with ffmpeg or Pillow and take k-means centres), so the model only checks it. Keep **controlled vocabularies** for `format`, `discipline`, `technique` and `mood` in `pipeline/vocab-*.txt`. Add to them deliberately, so filters stay useful. In the recipes project, `ingredients-vocab.txt` did this job.

---

## 6. Politeness and safety (non-negotiable)
- **At most 50 posts per run, at most 2 runs a day.** These limits are enforced in `collect.py` through `pipeline/runs.csv`.
- **One Instagram media request per post.** Comments are an extra request, made only when the caption says the content is there; pinned comments can need 2.
- **Stop instantly** on `429`, `rate limit`, `login required`, `checkpoint`, `challenge_required` or `feedback_required`. Use the regex in `STOP_PATTERNS`, and keep the 429 pattern tight (`\bstatus(?:_code)?\W{0,3}429\b`): a loose one matched "429" inside media IDs and stopped a run for nothing. Exit with code 3, tell Craig, and **never retry in a loop**.
- **Only one collector process at a time.** Parallel runs overwrite `state.csv`.
- CDN image and video downloads (`*.cdninstagram.com`, `*.fbcdn.net`) are not API calls, but keep them sequential.
- Credit every creator and link the original. The archive is private reference, not for republishing.
- **Write only inside the project's own folders.** Craig's vault has work folders that must not be read or touched. Ask Craig where the new project's folder and vault subfolder should live before writing.

---

## 7. Lessons learned (save yourself the debugging)
1. **YouTube "reload" or format errors:** use Homebrew's newer yt-dlp, not the venv copy.
2. **A false 429 stop** came from a loose regex (see above).
3. **"(no speech)" overwrote real transcripts.** Never overwrite `transcript.txt`; let the model judge whether it's speech.
4. **The caption is the main source** for facts. Audio added something useful in about 1 in 3 posts, and was critical in about 1 in 13.
5. **"Full" captions still miss things.** Check every note for gaps and list them under "To check".
6. **Key images:** reject frames with burned-in subtitles. Re-pick any that slipped through in a final pass. In the food project, 1 of 37 needed a manual re-pick.
7. **Carousels:** save *every* item, including videos inside carousels.
8. **Test on about 10 varied posts first** (silent, spoken, carousel, non-English, link-out), with a checkpoint for Craig to review before the full run.
9. **Keep state on disk, not in the conversation.** Write a `PROJECT-STATE.md` (links, decisions, data status, next steps) and update it at each milestone, so a compacted or new session can resume.

---

## 8. Suggested first session for the inspiration project
1. Ask Craig for: the collection URL (for the ID), the project folder (for example `~/Documents/Inspiration/`), the vault subfolder for notes, and which disciplines matter most.
2. Copy `~/Documents/Recipes/pipeline/collect.py` and change these:
   - `ROOT`, `VAULT_THUMBS`
   - the candidate-frame spread (the whole clip, about 12 frames)
   - the full-resolution key images
   - the triage classes in `--next`
3. Run Phase 0 to list the collection, then Phase 1 triage.
4. Run a test batch of 10, then **checkpoint**: show the notes, folders, MB used, any warnings and doubts. Stop for review.
5. After approval: `--next 50` up to twice a day. Between runs, write notes in batches with subagents.
6. Once there are about 50 notes, review whether the labels support the searches Craig actually makes, before building any UI.
