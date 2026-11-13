# s11 QA: film 5, shot 11 (the gaffer lifts his bright lamp: quote 2), mine set tunnel LAMP

Delivered: `take.mkv` = `frames/g_0963.png .. g_1100.png` (138 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 971..1092 = shot 11 ([g0, g1) = [971, 1093)); g 963..970 = in-handle, g 1093..1100 = out-handle (both rendered in 3D).
Also `meta.json` (first_g 963, n_frames 138), `cues.json`, `contact.jpg`, `compare.jpg` (11a/b/c vs ref a t0083/t0085/t0087).
Scripts: `shot.py`, `tk.py`, `deliver.py` + `tk_deliver.py` (-> `work/qa.txt`).

## Client rules
- No depth of field: `M.setup_dof(scene, None, None, cam=...)` before every render. No motion blur. Everything is sharp.
- No cage in this shot (the set's 3D cage is hidden).

## Timing
| seg | g | what | ref a |
|---|---|---|---|
| 11a | 963-1010 | low angle (pitch 23-25 deg) under the roof timbers: the gaffer lifts his flame safety lamp (lift g 978-992, back_out; up on "ตะเกียงขึ้นชี้" 32.97 s = g 992). His flame goes 1.0 -> 1.7 and the keyed lamp_light 1.0 -> 1.6; the other hand comes across to point at the lamp; miners behind; slow push | t0083 |
| 11b | 1011-1050 (cut) | closer and lower on the gaffer: the raised bright lamp beside his smug face. His mouth moves from g 1026 (the quote "ไฟยังสว่างอยู่เลย นกเอ็งแค่ง่วงนอน", 34.09-36.40 s = g 1026-1095), lip-synced from the narration level with a new drawing every 2 frames (flat / talk_a / talk_b / talk_o); his gaze turns from the lamp to the boy | t0085 |
| 11c | 1051-1100 (cut, handle 1093-1100) | alfie's point of view at eye level, 30 mm, looking outbye: the three miners in front shrug (palms up g 1054-1072, then settle to a half shrug) with unimpressed / smirk faces; the gaffer between them still talking, lamp high; slow push | t0087 |
Framing changes: g 971 (in), 1011 (1.33 s), 1051 (1.33 s), out 1093 (1.40 s). The camera moves in every frame.

## Staging (`work/qa.txt`)
| seg | head | width px | centre x | centre y (H) |
|---|---|---|---|---|
| 11a | gaffer | 183-197 | 288-293 | 0.41-0.42 |
| 11a | miner2 / miner3 / miner1 (behind) | 159-174 / 129-138 / 102-108 | 646-682 / 477-494 / 279-284 | 0.52-0.60 |
| 11b | gaffer | 278-293 | 226-235 | 0.46-0.47 |
| 11c | gaffer / miner1 / miner2 / miner3 | 124-132 / 214-238 / 142-152 / 162-175 | 376-381 / 624-650 / 108-125 / 244-254 | 0.38-0.49 |
All heads are above y 880. Mouths: only the gaffer's moves, and only during g 1026..1095. The miners' mouths are closed.
Popcheck: pops only at the cuts 1010 -> 1011 and 1050 -> 1051. No black or magenta frames, no retried frames, no clipped sprites.

## Colour (hue_report rows)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s11 11a (g 963-1010)                           16.4   24.2    0.3    0.1    0.0   44.9    6.4    7.6  0.42 0.43 0.07
s11 11b (g 1011-1050)                          21.1   40.6    0.0    0.0    0.0   29.0    3.6    5.7  0.45 0.45 0.07
s11 11c (g 1051-1100)                          10.2   11.2    0.6    0.2    0.0   59.9   10.9    6.9  0.35 0.43 0.06
s11 all (g 963-1100)                           16.3   26.1    0.3    0.1    0.0   43.7    6.7    6.8  0.41 0.44 0.07
ref a t0083 t0085 t0087                         1.0    1.2    0.0    0.0    0.0   82.3   10.4    5.2  0.56 0.61 0.04
```
Blue night tunnel by the set's design (the reference night rampart is even bluer). 11b is the warm close-up: the bright lamp lights the timbers orange. Shade reads blue-violet, never magenta.

## Seconds per frame
13.4 s wall / 26.1 s CPU mean (2 threads, another render process running alongside). 11a 27.3, 11b 21.1 (gaffer only), 11c 28.8 CPU s.

## Differences from the plan / known issues
- The plan has one `tunnel_low` setup. I split it into 11a and 11b (both low angles on the foreman) and 11c (eye-level reverse, so the miners' shrug reads). All cameras are custom.
- His smug mouth before the quote is a small dark bar under the walrus moustache. It is static and only opens on the quote.
- 11c: the coal heaped in the near tub (left foreground) catches a bright glint from the set's coal-sparkle shader. miner1 is cut by the right frame edge.
- The quote runs to g 1095, 3 frames past the shot end; the out-handle carries those frames.
