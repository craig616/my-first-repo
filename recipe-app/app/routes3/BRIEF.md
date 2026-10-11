# Round 3: four wider routes

Round 2 (A/B/C) was too close: those options only changed image size, title font and separators. In round 3, each route makes its **own decisions together**: colour, typeface, how images behave, and the **structure** of the landing page. Every route builds on Craig's round 1 feedback (`Me/Personal/Recipes/_design/Round 1 feedback.md` in the vault). If you put the four side by side, someone should be able to tell them apart from across the room.

## The product (short)
Craig and Mary's private recipe app. About 500 recipes saved from Instagram Reels, each with a video, a dish photo, ingredients and a timed method. The household is pescatarian; Craig eats meat only when cooking alone. UK English, grams, "180°C fan", induction hob 1–9. The voice is quiet, like Nigel Slater. No emoji, calories, scores or streaks.

It gets used three ways:
- on the sofa, choosing
- one-handed at the fridge
- propped up while cooking

## What every route must contain (the functions; the form is free)
1. **Landing:**
   - a quiet context line: "Tuesday evening · mid autumn · the box is in" (never "for both of us")
   - **Feel like:** a single choice from comforting, light, quick, something new, for a crowd. "light" is selected.
   - **With:** ingredients, multi-select. Cod and spinach are selected and shown as removable chips.
   - **For tonight:** at least 3 suggestions visible, each with a time and a short reason line
   - **discovery below:** at least two of In season · Quick tonight · Our list (the shared shortlist/queue) · Something different
   - **search and filters** reachable at the bottom with the thumb
   - The route may express these in its own way (a pager, a timeline, a queue, an issue), but they must all be there and usable.
2. **Recipe: *Japanese mirin baked cod*** by Lisa @thelisafeed
   - video or photo, and the meta line "Fish · Japanese · weeknight"
   - "Takes about 1 hr 22 min (incl. 1 hr marinating)" and "Serves: not given"
   - **one** clear primary action, "+ Add to our list", plus ♡ and "Watch the Reel"
   - ingredients (grams), the start of the method
   - "Start cooking" pinned at the bottom
3. **Cook mode:** the *transition from atmosphere to focus*. It should feel like a change of room from the landing page.
   - step 2 of 7: "Turn the cod in the marinade so every side is coated, then cover and leave to marinate for at least 1 hour (the fridge is the safe place)."
   - a 60 min timer running at **52:14**, always visible
   - "For this step: cod"
   - "While you wait: heat the oven to 180°C fan near the end."
   - the next step previewed (opacity at least 0.6): "Line a tray with baking paper and lay the cod skin-side down."
   - Back | Next joined together, at least 64px tall

### Recipe data to use
**Ingredients:**
- 4 cod fillets (about 500 g)
- 3 tbsp mirin
- 2 tbsp soy sauce
- 1 tbsp sake
- 1 tbsp sugar
- 1 tsp grated ginger
- spring onion to finish
- steamed rice to serve

**Method, step 1:** "Mix the mirin, soy, sake, sugar and ginger in a shallow dish until the sugar dissolves."

**Landing suggestions** (images at `../../media/<code>/hero.jpg`; all heroes are portrait, 9:16):

| code | dish | time | reason line |
|---|---|---|---|
| C6_FrdiyZjh | Japanese mirin baked cod | 1 hr 22 min (mostly waiting) | on our list · uses the cod |
| DVbnwhjiExJ | Cod grenobloise | 25 min | light · uses the cod |
| C8kHapDNLG3 | Creamy pesto orzo with crispy salmon | 30 min | uses the spinach |
| Cyf04RxIO8c | Roast sweet potatoes with spinach and cannellini cream | 50 min | in season · uses the spinach |
| DPB6Q6SjBh5 | Cod with mustard sauce in paper boats | 35 min | | 

**In season:**
- CwiWc2KId6o: Late summer minestrone with fennel
- DDAItEoo_vi: Creamy kabocha pumpkin soup (the hero is landscape)

**Other options:**
- DG004YSIeMK: Creamy mushroom and miso pasta, 20 min
- DR8J3_njn8m: Hoisin garlic noodles, 15 min
- DT5nuU5iPAH: Tofu dan dan noodles, 25 min
- Cy2_tQfsh6_: Charred hispi cabbage with whipped miso tofu, 40 min
- DH4caL3y_uD: Chilli peanut crispy rice salad with honey soy salmon, 35 min (a long name: design for it)

