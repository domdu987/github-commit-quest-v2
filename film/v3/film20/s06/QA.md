# s06 (T06) QA, round 3: film 20, shots 6+7+8 as ONE camera-travel take -- CAFE cafe_wide scene, DAY, 1887 (stub view)
Delivered: take.mkv.partaa/ab (83 MB split 40M; `cat take.mkv.part* > take.mkv`), first_g 396, 212 frames. Shot g 404..603; in-handle 8 (g 396..403, DIS 13), out-handle 4 (g 604..607). 20.7 s/frame wall, 40.5 s cpu, 8 spp.
**Checks:** qa_auto PASS. `qa_stats2.py`: sat 0.539, vivid% 45.6, luma 103.4, contrast 57.2, warm 65.4 % cool 16.5 %, motion med 16.74 p90 24.13, still% 0.0 (gates: sat >= 0.50, vivid >= 45 %, luma <= 110, motion >= 4 / 12: met; vivid is only just over).
## The join T06 g603 -> T09 g604 (proof: `join_strip.jpg`, top row T06 g595-603, bottom row T09 g604-612 from render20/team7 s09)
- Camera: g603 = (2.618, 9.596, 1.334) D looking at (1.692, 13.160, 1.999) D, g604 = (2.599, 9.600, 1.350) -> (1.692, 13.160, 2.000), 22 mm, no shift, drift (-0.019, +0.004, +0.016) D/frame; = team7's start_cam.
- Maupassant is team7's own pose at g604 (their pose_t09 with ur = uf = 0: crouched on the banquette edge at (seat.x, seat.y - 0.30), hands at the sides, `sneer`, mouth flat, same idle terms), same canvas / PPD: NO wine glass. The banquette bar in front of his coat is T09's own geometry, present in both.
- Colour: my film-wide grade (sat 1.45, exposure -0.3) ramps to T09's own look (sat 1.08, exposure -0.37 relative to cafe_wide's, measured against their frames) over g 560-603; smoke thins from g 586 to none at g 603 like T09 (no smoke).
- Measured mean abs grey diff (90x160): T06 602->603 5.64, **T06 603 -> T09 604: 4.75**, T09 604->605 4.41, i.e. normal motion, not a cut (the old take had 82).
## Round-3 fixes
- Artists now stand on the north side of the table (the dive passes under them): the top-hat artist is whole g 396-448 and leaves through the top, not the side; papers are lowered / removed (arms down, leaning in) from g 452, so no paper covers a face g 456-480; waiter dropped cleanly (never in frame); artists' mouths closed (`outraged_c`).
- Glare patch gone with the T09 exposure ramp; floor in the end pose is T09's own (~30 %).
## The travel (waypoint camera, continuous velocity, no stop; min corner speed 3.6 px/frame)
| g | beat |
|---|---|
| 396-440 | slide past the four outraged artists waving greeked newspapers; sun shafts + gas lamps; Maupassant seated far right at the banquette |
| 430-446 | push-in SNAP on "สี่สิบกว่าคน" (444) |
| 446-490 | descend and push DOWN onto the protest sheet (the cafe_table_insert pose at g 490); "PROTESTATION" heading (Latin FONT mesh) on the sheet; first signature lands g 471 ("ลงชื่อประท้วง" 469) |
| 483-494 | quill passes from the painter's sleeve to the poet's sleeve; second signature lands g 496 |
| 512-572 | rise off the sheet, swing to the window; forge smoke ramps 0 -> 1 over g 513-572; artists switch (hidden behind the sheet g 500) from waving to finger-jabbing at the window; stub + black column of smoke clear in the window on "เหมือนปล่อง" (572) |
| 572-603 | sweep down + right to the banquette, arrive on team7's pose |
Mouths: none animated (outraged = held mouth, Maupassant 'smile'). No DOF. Text only the Latin "PROTESTATION" on the sheet (no LE TEMPS masthead: the news20 sprite is cast art). Feet on the floor, contact decals on (floor z 0 verified).
## Remaining weak points
- g 462-520 (the sheet insert / rise): the camera is 1-2 D from the sheet, the composer / poet faces are large (30-40 % of frame height, up to ~1.5 s) and partly cropped by the top edge; they are the planned over-the-shoulder / insert moments.
- Frame diff median 15-16 / p90 24: far above the targets because the travel is continuous (no static holds).
- Hands, sleeves and quill are simple meshes (the handover reads as a sleeve crossing the frame).
- Floor 30-35 % in g 396-440 (wide start, FG chair + checker) and ~30 % at the end.
- Only the Latin "PROTESTATION" heading was added as text (the LE TEMPS masthead would need cast art).
