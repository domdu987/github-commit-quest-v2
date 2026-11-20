# s12 QA: film 19, shot 12 (WORKSHOP shop_clock NIGHT, set_clock(3))
- Take g 929..994 (66 frames, 720x1280, 8 spp). Shot = g 938..985 (31.26-32.85 s); in-handle g 929..937 (dissolve 11 f in), out-handle g 986..994 (next shot is a cut). take.mkv crf 6, first_g 929. QA_AUTO PASS.
- Action: greying Harrison (default variant, apron) taps a chisel at the H3 (two round balances counter-rotate, set_balance every frame) by candlelight; the bench candle stub burns down (set_candles level 1.0 -> 0.3, keyed every frame, flame flicker). Snap g 952..972 (x1.4, peak 2.8, pan) on "สิบ" (caption g 960); he straightens and looks tired at the lens.
- Staging: he stands in front of the bench (offset from harrison_bench so the H3 does not hide him), contact shadow, feet on floor. Candle stub visible right.
- Heads 207-401 px wide (close at the end), centre y ~464-576, bottom < 681 (caption band clear). No text, no DOF, no caption_shade; mouth fixed.
- Frame-diff in-shot: median 4.19, p90 16.41 (draft 4.19 / 15.47). Night is dim, so this needed a strong drift (push 15 %/s) and a long snap.
- s/frame 15.8 wall / 31.1 CPU.
- Deviations: custom camera (preset cam hid him behind the H3; an early version drove into the right wall); shot is 1.6 s with a snap anyway (frame-diff).
