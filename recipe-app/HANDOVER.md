# Handover: Instagram food collection → Obsidian recipes

You are processing Craig's saved Instagram recipe Reels into clean recipe notes in his Obsidian vault, and archiving each post's media. Work in phases, keep state on disk so any session can resume, and **stop at each checkpoint for Craig to review**.

## Context
- A private, shared family recipe app for Craig and his partner (UK household). Obsidian is the interim "database". The notes and media will later be imported into a self-hosted web app, so **IDs, folder layout and frontmatter must stay exactly as specified**.
- Original design brief, for background: `/Users/craig/.claude/uploads/7e225530-d818-4274-ae32-023e08096998/841d871c-recipe-app-handover.md`
- **Posts disappear** (deleted, made private). This pass is the archive. Collect everything listed below in one go, so nobody has to go back to Instagram.

### What testing showed (13 Reels)
- The **caption is the main source** for quantities. Audio never had quantities the caption lacked.
- Audio caught something useful in 4 of 13 Reels. In 1 of 13 the gap would have broken the recipe: the mirin cod caption omits "marinate for at least an hour".
- **About a third of Reels have no speech at all** (music only). Their only other source is the on-screen text.
- On music, Whisper invents filler: it heard the single word "You" on a silent Reel. **A transcript under 20 characters means no speech.**
- Some `recipe_full` captions still miss key facts (the cod caption has no amount of cod). "Full" isn't a guarantee. Check every recipe for missing quantities and times.

