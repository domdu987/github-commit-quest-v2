# QA s14 (shot 14, 28.922-31.853 s, film g 868..955, frames g 860..964)

Lane ADVANCE-Y. Set office, light office_day (INTERIOR_DAY). Final: 12 samples, 720x1280, 105 frames (handle_in 8 for the 11-frame dissolve from shot 13, handle_out 9 for the 13-frame match dissolve into s15). Script `shot.py` on `otake.py` (copied from s04, unchanged). Numbers from `work/qa.json` (`python3 qa.py .`) and `raw/meta/g_*.json`.

Map state (seen at the left edge in part a): red hand-drawn line (set track, u = 1), smudge halo 3, crumbs, chalk curve, six ghost tracks, tick, label 'ทางด่วนพายุ', spinner turning. Same as s17. All frames rendered 18 Nov 16:4x-17:5x, after the line switch and the voice change (no mouths in this shot).

## Timing (narration clock + 0.1 = film time)
| event | clock | film g |
|---|---|---|
| teletype feeds the sheet up (stepped, platen clacks) | 28.95-29.80 | 872-897 |
| hero blink | 29.60 | 891 |
| stamp lands on the teletype header ('ทางการ'), stamp layer appears | 29.82 | 898 |
| tear (teletype sheet hidden, chief holds the paper) | 29.95 | 902 |
| sheet quad takes over from the puppet paper (inside the crash) | - | 905 |
| thrust at the lens | 30.10 | 906 |
| crash push x3 | 29.85-30.30 | 899-912 (14 f), peak 416 px/frame at the corners, streaked 903-908 (plate + matte, actors sharp) |
| word pop 'ฝนตก' / 'ลมกระโชก' (4-frame scale 1.08 + bloom) | 30.85 / 31.30 | 928 / 942 |
| tilt down eases out, near still (slow creep) | 31.60 | 951 |

## Camera
- (a) window_tt (-3.2, -2.6, 2.1) -> (2.6, -1.0, 1.85), truck right 0.30 D (eased + creep share) with a push of 8 %/s; the aim pans back left 0.55 D so both men stay in frame.
- (b) crash push quint/sine onto `sheet_fill_camera` of the quad (fill 0.86 instead of 1.0, see below), small arc up.
- (c) tilt down from header + stamp to the two lines (look point 0.26 -> 0.065 D above the sheet centre), small push-in that dies away, creep after 31.6.
- qa_motion: static runs over 6 frames: none. Linear runs: none. One move 901-910.

## Heads and staging
| actor | frames | head width px | head centre y | x |
|---|---|---|---|---|
| hero (near, low, left; at (-0.45, -1.25), hero_tt moved 0.7 D back so he stays in frame through the push) | 860-904 | 261-336 in part a (435 at 904, leaving frame left in the crash) | 480-513 (0.38-0.40 H) | 211 -> 4 |
| chief (by the teletype at (2.35, -1.75), 1.7 D off the map wall, three-quarter yaw -0.35) | 860-964 | 141-168 in part a; behind the sheet in c (only hat and brow visible) | 497 in a (0.39 H) | 453-547 |
Whole heads above y = 880 in every frame. Nobody shows his back; no mouths.

## Pinned prop
- Rubber stamp (puppet prop 'stamp', near hand) pinned on the stamp spot of the teletype sheet header (world (3.28, -0.80, 2.48)) from g 860 to the tear (902): ready above, anticipation lift, 4-frame cubic-in drop, contact at 898. Registration error 0.0 px (max, 42 frames), solve error 0.0 D.

## Sheet framing (match to s15)
| g | 'ฝนตก' centre | 'ลมกระโชก' centre | sheet width |
|---|---|---|---|
| 912 | (360, 731) | (360, 879) | 629 px |
| 942 | (362, 626) | (362, 773) | 635 px |
| 956 (cut) | (367, 618) | (367, 765) | 638 px |
| 964 (end of handle) | (360, 620) | (360, 767) | 641 px |
s15 g 947-960 (first frames): 'ฝนตก' centre about (360, 600), about 450 px wide; 'ลมกระโชก' about (360, 750). Here 'ฝนตก' is about 440 px wide at (360, 620): the two lines land within 20 px of the newspaper's lines. Fill 0.86 instead of the props module's 1.0 because at 1.0 the second line (with its pop) ran past both frame edges and was larger than the newspaper's.

## Checks
- popcheck: no pops (max frame change 46.4 at the crash, median 7.3). Black or magenta cards: none. All 105 frames present (frames/g_0860..g_0964).
- Contact sheet `contact.jpg`; full-size frames viewed: g 870, 899, 906 (streaked), 960.
- hue_report (frames/):

| red | orange | yellow | green | cyan | blue | violet | magenta | sat | val | dark |
|---|---|---|---|---|---|---|---|---|---|---|
| 32.3 | 31.7 | 0.1 | 1.4 | 1.0 | 27.3 | 1.6 | 4.6 | 0.37 | 0.57 | 0.14 |
Everything in band except saturation 0.37 (band 0.38-0.48): half the take is the cream forecast sheet filling the frame (low-chroma paper). Shade on the sheet reads blue-violet (window-bar shadows), magenta 4.6.
- Seconds per frame: median 39 s wall / 39 s CPU at 2 threads (machine at load 8-13 from other lanes), max 68 s.

## Deviations
- Chief at (2.35, -1.75) instead of `chief_tt` (2.20, -1.95), so the stamp reaches the teletype header; sheet hold moved with him to (1.90, -2.00, 2.05), same facing (sheet_face direction, lit by the window).
- Hero at (-0.45, -1.25) instead of `hero_tt`: at hero_tt the 8 %/s push threw him out of frame before the stamp.
- Crash push starts at 29.85 (g 899), one frame after the stamp lands, so the stamp is seen in the wide (the plan has both at 29.82).
- Finger balls: two ink hand balls with a short ink arm on a card parented to the sheet's bottom edge (this folder's `work/hand_ball.png`); in g 905-908 the quad travels from the chief's hand to the hold inside the streak, the arm is not solved to it.
- The sheet's typed words are visible from the start (they are on the teletype sheet already) and pop at their words instead of appearing.
