# QA.md: film 23 take s06 (shot S06, LANE morning)

Frames g 610 .. 715 (106 frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g 618 .. 696, render with the x1.25 tail to g 716 (exclusive), handles in 8 / out 0.
Transition in: {'type': 'dissolve', 'frames': 11}. Wall time 15.3 s per frame (2 render processes at once, 2 threads each).

## Automatic checks
- ground_check: see GROUND.md (every 10th frame + first + last).
- qa_auto.py: exit 0 (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg.
- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):
```
overall median jitter px 0.13
```
- Frame difference on 90x160 grey inside the shot: median 1.85 (rule >= 4), p90 4.26 (rule >= 12), min 0.77.
- Shade hue (target 240-260): first g618 258.2 (8% of px); mid g667 254.2 (11% of px); last g715 243.5 (9% of px)

## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)
| actor | y min | y max | x min | x max |
|---|---|---|---|---|
| major | 431 | 489 | 93 | 768 |
| driver | 420 | 474 | 249 | 862 |
| clip | 654 | 658 | 184 | 311 |
| sol | 642 | 643 | 532 | 724 |

## qa_auto output
```
# QA_AUTO PASS  (take_s06.mkv, 106 frames, 30.00 fps, g 610-715)

## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.

```
