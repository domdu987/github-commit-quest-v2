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

## Round 8 (director QA-tech): PASS
Checked 6 fps + g962-971, g992-1003, g1006-1015 (take g929-1024), frames in /tmp/qa19_r8/s12. Frame-diff g939-1015: median 5.79 / p90 13.23 OK. No text, black or frozen frames. Mouth fixed (frown / grimace), no mouth movement. Heads centre y ~ 460-600, nothing at 880.
Hair gag VERIFIED: hair is grey in every frame g938-995, including the whip g952-972 (no swap or pop at g965/966; diff there is the smooth whip 13-17 -> 11). At g996 (frame diff 11) the hair is white with spectacles, brown coat and puff clouds, g997 shows the squash/puff; this is the only pop in the take and sits on the word "หงอก". Chisel is in frame all the way (taps to g995, then dangles low left of the stool g996-1015, small but visible). Slump is real: he folds forward g996-1003, hand over the eyes with a sweat drop g1003-1015. The shop clock (gear box, H3) stays in frame at the left, behind him, g938-1015 (cropped by the left edge from g958 and dim in the dark, but readable).
Notes (non-blocking): (a) the lit pink wall on the right is still a large mostly empty area g963-988 (~25-30 % of the frame, "dead wall" only partly cured: a wall light, a hung tool or a shelf would help); (b) g1003-1015 the wig and ponytail come within ~20 px of the right edge, face intact; (c) legs end in stubs, shadow faint.
