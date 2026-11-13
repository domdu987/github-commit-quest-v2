# s19 QA: film 7, shots 19-20 (62.62-68.13 s): the police search in chaos; the young painter questioned, vincenzo strolls by

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps) = g 1873..2049 (first_g 1873, 177 frames): in-handle g 1873..1878, shot 19 g 1879..1964,
shot 20 g 1965..2043, out-handle g 2044..2049, all rendered in 3D (720x1280, 12 samples, 2 threads, denoise FAST). Also `meta.json`,
`cues.json`, `contact.jpg`, `compare.jpg`. Scripts: `engine.py` (same as s16), `shot.py`, `deliver.py`, `queue_lanes.sh` (the render queue
used for s18 + s19). Numbers: `work/qa.txt`, `work/hue.txt` (not in git).

| set-up | g | framing | action | caption |
|---|---|---|---|---|
| 1 | 1873-1918 | wide salon from the door side, 22 mm, slow push | three policemen run across in all directions, one searches by the divan with a lantern, the guard waves then shrugs | "ลูฟวร์ปิดหนึ่งสัปดาห์" |
| 2 | 1919-1964 | CUT at the empty wall, 22 mm | an inspector crouches with his lantern at the four hooks, the guard shrugs, a policeman runs through the foreground | "ตำรวจค้นทั้งตึก" 63.85 |
| 3 | 1965-2004 | CUT the service-door corner as an office | the inspector points and questions the generic young painter (striped shirt) across a little table with a lantern and papers; the painter flares up (g 1986) | "จับปิกัสโซไปสอบสวนด้วยซ้ำ" |
| 4 | 2005-2049 | CUT punch-in on the painter, 24 mm | indignant; behind him, small and unnoticed, vincenzo (normal clothes, hands in pockets) strolls across the gallery and gives us a smug glance (g 2026) | "แต่ไม่มีใครสงสัยไอ้มักกะโรนีเลย" 66.38 |

## Client rules
- No depth of field; everything sharp (the background hang and vincenzo far behind are crisp).
- Mouths: static expression mouths only (STORY7 talk shapes dropped). Nobody speaks.
- Generic young painter: cast7 `young_painter` (stocky, dark hair, navy-striped shirt), no name anywhere on screen. Its anger_fill fx was
  dropped (it renders as a purple-magenta face fill, against the colour rule): a plain 'furious' face instead.
- Heads above y 880 in every frame (see below); main heads: set-up 2 inspector 0.56-0.57 H, set-up 3 0.49-0.54, set-up 4 painter 0.55-0.56.
- Dense set: the Salon Carré hang; runtime office dressing in shot 20 (table, papers, ink pot, lit storm lantern).
- set_mona(False) keyed on every frame (the empty wall with four hooks).

## QA numbers (work/qa.txt)
```
set-up 1 cop1    head w   64.. 110 px, x   -24..  701, centre y  715.. 765 (0.56..0.60 H); bottom below 880: none
set-up 1 cop2    head w   73.. 102 px, x   -31..  756, centre y  726.. 752 (0.57..0.59 H); bottom below 880: none
set-up 1 cop3    head w   42..  54 px, x   288..  637, centre y  696.. 712 (0.54..0.56 H); bottom below 880: none
set-up 1 guard   head w   89.. 107 px, x   448..  462, centre y  728.. 748 (0.57..0.58 H); bottom below 880: none
set-up 1 search  head w   66..  76 px, x    98..  140, centre y  730.. 742 (0.57..0.58 H); bottom below 880: none
set-up 2 cop     head w  191.. 253 px, x   -90..  820, centre y  706.. 738 (0.55..0.58 H); bottom below 880: none
set-up 2 guard   head w  132.. 150 px, x   622..  674, centre y  692.. 698 (0.54..0.55 H); bottom below 880: none
set-up 2 insp    head w  124.. 140 px, x   250..  250, centre y  720.. 730 (0.56..0.57 H); bottom below 880: none
set-up 3 cop     head w  151.. 168 px, x   514..  528, centre y  625.. 625 (0.49..0.49 H); bottom below 880: none
set-up 3 vin     head w   54..  56 px, x   207..  254, centre y  651.. 653 (0.51..0.51 H); bottom below 880: none
set-up 3 yp      head w  135.. 150 px, x   144..  178, centre y  676.. 688 (0.53..0.54 H); bottom below 880: none
set-up 4 vin     head w   71..  81 px, x   280..  540, centre y  663.. 670 (0.52..0.52 H); bottom below 880: none
set-up 4 yp      head w  255.. 296 px, x   141..  167, centre y  704.. 718 (0.55..0.56 H); bottom below 880: none
render: wall 16.91 s, cpu 32.99 s per frame (mean); by set-up {'1': {'wall': 17.13, 'cpu': 33.68}, '2': {'wall': 15.18, 'cpu': 30.34}, '3': {'wall': 18.08, 'cpu': 33.84}, '4': {'wall': 17.42, 'cpu': 34.26}}; retried: []
popcheck (g -> g+1, change): [(1918, 1919, 57.9), (1964, 1965, 59.5), (2004, 2005, 46.6)]   planned cuts: [1879, 1919, 1965, 2005]
near-still transitions (< 0.35 levels): [1919, 1963]
frame change median 3.45, max 59.55 levels
magenta / black frames: []
```
Pops are exactly the planned cuts.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s19 shot 19 (g 1879-1964)                      53.2   40.1    1.8    0.8    0.0    2.1    0.4    1.7  0.47 0.58 0.04   OUT: red,orange,blue,dark
s19 shot 20 (g 1965-2043)                      44.5   43.3    2.6    0.3    0.1    3.4    1.3    4.5  0.37 0.55 0.08   OUT: red,orange,blue,sat,dark
ref a t0045 t0047 (busy interior)              40.1   47.3    2.1    0.2    0.0    2.0    5.0    3.4  0.46 0.47 0.14   OUT: orange,blue
ref a t0013 t0051 (red interior)               51.4   33.6    0.5    0.1    0.0    7.7    3.7    2.9  0.54 0.46 0.16   OUT: red,blue,sat,dark
```

## Differences from the plan / known issues
- Shot 20 "louvre / closet (as an office)": the closet is a 5 x 3.6 D box with no depth behind the actors, so "vincenzo walks by in the
  background" cannot be staged there; it is the gallery's service-door corner dressed as an office instead (same location as shot 19).
- In set-up 1 the action is mid-ground (police ~50-100 px heads) — a wide; the red bench edge shows at lower left in the first frames.
- In set-up 4 the inspector is off-frame (camera-right) for the punch-in.
- Vincenzo is small in the background (head 54-81 px), as the plan wants "unnoticed".
