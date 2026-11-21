# REVIEW of v3/set3d3/harbor.py (builder's own look, measurements and differences)

Pictures: `harbor_contact.jpg` (rows WINTER, WARM, NOON x the seven cameras with placeholder actors; a row of flood stills at u 0.2 / 0.5 / 1.0 from street_low and street_wide plus high_down at 0.5; the bucket insert empty-grey and full-overflowing-painted from the keyed test; the reference frames a/t0040, a/t0062, b/t0010, b/t0030). Full-size final frames: `harbor_work/final/`. Side by side at full size with b/t0030 and a/t0040: `harbor_work/cmp1.jpg`.

## 1. Looking against a/t0040, a/t0062, b/t0010, b/t0030 at full size

| question | now |
|---|---|
| warm saturated palette | red brick rows, ochre / orange warehouses with green frames, red stable, brown painted tank, red-brown sidewalks, ochre yard; grey steel tank in WINTER (by the story) |
| deep blue-violet shade, never magenta | shade hue 234..254 on every measured surface, 0.14..0.23 of lit; magenta 1..3 percent of chroma in the stills |
| one hard key, real cast shadows | one sun; the trestle throws striped shadows on the street and the tank wall, the rows shade the street in WINTER, actors cast shadows on the yard |
| exterior sky like b/t0010, b/t0030 | painted gradient dome with soft lavender-bottomed clouds, painted far shore / city plate (Custom House tower, steeples, Bunker Hill obelisk, cranes) |
| density | tank: 8 courses of riveted plates, lap ledges, ladder with cage, roof railing, vent, filling pipe on trestles from the pier; street: trestle with lattice columns, knee braces, ties and rails, lamp posts, kerb snow; yard: barrels, crates, dray, stable with hitching rail; harbour: quays, bollards, pier, freighter. Still sparse next to t0040 (no small clutter: signs, carts, people props, laundry, horses) |

## 2. hue_report rows (`python3 harbor_hue.py harbor_work/stills/*.png harbor_work/flood/*.png`; full table `harbor_work/hue_rows.txt`)

```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
reference B, whole clip                        33.6   23.1    0.7    0.5    0.5   29.1    2.7    9.7  0.48 0.63 0.08
ref b t0010 t0030 (exteriors)                   8.6    3.4    0.0    0.0    0.0   77.4    3.4    7.2  0.46 0.66 0.08
ref a t0040 t0062 + ref b t0010 t0030          23.7   14.1    1.1    0.1    0.0   49.8    2.9    8.4  0.43 0.62 0.12
WINTER_street_low                              19.9    2.8    0.0    0.9    0.2   74.5    0.9    0.8  0.49 0.48 0.12
WARM_street_low                                33.9   10.9    0.0    0.9    0.2   50.3    2.7    1.0  0.42 0.50 0.14
NOON_street_low                                15.2   29.5    0.0    0.2    0.1   47.4    5.9    1.7  0.43 0.51 0.18
NOON_street_wide                               32.8    8.8    0.0    0.3    0.0   51.1    3.5    3.4  0.35 0.60 0.04
WARM_base_eye                                  78.8   16.0    0.0    1.0    0.0    2.7    0.5    1.0  0.48 0.55 0.02
ALL WINTER (7 cameras)                         19.6   10.2    0.0    0.4    0.1   66.0    1.2    2.4  0.37 0.54 0.05
ALL WARM                                       55.8    9.9    0.0    0.3    0.0   30.3    2.0    1.6  0.44 0.54 0.06
ALL NOON                                       48.1   17.3    0.0    0.2    0.0   30.4    2.2    1.8  0.46 0.54 0.07
ALL flood (9 stills, NOON)                     25.5   15.5    0.0    0.2    0.1   45.8    7.8    5.0  0.39 0.50 0.14
band (day/interior): red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15
```

