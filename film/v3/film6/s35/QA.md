# s35 QA: film 6, shot 35 (the ending), market MORNING — render team 7

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps), first_g 3069, 125 frames g 3069..3193. g 3069..3074 = 6-frame in-handle for the
dissolve from shot 34 (rendered in 3D). g 3075..3193 = shot 35 (plan 102.50 s to the end; the last film frame is N-1 = 3193, so there is no out-handle).
Also included: `meta.json`, `cues.json`, `contact.jpg` (16 frames, red line = y 880), `compare.jpg` (3 finals + ref a t0061, ref b t0121),
`shot.py` (probe / stills / final), `deliver.py` (frames, meta, cues, sheets, mkv, `work/qa.txt`).

## What is on screen
Henry's bakery front in the market square (west row) on the next morning. Henry (smiling, hands on his belly) and kit (fists on his
hips, grinning) stand in front of their shop. Between them, on the let-down shutter board, is the basket of 13 loaves; **the 13th, on the very
top, is drawn paler** (its own pale crust gradient, swapped into `cast6.basket_svg`). White steam rises off the basket in the low
morning sun, and the bread sign hangs on its bracket above.
- g 3069..3108, close on the shop: a slow drift. Kit glances up at Henry (3077..3113), Henry nods (3083..3101), kit hops (3115..3127).
- g 3109..3183, crane pull-back and rise, sine-eased, from about 6 D to about 15 D. It ends low-high (z 4.5), under the bunting, on the
  whole bakery front with the market around it.
- g 3183..3193, still drifting at the end (never static).

## Client rules
- **No DOF / sharp**: `use_dof` is False and `B.setup_dof(None)` is set at build and before every render. No motion streaks.
- **Heads above the caption band**: no head bottom below y 880 on any frame (`work/qa.txt`). Main heads: henry centre 0.50..0.54 H,
  kit 0.56..0.59 H.
- **Mouths**: no quoted line, so static expression mouths only.
- **Continuity**: kit is floury with his cap; Henry is bald with his tuft; the 13th loaf is the pale one.

## Numbers (`work/qa.txt`)
| actor | head w px | centre x | centre y |
|---|---|---|---|
| kit | 203 -> 57 | 91..272 | 715..755 (0.56..0.59 H) |
| henry | 134 -> 57 | 483..555 | 634..687 (0.50..0.54 H) |

- Popcheck: no pops; no near-still frame pairs; frame change median 6.0 levels.
- No black or magenta frames; no retried frames.

Hue (shot frames):
- s35: red 37.7, orange 40.6, blue 12.5, violet 3.8, magenta 3.6, sat 0.35, val 0.63, dark 0.03.
- ref a t0061: red 54.5, orange 26.1, sat 0.49, val 0.68, dark 0.26.

Like every market shot, s35 is brighter and flatter than the refs (bakery_API 7). The shade is blue-violet, not magenta.

## Seconds per frame
16.7 s wall / 30.8 s CPU mean, with 12 samples, 720x1280, 2 threads and two render processes on 4 cores.

## Differences from the plan / known issues
- The plan says "pull back from the bakery sign". The sign hangs on a bracket perpendicular to the façade, so the take opens on the shop
  with the sign top-right and the steaming basket centre-left, then pulls back.
- Henry and kit are added in front of the shop (the plan names only the sign and the basket). Delete the actors in shot.py if an empty
  shopfront is wanted.
- Kit's head touches the left frame edge in the first ~10 frames (head centre x 91, w 203).
- The market's Henry's-bakery façade is not identical to the bakery interior's own front (set limitation, bakery_API 7).
- Steam uses local camera-only cards with the set's steam material, because the set's `set_steam` sources exist only in the bakery interior.
