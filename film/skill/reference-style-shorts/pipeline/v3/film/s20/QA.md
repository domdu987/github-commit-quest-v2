# QA: take s20 (shot 20, the corridor view and the launch), hand-drawn red line

- **Frames.** Film g 1419-1515 (97 f) plus handles 7 in (g 1412-1418, dissolve 9 f) and 7 out (g 1516-1522, dissolve 10 f):
  111 final frames `frames/g_%04d.png`, 720x1280, 12 samples, office_grey, all rendered 18 Nov after 16:40 with the
  HAND-DRAWN line (set TRACK_STYLE "hand"; no other version of the line exists in this take).
- **Code.** `shot.py` (take), `mc.py` (scene, camera grammar and render loop shared by s20/s21/s22, copied from film/s19/shot.py),
  `post.py <take>` (contact, meta, popcheck), `sheet.py` (draft strips). No shared module was edited.
- **No characters.** No mouths, no backs, no pinned hand props (no registration needed).
- **Continuity with s19.** Same scene build, walls locked, lane lit (glow 0.22 = s19's last value), chalk crumbled (alpha 0.45),
  spinner at u 0.17 where s19 leaves it, both pictograms where s19 popped them.

## Camera (numbers in work/probe.txt)
| phase | frames | camera | numbers |
|---|---|---|---|
| corridor view, creep 6 %/s (accelerating) | 1412-1443 | lens 0.35 D up, 0.15 D west of the chord (clear_lateral, as s19), u -0.115 -> -0.09, looking up the corridor | spinner 362-393 px at (420-435, 1145-1200); N.Y. at (381, 647); sign 177-184 px far ahead |
| launch (snap 47.95-48.45) | 1443-1467 | the lens rides 0.255 u behind the flung spinner ALONG the line (lens at M.world(a, u_lens(t)), a from the clear lateral to -0.035 by u 0.05, i.e. inside the lane before the walls begin), 5 Hz shake decaying | 0.46 u = 0.50 D of travel in 1.1 s; spinner stays 340-390 px at the bottom while it pulls away |
| brake to rest (Hermite) | 1467-1484 | from the follow speed to rest beside the speed sign, look turns to the sign | sign 380-420 px at y 260-370 |
| push, decaying shake | 1484-1522 | u_lens 0.36 -> 0.39 (decelerating) | sign 420-435 px across (scale 0.52 = 0.135 D), centre (360-420, 315-365): above y 600 as asked, read 49.2-50.3 |

- Lens clearance: in the lane (|a| 0.035 from the LINE) whenever u > 0.05; the sight line to the sign clears the bent east face
  (M.sight_margin >= 0.026 D for every lens u 0.25-0.40).
- Corner speed (work/motion.json): static runs none, linear runs none (creep accelerates, launch/brake are eased). Peak 223 px/f
  at g 1470 (a map point passing beside the lens at the end of the launch).
- **Popcheck** (post.py): 111/111, none missing, no pop flags, no black or magenta frames; largest diffs g 1455-1456 and 1477-1480
  (the launch snap and the sign spin, planned).

## Events (cues.json)
Gust waves 1425 / 1434 / 1443 (wind arrows 1/3, 2/3, all); the first two gusts flap the two no-turn pictograms and fold them back
into the wall faces (1424-1438: the lens flies past that spot); the third gust squashes the spinner flat (1440-1443), launch 1443:
it rockets north tall and leaning forward (squash 1.47 -> 1.12, wobble 16 deg, motion-blur disc) with the red-hot wake; it swerves
0.04 D west past the sign's pin and passes the sign at 1476 (49.10); the sign spins two turns in the wake (ease-out, 22 f), rocks
+-9 deg and settles on '100' at 1512 (50.30). The spinner runs on to u 0.985 (N.Y.) by 1500.

## Colour (hue_report.py frames)
`s20/frames  red 11.5 orange 19.3 yellow 0.0 green 0.0 cyan 0.1 blue 61.8 violet 0.6 magenta 6.7 sat 0.36 val 0.49 dark 0.11  OUT: red,orange,blue,sat`
A map-only office_grey shot like s19, but closer: the pale blue-grey pressure walls fill most of every corridor frame, so blue runs
far above the band and red/orange under it. Violet 0.6, magenta 6.7 (shade reads blue, not magenta); value and dark share in band.

## Changes from the plan / API (and why)
- Speed sign: NOT above the wall tops (API default height 0.62 D). From inside the lane that framing looks up into the ceiling and
  lamps and loses the corridor (tried, draft rejected). The disc rides at 0.42 D (below the 0.50 D wall tops), post at a +0.04 D
  (roadside of the lane, inside it: at a +0.085 the disc cut into the east wall face), scale 0.52; the post is moved behind the disc
  (local y +0.012) so it does not cross the '100'.
- Pictograms fold away at the first two gusts (otherwise the lens flies through them); s21/s22 keep them hidden.
- The sign is 420+ px rather than 300 px (more readable; plan asks 300 or more).

## Known
- Far behind the sign the Thai label is seen upside down and mirrored (the corridor camera's up is the wall normal; small, far,
  as in s19's corridor view).
- This take's final render ran at the same time as s21's (my render chain's wait failed and started s21 at once): two render
  processes for about 50 minutes instead of one. No effect on the frames.

## Cost
Wall 15-56 s per frame (median 39 s), CPU 26-37 s (median 30 s), 2 threads, machine load 10-12.
