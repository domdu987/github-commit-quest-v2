# DEAD ZONE 09 / เขตปิดตาย 09, EP.1: narration after the hook title (edited)

One voice (Ohm) tells the story in the third person and also speaks the short lines, as in the hook (`audio/narr_ohm/script.json`, s01-s16). Ids continue at s17. Lower-case `s` = sentence, upper-case `S` = shot. This is the script editor's version: the screenwriter's draft is kept as `narration_ep1_draft.md` / `.json`, ids were renumbered after the cuts, and every row carries its draft id. Machine copy: `narration_ep1.json`. Generator: `_gen_v2/edit.py` (the edit tables, on top of `_gen/narr.py`) and `_gen_v2/write2.py`.

## Numbers

| | edited | draft |
|---|---|---|
| Hook | 0:00.00 - 0:53.32 (bite at 0:43.80, title 0:50.72) | same |
| New narration | 0:53.62 - 5:15.11, 85 sentences, 211 captions (62 with a coloured key word) | 89 sentences, 227 captions (61) |
| Episode running time | **5:18.96** (7655 frames at 24 fps; new picture 6375 frames) | 5:34.62 (8,031; 6,751) |
| Characters to record | **2527** spoken Thai characters (numbers spelled out, no spaces or punctuation); **2685** counting spaces and punctuation, which is how a text-to-speech service bills | 2,685 / 2,856 |
| Voice time | 234.2 s of sentences in 265.6 s of new picture | 236.9 s in 281.3 s |
| Speaking rate (measured from the hook) | 11.04 characters per second with pauses; 12.58 inside a sentence; a sentence-final caption runs 0.38 s longer | same model |
| Estimate error | The hook's sentences ran from 6.8 to 18.1 characters per second, so single lines can be 30 % off. Times are intended starts; the cut follows the real recording, as the hook did | |

## What the edit changed and why

Checks asked for, and their result:

- **The hook's promise is paid on screen.** The hook's last words are 'อีก 60 วินาที เพื่อนของเขา จะไม่ใช่คน อีกต่อไป' (bite at 0:43.80). The first words after the title are 'เหลืออีก 50 วินาที' at 0:53.62, 9.8 s after the bite. '30 วินาที' falls at 1:13.80 (30.0 s after) and '10 วินาที' at 1:33.80 (50.0 s after). The eyes open on 'ลืมตา' at about 1:41.5, 57.7 s after the bite: inside the rule's 60 seconds, in real time, with no cut that skips time. The count is visible four times as Kong's watch (S26, S36, S44, S47). The watch was redesigned: no digits, one red second hand that has to come back round to a drop of blood on the 12 mark. A viewer reads it without reading.
- **First 10 seconds after the title (0:53.3 - 1:03.3).** Three things land: the countdown restated (s17), the fight (s18), and a question (s19: it drops a victim to go to a noise; why?). That question is answered by the siren at s54 and used by the heroes at s66. No line in this stretch describes scenery.
- **Dialogue against the screenplay.** All 20 screenplay lines used are word for word: s21, s25, s26, s32, s47, s55, s58, s59, s60, s72, s73, s74, s75, s78, s79, s80, s83, s94, s95, s96. One line is invented, the guard's (s87), because the screenplay only says he refuses. Kong says nothing in the phone call (s78-s80), which is what the screenplay has. In the hook's manner no line is attributed in words: each plays on a close shot of its speaker, or on Kong listening to the phone.
- **The cliffhanger.** The last words are 'ก้องยกชะแลงขึ้น / แต่เขาจะหวด ใคร', then black on 'ใคร' (s100-s101). Nothing follows but the end card.

Lines fixed because they contradicted the screenplay, the world rules or the hook:

- **Battery.** The draft made the third bar blink (draft s47, and the gauge at the chain). The bible says three bars in EP.1 and the hook says 'แบตเต็ม 3 ขีด'. The bar is steady again; the hook's set-up is paid at the gate instead (s88: 'แบตยังเต็ม 3 ขีด ตัดโซ่ขาดแน่', and he still cannot use it).
- **The 60 seconds at the end.** Draft s101 ('ก้องรู้ดี ว่า 60 วินาที มันสั้นแค่ไหน') put a 60-second clock on Tos. Tos has been with the group for minutes; by rule 1 a bite would have turned him long before. s97 now says only what Kong has seen ('น้องของเขา ใช้เวลาแค่ 60 วินาที'). The audience, who watched the glass cut him, knows more than Kong: that is the cliffhanger's irony, and the rule is not bent.
- **The crowbar.** The screenplay has Kong push the driver off with a crowbar in SCENE 02, then take a crowbar from the truck in SCENE 04. He cannot do both. He shoves with the cutter that is already in his hands (s18), and the crowbar stays a SCENE 04 choice that pays off in the last shot.
- **The roof chase.** In the draft the junior chases James over the roofs for 45 s without catching him, against rule 2. Now he loses James behind the bus (rule 7, S57) and is brought back by James's own shout (rule 3, S75). No line changed; the shot list carries it.

Cut or tightened for pace (every row below says which):

