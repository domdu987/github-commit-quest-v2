# H1 THE CHARGE v2 (g 1239-1345 + handles 1346-1348), team 9 (fix pass after the TAKE gate)
World `build_world(['hill_over','bridge_end_north'])`, 32 samples, 720x1280, new cast colours (Scots blue, English crimson). CUT in, no internal cut.
- Ride g1239-1275 (kept): camera behind 5 running Scots, gorse whipping past, 5 Hz shake decaying. Overtake + swoop kept; the path now looks at the neck from g1297 (fix 5: no shelf slab filling the frame).
- Fix 1: the swoop ends LOW and CLOSE past the bridge mouth: camera (9, 40, 3.2) at g1316 with a lens zoom 22 -> 32 (wall figures about 12-15 % of the frame), then eases back (zoom-out, pull away) and lands EXACTLY on P_NECK (-2.0, 50.0, 4.6) -> (0.0, 22.0, 1.8), 22 mm at g1345. g1346-1348 begin the crane up.
- Fix 2: the slam is an event: the flank Scots (pre-placed by the banner sites) are still running at g1310 (accelerating, wall NOT formed), close across the deck mouth on g1316 with a 0.45 m overshoot, spears drop level together (spear prop x1.45 thicker), squash, tan dust puffs g1316-1327.
- Fix 3: three tall blue saltire banners (6-7.4 m) rise out of the ground g1312-1320 in the wall.
- Fix 4: the English first turn their heads back toward the wall (g_hit-10..), then jump back toward the lens in 8 frames from g1313-1321 (hop 0.9 D + 0.6 m back), five helmets pop off (own painted kettle-hat cards fly up and land crooked on the ground).
- Fix 6: nearest English now at y <= 39.2 (head bottoms at the end stay above y 880, heads around y 600-700).
## Numbers
qa_auto PASS (blur FAIL of v1 gone), saturation 0.496, motion median 11.4 / p90 18.2 (rhythm.py 13.6 / 20.9), no stills. Luma 131 (colour normalized at the conform per director policy).
## Known limits
- The English keep their own painted helmet on the head when the card helmet pops (no hatless sprite exists): reads as a pop at phone size, double hat when paused.
- The wall is 2 ranks of cards; the world's 3D wall is hidden. The deck/wall continuity with H2a is the director's call.
