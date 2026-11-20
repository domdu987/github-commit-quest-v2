# QA-art s19 (oxen burst out of the wall holes, 47.56-50.51 s), TAKE gate round 8 — FIX-FIRST (reveal, strict)
I reviewed take.mkv at 6 fps (art11/f/NNN.png, g = 1421 + 5*(NNN-1)) at full size 720x1280 with a y 880 line (art11/h1.png, h2.png) and on art11/psheet_1-3.jpg (360x640).

## Earlier changes
1. Lift the herd out of the caption band: NOT met. The oxen are much bigger now (25-40 % of height), which is good. But their heads still cross y 880 in almost every shot frame. Measured on rendered frames: g 1431 mouth bottom about y 905, g 1456 about y 930, g 1466 about y 950, g 1486 about y 990, g 1496 about y 960. The captions "วัวพันกว่าตัวพุ่ง / ออกจากรู / ตรงเข้าค่ายเยียน" will sit on their roaring mouths.
2. Flames at phone size: DONE. The near flames are now big red/yellow teardrops that read on the phone. But see the new problem below.
3. Fg prop: Partly done. The warm pots and jars only appear at the whip landing (g 1506-1520). There are no clods or rubble in the lower-left during the shot.

## New problems
- **Flame over a face, g 1471 (f/011.png):** The flame of the ox behind sweeps across the lead ox's face (x 250-500, y 760-840). This breaks rule 3 and reads on the phone as a fire-breathing ox.
- **Purple strip is back:** A flat saturated indigo diagonal band runs from the bottom edge toward the horizon at g 1421-1501 (f/001-017). The render team could not find its source. On the phone it reads as a purple carpet. I had marked this DONE in round 8, but it is visible again in this take.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 7 | 6 | 5 | 7 | 7 |

The burst reads: rage-faced dragon oxen pour out of the broken wall with dust and fire, and the motion is energetic (median 12.6, p90 16.2). The caption-band overlap and the face flame are what still break it.

## Verdict: FIX-FIRST
1. **Heads above y 880 (whole shot):** Pitch the camera down another 5-6° (horizon and hole row to about y 0.45-0.50), or raise it about 0.4 D while keeping the look-at, so that the lowest mouth pixel of every ox is at y 860 or above. Measure it on rendered frames at g 1431, 1456, 1466, 1486 and 1496, not from the rig.
2. **No flame within 60 px of any ox face:** Fix g 1466-1476 by delaying or offsetting the ox behind the lead ox, or by shortening its flame card while it overlaps.
3. **Purple strip:** If no object owns it, it is most likely the long cast shadow on the ground lit by the blue sky/world colour. Try disabling shadow casting on the wall-top or ladder objects, or lay a warm-earth decal/plane over that region. The bottom of frame must show no flat indigo band.

## Notes
- The pots at the whip landing are nice. The same props sliding in the lower-left through the shot would cover change 3 of the last round.
