# QA-tech, SET gate, film 11 (set3d11 dairy) — VERDICT: FAIL

Inputs: dairy_work/final/*.png (11 tiles, 720x1280), contact.jpg, dairy_work/hue_rows.txt, API.md, BRIEF.md.
Placeholder cards are stand-ins; card pose issues (standing instead of seated/lying) are noted once (issue 1) and not counted per tile.

## Numbers
Laplacian variance, whole tile / lower third (y 880-1280):
barn_wide 470/381, barn_milking 289/151, barn_high 423/191, barn_door 253/42, garden_hut 556/311, garden_queue 725/281, lane_high 907/560, lane_wide 461/81, room_day 242/34, room_night 218/10, room_morning 236/22.
Whole-tile values are sharp (>200); no DOF seen. The lower third of barn_door, lane_wide and the three room tiles is near-flat (variance 10-81).
Hue (hue_rows.txt): shade hue 242-259 and magenta 1.5-8.1 % all inside the client limits. But hue_report flags OUT on every row, and blue+violet dominates the A tiles: barn_milking 84 %, room_day 90 %, room_morning 89 %, barn_door 67 %, barn_high 74 %, room_night 91 %. The rows are mostly shade-blue, not "warm lit".
Heads: all chins above y 880 (max chin 735 lane_high). No black/magenta/blank regions, no text, no signs found.

## Issues (tile, where, what, fix)
1. All tiles with seated/lying slots: barn_milking, garden_hut, room_day/night/morning. Cards stand upright on the stool/bed (sarah on the stool, boy on the stool, boy_bed upright in bed). Stand-in only. Real cast poses must be seated/lying at the contact z.
2. barn_wide: Blossom (2D puppet marker) not visible; jenner (-6.4,10) and boy (2,9) not in frame. BRIEF/API list them for the preset. Move the cameras or stand points so the listed slots are visible, or drop them from the staging.
3. barn_wide: not "golden morning". The sun pool and door light are only a thin strip at the left edge; the frame is violet-brown. Raise the key or aim the sun pool into the frame.
4. barn_wide: the loft hay is a floating cloud-like blob with no visible support (x 100-700, y 310-420). Add a loft floor edge or beams under it, or reshape the hay.
5. barn_wide: sarah and maid feet are on the far hay or boards at y 600-620, with no clear contact shadow. Both are small and distant, so scale is hard to judge. Add a contact blob under cards.
6. barn_wide: the near hens (about 1.6 D body) and the crates are huge against the milkmaids. They are camera-relative, but they dominate the lower third. Shrink the fg props 30 % or push them out of the frame.
7. barn_milking: no "golden morning" light. The whole floor and lower half are flat blue-violet (84 % blue). Warm the shade or add the sun pool on the floor around the stool.
8. barn_milking: the Blossom marker is a pale blue-white blob with a flat look, with a hen in front of the pail and the pail overlapped (x 370-470, y 700-830). The stool is under Sarah (OK); the pail sits beside and to the right of the stool (OK) but is half hidden by a hen. Remove or move the hen.
9. barn_milking: loft hay clouds at the top right (x 330-720, y 350-480) float with no support; a pitchfork/stool silhouette is clipped at the right edge (x 620-720, y 760-980).
10. barn_high: right maid is clipped by the right frame edge (x 640-720) and the left villager is clipped by the left edge (x 0-45). Shift the camera or slots.
11. barn_high: a translucent pale rectangle (sun shaft/door-plane) overlays the scene from x 250 to 720, y 230-870. It reads as a glowing glass panel. Fix the shaft geometry or fade it.
12. barn_high: the light state C does not read as amber; the lower half is saturated blue-violet (74 %) and the floor in the lower third is dark with a large shadowed blob (x 500-720, y 900-1100). Warm the amber and lift the shade value.
13. barn_high: the loft hay blob floats at the top right (x 480-720, y 130-300), unsupported. Blossom missing (slot at -4.2, 17.4).
14. barn_door: Sarah is in the foreground at the left in front of a huge pail (x 40-230, y 770-980); the pail (about 3 D wide) is far too big and hides her feet. Remove or shrink. Her legs are cut by the pail so contact is not visible.
15. barn_door: wagon wheel is clipped at the left edge (x 0-50, y 550-740) and the right edge (x 680-720, y 700-820). The hay on the wagon (x 500-660, y 625-725) is a floating lump above the wheel, not seated on a wagon bed.
16. barn_door: the vill_a/vill_b slots and Blossom are not visible. The outdoor background is hazy beige with a horizontal stone wall; it reads washed out. The lower third is almost empty (variance 42) blue floor with a few thin straws.
17. garden_hut: doctor (-4.4, 2.6) is hidden behind Sarah (his head at x 650-690 behind her hat). Overlap. Move one of them.
18. garden_hut: hens are clipped at the left edge (x 0-150, y 740-940). The brown hen in front hides Sarah's feet, and the Jenner/Sarah feet have no visible contact shadow. The foreground flower stalks (x 280-720, y 880-1250) are about 5 D tall, too big and coarse for "small near-camera foliage".
19. garden_hut: the cloud is a flat cut-out with a hard violet underside and straight edges (x 0-330, y 0-220); it reads as a sticker. Soften or replace.
20. lane_wide: the lower third (y 880-1280) is bare dirt with a few pebbles and petal specks, only a goose at the top of it (variance 81). BRIEF forbids an empty lower-third floor. Add props or ground clutter.
21. lane_wide: the top-right (x 590-720, y 170-340) shows a hay bale/roof edge and a pale blue-white panel that look like a floating fragment clipped at the frame edge. The barrel at the left edge (x 0-50, y 750-900) is clipped.
22. lane_wide: scale. The brown villager_c (37 px head) vs the foreground goose and cart reads fine, but the maid at (29,-9.2) stands on the cart-side next to a wagon box (x 560-720, y 690-800) with her feet hidden behind it. Move.
23. lane_high: bottom-edge clipping of the sheep/goose (x 440-490, y 1180-1280), the hay at the bottom right (x 590-720, y 1150-1280), a crate at the bottom left (x 100-170, y 1200-1280). Pull the fg props inward.
24. lane_high: the crowd cards are tiny (head px 28-33, minimum for phone legibility is about 40). The pockmark/mock reaction is unreadable; smoke is a chain of polyhedra (x 430-720, y 10-250) that reads as a column of rocks. The hills show visible polygon seams (x 0-720, y 100-300).
25. garden_queue: the "long queue from the gate to the hut" is not readable. The people stand behind the picket fence and in the flower beds (y -3.2 line), and only 3 plus the boy and Jenner are visible; the right figure is clipped by the right edge (x 680-720); the doctor at the tail (8.2,-3.6) is out of frame. There is no visible queue path on the ground. Move the camera or slots so the flagged path with the queue is visible, and keep the cards on the path, not in the flower beds.
26. garden_queue: Jenner and the boy are small and half hidden behind the fence post and hut edge (x 60-190, y 590-740). The foreground fence cuts the middle of the frame. A brown dog/hen stands against the fence (x 430-540, y 830-970) intersecting the fence pickets.
27. room_day: the bed is not readable. Only a quilt edge and a headboard post (x 0-300, y 450-680) show; the boy card stands there upright. BRIEF wants a bed under the window; reframe so the whole bed shows. Daylight is a faint stripe on the rug; the room is dark violet (90 % blue/violet), not a daylit morning.
28. room_day: hanging hams/herbs are big pale faceted blobs (x 480-580, y 220-370; x 300-340, y 370-430) that float like balloons. A tiny object floats at (648,218). Jenner is standing behind a chair with his legs crossing the seat (x 480-620, y 660-800); the contact is unclear.
29. room_night: no candle visible. The table with the candlestick at (3.4,5.5) is off-frame right; only the hearth flame shows at the right edge (x 690-720, y 590-650). BRIEF requires a candle in room_night. Reframe or move the candle into the frame.
30. room_night: doctor in the door (6.4,4.8) and Jenner (1.2,2.2) are not visible; the door is not visible. The false-payoff beat (doctor pointing at the door) cannot be staged from this camera.
31. room_night: not dusk/night-readable. It looks the same as room_day with lots of bright yellow mote dots (x 60-700, y 290-560) that read like stars or sparks. Cut the motes at night, darken the window to amber/dusk, and add a candle glow.
32. room_morning: the mother is clipped by the right edge (x 500-720, y 450-880); her feet are behind the stool (contact unclear). Morning sun appears only as a patch at the bottom right. No clear sun on the bed; the boy has no jump space visible. Bed not visible.
33. room_day/night/morning: the lower third (y 880-1280) is mostly flat floorboards with one barrel, near-flat (variance 10-34). Add rugs, props or objects there.
34. room_day/night/morning: the three tiles are almost identical (same camera, same dark violet); the light state difference (A day vs C night vs A morning) is not visible. Differentiate light colour and sun angle.

## Passes checked
No blur/DOF (whole-tile Laplacian variance 218-907). No tile has a head at or below y 880. No text or signs. No black/magenta/blank regions. Shade hue 242-259 and magenta 1.5-8.1 % inside limits.

## Verdict: FAIL (34 issues; blocking: 2, 3, 7, 12, 25, 27, 29, 30, 31, 33, 34)
