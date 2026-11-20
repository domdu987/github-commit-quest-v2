# s24 QA: film 19, shot 24 (HALL EVENING), round-2 fixes
- take.mkv: g 1924..2036 (113 frames), shot g 1933..2027; transition in: cut.
- King19 beside the table head (clear of the orrery) compares the pocket watch with the H4 (both 1.5x at face height); the ten candle stubs (moved in front of the King) grow 0->10 by the snap word 'สิบสัปดาห์' (g 2006) and stay in frame; closer start (King head 135-220 px), stronger drift, snap shift 2.4 D. Known: a candle edge shows at the left of the last frames.
- Rules: no DOF, no text, no caption_shade; set hooks keyed every frame; samples 8; heads in shot (px): {"king": {"w": [137, 222], "y": [546, 621], "x": [154, 566], "bottom_max": 695}}
- qa_auto: see QA_AUTO.md + phone_sheet.jpg. Contact sheet checked at full size.
- s/frame wall 18.07 (2 procs x 2 threads), cpu 35.46.
- Frame-diff in shot (90x160 grey): median 4.06, p90 13.94 (per-take rule: median >= 4, p90 >= 10).
