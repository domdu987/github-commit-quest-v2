# QA_TECH s16

## Round 2 - FAIL
Checked: qa_auto PASS (soft g1285-1288 are handle frames after g1280, outside the shot), meta g0 1190/g1 1280 handles 9/9 CUT in OK, framediff 6.12 / 12.48 OK. Ship ride OK (cards, deck and rail move together, no sliding), NOON light, mouths fixed smile, H4 pocket watch in the right hand (attached, with chain), contact shadows present, snap g1214-1230 on บอกเวลาที่ OK.
1. g1260-1280: William's hat, hair and left side are cut by the LEFT frame edge and his feet/shins run off the bottom edge over the last ~20 frames of the push. Fix: end the push centred on the watch (watch is at x ~ 590 and the figure drifts left), or stop the push 15 f earlier.
2. g1200-1280: the captain leaves the frame (cut out by the left edge from g ~1215) so he does not 'look on'. Fix: mark him closer to William or keep the camera wider until g1230.
3. NOTE: the watch is tiny (about 60 px) and held to the side, not toward the camera as planned.

## Round 4: PASS
Checked 6 fps (take g1181-1288), qa_auto PASS, cut in at g1190 (new ship framing continues from s15). No text, black/magenta, frozen, blur; mouths still (smile / frown). Frame-diff g1191-1279 median 4.60 / p90 12.88 OK.
Earlier issues: R2-1 (William clipped at left, feet off bottom) FIXED: William inside, whole body visible, final frame ends on both characters; R2-2 (captain out of frame) FIXED: captain stays in frame to the end; R2-3 watch now ~110-130 px, held at chest, tick marks and hands read from g~1215.
Notes: captain's hat brim and ponytail are cut by the left edge g1255-1279 (face intact, NOTE); the captain is larger than William.
