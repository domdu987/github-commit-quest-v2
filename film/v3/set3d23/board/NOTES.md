# Film 23 style board (builder notes)
Rebuild: `python3 film/v3/set3d23/ghost.py board` (3 finals 720x1280, 12 samples, Cycles CPU 4 threads, OIDN, no DOF; then style_board.jpg + numbers.json).
Modules: ghost.py (lights, shared toon material, camera, CLI), ghost_tex.py (painted textures), ghost_props.py (rubber M4 tank with `inflate` / `sag`, truck + horn, gun, nets, crates, pump, bike...), ghost_scenes.py (3 compositions), ghost_hue.py (numbers), board.py.

| still | sat | vivid % | luma (rgb mean) | magenta % | shade hue | wall s | cpu s |
|---|---|---|---|---|---|---|---|
| 1 dawn_fields_high | 0.551 | 58.6 | 105.8 | 0.6 | 234.2 (target 240-260: MISS) | 6.6 | 24.0 |
| 2 inflate_lane_morning | 0.616 | 55.4 | 108.7 | 0.7 | 244.1 | 5.6 | 20.6 |
| 3 night_sound_truck | 0.633 | 55.6 | 94.5 (night band 70-95) | 1.2 | 237.4 (MISS) | 7.6 | 28.4 |

What each tests: 1 patchwork fields, hedgerows, 10 rubber tanks on a lane (3 nets), farm + camp, village, river, dawn gold rim; 2 half-inflated tank (inflate 0.66, sag 0.85), readable stencils and sign, bike on wall, warm rim light; 3 moon key + warm lantern/tent emitters with halos, sound-truck horn.
Weak: see the report to the director (tank small in still 2, pumper/clip soldiers hidden, shade hue 3-6 deg low on 1 and 3, flat painted ground, plain lane foreground, night tank rows read as lumps, caption band 880-950 not fully clear).

## r2 changes (QA-art FIX-FIRST)
- Shade: lighter, less saturated blue-violet (shade/tint/lift raised), per-scene exposure; shade hue 231.7 / 235.5 / 242.3 (target 242-250: only still 3 in band).
- Still 2 rebuilt: tank centred (~50%% width, inflate 0.66, sag 0.9, valve + star toward camera, hose into valve), soldiers beside it, bike at right edge, sign words whole; foreground: puddle, flat rubber sheet, hose coil, toolbox, straw, chickens; smoke white-grey.
- Still 1: tanks skipped where they would sit in the caption band; smoother textured hills + treeline; soft clouds.
- Still 3: dark olive tank silhouettes with cool rim, halo_r 1.6, deep flared metal horn, ground filled (tufts, cables, crates), soldier off the pole.
- Rubber spec 0.22, ink seam lines on hull.

| still | sat | vivid | luma | magenta | shade hue |
|---|---|---|---|---|---|
| board_1.png | 0.609 | 63.9 | 98.3 | 0.6 | 231.7 |
| board_2.png | 0.585 | 47.1 | 106.8 | 0.5 | 235.5 |
| board_3.png | 0.634 | 48.5 | 87.4 | 1.1 | 242.3 |
