VERDICT: FAIL -- 1) the herd faces screen-LEFT but its whole clump slides screen-RIGHT as it shrinks (a moonwalk), and it faces the opposite way from the shot 24 matriarch, so "flees away" does not read cleanly; 2) hard-edged pale-khaki rectangles show inside the dust and through the rear elephants (g~1690-1770), and the rearmost elephant reads see-through. Fixes are below. Both are cheap: mirror the cards, and remove or hide the khaki quads.

# QA_RECHECK s25b v2 (film 14, shot 25, g1672-1770, 99 frames, first_g 1672, n = g - 1672) -- TAKE gate, round 4

Method: all 99 frames decoded to scratchpad/takes/qa_s25bv2/all. Phone sheet: every 5th frame at 180x320 with the y-880 line drawn in (sheets/phone.png). Full-size frames n0/15/45/98 (sheets/four.png). Zooms on the herd at n5/12/20/30/45/70/98 (sheets/n45_herd.png, n98_herd.png, patch.png, patch2.png). Frame-diff over the whole frame and the soil band. Phase correlation on three bands. The soil band was cross-checked by eye against the purple pebble and the footprints (sheets/soil_0_49_98.png). An elephant-colour mask gave the herd area, bbox, centroid and luma per 6 frames. The lantern-post exit was checked frame by frame (sheets/post_exit.png). Continuity: s20 take r26 g1677 (end of s24) and s26 take r24 g1764 (sheets/continuity.png).

## The 3 earlier blockers, re-checked
| earlier blocker | status | evidence |
|---|---|---|
| 1. Turn pop (g1683->1684) | FIXED | There is no on-screen turn: the herd is already running at g1672. Frame-diff is 2.9-6.4 over the whole shot, with no spike. The highest steps are 6.36 at g1679 and 6.27 at g1673, which is ordinary gait motion. The lantern post slides out to the left smoothly (g1694-1703). |
| 2. Dead air, and the herd running along the fence | Dead air FIXED. Direction only PARTLY fixed (new blocker 1) | The herd stays in frame to g1770. Mask area 220k -> 15k px, i.e. linear scale about 1.0 -> 0.26, with the bbox at the end x 327-639, y 414-537. That is not a dead frame. The fence is no longer a background line it runs along. But see blocker 1. |
| 3. No shadows at the feet, stray blotches, yellow patch | The big loose card-shadow blotches are FIXED. The bottom-left yellow patch of v1 is FIXED. A new hard-edged khaki patch is in the herd (blocker 2) | The lower soil now shows paired dark ovals in a trail plus long grass shadows. They move with the ground and read as footprints, not stains (note). The feet are hidden by the grass line throughout, so nothing hovers. |

## Checks
1. **Story read at phone size: FAIL (blocker 1).** Shrinking with a dust trail says "going away". But every card faces screen-left (3/4 profile, faces and eyes toward camera-left), while the clump drifts screen-right:
   - the left edge of the herd goes x 15 -> 327
   - its centroid goes x 361 -> 445
   On the phone sheet this reads as elephants running left while sliding backward to the right, toward the vanishing point. That is a moonwalk, not a herd fleeing away. Shot 24 also ends on the matriarch facing screen-RIGHT, so the cut flips screen direction.
2. **No pops: PASS** (see the table).
3. **Grounded: PASS.** The feet are always behind the grass line, or on the khaki yard band at the horizon with the grass in front, so none reads as floating. The hidden ellipses are acceptable.
4. **No stray blotches: FAIL (blocker 2).**
   - Hard-edged pale-khaki/yellow rectangles of about 20-35 px sit in the dust behind and inside the rear elephants. They are at about x 600-700, y 470-545 and appear from about g1690 (n20, n45, n98 zooms).
   - The rearmost elephant's lower body and legs are see-through: the yard plane and those rectangles show through it (n70, n98). It reads as a ghost elephant, not as an elephant behind dust.
   - The soil footprints are acceptable (note).
5. **The camera always moves: PASS.** The foreground pebble and the footprints travel about 160 px left and about 70 px down over the shot, about 1.6 px/frame, with no static run. Soil-band phase correlation locks at 0 px. That suggests a screen-locked grain/noise layer, which is harmless (note only).
6. **Heads above y 880: PASS.** The herd's lowest pixel is about y 568 (g1672) and the heads are at y 70-470.
7. **No text: PASS.**
8. **Continuity:**
   - **IN (s24 g1677 -> g1678): FAIL as to screen direction.** This is covered by blocker 1: the matriarch faces right and the herd faces left. Also a note: s24 has a deep indigo starry sky and a dense bee cloud, while s25 has a flat lighter periwinkle sky, no stars and sparse bees. This is the same note as last round.
   - **OUT (g1763 -> s26 dawn g1764 dissolve): PASS.** The herd is small on the horizon and the field and grass layer dissolve into the dawn farm. The fence-row match of v1 is gone (the camera now looks away from the fence), but the dissolve is soft enough.

Kept from earlier rounds:
- Night tint: PASS. Elephant luma 53-58, a cool grey-blue, below the lit soil.
- No ghosting from a cross-fade: PASS. The see-through rear elephant is a separate issue (blocker 2).
- Streak dust, not blobs: PASS. It is grey translucent streaks and wisps.
- Low camera with no down-view on the elephants: PASS. The camera is at grass height and sees the herd at or slightly above eye level.

## Admitted weak points
- **Sky about 38 %: NOTE.** The horizon is at about y 480, so the sky is about 37.5 %. Last round accepted 39 %.
- **The herd stays as a tiny clump to the end: NOTE, and it is the right choice.** At the end it is about 310x120 px, still legible on a phone, and it fixes the dead air.
- **Contact ellipses hidden by grass: NOTE.** The grass occludes the feet consistently, so nothing floats.

## Blockers and fixes
1. **The facing contradicts the travel, and the screen direction flips from s24.** Fix, cheapest first:
   - (a) Mirror every elephant card (scale X -1, or the flipped sprite) so the herd faces screen-RIGHT, the way it drifts toward its vanishing point. This also matches the s24 matriarch, who faces right. Keep the path and the scale-down.
   - (b) Optionally, yaw the lead cards about 20-30 deg toward profile-away so less face shows. Or swap the last 2-3 elephants to a rear 3/4 or rump card from about g1720, so the end reads as rumps going away.
   - Do not re-aim the path so the clump drifts left instead. That keeps the s24 direction flip.
2. **Khaki rectangles in the dust and a see-through rear elephant.** Fix:
   - Render one frame (g1717) with dust and bees off to find the planar objects at about x 600-700, y 470-545. They are likely the stand-ins for the hidden wire or hives, or the dust quads' unpremultiplied edges. Delete those objects or set them to holdout, or give them the yard-plane material.
   - Then either sort the dust cards behind the rearmost elephant, or cap the dust opacity over the elephants at about 0.5 with no alpha holdout, so the rear body stays solid and the dust sits over it, not through it.
   - Re-check n20, n45, n70 and n98 at full size.

## Notes (not blocking)
- Darken the sky toward s24's indigo and add a few stars, plus a trailing bee swarm over the herd for the first ~20 frames, to link to the s24 bee cloud.
- The darkest hard-edged footprint (g1770, about x 160, y 980) could be softened. All footprints sit under the caption band.
