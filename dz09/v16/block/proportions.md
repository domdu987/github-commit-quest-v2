# proportions.md -- DZ09 blocky cast, measured on the v3 sheets

Measured by `measure_sheets.py` with PIL / numpy / OpenCV on the turnaround rows of `uploads/sheets_v3/kong.png` and `uploads/sheets_v3/z_office.png`.
Silhouette extents and widths come from a background-distance mask (largest component per view; the sole row is the lowest *dark* row, so the soft ground shadow is not counted).
Internal lines (chin, belt, crotch, hem / boot top, fist top and bottom) are landmark rows read off 3x gridded crops (`out/g_*.png`) and drawn back onto `out/proportions_annot.png` for checking.
Heights: Kong 1.80 m (sheet info box and the lineup), office zombie ~1.75 m (sheet). Raw numbers: `out/proportions.json`.

| measure | Kong sheet | Kong metres | Kong model | Office zombie sheet | zombie metres | zombie model |
|---|---|---|---|---|---|---|
| hair top to chin / H | 0.261 | 0.469 | 0.261 | 0.278 | 0.487 | - |
| head cube width / H (front, 7 px above the chin) | 0.205 | 0.369 | 0.205 | 0.240 | 0.420 | 0.240 |
| head depth / H (side, same row; includes hair hanging at the back) | 0.231 | 0.416 | 0.205 | 0.244 | 0.427 | 0.235 |
| hair width / H (widest row above the eyes) | 0.293 | 0.528 | - | 0.346 | 0.606 | - |
| shoulder span / H (outer sleeves) | 0.645 | 1.161 | 0.626 | 0.660 | 1.156 | 0.660 |
| fists span / H | 0.625 | 1.126 | - | 0.671 | 1.174 | - |
| chin to belt / H | 0.287 | 0.516 | 0.285 | 0.308 | 0.539 | 0.304 |
| chin to crotch / H | 0.469 | 0.844 | 0.481 | 0.403 | 0.706 | 0.422 |
| crotch to sole / H | 0.270 | 0.487 | 0.258 | 0.319 | 0.557 | 0.300 |
| boot / shoe height / H | 0.143 | 0.258 | 0.143 | 0.079 | 0.138 | 0.080 |
| fist height / H | 0.147 | 0.264 | 0.147 | 0.149 | 0.260 | 0.149 |
| legs span at the shin / H | 0.397 | 0.715 | - | 0.446 | 0.780 | - |
| boot length / H (side, dark sole rows) | 0.316 | 0.569 | - | 0.280 | 0.491 | - |
| torso depth / H (side, mid torso, incl. arm and pouches) | 0.254 | 0.457 | - | 0.229 | 0.401 | - |

Front view pixel heights: Kong 307 px (5.86 mm/px), zombie 471 px (3.72 mm/px). All views: front 307, q45 308, side 302, back 301, back45 302 / front 471, q45 471, side 470, back 471, back45 467.
Fist row runs (front, px): Kong [[332, 522]] (one run: the fists touch the pouches), zombie [[242, 303], [320, 475], [491, 553]] (fist 61 px = 0.13 H wide).

## Reading

- Head about a quarter of the height incl. hair: Kong 0.26 H, zombie 0.28 H (hair top to chin).  The head cube itself is 0.205 H (Kong, 0.37 m) and 0.24 H (zombie, 0.42 m) wide: the zombie sheet draws a bigger head.
- Shoulders much wider than the head: shoulder span 0.645 H = 3.1 head widths (Kong), 0.66 H = 2.75 head widths (zombie).  At 1.80 m that is a 1.16 m span: toy proportions, about twice the puppet Kong's shoulder width at the same height.
- Short legs: crotch to sole 0.27 H (Kong), 0.32 H (zombie, the crotch hidden by the shirt tail, read where the legs part).  Big boots: 0.14 H (Kong); low shoes 0.08 H (zombie).
- Fists are big blocks: 0.147-0.149 H tall, 0.12-0.13 H wide.
- Model column = the numbers in `blockcast.SPECS` (fractions of H): the shoulder span is joint x * 2 + sleeve width; the head is a cube 0.205 x 0.205 x 0.190 H (Kong) / 0.240 x 0.235 x 0.220 H (zombie) with a 0.036-0.042 H soft bevel; hair adds the rest up to the measured hair top.
- Not measured: the cube's height under the hair (hidden by the fringe; set to 0.92 of the width), arm joint positions (the sheet arms hang straight; elbow placed at 0.545 H), torso depth without the arm.

## Check: the same measures on our turnaround renders (`measure_ours.py`, ortho camera, cream studio)

| measure / H | Kong sheet | Kong ours | zombie sheet | zombie ours |
|---|---|---|---|---|
| hair_top_to_chin | 0.261 | 0.257 | 0.278 | 0.256 |
| head_cube_w | 0.205 | 0.233 | 0.240 | 0.317 |
| hair_w | 0.293 | 0.329 | 0.346 | 0.399 |
| shoulder_span | 0.645 | 0.685 | 0.660 | 0.703 |
| hands_span | 0.625 | 0.685 | 0.671 | 0.703 |
| leg_span_at_shin | 0.397 | 0.319 | 0.446 | 0.440 |
| head_depth_side | 0.231 | 0.227 | 0.244 | 0.307 |
| foot_len_side | 0.316 | 0.309 | 0.280 | 0.281 |
