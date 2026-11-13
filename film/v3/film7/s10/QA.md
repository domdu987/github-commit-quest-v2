# s10 QA: film 7, shots 10-11 (night -> Monday): paris dusk street -> louvre closet -> Salon Carré

Delivered: `frames/g_0914.png .. g_1119.png` (206 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, **first_g 914, 206 frames**). Plan range 30.66-37.12 s = g 920..1113; in-handle g 914-919 and
out-handle g 1114-1119 rendered in 3D. `meta.json` (first_g, n_frames, transition_in "dissolve", transition_out "cut", the inner
transitions, set-ups, frame_source), `cues.json`, `contact.jpg` (cyan line = y 880), `compare.jpg` (g 930 / ref a t0061 sunset, g 1000 and
g 1090 / ref a t0046 interior). Scripts: `shot.py` (stills / probe / final; one location per process), `deliver.py` (frames incl. the
dissolve and the street grade, meta, cues, sheets, mkv, `work/qa.txt`).

## Set-ups
| id | g | shot | what | caption |
|---|---|---|---|---|
| 1 | 914-949 | 10 | the rue at dusk (paris notre_dame_view build, STREET_DUSK, papers 0): the gas lamps come up (set_flames 0.15 -> 1.2), slow crane down toward Notre-Dame | "คืนวันอาทิตย์ เขาแอบ" |
| 2 | 950-990 | 10 | CUT into the storage closet (CLOSET_NIGHT): vincenzo crouched between the crates and a zinc bucket, the brooms and smocks behind, his hand on the storm lantern (pinned to the set's lantern); slow push | "ซ่อนตัวในตู้เก็บของ" (31.7 s = g 954) |
| 3 | 991-1024 | 10 | punch-in on his face; he darts a look at the door (g 987-992, "stunned" behind the blink) | "เพราะวันจันทร์" (32.88 s = g 989) |
| -- | 1015-1024 | 10/11 | DISSOLVE closet -> gallery (10 frames centred on the shot boundary g 1020), baked into the take | "พิพิธภัณฑ์ปิด" |
| 4 | 1025-1062 | 11 | Monday: the empty salon from high in the service-door corner, three workers in white smocks crossing, nobody else | "มีแต่คนงาน" |
| 5 | 1063-1119 | 11 | lower, closer: two smocked workers walk on toward her wall (she is on the back wall, with her glass now) | "ใส่เสื้อคลุมขาวเดินกันทั้งตึก" |

## Client rules
- **No depth of field** (common.Take). Everything sharp; the soft clouds in the dusk sky are the set's painted sky texture, not blur.
- **Mouths**: no quoted line in shots 10-11 -> static expression mouths only.
- **Heads**: main heads 0.45-0.56 H; no head bottom below y 880 anywhere (the punch-in camera was re-aimed after the first final put the
  chin 2 px past 880 in g 1013-1024). The wide set-up 4 has small figures (51-87 px heads, exempt as a wide), all above 880.
- **Dense sets**: shelves, brooms, mops, smocks, crates and buckets in the closet; the full salon hang in the gallery; the dusk rue with lamps,
  balconies and Notre-Dame.

## Runtime additions (shot.py; cast7 and the set untouched)
- Three Monday workers in white smocks = runtime cast copies (`worker7_a/b/c`) of coworker1 / coworker2 / guard bodies, re-dressed in cast7's
  `smock7` (white, as vincenzo_smock) with flat caps, canvases copied; registered in `P.CAST` / `sprites.DEFAULT_CANVAS` in this process only.
- Vincenzo uses `vincenzo_hide_closet` without the hand-held lantern prop: his hand is pinned to the set's storm lantern (the scene's only light).

## QA numbers (`work/qa.txt`)
Popcheck: only the planned cuts (950, 991, 1063); the dissolve is smooth. Near-still: 914 and 948 (the eased crane ends, one frame each).
No magenta / black frames, no retries.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s10 street dusk (g 914-949)                    31.2   29.5    2.0    0.0    0.0   12.7   15.5    9.1  0.35 0.52 0.08
s10 closet (g 950-1014)                         3.3   26.6   14.7    0.0    0.1   47.2    3.5    4.5  0.37 0.40 0.30
s10 gallery Monday (g 1025-1119)               54.3   38.9    2.7    0.3    0.0    1.0    0.2    2.6  0.38 0.57 0.03
s10 all (g 914-1119)                           37.3   34.2    5.5    0.1    0.0   14.3    4.0    4.6  0.37 0.50 0.13
```
The dusk street rendered magenta 12.8 (the set's pink-lit facades under STREET_DUSK; the set reports 8.0 for its own preset camera).
`deliver.py grade_magenta()` pulls the 290-345 deg band ~28 deg toward violet on set-up 1 only -> magenta 9.1, violet 15.5 (dusk blue-violet
shade, as the brief wants: "blue-violet, never magenta"). The closet is the set's night frame (blue 47, dark 0.30) with the warm lantern.

## Seconds per frame
11.08 s wall / 18.57 s CPU mean (12 samples, 2 threads, two processes at once). Sprites 192-448 px/D.

## Differences from the plan / known limits
- "Night falls on the Louvre": the paris set has no Louvre façade, so night falls on the rue outside (lamps lighting), then the closet.
- The fiacre horse's dark rump sits at the lower right edge of the street frames (set dressing, left in place).
- 2D cards cannot turn their backs: in set-up 5 the workers face three-quarter toward the lens while walking away into the room.
- The Monday workers reuse the coworkers' faces (they are the Louvre workers, now in the white Monday smocks).
