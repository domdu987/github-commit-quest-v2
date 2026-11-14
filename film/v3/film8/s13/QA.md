# s13 QA: film 8, shots 13-14 (the false ending): desert_ice plain, NOON

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, **first_g 958, 222 frames** g 958..1179; 75.6 MB, so also split as
`take.mkv.partaa` + `take.mkv.partab`: `cat take.mkv.part* > take.mkv`). g 958..963 in-handle, g 964..1064 shot 13, g 1065..1173
shot 14, g 1174..1179 out-handle (all rendered in 3D). 720x1280, 12 samples, 2 threads, denoise FAST. `meta.json`, `cues.json` (11 cues),
`contact.jpg` (cyan line = y 880). Scripts: `shot.py` (probe / stills / final), `deliver.py`, `qa.py` (-> `work/qa.txt`), `sheet.py`.

## What happens
| g | shot | action | caption |
|---|---|---|---|
| 958-979 | 13 | farid asleep on his back on a straw mat at the foot of the wall, in its shade (zzz, breathing); bucket, jars, saw, pick, brick pile, rocks round him | "จนวันหนึ่ง" |
| 980-985 | 13 | jolts awake: lie 90 -> 0 in 5 frames with a stretch pop, shocked, pale, sweat, arms flying up | "เขาตื่นสาย" 32.75 = g 985 |
| 986-1064 | 13 | trembling, turns to the channels, hands to his head, stares at the mud | "น้ำแข็งในร่องละลาย เป็นโคลน ตอนเที่ยง" |
| 1065 | 14 | CUT (plan) to the merchant, same place | "พ่อค้า" |
| 1065-1112 | 14 | big belly laugh, head back -> bent over laughing to tears (cry + tears, slapping) | "หัวเราะจนน้ำตาไหล" |
| 1113-1170 | 14 | lip-sync on the quote, pointing at the mud, tears still running | "เห็นมั้ย ทะเลทรายไม่มีน้ำแข็งหรอก!" |
| 1162-1179 | 14 | back into the laugh on "หรอก!" | |
Farid stands sad in the background of shot 14, on the north bank beyond channel 5, with the dome door behind.

Camera: shot 13 starts low north-west of him looking south-east (az 116, z 1.6), then cranes up and back west while panning left to az 101 (z 6.2).
It ends on the five channels of mud running to the yakhchal. Shot 14 is a medium from west-north-west over channel 5 (az 105 -> 107.5,
z 2.7) with a slow push of 1.1 D and an orbit. 22 mm, NO depth of field, moves are 0.35 sine + 0.65 linear.

## Numbers (`work/qa.txt`)
- Heads: farid shot 13 48-97 px, centre y 0.41-0.53 H; merchant 134-161 px, y 0.48-0.51 H; farid (bg) 47-51 px. No head below 880.
- Popcheck: one jump, the planned cut 1064 -> 1065. No near-still frames (median change 3.4 levels). No black / magenta frames.
- Render: 13.4 s wall / 17.7 s CPU per frame (2 threads; up to three processes at once).
- Hue: shot 13 red 20 / orange 31 / blue 24 / violet 23 (the wall's shade); shot 14 orange 35 / blue 42 / violet 5; magenta <= 1.6.

## Differences from the plan / decisions
- **Sun raised at runtime** (NOON key 44 -> 70 deg, same colour; `D.STATE['sun']` rotation): at 44 deg the 15 D wall shades every
  channel, so the mud read as a dull violet shadow. Now farid sleeps in the shade at the wall foot and the mud plus the merchant
  are in the blazing sun. The painted sun is not in frame.
- Shot 13 "channels_wide" is reached at the end of a crane, not the preset camera (the preset from the far north-west keeps farid tiny).
- Shot 14 is set on the bank lane y 11.6, away from the lantern posts (the y 6.0 post stood in the middle of the frame in draft 1).
- Mouths: the merchant's static laughing mouth ('talk_b') outside the quote, and talk_mouth driven by the narration envelope only in g 1113..1170.
