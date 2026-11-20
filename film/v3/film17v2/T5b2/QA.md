# T5b2 QA (take T5, g1297-1383, 87 frames, 720x1280, 30 fps)

Setup: T5b render_T5b.py @3ff5509 + override.json (camera override for g>=1250, ARCHIVE_NIGHT values, day-scale ramp), 16 samples + OIDN, adaptive 0.03, 2 threads. Only differences from T5b's script, all director-directed:
1. output folder (T5b2/frames);
2. cast-leak fix (clear c2_/back_hair_/back_coat_ objects + actors.clear_registry() before every stage_cast2);
3. beam FX strength = 0 (beam_k = 0 in ARCHIVE_NIGHT and ARCHIVE_DAY) for the whole range.

## Numbers (RGB-mean metric: 90x160 bilinear, mean of R,G,B)
- All 87 frames: mean 91.0, min 88.3, max 93.5. Largest frame-to-frame step 3.15 (g1319-1320, a pose change). Target 90-108 per director; the director accepts ~89-92 and will trim at conform.
- Pixels below luma 8: max 0.0001 % on any frame. No black slabs.
- qa_stats2 (take.mkv): sat 0.620, vivid 76.2 %, luma 89.5, contrast 28.9, motion med 4.00, p90 6.43.
- qa_auto.py: PASS (magenta 0.0 %). It notes the planned cut at g1377 shows no visible change within +-2 frames (see below).
- rhythm.py (cut g1377 excluded): in-shot median 4.63, p90 7.31.
- Regression check: with the beam at 0, g1299-1383 are NOT identical to the beam-on frames (-23 to -25 RGB-mean; the beam was a milky veil over the whole range). All 87 frames were re-rendered beam-off. The beam-on frames are not in this commit.
- Frame g1300 / g1360 beam-on in-process frames were bit-identical to T5b's approved stills (diff 0.0 / 0.073 mean), before the beam was switched off.

## Frames viewed (full size 720x1280, then in a 360x640 phone-size sheet)
- g1297: Four figures in a row in the archive: left gendarme with arms crossed, a smirk and big moustache; Bertillon (glasses, beard, dark coat); Dupont in a beret with shrugging, open hands; right gendarme in a blue cape. Cabinet wall, blue-railed balcony above, tiled floor and a red/blue rug in the foreground. No veil and no light shaft (this frame had both in the beam-on render). Feet sit on the floor and each figure has a soft shadow under it. A tiny white speck at the top edge near the balcony.
- g1320: Camera has moved closer. The left gendarme is cropped by the left edge (face and cap visible), a desk with instruments beside him, a stool now behind Dupont, and the right gendarme is cut off at the right edge. Colours saturated; floor tiles read clearly; no veil.
- g1345: Bertillon's arm is out and his calipers point at Dupont's head; Dupont keeps the open-hands shrug and smile. A white oval blob is visible at the top of the frame over the balcony (about x 187, y 28); I believe it is a lamp or glow object but I did not identify it. The right gendarme is almost out of frame (a strip of blue at the right edge).
- g1360: Same pose and framing, calipers at Dupont's cheek/head; the stool and desks stand on the floor with their legs touching the tiles. No veil.
- g1376: Slightly closer again; the left gendarme's face is half cropped by the left edge; the table at the right edge; Bertillon and Dupont as before.
- g1383: Nearly the same as g1376 (a little closer); nothing floating; colours unchanged.
- Phone sheet (6 frames at 360x640): all six frames read clearly at phone size; the four figures and the caliper line are legible. The white blob in g1345 is also visible at that size.

## Not verified / open
- Mouths: I did not step through frames to check mouth motion against the quote windows. In the six frames viewed, no mouth is open.
- The planned cut at g1377: qa_auto sees no visible change within +-2 frames, and g1376 vs g1383 differ only by a slight push-in. I did not look at g1377 specifically.
- The white blob at the top of g1345 (and a tiny speck at the top of g1297) was not identified.
- Left gendarme is cropped by the frame edge from about g1320 on; this comes from T5b's camera override, which I did not change.
- OIDN shimmer: I did not measure it on the camera hold (g1345+) with a tool that separates shimmer from motion; in the full-size frames viewed (g1345, g1360, g1376, g1383) I saw no visible shimmer on the flat wall.
