# START HERE: Recipe app

Read this first. It explains what this folder is, what's already done, what's still missing, and how to pick the project up from a new Claude session (phone, or a different account).

## What this project is

A private, mobile-first recipe app for two people (Craig and his partner). It turns saved Instagram recipe Reels into a shared cookbook that can:

- search and filter recipes
- say what you can cook from what's in the fridge, cupboard and freezer
- walk you through a recipe step by step in cook mode, with timers
- log how each cook went and create a new version of the recipe when you change it

**Conventions:** UK English. Metric units (g, ml, °C, gas mark). UK ingredient names (courgette, aubergine, coriander, double cream, plain flour). Money in pounds sterling.

## Where things are

| Path | What it is |
|---|---|
| `START-HERE.md` | This file |
| `README.md` | Earlier handover notes and decisions |
| `DESIGN-BRIEF.md` | Full product and design brief: features, screens, data model, open questions |
| `PROJECT-STATE.md` | **Source of truth for progress.** Read this before doing anything else. |
| `HANDOVER.md` | Earlier handover from the build work |
| `INSTAGRAM-EXTRACTION-HANDOFF.md` | How recipes are pulled out of Instagram and what's been tried |
| `wireframes/` | Source for the 10-screen clickable prototype (`.dc.html` files plus `canvas.json`) |
| `app/` | The app build, including `app/index.html`, `app/build_data.py`, the `routes/`, `routes2/` and `routes3/` design explorations, and `app/wireframes/` |
| `pipeline/` | Scripts and logs for collecting and processing the saved recipes (`collect.py`, batch logs, ingredient vocabulary, staples list) |
| `source/` | Raw data: the Instagram food collection (`instagram-food-collection.json`), the URL index and the URL list |
| `styles/` | Writing and style guides, e.g. `nigel-slater.md` |
| `media/` | Screen recordings and videos. **Not in Git yet, see below.** |

## What's done

- Design brief and 10-screen wireframe prototype (`wireframes/`)
- Build files, pipeline scripts, source data and style notes (uploaded from Craig's Mac in the `Recipes` folder)
- Git LFS set up on Craig's Mac for the `media/` folder

## What's still missing

1. **The videos (`media/`).** They're too big for chat uploads and aren't in the repository yet. Craig is adding them with Git LFS from his Mac. Check `git lfs ls-files` in this folder: if it lists files under `recipe-app/media/`, they're in. If not, they still need adding.
2. **The `exports/` and `intake/` folders** from Craig's `Recipes` folder. They weren't in the archive. Ask him to add them.
3. **Import apps.** Deglaze, SousChef AI and ReciMe were shortlisted to turn Reel videos into recipes. None has been tested yet. Ask Craig which one he tried, and whether the results can be exported.
4. **The real app.** Shared storage for the two users, pantry matching, cook mode, versions and the cook log are all still to be built.

## Things that will block you

- **Instagram is blocked from Claude's cloud sessions.** Don't try to download Reels from Instagram links. Ask for a screen recording of the Reel, or use an import app on the phone.
- **Don't use Craig's Instagram login** to get around anything. It risks his account.
- **Figma isn't connected** in the work account, so the wireframes can't be edited in Figma directly. Edit the `.dc.html` files here instead.

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
- Do you have the `exports/` and `intake/` folders? Can you add them?
- Is the `media/` folder in Git LFS yet?
- Who is the second user, and what's their name to use in place of "[Partner]"?
