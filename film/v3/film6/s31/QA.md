# s31 QA: film 6, shots 31-32 (the reveal: steam = water; the dawn loaf vs the afternoon loaf), bakery MORNING -> AFTERNOON

Delivered: `frames/g_2581.png .. g_2841.png` (261 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions/audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 2581). g 2587..2835 = shots 31-32 ([2587, 2836)); g 2581..2586 and 2836..2841 are
6-frame handles rendered in 3D. Also `meta.json`, `cues.json` (9 cues), `contact.jpg` (22 frames, caption line drawn), `compare.jpg`
(drops ECU / scale insert beside ref a mechanism ECUs t0101 / t0106). Scripts: `shot.py`, `deliver.py`; raw renders in `raw/s31`
(shot 31), `raw/s32` (shot 32 MORNING part), `raw/s33` (shot 32 AFTERNOON part), git-ignored.

## Framings (plan 86.24-94.54 s)
- **31a** g 2581-2629 table_insert push over fresh loaves, full white steam (`set_steam 1.0`): "เพราะควันขาว ๆ ที่เด็กเห็นทุกเช้า".
- **31b** g 2630-2672 closer on the front loaf: on "ไม่ใช่ควัน" the steam thins (1.0 -> 0.22, g 2640-2664) and turns into **tiny
  water drops** popping out of the crust and rising (diagram look: pale-blue drop, white glint, plum ink outline).
- **31c** g 2673-2714 ECU on the crust: a column of drops leaving the loaf + two dashed **up arrows** pulsing (diagram):
  "มันคือน้ำในขนมปัง ที่ระเหยหนีออกมา".
- **32a** g 2715-2750 MORNING hand balance (street through the opening, candle): the loaf just set down, the beam wobbles and
  settles **level** by g 2738 -- "ก้อนที่ชั่งเป๊ะตอนเช้า".
- **32b** g 2751-2792 MORNING closer on the beam + loaf pan, level; **dissolve g 2781-2792** (12 f, made in deliver.py) into
- **32c** g 2781-2841 AFTERNOON, same lens and continuous push (match dissolve): a few drops drift off the same loaf and the
  **loaf side rises** 0 -> -8 deg (g 2796-2826, on "เบาลงทุกก้อน" 93.57 s).

## Client rules
- **No depth of field**: off at build and before every render (common.Take.no_dof). Everything sharp (racks, shelf loaves, street).
- **Heads / caption band**: no people in this take. The key objects stay above y 880: hero loaf centre y 625-700 (31a/b), crust
  top ~770 (31c), loaf on the pan ~675-720 (32b/c), beam and pointer well above.
- **Mouths**: none (no actors).
- **Continuity**: steam motif from shots 2 / 10 is paid off; same bakery set and hand balance as shots 8 / 19 (`set_scale`,
  + = loaf side down, here 0 then -8 = loaf side up, as shot 19).

## 2D pieces (added in shot.py)
`drop_svg` (3 shape variants) and `arrow_svg` drawn in D units, rasterised by `common.svg_pngs` (256 px/D), on `common.PropCard`
emission cards facing the camera; every drop keyed per frame (location, scale pop-in 4 f / shrink-out 8 f, CONSTANT visibility).
Shot 31: ~90 drops spawned from g 2638 on the hero loaf (rate 0.3 -> 1.1/frame), size 0.032-0.050 D; shot 32c: ~26 drops from the
pan loaf (0.45/frame, 0.028-0.040 D), spawned at the loaf's current position on the moving pan.

## AFTERNOON look
On a tight insert the stock MORNING vs AFTERNOON presets look nearly identical, so the AFTERNOON half adds a runtime light tweak in
shot.py (`afternoon_look`, set module untouched): sun energy x1.3, colour warmer (G x0.92, B x0.75), sun shafts 0.55 (from 0.3).

## Pop check (`deliver.py popcheck`)
In-shot frame-to-frame median 2.3, max 11.4 levels; no near-still pairs; cuts at 2630 / 2673 / 2715 / 2751 read as cuts (34-46).
The dissolve is smooth (no pops). No black / magenta / retried frames.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s31 shot 31 (g 2587-2714)                      47.2   45.3    1.0    0.0    0.4    1.4    0.3    4.5  0.41 0.61 0.04
s31 shot 32 (g 2715-2835)                      21.1   65.1    3.5    0.0    0.0    2.0    3.5    4.7  0.45 0.55 0.08
reference A, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08
```
Warm bakery interior as the set measures it (s01 QA: same story -- almost no blue, red/orange high); the drops add a little cyan.
Not graded per shot; if the director wants the bakery closer to ref A, grade all bakery shots alike in the conform.

## Seconds per frame
13.9 s wall / 27.0 s CPU mean (two render processes at once on 4 cores; bakery is the costlier set).

## Differences from the plan
- "DAWN" = the set's MORNING preset (as s01).
- Shot 31 is cut into three framings and shot 32 into 32a/32b + the dissolve to 32c, for the 1.0-2.0 s framing-change rule.
- The dissolve sits inside shot 32 (g 2781-2792), between the two light presets, both sides rendered; not at the take boundaries.
- Added the two dashed up arrows (diagram) and a few drops in the afternoon 32c to make "the weight floats away" literal.
