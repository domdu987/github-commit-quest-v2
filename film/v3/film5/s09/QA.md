# s09 QA: film 5, shots 9 + 10 (the song countdown + "run"), mine set tunnel LAMP

Delivered: `take.mkv` = `frames/g_0749.png .. g_0978.png` (230 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 757..970 = shots 9 + 10 (shot 9 = 757-870, shot 10 = 871-970); g 749..756 = in-handle, g 971..978 = out-handle (both rendered in 3D).
Two 10-frame dissolves are mixed inside the take (smoothstep, as in s01): day 1 -> day 5 (g 807-816, raw 9b to g 819 / 9c from g 805) and
day 5 -> day 10 (g 866-875, raw 9d to g 878 / 10a from g 864). Also `meta.json` (first_g 749, n_frames 230, transitions, frame_source),
`cues.json`, `contact.jpg`, `compare.jpg` (9a/9b/9c/10b/10c vs ref a t0039/t0041/t0043/t0069/t0071). Scripts: `shot.py`, `tk.py`, `deliver.py` + `tk_deliver.py`.

## Client rules
- No depth of field: `M.setup_dof(scene, None, None, cam=...)` before every render (the set's cage_insert DOF default is never applied). No motion blur. Everything is sharp.
- **Hanging cage (9a-10b)**: the set's 3D cage on its nail. The canary sprite card stands at the perch point (the cage centre), INSIDE the bars:
  front wires cross the bird and the back wires are hidden behind it; its feet are on the perch dowel. I checked this by eye at full size in every insert.
  The cage's second wooden cross dowel (0.15 D above the perch, pointing at the camera) is removed at runtime in `tk.py`
  (`_drop_cross_dowel`, set file untouched). Without that, a bar cut through the bird's chest in the ECUs.
- **Held cage (10c)**: the cast's 2D held cage (prop `cage` + pose key `bird`: perch_quiet, eyes half shut, drooping, inside the bars). The set's 3D cage is hidden.
- The canary stays gentle: no X eyes. Day 10 ends quiet (beak closed, eyes 0.5, droop 0.25). It doesn't fall in this take; the fall is shot 12.

## Timing
| seg | g | what | ref a |
|---|---|---|---|
| 9a | 749-786 | day 1, insert wide: cage on the nail, chalk tally "1" (one stroke) on the pit prop above the nail, 5 notes; slow push + arc | t0039 |
| 9b | 787-811 (cut) | ECU between the wires, 5 notes floating up; push | t0041 |
| 9b->9c | 807-816 | dissolve (days pass) | |
| 9c | 812-841 | day 5 ("วันที่ห้า" 27.03 s = g 814), wide: tally "5" (four strokes + slash), 3 notes, bird a little ruffled; opposite arc | t0043 |
| 9d | 842-870 (cut) | ECU, 3 notes | |
| 9d->10a | 866-875 | dissolve = the shot 9 / 10 boundary (g 871) | |
| 10a | 871-905 | day 10 ("วันที่สิบ"), wide: tally "10" (two groups), 3 weak notes, bird tired | t0067 |
| 10b | 906-935 (cut) | ECU push: notes 3 -> 2 -> 1, the beak closes on "แล้วก็เงียบ" (30.32 s = g 913), silence, the bird droops | t0069 |
| 10c | 936-970 (HARD CUT on "เขาตะโกน" 31.11 s = g 936) + handle 971-978 | alfie (mirrored, facing the men and the far exit) shouts "run!" (held shout drawing, sweat), points with a back_out jab; cage in his other hand; gaffer, miner1, miner2 in the depth turn (stunned); fast cubic_out push, then a slow one | t0071 |
Framing changes: g 757 (in), 787, 812 (dissolve), 842, 871 (dissolve), 906, 936, 971: gaps 1.00, 0.83, 1.00, 0.97, 1.17, 1.00, 1.17 s.
Every camera moves in every frame.

## Staging (`work/qa.txt`)
| seg | head | width px | centre x | centre y (H) |
|---|---|---|---|---|
| 9a / 9c / 10a (wide) | canary | 109-129 | 380-410 | 0.56-0.57 |
| 9b / 9d / 10b (ECU) | canary | 201-263 | 341-357 | 0.52-0.62 |
| 10c | alfie | 254-324 | 448-474 | 0.52-0.55 |
| 10c | gaffer / miner1 / miner2 (far) | 85-92 / 106-116 / 98-106 | 112-251 | 0.44-0.48 |
The canary's head crosses y 880 by up to ~17 px at the end of the 9b and 9d ECU pushes (g 810-818, g 865-877). Those frames sit almost entirely inside the
dissolves and handles; its head centre there is 0.61-0.62 H. All other heads stay above y 880.
Mouths: no mouth moves. Alfie's shout is a single held drawing (`shouting` / talk_b), not lip-synced; the bird's beak animates as the song.
Popcheck: pops only at the cuts 786/787, 841/842, 905/906, 935/936. No black or magenta frames, no retried frames, no clipped sprites.

## Colour (hue_report rows)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s09 9a (g 749-786)                              1.2   29.9    4.0    0.0    0.0   49.8   11.6    3.5  0.42 0.41 0.08
s09 9b (g 787-818)                              2.4   48.8    6.3    0.0    0.0   28.0    9.9    4.6  0.43 0.46 0.13
s09 9c (g 805-841)                              2.1   36.0    4.4    0.0    0.0   44.5    9.6    3.4  0.43 0.42 0.08
s09 9d (g 842-877)                              2.5   47.5    8.7    0.0    0.0   27.7    8.9    4.7  0.43 0.47 0.12
s09 10a (g 864-905)                             1.8   34.6    4.7    0.0    0.0   44.6   10.7    3.5  0.41 0.42 0.08
s09 10b (g 906-935)                             2.2   60.6    7.4    0.0    0.0   18.3    7.4    4.1  0.46 0.51 0.16
s09 10c (g 936-978)                            14.1    7.5    0.1    0.0    0.0   59.3   11.1    7.8  0.36 0.41 0.08
s09 all (g 749-978)                             3.6   38.7    5.2    0.0    0.0   38.3    9.7    4.4  0.42 0.44 0.10
ref a t0039 t0041 t0043 t0069 t0071            13.5    7.5    0.3    0.1    0.0   68.6    6.2    3.8  0.43 0.51 0.09
```
The inserts are gold brass and a yellow bird against the blue-violet tunnel. Shade is blue-violet, never magenta (3.4-7.8).

## Seconds per frame
15.0 s wall / 29.3 s CPU mean (two processes x 2 threads). Wides 27-28, ECUs 30-31 (2048 px/D bird sprite), 10c 30.7 CPU s.
260 raw frames for 230 delivered (the dissolve overlaps).

## Differences from the plan / known issues
- Shot 9 uses a wide + ECU per day (4 setups) and shot 10 uses wide + ECU + 10c, all custom cameras, for the 1.0-1.5 s rhythm. The plan's `cage_insert` camera
  looks along the perch axis (end-on), so I placed the cameras across the tunnel, looking at the left wall, where the perch reads horizontal.
- The chalk tally sits on the pit prop ABOVE the nail (z 3.45-3.95), not below. Below the nail it would fall in the caption band.
  It is a runtime decal (PIL chalk texture on a plane shrink-wrapped to `timber_sets`).
- Day transitions are dissolves (9-12 f per the grammar). Shot 9 -> 10 is also a dissolve; the alarm is the hard cut at g 936.
- 10c: the near coal tub frames the left foreground. At the end of the out-handle (g 975-978) the cage is half cut by the right frame edge as the push continues.
- 10c: alfie's shout is a static open-mouth drawing (no lip-sync), because the quoted lines that move mouths are shots 7, 11 and 13.
