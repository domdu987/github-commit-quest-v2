# s15 QA: film 3, shot 15 (the diagram: water test vs molasses), harbor set WARM

Delivered: `take.mkv` = g 1323..1468 (146 frames, first_g 1323), 720x1280, 12 samples, 2 threads, no captions or audio.
g 1330..1461 = shot 15 ([g0, g1) = [1330, 1462)); in-handle g 1323..1329 and out-handle g 1462..1468 (10-frame dissolves both
sides, rendered in 3D). `meta.json`, `cues.json`, `contact.jpg`. Scripts: `shot.py`, `lib3.py` (shared), `deliver.py`.

## Timing
| event | g | s (film) |
|---|---|---|
| shot 15 starts ("ถังใหม่ต้อง") | 1330 | 44.33 |
| the tank shell turns x-ray (opacity 1 -> 0.32) | 1328..1342 | 44.27..44.73 |
| blue water test fills the tank ("เติมน้ำดูก่อนว่ารั่วไหม") | 1340..1384 | 44.67..46.13 |
| hold, ripples | 1384..1398 | |
| blue ghost fades away ("แต่บริษัทรีบ") | 1398..1410 | 46.60..47.00 |
| molasses pours from the pipe inlet at the rim ("เลยเทกากน้ำตาล") | 1404.. | 46.80 |
| brown level climbs | 1408..1468 | 46.93..48.93 |
Camera: slow push and orbit in four eased segments (speed changes g 1361, 1398, 1430), 30 % constant-speed share.

## Picture
- Custom elevated three-quarter view of the whole tank from the yard end of Commercial Street (1.2, -15, 8) -> (4, -7.6, 10.4).
- X-ray: runtime copies of the tank shell / patch materials mixed with Transparent (factor keyed per frame), so the inside
  shows: the far wall, the roof cone and the harbour behind. The tank's ink hull is off for the whole take.
- Ghost volumes (emission, translucent): blue water (alpha 0.5) with a pale top and a white water line; brown molasses
  (alpha 0.86, fades in over 7 frames) with an orange top and a white line; a thick brown stream from the filling pipe's inlet
  at the rim down to the brown surface.
- No actors (diagram); no mouths.

## Checks
Popcheck: no pops (first final had two: ink switch at g 1335 -> 1336 and the molasses volume appearing at 1409 -> 1410; fixed,
frames 1323-1336 and 1405-1418 re-rendered). No near-still transitions. No black/magenta cards, no retried frames.
Render: 13.8 s wall / 27.1 s CPU per frame (mean; two render processes running). Transparent mixing leaves a light grain on
the ghost shell at 12 samples (visible only at full size).

## Colour (`hue_report.row` on the final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s15 shot 15 (g 1330-1461)                      21.7   10.3    0.0    0.1    0.0   63.7    3.1    1.0  0.37 0.60 0.03
ref b t0010 t0030 (exteriors)                   8.6    3.4    0.0    0.0    0.0   77.4    3.4    7.2  0.46 0.66 0.08
```
Blue-heavy by design (sky seen through the x-ray tank, then the blue water ghost); red returns as the molasses rises. Violet
and magenta in band. Dark 0.03: an open, bright diagram frame (the shaded stable / warehouse corner at the right edge are the
darkest masses).

## Differences from the plan
- Camera: the plan's "high_down / insert" looks from the tank roof down onto the street and cannot show the tank filling; a
  custom elevated three-quarter view of the whole tank is used instead.
- The diagram is done as an x-ray of the real tank (translucent shell + ghost volumes) rather than a separate ghost tank.
