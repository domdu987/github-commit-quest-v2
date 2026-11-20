# QA sJ1 (film 21 plan v3 segment J1, g 1640-1708, 69 frames, CUT in, whip pan left out, no handles)
camp_table in build_world on set3d21 e07ceb1 (crimson/gold canopy) + cast21 528bf9d; 32 samples, default VIVID grade.
- Cressingham's EMPTY money table: stool with his cloak, "KING'S TREASURY" chest, lantern (flicker), coin scale, ledger. Nobody staged. Rug stripes (`table_extras_t_gold`) hidden; the rug cloth is out of frame (<12 %).
- Camera: one slow arc + push in (about 8 %/s, 5.0 -> 4.3 m, swinging from -7 to +7 deg around the table), start framing keeps chest and scale both in frame; last 6 frames (g 1703-1708) whip pan left (accelerating yaw to 95 deg).
- Beats: scale tips on "เร็วดี" g 1677 (set_scale_tip, damped overshoot), chest lid slams on "ประหยัดดี" g 1690 (set_chest_lid 72 -> 0 in 3 frames with a small rebound). Flags/smoke/water hooks keyed every frame.
- Numbers: saturation 0.518, luma 105.9, rhythm in-shot median 5.6 / p90 7.2 (the take has only a gentle push before the whip); qa_auto PASS (g 1707 is the whip streak).
- Known: ground fills the lower ~30 % (dark dirt, no rug); the scale beam is at the right edge of the frame during the tip (partly cut by the edge at the end of the push); no characters in this segment by design.
