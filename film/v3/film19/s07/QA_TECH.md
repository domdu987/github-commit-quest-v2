# s07 QA_TECH

## Round 2: FAIL
Shot 7, HALL hall_window DAY, take g457-553 (handles 9/9, meta g0 466, g1 545 exclusive: note), 6 fps + cuts g466/g545 +-3 checked. qa_auto PASS (cuts "no visible change" = handle continues). No text, no black/magenta/blank, no frozen run, no pop, no blur. Mouths: all closed/flat, none moving (outside windows): OK. Snap on "คณะกรรมการ" (g500): visible g497-512: OK. Frame-diff (take.mkv): median 4.26, p90 11.23 vs target >= 4 / >= 12. Contact shadows under astro_c's feet are faint (NOTE).
1. g507-553 (end of snap, ~45 frames): astro is clipped by the right frame edge (right half of wig and the right eye/lens cut; face about 15 % outside from g537, glasses cut at g543+). The shot ends parked on a cropped face. Fix: finish the snap with astro centred (shift camera ~120 px right) and scale x2.0 at most.
2. g487-545: plan coverage: astro_b and astro_c should nod beside the lecturing astro. astro_b leaves the frame from g487; astro_c is mostly behind astro's wig from g507 and shows no nod. Fix: keep both inside the final framing (marks 0.6 D to the left of astro, nodding with a 0.05 D bounce) or lessen the snap scale.
3. g466-545: p90 11.23 (< 12). Fix: a faster snap (x2.2 over 13 f) or more slide before it.
4. g497-545: eye-line: astro looks at the lens while pointing; the raised hand points up-left at the Moon but his eyes/head do not turn to it. Fix: turn head/pupils toward the Moon plate for g470-500, then back to lens on the snap.
NOTES: meta g1 = 545 is exclusive (plan g1 = 544); candle/hands fine; chair legs and left-side bookcase fine.

## Round 3: FAIL
Checked 6 fps + cuts g466/g545 +-3 (take g457-553), qa_auto PASS. No text, no black/magenta, no frozen, no blur. Mouths closed/flat. Frame-diff (take.mkv, g467-544): median 4.71, p90 13.70: OK (R2-3 FIXED). Heads centre in band.
Earlier issues: R2-1 NOT FIXED, R2-2 NOT FIXED, R2-4 not fixed (note).
1. g506-553 (R2-1): astro19 is still cropped by the right frame edge for the whole end of the snap: right half of the wig and the right shoulder cut (300-500 rows at the right column, g506-544), right lens of the pince-nez touches the edge at g537-544; shot parks on it. Fix: end the snap with astro19 centred (camera ~120 px right) and scale <= x1.8.
2. g487-545 (R2-2, plan "astro_b and astro_c nod beside him"): astro_b is out of frame from g~497; astro_c is half hidden behind astro19's wig and shows no nod in the snap (g507-545). Fix: keep both inside the final framing (marks 0.6 D left of astro19, nod 0.05 D) or lessen the snap.
Notes: eye-line still to the lens while pointing at the Moon (R2-4), feet shadows faint, meta g1=545 exclusive.

## Round 5: FAIL
Checked 6 fps + cuts g466/g545 +-3 (take g457-553), qa_auto PASS, no text/black/magenta/frozen/blur, mouths closed. Frame-diff g467-544: median 5.60 / p90 13.22 OK. Heads centre in band.
Earlier: R2-1 changed side but NOT FIXED; R2-2 astro_b/astro_c now stay in frame (nods small).
1. g506-553 (clipping): astro19's pointing arm/hand is cut by the LEFT frame edge for the whole end of the snap (sleeve runs off x 0, hand not visible), and his wig lappet touches x ~ 20. The pointing hand is the key gesture. Fix: end the snap with the camera ~80-100 px left (astro19 centre x ~ 300-360) so arm and hand end inside x 30-700.
2. g520-553 (clipping): the grey-wig astronomer behind the table touches the RIGHT edge; face edge cut by about 10-15 % at g540-553 (wig cut). Fix: same re-centre, or put his mark 0.3 D toward centre.
NOTES: astro19 eye-line to the lens while pointing at the Moon; foot shadows faint.

## Round 6 (director QA-tech): PASS
Checked take g457-553 (97 frames): 6 fps (every 5th frame, /tmp/qa19_s07/six) plus every frame g506-553 (/tmp/qa19_s07/all, g = 457 + index). Overall colour ignored (conform).
Earlier failures re-checked:
- R5-1 (pointing hand clipped at LEFT edge, g506-553): FIXED. Hand and raised sleeve stay inside the frame the whole window (hand tip at x ~100 at g553, ~105 at g506; wig lappet clear of x 0).
- R5-2 (grey-wig face clipped at RIGHT edge): FIXED. Wig right edge at x ~590/720 at g553 and ~540 at g506; the face is fully inside.
- Chair over astro19_c's face: FIXED. The red stool sits low, beside the legs and hems, and never crosses any face at 6 fps or in g506-553.
Checks: hands/faces inside the frame OK; no face overlapped by a prop OK; faces about 14 % of frame height (limit 35 %) OK; no character cut by an edge OK; head bottoms about y 750 (meta 769 max), limit 880 OK; mouths closed/flat throughout, no mouth movement OK; no glitch, pop, black/magenta or text; no frozen run (lowest in-shot diff 0.6).
Frame-diff (90x160 grey, bilinear, in-shot g466-544, 79 diffs): median 4.64 (>= 4 OK), p90 11.90 (>= 10 OK), max 13.4 at g498 (snap), no spike outside the snap.
Issues (none blocking):
1. g466-520 (NOTE): the third astronomer (grey wig, right, behind the table) is half-hidden by astro19_b's hat/wig. At g506 only the wig and a sliver of face show; the face is mostly visible again from g~530. This is character overlap, not a prop, and nothing is cut by the frame edge. Fix if wanted: move his mark about 0.2 D to the right.
2. g522-544 (NOTE): the final 23 frames are nearly static (diff 0.6-0.9), so the nods are very small at the parked framing. Not frozen. Fix if wanted: 0.05 D nod bounce on astro19_b/c.
3. whole shot (NOTE): contact shadows under all feet are very faint on the dark carpet (e.g. g553 feet at y ~1090). No foot floats, but the shadow is hard to see. Same note as earlier rounds; can be pushed in the conform.
4. g497-545 (NOTE, carried from R2-4): astro19's eyes go to the lens while the hand points up-left at the Moon.
