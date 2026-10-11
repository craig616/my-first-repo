# Recipe App: project handover

A private, mobile-first recipe app for two people that turns saved Instagram recipe Reels into a shared cookbook. It covers searching, "what can we make with what's in?", step-by-step cook mode, and improving recipes after cooking them.

**Conventions:** UK English, metric units (g, ml, °C plus gas mark) and UK ingredient names (courgette, aubergine, coriander, double cream).

## What's in this folder

| File | What it is |
|---|---|
| `DESIGN-BRIEF.md` | Full product and design brief: features, screens, data model, design principles, constraints, open questions |
| `wireframes/` | Source of the 10-screen clickable wireframe prototype (see below) |

## The wireframes

Built as a Claude design canvas (`.dc.html` files plus `canvas.json`). They depend on the canvas runtime (`support.js`), so **they won't open as normal web pages straight from GitHub**. They're here so a future session can read, edit or rebuild them.

The live, clickable version is a private claude.ai artifact on Craig's work account. It only opens for accounts it has been shared with.

Screens (390 × 844, phone):
1. `Main` – Library: search, category chips, recipe cards with pantry match ("Have 9/10")
2. `Recipe` – Reel embed, servings scaler, ingredients marked have/missing, method steps with video timestamps, version tag
3. `Cook` – Cook mode: dark, one step at a time, live countdown timer, big Back/Next buttons
4. `Log` – After cooking: rating, cook again?, quick tags, notes, "edit recipe" to create a new version
5. `Versions` – Recipe history (v3, v2, original) and cook log
6. `Filters` – Meal, main ingredient, cuisine, diet, time, favourites
7. `Pantry` – What's in: fridge, cupboard and freezer lists with add, remove and quick-add
8. `PantryResults` – What can we make: ready now, plus missing 1–2 with swaps and a shopping list
9. `AddRecipe` – Paste text or a link, upload a screen recording, or bulk-import an export
10. `NeedsCheck` – Recipe from a video with missing amounts to fill in

The recipe content in the wireframes (miso aubergine etc.) is example content only.

## Decisions and findings so far

- **Getting recipes out of Instagram:** Claude's cloud sessions on the work account blocked `instagram.com` through the environment's network setting. Even when allowed, Instagram often blocks cloud servers. Don't rely on Claude downloading Reels.
- **Workable routes, in order of preference:**
  1. The caption contains the recipe → parse it.
  2. The creator's website has a written recipe → fetch it.
  3. Video only → screen-record the Reel and upload it. Claude transcribes the audio (Whisper) and reads frames (ffmpeg). Both tools are available in the cloud container.
  4. Still unclear → mark as "needs checking", never guess quantities.
- **Bulk import:** use a phone app that reads Reel videos, then export and bring the results in. Candidates: Deglaze, SousChef AI (5 free imports a month), ReciMe (5 free a week; $39.99 a year with a 7-day trial), Wecipe, Pullit. Not yet tested. **Check the app can export** before relying on it.
- **Video in the app:** an Instagram embed can't jump to timestamps. Linking steps to video moments needs our own uploaded clip.

## Next steps

1. Test Deglaze and SousChef AI on the same Reel (e.g. `https://www.instagram.com/reel/Dd84FlQRp6g/`) and compare accuracy.
2. Get feedback on the wireframes (screens to add or cut, flow changes, partner's name instead of "[Partner]").
3. Build the real app: shared storage for the two users, pantry matching, cook mode, recipe versions and cook log.
4. Bulk-import the saved recipe collection.
