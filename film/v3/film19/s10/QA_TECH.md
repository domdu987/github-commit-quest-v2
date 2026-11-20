# s10 QA_TECH: FAIL
Shot 10, HALL hall_wide DAY, take g764-871 (handles 9 in / 10 out, out side DIS 15), 6 fps + cuts g773/g862 +-3 checked. qa_auto reports FAIL (suspected blur g852-871, 20 frames); I checked g854-871 at full size: sharp, the close-up has flat colour so the Laplacian drops (false positive; the worker should say so in QA.md). No text, no black/magenta, no frozen run. Frame-diff re-measured median 4.28, p90 18.41: OK. Spike g848-852 = planned snap. Mouths: the Board laughing grins are plan-required (shot 10); Harrison mouth fixed. Wide exempt from head band g764-843.
## Issues
1. g764-843: plan says Harrison "stands at the door with his tricorne". He stands in the middle of the hall at the table, no door visible; the door-leaf hiding note means the door never appears. Fix: stage Harrison at the door mark (in the final third of the shot the camera should find him there) or change the plan row.
2. g764-843: Board staging: astro_b and astro_c (right) overlap heavily and stack, one face hidden behind another; Harrison's body covers astro_b. The "fingers point" beat is not visible (no pointing arms in the frames; only wig bounce). Fix: separate marks by >= 0.8 D, mirrored toward the aisle, with alternate pointing arms.
3. g764-789: the carpet medallion arcs fill both bottom corners (large dark-red arcs at y > 1000, g764-779 ~25 % of the bottom). Set note: keep them low/cropped. Fix: tilt the camera up 8-10 % so the bottom 30 % is cropped, or raise the horizon.
4. g764-850: the bottom ~35 % of frame is empty blue carpet; the cast sits in the top 55 %. Fix: lower the camera, closer FG prop (chair/telescope leg) in the empty zone.
5. g843-849: snap to Harrison: g849 is a mid-whip frame with a Board wig sliver and a foreign table in the left of the frame; the whip is fast (diff 23-25 over 5 f), ok, but the end hold g854-871 is near-static (diff ~3.8-4) for 18 frames, a ">1 s" style hold risk is small, but the framing parks. Fix: continue a slow push (6 %/s) through g854-871.
6. g859-871: Harrison's ponytail bow/hair edge touches the left of the frame and the tricorne is a flat black wedge hanging in front of the belly at an angle (g860); hand does not visibly hold it (fingers hidden behind the apron). Fix: raise the hat in his right hand at chest height with the fingers over the brim.
7. g764-843: no visible contact shadows under Harrison's and astro19's feet on the rug (g814: legs end in shoes with no decal). Fix: contact decals.
8. meta.json g1 = 862 is exclusive (plan g1 = 861). Note only. Handles 9 in / 10 out present.

## Round 2: FAIL
Re-checked at 6 fps + cuts g773/g862 +-3 (take g764-871; handles 9 in / 10 out). qa_auto PASS (soft g848/849/852 = the planned snap streak, 3 frames: OK; the old g852-871 blur run is gone). No text, no black/magenta, no frozen, no pop outside the snap. Frame-diff (take.mkv): median 4.50, p90 17.36: OK. Snap on "ไอ้ช่างไม้" g846-849: OK.
Earlier issues: 1 FIXED (Harrison now at the open door), 2 PARTLY (pointing arms now visible g814-844; astro_b/c still stack at g764-809), 3 FIXED, 4 FIXED, 5 FIXED (slow push continues), 6 NOT FIXED, 7 faint shadow under Harrison at the door: OK; the astronomers' feet are hidden by the table, 8 note still true (g1=862 exclusive).
1. g854-871: plan "Harrison with his tricorne": no tricorne visible; his arms are folded/crossed low with empty hands (the QA_TECH round-1 item 6 fix of "hat in the right hand at chest height" is not done). Fix: put the tricorne in his raised hand, fingers over the brim.
2. g764-809: astro_b and astro_c (right) still overlap into one clump (two wigs, one face partly hidden). Fix: separate marks by >= 0.8 D.
3. g829-849: the right-hand Board member is about 50 % clipped by the right frame edge (face half cut at g839-844). Fix: shift the slide end ~50 px left or put him at the mark 0.4 D inboard.
NOTES: g854-871 a candle-like shape on the top of the painting sits right above Harrison's head (tangent): set note; Harrison's hat bow/ponytail fine; nobody on the rail issue n/a.

