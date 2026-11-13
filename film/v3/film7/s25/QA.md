# s25 QA: film 7, shot 25 (the real painting lies in a wooden trunk under his bed, two whole years)

Delivered: `frames/g_2438.png .. g_2578.png` (141 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 2438, 141 frames, checked with ffprobe). Plan range g 2444..2572 (81.48-85.77 s);
handles g 2438..2443 / 2573..2578 rendered in 3D. transition_in = dissolve (10 f, as the task says), transition_out = dissolve (10 f).
Scripts: `shot.py`, `deliver.py` (uses ../s21/t5deliver.py).

## Set-ups (attic, under_bed_insert build, ATTIC_DUSK; framing change every 1.5-1.6 s)
| id | g | what | caption |
|---|---|---|---|
| A | 2438-2484 | floor level under the bed by the floor candle: the trunk slides out toward us (pull 0 -> 0.75, g 2450-2482), slow push | "ส่วนภาพจริง นอนอยู่ในหีบ" |
| B | 2485-2530 | the attic: vincenzo (normal clothes) crouched beside the bed, peeking; the trunk comes fully out (-> 1, 2485-2494), the lid swings open (0 -> 100 deg, 2494-2514); smirk -> smug, a glance at the window (2512-2521) | "ไม้ใต้เตียง ห้องเช่าของเขา" |
| C | 2531-2578 | looking down into the open trunk: the panel, her smile in the candlelight; linear push in | "สองปีเต็ม" |

Runtime set fixes (set module untouched): the trunk's panel sat under the trunk's inner top face, so it never showed even with the lid
open; it is raised 0.13 D (keyed) once the lid passes 35 deg, and turned 180 deg about its centre so she reads upright from the open side.
The camera-only sun-shaft sheet (grey haze over the trunk) is hidden. A small warm no-shadow fill (candle colour, flickering) over the trunk.
Differs from the plan: the plan's "under_bed_insert -> room_wide" is done as three set-ups (insert / room / trunk insert); B uses a
custom room camera rather than the room_wide preset (the preset frames the trunk at the far left behind him).

## Client rules
- **No depth of field**: off at build and before every render. No streaks.
- **Mouths**: nobody speaks; vincenzo's static smirk / smug mouths.
- **Heads above y 880**: vincenzo head bottom <= 704 (head centre 0.46-0.47 H, 180-202 px).
- Night-ish attic: candle (table + floor) are the warm in-scene emitters, flicker keyed every frame.

## Numbers (`work/qa.txt`)
    set-up 1 g 2438..2484 A floor level: the trunk slides out from under the bed by the candle
      render: wall 8.63 s, cpu 16.65 s per frame
    set-up 2 g 2485..2530 B attic: vincenzo crouched peeking, trunk out, lid opens
      vin     head w  180.. 202 px, x  399.. 414, y  593.. 603 (0.46..0.47 H); bottom below 880: none
      render: wall 8.55 s, cpu 16.82 s per frame
    set-up 3 g 2531..2578 C down into the open trunk: the panel, her smile, push in (out-handle 2573-2578)
      render: wall 9.59 s, cpu 18.83 s per frame
    all: wall 8.93 s, cpu 17.45 s per frame; retried: []

Popcheck: jumps only at the planned cuts (2484->2485, 2530->2531); the small flags 2440 (1.1) and 2521 (2.3, the glance back) are motion,
not pops. No still runs, no black / magenta frames, no retried frames, no clipped sprites.

## Colour (hue_report rows)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s25 set-up 1 (g 2438-2484)                     20.3   52.6    1.5    0.2    0.0   18.9    1.3    5.2  0.27 0.39 0.12   OUT: red,orange,sat,val
s25 set-up 2 (g 2485-2530)                     17.2   37.3    1.3    0.0    0.0   24.8    9.8    9.7  0.20 0.37 0.23   OUT: red,violet,sat,val,dark
s25 set-up 3 (g 2531-2578)                     56.5   28.0    0.4    0.0    0.0    5.1    3.7    6.1  0.32 0.31 0.33   OUT: red,blue,sat,val,dark
s25 all                                        33.8   39.6    1.1    0.1    0.0   14.8    4.1    6.5  0.27 0.36 0.23   OUT: orange,sat,val,dark
ref a t0080                                    10.2    2.2    0.1    0.0    0.3   62.0   14.3   10.9  0.41 0.49 0.07   OUT: red,orange,blue,violet,magenta,dark
ref a t0010                                    26.3   28.6    2.2    0.2    0.0   31.2    3.9    7.6  0.27 0.51 0.07   OUT: red,blue,sat,dark
ref a t0030                                    29.3    5.0    0.1    0.4    2.7   51.8    2.2    8.4  0.19 0.72 0.00   OUT: red,orange,blue,sat,val,dark
```
Dusk attic lit by candles: low value (0.31-0.39) and saturation as the set measures (louvre_API: attic sat 0.21); A is orange-heavy (the
candle pool), C red from the trunk wood and her ochre sleeves. Shade is blue (hue ~225) - violet 4, magenta 6.5 over the take, no magenta cast.

## Cost
Mean 8.9 s wall / 17.5 s CPU per frame (two 2-thread processes at once).
