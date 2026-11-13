# s21 QA: film 7, shots 21-22 (reopening day: the queue at the empty wall; the four hooks, a gasp, a bowler)

Delivered: `frames/g_2038.png .. g_2241.png` (204 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 2038, 204 frames, checked with ffprobe). Plan range g 2044..2235 (68.13-74.53 s):
shot 21 = g 2044..2135, shot 22 = g 2136..2235; handles g 2038..2043 and g 2236..2241 rendered in 3D (camera and crowd keep moving).
transition_in = dissolve (10 f; closet-office -> gallery); transition_out = dissolve (next take is paris).
Scripts: `shot.py` (probe / stills / final), `deliver.py` (frames, meta, cues, contact, compare, mkv, `work/qa.txt`), shared helpers
`t5lib.py` (crowd colour variants, the bowler doff) and `t5deliver.py` (delivery + QA numbers), also used by s23 / s25.

## Set-ups (one location: louvre empty_wall_queue build, GALLERY_DAY; framing change every 1.1-1.8 s)
| id | g | what | caption it sits under |
|---|---|---|---|
| A | 2038-2091 | high wide over the queue lane (12 visitors + guard), the empty spot with its hooks on the red damask; slow drift in, 22->23 mm | "แล้วเรื่องประหลาดก็เกิดขึ้น" |
| B | 2092-2135 | reverse from beside the empty wall: the faces of the queue staring up at it (= at us), the hung room behind; lateral drift, 18 mm | "พอลูฟวร์เปิดอีกครั้ง" |
| C | 2136-2169 | (shot 22) ECU the four iron hooks and the dust-line patch, push in, 30 mm | "คนต่อแถวยาวเหยียด" |
| D | 2170-2207 | two-shot at the rope: the lady gasps, gloved hand to her mouth (g 2174-2178); the gentleman lifts his bowler off (2182-2189 hand to brim, 2190-2200 down to his chest, a small bow of the head) | "เพื่อมาดู ผนังว่าง ๆ" |
| E | 2208-2241 | the hooks again, low and a little wider (rope, plaque, gilt neighbours), push in; "ตะปูสี่ตัว" 74.07 s = g 2225 | "ที่มีแค่ตะปูสี่ตัว" |

Differs from the plan: shot 22's order is hooks -> gasp/bowler -> hooks again (instead of hooks then people), so the narration's
"empty wall with only four hooks" lands on the hooks. The bowler doff: cast7 has no hat prop, so `t5lib.hat_doff_patch()` adds a runtime
pose key `hat_off` (the derby style draws nothing for that figure) and the same derby is drawn in his hand as a sprite overlay that leaves
the head exactly where it sat. Crowd: lady / gentleman / newsboy / guard + runtime colour copies (lady_b teal, lady_c mustard, lady_d navy,
gentleman_b brown, gentleman_c green), no cast file edited. Queue ropes + set_mona(False) + set_flames keyed every frame.

## Client rules
- **No depth of field**: Take sets `use_dof = False` + `L.setup_dof(scene, None, None, cam=cam)` at build and before every render. Sharp
  everywhere (the far salon hang in B/D is crisp). No motion streaks (no whips).
- **Mouths**: no quoted line in shots 21-22 -> static expression mouths only (stunned; lady -> shocked behind the blink at g 2173).
- **Heads above y 880**: every head bottom <= 880 in every frame (`work/qa.txt`). The first final of set-up A had the two nearest
  visitors below the line: camera tilted down, the nearest gentleman removed, A re-rendered (old frames in work/old_raw).
- **Main head centre 0.35-0.59 H**: B main face (ladyb, front left) 0.56-0.57, lady 0.54-0.55; D gentleman 0.54, lady 0.54-0.55.
  A is a wide (exempt; heads 0.45-0.63 H). C / E are inserts without people.
- **Dense set**: the salon hang floor-to-ceiling, torchères, ropes, plaque, the Venetian feast canvas behind the queue in D.

