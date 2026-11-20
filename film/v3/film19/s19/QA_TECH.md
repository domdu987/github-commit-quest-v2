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
