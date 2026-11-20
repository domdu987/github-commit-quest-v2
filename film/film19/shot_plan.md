# Shot plan, film 19 (ไอ้ช่างไม้)

## Clock
- Narration: film/film19/audio/narration.wav (71.90 s), placed at +0.10 s.
- Frame of a shot boundary: g = round(t*30). Frame of an in-shot event at narration time x: round((x+0.10)*30).
- N = 2160 (72.0 s). Captions: film/film19/script/captions.json; the phrase times below are caption starts on the narration clock.
- Sentence starts:

| Sentence | Start (s) |
|---|---|
| hook | 0.00 |
| pivot | 6.37 |
| boss | 15.54 |
| nickname | 25.78 |
| count | 28.74 |
| reveal | 33.86 |
| aha | 46.12 |
| false | 52.71 |
| crisis | 55.49 |
| ending | 61.86 |
| end | 71.90 |

## Look
The SET gate passed: film/v3/set3d19/QA_ART.md, rounds 1-6. Render teams must respect the NOTE lists in rounds 2-4.
- Sharp. NO DOF. NO text anywhere.
- Warm lit 3D world, with foreground props 1-2 D from the lens in most shots.
- Heads: whole heads above y 880, head centre at y 450-760 (wides are exempt).
- Never add the removed `caption_shade` card.

## Camera (production-lessons §10, film-2 rhythm)
- Every shot moves: push/pull 6-10 %/s plus a slide of 20-60 px/s. One eased snap on the strongest word in every shot over 2 s.
- No near-static hold over 1 s.
- Laughing characters bounce about 0.06 D at about 3 Hz.
- Joins: DIS = dissolve, 11 frames (13-15 f for a place or time change). CUT = hard cut.
- Target in-shot frame-diff: median ≥ 4, p90 ≥ 12.

## Mouths
Only the astronomer (astro19) moves his mouth, and only inside his quotes:
- boss quote, shots 8-9: 20.80-25.75 (laugh "ฮ่า ฮ่า ฮ่า!" then "นาฬิกาเนี่ยนะ! … ให้พระราชามาจับเวลาเองเลย!")
- false quote, shot 20: 54.25-55.45 ("ฟลุ๊ค! ต้องลองใหม่!")

Everyone else keeps a still mouth. Comic falls only, with no injury.

## Cast and set
- Cast: film/v3/cast19 (API.md, STORY19).
  - harrison19 (young=1 in shot 11; default in shots 1, 12, 14; grey/old look in shot 13 via the default with white hair: old=1; old=1 in shots 23-26)
  - william19
  - astro19, the mocker
  - astro19_b and astro19_c
  - king19
  - captain19
  - sailor19_a/b/c
- Set: film/v3/set3d19 (API.md, SHIP_API.md). The preset, light and hook names are as in API.md.

