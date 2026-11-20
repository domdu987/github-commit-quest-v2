# QA s02 (film 18, team 1) — "ผูกมีด": blade tying + herd reveal (round 8)
Take: g 78-155 in-shot (78 frames) + 10 handle frames after (g 156-165); first_g 78, n_frames 88. jimo_in NIGHT, 720x1280, 12 samples, ~17 s/frame. transition_in: CUT.
Round-7 changes: all v1 dressing removed (no dress_ground in this take); the warm contact-pool decals under the oxen removed; the woman is camera-locked at 4.8 -> 3.9 D from the lens, 1.8 D tall, kept right of the left edge for the whole take with her head above y 880 and nothing covering her feet; the green figure at the right edge is gone; crane up 1.5 -> 5.8 D with the herd cards pitched back, 72 oxen stacked from y ~0.35 to the bottom; warm fill lights along the wall base.
Round-8 fix: the flat violet band behind the herd was Cycles' transparent-bounce limit (dense stacks of alpha cards ran out of transparent depth and rendered the rest as violet); transparent_max_bounces raised to 96 in c18.py for this take, so the band is gone and the herd reads as red coats from the front rows to the far gate (no plane needed). Tian Dan eases right (-2.4 D) from g125 so he is fully inside the frame at g153-165.
## Frame-diff (90x160 grey, in-shot g 78-155)
median 9.28 (>= 4 OK), p90 12.59 (>= 12 OK), min 4.10, max 19.26.
## Checks
qa_auto PASS. Heads above y 880, no mouths, no text, no flames.
Known: bare dirt at the bottom about 25-30 % from g 108.
