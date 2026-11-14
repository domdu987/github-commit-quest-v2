# s13 QA: film 6b, shots 13-16 (plan 20.74-32.15 s), market MORNING + bakery MORNING

Delivered: `frames/g_0616.png .. g_0969.png` (354 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions/audio) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 616, 99 MB -> committed as `take.mkv.partaa/ab/ac`, rejoin with `cat take.mkv.part* > take.mkv`).
Take range g 622..963 ([g0, g1) = [622, 964)), 6 handle frames rendered in 3D on each side (g 616..621, 964..969).
Also `meta.json`, `cues.json`, `contact.jpg`, `compare.jpg` (our frames beside the pink_0 reference sheet), scripts `shot.py`
(probe / stills / final), `signs.py` (Thai cards), `deliver.py`, `qa.py` (-> `work/qa.txt`), `sheet.py`. Raw renders + per-frame json in `raw/`.

## Shots
| shot | g | picture |
|---|---|---|
| 13A | 616-667 | low push past a laughing farmer onto three EMPTY pillories under the plank "ห้ามขายขาดน้ำหนัก!", guards, a jeering woman ("แล้วร้านขนมปังในเมืองก็โดนจับทีละร้าน") |
| 13B | 668-734 | frontal on the row; heads pop into the pillories on the spoken count: "หนึ่ง" g 697, "สอง" g 712, "สาม" g 724 (voiced onsets 23.12 / 23.63 / 24.02 s measured in narration.wav, +0.1 s), each with a yellow count word "หนึ่ง!/สอง!/สาม!" popping above the head (overshoot) and a 3-frame camera bump toward it |
| 14 | 735-796 | CU truck along the pilloried bakers (tears, sweat, heads shaking, open hands in the wrist holes), punch-in on the middle baker g 772 (head 492 px = 68 % of width); bubble "ชั่งเป๊ะ!" pops on "เป๊ะ" g 787 |
| 15 | 797-878 | low MCU Henry: belly laugh 797-841 (eyes shut, tears, body bounce, mouth a fixed grin); punch-in g 842 to CU, smug half-lids, finger raised, lip-sync talk_mouth g 842-874 on "พวกขี้โกงทั้งนั้น!" (27.98-29.24 s) |
| 16 | 879-969 | ECU along three customer baskets on the counter: the PALE 13th loaf sits on top of each; Henry's hand reaches in and plucks it (g 893, 914, 935), lifts it smugly, drops it behind the counter; camera slides basket to basket; g 945 widens to kit behind the counter, deadpan, watching |

## Rules
- No depth of field (common.Take); everything sharp. No motion streaks.
- Mouths: only Henry's lip-sync g 842-874 moves. Bakers / townsfolk mouths are fixed drawings (the bubble carries the swearing).
- Framing changes: 668, 735, 772, 797, 842, 879 (+ slides at ~900 / ~922), 945; camera moves on every frame. Longest near-still run 1 frame.
- Heads (work/qa.txt): main heads centre 0.44-0.56 H. Exceptions: shot 15 lip-sync CU head bottom reaches y 887 (7 px into the band,
  chin/moustache only); shot 16 kit's head centre 0.23-0.27 H in the two-shot (Henry is the main head there, 0.33-0.44 H).
- Pale 13th loaf: drawn with paler BREAD colours (basket top loaf and Henry's held prop, `pale_bread` patch in shot.py only).
- Comic, not cruel: bakers sob/sweat in the pillories, no injury.

## Colour (hue_report stats, every 3rd frame)
```
shot 13  red 21.3 orange 31.7 yellow 1.5 green 0.8 cyan 0.2 blue 26.0 violet 10.7 magenta 7.8  sat 0.32 val 0.64 dark 0.02
shot 14  red 15.6 orange 31.2 yellow 0.2 green 1.8 cyan 0.6 blue 12.5 violet 16.4 magenta 21.6  sat 0.28 val 0.62 dark 0.06
shot 15  red 57.3 orange 41.1 yellow 0.8 green 0.1 cyan 0.0 blue 0.0 violet 0.0 magenta 0.6  sat 0.37 val 0.64 dark 0.01
shot 16  red 30.9 orange 62.4 yellow 1.7 green 0.0 cyan 0.0 blue 0.7 violet 0.3 magenta 4.0  sat 0.43 val 0.68 dark 0.02
```
Market morning = cool blue/violet sky + cobbles against warm houses (complementary). Shot 14's "magenta" is the set's lilac shade
on the cobbles/houses (market MORNING haze), not a pink cast. The bakery shots stay warm: the added cool area light (s13_cool) is
too weak to register in the numbers -- if the director wants the blue counter-colour stronger, grade the bakery shots in the conform.
Darks are low (set look, bakery_API 7).

## Known issues
- Pillory hands: the baker2 pillory drawing shows the sleeves going down behind the board; the hands at the wrist holes hardly read.
- Henry's reach in shot 16 is short: the hand target is corrected by AIM16 (measured ~100 px miss); the held loaf rides ~80 px
  screen-right of the basket's top spot at the pluck frame, reads as "lifted off the top".
- Foreground shutter-board basket (set dressing outside the counter) fills the lower third on basket 1 / 2 of shot 16 (caption band).
