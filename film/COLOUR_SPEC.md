# COLOUR SPEC: the client's colour standard (2026-11-21, binding for every film)

These are the values of the reference-style-shorts skill used for the storm film. They come from SKILL.md (style card) and references/bible/colour-light.md (paths in film/skill/reference-style-shorts/).

**This file OVERRIDES the colour and saturation rules in QA_TEAM.md §G and §I** (saturation ≥ 0.47/0.50, vivid ≥ 45 %, "signature colour"). Those rules are void.

## 1. Main colours by role
| Surface | Colour |
|---|---|
| Walls (deep red / terracotta) | #561e37, #5e2221 |
| Navy floor | #152a63 to #17153a |
| Wooden floor | #ac825e |
| Wood | #976c4d |
| Lower wall panelling | #491309 |
| Red cloth | #a1001c to #da0045 |
| Gold metal | #cb9f48 |
| Daytime sky | #4a78cd to #92b7e7 |
| Cream paper | #fcf4e1 (never pure white) |
| Lamp filament | #fffeec |

## 2. Characters
- Colours:
  - head #fef7f6
  - head shading edge #e9dceb
  - ink line #3a2832
  - inside of the mouth #4d2433
- Characters are UNLIT: no shading on the body and no bloom, but they DO cast shadows onto the ground.
- A whole-body tint is allowed only when needed: night #fbdaf7, warm interior light #faded0.

## 3. Whole-frame colour shares
Measure with film/v3/tools/hue_report.py (also at film/skill/reference-style-shorts/pipeline/v3/tools/).

| Measure | Target |
|---|---|
| Red | 30-41 % |
| Orange | 22-38 % |
| Blue | 14-30 % |
| Purple | 0-5 % |
| Magenta-pink | 0-10 % |
| Saturation | 0.38-0.48 |
| Brightness | 0.45-0.63 |
| Dark area (V < 0.25) | 8-15 % |

- Large surfaces are saturated mid-to-deep tones: S 0.45-0.9 and V 0.30-0.75.
- No large surface is brighter than V 0.80, except sky.
- Exteriors, map close-ups, night and storm shots may fall outside these bands, but the reason must be written in the take's QA.md.

## 4. Light (office, daytime values)
- **Key light:** one sun only, KEY (2.30, 1.65, 0.74), coming from camera-left, with a shadow softness angle of 0.45 deg.
- **Shade:** added as emission SHADE (0.20, 0.27, 0.54), tinted per surface with shade_mul.
- **Shadows:**
  - blue-violet, hue 240-260 (e.g. #332d40, #525065)
  - 15-31 % of the lit level
  - edges 4-21 px wide
- **Glow:** only real light sources brighter than 1.0 may glow, with a radius of 12-24 px.
- **Black point:** luma p1 of 0.08-0.12.

## 5. Final grade
Use the v1.1 grade: `examples/film_mini.py grade`.
- one S-curve
- saturation × 1.18
- bloom on hot spots only: threshold 0.955-0.985, bloom colour (1, 0.94, 0.84)
- protect reds and whites
- brightness ceiling 0.985
- vignette ≤ 5 %
- no grain and no sharpening

## 6. Captions
- Kanit Black, 88 px, white #ffffff.
- Black outline 4 px, shadow 1.5.
- Position \pos(360,900) on 720x1280.
