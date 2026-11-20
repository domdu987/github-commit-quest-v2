# QA T21 = s21 (shots 21+22 as ONE camera-travel take): g1431..1655, handles g1427-1430 (hard cut in) and g1656-1663 (8 f, dissolve 13 out into T23)
Per QA_TEAM s I / WORKER20 s8. s22 folder deleted (merged here).
- qa_auto PASS (QA_AUTO.md; soft-frame note g1566-1582 = the swoop landing; 'cut with no visible change at 1431' = cut against shot 20, handles are 3-D).
- qa_stats : `take.mkv: 7.9s, shots=1 ... saturation 0.578, brightness 84.5, in-shot motion median 15.69 p90 29.18`
- qa_stats2: `sat 0.578 vivid% 62.4 luma 84.5 contrast 38.7 detail 11.55 warm 20.0% cool 65.5% | motion med 15.69 p90 29.18 still% 0.0` (sat >= 0.50, vivid >= 45, luma >= 70: PASS)
- frame-diff (90x160 grey): median 13.94, p90 26.87. 237 frames, 10.99 s/frame wall, 21.18 cpu (2 procs x 2 threads, 720x1280, 8 spp). take.mkv 125 MB: take.mkv.part* (40 MB), take.mkv gitignored.
## Take-gate r3 fixes (QA-tech TAKE3_B)
1. Group phase g1577-1655: camera pushed in to a medium (CAM_BACK -5 D, tilt +9) with the five bunched tighter: heads Eiffel 85-106 px, officer 74-96 px, men 66-102 px, centre y ~700-725, nobody cut; the bare ground is now a lit COBBLED forecourt (brick texture, runtime plane under the group) with kegs at the sides: no flat slab.
2. g1607-1630 the dropped crowbars land on the cobbles and the officer's salute reads at 80+ px heads.
3. Ring edge-on slab g1526-1529: no ring is born after g1521 (RING_STOP), so no ring sits on the camera when it crosses the ring plane near g1529; the last rings die out by g1573.
4. Glow g1530-1539: a blue-white aura cone over the upper lattice (rim over the red iron), a blue halo tube on the wire and a stronger wire; the lower iron stays red-orange.
5. Wire, halo, aura leave at g1566 and the rings are gone by g1573: the group framing is clean (no white slashes).
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
- The cobbled forecourt is a runtime plane (16 x 14 m) under the group; seen from the swoop it is a visible rectangle of cobbles.
- 'Crowbar' = cast5 pickaxe prop; fallen bars are plain cylinders. Marks bunched at runtime so five fit at 15 D.
- Hue not measured; the whole take is night (exception in the hue band).
