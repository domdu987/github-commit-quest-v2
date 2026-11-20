# H1 THE CHARGE (g 1239-1345 + 3 handle frames 1346-1348), team 9
World `build_world(['hill_over','bridge_end_north'], fg=['bridge_end_north'])`, 32 samples, 720x1280. CUT in, no internal cut.
- Ride g1239-1275: camera behind 5 Scots running with spears forward (cast sprite cards, contact shadows, gold rim), gorse whipping past, 5 Hz shake decaying (0.9 s).
- Overtake + swoop g1275-1316 (Hermite from the ride velocity, ~190 m), settle to P_NECK, which is hit EXACTLY at g1345 (-2.0, 50.0, 4.6) -> (0.0, 22.0, 1.8), 22 mm. g1346-1348 begin the crane up (z +0.01..0.06 m, ease-in).
- Slam g1316 ("ปิดหัวสะพาน" 43.78): pre-placed Scots (flanks, by the blue saltire banners) sprint in and form a 2-rank spear wall (spear_wall pose, blue-tinted cards); 10 crimson English (no blue) hop back and wobble their helmets. Bloodless.
- Hill dressing cleared in a 24 m circle on the shelf for the run lane (monkeypatched at runtime, set module untouched). World 3D spear_wall hidden (replaced by the cards).
## Numbers (qa_stats / qa_stats2 / rhythm.py)
saturation 0.508, vivid 54 %, luma 130 (over the 85-110 band: bright sunny exterior; allowed up to 150 with sat >= 0.47 per QA_ART_SET ruling, listed here), motion median 10-12, p90 20-23, still 0 %.
## Notes / known limits
- Wall at P_NECK is small (22 m, ~60 px figures) and rank 2 is partly hidden behind rank 1; the 4-5-rank wall of API §13 was not available in the set code, so H2a should compare against my 2-rank card wall or the director may tint the world wall.
- The Scots wall tint is a light blue multiply on the cards; the saltire banners are the world's.
- Placeholder crowd cards (meadow) are not re-faced per frame; they are tiny in this segment.
- qa_auto: one FAIL, 'suspected blur' on 6 frames (g1280, 1281, 1299, 1300, 1302, 1307): the sharp-frame check trips on the fast terrain/water sweep of the swoop (no blur or DOF is rendered; it is low-texture water and sky at speed). Left as is; director to judge.
