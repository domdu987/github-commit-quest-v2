# s15 QA: film 8, shots 15-16 (summer): bazaar SUMMER -> dissolve -> inside the yakhchal SUMMER

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, **first_g 1168, 185 frames** g 1168..1352; over 45 MB, so it is split as
`take.mkv.partaa` + `take.mkv.partab`: `cat take.mkv.part* > take.mkv`). g 1168..1173 in-handle, g 1174..1265 shot 15,
g 1266..1346 shot 16, g 1347..1352 out-handle. **The plan's 15 -> 16 dissolve is already in the take**: 12 frames, g 1260..1271,
linear, blended in `deliver.py` from both sides rendered 8 frames past the centre (bazaar to g 1274, dome from g 1258; raw kept in
`raw/s2`, `raw/s3`). 720x1280, 12 samples, 2 threads. `meta.json` (transitions, events), `cues.json` (10 cues), `contact.jpg`.
Scripts: `shot.py` (probe / stills / final; two locations, final_loop take_key), `deliver.py`, `qa.py` (-> `work/qa.txt`), `sheet.py`.

## What happens
| g | set-up | action | caption |
|---|---|---|---|
| 1168-1205 | 15a stall | the water merchant on his takht sweating (sweat + heat shimmer), beating a palm fan every 8 frames; steam curling up from his five great jars; push + orbit | "แล้วหน้าร้อนก็มาถึง" |
| 1206 | | CUT inside shot 15 to the square | "น้ำในบ่อ" 40.19 = g 1209 |
| 1206-1271 | 15b well | the woman tips the well bucket into a clay jar (the stream steams), the old man fans himself, the boy flaps a hand at his face, steam rises off the well; iwan + minaret behind; push | "ทั้งเมืองกลายเป็นน้ำอุ่น" |
| 1260-1271 | | DISSOLVE to the inside of the dome | "แต่ในโดมผนังดินหนาสองเมตร" |
| 1260-1352 | 16 dome | cool blue interior, ice blocks stacked 2-5 high round the pit, farid on the ice holding up a lantern (warm point light + halo keyed to the drawn lantern), happy -> turns to us smug (g 1300-1314); crane down + push | "น้ำแข็งยังอยู่เต็ม" |

## Numbers (`work/qa.txt`)
- Heads: merchant 124-158 px, y 0.56-0.59 H; woman / old man y 0.55 H, boy y 0.60-0.61 H (a wide square shot), farid 140-173 px,
  y 0.36-0.38 H. No head below 880.
- Popcheck: one jump, the internal cut 1205 -> 1206 (expected); the dissolve is smooth. No near-still frames, no black / magenta frames.
- Hue: shot 15 orange 49 / red 15 / blue 25 (hot sunlit bazaar); shot 16 red 42 / orange 23 / blue 28 (mud cone + cool ice); magenta <= 1.7.
- Render ~11 s wall / 21 s CPU per frame.

## Differences from the plan / decisions
- Shot 15 has two set-ups: the merchant's steaming jars (plan "merchant's jars steaming"), then the well (plan well_eye, camera nearer
  and turned right so the pour reads). The cut is on "น้ำในบ่อ".
- Steam is runtime camera-only scrolling cards (bakery `_mat_add` with the set's wisp texture plus a side fade added in shot.py). The first
  final showed hard card edges, so the material got the side fade and both bazaar set-ups were re-rendered.
- The dome's ice is a pit below the walkway, so "stacked high" is runtime columns of ice blocks on the ice top round farid.
- No quote: mouths static (panting `talk_a` for the hot townsfolk, smile for farid).
