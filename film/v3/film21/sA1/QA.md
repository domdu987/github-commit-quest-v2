# QA, segment A1 (BIGZOOM 1, first half) v3 - g 0..80 (+3 handles g81..83), film start

- **Camera:** one travelling `K.cam_path`: pre-roll key g-40 -> **new P_A at g80 exactly** (40, 10, 95 -> 150, 140, 20, 22 mm) -> g159 `hill_over` key (so g81-83 continue the move). Start = `P_HOOK` (-60, -260, 230 -> 60, 60, 0). Probed g0 (-60.7, -258.7, 229.0), g80 (40.0, 10.0, 95.0).
- **EXACT Scots call (team 5 / A2 must use the same one for the P_A match):**
  `K.build_world(['valley_wide'], fg=False, scots_wide=False)` then
  `K.scots_wide_line(n=26, banners=5, scale=2.2, toward=(120.0, -300.0))`
  (toward is south-south-east of the crag so the line stands on the SUNLIT flank facing the P_HOOK/P_A camera; blue saltire/white tunics from API §17, 5 saltire banners). The default bridge troops are removed and replaced by the knight-pair column below.
- **Ground (QA §K, GROUND.md PASS):** the column's horses were floating 10-45 cm over the deck and causeways in the first version; each horse is now placed on the ray-cast support height under it (deck, causeway ramp or terrain). The deck pairs (y -30..34) walk north 1.0 m over the segment, only where the support height does not change over that travel (3 pairs near the step were left out); the causeway pairs are a static batch. `GROUND.md` ray-casts all 54 horse support points: FAIL 0 (tolerance 2 cm). `GC.check` itself is not meaningful on the merged per-material meshes of the column and of the Scots line (the Scots figures are placed with `K.ground(x, y)` by `scots_wide_line`).
- **Bridge column:** knight pairs on the whole deck and both causeways (`np.arange(-56, 66, 4.2)`, pairs at x +-0.95, scale 1.4, caparisons crimson/white and crimson/cream, a rider each, one gold pennon per pair), walking north at 1.3 m/s.
- **Grade:** set default VIVID eased by `cam_path` P_HOOK -> P_A; no post pass.
- **Numbers (`take.mkv`, 84 frames, 32 samples):** `qa_stats2` sat 0.494, vivid % 51.6, luma 101.0, motion med 7.92 / p90 10.09, still % 0; `rhythm.py` median 9.64, p90 12.02; `qa_auto` PASS.
- **Known:** the Scots line and banners are findable from g0 on the sunlit lower flank (blue clusters with white saltire cloth) and grow as the camera descends; the knight pairs read as a double line on the bridge from this height.

- **qa_jitter:** overall median jitter 0.34 px. `qa_auto` PASS. Final numbers (`take.mkv`, 84 frames, 32 samples): sat 0.494, luma 101.0, rhythm median 9.57 / p90 11.88 (motion 7.89 / 9.98, still 0 %). Rendered on set 29eb5c0 (warm tent shade, API §18).
