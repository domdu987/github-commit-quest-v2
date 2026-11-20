# QA s03 = T03 round 6 (partial re-render of round 5; see the ROUND 6 section at the end)
# (round-5 text below)
# QA s03 = T03 round 5 (shots 3+4+5 as ONE continuous take; g 178..403, first_g 170, 242 frames = 8 + 226 + 8 dissolve handles)
Round-5 fixes after TAKE6 (QA-tech + QA-art). Move, timing (5 % at g ~203, 35 % at ~g 290, 42 % at g 300), landing and the two 13-frame dissolve handles unchanged.
- take.mkv 111.5 MB -> take.mkv.partaa/.partab/.partac (`cat take.mkv.part* > take.mkv`; take.mkv is git-ignored). 720x1280, 8 spp, 13.8 s/frame wall. qa_auto PASS.
- qa_stats2: sat 0.556, vivid 68.4 %, luma 98.4, warm 73 % / cool 10 %, motion median 10.74 p90 26.12, still 0.0 %. (own frame-diff 9.41 / p90 24.99.)
- BLOCKING fixes:
  1. Deck underside (g 362-411): a warm point up-light follows the camera (+2.5 D above it, energy 0 -> 9000 over g 322-362) and the end pitch is 22 deg (was 26): the deck undersides are now lit orange-brown, not a black slab; I did not measure the exact share of dark pixels at g 370-390 (the deck still covers the top ~25 % of g 360-380).
  2. White dome bottom-left (g 186-210): its black dots were the pn_stonedk scatter (now hidden with hide_render, no shadow blobs); the pale disc that remains in g 196-215 is a gravel patch (pn_gravelp) at ~3 % of the frame.
  3. Findable start: the wide is held 7 frames longer (distance keys 620 D g 170 -> 560 D g 178 -> 39 D g 203 -> 4.6 D g 300, so 5 % now at g ~203); a warm glow sphere (radius ~12 px on screen) plus a soft vertical light shaft (~3 px x 90 px) mark his table from g 170 and fade out before p 0.65; the set beacon is OFF after p 0.22. At g 171 the shaft is visible above the table; Eiffel himself is still ~1 px until ~g 185.
  4. The white flag pole and flags are removed (pnoink_white, pnoink_flag_* hidden with hide_render).
  5. The wheelbarrow and the mid-band timber / metal scatter (pm_timber, pm_timberdk, pm_metal) and the small near-black scatter (pf_/pm_/pn_ coal, soot, rivet, metal, stonedk) are hidden with hide_render (no leftover shadow blobs).
- Notes: the riveters are still stacked (two per platform, offset 1.6 D; not spread out further); the leg stays in frame during the crane-up but the pitch sweep still passes scaffold timber at g ~330-345; the landing is still ~g 290-300, later than the word (g 268, where he is a 23 % figure with his arm up); hat / arm overlap the leg beam at g 285-300.
- Not done: hue measurement; full-size crops at g 198 / 290 / 380 were checked on the 6-fps contact sheet only; dissolve ends not reviewed frame by frame.

## ROUND 6 (partial re-render, TAKE7 fixes; frames g 216-339 untouched)
- Re-rendered only g 170-215 and g 340-411; the end pose and the dissolve handles are identical. Commit: see git log (message "T03 round-6").
- A) Deck underside g 340-411: the follow up-light has 2.7x more energy from g 345 (9000 -> 9000 + 18000 W, ramp g 345-365), the source-less smoke puffs (pnoink_smokep) are hidden from g 340, and the delivery grade adds +18 % brightness ramping in over g 362-376 (deliver.py, post). Measured on the final frames: near-black share (luma < 25) in the top 35 % of the frame: 51 % -> 6.3 % at g 380 (8.2 % at g 370, 3.3 % at g 411); overall luma g 374-411: min 82, mean 89 (was 64-75); whole take luma 101.0, sat 0.546, vivid 68.1 %, motion median 10.71 p90 27.83 (qa_stats2). qa_auto PASS.
- B) g 170-215: the pale gravel disc (pn_gravelp) is hidden for g <= 215 (keyframed render visibility); the start marker is now a small warm yellow-orange work-lamp glow (emission colour 1.0/0.58/0.10, strength 2.2, no white core), faded fully out by g 190; the vertical shaft is dropped. The glow alone is a ~12 px warm dot at g 171-185.
- Not done: Eiffel himself is still ~1-3 px until ~g 190; hue measurement; dissolve ends not reviewed frame by frame.
