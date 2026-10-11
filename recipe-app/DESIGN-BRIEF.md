# Handover: Shared Recipe App (design brief)

## 1. What we're building
A private, mobile-first recipe app for two people (me and my partner) that turns our saved Instagram recipe Reels into a shared, searchable cookbook we can actually cook from, and that gets better each time we cook something.

Audience: UK household. Use UK English, metric units (g, ml, °C plus gas mark) and UK ingredient names (courgette, aubergine, coriander, double cream, plain flour).

## 2. The problem
- We have hundreds of saved Instagram recipes that are impossible to search or cook from.
- Many Reels only *say* the recipe out loud, with nothing written in the caption.
- There's no way to say "what can we make with what's in the fridge?"
- When we tweak a recipe ("needed more garlic"), the change is lost.

## 3. How recipes get in (context, not something to design)
1. A third-party import app (being tested: Deglaze, SousChef AI) pulls the recipe out of each Reel from Instagram's share menu, including spoken and on-screen content.
2. We export the results from that app.
3. Claude cleans them up (UK units, tags, categories) and loads them into this app.
4. Each recipe keeps a link back to the original Reel.

Design needs: an **"Add recipe"** route (paste text, a link or a screenshot) and a **"Needs checking"** state for recipes with missing quantities or steps.

## 4. Core features and screens

### a) Library / Discover (home)
- Search across names, ingredients and tags.
- Filter chips: meal (breakfast, midweek dinner, fakeaway, baking, sides), main ingredient, cuisine, diet (veggie, vegan, gluten-free), time (under 15, 30 or 60 minutes), rating, "not cooked yet".
- Recipe cards: image or video thumbnail, title, time, a "you have 8/10 ingredients" badge, star rating, and who added it.
- Sorting: recently added, most cooked, best rated, best match to our pantry.

### b) Pantry: "What can we make?"
- A quick-add list of what we have (fridge, cupboard, freezer), with common staples as one-tap chips.
- Results ranked by match: "Ready to cook" (everything in), "Missing 1–2" (shows what's missing, plus suggested swaps).
- Missing items can go on a shopping list.

### c) Recipe detail
- Hero area with the embedded Instagram Reel, or our own uploaded clip. Fallback: thumbnail and a "Watch on Instagram" button.
- A servings scaler that adjusts every quantity.
- Ingredients with pantry status (have / don't have).
- Numbered method steps. If we hold our own copy of the video, each step has a "▶ 1:42" link that jumps to that moment.
- Version history and notes: "Our version (v3)" versus "Original", with a change log.
- Source credit (creator's handle and a link to the original post).

### d) Cook mode (the most important screen)
- One step at a time, with very large type that's readable from arm's length.
- The screen stays on (wake lock).
- Big tap targets for next and back, usable with messy hands. Swipe as well.
- Inline timers that start from the step text (e.g. "simmer 10 minutes"), with several timers able to run at once and stay visible.
- Ingredients for the current step appear on the step itself.
- Optional extra: hands-free "next step" by voice.

### e) After cooking: log and adjust
- A prompt when cook mode finishes: a rating (1–5), "Would cook again?", and quick tags (too salty, too spicy, needed longer, great as is).
- Free-text notes, plus "Adjust recipe": edit quantities, steps or timing.
- Saving creates a new version. We cook from the latest version, but the original is always viewable.
- A cook log: date cooked, who cooked it, rating, notes.

### f) Shared use
- Two users on the same collection, with "added by" and "cooked by" shown.
- Notes are visible to both of us.
- Optional: favourites per person ("Craig's favourites", "Partner's favourites").

## 5. Data model (for reference)
- **Recipe:** id, title, source_url, creator_handle, video (embed or upload), image, servings, prep_time, cook_time, tags[], categories[], status (ok / needs_checking), current_version
- **Ingredient:** name (UK), quantity, unit, prep note ("finely chopped"), optional (yes/no)
- **Step:** order, text, timer_seconds (optional), video_timestamp (optional), ingredient_refs[]
- **Version:** number, changes, author, date
- **CookLog:** date, cook, rating, tags[], notes
- **PantryItem:** name, location (fridge/cupboard/freezer), added_by

## 6. Design principles
- **Mobile first:** used on a phone propped up in the kitchen.
- **Low friction:** opening the app to cooking should take at most two taps.
- **Readable in the kitchen:** strong contrast and big type in cook mode, with dark mode.
- **Accessible:** must work without sound (captions and written steps are the primary content; video is secondary).
- **Warm and homely, not clinical:** a family cookbook feel rather than a fitness app.

## 7. Known constraints
- Instagram's embed player can't jump to a timestamp. Step timestamps only work with our own uploaded clip.
- Some recipes will arrive incomplete, so "needs checking" needs a clear but non-alarming visual state.
- No accounts or passwords beyond us two. It's a private app, shared by link.

## 8. Deliverables wanted from Figma
1. Mobile frames (390 × 844): Library, Filters, Pantry, Pantry results, Recipe detail, Cook mode (step plus active timers), After-cook log, Version history, Add recipe, Needs-checking state.
2. Light and dark versions of cook mode as a minimum.
3. A small component set: recipe card, filter chip, ingredient row (have/missing), step card, timer, rating input.
4. A simple prototype flow: Library → Recipe → Cook mode → After-cook log → updated recipe (v2).

## 9. Open questions
- Which import app wins the accuracy test (Deglaze or SousChef AI)?
- Do we want a shopping list in version 1, or later?
- Per-person favourites: yes or no?
- App name: to be decided.
