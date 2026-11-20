# s12 QA: film 19, shot 12 (WORKSHOP shop_clock NIGHT, set_clock(3))
- Take g 929..994 (66 frames, 720x1280, 8 spp). Shot = g 938..985 (31.26-32.85 s); in-handle g 929..937 (dissolve 11 f in), out-handle g 986..994 (next shot is a cut). take.mkv crf 6, first_g 929. QA_AUTO PASS.
- Action: greying Harrison (default variant, apron) taps a chisel at the H3 (two round balances counter-rotate, set_balance every frame) by candlelight; the bench candle stub burns down (set_candles level 1.0 -> 0.3, keyed every frame, flame flicker). Snap g 952..972 (x1.4, peak 2.8, pan) on "สิบ" (caption g 960); he straightens and looks tired at the lens.
- Staging: he stands in front of the bench (offset from harrison_bench so the H3 does not hide him), contact shadow, feet on floor. Candle stub visible right.
- Heads 207-401 px wide (close at the end), centre y ~464-576, bottom < 681 (caption band clear). No text, no DOF, no caption_shade; mouth fixed.
- Frame-diff in-shot: median 4.42, p90 13.37 (re-render after the director's QA-tech FAIL). Night is dim, so this needed a strong drift (push 15 %/s) and a long snap.
- s/frame 15.8 wall / 31.1 CPU.
- Deviations: custom camera (preset cam hid him behind the H3; an early version drove into the right wall); shot is 1.6 s with a snap anyway (frame-diff).

## Re-render (after QA_TECH FAIL + the lantern set fix)
- Re-rendered with the new iron-cage lantern (h19_shop.py from film19/main).
- Candle burn-down now reads: at runtime the bench stub and its point light are moved onto the foreground chest (it stayed in frame only at the far left before), set_candles level 1.0 -> 0.12 keyed every frame (stub 17 cm -> 2 cm, flame follows), in frame for the whole shot.
- Tapping continues through the end of the shot (bigger stroke, the straighten/look-up moved out of the shot); snap x1.45 g 952..972.
- Head 198-420 px wide, centre y 463-580. Contact shadow: cast19 contact decal is on; the legs still end in thin stubs (rig limit).
