# s26 QA: film 19, shot 26 (HALL EVENING), gate-G fixes
- take.mkv: g 2077..2159 (83 frames), shot g 2086..2159.
- Client gate G (no character cut by a frame edge): the push/orbit was reworked so BOTH men stay fully in frame to the last frame g 2159 (Harrison head x 197-364, w 180-241; King head x 400-607, w 97-127; checked g_2159 full size: Harrison, sack with coins, King all inside the frame), still moving at the film's hard cut. Legs hidden by the table panel, face never cut. Known: King head centre dips to y 448 around g 2141 (2 px under 450); the sack has no tie facing the camera; p90 9.09 is just under the per-take 10.
- qa_auto PASS (QA_AUTO.md, phone_sheet.jpg). qa_stats.py: saturation 0.631, brightness 57.3, in-shot motion median 4.93 p90 8.61
- heads in shot (px): {"har": {"w": [180, 241], "y": [497, 721], "x": [197, 364], "bottom_max": 841}, "king": {"w": [97, 127], "y": [448, 573], "x": [400, 607], "bottom_max": 636}}
- s/frame wall 17.59 (2 procs x 2 threads), cpu 34.52.
- Frame-diff in shot (90x160 grey): median 4.32, p90 9.09 (per-take rule: median >= 4, p90 >= 10).
