# QA s03 (team 4): BIGZOOM 1 part B, g 192-323 (+6 handle frames each side, file g 186-329, 144 frames)
take.mkv is split (`cat take.mkv.part* > take.mkv`, libx264rgb crf 6, 30 fps, 720x1280).

## What is in it
- Starts on the s02 end framing (J2): the iron grille with the SAME geometry as beck_london (7 bars, 3 cross bars, frame, rivets, warm plane under it, lamp halos), the pill-tile plate is hidden. The camera is tilted 3 degrees from straight down (a vertical look-at made the roll spin).
- Dive through the grate and down the brick shaft (the shaft ribs/ladder are hidden: their repeating rungs aliased at speed), then the noodle-tunnel KNOT seen from OUTSIDE the tubes (camera about (GX-13, GY-8, -32) looking at the knot) for about 0.7 s: tubes in red/yellow/green/blue with lit trains and round signal lamps (the fan-shaped halo quads are hidden and replaced by round glow spheres); then the dive into the straight tunnel (lamp string of round lamps), out of the tunnel mouth onto the platform and along it.
- 9.3 s (local 90): MEDIUM on old_gent squinting at the OLD map with the magnifier (about 38 % of the frame height; sway variants), pass_man (mirrored, so he comes from the right) bumps into him from 9.81 s (pose 'bump', hat askew), pass_woman unfolds her map far right; the camera slides and pushes on to the OLD map.
- OLD map: moved down 1.2 D (vault no longer cuts it, title MAP OF LONDON fully in frame, not cut at the end), light-tinted by multiplying its texture to the cool lilac-grey of the lodgings map (measured: s03 end map RGB 141/139/157 hue 248; s04 start map 147/142/167 hue 252). The map is 80-100 % of the frame width at the end (>= 12 %).
- Platform crowd near the camera path hidden, two cast22 walkers (walk cycle) pass in the distance; no vending machine in frame.

## Numbers (take.mkv)
```
STATS
take.mkv       dur   4.8s shots   1 mean 4.80s med 4.80s <1s  0 >4s  1 | sat 0.731 vivid% 72.6 luma  95.2 contrast 31.9 detail 6.12 warm 18.4% cool 69.4% | motion med 10.81 p90 23.94 still%  0.0
JITTER
0s shake  10.5px
  1s shake  10.2px
  2s shake   7.2px
overall median jitter px 4.83
AUTO
# QA_AUTO FAIL  (take.mkv, 144 frames, 30.00 fps, g 186-329)

## FAIL
- suspected blur on 46 frames, e.g. g [186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200]
## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.
GROUND RESULT: PASS (0 failures)

```
- Required: sat >= 0.50 (0.73), vivid >= 45 % (72.6), luma 85-110 (95.2): PASS. Frame diff median >= 4 / p90 >= 12: PASS (10.8 / 23.9).
- Heads above y 880 on the platform frames (phone sheet): PASS, old_gent's chin at about y 860 on the last frames; nobody is cut by the bottom edge.
- Section K: GROUND.md = PASS (mounted flags on the set pieces seen touching: vault ribs, globes, hang signs, clock, liner, WAY OUT panel, posters, OLD map frame, columns; glow quads and the noodle tubes/trains flagged airborne; the vending machine is hidden as it is never in frame). Cards have contact shadows.

## FAILS / open items (honest)
1. **qa_auto FAIL "suspected blur on 46 frames"**: the flagged frames are g 186-200 (grate plates with flat orange fills), the plain navy/blue tunnel frames (about g 236-262) and the tube-wall crossing. They are low-detail (flat colour) not blurred: no depth of field, no motion blur, the edges are crisp at 720x1280 (see phone_sheet.jpg). The set has no texture in those areas; I did not add noise.
2. **qa_jitter (section L) FAIL in seconds 0-2: 10.5 / 10.2 / 7.2 px** (overall median 4.8 px; the rest of the take is below 2 px). This is the s03 dive: the camera moves 30-90 D/s through the grate, the shaft and the tube walls, and the frame content changes completely between frames, so the phase-correlation tool reports large translations (up to 900 px at the frames where the camera crosses a bar or a tube wall). The camera itself is smooth: I replaced the Hermite keys by a Gaussian-smoothed path (sigma 3 frames, no velocity overshoot, max speed 90 D/s, max acceleration 0.46 D/frame^2, down from 245 D/s and 6 D/frame^2 before) and removed the roll spin; the remaining measurement is the geometry flying past the lens, not shake. I could not get it under 2 px without slowing the BIGZOOM dive, which does not fit the 4.4 s window (BIGZOOM 1 is 3.55-9.30 s). Director: decide if the metric is waived for this take or the dive is to be shortened/slowed with a longer take.
3. J2: the grille geometry is the same as london's; the first frame is the s02 end key (8, 18.7, 6) with the look tilted 3 degrees, so if team 2's last frame is exactly straight down use a 4-6 frame dissolve.
4. J3: the end frame is the OLD map (grey-lavender) large with the title in frame; team 1 starts s04 about 25 % closer; use the 9-frame eased match dissolve.

## Colour (film/COLOUR_SPEC.md, film/v3/tools/hue_report.py `stats` on every 3rd final frame, caption band excluded)
```
set     red orange yellow  green   cyan   blue violet magent   sat  val dark | target red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15
s03     12.6    8.2    2.3    1.0    0.6   61.9    4.6    8.8  0.73 0.68 0.00   OUT: red,orange,blue,sat,val,dark
s09      1.8    3.1    1.0    0.1    0.7   71.4    9.9   11.8  0.66 0.57 0.00   OUT: red,orange,blue,violet,magenta,sat,dark
s10      6.2    7.9    1.8    1.2    0.2   58.5    6.5   17.8  0.68 0.59 0.01   OUT: red,orange,blue,violet,magenta,sat,dark
```
Underground shaft/tunnel/platform: deep blue-violet tunnel by design (QA_ART carry-forward rule 5, tunnel stays near-black navy), lit only by amber lamps and the tube colours. Hue shares blue 62 %, red 12.6 %, orange 8 %; sat 0.73 (target 0.38-0.48). Over-blue and over-saturated against the new spec; unlit-cast/blue-violet shade is as asked, but warm light is below the band. Not graded by team 4 (the director applies the v1.1 grade). The set light presets (UNDER/HALL) are the cause; a per-take re-light (more warm key, less blue shade) would be needed to reach the bands and was not done. The tool itself could not run its reference rows here (the reference clips are not in this container).
