# T5b2 QA (take T5, g1297-1383, 87 frames, 720x1280, 30 fps)

Setup: T5b render_T5b.py @3ff5509 + override.json (camera override for g>=1250, ARCHIVE_NIGHT values, day-scale ramp), 16 samples + OIDN, adaptive 0.03, 2 threads. Only differences from T5b's script, all director-directed:
1. output folder (T5b2/frames);
2. cast-leak fix (clear c2_/back_hair_/back_coat_ objects + actors.clear_registry() before every stage_cast2);
3. beam FX strength = 0 (beam_k = 0 in ARCHIVE_NIGHT and ARCHIVE_DAY) for the whole range;
4. TAKE-gate staging fix (camera untouched): inspector eased +0.5 m screen-right (+y) over g1335-1355 with a 0.035 m, 2 Hz shuffle bob and a lean of up to 3 deg, same pose; gend_a eased 1.3 m screen-right out of frame over g1300-1320 (g1297-1299 are unchanged, since the ease is 0 at g1300). Cards have no walk cycle, so the inspector's move is a slide with a bob, not a real step.

## Numbers (RGB-mean metric: 90x160 bilinear, mean of R,G,B)
- All 87 frames: mean 90.8, min 88.1, max 93.6. Largest frame-to-frame step 3.19 (g1319-1320, a pose change). Director target 90-108; the director accepts ~89-92 and will trim at conform.
- Pixels below luma 8: max 0.0001 % on any frame. No black slabs.
- qa_stats2 (take.mkv): sat 0.621, vivid 76.6 %, luma 89.4, contrast 28.6, motion med 3.92, p90 6.82.
- qa_auto.py: PASS (planned cut g1377 shows no visible change within +-2 frames; see open items).
- rhythm.py (cut g1377 excluded): in-shot median 4.55, p90 7.71.
- Beam-on frames were replaced: with the beam at 0 the whole range is 23-25 RGB-mean darker and has no milky veil. Beam-on frames are not in this commit.

## Frames viewed
Full size (720x1280) and then in an 8-frame phone sheet (360x640, g1300, 1320, 1341, 1342, 1350, 1358, 1376, 1383).
- g1315 (full size): gend_a is gone from the right edge. The inspector (arms crossed) is still cut by the LEFT edge here (his body from the left edge to about x=140); this is before the move, and it is outside the g1358-1376 range the director flagged. Bertillon and Dupont stand in the middle, stool behind Dupont, desks left and right. No veil.
- g1358 (full size): the inspector is fully in frame, left of Bertillon, standing in front of his desk (desk legs show behind his legs); feet on the tiles with a soft shadow. Bertillon's calipers point at Dupont's head, Dupont smiling with open hands, stool beside him. The right edge shows only the green-topped desk. No gendarme sliver.
- g1376 (full size): the inspector fully in frame with room on the left; same framing as g1358, a little closer. Nothing floats. The desk at the right edge is partly cut.
- g1300, g1320, g1341, g1342, g1350, g1383 (phone sheet only): inspector in frame at 1342 onward; no gendarme at the right from g1320 onward; at g1300 the cape gendarme is still visible at the right as before. I saw no pop between g1341 and g1342 (the join of the two render processes).
- Earlier full-size views of g1297, g1320, g1345, g1360 and g1383 (before the staging fix) found no veil and nothing floating.

## Not verified / open
- Mouths: I did not step through frames to check mouth motion against the quote windows. In the frames viewed, no mouth is open.
- The planned cut at g1377: qa_auto sees no visible change within +-2 frames. I did not look at g1377 specifically.
- A white oval blob at the top of g1345 and the neighbouring frames (about x187, y28), and a speck in g1297: probably a lamp object over the balcony, not identified.
- The inspector's shuffle bob and lean were checked only on a still at g1345 (he is in frame, pose unchanged); I did not review the motion as video. The sign of the lean ("into the move") is a guess.
- g1300-1320: the gendarme's slide out of frame (1.3 m in 20 frames) is a card slide on the floor. I did not review it as video.
- The inspector is cut by the left edge at about g1315-1330 (before the move starts); the director's note covered g1358-1376 only.
- OIDN shimmer: judged by eye only on full-size frames; nothing visible on the flat wall.
