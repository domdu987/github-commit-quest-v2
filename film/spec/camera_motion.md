# Camera, staging, motion and editing spec (lens: camera-motion)

Reference: clip A "Why Perfect Railroads Don't Work" (1956 frames, 65.2 s) and clip B "The Ancient Jar That Warned an Empire" (1946 frames, 64.9 s), both 720x1280 at 30 fps.
All pixel values are at 720x1280. W = 720, H = 1280. D = head diameter (outer, including ink). `fNNNN` = 0-based frame index at 30 fps (t = f / 30). `a/tSS.S`, `b/tSS.S` = the half-second reference stills.

Evidence and scripts (all re-runnable):
- frames: `ref/extra/camera-motion/lowA|lowB/` (every frame, 360x640), `fullA|fullB/` (selected ranges, 720x1280, file name = frame index)
- scripts: `ref/extra/camera-motion/scripts/` (`shots.py`, `alpha.py`, `gmotion.py`, `shotstats.py`, `beats.py`, `easing.py`, `heads.py`, `framing.py`, `vp.py`, `vp1.py`, `holds.py`, `headtrack.py`, `facediff.py`, `final_stats.py`, `shots_def.py` = the transition table)
- per-frame camera motion: `ref/extra/camera-motion/gmA.npy`, `gmB.npy` (similarity transform frame to frame from 600 tracked features + RANSAC; columns: frame, scale, rotation deg, centre tx, centre ty at 360x640, inliers, n, median flow, p90 flow)
- pictures: `ref/crops/camera-motion/` (`sheet_*`, `rowsA_*`, `rowsB_*`, `trA_*`, `gm_A_0.png` ... `gm_B_1.png` = zoom and pan rate plots with transitions marked, `framing_a.jpg`, `framing_b.jpg`, `vp1_montage.jpg`, `grid_*.jpg`, `cs_*.jpg`, `blur_1.jpg`, `blur_2.jpg`, `v1_grid.jpg`)

How motion was measured. "Zoom rate" = (scale - 1) x 30 x 100 in percent per second of the fitted background similarity transform (positive = things get bigger = push-in). "Pan" = translation of the frame centre in px/s. "Corner speed" = |zoom rate| / 100 x 734 px + pan speed, i.e. how fast the picture moves at a frame corner; it is the single number used to separate snap moves (> 450 px/s) from drifts. The fit follows the dominant textured layer (the background), so it is camera motion, not character motion. It is unreliable inside dissolves and for 17 (A) and 3 (B) frames where tracking failed.

Limits, stated up front. (1) Horizontal field of view could only be measured on clip A, where rails and sleepers give two orthogonal vanishing points. Clip B backgrounds are one-point-perspective paintings, so only the horizon height is measurable there. (2) Whether mouths follow the audio was tested only against the loudness envelope on three shots. (3) Per-shot move labels in the shot tables combine the motion plots with looking at the strips; the numbers are measured, the labels are my reading.

---

## 1. Observations

### 1.1 The camera almost never stops
- Fully static frames (zoom < 1.5 %/s and pan < 8 px/s) are 3.8 % of in-shot frames in A and 5.5 % in B. Holds of 6 frames or more: 4 in A totalling 1.30 s, 3 in B totalling 1.03 s, longest 0.47 s (A f1718-1731, the glowing rail just before the hero drops in).
- Only one shot in 38 is close to locked off: B shot 17, the inventor walking away at night (b/t44.0-t45.5, f1315-1376): zoom -2.2 %/s, pan 4 px/s. The character's walk cycle supplies the motion there.
- Time budget: A = 44 % snap moves, 44 % drift, 8 % inside transitions, 4 % near static. B = 17 % snap moves, 64 % drift, 11 % inside transitions, 8 % near static. Clip A is the hyperactive one (median corner speed 332 px/s), clip B is calmer (150 px/s).

### 1.2 Two kinds of camera move
- Drift: a slow push-in, pull-out or sideways slide that fills the time between events. Median 7.8 %/s zoom in A and 7.6 %/s in B (interquartile 2.5-17.5 and 3.0-13.6), with 30-33 px/s of pan. Direction: A pushes in 59 % of drift frames and pulls out 19 %; B is balanced, 39 % in and 45 % out.
- Snap: a fast reframing inside the shot, 0.3 to 1.1 s long, that changes the picture as much as a cut would. A has 36 of them (median 24.5 frames, interquartile 13-32), B has 22 (median 13.5 frames, interquartile 9-20). Typical size: scale x1.5 to x3 or the inverse, often combined with 150-700 px of pan or tilt. Examples: A f418-445 tilt up and push x2.56 into the low-angle boss close-up; A f541-588 pull back x0.50 and pan 941 px to open the two-shot; A f1738-1751 crash pull-out x0.27 (`rowsA_1.jpg` rows 4-5); B f21-30 whip-push x3.59 onto the dragon head (`blur_1.jpg`); B f625-649 crash pull-out x0.10 from the goblet to the throne.
- Counting dissolves, cuts and snaps together, the framing changes every 1.19 s (median) in A and every 1.26 s in B (mean 1.25 and 1.54 s). This is the pacing number that matters more than shot length.

