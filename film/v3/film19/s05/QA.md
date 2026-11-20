# QA s05 (shot 5, ship_rocks STORM_DUSK) — revision 3 (after round-2 TAKE gate)
Take g 253-364 (shot g 262-355; 9 handle each side). 112 frames, 720x1280, 12 spp.
- QA_AUTO PASS. Frame-diff in-shot (g 263-355) median 5.66 / p90 21.79. 21.06 s/frame wall. Heads [61, 152] px, centre y [516, 727], chin max 797.
- Round-2 fixes: foreground sailor A moved inboard (x 1.5) and the camera slide/arc cut (15 px/s, no arc) so he stays >= 20 px inside the frame through g 363; sailor C moved out from behind the captain (2.4, 36.6) and the captain back and left (0.8, 38.4): three sailors visible side by side, each with a bucket and its own bail phase; nobody on the bulwark.
- Earlier fixes kept: cannon/carriage/hatch hidden, whip peak g 262-268, ONE shake g 330-339 on "เรือจมกัน", label of framediff.json.
- Known: the captain stands behind sailor A (head and hat visible, body partly covered); FG lantern glass flat lemon (set NOTE).
