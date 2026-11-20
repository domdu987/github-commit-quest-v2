# s10 QA: film 20, shot 10 (CAFE cafe_low_close, DAY, view stub): QUOTE 1 lip-sync
Delivered: take.mkv g 672..756 (85 frames; shot g 676..752, 4-frame handles each side, cut in / cut out), 720x1280, 8 spp, 23.11 s/frame wall (36.38 cpu).
Beat: he turns his back on the window (yaw +0.30 -> -0.60 over g 676-712), arms crossed, eyes shut behind a blink at g 685; chin-jerk on "มันสักครั้ง!" (g 732), snap push + 48 deg orbit g 729-742. Orbit + push all shot (frame-diff).
LIP-SYNC: g 682..755 only (22.62-25.11 s narration clock, +0.10 s). Mouth = narration RMS loudness per frame (1-frame window, 3-frame smoothing, 2-frame hold): flat under 10 % level, cast20.talk_mouth (talk_a/b/o) in the mid levels, ('open', .12,.05) / (.20,.10) / (.30,.19) by loudness. g 676..681 mouth flat (pose mouth), nothing outside the window. Lip-sync table: `python3 shot.py mouth`.
Numbers: head 235-313 px wide (peak at the snap, ~25 % of frame height: under the 35 % limit), centre y 603-644, lowest head bottom y 769 (< 880); head never cut by an edge.
qa_stats: saturation 0.576, luma 94.5, in-shot motion median 5.19 / p90 9.60. Own frame-diff (deliver.py): median 4.54 / p90 11.1 (target 4 / 12; p90 slightly under).
qa_auto: PASS (QA_AUTO.md). Phone sheet and 6 fps contact sheet checked.
Deviations: p90 under 12 (snap limited by the 35 % head rule; k 1.25). The plan's "artists nod" is not shown: the artists are not in frame from cafe_low_close. Camera starts ~1 m left of the preset spot (orbit start -30 deg) so the window shows the stub tower on the right.
