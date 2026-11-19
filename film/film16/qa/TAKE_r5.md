# Film 16 TAKE gate round 5: QA-tech and QA-art combined (s17 and s18)
Takes: s17 and s18 from render16/team5 @bc3d5f2 (one take.mkv each, 720x1280, 30 fps).
Method: I decoded each take to full-res JPEG one at a time and deleted the frames afterwards. I checked 6 fps sheets with the y 880 line drawn, every cut ±3 frames (handles), full-size frames, prop/face/eye/band crops, and a 360x640 phone sheet. I ran film/qa_auto.py on each take and recomputed the frame-diff myself (90x160 grey, in-shot pairs).
Lip-sync window for s18: 38.46-40.80 s + 0.10 s clock = g 1157-1227 (±0.15 s = ±4.5 f). s17 has no quote.
Earlier report: qa/TAKE_r4.md.

| take | qa_auto | diff median / p90 (min) | heads y<880 | verdict |
|---|---|---|---|---|
| s17 | PASS | 6.11 / 10.26 (2.73), longest run <3 = 4 f | yes (bottoms <= ~721) | **PASS (notes)** |
| s18 | PASS | 5.47 / 12.82 (2.50), longest run <3 = 1 f | yes (group bottoms ~790-825) | **PASS (notes)** |

I found no frozen run, no black, blank or magenta frames (magenta 0.0 %), no DOF, and no text in the picture. qa_auto's "planned cuts with no visible change" is expected, because the handles are continuous. The handles (s17 g 1072-1078 and 1116-1122; s18 g 1116-1122 and 1223-1229) show no pops.
s17 p90 is 10.26, under 12. That is a NOTE, not blocking: the film-level target is met and the take moves visibly (push and arc, the shakes, the snap at g 1100-1110).

## s17: empty money bag: PASS (notes)
Earlier blocking issues (TAKE_r4):
1. The sack read as a vase or bell with an open round top: **FIXED**. The top is now a twisted, lumpy neck tied with a red-brown string. The body hangs limp and pear-shaped, mouth DOWN. The bottom is a dark, gaping, scalloped opening. Grey dust puffs come out on each shake (g 1084-1092 and 1096-1110). A grey two-winged moth drops at g 1096-1100.
2. Nobody held it: **FIXED**. Morse's arm reaches out to screen-right, and his dark fist and white cuff sit on the tied neck in every frame from g 1066 to 1127. The bag swings from that point.
3. Eye-line to the lens: **PARTLY FIXED (now a note)**. At g 1096-1104 the half-moon pupils hang under the lids, offset toward screen-right and down (toward the bag). By g 1110-1118 they are centred again. You cannot see the head pitch: the face stays frontal. On the phone he reads as "looking down, crushed" rather than "staring into the bag". This is acceptable for a 1.5 s shot.
4. Workers (note in r4): **FIXED**. Worker a (plaid) is fully visible at screen-left for the whole shot. Worker b's hands rest on top of the shovel and his forearms no longer cross. The slump on the shakes is small but visible.

Phone read (360x640): "Morse holds a cloth sack upside down by its tied neck at arm's length and shakes it. Only dust and a moth fall out, and he and the workers droop." The empty bag READS.
Notes (non-blocking):
- a. A white, bone-shaped piece (the "small crumpled lining" or the button) sits in the bag mouth in EVERY frame, g 1075-1118. On the phone it reads as a little white bone or popcorn stuck in the mouth, which slightly contradicts "nothing inside". If the take is touched again, shrink it to a thin cream lip, or make it fall once (the button) and leave the mouth dark.
- b. The bag's flared, scalloped hem still looks a little like a skirt or bell. It no longer blocks the read, because the held neck and the falling dust carry it.
- c. Head pitch: 10-15 deg more visible downward tilt at g 1096-1110 would sell "looks into it".
- d. p90 10.26 < 12 (see above).

