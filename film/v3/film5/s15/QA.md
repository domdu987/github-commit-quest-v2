# s15 QA: film 5, shot 15 (the reveal, diagram look), mine set (tunnel LAMP)

Delivered: `take.mkv` = frames g 1494..1714 (221 frames, 720x1280, 12 samples, 2 threads, no captions, no audio); first_g 1494; shot 15 = g 1502..1706,
handles g 1494..1501 / 1707..1714 rendered in 3D for 12-f dissolves. Also `meta.json`, `cues.json`, `contact.jpg`, `compare.jpg` (finals beside ref a
t0099 / t0103 / t0107 / t0111), `shot.py`, `deliver.py` (+ breath-trace overlay), `qa.py`.

## The diagram
Three heights, top to bottom: the bird (cage hung high under the cap bar of set 6), the man (gaffer, mouth closed), his flame lamp hanging low at his side.
- **Breathing side by side** (15a-15c, g 1504-1617): bird chest `breath` 1 at ~4.2 pumps/s; the man breathes slowly (squash/lean, 3.2 s period).
  deliver.py draws two crisp scrolling breath traces over the same 2 s window beside them: the bird's yellow zigzag (~8 bumps) vs the man's single
  slow pale-blue wave (drawn at 4x and reduced: anti-aliased lines, no blur filter). The bird's trace greys toward green once the gas has reached it.
- **Gas reaches the bird first**: my camera-facing haze card (green-grey, alpha <= 0.30, wavy noise edge with a faint bright line) sinks from the roof:
  edge passes the bird ~g 1590, the man's mouth ~1622, the lamp 1656.
- **The lamp changes only at the end**: flame steady yellow through 15d; 15e (cut on "สายไปแล้ว", g 1654) the flame flares tall and blue g 1656-1663
  (cast keys `flame` 1 -> 1.9, `flame_blue` 0 -> 0.9, keyed warm + cold lamp_lights).
- 15f: back to the bird inside the bars, still breathing fast, a little heavy-eyed in the haze ("แต่นกบอกได้ก่อน").

| sub-shot | g | framing | caption |
|---|---|---|---|
| 15a | 1502-1539 (in-handle 1494) | two-shot across the roadway, slow push | นกหายใจเร็วกว่าคน |
| 15b | 1540-1578 | from inbye: bird near (right, high), man left | หลายเท่า |
| 15c | 1579-1617 | low wide, all three heights, gas edge sinking | แก๊สเข้าตัวมันก่อนคน หลายนาที |
| 15d | 1618-1653 | man + lamp, gas just above the lamp, flame steady | ตะเกียงบอกได้ก็ตอนที่ |
| 15e | 1654-1676 | ECU lamp: blue flare | สายไปแล้ว |
| 15f | 1677-1706 (out-handle to 1714) | ECU bird behind the front wires | แต่นกบอกได้ก่อน |

## Client rules
- No DOF anywhere (`M.setup_dof(scene, None, None, cam=...)` at build and before every render); no motion blur.
- Bird: the cage hangs (nobody holds it), so the set's 3D cage with the canary sprite on the perch behind the front wires (checked at full size in 15f).
- Gentle bird: never falls in this shot; eyes 1 -> 0.75, slight droop in the gas.

