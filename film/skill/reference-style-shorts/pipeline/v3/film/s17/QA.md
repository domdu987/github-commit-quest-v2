# QA s17 (shots 17)

Film frames g 1077..1122 (cut range [1086, 1123)), handles in 9 / out 0, transition in: dissolve. Set office, light office_grey, 12 samples, 720x1280.

Frames delivered: 46 of 46 expected (complete). Every frame rendered in 3D (no 2D handle extension).


## Heads (from the per-frame meta of the final render; px at 720x1280)

| actor | frames | width min-max | centre y min-max (fraction of H) | lowest head bottom y |
|---|---|---|---|---|
| boss17 | 46 | 175-187 | 381-511 (0.30-0.40) | 591 |
| hero17 | 46 | 229-237 | 400-472 (0.31-0.37) | 573 |

Near/far head ratio (hero / chief) where both are in the render: min 1.26, median 1.29, max 1.32.


## Pinned props

Max registration error: no pinned prop in this take.


## Camera (qa_motion method: true camera, corner speed px per frame)

Moves (speed > 12 px/frame): none.

Static runs (< 0.25 px/frame): none. Linear runs (speed change < 2 % per frame at > 1 px/frame): [[1092, 1101]].

Speed per frame: min 0.47, median 3.18, max 4.3 px.


## Popcheck (final frames, mean abs difference at 180x320)

Median 6.68, max 8.68; isolated pops: none.


## Colour (`v3/tools/hue_report.py frames/`)

```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
reference A, whole clip                        33.6   23.1    0.7    0.5    0.5   29.1    2.7    9.7  0.48 0.63 0.08   OUT: sat,val,dark
reference B, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08   OUT: red,dark
reference A interiors                          40.1   27.6    0.3    0.4    0.0   21.9    1.1    8.6  0.47 0.55 0.09   all in band
reference B interiors                          36.3   37.7    2.3    0.1    0.0   13.9    4.5    5.1  0.38 0.45 0.15   OUT: blue
target band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15  (percent of chroma for hue families)
v3/film/s17/frames                             33.1   43.4    0.0    3.0    0.7   16.0    0.9    2.9  0.41 0.46 0.17   OUT: orange,dark
```


## Cost

CPU s per final frame min / median / max: [25.6, 27.0, 29.1]; wall s: [32.5, 34.3, 43.9] (2 threads, other agents rendering at the same time). Retried frames: none; still wrong: none.


## Notes, deviations

- Camera: lens 0.70 -> 0.90 D above the floor, 4.5 D from the map wall, truck left 0.6 D (the plan's 0.6 D/s over the whole take would be 0.9 D; 0.6 D keeps the near hero right of centre), pitch +14.5 deg (plan +16: lowered 1.5 deg so the head centres sit near 0.35 H), pan from 11.6 to 15.4 deg right of the wall normal. The plan's 20 -> 10 deg, read with these marks, puts the hero left of centre and the chief at the frame edge, so the pan turns the other way while the camera trucks left; the parallax still carries the chief right to left across the frame. Settles over the last 6 frames (ease, then 0.4 %/frame creep: never parked).
- Chief: acting.boss_whistle_stroll (held whistle drawing: eyes shut, brows up, round pucker; never flapping), hands behind his back, pointer tucked under the near arm, step 0.68 s, bob 0.47 D, sway 0.13 D, 0.72 D/s on a diagonal from (2.20, -0.82) to boss_mark, planted on a contact phase at g 1116, then the knees and the bob settle over 5 frames. He starts 0.82 D off the wall (plan 1.3 D) and emerges from behind the hero during the dissolve: from this low lens any path 1.3 D off the wall stays hidden behind the near hero for half the take. His head is 175-195 px (plan about 230): 230 px would put him 3.4 D from a lens that must also hold the hero at gloat_near.
- Three note glyphs (acting.note_glyphs_svg) leave the mouth at 36.5, 36.8, 37.1 (g 1098, 1107, 1116), drawn in the sprite overlay on an extended canvas.
- Hero at gloat_near, three-quarter to the lens facing the map side: acting.hero_slumped (lean 4 deg, head down, sad_down, turning the pencil stub), one blink at 37.0 (g 1113); his mouth never moves.
- Map state: red line complete with arrow head, smudge halo level 3, chalk curve, six old tracks, tick, Thai label pinned (not featured, top left), spinner at the storm symbol (0.5 rev/s); calendar leaf 21 set but off frame. The window wall is just outside the right frame edge in this framing, so the rain card is not seen; the rain remains a sound bed.
- Heel clicks in cues.json are at the walk's real contact frames (36.42, 37.10, settle 37.30), not the plan's 0.35 s spacing: the cycle steps every 0.68 s as the plan's walk numbers ask.
- qa_motion flags one near-constant-speed run g 1092-1101 (speed change under 2 %/frame): it is the peak of the smoothstep truck, not a linear move; left as is rather than re-render the take.
- Colour: grey light (special light per the plan). Orange 43.4 and dark share 0.17 are above the day band: the low lens fills the lower third with the warm plank floor and the dark under-ceiling; shade still reads blue-violet, magenta 2.9.
