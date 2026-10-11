# Recipe app: project state (2026-10-04, late evening)

Read this first when resuming. The detailed specs live in the files linked below.

## Live links (private; share from each page's Share menu)
- **Prototype (landing option 3, working, 37 recipes, cook-log story with sounds):** https://claude.ai/artifact/JcpCJraUNC6XwXGvypqNUB (source: scratchpad `proto/template.html` → `supper-test.html`; rebuild by injecting `recipes.json` and the sound block from `app/wireframes/cook-log-play.html`)
- **Cook-log story with sounds (standalone):** https://claude.ai/artifact/QuC4Be2mM5beGn7kvpnVds
- **Interactive wireframe prototype (whole flow, neutral greyscale, 37 recipes):** https://claude.ai/artifact/HTvBwLLpzusThwoJyb27Vg (source: `app/wireframes/flow-proto/`, run `python3 build.py` there; images from scratchpad `proto2/img`)
- **Neutral wireframe flow (whole app, nav, Kitchen/ingredients, 14 screens):** https://claude.ai/artifact/BB3JuqzfffZvcSHnAwsWz4 (source: `app/wireframes/flow.html`). Craig: wireframes lock behaviour and placement; visual design must not move them.
- **Round 3, four wider routes (Cinema · Instrument · Counter evolved · Editorial):** https://claude.ai/artifact/E2t7UGqjj97JMbh4Ye3eot (sources: `app/routes3/`; publish copy with images in scratchpad `r3pub/`)
- **Round 2 options A/B/C:** https://claude.ai/artifact/CmU7nf8jPFLnFeYUTAC2bD (sources: `app/routes2/`)

## Local files
- `HANDOVER.md`: the Sonnet pipeline spec (labels, units, IDs, Instagram pacing)
- `pipeline/state.csv`, `collect.py`, `seasonality.csv`, `ingredients-vocab.txt`, `staples.txt`, `batch2-codes.txt`
- `media/<code>/`: video, audio, transcript, cover, hero, frames
- `app/`: test app (`index.html`, `build_data.py`), `wireframes/` (landing options, landing-v3, cook-log, cook-log-play, architecture, features), `routes/` (round 1: six routes), `routes2/` (round 2: A/B/C + BRIEF.md)
- Vault `Me/Personal/Recipes/`: 37 recipe notes, `_thumbs/`, `_design/` (board canvas, refs, Round 1 feedback, Seasonal model)
- `intake/`: placeholder for the box email, receipts and photos

## Data status
- 533 saved posts listed and sorted. **37 recipes written** (7 ok, 30 needs checking).
- **13 posts from batch 2 still to collect.** Run `collect.py` on the batch2 codes with no `media/<code>/video.mp4` (at most 2 runs a day). Then about 450 more in total.
- The collector's false "429" stop is fixed. yt-dlp is installed via Homebrew (`/opt/homebrew/bin/yt-dlp`, 2026.08), and is newer than the venv's.
- The kabocha soup hero has been replaced. A few heroes still have small burned-in captions; re-pick them in the full run.

## Household (also in memory)
Craig and Mary · pescatarian together, Craig eats meat alone · fan oven · 1–9 induction · grams · fresh box on Tuesday (fresh first Tue–Thu, cupboard Sun–Mon) · Nigel Slater-style voice · season ordering as a gentle nudge, blended by month.

## Design verdicts
- **Round 1:** 4 Counter strongest (colours, hidden filters, speed suggestions, shortlist) · 1 Index (typography, bottom search bar, step by step, atmosphere → focus transition) · 5 Reel (type, full-screen video and image) · 2 Cookbook mostly no (kept: meta line, meal times) · **3 Kitchen drawer and 6 Poster eliminated**.
- **Rules:** function first · images and video essential · no divider lines · no boxes inside boxes · vary the spacing · fine type, not bold · no dashed lines · design for long names · dark by default (no glare).
- **Decided:**
  - **Landing option 3:** a quiet header (day, plus season and rhythm). The diner is shown only as a chip when it isn't the default.
  - **Feel like** is a single choice. **With** (ingredients) is multi-select.
  - **"For tonight"** is a swipe row with 3+ visible. Mood and ingredients affect only this row. Below it: In season · Quick tonight · Our list · Something different, as open discovery.
  - The bottom bar has search plus the filter sheet (= the library).
  - **Cook-log story** (fill in the blanks, game-style sounds) creates the next version.
- **Round 2 A/B/C:** judged too close (over-constrained brief). Proposed wider round: **Cinema · Instrument · Editorial paper** (+ optional Kitchen colour), varying colour, type, images and structure together. **Round 3 published (2026-10-04), awaiting Craig's pick:** `app/routes3/` (BRIEF.md + 1-cinema, 2-instrument, 3-counter, 4-editorial; landing · recipe · cook mode each).

## Persona test (5 simulated testers): fixed in the prototype
44px targets, multi-select With, removable chips, named empty states, visible times ("about 1 hr 22 min incl. 1 hr waiting"), one clear "Add to our list" + ♡, cook-mode timers with "while you wait", joined Back/Next, story asks who cooked, focus handling, light-mode contrast.

## Prototype feedback, round 1 (2026-10-05, built in v2 of the interactive prototype)
- **Want to try vs Favourites** are separate: "Ours" tab with two views. Want to try is a queue that empties as we cook. Favourites are ♥ go-tos that come back round when not made for a while.
- **Feel like:** exploring one vs several (switch next to the label; several = match any, more matches first).
- **Who's cooking:** Craig / Mary / Together. Per-person likes give "made your way" tweaks. Together splits the steps (heat vs prep) with a "Meanwhile" card. Open: one phone or two, fixed split or rebalance.
- **Hands-on vs Ready in** shown separately (estimated from the steps). New sections: "On the table in 30" and "Little effort, then wait".
- **In season** is ordered by how much we have in the Kitchen.

## Decided 2026-10-06 (Craig: "rest on the recipe app sounds good")
- **Navigation:** four tabs (Tonight · Ours · Kitchen · Log), search above the tabs on Tonight; recipe → cook → story is a focused flow without tabs.
- **Kitchen** tracks have / running low / out, with staples assumed and no quantities.
- **Box:** a manual Tuesday prompt now; the Abel & Cole email later.
- **Add a recipe** lives on Ours (plus the share sheet).
- **Cooking together:** one phone, rebalance as you go, split by station (Prep board · Hob · Oven · Finish together). Built in prototype v3: two lanes, Give to ⇄, Take over.
- Still open: shopping list in v1; Feel like one vs several (testing both).

## Open questions
Shopping list in v1? · app name · home machine (Mac mini / NAS / Pi) · Figma team for the design system · the Abel & Cole inbox (a personal address, not connected).

## Next steps
1. Craig settles the wireframe decisions (nav model, Kitchen tracking, shopping list v1, box, where Add a recipe lives) → lock the flow.
2. Then visual routes (round 3, `app/routes3/`) are dressed onto the locked flow. Craig reviews round 3 (four wider routes, `app/routes3/`) → pick or mix.
2. Kitchen test with Mary using the prototype.
3. Collect the remaining 13, then the full run (Sonnet notes, data-file master copy).
4. Lock the direction → Figma design system → real build on a home server (Postgres, PWA, Tailscale).
