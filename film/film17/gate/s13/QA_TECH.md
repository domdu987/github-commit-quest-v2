# QA-tech s13 (film 17 shots 31-33, ending) - FAIL

Checked: all 49 frames of f6 (every 5th + cut neighbourhoods) at 480x853 montages with the y 880 line, plus g2047 at full size.
Not measured: Laplacian (no cv2 here); no frame was visibly blurred/DOF. Heads: all above y 880 in every frame (OK). No black/blank frames seen.

## Issues
1. g2014-2047 (shot 33, the key punch): caliper jaws do NOT touch the ear. The ear sits ~100 px left of the jaw, the jaw hangs beside the moustache tip / in front of the next gendarme's cap. Fix: put the caliper tips on the ear (ear between the jaws), same framing as shot 3.
2. g2014-2047 (shot 33): calipers have no hand/arm: the bar enters from the right edge out of nothing (Bertillon not in frame) and runs behind the kepi. Fix: show Bertillon's hand on the calipers, or frame so the bar is held; bar must not pass behind the inspector's hat while the jaws are at the ear.
3. g2014-2051 (shot 33): inspector cropped by the left edge (head and ear half out), subject off-centre; the stated plan was an ear insert (callback to shot 3). Shot 3 framing was never matched (QA.md admits it is "my own estimate"). Fix: match shot 3 camera, ear centred.
4. g1947-2013 (shot 32): the closing of the calipers on the inspector's ear is not visible. Bertillon's head/body is in front of the inspector and hides his right ear; the calipers are a tiny white stick at Bertillon's hip (g1947-1992) and only appear at the ear from ~g1997 as a grey stub in front of the cap/eye. Fix: reframe so the ear is visible, Bertillon beside/behind, calipers clearly closing on the ear with a readable opening/closing motion.
5. g1947-1967 (shot 32 start): stray white/yellow cross-shaped object lying/floating on the floor at right (x ~400-440, y ~520-570 of 853). Unexplained prop or dust; clutters the first frames after the cut. Fix: remove or make it a readable prop.
6. g1862-1946 (shot 31): coverage miss, Bertillon does not visibly raise calipers; only a white stick at his hip and a small grey wedge by the green gendarme's chest (g1922-1946, floats unattached). Fix: Bertillon holds calipers in hand, visible.
7. g1862-2013 (shots 31-32): see-through geometry. A translucent lighter diagonal wedge crosses the inspector's torso/skirt and chair in every frame (e.g. g1862, g1917, g1992, g2012); Bertillon's trousers/coat tail are semi-transparent in g1862-1877 and the dark coat tail in front of the table is see-through in g1947-1967 (table edge shows through). Fix: kill the translucent plane (hood/light cone/shadow card), make Bertillon's coat opaque.
8. g1862-1877 (shot 31 open): foreground brass pole plus semi-transparent hood slab covers the left third and the left gendarme; the pole is a hard vertical dividing the frame. Hood is noted in QA.md but reads as a see-through cloth. Fix: opaque or move out of frame.
9. Mouth: inspector's mouth changes shape without a quote: closed/flat in g1862-1897, oval "o" g1922, g2014-2022, becomes a wider flatter ellipse g2037-2042 and thinner g2022. "No mouth may move" rule: fix by locking the mouth state (no jaw/mouth jitter); eyes/moustache twitch only.
10. g1862-1877, g1947-1967 (left edge) and g1972-2002: stray small white discs/dust specks (e.g. g1862 x~60-110, y~640-740; g1972 x~15, y~700). Fix: remove the particle layer or make it clearly dust motes with lower contrast/size, not bright dots.
11. Plan coverage shot 32: "gendarmes/prisoners grinning" in shot 31 is met (green gendarme laughing, tears), but in shot 32 the bowler gendarme is stern/unamused and the grin is not shown (g1947-2013); only a faint smirk on a gendarme in shot 33. Acceptable for shot 32 per plan (not required) - note only.
12. Continuity at cut g1947: Bertillon switches from right of the inspector to in front of him and the camera jumps to a different height/angle (clock now visible at upper centre); inspector becomes tiny behind Bertillon's head. Fix with issue 4 reframing; the cut itself lands on 1947 (OK).
13. Moustache twitch / eyes sideways (shot 32): eyes look sideways (OK, g1957-2013); moustache shows tip shifts but no readable twitch at 6 fps. Minor, verify at 30 fps.

## Verdict: FAIL (blockers: 1, 2, 3, 4, 7)
