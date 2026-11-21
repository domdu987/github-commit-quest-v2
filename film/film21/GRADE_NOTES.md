# Film 21 grade vs the client COLOUR_SPEC (v1.1 grade, measured with hue_report stats, caption band excluded)

Test conform of the 10 accepted segments with the v1.1 grade (2026-11-21 11:00 UTC), whole film so far:
| measure | film 21 | spec | in band? |
|---|---|---|---|
| brightness V | 0.54 | 0.45-0.63 | yes |
| saturation S | 0.50 (sat floor 0.70); floor lowered to 0.55 for the final | 0.38-0.48 | to re-measure at the final |
| red | 11 % | 30-41 % | no (exterior) |
| orange | 29 % | 22-38 % | yes |
| blue | 26 % | 14-30 % | yes |
| violet / magenta | 1 % / 1 % | 0-5 / 0-10 % | yes |
| dark (V < 0.25) | 0.23 | 0.08-0.15 | no (exterior) |

## Why the battle exteriors fall outside (spec §3: "exteriors ... may fall outside these bands, the reason must be written")
- **Red 11 %**: film 21 is a daylight valley battle (Forth meadows, river, Abbey Craig). The frame is mostly grass, gold fields, river and sky; red appears only on the English surcoats, pavilions and banners. Interior films (the spec's walls #561e37 / #5e2221) put red on every wall; a meadow has no red surface.
- **Dark 0.23**: the deep river water (navy-teal, V < 0.25) and the long low-sun cast shadows on the crag fill 20-40 % of several frames (sI on the bridge over the river 0.42, sB2/sE2/sG on the shadowed crag 0.25-0.28).
Shadows stay blue-violet as the spec asks.
Per-segment SHOT values (the v1.1 grade's own stage 1) are written next to the conform as <out>_grade.json.
