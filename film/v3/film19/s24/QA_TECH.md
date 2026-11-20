# QA_TECH s24 - FAIL
Checked: qa_auto PASS (cuts g1933 / g2028 not visible, expected: handles), 6 fps + cut +-3 sheet g1924-2034, meta g0 1933 / g1 2027 (plan 64.44-67.61 -> 1933/2027 OK), cuts both sides with 9 f handles OK, framediff median 4.06 (marginal) / p90 15.07 OK. EVENING hall_table, king's chair, regulator, no text, no blur, king's mouth flat (no lip-sync), snap g2003-2019 visible.
Issues:
1. g2014-2034 (blocking, occlusion): a foreground candelabra fills the left/centre of the frame and covers the King's face-side and the two watches (flame overlaps his face at g2019-2027); the subject is half hidden for the last ~1 s of the shot and the out-handle. Fix: move the camera path/slide so the candelabra is out of the King's silhouette, or drop it.
2. g1933-2034 (plan coverage): "stubs pile up 0 -> 10" is only readable up to ~5-6 stubs (g1999-2004); from g2009 the table row is out of frame, so the count never reaches 10 on screen. Fix: keep the near-edge stub row in frame through the end (lower camera, shorter push) or time the stub growth to finish before the camera moves.
3. g1933-2004 (scale): King head 80-150 px (a speck for a 720x1280 phone) and the two watches rising/falling out of phase (0.9 s) cannot be read; "compares the watch with his gold watch" does not register. Fix: closer framing on the King for the middle 2 s.
4. g2019-2034: candle flames are clipped pure white (blown out); acceptable look but check at phone size.
5. Plan says the King stands; he reads as seated behind the table with the chair back visible. Note only.

## Round 2 - FAIL
Checked: qa_auto PASS (cuts g1933 / g2028 are handle boundaries); 6 fps + cut +-3 sheet g1924-2034; meta g0 1933 / g2027 OK, cuts with 9 f handles OK; frame-diff median 3.94 / p90 9.94 (measured; limits 4 / 12).
Verification of round 1: 1 foreground candelabra occlusion FIXED (it slides left and clears the King at g2019+). 2 stubs 0->10 NOT fixed. 3 King scale PARTLY fixed. 4 blown flames: NOTE. 5 seated vs standing: NOTE.
Issues:
1. Frame-diff median 3.94 and p90 9.94 are both under the limits (p90 got worse than round 1 15.07). Fix: add the snap amplitude back (x1.3 pan in g2003-2019 is the only spike), stronger slide in g1933-2000.
2. g2009-2034 (plan coverage): the near-edge stub row leaves the frame; only ~5-6 stubs are visible at g2004-2014 and none from g2019, so the pile never reads as 10 at the end. Fix: keep the stub row in frame to the cut (lower camera or shorter push) or time the growth to finish before the camera leaves it.
3. g1924-1974 (scale): King head 80-100 px, the two watches are specks; the comparison does not read until g1984. Fix: start closer (the mid-shot size of g1994) and keep it.
Notes: an orrery sits in front of the King and covers his lower body; the King reads seated; flames are blown white.

## Round 4: PASS
Checked 6 fps + cut +-3 (take g1924-2036). qa_auto PASS. No text, black/magenta, frozen, blur. King's mouth is closed throughout (only expression changes). Frame-diff g1934-2027 median 4.05 / p90 13.91: R2-1 FIXED. R2-2 FIXED: the stub row stays in frame and grows from 0 to ~10 by g2006-2014. R2-3 FIXED: King head 135-220 px from the start, the two watches read; the candelabra no longer covers him.
Notes: King's wig touches the left edge at g2009-2027 (face intact); a candle edge shows at the left of the last frames; the King reads seated behind a lectern; flames blown white.

## Round 10 (director QA-tech): PASS
Checked 6 fps (g1924-2159, from the cat of the two parts) plus every frame g2094-2146 (table-front crop) and g2084-2095, g2130-2159 at full size. Frames in /tmp/qa19_r10/s24/. Frame-diff (own calc, 90x160 grey bilinear, in-shot pairs g1933-2159): median 4.78, p90 20.21 (limits 4 / 10) OK; no pair < 0.3, no black frame, no frozen run. Spikes only on the planned whips and the snap (g2008-2012 snap, g2022-2027 whip 1, g2087-2088 whip 2).
Round 9 blocker (pale semi-transparent hard-edged rectangle / light-shaft plane over the table front at g2094-2146): FIXED. On every frame g2094-2146 the table front is a clean dark-wood panel with the green top above it; no pale plane, no hard-edged lighter rectangle at any g.
Earlier passes hold: the mocker (astro, jaw-drop) is last seen g2087 and is smeared out by g2089-2091 inside whip 2 (g2086-2093), gone at g2092; the bag appears at g2107 and sits on the table by g2108 (g2107 = 70.23 s, inside 70.1-70.3 s), coins settle on the table; Harrison grins from g2106 and hops (head bobs g2110-2146); the King nods g2146-2159; Harrison's pocket watch dial stays inside the frame at the left of his head g2130-2159 (partly behind the hair, never cut by the edge); the camera is still moving on the last frame (pair diff 5.5 at g2158-2159, push/orbit visible). Stubs 0 -> 10 read, both watches read, no props through faces, nothing floating, heads/bottoms: Harrison head y <= 702, astro bottom 759 (< 880); biggest face about 33 % (g2069-2084 push-in, planned).
No mouth movement other than the astro jaw-drop gulp and Harrison/King smiles (expressions, not speech).
Notes (not blocking): the ~5 frames of heavy blur at whip 1/2 are the planned motion streak; King's wig touches the left edge around g2009-2027 (face intact); Harrison's face is large (about 22-28 %) in the last 15 frames, within the 35 % cap.