### 1.3 Moves are eased, not linear
- Snap moves: the speed profile peaks at 1.71 x its mean (interquartile 1.56-2.09, n = 61) and the peak sits at 0.50 of the move (interquartile 0.33-0.67). A linear move would give 1.00; smoothstep gives 1.50, sine in-out 1.57, quintic 1.88. So snaps are symmetric ease-in ease-out, between sine and quintic.
- Drifts are eased too and die out before the shot ends. Zoom rate in the first quarter, middle half and last quarter of the shot: B throne +30.0 / +6.7 / -1.6 %/s (f729-802), B underground -14.4 / -7.5 / 0.0 (f1865-1945), A sunset bridge +64.8 / +24.3 / -2.3 (f1792-1882), B inventor +6.5 / +16.5 / +2.7 (f95-145), B wall +11.6 / +17.4 / +1.7 (f1221-1304), A macro gap +9.0 / +23.8 / +0.3 (f1160-1255). Six of eight sampled drifts end below 3 %/s. Only the 0.8 s camp shot is constant (+8.0 / +8.4 / +7.7, B f964-987).
- Clip A shots arrive moving and settle: median corner speed 645-872 px/s in the first 0.8 s of a shot against 66-137 px/s in the last 0.8 s. Clip B is flatter (106-207 at the start, 72-159 at the end).
- Horizon roll is about zero where measurable (A t16.0 +0.25 deg, t20.0 -0.5 deg, t21.0 +0.2 deg from the two vanishing points). No Dutch angles were found. The one rotating shot is the top-down pendulum interior (B f1468-1663, -94 deg of roll in 6.5 s).
- One shot has deliberate camera shake: the sweating passenger in the train window (A f894-930), about 5 Hz, 12 px per frame standard deviation, 86 px peak to peak.

### 1.4 Editing
- A has 16 shots (mean 3.75 s, median 3.65 s, range 0.70-7.73 s). B has 22 shots (mean 2.62 s, median 2.45 s, range 0.40-6.53 s).
- 29 of 36 transitions (81 %) are cross-dissolves: 11 in A, 9 to 17 frames, median 13; 18 in B, 9 to 23 frames, median 10.5. The mix curve is a smoothstep, not linear: measured mix per frame at A f346-357 is 0.02, 0.07, 0.14, 0.22, 0.35, 0.47, 0.60, 0.72, 0.82, 0.90, 0.95, 0.99, which matches a 12-frame smoothstep to within 0.04.
- Both shots keep moving through the dissolve; the incoming shot is already in motion on its first visible frame (`trA_344.jpg`, `trB_802.jpg`).
- The other 7 transitions: 2 plain hard cuts (A f1322, B f93), 1 punch-in cut with speed lines (B f146-147), 1 whip pan (B f160-166, 7 frames, `blur_1.jpg` row 2), 1 wipe by a foreground object, the train crossing the lens (A f111-113), 1 cut hidden inside a fast tilt (A f276-277), 1 white explosion flash (A f1930-1934).
- Long takes are common: A shot 5 (13.83-21.50 s) holds one continuous take through five reframings, from the workers to the boss close-up, the purple face and the two-shot (`rowsA_3.jpg`).
- Inference, not proven: the shots look like separately generated 2-8 s clips joined by short dissolves.

### 1.5 Lens and camera height
- Clip A is a wide lens. Focal length from rail and sleeper vanishing points, principal point assumed at the frame centre: 622-870 px over seven frames (A t13.5 767, t14.0 622, t16.0 662, t19.5 787, t20.0 793, t21.0 838, t37.0 870), median 787 px. That is 49 deg horizontal and 78 deg vertical (range 45-60 deg horizontal).
- Clip B: cannot be determined. Sets are frontal one-point-perspective paintings; the orbit around the jar (b/t08.5 to b/t11.0, `grid_jar.jpg`) shows real parallax and the jar base reads about 11 % wider than its shoulder, which suggests a moderately wide lens, but I could not turn that into a number.
- Camera height varies by purpose in A: low angle for the boss (A t16.0: horizon at y = 854 = 0.67 H while the head centre is at 545 and the feet at 1075, so the camera is 1.16 D above the ground, 0.42 of head-centre height), eye level for dialogue (A t20.0: horizon 600, head centre 650; A t37.0: horizon 531-564, head centre 557), high for wides (A t58.5: horizon 565, head centre 792, feet 945, camera about 3.2 D above the ground).
- Clip B stays at or above head height: eye level at b/t44.5 (horizon 625, head centre 647) and b/t23.0 (horizon 597, head 559); high at b/t42.0 (horizon 432, head centre 794, about 2 D above the head) and on the balcony b/t14.5 (horizon 402).
- In clip A the horizon sits at 0.34-0.50 H in 9 of 11 measured frames (median 0.44 H; the outliers are 0.67 H in the low-angle shot and a weak 0.20 H fit at a/t53.5), so it is above the caption line and close to head level.

