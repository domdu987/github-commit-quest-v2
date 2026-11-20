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
