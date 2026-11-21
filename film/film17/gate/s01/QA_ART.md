# QA-art, film 17 take s01 (HOOK, shots 1-3, g0-143): FIX-FIRST

Reviewer: QA-art (opus), TAKE gate for a key shot (QA_TEAM.md, Stricter QA C). The client delegated approval to QA, so this verdict decides the take.
Material reviewed: phone_sheet.jpg (360x640), contact.jpg, and full-res frames f6/g0000-g0145 (every 5th frame, plus g45-51 and g90-96 around the cuts).
Numbers: rhythm in-shot median 6.44 / p90 14.61 (target >= 4 / >= 12; film 2 = 5.1 / 18.7). qa_auto: PASS.

## Scores (1-10)
| Area | Score | Notes |
|---|---|---|
| Hook clarity | **3** | The hook image is "calipers on a thief's ear", and the take never shows it. In shot 1 (g0-47), Bertillon holds the calipers across his own chest. They point to the left, away from the prisoner, and the jaws are about 150 px from the ear. In shot 3 (g93-143), the caliper is a huge flat grey bar that crosses the cheek and face (g105, g135). No jaw tips close on an ear in either shot. At phone size it reads as "a man holding a pipe next to a bored guy". |
| Set density | 7 | The set is good: clock, book shelves, measuring post, camera on its tripod, rugs, lamps. In shot 2 the centre of the frame is a stool with a pile of ledgers, and the planned queue of prisoners on the bench is missing. |
| Light / colour | 7 | Warm practical lamps, orange walls against the blue ceiling, a light shaft in shot 2. This matches the house look. Shot 3 is a little flat and grey on the caliper. |
| Composition | 4 | Shot 1: heads sit well (centres at y 560-660). The measuring-post headrest bar comes down onto the prisoner's forehead (g0, g45), so it looks like a spike in his head. Shot 2: the subject (Bertillon at the chair) is about 90 px tall in the back of the room. The green-coat prisoner is cut off at the left edge, and the frame centre is the ledger stool. Shot 3: the caliper bar covers the face. |
| Acting | 4 | The prisoner's bored, heavy-lidded look is good and reads as funny. Bertillon is static, and his arm never reaches for the ear. Bertillon's coat skirt renders as a see-through dark box with the chair lines showing through (g20, g45). |
| Camera energy vs film 2 | 7 | The median is above film 2 and the p90 passes. The push and slide in shot 1 and the snap in shot 3 (g120-135) both read well. The pull-out in shot 2 is gentle. |

Noise / blotches (12 samples + denoise): mostly clean, and lines are sharp. There is fine grain on the dark wainscot and a lighter speckled patch where the floor meets the wall (g20, around x 120-300, y 600-800). This is not blocking on its own, but the area is large on a phone. The set_dust specks are big, hard white dots (g20, g70). At 360 px they look like dead pixels, so make them fewer and softer.

## Verdict: FIX-FIRST
The take passes on camera rhythm and look, but it fails on the one thing a hook must do. The first 1.6 s does not show the strange act.

## Fixes (in priority order)
1. **Shot 1 (g0-47): put the calipers ON the ear.**
   - By g15 at the latest, Bertillon's arm reaches out. Use `hand_for_anchor()` with the calipers_r anchor pinned to prisoner_a's near ear (camera-left), so one jaw tip sits above the ear and one below it, and the jaws close slightly over g15-40.
   - Keep the calipers at least ~220 px long on screen, and keep them clear of both faces.
   - Raise the headrest bar of the measuring post so it sits on top of the hair, or hide it, so it no longer stabs the forehead.
   - Fix the see-through coat skirt: use an opaque card, or move the skirt in front of the chair.
2. **Shot 3 (g93-143): re-stage the insert as a near-profile ear shot.**
   - Swing the camera about 60° toward the side of the sitter so the ear faces the lens and sits in the frame centre (x 300-450, y 500-700).
   - Show the two caliper jaw tips enclosing the ear from top and bottom. The bar runs out of frame to the left, above the eye line, and does not cover the face.
   - Keep one eye in frame so the stiff, sideways look still plays.
   - Repeat the same framing on prisoner_b after the snap (currently g135, where the bar crosses his face and hides an eye).
3. **Shot 2 (g48-92): show the queue the narration describes ("ทุกคนที่ถูกจับมา", every thief brought in).**
   - Put 3 prisoners on the bench in the midground, left of centre, all fully in frame (the green-coat prisoner is cut off at x 0 now), and a gendarme at the door.
   - Start the camera ~30 % closer to the chair so Bertillon and the sitter are at least 2x their current size.
   - Move the ledger-stool foreground prop to the left or right third, where it gives parallax without being the frame centre.
   - Halve the dust specks.

To re-check after the fixes: send me the phone sheet plus g15, g40, g70, g105 and g135 at full res.
