# s23 QA: film 16, shot 23 (callback of shot 1) -- LINE line_close, AFTER_RAIN

Method of s01 reused (shot.py is s01's with new timing; the 3D bottle copy pinned to the fist, set bottle switched on at the contact frame, per-frame slack wire, set spans + wrap ring on at the drape).

## Delivered
- take.mkv: 103 frames, g 1446..1548 (shot = g 1455..1539; 9 handle frames each side), libx264rgb crf 6, 22.2 MB.
- Cut in at g 1455, hard cut out at g 1540 (meta.json transition_in/out).
- cues.json, contact.jpg, framediff.json, QA_AUTO.md (PASS) + phone_sheet.jpg.

## Beats (event g = round((t+0.10)*30))
| g | beat |
|---|---|
| 1446-1472 | bottle held up over the bare pole top (caption "เขาเลยคว่ำ" 1458); camera already moving |
| 1473-1486 | SNAP x3.0 + 1.2 D pan (13 f) on "คอขวดเบียร์" 1475; sun glint 1475-1482 |
| 1484-1494 | lowered mouth-down; contact 1494 (just before "บนหัวเสา" 1495): set peg + glass + star on, copy off, flare 1494-1503 |
| 1498-1500 | blink, pose cap -> drape on the closed frame 1499 |
| 1505-1520 | hand takes the wire, flicks it over the glass ("แล้วพาดลวด" 1509), settles |
| 1521 | set wire spans + wrap ring on, slack wire off; happy from 1522 |

## Checked
- Same marks (morse_ladder) and camera start as s01; light AFTER_RAIN (wet set, puddles).
- Heads [90, 304] px wide, centre y [396, 588], lowest head bottom 713: none reaches the caption band (y 880).
- No text, no DOF, mouths still (no quote). Hands: pinned to bottle neck / wire (hand error 0 except the intended wire overshoot g 1517-1519).
- No magenta; no retried frames.

## Frame-diff (in-shot g 1456..1539, 90x160 grey)
median 7.14  p90 11.39  (target >= 4 / >= 12). The p90 is just under target: the snap is 13 f, x3.0 with pan; 360x640 draft gave 11.55.

## Differs from plan / notes
- Camera drifts harder than s01 (slide 75 px/s, arc 20 deg/s, push 10 %/s) to carry the longer 2.8 s shot; the glass drifts to the left edge in the last 20 frames but stays in frame.
- During the flick his raised hand crosses his face (same as s01).
- 7.53 s/frame wall, 14.42 s CPU (720x1280, 7 spp, 2 procs x 2 threads).