### 1.6 Framing in the 9:16 frame
- Main-character head centre: median 0.50 H, 10th-90th percentile 0.35-0.59 H (n = 45 heads on 40 stills, `framing_a.jpg`, `framing_b.jpg`). Every head centre is above the caption top (y = 880) and 91 % of heads are entirely above it. The caption line at y = 900 crosses chest in close shots, thighs or shins in medium shots and the ground in wides.
- Size classes (white face width; add about 10 % for outer D): close 261-355 px, medium 148-242 px, wide 47-135 px.
- 67 % of main heads are inside the centre third horizontally. Median offset from centre 0.05 W in A close shots, 0.10-0.16 W otherwise.
- Two-shots are staged in depth, not side by side: at A t45.0-t47.0 the hero is nearer and larger (white width 210-309 px) at x = 154-252, the boss farther (153-228 px) at x = 474-490, size ratio 1.36-1.40, and the far head sits 126-134 px higher. The face-to-face two-shot at A t20.5 is the exception: equal size (180 and 182 px), same height (644 and 634).
- Depth of field is selective. Background sharpness (Laplacian energy) relative to the character: 0.09-0.10 at b/t03.0 and b/t04.0 (strongly defocused court behind the inventor), 0.51-0.79 at b/t24.5 and b/t44.5, and 1.1-2.7 at a/t15.0, a/t20.0, a/t46.0 (background as sharp as the character). So clip A is deep focus and clip B blurs the background only in its first dialogue close-ups.

### 1.7 Character animation
- On ones, 30 fps. With the camera locked (B f1316-1376) no frame pair is a hold: 0 of 60 character-region differences fall to the background noise level, and the differences show no alternating pattern (adjacent min/max ratio median 0.87). Same result on five other shots.
- Bodies move by smooth interpolation; faces change by instant swap. Expression swaps complete within 1-2 frames (`cs_b_inventor.jpg`: f117 wide eyes, f119 closed; f131 neutral, f133 wide eyes) at 1.3-3.5 swaps per second.
- The active character moves, the listener freezes. A two-shot f1346-1430: the talking boss travels 0.34 D vertically and 0.12 D sideways, the listening hero 0.03-0.04 D and is slower than 0.05 D/s for 40 % of frames. Speaking heads in B sway 0.28 D sideways and 0.14-0.15 D vertically per shot (emperor f730-800, inventor f95-144).
- Walk cycle (B f1316-1376): head bob 0.47 D peak to peak, period 0.68 s, sideways sway 0.13 D.
- Blinks are frequent and short in A: 4 in 2.83 s on the listening hero (f1350, f1383, f1399, f1420) and 3 in 1.70 s on the wide-eyed hero (f1654, f1672, f1694), each 3-4 frames with 1-2 frames closed. B blinks less: 1 in 2.4 s on the throne (f750-752) plus a held wink (f787-799).
- Mouths flap fast while a character "speaks": about 7 shape changes per second counted by eye on the boss (12 states in f1381-1429, `cs_a_boss_mouth.jpg`), 4.9-9.8 per second by the ink-area threshold on three shots. The shapes are a small set: closed line, smirk, small o, wide oval, big O, teeth grin. A listener's mouth does not move at all (hero mouth ink constant at 22-43 px for 85 frames).
- Sync to the narration is loose. Correlation of mouth openness with audio loudness at a 0-1 frame lag: 0.57 for the inventor (B f95-144), 0.36 for the boss (A f1366-1429), about 0 for the emperor (B f740-800). Treat it as loudness-driven flapping during the lines the narrator voices for that character, not phoneme lip-sync.
- Motion blur exists only on fast camera moves. In the whip pan B f159-166 the picture shifts 40-190 px per frame and gradient energy falls to 0.38 of the sharp value (2.07 to 0.78). In the fly-in A f296-312 horizontal gradient energy is half the vertical (ratio 0.47-0.54, against 1.0 normally), i.e. radial streaks. Characters stay sharp even when they move about 250 px per frame (A f1736-1740, `blur_2.jpg` row 2).

---

## 2. Measurements

