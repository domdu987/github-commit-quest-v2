# T5 + T6 QA (44.38-60.15 s, g 1331-1804, take.mkv g 1325-1810, 486 frames, 720x1280, 12 spl)
Render: ~24 s/frame/process (2 procs x 2 threads); coach-in-stands close-up frames ~60 s. Script: shot.py (one camera path, no cut between T5 and T6).
## Numbers
- qa_auto: PASS (magenta 0.0 %; soft g1782-1795 = the directional-blur whip fly to the coach, 5 sub-frames per frame, no pops).
- motion_check: median 9.5, p90 22.2.  qa_stats2: sat 0.748, vivid 76.8 %, luma 106.2 (post eq brightness -0.012), warm 28.4 / cool 60.9 %.
## Beats (narration clock, frame = round(t*30))
head over bar 46.4 (g1392), back 47.2 (g1416), legs 47.8 (g1434); arch hold 47.8-50.3; rival face-down straddle plate 50.35-52.85 with 7-frame match dissolves both ways (g1511-1518, g1584-1591); Dick flicks over and drops 52.9-54.0; lies 53.75-55.3, sits up from 55.35; bar never moves in T6; crowd cheer ramp + flashes from 57.3; Dick->podium plate dissolve 57.75-58.25 (high crane); podium medal 58.4-59.4; whip fly to coach 59.4-59.8; close-up 3 (coach jaw drop) 59.8-60.15 (+ handles).
## Angles
side ride-along low 1325-1390; hover track 1390-1434; slow orbit on arch 1434-1511 (arch 60-70 % of width, head and legs hanging below the bar, floodlight rim); same framing straddle plate 1511-1591; drop follow 1591-1645; top-down-ish crane over the mat 1645-1722; crane up and out 1722-1745; descent to podium 1745-1782; whip + close-up 1782-1810.
## Close-up: g1795-1810 (coach, ~0.5 s hold). No BIGZOOM in this take.
## Differs from plan / known issues
- Dick on the mat is small in 1645-1720 (top-down crane); bar sits at the lower frame edge there.
- Coach close-up: black canopy-underside band top-left and bare seats lower third (set limit); it is a 0.5 s punch.
- Officials table / kit bags (merged set meshes officials_*, kit_*) hidden at runtime so they do not cross the lens; sprites are per-process (shared PNG caused magenta card holes, plus retry-on-magenta in shot.py).
- Bar 2.24 m. Exposure +0.3 during the eruption (TENSE preset kept).

## Round 3 (director gate FIX) applied
1) take-off g1398-1408: head path lowered 0.2 m and card pushed in front of the bar, face clear. 2) flick g1604-1612: drop stays in front of the bar until low, then moves to the mat; face clear. 3) landing g1612-1645: camera now over the bar, closer (lens 29), Dick lies in frame (about 60 % of width, 12-15 % tall), sits up centred. 4) whip g1782-1795: continuous arc path + 5-sub-frame directional blur. 5) close-up g1795-1810: lens 100, face ~22-25 %, navy backdrop removes the black band, seat rows filled. 6) top-down pushed in (cam y 10.2-10.8, lens 29); gold medal: podium Dick scaled 1.25 and camera closer; exposure -0.15 EV g1745-1775.
Remaining: lower third of the close-up still shows plain stand treads; lying Dick is a thin strip by nature (side view).
