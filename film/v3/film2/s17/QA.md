# s17 QA: film 2, shot 17 (the diagram moment: rod + wire, the pulse goes quietly into the ground), tower DAY, set_rod(2)

Delivered: `take.mkv` = g 1330..1453 (124 frames, `first_g` 1330, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), no captions or audio.
Shot range [g0, g1) = [1337, 1447) (t 44.57-48.23); handles 7 frames each side (g 1330-1336, 1447-1453) rendered in 3D for the
10-frame dissolves. `meta.json`, `cues.json` (7 cues), `contact.jpg`. Script `shot.py` (+ `common.py`), `deliver.py`, `qa_cam.py`, `popcheck.py`.

## Timing
| event | g | narration |
|---|---|---|
| close on the pointed iron rod on the spire (wire visible running down the spire's west facet), drift up the rod | 1330-1364 | "ถ้ามีแท่งเหล็กปลาย" 1340-1351 |
| glint on the rod tip | 1359-1371 (peak 1362) | "แหลม" 1362 |
| eased pull-back (cubic) to the full-height side view of the tower: rod, wire down the spire, over the parapet, down the west face | 1364-1392 | "ต่อสายลงไปถึงดิน" 1376-1390 |
| camera tilts up to the rod tip in anticipation | 1395-1406 | |
| the glowing pulse leaves the rod tip and runs down the wire (core 1.6 D + glow + trail, sine-eased), camera follows it down | 1405-1430 | "ไฟฟ้าจะวิ่ง" 1406 |
| pulse sinks into the ground plate: three soft rings spread and fade, the head glow shrinks out; slow creep in | 1429-1453 | "ลงดินไป" 1425, "เงียบ ๆ" 1436 |
Framing changes: 1330, 1364-1392 (pull-back), 1395-1406 (tilt up), 1405-1432 (follow down), 1432- (creep on the plate): gaps 1.0-1.3 s.

## Camera / pops
`qa_cam.py`: min 0.27, median 13.3, peak 146 px/frame (g 1377, middle of the pull-back). Static runs: none. Constant-speed runs: none.
`popcheck.py`: median frame difference 14.5, nothing above 3x the median, no near-still transitions.
(The first final had a 833 px one-frame jump at g 1404 where the follow started; fixed by ramping the follow in from g 1395, frames 1395-1453 re-rendered.)

## Staging
No actors. Rod tip on screen: (361, 536) -> (359, 626) during the close (0.42-0.49 H), (386, 110) in the full-height view. The ground plate is below the frame in the full-height view
(the wide shows rod to the lower shaft); the camera arrives at the plate with the pulse (plate at (345, 755-800) = 0.59-0.63 H from g 1430).
Runtime changes (no set module edits): wire bevel 0.028 -> 0.07 D so it reads in the wide; `market` stall hidden (as s01). The pulse, glint and ground rings are this take's own emissive curves/spheres (camera rays only, additive glow, bloom from the grade).

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s17 all (g 1330-1453)                          32.4   18.5    0.3    1.7    0.0   46.3    0.3    0.4  0.51 0.71 0.01
```
Day exterior with much sky: red in band, blue above (the close insert is rod against the sky, as the set's DAY spire_insert measures 70 percent blue); violet and magenta in band, shade blue-violet. Few darks (0.01): a sunlit exterior with no foreground occluder (same as the set's DAY tower_side_mid, 0.04).
Seconds per frame: 7.9 s wall / 15.0 s CPU mean (2 threads, a second render running alongside).

## Differences from the plan
- tower_side_mid alone does not show rod, wire and ground in one frame; the take travels: rod close -> full-height side view -> follows the pulse down to the ground plate.
