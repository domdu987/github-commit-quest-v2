# QA-tech sD1 v2 (team2 8289c28)

**Verdict: FAIL** (one blocking issue, easy fix). Take: 101 frames, g542-642, 720x1280, cut in from C, whip out to D2 at g642.

## What was fixed against the old list (team 7)
| old item | now |
|---|---|
| 1 Sign "KING'S TREASURY" cropped | FIXED. Both lines fully readable and centred g542-~580 (g557/572 best); leaves the frame only at ~g584-590 as the camera glides on (planned). |
| 2 Coins not visible, hand hidden, chalk-white | FIXED. Coins and stacks are gold; raised hand pinching a coin visible g592-607; loose coin on the table. |
| 3 Rim light (set/cast limit, not waived) | Unchanged, still open at the FINAL gate (film-wide question). Not judged here. |
| 4 Slab 45 %, head 12 % | FIXED. Slab ~25 %, no underside after g584, head ~18-25 % of frame height (about 22 % at the laugh, under the 35 % limit). |
| 5 No look-up beat before the laugh | FIXED. g602-612: head and eyes turn toward the river, then the laugh at g612 (= narration 20.29, correct). |

## Mouth windows
- Narration 17.97-21.29 only (g542-642). Cressingham's speech window starts at 21.29 = g642, so no lip-sync belongs in D1. The mouth is closed while counting (g542-607).
- The laugh (20.29-21.29 = g612-642) is the fixed laugh drawing with open mouth, bounce and tears. Correct per WORKER21, no speak call.
- No one else talks.

## Whip
qa_auto FAIL "suspected blur" g637-642 IS the planned whip W (6 frames, horizontal motion blur, camera sweeping right off the table to the camp). Accepted. The only pops are inside it. Rhythm median 10.73 and p90 36.04, as expected for a held shot plus a whip; 0 cuts inside the shot.

## Beat table
| g | beat | readability at phone size | verdict |
|---|---|---|---|
| 542-560 | Cut in: sign big and centred, lantern top, Cressingham's head peeking right behind the chest | Sign reads well. Head small and half hidden. | OK |
| 562-582 | Push-in on the sign, camera glides right | Sign reads. His head is cut by the RIGHT frame edge (about half the face at g572). | **blocking, issue 1** |
| 584-598 | Sign leaves left, he comes into view, smirk, counting, coin pinched | Clear. At g587 the sign reads "S / REASURY" at the left edge. | OK (issue 2) |
| 598-611 | Look-up beat toward the river, gold stacks foreground | Clear. Smug eyes-up reads. | OK |
| 612-636 | Laugh, bounce, tears, hand on hip, push-in. Head y about 470-850, under 880. | Strong and readable. Face about 22 %. | OK |
| 637-642 | Whip right, tent and flag smear, grass and ground | Planned blur. | OK (issue 3 minor) |

## Other checks
- Heads above y 880: pass (head bottom about y 850 at the closest push-in).
- Nothing floats: pass (coins sit on the table, sign on its post).
- Face over 35 %: pass.
- Colour story: crimson canopy, gold coins and lantern, with the teal river, sky and hills as backdrop. No blue in the English canopy, pavilions or banners while the table is in view. Brightness and cast are left to the conform.
- Characters acting: he counts, looks up, laughs and bounces. During g542-582 he is only a half-hidden head peeking behind the sign (little action visible, tolerable as the sign beat).
- Camera clearance: no clipping; the table slab and sign are passed cleanly. The camera is above the table from g598.
- Bloodless: yes.

## Issues
1. **BLOCKING, g562-582: Cressingham's head is cut by the right frame edge** (about half the face at g572) while the sign is centred. Fix: shift the camera framing about 8-10 % of frame width to the right (or start the glide towards him about 15 frames earlier) so the whole head stays inside while the sign still reads fully. Alternatively hold his head inside by moving him about 0.1 m left behind the chest.
2. Non-blocking, g584-592: the sign crops hard at the left edge ("S / REASURY") during the glide. Move the leave-frame sooner (about g580) so the half-readable state lasts under 6 frames, or fade the glide faster.
3. Non-blocking, g641-642: the pavilion seen in the whip goes violet or lavender, with a blue-ish shade cast (mean RGB at g642 about 0.34/0.26/0.41, b above r). Under the NO-blue-in-the-English-camp rule, make sure the pavilion cloth reads crimson or gold in shade. It is only 1-2 frames inside the blur, so it is not blocking, but D2 should start on a crimson or gold pavilion, not a violet one. Check D2's first frames at the dissolve or whip join.
4. Non-blocking, g542-560: the foreground grass and ground in shade go purple-blue, which is not English-camp kit. A warmer shade would help. Left to the conform.
5. Non-blocking: the rim light stays an open film-wide item (see old item 3).

## Fix list for rerender
Only issue 1 is needed for PASS; 2 to 4 are optional polish.