### 2.1 Summary table
| Quantity | Clip A | Clip B | Evidence |
|---|---|---|---|
| Shots | 16 | 22 | `shots_def.py`, `shotstats.py` |
| Shot length mean / median / range | 3.75 / 3.65 / 0.70-7.73 s | 2.62 / 2.45 / 0.40-6.53 s | same |
| Cross-dissolves | 11 (9-17 frames, median 13) | 18 (9-23 frames, median 10.5) | `alpha.py` on each transition |
| Plain hard cuts | 1 (f1322) | 1 (f93) | `shots.py` |
| Other transitions | train wipe f111-113, hidden cut f276-277, flash f1930-1934 | punch-in f146-147, whip pan f160-166 | `rowsA_2.jpg`, `rowsB_1.jpg` |
| Dissolve mix curve | smoothstep, 12 frames: .02 .07 .14 .22 .35 .47 .60 .72 .82 .90 .95 .99 (f346-357) | same shape, 7 frames of visible mix: .07 .24 .40 .61 .80 .91 .99 (f1749-1755) | `alpha.py` |
| Snap moves (> 450 px/s corner speed, 3+ frames) | 36, median 24.5 frames | 22, median 13.5 frames | `beats.py` |
| Interval between framing changes | median 1.19 s, mean 1.25 s | median 1.26 s, mean 1.54 s | `beats.py` |
| Fully static frames | 3.8 % | 5.5 % | `shotstats.py` |
| Static holds of 6+ frames | 4, total 1.30 s | 3, total 1.03 s | `beats.py` |
| Drift zoom rate, median (quartiles) | 7.8 %/s (2.5-17.5) | 7.6 %/s (3.0-13.6) | `beats.py` |
| Drift pan, median (quartiles) | 30 px/s (11-67) | 33 px/s (10-114) | `beats.py` |
| Drift direction in / out | 59 % / 19 % | 39 % / 45 % | `beats.py` |
| All in-shot frames, zoom rate 50th / 90th percentile | 20.8 / 129 %/s | 9.7 / 64 %/s | `shotstats.py` |
| All in-shot frames, pan 50th / 90th percentile | 133 / 787 px/s | 57 / 333 px/s | `shotstats.py` |
| Time share snap / drift / transition / near static | 44 / 44 / 8 / 4 % | 17 / 64 / 11 / 8 % | `final_stats.py` |
| Snap speed profile, peak / mean | 1.71 median, quartiles 1.56-2.09, peak at 0.50 of the move (both clips, n = 61) | | `easing.py` |
| Fastest snap, peak corner speed | 5851 px/s (f1740, crash pull-out) | 6811 px/s (f26, whip-push) | `easing.py` |
| Focal length | 622-870 px, median 787 px = 49 deg horizontal | not measurable | `vp.py` on a/t13.5, 14.0, 16.0, 19.5, 20.0, 21.0, 37.0 |
| Horizon height | 0.20-0.67 H, 9 of 11 frames within 0.34-0.50, median 0.44 H | 0.26-0.55 H (8 frames) | `vp.py`, `vp1.py` |

### 2.2 Framing
| Shot size | White face width | Head centre y | Offset from centre | Frames |
|---|---|---|---|---|
| A close (n = 8) | 283-355 px, median 308 = 0.43 W | median 0.36 H (0.24-0.58) | 0.05 W | a/t14.5, 15.0, 29.5, 30.0, 46.0, 47.0, 55.0, 56.0 |
| A medium (n = 14) | 149-228 px, median 168 = 0.23 W | median 0.45 H (0.25-0.59) | 0.16 W | a/t02.0, 03.0, 16.5, 19.5, 20.5, 27.5, 35.0, 37.0, 45.0, 53.5 |
| A wide (n = 3) | 112-118 px = 0.16 W | median 0.49 H (0.45-0.62) | 0.10 W | a/t12.5, 58.5 |
| B close (n = 4) | 261-313 px, median 268 = 0.37 W | median 0.51 H (0.42-0.59) | 0.12 W | b/t04.0, 05.0, 06.0, 34.0 |
| B medium (n = 11) | 148-242 px, median 177 = 0.25 W | median 0.51 H (0.44-0.62) | 0.10 W | b/t00.0, 03.0, 17.0, 18.5, 24.5, 25.5, 35.5, 41.0, 42.5, 44.5 |
| B wide (n = 5) | 47-135 px, median 71 = 0.10 W | median 0.57 H (0.41-0.60) | 0.11 W | b/t23.0, 27.5, 36.0 |
| All (n = 45) | | median 0.50 H, 10th-90th pct 0.35-0.59 | 67 % inside the centre third | |
| Head against caption | 100 % of head centres above y = 880; 91 % of heads fully above it | | | |

### 2.3 Camera height and pitch (D = head diameter of the subject in that frame)
| Frame | Horizon y | Head centre y | Feet y | D px | Camera height | Pitch (at f = 782 px) | Type |
|---|---|---|---|---|---|---|---|
| A t16.0 | 850-858 | 545 | 1075 | 191 | 1.16 D above ground = 0.42 of head-centre height | up 15 deg | low angle |
| A t20.0 | 594-608 | 650 | 1050 | 180 | 2.5 D above ground, 0.3 D above head centre | down 3 deg | eye level |
| A t37.0 | 531-564 | 557 | not measured | 150 | at head centre, within 0.2 D | down 5-8 deg | eye level |
| A t27.5 | 611 | 542 | seated | 149 | 0.46 D below head centre | down 2 deg | chest level |
| A t58.5 | 563-568 | 792 | 945 | 120 | 3.2 D above ground (subject crouching) | down 5 deg | high wide |
| B t44.5 | 625 | 647 | not measured | 197 | 0.1 D above head centre | down 1 deg | eye level |
| B t23.0 | 597 | 559 | not measured | 135 | 0.3 D below head centre | down 3 deg | eye level |
| B t42.0 | 432 | 794 | not measured | 177 | 2.0 D above head centre | down 15 deg | high |
| B t14.5 | 402 | none | none | none | balcony view | down 17 deg | high wide |
The extreme low-angle close-up at A t14.5-t15.0 (boss leaning over the lens, ballast in the foreground) was not measurable; it is lower and steeper than A t16.0.

