# v3/set3d8/desert.py : film 8 sets ("ไอ้บ้าน้ำแข็ง", the ice-maker of the Persian desert, c. 1600) (bpy 5.3, Cycles CPU)

Files:
- `desert.py`: the two locations (`desert_ice`, `bazaar`) and their hooks.
- `desert_tex.py`: the artwork. Patterned surfaces (sand, mud-brick, kahgel plaster, the three channel states, ice blocks, heat wisps, Persian brick, tile bands and panels, kufic band, 6 carpets, 2 kilims, pavers, lattice, pierced-lantern glass, shop niches, the painted desert / town rings) are SVG rasterised by `v3/set3d/raster.js`. The four skies (`sky_NIGHT` 8192 px wide with ~13 000 stars and the Milky Way, `sky_DAWN`, `sky_NOON`, `sky_SUMMER`) are painted with numpy + PIL. Everything is cached in `tex_desert/` by content hash (bump `SKY_V` to repaint the skies).
- `desert_hue.py`: hue rows through `v3/tools/hue_report.py`.
- `contact.jpg`: every preset x relevant light (and ice state) at 720x1280, 12 samples, with placeholder actors, plus a row of 6 reference frames (A t0069 t0077 t0081 t0061, B t0033 t0029). The cyan line is y 880. `contact_small.jpg` is half size.

Work files in `desert_work/`: `final/` (the finals), `stills/` (360x640 previews), `final_log.txt` (CPU s and head pixels per frame), `hue_rows.txt`, `t_anim.py` (hook test; also renders `hooks/` + `hooks.jpg`), `run_finals.sh`, `sheet.py`, `actors/`, `REF_*.jpg`.

Built on `v3/set3d7/louvre.py` → `bakery.py` → `mine.py` → `pagoda.py` / `tower.py`. Helpers are imported, not copied:
- `tower`: `mat_lit`, `mat_emit`, `MB`, ink hull, `setup_grade`, `make_camera`, `render`, `no_bounce`, keys (`_key`, `_show`, `_fcurves`), `placeholder_actor`.
- `pagoda`: `_kd`, `_haze_mat`, `digest`. `mine`: `obox`, `beam`, `rod`, `lumpy`, `catenary`, `chain_rod`, `_obj`, `_untoon`, `_glossy`, `_append_shader`, `_denoise`, `setup_render`.
- `bakery`: `Frame`, `_mat_add` (camera-only glow / scrolling wisp cards), `_halo`, `_light`. `louvre`: `_flick`.

`desert.STATE` is `tower.STATE`. **No depth of field anywhere** (`apply_dof()` is a no-op; `setup_dof` is re-exported for the film-6 shot scripts).

