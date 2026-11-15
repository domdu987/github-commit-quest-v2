# s08 QA: film 9, shots 8-9 (the split, cooking rice again at dawn)

Delivered: `take.mkv.partaa..partab` (= `take.mkv` 78 MB split at 40 MB: `cat take.mkv.part* > take.mkv`; libx264rgb crf 6, 30 fps,
first_g 501, 202 frames g 501..702, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio). Plan range g 507..696
(16.90-23.24 s) + 6 handle frames each side rendered in 3D (g 501..506 = shot 8 set-up backwards; g 697..702 = shot 9 continued).
Set: the client-approved `set3d9/wall.py` (commit 5d511aa). Also `meta.json`, `cues.json` (6 cues), `contact.jpg` (16 frames, cyan line
= y 880). Scripts as s05 (`shot.py`, `c9.py`, `take_info.py`, `deliver.py`, `qa.py`, `sheet.py`, `gp.py`). Two builds (one location per
process / light): shot 8 wall_site DAY (two_sections area), shot 9 wall_site DAWN (cauldron area), joined by the plan's cut at g 615.

## Client rules
- **No depth of field** (as s05). **No text signs.** Calm moves: shot 8 a 1.0 D push with a slight drift, shot 9 a 1.5 D push.
- **Heads above the caption band**: all head bottoms < 880 (shot 8: general 0.54 H, lin 0.56-0.57 H, worker 0.56 H; shot 9: lin 0.48 H).
- **Mouths**: no quote in shots 8-9: static mouths only.

## Timing
| g | what | narration |
|---|---|---|
| 501-519 | shot 8: the wall seen from the site: the general's grey plain-mortar section (screen-left) and lin's creamy rice-mortar section (screen-right) meeting at the seam mid-frame; the general at the seam, akimbo, smug; lin, arms folded, in front of his section; a worker with a brick stack waits behind the general | "แม่ทัพเลย" 16.87 |
| 519-546 | the chop: his right hand rises high (519-529), holds, cuts straight down the seam (537-546) | "แบ่งกำแพง" 17.44, "เป็นสองช่วง" 18.09 |
| 546-558 | he faces the camera, hands on hips; behind the blink at 558 the drawing flips to face screen-left | |
| 560-571 | turns to his own grey section and points at it proudly | "ช่วงของ" 18.81 = g 567, "แม่ทัพใช้ปูน" 19.24 |
| 602-614 | arm back to the hip, chin up | "ธรรมดา" 20.11 |
| 615 | CUT to dawn: lin alone on his platform stirring the steaming rice soup, his section behind, pink-gold light | "ส่วนช่วงของ" 20.57 |
| 662- | a content smile (behind the blink) | "ไอ้ช่างขนม" 21.25, "ต้องรอต้มข้าวทุกวัน" 21.91 |
| 697-702 | out-handle | |

## Staging
| set-up | camera | figures |
|---|---|---|
| 8 two_sections DAY | closer and lower than the preset so the figures read (QA_TECH 7): (0.3, 17.8, 4.2) -> (0.6, 16.9, 4.1), look (0..0.2, 5, 2.9), 20 mm | general (1.5, 10.6) at the seam on his side; lin (-1.7, 10.3) mirrored to watch him; worker_b (3.6, 8.9) holding bricks (workers_carry_b, idle sway) |
| 9 cauldron DAWN | (-12.4, 21.8, 6.6) -> (-12.9, 20.4, 6.2), look (-14.4..-14.8, 12.5..12.6, 3.5..3.6), 24 mm | lin on `lin_stir` (platform z 1.5), mirrored so he stirs into the wok; hands on a 24-frame ellipse |
Wall heights lin 16 / general 16 keyed every frame (just split, both level; month 1 = 18 / 21 in shot 10). Steam 1.0, flames keyed
every frame. Sprites 256 px/D.

## Checks (`work/qa.txt`)
- Pops: the planned cut 614 -> 615, and a small 3.4-level change at 557 -> 558 = the general's mirror flip, done at yaw 0 with symmetric
  hips-akimbo arms and hidden by a blink (only the plume side and the shading change; checked at full size, `work/flip.jpg`).
- No near-still transitions; frame change median 1.6. No black / magenta frames, no retried frames, no sprite clipping.
- Fixed after the first final (withdrawn): a hard pop at g 561 (the flip mid-gesture), a chop that did not read, a brick carrier who walked
  in front of the general at the end, and the cauldron steam column covering the left third of shot 9 (camera panned toward lin). All
  202 frames re-rendered.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s08 shot 8 (g 507-614)                         19.1   51.0    0.9    0.4    0.0   24.9    2.4    1.3  0.45 0.57 0.04
s08 shot 9 (g 615-696)                         41.9   30.9    1.4    0.0    0.0   11.5    3.5   10.7  0.35 0.55 0.03
s08 all                                        27.4   43.6    1.0    0.3    0.0   20.2    2.8    4.7  0.41 0.56 0.04
ref a t0062 t0072 (day wide / medium)          23.6   12.5    1.0    0.0    0.0   55.3    2.8    4.7  0.58 0.65 0.14
```
Shot 8: the set's warm DAY. Shot 9: the DAWN preset's pink-gold (red + magenta 10.7 = the peach sky and the pink-lit brick; the set notes
cauldron DAWN as the most magenta frame of the set, 12.4); shade stays blue.

## Seconds per frame
19.2 s wall / 37.7 CPU s mean (2 threads, two render processes at once on 4 cores, 12 samples).
