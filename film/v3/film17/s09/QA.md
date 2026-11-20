# QA s09 (film 17, shots 22-23, narration 39.76-44.65 s) - round 4
Take g 1190..1348 (159 frames; g0 1196, g1 1342, 6 handle frames each side), 720x1280, 12 samples + OIDN. take.mkv is split: `cat take.mkv.part* > take.mkv`.

## Numbers
- rhythm.py --first_g 1190 --cuts 1275: in-shot median **7.62**, p90 **14.30**. qa_auto **PASS**, magenta 0.0 %.

## R3 fixes
- B1 root cause was mine: with_expr(pose, "happy") fell back to neutral. Now the pose dict is set directly (expr "happy", mouth "smile"): smile-arc eyes, head yaw 0.5 + roll -10 toward Bertillon, gaze at him. Inspector moved about 45 px left (0.05, 1.9): Dupont's beret no longer overlaps his face or moustache in the frames checked (g1290-1330).
- B2 head shake: clipped sine (flat extremes, held 2+ frames), period 12 frames (2.5 Hz), yaw 0.1 +-0.5, roll +-12, torso lean +-5 so the head moves sideways; two bursts g1290-1310 and g1318-1338.
- Legs: dupont sunk 0.3 m so the dais edge hides the legs; the coat hem sits on the seat (no stub legs).
- g1274: camera look shifted 0.1 m more so the gendarme's cape stays clear of the left edge.
- g1190-1210: inspector offset now starts closer to the group (1.4 -> 1.9) so he trails it.

## Self-check (full-res frames viewed at 360x640 downscale)
g1290, g1296, g1302, g1310, g1330 (shake frames; eyes, head turn, no overlap), earlier g1212, g1274, g1300, g1305; contact sheet of 12 frames, both cuts +-3, decode check of all 159 PNGs. Not every frame at 6 fps.
