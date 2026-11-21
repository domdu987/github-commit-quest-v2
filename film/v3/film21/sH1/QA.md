# H1 THE CHARGE v4 (g 1239-1345 + handles 1346-1348), team 9 (after the v3 TAKE gate)
Same H2a staging as v3 (WALL_Y 31.5, deck ends at WALL_Y-0.4, crimson English, big saltire banners). Frames g1239-1289 are the v3 render (unchanged code path); g1290-1348 re-rendered on set bb7aa85/bc93c82.
- **B2 (D6 handles)**: from g1326 the camera blends into H2a's EXACT path: `h2a_cam(g)` = `K.cam_path(None, H2A_KEYS, g)` with H2a's KEYS copied verbatim from render21/team3 sH2a/shot.py (g>=1342; before 1342 the same line continued backwards at its g1342 velocity), weight 1 from g1338. g1342-1348 therefore equal H2a's camera (lens 22), with H2a's approach from (-2.3, 53, 5.6) and its fast crane up.
- **B3 (slam bodies)**: the camera-side ranks are now Scots CHARACTER CARDS; 3D bodies only behind them (they rise g1318-1326 behind the cards). Exact front-rank call for H2a to copy (WALL_Y = 31.5, 14 per rank, 2 card ranks):
```
for rank in range(2):                                   # card ranks, rank 0 is the camera-side (northmost) one
    for k in range(14):
        tx = -9.0 + 18.0 * k / 13.0 + (0.5 if rank else 0.0); ty = WALL_Y + 1.1 * (4 - rank)     # y 35.9 and 34.8
        base = ("scot_a", "scot_b", "scot_c")[(k + rank) % 3]; cast = base + "_blue"        # add_variant(base, base+"_blue", "#2b50b8")
        hm = _hm(base, base + "_spear_wall", 1.70)           # actor scale; pose = STORY21[base+"_spear_wall"] with prop_r scale 1.45
# 3D back bodies (K.Batch 73): ranks 0..2 at y = WALL_Y + 1.1*rank, x = -9 + 18*k/13 + (0.5 if rank % 2 else 0), t_blue box (0.8,0.6,1.6) + steel ball + K.spear tilt (0,-0.9) h 2.4
```
  The slam: flank cards run in (still running at g1310), close g1316 with a 0.45 m overshoot, spear prop x1.45, squash, dust (tan puffs in front of the feet); banners rise g1312-1321.
- **B4 (chins)**: hop back reduced to 0.3 m; look target dips up to 1.2 m g1322-1344 (heads about y 790, chins about 840, inside the band at g1329-1336).
- N2: foreground gorse and a stone added at the bottom edge for the slam. N1/N3/N4 not done (banner colour is the set's; the hatless English sprite does not exist; the smoke strokes are the set's).
- §K ground check: `GROUND.md` (GC.check on 50 items, frames 1239..1348 step 10): FAIL 0. SUNK rows are the transparent card margin below the soles. Contact shadows on every card (contact=True). `sheet1fps.jpg` made.
## Numbers
qa_auto PASS (1 soft frame g1310 = motion), motion median 14.3 / p90 27.8. Colour left to the conform.
