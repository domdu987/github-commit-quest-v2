# s14 QA: film 7, shots 14-15 (the locked door and the friendly plumber): louvre exit_door

Delivered: `frames/g_1330.png .. g_1541.png` (212 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions / audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 1330, 212 frames). Plan bounds g 1336..1535 (44.53-51.19 s); 6-frame handles in 3D on both
ends (g 1330..1335: the first tug under way; g 1536..1541: the door wide open, plumber still waving). Shot 14 = g 1336..1433, shot 15 =
g 1434..1535. `transition_in` cut. One location: `raw/s1`.
Also `meta.json`, `cues.json`, `contact.jpg` (16 frames, cyan line y 880), `compare.jpg` (g 1400 beside ref a t0005; g 1520 beside ref a
t0013). Scripts: `shot.py`, `deliver.py` (-> `work/qa.txt`); helpers `../common.py`; the corridor dressing is s01's `dress_corridor()`,
imported read-only from `../s01/shot.py`. Drafts `work/d1..d3.jpg`.

## Set-ups (framing change every 1.0-1.8 s)
| g | set-up | what | caption |
|---|---|---|---|
| 1330-1380 | C1 medium wide, slow push, 22 mm | vincenzo (smock, bulge, sweat) yanks the locked door: right hand pinned on the lock (the knob is missing), three hard tugs 1340 / 1352 / 1364, the door rattles 0-0.9 deg in its frame | "แต่ประตูทางออกล็อกอยู่" 44.50 |
| 1381-1433 | C2 CUT close 3/4, 26-27 mm, sprites 512 px/D | the sweat pours (0.6 -> 1, pale), a weak last tug 1398, a gulp 1410-1417, steps behind him: eyes flick right 1422 | "เขายืนเหงื่อแตก" 46.01 |
| 1434-1464 | C3 CUT wide, 20 mm | the plumber walks in from screen-right to the door (cycle), vincenzo backs off to the left with a stiff grin; key into the lock 1458 | "จนช่างประปาคนหนึ่งเดินผ่านมา" |
| 1465-1494 | C4 CUT insert (ECU from the left), 27-28 mm, 512 px/D | the key (tip pinned in the lock) turns 180 -> 90 deg 1463-1475, then he pulls: the door starts to swing 1484 (key still in the lock, following it) | "ช่วยไขประตูให้" 48.81 s = g 1467 |
| 1495-1541 | C5 CUT medium two-shot, 22 mm | the door swings wide (-> 92 deg by 1520) on the bright courtyard; the plumber greets him with a big closed smile and a wave; vincenzo's frozen nervous grin, a stiff nod back | "แถมยิ้มทักอีกต่างหาก" 49.69 / 50.35 |

## Client rules
- **No depth of field**: common.Take. All sharp.
- **Mouths**: no quoted line in shots 14-15: static expression mouths only. The cast's `plumber_greet` has `mouth="talk_a"`: dropped (closed
  "happy" smile), as in `plumber_open_door`.
- **Heads** (`work/qa.txt`): vincenzo C1 0.56-0.57 H, C2 0.51, C3 0.55-0.57, C5 0.57-0.58; plumber C3 0.53-0.54, C4 0.44-0.47, C5 0.53. No
  visible head bottom below y 880. (qa.txt also lists a "pl" head in C1 at x -41..77 below 880: that is the plumber waiting BEHIND the C1
  camera, projected through the lens plane; he is not in those frames, checked at full size g 1360 / 1378.)
- **Theft headlines covered**: the corridor's own framed notices (`corridor_notice_0/1`, louvre news[2] / news[3] "LE VOL DU LOUVRE" /
  "MYSTÈRE AU LOUVRE") are re-textured at runtime with the neutral posters choc / opera (`neutral_notices()`); s01's dressing notices are
  opera / cirque. No Mona Lisa front page anywhere in the take.
- **Dense set**: s01's glazier's corner (smock rail + caps, crates + panes, lit storm lantern, notices, key board, ladder, broom, toolbox,
  bucket, sack) + the set's pipes, gas brackets, bench. The fanlight shaft sheet is hidden (as s01).

## Checks
Popcheck: jumps only at the four planned cuts (1381, 1434, 1465, 1495) + 1396 -> 1397 (9.0, the weak tug's rattle). First final had a pose
snap inside the insert at 1486 -> 1487 (the plumber let go of the key and jumped into the wave): retimed so the key stays in the lock while
the door starts to open and the greeting begins exactly on the 1495 cut (door 0 -> 92 now 1484-1520; frames 1484-1541 re-rendered).
Near-still: 1431 only (1 pair). No magenta / black frames, no retried frames, no clipped sprites.

## Colour (`hue_report.row`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s14 shot 14 (g 1330-1433)                      33.1   51.4    3.3    0.0    0.1    2.4    1.8    7.8  0.24 0.44 0.17
s14 shot 15 (g 1434-1541)                      21.1   69.9    0.8    2.2    0.0    1.0    0.5    4.4  0.28 0.49 0.12
ref a t0005                                    43.1   47.7    2.8    0.0    0.0    0.8    0.1    5.5  0.34 0.50 0.04
```
Warm stone + gas + door oak, close to the warm interior ref (orange 51-70 / 48). Saturation 0.24-0.28 is the corridor's own low (louvre_API
7: exit door 0.19); magenta <= 7.8 (the oak and the red bucket under shade), no violet drift. Not graded here.

## Seconds per frame
13.4 s wall / 24.3 s CPU mean (two 2-thread processes at once). Sprites 320 px/D, 512 px/D in C2 and C4.

## Differences from the plan / notes
- The plumber comes from the corridor behind vincenzo (the door is locked, so not from the courtyard), unlocks, pulls the door open, then
  greets him; the plan's beats are all there.
- The knob is missing on the set's door (louvre_API), so vincenzo tugs at the lock box edge.
