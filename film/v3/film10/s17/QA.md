# s17 QA (round 2, after QA-art FIX-FIRST): film 10, shots 17-19 (the reveal)
Delivered: take.mkv as take.mkv.part* (cat to rebuild), g 1084..1433, 350 frames, first_g 1084, g0 1090, g1 1428. qa_auto PASS.
Fixes: 
- 17: wider steeper camera (lens 14.5-15, loc z 125) keeps torpedo, ship, gold buoy in frame the whole shot; top third now sea + convoy row.
- 18: ghost laid hull-on-hull on the real ship (offset 5 s, mirrored), opacity 0.85; lens 35-36.5, camera follows the ship, ship fills ~90% of the circle; ghost rigging wires removed from the mesh.
- 19: ghost peels away left and fades to 0.3 right after the cut (g 1296-1332), then 0.1 at the end; camera holds on the crossing (g ~1320-1375, torpedo reaches the cyan buoy in clear water behind the real stern) before following the ship.
- Buoy lamp lights keyed to 0 energy: no glare streaks on the water.
Known: ship is smaller on screen in 17/19 (about 25-30% width) because torpedo, ship and buoy must share the frame.
