# REVIEW of v3/set3d2/tower.py (builder's own look, measurement and list of differences)

Pictures: `tower_contact.jpg` (rows: DAY, DUSK, NIGHT_STORM, NIGHT_CALM x the six cameras with placeholder actors; a row of storm frames with flash, bolts, bell swung 35 degrees, rod on and off; the reference frames a/t0062, t0072, t0080, t0096, t0040). Stills: `tower_work/stills/`, storm tests `tower_work/storm/`, full-size final frames `tower_work/timing_*.png`, side by side with the reference `tower_work/cmp1.jpg`.

## 1. Looking against a/t0062, t0072, t0080, t0096, t0040 at full size

| question | now |
|---|---|
| warm saturated palette | yes: orange-terracotta brick, ochre / pink / red / cream plaster, terracotta roofs, green shutters, red geraniums, bronze bell; lit surfaces hue 12 to 34, mean saturation 0.50 |
| deep blue-violet shade, never magenta | cast shadow and shaded faces hue 238 to 252 in DAY (measured), 0.15 to 0.18 of lit; violet 0.9 and magenta 0.8 percent of chroma in DAY |
| one hard key, real cast shadows | one sun / moon, 0.5 to 0.7 deg; actor shadows lie on the cobbles and on the chamber floor, the arch throws a hard sun patch into the chamber, the tower and houses shadow the square at dusk |
| painted plate behind real geometry | yes: 3D square, tower, church, houses, then about 60 simplified 3D mid-town houses, two campaniles, a dome and cypresses (parallax), then the painted plate ring of roofs, towers, cypresses and hills, then the sky dome; the plate is seen through the north arch and behind every wide |
| density of detail | tower: corner strips, three courses with hanging arches, clock, slits, voussoir rings, dentils, 48 balusters; chamber: bell frame, rope with sally, trapdoor and ladder, lantern, bucket, coiled rope, crate, broom, pigeons; square: fountain, stall with produce, cart, barrels, pots, lanterns. Still below the reference interiors (t0040 has columns, tapestries, candelabra, a rug, throne and dozens of props) |
| night look (t0072, t0080) | blue night with moon, stars, warm lit windows and a glowing rose window, lanterns; storm clouds; lightning bolts bloom |

## 2. hue_report rows (`python3 tower_hue.py tower_work/stills/*.png`, 360x640 stills with placeholder actors, caption band excluded)

```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
reference A, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08
ref a t0040 t0062 t0072 t0080 t0096            17.7   31.3    2.4    0.1    0.0   39.2    4.1    5.1  0.46 0.63 0.08
DAY_chamber_eye                                13.9   28.7    0.6    4.5    0.0   44.3    4.4    3.6  0.40 0.48 0.29 
DAY_chamber_high_down                          38.9   51.8    1.2    0.3    0.0    6.5    0.8    0.4  0.49 0.66 0.02 
DAY_spire_insert                               17.3    7.1    0.7    4.0    0.0   70.2    0.2    0.6  0.55 0.69 0.01 
DAY_square_low                                 23.2   28.2    0.0    0.9    0.0   45.9    0.8    0.9  0.52 0.68 0.03 
DAY_tower_side_mid                             47.6   18.2    0.0    0.3    0.0   33.0    0.5    0.4  0.53 0.71 0.04 
DAY_town_wide                                  18.7   22.9    0.3    1.2    0.0   56.1    0.4    0.3  0.50 0.68 0.01 
ALL DAY (6 cameras)                            27.9   25.2    0.5    1.6    0.0   43.1    0.9    0.8  0.50 0.65 0.06
ALL DUSK                                       55.2   11.8    0.0    0.4    0.0    8.5   17.4    6.7  0.45 0.68 0.05
ALL NIGHT_STORM                                 0.3    0.2    0.3    0.5    0.0   97.4    0.4    1.0  0.57 0.42 0.04
ALL NIGHT_CALM                                  0.2    0.2    0.2    0.4    0.0   97.4    0.7    0.9  0.61 0.49 0.03
band (day/interior): red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15
```
(full per-file table: `tower_work/hue_rows.txt`.)

