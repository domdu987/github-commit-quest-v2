# QA T21 = s21 (shots 21+22 as ONE camera-travel take): g1431..1655, handles g1427-1430 (hard cut in) and g1656-1663 (8 f, dissolve 13 out into T23)
Per QA_TEAM s I / WORKER20 s8. s22 folder deleted (merged here).
- qa_auto PASS (QA_AUTO.md; the note 'cut with no visible change at 1431' = the cut is against shot 20, handle frames are 3-D).
- qa_stats : `take.mkv: 7.9s, shots=1 ... saturation 0.535, brightness 88.2, in-shot motion median 15.93 p90 31.27`
- qa_stats2: `sat 0.535 vivid% 47.9 luma 88.2 contrast 39.2 detail 12.08 warm 21.9% cool 64.0% | motion med 15.93 p90 31.27 still% 0.0` (targets sat >= 0.50, vivid >= 45, luma >= 70: PASS)
- frame-diff (90x160 grey, in shot): median 14.01, p90 28.65 (>= 4 / 12 PASS). 237 frames, 11.48 s/frame wall, 22.08 cpu (2 procs x 2 threads, 720x1280, 8 spp). take.mkv 132 MB: delivered as take.mkv.part* (40 MB parts), take.mkv gitignored.
## The travel (one continuous camera, Hermite spline then c20.CamPath, no cut inside)
| g | what |
|---|---|
| 1427-1469 | RISE from beside the hut roof / post along the antenna wire up the tower to the summit lamp ("หอยิ่งสูง สัญญาณยิ่งไปไกล" 1434-1467); the lit lattice and lamp necklaces fill the frame, city below |
| 1468-1532 | at the summit the camera hovers 30-80 m above the ring plane looking down over lit Paris; the first ring is BORN at the lamp (flash) at g1468 and spreads over the city, a ring every 18 f (3 alive); the rings are not visible before the camera arrives |
| 1530 | "เสาอากาศยักษ์": blue-white glow along the wire + lattice edges (iron stays red), ring flash |
| 1532-1576 | SWOOP down the tower face and back along the avenue to the foot (lens shift 0 -> -0.03), landing on the group |
| 1576-1655 | old Eiffel, officer and three demolition men: bars on shoulders; 1586 'ไร้ประโยชน์' they stop; 1607-1619 they DROP the bars (3-D bars tumble); 1625-1630 officer salutes old Eiffel; Eiffel worried -> proud on a blink; men cheer (bounce); wagon + scrap cart roll away; 1642 snap push on 'ขาดไม่ได้' |
## Rule checks (WORKER20 s6-s8)
- Tower in frame and reads as the Eiffel Tower on every frame (rise: lattice fills the frame; wide: full tower); motivated lights: lamp necklaces + hut window + summit flash + wire glow, warm vs deep blue in every frame.
- Everyone acts in the group phase (sway, bars, drop, salute, cheer bounce); nobody floats (contact decals + proxy shadows, ground ray-cast); heads 45-84 px in the wide of five, centre y 560-720 (lowest bottom < 880); no face > 35 % of frame height.
- Mouths: none animated (held expression mouths only). No DOF, no text (in-world signs optional: none added).
- Wire: one thin pale wire for the whole take, own object (set's 4 fat wires hidden); rings: own thick tori (set's thin rings hidden); exposure +0.95; foreground kegs/crates at the sides of the group phase (kit20).
## Known misses / deviations
- Ground under the group still reads as a large dark slab below y ~880 in the last 3 s (under the captions); only side props fill it.
- 'Crowbar' = cast5 pickaxe prop; fallen bars are plain cylinders. Marks bunched at runtime so five fit at 15 D.
- The wire crosses the sky as a bright diagonal in the group phase (it runs summit -> post); it carries the glow.
- Hue not measured; the whole take is night (exception in the hue band).
