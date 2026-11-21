# QA.md: film 23 take s08 (shot S08, LANE morning)

Frames g 822 .. 936 (115 frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g 822 .. 906, render with the x1.25 tail to g 927 (exclusive), handles in 0 / out 10.
Transition in: {'type': 'cut', 'frames': 0}. Wall time 25.3 s per frame (2 render processes at once, 2 threads each).

## Automatic checks
- ground_check: see GROUND.md (every 10th frame + first + last).
- qa_auto.py: exit 0 (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg.
- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):
```
overall median jitter px 0.08
```
- Frame difference on 90x160 grey inside the shot: median 1.50 (rule >= 4), p90 1.93 (rule >= 12), min 0.62.
- Shade hue (target 240-260): first g822 251.3 (16% of px); mid g874 250.5 (17% of px); last g926 250.1 (17% of px)

## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)
| actor | y min | y max | x min | x max |
|---|---|---|---|---|
| driver | 770 | 777 | 462 | 669 |
| major | 575 | 620 | 294 | 350 |
| sol | 522 | 557 | 170 | 175 |
| clip | 510 | 547 | 257 | 285 |
| pm | 490 | 522 | 136 | 141 |

## qa_auto output
```
# QA_AUTO PASS  (take_s08.mkv, 115 frames, 30.00 fps, g 822-936)

## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.

```
