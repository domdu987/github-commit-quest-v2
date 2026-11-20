# s11 QA: film 19, shot 11 (WORKSHOP shop_wide DAY, set_clock(1))

- Take: g 853..946 (94 frames, 720x1280, 8 spp, 2 threads). Shot = g 862..937 (28.74-31.26 s); in-handle g 853..861 (dissolve 15 f in), out-handle g 938..946. `take.mkv` libx264rgb crf 6, first_g 853. QA_AUTO PASS.
- Action: young Harrison (young=1, brown hair) files at the H1 (file19 prop, 2.5 Hz stroke); H1 bars rock (set_balance(g/30) every frame), candle flicker keyed every frame. Snap g 912..930 (18 f, x1.5, peak 2.2, pan) on "ห้าปี" (caption g 918, word ~g 925): he stops filing and looks up with a smile.
- Staging: Harrison stands IN FRONT of the bench at (3.03, 2.69) with the H1 behind him (offset from the mark so the H1 does not hide him); contact shadow on; feet on floor. Sawhorse plank, plane, stump/rug in FG.
- Heads: 153-302 px wide, centre y 506-592, bottom max < 680 (caption band y 880 clear). No text, no DOF, no caption_shade. Mouth fixed (no quote).
- Frame-diff (in-shot, 90x160 grey): median 4.01, p90 12.78 (draft 4.77 / 12.49). Targets met (median has little margin).
- s/frame: 20.2 s wall / 38.8 s CPU (two processes, other renders ran during the first minutes).
- Deviation: Harrison is not at harrison_bench behind the clock (the H1 hid him); the camera is a custom path, not the preset.
- Known: the file blade reads as a thin dark/silver rod; the plank fills the lower FG until the snap.

## Re-render (after QA_TECH notes + the lantern set fix)
- Re-rendered with the new iron-cage lantern (h19_shop.py from film19/main). The file hand is raised and pushed out so the file tip reaches the H1's base on the bench (hand (1.0, 1.45)); frame-diff median 4.02 / p90 12.78.
- Contact shadow: cast19 contact decal is on; the legs still end in thin white stubs behind the plank (rig limit).
