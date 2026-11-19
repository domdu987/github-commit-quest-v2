# set3d15 style board (Fosbury Flop)
Run: `python3 sb.py a|b|c|all [draft]` (helpers adapted from ref_sb14.py; box/sphere/rod builders replaced with O(1) instancing). 720x1280, 22 mm, no DOF, Cycles CPU 24 spl + OIDN. No text anywhere (flags are plain colour stripes, boards are blank).

## Stills
1. sb1_track_golden.jpg - Oregon HS track 1963, golden afternoon. Cinder track curving behind, grass infield, sawdust pit in low wooden frame, wooden standards with pegs, striped crossbar, bleachers with coats/bags, chain-link fence, pennant string, brick gym, pines, benches, coolers, hurdles, rake, tape reel, wheelbarrow, bags, shoes, cones. Foreground hurdle + gym bag ~1.5-2 m from lens.
2. sb2_stadium_evening.jpg - Mexico City 1968 bowl: 28 steep tiers with ~8k crowd blocks+heads, red tartan, blue-grey stacked foam pit, steel standards + bar against the crowd, floodlight towers (lamps lit), rim flags, glowing cauldron tower, officials' table (flag, clipboard, chairs), blue-violet sky with warm sunset band.
3. sb3_bar_low.jpg - same set, camera 1.5 m from the bar at 0.5 m height looking up; foam pit edge in foreground, open sky above the bar for an arched jumper card.
board.jpg - the three side by side (2256x1328).

## Palette
Sunset/warm: #f2a068 #f8cf96 #ffb070 | shade sky: #2a3494 #4a62c0 #5c6ee6 #7a70e0 | tartan #b4452e #cc643f | cinder #7e3a2a #a65a3a | sawdust #d9a858 #ecc880 | wood #6e4224 #b87c42 | brick #9c4c36 #bd6e4a | grass #8d9c3c #bcb458 | foam #7e9ccc #a2b8dc | concrete #c4b2a8 | crowd #e8c84a #d9532f #f0e4c8 #3a6fb8 #4aa086 #e88a2e #a8c8e8 #c8d24a #2d4a7a #cf3c2a | bar #f2e2ac #d9552e

## Key light (single sun, plus blue-violet sky ambient)
- sb1: sun azimuth -52 deg (from left/behind), elevation 22, colour (1.0,0.72,0.42), energy 4.6, angle 0.9.
- sb2: azimuth -48, elevation 19, (1.0,0.64,0.34), 4.4.
- sb3: azimuth -62, elevation 15, (1.0,0.62,0.32), 4.4.
(az = compass bearing of the sun, 0 = +y, 90 = +x.)

## hue_report (percent chroma by family; hue_report.py's reference clips are missing here, so its stats() was called directly on each still)
| still | red | orange | yellow | green | cyan | blue | violet | magenta | sat | val | dark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sb1 | 23.0 | 68.7 | 1.6 | 1.5 | 0.1 | 0.3 | 1.5 | 3.4 | 0.49 | 0.69 | 0.04 |
| sb2 | 49.9 | 27.6 | 0.4 | 0.1 | 0.2 | 16.0 | 4.0 | 1.8 | 0.54 | 0.67 | 0.01 |
| sb3 | 8.2 | 5.4 | 0.1 | 0.0 | 0.0 | 81.2 | 3.6 | 1.3 | 0.56 | 0.64 | 0.02 |
Magenta <= 3.4 % everywhere. Shade/ambient is blue-violet (sky zenith hue ~235-250).

## Render times (4 cores, 24 samples, incl. scene build)
sb1 20 s, sb2 21 s, sb3 17 s.
