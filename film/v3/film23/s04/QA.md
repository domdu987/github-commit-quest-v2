# QA.md: film 23 take s04 (shot S04, LANE morning)

Frames g 349 .. 518 (170 frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g 357 .. 486, render with the x1.25 tail to g 519 (exclusive), handles in 8 / out 0.
Transition in: {'type': 'dissolve', 'frames': 11}. Wall time 15.2 s per frame (2 render processes at once, 2 threads each).

## Automatic checks
- ground_check: see GROUND.md (every 10th frame + first + last).
- qa_auto.py: exit 0 (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg.
- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):
```
overall median jitter px 0.16
```
- Frame difference on 90x160 grey inside the shot: median 3.76 (rule >= 4), p90 9.75 (rule >= 12), min 1.10.
- Shade hue (target 240-260): first g357 251.9 (21% of px); mid g438 252.8 (20% of px); last g518 251.8 (7% of px)

## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)
| actor | y min | y max | x min | x max |
|---|---|---|---|---|
| painter | 585 | 645 | 309 | 412 |
| pumper | 620 | 697 | 23 | 224 |
| designer | 614 | 689 | 155 | 261 |
| sound | 653 | 688 | 343 | 670 |

## qa_auto output
```
# QA_AUTO PASS  (take_s04.mkv, 170 frames, 30.00 fps, g 349-518)

## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.

```
