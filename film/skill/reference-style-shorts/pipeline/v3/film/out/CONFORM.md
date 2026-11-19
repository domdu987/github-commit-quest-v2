# CONFORM: build-order step 12 (picture, captions, cue list)

Out folder: PROJ/v3/film/out/ (PROJ = __PROJ__)

| Output | What |
|---|---|
| frames/g_0000.png .. g_1964.png | 1965 picture frames, 720x1280, no captions |
| film_silent.mp4 | H.264, yuv420p, 30 fps, 1965 frames, 65.500 s, about 5.25 Mbit/s, CRF 18; 104 Thai captions burned last with PROJ/assemble.py |
| film_silent.ass, caps_burn.json | the caption script: 104 phrases from PROJ/audio/th/full_v2/narration_timing.json (the the new voice voice), +0.100 s, `{\fnKanit Black\fs88}` in front of each, centred at (360, 900), hard swaps; the last phrase ends at 65.500 s |
| cues_all.json | 233 cues on the film clock (seconds), each with its take: hook 24 (PROJ/v3/out/sfx_cues.json) + the 23 take cue lists; fields t, dur, take, g, kind, label, clock (= t - 0.100) |
| contact_film.jpg | 48 evenly spaced frames of film_silent.mp4 (captions in), labelled with g, time and take |
| conform.py, grammar.py | the conform (joins, transitions, overlays) and the picture-based grammar recount |
| work/ | joins.json, conform logs, join strips joins_0..3.jpg, caption sheets, grammar.json, recount.json, framing_changes.json |

## Takes
All 23 takes (s04 .. s26) were complete when the conform started (18 Nov 18:33): meta.json present, every frame g0..g1-1 and every declared handle in frames/. No waiting was needed, no take is missing, no frame was held, and no handle had to be extended in 2D (the extension code is in conform.py; it ran on 0 frames).
The hook: PROJ/v3/out/frames/f_0001..f_0129 are film frames g 0..128 (shots 1-3); f_0124..f_0135 (g 123..134) are mixed under the 12-frame dissolve into s04; f_0136..f_0150 are not used.

## Joins (film frame of the cut gb = first frame of the incoming take)
| # | Join | gb | Plan | Done | Frames mixed |
|---|---|---|---|---|---|
| 1 | hook > s04 | 129 | dissolve 12 | smoothstep dissolve | 123-134 |
| 2 | s04 > s05 | 199 | cut hidden in the whip-tilt | straight cut inside the blur (both takes carry the whip frames) | - |
| 3 | s05 > s06 | 271 | dissolve 13 | smoothstep dissolve | 265-277 |
| 4 | s06 > s07 | 336 | dissolve 10 | smoothstep dissolve | 331-340 |
| 5 | s07 > s08 | 401 | dissolve 15 | smoothstep dissolve | 394-408 |
| 6 | s08 > s09 | 505 | dissolve 13 | smoothstep dissolve | 499-511 |
| 7 | s09 > s10 | 610 | dissolve 9 | smoothstep dissolve | 606-614 |
| 8 | s10 > s11 | 694 | dissolve 9 | smoothstep dissolve | 690-698 |
| 9 | s11 > s12 | 792 | dissolve 11 | smoothstep dissolve | 787-797 |
| 10 | s12 > s13 | 839 | punch-in with speed lines | straight cut; the speed lines are in s13 (g 839-844) | - |
| 11 | s13 > s14 | 868 | dissolve 11 | smoothstep dissolve | 863-873 |
| 12 | s14 > s15 | 956 | match dissolve 13 | smoothstep dissolve, paper to paper | 950-962 |
| 13 | s15 > s16 | 1013 | dissolve 13 | smoothstep dissolve | 1007-1019 |
| 14 | s16 > s17 | 1086 | dissolve 14 | smoothstep dissolve | 1079-1092 |
| 15 | s17 > s18 | 1123 | hard cut | hard cut | - |
| 16 | s18 > s19 | 1189 | match dissolve 12 in the crash push | smoothstep dissolve | 1183-1194 |
| 17 | s19 > s20 | 1419 | dissolve 9 | smoothstep dissolve | 1415-1423 |
| 18 | s20 > s21 | 1516 | dissolve 10 with the whip pull-out | smoothstep dissolve | 1511-1520 |
| 19 | s21 > s22 | 1571 | dissolve 14 | smoothstep dissolve | 1564-1577 |
| 20 | s22 > s23 | 1664 | dissolve 17 | smoothstep dissolve | 1656-1672 |
| 21 | s23 > s24 | 1720 | hard cut | hard cut | - |
| 22 | s24 > s25 | 1788 | object wipe 6 (foam sheet) | 2D foam sheet (lilac-white, scalloped, leaning) crosses the lens left to right; full cover on g 1787-1788 | 1785-1790 |
| 23 | s25 > s26 | 1873 | white flash 5 in, 4 out | lerp to white 0.15/0.35/0.60/0.85/1.00 on g 1868-1872, out 0.85/0.55/0.30/0.12 on g 1873-1876 (s26's own lightning key decays under it) | 1868-1876 |
Inside the hook: the in-take reframe (shot 1 > 2, g 33-47) and the whip pan with its cut at g 73.
Dissolve rule: frames gb - L//2 .. gb - L//2 + L - 1, weight of the incoming take smoothstep((g - a + 1)/(L + 1)).

## Overlays (plan list for the conform)
| Overlay | Status |
|---|---|
| speed lines, shot 13 | in the take (s13) |
| speed lines, shot 20 | ADDED: 42 white radial wedges about the corridor vanishing point (360, 470), g 1442-1472, ease in 4 f, retreat and fade |
| speed lines, shot 24 | ADDED: 40 white wedges, g 1730-1748 (the crash pull-out on 'กำแพงน้ำ') |
| focus lines, shot 24 | ADDED: dark-ink focus lines round the two faces on g 1720-1722 (0.85, 0.70, 0.45) |
| rain strokes, shot 16 | in the take (set_rain) |
| note glyphs, shot 17 | in the take |
| wake streak, shots 20, 21 | in the takes (3D red-hot wake) |
| wake streak, shot 25 | LEFT OUT (needs a per-frame track of the spinner; the spinner already carries its motion-blur disc) |
| ink blot, shot 25 | in the take (map decal) |
| foam wipe, white flash | ADDED (joins 22, 23) |
| camera streak, plate and matte passes | in the takes (and the hook) |

## Checks
- Frame count: 1965 PNG frames; film_silent.mp4 has nb_frames 1965, 30/1, yuv420p, 720x1280, 65.500 s.
- Pops (popcheck.py rule, mean absolute difference on 180x320, larger than 1.8 x both neighbours): g 1123 (54.3) and g 1720 (45.6) = the two planned hard cuts; g 1255 (5.8) inside s19 = the land pressure wall appears in one frame (take, not join). The wipe and flash frames change fast by design. Every join was looked at in a 6-frame strip (gb-3 .. gb+2: work/joins_0..3.jpg): dissolves run smoothly with no jump in brightness or framing at either end; the punch-in, both hard cuts and the hidden cut read as planned.
- Captions: all 104 phrases detected in the MP4, Kanit Black, white with a black outline; box top at y 858-887 (median 873), bottom about y 925-940, centred at x 360. Heads clear of the caption band in every caption sheet frame (work/captions_sheet_0.jpg, _1.jpg) EXCEPT s16 g 1068-1078: beach_man's head rises through y 880-950 under 'ฝนปรอยๆ' (the take's planned tilt down; its QA says the head is whole above y 880 only from g 1079). Also s14 g 902-925: the typed Thai 'ลมกระโชก' on the thrust forecast sheet sits at y 880-960 under the caption 'ก็ออกไป' (two Thai texts overlap for about 0.8 s).
- Contact sheet: contact_film.jpg viewed: story order, sets and lights as planned, no black, magenta or missing frames.
- Colour (PROJ/v3/tools/hue_report.py, every third frame per set and light): office_day both blocks "all in band"; office_grey blue 42 (OUT: red 27, blue, sat 0.35); office_storm, kitchen_storm, the beach blocks and kitchen_grey outside the interior band (exterior or special light, as the plan intends).

