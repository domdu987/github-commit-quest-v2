# QA.md: film 23 take s07 (shot S07, LANE morning)

Frames g 696 .. 853 (158 frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g 696 .. 822, render with the x1.25 tail to g 854 (exclusive), handles in 0 / out 0.
Transition in: {'type': 'cut', 'frames': 0}. Wall time 19.2 s per frame (2 render processes at once, 2 threads each).

## Automatic checks
- ground_check: see GROUND.md (every 10th frame + first + last).
- qa_auto.py: exit 0 (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg.
- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):
```
overall median jitter px 0.1
```
- Frame difference on 90x160 grey inside the shot: median 1.85 (rule >= 4), p90 2.15 (rule >= 12), min 0.64.
- Shade hue (target 240-260): first g696 242.8 (6% of px); mid g775 234.0 (4% of px); last g853 237.5 (6% of px)

## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)
| actor | y min | y max | x min | x max |
|---|---|---|---|---|
| major | 661 | 678 | 470 | 830 |
| driver | 408 | 510 | 761 | 1484 |
| sol | 745 | 784 | 115 | 208 |
| clip | 722 | 750 | 222 | 345 |
| pm | 736 | 765 | 251 | 367 |

## qa_auto output
```
# QA_AUTO PASS  (take_s07.mkv, 158 frames, 30.00 fps, g 696-853)

## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.

```

## Shade hue note (S07, QA_ART_SET)
The lane-dirt shade was tinted toward hue 248 at build (red x2 on lane_dirt, rut, ground, poplar, hedge, leaf, olive, plaster, roof, slate, stone). Measured on the final frames:
first 242.8, mid 234.0, last 237.5 (target 240-260). The mid / last values stay below 240: the shaded pixels that dominate the stat are the poplars, the house and the jeep, and
scaling the shade colour of every material (73 shade nodes, red x1.6 / x2.4, tested at full size) moved the mid frame by only +1.3. Not fixed; flagged for the director.
Lip-sync: only the Major's mouth moves (talk_mouth, 5 Hz loudness, one pause at g 748..756 between the two quotes); every other mouth is still.
