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

## v5 partial re-render (film-13 workflow, g1276-1332 only; g1239-1275 and 1333-1348 unchanged from v4)
- Camera passed through the meadow tree canopy at g1308-1312: new path key at g1307 (22.5, 43, 8.0) keeps 8 m clear of the trees (checked with a nearest-vertex scan g1296-1338); the path of g1276-1332 changed slightly, so the whole range was re-rendered.
- Black rectangles at the right edge (x 640-720) g1311-1314 / 1324-1328: they were the navy right-hand saltire banners (cloth edge entering the frame while the camera is at x 9). The two right banners are hidden g1306-1332 (they leave the frame at the right anyway); the left banners and the g1345 match to H2a are unchanged.
- qa_auto PASS (one soft frame g1279 = motion), qa_jitter overall median 3.6 px (the 5 Hz ride shake in g1239-1275 is the only shake; it is in the plan for the charge and was left as delivered, say if it must go).

## v6 (g1300-1348 re-rendered; g1239-1299 unchanged from v5), H1 -> H2a is now a HARD CUT
- g1326/27 jump and g1327-1332 freeze: the H2a-camera blend is gone. ONE eased path from the g1297/1307/1316 keys to an end pose at g1348 (P_NECK + (0, 0.3, 0.15), still moving 0.5-1.5 m per frame equivalent, ~1 px/frame at the end). Frame-to-frame diff g1318-1348 is 13-24 on every frame (no jump, no zero-motion run; checked with a gray mean-abs diff).
- Black slab at g1308-1311: the 3D back ranks were parked 3 m under the bank and showed through the sloping ground; they are now hidden (hide_render) until g1318 and then rise behind the card ranks.
- Flank Scots wait 3 m farther from the lens (y slot - 3) and run in diagonally, so their faces stay clear of the caption band at g1305-1311.
- No camera shake from g1300 (the planned ride shake g1239-1299 is unchanged and decays to nothing by ~g1300).
- qa_auto PASS (soft frame g1279 = motion), qa_jitter median 3.2 px (ride only), GROUND.md re-run: FAIL 0, sheet1fps.jpg made.
