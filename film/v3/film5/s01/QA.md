# s01 QA: film 5, shots 1-4 (the opening), mine set (tunnel LAMP + pithead DUSK)  (re-render 1: held 2D cage in shots 1 and 3)

## Re-render 1 (client note: the bird read as outside the cage in shot 1)
Shots 1 (g 0-41) and 3 (g 81-156) were re-rendered final (12 samples, 2 threads, one process, no DOF, denoise FAST) and re-delivered; shots 2 and 4 are
untouched (same raw files). Old shot-1/3 raws kept in `work/old_raw/`. Checks: `work/d9.jpg`, `work/d10.jpg`, `work/d11.jpg`, `work/d12.jpg`, `work/f3.jpg`.
**Held-cage method (copy this):** whenever an actor holds the cage, draw it as the cast's 2D prop, not the set's 3D cage: pose
`prop_r` (or `prop_l`) = `dict(type="cage", scale=1.45)` and pose key `bird` = the canary pose (here `dict(state="perch_sing", notes=3, beak=0.7+0.2 sin, t=g/30, swing=2.5 sin)`),
with the holding arm's `hand` keyed in puppet-local D (shot 1: (0.52, 0.55) -> (0.78, -0.40) over g 0-14, screen-right; shot 3: `arm_l` (-0.74, -0.40), screen-left).
The cast draws the front bars over the bird and hangs the cage upright from the fist, so the bird is always inside the bars in his hand. Hide the set's
3D cage in those shots (`bpy.data.objects["canary_cage"].hide_render = True`) and do not show the standalone canary sprite. Scale 1.45 gives a bird head
of 65-72 px (shot 1) and 51-67 px (shot 3) at 720 px; the notes rise above the cage. Keep the 3D cage + standalone sprite only for ECUs (shot 2).
Also changed in shot 3 for the bigger cage: alfie moved 0.4 D toward screen-right (TP(10.7, -0.10)) and the camera aims 0.25 D further left, so the cage
clears the foreground tub; the point at the bird is an arm across the chest (hand (-0.38, 0.62), layer front) toward the cage.


Delivered: `frames/g_0000.png .. g_0321.png` (322 frames, 720x1280, 12 samples, 2 threads, one render process, no captions, no audio).
g 0..314 = shots 1-4 ([g0, g1) = [0, 315)); g 315..321 = 7-frame out-handle (4d camera keeps moving, rendered in 3D).
Also `meta.json` (first_g 0, n_frames 322, transitions, shot ranges incl. 4a-4d), `cues.json` (19 cues, film seconds), `contact.jpg` (16 frames,
labels above the picture), `compare.jpg` (one final frame per shot beside its ref a frame). Scripts: `shot.py`, `deliver.py`, `qa.py` (-> `work/qa.txt`),
`sheet.py`. Raw renders + per-frame json in `raw/s1..s7` (s4 = 4a to g 213, s5 = 4b from g 198 for the dissolve). Drafts: `work/d1..d8.jpg`, `work/f1.jpg`, `work/f2.jpg`.

## Client note applied (director, mid-task)
- **No depth of field anywhere**: `M.setup_dof(scene, None, None)` at build and again before every render (cage_insert / lamp_insert defaults never applied). No motion-streak blur (no whips in this take; the shot-3 punch-in is a plain 8-frame camera move).
- Denoiser: OIDN albedo+normal. ACCURATE prefilter tested against FAST on shot 1 and shot 2 at 720x1280 (`work/pf/crops.png`): no visible difference on the coal / timber texture or the canary outline, +12 CPU s per frame -> FAST kept. Without the denoiser 12 samples are visibly grainy (`s1_noden_12`), so it stays on.
- The canary insert is crisp by framing (bird head 179 -> 282 px, the whole bird ~45 % of the frame width) and lighting (keyed warm rim lamp behind the cage + key lamp), not by blur.

## Timing (captions.json, narration at +0.10 s)
| shot | g | what | ref a |
|---|---|---|---|
| 1 | 0-41 | medium, eye level: alfie (screen-left) lifts the held brass cage (cast 2D prop, bird inside, 3 notes) from his hip to beside his face (g 0-14, eased); miner1 with a flame lamp, miner2 digging, miner3 far; slow push | t0001 |
| 2 | 42-80 (cut) | ECU of the canary singing, 5 notes floating up, cage wires behind it, hanging lamp warm above, alfie's cap/face soft-edge in the left background; orbit + push, tilt with the notes | t0003 |
| 3 | 81-156 (cut) | low angle looking outbye: tub "37" foreground left, alfie holding the 2D cage up on screen-left, the bright pit bottom (exit) screen-right; point at the bird lands g 86 ("ถ้าเสียงมัน"), punch-in g 119-127 (middle g 123 = plan t 4.0), point flung at the exit lands g 135 ("ให้วิ่งทันที" 4.41 s), turns to camera g 141-147 | t0007 / t0009 |
| 4a | 157-205 (cut) | pithead DUSK high establishing: chimney + smoke, engine house, headframe + wheels, heaps, terraces, first-aid hut lit; crane down + push toward the bank | t0029-t0033 |
| 4b | 206-250 (12-f dissolve g 200-211) | tunnel eye level, faint gas haze (set_gas 2.0) in the depth, slow push inbye | |
| 4c | 251-287 (cut) | the hanging lamp (y 13.75) in the haze (2.4), drifting layers | |
| 4d | 288-314 + handle 315-321 (cut) | low under the roof lamp of set 8, haze layers under the roof (2.4), push | |
Framing changes g 0, 42, 81, 119-127, 157, 200-211, 251, 288: gaps 1.40, 1.30, 1.27, 1.00, 1.43, 1.50, 1.23, 0.9 s.
Gas drift: the haze material's position input gets a keyed offset in my scene (y -0.9 D/s, z +-0.1 sine), so the layers slide past the lamps; the set file is untouched.

