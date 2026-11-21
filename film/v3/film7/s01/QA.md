# s01 QA: film 7, shot 1 (the hook): louvre exit_door -> paris street

Delivered: `frames/g_0000.png .. g_0078.png` (79 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 0, 79 frames). g 0..71 = shot 1 ([g0, g1) = [0, 72), plan 0.00-2.40 s); g 72..78 = 7-frame
out-handle (walk + camera track continue, rendered in 3D). Shot 2 is NOT in this take.
Two set-ups inside the shot, joined by a hard cut at g 40 (1.33 s), just before "ออกจาก" (1.48 s):
id 1 = corridor g 0..39 (`raw/s1`), id 2 = street g 40..78 (`raw/s2`).
Also `meta.json` (first_g 0, n_frames 79, events, set-ups), `cues.json` (17 cues, film seconds), `contact.jpg` (16 frames, cyan line =
y 880), `compare.jpg` (g 20 beside ref a t0055: figure before a bright archway; g 64 beside ref a t0085: hero walking toward the lens).
Scripts: `shot.py` (probe / stills / final), `deliver.py`, `qa.py` (-> `work/qa.txt`), `sheet.py`; shared helpers in `../common.py`
(gotchas at its top). Drafts `work/d1..d6(.jpg)`; first full final `work/old_raw/raw1` rejected by eye (see "Fixed after looking").

## Client rules
- **No depth of field anywhere**: `cam.data.dof.use_dof = False` and `L.setup_dof(scene, None, None, cam=cam)` at build and before every
  render (common.Take); louvre never sets DOF. Everything is sharp: the fanlight bars, the smocks, Notre-Dame's rose at the street's end.
- **Dense set**: corridor: the set's door, fanlight, gas brackets, lead pipes, plus runtime dressing in `shot.py dress_corridor()` (louvre
  helpers + materials; the set module is untouched): a peg rail with 3 white smocks and caps, the glazier's crates with leaning panes and a
  lit storm lantern, opera / cirque posters, a key board, ladder, broom, toolbox, putty tin, bucket, sack. Street: Haussmann facades with shop
  signs (LIBRAIRIE, PARFUMS...), balconies, gas lamps, trees, the fiacre, the kiosk edge, Notre-Dame at the end.
- **Heads above the caption band**: corridor head centre y 701-725 (0.55-0.57 H), bottom <= 827; street 568-596 (0.44-0.47 H), bottom
  <= 725. Nothing but floor / cobbles and his legs below y 880.
- **Mouths only on quoted lines**: shot 1 has no quote -> no lip-sync. Static expression mouths only (worried -> grinning, the change behind
  the blink at g 12 and g 56).

## Timing (captions.json, narration at +0.10 s)
| g | what | caption |
|---|---|---|
| 0-14 | the service door swings open 28 -> 92 deg, courtyard daylight floods in; vincenzo (smock, bulge, sweat) watches it | "ชายคนนี้เดิน" (0.06) |
| 10-16 | turns to the lens (yaw 0.62 -> 0.10), expression to the nervous grin behind the blink | |
| 16-30 | stiff nervous grin at us, both hands pressing the bulge flat; gulp 22-26 | "ถือโมนาลิซ่า" 0.75 s = g 26 |
| 30-39 | eases into a walk toward the bright doorway (screen-left), glancing back at us | |
| 40 | CUT to the street | "ออกจาก" 1.48 s = g 47 |
| 40-56 | walks toward us down the rue in the sun, eyes darting left (40-48) and right (49-55), worried | "พิพิธภัณฑ์" 1.83 s = g 58 |
| 57-78 | the nervous grin into the lens, hand on the bulge (handle 72-78) | "โดยไม่มีใคร" 2.52 s starts in shot 2 |
Camera: corridor = one slow push (0.8 D, sine, 20 mm, eye level z 2.45); street = a tracking camera backing up 0.052 D/frame while he
walks 0.067 D/frame toward it (slow push in, 22 mm, head 218 -> 258 px). Framing changes: g 0 / g 40 (1.33 s, 1.07 s + handle).

