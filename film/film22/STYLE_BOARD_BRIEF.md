# Film 22 style board brief (builder: Sonnet)
Film: "ไอ้ช่างวงจร": Harry Beck draws the London Underground diagram, 1931-33. Read film/film22/WORLD.md (the world and the look), film/film22/script/script_th.txt, film/QA_TEAM.md §G, §H and §I, and look at film/ref_shorts/R3_sheet.jpg, R5_sheet.jpg, R2_sheet.jpg (the target look: bold saturated colour, motivated light, rim light, dense sets, short in-world text signs).

PROJ = /home/user/github-commit-quest-v2/film (work in the repo; everything is path-relative). bpy 5.3 is installed (`python3 -c "import bpy"`). 4 cores: render with 4 threads, one render at a time.

## Goal
3 stills (720x1280, Cycles, about 12-16 samples with denoise, NO depth of field, sharp) that set the LOOK of the new world before it is built in full: palette, detail level, the key light presets. Build them in the module that will grow into the full set:
- `film/v3/set3d22/beck.py` (locations, cameras, CLI) and `film/v3/set3d22/beck_tex.py` (painted textures with numpy/PIL, including the signs and the diagram artwork).
- Output: `film/v3/set3d22/board/board_1.png` .. `board_3.png`, `film/v3/set3d22/board/style_board.jpg` (the 3 side by side, labelled under each tile, cyan line at y 880 on each tile), and `board/NOTES.md`.
- `python3 film/v3/set3d22/beck.py board` must rebuild the three stills.

## Reuse helpers, never an old set
NEW set: do not render any older location. You MAY import helpers the way v3/set3d10/harbour.py does (read its top and v3/set3d10/API.md, and v3/set3d9/wall.py): `tower.make_camera/render/mat_lit/mat_emit/setup_grade`, `mine.obox/rod/lumpy`, `bakery._halo`, `desert._mat_sky`, `wall._air_comp` ... Man-made props get thickness and the 3 px inverted-hull ink (sets.md); never ink sky, water, smoke or glass glow. Skill chapters: film/skill/reference-style-shorts/references/bible/sets.md (8-9), colour-light.md, camera.md (lens 22 mm on 36 mm sensor).

## The three stills (placeholder actor cards are fine; scale 1 unit = 1 head D, a person is about 3 D tall)
1. **london_dusk** (high wide, about 30-45° down, looking over the street to the city): the Underground HQ building with rows of warm lit windows (one big window labelled PUBLICITY DEPT; across the street a narrow lodging house with Beck's lit window), the street with the station entrance (big red ring + blue bar UNDERGROUND roundel, lit canopy, steps down), a red double-decker bus, black cabs, lamp posts with halos, a pavement grate glowing warm from below, crowds (placeholder cards) with hats; beyond: roofs and chimneys with smoke, the Thames with a bridge and glittering reflections, a big dome and a clock tower; deep blue dusk sky with a warm orange band at the horizon and a few stars. Dense: 25+ distinct objects.
2. **beck_lodgings_night** (Beck's own small room at home: he was laid off when he drew it; homely wallpaper, kettle, a letter marked NOTICE on the table; NO 'DRAWING OFFICE' sign) (medium-wide, slightly low, 3/4 view): Beck's drafting board in front, the diagram on it bright and readable (straight red, blue, green, yellow lines at 0/45/90°, white interchange rings, ticks), a green-shaded lamp as the key (warm pool), a cool blue rim from the night window behind (city lights outside), the OLD tangled geographic map pinned on the wall beside the board, a cork board of circuit diagrams, ink bottles in the line colours, T-square, set squares, rolled drawings, tea cup, a waste basket of crumpled paper. Warm amber room against the blue window.
3. **platform_tunnel** (eye level, along the platform toward the tunnel mouth): curved tiled vault (cream tiles with a maroon or green band), globe lamps, a big station-name roundel (e.g. PICCADILLY CIRCUS), posters, benches, a pinned old cramped map, a clock, WAY OUT sign; the tunnel mouth deep dark blue with the warm headlight of a red train coming out; a crowd of placeholder passengers along the platform edge, some holding small folded maps. Deep blue + warm lamps + red train.

## Look rules (client, hard)
- Sharp, no DOF, no blur, no haze over the frame. Saturated: mean saturation ≥ 0.50 (max-min over max, per pixel, averaged) and mean luma 85-110 on 0-255; measure with `python3 film/qa_stats2.py <png or mp4>` if it accepts images, else compute the same numbers with numpy. Shade hue 240-260 (v3/tools/hue_report.py).
- Motivated key light in every still and a rim light on the actor cards (show it with placeholder cards).
- Text signs: short, sharp, readable on a phone (check at 360x640). Nothing important and no text in the caption band y 880-950.
- Layered depth: a dark foreground prop within the nearest 15 % of the frame, the lit subject band, a far wall or skyline. No empty floors or bare walls.

## Done
The 3 PNGs + style_board.jpg + NOTES.md (numbers per still: saturation, luma, vivid %, shade hue, render seconds; what each still tests) + runnable `beck.py board`. Do not commit; the director commits. Report paths and numbers.
