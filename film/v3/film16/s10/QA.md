# s10 QA: film 16, shot 10 (CHAMBER, DAY, low close on the mocker, quote 2) -- re-render after the TAKE gate
- Frames g 588..706 (119): shot g 597..697 (19.91-23.26 s), 9-frame handles each side (hard cuts). 720x1280, 6 spp. take.mkv crf 6, first_g 588.
- Gate fix: the camera is now ~2 D from the mocker from the first frame (1.75 D horizontal, 1.85 D up, pitch ~25 deg up): head 367-539 px wide (face disc ~300-450 px), so the cut from s09 (face 269 px) goes CLOSER. Head centre y 409-533 (a little under 450 at the push-in's top), bottom max 753 (band y 880 clear).
- Mouth LIP-SYNC (talk_mouth, closed on the last 2 frames of each phrase) the whole shot = inside the quote window 18.32-23.20 s (+0.10 s). boast_finger to g 661, blink swap g 662, boast_chest (thump) to the end. Blush; no tears.
- Punch-in on "เฝ้ามันเอง" (g 677): snap x1.3 over g 672..686 (the close camera needs little zoom) with 80 focus lines (was 34; the puppet draws them as thin strokes, so they stay fine, but denser).
- Frame-diff in-shot (g 598..697): median 8.46, p90 14.52. qa_auto PASS.
- Differs from the plan/gate: focus lines remain thin strokes (the puppet fx has no width parameter); desk-corner FG is out of frame at this distance.
- s/frame 11.4 wall / 20.4 CPU.
