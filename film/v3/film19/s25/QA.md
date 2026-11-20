# s25 QA: film 19, shot 25 (HALL EVENING), gate-G fixes
- take.mkv: g 2019..2094 (76 frames), shot g 2028..2085.
- Client gate G (face <= ~35 % of frame height): the 'เป๊ะ' snap is now x1.18 with a pan (was x1.7), peak head width 218 px (face with wig about 30 % of frame height); jaw-drop open mouth held from g 2028; wider contact shadow; wig clear of the frame edges in the shot.
- qa_auto PASS (QA_AUTO.md, phone_sheet.jpg). qa_stats.py: saturation 0.742, brightness 50.7, in-shot motion median 5.88 p90 8.38
- heads in shot (px): {"astro": {"w": [159, 218], "y": [573, 651], "x": [336, 549], "bottom_max": 759}}
- s/frame wall 13.47 (2 procs x 2 threads), cpu 26.39.
- Frame-diff in shot (90x160 grey): median 5.01, p90 11.46 (per-take rule: median >= 4, p90 >= 10).
