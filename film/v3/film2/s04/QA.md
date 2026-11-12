# s04 QA: film 2, shots 4-5, tower set NIGHT_STORM

Delivered: `take.mkv` (frames g 204..366, 163 frames, `first_g` 204, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), `meta.json`, `cues.json`, `contact.jpg` (16 frames, labels above the picture). Take script `shot.py`; delivery `deliver.py`; shared helpers `tk.py` (also used by s06 and s07). Raw renders with per-frame json (gitignored): `raw/s4` (g 204-311), `raw/s5` (g 298-366). Full numbers: `work/qa.txt` (gitignored, reproduced below).

## Timing (g = round((t + 0.10) * 30); boundaries round(t * 30))
| event | g | s |
|---|---|---|
| in-handle: whip pan still fast (streaked 68 -> 20 px) | 204-210 | 6.80-7.00 |
| shot 4 starts (s01 delivered g1 = 211; plan 7.01 s = g 210) | 211 | 7.03 |
| whip brakes into the chamber (ease from 75 deg, power 2.2) | 211-219 | |
| lightning flashes through the north arch (bolt on the first frames) | 232, 258, 281 | 7.73, 8.60, 9.37 |
| snap punch-in on padre (8 f, quint), lands on "ต้องตีระฆังรัว ๆ" (g 274) | 268-276 | 8.93-9.20 |
| dissolve 4 -> 5, 10 frames, smoothstep, mixed here | 300-309 | 10.00-10.30 |
| shot 5 sky bolts (far over the hills, left / right / left of the tower) | 312, 339 ("ฟ้าผ่าไปเอง" g 340), 352 | |
| out-handle (shot 5 camera continues) for the 12-frame dissolve into shot 6 | 359-366 | |
Framing changes: 211-219 (whip lands), drift, 268-276 (punch), 300-309 (dissolve), 340 (speed change of the push + bolt jolt): gaps 1.6, 1.0, 1.3, 1.0 s, then the eased push to 366.
Bell: `set_bell` 26 deg x sin, 40-frame cycle (strike at each end of the swing: g 210, 230, ...); each ringer hauls once per half cycle with his own phase.

## Camera (fastest of 9 screen points at 8 D, px per frame)
| shot | min | median | peak | static runs | constant-speed runs (>= 4 f) |
|---|---|---|---|---|---|
| 4 | 0.48 | 2.9 | 200 (g 204, whip handle) | none | none |
| 5 | 1.33 | 6.9 | 28 (g 352, thunder jolt) | none | none |
Whip frames g 204-213 and the punch g 271-272 carry a horizontal streak (box blur 0.5 x pan speed, frames with pan > 40 px/frame).

## Staging (from raw/*/g_*.json, on-screen frames g >= 214)
| shot | head | width px | centre y (H) | notes |
|---|---|---|---|---|
| 4 | padre (main) | 220 -> 300 after the punch | 0.45-0.52 | near, screen-left |
| 4 | baker | 200-290 | 0.51-0.57 | right; pushed half out of frame by the punch |
| 4 | woman | 145-190 | 0.53-0.63 | far, between them |
| 5 | (wide, no actors) | | | |
No head bottom below y 880 on screen. head_flip False (moon key from screen-left). Mouths: clenched (padre) / story-pose mouths, held, no talking.
Ropes: three 3D ropes with striped sallies hang from the ceiling 0.10 D behind each card and move with the haul (0.36 D); both hands pinned on them: solve error 0.000-0.034 D on every on-screen frame (the large errors in work/qa.txt are whip-handle frames where the cards are off-screen behind the wall).
Popcheck: jumps only at lightning flashes (311->312, 314->315, 338->339): intended. No black / magenta cards, no retried frames.

## Colour (`tk.qa_text` -> hue_report.row on the final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s04 shot 4 (g 204-304)                          1.4    1.2    0.0    0.6    1.6   85.4    4.0    5.9  0.46 0.39 0.23
s04 shot 5 (g 305-366)                          0.0    0.3    0.9    0.0    0.0   98.3    0.3    0.2  0.60 0.42 0.00
s04 all (g 204-366)                             0.7    0.7    0.4    0.3    0.9   91.5    2.3    3.2  0.52 0.40 0.15
```
NIGHT_STORM: blue-dominant by design (set review: 97 % blue), magenta 0.2-5.9 % (under 10), shade blue-violet. Shot 5 has few darks (moonlit cobbles fill the lower half), as in the set's town_wide still.
Seconds per frame: shot 4 13.9 s wall / 26.6 s CPU (three sprites, chamber interior; partly with 3 processes on the machine during drafts), shot 5 8.2 / 15.1.

## Differences from the plan
- Shot 4 starts at g 211 (s01's g1) instead of 210, so the takes butt; the whip in-handle g 204-210 is extra (cut or use as the conform wants).
- Rod: set_rod(0) in both shots (the old belief, before the boy's rod); the plan does not say.
- Bolts in shot 5 use the set's `bolt_sky`, moved per flash at runtime (shot.py) so they fall far left/right of the tower, never on it.
- The market stall is hidden (as in s01).
