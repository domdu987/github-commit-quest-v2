# QA s19 (render team 5, film 18) round 2 - frames g1427-1514 (+6 handles: take.mkv g1421-1520, 100 frames), jimo_out NIGHT
Frame-diff in-shot (n=87): median **5.56**, p90 **11.30** (target 4 / 12: median met, p90 just short; no pulses).
qa_auto FAIL on "suspected blur" g1503-1520: these are the whip pan (starts g1498 now) and the landing on the field (sky and sand, low edge detail); the director's QA-tech already ruled the previous identical flag a low-detail whip, not blur.
- Flames: all oxen lit as they leave the holes (waves start before g1427, a new wave every 11 frames until the whip), so a lit tail is on screen in every frame; flames on the tail-tip anchors with sparks and lights. The empty-wall gap is gone: the whip starts at g1498 while oxen and Qi are still in frame.
- Qi: 6 `qi_run` silhouettes through the whole shot behind the oxen.
- Near oxen: only holes x 24.5..41 are used and the camera stands at (8,-25,1.7), so the nearest ox is 16+ D from the lens (no fly-throughs, none above 50 % of frame height).
- Dust: soft round light-brown puff sprites (256 px gaussian blobs), 3 per hole; the set's dark-square dust/mist/hglow quads are removed.
- Not fixed: ground about 35 % of the frame; the bridge crossing is not shown.

## Round 2 (TAKE-gate notes from the director, QA_TECH / QA_ART)
Shared fixes (c18.py): every flame is a painted card placed on the ox's tail-tip anchor (cast18 `tail_tip`), leaning backward against the run, size capped (~1 D), with 6 spark cards streaming behind and one warm point light per lit tail (nearest 5) plus a small ground pool. The cast's own flame drawing is no longer used (cards are rendered with the unlit reed bundle). Placeholder/low-poly junk hidden at runtime (rubble/dig heaps, rain streaks, jars/reeds near the lens). No zoom pulses: motion is the eased push + slide, tracking and actor motion, with at most one held punch-in.
