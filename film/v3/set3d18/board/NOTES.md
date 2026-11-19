# Film 18 style board, round 2 (Jimo, 279 BC) after the QA-art FIX-FIRST (board/QA_ART.md, fixes 1-10)
Rebuild: `python3 jimo.py board` (jimo.py, jimo_tex.py [TEX_V j15], jimo_camp.py, jimo_ox.py, board.py, jimo_hue.py). Round-1 images kept in board/r0/.
720x1280, Cycles CPU, 12 samples, OIDN, no DOF, no text. Final render per still (4 threads): 7.7 s wall / 29.6 cpu (1), 6.7 / 25.7 (2), 11.9 / 45.9 (3).
Debug helpers: `JIMO_CAM=x,y,z,lx,ly,lz,lens JIMO_OUT=/path.png python3 jimo.py still holes draft`; `jimo.px(world_point)` -> pixel on the current camera.

## What changed (by QA fix)
1 wall: ochre-loess albedo `#b8874e`, joints `#8e6438` 0.12 D tall, stains, runnels, repaired patches (texture + proud patch blocks); moon key now blue (0.24,0.42,1.18), key_desat 0.55, warm light only as pools around torches.
2 sky: bible night gradient `#1e2e7b` -> `#1748ae` -> `#204c8f` with a low violet band, cool clouds `#8fa0d8`, blue moon halo `#5a8af5`-ish (bloom size 0.12, strength left at 0.5, see "not met").
3 flames: `jimo.flame()` layered tongues (outer `#b8301a`/`#e8561c`, mid `#ffb238`, core `#fffeec`), arranged by camera direction so the layers show, embers, fire light (1.0,0.50,0.18); used by braziers, camp fires, ox tails.
4 board 3 darker/colour: key and ambient lowered, p50 luma 0.30.
5 hero ox (jimo_ox.py): lofted barrel with deep chest, hump, dewlap, short legs with hooves, low head with ears and eyes, horns with lashed flat bronze blades (~0.7 D, not 0.5: 0.5 read as a stub), draped crimson silk with big painted dragon + five-colour clouds + gold scalloped hem, raised reed-bundle tail with a streaming flame.
6 board 3 restaged: OUTSIDE view (moat omitted, the oxen run on open earth) at 1.0 D, three oxen, lead ox about 40 % of frame height at about 40 deg to the wall, ragged breaches (stepped broken courses, clods, raw timber props, slumped lintel, rubble fans), dust, flying clods, glowing lit lane and Qi stand-ins + drums behind, fallen ladder, spades, mattock, baskets, reeds. No mallet, no torii frames.
7 caption band: bridge lamps removed from the foot (board 1); near fire pit lifted and table/cups cleared (board 2); hooves of the lead ox at y 950-1000 (board 3).
8 period dress: two-stage plain hall, dark-lacquer posts, grey tile hip roofs with near-straight eaves and wadang, no horns, no paper lanterns; bronze standing oil lamps and tripod braziers; timber ramp; plain banners; shields on crenels.
9 camp: lens 16.5 so both tents are whole; stand-in soldiers (3 seated drinking at each of two fires, 2 toasting at the table, 1 asleep, 3 guards), stone-ringed fire pit with ash, no red disc.
10 wall detail: stains, rain-streak cards under the parapet, patches, ropes, ladders, repair scaffold, ramp, guards, far roofs with lit windows.

