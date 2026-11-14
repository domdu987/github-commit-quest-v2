# s26 QA: film 6b, shots 26-28 (48.60-56.80 s): the reveal as a cutaway diagram, then the 13th loaf levels the balance

Delivered: `frames/g_1452.png .. g_1709.png` (258 frames, 720x1280, 12 samples, 2 threads, no captions/audio) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 1452). Plan range g 1458..1703 ([1458, 1704)); g 1452..1457 and 1704..1709 are 6-frame
handles rendered in 3D. Also `meta.json`, `cues.json`, `contact.jpg` (24 frames, caption line y 880 drawn in red), `compare.jpg`
(three frames beside two director reference sheets). Scripts: `shot.py`, `deliver.py`; raw renders in `raw/s26` (diagram) and
`raw/s28` (bakery), git-ignored.

## Framings (a new picture every 1.1-1.9 s, camera always moving, all hard cuts)
- **26a** g 1452-1485 diagram: the sliced loaf on the left pan of a 2D balance, cool-blue blueprint backdrop; blue water drops sit
  in the crumb, some rise out of the crust and turn into white steam puffs; a "ควัน" label pops with a red X on "ไม่ใช่ควัน". Slow push.
- **26b** g 1486-1530 punch-in on the crumb: the drops pulse; label "น้ำ" points into the crumb on "มันคือน้ำใน".
- **26c** g 1531-1553 the drops race out of the crust (rate x2.5), tilt up with them into the steam; label "ไอน้ำ" ("ระเหยหนีไป").
- **27** g 1554-1592 fast pull back to the whole diagram balance: no new drops, the crumb dries paler (3 drawings) and the loaf shrinks
  8 %, the loaf pan rises (beam 0 -> +9 deg), a tag "500 ก." flips to red "480 ก." on "ก็ยิ่งเบา" (g 1574). Weights "500 ก." on the right.
- **28a** g 1593-1648 bakery MORNING, ECU of the hand balance's loaf pan holding a small basket of 12 (beam loaf side up, light);
  the pale 13th loaf drops in on "ก้อนที่สิบสาม" (lands g 1606, squash), the beam swings down and settles level, a "+1" burst badge pops (g 1610).
- **28b** g 1649-1709 wider: the whole balance level with the "+1" badge; little blue drops keep rising off the basket
  ("ชดเชยน้ำหนักที่หายไปกับไอน้ำ").

## Client rules
- **No depth of field**: the diagram camera has DOF off (own scene); the bakery uses common.Take (DOF off at build and every render).
  Everything sharp.
- **Heads / caption band**: no people in this take. Key objects stay above y 880 (loaf base ~840-900 only in 26c's last frames
  while the camera tilts up with the steam; balance base in 27 sits on the line). Labels and tags all above 700.
- **Mouths**: none.
- **Continuity**: the 13th loaf is the paler one (cast6 BREAD colours blended 55 % to cream; cast6's `tint` is a no-op, see
  `pale_svg`); same hand balance as shots 9/23/24 (`set_scale`, + = loaf side down; here -7 then level), the stock loaf on the pan
  hidden (`set_scale_loaf(False)`), the basket = cast6 `basket_svg(12)` x0.40 on a PropCard following the pan every frame.
- **Colour**: the diagram is the cool counter-colour (blue backdrop) against warm bread, as the plan asks; the bakery insert is the
  warm set with the blue street through the opening.

## 2D pieces
All drawn in shot.py: `loaf_cut_svg` (3 dryness variants), `drop_svg`, `puff_svg`, `post_svg`/`dial_svg`/`beam_svg`/`pan_svg`/
`weights_svg` (Chromium raster via common.svg_pngs) and the Thai labels / tags / badge with PIL + raqm in Kanit Black
(`label_png`, `badge_png`: correct Thai shaping; the outline layer is morphologically closed so small glyph loops stay ink).
Drop simulation `DropSim` is deterministic (seeded): ~24 drops always in the crumb until shot 27, each leaving drop turns into a
puff at 1.2-1.45 D above the base.

## Seconds per frame
See meta.json (`s_per_frame_wall_*`): diagram ~3.5-4.5 s wall, bakery ~20 s wall (two 2-thread processes in parallel on 4 cores).

## Differences from the plan
- Shot 28 "ECU basket" is staged on the counter's hand balance (a little basket of 12 on the loaf pan), so "+1 balances the beam"
  is literal in one picture; 28b widens to the whole balance.
- Shot 27's "scale beam rises" is the diagram balance (same diagram world as 26), not the 3D one.
