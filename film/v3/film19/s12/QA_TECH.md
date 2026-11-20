# QA_TECH s12 - FAIL
Checked: qa_auto PASS, 6 fps sheet g929-994, meta g0 938 / g1 985 (plan 31.26-32.85 -> 938/985 OK), handles 9/9, DIS 11 in OK, framediff median 4.19 / p90 16.41 OK. Default (greying, apron) Harrison OK, NIGHT OK, no text/blur, head centre y 464-580, mouth fixed (tired frown), eye-line to lens after snap OK, snap g952-972 visible.
Issues:
1. g929-959 (plan coverage): "candle stub burns down" is not readable. The one candle visible (left of the H3 frame) has the same height at g938 and g958 and scene luminance does not drop (mean 65.6 -> 66.3); after the snap (g964+) the candle is out of frame. Fix: keep the candle in frame (lower the camera slide or move the stub to the bench in front of H3), drive visible stub-length + flame-size 1.0 -> 0.3, and dim the set_candles key light.
2. g964-994: ~1 s of near-static huge head (head 401 px) with only a blink; the tapping (~2 Hz) is not visible after the snap. Fix: keep the chisel hand-stroke in frame or cut the move earlier.
3. g929-994: no contact shadow under the shoes (g929-959). Minor.

## Round 2 - FAIL
Checked: qa_auto PASS, meta g0 938/g1 985 OK, handles OK, framediff median 4.42 / p90 13.37 OK, default look OK, NIGHT OK, no text/blur, mouth fixed, snap g952-972 OK.
1. NOT FIXED (was 1), g938-985: candle stub burn-down not readable. Candle now stays in frame (small table at right, then bottom-right) but its height and flame look the same g929 -> g985; mean luminance does not fall (62.9 at g929 -> 66.8 at g959 -> 88 after the snap, it rises). Fix: drive visible stub length + flame size 1.0 -> 0.3 and actually dim set_candles; the push-in raises exposure, so compensate.
2. Earlier 2 (tapping after snap) improved: chisel angle changes after the snap, accepted, NOTE.
3. Earlier 3 (no contact shadow under shoes g929-959): NOT fixed, NOTE.

## Round 3: PASS
Checked 6 fps (take g929-994), qa_auto PASS (no planned cuts: dissolve in). No text, no black/magenta, no frozen, no blur. Mouth fixed. Head centre y ~ 460-580, nothing at 880. Frame-diff (take.mkv, g939-985): median 4.36, p90 10.59: OK. Snap g952-972 visible, tapping continues to the end, eye-line to lens at the end.
Earlier issues: R2-1 candle burn-down: FIXED (candle stays in frame on the chest; tall slim candle at g938 -> short stub at g985; flame smaller; frame mean luma falls 64 -> 56). R2-2 tapping: OK. R2-3 shadows: still faint, NOTE.
Notes: p90 10.59 is just above the limit; legs end in thin stubs (rig limit); the film-level 12 is for FINAL.

## Round 4: PASS
Checked 6 fps (take g929-994), qa_auto PASS. No text, black/magenta, frozen, blur; mouth fixed (frown). Frame-diff g939-985 median 4.22 / p90 10.62 (>= 4 / >= 10) OK. Round 3 PASS stands: candle burn-down reads, tapping continues, eye-line to lens. New: nothing blocking.
Notes: Harrison's ponytail/hair touches the right edge in the last frames (face intact); legs end in thin stubs; shadow under shoes faint.

## Round 10 (director QA-tech): PASS
Checked 6 fps (g929-1019) plus every frame g985-1016 on crops x 450-720 (and full frames at 10 key g). Frames in /tmp/qa19_r10/s12/. Frame-diff (own calc, 90x160 grey bilinear, in-shot pairs g938-1015): median 6.38, p90 14.31 (limits 4 / 10) OK; max 17.2 at g962 (whip), no pair < 0.3, no black frame, no frozen run.
Round 9 blocker (hard vertical cut of the hair/bow/ponytail/puffs at g997-1016): FIXED. On every frame g985-1016 the ponytail, bow and puffs are whole; the plaster wall is a smooth gradient with no straight edge cutting the card; right-most card pixel stays well left of x 720. Mark is clear of the wall, payoff exposure is lifted (warm wall, luma readable).
Other checks: hair grey through g995 and pops to white with puffs, spectacles and the brown coat on g996 (single frame); backward slump g996-1010 reads; the chisel stays in his hand and visible (low left) through g1016; head about 20 % of frame height, head centre y ~ 450-600 (never near 880); candle on the chest, no floating; mouth fixed (tired frown/wobble during the rub, no lip-sync); no character cut, no text, no blur; Harrison always acting (tap, lean, rub).
Notes (not blocking): legs end in thin stubs; shoe contact shadow faint; ponytail tip is close to the wall at g996-1000 but whole.
