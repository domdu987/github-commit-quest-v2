VERDICT: PASS (with notes) -- both v2 blockers are fixed. 1) Every card now faces screen-RIGHT, the way the clump travels and recedes, and the same way as the s24 matriarch, so there is no moonwalk and no direction flip at the cut. 2) No hard-edged khaki rectangles are left in the dust, and the yard no longer shows through the rear elephants. All v2 passes still hold. The faint dust veil and streaks over the rear elephants are acceptable at phone size (note 1).

# QA_RECHECK s25b v3 (film 14, shot 25, g1672-1770, 99 frames, first_g 1672, n = g - 1672) -- TAKE gate, round 5

Method: all 99 frames decoded to scratchpad/qa_s25bv3/all. 6 fps sheets (every 5th frame):
- phone sheet at 180x320 with the y 880 line drawn in (sheets/phone.png)
- half-size strips (sheets/half_01..04.png)

Herd zooms at 2x to 4x around g1690, 1720 and 1750:
- sheets/g1690_top.png
- g1720_herd2x.png, g1720_rear3x.png and g1720_rear4x.png
- g1750_herd2x.png and g1750_rear4x.png
- patch_n20_45_70_98.png

Measurements:
- frame-diff over the whole frame
- an elephant-colour mask (area, extent, luma)
- a column scan through the rear bodies across the horizon line, looking for yard showing through
- a track of the purple pebble, for camera motion

Continuity (sheets/continuity.png):
- s20 take g1677, the end of s24 (conform/takes/s20, n376)
- s25b g1678 and g1763
- s26 take g1764 (conform/takes/s26, n6)

## The 2 v2 blockers, re-checked
| v2 blocker | status | evidence |
|---|---|---|
| 1. Moonwalk: the cards face left while the herd moves right, and the screen direction flips from s24 | FIXED | Every card faces screen-right: the heads, eyes and trunks are on the right and the tails trail on the left (g1690, 1720, 1750 zooms). The clump's centroid goes x 415 -> 517 (g1672-1714) while it shrinks, and is then roughly steady at x 488-515 as it recedes toward its vanishing point. The late drift of about -0.5 px/frame cannot be seen against the scale-down. On the phone sheet it reads as a herd running right and away. |
| 2. Hard-edged khaki rectangles in the dust, and a see-through rear elephant | FIXED | No flat or hard-edged quads appear anywhere in the herd and dust region at n20/45/70/98 or in the 6 fps strips. The dust now reads as soft streaks and wisps. A column scan through the rear bodies at g1720 and g1750 (x 560-700, y 455-495) stays blue-grey (g-b about -15 to -25) straight across the horizon line at y about 471-479. The khaki yard (g-b > 0) does not show through. It shows only below the bellies and between the legs, where it should. |

## v2 passes, confirmed
| check | status | evidence |
|---|---|---|
| No turn pop | PASS | The herd is already running at g1672. Frame-diff is 3.1-4.9 over the whole shot, with no step above 5.5. |
| No dead air | PASS | The herd is on screen to g1770. At the end it is a legible clump about 300x120 px. |
| The herd recedes away from the fence | PASS | The camera is inside the fence looking out, and the fence is not in frame. The mask area goes 275k -> 25k px, i.e. linear scale about 1.0 -> 0.3, while the clump rises toward the horizon (y about 480). |
| Night tint | PASS | Elephant luma is 56-62, below the lit soil at 72-76. The sky is the same cool periwinkle as v2 (RGB about 112/103/220). |
| No blotches or yellow patch | PASS | There is no bottom-left yellow patch and no loose card-shadow blotches. Only the soil footprints remain, and they move with the ground (note as in v2). |
| The camera moves | PASS | The foreground pebble travels x 564 -> 405 and y 756 -> 817, steadily, with no static run. |
| Heads above y 880 | PASS | The herd's lowest pixel is about y 620, inside the grass. The heads are at y about 60-470. |
| No text | PASS | No text, numbers or watermark appear in any frame. |

## Continuity
- **IN (s24 g1677 -> s25 g1678): PASS.** The s24 matriarch faces screen-right, and so does the s25 herd, so the cut keeps the screen direction. Carried over from v2 as a note only: s24 has a deep indigo starry sky and a dense bee cloud, while s25 has a flat lighter periwinkle sky and sparse bees.
- **OUT (dissolve from about g1760 into s26 g1764, dawn farm): PASS.** The herd is small on the horizon and the dissolve is soft.

## Team claim: "a few faint dust streaks still cross the rear elephants" -- ACCEPTABLE at phone size
- At 3-4x the rear 3-4 elephants sit under a warm-grey dust veil plus thin streaks. Inside that veil, the card-on-card overlaps are faintly visible. At g1720, the legs of the middle rear elephant show through the rump of the right-hand one.
- At the phone sheet scale, the rear group reads as a hazier grey mass "in the dust" behind the two solid front elephants. That supports the depth and the "fleeing in dust" idea. The yard does not show through, and no edges or rectangles are visible.
- Not blocking. If there is a later pass, raise the rear cards' alpha to 1 under the veil.

## Notes (not blocking)
1. Rear-elephant veil: see above. The optional fix is solid rear cards with the dust on top only.
2. From g1672 to about g1735, the leading heads and the rightmost elephant are cropped by the right frame edge. This is acceptable, because the herd runs out toward the right, and from about g1740 the whole clump is in frame.
3. A small hard-edged red rectangle on a rail sits at x about 670-700, y about 510-530, from about g1715. It moves with the set and reads as a hive or sign on the horizon, not as an artefact. It is about 7 px wide on a phone.
4. The cards are 3/4 views with faces toward the camera rather than rumps. This is acceptable: the facing matches the travel and the shrink sells "away". The v2 optional idea of rump cards late in the shot still applies.
5. Sky and bees vs s24: same as v2 (darken the sky toward indigo, add stars, and more bees early).
6. Footprints: the darkest soil print under the caption band could be softened (same as v2).
