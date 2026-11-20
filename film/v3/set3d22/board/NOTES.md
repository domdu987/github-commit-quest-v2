# Film 22 style board (set3d22)
Rebuild: `python3 film/v3/set3d22/beck.py board` (about 25 s; 720x1280, Cycles 14 samples + OIDN, 4 threads, no DOF). One still: `beck.py still <name> [preview]`.

| still | sat | luma | vivid | shade hue | render |
|---|---|---|---|---|---|
| london_dusk | 0.719 | 87.7 | 81.9% | 249 | 8.0 s wall (30 s CPU) |
| beck_lodgings_night | 0.542 | 112.1 | 55.0% | 253 | 6.7 s wall (26 s CPU) |
| platform_tunnel | 0.567 | 108.0 | 51.4% | 250 | 7.7 s wall (30 s CPU) |

Numbers: `stats.py` (sat = mean (max-min)/max at 360x640, luma = channel mean 0-255 as qa_stats2, vivid = share of pixels with sat > 0.5, shade hue = chroma-weighted mean hue of pixels with value < 0.5 and chroma > 0.1, caption band excluded). The stock tools/hue_report.py points at a missing scratch path, so it was not used.

## What each still tests
1. london_dusk: high wide view (about 40 deg down). Dusk key = low warm sun from the right, so camera-facing facades fall in blue shade while windows, lamp globes, canopy and grate glow warm. Tests the palette (orange horizon band, magenta-to-deep-blue sky, stars), the dense lit-window facades (PUBLICITY DEPT sign, HQ), the UNDERGROUND roundel, red bus, black cabs, lamp halos, river glitter, bridges, dome, clock tower, smoke, 100+ hatted crowd cards with painted rim light. Lodging house (Beck's lit window, ROOMS sign) is the dark foreground at bottom left.
2. beck_lodgings_night: Beck's own room. Key = green-shaded lamp (point light, right) plus a warm pendant; cool blue rim from the night window (HQ with roundel seen across the street) on Beck's card. Tests indoor amber against blue, the readable diagram (red/blue/green/yellow at 0/45/90 deg, rings, ticks), the NOTICE letter, ink bottles in line colours, T-square, set squares, the old tangled map and cork board of circuits (right, small), wallpaper, kettle, coat, rolled drawings, basket of crumpled paper.
3. platform_tunnel: eye-level view along the platform. Tiled vault with maroon band and ribs, globe lamps, PICCADILLY CIRCUS roundel, clock, WAY OUT sign, posters, pinned old map (left wall, grazing), MIND THE GAP board, benches. The key is the red train's headlamp at the tunnel mouth (spot light, backlight) plus globes. Crowd cards with maps along the platform edge.

## Known limits / next steps
- Old map and cork board in still 2 and the old map in still 3 are small at the frame edge; move them in the full build.
- Crowd cards are placeholders drawn in beck_tex.py (hats, folded maps); Beck and one extra are tower.placeholder_actor puppets with a repainted rim.
- Light presets: DUSK_CITY (sun key), LODGINGS and PLATFORM (point-lamp interiors) in beck.py LIGHTS.
- Signs use DejaVu Sans Bold; check 360x640 crops before final (PUBLICITY DEPT, UNDERGROUND, NOTICE, PICCADILLY CIRCUS read; ROOMS and the clock are small).