## IDs and labelling (do not deviate)
- **`code`** = the Instagram shortcode (e.g. `DcBld-hI3ef`, also yt-dlp's `%(id)s`). It is the permanent key for a **post** and its media.
- **`id`** = the recipe's own ID: a lowercase slug from the UK title (e.g. `fried-mushroom-pasta`). It must be unique, so add `-2` and so on if needed. One recipe can have several sources.
- **`sources`** = a list of source keys: `ig:<code>`, and later `web:<url>` and so on. Duplicate posts of the same recipe become **one note** with several `sources`, and the media stays in each code's own folder.
- Every file belonging to a post lives in **its own folder named after the code**. Filenames inside are fixed (see below), so the app can find them without a lookup.
- `pipeline/state.csv` stays the single source of truth for progress. `media/INDEX.csv` maps `code → recipe id, note filename, creator, title` for humans and the future app.

## Paths
| What | Where |
|---|---|
| Working folder | `~/Documents/Recipes/` |
| Collection data (533 posts with captions) | `source/instagram-food-collection.json` (+ `instagram-food-urls.txt`, `instagram-food-index.csv`) |
| Writing style | `styles/nigel-slater.md`. Read it fully before writing anything. |
| Per-post media | `media/<code>/` (layout below) |
| Media index | `media/INDEX.csv` |
| Pipeline state, scripts, vocab | `pipeline/` (`state.csv`, `collect.py`, `ingredients-vocab.txt`, archives) |
| Output notes | `~/Documents/Obsidian Vault/Me/Personal/Recipes/` |
| Vault images (small) | `~/Documents/Obsidian Vault/Me/Personal/Recipes/_thumbs/<code>.jpg` |

**Only write inside these two Recipes folders.** The rest of the vault is Craig's work, so don't read or touch it.

### Per-post folder: `media/<code>/`
| File | What |
|---|---|
| `video.mp4` | Reel at **720p max**, with metadata embedded (`--embed-metadata`: title, creator, description, URL) |
| `info.json` | yt-dlp metadata sidecar (creator name, date, location, music, etc.) |
| `audio.m4a` | extracted locally from the video with ffmpeg (`-vn -c:a copy`), **not** downloaded separately |
| `transcript.txt` | Raw `[start-end] text` lines, **never overwritten**. Whether it's real speech is judged by the model, not by length: Whisper transcribes song lyrics and invents filler ("You") on music. Record the verdict as `has_speech` in state.csv and the note. |
| `cover.jpg` | Instagram's cover image |
| `frames.jpg` | contact sheet, 1 frame per 2–4 s (for on-screen text) |
| `hero.jpg` | the best full-resolution frame of the **finished dish** (usually in the last 25% of the video). Choose it by looking at candidate frames. Fall back to the cover image if none shows the dish. |
| `comments.json` | only when the caption says the recipe is in the comments: the **creator's own** comments only |
| `web.md` + `web.json` | only when the caption or bio points to a website recipe: the page URL plus the recipe extracted from it (schema.org Recipe JSON-LD if present) |
| `carousel_01.jpg`… / `carousel_NN.mp4` | carousel posts only: every image **and** every video item |

Vault thumbnail: copy `hero.jpg` → `_thumbs/<code>.jpg`, shrunk with `sips -Z 720`.

Already done for 13 codes: audio and transcripts are in the old flat layout (`media/audio/<code>.*`, `media/transcripts/<code>.txt`). **Migrate them into `media/<code>/`** (rename to `audio.m4a`/`transcript.txt`; `C6_FrdiyZjh` is an `.mp4` with audio, so extract its audio track). Then delete the empty old folders and the `media/video` folder. These codes still need their video downloaded.

## Setup (done)
`.venv` contains yt-dlp, faster-whisper and requests. ffmpeg is at `/opt/homebrew/bin/ffmpeg`. Whisper `small` is cached. Disk: about 33 GB free; the full archive at 720p is about 3 GB.

## Instagram access: be polite, this is Craig's personal account
- Auth: `--cookies-from-browser chrome`.
- Video: `-f "bv*[height<=720]+ba/b[height<=720]/b" --merge-output-format mp4 --embed-metadata --write-info-json --write-thumbnail --convert-thumbnails jpg`, with output to `media/%(id)s/video.%(ext)s` (rename the sidecars to `info.json`/`cover.jpg`).
- Pacing: `--sleep-requests 3 --sleep-interval 20 --max-sleep-interval 60`, **at most 50 posts per run and 2 runs a day**, and `--download-archive pipeline/downloaded-video.txt`.
- **One Instagram media request per post.** Comments are an extra request, made only for posts that need them.
- On "rate-limit reached / login required" or HTTP 429: **stop at once** and tell Craig. Never retry in a loop.
- Creator comments: if yt-dlp can't limit them, use the logged-in web API once per post (headers: `X-IG-App-ID: 936619743392459`, `X-Requested-With: XMLHttpRequest`, `X-ASBD-ID: 129477`, `X-CSRFToken` from the cookie, Sec-Fetch same-origin/cors/empty). Keep only comments whose author is the post's creator.
- Websites: normal polite fetches (one page per recipe). Find the link in the caption, or in the creator's profile `external_url` (from `info.json` or one profile request), then find the matching recipe page. Never fetch paywalled content around a paywall. If it isn't found within about 3 fetches, skip it and note that.

## Lessons from the test batch (apply everywhere)
- **Only one `collect.py` process at a time.** Parallel runs overwrite each other's state.csv/INDEX.csv. Use `--reindex` if in doubt.
- **Pinned comments need up to 2 requests** (the first page doesn't include the pin). Allowed only for posts that say the method is in a pinned comment.
- **Seasonality calendar:** keep `pipeline/seasonality.csv` (`ingredient,peak_months`, e.g. `squash,9|10|11|12`; UK seasons; fish included). Add a row for each new name in `ingredients-vocab.txt`; use `all` for year-round staples (tofu, pasta, tinned goods). The app combines it with `served`, `heft`, `method` and `seasons` to order results by season (see the vault: `_design/Seasonal model.md`).
- **Staples:** `pipeline/staples.txt` lists ingredients assumed always in the house (salt, black pepper, olive oil, vegetable oil, water, plus anything Craig adds). Keep them in `ingredients_canonical`; the app ignores them when matching the pantry.
- **Regenerate the original 10 test notes** in the current format (grams, fan °C only, hob 1–9, contains_meat, swap notes, cuisine list). Keep their `id`s.

## Phases

### Phase 1: Triage. ✅ Done
`pipeline/state.csv`: 233 recipe_full · 84 recipe_partial · 179 recipe_spoken · 33 not_recipe · 4 carousel. Add columns as needed: `recipe_id, note_file, has_speech, web_url, needs_comments, video_ok, hero_ok`.

### Phase 2: Build `pipeline/collect.py` + test batch of 10 (Checkpoint 2)
`collect.py` takes a list of codes (or `--next N` from state.csv) and, for each post, does the following. **Every step skips work already done**, so it's safe to rerun.
1. Download the video and sidecars (as above) into `media/<code>/`.
2. Extract the audio, then transcribe it (faster-whisper `small`, `int8`, `vad_filter=True`, keep the source language).
3. Make `frames.jpg`, plus candidate hero frames (e.g. 6 frames from the last 25%) into `media/<code>/_candidates/`. Remove that folder once `hero.jpg` is chosen.
4. Carousel: save every image.
5. Update `state.csv` and `media/INDEX.csv`.

Then, as the model (not the script), for each post:
- Pick `hero.jpg` from the candidates.
- If the caption points elsewhere: get `comments.json` or `web.md/json`.
- **If there's no speech and the caption is incomplete, read `frames.jpg` for on-screen text.**
- Write the note (format below).

**Hero frames:** never choose a frame with burned-in caption or on-screen text when a clean frame of the dish exists. These images are shown full-screen.

**Test batch (10):** the cod (`C6_FrdiyZjh`), the Russian bake (`DVbI3SgDMBz`), the sukiyaki (`C4kZDKtBbQO`, silent with missing quantities), 2 `recipe_spoken` that point to a website, 1 "recipe in comments", 1 carousel, 1 other non-English post, and 2 more `recipe_spoken`.

**Checkpoint 2:** list the 10 notes and folders, total MB used, any Instagram warnings, and doubts. **Stop.**

### Phase 3: Full run (after Craig approves)
Craig, or a scheduled job, runs `collect.py --next 50` up to twice a day. Between runs, a Sonnet session writes the notes for the posts collected so far, in batches of about 25, using subagents (about 5 notes each) to parallelise. Skip `not_recipe` (keep them in state.csv). Merge duplicates into one note with several `sources`.

## Note format
Filename: `<Recipe title>.md` (UK title in title case; append ` (@creator)` only if needed to stay unique).

```markdown
---
id: fried-mushroom-pasta
title: Fried mushroom pasta
status: ok                    # ok | needs_checking
sources: [ig:DcBld-hI3ef]
source_url: https://www.instagram.com/p/DcBld-hI3ef/      # primary source
creator: "@helensplate"
creator_name: Helen's Plate
creator_url: https://www.instagram.com/helensplate/
web_recipe_url:               # if the creator's site had it
posted: 2026-08-14
media: "~/Documents/Recipes/media/DcBld-hI3ef/"
video_local: "file:///Users/craig/Documents/Recipes/media/DcBld-hI3ef/video.mp4"
thumbnail: "[[_thumbs/DcBld-hI3ef.jpg]]"
has_speech: true
servings: 3
prep_min: 25
cook_min: 15
total_min: 40
difficulty: easy              # easy | medium | involved
meal: [midweek dinner]        # breakfast | lunch | midweek dinner | fakeaway | baking | sides | dessert | snack | drinks | sauces & basics
cuisine: [italian]            # one or two of: british, irish, french, italian, spanish, portuguese, greek, turkish, middle-eastern, north-african, west-african, indian, sri-lankan, thai, vietnamese, chinese, japanese, korean, south-east-asian, mexican, latin-american, caribbean, american, scandinavian, eastern-european, russian, fusion. Leave it empty if unsure.
main_ingredient: [pasta, mushroom]
diet: [pescatarian, vegetarian]   # pescatarian | vegetarian | vegan | gluten-free | dairy-free. List every one that applies: vegan → also vegetarian + pescatarian; vegetarian → also pescatarian; fish/seafood with no meat → pescatarian. Meat (incl. meat stock, gelatine, lard) → none of the first three.
contains_meat: false          # true if any meat/poultry/meat stock. The household eats pescatarian; meat recipes are only for Craig alone.
allergens: [gluten, milk]     # UK 14: celery, gluten, crustaceans, eggs, fish, lupin, milk, molluscs, mustard, nuts, peanuts, sesame, soya, sulphites
equipment: [frying pan]       # oven, hob, frying pan, wok, casserole, blender, food processor, stand mixer, air fryer, slow cooker, grill, barbecue
spice: 0                      # 0 none · 1 mild · 2 medium · 3 hot
make_ahead: false
freezable: false
season: [all]                 # spring | summer | autumn | winter | all
occasion: [weeknight, cupboard]   # weeknight | cupboard | hosting | weekend project | batch cook | lunchbox | treat
larder: fresh                 # fresh | cupboard | mixed. fresh = relies on perishables (fish, tofu, fresh veg/herbs); cupboard = mostly store-cupboard (pasta, rice, tins, dried goods, frozen); mixed = in between. The fresh delivery arrives on Tuesday, so the app suggests fresh recipes early in the week and cupboard ones later.
perishables: [cod, bok choy]  # the fresh items to use first (fish and seafood before veg); empty for cupboard recipes
course: main                  # main | lunch | side | baking | breakfast | dessert | sauce. Only main and lunch appear in landing-page recommendations; the rest live in the library.
mood: [comforting, fresh]     # 1–3 of: comforting | light | fresh & green | spicy | something special | quick fix | warming | crunchy. How the dish FEELS to eat; powers "What do you feel like?" on the landing page.
served: hot                   # hot | warm | room temperature | cold
heft: medium                  # light | medium | hearty
method: [roast]               # 1–2 of: raw | quick | grill | barbecue | roast | braise | bake | soup | fry | steam
seasons: [autumn, winter]     # when it's at its best (ingredients and way of eating); [all] only if truly year-round
ingredients_canonical: [pasta, dried mushrooms, red onion, garlic, olive oil, butter, parmesan, lemon, salt]
tags: [one-pan]
sources_used: [caption, transcript, frames]    # + comments | web
original_language: en
style: nigel-slater
version: 1                    # v1 = as imported; later edits create v2, v3…
cooked_count: 0
rating:
added_by: Craig
added: 2026-10-04
---

# Fried mushroom pasta

<2–3 sentence intro in the house style>

## Ingredients
- 250 g dried pasta (shells or broken spaghetti)
- 40 g dried mushrooms
...

## Method
1. <step text> ⏱ 20 min · ▶ 0:14
   *Uses: dried mushrooms, hot water*
2. ...

## Notes
- <tips, swaps, what to serve with it, how it keeps>

## To check
- <every discrepancy between sources, every guess, every converted or estimated value>. Leave this section out if there's nothing to check.

## Source
Recipe by [Helen's Plate (@helensplate)](https://www.instagram.com/helensplate/) · [Original Reel](https://www.instagram.com/p/DcBld-hI3ef/)

> [!quote]- Original caption
> <verbatim caption>

> [!note]- Transcript
> <verbatim transcript with timestamps, or "(no speech)">
```

### Content rules
- **UK English and UK measures. Craig prefers grams.**
  - **Solids in grams, always,** including butter, sugar, flour, cheese, rice, pasta, nuts and chopped veg, even when the source uses tbsp or cups (1 tbsp butter ≈ 15 g, 1 cup grated parmesan ≈ 90 g, 1 cup rice ≈ 190 g, 9 oz → 250 g). For whole items, give a count plus an approximate weight: "2 onions (about 300 g)".
  - **Liquids in ml** (1 cup → 240 ml).
  - **tsp and tbsp only for small amounts** (under about 3 tbsp) of spices, seasoning, oils and sauces.
  - **No cups, oz, lb, °F, sticks or fl oz** anywhere outside the verbatim Source callouts.
  - **Oven: Craig has a fan oven, so give the fan temperature only:** `180°C fan` (conventional minus 20°C). No gas marks, no °F, no conventional temperature.
  - **UK names:** courgette, aubergine, coriander, double cream, plain flour, spring onion, prawns, minced beef.
- **Hob: Craig has an induction hob.**
  - The hob is a 1–9 induction. Give heat as the word followed by the hob setting: `low (2–3)`, `medium-low (4)`, `medium (5–6)`, `medium-high (7)`, `high (8–9)`. "Bring to the boil" can use `9`.
  - Rewrite gas-flame techniques (charring a pepper or tortilla over the flame, flame-toasting) as induction-friendly alternatives: under the grill, in a dry cast-iron pan, or with a blowtorch. Note the change under **To check**.
  - Woks: say "a flat-bottomed wok or large frying pan".
- **Source priority for facts:** creator's website recipe > caption > creator's comment > transcript > on-screen text. Use the lower sources to fill gaps and catch omissions. Record conflicts under **To check**.
- `ingredients_canonical`: lowercase base names with no quantities or prep. Reuse names from `pipeline/ingredients-vocab.txt` and add new ones there. This powers "what can we make", so consistency matters more than detail.
- **Step `Uses:` line:** the canonical names of the ingredients used in that step. Cook mode shows these on the step.
- Method: one action per step. Keep every quantity, temperature and time explicit, with a sensory cue. `⏱ N min` whenever a step has a duration; `▶ m:ss` from the transcript where the step starts (omit it if there's no speech).
- Controlled lists: use only the values listed in the frontmatter comments. If something doesn't fit, use `tags` and note it in the checkpoint report.
- **Never invent.** If a quantity is missing, write "a little" or "to taste", set `status: needs_checking` and add it under **To check**. Mark inferences (e.g. "looks like porcini") as guesses.
- Translate non-English recipes into UK English; keep the original caption verbatim in the Source callout.
- The style applies to the intro, step wording and notes, never to quantities or facts.
- **Household diet:** Craig and Mary eat pescatarian at home (Mary eats only fish and veg; Craig eats meat only when cooking for himself). For every `contains_meat: true` recipe, add a Notes line starting `Fish or veg swap:` when a sensible swap exists (e.g. chicken thighs → firm white fish or halloumi; beef mince → lentils or mushrooms; chicken stock → veg stock), and say honestly when none does. Keep the original recipe unchanged.

## Done means
Every recipe in state.csv has a note and a complete `media/<code>/` folder. `status` is honest, the controlled labels are valid, `ingredients_canonical` uses the shared vocabulary, `media/INDEX.csv` is complete, and Craig has approved the test batch.
