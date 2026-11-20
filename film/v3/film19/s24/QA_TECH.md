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
