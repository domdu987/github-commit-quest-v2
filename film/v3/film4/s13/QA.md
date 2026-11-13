# s13 QA: film 4, shot 13 (SUNSET: the master pats kenta's shoulder, smug quote; kenta worried), pagoda set v2

Delivered: `take.mkv` = `frames/g_1048.png .. g_1186.png` (139 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 1055..1179 = shot 13 ([g0, g1) = [1055, 1180)); g 1048..1054 in-handle and g 1180..1186 out-handle, both rendered in 3D (camera keeps
moving) for 10-frame dissolves (in from shot 12, out to the NIGHT take s14). Also `meta.json` (first_g 1048, n_frames 139), `cues.json`
(9 cues), `contact.jpg` (16 frames), `compare.jpg` (3 final frames beside ref a t0055 / t0057 / t0059). Scripts: `shot.py`, `base4.py`
(shared, same file in s14 / s16), `deliver.py`. Raw renders + per-frame json in `raw/s13`.

## Timing (narration_bankky.wav at +0.10 s, captions_bankky.json)
| part | g | what |
|---|---|---|
| A | 1048-1092 | street two-shot in front of the red gate (pagoda finial above it), master left and nearer, kenta right; slow push. The master's right hand comes down onto kenta's shoulder g 1066-1072 (pinned to kenta's shoulder anchor, world target), pat lands on "ไหล่เขา" (35.80 s = g 1077), pats again g 1091, 1104; kenta flinches on each (squash pulse) |
| B | 1092-1099 snap, -1131 | punch-in from the left on the master (low-ish, he towers over kenta); quote "หอของข้านิ่งยังกับภูเขา เจดีย์เมาของเจ้าใกล้ล้มแล้ว" from g 1090 (36.25 s) to the end of the take (39.29 s = g 1182): mouth lip-synced to the narration RMS, a new drawing every 2 frames, chin up, smug bob |
| C | 1131-1139 snap, -1186 | on "เจดีย์เมาของเจ้า" (37.55 s = g 1130): two-shot favouring kenta, worried, looking up at him; a worried glance away toward the pagoda g 1150-1172 |
Framing changes g 1055 (start), 1077 (pat), 1092-1099, 1131-1139: gaps 0.73, 0.5, 1.3, 1.3 s, then 1.4 s of drift to the shot end.

## Staging (`work/qa.txt`)
| head | width px | centre x | centre y (H) | head bottom below 880 |
|---|---|---|---|---|
| master | 139 -> 244 | 235-306 | 0.40-0.46 | none |
| kenta | 138 -> 220 | 416-494 | 0.54-0.58 | none |
Pinned hand: master's right hand on kenta's shoulder (`actors.local_to_world` of kenta's shoulder anchor + pat lift), solver error 0.0 D;
the master stands 0.2 D nearer than kenta so the hand draws over him. head_flip off (sun from the west = screen-left in every view).
Nobody's back to the camera. Mouths: only the master's moves, only inside the quote (g 1090-1182); kenta's is the fixed "wavy" worried mouth.
Actor cards tinted `#ffe2cc` (sunset). Sprites 320 px per D.

## Motion / popcheck
No cuts inside the take. Largest frame-to-frame change 1.7 levels (the snaps); median 1.1; one near-still frame (g 1127, end of B's
drift, < 0.35 levels; the hand-held shake 0.06 deg keeps every frame moving). No black / magenta frames, no retried frames, no clipped sprites.
**Re-render fix:** the SUNSET haze veil is a camera-only cylinder of radius 36 about (6, -8); camera C stood right on it, and g 1152 rendered
without the haze (a 16-level pop). shot.py now keeps the camera at least 36.6 D from that axis (C sits ~0.6 D further back); the 90 affected
frames (g 1097-1186) were re-rendered.

## Colour (`hue_report.row`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s13 shot 13 (g 1048-1186)                      46.8   33.7    0.0    0.0    0.0    0.0    3.7   15.7  0.43 0.65 0.00
ref a t0055 t0057 t0059                        16.0   72.2    1.6    1.4    0.2    7.5    0.6    0.4  0.31 0.69 0.01
```
Out of band: red 46.8 (band 30-41), magenta 15.7 (0-10), blue 0, dark 0.00. This is the set's SUNSET preset itself: the low west sun leaves
the whole street in violet shade and the preset's warm haze veil (#ffb47a x 0.10) is added over it, which pushes the shade toward pink.
On the one frame that lost the veil (old g 1152) the shade read blue-violet. I did not change the set's haze (shot 12, also SUNSET,
shares it); if the director wants the shade bluer, lowering that veil at runtime from shot.py is a one-line change + re-render (~27 min).

## Seconds per frame
11.46 s wall / 22.7 s CPU mean (2 threads).

## Differences from the plan / the reference
- Plan "street_eye two-shot": custom eye-level cameras in the street 4-6 D in front of the gate (the set's street_eye is 18 D away).
- Ref t0055-t0059 is a daylight wide at a castle gate; ours is the sunset street at the red gate, two-shot.
- Mouth quote times taken from captions_bankky.json (36.25-39.29 s) rather than the plan's 36.4-39.1.
