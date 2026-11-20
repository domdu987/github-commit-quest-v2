# s23 QA: film 19, shot 23 (HALL EVENING), round-2 fixes
- take.mkv: g 1847..1941 (95 frames), shot g 1856..1932; transition in: dissolve.
- Old Harrison (old=1) starts in the corridor, shuffles THROUGH the doorway toward the camera (about 3.5 D, 34-frame stride cycle), H4 on his palm; stronger contact shadow (opacity 1.0, 1.5 D wide); crane-down + arc camera, faster whip-pan snap (shift 7.3 D) on 'พระราชา' (g 1898). qa_auto 'suspected blur' on the first 5 in-handle frames (g 1847-1851) is a false positive: sharp frames, Harrison half behind the door leaf, handle only. Known: the hall is dark late in the shot.
- Rules: no DOF, no text, no caption_shade; set hooks keyed every frame; samples 8; heads in shot (px): {"har": {"w": [96, 166], "y": [553, 643], "x": [176, 646], "bottom_max": 691}}
- qa_auto: see QA_AUTO.md + phone_sheet.jpg. Contact sheet checked at full size.
- s/frame wall 16.95 (2 procs x 2 threads), cpu 33.18.
- Frame-diff in shot (90x160 grey): median 4.54, p90 12.94 (per-take rule: median >= 4, p90 >= 10).
