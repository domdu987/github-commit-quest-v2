# QA s01 revision 2 (shots 1-3, g 0-178; 720x1280, 24 samples, ~28 s/frame at 2 threads)
Director gate fixes applied:
1. Shot 1: custom closer camera (y -6.5 -> -3), Hanway starts ~9 units away and walks toward camera (man + umbrella ~300 px tall on 1280 from frame 0); a coachman glares from the kerb, readable from g 0.
2. Shot 2: box_trio preset (approved tile 10); head coachman huge on the right whip-pointing down (pose point_mock with mouth flat), box_b / box_c turn from nod to glare (g 86 / 92); Hanway lower-left, whole body in frame, passing in front of the horses without touching a wheel. box_c stays small (as in the approved tile).
3. Shot 3: a coachman on foot (thrower, face visible, wind-up then release) throws a cabbage g118-124; it hits the umbrella apex at g124 (0.17 s later than the 3.9 s cue, so the wind-up is visible after the cut), bounces and lands on the road behind Hanway and STAYS there (no pop, no vanish); no leaf on the umbrella (leaf_stick 0 everywhere); Hanway flinches 10 frames then walks on.
4. Mouths: every coachman card carries mouth='flat' (closed) in the whole take.
5. 24 samples; blob contact shadows under Hanway, the thrower and walkers; Hanway stays left of the coach, no overlap with wheels.
- qa_auto PASS. Its "no visible change" note at cuts 66/117 is a tool quirk (cuts checked by eye).
- Known weaknesses: box_c small in shot 2; Hanway walks in place facing camera (cycle) with some foot slide; cabbage lies as a dark-green lump on the road for the last 40 frames.
