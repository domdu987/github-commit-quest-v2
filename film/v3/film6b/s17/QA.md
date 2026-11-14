# QA, film 6b take s17 (shots 17-21, g 964..1237, handles g 958..963 and 1238..1243)

take.mkv = g 958..1243 (286 frames, first_g 958). 720x1280, Cycles 12 samples, OIDN, no depth of field, every frame rendered in 3D for this clock.

| shot | g | set / framing | what is on screen | word-literal hook |
|---|---|---|---|---|
| 17 | 958..1028 | market AFTERNOON, low push from MS to CU | hooded stranger walks in (long shadows to screen-right), stops, turns, throws the hood back (g 1007-1016), blink, inspector_royal (tabard, chain) + snap push to CU (head ~390 px = 54 % width) | "บ่ายวันนั้น" / "ผู้ตรวจของพระราชา" (swap on g 1017) |
| 18 | 1029..1082 | bakery AFTERNOON, Henry MCU, punch-in g 1062 | Henry counts 1..10 on both hands next to the basket of 12 with the Thai tag "12 ก้อน"; punch-in: smug Henry over the tag (head ~330-356 px) | "ซื้อขนมปังหนึ่งโหล" (tag) |
| 19 | 1083..1131 | market, looking down into the big bread pan | inspector_royal tips the basket, 12 loaves fly one by one onto the pan (set_loaves 0 -> 12), beam rises from -11 and stops at -7 | "เทลงตาชั่งกลางตลาด" |
| 20 | 1132..1163 | ECU of the balance needle on a blue enamel dial "ผ่าน / ขาด!" | needle (3 x beam tilt) stays on the red side, trembles; on "ขาด!" g 1157 the label flares yellow with burst lines + snap punch-in | "เข็มชี้ว่าขาด!" |
| 21 | 1164..1243 | market: tracking MCU g 1164-1196, low wide g 1197- | two guards drag pale sweating Henry (heels sliding); wide: the pillory with the sign "ห้ามขายขาดน้ำหนัก!", townsfolk pointing / laughing | "ลุงเฮนรี่โดนลากไปที่ขื่อทันที" |

Checks
- Heads above the caption band (y 880): all main heads 500-680 px (head_report in raw/s*/g_*.json). Main head centre 0.39-0.53 H except the
  shot-21 wide (exempt) and shot 17's walk (0.41-0.44 H).
- Mouths: no quoted line in this take; all mouths are static expression mouths (no talk_mouth).
- No DOF, no motion blur. Complementary colour: warm gold sun vs blue shade / blue sky in the market, blue enamel dial vs red/yellow labels.
- Signs: Kanit Black, ink outline, rasterised via Chromium (dial, tag, pillory board).

Differences from the plan
- Shot 18: the hooded customer is not in frame (over-the-shoulder hid Henry); the count is on Henry's fingers 1..10 and the "dozen"
  is carried by the basket tag "12 ก้อน".
- Shot 17 reveals the tabard in the square; shot 18 does not show the stranger again, so there is no continuity clash with the hood.
- Shot 20 dial and needle are added PropCards (the set's own pointer hides inside the pivot block); the needle swings 3x the beam tilt
  for readability.
