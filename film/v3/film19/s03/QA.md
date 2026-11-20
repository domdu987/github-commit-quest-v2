# s03 QA: film 19, shot 3 (HALL hall_window, DAY)
## Delivered
- take.mkv (libx264rgb crf 6, 30 fps), first_g 101, 99 frames: g 101-109 in-handle (CUT from shot 2), g 110-190 = shot 3 (3.65-6.37 s), g 191-199 out-handle (DIS 13 into shot 4). 720x1280, 8 spp (set's own), 2 threads.
- meta.json, cues.json, contact.jpg, QA_AUTO.md (PASS), phone_sheet.jpg, framediff.json. Its only note, 'cut g 110 has no visible change', is expected (the handle continues in 3D).
## Shot
astro19_b (mirrored) bends to the brass telescope eyepiece, squinting; astro19 beside him scratches under his wig (3 Hz scrub), puzzled. Chair and tripod leg pass through the foreground. SNAP x2.0 (15 f, g 169-184) with a pan on "ทำไม่ได้" (g 177): astro_b straightens from the eyepiece with a frown. Candles keyed every frame; no DOF, no text, no caption_shade (dof false / caption_shade false in every raw json).
## Numbers
- Head width 112-345 px, head centre y 553-656, lowest head bottom y 766 (< 880).
- Frame-diff in-shot (90x160 grey): median 4.75, p90 15.64 (draft 4.75 / 15.5). Camera never parked (camreport: 0 frames under 0.25 px).
- 14.92 s/frame wall, 28.74 s CPU (two processes).
## Notes / deviations
- Mouths: flat for both (no quote in this shot). Characters stand on the floor with contact decals.
- The camera arc (-21 deg/s) is strong to reach the frame-diff target; at g 185-199 a dark tripod leg crosses the left foreground and astro_b's head is large (x 15-60 px at the end of the handle, inside the frame during the shot).
- The tripod leg renders very dark (set material); it reads as a foreground occluder.
