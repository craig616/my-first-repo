# Intake: what food is in the house

Placeholder for the future "what's in the house" feed. Each source turns into the same pantry items, so the app's "What can we make?" view works the same way whatever the source.

## Planned sources
| Source | How it arrives | Status |
|---|---|---|
| Abel & Cole weekly box | "What's in your box" email to a **personal** address (not the connected work Gmail). Needs that inbox connected, or an auto-forward filter. | Not started |
| Supermarket orders and invoices | Order-confirmation or receipt emails (e.g. Ocado, Tesco, Sainsbury's) | Not started |
| Photos | A photo of the shopping, a receipt or the fridge, read by Claude's image recognition | Not started |
| Manual | Tapping items in the app | Wireframe only |

## Folders (drop test files here)
- `email/`: saved emails (`.eml` or PDF) for testing parsers
- `photos/`: shop or fridge or receipt photos
- `receipts/`: PDF invoices

## Pantry item (target format)
```json
{
  "name": "courgette",            // canonical name, from pipeline/ingredients-vocab.txt
  "label": "Courgettes x3",       // as written by the source
  "quantity": "3",                // optional
  "location": "fridge",           // fridge | cupboard | freezer
  "source": "abel-cole",          // abel-cole | receipt | photo | manual
  "source_ref": "email:<id> or intake/photos/<file>",
  "added_at": "2026-10-04",
  "added_by": "Craig",            // Craig | Mary | auto
  "use_by_estimate": "2026-10-09" // optional, for "use it up" suggestions
}
```

## Ideas this enables
- "In this week's box": recipes that use this week's Abel & Cole veg come first
- "Use it up": items close to their use-by date push their recipes up the list
- A shopping list that already knows what's in the house
