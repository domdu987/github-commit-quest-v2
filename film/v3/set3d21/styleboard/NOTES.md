# set3d21 style board, re-render after QA-art REJECT (720x1280, 64 samples, Cycles CPU 4 cores)
Render: `python3 make_board.py` (renders all three, builds still1-3, board.jpg, phone.jpg, prints the colour table). Draft: `python3 make_board.py draft`.

## Measured (stirling_hue.py, caption band excluded; sharpness = Laplacian variance, y 0-320 / 320-640)
| still | red | orange | blue | violet | magenta | sat | val | dark | shade hue | top/middle sharp | render s (build s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| target | 30-41 (camp >=28) | >=20 | 14-30 | 0-5 | <=10 | .38-.48 | .45-.63 | .05-.15 | 240-260 | >=0.40 (valley) | <300 |
| 1 hill_over | 19.8 | 28.2 | 11.6 | 11.5 | 4.9 | 0.35 | 0.58 | 0.064 | 257.8 | 0.07 (sky, n/a) | 89 (3) |
| 2 camp_bank | 15.5 | 32.3 | 33.3 | 9.4 | 5.3 | 0.29 | 0.60 | 0.055 | 251.8 | 0.16 (sky, n/a) | 86 (4) |
| 3 valley_loop | 22.1 | 28.8 | 21.8 | 2.4 | 2.7 | 0.36 | 0.48 | 0.001 | 224.1 | 0.78 (465 / 594) | 104 (34) |
Heads (placeholder cards, y of head centre): hill_over 519-758, camp_bank 510-648, all above 880. Bridge in hill_over: x ~235-510, y ~520-570, about 280 px long, knights two by two.

## Still out of band (honest)
- valley_loop: dark share 0.001 (target 5-15 %) and shade hue 224 (target 240-260; the teal river dominates the shaded pixels). The luma floor is about 0.28 even with the world light off and the shade tint darkened.
- red below 28-30 on hill_over and camp_bank; blue 33 on camp_bank (target <= 30); sat 0.29 on camp_bank (target .38-.46); violet 9-11 on the two ground-level stills (shaded heather and grass).
- camp_bank: the river band at y 530-640 is about 100 px tall but thin at the far end; the bridge is only about 15 px tall (low 1.2 D camera, 150 m away), deck planks do not read, piers and knights do not read. The big flag-pole in the foreground still covers a lot of the frame.
- hill_over: the near field is a spiky purple/orange sprig carpet (reads as heather but busy); placeholder cards stand on a small levelled ledge (PAD) so the lens looks over its edge to the bridge.
- valley_loop: loop spans about 60 % of the width (target 65-80), Abbey Craig fully in frame upper right but only about 300 px wide; Scots line is a dark band of 90 boxes with spear tips at 2 px (reads as a dark seam); pavilions still read as striped umbrellas from above, with pennants.

## QA_ART fix list
1. valley_loop haze: DONE. Distance by colour only (haze capped 20-25 % toward #a39cec, far-hill mix 0.9 to 0.5, volume none). Top band 465 vs middle 594 = 0.78. Irregular Voronoi fields in 8 tints with furrows, hedgerows (3200 mounds and oaks), 10 farmsteads with smoke, lanes. Camera pitch 50 deg, horizon out of frame.
2. Organic river: DONE. Pear loop (21 control points, width 25-35 m), no glow outline, depth noise, teal #5cc8b4 to #0f5e74, broken shore foam, sparkle stretch, wide V wakes on piers (wake_k), mud/shingle bank strip, reeds. Reed clumps are only in camp_bank.
3. valley_loop framing: PARTLY. Hill in frame upper right with grey crag, heather, gorse, pines, 90-figure Scots line; neck near centre (x ~330, y ~640); river y 620-860; nearest camp above y 870. Loop width 60 %; cloud shadow slabs removed (they were banner shadows, banners no longer cast shadows); camp now 230 ridge/bell tents, 19 pavilions with pennants, 7 fires with smoke columns; no horse lines or carts visible at this scale.
4. camp_bank river and bridge: DONE in a reduced form: bank-edge camera 2 m up, teal water band with glitter, bridge visible across the frame (x ~235-500), hill with Scots-side crag at left, Cressingham x 178, Surrey x 640, nothing in x 260-560 at head height.
5. camp_bank warm and full: PARTLY. Low SE key (24 deg, sun_k 2.1), orange 32 %, long shadows, sky about 30 %; 6 pavilions, 15 tents, banners with lions/chevrons, fires, cart, weapon rack, horse line, pegs; grass spikes halved. Missing: red >= 28, sat, mud near bank is only a thin strip.
6. Abbey Craig crag: DONE. SW rock face (stepped), grey boulder stacks, heather mounds (brown/red-brown, no pink), gorse mounds with yellow flowers, red-trunk pine clumps; same model in all three stills.
7. hill_over hook: DONE. Camera on the slope, pitch -17 deg, lens 32, bridge x 235-510 y 520-570 (about 280 px), knights readable; castle rock moved to upper left at 70 % size; one pine at the left edge; no cobbles, heather/gorse instead; run path coloured on the slope. Slope fall is steep (45 deg+) and starts behind a levelled ledge.
8. Water rule: DONE for the three stills (layered water, foam, glitter, wakes). Other presets not built yet.
9. Life and density: PARTLY. Smoke columns, banners, farms, haystacks, Scots line (valley), 22 Scots extras with spears (hill_over). Not yet: settable column counts, camp_table preset, castle in valley_wide.
10. Cloud style: DONE (underside offset cut from 0.14 to 0.05, softer lavender). Clouds are still a flat painted sticker look at phone size; max about 25 % of the frame now.
