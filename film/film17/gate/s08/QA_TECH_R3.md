# QA_TECH s08 ROUND 3 (shots 20-21, g1039-1201, cut g1127) - VERDICT: PASS

Reviewed: full-size g1064, 1094, 1109, 1124, 1130, 1144, 1164, 1199; hand crops g1130-1199 (10 frames); mouth strip g1127-1129 and 1190-1201; take.mkv decoded for all 163 frames (per-frame Laplacian variance and frame-diff). QA_AUTO PASS, rhythm 4.92 / 14.39 OK.

## R2 blocker B1 - FIXED
1. Both cards are held in shot 21 in every frame checked (g1130, 1134, 1139, 1149, 1159, 1169, 1179, 1189, 1194, 1199). Each card has a dark glove ball at its lower corner, and the sleeve with a white cuff runs into it. Nothing floats.
2. The thumb arc sits only under the right glove and joins its ball. It reads as part of the glove, not a separate ring. Small nit: the arc is tan, lighter than the black glove. Not blocking.

## Other R2 fixes
- Inspector head is turned toward Bertillon (camera-left) and his gaze is on him from about g1150. Seen at g1164 and g1199.
- The sconce is inside the frame at g1199, at the top left near x 210, y 180.
- Right gendarme's grey box is gone (g1130-1199).
- Shot 20 candle is visible and taller. It sits on the desk at g1094 and g1109 with a bright glow. The flame is blown out by bloom, so it reads as a glowing candle, not a distinct flame. Acceptable.

## Regressions - none
- Inspector's mouth opens from g1128. It is open through g1195 and closed from g1197. No other mouth moves.
- Chins: inspector about 780 and Bertillon about 800 at most, all above y 880.
- No see-through cards, no beam shafts, no dust. No leftover geometry.
- Sharpness: the Laplacian variance drops to about 150 over g1104-1126. That is smooth wall at the pull-out, and full-size frames g1109 and g1124 are crisp. No blur.
- No frozen hold: the minimum frame-diff is about 3.2 and it never stays near zero.
- The hard cut at g1127 is clean (diff 25).

## Should-fix (optional)
- Recolor the thumb arc to the glove colour.
