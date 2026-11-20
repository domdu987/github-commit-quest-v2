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

## Round 7 (director QA-tech): FAIL
Checked take.mkv (13:25), g929-1024, 6 fps + every frame g948-977 (merged s12+s13, meta g0 938 / g1 1016). Frames in /tmp/qa19_r7/s12/. No text/black/frozen; no mouth movement (frown / hand over mouth); face height ~16-19 % of frame (<35 %); head centre y ~ 560-650 (<880). Frame-diff (g939-1015): median 6.04, p90 15.48: OK. Lowest pairs g977 (2.0), g984-985 (2.4-2.8), g1009-1015 (2.6-3.5): short, no frozen run >1.5 s.
OK: candle burn-down reads (tall candle g929, flame/stub shorter and dimmer by g1024; scene luma falls); dissolve-in from s11 and out to s14 have handles; whip-pan g952-972 present; Harrison busy (chisel taps to g965, hand-to-mouth, lean back g993-1003, rub g1003-1024).
1. g965 -> g966 (age swap is a visible POP): the camera pan has already slowed by g964 (background settles, frame-diff 17.7 at g965 and 17.9 at g966 is the whole-frame jump, not a hidden wipe). In ONE frame the same Harrison in the same screen position changes from grey hair, apron, chisel arm to white hair, spectacles, brown coat, hand over mouth, with the same background and no whip blur, wipe object or foreground cover. The planned "age swap hidden in the whip / foreground wipe" is not achieved. Fix: put the swap on the frame of peak pan speed (g958-962, where the bench is still smearing) and add a foreground wipe (bench edge / chest / beam crossing the whole frame height) or motion blur on those 2-3 frames, so the character change is covered.
NOTES: legs end in thin stubs (rig); shoe contact shadow faint; Harrison's ponytail close to the right edge at g1019-1024 (face inside).
