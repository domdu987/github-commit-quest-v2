# s01 QA: film 24, shots 1-2 (the hook): yard roof_low + macro_dragon (WORKED EXAMPLE)

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 0, 157 frames g 0..156, 33.3 MB, not split), `frames/g_0000..0156.png`
(local only, 720x1280, R9 post applied), `meta.json`, `cues.json` (10 cues), `contact.jpg` (16 frames, cyan line = y 880),
`QA_AUTO.md` + `phone_sheet.jpg` (qa_auto PASS). Scripts: `shot.py` (probe / stills / final), `deliver.py` (frames, meta, cues,
contact, strips, `work/qa.txt`, encode); shared helpers and the GOTCHAS in `../common.py`.
g 0..77 = shot 1 (plan 0.00-2.60 s), g 78..150 = shot 2 (plan 2.60-5.02 s), g 151..156 = 6-frame out-handle (smoke + push go on).
No in-handle (film start). Hard cut at g 78 inside the take (second build: the sun follows each preset's camera).

## Client hard rules
| rule | how / measured |
|---|---|
| nothing floats, contact shadows | Yi: stage contact decal + shadow proxy on the quay (z 2.25). Both roof workers: Child-Of the turtle ride, decal laid on the roof normal (`C.roof_contact`), sun shadow on the roof. Kneeler card turned along the ship (`yaw_fixed` 90): knees, shins and toes on the roof (see "Fixed"). Checked at 3x crops g 1, 49. |
| no shake, one eased move | shot 1: preset camera pushed 8 % along its view line (0.35 sine + 0.65 linear); shot 2: 5 % push. qa_jitter median 0.11 px, no shaky second. |
| never static > 6 frames | qa_auto: no frozen runs. |
| nothing parented to the camera | camera unparented; DOF focus is a world-fixed empty on the mouth. |
| feet planted, no slide | feet / ground anchors keyed on one point every frame; their screen paths move only with the push (max 0.22 / 0.76 / 1.14 px per frame for ka / kd / Yi, smooth). 6 fps strips `work/strip_s1.jpg` checked. |
| no identical duplicates | yi24 + kor_a24 (kneel_hammer) + kor_d24 (stand_carry_spikes, mirrored): three members, three poses. |
| near bigger than far | head width Yi 79-95 px (9.5 D) > kd 68-79 (11 D) > ka 51-59 (13 D, kneeling). |
| heads above y 880 | head bottoms max: Yi 664, ka 558, kd 503. Shot 2 has no people. |
| characters sharp / DOF | shot 1 DOF off; shot 2 preset f/2.8 on the mouth, no characters. qa_auto: no soft frames. |
| mouths | no quote: fixed expression mouths only. |
| hard cuts | cut at g 78 (qa_auto detects it, no pop elsewhere); out at g 151 is a cut. |

## Timing (captions.json, narration at +0.10 s)
| g | what | caption |
|---|---|---|
| 0-77 | roof_low push-in; Yi idle sway, kd planted, ka hammers: strikes g 1, 13, 25, 37, 49, 61, 73 (3 frames down, 5 up, 4 wind-up) | "แม่ทัพคนนี้" / "เอาเหล็กแหลม" |
| 49 | strike on the word | "ไปตอกเต็ม" 1.54 s = g 49 |
| 78 | HARD CUT to the dragon macro | "หลังคาเรือ" (2.11-2.74) |
| 85 | the first puff leaves the snout, the next ones follow (level 0.35 -> 0.85) | "แล้วติดหัวมังกร" 2.74 = g 85 |
| 109-125 | the smoke swells (0.85 -> 1.2) | "พ่นควัน" 3.72 = g 115 |
| 125-156 | thick smoke rising across the sky, push continues into the handle | "ไว้ที่หัวเรือ" 4.15 |

## Set state per frame (keyed on every rendered frame)
set_spikes 2, set_ports 0, set_dragon_smoke (0 in shot 1; rising in shot 2, speed 1.3) + puff release keys (common.Take.key_set smoke_start).
Shot 2 kept spikes 2 for continuity with shot 1 (the macro barely shows the roof).

## Fixed after looking at full size (drafts work/d1-d4.jpg, crops work/f1crop2.png, d3crop.png, kd61.png)
- **Floating kneeler**: with the default camera-facing yaw the kneeling card ran 38 deg across the 49 deg eave slope; the roof hid
  its shins and toes and he hovered as a legless figure above his mark (only visible in a full-quality 3x crop, the 0.4 draft
  hid it). Card turned along the ship (`yaw_fixed = 90`). All of shot 1 was re-rendered.
- **Second worker off frame**: no quay point is inside the 9:16 frame AND farther than Yi; kd now stands on the same roof edge
  toward the bow (local x 6.1). At 5.5 his spike bundle overlapped the hammer swing; 6.1 separates them (re-rendered).
- **Smoke into the lens**: the preset macro_dragon camera is 8.2 D in front of the mouth; the puffs drift toward the bow and up,
  i.e. into the lens as huge blobs. Custom position 11 D off at -50 deg (preset lens 55 mm, f/2.8, focus on the mouth), sun re-aimed.
- **Smoke pop-in**: set_dragon_smoke(level > 0) shows all puffs at once; s01 hides each puff until it is younger than the time
  since the smoke started, so the stream leaves the snout one puff at a time.
- Shot 2 was re-rendered after the set's soft-smoke update (joseon.py, director's hold) at the preset's 16 samples.

## Seconds per frame
50.9 s wall / 97.7 s CPU mean per 720x1280 frame (540x960 Cycles + post, 2 threads, mostly two render processes on 4 shared cores):
shot 1 (24 samples) 50.4 / 96.4, shot 2 (macro_dragon, 16 samples) 51.4 / 98.9. On a free box with one process ~45 s wall.
157 frames ~1 h 20 min wall with two processes. Scene build ~1 s per preset (textures cached).

## Differences from the plan / known limits
- Shot 2 camera is not the preset position (see above); lens, f-stop, focus point and the set state are the preset's.
- Background bokeh in shot 2 is moderate (11 D focus at f/2.8): the pavilion reads soft, not a blur wall.
- The smoke leaves from the snout tip (the set's mouth point), not from between the jaws (set geometry; joseon.py not edited).
- The kneeler's toes sit up to ~0.1 D into the roof (7 deg slipway pitch along the card) - buried, never floating.
- Large plain wharf in the lower third of shot 1 (the preset's low framing; the caption sits there).
