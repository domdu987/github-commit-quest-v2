# s18 QA: film 19, shot 18 (the ship under full sail) -- SHIP ship_hero, NOON  (round 10)

## Delivered
- `take.mkv` (libx264rgb crf 6, 32.4 MB, one file, no parts): first_g 1375, 102 frames, 720x1280, 12 spp, 2 threads. No captions / audio.
- g 1375..1383 in-handle, **g 1384..1467 = shot 18 (46.12-48.92 s)**, g 1468..1476 out-handle. Join in: dissolve 11 from shot 17; out: dissolve 13 into shot 19.

## Round-10 fixes
- **Colour:** exposure -0.8 EV on top of the colour-fixed set, the pale horizon band of the NOON sky deepened (runtime edit of the light table), 30 % fewer foam lines (40 -> 28). **qa_stats: luma 100.7 (target 100-110, band 85-110), saturation 0.644.**
- **Story:** william19 stands on the forecastle (port side, in front of the foremast) holding the H4 watch on his open palm: "his son carried it across the sea". He is drawn at 4x scale so he reads on a phone (head 26-39 px wide); he rides `ship_root`. The bow itself is hidden behind the jibs from this camera, so he stands just aft of them. (A palm island was not added.)
- **Sun glint:** the `glint` light x0.03: the blown white hole at the bottom right (g 1395-1415) is gone.
- **No parking:** a second gentle move g 1446-1476 (x1.05 and a 0.8 D pan) keeps the camera moving after the snap; camreport: 0 frames under 0.25 px/frame.
- Kept: ship fully in frame, the snap on "จาไมกา", the crests, the floating spar. DOF off, no text, no caption_shade in every raw json. qa_auto PASS.

## Frame-diff (in-shot g 1385..1467)
median **4.79**, p90 **9.96** (qa_stats on all frames: 5.17 / 10.90). Targets: median >= 4, p90 >= 10: met (p90 is on the line; the qa_stats measure is 10.9).