DAY: orange, violet and magenta in band; red 27.9 just under; blue 43 above the band because the open sky fills 20 to 50 percent of the exterior frames (the reference exterior group above measures 39); saturation 0.50 and value 0.65 slightly high; only 6 percent of pixels below V 0.25 (target 8 to 15): a sunlit exterior has little deep black; the interior camera `chamber_eye` has 29 percent.
DUSK: golden red-orange dominant with a violet sky, no green; magenta 6.7 percent (from the pink-violet sky and shaded brick), under the 10 percent limit.
Night presets: 97 percent blue, as expected, no magenta cast (0.9 to 1.0 percent); the warm windows are small accents (under 1 percent of chroma).

## 3. Light

`tower_measure.py DAY square_low final` (key on / key off on the same pixels; pixels attributed to objects by ray casting): shade / lit linear luminance tower shaft 0.160, chamber walls 0.161, church facade 0.172, house 0.156, cobbles 0.148. Hues lit -> shade: brick 18 -> 246, church 34 -> 238. The first build (red brick lit by key + blue sky ambient) shaded to hue 326 (magenta) at 0.14; the painted shade term (`shade_mix`, `shade_tint`) fixed both.

## 4. Contract

| check | result |
|---|---|
| every camera x DAY / DUSK / NIGHT_STORM (and NIGHT_CALM) at 360x640, 6 samples, placeholder actors | `tower_work/stills/`, 24 stills, about 2.5 CPU s each |
| set_rod 0 / 1 / 2, set_bell keyed, flash keyed, set_bolt tower (rod and no rod) and sky | rendered in `tower_work/storm/` (frames 1, 10, 20, 30): the bolt ends exactly on the rod tip, or on the finial top without the rod |
| final 720x1280, 12 samples | 11.3 to 17.8 CPU s (5.7 to 8.9 s wall on 2 threads, load about 3) |
| deterministic | two processes: same digest, max pixel difference 0 |

## 5. What still differs from the reference

1. Density: the chamber and the square are dressed but sparse next to t0040's throne room; the walls carry texture, not ornament (no frescoes, no hanging cloth, no foliage on the houses).
2. Blue share in DAY exteriors is 43 percent against the 14 to 30 band: the sky is large in every exterior camera; red sits at 27.9 (band 30 to 41).
3. Dark share in DAY exteriors is 1 to 4 percent of pixels (target 8 to 15); the reference gets its darks from big foreground shadow masses (t0062 hill, t0040 rug). A foreground occluder in shade for `square_low` would help.
4. Painted plate: one panorama per time of day, repeated twice around the ring; it reads well through the arches and behind wides, but it is less painterly than the reference plates (no soft gradients inside the hills, no haze bands, no atmospheric glow at dusk like t0062's sun rays on the hills).
5. Ink: inverted hulls of fixed world thickness (tower 0.054 D for 14 D, chamber 0.023 D for 6 D); in `chamber_eye` the near jambs are not inked, in `town_wide` the tower outline is under 2 px. Big flat walls carry their lines in the textures.
6. Night: the windows are warm but small; the reference night (t0072, t0080) has warm torch pools on walls and floors, which here would need a second light (against the one-key rule) or painted glow cards.
7. Lightning: the flash is a second sun along the moon's direction (no new shadow direction) plus a brighter sky; the bolt is an emissive tube with an additive glow, not a painted bolt with a halo card.
8. `chamber_high_down` shows the west face of the tower large on the left and the actors at about 30 px heads: a true high establishing shot, not a staging shot.
9. Placeholder actors are v2 / cast_ext puppets (beach_kid as the boy, boss as the priest), not nico and padre.
