# s06 (T06) QA, round 2: film 20, shots 6+7+8 as ONE camera-travel take -- CAFE cafe_wide scene, DAY, 1887 (stub view)
Delivered: take.mkv.partaa/ab/ac (83 MB split 40M; `cat take.mkv.part* > take.mkv`), first_g 396, 212 frames. Shot g 404..603 (13.47-20.15 s); in-handle 8 (g 396..403, DIS 13), out-handle 4 (g 604..607). 23.4 s/frame wall, 45.8 s cpu, 8 spp.
**Checks:** qa_auto PASS. `qa_stats.py`/`qa_stats2.py`: sat 0.563, vivid% 48.8, luma 100.6 (was 110.4: exposure -0.3), contrast 58.6, warm 63.3 % cool 18.1 %, motion med 15.91 p90 24.28, still% 0.0 (gates: sat >= 0.50, vivid >= 45 %, luma 85-110, motion >= 4 / 12: met). My own diff: 14.75 / 22.10.
**end_cam (meta.json) = team7's exact T09 start (their s09/meta.json start_cam):** g603 camera (2.618, 9.596, 1.334) D looking at (1.692, 13.160, 1.999) D; handle g604 (2.599, 9.600, 1.350) looking at (1.692, 13.160, 2.000); 22 mm, no shift; drift (-0.019, +0.004, +0.016) D/frame, g605-607 keep it. Maupassant sits on the banquette the whole take, idle + sips (arm sip fades out by g 597), head ~150-180 px at the end.
## Round-2 fixes (TAKE2_A)
- Half-cut artists g437-480: artists spread wider (radius ~2 D from the table), start aim shifted left; the camera dives onto the sheet by g 466 so the group leaves frame cleanly (the edge crops are single-digit frames during the descent).
- Papers: news20 scaled 0.6 and the hands lowered, no paper over a face in the wave beat.
- Rise g 512-580 stretched (was 512-572): corner speed 20-35 px/frame instead of 45-65; the purple artist moved back (face <= ~25 %).
- Ending: new landing pose (2.6, 9.6, 1.35 -> exact team7 values): ceiling gone, floor ~30 %, Maupassant ~150 px, window with stub + black smoke behind him; glare patch gone with exposure -0.3.
- Artists' mouths closed (runtime expression `outraged_c`, frown mouth): only Maupassant's mouth is drawn at all and it is held 'smile'.
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