### 2.4 Character motion
| Shot | Frames | Head travel, detrended peak to peak | Speed median / 90th pct | Notes |
|---|---|---|---|---|
| Walk, locked camera | B f1316-1376 | y 0.47 D, x 0.13 D | 0.49 / 1.46 D/s | bob period 0.68 s |
| Emperor speaking on throne | B f730-800 | x 0.28 D, y 0.15 D | 0.22 / 1.05 D/s | leans, one wink |
| Inventor speaking | B f95-144 | x 0.28 D, y 0.14 D | 0.43 / 1.62 D/s | 4 expression swaps in 1.67 s |
| Two-shot, talking boss | A f1346-1430 | y 0.34 D, x 0.12 D | 0.06 / 1.68 D/s | pops up, then small nods |
| Two-shot, listening hero | A f1346-1430 | y 0.03 D, x 0.04 D | 0.06 / 0.17 D/s | frozen, 4 blinks |
| Tycoon with tea | A f800-850 | y 0.07 D, x 0.01 D | 0.10 / 0.25 D/s | almost a held pose |
| Hero wide eyes | A f1650-1690 | x 0.18 D, y 0.08 D | 0.15 / 1.11 D/s | 3 blinks in 1.7 s |
Head positions are compensated for the fitted camera motion except the walk shot, so residual camera error is included; treat values under 0.05 D as "still".

### 2.5 Shot lists (time, length, what the camera does, how the shot ends)
Clip A
| # | Time s | Len | Content | Camera | Out |
|---|---|---|---|---|---|
| 1 | 0.00-3.70 | 3.70 | hero intro, train arrives | push x1.72 in 0.5 s, then pull back x0.70 with pan | train wipes the lens, 3 frames |
| 2 | 3.80-9.20 | 5.40 | canyon and bridge | forward flight x2.92 in 1.2 s, tilt down into the canyon, total x4.9 | cut hidden in a tilt |
| 3 | 9.27-11.53 | 2.27 | desert to station | hyper fly-in x63 in 1.8 s, radial blur | dissolve 12 |
| 4 | 11.93-13.40 | 1.47 | workers on a beam | sideways slide 59 px/s, zoom 0.9 %/s | dissolve 13 |
| 5 | 13.83-21.50 | 7.67 | boss: low close-up, full body, purple face, two-shot | five snaps: x2.56 tilt up, x0.83 back, x1.52 push, x0.50 back with 941 px pan, whip off | dissolve 13 |
| 6 | 21.93-26.13 | 4.20 | construction, foreman | fast pans, 1347 px in 1.6 s | dissolve 10 |
| 7 | 26.47-28.37 | 1.90 | tycoon with tea | push x3.05 in 0.83 s, then drift 10 px/s | dissolve 11 |
| 8 | 28.73-31.03 | 2.30 | sweating passenger | push x8.4 in 1.0 s, then 5 Hz shake | dissolve 14 |
| 9 | 31.50-35.97 | 4.47 | newspaper kid, crowd | pull back 5.9 %/s, then whip pan 1335 px in 1.17 s | dissolve 11 |
| 10 | 36.33-44.07 | 7.73 | calendar, hero at the gap, macro rail gap | pull back x0.15, push x2.57 to macro, 3 s slow push, 0.4 s hold, pull x0.70 | hard cut |
| 11 | 44.10-47.70 | 3.60 | two-shot, smug boss | crash zoom out x0.30, push x1.38, drift | dissolve 16 |
| 12 | 48.23-54.23 | 6.00 | rail point of view | travel along the rail with pans, total x6.3 | dissolve 15 |
| 13 | 54.73-59.13 | 4.40 | hero wide eyes, rail, wide | push x1.92 down to the rail, 0.47 s hold, crash pull-out x0.27 | dissolve 17 |
| 14 | 59.70-62.77 | 3.07 | sunset bridge | push 24 %/s easing to 0, x2.15 | dissolve 14 |
| 15 | 63.23-64.33 | 1.10 | snake rail, train falls | tilt down 521 px/s following the train | white flash, 5 frames |
| 16 | 64.50-65.20 | 0.70 | fireball, onlookers | pull back x0.37 | end |

