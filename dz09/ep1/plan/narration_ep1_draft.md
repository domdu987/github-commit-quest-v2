# DEAD ZONE 09 / เขตปิดตาย 09, EP.1: narration after the hook title

One voice (Ohm) tells the story in the third person and also speaks the short lines, as in the hook (`audio/narr_ohm/script.json`, s01-s16). Ids continue at s17. Lower-case `s` = sentence, upper-case `S` = shot (the hook's convention). Machine copy: `narration_ep1.json`. Generator: `_gen/narr.py` (text + timing model), `_gen/write.py`.

## Numbers

| | |
|---|---|
| Hook | 0:00.00 - 0:53.32 (bite at 0:43.80, title 0:50.72) |
| New narration | 0:53.62 - 5:30.77, 89 sentences, 227 captions (61 with a coloured key word) |
| Episode running time | **5:34.62** (334.62 s, 8031 frames at 24 fps; new picture 6751 frames). Last word ends 5:30.77, then black and the end card |
| Characters to record | **2685** spoken Thai characters (numbers spelled out, no spaces or punctuation); **2856** counting spaces and punctuation, which is how a text-to-speech service bills. The hook was 573 / 609 |
| Speaking rate measured from the hook | 553 caption characters in 50.07 s = 11.04 per second with pauses; 12.58 per second inside a sentence; the last caption of a sentence runs 0.38 s longer |
| Voice time / silence | 248.3 s of sentences in 281.3 s of new picture; the rest is picture and effect beats |
| Estimate error | The hook's sentences ran from 6.8 to 18.1 characters per second, so single lines can be 30 %% off. Timings here are intended starts; the cut follows the real recording, as the hook did |

## Length: 5:35 against the 6:00-6:40 target

The screenplay gives the rest of SCENE 02 and SCENES 03-06 5:47 (0:53 to 6:40). This script takes 4:41 for them. What went and why:

- **SCENE 03, the first drive.** The screenplay has the truck drive along the gaps before the lorry. Here it is two shots (S83-S84). A truck driving through a jam is the most expensive thing to animate honestly and tells nothing new.
- **SCENE 04, the walk.** The talk on the way down is three whispered lines at the stair foot. No walking-and-talking filler.
- **SCENE 05.** The call is three lines from her and none from Kong: he is cut off before he can promise. Praew's argument is one line. The screenplay's 65 s becomes 29 s.
- **SCENE 06.** The refusal at the gate is one line; the flight to the building site is two shots.
- **Not cut:** the 60 seconds of SCENE 02 run in real time (the junior's eyes open 57.6 s after the bite on the episode clock), so that scene keeps its full length.
- Rendering is the other reason: every 10 s of picture costs about 3.5 CPU hours at these settings.
- 4 sentences are marked *trim*: they can go without breaking a set-up (10.5 s together).

## Retention structure

| Loop | Opened | Kept alive | Paid off |
|---|---|---|---|
| 60 seconds | hook s16 | s17 / s23 / s30 countdown, four watch inserts | s32-s33 (eyes open at 57.6 s); s101 at the end |
| Sound and light call them | s19 car alarm | s35 (out of sight = lost) | s54-s55 siren; s58 rule said aloud; s66-s67 flare; s79 phone light; s92 the cutter not used; s102 the shouting |
| The battery | hook s04 | | s47 third bar blinks; s91 at the chain |
| Kong's promises | hook s06-s10 | s26-s27 promise two | s51 the junior at the glass; s82-s84 promise three never spoken |
| The daughter's call | hook s05-s10 | s78 no call yet | s79-s83 the call; the pier is the series goal |
| The rider | s36 | | s48-s49 |
| Tos's wound | s69-s70 | s75-s76, s90 | s97-s100; left open by s105 |
| What was left behind | s63-s65 | s73-s75 | later episodes |

## Script

Caption split is marked with `/`. **Bold** = the coloured word (amber = fact, red = threat). Start and length are on the episode clock.


### SCENE 02 (rest) คนที่กลับมา (0:53.62 - 2:07.82)

| id | start | s | who | captions | colour | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s17 | 0:53.62 | 1.97 | narration | เหลืออีก / **50 วินาที** | amber | 20 | hard cut from title to picture; rain + beacons back at full level; low heartbeat pulse starts (one beat per second, under the voice) and runs to s31 | S25 S26 | countdown opens (pay-off of the hook's last line) |
| s18 | 0:55.69 | 4.12 | narration | ก้องเอาเครื่องตัด / กระแทกมันกระเด็น / ไปชนรถคันข้างๆ |  | 47 | metal thud on 'กระแทก'; body hits a car door on 'ชนรถ' | S27 S28 | Kong rams the driver off with the tool body |
| s19 | 0:59.91 | 3.58 | narration | สัญญาณกันขโมย / ดังลั่น / มันหันไปหา**เสียง** / ทันที | amber | 40 | car alarm (two-tone, panned to the alarm car's side) from the first caption, hazards blink; infected snarl turning away | S29 S30 | SETUP: they go for sound and flashing light |
| s20 | 1:03.64 | 2.69 | narration | ก้องพยุงน้อง / ไปหลบหลังรถกู้ภัย |  | 29 | two pairs of boots, one dragging; alarm now further off (distance + low-pass) | S31 | cover |
| s21 | 1:06.57 | 2.13 | ก้อง (line) | มองหน้าพี่ไว้! / ได้ยินไหม! |  | 22 | dry, close; rain on truck metal | S32 | dialogue |
| s22 | 1:08.85 | 2.77 | narration | น้องพยักหน้า / แต่เลือด / **ไหลไม่หยุด** | red | 30 | wet cloth press; junior's breath | S33 S34 S35 | wound |
| s23 | 1:13.80 | 1.33 | narration | **30 วินาที** | amber | 12 | watch tick, close and dry (three ticks before the line) | S36 | countdown |
| s24 | 1:15.43 | 2.29 | narration | ลมหายใจน้อง / สั้นลง / **ถี่ขึ้น** | red | 24 | fast shallow breathing, shivering | S37 | symptoms |
| s25 | 1:18.17 | 1.28 | น้องในทีม (line) | พี่... / ผม**หนาว**... | red | 9 | voice low; heartbeat a little faster | S38 | dialogue |
| s26 | 1:19.75 | 2.69 | ก้อง (line) | อดทนไว้ / เดี๋ยวพี่พาไป / **โรงพยาบาล** | amber | 29 |  | S39 | promise no. 2 (SETUP for s50, s76, s87) |
| s27 | 1:22.93 | 2.69 | narration | คืนนี้ ก้องสัญญา / ไปแล้ว **2 ครั้ง** | amber | 29 |  | S40 | open loop: the promise count |
| s28 | 1:26.22 | 2.23 | narration | มือที่สั่น / ค่อยๆ / **หยุดนิ่ง** | red | 23 | breathing stops; heartbeat stops with it; only rain | S41 | he goes still |
| s29 | 1:28.75 | 3.00 | narration | ก้องแตะชีพจรที่คอ / **ไม่มีอะไรเต้น**เลย | red | 33 | rain only; glove on wet skin | S42 | he checks for a response |
| s30 | 1:33.80 | 1.09 | narration | **10 วินาที** | amber | 9 | watch tick alone | S43 | countdown |
| s31 | 1:35.25 | 1.75 | ก้อง (line) | เฮ้ย! / ได้ยินพี่ไหม! |  | 16 |  | S44 S45 | dialogue |
| s32 | 1:40.90 | 1.57 | narration | แล้วน้อง / ก็**ลืมตา** | red | 15 | three watch ticks in silence before the line; sub-bass swell into the next line | S47 | PAY-OFF of the 60-second rule: eyes open 57.6 s after the bite |
| s33 | 1:42.52 | 2.45 | narration | แต่ตาคู่นั้น / **ไม่ใช่ตาคน**แล้ว | red | 26 | red flash 1 frame on the cut; infected inhale | S48 | pay-off of 'จะไม่ใช่คนอีกต่อไป' |
| s34 | 1:45.07 | 4.20 | narration | มันพุ่งใส่ก้อง / ก้องเอาเครื่องตัดขวาง / ผลักมันสุดแรง |  | 48 | snarl; teeth on metal; shove grunt; body against the truck panel | S49 S50 S51 | the attack |
| s35 | 1:49.42 | 2.84 | narration | ก้องถอยหลบมุมรถ / มัน**มองไม่เห็น**เขา | amber | 31 | the snarl drops to short searching breaths; Kong's held breath | S52 S53 | world rule 7 planted |
| s36 | 1:52.46 | 4.83 | narration | บนหลังคารถ / ไรเดอร์เสื้อเขียว / วิ่งหนีสุดชีวิต / มัน**กระโจนตาม**ไป | red | 56 | boots on car roofs (hollow bangs), windscreen cracking, a far scream | S54 S55 S56 | SETUP: the rider (James) and who chases him |
| s37 | 1:57.54 | 4.75 | narration | ก้องมองไปรอบตัว / ทั้งทางด่วน / มีแต่คนวิ่งหนี / กับพวกที่**ไล่กัด** | red | 55 | crowd screams from several directions, glass breaking left then right, horns | S57 S58 S59 | scale |
| s38 | 2:02.49 | 2.84 | narration | นี่**ไม่ใช่อุบัติเหตุ** / อีกต่อไปแล้ว | red | 31 |  | S60 | realisation |
| s39 | 2:05.69 | 2.13 | narration | และไม่ได้เกิด / **แค่ที่นี่** | red | 22 | city-wide sirens layered far away, wind; screams reduced to a distant bed | S61 | city wide shot *(trim)* |

### SCENE 03 รถกู้ภัยคันสุดท้าย (2:08.27 - 3:21.54)

| id | start | s | who | captions | colour | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s40 | 2:08.27 | 3.56 | narration | ไม่ไกลจากรถกู้ภัย / รถเก๋งคันหนึ่ง / **พลิกตะแคง** | amber | 40 | hazard relay ticking, dripping, a woman's strained effort | S62 S63 | new place |
| s41 | 2:11.93 | 4.28 | narration | **หมอแพรว** / หมอห้องฉุกเฉิน / กำลังดึงชายใส่สูท / ออกจากซากรถ | amber | 49 |  | S64 S65 | Praew introduced |
| s42 | 2:16.30 | 3.24 | narration | เขาชื่อ**คุณทศ** / ประตูที่ยุบ / อัดเขาติดเบาะ | amber | 36 | metal creak; Tos's grunts | S66 S67 | Tos introduced |
| s43 | 2:19.74 | 2.61 | narration | ไกลออกไป / **ฝูงของมัน** / กำลังวิ่งมา | red | 28 | many running feet on wet road, far, growing | S68 | deadline |
| s44 | 2:22.55 | 2.29 | narration | ก้องชะงัก / หนีตอนนี้ / ยังทัน |  | 24 | everything dips for half a second | S69 | the choice |
| s45 | 2:25.03 | 2.29 | narration | แต่เขา / วิ่ง**กลับเข้าไปช่วย** | amber | 24 | boots splashing | S70 | Kong's value shown by action |
| s46 | 2:27.42 | 3.08 | narration | ก้องสอดเครื่องถ่าง / เหล็กค่อยๆ / อ้าออก |  | 34 | cordless pump whine, metal groaning open | S71 S72 | the tool is used |
| s47 | 2:30.61 | 3.56 | narration | คุณทศหลุดออกมา / แต่แบตขีดที่ 3 / **เริ่มกะพริบ** | red | 40 | gauge warning beep x2 (quiet, close) | S73 S74 | PAY-OFF of 'แบตเต็ม 3 ขีด' + new open loop |
| s48 | 2:34.37 | 1.44 | เจมส์ (line) | พี่! / รอผมด้วย! |  | 11 | shout from above/behind, roof bangs | S75 | dialogue |
| s49 | 2:35.90 | 5.73 | narration | เจมส์ / ไรเดอร์ส่งอาหาร / กระโดดลงจากหลังคารถ / และที่ไล่ตามมา / คือ**น้องของก้อง** | red | 67 | landing splash; snarl close behind | S76 S77 S78 | PAY-OFF of s36 |
| s50 | 2:41.78 | 3.80 | narration | ทุกคนขึ้นรถกู้ภัย / ประตูปิดทัน / แค่เสี้ยววินาที |  | 43 | door slam, then a body hitting it | S79 S80 | into the truck |
| s51 | 2:45.83 | 4.28 | narration | หน้าที่**แนบกระจก** / คือคนที่เขาสัญญา / ว่าจะพาไปโรงพยาบาล | red | 49 | muffled snarl through glass, nails on glass; cabin is quiet | S81 S82 | PAY-OFF of promise no. 2 |
| s52 | 2:50.35 | 2.45 | narration | ก้องออกรถ / แทรกไปตามช่องว่าง |  | 26 | diesel start, tyres on wet road, mirrors scraping | S83 | drive |
| s53 | 2:52.90 | 2.77 | narration | แต่ข้างหน้า / รถบรรทุก**ขวาง** / เต็มถนน | red | 30 | brakes; wipers | S84 S85 | obstacle |
| s54 | 2:55.81 | 3.40 | narration | มือเขาไปเอง / ตามความเคยชิน / เปิด**ไซเรน**ขอทาง | red | 38 | switch click, then the siren at full level for 1.2 s (the only moment an effect is allowed to rival the voice: it sits in the gap after the line) | S86 S87 | the mistake |
| s55 | 3:00.41 | 3.56 | narration | ทุกตัวบนทางด่วน / หยุดวิ่ง / แล้ว**หันมา** / พร้อมกัน | red | 40 | siren ducks under the voice; all other screams stop | S89 S90 | PAY-OFF of the car alarm (s19) |
| s56 | 3:04.12 | 1.44 | หมอแพรว (line) | ปิดเสียง! / เร็ว! |  | 12 |  | S91 | dialogue |
| s57 | 3:05.66 | 4.59 | narration | ก้องปิดไซเรน / แต่**สายไปแล้ว** / พวกมันรู้แล้ว / ว่าเขาอยู่ตรงไหน | red | 53 | siren winds down; silence 0.4 s; then many feet running toward us | S92 S93 S94 | consequence |
| s58 | 3:10.50 | 2.69 | narration | **เสียง กับแสง** / คือสิ่งที่เรียกมัน | amber | 29 | first bodies hit the truck | S95 S96 | the rule, learned (used in s67, s92) |
| s59 | 3:13.39 | 2.53 | คุณทศ (line) | ขับไปสิ! / จะจอดให้มันกิน / หรือไง! |  | 27 | pounding all around | S97 | Tos's value shown |
| s60 | 3:16.02 | 1.97 | ก้อง (line) | รถข้างหน้า / ขยับไม่ได้! |  | 20 |  | S98 | dialogue |
| s61 | 3:18.13 | 3.40 | เจมส์ (line) | พี่! ผมเคยผ่านแถวนี้ / มี**ทางลง** / ข้างรถคันนั้น! | amber | 38 |  | S99 S100 | way out |

### SCENE 04 สิ่งที่ต้องทิ้ง (3:21.79 - 4:14.00)

| id | start | s | who | captions | colour | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s62 | 3:21.79 | 2.92 | narration | ฝูงกระแทกรถ / ไม่หยุด / กระจกเริ่ม**ร้าว** | red | 32 | body hits in an irregular rhythm, glass crack ticks | S101 S102 | pressure |
| s63 | 3:24.86 | 4.36 | narration | ก้องเปิดตู้อุปกรณ์ / ของเต็มตู้ / แต่แบกไปได้ / แค่ **4 อย่าง** | amber | 50 | locker latch, roll-up shutter | S103 S104 | the choice of things |
| s64 | 3:29.36 | 3.52 | narration | เครื่องตัด / ชะแลง / วิทยุ / กระเป๋าพยาบาลใบเล็ก |  | 39 | one grab sound per item, on the cut | S105 | the four things |
| s65 | 3:33.09 | 2.21 | narration | ที่เหลือ / ต้อง**ทิ้ง**ทั้งหมด | red | 23 | shutter left open; a monitor beeping once, abandoned | S106 | cost |
| s66 | 3:35.55 | 3.24 | narration | ก้องจุดพลุไฟฉุกเฉิน / ขว้างไปอีกฝั่งถนน |  | 36 | flare strike and hiss, window crank, the flare skittering on the road | S107 S108 | plan built on the rule |
| s67 | 3:38.94 | 2.29 | narration | เกือบทั้งฝูง / วิ่ง**ตามแสง**ไป | amber | 24 | the pounding moves away to the left | S109 | PAY-OFF of s58 |
| s68 | 3:41.43 | 1.97 | narration | คุณทศปีนออก / เป็น**คนแรก** | amber | 20 | glass crunch, cloth | S110 | character |
| s69 | 3:43.50 | 3.72 | narration | แขนเสื้อเกี่ยวกระจก / ขาดเป็นทาง / **เลือด**ซึมออกมา | red | 42 | cloth rip, sharp breath | S111 | SETUP: the wound (glass, shown clearly) |
| s70 | 3:47.37 | 3.48 | narration | เขารีบดึงแขนเสื้อ / ลงปิดแผล / **ไม่บอกใคร**สักคำ | red | 39 |  | S112 S113 | SETUP: the secret |
| s71 | 3:51.10 | 2.92 | narration | ทุกคนวิ่งลง / บันไดเหล็ก / ข้างทางด่วน |  | 32 | steel treads ringing under four pairs of feet, rain on steel | S114 S115 | escape |
| s72 | 3:54.37 | 1.89 | narration | ข้างล่าง**มืด** / และเงียบ | amber | 19 | the expressway noise is now overhead and muffled; drips | S116 | world rule 5 |
| s73 | 3:56.61 | 2.05 | หมอแพรว (line) | ของเหลือ / แค่นี้เองเหรอ |  | 21 | whispered | S117 | dialogue |
| s74 | 3:58.81 | 1.81 | ก้อง (line) | เอาออกมาได้ / เท่านี้ |  | 18 | whispered | S118 | dialogue |
| s75 | 4:00.82 | 2.84 | หมอแพรว (line) | ถ้ามีคนเจ็บหนัก / เราอาจ**ช่วยไม่ได้** | red | 31 | whispered | S119 S120 | irony: picture is Tos's arm |
| s76 | 4:03.91 | 3.32 | narration | ไม่มีใครเห็น / ว่าคุณทศ**กอดอก** / แน่นกว่าเดิม | red | 37 |  | S121 | irony stated *(trim)* |
| s77 | 4:07.54 | 3.24 | เจมส์ (line) | **โรงพยาบาล**อยู่ข้างหน้า / ผมเคยไปส่งอาหาร | amber | 36 |  | S122 S123 | goal |
| s78 | 4:11.08 | 2.92 | narration | ก้องมองโทรศัพท์ / **ยังไม่มีสาย** / จากลูก | red | 32 |  | S124 S125 | open loop: the daughter |

### SCENE 05 ลูกสาว (4:14.50 - 4:43.29)

| id | start | s | who | captions | colour | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s79 | 4:14.50 | 3.48 | narration | แล้วโทรศัพท์ก็สั่น / จอ**สว่างวาบ** / กลางความมืด | red | 39 | phone buzz on a hard surface x2; everybody's breath stops | S126 S127 | PAY-OFF of the missed calls + light = danger |
| s80 | 4:18.28 | 1.59 | น้ำเหนือ (line, on the phone) | พ่อ! / พ่ออยู่ไหน! |  | 13 | phone-band filter, crowd and engine behind her | S128 S129 | dialogue |
| s81 | 4:20.08 | 3.16 | น้ำเหนือ (line, on the phone) | เขาพาหนู / ขึ้นรถอพยพ / บอกว่าจะไป**ท่าเรือ** | amber | 35 |  | S130 | the series goal |
| s82 | 4:23.59 | 2.37 | น้ำเหนือ (line, on the phone) | ครั้งนี้ / พ่อ**อย่าผิดสัญญา**นะ | red | 25 | signal breaking up on the last word | S131 | the promise asked for |
| s83 | 4:26.25 | 2.53 | narration | ก้องยังไม่ทันตอบ / **สัญญาณก็ขาด** | red | 27 | dead-line tone, one beat, then nothing | S132 S133 | cut off |
| s84 | 4:29.18 | 3.48 | narration | **สัญญาครั้งที่ 3** / เขายังไม่ทัน / ได้พูดออกไป | amber | 39 |  | S134 | PAY-OFF of the promise count (s27) |
| s85 | 4:32.96 | 2.37 | narration | ก้องหันหลัง / จะไปเดี๋ยวนั้น |  | 25 | boots turning on gravel | S135 | impulse |
| s86 | 4:35.53 | 3.40 | หมอแพรว (line) | ถ้าคุณไปคนเดียว / ตอนนี้ / คุณอาจ**ไปไม่ถึงลูก** | red | 38 |  | S136 S137 | the argument |
| s87 | 4:39.33 | 3.96 | narration | ก้องกำโทรศัพท์แน่น / แล้วเดินตามเจมส์ / ไปโรงพยาบาล |  | 45 |  | S138 S139 | decision |

### SCENE 06 ประตูที่ไม่เปิด (4:43.79 - 5:30.77)

| id | start | s | who | captions | colour | chars | effect cue | shots | note |
|---|---|---|---|---|---|---|---|---|---|
| s88 | 4:43.79 | 2.61 | narration | โรงพยาบาลริมแม่น้ำ / **ไฟยังสว่าง** | amber | 28 | river wash, a generator hum, no rain noise on roofs for the first time | S140 | hope |
| s89 | 4:46.59 | 1.97 | narration | แต่ประตูเหล็ก / **ปิดสนิท** | red | 20 | hands on steel bars, a chain rattling | S141 | but |
| s90 | 4:48.81 | 3.32 | รปภ. โรงพยาบาล (line) | เปิดไม่ได้! / เราไม่รู้ว่า / ใคร**โดนกัด**มาบ้าง! | red | 37 | voice from inside, behind steel | S142 S143 | refusal; SETUP for the wound reveal |
| s91 | 4:52.38 | 3.72 | narration | ก้องยกเครื่องตัดขึ้น / โซ่เส้นนี้ / ตัดขาดได้แน่ |  | 42 | gauge beep (the blinking bar) | S144 S145 | temptation; battery loop touched again |
| s92 | 4:56.20 | 3.40 | narration | แต่เสียงตัดเหล็ก / จะเรียกพวกมัน / มา**ทั้งฝูง** | red | 38 |  | S146 S147 | the rule applied (pay-off of s58) |
| s93 | 4:59.70 | 2.45 | narration | และคนข้างใน / จะไม่เหลือประตู |  | 26 |  | S148 | Kong's value *(trim)* |
| s94 | 5:02.30 | 1.18 | narration | เขาลดมือลง |  | 10 |  | S149 | decision |
| s95 | 5:03.77 | 3.00 | narration | ข้างๆ กัน / มีตึกสร้างไม่เสร็จ / **มืดสนิท** | amber | 33 | tarpaulin flapping, dripping concrete | S150 | refuge by rule 5 |
| s96 | 5:06.88 | 1.83 | narration | ทุกคน / วิ่งเข้าไปหลบ |  | 18 |  | S151 | move *(trim)* |
| s97 | 5:09.21 | 4.43 | narration | แล้วก้องก็เห็น / **เลือด**หยดลงพื้น / ทีละหยด / จากแขนเสื้อคุณทศ | red | 51 | single drops on concrete, very close, in a quiet room | S152 S153 S154 | PAY-OFF of the hidden wound |
| s98 | 5:14.00 | 0.94 | หมอแพรว (line) | แผลอะไร? |  | 7 |  | S155 | dialogue |
| s99 | 5:15.08 | 1.09 | คุณทศ (line) | ไม่มีอะไร! |  | 9 | loud; it echoes in the bare concrete | S156 | dialogue |
| s100 | 5:16.28 | 1.41 | หมอแพรว (line) | ขอดูเดี๋ยวนี้! |  | 13 | louder; echo | S157 | dialogue |
| s101 | 5:17.99 | 3.24 | narration | ก้องรู้ดี / ว่า **60 วินาที** / มันสั้นแค่ไหน | amber | 36 | heartbeat pulse of scene 02 returns | S158 S159 S160 | PAY-OFF of the 60-second rule |
| s102 | 5:21.48 | 2.37 | narration | แต่เสียงเถียงกัน / **ดังเกินไป** | red | 25 | the echo of the shouting dies; one far snarl answers | S161 | cause |
| s103 | 5:24.00 | 2.92 | narration | ในความมืด / มี**เสียงฝีเท้า** / วิ่งเข้ามา | red | 32 | running feet on gravel from behind, closing | S162 S163 | effect |
| s104 | 5:27.27 | 1.57 | narration | ก้องยก**ชะแลง**ขึ้น | amber | 15 | steel bar scrape, heartbeat louder | S164 | the last action |
| s105 | 5:29.10 | 1.67 | narration | แต่เขาจะฟาด / **ใคร** | red | 14 | all sound cuts to nothing on 'ใคร'; black; 1.0 s of silence; then one watch tick | S165 S166 | CLIFFHANGER |

## Text for the recording (one line per sentence, numbers spelled out)

```
s17	เหลืออีก ห้าสิบวินาที
s18	ก้องเอาเครื่องตัด กระแทกมันกระเด็น ไปชนรถคันข้างๆ
s19	สัญญาณกันขโมย ดังลั่น มันหันไปหาเสียง ทันที
s20	ก้องพยุงน้อง ไปหลบหลังรถกู้ภัย
s21	มองหน้าพี่ไว้! ได้ยินไหม!
s22	น้องพยักหน้า แต่เลือด ไหลไม่หยุด
s23	สามสิบวินาที
s24	ลมหายใจน้อง สั้นลง ถี่ขึ้น
s25	พี่... ผมหนาว...
s26	อดทนไว้ เดี๋ยวพี่พาไป โรงพยาบาล
s27	คืนนี้ ก้องสัญญา ไปแล้ว สองครั้ง
s28	มือที่สั่น ค่อยๆ หยุดนิ่ง
s29	ก้องแตะชีพจรที่คอ ไม่มีอะไรเต้นเลย
s30	สิบวินาที
s31	เฮ้ย! ได้ยินพี่ไหม!
s32	แล้วน้อง ก็ลืมตา
s33	แต่ตาคู่นั้น ไม่ใช่ตาคนแล้ว
s34	มันพุ่งใส่ก้อง ก้องเอาเครื่องตัดขวาง ผลักมันสุดแรง
s35	ก้องถอยหลบมุมรถ มันมองไม่เห็นเขา
s36	บนหลังคารถ ไรเดอร์เสื้อเขียว วิ่งหนีสุดชีวิต มันกระโจนตามไป
s37	ก้องมองไปรอบตัว ทั้งทางด่วน มีแต่คนวิ่งหนี กับพวกที่ไล่กัด
s38	นี่ไม่ใช่อุบัติเหตุ อีกต่อไปแล้ว
s39	และไม่ได้เกิด แค่ที่นี่
s40	ไม่ไกลจากรถกู้ภัย รถเก๋งคันหนึ่ง พลิกตะแคง
s41	หมอแพรว หมอห้องฉุกเฉิน กำลังดึงชายใส่สูท ออกจากซากรถ
s42	เขาชื่อคุณทศ ประตูที่ยุบ อัดเขาติดเบาะ
s43	ไกลออกไป ฝูงของมัน กำลังวิ่งมา
s44	ก้องชะงัก หนีตอนนี้ ยังทัน
s45	แต่เขา วิ่งกลับเข้าไปช่วย
s46	ก้องสอดเครื่องถ่าง เหล็กค่อยๆ อ้าออก
s47	คุณทศหลุดออกมา แต่แบตขีดที่สาม เริ่มกะพริบ
s48	พี่! รอผมด้วย!
s49	เจมส์ ไรเดอร์ส่งอาหาร กระโดดลงจากหลังคารถ และที่ไล่ตามมา คือน้องของก้อง
s50	ทุกคนขึ้นรถกู้ภัย ประตูปิดทัน แค่เสี้ยววินาที
s51	หน้าที่แนบกระจก คือคนที่เขาสัญญา ว่าจะพาไปโรงพยาบาล
s52	ก้องออกรถ แทรกไปตามช่องว่าง
s53	แต่ข้างหน้า รถบรรทุกขวาง เต็มถนน
s54	มือเขาไปเอง ตามความเคยชิน เปิดไซเรนขอทาง
s55	ทุกตัวบนทางด่วน หยุดวิ่ง แล้วหันมา พร้อมกัน
s56	ปิดเสียง! เร็ว!
s57	ก้องปิดไซเรน แต่สายไปแล้ว พวกมันรู้แล้ว ว่าเขาอยู่ตรงไหน
s58	เสียง กับแสง คือสิ่งที่เรียกมัน
s59	ขับไปสิ! จะจอดให้มันกิน หรือไง!
s60	รถข้างหน้า ขยับไม่ได้!
s61	พี่! ผมเคยผ่านแถวนี้ มีทางลง ข้างรถคันนั้น!
s62	ฝูงกระแทกรถ ไม่หยุด กระจกเริ่มร้าว
s63	ก้องเปิดตู้อุปกรณ์ ของเต็มตู้ แต่แบกไปได้ แค่ สี่อย่าง
s64	เครื่องตัด ชะแลง วิทยุ กระเป๋าพยาบาลใบเล็ก
s65	ที่เหลือ ต้องทิ้งทั้งหมด
s66	ก้องจุดพลุไฟฉุกเฉิน ขว้างไปอีกฝั่งถนน
s67	เกือบทั้งฝูง วิ่งตามแสงไป
s68	คุณทศปีนออก เป็นคนแรก
s69	แขนเสื้อเกี่ยวกระจก ขาดเป็นทาง เลือดซึมออกมา
s70	เขารีบดึงแขนเสื้อ ลงปิดแผล ไม่บอกใครสักคำ
s71	ทุกคนวิ่งลง บันไดเหล็ก ข้างทางด่วน
s72	ข้างล่างมืด และเงียบ
s73	ของเหลือ แค่นี้เองเหรอ
s74	เอาออกมาได้ เท่านี้
s75	ถ้ามีคนเจ็บหนัก เราอาจช่วยไม่ได้
s76	ไม่มีใครเห็น ว่าคุณทศกอดอก แน่นกว่าเดิม
s77	โรงพยาบาลอยู่ข้างหน้า ผมเคยไปส่งอาหาร
s78	ก้องมองโทรศัพท์ ยังไม่มีสาย จากลูก
s79	แล้วโทรศัพท์ก็สั่น จอสว่างวาบ กลางความมืด
s80	พ่อ! พ่ออยู่ไหน!
s81	เขาพาหนู ขึ้นรถอพยพ บอกว่าจะไปท่าเรือ
s82	ครั้งนี้ พ่ออย่าผิดสัญญานะ
s83	ก้องยังไม่ทันตอบ สัญญาณก็ขาด
s84	สัญญาครั้งที่สาม เขายังไม่ทัน ได้พูดออกไป
s85	ก้องหันหลัง จะไปเดี๋ยวนั้น
s86	ถ้าคุณไปคนเดียว ตอนนี้ คุณอาจไปไม่ถึงลูก
s87	ก้องกำโทรศัพท์แน่น แล้วเดินตามเจมส์ ไปโรงพยาบาล
s88	โรงพยาบาลริมแม่น้ำ ไฟยังสว่าง
s89	แต่ประตูเหล็ก ปิดสนิท
s90	เปิดไม่ได้! เราไม่รู้ว่า ใครโดนกัดมาบ้าง!
s91	ก้องยกเครื่องตัดขึ้น โซ่เส้นนี้ ตัดขาดได้แน่
s92	แต่เสียงตัดเหล็ก จะเรียกพวกมัน มาทั้งฝูง
s93	และคนข้างใน จะไม่เหลือประตู
s94	เขาลดมือลง
s95	ข้างๆ กัน มีตึกสร้างไม่เสร็จ มืดสนิท
s96	ทุกคน วิ่งเข้าไปหลบ
s97	แล้วก้องก็เห็น เลือดหยดลงพื้น ทีละหยด จากแขนเสื้อคุณทศ
s98	แผลอะไร?
s99	ไม่มีอะไร!
s100	ขอดูเดี๋ยวนี้!
s101	ก้องรู้ดี ว่า หกสิบวินาที มันสั้นแค่ไหน
s102	แต่เสียงเถียงกัน ดังเกินไป
s103	ในความมืด มีเสียงฝีเท้า วิ่งเข้ามา
s104	ก้องยกชะแลงขึ้น
s105	แต่เขาจะฟาด ใคร
```

## Lines for `finish.EMPH` (caption, word, colour)

```
("50 วินาที", "50 วินาที", AMBER_ASS),
("มันหันไปหาเสียง", "เสียง", AMBER_ASS),
("ไหลไม่หยุด", "ไหลไม่หยุด", RED_ASS),
("30 วินาที", "30 วินาที", AMBER_ASS),
("ถี่ขึ้น", "ถี่ขึ้น", RED_ASS),
("ผมหนาว...", "หนาว", RED_ASS),
("โรงพยาบาล", "โรงพยาบาล", AMBER_ASS),
("ไปแล้ว 2 ครั้ง", "2 ครั้ง", AMBER_ASS),
("หยุดนิ่ง", "หยุดนิ่ง", RED_ASS),
("ไม่มีอะไรเต้นเลย", "ไม่มีอะไรเต้น", RED_ASS),
("10 วินาที", "10 วินาที", AMBER_ASS),
("ก็ลืมตา", "ลืมตา", RED_ASS),
("ไม่ใช่ตาคนแล้ว", "ไม่ใช่ตาคน", RED_ASS),
("มันมองไม่เห็นเขา", "มองไม่เห็น", AMBER_ASS),
("มันกระโจนตามไป", "กระโจนตาม", RED_ASS),
("กับพวกที่ไล่กัด", "ไล่กัด", RED_ASS),
("นี่ไม่ใช่อุบัติเหตุ", "ไม่ใช่อุบัติเหตุ", RED_ASS),
("แค่ที่นี่", "แค่ที่นี่", RED_ASS),
("พลิกตะแคง", "พลิกตะแคง", AMBER_ASS),
("หมอแพรว", "หมอแพรว", AMBER_ASS),
("เขาชื่อคุณทศ", "คุณทศ", AMBER_ASS),
("ฝูงของมัน", "ฝูงของมัน", RED_ASS),
("วิ่งกลับเข้าไปช่วย", "กลับเข้าไปช่วย", AMBER_ASS),
("เริ่มกะพริบ", "เริ่มกะพริบ", RED_ASS),
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
("ว่าคุณทศกอดอก", "กอดอก", RED_ASS),
("โรงพยาบาลอยู่ข้างหน้า", "โรงพยาบาล", AMBER_ASS),
("ยังไม่มีสาย", "ยังไม่มีสาย", RED_ASS),
("จอสว่างวาบ", "สว่างวาบ", RED_ASS),
("บอกว่าจะไปท่าเรือ", "ท่าเรือ", AMBER_ASS),
("พ่ออย่าผิดสัญญานะ", "อย่าผิดสัญญา", RED_ASS),
("สัญญาณก็ขาด", "สัญญาณก็ขาด", RED_ASS),
("สัญญาครั้งที่ 3", "สัญญาครั้งที่ 3", AMBER_ASS),
("คุณอาจไปไม่ถึงลูก", "ไปไม่ถึงลูก", RED_ASS),
("ไฟยังสว่าง", "ไฟยังสว่าง", AMBER_ASS),
("ปิดสนิท", "ปิดสนิท", RED_ASS),
("ใครโดนกัดมาบ้าง!", "โดนกัด", RED_ASS),
("มาทั้งฝูง", "ทั้งฝูง", RED_ASS),
("มืดสนิท", "มืดสนิท", AMBER_ASS),
("เลือดหยดลงพื้น", "เลือด", RED_ASS),
("ว่า 60 วินาที", "60 วินาที", AMBER_ASS),
("ดังเกินไป", "ดังเกินไป", RED_ASS),
("มีเสียงฝีเท้า", "เสียงฝีเท้า", RED_ASS),
("ก้องยกชะแลงขึ้น", "ชะแลง", AMBER_ASS),
("ใคร", "ใคร", RED_ASS),
```

`finish.emph` matches on the whole caption text. No new caption repeats another with a different colour; `เฮ้ย!` (s31) is already red in the hook table.

## Mix notes

- Narration stays clearly above effects, as in the hook mix. One exception by design: the siren after s54 plays at full level for 1.2 s in a gap with no words, then ducks under s55.
- The heartbeat pulse (s17-s28, back at s101) is a low effect under the voice, not music.
- Whispered lines (s73-s77) are performed quietly by the narrator, not lowered in the mix.
- No status icons anywhere. The watch, the phone screens, the gauge LEDs and the map are props shown full frame.
