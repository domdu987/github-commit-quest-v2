# s22 QA: film 2, shot 22 (the ending: the rod beside the bed), room set DAWN

Delivered: `take.mkv` = g 1835..1967 (133 frames, `first_g` 1835, 720x1280, 12 samples, 2 threads, libx264rgb crf 6). g 1844..1967 = shot 22 ([g0, g1) = [1844, 1968), the last frame of the film is g 1967); g 1835..1843 = in-handle (9 frames = 15/2 + 2, rendered in 3D, the push continues backward) for the 15-frame dissolve from s20. `meta.json`, `cues.json`, `contact.jpg` (16 frames). Script `shot.py` (uses `../s19/fx.py`). Raw frames in `raw/s22` (not in git).

## Timing / camera
Quiet attic, dawn light patch on the floor; slow push from the push_rod side to the iron rod leaning beside the bed, held to the end of the film. Three eased segments with a 25 percent constant-speed share (never parks; the last key is past the end of the film, so the camera still creeps at g 1967) and a slow +-0.6 deg roll:
| segment | g | word |
|---|---|---|
| 1 | 1835 -> 1880 | dissolve in; "ส่วนไม้จิ้มฟ้าของเขา" 61.48 |
| 2 | 1880 -> 1914 | "ยังพิงอยู่" (g 1880) |
| 3 | 1914 -> 1968 | "ตรงที่เขาวางไว้" (g 1914), slow creep to the end |
Framing changes: 1844 (dissolve), 1880, 1914, then a slow creep to the end (1.8 s; the end of the film is a hold, as the plan asks). Mean abs difference of consecutive frames 0.17-1.94 (8-bit, 90x160): never static.
No actors (exempt from head rules). The rod sits at 0.45-0.62 W, its foot at about 0.6-0.8 H.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s22 shot 22 (g 1835-1967)                      44.3   36.1    0.0    0.0    0.0   16.6    0.2    2.8  0.54 0.44 0.03   OUT: red,sat,val,dark
```
Orange, blue, violet and magenta in band; red 44.3 (band 30-41), saturation 0.54, value 0.44 and dark 0.03 just outside. The floor's shade reads blue-violet, no magenta. A first final pass framed higher (more roof boards: red 54.5, blue 10.7) and was re-rendered lower so the blue-violet floor fills the bottom half (raw of that pass kept locally in work/raw_v1, not delivered).

Seconds per frame (final, 2 threads): 8.40 s wall, 16.48 s CPU mean.

## Differences from the plan
- None in content. The window itself is outside the frame; the dawn reads through the light patch on the floor (the set's push_rod camera shows the same).