Clip B
| # | Time s | Len | Content | Camera | Out |
|---|---|---|---|---|---|
| 1 | 0.00-3.10 | 3.10 | inventor, dragon head, emperor | whip-push x3.59 in 10 frames, pull back x0.46 with tilt | hard cut |
| 2 | 3.13-4.87 | 1.73 | inventor speaking | push 11.8 %/s, x1.21 | punch-in cut |
| 3 | 4.93-5.33 | 0.40 | inventor shocked, speed lines | held close | whip pan, 7 frames |
| 4 | 5.57-7.37 | 1.80 | court laughing | pull back x0.56 in 0.6 s | dissolve 10 |
| 5 | 7.70-13.40 | 5.70 | orbit around the jar | orbit, background slides 89 px/s median, zoom 5.5 %/s, tilt down to the frog | dissolve 11 |
| 6 | 13.77-17.77 | 4.00 | army, balcony | slow crane, tilt up to 100 px/s, zoom 8 %/s | dissolve 11 |
| 7 | 18.13-20.30 | 2.17 | inventor by the jar, goblet | near still, then crash push x3.23 in 0.5 s | dissolve 9 |
| 8 | 20.60-22.43 | 1.83 | goblet to emperor | crash pull-out x0.10 in 0.83 s | dissolve 9 |
| 9 | 22.73-23.97 | 1.23 | banquet | pull back 8.2 %/s, slide 42 px/s | dissolve 9 |
| 10 | 24.27-26.77 | 2.50 | emperor on throne | push easing out, 30 to 0 %/s, x1.31 | dissolve 11 |
| 11 | 27.13-29.57 | 2.43 | city gate | pull back, then push 8.9 %/s | dissolve 11 |
| 12 | 29.93-31.63 | 1.70 | sunset hill | tilt 158 px/s | dissolve 14 |
| 13 | 32.10-32.93 | 0.83 | camp | constant push 8.2 %/s | dissolve 13 |
| 14 | 33.37-37.10 | 3.73 | night, inventor and jar | long pull-out, 31 %/s median, x0.31 | dissolve 10 |
| 15 | 37.43-40.37 | 2.93 | portcullis | pull back 10.4 %/s, x0.78 | dissolve 9 |
| 16 | 40.67-43.50 | 2.83 | guards on the wall | push 9.7 %/s, x1.46 | dissolve 10 |
| 17 | 43.83-45.90 | 2.07 | inventor walks away | locked off (2.2 %/s, 4 px/s) | dissolve 12 |
| 18 | 46.30-48.50 | 2.20 | next morning, ruined palace | still, then crash push x2.17 in 0.43 s | dissolve 13 |
| 19 | 48.93-55.47 | 6.53 | pendulum inside the jar | rotating top-down orbit, 94 deg of roll, total x2.1 | dissolve 9 |
| 20 | 55.77-58.23 | 2.47 | dragon jaw | pull back 20 %/s with tilt 153 px/s | dissolve 10 |
| 21 | 58.57-61.37 | 2.80 | mountain to jar on the hill | whip pull-out x0.20 with 1124 px pan, then push x1.64 | dissolve 23 |
| 22 | 62.13-64.87 | 2.73 | underground cross-section | pull back 14 %/s easing to 0, last 0.4 s still | end |

Tally of the dominant move per shot (38 shots): compound sequences of two or more snaps 11, push-in 7, pull-out 8, fly-through or forward travel 3, orbit, slide or pan 4, tilt or crane 3, held or locked off 2.

---

## 3. How to reproduce

### 3.1 Global settings
- 30 fps, 720x1280, 1950 frames for 65 s. v1 was 24 fps.
- One lens for all 3D shots: `cam.data.lens = 22`, `sensor_width = 36`, `sensor_fit = 'AUTO'`. Checked in bpy 5.3 without rendering: this gives 49.4 deg horizontal, 78.6 deg vertical, focal 782 px. Acceptable range 18 mm (58.7 deg, the widest measured) to 24 mm (45.7 deg). v1 used 32 mm = 35.1 deg, which flattens the floor and hides the vanishing point.
- For flat painted sets in the clip B manner the lens matters less; keep 22 mm so that multiplane parallax has the same strength.
- Characters are flat cards that copy the camera rotation (see `character_anatomy.md` 3.4). A card parallel to the sensor is not distorted by a wide lens, so 22 mm is safe for faces.

### 3.2 Distances and heights in head diameters (lens 22 mm, focal 782 px; distance = 782 x D / on-screen D)
| Shot size | On-screen outer D | Camera to character | Head centre y | Use |
|---|---|---|---|---|
| Extreme close | 390-440 px | 1.8-2.0 D | 0.30-0.40 H | reaction beat, 0.4-1 s |
| Close | 300-350 px | 2.2-2.6 D | 0.36-0.51 H | one face, chest under the caption |
| Medium | 170-230 px | 3.4-4.6 D | 0.45-0.51 H | default, figure about 0.43-0.61 H tall |
| Wide | 110-135 px | 5.8-7.1 D | 0.49-0.57 H | figure plus place |
| Establishing | 30-75 px | 10-26 D | 0.55-0.60 H | place, crowd |

Camera height presets (subject standing, head centre about 2.4-2.9 D above the ground depending on the build):
- Eye level, the default for dialogue: camera at head-centre height plus 0 to 0.3 D, pitched 2-5 deg down. Result: horizon at 0.40-0.50 H, head centre at 0.45-0.50 H.
- Low angle, for authority (the boss) and the hero introduction: camera 1.2 D above the ground, 4 D away, pitched 15 deg up. Result: horizon at 0.67 H, head centre at 0.43 H, sky or ceiling behind the head, ground filling the bottom third (A t16.0).
- High angle, for wides and for a character who has lost: camera 3-5 D above the ground, 6-7 D away, pitched 5-15 deg down. Result: horizon at 0.34-0.44 H, head centre at 0.57-0.62 H (A t58.5, B t42.0).
- Keep roll at 0.

