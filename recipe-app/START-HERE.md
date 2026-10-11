# START HERE: Recipe app

Read this first. It explains what this folder is, what's already done, what's still missing, and how to pick the project up from a new Claude session (phone, or a different account).

## What this project is

A private, mobile-first recipe app for two people (Craig and Mary). It turns saved Instagram recipe Reels into a shared cookbook that can:

- search and filter recipes
- say what you can cook from what's in the fridge, cupboard and freezer
- walk you through a recipe step by step in cook mode, with timers
- log how each cook went and create a new version of the recipe when you change it

**Conventions:** UK English. Metric units (g, ml, °C, gas mark). UK ingredient names (courgette, aubergine, coriander, double cream, plain flour). Money in pounds sterling.

## The current design

The working design is the **Supper wireframe prototype**: four tabs (Tonight · Ours · Kitchen · Log), 37 of our recipes, cook mode with timers, cooking together, and the cook-log story. It locks behaviour and placement, not looks (deliberately greyscale).

- **Ready-built copy:** `exports/supper-prototype/` (`index.html` plus `img/`). Publish this folder as an artifact to test it.
- **Source:** `app/wireframes/flow-proto/`. Run `python3 build.py` there to rebuild it from `template.html`, `recipes.json` and `sound.js`. The images are the ones in `exports/supper-prototype/img/`.
- **Published copies** are private and tied to the account that published them. `PROJECT-STATE.md` lists the work-account links. A copy published on 2026-10-11 from a separate session (opens only for the account that published it, unless shared): https://claude.ai/artifact/4gzhZYgRUdsFpbFJnd99V1

The 10-screen wireframe in `wireframes/` is the **first round** and is superseded. Keep it for reference only.

## Where things are

| Path | What it is |
|---|---|
| `START-HERE.md` | This file |
| `PROJECT-STATE.md` | **Source of truth for progress and decisions.** Read this before doing anything else. |
| `README.md` | Earlier handover notes and decisions |
| `DESIGN-BRIEF.md` | Full product and design brief: features, screens, data model, open questions |
| `HANDOVER.md` | Earlier handover from the build work (pipeline spec: labels, units, IDs, Instagram pacing) |
| `INSTAGRAM-EXTRACTION-HANDOFF.md` | How recipes are pulled out of Instagram and what's been tried |
| `exports/` | The ready-built Supper prototype (`supper-prototype/`) and the "Recipe app – where everything lives" diagrams (PDF and PNG, desktop and phone) |
| `app/wireframes/` | Current wireframe work: `flow-proto/` (Supper prototype source), `flow.html` (whole-app flow), landing options, cook log, architecture and features |
| `app/` | Test app (`index.html`, `build_data.py`, `recipes.js`) and the visual design rounds: `routes/` (round 1), `routes2/` (round 2), `routes3/` (round 3, awaiting Craig's pick) |
| `wireframes/` | First-round 10-screen wireframe (`.dc.html` files plus `canvas.json`). Superseded. |
| `pipeline/` | Scripts and logs for collecting and processing the saved recipes (`collect.py`, batch logs, ingredient vocabulary, staples, seasonality) |
| `source/` | Raw data: the Instagram food collection (`instagram-food-collection.json`), the URL index and the URL list |
| `intake/` | Plan for the "what's in the house" feed (box email, receipts, photos). Placeholder only. |
| `styles/` | Writing and style guides, e.g. `nigel-slater.md` |
| `media/` | Screen recordings and videos. **Not in Git yet, see below.** |

## What's done

- Design brief, first-round wireframe, and three rounds of visual routes (see `PROJECT-STATE.md` for the verdicts)
- The Supper wireframe prototype, with 37 recipes written up (7 ok, 30 needs checking)
- Build files, pipeline scripts, source data, style notes, `exports/` and `intake/` (uploaded from Craig's Mac in the `Recipes` folder)
- Git LFS set up on Craig's Mac for the `media/` folder

## What's still missing

1. **The videos (`media/`).** They aren't in the repository yet. Craig is adding them with Git LFS from his Mac. Check `git lfs ls-files` in this folder: if it lists files under `recipe-app/media/`, they're in.
   - As of 2026-10-11 the repository has **no `.gitattributes` file**, so nothing is tracked by LFS here. Commit one (e.g. `git lfs track "recipe-app/media/**"`) **before** adding the videos, or they'll be pushed as ordinary files.
2. **Import apps.** Deglaze, SousChef AI and ReciMe were shortlisted to turn Reel videos into recipes. None has been tested yet. Ask Craig which one he tried, and whether the results can be exported.
3. **The remaining recipes.** 13 posts from batch 2 still to collect, then about 450 more (see `PROJECT-STATE.md`).
4. **The real app.** Shared storage for the two users, pantry matching, cook mode, versions and the cook log are all still to be built.

## Things that will block you

- **Instagram is blocked from Claude's cloud sessions.** Don't try to download Reels from Instagram links. Ask for a screen recording of the Reel, or use an import app on the phone.
- **Don't use Craig's Instagram login** to get around anything. It risks his account.
- **Figma isn't connected** in the work account, so the wireframes can't be edited in Figma directly. Edit the HTML files here instead.
- **Scratchpad paths in `PROJECT-STATE.md`** (e.g. `proto/`, `proto2/img`, `r3pub/`) were on an earlier session's machine and won't exist in a new session. Use the copies in this repository instead.
- **Artifact links are per account.** Links in `PROJECT-STATE.md` only open on the work account (or for people they've been shared with).

## How to recipe-process a new recipe

1. If the recipe is in the caption, copy it in as text.
2. If the creator has a website with the recipe, use that.
3. If it's only in a video, ask for a screen recording of the Reel and read it from the transcript and on-screen text.
4. If anything is unclear (missing amounts, vague steps like "a splash of soy"), mark the recipe **Needs checking**. Never guess quantities.

Always convert to UK units and names.

## Picking this up from a new session

1. Open `PROJECT-STATE.md` and check the latest status.
2. Run `git status` and `git lfs ls-files | head` to see what's in the repository.
3. Ask Craig before changing anything he's already done. He works on the Mac copy too.
4. Make small commits on branch `ccr-b14c4929-8vt823`. Don't open pull requests unless Craig asks.
5. Don't include model names in commit messages.

## Questions to ask Craig

- Which import app did you test, and did it export?
- Is the `media/` folder in Git LFS yet? (Add `.gitattributes` first, see above.)
- Which round 3 route (`app/routes3/`) do you want, or which mix?
- Is the first-round `wireframes/` folder still needed, or can it be archived?
