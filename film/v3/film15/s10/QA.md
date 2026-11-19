# QA s10 (film 15, render team 3): shots 10-16, g 489..931 (+6 in, +8 out handle: take g 483..939, 457 frames)
Set3d15 A GOLDEN (shot 16: GOLDEN -> DAY season dissolve g 897-907 baked in, two plates blended). Cast15 cards per frame (c15.py), 12 samples, 720x1280, ~11 s/frame wall.
## Numbers
- motion_check (cuts 489,564,621,708,762,838,862,932): **median 5.5, p90 13.2** (r3) (target 4 / 12). Per shot median: 10: 2.9 | 11: 5.8 | 12: 10.9 | 13: 2.5 | 14: 5.3 | 15: 11.8 | 16: 8.4. Shots 10 and 13 are the low ones (framing limits: the sway/orbit had to stay small to keep the group / photographer in frame); no frozen runs (qa_auto PASS).
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

## r2 (director take-gate fixes)
- Shot 11: coach neck mime (head tilted, hands at the collar) g564-596, then points at Dick (eye-line on Dick); Dick on the grass at ~20 % height, boys behind; the set's flat green ground patch is hidden in this shot.
- Shot 14: my own newspaper card (grey bars, big photo of the arched Dick, head below a tan bar) over the cast prop, ~70 % of the frame width; reader's thumbs at its edges; the seated spectator is removed.
- Shot 15: coach_laugh (eyes squeezed, tears, 3 Hz bounce, mouth shut).
- Shot 16: camera head-on to the bar, boy at the left standard (in frame) slides the peg: bar 1.72 m -> 1.98 m at g 886-906 (GOLDEN), DAY plate holds 1.98 then 2.14; Dick's hip arc follows the bar height.
- Shot 13: 22 % push-in at g 729-741 (arch at the flash is larger).
- Per-shot median/p90: 10: 2.9/6.2 | 11: 4.8/10.8 | 12: 10.9/14.7 | 13: 3.1/13.4 | 14: 7.9/11.9 | 15: 9.0/12.2 | 16: 4.1/5.7. qa_auto PASS.

## r3 (director polish)
- Shot 11 g564-596: both hands clutch his own throat (hand targets rebuilt, small tremble), head tilted ~34 deg, talking mouth (quote window), 18 % push-in at g564; point at Dick g606-620 unchanged. Coach moved toward the lens axis so the push does not crop him.
- Shot 16 g884-906: boy's right hand rides up with the bar (reach 0.4 -> 1.35 D above the shoulder line), eyes open ('excited'), 20 % push-in at g884; camera shifted left so boy + standard stay in frame through the push.
- Extra motion to keep p90 >= 12: shot 12 push 18 %/s, slide 100, orbit 14; shot 15 push 45 %.
- Per-shot median/p90: 10: 2.9/6.2 | 11: 4.4/7.4 | 12: 12.1/16.5 | 13: 3.1/13.4 | 14: 7.9/11.9 | 15: 9.2/11.8 | 16: 4.5/8.1. qa_auto PASS (it still flags g489, 564, 621, 862 as 'no visible change'; all are real cuts / the dissolve-free start of shot 16).
