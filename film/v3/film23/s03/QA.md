# QA.md: film 23 take s03 (shot S03, LANE morning)

Frames g 252 .. 391 (140 frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g 252 .. 357, render with the x1.25 tail to g 384 (exclusive), handles in 0 / out 8.
Transition in: {'type': 'cut', 'frames': 0}. Wall time 12.4 s per frame (2 render processes at once, 2 threads each).

## Automatic checks
- ground_check: see GROUND.md (every 10th frame + first + last).
- qa_auto.py: exit 0 (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg.
- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):
```
overall median jitter px 0.1
```
- Frame difference on 90x160 grey inside the shot: median 1.67 (rule >= 4), p90 2.57 (rule >= 12), min 0.79.
- Shade hue (target 240-260): first g252 252.6 (10% of px); mid g318 250.3 (11% of px); last g383 243.1 (9% of px)

## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)
| actor | y min | y max | x min | x max |
|---|---|---|---|---|
| pricker | 606 | 621 | 398 | 560 |
| pumper | 624 | 638 | 37 | 74 |
| clip | 600 | 611 | 122 | 144 |

## qa_auto output
```
# QA_AUTO PASS  (take_s03.mkv, 140 frames, 30.00 fps, g 252-391)

## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.

```
