# QA s05 (shot 5, ship_rocks STORM_DUSK) — render19/team2, revision 2 (after the TAKE-gate QA_TECH)
Take g 253-364 (shot g 262-355; 9 in-handle after the hard cut, 9 out-handle for DIS 13). 112 frames, 720x1280, 12 spp.
- QA_AUTO PASS (magenta 0 %). Frame-diff in-shot (g 263-355) median 6.26 / p90 22.01 (target 4 / 12); framediff.json label fixed to shot 5's range.
- Wall 19.84 s/frame. Heads: width [59, 154] px, centre y [534, 740], chin max 810 (all above 880).
- QA_TECH fixes: (1) all three sailors now bail, spread in x/depth, each with a bucket and its own cycle phase; (2) nobody on the bulwark (B restaged inboard); (3) captain moved clear of the sail edge; (5) cannon, gun carriages and the hatch box hidden at runtime (deck_cannon_iron, deck_carr_w, deck_hatchw: they rendered as black blobs); (6) whip now peaks on g 262-268 (30 deg, 7 f window); (7) label fixed.
- The one shake stays at g 330-339 on "เรือจมกัน" (caption 10.91 s -> g 330).
- Known: sailor C partly behind the captain/B in places; FG lantern glass flat lemon (set NOTE).
