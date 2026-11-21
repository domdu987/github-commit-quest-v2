# QA-art R5: film 17 take s10 (THE REVEAL, g1336-1520, commit 669e44b, render17/team9): PASS

Reviewer: QA-art. This is the take gate for a key shot, and approval is delegated to QA.
Scope, as promised in R4: only P1 (card warmth, g1476-1520) and P2 (finger insert, g1406-1419). Nothing else has been reopened.

## How I reviewed
- I read `qa/phone_sheet.jpg` and `dir5.png` first.
- I extracted all 185 frames from the R5 `take.mkv`. It is byte-identical to `partaa + partab`.
- I extracted the R4 take (72847cc) from git for an A/B comparison.
- All 66 `f6/` frames match the take (mean |d| < 0.5).
- I built 360x640 finger strips (g1406-1419) and full-res crops, and a three-way card comparison (R4 g1510, R5 g1510, R5 g1490).
- I measured these myself: per-frame R4/R5 difference, steel/ink/pink pixel runs across the finger, raw RGB at the jaw/finger boundary, card paper RGB and luma, clipped pixels, shot mean, and the card ramp at g1474-1481.

## Nothing else changed
| Range | Mean \|d\| R4 -> R5 | Reading |
|---|---|---|
| g1336-1405, g1420-1475 | <= 0.61 | Encoder noise only. g1420 is 0.11 and g1475 is 0.42. |
| g1406-1419 | 49-53 | Re-render, as declared. |
| g1476-1520 | 2.0-2.8 | Post-only change, as declared. |

- The `post.py` diff touches only the `g >= 1476` block.
- The card exposure ramp starts at zero on g1476. Frame means go 1474 -> 1476 -> 1481 smoothly: (132,89,82) -> (134,89,81) -> (115,77,70). There is no pop.

## P1: card warmth, g1476-1520. PASS
These are my measurements. Region values are from x 110-330, y 540-600, paper pixels only (luma > 180). Global values are paper pixels with luma > 190 and S < 70.

| | R4 g1510 | R5 g1505 | R5 g1510 | R5 g1515 | Target |
|---|---|---|---|---|---|
| Paper RGB, region | (211,218,224) | (232,220,210) | (232,220,210) | (232,220,209) | |
| Paper RGB, global | (209,216,218) | (229,218,205) | (229,218,204) | (229,218,204) | (team: 229,218,205) |
| R - B | -13 | **+23** (global +24) | **+23** | **+23** | >= +10 |
| Paper luma | 217 | **223** | **223** | **223** | >= 220 |
| Pixels >= 248 | 0 % | **0.73 %** | **0.71 %** | **0.67 %** | < 1 % |
| Shot mean luma | 80.2 | 84.0 | 81.9 | 80.1 | ~76-82 |
| Top 200 + bottom 200 rows | 61.2 | 63.7 | 61.8 | 62.1 | unchanged |

- The team's numbers check out. Paper is RGB (229,218,205), R-B is about +25, luma 220-223 and 0.7 % of pixels clip. Each target is met with margin.
- Surroundings move +0.5 to +1.6 luma, which is unchanged in practice.
- **At phone size** (phone sheet g1501/g1516, my 360x640 comparison), the card now reads as warm cream paper. It is the warmest and brightest thing in a cool, dim frame, which is the reveal it needs. In R4 it read as cold grey-white.

Non-blocking:
- The clipped pixels sit in one area (x 301-417, y 488-608), which is the pool centre on the upper card just left of the name field. It shows as a faint pale-yellow sheen at full res. At phone size it is barely visible and reads as lamp light, so it can stay.
- The pale green bottle outline in the name field is still there (R4 note). It is barely visible at phone size.

## P2: finger insert, g1406-1419. PASS
| Requirement (R4) | What the frames show | |
|---|---|---|
| (a) Jaws close on the finger by g1417 and hold to the cut | **Met.** The steel-edge-to-pink gap closes from L 91 / R 56 px (g1408-1409) to **L 18 / R 18 px at g1415**, then holds at 17-23 px through g1416-1419 on rows y 600-720. It never reopens. In the raw pixels at g1416 and g1419 (y 660), the run from steel to pink is a gradient into **one continuous ink band** at (58,39,50), 9-12 px wide, then a gradient into pink. **No background pixel shows between jaw and finger** on either side. The jaw's outline and the finger's outline are merged into a single line. | PASS |
| (b) Fist and knuckles visible, finger rising out of a hand | **Met.** Dupont's fist with three knuckle lines sits under the finger in every frame, joined to his brown sleeve. | PASS |
| (b) Dark bin gone | **Met.** The bin is removed from the finger frames. | PASS |
| Preferred: push-in ~1.3-1.4x, beam >= 400 px, ear/eye mostly out | Done. The beam now spans x 0 to about 440-600. Dupont's eye leaves frame by g1414-1419, with only ear and cheek at the right edge. | OK |

**On the team's ~20 px argument.** I agree with it. My R4 spec asked for jaw tips within <= 4 px of the finger **outline**. Measured edge to outline, the gap is **0 px**: the ink lines touch and merge. The ~20 px "steel-to-pink" figure is just the two ink lines plus anti-aliasing. Getting it under 4 px would mean the jaws painting over the finger.

**Visually, do the jaws grip the finger?** Yes.
- **Full res (g1416 crop):** the two steel jaws press against both sides of the finger, with a 13-30 px strip of pink between them that narrows toward the beam. The jaw tips come down onto the top of the fist.
- **Phone size (g1414-1419 strip, `dir5` middle panel):** it reads clearly as a finger clamped in the calipers, coming up out of a fist. At g1406-1412 the shot sets up the action well: the finger stands free, the sliding jaw travels in, and then it clamps.
- **Mechanism clarity:** the insert has gone from "pink tube standing in a bin" (R4) to an obvious finger measurement.

Non-blocking:
- I cannot really make out Bertillon's "drawn hand holding the beam" at phone size. The left edge is mostly his head outline and some lines, with a small round form at the left end of the beam at g1406. It was not required, and the beam still reads as being held off-screen.
- The jaw tips overlap the top of the knuckles slightly. It reads as gripping at the base of the finger, which is fine.

## Scores (R4 -> R5)
| Area | R4 | R5 | Notes |
|---|---|---|---|
| Mechanism clarity (phone) | 7.5 | 8.5 | Finger 5 -> 8. Card and boxes as in R4. |
| Key image / beauty | 7.5 | 8.5 | The payoff card is warm and is the brightest thing on screen. |
| Light / colour | 6.5 | 8 | The pool tint is fixed (BGR). The paper is cream with R-B +23. |
| Camera | 8 | 8.5 | The finger push-in stops the shot pre-echoing the ear. |

## Verdict: PASS
Both R4 items landed as specified, and the frames outside them did not change. No issue left is one a viewer would notice.

Optional polish, none blocking:
1. Remove the green bottle outline from the card's name field.
2. Soften the small clipped sheen on the upper card.
3. Make Bertillon's hand on the beam legible, if there is ever a re-render.
4. Update QA.md: it says g1417-1419 are "identical", but they drift with the camera by a few px. The jaws do stay closed.
