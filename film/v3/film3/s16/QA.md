# s16 QA: film 3, shots 16-17 (NOON, the seam swells), harbor set NOON

Delivered: `take.mkv` = g 1455..1675 (221 frames, first_g 1455, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), from `frames/g_%04d.png` (not in git). g 1462..1675 = shots 16-17 ([g0, g1) = [1462, 1676)); g 1455..1461 = 7-frame in-handle for the 10-frame dissolve from shot 15 (shot 16's camera runs on before g 1462, rendered in 3D). No out-handle (hard cut to s18). `meta.json`, `cues.json` (cues in film seconds), `contact.jpg` (16 frames, labels above), `qa.json` (numbers below). Scripts: `shot.py` (take), `fx.py` (runtime set additions), `deliver.py` + `take_cfg.py`. Raw renders with per-frame json: `raw/s16` (g 1455-1587), `raw/s17` (g 1576-1675).

## Timing (g = round((t + 0.10) * 30); boundaries round(t * 30))
| event | g |
|---|---|
| shot 16 starts (dissolve in, handle from 1455) | 1462 |
| groans (bulge pulse +0.035 D, camera tremor peak) | 1495, 1540, 1570, 1610, 1650 |
| snap reframe on the first groan | 1490-1503 |
| "ขยายตัว" bulge speeds up / "ดันผนังเหล็ก" crane back and down to the low angle up the wall | 1509 / 1530-1552 |
| drips land in the bucket | 1493, 1541, 1585, 1629, 1673 |
| dissolve 16 -> 17, 9 frames, smoothstep, centred on 1582 (mixed inside the take) | 1578-1586 |
| trembling rivet (row of seam 1, right of the bucket seam) rattles and creeps out | 1590-1675 |
| pull back: tommy's worried face rises into the near foreground, lands on "ทุกวัน" | 1601-1617 |
| tommy's eyes go wide (worried -> stunned behind a blink) | 1641-1643 |
Framing changes: 1462, 1490-1503, 1530-1552, (dissolve) 1578-1586, 1601-1617, groan jolts 1650; the longest gap is 1617 -> 1675 (1.9 s, slow push + tremor + rivet/eye action).

## Camera (fastest of 9 screen points re-projected at 4 D, px/frame)
| shot | min | median | peak | static runs (>= 6 f) | constant-speed runs |
|---|---|---|---|---|---|
| 16 | 0.63 | 5.8 | 255 (g 1540, crane) | none | none |
| 17 | 0.39 | 3.6 | 133 (g 1608, pull back) | none | none |

## Staging
- tommy (shot 17, head_flip True: key from screen-right): head 377-409 px wide, centre x 189-214, y 582-621 (0.45-0.49 H) from g 1612 on; whole head above y 880 from g 1611. g 1602-1610 his head rises in from the bottom-left corner during the pull back (transit frames, head partly below 880 for those 9 frames). No mouth movement (worried / stunned), nobody's back to the camera.
- Popcheck (mean abs diff vs running median): flags only at g 1496-1498 (snap reframe) and 1610-1611 (pull back), both intended moves. No near-still runs.

## Colour (`hue_report.stats` on the final frames)
```
                         red orange blue violet magenta  sat  val  dark
shot 16 (g 1462-1581)   62.7   0.8  34.2   1.2   1.2   0.50 0.53 0.06
shot 17 (g 1582-1675)   73.0  16.5   5.7   0.5   4.3   0.46 0.53 0.10
all (g 1455-1675)       66.7   7.0  22.8   1.0   2.4   0.48 0.53 0.08
```
Red is above band and orange below: the brown-painted tank fills these close shots (harbor_REVIEW.md section 2 predicts it: the paint renders at hue 16-24). Shade blue-violet, magenta in band. Darks: shot 16 0.06 (raking views with sky), shot 17 0.10 (in band; tommy's shadow and the bucket side).

Seconds per frame: 12.2 s wall / 24.0 s CPU mean (2 threads, another render running alongside).

## Differences from the plan / runtime set changes
- Bulge: `tank_patch` is hidden and replaced at runtime by a fine (90 x 105) copy with the same art that swells outward (0.04 -> 0.44 D, a broad swell on the seam crossing plus a sharp ridge along the horizontal seam), with groan pulses. Seep strips follow it (extra shape key) and no longer cast offset shadows.
- 3D rivet heads (domes) over the painted rivets near the bucket seam, so one can tremble (shot 17) and they can fly in s18.
- The set's dot drop is replaced by an elongated glossy drop that forms at the strip end, stretches, falls into the bucket and leaves a ring (WORKER3 note).
- No steam/haze cards: tested, did not read at this scale; the swelling is carried by the silhouette (raking view) and the groan tremor.
- Shot 16 starts raking along the wall (not frontal seam_insert) because a frontal view cannot show the swell; it ends on the low angle up the wall (tank_low side).
- Shot 17's close is on the rivets of the seam crossing; tommy stands 1.2 D from the wall beside the bucket (bucket fill 0.72, put back by him in winter).