| draft id | draft text | now | reason |
|---|---|---|---|
| s19 | สัญญาณกันขโมย ดังลั่น มันหันไปหาเสียง ทันที | s19: สัญญาณกันขโมย ดังลั่น มันทิ้งเหยื่อ หันไปหาเสียง | 'ทันที' was filler; 'มันทิ้งเหยื่อ' states the strange thing the viewer must notice (it leaves a victim for a noise), which is the question the siren answers |
| s27 | คืนนี้ ก้องสัญญา ไปแล้ว 2 ครั้ง | s27: สัญญาครั้งที่ 2 ของคืนนี้ | shorter; the count is kept as a motif but no longer does arithmetic in the middle of the countdown |
| s29 | ก้องแตะชีพจรที่คอ ไม่มีอะไรเต้นเลย | s29: ก้องจับชีพจร ไม่เต้นแล้ว | 'ไม่มีอะไรเต้นเลย' is not how a rescuer says it; the neck is where the wound is, so the place is left to the picture |
| s37 | ก้องมองไปรอบตัว ทั้งทางด่วน มีแต่คนวิ่งหนี กับพวกที่ไล่กัด | s38: ทั้งทางด่วน มีแต่คนวิ่งหนี กับพวกที่ไล่กัด | 'ก้องมองไปรอบตัว' described the picture; the look is now a silent shot before the line |
| s39 | และไม่ได้เกิด แค่ที่นี่ | *cut* | the hook already ends on this crane 75 s earlier; the shut hospital and the evacuation bus say 'everywhere' later |
| s40 | ไม่ไกลจากรถกู้ภัย รถเก๋งคันหนึ่ง พลิกตะแคง | s40: ไม่ไกลกัน รถเก๋งคันหนึ่ง พลิกตะแคง | shorter |
| s41 | หมอแพรว หมอห้องฉุกเฉิน กำลังดึงชายใส่สูท ออกจากซากรถ | s41: หมอแพรว หมอห้องฉุกเฉิน กำลังดึงคุณทศ ออกจากซากรถ | names Tos here, so the filler sentence 'เขาชื่อคุณทศ' can go; the suit is in the picture |
| s42 | เขาชื่อคุณทศ ประตูที่ยุบ อัดเขาติดเบาะ | s42: แต่ประตูที่ยุบ อัดเขาติดเบาะ | but-therefore instead of an introduction |
| s46 | ก้องสอดเครื่องถ่าง เหล็กค่อยๆ อ้าออก | s46: ก้องเอาเครื่องตัดง้างประตู คุณทศหลุดออกมา | the mechanics of the rescue are not the drama; the choice before it is |
| s47 | คุณทศหลุดออกมา แต่แบตขีดที่ 3 เริ่มกะพริบ | *cut* | merged into the sentence before it; the blinking bar contradicted the bible |
| s49 | เจมส์ ไรเดอร์ส่งอาหาร กระโดดลงจากหลังคารถ และที่ไล่ตามมา คือน้องของก้อง | s48: เจมส์ ไรเดอร์ส่งอาหาร กระโดดลงจากหลังคารถ แต่ที่ตามหลังมา คือน้องของก้อง | 'แต่' turns the line; James's name gets a colour as the other two principals' names do |
| s57 | ก้องปิดไซเรน แต่สายไปแล้ว พวกมันรู้แล้ว ว่าเขาอยู่ตรงไหน | s56: ก้องปิดไซเรน แต่สายไปแล้ว ทั้งฝูงรู้แล้ว ว่าเขาอยู่ตรงไหน | 'ทั้งฝูง' is the screenplay's word and is stronger than 'พวกมัน' |
| s68 | คุณทศปีนออก เป็นคนแรก | s67: คุณทศเบียดออกไป เป็นคนแรก | the door opens a hand-span against a taxi: he squeezes, he does not climb |
| s76 | ไม่มีใครเห็น ว่าคุณทศกอดอก แน่นกว่าเดิม | *cut* | said what the insert of his arm shows |
| s83 | ก้องยังไม่ทันตอบ สัญญาณก็ขาด | s81: ก้องยังไม่ทันรับปาก สัญญาณก็ขาด | carries the meaning of the cut sentence s84 in two words ('รับปาก') |
| s84 | สัญญาครั้งที่ 3 เขายังไม่ทัน ได้พูดออกไป | *cut* | bookkeeping; the sentence before it now says it with 'รับปาก' |
| s85 | ก้องหันหลัง จะไปเดี๋ยวนั้น | s82: ก้องหันหลัง จะไปหาลูกเดี๋ยวนั้น | says where he is going |
| s87 | ก้องกำโทรศัพท์แน่น แล้วเดินตามเจมส์ ไปโรงพยาบาล | s84: ก้องกำโทรศัพท์แน่น แล้วเดินตามเจมส์ไป | the next sentence starts with 'โรงพยาบาล'; saying it twice in a row was a stumble |
| s90 | เปิดไม่ได้! เราไม่รู้ว่า ใครโดนกัดมาบ้าง! | s87: เปิดไม่ได้! ใครโดนกัดมาบ้าง ก็ไม่รู้! | spoken word order; the line is invented (the screenplay gives the guard none) and stays short |
| s91 | ก้องยกเครื่องตัดขึ้น โซ่เส้นนี้ ตัดขาดได้แน่ | s88: ก้องยกเครื่องตัดขึ้น แบตยังเต็ม 3 ขีด ตัดโซ่ขาดแน่ | keeps the bible's three bars and pays the hook's set-up here |
| s93 | และคนข้างใน จะไม่เหลือประตู | s90: และคนข้างใน จะไม่เหลือประตูกั้น | no longer optional: without it Kong spares the chain only to save himself, and his value (other lives count) is not on screen |
| s96 | ทุกคน วิ่งเข้าไปหลบ | *cut* | the picture shows it |
| s97 | แล้วก้องก็เห็น เลือดหยดลงพื้น ทีละหยด จากแขนเสื้อคุณทศ | s93: แล้วก้องก็เห็น เลือดหยดลงพื้น จากแขนเสื้อคุณทศ | 'ทีละหยด' is in the picture and the sound |
| s101 | ก้องรู้ดี ว่า 60 วินาที มันสั้นแค่ไหน | s97: ก้องจำได้ดี น้องของเขา ใช้เวลาแค่ 60 วินาที | the draft ('ก้องรู้ดี ว่า 60 วินาที มันสั้นแค่ไหน') implied a 60-second clock on Tos, who has been with them for minutes; a bite would have turned him long ago. This wording is only what Kong knows and keeps the number |
| (new) | | s30: ก้องคิดว่า เขาเสียน้องไปแล้ว | new: the shortened s29 left 3 s of dead air before '10 วินาที'; this line uses it to put Kong one step behind the audience, which is the hook's own device ('ก้องยังไม่รู้เลยว่า') |

The episode is now 5:18.96, 16 s shorter than the draft and 1:21 under the screenplay's 06:40. Nothing was added to fill the time: see PRODUCTION_PLAN.md, decision 2.

## Retention structure