World: 1 unit = 1 D (head diameter), Z up, ground z = 0, **+x = east, +y = north** (the sun is in the south, -y). `build` clears the scene and builds only the preset's area.

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d8"); import desert as D
A = D.build('desert_ice', 'channels_wide', light='NIGHT')   # build(location, preset=None, clear=True, dress=True, light=None) -> anchors
cam = D.make_camera(A['cam'])                # preset camera; all cameras of the area in A['cams'], A['cam_name']
D.setup_render(scene, 'final' | 'preview')   # 720x1280 12 samples / 360x640 6, 2 threads, direct light, OIDN, light tree off
D.apply_preset_state(preset); D.clear_keys()
D.stage_placeholders(A, cam_name, cam_loc); D.head_pixels(cam_name)   # stand-in cards + caption check
D.render(path) -> (wall s, cpu s);  D.digest() -> sha1
```

`light=` takes any key of `D.LIGHTS`: **NIGHT | DAWN | NOON | SUMMER**, for every preset of both locations (the time-of-day hook: rebuild with another light).

**Keys rule** (as the templates): once a hook was keyed with `frame=`, keys win over un-keyed calls. Key every state, or `clear_keys()` first.

### Hooks (all keyable with `frame=N`; key the start state too)

| hook | where | what |
|---|---|---|
| `set_ice(level, melt=0, frame=None)` | desert_ice plain | Every channel. `level` 0 = open water (dark, mirrors the sky and the stars, warm lantern glints) .. **0.25 = night 1: a thin translucent sheet** (water and stars show through, white frost needles, whiter rims at the banks, hair-line cracks) .. **1 = night 10: thick opaque white-blue slab** (milky patches, cracks, bubble strings; the sawn hole in channel 2 shows cut faces 0.185 D high). `melt` 0..1 fades the ice into **brown mud and grey slush with puddles** (the puddles mirror the sky); the water under it turns murky. Strings: `'water'` (0, 0), `'thin'` (0.25, 0), `'thick'` (1, 0), `'mud'` (1, 1). Material values keyed linear; the ice plane rises 0.08 D with thickness. |
| `set_heat_wisps(level, frame=None, speed=1)` | desert_ice plain | The reveal: faint shimmering heat ribbons rising from all five channels toward the stars (30 crossed camera-only cards, 14-22 D high, faded at both ends). 0 none (cards hidden, no cost) .. 1 clear .. 1.5 strong. They drift upward with the frame number: **call every frame**. Cost +5 CPU s when shown. |
| `set_flames(k=1, frame=None)` (= `set_lanterns`) | all | Every lantern, the camp fire, the dome door glow, the lamp-lit shop niches: lamp energies + glow materials, 0 out .. 1 normal .. 1.5 bright, deterministic flicker from the frame number. **Call every frame**. |
| `set_stars(k=1, twinkle=0.35, frame=None)` | sky (NIGHT, DAWN) | Star brilliance: the brightest stars are boosted above 1 and bloom (k 0 flat .. 1 normal .. 2 brilliant); `twinkle` 0..1 per-star flicker from a 4D noise whose W follows the frame. Call per frame for twinkling. No effect in NOON / SUMMER. |
| `clear_keys()` | all | Drop every hook key. |

`desert_work/t_anim.py`: ALL OK (water → thin → thick → mud keyed and eased, cut-face thickness, wisp level and scroll, flame flicker, star twinkle W). It renders `hooks.jpg`: ice water / thin / 0.55 / thick / melting 0.5 / mud, wisps 0 / 1 / 1.5.

## 2. Presets (`D.PRESETS`, `D.LOC_PRESETS`)

| location | preset | area | default light | state at build |
|---|---|---|---|---|
| desert_ice | `channels_wide` | plain | NIGHT | ice 0.25 (thin) |
| desert_ice | `channel_ecu` | plain | NIGHT | ice 0.25 |
| desert_ice | `wall_low` | plain | NOON | ice 1 |
| desert_ice | `dome_wide` | plain | NIGHT | ice 1 |
| desert_ice | `sky_reveal` | plain | NIGHT | ice 0.6, wisps 1 |
| desert_ice | `dome_interior` | inside the dome | NIGHT | lanterns |
| bazaar | `bazaar_wide` | bazaar | NOON | |
| bazaar | `merchant_stall` | bazaar | NOON | |
| bazaar | `well_eye` | bazaar | NOON | |

Relevant lights per preset (all in `contact.jpg`): channels_wide NIGHT / DAWN (thick) / NOON (mud) / SUMMER (mud); channel_ecu NIGHT water / thin / thick, NOON mud; wall_low NOON / DAWN; dome_wide NIGHT / SUMMER; sky_reveal NIGHT; dome_interior NIGHT / SUMMER; bazaar_wide NOON / SUMMER / NIGHT; merchant_stall and well_eye NOON / SUMMER.

### What each area holds

**The plain** (desert_ice)
- Desert floor (warm rippled sand, pebbles) to R 150; packed-earth banks with raked lips.
- **Five channels**, x -26..26, 2 D wide, centres y 1.8 / 4.6 / 7.4 / 10.2 / 13.0, trench floor z -0.32, water z -0.13. Channel 2 (y 4.6) has the sawn hole at x -1.6..0.
- **The shade wall** along the south side: x -30..30, y -2.4..-0.8, **15 D high** (3 storeys), battered north face, pilaster strips every 6 D, two rows of beam ends (storey lines z 4.6 / 9.6), putlog holes, a stepped merlon crest, a mud stair up the west end.
- **The yakhchal**: centre (38, 8), foot R 12.5, 27 D high, 13 steps of straw-mud kahgel, a chimney cap with the dark vent, a buttressed base ring, the porch facing west with a pointed arch; the passage behind it **glows warm** (lamps ≥ 0.5: NIGHT, DAWN).
- The qanat outlet at the west end, the feeder ditch, a wooden sluice per channel, a line of 12 qanat shaft mounds marching west-north-west.
- Farid's camp at the west end of the wall: reed lean-to with a kilim, the **brazier fire**, buckets, the ice saw and pick, three cut blocks on a straw mat, a wooden sledge.
- **Warm practicals into depth**: five lantern posts on the banks (x -20, -9, 2, 12, 22), a lantern on the bank by the cut hole, the fire, the dome door.
- Date palms, camel-thorn shrubs, rocks; the painted ring (R 120): Zagros ranges, dunes, the mud town with domes, windcatchers, a minaret and palms (warm windows at NIGHT).
- Sky dome R 160. **NIGHT: deep blue, ~13 000 stars (sparkle crosses on the brightest, bloom), the Milky Way** with dust lanes and a warm core rising from the north-east horizon (az 35°) to near the zenith (best seen in `dome_wide` and `sky_reveal`). DAWN: sun on the east horizon, pink cloud streaks, last stars in the west. NOON: deep blue, sun in the south 50°, a few flat clouds. SUMMER: white-hot sun 72°, hazy horizon.

**Inside the dome**: corbelled inner cone (R 11.6, 25 D high, mud-brick rings) to the oculus (sky disc), the walkway ring r 9..11.6 at z 0, **the ice pit** (r 9, 6 deep) stacked with sawn blocks to z -1.6 under a straw layer, a top layer of separate blocks to z -0.8 (one corner cut away, a few blocks two high), a ladder down, the arched door (west) with the sky outside, three lanterns (one on the ice beside the camera, warm orange against the cool ice), a sledge, blocks and a bucket on the walkway. Moon/sun shaft from the oculus when the key is steep (NOON/SUMMER).

**The bazaar** (street along +y, x -4.5..4.5, y -14..30; square y 30..46, x -13..13)
- Two rows of two-storey **Persian brick arcades** (4.5 D bays, 10.5 D high): ground pointed arches with **tile spandrels** (two girih panels) and a turquoise alfiz frame, the shop niche (raised plank floor, a lamp-lit goods wall of shelves: copper, jars, cloth) — warm in the blue shade. Upper storey: arched window niche with a wooden lattice and a ledge, the cobalt tile band, a kufic-style ornamental band (not readable text), crest.
- Goods per bay under **striped awnings** on poles (4 colourways): hanging and stacked **carpets**, copper pots and trays, terracotta/turquoise jars, **spice baskets with coloured cones**, fruit crates (pomegranates, dates, melons).
- **Strings of pierced-brass lanterns** across the street every 9 D, and wall lanterns on brackets.
- **The water merchant's stall** (east row, y 4..13): a raised takht (z 0.9) under a great carpet canopy on four gilt-banded posts, two lanterns, bolsters, a kilim front, **five huge water jars** (turquoise and terracotta), a brass tray of copper cups, a brass ewer, the coin chest with gold.
- **The square**: arcades on its sides, **the well** at (1.5, 37.5): octagonal tile parapet, stone rim, water (sky mirror), timber frame, pulley wheel, rope, bucket, water jars round it.
- **The mosque iwan** closing the square (y 46): 14 x 19 D tiled pishtaq, the half-dome niche, kufic band, two minarets with turquoise caps, the **turquoise onion dome** on its drum.
- Painted ring: the town wall with round towers, domes, minarets, windcatchers, mountains.

## 3. Cameras, stand points, card scales, caption check

Card scale: the card height in D equals the role height in `D.HEIGHT` (cast scale 1.0): **farid 3.0, merchant 3.2, woman 2.9, oldman 2.9, boy 2.3**. Placeholders use `beach_man` (farid), `boss` (merchant), `beach_woman`, `senior_a`, `beach_kid` until the film-8 cast exists.

**Caption rule: every staged head stays above y 880 of 1280.** The table gives head centre / **chin** px at 720x1280 (`head_pixels`). All chins < 880.

| cam | loc → look_at, lens | shows | staged (feet) | head centre / chin px |
|---|---|---|---|---|
| `channels_wide` | (-33, 17, 9) → (10, 3, 2.6), 20 | high from the north-west: the five channels running east, the wall on the right, the dome at the end with its glowing door, lantern posts into depth | farid (-16, 8.8) | 780 / 797 |
| `channel_ecu` | (-4.2, 4.4, 1.05) → (5, 6.0, -0.35), 22 | low over channel 2: the ice surface fills the lower half (state reads clearly), the sawn hole and its cut faces, the bank lantern, the dome and its door behind | farid (2.2, 6.35) on the bank | 342 / 406 |
| `wall_low` | (-7, 14.5, 2) → (0.5, -1, 7), 20 | from the channels up at the 15 D wall: crest against the sky; at NOON the sun blazes over the crest and the wall face is in blue shade | farid (-2.2, 0.9) at its foot | 820 / 846 |
| `dome_wide` | (4, 1.4, 2.8) → (38, 9.5, 10), 22 | the yakhchal across the channels, porch door warm; at NIGHT the Milky Way rises left of it | farid (21.5, 7.4) at the door | 814 / 837 |
| `sky_reveal` | (-2, 1.4, 0.5) → (18, 10, 9), 18 | low in channel 1 looking up north-east: ice in front, heat wisps rising from every channel, the Milky Way overhead, the dome and its glowing door, lanterns | none | — |
| `dome_interior` | (-9, -0.6, 2.9) → (3, 2.2, -0.4), 18 | inside from the walkway: the ice stack, the warm lantern on the ice, the far lantern, the brick rings of the cone | farid (-4.2, -0.9, z -0.8), merchant (-2.6, 2.4, z -0.8) on the ice top | 636 / 699, 564 / 609 |
| `bazaar_wide` | (0.4, -12, 6.4) → (0, 30, 4.4), 20 | high down the street: both arcades, awnings and goods, lantern strings, the merchant stall right, the iwan, minarets and dome | woman (-2.4, 4), boy (1, 8), oldman (-1.6, 15), farid (1.4, 19) | 782..695 / 804..707 |
| `merchant_stall` | (-3, 0.5, 3.3) → (4.2, 9.6, 2.7), 22 | the merchant's stall: canopy, lanterns, takht, jars, chest; the east arcade above | merchant on the takht (3.3, 8.1, z 0.9), farid (0.4, 6.2) | 576 / 615, 694 / 753 |
| `well_eye` | (-4.2, 26, 2.6) → (1.6, 40, 4.6), 22 | eye level in the square: the tiled well with its pulley, the iwan and minaret behind | woman (3.4, 35), boy (-1.2, 34.2), oldman (-2.8, 38.5) | 757 / 793, 817 / 864, 756 / 790 |

### Stand points (`A['marks']`, feet; z is the floor)

**Plain**: `farid_camp` (-18.4, 1.6), `farid_cut` (-1.8, 6.1) beside the hole, `farid_pour` (-6, 8.8), `merchant_watch` (-12, 17) beyond the channels, `townsfolk` (-14.5, 16.4) / (-9.5, 17.6), `wall_foot` (4, 0.25), `dome_door` (21.5, 9.2), `bank_lanes` y 3.2 / 6.0 / 8.8 / 11.6 (walk along x on the banks). Plus `A['channels']`, `A['wall']`, `A['dome']`.
**Dome inside**: `farid_walk` (-9.6, -2.4, 0), `merchant_walk` (-9.8, 2.6, 0) on the walkway; `farid_on_ice` (-4.2, -0.9, -0.8), `merchant_on_ice` (-2.6, 2.4, -0.8), `farid_pit` (-1.5, 2, -0.8) on the top layer of blocks; `lantern`.
**Bazaar**: `merchant` (3.3, 8.1, 0.9) on the takht, `merchant_front` (-0.1, 9.7) in front of the jars, `street_centre` (0, 8), `passers` (-2, 2) (1.6, 12) (-1.4, 22), `well` (1.5, 37.5), `well_woman` (3.6, 35.4), `boy` (-0.8, 34.4), `oldman` (-3.6, 36.6).

Keep-out zones are in `A['keep_out']` (channels, wall, dome, camp; pit; goods |x| > 2.1 in the street, takht, jars, well, iwan).

## 4. Light presets

Same light model as the templates: one hard sun (or moon) with real shadows, painted shade emission, no bounce, every material `_untoon`ed (plain Lambert), warm point lamps for the practicals (shadowed only where it matters), camera-only halo cards, the grade compositor with bloom.

| light | key | shade | practicals | sky / ring / haze |
|---|---|---|---|---|
| NIGHT | moon (0.24, 0.34, 0.72), 38° from the north-west, desat 0.25; ground gain 0.55 | (0.055, 0.085, 0.24) | lanterns 50 W, fire 220 W (shadowed), dome door 60 W, all glows x 1; bazaar lanterns 90 W | stars + Milky Way (star bloom), night ring with warm windows, blue haze |
| DAWN | low sun (1.70, 0.98, 0.62) from the east, 7° | (0.10, 0.12, 0.28), mix 0.55 | lamps x 0.7 | sunrise sky, pink haze |
| NOON | harsh sun (1.80, 1.52, 1.08) from the south, 44° (bazaar: from the south-west, 56°, so the east row is lit, the west row in blue shade) | (0.10, 0.12, 0.30), mix 0.45 | lamps x 0.35 (shop niches keep glowing) | deep blue sky, white haze |
| SUMMER | white-hot sun (1.92, 1.72, 1.18), 70° | (0.12, 0.13, 0.29), mix 0.45 | lamps x 0.3 | white-hot sky, strong heat haze, grade sat 1.06 |

Inside the dome the shade is pushed to hue ~205 (complement of the orange lanterns; red mud + violet shade read magenta), an oculus fill (cool at night, warm-yellow by day) and a door fill light the cone.

## 5. Measured

**Render cost** (final 720x1280, 12 samples, 2 threads, denoise + bloom; `desert_work/final_log.txt`): 14..24 CPU s per frame (all ≤ 25). Highest: `channel_ecu` NIGHT 23.9 (lantern glints in the ice), `sky_reveal` NIGHT with wisps 23.7, channel_ecu water 23.0. The wide plain frames 14-18, bazaar 17-20, interior 17-19.

**Hue** (`desert_work/hue_rows.txt`): see that file for every frame. Night frames are blue-dominant (~90-98 % blue, like ref A's night frames at 82 %), magenta ≤ 3 in every frame (dome_interior SUMMER 2.8 after pushing its shade to hue ~205). All NOON frames: red 5, orange 26, blue 57, violet 7, sat 0.47, val 0.56, dark 0.09; SUMMER: red 11, orange 42, blue 38; DAWN: blue 65, violet 31 (dawn shade + sky). Day frames are bluer and less red than ref A (red 30-41 / blue 14-30) because the desert frames are half sky and half wall shade; the bazaar stall is closest. Dark fraction is low (0-9 % vs 8-15 %).

**Determinism**: `D.digest()` identical in two processes: desert_ice channel_ecu `2fa4dbfa…`, bazaar merchant_stall `dd86cd4f…`.

## 6. Command line

```
python3 desert.py stills <desert_ice|bazaar> [preset[:LIGHT[:ice[:wisps]]] ...]   # desert_work/stills 360x640, placeholders, head pixels
python3 desert.py final  <desert_ice|bazaar> [spec ...]                          # desert_work/final 720x1280 12 samples, CPU s, head pixels
   e.g. python3 desert.py final desert_ice channel_ecu:NIGHT:thick dome_wide:SUMMER:mud sky_reveal:NIGHT::1.5
