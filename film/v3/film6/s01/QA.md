# s01 QA: film 6, shot 1 (the hook), bakery MORNING (the plan's "DAWN / counter")

Delivered: `frames/g_0000.png .. g_0069.png` (70 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 0). g 0..62 = shot 1 ([g0, g1) = [0, 63), plan 0.00-2.10 s); g 63..69 = 7-frame out-handle
(push + grin continue, rendered in 3D). Shot 2 is NOT in this take (as asked).
Also `meta.json` (first_g 0, n_frames 70, events), `cues.json` (9 cues, film seconds), `contact.jpg` (16 frames), `compare.jpg`
(g 56 beside ref a t0046, the closest framing: people behind a laden table, warm candle-lit interior; and the wink g 42 beside ref a t0001).
Scripts: `shot.py` (probe / stills / final), `deliver.py`, `qa.py` (-> `work/qa.txt`), `sheet.py`; shared helpers in `../common.py`.
Raw renders + per-frame json in `raw/s1`. Drafts: `work/d1..d8.jpg`, `work/f1..f4`, crops `work/fin_a.png`, `work/fin_b.png`.
First full final (`work/old_raw/raw1`) was rejected by eye: the loaf + hand vanished behind the basket pile -> loaves now hover and drop.

## Client rules
- **No depth of field anywhere**: `cam.data.dof.use_dof = False` and `B.setup_dof(scene, None, None, cam=cam)` at build and before every
  render (common.Take). Everything is sharp: the oven bricks, ceiling herbs, the board loaves in the foreground.
- **Dense set**: the bakery's own dressing, kept whole: candle wheel, hanging herbs / wheat / copper pans, oven mouth fire, racks with loaves,
  the hand balance, baskets and loaf heaps on the shutter board (foreground). Steam lowered to 0.35 (0.8 put ribbons across kit's face).
- **Heads above the caption band**: kit head centre y 511-520 (0.40 H), bottom <= 631; henry 584 (0.46 H). Nothing below y 880 but the
  counter and the board loaves.
- **Mouths only on quoted lines**: shot 1 has no quote -> no lip-sync. Kit's mouth is the static mouth of each expression
  (happy smile -> wink smirk -> smirk -> grin, the grin change behind a blink); henry closed ("unimpressed").

## Timing (captions.json, narration at +0.10 s)
| g | what | caption |
|---|---|---|
| 0-8 | loaf 10 rises from below the counter, held above the pile, drops g 8 | "เด็กคนนี้ขาย" (-0.01) |
| 13-21 | loaf 11, drops g 21 | "ขนมปังทีละโหล" (0.84 s = g 28) |
| 26-34 | loaf 12 (far spot, arm at full stretch), drops g 34 | |
| 36-45 | looks up into the lens (36-40), WINK 40-45 | |
| 46-50 | glance back at henry (screen-left, by the oven) | "แต่ยัดก้อน" 1.58 s = g 50 |
| 49-57 | the 13th loaf: up and held over the top (g 56), drops on the very top g 57 | "แต่ยัดก้อน" |
| 58-69 | grin into the lens (blink g 56-58, 67-69) | "ที่สิบสามลง" starts g 70, after the shot |
Camera: one slow push (sine, 0.38 D in, 24 mm, eye level just above kit's eyes, pitch -6 deg). The shot is 2.1 s with one framing
(plan: shot 2 follows as a cut at 2.10 s).

## Staging (`work/qa.txt`)
| actor | head width px | centre x | centre y (H) |
|---|---|---|---|
| kit | 201 -> 221 (push) | 406-433 | 0.40-0.41 |
| henry (background, by the oven) | 101-106 | 91-108 | 0.46 |
Near/far 221 / 106 = 2.1 (plus the board loaves in the foreground, ~260 px wide). Kit stands on a hidden stool (feet z 0.98) so his
chest and apron bib clear the counter top (z 1.25) and his arm comes down over the basket rim.
Basket: `cast6.basket_svg` drawings with 9..13 loaves on one `common.PropCard` (scale 1.4, base on the inside counter at (1.30, 1.08)),
the variant switched (constant keys) the frame after each drop. Kit's loaf is the cast prop `loaf` x0.9 (= the size of the drawn loaves).
Hand registration: the hand (not the prop tip: `hands={'r': {'tip':..., 'prop': 'loaf'}}` came out 0.14 D off) is pinned in kit's card at
`actors.world_to_local(hover point) + (0, 0.13)`; IK reach error 0 except the far 12th spot (<= 0.07 D, ~13 px, g 32-34); the loaf then drops ~35 px onto the drawn position when the next variant takes over (reads as the drop).
Popcheck: no pops (no cut in the take); frame change median 2.9, max 4.3 levels; no near-still pairs. No black / magenta frames, no retried
frames, no clipped sprites.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s01 shot 1 (g 0-62)                            44.5   44.0    1.2    0.4    0.0    0.8    0.7    8.4  0.45 0.55 0.08
s01 all (g 0-69)                               44.9   43.7    1.2    0.5    0.0    0.8    0.7    8.3  0.45 0.55 0.07
ref a t0001 t0046 t0047                        32.1   44.2    4.9    0.3    0.0    7.0    6.1    5.4  0.34 0.47 0.12
```
Warm interior as the set measures it (bakery_API 7: warmer / lighter than ref A interiors, almost no blue). Orange matches the ref (44 / 44);
red is higher (the brick oven wall fills the left third); blue 0.8 vs 7 and saturation 0.45 vs 0.34. Not graded here (set look, same for
every bakery shot); if the director wants it closer to ref A, darken / cool the bakery in the conform for all bakery shots alike.

## Seconds per frame
17.66 s wall / 34.6 s CPU mean (2 threads, two render processes at once on 4 cores, denoise FAST, 12 samples). Kit sprite 448 px/D,
henry 192 px/D, basket PNGs 512 px/D. Cost is the set (bakery 28-38 CPU s in bakery_API 5; steam 0.35 still on).

## Differences from the plan / known issues
- "DAWN": the set has MORNING / AFTERNOON only; MORNING used.
- Camera: custom (not the `counter` preset, whose 22 mm view puts kit at 141 px behind a wall of board loaves): street-side, 24 mm, over
  the shutter board, kit 201-221 px.
- The customer is not in frame (from the street the customer would stand between the camera and the counter at ~400 px head size);
  her basket stands on the counter, filled by kit. If the director wants her, a later shot can show her taking it.
- The basket handle hides kit's hand ball while a loaf hovers (the loaf and the forearm read); the hand balance's weights pan sits just
  right of the basket (set object, not moved).
- Glance back at henry is a quick yaw + gaze to screen-left with the smirk (half-lid eyes, so the pupils move only a little).
