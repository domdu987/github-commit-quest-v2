# QA_TECH s03 (take g147-298, in-shot g156-296) - FAIL
Checked: 6 fps frames + first/last 3. Frame-diff re-measured: median 6.48, p90 8.35 (min 4.2, max 8.8). Smooth monotonic ramp 4 -> 9 -> 7: NO pulsing now. p90 < 9 but orbit parallax is visible (guide only).
## Earlier blockers
- E1 pulsing: FIXED (orbit, smooth diff).
- E3 bare ground: NOT FIXED. E4 sticker clouds clipped at the corners: NOT FIXED. Spike shadow triangles: NOT FIXED.
- Pennants pop-up mandatory: met (black pennants appear g~232-262, dense by g~270).
## Issues
1. g147-232 - bare ground: the bottom 45-60 % of the frame is empty tiled grey-green ground (towns only in a band at y 0.35-0.65); until g~205 about 55 %, g205-232 about 35-40 %; even at g257-298 the bottom 25 % is plain ground. Far over 30 %. For ~55 % of the take the viewer sees sky plus an empty field. Fix: tilt/lower the camera so towns fill >= 75 % of the frame from the first frame, or fill the field.
2. g147-298 - rule 2: dark blue spike/cone shadow triangles stand on the empty ground (g147-215 and g257-298, growing in size as the camera lowers); they read as untextured placeholder spikes. Fix: hide them.
3. g147-170 and g257-298 - clipped cloud stickers at the top-left (g147-170) and top-right (g257-298) corners (scalloped flat cloud shapes cut by the frame edge). Fix: drop the cloud sprites.
4. g147-232 - sky about 35 % flat orange gradient.
## Notes
- no text, no characters, no mouths; band mid-dark, no bright emitters.
- dissolve handle g147-155 shows the same set; s04 follows as a cut, check pairing at conform.