## s18: mocker's taunt from the buggy: PASS (notes)
Earlier blocking issues (TAKE_r4):
1. Group heads in the caption band (g 1160-1200): **FIXED**. Morse (holding the coil), worker a and worker b now stand higher and further back. In my band crops (g 1160-1225) every chin sits clearly above y 880. The lowest chin is about y 830 (worker a, at the end), which matches meta bottoms of 791-825.
2. No real point: **FIXED**. From about g 1165 his right arm is fully out toward screen-right, with a tapered pointing hand and a white cuff. His eyes are OPEN from about g 1175 (round, behind glasses, with tears), and the pupils sit on the screen-right side of the eyes (toward the group) through g 1180-1224. Note: the arm is horizontal at shoulder height, so it aims at the tree just above the group's heads, not at them. Their heads are about 150-200 px lower.
3. Snap panning away: **FIXED**. The snap at g 1204-1216 moves toward the group. The end framing (g 1212-1225) keeps the mocker at screen-left and the three of them at screen-right, side by side. Small note: worker a (red plaid) is clipped at the right frame edge, about half his face, at g 1215-1225. Morse stays fully in frame.
4. Flat mint-green slab: **PARTLY FIXED (now a note)**. The mint tint is gone, and the large side panel now has a very faint plank grain. But from g 1206 to the end it is still a large PALE grey-sage flat face (about x 20-370, y 800-1030, roughly 10 % of the frame). It is the brightest flat area in the end frames and does not match the dark-blue panel of the opening. It is NOT "a rail at the lower edge", as QA.md says. It lies mostly inside the caption band (y >= 880) and lasts about 0.5 s in-shot, so the caption will cover most of it. I do not block on it. If anything is re-rendered, darken it to the panel blue (value about 0.5x) or give it the same visible grain.
5. Walking legs: **FIXED**. He is seated behind the side panel. Only the torso and plaid waistcoat show, with a dark seat mass at g 1218-1225. No stride is visible.

Lip-sync: the mouth is closed and flat/smug until g 1153, then closed in the laughing pose (g 1154-1156). The talk shapes run from g 1157 through the cut at g 1226, and the handles continue to g 1230. All of this is inside the window plus tolerance. Tears and the belly bounce read.
Other notes:
- Morse is half hidden behind the rear wheel rim at g 1155-1165, just as he enters. He clears it from about g 1170.
- The furrow itself is not readable. The group stands in grass and fence, and "by the failed furrow" relies on the narration. This was accepted in r4.
- The mule is not visible (accepted in r4).
- A thin yellow-lit grass blade crosses the top-left corner at g 1122-1127 (a real FG blade, not an artefact).
Phone read (360x640): "A laughing fat man in a top hat rides a cart. He points to the right and shouts, and sad Morse with his coil and two workers stand right below him." The taunt has a target and READS.

## Summary
- s17 **PASS (notes)**: the bag is a tied, held, mouth-down sack shaken empty (dust and moth). Held and vase-like are FIXED; the workers are FIXED; the eye-line is partly fixed (pupils down-right at g 1096-1104, no head pitch). Notes: the white bone-like lining in the mouth, p90 10.26.
- s18 **PASS (notes)**: the heads are above 880 (lowest chin about 830), there is a real point with eyes open on the group, the snap goes toward the group, he is seated, and the lip-sync is in window. These are FIXED. The slab is partly fixed: it is pale grey-sage with faint grain, not mint, still large but mostly under the captions in the last 0.5 s. Notes: the arm aims slightly over the group's heads, and worker a is clipped at the right edge at the end.
Sheets and crops: /tmp/claude-0/-home-user-github-commit-quest-v2/d013e474-c7c9-591e-b74b-eccded3d274b/scratchpad/qa16/r5/<take>/ (p6.jpg, phone360.jpg, full*.jpg, bag.jpg, face.jpg, eyes.jpg, band.jpg, point.jpg, lips.jpg, slab.jpg, QA_AUTO.md). Frames and the worktree are deleted, and the repo is untouched (film16/main).
