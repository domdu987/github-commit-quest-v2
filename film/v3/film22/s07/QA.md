# s07 QA (render team 3) — g 823-937 (+8 handles each side: 815-946), 720x1280, 13 samples + denoise
Take file: `take.mkv.part00` + `part01` (cat them to restore take.mkv; 49.6 MB).
- qa_stats2: sat 0.689, vivid 76 %, luma 93.4 (in 85-110); frame-diff in-shot median 6.45, p90 21.4. qa_auto PASS (soft frames 815-817 only: motion streak at the start of the handle).
- Travel join J5: the camera path list is identical to s06's (same code, same spline), so g 822/823 are the same camera; official pose changes from eat_mime to toss_drawer, Beck is beck_sag in both.
- Mandatory items: official's head clear (dark in-tray / desk-items object hidden, chair kept); s07 slab gone (ceiling_off + south wall off + pub_shafts hidden); clerks visible laughing/pointing at their desks with a 0.06 D, 3 Hz bounce; official and Beck never cut by the top edge; PUBLICITY glass sign hidden after g 856 so the official shows from above. Beck walks out of the office through the glass door gap with the cast22 walk_sag cycle, contact shadow under every card.
- Deviations: Beck does not reach the far corridor door (path too long for 3.8 s); he leaves the glass office and heads along the aisle. From the high view the official is mostly hidden by the partition rail (only head/shoulders). The top 12 % of the high frames is empty dark blue (outside the building). Clerks' lower bodies are hidden by their desks (they stand behind them). Shade hue not measured.

## Final re-render notes (after director rules §K, §L, colour spec)
- Re-rendered without the hand-held sway; PATH shared with s06 (same list), s07 g 815-822 continue the s06 bite-mime pose and mouth; toss-the-sheet from g 832, slam at 28.08 s (g 845).
- qa_stats2: sat 0.697, vivid 77 %, luma 93.9; frame-diff median 9.3, p90 17.8; qa_auto PASS (soft frames g 862-863 are the retreat through the door); qa_jitter overall 0.38 px, no second above 2.0 px.
- hue_report (every 6th frame): red 12.4, orange 0.5, blue 29.2, violet 5.5, magenta 41.5, sat 0.71, val 0.58, dark 0.00 -> out of the new band (lilac/magenta wash of the set, not graded).
- GROUND.md PASS (clerk desks rebuilt, flags as in s06).
