# QA_TECH s24 - FAIL
Checked: qa_auto PASS (cuts g1933 / g2028 not visible, expected: handles), 6 fps + cut +-3 sheet g1924-2034, meta g0 1933 / g1 2027 (plan 64.44-67.61 -> 1933/2027 OK), cuts both sides with 9 f handles OK, framediff median 4.06 (marginal) / p90 15.07 OK. EVENING hall_table, king's chair, regulator, no text, no blur, king's mouth flat (no lip-sync), snap g2003-2019 visible.
Issues:
1. g2014-2034 (blocking, occlusion): a foreground candelabra fills the left/centre of the frame and covers the King's face-side and the two watches (flame overlaps his face at g2019-2027); the subject is half hidden for the last ~1 s of the shot and the out-handle. Fix: move the camera path/slide so the candelabra is out of the King's silhouette, or drop it.
2. g1933-2034 (plan coverage): "stubs pile up 0 -> 10" is only readable up to ~5-6 stubs (g1999-2004); from g2009 the table row is out of frame, so the count never reaches 10 on screen. Fix: keep the near-edge stub row in frame through the end (lower camera, shorter push) or time the stub growth to finish before the camera moves.
3. g1933-2004 (scale): King head 80-150 px (a speck for a 720x1280 phone) and the two watches rising/falling out of phase (0.9 s) cannot be read; "compares the watch with his gold watch" does not register. Fix: closer framing on the King for the middle 2 s.
4. g2019-2034: candle flames are clipped pure white (blown out); acceptable look but check at phone size.
5. Plan says the King stands; he reads as seated behind the table with the chair back visible. Note only.