## Numbers (`work/qa.txt`)
    set-up 1 g 2038..2091 A high wide over the reopening-day queue, the empty wall
      boy     head w   63..  75 px, x  203.. 225, y  617.. 620 (0.48..0.48 H); bottom below 880: none
      gent    head w   67..  80 px, x  385.. 395, y  583.. 591 (0.46..0.46 H); bottom below 880: none
      gentb   head w   71..  85 px, x  202.. 224, y  596.. 600 (0.47..0.47 H); bottom below 880: none
      gentb2  head w   91.. 114 px, x  206.. 226, y  685.. 704 (0.54..0.55 H); bottom below 880: none
      gentc   head w   86.. 106 px, x  406.. 413, y  663.. 673 (0.52..0.53 H); bottom below 880: none
      guard   head w   71..  84 px, x  580.. 618, y  598.. 604 (0.47..0.47 H); bottom below 880: none
      lady    head w   64..  76 px, x  296.. 304, y  581.. 590 (0.45..0.46 H); bottom below 880: none
      ladyb   head w   72..  87 px, x  444.. 467, y  626.. 627 (0.49..0.49 H); bottom below 880: none
      ladyb2  head w  103.. 132 px, x  303.. 307, y  762.. 804 (0.60..0.63 H); bottom below 880: none
      ladyc   head w   76..  92 px, x  314.. 316, y  642.. 646 (0.50..0.51 H); bottom below 880: none
      ladyd   head w   80..  97 px, x   97.. 145, y  659.. 670 (0.52..0.52 H); bottom below 880: none
      ladyd2  head w   99.. 127 px, x   17..  88, y  748.. 788 (0.58..0.62 H); bottom below 880: none
      render: wall 10.51 s, cpu 20.88 s per frame
    set-up 2 g 2092..2135 B reverse from the wall: faces of the queue
      boy     head w  136.. 148 px, x  714.. 743, y  685.. 704 (0.53..0.55 H); bottom below 880: none
      gent    head w  203.. 224 px, x  406.. 504, y  739.. 766 (0.58..0.60 H); bottom below 880: none
      gentb   head w  130.. 140 px, x  566.. 605, y  561.. 569 (0.44..0.44 H); bottom below 880: none
      gentb2  head w  102.. 106 px, x  289.. 326, y  503.. 505 (0.39..0.39 H); bottom below 880: none
      gentc   head w  136.. 142 px, x  130.. 180, y  570.. 574 (0.45..0.45 H); bottom below 880: none
      gentc2  head w   82..  83 px, x  171.. 191, y  460.. 461 (0.36..0.36 H); bottom below 880: none
      lady    head w  175.. 195 px, x  651.. 699, y  690.. 710 (0.54..0.55 H); bottom below 880: none
      ladyb   head w  196.. 212 px, x  140.. 252, y  717.. 735 (0.56..0.57 H); bottom below 880: none
      ladyb2  head w   97.. 100 px, x  144.. 182, y  522.. 523 (0.41..0.41 H); bottom below 880: none
      ladyc   head w  135.. 143 px, x  342.. 401, y  602.. 610 (0.47..0.48 H); bottom below 880: none
      ladyd   head w   99.. 104 px, x  482.. 499, y  526.. 532 (0.41..0.42 H); bottom below 880: none
      ladyd2  head w   82..  85 px, x  339.. 355, y  485.. 488 (0.38..0.38 H); bottom below 880: none
      render: wall 12.06 s, cpu 23.68 s per frame
    set-up 3 g 2136..2169 C ECU the four hooks, push in
      render: wall 7.64 s, cpu 14.98 s per frame
    set-up 4 g 2170..2207 D two-shot at the rope: lady gasps, gentleman doffs his bowler
      boy     head w  180.. 193 px, x  641.. 664, y  735.. 745 (0.57..0.58 H); bottom below 880: none
      gent    head w  332.. 360 px, x  255.. 308, y  689.. 691 (0.54..0.54 H); bottom below 880: none
      gentb   head w  170.. 178 px, x  442.. 460, y  590.. 592 (0.46..0.46 H); bottom below 880: none
      gentb2  head w  140.. 141 px, x   79..  90, y  571.. 576 (0.45..0.45 H); bottom below 880: none
      lady    head w  245.. 267 px, x  560.. 587, y  695.. 704 (0.54..0.55 H); bottom below 880: none
      ladyc   head w  196.. 202 px, x  164.. 172, y  653.. 656 (0.51..0.51 H); bottom below 880: none
      ladyd   head w  129.. 132 px, x  319.. 340, y  600.. 602 (0.47..0.47 H); bottom below 880: none
      ladyd2  head w  108.. 109 px, x  128.. 163, y  582.. 585 (0.46..0.46 H); bottom below 880: none
      render: wall 13.08 s, cpu 25.71 s per frame
    set-up 5 g 2208..2241 E the hooks again, low and wider, push in (out-handle 2236-2241)
      render: wall 7.86 s, cpu 15.41 s per frame
    all: wall 10.40 s, cpu 20.49 s per frame; retried: []

