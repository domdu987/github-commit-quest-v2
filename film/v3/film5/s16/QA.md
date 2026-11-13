# s16 QA: film 5, shot 16 (fast replay of the shrinking song), mine set (tunnel LAMP)

Delivered: `take.mkv` = frames g 1699..1821 (123 frames, 720x1280, 12 samples, 2 threads, no captions, no audio); first_g 1699; shot 16 = g 1707..1813,
handles g 1699..1706 and 1814..1821 rendered in 3D (cameras keep moving) for 12-f dissolves. Also `meta.json`, `cues.json`, `contact.jpg`, `compare.jpg`
(finals beside ref a t0113 / t0115 / t0117), `shot.py`, `deliver.py`, `qa.py`.

## Client rules
- **No DOF / no blur**: `M.setup_dof(scene, None, None, cam=...)` at build and before every render (cage_insert's DOF default never applied). No streaks.
- **Bird inside the cage**: the cage hangs on its nail (nobody holds it), so the set's 3D brass cage is used with the canary sprite standing on the perch,
  0.09 D right of centre (room for the notes) and behind the front wires; checked by eye at full size in all three beats.
- **Gentle bird**: in 16c after the one note the beak closes, eyes grow heavy (0.85 -> 0.45), droop/ruffle; never closed, never X; it stays on the perch.

## Timing
| sub-shot | g | notes | haze | caption |
|---|---|---|---|---|
| 16a | 1707-1742 (in-handle 1699-1706) | 5 | card 0.10, set_gas 1 | "เพลงที่สั้นลงทุกวัน" |
| 16b | 1743-1778 (cut) | 3 | 0.22, gas 2 | "ก็คือแก๊สที่ค่อย ๆ" |
| 16c | 1779-1813 (cut, out-handle 1814-1821) | 1, silent from 1797 | 0.36, gas 3 | "เพิ่มขึ้นทุกวัน นั่นเอง" |
Each beat: new angle (-38 / +8 / -12 deg) and a quick cubic-out push (1.75 -> 1.2 D etc.): the "replay" energy.
Haze = my camera-facing card (same material as s15, edge below the frame so the whole picture sits in it) + the set's gas slabs.

## Numbers (`work/qa.txt`)
```
sub-shot 16a (g 1699..1742, 44 frames)
  bird    head w    82..  120 px, centre x  434.. 469, centre y  742.. 748 (0.58..0.58 H); head bottom below 880: none
  render: wall 15.23 s, cpu 27.81 s per frame (mean)
  retried frames: []
sub-shot 16b (g 1743..1778, 36 frames)
  bird    head w    87..  126 px, centre x  439.. 474, centre y  749.. 755 (0.59..0.59 H); head bottom below 880: none
  render: wall 13.56 s, cpu 26.67 s per frame (mean)
  retried frames: []
sub-shot 16c (g 1779..1821, 43 frames)
  bird    head w   103..  149 px, centre x  448.. 480, centre y  777.. 798 (0.61..0.62 H); head bottom below 880: none
  render: wall 14.26 s, cpu 26.87 s per frame (mean)
  retried frames: []
```
popcheck: pops (g -> g+1, change): [(1742, 1743, 25.8), (1778, 1779, 20.3)]
near-still transitions (< 0.35 levels): [1741, 1775, 1776, 1777, 1817, 1818, 1819, 1820]
magenta / black frames: []


Pops only at the two cuts.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s16 16a (g 1699-1742)                           3.6   37.9    5.5    0.0    0.1   49.7    0.7    2.3  0.27 0.44 0.02   OUT: red,blue,sat,val,dark
s16 16b (g 1743-1778)                           3.5   45.7    9.1    1.7   14.3   25.6    0.0    0.0  0.22 0.46 0.00   OUT: red,orange,sat,dark
s16 16c (g 1779-1821)                           0.3   52.6   11.7   18.0   14.4    2.9    0.0    0.0  0.20 0.51 0.00   OUT: red,orange,blue,sat,dark
s16 all                                         2.5   44.8    8.5    6.2    8.6   28.2    0.3    0.9  0.23 0.47 0.01   OUT: red,orange,sat,dark
```
Gold insert: orange dominant; the haze turns the shade from blue (16a) to grey-green (16c) on purpose (the gas thickening); magenta 0-2.

## Seconds per frame
~14.4 s wall / ~27 CPU s mean (2048 px/D bird sprite + gas slabs, 12 samples).

## Differences / known issues
- 16c's single note is small and sits inside the cage behind the wires (the cast draws one note close to the beak); readable at full size, less obvious than 5 / 3.
- No chalk tally (day numbers) on screen: the haze level and note count carry the countdown.
