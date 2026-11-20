# s09 QA: film 20, shot 9 (CAFE cafe_low, DAY, view stub): Maupassant rises
Delivered: take.mkv g 600..679 (80 frames; shot g 604..675, 4-frame handles each side, cut in / cut out), 720x1280, 8 spp, 22.58 s/frame wall (43.88 cpu).
Beat: seated-crouch -> rises (legs crouch 0.6 -> 0, step forward, lean) g 612-640, two cravat tugs g 640-658, chin up smug g 654-668; snap push+orbit on "ก็ประกาศลั่น" g 657-670; crane up + orbit all shot. Mouth held flat the whole shot (quote starts g 682).
Numbers: head 152-230 px wide, centre y 658-740, lowest head bottom y 855 (< 880); no head > 35 % of frame height.
qa_stats: saturation 0.556, luma 96.5, in-shot motion median 5.04 / p90 10.02. Own frame-diff (deliver.py): median 4.41 / p90 10.36 (target 4 / 12: p90 slightly under; the snap is limited by the head band).
qa_auto: PASS (see QA_AUTO.md). Checked contact sheet / phone sheet at 6 fps.
Deviations: there is no seated Maupassant puppet on a banquette: he starts in a crouch with the banquette behind him (reads as perched on its edge, feet on the tiles with a contact decal) and straightens. Floor share ~20-25 % in the first 20 frames. p90 10.0 < 12.