| Loop | Opened | Kept alive | Paid off |
|---|---|---|---|
| 60 seconds | hook s16 | s17 / s23 / s31 countdown, four watch inserts; s30 (Kong thinks it is over) | s33-s34 (eyes open); s97 at the end |
| Sound and light call them | s19 car alarm | s36 (out of sight = lost) | s53-s54 siren; s57 rule said aloud; s65-s66 flare; s77 phone light; s89 the cutter not used; s98 the shouting |
| The battery | hook s04 | | s88 at the chain: full, and useless |
| Kong's promises | hook s06-s10 | s26-s27 promise two | s50 the junior at the glass; s80-s81 the third is asked for and never given |
| The daughter's call | hook s05-s10 | s76 no call yet | s77-s81 the call; the pier is the series goal |
| The rider | s37 | | s47-s48 |
| Tos's wound | s68-s69 | s74 (picture: his arm), s87 | s93-s96; left open by s101 |
| What was left behind | s62-s64 | s72-s74 | later episodes |

Every scene clip ends on an open question, so each delivered clip holds on its own: 02 'นี่ไม่ใช่อุบัติเหตุ อีกต่อไปแล้ว'; 03 James's way out, unseen; 04 'ยังไม่มีสาย จากลูก'; 05 he follows the others, away from her; 06 'ใคร'.

## Script

Caption split is marked with `/`. **Bold** = the coloured word (amber = fact, red = threat). Start and length are on the episode clock.


### SCENE 02 (rest) คนที่กลับมา (0:53.62 - 2:05.14)

