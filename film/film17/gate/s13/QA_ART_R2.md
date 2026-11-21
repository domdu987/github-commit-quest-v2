# QA-art R2, film 17 take s13 (ENDING, shots 31-33, g1862-2051, hard cut g2052): FIX-FIRST (1 blocking fix + 1 same-pass cleanup)

Reviewer: QA-art (opus), round 2. The client delegated approval to QA, so this verdict decides the take.
Material reviewed: phone_sheet.jpg; full/g1917, g1987, g2007, g2030, g2050; f6 frames (every 5th frame, plus the cut strips at 1944-1950 and 2011-2017), checked at 180 px and 360 px width and with an ear crop at full res for g2017, g2032 and g2047.
Numbers: rhythm 4.45 / 12.58 (target >= 4 / >= 12), so it passes. qa_auto PASS.
Director ruling applied: shot 33 does not have to match shot 3 geometrically (frontal shot, vertical bar). It only has to read instantly as "calipers measuring the inspector's ear".

## Round-1 fixes, checked one by one
| R1 fix | Status | Evidence |
|---|---|---|
| 1. Shot 33 jaws on the INSPECTOR's ear, not prisoner_b | **Mostly done** | The jaws now point at the inspector's screen-left ear, and prisoner_b is gone. This is the big win: the last frame points at the right man. **But the jaws never close on the ear.** The gap between the jaws is about 200 px, while the ear is about 120 px tall. The lower (slider) jaw touches the bottom-left of the ear, and the top jaw floats about 60-70 px above the ear's top (g2030: top jaw y ~420-440, ear y ~500-600; g2050: top jaw y ~345-375, ear y ~440-560). The slider does not move from g2017 to g2047. At 360 px it reads as "an open caliper held up beside his ear", not "his ear clamped". See Fix 1. |
| 1. Slit-eye frame removed in shot 33, moustache twitch added | Done | g2014-2047 keep round, wide eyes with pupils slid toward the caliper. The twitch is there. |
| 1. Bertillon's cut-off head disc out of shot 33, hand in its place | **Partly done** | His dark sleeve, cuff and hand on the bar come in from the left, which is good. But a white head sliver with glasses still sits at the top-left edge in g2017-2032 (x 0-60, y 180-420), and it is only a dark arc by g2047. Minor, and it can go in the same pass as Fix 1. |
| 2. Shot 32 measuring visible, Bertillon not in front of the face | Done | Bertillon stands camera-left and clear of the inspector. The caliper bar is about 250 px long and vertical, and its jaws arrive at ear height over g1960-2000. The inspector's pupils slide toward the instrument. The grey stub over the eye is gone. g2007 is a normal blink (1-2 f), which is fine. |
| 3. Shot 31 calipers in Bertillon's hand, grey blade gone | Done | In g1917 the calipers are at his waist, clear of every face. No blade at the gendarme's mouth. |
| 3. See-through skirt and ghost leg | Done | The legs are opaque in g1917 and g1952-1972. No wedge. |
| 3. Opening slabs in shot 31 | Done | The coat rack and camera-hood slabs are gone. The foreground is the kepi stool, which slides out. The room and the red face own the opening. |

## Other items
- **Shot 32, tripod hood at the top-left in g1947-1965 (team note):** confirmed. It covers about 20-25 % of the width at the top-left for about 0.75 s right after the cut, then slides out. It is dark dead mass, but it sits in the corner, away from the subject: the eye lands on the centred red face on the cut. **This does not block on its own.** See Fix 2.
- **Shot 33 foreground:** the orange chair arm with its yellow cap fills the bottom 15-20 % in g2014-2032, then the push removes it. Acceptable.
- **Callback to shot 3:** shot 33 is frontal, not raking. This is accepted per the director's ruling. The echo still comes through the caliper silhouette at the ear plus the push-in. A real clamp (Fix 1) is what makes the echo land.
- Comedy and acting are now good: laughing gendarmes with tears, the deadpan prisoners, the sweating, stiff inspector, and eyes that slide to the instrument.

## Scores (1-10), R1 to R2
| Area | R1 | R2 |
|---|---|---|
| Ending punch / clarity at phone size | 3 | **6** (right ear, right man; the clamp is not there yet) |
| Comedy / acting | 5 | 7 |
| Set density | 7 | 7 |
| Light / colour | 7 | 8 |
| Composition | 4 | 7 |
| Camera energy vs film 2 | 7 | 7 |

## Verdict: FIX-FIRST (one shot only: 33, plus an optional cleanup in 32)
Everything that was broken in R1 is fixed except the payoff action itself. The final image shows a caliper next to the ear, but the caliper is not measuring it. The joke is that HIS ear gets measured, and the last 1.2 s of the film must show the jaws biting the ear. This is a small animation fix on one shot, not a re-stage.

### Fix 1 (blocking): shot 33 (g2014-2051), close the jaws on the ear
- Lower the caliper about 60 px (or move the fixed top jaw down) so that the top jaw tip rests on the top of the ear.
- Animate the slider (lower jaw, the one with the gold screw) upward over about g2020-2028, until it seats on the bottom of the ear. The final jaw gap should equal the ear height (about 120 px at g2050 scale), with both tips overlapping the ear by about 20-30 px horizontally (tips to about x 260-280), so they pinch the ear rather than sit beside it.
- Put the moustache twitch (g2027-2034) right on the contact frame, so the clamp and the reaction read as one beat.
- Keep the framing, the push x1.4, the eyes, and the hard cut at g2052.
- In the same pass, slide or hide Bertillon's head sliver at the top-left edge (g2017-2032).

### Fix 2 (cleanup, same re-render only): shot 32, tripod hood
- Hide the camera/tripod-hood object for the shot 32 set-up, or trim it so it is out of frame by g1950.
- If this would cost a separate render round, skip it. It does not block shipping.

Re-check: phone sheet + full/g2022, g2030, g2050 (and g1950 if Fix 2 was done). If the jaws visibly seat on the ear at g2030 and g2050, it's SHIP with no further round.
