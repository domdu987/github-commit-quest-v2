# film19 camera-motion QA tools (from the §E independent review, round 15)
These measure the CAMERA, not the characters: ship-only motion with the sea masked out.
1. Extract frames named by g, e.g. `ffmpeg -i take.mkv -start_number <first_g> /tmp/qa19_ov/s02/g%03d.png`.
2. `FRAMES=/tmp/qa19_ov/s02/ python3 sim.py` fits ship-only similarity motion per frame (teal water and foam masked) and prints speed (px/frame at 720 wide) and rotation.
3. `python3 stub.py` evaluates the camera path from ../../v3/film19/s02/shot.py outside Blender: tau, position and aim per g.
4. `reg.py` gives regional LK medians. `track.py` runs NCC templates on rigid features; re-seed the template positions if the framing changed.

s02 acceptance for g128-160:
- ship-only median ≥ about 6 px/f, top band ≥ about 10 px/f;
- no climb-back > 20 % after any local low;
- no aim reversal squeezed into fewer than 8 frames.
