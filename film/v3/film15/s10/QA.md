# QA s10 (film 15, render team 3): shots 10-16, g 489..931 (+6 in, +8 out handle: take g 483..939, 457 frames)
Set3d15 A GOLDEN (shot 16: GOLDEN -> DAY season dissolve g 897-907 baked in, two plates blended). Cast15 cards per frame (c15.py), 12 samples, 720x1280, ~11 s/frame wall.
## Numbers
- motion_check (cuts 489,564,621,708,762,838,862,932): **median 5.5, p90 13.1** (target 4 / 12). Per shot median: 10: 2.9 | 11: 5.8 | 12: 10.9 | 13: 2.5 | 14: 5.3 | 15: 11.8 | 16: 8.4. Shots 10 and 13 are the low ones (framing limits: the sway/orbit had to stay small to keep the group / photographer in frame); no frozen runs (qa_auto PASS).
- qa_auto: PASS, magenta 0.0 %, phone_sheet.jpg, QA_AUTO.md.
## Checked
- Heads above y 880 in every shot; the coach talks only g 537..710 (17.80-23.55 s) in shots 10-12 (talk_mouth); all other mouths static; the bar does not fall (shots 10-16 are clean flops); no letters/numbers (newspaper = grey bars + arched photo).
- Shot 13: flash_bulb at g 741 (24.6 s), Dick at the flop apex over the bar at g 741, bar-anchor on the bar; photographer flash burst g 741-744; spray at the landing g 753.
- Shot 16: GOLDEN plate flop g 866, bar raised by the boy after it (boy is outside the frame), season change dissolve g 897-907 (green leaves, blue sky), DAY plate second flop g 916.
## Differs from the plan / known
- Cameras reframed from the table (closer: 10, 12, 13, 14, 16) so figures read; orbit/push/sway added for the rhythm rule. Shot 11: coach is a large FG card at the right edge (over-shoulder as a front-drawn card).
- Shot 14: reader is boy1 with sit_read, a seated crowd4 laughing at the right edge; no reader's-thumb FG (no cast piece).
- Shot 16: the boy raising the peg stands at the right standard (mostly off frame); the sawdust pile of the set is large in frame.
- Dick's flop at 13/16 is small in frame (wide shots, ~12 % of the height at the apex) because the camera has to keep photographer / bar / pit together.
- Fixed in the take: flash_bulb's unlit bulb renders as a black ball -> hidden except on the flash frames.
