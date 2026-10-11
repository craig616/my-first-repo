"""Read the Obsidian recipe notes and write app/recipes.js for the wireframe.

Run: python3 app/build_data.py   (from ~/Documents/Recipes)
"""
import json, re, pathlib

VAULT = pathlib.Path.home() / "Documents/Obsidian Vault/Me/Personal/Recipes"
OUT = pathlib.Path(__file__).with_name("recipes.js")


def parse_value(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
    v = v.strip('"')
    if v in ("true", "false"):
        return v == "true"
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v or None


def sections(body):
    out, name = {}, "_intro"
    for line in body.split("\n"):
        m = re.match(r"^## (.+)", line)
        if m:
            name = m.group(1).strip()
            continue
        out.setdefault(name, []).append(line)
    return out


def parse_steps(lines):
    steps = []
    for line in lines:
        m = re.match(r"^\d+\.\s+(.*)", line)
        if m:
            text = m.group(1)
            timer = re.search(r"⏱\s*(\d+)(?:\s*[–-]\s*(\d+))?\s*min", text)
            seek = re.search(r"▶\s*(\d+):(\d{2})", text)
            clean = re.sub(r"\s*(·\s*)?(⏱[^·▶]*|▶\s*\d+:\d{2})", "", text).strip(" ·")
            steps.append({
                "text": clean,
                "timer_min": int(timer.group(2) or timer.group(1)) if timer else None,
                "video_s": int(seek.group(1)) * 60 + int(seek.group(2)) if seek else None,
                "uses": [],
            })
        elif steps and re.match(r"^\s+\*Uses:", line):
            steps[-1]["uses"] = [u.strip() for u in re.sub(r"^\s+\*Uses:\s*|\*\s*$", "", line).split(",") if u.strip()]
    return steps


def parse_note(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).split("\n"):
        kv = re.match(r"^([a-z_]+):\s*(.*?)(\s+#\s.*)?$", line)
        if kv:
            fm[kv.group(1)] = parse_value(kv.group(2))
    if not fm.get("id"):
        return None
    sec = sections(m.group(2))
    intro = " ".join(l.strip() for l in sec.get("_intro", []) if l.strip() and not l.startswith("# "))
    ingredients = []
    for line in sec.get("Ingredients", []):
        h = re.match(r"^- \*\*(.+?)\*\*", line)
        if h:
            ingredients.append({"heading": h.group(1)})
        elif line.startswith("- "):
            ingredients.append({"text": line[2:].strip()})
    bullets = lambda name: [l[2:].strip() for l in sec.get(name, []) if l.startswith("- ")]
    code = (fm.get("sources") or ["ig:"])[0].split(":", 1)[1]
    return {
        **fm,
        "code": code,
        "intro": intro,
        "ingredients": ingredients,
        "steps": parse_steps(sec.get("Method", [])),
        "notes": bullets("Notes"),
        "to_check": bullets("To check"),
        "hero": f"../media/{code}/hero.jpg",
        "video": f"../media/{code}/video.mp4",
        "note_file": path.name,
    }


recipes = [r for p in sorted(VAULT.glob("*.md")) if (r := parse_note(p))]
staples = [l.strip() for l in (OUT.parent.parent / "pipeline/staples.txt").read_text().splitlines() if l.strip()]
OUT.write_text("window.RECIPES = " + json.dumps(recipes, ensure_ascii=False, indent=1) + ";\nwindow.STAPLES = " + json.dumps(staples) + ";\n", encoding="utf-8")
print(f"{len(recipes)} recipes → {OUT}")
for r in recipes:
    print(f"  {r['id']}: {len(r['ingredients'])} ingredients, {len(r['steps'])} steps, "
          f"{sum(1 for s in r['steps'] if s['timer_min'])} timers, status={r.get('status')}")
