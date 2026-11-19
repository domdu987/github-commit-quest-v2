# s02 QA: film 16, shot 2 (2.31-3.66 s) -- LINE line_wide, DAY
- Delivered: take.mkv g 60..118 (59 frames; shot = g 69..109, 9 handle frames each side), 720x1280, 7 spp, libx264rgb crf 6; meta.json, cues.json, contact.jpg, phone_sheet.jpg, QA_AUTO.md (PASS), framediff.json.
- Shot: the plan's one WHIP: the look point starts 11 D off the line (fence and wheat) and whips back onto it over g 66..80 (cubic ease-out; the first in-shot frames g 69..72 are still mid-whip), then crane down 85 px/s + push 9 %/s + slide 85 px/s + arc 7 deg/s to the end, still moving on the last frame. Morse (cast16 morse_proud_point) at the ladder foot points along the pole row (marching bottle-necked poles to the horizon), small sway, pointing hand sweeps, blinks at g 66 and 97. Train creeps in the far left with smoke.
- Checked at 6 fps: heads 106-158 px wide (wide-shot range, small head grows with the push), head centre y within the frame, in-shot head bottom max y 739 (< 880); the meta.json max 893 is on handle frames g 60..66 where Morse is still off screen (x < 0) during the whip. No mouth movement (smile expression only). Contact shadow on the grass.
- Frame-diff (90x160 grey, in-shot, includes the whip): median 5.29, p90 27.48 (target 4 / 12).
- No streak added on the whip (not needed to read); noted as a conform option. Morse is drawn unmirrored; he points to screen-right along the poles.

## Re-render (director / QA-art FIX list)
- Reframed: camera 2.7 D up on the road side, 4 D from Morse, looking along the pole line (yaw toward the row, slight tilt up): Morse is medium (head 161-271 px in shot, centre y 501-636, bottom max 718 < 880), the hero pole's bottle cap is ~150-200 px at the top and the row of capped poles marches away to the right behind him (the plan's "marching to the horizon" is kept, the caps are no longer ~10 px). The preset's own foreground belongs to the preset camera, so it is hidden and a new foreground (crate of bottles, crate, spool dome, rail grass) is built round the start camera with the set's fg_dress: the lower third is props and grass, not empty ground.
- Eye-line: gaze (1.0, -0.05) + yaw 0.5: Morse looks down the line he points along.
- Move: whip arrival kept (g 66..80); then push 6 %/s, slide 100 px/s, arc 12 deg/s, crane -20 px/s; still moving at the cut.
- Frame-diff in-shot: median 6.84, p90 22.04 (whip included). QA_AUTO PASS.
