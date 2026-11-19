# Independent review of the 3D beach set (`beach3d.py`)

Reviewer did not build the set. Everything below was rendered and measured again by the reviewer. Working files are in `v3/tmp/beach_review/`. The builder's originals are kept there as `beach3d_orig.py` and `API_orig.md`.

The review scripts, all in `v3/tmp/beach_review/`:

| script | what it does |
|---|---|
| `rv.py` | renders any preset x camera x state |
| `strip.py` | renders the fog and wave strip |
| `meas.py` | camera geometry, wave against the ridge, lit and shadow, heads |
| `contract.py` | keys, determinism, rebuild, sea motion, rain, debug markers |
| `prof2.py` / `prof3.py` | cost breakdown and persistent data |
| `sheet.py` | contact sheets |

The sheets to look at:

| sheet | contents |
|---|---|
| `review_compare.jpg` | a/t09.0, t13.5, t16.0, t48.5, t53.0, t58.5 above all 7 cameras x 3 presets at 720x1280 final quality, two actor cards |
| `review_strip.jpg` | fog and wave at 0, 0.33, 0.66 and 1, in three rows: GREY_DRIZZLE sea_view, STORM wave_low, STORM low_cottages |
| `base_sheet.jpg`, `old_sheet.jpg`, `old_storm.jpg`, `old_strip.jpg` | the set as delivered, before the repairs |
| `contract_dbg.jpg` | the debug markers |
| `contract2/sea_alive.png` | the sea 1 s apart |
| `rain_crops.jpg` | the rain over the hero's head |

## 1. What I saw (step 1, looking)

