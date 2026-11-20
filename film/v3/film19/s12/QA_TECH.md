# QA_TECH s12 - FAIL
Checked: qa_auto PASS, 6 fps sheet g929-994, meta g0 938 / g1 985 (plan 31.26-32.85 -> 938/985 OK), handles 9/9, DIS 11 in OK, framediff median 4.19 / p90 16.41 OK. Default (greying, apron) Harrison OK, NIGHT OK, no text/blur, head centre y 464-580, mouth fixed (tired frown), eye-line to lens after snap OK, snap g952-972 visible.
Issues:
1. g929-959 (plan coverage): "candle stub burns down" is not readable. The one candle visible (left of the H3 frame) has the same height at g938 and g958 and scene luminance does not drop (mean 65.6 -> 66.3); after the snap (g964+) the candle is out of frame. Fix: keep the candle in frame (lower the camera slide or move the stub to the bench in front of H3), drive visible stub-length + flame-size 1.0 -> 0.3, and dim the set_candles key light.
2. g964-994: ~1 s of near-static huge head (head 401 px) with only a blink; the tapping (~2 Hz) is not visible after the snap. Fix: keep the chisel hand-stroke in frame or cut the move earlier.
3. g929-994: no contact shadow under the shoes (g929-959). Minor.
