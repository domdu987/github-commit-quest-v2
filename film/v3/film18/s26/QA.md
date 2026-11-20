# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 10.1 s wall/frame (median 10.1); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 6.86, p90 8.56** (min 2.56, max 9.35), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 68.

## TAKE-gate round 2 fixes (director message + QA-art notes)
- General at 49-55 % of the frame height (camera at 0.95 D, 4.3-4.9 D from him, ~35 % closer than before); head top y 268-371, chin <= 520.
- Road is warm dawn dirt for the WHOLE take: the group now starts near the wall (the set's warm light weights fade to blue far from the wall) and travels only 31 D.
- Panic face: round stunned eyes (small pupils), brows up, sweat drop, closed grimace; forward lean 21; head turned to profile g 2070-2080; cup held out at arm's length on a red sleeve (the drawn arm ends behind the cup, no dark arm over the face).
- Camera: slow eased pull (4.3 -> 4.9 D) with the tracking + a lateral weave, then ONE held push-in of +19 % from g 2068 (eased over 10 frames) held through the hard cut. No pulses.
- Four front-3/4 dragon oxen directly behind him gaining from 9-16 D to 2.6-7.8 D by g 2085, grey tail smoke, no flame. All set dressing rocks / wheels / hay / pots / baskets hidden (also the 'fgwood.001' etc.).
## Deviations
- p90 8.6 is just under the 9 guide. A drawn HAND is not visible: the arm's sleeve ends behind the cup (the cast draws the cup in front of the fist).
- No out handle (hard cut at the film end). Ground-dressing helper (J.dress_ground) was not yet on film18/main when this was rendered, so the road is plain dirt with silk strips.

