# s20 QA: film 6, shot 20 (kit's realisation: the busts all happened in the afternoon), market AFTERNOON

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 1572, 73 frames = g 1572..1644, 720x1280, 12 samples, 2 threads, denoise FAST,
no captions / audio), `frames/` (local only, gitignored), `meta.json`, `cues.json` (5 cues), `contact.jpg` (16 frames), `compare.jpg`
(g 1600 beside ref a t0062, g 1630 beside ref a t0001). Scripts: `shot.py` (probe / stills / final), `deliver.py` + `deliver_lib.py`.
Range: plan 52.60-54.64 s -> [g 1578, g 1639); handles 6 + 6 rendered in 3D (in 1572..1577, out 1639..1644).

## Client rules
- **No depth of field / no blur**: `cam.data.dof.use_dof = False` + `B.setup_dof(scene, None, None, cam=cam)` (common.Take, before every
  render). No motion streak (no whip move). The soft-edged clouds are the set's painted sky cards, not blur.
- **Heads above the caption band**: kit head centre y 658-684 (0.51-0.53 H), head bottom <= 824. 20a has no actors.
- **Mouths**: no quoted line -> kit's mouth is the static mouth of each expression (determined -> stunned -> shocked "O").

## Timing / staging
| g | what | caption |
|---|---|---|
| 1572-1605 | 20a: the EMPTY pillory on its platform, low warm sun from the WSW: long raking shadows of the steps / posts / board across planks and cobbles; slow push in (0.95 D) + tilt up | "ที่โดนจับ" 52.66 |
| 1606 | cut: reverse on kit, the pillory board behind him over his shoulder (left of his head), same sun | |
| 1606-1613 | kit studies it, hand on chin, head 3/4 to screen-left (kit_think) | "ก็โดนตอนบ่าย" 53.20 (g 1599) |
| 1614-1622 | eyes go WIDE (stunned, then shocked), hands drop and open, small squash-up, head snaps round to the lens | "ทั้งนั้น" 54.01 (g 1623) |
| 1622-1644 | holds the realisation (shocked) on a continuing slow push (head 237 -> 279 px); blink at 1610 | |
Two framings in 2.04 s (cut at 1.07 s / 0.97 s from the shot edges). Camera 22 mm; 20a pitch +4..+8 deg (low), 20b eye level ~0 deg.
Kit head 237-279 px (a medium close-up), centre x 507-545.
Popcheck: no pops outside the cut g 1606; no near-still frame pairs (median change 3.8 levels). No black / magenta frames, none retried.

## Colour (`work/qa.txt`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s20 shot 20 (g 1578-1638)                      41.6   13.8    0.9    0.4    0.1   25.3    9.4    8.6  0.41 0.64 0.04
s20 20a pillory (g 1572-1605)                  37.2   11.2    1.3    0.4    0.1   27.0   11.5   11.2  0.44 0.61 0.04
s20 20b kit (g 1606-1644)                      45.4   16.3    0.5    0.3    0.1   23.8    7.3    6.3  0.39 0.67 0.03
ref a t0062 t0072                              23.6   12.5    1.0    0.0    0.0   55.3    2.8    4.7  0.58 0.65 0.14
```
The set's market AFTERNOON look (bakery_API 5: red 37 orange 14 blue 34 violet 7, val 0.66, dark 0.02): low orange, few deep darks,
violet 7-11 from the blue-violet shade on the timber (shade is blue-violet, not magenta; magenta 6-11 is the red-pink timber / bunting).
Not graded per take; if the director wants it, warm / darken all market AFTERNOON shots alike in the conform.

## Seconds per frame
16.2 s wall / 24.5 s CPU mean (2 threads, two render processes at once). Kit sprite 512 px/D.

## Differences from the plan
- "kit's POV ... kit's eyes widen" is done as two framings: the empty pillory (his POV, the long afternoon shadows) then a reverse on
  kit in the square with the pillory behind him (his eyes widen). Kit is shown in the market (memory / realisation beat), not in the
  bakery window of shots 18-19.
- No crows / extra props added.
