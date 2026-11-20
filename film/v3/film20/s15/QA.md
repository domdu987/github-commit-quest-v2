# QA s15 v3 (shot 15, TOWER tower_fair DAY 1889, g 996..1092 + handles g 988..995 (dissolve in) and 1093..1096 (cut out))
After TAKE_ART (F1-F3), TAKE_B and QA_TEAM §G. Checked at 6 fps contact + phone sheet.
- `qa_stats.py take.mkv` (whole file incl. handles): **saturation 0.561, brightness 87.7, in-shot motion median 7.56 p90 11.26** (sat/luma met; p90 0.7 short). In-shot only (g 997..1092, 90x160 grey): median 6.45, p90 10.68, max 18.0. Colour: runtime grade bump (tower20.LIGHTS DAY sat 1.22, exposure -0.42) set from shot.py.
- Distance: camera 4.3 D from Eiffel, Eiffel head width 179-448 px (35 % of frame height at the end of the snap, centre y 513-623, chin <= 768); the official's head never exceeds ~275 px and never sits half-cut: he hands the document over (g 1008-1030), then steps back and aside (g 1030-1062) so the snap lands on Eiffel with him small, behind (leaves frame right only in the out handle).
- Ground: the nearest ground is trampled sand with long shadows; below the feet <= ~25 % of the frame. Crowd: 24 preset cards + 16 extra cast20 crowd cards (lady / gent / child / artists) in the midground, all bobbing.
- Foreground: gent20 BACK card (top hat, brown coat) bottom-left corner, 3 D ahead of the lens, feet underground, camera-relative every frame; the preset lamp-post and bench are moved out of frame (no pole across the lens, no black bars).
- Beat: push-in x1.35 on 'ใบอนุญาต' g 1003-1011, document handover, on g 1067 Eiffel's smile drops to worried + sweat on the closed frame of a blink (g 1066-1068), snap x1.6 g 1064-1080. Feet + contact shadows on both actors. Mouths never move.
- take.mkv 32.0 MB (single file).

## v4 (QA_TEAM §I client decision)
- Added an "EXPOSITION UNIVERSELLE 1889" banner (Latin text objects, gold on a red board, two poles) behind the pair (readable on frames g 988-1015, then the orbit carries it out of frame), 6 keyed fluttering pennant poles, and a lower raking sun (key_dir elevation ~27 deg: long cast shadows, warm sun + deep-blue shade in every frame). Crowd (40 cards) and flags move; nobody frozen. Join out = hard CUT (4 handle frames g 1093-1096), join in = DIS 13 (8 handle frames).
- `qa_stats2.py take.mkv`: sat 0.561, vivid 47.2 % (>= 45), luma 86.0, warm 30.9 % / cool 33.6 %, motion median 7.56 p90 11.74, still 0 %. In-shot g 997..1092: median 6.46, p90 11.02 (p90 still 1 short of 12).
- take.mkv 31.5 MB.

## v5 (director re-measure request)
- Re-rendered with more orbit (24 deg/s) and slide (-75 px/s), push-in x1.28 on 'ใบอนุญาต', snap x1.35 (peak 2.3, tilt -3.5) on worried Eiffel, grade sat 1.28 / exposure -0.36. Eiffel head width 178-458 px (centre y 469-612, chin <= 741).
- `qa_stats2.py take.mkv` (the pushed file): **sat 0.587, vivid 47.2->48.6 %, luma 84.3 (0.7 under the 85 floor), warm 25.9 % / cool 39.7 %, motion med 7.88 p90 11.72, still 0 %**. In-shot g 997..1092: median 6.49, p90 10.62.
- The director's earlier read (sat 0.442 / vivid 37 % / p90 8.3) did not match the pushed file at that commit (md5 2c507741...: sat 0.561 / vivid 47.2 %); re-pull before measuring.
- take.mkv 29.4 MB.

## v6 (TAKE2_ART s15 fixes F1-F3)
- F1 document: the permit is now always in a visible hand on a visible arm. The official holds it on a stretched arm (hand (-0.62..-1.1, 0.7), stretch 1.1-1.3, the cast `official_doc` values) while handing it over, Eiffel takes it with his right arm (hand (0.62, 0.72), stretch 1.1 = the cast `official_doc` hold) and holds it at his chest through the payoff frame; the dark ball at the document edge is his fist.
- F2 official: he stays inside the frame (head x 408-646, widest 262 px, right edge < 720 in-shot) and steps back along the depth only.
- F3 tower: the camera is wider (5.4 D, was 4.3) and the orbit is only 8 deg/s (was 24), so the tower legs, the first platform and the EXPOSITION banner stay behind Eiffel through the snap (g 1064-1080).
- Head width 145-370 px (centre y 545-635, chin <= 764): Eiffel never exceeds 29 % of the frame height.
- `qa_stats2.py take.mkv`: sat 0.585, vivid 49.1 %, luma 86.7, warm 42.8 % / cool 25.7 %, motion med 5.72 **p90 12.06**, still 0 %. In-shot g 997..1092: median 4.95, p90 10.87. take.mkv 38.1 MB.

## v7 (TAKE2_A adds)
- Banner raised (z 11.2) so the official's hat no longer hides it: "EXPOSITION UNIVERSELLE 1889" reads on every frame through g ~1075 (then the snap carries it out).
- Acting g 1020-1060: stronger idle sway (lean 5, head-roll 4, breathing), the official gestures with his free arm (small wave toward the tower g 1032-1066), Eiffel bows over the permit to read it (head pitch to 0.22 g 1030-1065), crowd and pennants moving.
- Last push eased (snap x1.5, peak 1.7, 20 frames g 1064-1083) against the soft-frame note; luma 86.9 (>= 85).
- `qa_stats2.py take.mkv`: sat 0.585, vivid 49.4 %, luma 86.9, warm 43.2 % / cool 25.7 %, motion med 7.10 **p90 11.40** (the eased snap costs ~0.7 p90), still 0 %. In-shot g 997..1092: median 6.08, p90 10.34. Head width 145-348 px (chin <= 769). take.mkv 39.2 MB.

## v8 (set flag fix d1511f7 merged)
- Re-rendered with the merged set (vertical tricolour flags). Same shot as v7. `qa_stats2.py take.mkv`: sat 0.586, vivid 49.5 %, luma 86.8, motion med 7.12 p90 11.33, still 0 %. In-shot median 6.10, p90 10.29. take.mkv 39.3 MB.
