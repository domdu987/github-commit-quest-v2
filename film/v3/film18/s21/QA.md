# QA s21 (film 18; moved from team 4 to team 3 by the director, rework of rounds 14/15 + FINAL-gate B4 fixes)
Range g 1596-1682 (take.mkv g 1590-1688, 99 frames, 6 handle frames each side), transition in: cut. 720x1280, 12 samples, OIDN, 2 threads, 24.1 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames)
median **5.57**, p90 **13.29**, min 1.31, max 17.61, frames < 1: 0 (gate median >= 4, p90 >= 9/12). Motion = the set's eased 9 %/s push, slide 6 px/s, sway, and ONE held snap x1.5 at g 1644 (no pulses).

## Round-14/15 blockers
1. **Ground before the snap** (director script `film18/qa/ground_share.py take.mkv 1590 1596 1683 10`): g1596 0.25, g1606 0.29, g1616 0.30, g1626 0.30, g1636 0.29, g1646 0.27, g1656 0.24, g1666 0.21, g1676 0.18: max **0.304** (<= 0.35 before the snap, <= 0.30 after). Done with: five dark, rim-lit foreground props (3 jars, a bowl, a bronze helmet: `J.prop_pot` / `J.prop_helmet`, toon-glazed dark) in the lower third 1.5-2 D from the lens, a darker flat floor (0.026/0.02/0.03 instead of 0.045/0.035/0.05) and the camera look-at lowered (z 2.4 -> 0.9). `J.dress_ground` not used (director note).
2. **Hero mouth <= y 840 on rendered frames**: mouth interior lowest pixel 769 (g1676), 761 (g1679), 787 (g1681), 796 (g1682); with the outline about 815 at g1682 (margin > 20 px). Checked on the rendered PNGs (brown mouth mask) and on 1:1 crops with a y 840 line.
3. **Soldiers' shock reads**: three silhouettes with arms thrown up and leaning back, frozen at the snap; the neon outline is now a thin warm fire-side rim (7 % of the figure width instead of 20 %, k 1.7) plus a thin moon-blue rim on the far side. The cup is a 2x larger bronze cup that leaves the right soldier's raised hand on "สัตว์ประหลาด" (g ~1644), is held up in front of him for a moment and falls toward the lens, landing at g ~1664 (visible on the 6 fps sheet at g1646 / g1658).
4. Kept: ONE held snap x1.5 at g 1644 on the word, the rage faces, flame cards on the tail tips (wall of fire behind the herd from g 1645), moon-blue rim; deep night opening with blur on the dark frames accepted by the director.

## Numbers
- qa_auto PASS (QA_AUTO.md, phone_sheet.jpg). Max soldier chin y 630 (< 880).
- Ground max 0.304.
## Notes
- At g >= 1675 the hero ox covers the soldiers (the three stay 7-13 D from the lens, the hero charges across them): the shock reads at g 1646-1668.

## FINAL-gate B4 fixes (round 16)
- **See-through pots: fixed.** The row of foreground props no longer uses the toon-glaze emission material (its facing ramp read as a glowing x-ray). They now keep `J.prop_pot` / `J.prop_helmet`'s own opaque clay / bronze materials with outline and lathe detail, lit by two small point lights (warm fire side, cool moon side) that ride with the camera. `scene.cycles.transparent_max_bounces` is 64 (c18.begin).
- **Cups: fixed.** The dropped / raised cup is now a small lit 3D bronze jue-style cup (bowl, rim ring, two posts, three legs, Principled bronze with a little emission and its own warm point light), 2x the old size, leaving the right soldier's raised hand on "สัตว์ประหลาด" (g ~1644), held up for a moment and falling toward the lens (g1646 held above his head, g1658 gold cup falling in front of the right soldier, lower right at g1668).
- **Palette: fixed.** Sky = moon-blue (RGB 25,80,175 flat), blue-tinted dark ground, key (moon) light x0.8 instead of x0.3, warm fire kept (flames, tail lights, warm rims). In-shot HSV saturation mean 0.655 (director target >= 0.48), luma mean 58.9; the shot now sits next to s22's moonlit blue.
- Kept: mouth at y <= 840 (mouth interior lowest pixel 769 at g1676, 796 at g1682), soldiers' shock with a thin warm fire-side rim, the held snap x1.5 at g1644, rage faces, tail-tip flames.

## Final numbers (this render)
- Frame diff median 6.04, p90 13.64, min 1.57, max 17.87 (n 86), frames < 1: 0.
- Ground (`ground_share.py take.mkv 1590 1596 1683 10`): g1596 0.14, g1606 0.08, then 0.01-0.03: max **0.136** (<= 0.35 before the snap, <= 0.30 after; the blue floor is saturated so the metric no longer counts it as plain).
- qa_auto PASS (QA_AUTO.md, phone_sheet.jpg); max soldier chin 630.