| question | as delivered | after repair |
|---|---|---|
| SUMMER_SUN reads as clip A? | Yes for staging: the horizon sits at 0.40 to 0.48 H, lines converge to one vanishing point, figures cast hard whole-body shadows on the ground, there is no ink on the terrain, and warm ground sits against blue. The ground was flat pale orange (lit V 0.85) and hardly reached the red family (red 11, orange 27). | The sand now spans the red and orange boundary like the reference ground (red 27, orange 16 against the reference's 15 and 20). The shade is darker: cast-shadow ratio 0.45 to 0.58. Deep darks are still missing (section 4). |
| GREY_DRIZZLE is a dull morning of the same film? | Yes, but almost dead: saturation 0.21. The brown sand times the blue ambient pushed magenta to 5.9 to 8.3. The fog at 0.25 to 0.33 was the colour of the sky, so it could not be seen. | Saturation 0.24 to 0.25 and magenta 4.7. The fog bank is lighter than the sky, with a billowing top, and is visible from 0.25 on. The drizzle is subtle (1.8 percent of pixels). |
| STORM threatening? | Partly. The slate sky worked, but the sand was bright salmon-orange under a pink glow, which read as a sunset beach. The rain was a curtain of fat white bars over the faces. | The sand is wet and dark red-brown, the warm break is weaker (0.35), and the rain is thinner and blue-grey. Faces stay readable (`rain_crops.jpg`). |
| Is the wave ONE readable wall of water, taller than the cottages at p = 1? | No. Its face had the same blue and value as the storm sky, its horizontal light bands read as cloud strata, and the lit, lumpy foam ribbon (2 D scallops) read as a row of cumulus clouds above the roofs (`old_storm.jpg`, low_cottages). It was taller than the cottages in geometry only. | Yes. The face is a deep blue-teal with a lighter translucent band under the lip, streaks run up the face, the crest is a thin white lip, and there is white churn at the toe. The crest stands 257 px above the cottage_06 ridge in low_cottages (section 2.4). |
| Does the fog band at low progress pass for fog? | No in GREY_DRIZZLE: the fog was `#bfc2d0` against a sky of `#c0c6da`. At 0.66 its top was a hard, jagged line. | Yes. At 0.33 it is a pale bank about 28 px high, and at 0.66 a billowing grey wall that the wave comes out of (`review_strip.jpg` row 1). |
| Is the sea alive? | Yes, when `sea_t` is keyed. Static `set_sea(t)` holds it still. | Unchanged: 38 percent of the pixels in the sea band change between frames 1 and 31 (`contract2/sea_alive.png`). |
| Do white heads read against every sky? | Yes in all three presets. In STORM, rain bars crossed the faces. | Yes. Head luma 0.97 against a background of 0.49 to 0.68 in SUMMER and GREY and 0.14 to 0.28 in STORM, with the ink outline everywhere. The weakest case is GREY_DRIZZLE sea_view with the fog at 0.66 or more: the head (`#fff5f3`) sits on the fog bank (`#dcdee6`), and only the ink outline separates them. |

## 2. Measurements (step 2)

### 2.1 Horizon and vanishing point

From the camera matrices (`meas.py`).

| camera | pitch (deg) | horizon (H) | VP of the shore (W, H) | head at the marks (px) |
|---|---|---|---|---|
| vista_high | -7.3 | 0.421 | 0.33, 0.421 | 58 / 49 |
| low_cottages | +13.4 | 0.645 | off frame | 165 |
| eye_beach | -5.6 | 0.441 | off frame (looks along -y) | 117 / 158 |
| sea_view | -9.4 | 0.399 | - (looks out to sea) | 105 / 101 |
| wave_low | +32.9 | 0.895 | - | 136 / 128 |
| boardwalk_eye | -1.9 | 0.479 | 0.49, 0.479 | 98 |
| surf_side | -2.5 | 0.473 | 0.39, 0.473 | 108 / 58 |

- The spec range for exterior horizons is 0.34 to 0.50 H, and every eye-level and high camera is inside it.
- low_cottages is the low angle (spec 0.67 H).
- wave_low is a special pitched-up camera for the wave.
- In a/t58.5 the vanishing point sits right of centre (about 0.65 to 0.70 W, 0.44 H). vista_high puts it at 0.33 W, the mirror composition with the sea on the left and the colony on the right. I left that as a composition choice.

### 2.2 Light and shadow in SUMMER_SUN

Lit ground against shadow on the ground, lower 45 percent of the frame. Key elevation 44.6 deg, so a whole-figure shadow is 1.02 x the figure height (2.94 D for the 2.9 D hero).

| frame | lit V | shadow V | ratio | lit hue | shadow hue |
|---|---|---|---|---|---|
| ref a/t13.5 | 0.60 | 0.30 | 0.49 | 18 | 262 |
| ref a/t16.0 | 0.54 | 0.30 | 0.55 | 347 | 254 |
| ref a/t48.5 | 0.50 | 0.20 | 0.40 | 352 | 262 |
| ref a/t53.0 | 0.52 | 0.23 | 0.44 | 351 | 250 |
| ref a/t58.5 | 0.79 | 0.22 | 0.27 | 22 | 266 |
| vista_high | 0.84 | 0.39 | 0.47 | 17 | 254 |
| eye_beach | 0.87 | 0.39 | 0.45 | 18 | 252 |
| boardwalk_eye | 0.68 | 0.39 | 0.58 | 17 | 252 |
| low_cottages | 0.86 | 0.57 | 0.66 | 18 | 244 |

- The ratio and the hue shift sit inside the spec target (hue 230 to 270, V ratio 0.35 to 0.60) and the reference range.
- In low_cottages most of the "shade" pixels are the blue cottage wall, so its 0.66 ratio is not a cast shadow.
- sea_view and surf_side are not listed: there the mask picks up the sea instead of shadows.
- Our lit sand is brighter than the reference's gravel and decks (0.85 against 0.50 to 0.79). It is comparable with the reference's sand frames (t09.0, t58.5).

### 2.3 Tone per preset

`hue_report.py` (shares in percent):

| set | red | orange | blue | violet | magenta | sat | val | dark |
|---|---|---|---|---|---|---|---|---|
| clip A exterior frames (6) | 15.3 | 20.0 | 52.8 | 2.5 | 9.2 | 0.42 | 0.70 | 0.07 |
| SUMMER_SUN as delivered (7 cams, preview) | 12.9 | 19.5 | 66.0 | 0.3 | 0.8 | 0.45 | 0.80 | 0.01 |
| **SUMMER_SUN repaired, 4 main cams** | 27.3 | 16.0 | 54.6 | 0.4 | 0.9 | 0.44 | 0.80 | 0.01 |
| SUMMER_SUN repaired, 7 cams | 20.5 | 12.6 | 65.2 | 0.4 | 0.8 | 0.46 | 0.79 | 0.01 |
| GREY_DRIZZLE as delivered | 21.1 | 2.1 | 66.2 | 0.9 | 8.3 | 0.21 | 0.65 | 0.01 |
| **GREY_DRIZZLE repaired** | 30.0 | 2.0 | 61.0 | 0.9 | 4.7 | 0.24 | 0.65 | 0.01 |
| STORM as delivered | 18.3 | 2.3 | 73.7 | 2.1 | 2.7 | 0.40 | 0.48 | 0.03 |
| **STORM repaired** | 11.4 | 2.4 | 78.7 | 2.3 | 3.0 | 0.44 | 0.47 | 0.04 |

`metrics.py` (medians):

| set | S | V | edge | Vp5 | Vp95 |
|---|---|---|---|---|---|
| ref A (6) | 0.452 | 0.686 | 0.054 | 0.239 | 0.929 |
| SUMMER_SUN | 0.483 | 0.776 | 0.035 | 0.365 | 0.918 |
| GREY_DRIZZLE | 0.246 | 0.653 | 0.037 | 0.357 | 0.812 |
| STORM | 0.438 | 0.464 | 0.078 | 0.255 | 0.847 |

- Violet stays under 5 and magenta under 10 in every preset.
- The shade reads at hue 244 to 254, blue-violet, never magenta.
- The STORM blue share is high (79) by design: it is a cold night-like storm, and no reference exists for it.

### 2.4 The wave against the cottage_06 ridge

Screen y in px; smaller is higher; "-" means the point is behind the camera.

| camera | ridge y | p 0 | 0.33 | 0.5 | 0.66 | 0.8 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|---|---|
| low_cottages | 578 | 830 | 787 | 759 | 703 | 596 | 458 | **321** |
| sea_view (ridge behind camera) | - | 517 | 477 | 448 | 380 | 193 | -289 | -1744 |
| wave_low | - | 1150 | 1091 | 1049 | 958 | 757 | 427 | 22 |

- In low_cottages the crest clears the ridge from about p = 0.82 on and stands 257 px above it at p = 1. In world units the crest is 17.5 D against a 4.04 D ridge.
- Below about p = 0.8 the wave hides behind the roofs from that camera. That follows from the toe law y = 17 + 420 (1 - p)^1.7, which brings the wave in fast at the end.

### 2.5 Head fill, ink, rain

| check | result |
|---|---|
| Head fill on screen | `#fff4f2` to `#fff6f3`, every preset and camera |
| Ink on screen | `#3f2638` to `#402a39`, every preset and camera |
| Grade | does not tint the heads (stage spec: `#fef7f6` / `#fff8f7` with bloom, `#3a2832`) |
| Rain at final resolution, sea_view | pixels changed by more than 8/255: drizzle 1.8 percent (mean lift 21), storm 8.8 percent (mean lift 56, p90 99) |
| Rain at 360x640 | the 1 px streaks mostly vanish: 0.06 and 0.26 percent. Judge rain only at final resolution. |

### 2.6 Cost per final 720x1280 frame

12 samples, 4 threads. Rain is on in every row; the GREY_DRIZZLE and SUMMER_SUN rows also have wave 0.7 and fog 0.6. All rows except the last use sea_view.

| condition | GREY_DRIZZLE | SUMMER_SUN | STORM (wave 1, fog 1) |
|---|---|---|---|
| as delivered, still mode, load 3 to 4 (4 of it this render) | 5.5 to 5.8 s, 21.4 to 22.6 CPU-s | 6.2 to 9.4 s, 21.5 CPU-s | 6.6 to 6.7 s, **25.5 to 26.2 CPU-s** |
| repaired, still mode, load 1 to 2.5 before this render | - | 5.2 to 5.3 s, 19.9 to 20.6 CPU-s | 5.9 to 6.1 s, 22.8 to 23.5 CPU-s |
| repaired, frame loop (`prof3.py`), load about 1 | - | - | first frame 5.4 to 5.6 s; **following frames 4.1 to 4.2 s, 16.0 to 16.3 CPU-s** |
| repaired, `cli_timing` frame loop, other agents' load 6 to 7.5 | 7.5 to 7.8 s, 14.5 to 15.2 CPU-s | 7.8 to 7.9 s, 15.2 to 15.4 CPU-s | 8.3 to 9.3 s, 16.3 to 17.9 CPU-s |
| STORM low_cottages / wave_low, still mode, load about 2 | | | 5.25 s / 5.26 s, 20.2 CPU-s |

- "Still mode" re-rasterises and re-uploads the actor sprites and the new camera for every frame. An animation loop does not.
- The machine was never entirely free. The rows at load 1 to 2.5 had at most one other job.
- What I changed for cost:
  - The wave shader dropped a Voronoi and a Wave texture. The wave had cost 19 percent of the storm frame.
  - The rain dropped from 1800 to 1300 streaks.
- Persistent data gives no gain, but it renders pixel-identical, so it is safe if a renderer wants it.
- The STORM frame went from 26 to 23 CPU-s in still mode. In an animation loop it costs about 4.2 s with the machine nearly to itself, which is inside the 6 s budget.
- Under the other agents' load it measured 8.3 to 9.3 s, near the 9 s hard limit. That is contention, not the frame.

## 3. Contract (step 3)

`contract.py`, output in `contract2/`.

| check | result |
|---|---|
| Keys: `set_wave(0, frame=1)` / `set_wave(1, frame=91)`, with fog, rain, wind and sea keyed too | At frames 1, 16, 31, 46, 61 and 91 the driven wave toe, height and crest equal `wave_state(ctl['wave'])` to 1e-3. Interpolation is linear (wave 0.5 at frame 46, rain 0.5 at frame 16). Rain is hidden at 0 and shown at 0.5 or more. The fog height is 30 a^0.75. The umbrella follows the wind. |
| The same frame rendered twice | max pixel difference 0 |
| `build()` again (same preset), same frame | max pixel difference 0. The anchors dict is identical. The objects (56) and meshes (51) are identical. |
| Data growth on rebuild, as delivered | +1 orphan `key_sun` light per build; +4 materials and +2 images per rebuild from the placeholder actor cards. **Fixed**: 0 growth over two rebuilds. |
| `build(clear=False)` | keeps the camera; `attach_rain(cam)` re-parents the rain |
| Debug markers on every camera (`contract_dbg.jpg`) | sand_a..d sit on open sand and surf_a/b on the wet sand. road_a/b sit on the road behind the cottages and boardwalk on the deck. The ridge marker sits inside the roof's ridge cap, i.e. on the roof. The pole tops sit on the crossarms. The sign and the deck chair are at their props. |
| Marks against `ground_z` | **Defect found and fixed.** surf_a / surf_b (y 11.6 / 11.9) were reported at z 0, but the sand sloped from y 10, so it lay at -0.048 / -0.057 and the actors floated 4 to 6 px. The sand is now flat to y 12.2 and slopes 1:15 to the waterline (unchanged at y 14, z -0.12). Every mark now has ground_z = 0. |
| Builder's own commands | `python3 beach3d.py stills / strip / timing` write their temporary files into `v3/tmp/beach` (`TMP`). The review drivers set `B.TMP` to `v3/tmp/beach_review/work`. |

## 4. Repairs made in `beach3d.py`

The API is backward compatible: same functions, same arguments, the same anchors and keys, and new preset keys only.

1. **Wave material** rewritten as `mat_wave()`, a new function:
   - painted by height, with streaks running up the face, a churn band at the toe and spray specks;
   - self-coloured: emission art x `wave_emit`, plus the key x `wave_gain`;
   - hazed to the fog colour with distance;
   - the old horizontal bands, Voronoi and Wave texture are gone.
2. **Foam lip** made thin and finely scalloped (radius 0.026 to 0.046 of the height instead of 0.045 to 0.115). It is drawn flat two-tone by `mat_wave_foam()`, unlit.
3. **Fog bank**:
   - billowing soft top;
   - colour gradient from `fog_foot` to `fog`;
   - drizzle fog lighter than the sky;
   - height 30 a^0.75; a = 0 and a = 1 are unchanged.
4. **Rain**:
   - 1300 streaks, 1 px wide, 1.8 to 11 D from the lens;
   - fainter, and the near streaks halved;
   - blue-grey (`rain_col`).
5. **STORM**: wet dark sand, warm glow 0.6 to 0.35, and its own wave ramp, deep teal, so the wave separates from the slate sky.
6. **SUMMER_SUN**: darker ambient and shade tint (the cast-shadow ratio went from about 0.5 to 0.45 to 0.58 with hue 252), and sand tones that span the red and orange boundary.
7. **GREY_DRIZZLE**:
   - a less blue ambient, which cuts magenta from 8.3 to 4.7;
   - sand a touch more orange;
   - grade saturation 1.10 to 1.16.
8. **Terrain**: flat to y 12.2, so the surf marks stand on z = 0. There is a vertex row at the slope break.
9. **Leaks**: the orphan `key_sun` light and the orphan placeholder actor materials and images are purged on rebuild.
10. The stills `still_<PRESET>_<cam>.png` and `still_strip_fog_wave.png` were re-rendered with the repaired code, at final quality.
11. `API.md` was updated in sections 3, 5, 7 and 9.

## 5. What remains

- **Deep darks**: 1 percent of pixels below V 0.25 in SUMMER_SUN and GREY_DRIZZLE, and 4 percent in STORM.
  - The clip A exteriors sit at 7 percent; the film target is 8 to 15.
  - The reference gets its darks from rail ties, gravel and canyon walls, and an open beach has none of those.
  - Even a darker cast shadow stays above V 0.3 on the sand.
  - Remedy, per shot: a foreground element in shade (a dune lip, a fence post or a porch corner close to the lens, the spec's "nearest 15 percent of the frame at half brightness"). Or let the interiors carry the darks in the film mix.
- **SUMMER_SUN overall value** 0.78 to 0.80 against the reference's 0.69 to 0.70. The bright sky and the sand dominate.
- **The wave** is still one rigid sculpt moved by drivers:
  - it does not break or flood;
  - between p 0.66 and 1 it covers 70 D in a third of the progress, so key p with an ease if the approach must feel steady;
  - the churn at the toe is blobby at full resolution;
  - seen side-on (vista_high, surf_side, boardwalk_eye at p = 1) the wave reads as a glassy cliff at the frame edge, which works but is not a curl.
- **GREY_DRIZZLE saturation** 0.24 is below the 0.38 to 0.48 band. That is deliberate for a dull morning, but it can be raised with `grade_sat`.
- **vista_high's vanishing point** sits at 0.33 W where a/t58.5 has about 0.68 W. I kept it as a mirrored composition.
- **Timing on a completely free machine** was never possible. The best measurement had load about 1 (section 2.6).
- **Sky clouds** in vista_high, boardwalk_eye and surf_side are long smeared streaks toward the horizon, where the reference has soft separate puffs. I did not change them.
