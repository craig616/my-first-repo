# Design routes brief: 6 routes × 3 key frames

Static frames for comparison. **No interactions yet.** The focus is UX layout, UI and content design.

## The product
A private recipe app for **Craig and Mary** (a UK household). It holds about 500 recipes saved from Instagram Reels, each with its own video, a dish photo, ingredients, a method with timers, and ▶ timestamps into the video. Used:
- **one-handed with the fridge or cupboard open** ("do we have it?"), so key controls must sit within thumb reach at the bottom
- **propped up at arm's length while cooking** with messy hands, so type must be big and tap zones huge
- **in hand on the sofa**, browsing and choosing

The household eats **pescatarian** (Mary eats fish and veg; Craig eats meat only when cooking alone). UK English. **Grams**, ml, **fan oven °C only** (e.g. "180°C fan"), and a **1–9 induction hob** (e.g. "medium heat (5–6)").

## The three frames (each 390 × 844, an iPhone-size screen, side by side)
1. **Discover:** the home screen. Choosing what to cook. It must include, in whatever form the route suits:
   - the **Who's eating?** choice (Both of us / Mary / Craig alone), set to *Both of us*
   - a way to browse by **main ingredient** (fish, veg, beans & pulses, pasta & noodles, eggs, rice & grains, baking & sweet)
   - some sense of **Quick (≤30 min)**, **Not cooked yet**, and "**have X of Y**" ingredients from the pantry
   - search
2. **Recipe:** *Japanese mirin baked cod* (`japanese-mirin-baked-cod`, media code `C6_FrdiyZjh`). It must include:
   - the video or dish photo
   - title and creator credit (Lisa, @thelisafeed)
   - time and servings
   - **Start cooking** within thumb reach
   - ingredients with have/don't-have status
   - the method with ⏱ timers and ▶ video jumps
   - a gentle **"needs checking"** state: the cod amount isn't stated anywhere, which is honest but not alarming
   - the source credit
3. **Cook mode:** the same recipe, **step 5 of 7** ("Set the cod on the same tray, skin side up, and bake for 15 minutes, until the marinade is bubbling and the fish has begun to colour."), with **two timers running**: the step 5 bake at 11:42 left, and a second timer (e.g. rice) at 3:05. Show this step's ingredients, Back/Next, and step progress. It must be readable at arm's length.

## Content
- Real data: `app/recipes.js` (`window.RECIPES`; read it, don't change it). The intro, ingredients, steps, uses, timers and ▶ seconds are all there.
- Photos: `../../media/<code>/hero.jpg` (relative to `app/routes/`). Video: `../../media/<code>/video.mp4` (use it as a `<video>` with the poster, not playing, if your route shows video).
- Discover should show the **9 household recipes** (everything except `sukiyaki`, which contains beef).
- You may **rewrite content for the final format** (grams, fan °C, hob numbers, quiet wording). This is content design, so show what the content *should* be. Don't invent facts: missing amounts stay missing, shown as "needs checking".
- The cod recipe in the final format: 180°C fan for 15 min, then grill at 200°C for 5–7 min. Marinade: 1 tbsp mirin, 1 tbsp soy sauce, 1 tsp shiro dashi, 1 tbsp sugar (about 12 g). Cod: amount not stated (2 skin-on pieces shown). Bok choy, a little oil, salt, sesame seeds, yuzu kosho (optional), rice to serve. Marinate for at least 1 hour.

## Voice (all routes)
**Quiet, like Nigel Slater.** Understated, warm, plain. "Something for tonight", not "Let's get cooking!!". Headings and buttons are short and calm.

## Never (all routes)
- No scores, streaks or gamification
- No calories or nutrition
- No glossy, stock-photo, supermarket or meal-kit polish
- **No emoji in the interface.** Use simple line icons (inline SVG) or words. The ⏱ and ▶ symbols may be replaced by SVG icons.

## Shared foundations (routes may push away from these, deliberately)
- Palette, taken from their kitchen (dark walnut by default):
  - background `#17100c` · cards `#2b1d17` · raised `#39261c` · lines `#4a3225`
  - text `#ebdac6` · secondary text `#b39476`
  - brass accent `#d4a463` · steel `#ada396`
  - **yolk highlight `#f2c75c`** (walnut text on it)
  - Daytime light: `#efe8de` / `#2b1812`
- Type: **Jost** (Google Fonts). Routes may add one more face (a serif, a handwritten face or a display face) when the route calls for it.
- Text contrast must be at least 4.5 : 1. Tap targets at least 44 px (cook mode much bigger). Body text at least 16 px; cook-mode step text 30 px or more.

## Deliverable for each route
One file: `app/routes/<n>-<slug>.html`, a single self-contained page (inline CSS; Google Fonts only; no JS frameworks, little or no JS) showing:
1. A header: route number and name, a one-line idea, and the video behaviour.
2. **The three frames side by side** (390 × 844 each, rounded like a phone, with a status bar at the top), on a neutral page background, then **wrapping** on narrow screens.
3. Below the frames, a short **rationale** in three parts:
   - **UX:** how it serves the fridge, propped-up and sofa postures
   - **UI:** layout, type, colour and image choices
   - **Content:** voice, hierarchy, and how "needs checking" and the swaps appear
   - plus **Risks:** what might not work

Frames must look finished at 1× and 2×. Content must not overflow or clip inside a frame (the frame clips at 844 px tall; it's fine for content to continue below the fold, but design what's visible). Don't touch anything outside `app/routes/`.
