# Round 2 design options: A · Quiet Index, B · Full Bleed, C · Kitchen Journal

Three options **within one agreed direction**. They differ only on three open questions:
1. **How much the images lead** (calm frame ↔ full-screen)
2. **The voice of the type** (Jost only ↔ serif titles + Jost)
3. **How sections are separated** (space and scale only ↔ soft colour fields)

Everything else is fixed, so Craig compares design, not content.

## Fixed for every option
- **Four frames, each 390 × 844** (phone, rounded, status bar), side by side on a near-black page (`#0e0a08`), wrapping on narrow screens:
  1. **Landing** (option 3): context line · Feel like (mood words) · With (round ingredient photos, multi-select) · Best match (the first one larger, then 2 rows, each with a reason line) · the start of "In season now" · bottom bar (search + filter button).
  2. **Recipe:** *Japanese mirin baked cod* (media `C6_FrdiyZjh`) · photo or video · title · creator (Lisa @thelisafeed) · "Takes about 1 hr 22 min (incl. 1 hr marinating)" · Serves (not given) · **"+ Add to our list"** (one clear primary) + ♡ favourite + "Watch the Reel" · ingredients · start of method · Start cooking pinned at the bottom.
  3. **Cook mode:** step 2 of 7, "Turn the cod in the marinade… leave to marinate for at least 1 hour (the fridge is the safe place)." A **60 min timer running (52:14)** in a sticky timer row · "For this step: cod" · "While you wait: heat the oven to 180°C fan near the end." · the next step visible but quieter · big Back | Next joined (no gap), at least 64px tall.
  4. **Cook-log story:** "On **Tuesday**, **Craig** made the **Japanese mirin baked cod**. It was **lovely**, but it **was a bit sweet**. Next time, ___. We'll ___." The word sheet is open for "Next time…" with options (change nothing · use less sugar · add more ginger · marinate overnight · make it ahead).
- **The moment:** Tuesday evening, the fresh box has arrived, the cod is on our list, early-to-mid autumn. Context line: "Tuesday evening · for both of us · mid autumn · the box is in".
- **Content rules:** UK English, grams, fan °C, hob 1–9. Quiet, Nigel Slater-like voice. No emoji. No calories, scores or streaks. No glossy stock-photo feel.
- **Craig's rules (must hold in every option):** function first · images and video are essential · **no divider lines** · **no boxes inside boxes** (avoid repeating rounded containers; vary the spacing to make rhythm) · **fine type, not bold** · no dashed lines · nothing poster-bold · design for real (long) recipe names.
- **Usability fixes from the persona tests (include in all):**
  - 44px minimum targets
  - a visible time, never "time to check"
  - one clear save action
  - selected ingredients shown as removable chips
  - faded steps no fainter than about 0.6 opacity
  - timers you can start and that stay visible
  - the next step previewed
  - the story defaults to the current cook
- **Palette (dark walnut):**
  - background `#17100c` · surface `#231812` · raised `#2f2119`
  - text `#ebdac6` · secondary `#b39476`
  - brass accent `#d4a463` · **yolk `#f2c75c` only for the single key thing**
  - story colours: people `#9fbf9a` · feel `#8fb3c4` · time and changes `#f2c75c` · dish `#d4a463`
- **Images:** `../../media/<code>/hero.jpg` relative to `app/routes2/`.
  - Landing: Best match uses `C6_FrdiyZjh` (mirin cod), `DVbnwhjiExJ` (cod grenobloise), `C8kHapDNLG3` (pesto orzo with salmon).
  - With circles: cod `C6_FrdiyZjh`, salmon `C8kHapDNLG3`, tofu `DT5nuU5iPAH`, eggs `DIJpP8hKBoA`, spinach `Cyf04RxIO8c`, cabbage `Cy2_tQfsh6_`.
  - In season: `CwiWc2KId6o`, `DDAItEoo_vi`.
  - Video: `../../media/C6_FrdiyZjh/video.mp4` (show as `<video poster=…>`, not playing).

## The three options
**A · Quiet Index:** calm and type-led; images where they earn it.
- Jost only (300/400).
- Landing as in the wireframes: small circles, a moderately sized lead card, compact rows, lots of space.
- Recipe: photo at the top (not full-screen), then a long calm page of text.
- Cook mode: focused steps on plain walnut.
- Separation by space and scale only.

**B · Full Bleed:** the food is the interface.
- Jost only, lighter and larger over images.
- Landing: Best match leads with **one large edge-to-edge photo** with the title over a gradient, images throughout.
- Recipe: a **full-screen photo or video** with the content on a sheet that slides up over it (a sheet is one surface, not boxes in boxes).
- Cook mode: focused steps (current one bright, the others quieter) over a **blurred, darkened photo of the dish** (Apple News reference).
- Separation: image ↔ sheet; space within.

**C · Kitchen Journal:** warm and editorial, like a well-kept cookbook.
- **Serif titles** (Newsreader or Fraunces, light weights) + Jost for everything working.
- The highlighted meta line, e.g. "Fish · Japanese · weeknight".
- Landing: a serif heading per section, **soft muted colour fields** (sage `#2c3327`, clay `#3a2620`, plaster `#2e2a26`) instead of lines; larger thumbnails.
- Recipe: the photo set like a book plate, an editorial ingredients column.
- Cook mode: the step in serif, ingredients in the margin.

## Deliverable
`app/routes2/<a-quiet-index | b-full-bleed | c-kitchen-journal>.html`: one self-contained page (inline CSS; Google Fonts only; little or no JS) with:
1. **A header:** option letter and name, a one-line idea, and the three choices it makes (images · type · separation).
2. **The four frames, side by side.**
3. **Below:** "What this option is good at" and "Watch out for", 3 bullets each.

Frames must look finished. Nothing clipped or overflowing, and long titles must wrap gracefully. Verify by rendering with headless Chrome and looking at the PNG, then fix and repeat. Only write inside `app/routes2/` (and the scratchpad for screenshots).