**Ingredient photos:**
- cod `C6_FrdiyZjh`
- salmon `C8kHapDNLG3`
- tofu `DT5nuU5iPAH`
- eggs `DIJpP8hKBoA`
- spinach `Cyf04RxIO8c`
- cabbage `Cy2_tQfsh6_`

**Video:** `../../media/C6_FrdiyZjh/video.mp4`, as `<video muted playsinline poster=…>`. Autoplay and loop are fine in Cinema.

## Craig's rules (hard)
- Function first; no aesthetic in the way.
- Images and video are essential.
- **No divider lines** (no borders, no `<hr>`); type and space separate things.
- **No boxes inside boxes.** Avoid repeated rounded cards; vary the corners and the spacing to create rhythm.
- **Fine type, never bold.** Weights 200–400; 500 at most for tiny labels.
- No dashed lines; nothing poster-bold.
- Design for long recipe names.
- Dark, no glare.
- Never use the word "Saffron" anywhere; the highlight colour is called "yolk".
- 44px minimum targets.

## The four routes

### 1 · Cinema (from 5 Reel + B's full-screen; Apple News focused steps)
**The food moves.** A black screen, and the Reels are the interface.
- **Landing:** a full-height vertical pager, like Reels. The For tonight pick fills the screen as an image or video, with the title in large fine type at the bottom over a soft scrim, the time and reason line, and a peek of the next card's edge. Make it read as "1 of 5 for tonight", for example with a filmstrip of 3+ small frames along the bottom so at least 3 suggestions are visible. Feel like and With float as a translucent strip at the top. Discovery sits below the fold, but draw its first row (big full-bleed tiles, no rounded boxes).
- **Recipe:** the video plays full-screen. Its steps are captions synced to the video's ▶ timestamps. Ingredients come from a sheet that pulls up (a single surface).
- **Cook mode:** the step's video loops behind, blurred and very dark; the step text is very large; the timer is a thin progress line along the top edge plus large numerals.
- **Look:** pure black `#000` and warm white `#f3ece4`; yolk `#f2c75c` only for the single key action. Type: **Jost 200/300**, large, with tight tracking on titles. Corners: 0 on images, a pill only on the one primary button.

### 2 · Instrument (from 1 Index: typography, step by step, bottom search)
**A precise kitchen tool.** Typographic, tabular and calm, like a good Braun clock or a train departure board, but quiet.
- **Landing:** the For tonight suggestions are laid out as a **timeline by "ready by" time**. If you start now (18:40), dinner is ready at 19:00 · 19:05 · 19:10 · 19:30 · 20:02. Each row has a big tabular time, the name (wrapping), the reason, and a small square thumbnail on the right. Feel like is a segmented text row; With is a line of text chips ("cod ×", "spinach ×"). Discovery sits below as compact indexed lists ("In season — 12", "Our list — 4") rather than images. The bottom bar is a full-width search field with a filter glyph.
- **Recipe:** a narrow photo/video band at the top (16:9), then a strict grid: quantities in a right-aligned tabular column, steps numbered in a hanging margin, and the time broken into a small horizontal time bar (prep / marinate / bake) drawn as segments, not lines.
- **Cook mode:** a big countdown in tabular numerals as the hero. The step text is beneath it, in large type. The remaining steps are shown as a numbered progress index.
- **Look:** graphite `#141516`, ink `#e8e6e1`, secondary `#8d8f91`; yolk only for the running timer and the primary action. Type: **IBM Plex Sans 300/400 + IBM Plex Mono 300** for numbers, times and quantities. Square corners throughout (0–2px). Generous, *uneven* spacing: tight within groups, wide between them.

