# s12 QA: film 7, shots 12-13 (the lift and the unframing): louvre wall_eye area -> louvre staircase

Delivered: `frames/g_1108.png .. g_1341.png` (234 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions / audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 1108, 234 frames). Plan bounds g 1114..1335 (37.12-44.53 s); 6-frame handles rendered in
3D on both ends (g 1108..1113 = A1 walk already under way; g 1336..1341 = B3 smirk + push continue). Shot 12 = g 1114..1214, shot 13 =
g 1215..1335. `transition_in` cut (plan lists no dissolve: shot 11 -> 12 and 13 -> 14 stay in the louvre).
Two locations (one per render process): id 1 = gallery g 1108..1214 (`raw/s1`), id 2 = staircase g 1215..1341 (`raw/s2`).
Also `meta.json`, `cues.json` (film seconds), `contact.jpg` (16 frames, cyan line y 880), `compare.jpg` (g 1205 beside ref a t0049, warm red
interior close; g 1262 beside ref a t0085, stone walls). Scripts: `shot.py` (probe / stills / final), `deliver.py` (also writes `work/qa.txt`);
helpers from `../common.py`. Drafts `work/d1..d5.jpg`.

## Set-ups (framing change every 0.9-1.7 s)
| g | set-up | what | caption |
|---|---|---|---|
| 1108-1159 | A1 wide from the rope, slow push, 22 mm | Monday, the salon empty: vincenzo in the white smock walks in along the back wall from screen-right, glancing back, stops under her (1148) and looks up | "เช้าวันจันทร์" 37.10 |
| 1160-1194 | A2 CUT low from the left, 22 mm | eyes + head dart left / right (1162-1177), then both hands rise onto the frame's side edges (1178-1190) | "เขาสวมเสื้อคลุมขาวแบบเดียวกัน" |
| 1195-1214 | A3 CUT close low, 22 mm | up on his toes, he lifts the REAL 3D painting off its four hooks: `set_mona_lift` 0 -> 0.32 D (1197-1211), the hooks come free; hands world-pinned to the frame edges every frame | "ยกภาพลงจากผนัง" 39.87 s = g 1199 |
| 1215-1255 | B1 CUT, foot of the service stair, 26 mm | he hurries down the flight toward us with the framed painting at his side (prop `mona_framed` x1.85), glancing back up; frame-on-stairs off | "เดินเข้าบันไดหนีไฟ" |
| 1256-1289 | B2 CUT from the lower right, 22-23 mm | crouched on step 5 beside the empty gilt frame and her glass box (`set_frame_on_stairs` on), the bare panel (prop `mona_panel` x2.0 = the set canvas size) rising in his hands; glance up the stairs 1276 | "แกะกรอบทิ้ง" 41.98 s = g 1262 |
| 1290-1341 | B3 CUT front medium, slow push 25 -> 26 mm | he stands, brings the panel to his belly, tucks it behind the smock front (arms + panel to the back layer 1300-1302, bulge 0 -> 1 1300-1309), hands press it flat, sly smirk up the stairs (1312-) | "แล้วซุกภาพไว้ใต้เสื้อ" 42.84 / 43.60 s |

## Client rules
- **No depth of field**: common.Take (use_dof False + `L.setup_dof(..., None, None)` before every render). All sharp.
- **Mouths**: no quoted line in shots 12-13 -> static expression mouths only (worried / determined / smirk; changes behind blinks).
- **Heads** (`work/qa.txt`): gallery A1 0.56-0.57 H, A2 0.55, A3 0.55-0.57; stair B1 0.36-0.39, B2 0.40-0.42, B3 0.46-0.51. No head
  bottom below y 880 in any frame.
- **Dense set**: the salon hang + torchères; runtime dust sheet + bucket by the wall; staircase bucket, rag, broom. Theft headlines: none in
  either area (the gallery and stair carry no news textures).

## Runtime set changes (louvre.py untouched)
- The two velvet-rope spans in front of her and the two right-hand stanchions (x 0.9, 2.6) are deleted from this scene's `gallery_dressing`
  mesh (`unhook_rope()`): the rope crossed his face in the low angles and a stanchion crossed him in A1. Story-wise the museum is closed on
  Monday and the rope is unhooked. The left stanchions keep their span.
- `set_mona_lift` keyed every frame; `set_frame_on_stairs` keyed every frame; `set_flames` keyed every frame.

## Checks
Popcheck: jumps only at the five planned cuts (1160, 1195, 1215, 1256, 1290), plus 1302 -> 1303 (7.6 levels, median 3.9) = his hands come
back in front onto the bulge after the 3-frame tuck (first final vanished the panel in one frame, 11.6: re-rendered 1300-1302 with the
tuck). Near-still pairs: 1158 (the stop under her, 1 pair), 1160/1193 (A2 head holds), never more than 1 frame. No magenta / black frames, no
retried frames, no clipped sprites.

## Colour (`hue_report.row`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s12 gallery (g 1108-1214)                      61.8   34.4    1.6    0.3    0.0    0.4    0.3    1.1  0.58 0.63 0.03
s12 staircase (g 1215-1341)                     9.9   65.3    1.3    0.8    0.1   16.9    2.2    3.5  0.21 0.41 0.14
ref a t0049                                    54.2   32.7    0.7    0.0    0.0    8.5    0.9    2.9  0.56 0.41 0.20
```
Gallery matches the warm red interior ref (red 62 / 54, sat 0.58 / 0.56). The staircase is the set's grey-stone morning (sat 0.21, as
louvre_API 7 reports for the service rooms); shade stays blue (17), magenta 3.5, no magenta drift. Not graded here.

## Seconds per frame
13.8 s wall / 26.5 s CPU mean (two 2-thread processes at once): gallery 14.1 / 27.5, staircase 13.6 / 25.7. Sprites 320 px/D.

## Differences from the plan / notes
- The lift uses the set's real framed painting (hands pinned to it), not the cast prop; in the stair he carries the cast prop `mona_framed`
  scaled to the set frame. Lift height 0.32 D (clear of the hooks): his arms (rubber hose, stretch up to 2.0) still miss the frame edge by up
  to ~0.3 D in puppet units at full lift, hidden behind the frame's gilt.
- The 2D card cannot turn its back, so in A2/A3 he faces us while reaching up behind his head to the frame.
