# QA.md: film 23 take s05 (shot S05, LANE morning)

Frames g 486 .. 656 (171 frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g 486 .. 616, render with the x1.25 tail to g 649 (exclusive), handles in 0 / out 8.
Transition in: {'type': 'cut', 'frames': 0}. Wall time 12.2 s per frame (2 render processes at once, 2 threads each).

## Automatic checks
- ground_check: see GROUND.md (every 10th frame + first + last).
- qa_auto.py: exit 0 (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg.
- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):
```
overall median jitter px 0.2
```
- Frame difference on 90x160 grey inside the shot: median 6.67 (rule >= 4), p90 10.08 (rule >= 12), min 1.87.
- Shade hue (target 240-260): first g486 238.7 (8% of px); mid g567 257.2 (9% of px); last g648 251.0 (7% of px)

## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)
| actor | y min | y max | x min | x max |
|---|---|---|---|---|
| m00 | -258913 | 15295 | -94814 | 1675561 |
| m01 | -10569 | 47977 | -319732 | 76140 |
| m02 | -8228 | 17992 | -128313 | 66778 |
| m03 | 633 | 914 | -995 | 811 |
| m04 | -56790 | 5617 | -72750 | 833366 |
| m05 | -3133 | 61336 | -971813 | 61092 |
| m06 | 558 | 1062 | -5609 | 442 |
| m07 | 529 | 757 | -510 | 704 |
| m08 | -2215 | 50423 | -1223023 | 69402 |
| m09 | -1620 | 40154 | -1199651 | 70497 |
| m10 | 500 | 829 | -4790 | 301 |
| m11 | 485 | 734 | -989 | 520 |

## qa_auto output
```
# QA_AUTO PASS  (take_s05.mkv, 171 frames, 30.00 fps, g 486-656)

## Notes
- soft frames (check by eye; motion streak allowed 1-3 frames): g [495, 496, 497, 498, 499, 500, 501]
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.

```