python3 desert.py digest <loc> <preset>
desert_work/run_finals.sh ; python3 desert_hue.py desert_work/final ; python3 desert_work/t_anim.py [norender]
cd desert_work; W=360 H=640 COLS=6 CAP=1 python3 sheet.py ../contact.jpg <pngs...>
```

## 7. Known gaps (honest)

- **The Milky Way sits in the north-east** (az ~35° rising to near the zenith). It is the hero of `dome_wide` and `sky_reveal`; `channels_wide` (looking east-south-east) shows only stars. To get it in another framing turn the camera toward az 20-60°, or change the pole in `desert_tex._sky_paint` and bump `SKY_V`.
- **Hue vs the band**: the desert day frames are blue-heavy (sky + wall shade) and low on red; the dark fraction is low everywhere (no deep blacks; the look is airy). Night frames are by nature ~95 % blue.
- `wall_low` is a big shaded wall: readable but plain (wall face in blue shade; the drama is the sun over the crest at NOON). At DAWN it reads violet-blue.
- The lantern glints on the ice / water are bright warm blooms (pretty, but large in `channel_ecu`); lower `_glossy` on `_mat_ice` or the lamp energies if a shot needs calmer ice.
- Heat wisps are camera-only cards; seen from below at the top of `sky_reveal` they read as long streaks (by design faded at both ends). Do not show them with level > 1.5.
- The thin-ice state is a translucent veil + frost texture, not real refraction; very low grazing views show the reflection more than the frost.
- `dome_interior`: the oculus is above the frame (the cone is 25 D high); the moon shaft appears only with a steep key (NOON / SUMMER). The interior is a separate area (cannot be seen from the plain through the door).
- Bazaar: the arcade bays repeat (4 shop-wall images, random goods); the merchant stall projects 2.6 D into the street, the street is walkable at |x| < 2. Square side arcades exist but the square's south corner walls are flat.
- **Placeholders only** (cast from earlier films). The well rope/bucket, saw, pick, buckets are static set props; the hand props of the brief (bucket, saw, ice block, coin purse, water jar) belong to the cast.
- Summer channels use `set_ice('mud')`; there is no separate "dry, cracked" channel state.