| id | draft | start | s | who | captions | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s17 | s17 | 0:53.62 | 1.97 | narration | เหลืออีก / **50 วินาที** (amber) | 20 | hard cut from title to picture; rain + beacons back at full level; low heartbeat pulse starts (one beat per second, under the voice) and runs to s32 | S25 S26 | countdown opens (pay-off of the hook's last line) |
| s18 | s18 | 0:55.69 | 4.12 | narration | ก้องเอาเครื่องตัด / กระแทกมันกระเด็น / ไปชนรถคันข้างๆ | 47 | metal thud on 'กระแทก'; body hits a car door on 'ชนรถ' | S27 S28 | Kong rams the driver off with the tool body |
| s19 | s19 | 0:59.91 | 3.96 | narration | สัญญาณกันขโมย / ดังลั่น / มันทิ้งเหยื่อ / หันไปหา**เสียง** (amber) | 45 | car alarm (two-tone, panned to the alarm car's side) from the first caption, hazards blink; infected snarl turning away | S29 S30 | SETUP: they go for sound and flashing light *(edited)* |
| s20 | s20 | 1:04.01 | 2.69 | narration | ก้องพยุงน้อง / ไปหลบหลังรถกู้ภัย | 29 | two pairs of boots, one dragging; alarm now further off (distance + low-pass) | S31 | cover |
| s21 | s21 | 1:06.95 | 2.13 | ก้อง (line) | มองหน้าพี่ไว้! / ได้ยินไหม! | 22 | dry, close; rain on truck metal | S32 | dialogue |
| s22 | s22 | 1:09.23 | 2.77 | narration | น้องพยักหน้า / แต่เลือด / **ไหลไม่หยุด** (red) | 30 | wet cloth press; junior's breath | S33 S34 S35 | wound |
| s23 | s23 | 1:13.80 | 1.33 | narration | **30 วินาที** (amber) | 12 | watch tick, close and dry (three ticks before the line) | S36 | countdown |
| s24 | s24 | 1:15.43 | 2.29 | narration | ลมหายใจน้อง / สั้นลง / **ถี่ขึ้น** (red) | 24 | fast shallow breathing, shivering | S37 | symptoms |
| s25 | s25 | 1:18.17 | 1.28 | น้องในทีม (line) | พี่... / ผม**หนาว**... (red) | 9 | voice low; heartbeat a little faster | S38 | dialogue |
| s26 | s26 | 1:19.75 | 2.69 | ก้อง (line) | อดทนไว้ / เดี๋ยวพี่พาไป / **โรงพยาบาล** (amber) | 29 | - | S39 | promise no. 2 (SETUP for s49, s76(cut), s84) |
| s27 | s27 | 1:22.93 | 2.37 | narration | **สัญญาครั้งที่ 2** (amber) / ของคืนนี้ | 25 | - | S40 | open loop: the promise count *(edited)* |
| s28 | s28 | 1:25.90 | 2.23 | narration | มือที่สั่น / ค่อยๆ / **หยุดนิ่ง** (red) | 23 | breathing stops; heartbeat stops with it; only rain | S41 | he goes still |
| s29 | s29 | 1:28.43 | 2.21 | narration | ก้องจับชีพจร / **ไม่เต้นแล้ว** (red) | 23 | rain only; glove on wet skin | S42 | he checks for a response *(edited)* |
| s30 | n1 | 1:30.94 | 2.53 | narration | ก้องคิดว่า / เขา**เสียน้องไปแล้ว** (red) | 27 | rain only; Kong's breath going out of him | S43 S44 | REVERSAL SET-UP: Kong believes the worst is over; the audience has been told what comes next *(new)* |
| s31 | s30 | 1:33.80 | 1.09 | narration | **10 วินาที** (amber) | 9 | watch tick alone | S44 | countdown |
| s32 | s31 | 1:35.25 | 1.75 | ก้อง (line) | เฮ้ย! / ได้ยินพี่ไหม! | 16 | - | S45 S46 | dialogue |
| s33 | s32 | 1:40.90 | 1.57 | narration | แล้วน้อง / ก็**ลืมตา** (red) | 15 | three watch ticks in silence before the line; sub-bass swell into the next line | S48 | PAY-OFF of the 60-second rule: eyes open 57.6 s after the bite |
| s34 | s33 | 1:42.52 | 2.45 | narration | แต่ตาคู่นั้น / **ไม่ใช่ตาคน**แล้ว (red) | 26 | red flash 1 frame on the cut; infected inhale | S49 | pay-off of 'จะไม่ใช่คนอีกต่อไป' |
| s35 | s34 | 1:45.07 | 4.20 | narration | มันพุ่งใส่ก้อง / ก้องเอาเครื่องตัดขวาง / ผลักมันสุดแรง | 48 | snarl; teeth on metal; shove grunt; body against the truck panel | S50 S51 S52 | the attack |
| s36 | s35 | 1:49.42 | 2.84 | narration | ก้องถอยหลบมุมรถ / มัน**มองไม่เห็น**เขา (amber) | 31 | the snarl drops to short searching breaths; Kong's held breath | S53 S54 | world rule 7 planted |
| s37 | s36 | 1:52.46 | 4.83 | narration | บนหลังคารถ / ไรเดอร์เสื้อเขียว / วิ่งหนีสุดชีวิต / มัน**กระโจนตาม**ไป (red) | 56 | boots on car roofs (hollow bangs), windscreen cracking, a far scream | S55 S56 S57 | SETUP: the rider (James) and who chases him |
| s38 | s37 | 1:58.54 | 3.56 | narration | ทั้งทางด่วน / มีแต่คนวิ่งหนี / กับพวกที่**ไล่กัด** (red) | 40 | crowd screams from several directions, glass breaking left then right, horns | S59 S60 | scale *(edited)* |
| s39 | s38 | 2:02.30 | 2.84 | narration | นี่**ไม่ใช่อุบัติเหตุ** (red) / อีกต่อไปแล้ว | 31 | - | S61 | realisation |

### SCENE 03 รถกู้ภัยคันสุดท้าย (2:05.59 - 3:14.17)

| id | draft | start | s | who | captions | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s40 | s40 | 2:05.59 | 2.92 | narration | ไม่ไกลกัน / รถเก๋งคันหนึ่ง / **พลิกตะแคง** (amber) | 32 | hazard relay ticking, dripping, a woman's strained effort | S62 S63 | new place *(edited)* |
| s41 | s41 | 2:08.62 | 3.96 | narration | **หมอแพรว** (amber) / หมอห้องฉุกเฉิน / กำลังดึง**คุณทศ** (amber) / ออกจากซากรถ | 45 | - | S64 S65 | Praew introduced *(edited)* |
| s42 | s42 | 2:12.68 | 2.53 | narration | แต่ประตูที่ยุบ / อัดเขา**ติดเบาะ** (red) | 27 | metal creak; Tos's grunts | S66 | Tos introduced *(edited)* |
| s43 | s43 | 2:15.40 | 2.61 | narration | ไกลออกไป / **ฝูงของมัน** (red) / กำลังวิ่งมา | 28 | many running feet on wet road, far, growing | S67 | deadline |
| s44 | s44 | 2:18.21 | 2.29 | narration | ก้องชะงัก / หนีตอนนี้ / ยังทัน | 24 | everything dips for half a second | S68 | the choice |
| s45 | s45 | 2:20.69 | 2.29 | narration | แต่เขา / วิ่ง**กลับเข้าไปช่วย** (amber) | 24 | boots splashing | S69 | Kong's value shown by action |
| s46 | s46 | 2:23.08 | 3.56 | narration | ก้องเอาเครื่องตัดง้างประตู / คุณทศหลุดออกมา | 40 | cordless pump whine, metal groaning open; Tos's breath as he comes free | S70 S71 | the tool is used; Tos is out (two draft sentences in one) *(edited)* |
| s47 | s48 | 2:26.84 | 1.44 | เจมส์ (line) | พี่! / รอผมด้วย! | 11 | shout from above/behind, roof bangs | S72 | dialogue |
| s48 | s49 | 2:28.38 | 5.81 | narration | **เจมส์** (amber) / ไรเดอร์ส่งอาหาร / กระโดดลงจากหลังคารถ / แต่ที่ตามหลังมา / คือ**น้องของก้อง** (red) | 68 | landing splash; snarl close behind | S73 S74 S75 | PAY-OFF of s37 *(edited)* |
| s49 | s50 | 2:34.34 | 3.80 | narration | ทุกคนขึ้นรถกู้ภัย / ประตูปิดทัน / แค่เสี้ยววินาที | 43 | door slam, then a body hitting it | S76 S77 | into the truck |
| s50 | s51 | 2:38.38 | 4.28 | narration | หน้าที่**แนบกระจก** (red) / คือคนที่เขาสัญญา / ว่าจะพาไปโรงพยาบาล | 49 | muffled snarl through glass, nails on glass; cabin is quiet | S78 S79 | PAY-OFF of promise no. 2 |
| s51 | s52 | 2:42.91 | 2.45 | narration | ก้องออกรถ / แทรกไปตามช่องว่าง | 26 | diesel start, tyres on wet road, mirrors scraping | S80 | drive |
| s52 | s53 | 2:45.46 | 2.77 | narration | แต่ข้างหน้า / รถบรรทุก**ขวาง** (red) / เต็มถนน | 30 | brakes; wipers | S81 S82 | obstacle |
| s53 | s54 | 2:48.37 | 3.40 | narration | มือเขาไปเอง / ตามความเคยชิน / เปิด**ไซเรน**ขอทาง (red) | 38 | switch click, then the siren at full level for 1.2 s (the only moment an effect is allowed to rival the voice: it sits in the gap after the line) | S83 S84 | the mistake |
| s54 | s55 | 2:52.97 | 3.56 | narration | ทุกตัวบนทางด่วน / หยุดวิ่ง / แล้ว**หันมา** (red) / พร้อมกัน | 40 | siren ducks under the voice; all other screams stop | S86 S87 | PAY-OFF of the car alarm (s19) |
| s55 | s56 | 2:56.68 | 1.44 | หมอแพรว (line) | ปิดเสียง! / เร็ว! | 12 | - | S88 | dialogue |
| s56 | s57 | 2:58.22 | 4.67 | narration | ก้องปิดไซเรน / แต่**สายไปแล้ว** (red) / ทั้งฝูงรู้แล้ว / ว่าเขาอยู่ตรงไหน | 54 | siren winds down; silence 0.4 s; then many feet running toward us | S89 S90 S91 | consequence *(edited)* |
| s57 | s58 | 3:03.14 | 2.69 | narration | **เสียง กับแสง** (amber) / คือสิ่งที่เรียกมัน | 29 | first bodies hit the truck | S92 S93 | the rule, learned (used in s66, s89) |
| s58 | s59 | 3:06.03 | 2.53 | คุณทศ (line) | ขับไปสิ! / จะจอดให้มันกิน / หรือไง! | 27 | pounding all around | S94 | Tos's value shown |
| s59 | s60 | 3:08.65 | 1.97 | ก้อง (line) | รถข้างหน้า / ขยับไม่ได้! | 20 | - | S95 | dialogue |
| s60 | s61 | 3:10.77 | 3.40 | เจมส์ (line) | พี่! ผมเคยผ่านแถวนี้ / มี**ทางลง** (amber) / ข้างรถคันนั้น! | 38 | - | S96 S97 | way out |

### SCENE 04 สิ่งที่ต้องทิ้ง (3:14.42 - 4:03.38)

| id | draft | start | s | who | captions | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s61 | s62 | 3:14.42 | 2.92 | narration | ฝูงกระแทกรถ / ไม่หยุด / กระจกเริ่ม**ร้าว** (red) | 32 | body hits in an irregular rhythm, glass crack ticks | S98 S99 | pressure |
| s62 | s63 | 3:17.50 | 4.36 | narration | ก้องเปิดตู้อุปกรณ์ / ของเต็มตู้ / แต่แบกไปได้ / แค่ **4 อย่าง** (amber) | 50 | locker latch, roll-up shutter | S100 S101 | the choice of things |
| s63 | s64 | 3:22.00 | 3.52 | narration | เครื่องตัด / ชะแลง / วิทยุ / กระเป๋าพยาบาลใบเล็ก | 39 | one grab sound per item, on the cut | S102 | the four things |
| s64 | s65 | 3:25.72 | 2.21 | narration | ที่เหลือ / ต้อง**ทิ้ง**ทั้งหมด (red) | 23 | shutter left open; a monitor beeping once, abandoned | S103 | cost |
| s65 | s66 | 3:28.18 | 3.24 | narration | ก้องจุดพลุไฟฉุกเฉิน / ขว้างไปอีกฝั่งถนน | 36 | flare strike and hiss, window crank, the flare skittering on the road | S104 S105 | plan built on the rule |
| s66 | s67 | 3:31.57 | 2.29 | narration | เกือบทั้งฝูง / วิ่ง**ตามแสง**ไป (amber) | 24 | the pounding moves away to the left | S106 | PAY-OFF of s57 |
| s67 | s68 | 3:34.06 | 2.29 | narration | คุณทศเบียดออกไป / เป็น**คนแรก** (amber) | 24 | glass crunch, cloth | S107 | character *(edited)* |
| s68 | s69 | 3:36.45 | 3.72 | narration | แขนเสื้อเกี่ยวกระจก / ขาดเป็นทาง / **เลือด**ซึมออกมา (red) | 42 | cloth rip, sharp breath | S108 | SETUP: the wound (glass, shown clearly) |
| s69 | s70 | 3:40.32 | 3.48 | narration | เขารีบดึงแขนเสื้อ / ลงปิดแผล / **ไม่บอกใคร**สักคำ (red) | 39 | - | S109 S110 | SETUP: the secret |
| s70 | s71 | 3:44.05 | 2.92 | narration | ทุกคนวิ่งลง / บันไดเหล็ก / ข้างทางด่วน | 32 | steel treads ringing under four pairs of feet, rain on steel | S111 | escape |
| s71 | s72 | 3:47.32 | 1.89 | narration | ข้างล่าง**มืด** (amber) / และเงียบ | 19 | the expressway noise is now overhead and muffled; drips | S112 | world rule 5 |
| s72 | s73 | 3:49.56 | 2.05 | หมอแพรว (line) | ของเหลือ / แค่นี้เองเหรอ | 21 | whispered | S113 | dialogue |
| s73 | s74 | 3:51.76 | 1.81 | ก้อง (line) | เอาออกมาได้ / เท่านี้ | 18 | whispered | S114 | dialogue |
| s74 | s75 | 3:53.77 | 2.84 | หมอแพรว (line) | ถ้ามีคนเจ็บหนัก / เราอาจ**ช่วยไม่ได้** (red) | 31 | whispered | S115 S116 | irony: picture is Tos's arm |
| s75 | s77 | 3:56.92 | 3.24 | เจมส์ (line) | **โรงพยาบาล**อยู่ข้างหน้า (amber) / ผมเคยไปส่งอาหาร | 36 | - | S117 S118 | goal |
| s76 | s78 | 4:00.46 | 2.92 | narration | ก้องมองโทรศัพท์ / **ยังไม่มีสาย** (red) / จากลูก | 32 | - | S119 S120 | open loop: the daughter |

### SCENE 05 ลูกสาว (4:03.88 - 4:28.71)

| id | draft | start | s | who | captions | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s77 | s79 | 4:03.88 | 3.48 | narration | แล้วโทรศัพท์ก็สั่น / จอ**สว่างวาบ** (red) / กลางความมืด | 39 | phone buzz on a hard surface x2; everybody's breath stops | S121 S122 | PAY-OFF of the missed calls + light = danger |
| s78 | s80 | 4:07.66 | 1.59 | น้ำเหนือ (line, on the phone) | พ่อ! / พ่ออยู่ไหน! | 13 | phone-band filter, crowd and engine behind her | S123 S124 | dialogue |
| s79 | s81 | 4:09.46 | 3.16 | น้ำเหนือ (line, on the phone) | เขาพาหนู / ขึ้นรถอพยพ / บอกว่าจะไป**ท่าเรือ** (amber) | 35 | - | S125 | the series goal |
| s80 | s82 | 4:12.97 | 2.37 | น้ำเหนือ (line, on the phone) | ครั้งนี้ / พ่อ**อย่าผิดสัญญา**นะ (red) | 25 | signal breaking up on the last word | S126 | the promise asked for |
| s81 | s83 | 4:15.64 | 2.77 | narration | ก้องยังไม่ทันรับปาก / **สัญญาณก็ขาด** (red) | 30 | dead-line tone, one beat, then nothing | S127 S128 | cut off before he can promise: PAY-OFF of the promise motif (s27) *(edited)* |
| s82 | s85 | 4:18.70 | 2.77 | narration | ก้องหันหลัง / จะไปหาลูกเดี๋ยวนั้น | 30 | boots turning on gravel | S129 | impulse *(edited)* |
| s83 | s86 | 4:21.67 | 3.40 | หมอแพรว (line) | ถ้าคุณไปคนเดียว / ตอนนี้ / คุณอาจ**ไปไม่ถึงลูก** (red) | 38 | - | S130 S131 | the argument |
| s84 | s87 | 4:25.47 | 3.24 | narration | ก้องกำโทรศัพท์แน่น / แล้วเดินตามเจมส์ไป | 36 | - | S132 S133 | decision *(edited)* |

### SCENE 06 ประตูที่ไม่เปิด (4:29.21 - 5:15.11)

| id | draft | start | s | who | captions | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s85 | s88 | 4:29.21 | 2.61 | narration | โรงพยาบาลริมแม่น้ำ / **ไฟยังสว่าง** (amber) | 28 | river wash, a generator hum, no rain noise on roofs for the first time | S134 | hope |
| s86 | s89 | 4:32.02 | 1.97 | narration | แต่ประตูเหล็ก / **ปิดสนิท** (red) | 20 | hands on steel bars, a chain rattling | S135 | but |
| s87 | s90 | 4:34.24 | 3.00 | รปภ. โรงพยาบาล (line) | เปิดไม่ได้! / ใคร**โดนกัด**มาบ้าง (red) / ก็ไม่รู้! | 33 | voice from inside, behind steel | S136 S137 | refusal; SETUP for the wound reveal *(edited)* |
| s88 | s91 | 4:37.49 | 4.20 | narration | ก้องยกเครื่องตัดขึ้น / แบตยังเต็ม **3 ขีด** (amber) / ตัดโซ่ขาดแน่ | 48 | the cutter's motor clicks ready (no warning beep: the gauge is steady) | S138 S139 | PAY-OFF of the hook's 'แบตเต็ม 3 ขีด': he has the power and still cannot use it *(edited)* |
| s89 | s92 | 4:41.78 | 3.40 | narration | แต่เสียงตัดเหล็ก / จะเรียกพวกมัน / มา**ทั้งฝูง** (red) | 38 | - | S140 S141 | the rule applied (pay-off of s57) |
| s90 | s93 | 4:45.29 | 2.77 | narration | และคนข้างใน / จะ**ไม่เหลือประตู**กั้น (red) | 30 | - | S142 | Kong's value *(edited)* |
| s91 | s94 | 4:48.20 | 1.18 | narration | เขาลดมือลง | 10 | - | S143 | decision |
| s92 | s95 | 4:49.68 | 3.00 | narration | ข้างๆ กัน / มีตึกสร้างไม่เสร็จ / **มืดสนิท** (amber) | 33 | tarpaulin flapping, dripping concrete | S144 S145 | refuge by rule 5 *(retimed)* |
| s93 | s97 | 4:53.63 | 3.88 | narration | แล้วก้องก็เห็น / **เลือด**หยดลงพื้น (red) / จากแขนเสื้อคุณทศ | 44 | single drops on concrete, very close, in a quiet room | S146 S147 S148 | PAY-OFF of the hidden wound *(edited)* |
| s94 | s98 | 4:57.86 | 0.94 | หมอแพรว (line) | แผลอะไร? | 7 | - | S149 | dialogue |
| s95 | s99 | 4:58.94 | 1.09 | คุณทศ (line) | ไม่มีอะไร! | 9 | loud; it echoes in the bare concrete | S150 | dialogue |
| s96 | s100 | 5:00.14 | 1.41 | หมอแพรว (line) | ขอดูเดี๋ยวนี้! | 13 | louder; echo | S151 | dialogue |
| s97 | s101 | 5:01.85 | 3.72 | narration | ก้องจำได้ดี / น้องของเขา / ใช้เวลาแค่ **60 วินาที** (amber) | 42 | heartbeat pulse of scene 02 returns | S152 S153 S154 | PAY-OFF of the 60-second rule, stated as what Kong has seen, not as a clock running on Tos *(edited)* |
| s98 | s102 | 5:05.82 | 2.37 | narration | แต่เสียงเถียงกัน / **ดังเกินไป** (red) | 25 | the echo of the shouting dies; one far snarl answers | S155 | cause |
| s99 | s103 | 5:08.34 | 2.92 | narration | ในความมืด / มี**เสียงฝีเท้า** (red) / วิ่งเข้ามา | 32 | running feet on gravel from behind, closing | S156 S157 | effect |
| s100 | s104 | 5:11.61 | 1.57 | narration | ก้องยก**ชะแลง**ขึ้น (amber) | 15 | steel bar scrape, heartbeat louder | S158 | the last action |
| s101 | s105 | 5:13.43 | 1.67 | narration | แต่เขาจะหวด / **ใคร** (red) | 14 | all sound cuts to nothing on 'ใคร'; black; 1.0 s of silence; then one watch tick | S159 S160 | CLIFFHANGER |

## Text for the recording (one line per sentence, numbers spelled out)

Record all five scenes in one session, after the user has approved this text. Each scene is its own file set (`audio/ep1/scNN/`).

```
# scene 02
s17	เหลืออีก ห้าสิบวินาที
s18	ก้องเอาเครื่องตัด กระแทกมันกระเด็น ไปชนรถคันข้างๆ
s19	สัญญาณกันขโมย ดังลั่น มันทิ้งเหยื่อ หันไปหาเสียง
s20	ก้องพยุงน้อง ไปหลบหลังรถกู้ภัย
s21	มองหน้าพี่ไว้! ได้ยินไหม!
s22	น้องพยักหน้า แต่เลือด ไหลไม่หยุด
s23	สามสิบวินาที
s24	ลมหายใจน้อง สั้นลง ถี่ขึ้น
s25	พี่... ผมหนาว...
s26	อดทนไว้ เดี๋ยวพี่พาไป โรงพยาบาล
s27	สัญญาครั้งที่สอง ของคืนนี้
s28	มือที่สั่น ค่อยๆ หยุดนิ่ง
s29	ก้องจับชีพจร ไม่เต้นแล้ว
s30	ก้องคิดว่า เขาเสียน้องไปแล้ว
s31	สิบวินาที
s32	เฮ้ย! ได้ยินพี่ไหม!
s33	แล้วน้อง ก็ลืมตา
s34	แต่ตาคู่นั้น ไม่ใช่ตาคนแล้ว
s35	มันพุ่งใส่ก้อง ก้องเอาเครื่องตัดขวาง ผลักมันสุดแรง
s36	ก้องถอยหลบมุมรถ มันมองไม่เห็นเขา
s37	บนหลังคารถ ไรเดอร์เสื้อเขียว วิ่งหนีสุดชีวิต มันกระโจนตามไป
s38	ทั้งทางด่วน มีแต่คนวิ่งหนี กับพวกที่ไล่กัด
s39	นี่ไม่ใช่อุบัติเหตุ อีกต่อไปแล้ว
# scene 03
s40	ไม่ไกลกัน รถเก๋งคันหนึ่ง พลิกตะแคง
s41	หมอแพรว หมอห้องฉุกเฉิน กำลังดึงคุณทศ ออกจากซากรถ
s42	แต่ประตูที่ยุบ อัดเขาติดเบาะ
s43	ไกลออกไป ฝูงของมัน กำลังวิ่งมา
s44	ก้องชะงัก หนีตอนนี้ ยังทัน
s45	แต่เขา วิ่งกลับเข้าไปช่วย
s46	ก้องเอาเครื่องตัดง้างประตู คุณทศหลุดออกมา
s47	พี่! รอผมด้วย!
s48	เจมส์ ไรเดอร์ส่งอาหาร กระโดดลงจากหลังคารถ แต่ที่ตามหลังมา คือน้องของก้อง
s49	ทุกคนขึ้นรถกู้ภัย ประตูปิดทัน แค่เสี้ยววินาที
s50	หน้าที่แนบกระจก คือคนที่เขาสัญญา ว่าจะพาไปโรงพยาบาล
s51	ก้องออกรถ แทรกไปตามช่องว่าง
s52	แต่ข้างหน้า รถบรรทุกขวาง เต็มถนน
s53	มือเขาไปเอง ตามความเคยชิน เปิดไซเรนขอทาง
s54	ทุกตัวบนทางด่วน หยุดวิ่ง แล้วหันมา พร้อมกัน
s55	ปิดเสียง! เร็ว!
s56	ก้องปิดไซเรน แต่สายไปแล้ว ทั้งฝูงรู้แล้ว ว่าเขาอยู่ตรงไหน
s57	เสียง กับแสง คือสิ่งที่เรียกมัน
s58	ขับไปสิ! จะจอดให้มันกิน หรือไง!
s59	รถข้างหน้า ขยับไม่ได้!
s60	พี่! ผมเคยผ่านแถวนี้ มีทางลง ข้างรถคันนั้น!
# scene 04
s61	ฝูงกระแทกรถ ไม่หยุด กระจกเริ่มร้าว
s62	ก้องเปิดตู้อุปกรณ์ ของเต็มตู้ แต่แบกไปได้ แค่ สี่อย่าง
s63	เครื่องตัด ชะแลง วิทยุ กระเป๋าพยาบาลใบเล็ก
s64	ที่เหลือ ต้องทิ้งทั้งหมด
s65	ก้องจุดพลุไฟฉุกเฉิน ขว้างไปอีกฝั่งถนน
s66	เกือบทั้งฝูง วิ่งตามแสงไป
s67	คุณทศเบียดออกไป เป็นคนแรก
s68	แขนเสื้อเกี่ยวกระจก ขาดเป็นทาง เลือดซึมออกมา
s69	เขารีบดึงแขนเสื้อ ลงปิดแผล ไม่บอกใครสักคำ
s70	ทุกคนวิ่งลง บันไดเหล็ก ข้างทางด่วน
s71	ข้างล่างมืด และเงียบ
s72	ของเหลือ แค่นี้เองเหรอ
s73	เอาออกมาได้ เท่านี้
s74	ถ้ามีคนเจ็บหนัก เราอาจช่วยไม่ได้
s75	โรงพยาบาลอยู่ข้างหน้า ผมเคยไปส่งอาหาร
s76	ก้องมองโทรศัพท์ ยังไม่มีสาย จากลูก
# scene 05
s77	แล้วโทรศัพท์ก็สั่น จอสว่างวาบ กลางความมืด
s78	พ่อ! พ่ออยู่ไหน!
s79	เขาพาหนู ขึ้นรถอพยพ บอกว่าจะไปท่าเรือ
s80	ครั้งนี้ พ่ออย่าผิดสัญญานะ
s81	ก้องยังไม่ทันรับปาก สัญญาณก็ขาด
s82	ก้องหันหลัง จะไปหาลูกเดี๋ยวนั้น
s83	ถ้าคุณไปคนเดียว ตอนนี้ คุณอาจไปไม่ถึงลูก
s84	ก้องกำโทรศัพท์แน่น แล้วเดินตามเจมส์ไป
# scene 06
s85	โรงพยาบาลริมแม่น้ำ ไฟยังสว่าง
s86	แต่ประตูเหล็ก ปิดสนิท
s87	เปิดไม่ได้! ใครโดนกัดมาบ้าง ก็ไม่รู้!
s88	ก้องยกเครื่องตัดขึ้น แบตยังเต็ม สามขีด ตัดโซ่ขาดแน่
s89	แต่เสียงตัดเหล็ก จะเรียกพวกมัน มาทั้งฝูง
s90	และคนข้างใน จะไม่เหลือประตูกั้น
s91	เขาลดมือลง
s92	ข้างๆ กัน มีตึกสร้างไม่เสร็จ มืดสนิท
s93	แล้วก้องก็เห็น เลือดหยดลงพื้น จากแขนเสื้อคุณทศ
s94	แผลอะไร?
s95	ไม่มีอะไร!
s96	ขอดูเดี๋ยวนี้!
s97	ก้องจำได้ดี น้องของเขา ใช้เวลาแค่ หกสิบวินาที
s98	แต่เสียงเถียงกัน ดังเกินไป
s99	ในความมืด มีเสียงฝีเท้า วิ่งเข้ามา
s100	ก้องยกชะแลงขึ้น
s101	แต่เขาจะหวด ใคร
```

## Lines for the caption emphasis table (caption, word, colour)

```
("50 วินาที", "50 วินาที", AMBER_ASS),
("หันไปหาเสียง", "เสียง", AMBER_ASS),
("ไหลไม่หยุด", "ไหลไม่หยุด", RED_ASS),
("30 วินาที", "30 วินาที", AMBER_ASS),
("ถี่ขึ้น", "ถี่ขึ้น", RED_ASS),
("ผมหนาว...", "หนาว", RED_ASS),
("โรงพยาบาล", "โรงพยาบาล", AMBER_ASS),
("สัญญาครั้งที่ 2", "สัญญาครั้งที่ 2", AMBER_ASS),
("หยุดนิ่ง", "หยุดนิ่ง", RED_ASS),
("ไม่เต้นแล้ว", "ไม่เต้นแล้ว", RED_ASS),
("เขาเสียน้องไปแล้ว", "เสียน้องไปแล้ว", RED_ASS),
("10 วินาที", "10 วินาที", AMBER_ASS),
("ก็ลืมตา", "ลืมตา", RED_ASS),
("ไม่ใช่ตาคนแล้ว", "ไม่ใช่ตาคน", RED_ASS),
("มันมองไม่เห็นเขา", "มองไม่เห็น", AMBER_ASS),
("มันกระโจนตามไป", "กระโจนตาม", RED_ASS),
("กับพวกที่ไล่กัด", "ไล่กัด", RED_ASS),
("นี่ไม่ใช่อุบัติเหตุ", "ไม่ใช่อุบัติเหตุ", RED_ASS),
("พลิกตะแคง", "พลิกตะแคง", AMBER_ASS),
("หมอแพรว", "หมอแพรว", AMBER_ASS),
("กำลังดึงคุณทศ", "คุณทศ", AMBER_ASS),
("อัดเขาติดเบาะ", "ติดเบาะ", RED_ASS),
("ฝูงของมัน", "ฝูงของมัน", RED_ASS),
("วิ่งกลับเข้าไปช่วย", "กลับเข้าไปช่วย", AMBER_ASS),
("เจมส์", "เจมส์", AMBER_ASS),
("คือน้องของก้อง", "น้องของก้อง", RED_ASS),
("หน้าที่แนบกระจก", "แนบกระจก", RED_ASS),
("รถบรรทุกขวาง", "ขวาง", RED_ASS),
("เปิดไซเรนขอทาง", "ไซเรน", RED_ASS),
("แล้วหันมา", "หันมา", RED_ASS),
("แต่สายไปแล้ว", "สายไปแล้ว", RED_ASS),
("เสียง กับแสง", "เสียง กับแสง", AMBER_ASS),
("มีทางลง", "ทางลง", AMBER_ASS),
("กระจกเริ่มร้าว", "ร้าว", RED_ASS),
("แค่ 4 อย่าง", "4 อย่าง", AMBER_ASS),
("ต้องทิ้งทั้งหมด", "ทิ้ง", RED_ASS),
("วิ่งตามแสงไป", "ตามแสง", AMBER_ASS),
("เป็นคนแรก", "คนแรก", AMBER_ASS),
("เลือดซึมออกมา", "เลือด", RED_ASS),
("ไม่บอกใครสักคำ", "ไม่บอกใคร", RED_ASS),
("ข้างล่างมืด", "มืด", AMBER_ASS),
("เราอาจช่วยไม่ได้", "ช่วยไม่ได้", RED_ASS),
("โรงพยาบาลอยู่ข้างหน้า", "โรงพยาบาล", AMBER_ASS),
("ยังไม่มีสาย", "ยังไม่มีสาย", RED_ASS),
("จอสว่างวาบ", "สว่างวาบ", RED_ASS),
("บอกว่าจะไปท่าเรือ", "ท่าเรือ", AMBER_ASS),
("พ่ออย่าผิดสัญญานะ", "อย่าผิดสัญญา", RED_ASS),
("สัญญาณก็ขาด", "สัญญาณก็ขาด", RED_ASS),
("คุณอาจไปไม่ถึงลูก", "ไปไม่ถึงลูก", RED_ASS),
("ไฟยังสว่าง", "ไฟยังสว่าง", AMBER_ASS),
("ปิดสนิท", "ปิดสนิท", RED_ASS),
("ใครโดนกัดมาบ้าง", "โดนกัด", RED_ASS),
("แบตยังเต็ม 3 ขีด", "3 ขีด", AMBER_ASS),
("มาทั้งฝูง", "ทั้งฝูง", RED_ASS),
("จะไม่เหลือประตูกั้น", "ไม่เหลือประตู", RED_ASS),
("มืดสนิท", "มืดสนิท", AMBER_ASS),
("เลือดหยดลงพื้น", "เลือด", RED_ASS),
("ใช้เวลาแค่ 60 วินาที", "60 วินาที", AMBER_ASS),
("ดังเกินไป", "ดังเกินไป", RED_ASS),
("มีเสียงฝีเท้า", "เสียงฝีเท้า", RED_ASS),
("ก้องยกชะแลงขึ้น", "ชะแลง", AMBER_ASS),
("ใคร", "ใคร", RED_ASS),
```

The conform matches on the whole caption text. No new caption carries two different colours. New captions that are also in the hook's table and so take the hook's colour: `เฮ้ย!`.

## Mix notes

- Narration stays clearly above effects, as in the hook mix. One exception by design: the siren after s53 plays at full level for 1.2 s in a gap with no words, then ducks under s54.
- The heartbeat pulse (s17-s28, back at s97) is a low effect under the voice, not music.
- Whispered lines (s72-s75) are performed quietly by the narrator, not lowered in the mix.
- No status icons anywhere. The watch, the phone screens, the gauge LEDs and the map are props shown full frame.