| # | t0-t1 (s) | in | set / preset / light | action (anchor words) | camera |
|---|---|---|---|---|---|
| 1 | 0.00-1.91 | — | WORKSHOP shop_bench DAY, set_clock(1), balance rocking | HOOK IMAGE: Harrison (default, apron, shavings) behind the bench beside his big brass H1 sea clock, presenting it proudly with both arms, grinning; the H1 bars rock | low, already moving on frame 0; push 8 %/s + slide; plane and shavings in FG; snap on "นาฬิกา" (1.12) |
| 2 | 1.91-3.65 | CUT | SHIP ship_aerial NOON | "เรือนเดียว … เรืออยู่ตรงไหนกลางทะเล": the lone ship on the endless glittering sea | high drift + slow orbit, pull 7 %/s |
| 3 | 3.65-6.37 | CUT | HALL hall_window DAY | "ทั้งที่นักปราชญ์ยังทำไม่ได้": astro19_b peers through the brass telescope, astro19 beside it scratches his wig, puzzled | slide past the telescope tube (FG), push; snap on "ทำไม่ได้" (5.80) |
| 4 | 6.37-8.74 | DIS 13 | SHIP ship_rocks STORM_DUSK | "อังกฤษ เกือบสามร้อยปีก่อน กลางทะเล…": captain19 at the rail peers into fog over a blank chart, lantern swinging | push 7 %/s, lantern FG |
| 5 | 8.74-11.88 | CUT | SHIP ship_rocks STORM_DUSK, set_roll strong, rain | "เรือจมกันเป็นลำ ๆ": the ship lurches past the black rocks; sailors bail water with buckets (comic, no injury); ONE shake | whip arrival, then drift; shake ≤ 10 f on "จมกัน" (10.91) |
| 6 | 11.88-15.54 | DIS 13 | HALL hall_table DAY, set_moneybag('full') keyed at "รางวัล" (12.50) | "สภาเลยตั้งรางวัล … สองหมื่นปอนด์": a fat money bag drops onto the baize table (bounce); astro19 and astro19_b lean in, eyes glint | push-in on "สองหมื่นปอนด์" (14.81) |
| 7 | 15.54-18.17 | CUT | HALL hall_window DAY | "นักดาราศาสตร์ในคณะกรรมการบอกว่า ต้องวัดดวงจันทร์": astro19 at the telescope points at the Moon picture, lecturing; astro19_b and astro19_c nod | slide + push; snap on "ดวงจันทร์" (18.17 is the cut, so snap on "คณะกรรมการ" 16.58) |
| 8 | 18.17-22.02 | CUT | HALL hall_low DAY | "กับดวงดาวเท่านั้น คนหนึ่งหัวเราะลั่น": astro19 turns toward camera with a belly laugh (bounce), then the quote "นาฬิกาเนี่ยนะ!" (21.14), mouth moving from 20.80 | low angle, push 9 %/s; snap on "นาฬิกาเนี่ยนะ" |
| 9 | 22.02-25.78 | CUT | HALL hall_low DAY (closer framing) | "ถ้านาฬิกาของช่างไม้แม่นขนาดนั้น ให้พระราชามาจับเวลาเองเลย!": mock-royal bow while miming timing a pocket watch, mouth moving | quick push-in on "จับเวลาเอง" (24.82) |
| 10 | 25.78-28.74 | CUT | HALL hall_wide DAY | "นักปราชญ์หัวเราะกันครืน แล้วเรียกเขาว่า ไอ้ช่างไม้": the whole Board laughs (wigs bounce, fingers point); Harrison stands at the door with his tricorne; snap to him on "ไอ้ช่างไม้" (28.10) | slide across the room, snap |
| 11 | 28.74-31.26 | DIS 15 | WORKSHOP shop_wide DAY, set_clock(1) | "เขาสร้างนาฬิกาเรือเครื่องแรกใช้เวลาห้าปี": young Harrison (young=1) files at the H1 on the bench | push 7 %/s + slide, stump and rug FG |
| 12 | 31.26-32.85 | DIS 11 | WORKSHOP shop_clock NIGHT, set_clock(3) | "เครื่องที่สาม สิบกว่าปี": Harrison (default, greying) works on the H3 by candlelight, candle stub burns down | push + slide |
| 13 | 32.85-33.86 | CUT | WORKSHOP shop_bench NIGHT | "จนผมหงอกทั้งหัว": white-haired Harrison (old=1 look) leans back and rubs his eyes (comic tired) | quick push-in |
| 14 | 33.86-36.52 | DIS 11 | WORKSHOP shop_clock DAY, set_clock([1,4]) | REVEAL IMAGE "แล้วเขาก็ย่อมันเหลือแค่เรือนกลม ๆ เท่าจานรอง": the tiny silver H4 on its red cloth beside the giant H1; Harrison holds out his palm toward it, proud | snap/whip onto the H4 on "เท่าจานรอง" (35.88) |
| 15 | 36.52-39.67 | DIS 15 | SHIP ship_deck NOON, set_sun_overhead 0→1 | "ความลับคือ เที่ยงวันกลางทะเล ดวงอาทิตย์อยู่ตรงหัว": william19 aims the brass quadrant straight up at the sun; the mast shadow shrinks short on the deck | crane up toward the sun then settle; snap on "อยู่ตรงหัว" (38.98) |
| 16 | 39.67-42.65 | CUT | SHIP ship_deck NOON | "แต่นาฬิกายังบอกเวลาที่บ้าน": william19 holds the H4 out on his palm toward camera (captain looks on) | push to the watch, rail/wheel FG |
| 17 | 42.65-46.12 | CUT | SHIP ship_aerial NOON (camera from ship_hero side ok) | "ทุกหนึ่งชั่วโมงที่ต่างกัน เรือก็ห่างบ้านสิบห้าองศา ยิ่งเวลาต่าง ยิ่งไกล": the ship sails on, the V-wake lengthening behind it; the camera pulls back and up as it grows smaller (distance grows) | pull 9 %/s + rise; snap back on "ยิ่งไกล" (45.56) |
| 18 | 46.12-48.92 | DIS 11 | SHIP ship_hero NOON | "ลูกชายเขาพกมันข้ามทะเลไปจาไมกา": the ship under full sail with bow wave and wake | slide + push, swell crest FG |
| 19 | 48.92-52.71 | DIS 13 | SHIP ship_coast DAY_JAMAICA | "ถึงฝั่ง นาฬิกาคลาดไปแค่ห้าวินาที แม่นกว่าที่รางวัลกำหนดซะอีก": william19 on the beach holds the H4 high; sailors cheer (tricornes up) | push-in on "แค่ห้าวินาที" (49.80) |
| 20 | 52.71-55.49 | CUT | HALL hall_low DAY | "แต่นักดาราศาสตร์คนเดิมยักไหล่ ฟลุ๊ค! ต้องลองใหม่!": astro19 shrugs, palms up, smug, mouth moving 54.25-55.45 | hard cut in, push 9 %/s; snap on "ฟลุ๊ค" (54.31) |
| 21 | 55.49-58.53 | DIS 13 | SHIP ship_coast DAY_BARBADOS | "รอบสองที่บาร์เบโดส นาฬิกาแม่นกว่าวิธีดวงจันทร์อีก": william19 holds the H4 calmly; astro19_c (sent by the Board) fumbles a big quadrant at the sky beside him (comic) | slide + push |
| 22 | 58.53-61.86 | DIS 11 | HALL hall_table DAY, set_moneybag('half') at 59.17, set_box closed→sealed at 60.60 | "แต่คณะกรรมการจ่ายให้แค่ครึ่ง แล้วยึดนาฬิกาไปขังในกล่อง": a half-full bag slid across; then the H4 goes into the box and three red seals stamp down; astro19 smug in BG | push-in on the seals on "ขัง" (60.60) |
| 23 | 61.86-64.44 | DIS 15 | HALL hall_door EVENING | "ตอนเขาอายุเกือบแปดสิบ พระราชาได้ยินเรื่องนี้": old Harrison (old=1) shuffles in at the panelled door holding his new watch | crane down + push |
| 24 | 64.44-67.61 | CUT | HALL hall_table EVENING, set_kings_chair(True), set_stubs 0→10 over the shot, set_regulator(True) | "เลยมาจับเวลานาฬิกาของเขาเองกับมือ ทุกวัน สิบสัปดาห์": king19 at the table compares the watch with his gold pocket watch, squinting; candle stubs pile up (time-lapse) | slide + push; snap on "สิบสัปดาห์" (66.77) |
| 25 | 67.61-69.55 | CUT | HALL hall_low EVENING | "ตามที่นักดาราศาสตร์ท้าไว้เป๊ะ": astro19 jaw-dropped, wig askew (shock pose), sweat drop | snap push-in on "เป๊ะ" (68.89) |
| 26 | 69.55-71.90 | CUT | HALL hall_table EVENING, set_moneybag('full') lands at 70.12 | "แล้วสภาก็ต้องควักเงินจ่ายให้ไอ้ช่างไม้": a fat money bag lands in front of old Harrison; the King nods; Harrison grins; the film ends on a hard cut on "ช่างไม้" | push-in; ends moving |

Count and timing: 26 shots, mean 2.77 s. Joins: 11 dissolves, 15 cuts.
Marks (check API.md): Harrison and the King must not overlap in hall_table (QA-art note). Keep characters off the ship_rail bulwark. Use ship_rocks at STORM_DUSK only.

## Teams
s01 is the director's worked example. All other teams run on Sonnet.

| Team | Shots | Location |
|---|---|---|
| s01 | 1 | WORKSHOP shop_bench |
| team1 | 2, 17, 18 | SHIP aerial/hero |
| team2 | 4, 5 | SHIP rocks |
| team3 | 3, 6, 7 | HALL window/table DAY |
| team4 | 8, 9, 20 | HALL low, mocker quotes |
| team5 | 10, 22 | HALL wide, table DAY |
| team6 | 11, 12, 13, 14 | WORKSHOP |
| team7 | 15, 16 | SHIP deck |
| team8 | 19, 21 | SHIP coast |
| team9 | 23, 24, 25, 26 | HALL evening, ending |
