# v3/set3d_ext/light/office_light.py: office_grey and office_storm (shot plan build step 8, presets only)

This module extends `v3/set3d/office3d.py` without editing it. It imports `office3d` and switches the scene that `office3d.build()` made to one of three lights. It covers shots 17-22 (`office_grey`) and shot 25 (`office_storm`). The light items of step 8 are all here: the two presets, the window rain card, and lightning as a pulse of the key. Props are not part of this module: the note glyphs, the ink-blot card and the label belong to step 4, 8 and 9 props.

Files:

| File | What |
|---|---|
| `office_light.py` | the module |
| `gen_tex.py` | writes `tex/`: `sky_grey.png` and `sky_storm.png` (the set's own sky.png recoloured, with the same roofline; in the storm, about half the window panes are lit) and two 96-frame rain loops (`tex/rain_drizzle/`, `tex/rain_lash/`). It is deterministic and uses only numpy and PIL. |
| `prove.py` | the light review. Its output is in `proof/`. |
| `proof_close.py` | the wall map from 0.75 D and 0.45 D, plus the cost of a lightning frame |
| `proof/` | `compare.jpg` (each camera beside a reference frame, then day, grey and storm), `compare_by_preset.jpg`, `flash_strip.jpg`, `rain_strip.jpg`, `close.jpg`, `stills/` (720x1280, 12 samples, two stage actors), `measure.json`, `identity.json`, `timing_4t.json`, `timing_flash.json` |
| `work/` | scratch from the tuning passes |

## 1. Use

```python
sys.path.insert(0, ".../v3/set3d"); sys.path.insert(0, ".../v3/set3d_ext/light")
import office3d as S, office_light as OL
A = S.build("INTERIOR_DAY")          # always build the reviewed set first (that is office_day)
OL.apply("office_grey")              # or "office_storm" / "office_day"; returns the numbers it set
# ... build stage actors (actors.Actor ...), then:
OL.tint_cards()                      # applies the preset's card tint to the cards that now exist (needed for office_storm only)
OL.set_rain(drizzle=1.0, lash=0.0, frame=None, phase=None)   # window rain levels 0..1; frame=N keys them (LINEAR); phase = loop offset
OL.flash(amount, frame=None)         # lightning: amount 0..1; frame=N keys it (CONSTANT, holds until the next key)
OL.lightning(f, pattern=(1.0, 0.35, 0.8))   # keys f, f+1, f+2 with the pattern and 0 on f+3 (the plan's "key pulsed for 3 frames")
OL.set_flash_energy(e)               # allow lightning in office_day or office_grey too (it is 0 there; 3.2 in office_storm)
OL.state()                           # {'preset', 'flash', 'drizzle', 'lash'}
```

Rules:

- Call `apply()` after `S.build()`. Call it again after any new `S.build()`, because a new build forgets the old bookkeeping.
- `apply()` rebuilds nothing and moves nothing in `SET`. Actors, cameras and the track state are untouched.
- `apply("office_day")` brings the reviewed INTERIOR_DAY back bit for bit. This was checked: after day, then grey, then storm with a flash and rain keyed, then day again, the frames are identical to a fresh build (max abs diff 0 on eye_two_shot and insert_rake, `proof/identity.json`).
- `apply()` writes the preset's `shade` and `lift` into `S.STATE['P']`, so a material made later with `S.mat_lit` gets the right ambient. The per-surface tints and key gains reach a new prop only when `apply()` runs again. The same holds for the card tint and `tint_cards()`.
- The flash and rain controls are custom properties `flash`, `drizzle` and `lash` on the empty `olt_ctl`, read by drivers. The functions above key them. Every `apply()` clears the flash keys.
- New objects: the collection `LIGHT_EXT` holds `olt_ctl`, `olt_rain` (the rain card) and `olt_flash` (the lightning sun). The materials are `OLT_rain`, `OLT_sky_grey` and `OLT_sky_storm`.
- The rain card is a plane just inside the glazing at x = 3.895 (y -7.72..-1.74, z 0.36..5.08). The glazing bars cut through it. It is emission-only, alpha-cut, casts no shadow and is hidden from bounce rays. The loop is 96 frames (3.2 s) and seamless, and the frame is taken from the scene frame.
  - drizzle: beads plus 26 drops that slide down in stick-slip steps, leaving thin wet trails.
  - lash: dense drops plus 170 wind-slanted streaks.

## 2. What a preset changes (numbers)

The light model is the set's: `pixel = art x gain x KEY x visibility + (art x SHADE x shade_mul + LIFT) x F`.

`apply()` changes the following:

- **SHADE** and **LIFT**.
- **surf**: an extra per-surface multiplier on the ambient, applied on top of the set's own `shade_mul`. It is selected by material name: `tex_<name>`, `flat_<hex>`, or `warm_flat` (any untextured material with a red-brown albedo: hue < 45 deg, S > 0.35, V < 0.75).
- **kgain**: a per-surface multiplier on the key gain.
- **The key sun**: colour x energy and angle.
- **Shell shadows**: whether the room shell (walls, wall_relief, window, ceiling, beams, pendants) shadows the key.
- **The sky card**, the bulbs (the banker-lamp slit scales with them), the rain levels, the flash energy, the grade, and the card tint.

| | office_day (= INTERIOR_DAY) | office_grey | office_storm |
|---|---|---|---|
| SHADE | (0.20, 0.27, 0.54) | (0.20, 0.23, 0.41) | (0.068, 0.082, 0.165) |
| LIFT | (0.0, 0.010, 0.026) | (0.002, 0.005, 0.014) | (0.003, 0.003, 0.007) |
| KEY (scene-linear) | (2.30, 1.65, 0.74), 0.45 deg | (0.66, 0.58, 0.50), 3 deg: x0.29 of the day key, much cooler (R/B 1.3 against 3.1) | (0.12, 0.13, 0.19), 3 deg: x0.083 |
| Room shell shadows the key | yes (window patch, bar shadows) | no: no sun patch, a flat wash from the window side; actors and furniture keep soft 3 deg contact shadows | no, except on lightning frames |
| surf (ambient multipliers) | none | map (1.60, 1.48, 1.18) (paper reads cream, not blue); wallpaper (0.92, 1.0, 1.08); frieze (1.10, 0.95, 0.80); wainscot and warm flats (1.30, 1.50, 0.60); planks (1.45, 1.12, 0.72); ceiling (1.15, 1.45, 0.55); beams (1.20, 1.45, 0.55); rug (1.10, 1.0, 0.88); paper, calendar (1.35, 1.30, 1.10); sign (1.2, 1.15, 1.05); red ink `flat_c8301c` (2.0, 0.35, 0.3) | the same woods, with: wallpaper (1.12, 0.92, 0.62); frieze (1.15, 1.10, 0.55); planks (1.40, 1.25, 0.65); beams (1.15, 1.55, 0.50); warm flats (1.25, 1.60, 0.55); rug (1.15, 1.0, 0.85); red ink (2.8, 0.35, 0.3) |
| kgain | none | wallpaper 0.60, frieze 0.70, red ink 1.8 | wallpaper 0.70, frieze 0.75, red ink 4.5 |
| Sky card | the day sky, 1.0 | `sky_grey.png` (pale blue-grey overcast, slate roofs), 1.0 | `sky_storm.png` (slate-violet, navy roofs, lit panes), 1.0; brightens x(1 + 2.2 flash) |
| Bulbs | 6 | 8 (the lamps are on and glow) | 12 |
| Rain card (drizzle, lash) | hidden | (1.0, 0.0), gain 0.9 | (0.35, 1.0), gain 0.55, lit x(1 + 1.5 flash) |
| Lightning | none | none (unless `set_flash_energy`) | `olt_flash`: sun from the key direction, colour (0.82, 0.88, 1.0), 1.2 deg, energy flash x 3.2 x the day key. While flash > 0, the shell casts shadows again: the window and its bars print on the floor and the map wall. At flash 0 the light is hidden and costs nothing. |
| Grade: offset / slope / power / saturation / bloom size, strength | (0.002, 0.0045, 0.010) / (1, 0.985, 0.97) / 1 / 1.06 / 0.05, 0.5 | (0.003, 0.004, 0.008) / (1.005, 1.005, 1.02) / (1.02, 1.01, 1.0) / 0.96 / 0.08, 0.65 | (0.003, 0.003, 0.006) / (1.0, 0.99, 0.99) / (1.02, 1.01, 1.0) / 1.0 / 0.08, 0.7 |
| Card tint | 1 | 1 | (0.86, 0.86, 0.95) |

Why these choices:

- **The shade is still blue-violet.** The base SHADE stays blue (B ≈ 2 x R). The faces turned away from the window and the room depth go navy.
- **The woods stay warm.** The ambient tints on the woods, ceiling and floor carry more green than red, so dark browns land at hue 15-30 (orange-brown) and not at hue 0-5 or 300+.
- **The dark lift is kept low and only slightly blue.** Its blue part pulled every dark red-brown toward magenta: the storm went from 14.5 to 6.1 percent magenta when it was cut.
- **The wallpaper keeps its key cut (kgain 0.6-0.7).** Without it the crimson wall took half of all chroma (red 47-50 percent).
- **The red track gets a raised key gain and a red-only ambient.** In the map close-ups the line measures RGB (236, 6, 4) in day, (205, 64, 66) in grey and (145, 34, 38) in storm (`proof/close.jpg`, plan view 0.45 D). It stays the most saturated mark on the map.

## 3. Measured (`prove.py`, `proof/`)

Setup for every measurement:

- Stage actors: `actors.Actor` hero and boss, `head_flip`, contact decals, shadow proxies, 256 px per D.
- Two-shot cameras (eye_two_shot, high_two_shot, wide_high): the chief stands far at boss_mark and the hero near at near_mark (as take B).
- low_medium: both actors at the wall marks.
- insert_rake: no actors.
- Render: 720x1280, 12 samples.

**hue_report.py rows** (the five cameras with actors; `python3 v3/tools/hue_report.py "proof/stills/<preset>_*.png"`). Band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15.

| Preset | red | orange | yellow | green | cyan | blue | violet | magenta | sat | val | dark | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| office_day | 36.6 | 27.8 | 0.1 | 1.4 | 4.3 | 24.1 | 1.1 | 4.6 | 0.45 | 0.46 | 0.16 | dark 0.16 |
| office_grey | 38.7 | 33.5 | 0.0 | 2.7 | 1.2 | 20.6 | 0.6 | 2.7 | 0.41 | 0.45 (0.449) | 0.13 | val just under: deliberately a little dimmer and flatter than day |
| office_storm | 41.4 | 16.2 | 0.0 | 2.3 | 1.2 | 31.7 | 0.9 | 6.1 | 0.40 | 0.28 | 0.43 | special light (a night-dark storm with lamps on) |

office_storm is outside the band in red (just over), orange, blue, value and dark share. This is a deliberate "special light" shot, as CONVENTIONS allows: the storm is meant to be darker. Its shade still reads blue-violet, and magenta stays at 6.1.

**Head fill and ink colour on screen; wall luminance in a ring 0.62-0.95 D around each head** (actor pixels excluded by ray cast against the sprite alpha; display luma 0-255):

| Preset | Head fill | Ink: boss / hero | Wall ring: far head (boss) | Wall ring: near head (hero) |
|---|---|---|---|---|
| office_day | `#fff6f4` (V 1.00, S 0.043) | `#2d2b39`-`#302b39` / `#3b2b39` | 68-92 | 59-102 |
| office_grey | `#fff9fa` (V 1.00, S 0.028) | `#2e2b39`-`#362b38` / `#3a2c38`-`#3a2c39` | 73-82 | 63-89 |
| office_storm | `#eee6f0` (V 0.94, tint) | `#272737`-`#2a2635` / `#312632`; the ring catches the hero's red hair on two cameras: `#421c21` | 44-47 | 38-50 |

Per camera, wall ring luminance far / near:

| Camera | day | grey | storm |
|---|---|---|---|
| eye_two_shot | 90.5 / 66.7 | 76.2 / 71.2 | 44.9 / 40.8 |
| low_medium (hero / boss at the wall) | 102.3 / 63.6 | 88.9 / 73.0 | 49.5 / 44.2 |
| high_two_shot | 91.8 / 62.6 | 81.9 / 70.4 | 46.9 / 40.7 |
| wide_high | 68.3 / 59.3 | 73.5 / 62.9 | 44.8 / 37.5 |

The heads stay the brightest large shapes in all three presets. Only 0.8-2.4 percent of frame pixels are as bright as the head fill: the heads themselves and the bulb cores. In grey the wall behind the near head is a little brighter than in day (no shadow falls on it), and the far ring is a little lower. The reference band is 95-170. The day set was already under it (COLOUR.md section 4.2), and the storm is under it on purpose.

**Cost of a final frame** (720x1280, 12 samples, 4 threads, eye_two_shot with two actors, median of frames 2-4; `proof/timing_4t.json`). Another agent's render was running: 1-minute load 3.0-3.6.

| Preset | Wall s | CPU s |
|---|---|---|
| office_day | 4.82 | 17.97 |
| office_grey | 5.10 | 19.40 |
| office_storm | 4.89 | 18.70 |

A lightning frame (flash 1.0, office_storm, placeholder actors) costs the same as an unlit one: 3.8 against 4.0 s, 14.5 against 15.2 CPU s (`proof/timing_flash.json`).

The first version blocked the shell with Cycles light linking (a blocker collection). That gave the same picture but cost 30 percent more per frame: 18.6 against 14.1 CPU s on the same frame. It was replaced by toggling `visible_shadow` on the shell objects, keyed on lightning frames.

**Flash strip** (`proof/flash_strip.jpg`, office_storm, eye_two_shot, `lightning(2)`): frames 1-6 have flash 0, 1.0, 0.35, 0.8, 0, 0. At 1.0 the window and bar pattern whites the floor and the map wall, and the actors throw hard shadows. At 0 the frame is the plain storm. The flash frames are a little grainy at 12 samples (soft 1.2 deg edges), which is acceptable for one-frame flashes.

**Rain card at 4 times** (`proof/rain_strip.jpg`, Blender frames 1, 25, 49 and 73 of the loop, office_grey and office_storm, from a camera at the window): the drops move and the trails follow them. The storm lash slants with the wind. The overcast sky has no tile seam.

**Wall map from very close** (`proof/close.jpg`, raking at 0.75 D and square-on at 0.45 D, as in shots 19-22): readable in office_grey and office_storm. The land is tan, the sea blue-slate, and N.Y., BOSTON, FLA., the isobars and the grid are all legible. The red line stays red. There is no sun patch and no bar shadow on the paper in grey, so a 7-second take sees no moving light.

## 4. Limits and notes

- The plan's light column says "key x0.3 and cool". The key is x0.29 and neutral-warm (0.66, 0.58, 0.50). That is much cooler than the day sun, but not blue, because a blue key turned the floor and woods to grey mud (orange share 10-14 percent in the early passes). The coolness is in the ambient instead.
- The plan's light column also says "sun geometry kept". The key direction is the reviewed one (the toon shading normalises to it), but the shell no longer shadows it in grey and storm. That is what "no sun patch" requires.
- Lightning lights with the room shell casting shadows. The base key also casts the window pattern on those frames, but under the flash it cannot be seen.
- The actors' shadow proxies follow "the first visible sun". `olt_flash` points in the same direction as `key_sun`, so the shadows agree.
- `tint_cards()` inserts a Multiply node (`olt_tint`) into actor-card materials (objects named `*_card` or `actor_*`). With (1, 1, 1) the card is unchanged.
- The grey value is 0.449 against the band's 0.45. It is left a hair dimmer on purpose, to read flatter and sadder than day.
- The storm is a special light: dark share 0.43 and value 0.28.
- Not done here: props (note glyphs, ink-blot card, label), shots 17, 18 and 25, and the conform-step white flash overlay into shot 26.
