# QA.md: film 23 take s02 (shot S02, LANE morning)

Frames g 112 .. 284 (173 frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g 120 .. 252, render with the x1.25 tail to g 285 (exclusive), handles in 8 / out 0.
Transition in: {'type': 'dissolve', 'frames': 11}. Wall time 11.2 s per frame (2 render processes at once, 2 threads each).

## Automatic checks
- ground_check: see GROUND.md (every 10th frame + first + last).
- qa_auto.py: exit 0 (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg.
- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):
```
overall median jitter px 0.11
```
- Frame difference on 90x160 grey inside the shot: median 2.19 (rule >= 4), p90 2.72 (rule >= 12), min 1.14.
- Shade hue (target 240-260): first g120 246.8 (8% of px); mid g202 246.0 (7% of px); last g284 247.9 (26% of px)

## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)
| actor | y min | y max | x min | x max |
|---|---|---|---|---|
| polisher | 668 | 690 | 561 | 636 |
| saluter | 684 | 705 | 435 | 532 |
| stand1 | 690 | 702 | 456 | 510 |
| carry1 | 680 | 694 | -47 | 159 |

## qa_auto output
```
# QA_AUTO PASS  (take_s02.mkv, 173 frames, 30.00 fps, g 112-284)

## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.

```
