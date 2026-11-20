# QA_TECH s19 - FAIL
Checked: qa_auto PASS (cut g1581 not visible, expected), 6 fps + cut sheet g1459-1589, meta g0 1468 / g1 1580 (plan 48.92-52.71 -> 1468/1580 OK), DIS 13 in + cut out with 9 f handles OK. William holds the H4 high in his hand, tricorne in the other hand, sailors cheer, snap g1496-1509 (push-in on "ห้าวินาที") visible, no text, no blur, mouths are fixed grins (no lip-sync), DAY_JAMAICA OK, ship in background OK.
Issues:
1. Frame-diff p90 = 9.77 (limit >= 12); median 7.12 OK. After the snap the camera barely changes. Fix: add a second beat (slide or sailors pop) so p90 >= 12.
2. g1509-1589: William is clipped. The tricorne is cut by the right edge from g1509; from g1569 his head is cut by the right edge (x > 720) and at g1578-1589 more than a third of the face/hat is off-frame; legs/feet cut at the bottom from g1509. Fix: shift the push target left / reduce the end scale (head_px 397 is too large) so head + hat + H4 stay inside x 20-700.
3. g1559-1589: the sea plane ends in a hard straight diagonal edge (turquoise water cut off against sand beyond, left side y 230-290 at g1578) = geometry edge visible. Fix: enlarge the sea grid or limit camera pan/orbit.
4. g1569-1589: flat lavender patch in the sky at top right (clipped cloud/sky card). Fix: remove or re-place the sky card.
5. g1574-1589: a sailor's head sits directly under/behind the H4 and William's raised hand (tangent, watch overlaps sailor cap). Minor; re-space the sailor.
6. g1459-1504: wide-shot head y OK; g1509+ head centre y ~ 538-611 OK.

## Round 2 - PASS
Checked: qa_auto PASS (cut g1581 is the handle boundary, not visible, expected); 6 fps + cut sheet g1459-1589; meta g0 1468 / g1 1580, DIS 13 in, cut out, 9 f handles OK; frame-diff median 6.63 / p90 13.50 (measured).
Verification of round 1: 1 p90 FIXED (13.50). 2 clipping FIXED (heads, hats, H4 inside the frame to the end; head centre y 472-739, all heads above 880). 3 sea edge FIXED (no hard diagonal edge). 4 lavender sky patch FIXED (reads as a cloud). 5 sailor/H4 tangent FIXED (H4 clear of the sailor caps).
Snap on "ห้าวินาที" g1496-1509 (word g1497) visible. Mouths are fixed grins. Ship at left in the first frames, sails far right later; sea moves. Contact shadows present.
Notes: (a) g1578-1589 the left sailor raised hand touches the left frame edge. (b) left sailor feet shadow is faint at g1534/1564.

## Round 7 (director QA-tech) - PASS (with notes)
Checked: take.mkv 131 frames 720x1280 30 fps, meta g0 1468 / g1 1581 (shot 1468-1580), first_g 1459; 6 fps frames in /tmp/qa19_r7b/s19/, plus per-frame black/frozen/pop scan. BIGZOOM g1468-1552.
Numbers (measured by QA-tech):
- Start character height (g1468, idx 9): trio about 30 px of 1280 = ~2.3 % (< 5 %). Findable: three figures with raised arms beside the beached boat, at the foot of the cove.
- End of zoom (g1552): tallest figure (William incl. H4 and hat) 210-497 of 640 = ~45 %; at the last frame (g1580) ~53 %. Inside 35-60 %. Faces ~11-14 % of frame height (< 35 %).
- Frame-diff (90x160 grey, bilinear, 112 consecutive in-shot pairs g1468-1580): median 5.80 (>= 4 OK), p90 13.29 (>= 10 OK), min 1.43, max 16.9.
- Move smoothness: ONE continuous move, no cut, no pop (largest jump between neighbouring pairs 1.26x), ease-in from 1.4 (g1468) up to the push-in peak ~16.9 (g1505-1508, the snap), then eases out to ~5 by g1552. Speed profile has a second hump at g1520-1535 (11-14) and a third at g1535-1545 (~11), so it is a wavy ease rather than a clean bell. Not a defect on its own, flagged as a note.
- Parallax: big palm fronds and a red rock block pass the lens in g1468-1500, a palm trunk with crown crosses at g1500-1515, then it settles on the trio. Foreground parallax OK. No edge of the world, horizon and sea reach the sky normally, ship and island in the background, no bare backdrop at the high start.
- Characters: never cut by a frame edge in the move. Heads: face centres y ~540-640 at the end (< 880). Feet on sand with contact shadows at g1552-1580 (William shadow faint but present). Nobody floats. H4 held high by William with the tricorne in the other hand, sailors cheer and bounce through the whole shot (region diff 16-26 every 3 frames, no still run > 1.5 s). No frozen runs (min consecutive diff 0.54), no black frames. Mouths are fixed grins, no lip-sync. No prop passes through a face (H4 clear of the sailor caps).
Issues / notes:
1. g1497-1509 (peak g1506): foreground palm fronds and the crown render PURE BLACK (RGB < 28; up to 4.2 % of the frame at g1506, whole top-left frond at g1504). Reads as an unlit-geometry glitch, not a silhouette. After g1510 the top-right palm crown stays near black (~3 % of the frame) until the end. Fix: give the fronds the green material and rim light, or remove that frond.
2. g1468-1495: the two big brown flat-shaded polygon hills framing the cove (left y 270-450 and right y 220-330 at g1468) and the salmon face of the red rock read as bare untextured planes. Not an edge of the world, but thin on "rich set" (QA-art call).
3. g1540-1580: left sailor's raised hand sits within ~6-30 px of the left edge (touches at g1578-1580). Minor, was noted in round 2.
4. Start height is only ~2.3 %, tiny: findable only because of the boat and arms. Acceptable under the brief (< 5 %).
