# Sheet proportions: Kong, James, Khun Tos

Source: `uploads/character_sheet.webp` (1448x1086). Figures segmented on the cream paper (`|rgb-(253,243,232)| > 28`, connected components, hole-filled silhouettes).
Scripts and evidence: `spec/sheet_measure/measure_sheet.py` (writes `sheet_measure.json`, `*_cut.png`, `*_measured.png` annotated crops), `spec/sheet_measure/v2/` (segmentation `seg.py`/`crops.py`, head-circle and face-feature fit `face2.py` -> `face2.json`, gridded zooms `*_grid3.png`).
Crotch, boot top, shoulder points, glove box and hair limits were read from 3x-5x gridded zooms. Everything else is computed. Expect about +/-2 px error, which is about 1.5 % of the head.

**D** = bare head width including the outline, without hair. It is the mean of the circle fit on the lower face contour and the widest row of the face measured directly: Kong 127 px (fit 128.9 / measured 125), James 111 px (112.2 / 110), Tos 121 px (119 / 123). The head is a circle. The lower-half fit residual is 1.2 px on Kong and 3.0 px on James. Tos fits worse (4.5 px) because his glasses and hair break the contour. So the bare head height is D as well.
Bands are the target +/-6 %.

## 1. Figure proportions

| measure | Kong | band | James | band | Khun Tos | band |
|---|---|---|---|---|---|---|
| total height, hair top to sole (px) | 547 | - | 499 | - | 510 | - |
| head D (px) | 127 | - | 111 | - | 121 | - |
| bare head D / total | **0.232** | 0.218-0.246 | **0.223** | 0.210-0.236 | **0.237** | 0.223-0.251 |
| hair top to chin / total | **0.271** | 0.255-0.287 | **0.279** | 0.262-0.296 | **0.278** | 0.261-0.295 |
| figure height in bare heads | 4.31 | 4.05-4.57 | 4.49 | 4.22-4.76 | 4.22 | 3.97-4.47 |
| hair above skull top / D | 0.17 | 0.16-0.18 | 0.25 | 0.24-0.27 | 0.17 | 0.16-0.18 |
| hair vertical extent (top to lowest side spike) / D | 0.72 | 0.68-0.77 | 0.90 | 0.85-0.95 | 0.79 | 0.74-0.83 |
| hair mass width / D | 1.24 | 1.16-1.31 | 1.26 | 1.18-1.34 | 1.17 | 1.10-1.24 |
| shoulder width / D | **1.32** (sleeve to sleeve) | 1.24-1.40 | 0.94 (jacket; left side behind backpack, mirrored from collar) | 0.88-0.99 | **0.82** | 0.77-0.87 |
| shoulder + backpack span / D | 1.44 | 1.35-1.53 | 1.65 (delivery box) | 1.55-1.75 | - | - |
| torso width at belt / D | 0.89 | 0.84-0.94 | ~0.9 | - | ~0.9 | - |
| torso, chin to crotch / total | 0.333 | 0.313-0.353 | 0.316 | 0.297-0.335 | 0.310 | 0.291-0.329 |
| torso / D | 1.43 | 1.35-1.52 | 1.42 | 1.33-1.51 | 1.31 | 1.23-1.39 |
| legs, crotch to sole / total | 0.395 | 0.371-0.419 | 0.403 | 0.379-0.427 | 0.410 | 0.385-0.435 |
| legs / D | 1.70 | 1.60-1.80 | 1.81 | 1.70-1.92 | 1.73 | 1.62-1.83 |
| one trouser leg width at thigh / D | **0.44** (cargo) | 0.41-0.47 | 0.33 | 0.31-0.35 | 0.31 | 0.29-0.32 |
| hand (glove/fist) width / D | **0.33** (glove 42x40 px) | 0.31-0.35 | 0.30 (fist; 0.54 tall with raised thumb) | 0.28-0.31 | ~0.19 (fingers only; arms crossed) | - |
| forearm (bare) width / D | 0.13-0.18, white tube with ink outline | - | sleeved | - | sleeved | - |
| boot/shoe height / D | **0.65** (boot) | 0.61-0.69 | 0.50 (high-top sneaker) | 0.47-0.52 | 0.32 (low shoe) | 0.30-0.34 |
| boot/shoe sole length / D | **0.45 / 0.54** (3/4 / side) | 0.42-0.57 | 0.50 / 0.64 | 0.47-0.68 | 0.45 / 0.56 | 0.43-0.60 |
| head outline, median (px) / D | 4.9 / 0.038 | 0.036-0.041 | 4.9 / 0.044 | 0.041-0.047 | 4.75 / 0.039 | 0.037-0.042 |
| head outline, max (px) | 12 (thick at the left and right equator, 160-175 deg and 0 deg) | - | 15.5 | - | 12 | - |
| body/limb outline (px) / D | 4 / 0.032 | 0.030-0.034 | ~4 | - | 4 / 0.033 | 0.031-0.035 |

Landmarks (local crop px): Kong chin 148 / belt 283-300 / crotch 330 / boot top 463 / sole 546. James chin 139 / belt 280-290 / crotch 297 / shoe top 443 / sole 498. Tos chin 142 / belt 262-275 / crotch 300 / shoe top 470 / sole 509.

