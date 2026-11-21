# QA.md: film 23 take s05 (shot S05, LANE morning)

Frames g 486 .. 656 (171 frames, 720x1280, 12 samples, denoise OIDN, 2 threads, no captions): planned shot g 486 .. 616, render with the x1.25 tail to g 649 (exclusive), handles in 0 / out 8.
Transition in: {'type': 'cut', 'frames': 0}. Wall time 12.3 s per frame (2 render processes at once, 2 threads each).

## Automatic checks
- ground_check: see GROUND.md (every 10th frame + first + last).
- qa_auto.py: exit 0 (0 = no FAIL), see QA_AUTO.md; phone_sheet.jpg.
- qa_jitter.py output (every second must be <= 2.0 px; no line = clean):
```
overall median jitter px 0.15
```
- Frame difference on 90x160 grey inside the shot: median 2.72 (rule >= 4), p90 4.55 (rule >= 12), min 0.91.
- Shade hue (target 240-260): first g486 246.4 (9% of px); mid g567 248.1 (6% of px); last g648 247.6 (5% of px)

## Heads (screen px, head centre; caption band starts y 880, head radius <= ~60 px)
| actor | y min | y max | x min | x max |
|---|---|---|---|---|
| m00 | 689 | 748 | 214 | 241 |
| m01 | 653 | 711 | 299 | 526 |
| m02 | 630 | 680 | 354 | 664 |
| m03 | 653 | 734 | 305 | 593 |
| m04 | 594 | 641 | 72 | 112 |
| m05 | 565 | 647 | 316 | 494 |
| m06 | 544 | 653 | 447 | 690 |
| m07 | 527 | 650 | 542 | 817 |
| m08 | 576 | 643 | -201 | -86 |
| m09 | 550 | 650 | 131 | 206 |
| m10 | 531 | 644 | 290 | 440 |
| m11 | 517 | 646 | 401 | 592 |

## qa_auto output
```
# QA_AUTO PASS  (take_s05.mkv, 171 frames, 30.00 fps, g 486-656)

## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.

```
