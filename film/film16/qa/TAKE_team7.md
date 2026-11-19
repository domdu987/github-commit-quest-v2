# TAKE gate QA-tech, film 16, render team 7 (s22 PROVISIONAL, s23, s24)
Checked at 6 fps + cuts +-3, full-res frames; qa_auto.py run on each take.mkv; frame-diff recomputed (90x160 mean-RGB, in-shot pairs).

| take | verdict | median | p90 | qa_auto |
|---|---|---|---|---|
| s22 (PROVISIONAL, being re-shot) | FAIL (diff below target) | 3.64 | 9.60 | PASS |
| s23 | FAIL (blocking: legibility of the beat) | 7.13 | 11.39 | PASS |
| s24 | FAIL (blocking: p90 ok, coverage + blur flag) | 4.01 | 14.28 | FAIL (blur 1545-1552) |

## s22 (PROVISIONAL)
BLOCKING
1. g1382-1454: frame-diff median 3.64 / p90 9.60, both under the 4 / 12 targets (47 of 73 in-shot pairs < 4). Fix: add real camera travel (truck/orbit or stronger slide) during g1403-1454 after the snap; the post-snap hold is near-static drift. Keep the crate out of frame by trucking away from it, not toward it.
NOTES
2. g1372-1388: Morse's feet are hidden behind the wagon side board and the crate, no contact shadow visible on the wagon bed; reads as standing behind the board. Fix: raise camera slightly or lower the board.
3. Eye-line: eyes are closed smile arcs for the whole shot, so nothing looks at the bottle/sun. Fix: open eyes looking up at the bottle (g1383+).
4. Held bottle is ~2 D vs crate bottles, plausible; sun is not visible in the frame, only glints (g1396-1410, 1437). Acceptable, add a sun disc/rim light if the re-shoot allows.
5. Continuity: sky is warm sunset, s23 sky is similar; OK. Mouth still, no text, no DOF, heads: centre y 559-621, bottom max 800, OK (nothing > 880). No blur frames (Laplacian never < 60 % of median).

## s23
BLOCKING
1. g1511-1548 (36 frames, whole last third of the take): the beat "drape the wire on the glass" is not legible. Morse's raised fist covers his eye/face from g1511 on (looks like a telescope or wiping his eye), the wire exits the top of the frame as a thick diagonal bar crossing his face (g1511), and from g1526 the glass is a thin mint sliver on the left edge, wire out of frame, no visible wire-on-glass contact. Fix: pick a framing for g1505-1539 that keeps glass top + wire contact in frame (pan right / keep push smaller, slide the camera to put the pole top at frame centre), and make the free hand bring the wire to the glass instead of crossing the face; hold the hand down from the face.
2. g1446-1500: the held "bottle" is a noisy dithered mint translucent blob (visible grain on the glass material at g1458, g1486), not a readable bottle; the neck/inverted bottle is not recognisable until g1496. The callback must read as the s01 bottle. Fix: render the glass copy with the same material and enough samples (noise-free), keep neck-down silhouette readable on the snap g1475-1488.
NOTES
3. Morse's expression is an angry/grumpy frown for g1456-1520; plan beat is "now we know why" (proud). Same as s01 so consistent, but the face should turn happy before g1510, not at 1522+.
4. Callback matches s01 camera/marks (checked against s01 contact.jpg); lighting AFTER_RAIN: sky bluer/less warm than s22 end, minor.
5. Heads 90-304 px, centre y 396-588, bottom max 713: OK. No text, DOF, mouth movement, magenta; no blur. p90 11.39 is a hair under 12 (median 7.13 fine). Camera never parked.
6. Cut in g1455 from s22 (close head + bottle) to a wide pole shot: hard cut ok. planned cuts "no visible change within +-2" in qa_auto is a false alarm for this reason of colour/framing similarity? (frames do differ strongly; qa_auto note only).

## s24
BLOCKING
1. g1558-1623 (plan coverage): the plan beat is that the pulse crosses the neck, does NOT leak, "the wet pole below stays dark". After the snap (g1579+) the pole is entirely out of frame, and before it the pole is sunlit orange, not dark/wet, so the non-leak contrast is never shown (g1555-1573 pole is bright salmon). Fix: keep the pole below the glass in frame through the snap (snap onto the glass with the pole's top 30 cm visible) and darken/wet the pole (or keep it clearly non-glowing next to the cyan glass); end framing must include the dark pole under the glowing glass.
2. qa_auto FAIL: suspected blur g1545-1552 (Laplacian 0.36-0.49 of median). Visually this is empty sky gradient plus the fast whip (no true DOF), but the checklist FAIL stands. Fix: add detail in view during the whip (clouds/distant pole, or lower the whip speed / reduce the sky-only portion g1544-1551), or the team documents it and an opus reviewer waives it (override per QA_TEAM E).
3. Their QA.md says QA_AUTO PASS; actual run FAILs. They must re-run and report truthfully.
NOTES
4. g1615-1623 handles and end: the cyan wire stub at the glass top ends in a flat rectangular cut (g1597-1623) rather than tapering; looks like a cut-off bar.
5. Last ~35 frames (g1580-1614) the shot is a near-static glass close-up (diff ~3.9, never < 2.9, not parked by the 6-frame rule) but visually flat; consider a slow orbit.
6. Frame-diff median 4.01 passes barely; p90 14.28 ok. Pulse reads as one comet, parks in the glass at g1555-1558, glow stays in glass. No text, magenta, mouths N/A (no cast). Pop outside cuts: none.
