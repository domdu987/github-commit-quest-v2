# QA-art round 11 s22: FIX-FIRST
Shot: REVEAL close-medium, "หางลุกเป็นไฟ เขาติดมีดวาววับ". I reviewed take.mkv frames g 1677-1747: every 5th frame plus every frame from g 1729 to 1747. I viewed them at full size (720x1280), on 240x427 phone sheets, and on guide overlays with x 0.08/0.45/0.65/0.90 and y 860 marked. My extracts are in scratchpad/art11/ (sheet6.jpg, sheet_end.jpg, grid.jpg, chin.jpg).

**Warning: the team's phone_sheet.jpg is identical to contact.jpg (same md5).** It shows the same picture as the take. The round-8 claims in QA.md (soldier at x 0.65-0.80 front-3/4, mouth about y 880, brazier removed) do **not** match the rendered pixels. Only the sky claim holds.

## Director's must-fix list
1. **Soldier at x 0.65-0.90, front-3/4 toward the ox, clear of the tail and flame: NOT DONE.**
   - **Position:** His face is at x 0.60-0.80 (g 1683-1730) and drifts to x 0.47-0.70 from the punch on (g 1734-1747). His armoured torso starts at x 0.58 at g 1712 and x 0.47 at g 1742.
   - **Overlap:** He still stands IN FRONT of the ox's caparison. He hides the rear half of the ox.
   - **Facing:** He is square to the lens with his eyes on camera, not 3/4 toward the ox.
   - **Tail:** The tail rope and straw bundle (x 0.62-0.92, y 500-600) still come out from behind his shoulder. He still seems to hold a broom, with a torch flame beside it (flame at x 0.83-1.0, y 90-500).
2. **Ox head at x 0.08-0.45, chin y ≤ 860 in every frame: NOT DONE.**
   - **Chin:** The lower outline of the open mouth is at y about 878 (g 1683), 888 (g 1712), 900 (g 1732) and 932 (g 1742). It is never at or above 860.
   - **Left edge:** From g 1734 the head's left side is at x 0.00, so the left edge cuts the cheek and the near horn.
   - The "chin 595" figure in meta is still the head box, not the chin.
3. **Tripod brazier gone: NOT DONE.** A tan-legged tripod with a flat navy cone is still at the right edge. At g 1742 it sits at x 615-720, y 420-750, under the warm light at the edge. It is visible from about g 1736 to 1747, which is inside the in-film range up to 1742. QA.md says it was removed.
4. **Blue moonlit sky about 25,76,165: DONE.** The mean sky over y < 250 measures about RGB 34,87,180 in all frames, and the moon and cloud streaks are back. It matches s14/s15 closely enough.

## Phone read
On the phone you still see a calm soldier posing in front of an angry ox, holding a "broom" with a torch beside it. The ox's open mouth sits below the caption line. "Tail ablaze" does not read, because the flame looks like a torch and not like it comes from the ox's tail. The glint is optional this round and is not judged. The grade and the energy of the ox face are good.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 4 | 7 | 3 | 4 | 5 |

## Verdict: FIX-FIRST (3 blockers, each measurable)
1. **Soldier:** Move him so his whole figure (helmet to feet) sits inside x 0.65-0.90 in every frame, including after the punch, and behind the ox's rear (no overlap with the caparison or the tail rope). Yaw him to face left toward the ox (front-3/4, eyes on the ox), with the recoil pose and the sweat drop. The tail bundle and its flame must have no soldier pixels between them and the lens.
2. **Ox framing:** In every frame g 1683-1742, keep the lower outline of the mouth at y ≤ 860 and the head inside x 0.08-0.45. That means about 30-75 px higher than now, so tilt up or raise the ox. Hold that through the punch at g 1731, which must not push the head past the left edge. Fix the meta chin measure so it uses the mouth outline, not the head box.
3. **Brazier:** Delete the tripod brazier object itself, not just its flames. Check g 1736-1747 for zero tan and navy tripod pixels at x > 0.80.

Check the result against the actual rendered frames before resubmitting. This round's notes and sheet did not match the take.
