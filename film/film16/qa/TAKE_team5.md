# TAKE gate QA-tech, film 16, render team 5 (s16, s17, s18), branch render16/team5 @0a51885
Method: 6 fps montages of every take (g labelled, caption band y 880 drawn), cut frames +-3, full-size spot checks, qa_auto.py re-run on each take.mkv, frame-diff recomputed (90x160 grey, in-shot pairs only). Neighbouring takes (s15/s19) are not in this branch, so cross-cut continuity is judged against the plan only.

| take | verdict | qa_auto | frame-diff median / p90 (recomputed = reported) |
|---|---|---|---|
| s16 | FAIL | FAIL (blur g998-1011) | 3.97 / 10.48 |
| s17 | FAIL | PASS | 3.90 / 9.58 |
| s18 | FAIL | PASS | 6.73 / 14.71 |

## s16 (shot 16, trench cut-away) FAIL
BLOCKING
1. g1027-1049 and g1066-1074: frame-diff sits at ~1.9-2.0 (soil texture, slow push) and ~5.9; whole-shot median 3.97 < 4 and p90 10.48 < 12. Fix: raise push to ~12 %/s and slide to ~120 px/s along the pipe, add a second smaller snap or a roll-free drift of the camera past the split (the plan says "slow slide along the pipe", so the slide must visibly travel), re-measure.
2. g1007-1011 (shot frames, qa_auto blur FAIL, 14 frames flagged incl. handles): the dive reads as a soft slide of flat ground texture, not a streak whip; first shot frames g1007-1012 are the plain orange ground slab filling the top 60 % with the pipe tiny at the bottom, so the planned "dive down into the trench" beat is mostly in the handles and the cut lands on an empty frame. Fix: start the dive so the shot's first frame (g1007) is already mid-whip (fast tilt, pipe entering frame), reach the elevation view by ~g1016, and keep the blur only on the set (<= 3 frames) as the brief allows.
NOTES
- g1008-1050: the lower ~40 % of the frame is empty dark soil with a glow, pipe/rags sit in the middle band; composition is bare at phone size. Frame the split lower-centre or push further in earlier.
- Blue sparks read as large cyan ovals (g1058-1083), acceptable; copper wire, torn cloth, split lead and drips all read. No heads, text, magenta, black, frozen frames (longest low-motion run 4 frames, 0.73 diff, in the handle). No characters.

## s17 (shot 17, empty money bag) FAIL
BLOCKING
1. Frame-diff median 3.90 < 4, p90 9.58 < 12 (flat for g1075-1085 at 3.3, again 2.7-3.1 for g1100-1112). The soft snap g1085-1098 helps but the second half barely moves. Fix: stronger push (13 -> 16 %/s) plus the arc, or move the snap to g1095-1110 so it lands on "เปล่า" and the tail keeps moving; re-measure.
NOTES (non-blocking)
- Heads: Morse 330 px, workers 145-171 / 108-150 px, all heads at y 540-630, bottoms <= 721, above 880. OK.
- Bag held in Morse's extended hand through the whole shot, shake visible; shovels held by both workers; contact shadows on grass OK; mouths still (Morse expression only). Eye-lines: Morse looks down-left at the camera/bag side, workers look at the bag; acceptable.
- g1110-1118: worker_b (straw hat) is clipped by the right frame edge and worker_a by the left edge after the push; they remain readable but the "workers lean on shovels" beat is partly lost. Keep worker_b fully in frame at the end of the push (slide left or pull the snap target).
- Morse sprite slightly soft at the 330 px peak (as the team notes); acceptable.
- Plan says push 8 %/s, no snap; team used 13 %/s plus a soft snap: fine.

## s18 (shot 18, the mocker in the buggy) FAIL
BLOCKING
1. g1119-1203 (84 frames = 2.8 s of the 3.5 s shot, including the lip-sync window g1157-1203): the mocker's head is only ~84-100 px at the far left, mouth unreadable at phone size, below the wide minimum of 110 px and far below the "quick push-in" intent. The only readable lip-sync is g1206-1225 (about 0.7 s of the 2.34 s quote). Fix: open on a medium-wide (head >= 130 px, mocker + buggy side + mule head), push 8-10 %/s toward him from g1119, so head >= 200 px by g1157 when the lips start; keep the snap on "ใต้ดินแล้ว" to ~300 px.
2. g1120-1150: the foreground grass blades (large yellow spikes, one crossing the lens g1125-1135) fill the lower 40 % and cut across the wheel/buggy; the shot reads as through a hedge. Team calls it set dressing. Fix: lower or thin the foreground blades for this camera (move the grass hook out of the camera cone) while keeping some foreground depth.
NOTES (non-blocking)
- Mouths: flat until g1154-1156, lip-sync from g1157 (= 38.46 s +- 0.15 s) per meta and visible open mouth g1160+; per the team's raw json it is still sync at g1226-1227 (end of window 40.80 s = g1227 ok). Mule never lip-syncs. OK.
- Heads: mocker top-hat head centre y 573-625, bottom 737; mule head bottom ~893/1055 is the mule body (animal, not a character head; wheels/buggy bottom in the caption band is normal). Whole mocker head above 880 at all frames.
- Hat/props: top hat, plaid waistcoat consistent; buggy and mule hitched, mule walk cycle OK, buggy rolls +x, wheels turn. After the snap (g1206-1225) the buggy's red seat box and green side fill the lower third; mocker's hands are not visibly holding anything (none planned).
- g1218-1225: diff drops to 1.2-2.8 (camera almost parked, no run < 0.8 so the 6-frame rule is not broken). Add a small continued push after the snap.
- Frame-diff 6.73 / 14.71 meets target. Tears + blush appear from g1154 as planned.

## Common
- Plan coverage: s16 pipe/torn cloth/blue leaks yes; s17 empty bag yes; s18 mocker leaning out laughing, belly bounce, mule yes, quote at 38.46-40.80 yes, low-angle quick push-in only at the very end.
- No text, no DOF, no black/magenta/frozen frames in any take; magenta share 0.0 %. Frames removed after QA.
