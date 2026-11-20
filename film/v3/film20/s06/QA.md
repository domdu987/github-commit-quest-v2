# s06 QA: film 20, shot 6 (artists outraged) -- CAFE cafe_wide, DAY, tower stub in the window
Delivered: take.mkv (29.6 MB, libx264rgb crf 6), first_g 395, 75 frames. Shot = g 404..465; in-handle g 395..403 (9 f, dissolve 13 in); out-handle g 466..469 (cut).
Render 25.1 s/frame wall, 47.3 s cpu (8 spp, 2 threads, two processes). Frame-diff in shot (90x160 grey): median 4.86, p90 13.94 (targets 4 / 12). qa_auto: PASS.
Checked at 6 fps + contact sheet: four artists (painter, composer, poet, architect) + waiter wave greeked newspapers / brush, sway, 3 Hz bounce; nobody frozen; mouths held (no animation); no text, no DOF; feet on the floor (floor z 0 verified by ray cast), contact decals on.
Snap x1.3 on "สี่สิบกว่าคน" g 442..457. FG: bentwood chair + marble table 1-3 D from the lens, the lens clears them for the whole move.
## Deviations
- Checker floor is ~30-35 % of the frame (target <= 25 %): more tilt only buried the frame in ceiling; the FG chair seat covers part of it.
- Heads are small (wide): 70-140 px, centres y 640-780 (wide exempt).
- Tower stub is only partly visible between the artists in the window (it is clear in shot 8).
- Push 8 %/s toward the table, slide 40 px/s to the LEFT (away from the FG table), not the preset's cafe_wide_end direction.
