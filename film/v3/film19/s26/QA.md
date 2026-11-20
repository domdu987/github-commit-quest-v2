# s26 QA: film 19, shot 26 (HALL hall_table EVENING), round-4 fixes
- take.mkv: g 2077..2159 (83 frames), shot g 2086..2159, hard cut in; the film ends on a hard cut at g 2159 (N = 2160), no out-handle.
- Gold money sack (1.6x) falls and lands at g 2107 with a squash and 10 gold coins, warm key light; Harrison behind the table looks down at the bag, then up at the lens, arms rise, 2 bounces, H4 in his hand; King nods twice as hard; raised tilted-down camera, orbit drift + snap on 'ช่างไม้' (g 2147).
- Round-4 fixes: (1) Harrison's whole face stays in frame to the end (head x 111-410, w 180-218, left edge >= ~10 px at g 2159); (2) his legs are hidden by a dark-wood panel added under the table's near edge (runtime set dressing in shot.py); no floating legs.
- Known: the sack has no tie facing the camera; a candelabra edge flares at the right edge in the last frames.
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg). heads (px): {"har": {"w": [180, 218], "y": [587, 732], "x": [111, 410], "bottom_max": 835}, "king": {"w": [97, 119], "y": [501, 593], "x": [460, 647], "bottom_max": 652}}
- s/frame wall 17.42 (2 procs x 2 threads), cpu 34.15.
- Frame-diff in shot (90x160 grey): median 4.2, p90 10.28 (per-take rule: median >= 4, p90 >= 10).
