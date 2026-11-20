# s23 QA: film 19, shot 23 (HALL EVENING), after the QA-art / QA-tech fix round
- take.mkv: g 1847..1941 (95 frames), shot g 1856..1932; transition in: dissolve.
- Old Harrison (old=1) starts in the corridor beyond the door, shuffles THROUGH the doorway toward the camera (about 3.5 D of travel, 34-frame stride cycle, wider contact shadow) holding the H4 on his palm; crane-down + arc camera, whip-pan snap on 'พระราชา' (g 1898). qa_auto reports FAIL 'suspected blur' on the 7 in-handle frames g 1847-1853: false positive, the frames are sharp (full size checked); he is half hidden behind the door leaf there (dark, low-detail). Not screen time (the dissolve in uses the handle). The door leaf covers him briefly after the snap.
- Rules: no DOF, no text, no caption_shade; set hooks keyed every frame; samples 8; heads in shot (px): {"har": {"w": [96, 162], "y": [534, 643], "x": [207, 620], "bottom_max": 691}}
- qa_auto: see QA_AUTO.md + phone_sheet.jpg. Contact sheet checked at full size.
- s/frame wall 27.14 (2 procs x 2 threads, some frames rendered while a second job ran), cpu 31.21.
- Frame-diff in shot (90x160 grey): median 4.42, p90 11.34 (target 4 / 12).
