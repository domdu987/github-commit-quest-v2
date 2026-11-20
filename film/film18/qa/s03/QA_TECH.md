# QA_TECH s03 (take g147-298; in-shot g156-296) - FAIL
Checked: 6 fps frames + first/last 3; frame-diff re-measured (90x160 grey, AREA, 140 in-shot pairs): median 6.65, p90 11.54 (min 3.19, max 13.44). Caption band y880-950 mean 74-106, bright 0.00 %.
## Issues
1. whole shot - rule 1 (zoom pulsing): the motion comes from "push punches every 10 frames" (QA.md); the frame-diff is a repeating 11-frame burst (3.5 -> 10 -> 10 -> 4.7 -> 10 -> 10 -> 3.4). Between bursts the camera is near-static. Fix: remove the punches; use one eased push + slide.
2. whole shot - p90 11.54 < 12 (rule not met).
3. g147-258 - rule 5, bare ground: the bottom 40-50 % of the frame is flat, empty tiled green/violet ground (towns only in y 150-300 of 427) with stray dark spike shadow triangles. Only after g~260 do the towns fill the lower half. Fix: tilt or push so the towns/flag forest fill >= 75 % of the frame from the first frame.
4. g147-282 - sky ~35 % flat orange gradient with scalloped cloud stickers clipped at the top-left corner (g147-212) and top-right (g222-282). Fix: drop the sticker clouds, tilt down.
5. mandatory "pennants pop up": MET - black pennants appear one after another from g~227 (7.5 s) and are dense by g~262 (plan window 7.32-9.89 s). No issue.
## Notes
- Ending frames g296-298 and the dissolve handle g147-152 look the same set; the dissolve in is fine.
- Caption band is mid-dark, no bright emitters.
- No text, no characters, no oxen, no mouths.
