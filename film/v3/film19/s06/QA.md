# s06 QA: film 19, shot 6 (HALL hall_table, DAY)
## Delivered
- take.mkv (libx264rgb crf 6, 30 fps, 128 frames, first_g 347): g 347-355 in-handle (DIS 13 from shot 5), g 356-465 = shot 6 (11.88-15.54 s), g 466-474 out-handle (CUT to shot 7). 720x1280, 8 spp, 2 threads. meta.json, cues.json, contact.jpg, QA_AUTO.md (PASS), phone_sheet.jpg, framediff.json.
## Shot
Two astronomers stand either side of the Board table. At "รางวัล" (g 378) set_moneybag('full') is keyed and the bag pivot is keyed to fall 1.8 m in 5 f, bounce twice and squash on landing. astro19 (left, faces right) and astro19_b (right, mirrored) lean in and widen their eyes ('excited', gaze on the bag). Camera: slow push, slide and arc, then a SNAP x2.4 with a pan (g 439-455) on "สองหมื่นปอนด์" (g 447) that ends on astro19 and the bag. Candles keyed every frame; mouths flat (no quote); no DOF, no text, no caption_shade.
## Numbers
- Frame-diff in-shot (90x160 grey): median 4.55, p90 6.71. Target median >= 4 (met), **p90 >= 12 NOT met**: the snap ends on flat green baize and a smooth face; stronger pans (shift 1.6 -> 2.4) reached 12 on drafts but ended in the chair back, and a leftward whip ended on empty bookcases, so the composed framing was kept. Camera never parked.
- 10.19 s/frame wall, 19.77 s CPU (two processes).
- Heads: while astro19_b is in frame his head is at y ~570-650; he leaves frame right during the snap (head_report values for him after g ~440 are off-screen). astro19's head bottom stays above y 880.
## Notes / deviations
- qa_auto first FAILED (suspected blur, 9 low-detail close frames of the baize). Fixed by starting closer and a smaller snap (x2.4 -> x1.7 zoom with less pan in the final): PASS.
- Final settings: snap k 1.7, shift 1.2, peak 1.4 (the p90 numbers above).
- The bag appears from above the frame at g 378 (not visible before it); table stays empty before "รางวัล".
- Foreground: chair backs and the table edge pass the lens.
