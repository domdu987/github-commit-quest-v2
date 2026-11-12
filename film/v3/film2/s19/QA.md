# s19 QA: film 2, shot 19 (the empty finial in the rain), tower set NIGHT_STORM

Delivered: `take.mkv` = g 1578..1659 (82 frames, `first_g` 1578, 720x1280, 12 samples, 2 threads, libx264rgb crf 6). g 1585..1659 = shot 19 ([g0, g1) = [1585, 1660)); g 1578..1584 = in-handle (7 frames = 10/2 + 2, rendered in 3D, the push continues backward) for the 10-frame dissolve from shot 18. Out: hard cut to s20 (no handle). `meta.json`, `cues.json`, `contact.jpg` (16 frames, labels above the picture). Script `shot.py`; shared helpers of my three takes `fx.py` (rain, flash card, resumable render loop, contact, encode). Raw frames + per-frame json in `raw/s19` (not in git).

## Timing (g = round((t + 0.10) * 30); boundaries round(t * 30))
| event | g | s |
|---|---|---|
| in-handle (dissolve from s18, centred on 1585) | 1578-1584 | 52.60 |
| shot 19 starts ("และคืนนั้น") | 1585 | 52.83 |
| far flicker in the clouds (sky bolt, set flash 0.3 / 0.08 / 0.22), thunder cue | 1607-1609 | 53.57 |
| push quickens and tilts up onto the empty spike, "ไม่มีไม้จิ้มฟ้าแล้ว" (quint segment 1625 -> 1639) | 1625-1639 | 54.17-54.63 |
| last frame (hard cut to the strike) | 1659 | 55.30 |
Framing changes: 1578 (slow push, sine), 1607 (flicker), 1625-1639 (quickened push + tilt up), then slow push to the cut: gaps 1.0, 0.6, 0.7 s.

## Camera / motion
Custom spherical push around the finial (dist 3.4 -> 1.75 D, yaw 43 -> 52 deg, pitch 4 -> 11 deg, look z 27.85 -> 28.40) with a 15 percent constant-speed share (never parks) and a slow +-1.2 deg sway roll. Never static: mean abs difference of consecutive frames 7.1 to 20.5 (8-bit, 90x160; rain moves every frame anyway); the camera itself moves every frame (no hold key before the end).
Staging: no actors (exempt from head rules). set_rod(0) throughout: no rod, no wire. The copper spike sits at 0.38-0.52 H.

## Colour (`fx.hue_rows`, hue_report.row)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s19 shot 19 (g 1578-1659)                       0.0    0.1    0.1    0.0    0.0   99.6    0.3    0.0  0.62 0.41 0.00
```
Night storm: blue-dominant as expected for NIGHT_STORM (the set's own stills measure 97.4 blue), no magenta (0.0), violet 0.3; shade reads blue-violet. Dark share 0.00: the storm sky and the plate are mid-blue, the night preset has no deep blacks (as the set REVIEW notes). The warm windows of the town are the only warm accents.

Seconds per frame (final): 6.55 s wall, 13.26 s CPU mean.

## Differences from the plan
- None in content. Rain is our own runtime addition (fx.Rain: ~650 camera-facing emissive streaks, camera rays only, deterministic in g) because the set has no rain.