Popcheck: jumps only at the planned cuts (2091->2092, 2135->2136, 2169->2170, 2207->2208). Still runs: none longer than 1 frame
(the sine ease ends of the C push). No black / magenta frames, no retried frames, no clipped sprites.

## Colour (hue_report rows)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s21 set-up 1 (g 2038-2091)                     47.3   45.2    3.6    0.8    0.3    1.7    0.1    0.9  0.44 0.60 0.02   OUT: red,orange,blue,dark
s21 set-up 2 (g 2092-2135)                     33.6   51.5    2.1    0.1    2.3    3.6    1.5    5.2  0.33 0.58 0.08   OUT: orange,blue,sat,dark
s21 set-up 3 (g 2136-2169)                     97.7    1.7    0.0    0.0    0.0    0.1    0.2    0.3  0.92 0.64 0.06   OUT: red,orange,blue,sat,val,dark
s21 set-up 4 (g 2170-2207)                     34.1   39.3    1.5    0.2    0.4    4.7    2.4   17.5  0.32 0.53 0.12   OUT: orange,blue,magenta,sat
s21 set-up 5 (g 2208-2241)                     95.8    3.0    0.2    0.0    0.0    0.2    0.1    0.8  0.87 0.63 0.02   OUT: red,orange,blue,sat,val,dark
s21 all                                        74.2   19.9    1.2    0.2    0.4    1.2    0.5    2.5  0.55 0.59 0.06   OUT: red,orange,blue,sat,dark
ref a t0040                                    21.3   28.8    3.1    0.6    0.0   29.5    6.8    9.9  0.30 0.47 0.07   OUT: red,violet,sat,dark
ref a t0048                                    30.6   48.6    4.8    0.3    0.0    0.5   10.5    4.6  0.37 0.43 0.15   OUT: orange,blue,violet,sat,val
ref a t0030                                    29.3    5.0    0.1    0.4    2.7   51.8    2.2    8.4  0.19 0.72 0.00   OUT: red,orange,blue,sat,val,dark
```
Out of band, honestly: the hook inserts C / E are almost all red silk damask (red 96-98, sat 0.9): that is the wall the plan asks for in
ECU; the gilt neighbours in E help a little. A / B are warm (red + orange 80-85, blue low) like the set (louvre_API: gallery runs warm).
D magenta 17.5 comes from the aubergine / purple costumes of the cast7 lady (jacket, skirt, hat ribbon) filling the right half, not from
shade: the shade on the damask and the parquet is blue-violet as in the set. Dark pixels low in A (bright skylit hall).

## Cost
Mean 10.4 s wall / 20.5 s CPU per frame (two 2-thread processes at once); crowd set-ups 12-13 s wall, hook inserts 7.6-7.9 s.
