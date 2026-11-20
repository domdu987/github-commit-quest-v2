# s06 (T06) QA: film 20, shots 6+7+8 as ONE camera-travel take -- CAFE cafe_wide scene, DAY, 1887 (stub view)
Delivered: take.mkv.partaa/ab/ac (85 MB split 40M; `cat take.mkv.part* > take.mkv`), first_g 396, 212 frames. Shot g 404..603 (13.47-20.15 s); in-handle 8 (g 396..403, DIS 13), out-handle 4 (g 604..607). 22.5 s/frame wall (two processes), 43.7 s cpu, 8 spp.
**Checks:** qa_auto PASS (the "cut g 0" note is not a cut). `qa_stats.py`: saturation 0.545, brightness 110.4, in-shot motion median 14.09 p90 24.54. `qa_stats2.py`: sat 0.545 vivid% 47.2 luma 110.4 | warm 67.8 % cool 14.9 | motion med 14.09 p90 24.54 still% 0.0 (gates: sat >= 0.50, vivid >= 45 %, motion 4 / 12: all met). Luma is at the top of the 85-110 band.
**end_cam (meta.json):** g603 = camera (3.533, 6.506, 0.983) D looking at (1.692, 13.16, 2.944) D, 22 mm, no shift; handle g604 = (3.505, 6.531, 0.994) looking at (1.692, 13.16, 2.942): team7's exact T09 start numbers; the camera arrives with ~0.03 D/frame velocity (push + crane), g605-607 keep drifting. Maupassant sits on the banquette (maupassant_seated_toast_smug, mouth held, idle breathing only from g 585).
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
## Deviations / weak points (honest list)
- g 462-520: the camera is close over the sheet; the composer's head is cropped by the top edge at ~g 466-495 and the painter/poet faces reach ~35 % of the frame height at g 523-545 (poet). Close ones are the planned sheet insert + over-shoulder moments.
- Hands, sleeves and quill are simple runtime meshes (balls + tapered sleeves); the handover reads as a sleeve crossing the frame.
- Maupassant is a seated card ~7 D away (head ~60-100 px) and legs dangle slightly in front of the banquette; he does nothing but breathe and sip.
- Checker floor is 30-45 % of the frame in g 396-440 and again in the end pose (that pose is team7's cafe_low): ceiling+floor exceed the 25 % guideline there.
- The artists' pose swap (waving -> pointing) happens at g 500 while the camera looks at the sheet; waiter is off-frame right.
- Saturation grade 1.45 (runtime CO.setup_grade) gives the vivid look; the whites are slightly hot (luma 110).
