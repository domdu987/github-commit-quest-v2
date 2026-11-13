# s30 QA: film 7, shot 30 ("ทุกวันนี้ มีคนต่อแถวดูโมนาลิซ่าวันละหลายหมื่นคน"): louvre gallery, a huge crowd queueing for her

Delivered `take.mkv`:
- frames g 2974..3101, 128 frames, 720x1280;
- 12 samples, 2 threads, denoise FAST;
- libx264rgb crf 6, 30 fps;
- no captions, no audio.

`meta.json` gives first_g 2974, n_frames 128 and transition_in "dissolve" (from shot 29).

| g | part |
|---|---|
| 2974..2979 | 6-frame in-handle, rendered in 3D (the crane is already moving) |
| 2980..3095 | shot 30 (plan 99.33-103.20 s) |
| 3096..3101 | 6-frame out-handle, rendered in 3D |

The take is two set-ups joined by a hard cut at g 3039, just before "ละหลายหมื่นคน" (101.27 s = g 3041):

| id | g | render folder | what |
|---|---|---|---|
| 1 | 2974..3038 | `raw/s1` | Side angle from the right of the room, 32 mm, 13 D back, slow crane-in. The packed queue lane presses to the small painting, which shows clear above the hats; more people wait outside the ropes. |
| 2 | 3039..3101 | `raw/s2` | The reverse from beside her frame, 20 mm, slow crane up and back. A sea of hats and bowlers fills the Salon Carré to the far wall, every face turned up toward her (she is behind the lens). |

Also in this folder: `cues.json`, `contact.jpg` (the cyan line is y 880) and `compare.jpg`.

Scripts: `shot.py` (probe / stills / final), `deliver.py`, `qa.py` (writes `work/qa.txt`), `sheet.py`.

## Client rules
- **No depth of field.** C.Take turns DOF off at build and before every render. The crowd is sharp all the way to the far wall.
- **Period-ambiguous crowd, no phones.** Cast7 crowd folk (lady, gentleman, newsboy) plus coworker1/2, painter and plumber as extra costumes. They use the crowd_stare / crowd_point poses (with the _gentleman / _newsboy variants). Each person is turned toward her: mirror, yaw and gaze are computed from where they stand relative to the camera. Idle head moves step every 11 frames; blinks are staggered. Nobody speaks, so only static expression mouths.
- **Heads above y 880.** After posing, the script measures every person's real head (the sprite head anchor) on every frame. Anyone whose head bottom ever drops below y 875 is hidden for the whole set-up: 2 people in set-up 1, 3 in set-up 2.
  - `qa.py` finds no on-screen head below y 880.
  - A first full final broke the rule, with heads up to 42 px under the line, and was discarded. That is why the cull now uses the exact measurement.
  - The second final of set-up 1 kept the rule but looked thin and was also discarded. Its camera is now 32 mm from further back.
- **Dense set.** The salon hang covers every wall, with torchères, the coffered cove, the rope lanes and the divan. Her frame is on the hooks: she is back (set_mona True).

## Set-up notes
- The set is `louvre` empty_wall_queue. Keyed per frame: `set_mona(True)`, `set_queue(True)`, `set_flames`. `louvre.py` is untouched.
- **Crowd:** 107 actor cards in set-up 1 and 149 in set-up 2, placed at random spots with a minimum spacing.
  - Kept clear: the divan, the easel, the ladder and the 3 D around the camera.
  - Sprite resolution depends on distance from the camera: 224, 160 or 112 px per D.
- **Black patches fixed.** Dozens of stacked transparent cards ran out of transparent bounces and rendered black. `cycles.transparent_max_bounces` is now 160 (draft 1 showed the problem; fixed from draft 2 on).

## Measured (`work/qa.txt`)
- **Pops:** one, the planned cut 3038 → 3039.
- **Movement:** no near-still transitions (a framing change every frame: crane plus idle heads). Median frame change 2.1 levels.
- **Bad frames:** no magenta or black frames, none retried.
- **Seconds per frame:** 14.4 s wall / 28.6 s CPU mean.
  - side: 15.8 s / 31.3 s
  - reverse: 13.1 s / 25.7 s
  - These ran as two 2-thread processes at once for most of the render.
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s30 all                                        44.1   46.8    2.6    0.3    0.0    2.4    0.8    3.0  0.38 0.56 0.05
ref a t0040 t0046 t0051                        40.7   38.0    2.8    0.3    0.0    9.8    4.3    4.1  0.41 0.46 0.13
```
Warm gallery daylight, as `louvre_API.md` measures for this set. Magenta is 3.0. Not graded.

## Differences from the plan
- The plan's "empty_wall_queue" preset is used as the build, but the painting hangs on the wall and the queue is for her (today), not for the empty hooks.
- The take is two set-ups with a hard cut inside it, to get a framing change roughly every 2 s.
- The crowd faces the camera, turned toward her by yaw and gaze, because a 2D card cannot show its back.