## Round 3: FAIL
Checked 6 fps + cuts g773/g862 +-3 (take g764-871), qa_auto PASS (soft g848/849/852 = planned snap streak). No text, no black/magenta, no frozen. Frame-diff (take.mkv, g774-861): median 4.90, p90 19.65: OK. Wide exempt from head band g764-843; Harrison close-up head centre ~ 560-600.
Earlier issues: R2-1 NOT FIXED, R2-2 NOT FIXED, R2-3 NOT FIXED.
1. g854-871 (R2-1, plan "Harrison with his tricorne"): still no tricorne; hands clasped/low, empty. QA.md now says "the tricorne is dropped", but the plan beat is not changed. Fix: tricorne in his raised hand, fingers over the brim, or the director amends the plan row in writing.
2. g764-809 (R2-2): astro_b and astro_c (right) still overlap into one clump of two wigs, one face partly hidden. Fix: separate marks by >= 0.8 D.
3. g792-846 (R2-3): Board members are cut by BOTH frame edges: the left astronomer's wig/face is ~half off the left edge from g~800 (160-290 rows cut at x=0, g798-846) and the right-hand pair is ~50 % off the right edge (g786-839). Fix: pull the slide end and the marks inboard so every face stays inside x 20-700 until the snap.
Notes: contact shadows under Harrison faint; meta g1=862 exclusive.

## Round 4: FAIL
NOTE on files: take.mkv (09:17) is STALE; the current render is take.mkv.partaa+partab (09:57, matches meta/framediff/QA.md). Checked the concatenated parts (g764-871). qa_auto PASS (soft g850-854 = planned snap). 6 fps + cuts g773/g862 checked. No text, no black/magenta, no frozen. Frame-diff g774-861 median 6.92 / p90 17.82 OK. Wide exempt from head band; Harrison head centre y ~ 560.
Earlier issues: R3-1 tricorne NOT FIXED; R3-2 astro_b/c clump FIXED (smaller green-coat astronomer now sits clear of the right-hand one, faces readable); R3-3 edge clipping PARTLY (left astronomer's wig is cut by the left edge g764-846 and his face touches/loses ~20 % at the edge g836-846 during the whip; right one's wig cut at the right edge, face intact: NOTE).
1. g854-871 (R3-1, plan "Harrison with his tricorne"): still no tricorne; arms folded low, hands empty. Fix: tricorne in the raised hand (fingers over the brim) or the director amends the plan row in writing.
Notes: the take.mkv/parts duplication should be cleaned (deliver one file); contact shadows faint.

## Round 5: PASS
Checked the concatenated take.mkv.partaa+partab (g764-871; take.mkv alongside is the stale 09:17 render), qa_auto PASS (soft g851-854 = planned snap), 6 fps + cuts g773/g862 +-3. No text/black/magenta/frozen. Frame-diff g774-861: median 7.67 / p90 22.19 OK. Wide exempt; Harrison head centre y ~ 640. Laugh grins are plan-required.
Earlier: R4-1 tricorne dropped from the plan by the director (ruling), closed; no tricorne required.
NOTES: left astronomer's wig cut by the left edge g764-846; face half cut at the left edge g846-850 during the planned whip (2-3 frames); right one's wig cut at the right edge (face intact); delete the stale take.mkv when delivering; contact shadows faint.

## Round 8 (director QA-tech): PASS
Checked 6 fps + every frame g834-853 (take g764-871), all 108 frames extracted to /tmp/qa19_r8/s10. Frame-diff g774-861 (90x160 grey bilinear): median 7.34 / p90 13.25 OK. No text, black or frozen frames (min diff 1.45 at g850, the whip landing). No mouth movement (laugh grins are expression cards; Harrison fixed sad mouth). Heads centre y ~ 600-856, nothing at 880.
Whip fix VERIFIED: the Board enters the edge at g839 (both outer wigs touch/leave), at g840-841 the left and right astronomers are about 50 % off the edges but already heavy motion blur (ghosted face, smeared wig), at g842 only a grey-white streak remains on the left edge, gone at g843. Read: a smear, not a half person. The crossing is 3 frames (g840-842), slightly over "about 2"; accepted because every one of those frames is blurred. Harrison is fully in frame, sharp from g845 and centred in the door.
Notes: g773-838 right astronomer's wig lappet and left one's wig are touching the side edges (faces intact); contact shadows faint; Harrison holds the same folded-arm pose g853-861 (sway only, 0.3 s, fine).
