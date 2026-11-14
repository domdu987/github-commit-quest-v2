# REVIEW of v3/set3d4/pagoda.py (builder's own look, measurements and differences)

Pictures: `pagoda_contact.jpg` (rows DAY, SUNSET, NIGHT, DAWN x the eight cameras with placeholder actors; a row of tests: sway amp 1 at both phases, the cutaway with sway, the pillar swung +3 deg, crack 1 / 2+patch 1 / 3+patches, collapse u 0.3 / 0.5 / 0.7 / 0.85 / 1.0, a keyed NIGHT collapse frame, a quake frame; then the reference frames a/t0040, t0062, t0072, t0080, t0096, t0104). Full-size finals: `pagoda_work/final/` (all 32). Side by side with a/t0040: `pagoda_work/cmp1.jpg`.

Note on the reference frame numbers in the task: in `ref/a` the golden sunset is **t0062** (hill, sun rays), **t0072** is the moonlit night (jar under the moon), t0080 the barred window at night, **t0096** the dust explosion over the walled city, t0104 the top-down pillar insert, t0030/t0040 the wide city and the throne hall. SUNSET was matched to t0062, NIGHT to t0072/t0080, the collapse dust to t0096.

## 1. Looking against the reference at full size

| question | now |
|---|---|
| red lacquer, gold, tiled roofs | vermilion posts, rails, doors (gold studs), lower wall panels, red railings on every storey, painted bracket band (green/red/gold), ochre eave ends, red-brown rafter soffits; blue-grey hongawara tiles with lit crests; bronze sorin with nine rings, gold flame and jewel; gold wind bells; red gate, red banners, red paper lanterns |
| castle walls | courtyard walls with an ishigaki stone base, white plaster and tiled coping; stone platform; the painted plate has a castle keep on its stone base |
| painted mountain backdrop | one panorama ring per preset: two jagged ranges with snow caps, green/violet hills with fields and pine clumps, a far town band, keep and a far pagoda (flatter and simpler than t0030's plate) |
| night blue, moon, warm lanterns | NIGHT: big moon with glow in the north (behind the pagoda in two_buildings / street_eye / cutaway_full, as t0072), stars, moon key from the south-west, lanterns at 2.6 with bloom, lit lattice windows, warm light pools on the ground, glowing stone lanterns |
| sunset | SUNSET: red-orange sky with ray-burst sun, warm low key from the west, long shadows, violet shade (t0062) |
| dust explosion wide | collapse: ochre dust puffs lit warm with violet shade (t0096), timbers and plaster slabs flying, rubble pile, stump with splinters |
| one hard key, real cast shadows | one sun / moon; eaves throw deep shadow bands on the storey walls; actors cast shadows |

## 2. hue_report rows (`python3 ../set3d3/harbor_hue.py pagoda_work/stills/*.png`; full table `pagoda_work/hue_rows.txt`)

```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
reference A, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08
ref a t0062 (sunset)                           56.9   30.5    2.4    0.0    0.0    0.0    0.0   10.2  0.50 0.70 0.26
ref a t0072 (moon night)                        0.8    0.2    0.0    0.0    0.0   93.3    4.7    0.9  0.66 0.61 0.02
ref a t0080 (night window)                     10.2    2.2    0.1    0.0    0.3   62.0   14.3   10.9  0.41 0.49 0.07
ref a t0096 (dust wide)                         9.6   83.2    6.0    0.0    0.0    0.0    0.0    1.2  0.41 0.88 0.00
ALL DAY (8 cameras)                             3.4   23.9    0.3    0.7    0.0   66.6    3.8    1.2  0.45 0.61 0.12
ALL SUNSET                                     51.6   22.2    0.1    0.2    0.0    4.6   15.7    5.7  0.46 0.66 0.11
ALL NIGHT                                       0.6    1.0    0.0    0.2    0.0   97.3    0.6    0.2  0.65 0.50 0.10
ALL DAWN                                       20.0    7.3    0.1    0.5    0.1   44.9   21.1    6.0  0.28 0.65 0.07
DAY_street_eye                                  2.6   31.6    0.0    0.0    0.0   63.9    1.0    0.8  0.53 0.68 0.05
DAY_two_buildings                               0.9   26.6    0.0    0.3    0.0   69.2    2.1    0.9  0.48 0.71 0.04
NIGHT_street_eye                                3.2    6.8    0.0    0.0    0.0   87.4    1.6    1.1  0.65 0.53 0.03
band (day/interior): red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15
```

Why exteriors and night sit outside the interior band: the band was measured on interiors. Every DAY camera has open sky over the low town (55..80 percent of the frame in pagoda_low / town_wide), so blue dominates as in the reference exteriors (b t0010/t0030: 77 blue); orange comes from the lit gravel and earth (24..32, in band); red stays low (1..6) because the red lacquer is thin (posts, rails, doors, banners) and largely in eave shadow, the way real pagodas read. NIGHT is blue-dominant by design (97; t0072 is 93), the warm accents are small (street_eye orange 6.8), magenta 0..1. SUNSET matches t0062 (red 52 / orange 22 against 57 / 31); its violet 16 is the large shaded fronts under a low west sun. DAWN carries a gold haze veil and lavender shade: blue 45, violet 21 (the shaded street and the cutaway interior), magenta 6 (in band). Dark share: 0.10..0.12 per preset; 0.02..0.05 in single sunlit wides (no dark foreground mass), 0.3..0.4 in the two inserts.

## 3. Light

`pagoda_measure.py DAY <cam> preview` (key on / key off, pixels attributed by ray casting, hidden objects excluded), shade / lit linear: two_buildings tower walls 0.183, ground 0.168; pagoda_low pagoda storey fronts 0.171..0.173, platform 0.187; street_eye ground 0.164, street roofs 0.218; banners 0.167. All inside 0.15..0.31. Lit -> shade hue: plaster/timber 36 -> 236..238, lacquer 12 -> 250, banner red 354 -> 264..266 (violet, not magenta), earth 26 -> 242.

## 4. Contract

| check | result |
|---|---|
| every camera x DAY / SUNSET / NIGHT / DAWN at 360x640 with placeholder actors | `pagoda_work/stills/`, 32 stills, about 2 CPU s each |
| sway / pillar / crack / collapse / quake tests | `pagoda_work/tests/` (23 stills); keyed test `pagoda_work/t_anim.py` -> `anim/`: sway + quake keyed per frame for 30 frames, crack 0->1->2->3 with plaster keys, cutaway keyed on, collapse keyed 0 -> 1 over 30 frames |
| final 720x1280, 12 samples, 2 threads | 11.6..20.0 CPU s for 28 of 32; crack_insert 16.8 (DAWN), 21.0 (DAY, NIGHT), 25.1 (SUNSET: the crack/patch decal stack is alpha-transparent and the sunset haze veil adds transparent hits) |
| deterministic | same digest e446bc77..., max pixel difference 0 in two processes |

## 5. What still differs from the reference

1. Density: the courtyard is open gravel; the reference fills its frames with props (crowds, candles, carpets, statues). No market stalls, carts, signboards with lettering, laundry, or crowd extras; machiya fronts are textures on boxes (lattice and noren are painted, not 3D).
2. Painted plate: one flat panorama per preset, much simpler than t0030's town-and-mountain plate (no soft gradients inside forms, no layered haze within the plate).
3. Pagoda walls read dark: the deep eaves put most of each storey in shade under the 45 deg DAY sun, so the red lacquer is less present than in a stylised drawing. Raising the lacquer area further (all-red walls) would push DAY red up but would stop looking like the white-plaster Japanese type.
4. Cutaway: the inside is in shade in every preset (the key never reaches the pillar), lit only by the two oil-lamp flames and their floor pools; the pillar reads as violet-grey wood, not warm cypress. The chain is small (four links, 0.55 D) and reads only in cutaway_full at final size.
5. Dust: low-poly spheres with ink hulls, lit with violet shade like t0096, but faceting shows at full size and the column is a stack of balls, not a soft billow; at u = 1 the column in two_buildings goes off the right edge. No smoke texture, no flying stones in the air after u 0.95.
6. The rubble pile is a smooth mound with beams, slabs and tiles laid on it; it reads as a pile from rubble_dawn, less so from two_buildings (looks like a sandy heap with timbers).
7. NIGHT moon is painted in the north while the moon key comes from the south-west (a deliberate cheat so the moon stands behind the pagoda in the main cameras and the fronts stay lit).
8. Sway: storeys move rigidly (x offset + tilt); there is no gap opening/closing animation between storey and roof; at amp > 1.2 the roofs visibly intersect the storey above.
9. Placeholder actors are v2/cast_ext puppets (beach_kid as the apprentice, boss as the master, seniors / beach_woman as townspeople), not the film-4 cast.