### 3 · Counter, evolved (from 4 Counter, the strongest: colours, hidden filters, speed, shortlist)
**The kitchen itself:** walnut, plaster and lamp light. Warm and sociable, organised around **Our list**, the shared queue.
- **Landing:** **Our list** sits at the top as a stacked queue ("Next up: Japanese mirin baked cod, added by Mary on Sunday"), plus 2 more peeking, reorderable. Then For tonight as a horizontal swipe row of portrait images, grouped **by speed** under quiet headings ("Under 20 minutes", "About half an hour", "Worth the wait"), with 3+ visible. Feel like/With are a single quiet line that expands; the filters stay hidden behind the bottom bar. Use **meals by time of day** as one discovery shelf ("Slow Sunday breakfast", "Weeknight supper").
- **Recipe:** a large hero photo with a soft gradient into walnut. Who added it to the list and when ("Mary added this on Sunday"). The ingredients sit on a plaster-toned surface: **one** surface, not cards.
- **Cook mode:** the lamp turns off. The walnut fades to near-black with a single warm pool of light (a radial gradient) behind the step; the timer reads like a kitchen timer.
- **Look:** walnut `#17100c`, surface `#231812`, plaster `#d9cbb8` (used as a *field* behind one section, with walnut text on it), brass `#d4a463`, yolk `#f2c75c` for the single key thing. Type: **Jost 300/400**. Mixed corners: images 2px, the queue sheet 22px at the top only. **Deliberately varied spacing.**

### 4 · Editorial (Hers type, Creme, Apple News, the meta line, meals by time of day)
**This week's issue.** A dark, matte magazine that changes with the week's rhythm: the box arrives on Tuesday, fresh things come first, cupboard cooking later in the week.
- **Landing:** reads like the cover of an issue: "Week 41 · the box is in". The For tonight lead is a big editorial spread: an image across the full width, a **large, light, high-contrast serif headline** (Fraunces or Newsreader, 200–300) and a standfirst sentence in the Nigel voice ("The cod wants an hour in the mirin, so start it now and the rice can wait."). Two or three more picks follow as a typographic list with small images. **Sections by time of day and type of meal** ("Tonight's supper", "For the weekend", "Something sweet") with the meta line "Fish · Japanese · weeknight" in small caps. Feel like and With are a sentence: "Something **light** with **cod** and **spinach**", where each underlined word is tappable.
- **Recipe:** a magazine article. A full-bleed opening image, a serif headline, a standfirst, the byline "From Lisa @thelisafeed", ingredients in a narrow side column (mimic the column on a phone with a two-column grid for quantities and names), and pull-quote-style tips.
- **Cook mode:** the page goes quiet. One step at a time in large serif, Apple News style focused steps (the current one bright, previous/next at 0.6). The timer sits as a slim strip at the bottom above Back/Next.
- **Look:** ink-blue black `#0f1114`, paper-dark `#1a1c20`, text `#ece7df`, secondary `#9a958c`, accent clay `#c9785a`, yolk for the single key action. Type: **Fraunces 200/300 (opsz high) for headlines + Jost 300/400 for UI**. Image corners 0; generous editorial margins (24–28px) with wide vertical rhythm.

## Deliverable (each route)
`app/routes3/<1-cinema | 2-instrument | 3-counter | 4-editorial>.html`, one self-contained page:
- inline CSS; Google Fonts only; little JS (only for small things like video autoplay)
- `<meta name="viewport" content="width=device-width, initial-scale=1">`
- the page background `#0b0b0b`

Contents:
1. **A header:** the route number and name, a one-sentence idea, "Built from:" (which round 1 feedback it uses), and the four choices it makes (colour · type · images · structure).
2. **Three frames, side by side** (Landing · Recipe · Cook mode). Each is 390×844, with rounded phone corners (about 44px) and a status bar (9:41), clipped (`overflow:hidden`), and wraps on narrow screens. On a phone (under 430px wide), the frames scale to fit the width with no horizontal page scroll; use `zoom` or a transform-scaled wrapper.
3. **Below the frames:** "Good at" and "Watch out for", 3 short bullets each.

**Verify:**
- Render with puppeteer-core using Chrome at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. The module is in `/private/tmp/claude-502/-Users-craig-Documents/7e225530-d818-4274-ae32-023e08096998/scratchpad/uxtest/node_modules`; run node with `NODE_PATH` set to it.
- Take a desktop screenshot (1400 wide) and a phone screenshot (390 wide, isMobile).
- Look at the PNGs and fix anything clipped, overlapping or overflowing; check that long names wrap. Repeat until it looks finished and polished.
- Save screenshots to `scratchpad/r3/`.
- Write only `app/routes3/<your file>` and `scratchpad/r3/`. Don't touch anything else.