Framing rules:
1. Head centre between y = 450 and y = 760 (0.35-0.59 H); never let a face cross y = 880-930.
2. Fill below the caption with ground that carries perspective lines toward the horizon (floorboards, desk edge, rug, pier planks). The reference never has a blank lower quarter.
3. Single subject: within 0.16 W of the centre line.
4. Two-shot: put the listener nearer and lower, the speaker farther and higher. Near head 210-310 px at x = 150-250, far head 150-230 px at x = 470-490, far head 125-135 px higher. In D units of the near character: separate them 1.0-1.4 D in depth and 0.9-1.1 D sideways. Use the equal-size profile two-shot (both heads about 180 px at x = 240 and x = 630, same height) only for confrontation.
5. Background figures: 30-75 px heads, at least 10 D behind the principal.

### 3.3 Camera moves
Build every shot from this template (frames at 30 fps):
```
[0 .. 5]      incoming dissolve tail, camera already moving
[0 .. N-12]   primary move, one eased keyframe pair, velocity reaches 0 at N-12
(optional)    one snap, 14-24 frames, placed on a narration accent
[N-12 .. N]   near still (0-3 %/s), outgoing dissolve starts at N-6
```
Defaults:
| Move | Size | Duration | Interpolation |
|---|---|---|---|
| Drift push-in or pull-out | 6-10 %/s average, total x1.15-x1.45 or the inverse over a 2-3 s shot | whole shot minus 12 frames | `SINE` with `EASE_IN_OUT`, or `CUBIC` with `EASE_OUT` when the shot starts on a cut |
| Drift slide or pan | 20-60 px/s = 1.5-4.5 deg/s of pan, or a sideways truck of 0.03-0.08 D/s at 4 D | same | same |
| Snap push or pull | x1.5-x3 or the inverse; add 150-700 px of pan or tilt | 14-24 frames (clip B manner) or 24-32 (clip A manner) | `SINE` or `BEZIER`, `EASE_IN_OUT`; peak speed 1.6-1.9 x the mean |
| Crash zoom | x3-x10 or the inverse | 15-25 frames | `SINE` `EASE_IN_OUT`, motion blur on |
| Whip pan | 600-1300 px, peak 2000-6000 px/s | 7-20 frames | `SINE` `EASE_IN_OUT`, motion blur on |
| Orbit | background slides 90-210 px/s, about a quarter turn in 5-6 s (angle estimated, not measured) | 5-6 s | `BEZIER` |
| Shake (train, storm, wave) | 5 Hz, 12 px per frame standard deviation, 86 px peak to peak | 1-1.5 s | noise modifier or random keys every 3 frames |
| Hold | 0 | 6-14 frames, at most 3 or 4 in the whole film | none |

Converting percent per second to a dolly: a push of r per second at distance Z needs a speed of r x Z. At a medium shot (Z = 4.1 D) 8 %/s is 0.33 D/s. A total scale change of x1.3 means moving from 4.1 D to 3.15 D.

Conventions measured in the reference:
- Alternate direction from shot to shot (in, out, slide). Clip B splits 39 % in, 45 % out.
- Start a new scene with the bigger move (clip A opens shots at 645-872 px/s) and let it settle.
- Target one framing change every 1.2-1.5 s over the film: about 20-24 shots plus 20-30 snaps in 65 s. For this story the clip B profile fits better and is cheaper: about 22 shots of 2-3.5 s, one snap in every second shot, and three or four clip A style crash moves on the big beats (the erased line, the storm accelerating, the wave).

bpy 5.3 note, checked without rendering: `action.fcurves` no longer exists. Either set `bpy.context.preferences.edit.keyframe_new_interpolation_type` before inserting keys, or use this helper:
```python
def fcurves(obj):
    ad = obj.animation_data
    out = []
    for layer in ad.action.layers:
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot)
            if cb:
                out += list(cb.fcurves)
    return out

def key(obj, path, frame, value, interp='SINE', easing='EASE_IN_OUT'):
    setattr(obj, path, value)
    obj.keyframe_insert(path, frame=frame)
    for fc in fcurves(obj):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.5:
                    kp.interpolation = interp
                    kp.easing = easing
```
The interpolation set on a key governs the segment that starts at that key. Verified: keys at frame 1 (`SINE`, `EASE_IN_OUT`) and frame 25 give y = -4.0, -3.707, -3.0, -2.293, -2.0 at frames 1, 7, 13, 19, 25, and an `EXPO` `EASE_OUT` segment from 25 to 90 gives -1.76 at frame 40 and -1.707 at frame 60 toward -1.7.

### 3.4 Transitions
- Default, 4 of 5 transitions: cross-dissolve of 11 frames (0.37 s) with a smoothstep mix; use 13-16 frames for a change of place or time and 9 for quick continuity. Render 6 extra frames at the head and tail of each shot and keep the camera moving through them.
- ffmpeg, verified on the installed 6.1.1 build with black to white test clips (output mix .02 .07 .15 .26 .37 .50 .62 .74 .84 .93 .98, the same curve as the reference):
```
xfade=transition=custom:duration=0.4:offset=<shot_end-0.4>:expr='A*(P*P*(3-2*P))+B*(1-P*P*(3-2*P))'
```
  The built-in `fade` is linear (.08 .16 .25 ...) and is an acceptable fallback.
