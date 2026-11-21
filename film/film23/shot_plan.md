# Film 23 "ไอ้กองทัพลูกโป่ง": shot plan (v1, on ESTIMATED timing)
Process: film/skill_film13 (+ standing client decisions). Camera rhythm = film 2 (production-lessons §10): every shot has a clear eased
push/pull (6-10 %/s) plus a lateral slide (~40 px/s); quick push-ins on punch lines; dissolves (11 f) between places/times; hard cuts on
beats and quotes; a foreground prop 1-2 D from the lens in most shots. NO random shake (QA §L); camera keys eased only.
Sharp picture, no DOF; wide/medium framings showing the dense lit set; text signs allowed; heads above y 880.

## TIMING IS AN ESTIMATE (fal.ai out of balance; narration not recorded yet)
audio/timing_EST.json (film-18 Bankky rate 10.9 Thai base chars/s). Real sentence lengths can differ by up to ~25 %.
**Every take renders its planned length x 1.25** (the move simply continues, eased, into the extra tail) plus handles. Conform
re-times each shot to the real narration by trimming the tail. Lip-sync shots S07 and S13: the mouth talks with a generic
talk cycle across the whole estimated quote window. After the narration exists, these two shots are re-rendered with real loudness if the
quote drifts more than 0.3 s.

## Locations (one connected world, film/v3/set3d23/ghost.py; signature colours olive/khaki vs bright green + blue dawn; warm lanterns at night)
- FIELDS (dawn): Normandy bocage from high; tank column on the winding lane; farm, village, river.
- LANE (morning/day): farm lane at the farmhouse: inflation site, "23rd HQ SPECIAL TROOPS" sign, crates, hedgerow, poplars. Bikes come up this lane. Ending is here too.
- CAMP (night): moonlit field, rubber tank rows under nets, sound truck with flared horn, radio tent with lanterns.
- RHINE (night, March 1945): wide dark river with glints; SOUTH bank field full of rubber tanks + lanterns + sound truck (the decoy);
  far upstream (north) the real army's boats/pontoon bridge in shadow; far bank (east): German observation post (sandbags, binoculars) - comic, no weapons fired.

## Cast (film/v3/cast23)
ghost soldiers (olive uniform, M1 helmet; variants: painter with brush + paint pot, sound man with headphones + record, radio man,
pump man, clipboard man), "the Major" (mocker, invented: big moustache, cigar, peaked cap, khaki, red face when angry, blows balloons at the end),
two French cyclists (beret, striped shirt / waistcoat, bicycles), German observers (grey field cap, binoculars; comic).

| # | est. time (s) | sentence | location / light | framing, angle, move | action (characters always act) | trans in |
|---|---|---|---|---|---|---|
| S01 | 0.00-4.00 | hook | FIELDS dawn | **BIGZOOM 1**: extreme wide high bird's-eye over the patchwork, descend+push along the lane onto the column, end medium on lead tank (soldier riding on it waving the column on) | column rolls (tanks towed/pushed slowly), soldier waves | - |
| S02 | 4.00-8.40 | pivot (to "ชี้ขึ้นฟ้า") | LANE side field, morning | LOW hero angle along the row of tanks, barrels up; side-tracking slide | soldiers polish a barrel, one salutes | dissolve 11 |
| S03 | 8.40-11.90 | pivot ("เอาเข็มจิ้ม ฟู่ แฟบเลย") | LANE | medium, quick push-in on the pin | a soldier pricks the tank by accident with a pin from the patch kit; tank deflates, barrel droops onto his helmet; sweat drop | cut |
| S04 | 11.90-16.20 | who (artists, designers, sound men) | LANE inflation site | high crane down over the work area | painter paints the white star, sound man carries a record and headphones, designer with clipboard, pump man pumps | dissolve 11 |
| S05 | 16.20-20.55 | who ("แกล้งเป็นกองทัพใหญ่...") | LANE -> FIELDS | pull back and up past the "23rd HQ SPECIAL TROOPS" sign: a dozen men vs. a field filling with rubber tanks | crew inflate several at once; tanks rise | cut |
| S06 | 20.60-23.20 | mocker (narrator part + laugh) | LANE | medium-wide, OTS from behind the crew toward the jeep | jeep pulls up, the Major laughs, belly bounce, cigar | dissolve 11 |
| S07 | 23.20-27.40 | mocker QUOTE | LANE | LOW angle on the Major, slow push, crew small behind | Major points at the deflated tank, talks (mouth = quote only) | cut |
| S08 | 27.40-30.20 | nickname | LANE | wide high, pull back | Major's driver chalks "BALLOON ARMY" on a crate; crew droop | cut |
| S09 | 30.20-35.00 | count (speakers, 20+ km) | CAMP night | crane from tank rows to the sound truck, push toward the horn | sound man flips switches, record spins; tanks lit by moon rim | dissolve 15 |
| S10 | 35.00-39.70 | count (radio, fake insignia) | CAMP night | side-tracking through the radio tent and out to a truck | radio man chatters into handset; painter stencils a different division badge on a bumper by lantern | cut |
| S11 | 39.70-42.80 | bikes | LANE day | side tracking with two cyclists along the hedgerow (foreground hedge) | Frenchmen pedal, chat, baguette in basket | dissolve 13 |
| S12 | 42.80-45.60 | bikes ("ยกรถถังสี่สิบตัน") | LANE | **BIGZOOM 2 / reveal**: from close on the cyclists' faces, PULL BACK and up wide: 4 soldiers lift the tank over their heads | lift (tank airborne ONLY here, flagged airborne), cyclists brake | cut |
| S13 | 45.60-50.10 | cover + QUOTE "พวกเราอเมริกัน แข็งแรงมาก" | LANE | medium two-shot in depth, quick push on the soldier's dry smile | soldier with tank overhead grins and speaks; cyclists stare, one falls off the bike gently (no injury) | cut |
| S14 | 50.20-54.20 | turn (Rhine, March 1945) | RHINE night | extreme wide high over the river, slow descend; caption-safe sign "RHINE" post on the bank | soldiers unload crates of folded rubber from trucks | dissolve 17 |
| S15 | 54.30-57.60 | plan (600 decoys south) | RHINE south field | crane up over rows inflating in lantern light | dozens of tanks rising; pump crews | dissolve 11 |
| S16 | 57.60-60.90 | plan ("สองกองพล") | RHINE south field | push along the sound truck and radio tent; sign "30th INF DIV" / "79th INF DIV" crates | sound truck booming, radio chatter | cut |
| S17 | 60.90-63.50 | reveal (enemy stares) | RHINE far bank | OTS from behind German observers with binoculars across the river to the glowing balloon field | observers nudge each other, point south, one drops his sausage | dissolve 11 |
| S18 | 63.50-66.00 | reveal (real army crosses) | RHINE north, pre-dawn blue | wide, slow pan along boats/pontoon crossing quietly | soldiers paddle, tiptoe, a dog in a boat | dissolve 13 |
| S19 | 66.00-70.30 | ending | LANE day | wide -> medium push, ends on the Major | Major sits on a crate, red-faced, blowing up balloon after balloon; huge pile; crew grin; last balloon pops/loops away on the last word | dissolve 17 |

Counts: 19 shots, mean 3.7 s; BIGZOOM S01, S12; angle types: high/bird's-eye (S01, S04, S14), low hero (S02, S07), OTS (S06, S17),
side tracking (S02, S10, S11), crane (S05, S09, S15), through foreground frame (S11 hedge, S17 sandbags).
Comic and bloodless: no weapons fired, nobody hurt; the German observers only watch.