## Numbers (`work/qa.txt`)
```
sub-shot 15a (g 1494..1539, 46 frames)
  bird    head w    27..   30 px, centre x  477.. 490, centre y  496.. 503 (0.39..0.39 H); head bottom below 880: none
  gaffer  head w   227..  254 px, centre x  220.. 251, centre y  596.. 613 (0.47..0.48 H); head bottom below 880: none
  render: wall 10.39 s, cpu 18.61 s per frame (mean)
  retried frames: []
sub-shot 15b (g 1540..1578, 39 frames)
  bird    head w    54..   60 px, centre x  512.. 530, centre y  498.. 505 (0.39..0.39 H); head bottom below 880: none
  gaffer  head w   212..  228 px, centre x   66..  79, centre y  692.. 715 (0.54..0.56 H); head bottom below 880: none
  render: wall 10.16 s, cpu 19.76 s per frame (mean)
  retried frames: []
sub-shot 15c (g 1579..1617, 39 frames)
  bird    head w    23..   24 px, centre x  430.. 434, centre y  518.. 534 (0.40..0.42 H); head bottom below 880: none
  gaffer  head w   183..  192 px, centre x  240.. 254, centre y  456.. 495 (0.36..0.39 H); head bottom below 880: none
  render: wall 11.62 s, cpu 22.76 s per frame (mean)
  retried frames: []
sub-shot 15d (g 1618..1653, 36 frames)
  gaffer  head w   281..  305 px, centre x  379.. 384, centre y  276.. 325 (0.22..0.25 H); head bottom below 880: none
  render: wall 11.45 s, cpu 21.30 s per frame (mean)
  retried frames: []
sub-shot 15e (g 1654..1676, 23 frames)
  gaffer  head w   974.. 1294 px, centre x  884..1096, centre y -1031..-714 (-0.81..-0.56 H); head bottom below 880: none
  render: wall 9.39 s, cpu 18.79 s per frame (mean)
  retried frames: []
sub-shot 15f (g 1677..1714, 38 frames)
  bird    head w   133..  174 px, centre x  254.. 279, centre y  660.. 685 (0.52..0.53 H); head bottom below 880: none
  render: wall 15.16 s, cpu 27.50 s per frame (mean)
  retried frames: []
```
popcheck: pops (g -> g+1, change): [(1539, 1540, 38.0), (1578, 1579, 38.1), (1617, 1618, 39.0), (1653, 1654, 39.3), (1676, 1677, 26.5)]
near-still transitions (< 0.35 levels): [1494, 1677]
magenta / black frames: []


Pops only at the five cuts. 15e head numbers are off-screen (only his coat/lamp are in the ECU).

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s15 15a (g 1494-1539)                          11.9   19.3    0.3    0.0    0.0   53.1    8.0    7.5  0.41 0.40 0.07   OUT: red,orange,blue,violet,val,dark
s15 15b (g 1540-1578)                           9.2   24.1    1.1    0.0    0.0   51.8    7.1    6.7  0.44 0.41 0.07   OUT: red,blue,violet,val,dark
s15 15c (g 1579-1617)                          14.4   18.5    0.7    0.1    0.7   50.9    8.5    6.2  0.37 0.41 0.06   OUT: red,orange,blue,violet,sat,val,dark
s15 15d (g 1618-1653)                          20.4   24.9    0.3    0.3    1.1   45.3    2.0    5.5  0.40 0.43 0.07   OUT: red,blue,val,dark
s15 15e (g 1654-1676)                           0.1   31.9    0.8    0.3   35.3   31.4    0.0    0.1  0.24 0.46 0.00   OUT: red,blue,sat,dark
s15 15f (g 1677-1714)                           0.9   67.4   12.1    5.5   10.0    3.5    0.0    0.7  0.23 0.52 0.00   OUT: red,orange,blue,sat,dark
s15 all                                        10.6   29.6    2.4    1.0    4.6   41.7    5.0    5.1  0.36 0.44 0.05   OUT: red,blue,sat,val,dark
```
Underground blue-dominant like s01; 15e/15f are the haze-tinted inserts (cyan = the blue flame + green-grey haze). Magenta <= 7.5.

## Seconds per frame
~11 s wall / ~21 CPU s mean (15f 27.5 CPU: 2048 px/D bird sprite).

## Differences from the plan / known issues
- Runtime only: cage moved up to z 3.92 with a small nail (set_cage), the tub train hidden (it stood in the across-the-roadway cameras), my haze card.
- "Diagram look" done with the 3D staging + the overlaid breath traces (no text). If the director prefers no overlay, raw frames without traces are
  reproducible: `shot.py final` + deliver.py with TR_IN > TR_OUT.
- First final pass of 15d/15e came out magenta (gaffer sprite failed to load in the process that rendered 15f -> 15e -> 15d); re-rendered in a fresh
  process in order 15d -> 15e, all frames checked (no magenta/black frames).