Readings:
- With the hair included, the head is 0.27-0.28 of the figure (just over a quarter, the user's "a third"). The bare head is 0.22-0.24 of the figure. Figures are 4.2-4.5 bare heads tall.
- The neck is a tiny collar only. The jacket or vest starts about 0.05 D below the chin.
- Kong is the broad one: sleeve span 1.32 D, backpack span 1.44 D, trouser legs 0.44 D each, boots 0.65 D tall. James and Tos have shoulders at or below head width (0.82-0.94 D) and legs about 0.31-0.33 D wide.
- Legs are longer than the torso, about 1.7-1.8 D against 1.3-1.4 D.

## 2. Face (offsets from the head-circle centre, in D; +y is down)

| feature | Kong | James | Khun Tos |
|---|---|---|---|
| expression | determined: angry V brows, smile | joyful: closed ^ eyes, open mouth | stern: one flat brow, one angled, frown |
| face turn (eye midpoint offset) | +0.06 D (near frontal) | +0.07 D | +0.23 D (clear 3/4 view to screen right) |
| eye shape | solid vertical ovals, 10x25 px = **0.08 x 0.20 D** | closed arcs 28x18 / 25x15 px = 0.24 D wide, stroke 4.6 px | solid ovals 7x15 / 6x11 px = 0.06 x 0.12 D (behind glasses) |
| eye centre y | 0.00 D (at the circle centre) | -0.08 to -0.14 D | -0.05 to -0.07 D |
| eye spacing (centre to centre) | 39 px = **0.31 D** | 44 px = 0.40 D | 42 px = 0.35 D |
| brows | two straight bars 31 px and 27 px long = **0.21-0.24 D**, thickness 5.0-5.6 px (stroke up to 6.6) = **0.04-0.05 D**, angles +15 deg / -21 deg (inner ends down), at y -0.14 D, gap 17 px = 0.13 D | hidden under the fringe | 33 px (+7 deg, almost flat) and 23 px (-22 deg) = 0.19-0.27 D, thickness 4.2-4.7 px = 0.035-0.04 D, at y -0.17 to -0.20 D |
| mouth | smile arc 32 px = **0.25 D** wide, stroke 3.8 px = 0.03 D, sag about 4 px, at y +0.26 D | open D shape 29-32 x 27-29 px = **0.26-0.29 D** wide, 0.24 D tall, ink 8 px, pink tongue, at y +0.19 D | frown arc 22 px = 0.18 D, stroke 3.8 px, at y +0.24 D |
| glasses | - | - | black rectangular rims, lenses 37x22 and 32x22 px, overall 93 px = 0.77 D, rim about 3-4 px |
| stubble | 9-11 short ink ticks along the inside of the jaw outline, on the arc from about 45 deg to 130 deg (straight down is 90 deg). Spacing about 8-10 deg (about 8-9 px). Each tick runs 3-5 px inward from the outline (0.03-0.04 D), stroke 1.5-3 px, and stands roughly perpendicular to the contour. The ticks sit under the mouth, between y +0.35 and +0.44 D. | - | - |

## 3. Hair and colours

- Hair is a single solid ink-black mass of big pointed clumps, with no strands drawn inside. It overhangs the circle by about 0.1-0.13 D on each side.
  - Kong has about 6-8 clumps. The fringe points down onto the forehead, about 0.3 D into the face circle.
  - James has a taller crest (0.25 D above the skull) and side locks that reach near eye level (0.90 D extent).
  - Tos has a smooth side-swept volume, dark brown-black `#302a26`, that bulges on his back side (screen left).
- Colours sampled as 5x5 medians:

| item | colour |
|---|---|
| paper | `#fdf3e8` |
| face and bare arms | `#fdf6ed` (almost identical to the paper; the face reads only through the ink outline) |
| ink | `#070805` in the eyes, `#1d1d1d` in the hair |
| Kong orange | `#ed7e24` |
| Kong trousers | `#423e3b` |
| Kong boots and gloves | `#383838` / `#333333` |
| Kong vest black | `#1b1b19` |
| James green | `#52a753` |
| James trousers | `#313131` |
| Tos navy | `#323b4f` |
| Tos khaki | `#d0b190` |
| Tos shoes | `#383838` |

## 4. Kong kit, as drawn (read from the crops)

- Short-sleeve orange shirt with a big pointed collar. The left sleeve carries a Thai flag patch (screen left).
- The chest panel reads "RESCUE" in white on black, with a light grey reflective band below it.
- Black chest harness / backpack straps run over both shoulders, and the backpack shows on the screen-left side.
- A radio clipped to the chest (screen right) has its antenna rising to chin height.
- Black belt with a light buckle (y 283-300). A pouch hangs on the left hip and a holster/pouch with orange tabs on the right hip.
- Dark grey cargo trousers have:
  - a thigh pouch with a strap band at about y 385-398
  - a straight wide cut, 0.44 D per leg
- Chunky black lace-up boots, 0.65 D tall, with a wide sole and a toe cap.
- Big black gloves (0.33 D) on white stick forearms.
- He holds an orange hydraulic rescue cutter.
