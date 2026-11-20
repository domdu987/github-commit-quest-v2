# QA-tech sD2 (film 21, g642-793 + handles 794-796): FAIL
Method: 6 fps (31 frames), first/last 4 frames, and the team's edge frames (g754-756, 760, 780-786) at full size. 155 frames confirmed.

## Verdict
FAIL on 3 blocking issues (half-cut Surrey at the frame edge, missing purse slap, barrel covering Cressingham). Everything else passes.

## Checks that pass
- Whip-in g642-647: g642 is an empty beach plus barrel (soft, motion streak allowed), Cressingham enters from g643. Settles by g648.
- Lip-sync: mouth open only inside 21.29-26.26 (g642-791), closed smirk at g792+ and at P_BANK. g787 is a tiny mouth line, in tolerance.
- Heads: Cressingham head centre y about 450-760, all bottoms under 880. Faces: normal about 15-20 % of frame height. CU1 face about 27 % (under 35 %, allowed at CU1).
- CU1 push into the face on "เร็วดี ประหยัดดี!" starts about g756 and eases back out. Good.
- Banner pole is hidden, so nothing passes through his head. Surrey is clear of any pole and is behind him, trailing.
- Ends at P_BANK at g793: g793-796 are identical, with Cressingham hands on hips, Surrey at about 77 % of the width, smirk. Colour is saturated, with a golden rim.
- Rim light on cards is a known limitation, noted, not failed. No blood. No blur other than g642.

## Issues
1. g754-756 (and g784-786): Surrey is cut in half by the right frame edge. g754 shows about 40 % of his face and body, g756 about 25 %. At g784-786 he is again at the right edge (head half out), plus a background soldier sliver at the right edge at g780-782. This breaks "nobody cut in half at the frame edge" (§G3). The team noted it as "known" but it is a FAIL. Fix: move Surrey and the soldiers 1-1.5 m toward the camera centre, or hold him fully out of frame until the camera has pulled back. Do the same for the soldiers.
2. g756-778 (CU1): the purse slap on "เร็วดี ประหยัดดี!" is not visible. His right hand hangs near the chest and never reaches the purse (the purse is at the belt, left). The raised left hand waves. Then at g780+ both hands go on the hips. The plan says "slaps his purse" (g758). Fix: animate the right hand to the purse at g758 with a 2-frame jolt, and keep the purse in shot, with the face about 27 % so the purse fits.
3. g684-720 (approx. strip frames 8-16): a foreground barrel crosses in front of him and hides his legs and feet and most of the lower body for about 1.5 s (g690-715). He looks cut off at the waist and his contact with the ground is hidden, so he reads as "legs missing". Fix: shift the barrel off his path (or hide it once it reaches him) so his feet stay visible.
4. g642-646: Surrey's head is directly behind his neck and mostly hidden by his head, so he reads as part of him (g643-646). Fix: offset Surrey about 0.5 m to the right.
5. g793-796: the four handle frames are identical (frozen), not a continuing pull-out as meta.json says. A D6 dissolve into E1 will show a static start. Fix: continue the camera drift of about 1 % per frame, or accept a 4-frame hold and tell the conform.
6. Continuity in: not checked against D1's last frame (D1 gate not in this task); his walk begins from the beach edge with no table in view, which suits the whip.

Fix list: 1, 2, 3 must be fixed; 4-5 desirable.
