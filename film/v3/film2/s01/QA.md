# s01 QA: film 2, shots 1-3 (the opening), tower set DAY

Delivered: `frames/g_0000.png .. g_0217.png` (218 frames, 720x1280, 12 samples, 2 threads, no captions or audio). g 0..210 = shots 1-3 ([g0, g1) = [0, 211)); g 211..217 = 7-frame out-handle (shot 3's camera continues, rendered in 3D) for the dissolve into shot 4. `meta.json`, `cues.json` (21 cues, film seconds), `contact.jpg` (16 frames, labels above the picture). Take script `shot.py`; deliverables `deliver.py`; numbers `qa.py`, `qa_cam.py`, `hue.py`. Raw renders with per-frame json: `raw/s1` (g 0-66), `raw/s2` (g 67-129), `raw/s3` (g 114-217).

## Timing (film frame g = round((t + 0.10) * 30); boundaries round(t * 30))
| event | g | s |
|---|---|---|
| shot 1 starts (open) | 0 | 0.00 |
| hammer hits (t 0.3 / 0.8 / 1.3), small camera jolt on each, rod drops one step (0.15 D) per hit | 12, 27, 42 | 0.40, 0.90, 1.40 |
| snap pull-out (16 frames, quint ease, peak g 51) up and away to the high view: he is on the very top, town below | 44-60 | 1.47-2.00 |
| hard cut to shot 2 (padre, square) | 67 | 2.23 |
| snap punch-in on padre (8 frames), lands on "ทิ้งเฉยเลย" (g 105) | 100-108 | 3.33-3.60 |
| dissolve shot 2 -> 3, 12 frames, smoothstep mix, centred on the boundary g 122 | 116-127 | 3.87-4.27 |
| shot 3 push + rise, two cubic segments, joint at "เมืองเบรชชา" (g 165) | 114-217 | |
Framing changes: g 0 (open), 44-60 (pull-out), 67 (cut), 100-108 (punch), 116-127 (dissolve), 165 (speed change of the push): gaps 1.47, 0.77, 1.1, 0.5, 1.3, then the slow push to the end (1.5 s).

## Camera (`qa_cam.py`, fastest of 9 screen points, px per frame at 720x1280)
| shot | min | median | peak | static runs (< 0.25 px) | constant-speed runs (>= 4 f) |
|---|---|---|---|---|---|
| 1 | 0.45 | 4.0 | 214 (g 51, pull-out) | none | g 18-25 (mid-segment between hits, shakes off) |
| 2 | 0.52 | 2.8 | 92 (g 104, punch) | none | none |
| 3 | 0.57 | 2.9 | 11 (g 139) | none | none |

## Staging (from `raw/*/g_*.json`)
| shot | head | width px | centre y (H) | heads below y 880 |
|---|---|---|---|---|
| 1 close (g 0-43) / after pull-out | nico | 227-267 / 54-62 | 0.46-0.48 / 0.36 | none |
| 2 | padre (main) | 181 -> 251 after the punch | 0.51-0.55 | none |
| 2 | nico (tiny on the spire tip) | 25 | 0.20-0.23 | none |
| 3 (wide, exempt) | padre, baker, woman, old | 26-31 | 0.59-0.63 | none (centres y <= 811) |
| 3 | nico on top | 22-26 | 0.06-0.14 | none |
head_flip False everywhere (key from screen-left in all three views). Nobody's back to the camera. Padre's mouth is closed (expr angry, no talk) throughout.
Pins (solve error, D): shot 1 hammer head on the rod 0.000 on every strike frame (0.11 max while raised: the raised hammer is a free pose, not a pin); left hand on the rod 0.081 max at the start (rod 3 steps high), 0.0 from g 27. Shot 2 left hand 0.30 D (nico 25 px tall-head: under 8 px on screen).
Popcheck: one pop, g 66 -> 67 = the hard cut (expected). No near-still transitions. No black/magenta cards, no retried frames.

## Colour (`hue_report.row` on the final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s01 shot 1 (g 0-66)                            32.8   13.9    1.0    4.7    0.0   44.3    2.2    1.1  0.46 0.66 0.03   OUT: orange,blue,val,dark
s01 shot 2 (g 67-121)                          18.5   13.5    0.0    0.3    0.0   63.3    3.2    1.1  0.50 0.57 0.11   OUT: red,orange,blue,sat
s01 shot 3 (g 122-210)                         27.3   27.0    0.3    1.6    0.1   42.9    0.5    0.4  0.47 0.64 0.02   OUT: red,blue,val,dark
s01 all (g 0-217)                              26.9   19.7    0.5    2.3    0.0   48.2    1.7    0.8  0.47 0.63 0.04   OUT: red,orange,blue,val,dark
ref a t0062 t0040 t0072                        23.3   15.0    1.3    0.1    0.0   51.4    3.4    5.5  0.49 0.59 0.12
```
Day exteriors: blue is above the 14-30 band in every shot (open sky); violet and magenta in band, shade reads blue-violet. What was done against it: shot 1 frames the close from above (pitch -15) so the town below, not the sky, is behind nico (blue 55 -> 44 in drafts); shot 3 is pitched down (-2 to -7) so the square fills the lower half (blue 61 -> 43). Darks: shot 2 has a stone pier at the left edge standing in the true sun shadow of an off-screen block behind the camera (dark 0.11, in band); shot 3 has a brick pier + low wall at the left edge painted shade-only (key gain 0, no cast shadow: a real shadow-caster also darkened the whole near square blue, which raised blue to 61); shot 1 has no near foreground (the camera is at the spire tip), dark 0.03. Seconds per frame: 6.32 s wall / 12.9 s CPU mean (shot 1 7.25 / 14.8, shot 2 6.07 / 12.4, shot 3 5.91 / 12.1).

## Differences from the plan / brief
- Rod: set_rod(1) throughout, but in shot 1 the rod object is lifted 0.45 D at the start and drops 0.15 D on each of the three hits (director's note: the rod is driven into the finial); from g 42 on it sits at rod_base..rod_tip. Nico's own drawn rod (prop_l of nico_hammer) is removed; his left hand guides the set rod.
- Hammer (director's note): raised high beside his cap against the sky (hammer upright), swings down on an arc onto the rod's side at z 28.68 + rod offset; arm on the front layer. The arc is limited by nico's arm reach (0.62 D x 1.3), so it is a quarter-turn swing, not an overhead one.
- Shot 1 view is from the south-east (yaw -48), not the set's spire_insert (from the south-west): the shaded side of the spire is toward camera-right, the town is behind him, key from screen-left as in shots 2 and 3. Nico kneels in front of the finial with his feet just off the cone (the spire is 0.1-0.2 D wide there); it reads as perched on the tip.
- Shot 2 is a custom low camera behind square_low (0.25, -20.3, 1.05) with padre at (1.25, -16.4) so his head sits at 0.51-0.55 H and the tower top with nico stays in frame before the punch.
- Shot 3: padre also stands in the square (continuity), extras moved a little toward the tower so their heads stay above y 880. Market stall (`market` object: striped awning read as a US flag) hidden with hide_render in shot.py (director's note).
- Nico keeps hammering in shots 2-3 (every 16 frames, tiny); cues list them as optional far clanks.
- Dissolve 2 -> 3 is mixed inside this take (both sides are mine); raw handles kept in raw/s2 (to g 129) and raw/s3 (from g 114).
- Blue share above the band and too few darks in shots 1 and 3 (see Colour).
