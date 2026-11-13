# s23 QA: film 7, shots 23-24 (her face everywhere: kiosk, a gentleman reading, newsboy, the Morris column, a lady humming)

Delivered: `frames/g_2230.png .. g_2449.png` (220 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 2230, 220 frames, checked with ffprobe). Plan range g 2236..2443 (74.53-81.48 s):
shot 23 = g 2236..2339, shot 24 = g 2340..2443; handles g 2230..2235 / 2444..2449 rendered in 3D. transition_in / out = dissolve (10 f).
Scripts: `shot.py`, `deliver.py` (uses ../s21/t5deliver.py and ../s21/t5lib.py).

## Set-ups (paris street area, kiosk build, STREET_GOLDEN; set_papers(24) keyed every frame = full count; framing change every 1.6-2.0 s)
| id | g | what | caption |
|---|---|---|---|
| A | 2230-2279 | the kiosk front: two rows of front pages with her face (LE MATIN, EXCELSIOR, LE PETIT JOURNAL...), tracking along, 22 mm | "หน้าโมนาลิซ่าขึ้นหนังสือพิมพ์" |
| B | 2280-2339 | a gentleman at the kiosk reading the front page, shocked (eyes run along the lines, a small shudder), a lady (teal) reading behind him; push in, 24 mm | "ทั่วโลก มีเพลง มีโปสการ์ด" |
| C | 2340-2392 | (shot 24) the rue: the newsboy waves the front page high, shouting (static open mouth); two passers walk toward us; the Morris column with her posters, Notre-Dame far off | "มีโฆษณา คนที่ไม่เคย" |
| D | 2393-2449 | push past a lady humming happily (eyes shut on the long note, head swaying), she strolls off screen-left at g 2404, the push ends on the column poster: her smile ("Elle sourit encore") | "เห็นของจริง ก็จำรอยยิ้มนี้ได้หมด" |

Differs from the plan: "people humming" is one lady humming (closed-mouth smile, swaying; no music notes in the cast fx); the Morris
column posters appear in C (behind the newsboy) and as the D close-up rather than in a street_wide preset frame (the area is the same).

## Client rules
- **No depth of field**: off at build and before every render; sharp to Notre-Dame. No streaks.
- **Mouths**: no quoted line: the newsboy's shout and everyone's smile are static mouths (newsboy_shout's fixed talk_b shape, never animated).
- **Heads above y 880**: all head bottoms <= 880 (`work/qa.txt`). The humming lady's walk-off first dipped below it at the left edge:
  she now walks away from the lens as well as to the left (re-rendered).
- **Main head centre 0.35-0.59 H**: B gentleman 0.42-0.45, C newsboy 0.56-0.58, D lady 0.47-0.50. A is an insert without people.
- Theft known by now: papers 24 everywhere (continuity gotcha in common.py respected the other way round).

## Numbers (`work/qa.txt`)
    set-up 1 g 2230..2279 A the kiosk front pages with her face, tracking along
      render: wall 8.61 s, cpu 16.88 s per frame
    set-up 2 g 2280..2339 B gentleman reading the front page at the kiosk, shocked
      reader  head w  208.. 270 px, x  340.. 360, y  541.. 575 (0.42..0.45 H); bottom below 880: none
      reader2 head w  137.. 162 px, x  504.. 535, y  592.. 601 (0.46..0.47 H); bottom below 880: none
      render: wall 10.37 s, cpu 20.37 s per frame
    set-up 3 g 2340..2392 C the rue: newsboy waving the front page, shouting; passers; Morris column
      boy     head w  197.. 243 px, x  255.. 306, y  714.. 739 (0.56..0.58 H); bottom below 880: none
      walk1   head w   62..  87 px, x  275.. 333, y  621.. 628 (0.49..0.49 H); bottom below 880: none
      walk2   head w   49..  66 px, x   39..  76, y  608.. 612 (0.47..0.48 H); bottom below 880: none
      render: wall 9.35 s, cpu 18.37 s per frame
    set-up 4 g 2393..2449 D push past a lady humming into the column poster: her smile (out-handle 2444-2449)
      hum     head w  386.. 437 px, x  -36.. 141, y  600.. 646 (0.47..0.50 H); bottom below 880: none
      render: wall 9.49 s, cpu 18.66 s per frame
    all: wall 9.50 s, cpu 18.65 s per frame; retried: []

Popcheck: jumps only at the planned cuts (2279->2280, 2339->2340, 2392->2393). The lady's stand -> walk at g 2404 first popped (she
flipped direction): she now stands already facing screen-left, glancing back at the poster, and her hands / stride blend in over 6 frames
(g 2393-2412 re-rendered). No still runs, no black / magenta frames, no retried frames.

## Colour (hue_report rows)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s23 set-up 1 (g 2230-2279)                     33.4   32.5    5.5    1.5    1.1   19.2    4.6    2.2  0.36 0.47 0.25   OUT: sat,dark
s23 set-up 2 (g 2280-2339)                     33.2   34.8    4.9    1.1    2.8   14.4    5.7    3.1  0.34 0.49 0.17   OUT: violet,sat,dark
s23 set-up 3 (g 2340-2392)                      3.5   19.4    7.0    0.0    0.0   42.4   24.7    2.9  0.33 0.45 0.19   OUT: red,orange,blue,violet,sat,val,dark
s23 set-up 4 (g 2393-2449)                      2.5    6.5    0.3    0.1    0.0   62.9   16.6   11.1  0.37 0.37 0.35   OUT: red,orange,blue,violet,magenta,sat,val,dark
s23 all                                        19.9   24.6    4.5    0.7    1.1   32.6   12.1    4.6  0.35 0.44 0.24   OUT: red,blue,violet,sat,val,dark
ref a t0062                                    56.9   30.5    2.4    0.0    0.0    0.0    0.0   10.2  0.50 0.70 0.26   OUT: red,blue,magenta,sat,val,dark
ref a t0048                                    30.6   48.6    4.8    0.3    0.0    0.5   10.5    4.6  0.37 0.43 0.15   OUT: orange,blue,violet,sat,val
ref a t0085                                     0.8    1.1    0.0    0.0    0.0   82.6   10.9    4.6  0.55 0.61 0.03   OUT: red,orange,blue,violet,sat,dark
ref a t0030                                    29.3    5.0    0.1    0.4    2.7   51.8    2.2    8.4  0.19 0.72 0.00   OUT: red,orange,blue,sat,val,dark
```
A / B (the kiosk in the low gold sun) are in band for red / orange / blue. C / D sit in the shade of the east row (the sun travels along the
street, louvre_API: street frames run blue-heavy): blue 42-62 like ref a t0085 (blue 83); shade there is blue-violet, the D magenta 11 is
the column's purple poster frames plus the lady's navy-violet costume. Dark 0.19-0.34 in the shaded set-ups.

## Cost
Mean 9.5 s wall / 18.6 s CPU per frame (two 2-thread processes at once).
