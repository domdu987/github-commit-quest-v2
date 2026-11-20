# QA s05 (shot 5, ship_rocks STORM_DUSK) — render19/team2
Take g 253-364 (shot g 262-355; 9 in-handle after the hard cut from shot 4, 9 out-handle for DIS 13 to shot 6). 112 frames, 720x1280, 12 spp.
- QA_AUTO: PASS (magenta 0 %). Frame-diff in-shot median 6.25 / p90 21.76 (target 4 / 12).
- Wall 19.4 s/frame, 38.1 s cpu (2 procs x 2 threads, shared with s04).
- Heads (4 actors): width 55-145 px, centre y 527-705, chin max y 772: all above the caption band 880. Sailors inboard of the bulwark (NOTE: no one outboard).
- Roll: set's own roll x2.2 (+bob x1.2, + 2.3 deg slow roll) keyed on ship_root with set_sea(t) same t; cards ride the deck (ride_ship), camera on_ship. Same sea clock as s04 (t = g/30), so the lantern/sea continue over the cut.
- Camera: whip arrival g 262-273 (24 deg eased pan-in), drift push 7 %/s + slide + arc; ONE shake g 330-339 (10 f) on "เรือจมกัน" (10.91 s). Never parked (<0.25 px/frame run 0).
- Sailors bail (scoop low -> fling + splash jet), staggering; comic, no injury. Mouths: fixed expressions, no lip-sync.
- Known: the whip lands inside the shot (g 262-273); the bailers are bunched left of centre (A in front of B/C/captain) and the in-handle g 253-261 holds the whip start. FG lantern glass flat lemon (set NOTE). Planned cut g 356 is a dissolve to shot 6.