Why the exteriors sit outside the interior band: the band was measured on interiors. Every camera with sky (street_low, street_wide, high_down, tank_low) is blue-heavy, as the reference exteriors are (b/t0010 + t0030: 77 percent blue). WINTER is bluer still (66 percent) because the tank is grey steel and the low 20 deg sun leaves the street and the tank's street face largely in blue-violet shade (that is the brief's "long shadows"). WARM / NOON tip the other way (red 48..56): the brown tank fills the three tank cameras (base_eye, seam_insert, bucket_insert, 79 percent red in base_eye), and the warm key pushes brown toward red (the paint is drawn at hue 25, it renders at 16..24). Orange stays low (10..17) for the same reason. Violet and magenta are in band everywhere except the flood high_down frames (violet 15..21: the large shaded roof field under a high camera). Dark share is low (2..7 percent) in sunlit close shots (no big foreground shadow mass), 12..18 in street_low and the flood frames.

## 3. Light

`harbor_measure.py` (key on / key off, pixels attributed by ray casting), shade / lit linear: WINTER street_low houses 0.195, tank 0.162; NOON street_low cobbles 0.142 (just under 0.15), houses 0.234, tank 0.154, trestle 0.183; WARM base_eye yard 0.163, tank 0.170. Lit -> shade hue: brick 4..10 -> 242..252, tank 16..24 -> 234..242.

## 4. Contract

| check | result |
|---|---|
| every camera x WINTER / WARM / NOON at 360x640 with placeholder actors | `harbor_work/stills/`, 21 stills, 2.3..3.9 CPU s each |
| flood at u 0.2 / 0.5 / 1.0 | `harbor_work/flood/` from street_low, street_wide, high_down: burst and mound at the tank foot (0.2), a 7.7 D wave halfway down the street (0.5), the street full with the crest just in front of street_low (1.0) |
| keyed controls | `harbor_work/t_anim.py` -> `anim/`: paint 0 -> 1, seep 0 -> 1, bucket fill 0 -> 1 (overflow) and kicked over, flood 0 -> 0.5 -> 1 (keys given out of order) |
| final 720x1280, 12 samples, 2 threads | 14.5..24.6 CPU s (7..12 s wall); seam_insert is the slowest (24.6 with the tank ink hull, 19 without: `set_tank_ink(False)` when the tank silhouette is not in frame) |
| deterministic | same digest, max pixel difference 0 in two processes |

## 5. What still differs from the reference

1. Density and clutter: the street and yard are dressed but sparse against t0040 (no shop signs with lettering, carts in the street, horses, laundry, crowds of props). Facades are textures on boxes with a 3D cornice; windows are not recessed.
2. Hue balance: WINTER is too blue and WARM / NOON too red against the band (section 2); the reference gets its orange from lit sand / floor masses, here the lit ground is small in most frames.
3. Dark share: sunlit close shots have 2..4 percent pixels under V 0.25 (target 8..15); a dark foreground occluder (the stable, a cart in shade) would add it.
4. The flood is a flat-shaded height field: it reads as a brown mass with a steep front, but it has no curl, no foam-like rolling lip, no spray, and faceting is visible in close frames. Its sunlit faces read dark amber, its shaded faces violet-brown; the glossy highlight is deliberately faint (stronger gloss bloomed yellow under the toon key).
5. Grey steel lit by the warm key reads warm beige rather than steel grey in WINTER sun; in shade it is blue-violet.
6. Painted plate: one panorama per preset, simpler than the reference plates (no soft gradients inside forms, haze only by colour mixing).
7. Ink: inverted hulls at fixed world thickness; the tank hull is about 3 px in street cameras and thicker in tank_low; very close inserts show no outline on the wall seams (they carry their lines in the texture).
8. The bucket interior is barely visible from the low insert cameras; the fill level reads from base_eye height or higher. The seep drop above the bucket reads as a dark dot on the wall.
9. Placeholder actors are v2 / cast_ext puppets (beach_kid as the boy, boss as the foreman, clerk / senior_b as workers), not the film-3 cast.
