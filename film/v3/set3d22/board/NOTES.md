# Film 22 style board (set3d22)
Rebuild: `python3 film/v3/set3d22/beck.py board` (about 25 s; 720x1280, Cycles 14 samples + OIDN, 4 threads, no DOF). One still: `beck.py still <name> [preview]`.

| still | sat | luma | vivid | shade hue | render |
|---|---|---|---|---|---|
| london_dusk | 0.685 | 87.0 | 69.2% | 250 | 6.9 s wall (26 s CPU) |
| beck_lodgings_night | 0.645 | 98.2 | 63.9% | 256 | 6.4 s wall (25 s CPU) |
| platform_tunnel | 0.623 | 88.4 | 75.8% | 246 | 7.2 s wall (28 s CPU) |

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

## Round 2 (QA-art FIX-FIRST, all 8 items)
The numbers above are the round-2 renders. Each still was also checked as a 360x640 copy.
1. **1930s skyline (still 1).** Far field and south bank are now 8-14 high brick/stone blocks with pitched slate roofs, terracotta chimney stacks with pots, only about a third of the windows lit. The far skyline cards (`beck_tex.skyline`) are near-black blue roofs with chimneys, smoke, two spires, a gasholder, the dome with lantern and Big Ben (pinnacles on the near Big Ben, gold-trimmed face). Nothing on the horizon is taller than the clock tower.
2. **Sky.** CAM1 shift_y 0.19; magenta stop narrowed to 0.045 and desaturated, deep blue from 0.085: deep-blue top, magenta/purple about 6 % of the top 20 % of rows (3 % strict magenta), thin orange band between rooftops.
3. **Still 3 tunnel.** Vault tiles retinted cool blue-grey (`tiles_cool`, darker `tiles_cool_plain` arch), globes cut by about 40 % (then raised slightly for luma) so the vault is dark blue with warm practicals. The end wall now has a real round hole (annulus triangulation), a dark navy tube behind it, and the red train 12 D inside: only two headlamps, a halo and a warm spill on the track show; the headlamp spot (behind the wall) is the key and shines out of the hole. Top-third luma 92, overall 88.
4. **Still 2 reframe.** Camera z 5.0, lens 30, tilted down about 8 deg, room ceiling 13 D: ceiling about 10 % of the frame, floor/rug about 25 % but covered by the cot with patchwork quilt, the letter table, a trunk and the basket (the floor is the part still above the 20 % target). Old map (sepia, framed, 3.8 D wide, about 27 % of frame width) and the cork board of circuits (6.2 D) face the camera beside/above the board. Beck stands whole, right of the board, in front of the window (blue rim, contact shadow). Set squares moved to the ledge. Added: cot and quilt, kettle on a stove, coat stand, rolled drawings in a pot, T-square, bookshelf. Luma 98.
5. **Fill the floors.** Still 3: seated reader on the near bench (torso card cropped), porter's trolley with cases, vending machine, newspapers, suitcases, light pools; the dark slab is now a readable wooden bench. Still 1: more crowd cards on the near pavement and road, bigger NEWS and FLOWERS boards, extra railings and pillar boxes.
6. **Text.** WEMBLEY un-mirrored (left-wall posters, right-wall posters and the old map had reversed UVs; all fixed). MIND THE GAP board moved clear of the cards. Platform old map moved to the end wall, facing the camera, about 13 % of frame width. ROOMS is now a horizontal board standing on the pavement; NEWS and FLOWERS signs enlarged; diagram station labels enlarged. Checked at 360x640: PUBLICITY DEPT, UNDERGROUND, NEWS, NOTICE, PICCADILLY CIRCUS, MAP OF LONDON read; ROOMS is cropped by the frame edge and WAY OUT is small.
7. **Props.** Red (#c8201e) double-decker with two lit window rows, cream band, open rear platform and stair, front route board, with a warm light on its side. Dome in stone colour; Big Ben features.
8. **Contact shadows.** Dark soft discs under every crowd card in stills 1 and 3 and under Beck in still 2 (rim light kept).

Known remaining: Beck holds no pen (placeholder puppet pose is fixed); the still-2 floor share is above 20 %; the dome and clock tower are simple shapes.