## Staging (`work/qa.txt`)
| set-up | head width px | centre x | centre y (H) |
|---|---|---|---|
| corridor (g 0-39) | 169 -> 204 | 438-488 | 0.55-0.57 |
| street (g 40-78) | 218 -> 258 | 319-361 | 0.44-0.47 |
Vincenzo's walk cycles: `cast7.cycle("vincenzo_smock", ..., arms="l")` with arm_r pinned on the bulge (as `vincenzo_smug_walk`);
corridor facing -1 (mirror, matches the standing poses), street facing +1 at yaw 0.22 (reads as walking toward the lens).
Popcheck: one jump, the planned cut 39 -> 40 (58 levels); g 29 -> 30 (6.9 vs median 6.2) is the stand -> walk start + the blink ending,
eased (see below). No near-still pairs, no black / magenta frames, no retried frames, no clipped sprites.

## Fixed after looking at full size
- The first final's wall notice left of the door was louvre's `M['news'][0]` = a Mona Lisa front page "LA JOCONDE VOLÉE !" (theft not yet
  known): replaced by the opera poster. (common.py gotcha.)
- Street: a kerb gas lamp sat at the top-left edge as a blown yellow blob: vincenzo moved mid-road (x -1.0), camera x -0.4.
- Stand -> walk at g 30 popped (stride, the swinging hand vanished behind the body, lean): speed / stride / lift eased over 6 frames,
  the left hand blends off the bulge and stays in the front layer, lean blended (frames 30-36 re-rendered).
- Corridor camera moved off the bench (the preset camera x 1.5..2.05 put the bench top as a brown slab across the lower right); the
  fanlight shaft sheet hidden (it washed the left half).

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s01 corridor (g 0-39)                          12.8   84.0    0.9    0.0    0.0    0.3    0.4    1.5  0.26 0.56 0.04
s01 street (g 40-71)                           28.5   28.7    2.2    0.3    0.1   27.8    9.9    2.6  0.31 0.54 0.09
s01 all (g 0-78)                               21.0   55.0    1.7    0.1    0.1   14.8    5.3    2.1  0.29 0.55 0.07
ref a t0055 t0056 (gate, day)                  16.5   71.7    1.4    1.5    0.2    7.7    0.7    0.4  0.30 0.68 0.01
ref a t0085 t0086 (walk to cam)                 0.9    1.1    0.0    0.0    0.0   82.0   11.1    4.9  0.55 0.61 0.03
```
Corridor is the warm stone + daylight of the set (close to ref a t0055's sunlit stone gate: orange 84 / 72, sat 0.26 / 0.30). Street is
half shade (blue 28) with the golden sun, magenta 2.6. Saturation 0.29 is under the ref's daylight frames, as louvre_API 7 measures for
every preset; not graded here (same for every shot of the set; do it in the conform if wanted).

## Seconds per frame
11.67 s wall / 22.9 s CPU mean (2 threads, two render processes at once on 4 cores, denoise FAST, 12 samples): corridor 10.8 s wall /
21.3 s CPU, street 12.5 s / 24.5 s. Vincenzo sprite 320 px/D.

## Differences from the plan / known issues
- "exit_door -> paris street" done as two set-ups with a hard cut on the caption (no dissolve inside the shot).
- The paris set has no Louvre façade: the street is the rue outside (Notre-Dame at its end, as in `street_wide`). Papers keyed 0.
- In the corridor he walks off away from us (a 2D card cannot turn its back), so the "walks out" beat is the street half, toward the lens.
- SET BUG for other shots: the corridor's own framed notices on the left wall (y 1.0-2.2, behind this camera) use `M['news'][2]`, `[3]` =
  "LE VOL DU LOUVRE" and "MYSTÈRE AU LOUVRE" front pages (louvre_tex.py l. 762: all four news textures are theft headlines). Any exit_door
  shot that sees that wall (shots 14-15, before the theft is known) must cover or replace them at runtime, or the set owner should fix it.
