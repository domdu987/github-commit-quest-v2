# s26 QA: film 19, shot 26 (HALL EVENING), round-2 fixes
- take.mkv: g 2077..2159 (83 frames), shot g 2086..2159; transition in: cut.
- Gold money sack (1.6x) falls and lands on the tabletop at g 2107 with a squash and 10 gold coins spilling out, warm key light on it; Harrison behind the table looks at the bag, then up at the lens, arms rise, 2 bounces, H4 in his hand; King nods twice as hard; raised, tilted-down camera (tabletop fills the lower third), orbit drift + snap on 'ช่างไม้' (g 2147); ends at g 2159 (film end, N = 2160) with Harrison, bag and King in frame, still moving. Known: the sack has no tie facing the camera; Harrison's head is near the left edge at the end; a candelabra edge flares at the right edge in the last frames; Harrison's feet are visible below the table with a contact shadow, not hidden.
- Rules: no DOF, no text, no caption_shade; set hooks keyed every frame; samples 8; heads in shot (px): {"har": {"w": [180, 217], "y": [587, 729], "x": [108, 410], "bottom_max": 830}, "king": {"w": [97, 119], "y": [501, 593], "x": [460, 647], "bottom_max": 651}}
- qa_auto: see QA_AUTO.md + phone_sheet.jpg. Contact sheet checked at full size.
- s/frame wall 17.43 (2 procs x 2 threads), cpu 34.02.
- Frame-diff in shot (90x160 grey): median 4.26, p90 11.32 (per-take rule: median >= 4, p90 >= 10).
