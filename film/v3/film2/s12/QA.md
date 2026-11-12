# s12 QA: film 2, shots 12-13 (the storm night), tower set NIGHT_STORM

Delivered: `take.mkv` = frames g 877..1033 (157 frames, first_g 877, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), `meta.json`,
`cues.json`, `contact.jpg` (16 frames, labels above the picture). Take script `shot.py` (`probe` / `stills` / `final`), delivery
`deliver.py` (+ shared `deliver_lib.py`, also used by s14 and s15), numbers in `work/qa.txt` (not in git). Raw renders with per-frame json:
`raw/s12` (g 877-965), `raw/s13` (g 952-1033) (not in git).

## Timing (g = round((t + 0.10) * 30); boundaries round(t * 30))
| event | g |
|---|---|
| in-handle (9-frame dissolve from shot 11), rendered in 3D | 877-882 |
| shot 12 starts: high angle on the four ringers, bell swinging +-36 deg, period 34 f; ropes hauled on the back-swing | 883 |
| lightning flashes outside the arches | 896-900, 944-946 |
| snap reframe onto nico (lifted off his feet by his rope), lands on "ระฆังกันรัว ๆ" (937) | 930-938 |
| dissolve 12 -> 13, 10 frames, smoothstep, centred on 959 | 954-963 |
| shot 13: town_wide in rain, flashes light the clouds | 961-963, 978-983, 1004-1006, 1019-1023 |
| far forked bolts over the hills (right / left of the tower, never the tower) | 978-981, 1019-1021 |
| eased reframe up to the tower top with the rod, on "แต่ไม่ผ่า" (995) | 989-999 |
| out-handle (12-frame dissolve into shot 14) | 1026-1033 |
Framing changes: 877 (move), 930-938, 954-963, ~975 (speed change), 989-999, 1026: gaps 1.0-1.8 s; the camera never parks.

## Camera (fastest of 9 screen points, px/frame at 720x1280)
| shot | min | median | peak | static runs | constant-speed runs (>= 4 f) |
|---|---|---|---|---|---|
| 12 (ref depth 4 D) | 0.39 | 2.3 | 89 (g 934, snap) | none | none |
| 13 (ref depth 30 D) | 0.29 | 1.7 | 325 (g 994, the snap up to the tower top) | none | 967-973, 1013-1018 (6 f each) |
Shot 12 also carries a tiny vertical jolt at twice the bell rate (the ringing shakes the chamber).

## Staging (raw json, shot 12, g 883-958)
| head | width px | centre y (H) | below y 880 |
|---|---|---|---|
| nico (main) | 190-285 | 0.41-0.47 | none |
| padre (near right) | 214-316 | 0.41-0.44 | none |
| woman (back right) | 150-195 | 0.33-0.38 | none |
| baker (back left) | 141-188 | 0.29-0.35 | none |
Shot 13: no actors (everyone is in the bell chamber). head_flip True in shot 12 (camera looks +x, moon key from screen-right). Nobody's back to the camera; mouths closed (determined / clench), no lip movement. Popcheck: one pop 977 -> 978 = the lightning flash (intended). No black or magenta cards, no retried frames.

## Colour (hue_report rows of the delivered frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s12 shot 12 (g 883-958)                         3.3    8.2    0.1    0.4    0.3   77.7    3.2    6.9  0.43 0.46 0.07
s12 shot 13 (g 959-1025)                        0.1    0.2    0.5    0.0    0.0   98.3    0.6    0.4  0.57 0.44 0.00
s12 all (g 877-1033)                            1.5    3.9    0.3    0.2    0.1   88.8    1.8    3.4  0.50 0.45 0.04
ref a t0080 t0096                               9.8   54.6    3.9    0.0    0.1   21.9    5.1    4.6  0.41 0.68 0.04
```
Night storm: blue-dominant as the brief expects for NIGHT_STORM; magenta 6.9 / 0.4 (under 10), shade reads blue-violet. Shot 12 keeps warm accents (nico's tunic, ropes, the lantern, warm windows below). Seconds per frame: shot 12 19.9 s wall / 37.1 s CPU (rain streaks + chamber interior; two renders shared 4 cores), shot 13 9.7 / 18.6.

## Differences from the plan
- Shot 12 "chamber_eye (high angle)": custom camera hanging just outside the WEST arch, 4 D above the floor, looking in and down (pitch about -35): the bell swings across the frame (its axis is x, so it never swings into the lens), the rain falls in front of the arch and down the shaft below. Ringers: padre near right, nico near left (main), baker and woman behind. Four ringers but the set has two ropes: each puppet draws its own rope (bell_rope prop) on a canvas raised 3 D so the rope runs out of the top of frame.
- Rain is our own geometry (in shot.py): thin crossed emissive streaks (camera rays only), a 6 D periodic column moved down every frame (shot 12: 0.95 D/f, shot 13: 1.4 D/f); a clear zone around the shot-12 and shot-13 camera paths so no streak crosses the lens.
- Shot 13 bolts: the set's sky bolt lines up behind the tower from town_wide (it read as a strike), so two of our own forked bolts strike the far hills 15-20 deg either side of the view axis; the set's bolts are hidden.
- Shot 13 rod: the set rod (0.035 D radius, dark iron) vanished against the night sky, so it is hidden and a 2.2x thicker copy with a faint moonlit emission (0.95) stands in its place (same rod_base..rod_tip).
- Market stall hidden (director's note from s01).
- Darks low in shot 13 (0.00): the night wide is mid-blue everywhere, no foreground mass.