## Before / after (before = QA_ART table or r0 measured the same way; after = this build)
| metric | target | before | after |
|---|---|---|---|
| sky 100-300, board 1 | `#1e2e7b`..`#1748ae`, H 221-230, S <= 0.85 | `#100085` H247 S1.00 | `#1b3b8a` H223 S0.80 |
| sky board 2 | same | `#0b007f` H245 S1.00 | `#1f3882` H225 S0.76 |
| sky board 3 (top band) | same | `#350b8b` H260 S0.92 | `#1a3a85` H222 S0.80 |
| top-eighth luma b1 / b2 / b3 | 40-90 | 17 / 15 / 64 | 56 / 54 / 58 |
| wall median b1 (y 700-1030) | blue moon-shade, H 230-255 | `#d58484` H0 S0.38 V0.84 (all lit pink) | `#5d588a` H246 S0.36 V0.54 |
| wall share at H 230-255 b1 | >= 55 % | about 0 % | 69 % |
| wall fire-lit warm pools b1 | `#c07a3c`..`#a86a38`, V <= 0.75 | `#b9777d` V0.73 salmon | `#9e7995` H315 (NOT ochre, see below) |
| wall b3 | ochre lit / blue shade, no magenta | `#e5967a` lit, `#8d687c` H328 shade | `#80595f` H351 dusty rose-brown (NOT met) |
| flame body `#ffff00` px b1 / b2 / b3 | 0 | 2886 / 11643 / 19238 | 1 / 11 / 18 (core bloom only) |
| luma p50 b1 / b2 / b3 | b3 <= 0.34 | 0.31 / 0.32 / 0.48 | 0.26 / 0.23 / 0.30 |
| luma p1 b1 / b2 / b3 | 0.08-0.12 | 0.055 / 0.055 / 0.078 | 0.084 / 0.081 / 0.082 |
| mid-band luma (0-255) b3 | 100-120 | 145 | 102 (b1 100, b2 82) |
| violet % b1 / b2 / b3 (hue_report) | <= 6 | 15.4 / 12.7 / 8.3 | 3.2 / 7.4 / 3.4 |
| magenta % b1 / b2 / b3 | <= 8-10 | 5.0 / 6.1 / 14.0 | 2.6 / 1.9 / 18.3 (b3 NOT met) |
| b3 red+orange % | 45-55 | 57.4 | 40.9 (NOT met) |
| b3 blue+violet % | >= 30 | 19.6 | 39.0 |
| caption band 880-950 mean luma (0-255) b1 / b2 / b3 | 60-110, no bright emitters | lanterns, fire root, hooves+mallet; bright px >0.7: 1735 / 13277 / 119 | 83 / 71 / 63; bright px: 3 / 0 / 200 (b3: glints of the lead ox's rubble and hooves) |
| wall Canny edge density b1 / b3 | >= 0.05 | 0.079 / 0.029 (old wall was pink noise) | 0.048 / 0.011 (b3 NOT met: wall is far and blurred) |
| featureless 40 px block share b1 / b3 | <= 0.30 | 0.11 / 0.47 | 0.25 / 0.82 (b3 NOT met) |
| shade hue (jimo_hue, 240-260) b1 / b2 / b3 | 240-260 | 245 / 245 / 251 | 230 / 235 / 231 (SHADE-OUT: the bible sky H 221-230 is counted as shade) |

## Not met / open
- b3 wall: any warm light on blue ambient makes dusty rose (H 330-350), not ochre; removing the blue ambient makes it brown-rose and loses the blue night. Needs a per-material warm/cool split (fire-lit albedo ochre, ambient blue only in the unlit part) in the full set.
- b3 red+orange 40.9 % (target 45-55), magenta 18.3 %, wall edge density and featureless share (the wall is large and soft at that distance; needs bigger-scale stains/courses or lower camera nearer the wall).
- b1 wall fire-lit pools are lavender-pink (H315), not ochre, for the same reason; the moon-shade part meets the target.
- Moon bloom: strength fixed at 0.5 in tower.setup_grade (bloom size 0.12 used); not 0.20 / 1.0.
- Ox is a chunky stylised placeholder: head-on it still reads a little like a pig, dragon silk is readable only in a close shot, hind legs thick; blades 0.7 D.
- Board 3 is an outside view without a moat (the brief said inside); board 2 sleeping soldier is a crude lump; soldiers are low-poly stand-ins, not the 2D cast.
- hue_report SHADE-OUT on 1-3 (see table).