- Hard cut: 2 or 3 in the film, on a line that lands like a punch (reference: A f1322 at 44.07 s into the smug two-shot, B f93 at 3.10 s into the inventor's first line).
- Whip pan: one or two. End shot 1 with a 4-frame eased pan-off, start shot 2 with a 4-frame pan-on in the same direction, blur both.
- Object wipe: once, something large crossing the lens (in this story the wave or a slammed door).
- Flash: once, 5 frames to white, for the impact.

### 3.5 Motion blur and focus
- Blur only where the camera travels more than about 40 px per frame (rule of thumb from the whip frames, which shift 40-190 px): fast snaps, crash zooms, whips. `scene.render.use_motion_blur = True`, `motion_blur_shutter = 0.5`, and enable it only on those frame ranges if render time matters; the properties exist in bpy 5.3. A cheaper equivalent is to render 4 sub-frames across the frame interval and average them.
- Do not blur character animation; the reference keeps fast-moving characters sharp. If motion blur is global, keep character moves under about 40 px per frame or render characters in a pass without blur.
- Focus: deep focus by default. For two or three dialogue close-ups blur the background plate so that its Laplacian energy is about one tenth of the character's (a Gaussian blur on the plate is cheaper than `cam.data.dof`; start at a 6-8 px radius and tune it by measuring the ratio, the radius itself was not measured).

### 3.6 Character animation rules (small budget)
All motion on ones at 30 fps, eased.
1. Speaker or active character: one lean or nod every 1.0-1.5 s, moving the head 0.15-0.30 D sideways and 0.08-0.15 D vertically, eased over 8-12 frames, plus a head tilt of a few degrees (tilt not measured, read from the strips). Torso follows at half the amplitude.
2. Listener: frozen. Movement under 0.04 D. Blinks only.
3. Blink: 3-4 frames (half-closed 1, closed 1-2, open) every 0.7-1.2 s in the clip A manner, or every 2 s in the clip B manner. Offset the timing between characters.
4. Mouth: only on the character whose line the narrator is voicing. Swap among 5 or 6 shapes (closed line, smirk, small o, wide oval, big O, teeth grin) every 3-5 frames, 5-8 swaps per second. Drive it from the narration loudness: open shapes when the 33 ms RMS is above its running median, closed line otherwise, with a 0-1 frame lag. Phoneme accuracy is not needed.
5. Expression changes: swap the face sprite in a single frame, 1-3 swaps per second during a reaction. Add a 2-3 frame squash of about 0.03 D on the swap if wanted; the reference does not interpolate the face itself.
6. Walk: head bob 0.47 D peak to peak with a 0.68 s period (20 frames), sideways sway 0.13 D, legs alternating on the same period.
7. Entrances: a character pops up or slides in over 4-6 frames and then makes small nods (boss at A f1346-1366).
8. One gesture per shot is enough: an arm raise, a point, a shrug, eased over 8-10 frames and timed to the caption word.

---

## 4. Differences vs v1, ranked by visual impact

v1 facts come from `v1/scene_office_v1.py` and `ref/crops/camera-motion/v1_grid.jpg`.

1. v1 is one continuous 3 s framing with a single slow move. The reference changes framing every 1.2 s through 36 (A) or 22 (B) snap reframings plus 15 to 21 transitions. This is the largest gap: the reference feels directed, v1 feels like a parked camera.
2. v1 moves the camera with `LINEAR` keys at constant speed (0.63 m in 72 frames, about +5 %/s). The reference eases every move: snaps peak at 1.71 x mean speed and drifts fall below 3 %/s before the shot ends.
3. v1 characters do not live. Only one arm rotates and one face swaps at frame 46: no blink, no mouth, no head motion, no weight shift. The reference has a blink every 0.7-1.2 s, 5-8 mouth shapes per second on the speaker, head moves of 0.15-0.30 D and expression swaps at 1-3 per second.
4. v1 lens is 32 mm (35 deg horizontal) aimed square at a wall 1 m behind the characters, so there is no vanishing point and no depth. The reference uses about 22 mm (49 deg, measured 45-60 deg) with the ground plane running to a horizon at 0.34-0.50 H.
5. v1 staging is flat: both characters in one plane, heads at the same height (y = 550 and 551) and nearly the same size (198 and 224 px). The reference two-shot is staged in depth: size ratio 1.36-1.40 and 126-134 px of height offset.
6. v1 has one camera height (eye level, pitch 4 deg down). The reference switches between low (1.2 D above the ground, 15 deg up), eye level and high.
7. v1 leaves the bottom 22 % of the frame (y > 1000) as empty floor. The reference fills that area with ground detail and perspective lines under the caption.
8. v1 has no transitions at all in the test shot. The reference needs 11-frame smoothstep dissolves with both cameras still moving, plus a few cuts, a whip, a wipe and a flash.
9. v1 runs at 24 fps; the reference is 30 fps on ones.
10. v1 has no motion blur and no selective background blur. The reference blurs fast camera moves (sharpness down to 0.38) and defocuses the background in a few close-ups (0.09-0.10 of character sharpness).
11. Head height in frame is already right: v1 heads at 0.43 H against a reference median of 0.50 H (range 0.35-0.59). Head size is slightly large for a medium two-shot (198-239 px against a reference median of 168-177 px).