## Grammar recount (on the conformed film)
Method: qa_motion.py works from the hook's Blender camera; the conformed film has no single camera, so grammar.py fits the camera motion of every frame pair from the picture (LK tracks + RANSAC similarity) and uses qa_motion's own MOVE (12 px/frame), STATIC (0.25 px/frame) and run logic; pairs across a join are left out.
| Item | Plan | Conformed film |
|---|---|---|
| Shots / takes | 26 / 25 | 26 shots from 24 sources (hook + 23 takes); every shot boundary on its planned frame |
| Shot length | mean 2.52 s, median 2.29, 0.96-7.68 | the same (boundaries unchanged) |
| Transitions | 17 dissolves (9-17 f, median 12), 2 hard cuts, 1 whip, 1 hidden cut, 1 punch-in, 1 wipe, 1 flash, 1 in-take reframe = 25 | the same 25 |
| In-shot snaps | 26 | 26 of 26 found in the measured motion within 2 frames of their planned window (peaks 34-458 px/frame); measured length over 12 px/f median 11 frames |
| Moves over 12 px/f not in the snap list | - | 15 runs, all planned non-snap moves: hook whip, the whip-tilt and fly-in (g 195-219), shot 5 pull-back, shot 7 pointer pan, the punch-in shake, the s16 tilt down, the s19 arrival crash push and two bonk shakes, the s21 whip pull-out, the s22 arrival, the s25 tilt-up follow, the s26 shake |
| Framing changes | 51; interval mean 1.26 s, median 1.21, 0.34-2.4; after the hook 1.32 / 1.21; over 2 s: 2.4, 2.18, 2.29, 2.23 | 51 (25 transitions + 26 snaps) = 0.78 per second; interval mean 1.26 s, median 1.22, 0.32-2.42; after the hook 1.32 / 1.23; over 2 s: 2.42, 2.15, 2.27, 2.22 |
| Static runs (rule: at most 6 frames) | holds 8, 12, 6, 12 f | only single frames, plus g 1954-1964 (11 f, the planned last hold) |
| Constant-speed runs | - | longest 21 f (s21 drift, g 1543-1563); all others 10 f or less |
Framing changes measured (narration clock, s): 0.35, 1.20, 2.00, 2.38, 3.73, 4.20, 5.00, 6.53, 8.95, 11.10, 12.35, 13.28, 15.22, 16.75, 17.95, 19.37, 20.25, 21.17, 23.05, 24.62, 25.58, 26.32, 27.87, 28.85, 30.13, 31.78, 32.77, 33.68, 34.87, 36.10, 37.33, 37.65, 38.77, 39.53, 40.95, 43.22, 44.43, 45.85, 47.22, 48.22, 50.43, 52.27, 53.27, 54.37, 55.38, 57.23, 57.87, 59.50, 61.42, 62.32, 63.57 (the plan's list, within 0.07 s each).

## Missing or not done
- Wake streak overlay on shot 25 (left out, see above).
- Caption over a head: s16 g 1068-1078. Caption over picture Thai text: s14 g 902-925. Both are in the takes; captions stay at y 900 as the brief says.
- s19 g 1255: the land pressure wall appears in one frame instead of swelling (take).
- Sound is not part of this step: cues_all.json is the list for the mix.