## Staging (`work/qa.txt`)
| shot | head | width px | centre x | centre y (H) |
|---|---|---|---|---|
| 1 | alfie | 245 -> 276 | 217-236 | 0.51 |
| 1 | miner1 / miner2 / miner3 | 123-131 / 90-94 / 52-54 | 599-648 / 435-442 | 0.43-0.52 |
| 1 | canary inside the held cage | 65-72 | 362-416 | 0.61-0.74 |
| 2 | canary | 179 -> 282 | 291-328 | 0.47-0.55 |
| 2 | alfie (ECU background, cut by the frame) | 502-595 | 106-165 | 0.50-0.54 |
| 3 | alfie | 198 -> 262 (punch) | 389-442 | 0.44-0.46 |
| 3 | canary inside the held cage | 51-67 | 249-272 | 0.52-0.53 |
Near/far shot 1: 276 / 54 = 5.1. Shots 1 / 3: the cage is drawn in alfie's fist by the cast (no registration needed). Shot 2: 3D cage keyed at shot 1's raised position.
Mouths: alfie's never moves (shot 1 "happy" closed smile, static; shot 3 "frown"); miners closed. Nobody's back to the camera. Heads all above y 880
except alfie in the shot-2 ECU (framed through on purpose). Bird visible inside the bars in every frame of shots 1-3 (cage in alfie's hand).
Actor lamps: keyed `lamp_light` per frame: alfie's belt lamp (hip anchor), miner1's flame lamp (prop tip), shot 2 adds lamp_rim / lamp_key near the cage.
Popcheck: pops only at the cuts 41/42, 80/81, 156/157, 250/251, 287/288, plus 83->84 (3.1 levels: the fast back_out swing of the arm toward the bird, a gesture).
No black / magenta frames, no retried frames, no clipped sprites.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s01 shot 1 (g 0-41)                            12.6   32.8    1.6    0.0    0.0   34.0    9.4    9.6  0.31 0.49 0.05
s01 shot 2 (g 42-80)                            3.0   57.6   15.4    0.0    0.0   19.8    2.0    2.2  0.44 0.54 0.08
s01 shot 3 (g 81-156)                          10.7   14.8    0.3    0.0    0.0   50.7   15.0    8.5  0.34 0.43 0.06
s01 shot 4a (g 157-205)                        27.9   42.4    1.5    0.0    0.0    5.7   10.5   12.0  0.36 0.55 0.03
s01 shot 4b (g 206-250)                         5.9   12.4    0.4    0.0    0.0   63.8   14.2    3.3  0.26 0.47 0.00
s01 shot 4c (g 251-287)                         6.1   35.6    6.8    0.0    0.0   45.5    4.2    1.8  0.35 0.49 0.02
s01 shot 4d (g 288-321)                         6.0   13.0    0.3    0.0    0.0   71.8    5.5    3.3  0.36 0.42 0.02
s01 all (g 0-321)                              11.3   32.8    4.5    0.0    0.0   36.5    8.6    6.3  0.34 0.48 0.04
ref a t0001 t0003 t0007 t0009 t0031            23.8   39.1    5.4    0.2    0.1   21.8    3.3    6.3  0.26 0.55 0.05
```
Underground is blue-dominant by the set's design (LAMP night look, mine_REVIEW: tunnel finals red 11 / blue 42): red 11 and blue 36.5 are outside the
interior band, orange 33 / magenta 6.3 / val 0.48 inside. Shot 2 is the warm gold insert (orange 58, like ref t0003). 4a is the dusk exterior
(red 28, orange 42, magenta 12: the orange-pink sky). Shade reads blue, never magenta. Dark share 0.04 (band 8-15, ref 0.05).

## Seconds per frame
13.02 s wall / 26.2 s CPU mean (2 threads, denoise FAST). Per shot CPU: 1: 29.8, 2: 28.9, 3: 25.5, 4a: 20.2, 4b: 29.6, 4c: 25.9, 4d: 25.3.
Shots 1, 2, 4b are 2.5-4.6 s over 25 (five actors + four keyed lamps in 1; 2048 px/D bird sprite in 2; gas slabs in 4b), at 12 samples (not raised).

## Differences from the plan / known issues
- Cage: shots 1 / 3 use the cast's held 2D cage (see Re-render 1). Shot 2 uses the set's 3D cage (keyed where shot 1's raised hand is) with the
  canary sprite card 0.27 D in front of the cage centre (just outside the front wires) so no wire crosses the bird; the camera is level with the perch.
- Shot 2 continuity: alfie stays visible (his cap / face fill the left background) because the ring is at the frame top; no lamp bokeh (no DOF by client note).
- Shot 3: custom low camera looking outbye (not the set's tunnel_low, which looks inbye) so the exit (bright pit bottom) is on screen and the point lands on it.
- Shot 4: split 4a/4b/4c/4d for the 1.0-1.5 s rhythm; 4a uses a custom high camera (the set's pithead_wide is at 2.4 D); no actors at the pithead.
- Out-transition: 7-frame handle rendered; the conform decides cut or dissolve into shot 5.
