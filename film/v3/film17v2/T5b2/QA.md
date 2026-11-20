# T5b2 QA (take T5, g1297-1383, 87 frames, 720x1280, 30 fps)

Setup: T5b render_T5b.py @3ff5509 + override.json (camera override for g>=1250, ARCHIVE_NIGHT values, day-scale ramp), 16 samples + OIDN, adaptive 0.03, 2 threads. Only differences from T5b's script, all director-directed:
1. output folder (T5b2/frames);
2. cast-leak fix (clear c2_/back_hair_/back_coat_ objects + actors.clear_registry() before every stage_cast2);
3. beam FX strength = 0 (beam_k = 0 in ARCHIVE_NIGHT and ARCHIVE_DAY) for the whole range;
4. TAKE-gate staging fix (camera untouched): inspector eased +0.5 m screen-right (+y) over g1302-1320 (the director moved the window earlier) with a 0.035 m, 2 Hz shuffle bob and a lean of up to 3 deg toward screen-right, same pose; gend_a eased 1.3 m screen-right out of frame over g1300-1320 (g1297-1301 are unchanged, since both eases are 0 at g1300-1301; g1361-1383 are unchanged because the inspector's offset is constant there). Cards have no walk cycle, so the inspector's move is a slide with a bob, not a real step.

## Numbers (RGB-mean metric: 90x160 bilinear, mean of R,G,B)
- All 87 frames: mean 90.8, min 88.1, max 93.5. Largest frame-to-frame step 3.14 (g1319-1320, a pose change). Director target 90-108; the director accepts ~89-92 and will trim at conform.
- Pixels below luma 8: max 0.0001 % on any frame. No black slabs.
- qa_stats2 (take.mkv): sat 0.621, vivid 76.6 %, luma 89.4, contrast 28.5, motion med 3.91, p90 6.72.
- qa_auto.py: PASS (planned cut g1377 shows no visible change within +-2 frames; see open items).
- rhythm.py (cut g1377 excluded): in-shot median 4.54, p90 7.61.
- Beam-on frames were replaced: with the beam at 0 the whole range is 23-25 RGB-mean darker and has no milky veil. Beam-on frames are not in this commit.

## Frames viewed
Full size (720x1280) and in phone-size sheets (360x640): g1300, 1305, 1310, 1315, 1320, 1330, 1341, 1342, 1360, 1376 (10 frames in one sheet) plus earlier full-size views.
- g1315 (full size, after the earlier-ease re-render): the inspector (arms crossed, smirk, big moustache) is fully in frame at the left, standing in front of his desk, whose legs show between his legs; he leans slightly. Bertillon (glasses, beard) in the middle, Dupont in the beret with open hands beside a stool, and the green-topped desk at the right edge. No gendarme at the right edge. No veil. Feet on the tiles with soft shadows.
- g1358 and g1376 (full size, before the window change; frames 1361+ are unchanged by it, g1358 was re-rendered since): inspector fully in frame at the left, calipers at Dupont's head, nothing floating.
- Phone sheet g1300-1376: at g1300 the cape gendarme is at the right as before; at g1305 and g1310 he is a sliver leaving the right edge; from g1315 he is gone. The inspector is cut by the left edge at g1300-1305 and reaches full frame by g1310-1315. I saw no pop at the join of the render processes (g1341/g1342 and g1331/g1332 were not specifically compared).
- Earlier full-size views (before the staging fix) of g1297, g1320, g1345, g1360 and g1383 found no veil and nothing floating.

## Not verified / open
- Mouths: I did not step through frames to check mouth motion against the quote windows. In the frames viewed, no mouth is open.
- The planned cut at g1377: qa_auto sees no visible change within +-2 frames. I did not look at g1377 specifically.
- A white oval blob at the top of g1345 and the neighbouring frames (about x187, y28), and a speck in g1297: probably a lamp object over the balcony, not identified.
- The inspector's shuffle bob and lean were checked on stills only (g1315, g1345 earlier), not as video. The lean sign was set from the puppet code (a positive lean tips the top toward screen-right).
- g1300-1320: the gendarme's slide out of frame (1.3 m in 20 frames) is a card slide on the floor. I did not review it as video.
- The inspector is cut by the left edge at g1300-1305 (the move starts at g1302); full frame from about g1310-1315.
- OIDN shimmer: judged by eye only on full-size frames; nothing visible on the flat wall.
