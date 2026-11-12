# s18 QA: film 2, shot 18 (without a rod: through stone, wood, the wet rope), tower NIGHT_STORM, inside the bell chamber

Delivered: `take.mkv` = g 1440..1591 (152 frames, `first_g` 1440, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), no captions or audio.
Shot range [g0, g1) = [1447, 1585) (t 48.23-52.84); handles 7 frames each side (g 1440-1446, 1585-1591) rendered in 3D for the
10-frame dissolves. `meta.json`, `cues.json` (12 cues), `contact.jpg`. Script `shot.py` (+ `common.py`), `deliver.py`, `qa_cam.py`, `popcheck.py`.

## Timing (beats from script/captions.json)
| event | g | narration |
|---|---|---|
| the dark chamber from just outside the south arch: bell, rope with its striped sally, rain beyond the north and east arches, drops sliding down the rope and falling | 1440- | "แต่ถ้าไม่มี" 1450 |
| flash outside (1, .15, .45 x flash_e) | 1462-1465 | |
| faint intermittent crackle on the wall above the north arch; camera pushes and tilts up toward it | 1470-1500 | "มันจะหาทางลงเอง" 1470 |
| STONE: snap (6 f) onto the north arch; a jagged glow crawls down the wall and along the voussoir ring with three forks; point light rides it | 1494-1500 snap, 1501-1516 crawl | "ผ่านหิน" 1505 |
| WOOD: snap onto the bell frame from below; the glow climbs the frame post, runs under the frame beam, over the bearing, along the headstock, under the rope lever | 1517-1523 snap, 1521-1537 run | "ผ่านไม้" 1523 |
| ROPE: snap onto the rope top from the east arch; the glow runs down the wet rope through the sally to the end, camera tilts down with it | 1537-1543 snap, 1542-1560 run | "ผ่านเชือก" 1543 |
| the drops on the rope flare white as they slide and fall to the planks; embers on stone, wood and rope fade (14-frame decay) | 1548-1591 | "ระฆังที่เปียกฝน" 1554-1584 |
Framing changes: 1440 creep, 1466-1494 push, 1500 / 1523 / 1543 snaps (each with a small jolt on the beat), 1547-1565 tilt down the rope, 1565- creep: gaps 0.6-1.3 s.

## Camera / pops
`qa_cam.py`: min 0.37, median 8.7, peak 536 px/frame (g 1540, the 6-frame snap from the frame beam to the rope across the chamber; the other snaps are smaller). Static runs: none. Constant-speed runs: none.
(The first final had g 1440-1465 static (a duplicated key); fixed with a slightly wider first key, those 26 frames re-rendered.)
`popcheck.py`: median 5.6; spikes only at 1541 (rope snap) and 1549-1562 (the glow running down the rope close to camera, flaring drops). No near-still transitions.

## Staging
No actors (plan: close on the bell rope). Bell at 0 degrees (still), rope and sally as the set builds them. On screen (720x1280): sally (392, 902) -> (455, 1134) in the opening, (360, 859) -> (360, 390) during the tilt down the rope at the end (centred).
This take's own objects (no set edits): glow path in three curves (stone jagged on the north wall inner face and the voussoir ring, wood on the post / beam / headstock / lever faces the cameras see, rope coaxial with the rope), core + additive glow + ember, forks, a moving point light (0.72, 0.8, 1.0; 6 W, the only extra light, it lights the stone and the ceiling planks around the head), rain streaks (two camera-only additive meshes beyond the north and east arches, moving down 0.95-1 D per frame), five drops on the rope. `market` stall hidden (as s01).

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s18 all (g 1440-1591)                           0.0    0.2    0.1    0.0    0.0   95.3    0.7    3.7  0.56 0.35 0.18
```
Night storm interior: blue-dominant (expected for NIGHT_STORM); magenta 3.7 (the bronze bell in moonlight, under the 10 percent limit), violet 0.7, shade blue-violet. Darks 0.18 (a night interior).
Seconds per frame: 10.8 s wall / 21.3 s CPU mean (2 threads; part of it alongside a second render).

## Differences from the plan
- "chamber_eye close on the rope": opens on the chamber_eye side (from just outside the south arch) and then uses three custom set-ups inside the chamber (north arch from the south-east corner, the bell frame from below, the rope from the east arch), one per beat, because no single view shows stone, wood and rope; the bell hides the rope's top from chamber_eye.
- The stone beat is the wall above the north arch and its voussoir ring (the chamber's ceiling beams hide the wall top from below).
- Nobody is in the chamber (the plan names no actors for this shot).
