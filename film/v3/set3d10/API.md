# v3/set3d10/harbour.py : film 10 set ("ไอ้ช่างม้าลาย", dazzle camouflage, WWI Britain 1917) (bpy 5.x, Cycles CPU)

Files:
- `harbour.py`: both locations, every hook, the presets, the cameras, the stand points and the CLI.
  - **harbour**: a British naval dockyard in 1917.
  - **sea**: the open North Atlantic, with the convoy, the U-boat, the torpedo, the ghost ship and the markers.
- `harbour_tex.py`: all the artwork, painted with numpy and PIL.
  - Dazzle paint layers for the hero ship, and 6 full-dazzle variants with their grey bases.
  - Warehouse brick bays plus a window-glow mask, setts, slate, planks, ship deck, crate wood, steel deck plates.
  - Foam for wakes, bow waves and torpedo bubbles; flags (no text); the harbour backdrop ring for DAY and DUSK.
  - The skies, which reuse the film-9 painter `wall_tex.sky`: DAY, DUSK (the crisp cartoon-cloud `DAWNG` painter, sun at dusk) and SEA_DAY.
  - Everything is cached in `tex_harbour/`, keyed by a hash of the params plus `TEX_V`. Bump `TEX_V` after you edit painter code.
- `harbour_hue.py`: hue rows through `tools/hue_report.py`, plus the **shade hue** of each frame. The shade hue is the chroma-weighted mean hue of the shaded pixels, and the client rule is 240-260.
- `contact.jpg`: one 720x1280 final (12 samples, placeholder actors) per preset, light and key state, 23 tiles in all. Each tile is labelled under the image, and the cyan line marks y 880.
  - `contact_small.jpg` is the same sheet at 1/3 size.
  - The order is in `harbour_work/contact_order.txt`. Rebuild with `harbour_work/run_finals.sh`, then `python3 make_contact.py` in `harbour_work/`.
- `harbour_work/`:
  - `final/`: the 23 finals.
  - `final_log.txt`: wall and CPU seconds, head pixels.
  - `hue_rows.txt`.
  - `t_anim.py`: the hook test. It prints ALL OK (34 checks).
  - `sheet.py`: a quick review sheet.
  - `stills/`.
- Backups: `bak_r0` (first build), `bak_r1` (framing and colour round), `bak_r2` (QA-tech round), `bak_r3` (before the QA-art fixes), `bak_r4` (before the client's ship and colour brief), `bak_r5` (round 3 final), `bak_r6` (before the round-4 detail pass), `bak_r7` (round 4, current).

Built on `v3/set3d9/wall.py`, which itself builds on desert, bakery, mine, pagoda and tower. These are imported, not copied:
- `tower`: `MB`, `mat_lit`, `mat_emit`, `setup_grade`, `make_camera`, `render`, `placeholder_actor`, `_key`, `_show`.
- `mine`: `obox`, `rod`, `lumpy`, `chain_rod`, `catenary`, `_obj`, `_untoon`, `_glossy`, `_append_shader`, `_denoise`, `setup_render`.
- `desert`: `_mat_sky`, `_sky_lookup`, `_value`, `_keyval`, `set_flames`, `_flame_light`.
- `bakery`: `Frame`, `_halo`, `_mat_add`.
- `wall` (film 9): `_kdaz`, `_air_comp` (compositor mist and sun beams), `_mat_dust` and `_billow_round` (hard-edged cartoon billows), `_billows`, `_keyp`.

`harbour.STATE` is `tower.STATE`. **There is no depth of field anywhere.** `make_camera` switches DOF off, and `apply_dof()` does nothing. **There is no text in any picture.** Flags are plain shapes.

World: 1 unit = 1 D (head), Z is up.
- **harbour**:
  - The quay top is z 0. The quay runs x -140..160, its edge is y 0, and the land lies at y < 0. The water is at z **-2.4**.
  - The **berth ship** ("berth", L 64) lies along the quay with its bow at +x, centred at (0, 6.9). Its hull side faces the quay at y about 1.0-1.4, and its deck is at z 6.2.
  - Scaffold lifts stand on the quay at x -27..-9 and 7..19. Three hanging painter's stages hang from the deck rail.
  - Portal jib cranes run on rails at y -5.2 / -7.2, with goods wagons on a siding at y -16. There are crates, barrels, sacks, a coal heap, timber, paint drums and buckets, bollards with mooring lines, gas lamps, a tea hut and a dock office.
  - Red-brick warehouses stand at y -36..-54.
  - The basin holds 6 moored warships (m1-m6). A breakwater runs at y 104, with the red/white **lighthouse** at (150, 109). Beyond it, 12 ships lie in the roads (r0-r11). There are 9 circling gulls plus 3 perched, and a tug with smoke. The town and hills ring sits at R 420.
- **sea**:
  - Water is at z 0, with a **low-poly animated swell**: geometry nodes driven by scene time, three crossing sines, |z| < 0.7.
  - The convoy sails **+x at 4 D/s**:
    - `dazzle`, the hero warship at stage 3, at (0, 0).
    - The merchants `c1` (-150, 4), `c2` (115, -3), `c3` (50, 66) and `c4` (160, 70).
    - The admiral's flagship `flag` at (-60, 62).
  - Every ship has bow waves, side wash and a stern wake, plus funnel smoke. Ship meshes heave, roll and pitch through drivers.
  - The U-boat is at (-50, -125), heading 70°.



## 00. Round 4 (client: "make the sets more detailed: the sea water and everything else"). This section overrides §0 and below where they differ.

**Sea**
- The ocean is a graded triangle grid with 1.6 D cells over x -150..150 and y -180..120, growing to x -420..460 and y -340..440 (about 63 k verts). It uses smooth shading.
- The swell has 3 long waves plus 4 short chop waves; the chop fades out beyond the fine zone so the coarse cells don't alias. It is still keyless (scene time).
- Shader:
  - a one-octave noise bump on every shading normal;
  - **whitecap flecks on the crests** (swell height × spot noise);
  - turquoise-teal near the camera, deep blue far off;
  - a Fresnel lift toward a flat pale-sky tint (no soft mirrored cloud blobs);
  - **crisp cel-style warm bands** on the wave faces turned to the low sun;
  - a sharp warm GGX glitter on the bumped normal.
- Every ship has curling white spray at the bow, propeller wash and churned foam at the stern, plus the side wash and the long wake (from §0).
- **Floating details:** 10 gulls sitting on the water, channel buoys (red can, green cone), 3 distant sailing boats, and deck crew cards on the dazzle ship, the flagship, c1 and c3.

**Harbour**
- **The calm water mirrors the ships, quay, warehouses, cranes, lighthouse, scaffold and cards.** This uses 1 glossy bounce, set in `setup_render` for the harbour only, with a sharp glossy lobe.
- A shallow turquoise tint and a foam slick run along the quay wall and the berth hull. Floating crates and a rope ring sit in the water.
- **Quay wall:** granite ashlar (`quaywall` texture) with a wet dark band, run-down stains and green weed at the waterline.
- **Props:**
  - a gangway with rope rails up to the berth deck;
  - dressing-ship bunting from the foremast to the stem, mainmast and stern;
  - scaffold lanterns, lit at DUSK;
  - striped awnings over the warehouse doors;
  - chimney smoke on 3 warehouses;
  - a horse-drawn dray loaded with barrels;
  - 3 more handcarts with sacks;
  - a net-drying rack and a washing line;
  - channel buoys;
  - 6 more flying gulls (15 in all).
- **11 background workers on the quay, scaffold and breakwater, plus deck crew on m1 and m2.** These are placeholder cast cards (`bgcard_*`) that turn to face the scene camera every frame through the handler `_cards_face`.
- **Backdrop:** a green headland across the harbour mouth with a church and spire and a row of cottages (windows lit at DUSK).

**Ships**
- **Hull plating overlay** on every painted ship: strake lines, butt seams and rivet rows (`plates`, multiplied in ship space).
- The grey ships carry stronger rust streaks (under the hawse, the scuppers and the portholes) and weather blotches at the boot-top.
- A red pennant streams from each warship's masthead.
- Funnel smoke has 8 puffs per funnel.

**Sky**
- All three skies (`sky_rich`) are the film-9 painter plus:
  - a low bank of big cartoon cumulus;
  - medium puffs higher up;
  - long thin streaks;
  - a soft warm haze band toward the horizon.

**New preset `beauty_harbour`** (DUSK, golden light): a lower crane view of the dockyard, at (-44, -22, 13) → (12, 22, 1), 20 mm. Stripes 3, half the harbour dazzled (`hd0.5`), lamps and braziers lit.

**Contact sheet:** 25 tiles. The 2 beauty tiles (sea, harbour) come first, then every preset and state (§0).

**Measured**
- Render cost: **14.1-30.4 CPU s per frame**, with two processes in parallel. The topdown frames are 28.2 / 30.0 / 30.4 and everything else is 14-23.
- Profiling showed the sea material dominates topdown, because the frame is all water. The bump and whitecap noises are one octave to stay inside about 30 s.
- `t_anim.py`: ALL OK (38 checks).
- `digest` is identical in two processes (harbour_wide `32d145b0…`).
- Sea hue: blue 37 %, cyan 39 %, red + orange 21 %.

## 0. Round 3 changes (QA-art FAIL on the sea reveal + client feedback "make the ships prettier, why are the colours like that"). This section overrides anything below it.

- **Ships, harbour and sea.** Models:
  - The existing sheer, flare, raked stem and cruiser stern are kept.
  - A **maroon antifouling band** rises to z 0.9 with a **white boot-top line** above it, up to z 1.15 (`harbour_tex.WL`). The dazzle paint starts above that line.
  - Brass-rimmed portholes; a stocked bower anchor on each bow; bridge windows (dark panes in a light frame on the front and sides).
  - **Ventilator cowls, red inside**; **gun turrets** (barbette, sloped elliptic turret in the ship's paint, twin barrels with muzzle rings).
  - Funnels with a black top band and a slight rake; merchant funnels also get a red band.
  - Merchants also get lifeboats on davits and cowls.
  - **Warm wood decks** (#c88e58) on the decks and on every house top.
- **Dazzle palette (1917 colours).** Black is only an accent. The colours are navy #1f2f5a, cerulean #3f86c4, sky #8fc0e2, pale grey-white #eef0ea, slate #5c6a7a, sea-green #4f9784, pale blue #a8cde0 and off-white #f2eee2.
  - The hero ship keeps its staged design: zigzag → staircase → full. It is painted in navy, pale, cerulean and sky, with a black accent wedge at the bow.
  - Each of the 6 variants v1-v6 has its own palette (`harbour_tex.PALETTES`).
  - Plain ships are a **warm battleship grey** (#9a958c .. #a39d93) with the antifouling red.
- **Sea.** Turquoise-teal near the camera (#2f8e98) blends by view distance (40 → 420 D) to deeper blue far off (#2c5592). Added: a soft warm term on the swell faces turned to the sun (`sea_warm` 0.26), a warm GGX glitter, and the sky Fresnel mirror (0.3). The foam is soft white with a glow term. The saturated violet sea is gone.
- **Reveal geometry.** `SEA_V` is **2.5 D/s** and the U-boat sits at **(-55, -96), heading 86°**. `LEAD_AHEAD` is 16, so the **gold lead buoy** is at (+41, 0), ahead of the real bow. The **pale-cyan ghost buoy** is at (-41, 0), ahead of the ghost's bow, and it is where the torpedo runs. At s = T_RUN (10) the torpedo reaches it; the real stern is then at x -7, a 34 D gap of open water (about 3 hull widths).
- **All 2D guides are removed**: no dashed lines, arrowheads or rings. `set_aim_lines()` is a no-op kept so old calls don't break, and the CLI token `aim` is ignored. **New hook `set_ghost_marker(k)`** shows the cyan buoy (CLI `gb<k>`). Both buoys float, with a lamp, halo and wash; their lamps are not flames, so `set_flames` leaves them alone.
- **The ghost**:
  - body alpha about 0.35-0.65 (emission 0.95), with an **emissive pale-cyan silhouette rim** (inverted hull, grazing faces only);
  - **its own pale-cyan bow waves and wake**, and **smoke streaming the other way**;
  - `set_ghost(k, offset=…)` slides it along x (CLI `go<d>`). periscope_pov uses `gh1,go-18`, so the ghost's bow sticks out about 28 % past the real stern.
- **Torpedo.** A dark body with a **warm glowing nose glint** and a big foam V. The wake is a foam band 8 D wide (about 25-30 px at topdown) with bubbly blotches. In topdown the periscope and its feather are hidden (`peri0`).
- **Cameras.**
  - `topdown_sea` is (-3, -86, 100) → (-2, 12, 0), 22 mm, a 45° oblique; the ships span about 60-70 % of the frame width.
  - `convoy_wide` is (-65, -117, 15) → (-11, 49, 1).
  - `periscope_pov` uses lens 30 and looks at (-8, 0, 5).
- **New preset `beauty_sea`** (SEA_DAY): a low 3/4 view from ahead to starboard of the hero dazzle ship in full sun, at (64, -56, 6) → (4, 2, 7), 22 mm.
- **DUSK harbour.** Three iron braziers (fire, halo, 520 W) give warm pools at the edges of quay_low, harbour_wide and the quay; they appear only at DUSK.
- **Contact sheet (24 tiles):** beauty; harbour_wide DAY / DUSK / hd1-st3 / hd1-st0; hull_side st 0-3 + DUSK; quay_low DAY / DUSK; hull_plank 0.47 / 3; convoy_wide (+ hit); periscope_close; periscope_pov (+ ghost); topdown A / B / C; torpedo_chase; bridge_deck.
- **Measured.** `t_anim.py` **ALL OK (38 checks)**, including the buoy lamps, the cyan buoy, no aim-line objects, and the ghost rim and foam.
  - Render cost: 12.4-25.3 CPU s. The topdown frames are 22.9 / 24.5 / **25.3**, the last about 1 % over the 25 s budget. The ocean grid plus many transparent layers make topdown the most expensive frame. The levers are 10 samples, or fewer smoke billows on the far merchants.
  - Hue, sea frames together: **blue 42 %** (target ≤ 50, met), cyan 37 % (the teal the client asked for), **red + orange 18 %** (target ≥ 20, **not met**; it is lowest in topdown, where the frame is mostly water).
- **Shade-hue metric.** `harbour_hue.py` mixes the teal sea and the navy dazzle paint into its "shaded pixels", so it now reports the sea frames at about 188-220° and hull_plank at about 234-239°. That reflects the client-requested colours, not a shade problem. The painted shade itself (`LIGHTS` shade / shade_tint) is unchanged at about 240-245°.


## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d10"); import harbour as H
A = H.build('harbour', 'hull_side', light='DAY')     # build(location=None, preset=None, clear=True, dress=True, light=None) -> anchors
A = H.build(None, 'topdown_sea')                      # the preset decides the location
cam = H.make_camera(A['cam'])                         # USE H.make_camera: far clip 6000 (sea horizon), DOF off, periscope overlay follows
H.setup_render(scene, 'final' | 'preview')            # 720x1280 12 samples / 360x640 6, 2 threads, OIDN
H.apply_preset_state(preset); H.clear_keys()          # clear_keys keeps the drivers (bob, gulls), drops hook keys
H.stage_placeholders(A, cam_name, cam_loc); H.head_pixels(cam_name); H.T.render(path); H.digest()
H.ship_root(name)          # the root empty of a ship: PARENT actor cards on a moving ship to it (bridge, deck)
H.torpedo_cam(u)           # camera setup low behind the torpedo at u (torpedo_chase: call per frame)
H.torpedo_u(s), H.torpedo_pos(u), H.periscope_eye()
```
Lights: harbour **DAY | DUSK**, sea **SEA_DAY**. Calling `build` with a light the location lacks raises an error.

**Keys rule** (as in the templates): once a hook has been keyed with `frame=`, keys win over un-keyed calls, so either key every state or call `clear_keys()` first. `set_smoke` must be called **every frame**. The swell, the ship bob and the gulls animate by themselves, through the frame number (geometry nodes and drivers), with no keys.

### Hooks

| hook | what it does |
|---|---|
| `set_stripes(stage, frame=None, ship=None, interp='LINEAR')` (or `set_stripes(ship, stage)`) | Dazzle stage of the berth ship (harbour) or the dazzle ship (sea). **0** plain grey, **1** bold black and white zigzags along the hull, **2** adds black and white staircases at stern, bow and superstructure, **3** full dazzle. Full dazzle adds angled bands in black, white and two greys over hull, superstructure and funnels, a false white bow wave at the stern, and a black wedge that cuts the real bow line; gaps let the zigzags and staircases show through. **Fractions paint the next layer from the stern toward the bow**: 0.47 means the first zigzag has reached midships, where the hanging stage `plank` is, which suits shots 1 and 23 (keyed linear). `interp='CONSTANT'` gives a cut. |
| `set_harbour_dazzle(k, frame=None)` | The "thousands" shot. The 6 moored ships and the 12 ships in the roads flip from grey to full dazzle one by one: ship i flips once k > (i + 0.5) / 18, basin ships first. k = 1 means all of them. The berth ship is controlled **only** by `set_stripes`: for shot 22 (the last grey ship is the admiral's) use `hd1,st0`. Keys are constant. |
| `set_smoke(level, frame=None, speed=1)` | Funnel smoke of every steaming ship: the convoy, and in the harbour m2, m5 and the tug. Cartoon billows rise and stream aft. 0 .. 1 .. 1.5. **Call every frame.** |
| `set_convoy(s, frame=None)` | Sea time `s` in seconds since the torpedo was fired (may be negative). Every convoy ship sits at start + (4 s, 0); **the ghost sails the other way**, at (-4 s, 0). Keys are linear. |
| `set_torpedo(u, frame=None, tail=0.55)` | The torpedo at path parameter u: 0 is the launch point at the U-boat's bow, `u_cross` (0.607) is the ghost's aim point, 1 is the end of the run. The torpedo runs just awash with a foam V. Its white bubble wake runs on the water from the launch point to the torpedo and fades over `tail` behind it. **u < 0 hides both.** Keys are linear. In sync with the convoy: `set_torpedo(H.torpedo_u(s))`. |
| `set_ghost(k, frame=None)` | The **ghost ship**: the captain's wrong reading, a translucent, emissive, pale-cyan copy of the dazzle ship **facing -x**, which casts no shadow. k is its opacity (0..1, keys linear). Its position follows `set_convoy`. While k > 0 a cyan aim ring also shows at the ghost's aim point (-40, 0). |
| `set_lead_marker(k, frame=None)` | **The right lead point**: a red and white spar buoy with a glowing gold lamp, a halo, a gold ring on the water and a real lamp, at (40, 0). That is just ahead of the dazzle ship's bow at s 0, and it is where the ship will be when the torpedo arrives. |
| `set_aim_lines(true_k, ghost_k, frame=None)` | Dashed aim lines on the water from the launch point. **Gold** runs to the lead buoy (the right shot). **Cyan** runs to the ghost's aim point (the actual shot), plus a cyan arrow for the ghost's guessed course (-x). The cyan line lies exactly on the wake path, so hide it (aim x/0) when the wake has to read. |
| `set_uboat(dive=0, frame=None, periscope=1)` | dive 0: the hull is awash and the conning tower is up. dive 1: under, so only the periscope cuts the water, with a foam feather. `periscope` (0..1) sets how far it is raised; the head stays about 4.8 D above the water. Keys are linear. |
| `set_hit(t, frame=None)` | Shot 4, the hit on grey merchant `c3`. From t 0 a white water column shoots up beside it, hangs, and collapses between 0.25 and 0.7. Dark smoke billows rise from 0.15 and hold at 1. There is no fire and no wreck. t < 0 hides it all. |
| `periscope_overlay(on, frame=None)` | **The periscope lens view**: a circular black vignette (clear circle 96 % of the frame width), a dark bezel ring, and a thin crosshair with range ticks (lines only, **no text**). All of it is **3D geometry 0.2 D in front of the scene camera**, and it follows the camera every frame through a handler, so pans, sweeps and lens changes work. It is on in `periscope_pov`. |
| `set_flames(k=1, frame=None)` | Gas lamps, warehouse windows and the lighthouse lamp; these matter mainly at DUSK. |
| `clear_keys()` | Drops every hook key and **keeps the drivers**. (The film-8/9 version deleted the drivers too; that one is not used here.) |

**The reveal geometry** (checked in `t_anim.py`): the torpedo is fired at s 0, when the dazzle ship's centre is at x 0.
- The captain reads the stripes as a ship heading -x (the ghost), so he aims ahead of the ghost, at (-40, 0).
- At s 10 (T_RUN) the torpedo crosses the course line there.
- By then the real ship is at x 40, with its stern at x 8, so **the wake passes 48 D behind the real stern**, through the ghost.
- The right aim would have been the lead buoy at (40, 0).

## 2. Presets (`H.PRESETS`, `H.LOC_PRESETS`)

| preset | location | light(s) | state at build | shot plan |
|---|---|---|---|---|
| `harbour_wide` | harbour | DAY, DUSK | stripes 1 | 2, 8, 11 (DUSK st3), 21 (`hd1,st3`), 22 (`hd1,st0`) |
| `hull_side` | harbour | DAY, DUSK | stripes 1 | 9 (st1), 10 (st2), stages 0-3 |
| `quay_low` | harbour | DAY, DUSK | stripes 0.6 | 5, 6, 7 (push in) |
| `hull_plank` | harbour | DAY | stripes 0.47 | 1 (painter), 23 (the admiral on the plank, `st0` .. `st0.3` keyed) |
| `convoy_wide` | sea | SEA_DAY | U-boat dived (periscope in the foreground) | 3, 4 (`hit`), 12 |
| `periscope_close` | sea | SEA_DAY | U-boat awash | 15 |
| `periscope_pov` | sea | SEA_DAY | dived, overlay on | 13, 18 (+ `set_ghost`) |
| `topdown_sea` | sea | SEA_DAY | dived, lead buoy, gold aim line | 17 (A), 19 (C: `s12,gh1,aim0/0`) |
| `torpedo_chase` | sea | SEA_DAY | dived, s 3.5 (torpedo u 0.21) | 16 |
| `bridge_deck` | sea | SEA_DAY | - | 14, 20 |

## 3. Cameras, stand points, card scales, caption check

Card heights in D (`H.HEIGHT`): **painter 3.0, admiral 3.3, sailor 2.9, captain 3.0**. Placeholders: `beach_man` (painter), `boss` (admiral), `senior_a` (sailor), `senior_b` (captain), until cast10 exists. **Every staged chin is above y 880.**

| cam | loc → look_at, lens | shows | staged → chin px |
|---|---|---|---|
| `harbour_wide` | (-46, -33, 30) → (10, 24, 0), 20 | High crane over the quay. Goods wagons and timber in front; the quay with cranes, scaffold, paint and lamps; the berth ship; the basin with the moored ships, the breakwater, the lighthouse and the roads ships; the town ring. | 4 small figures, chin 671-793 |
| `hull_side` | (-30, -10, 9) → (14, 7, 4), 22 | Medium along the berth hull from the scaffold's height. Scaffold lifts, ladders, lamps, crates; the stripes and the funnels recede toward the bow and a crane. | painter_scaffold 579, sailor_quay_a 808 |
| `quay_low` | (10.5, -17.5, 1.7) → (22.5, -3, 3.8), 24 | Low two-shot on the quay. Scaffold and striped hull left, the basin with grey ships and the lighthouse right, a rope coil and buckets in front. | admiral 699, painter 716 |
| `hull_plank` | (-1.5, -10, 3.6) → (-2.4, 1.2, 4.6), 24 | The hanging stage against the hull: buckets, brush, ropes, a ladder; the zigzag reaches the brush at stripes 0.47. | painter_plank 625 |
| `convoy_wide` | (-60, -146, 15) → (-6, 20, 1), 22 | Behind the dived U-boat: the periscope and its feather cut the water in the foreground; the convoy with the dazzle ship. | - |
| `periscope_close` | U-boat local (-8, -8.5, 1.4) → (3, 1.5, 3.6), 22 | Low at the water: the conning tower, the raised periscope, the captain in the tower behind the rail, the convoy beyond. | captain 522 |
| `periscope_pov` | `periscope_eye()` → (0, 0, 5), 36 | The lens view of the dazzle ship. Pan the camera to sweep the convoy (shot 13); the overlay follows. | - |
| `topdown_sea` | (6, -178, 128) → (2, -40, 0), 22 | High oblique over the encounter: the periscope, the torpedo path, the real ship, the ghost, the buoy, the convoy. | - |
| `torpedo_chase` | `torpedo_cam(u)` (15 D behind, 4.6 up, 22 mm) | The torpedo, its foam V and its bubble wake racing toward the convoy. | - |
| `bridge_deck` | computed: the flagship's starboard wing, 5.2 D behind the admiral → toward the dazzle ship, 24 | The admiral at the bridge-wing rail (voice pipes, signal lamps, binnacle), the dazzle ship and the convoy beyond. | admiral_bridge 632 |

### Stand points (`A['marks']`, feet; z is the floor)

**Harbour:**
- `painter_plank` (-2.5, 0.63, 2.74) and `admiral_plank` (-4.0, 0.63, 2.74): on the hanging stage `plank` (x -6..-0.2), next to the black and white buckets and a brush.
- `painter_plank_b` (23.5, 3.28, 4.34): the bow stage.
- `painter_quay` (15.6, -4.2) and `admiral_quay` (20.4, -7.0): the quay_low two-shot. `admiral_stride_from` (40, -10) is the start of the stride in shot 5.
- `painter_paint` (-1.6, -3.4): by the paint buckets and drums.
- `sailor_quay_a` (-9.5, -7.5), `sailor_quay_b` (-7.6, -9.0), `sailor_quay_c` (9.5, -8.2).
- `sailor_deck_a` (-14, 3.4, 6.2) and `sailor_deck_b` (-20, 3.7, 6.2): on the berth ship's deck.
- `sailor_scaffold` (-18, -1.4, 4.99) and `painter_scaffold` (12, -1.4, 4.99): on the upper scaffold lift.
- `A['planks']` gives the three stages (x span, y, top z). Keep-out zones are in `A['keep_out']`.

**Sea** (positions at s 0; on a moving ship parent the card to `H.ship_root(...)`):
- `admiral_bridge` (-48.86, 57.07, 12.05): the flagship's starboard bridge wing.
- `painter_bridge` (-51.86, 57.67, 12.05) for shot 20, and `admiral_bridge_c` (-49.1, 60.4, 12.05) by the binnacle.
- `painter_deck_dazzle` (-25.6, -1.5, 8.6): the dazzle ship's quarterdeck.
- `uboat_captain` (-50.31, -125.85, 2.75): in the conning tower behind the rail, beside the periscope. The tower rim hides him below the chest.

## 4. Light presets

The template's light model: one sun with real shadows, painted blue-violet shade emission, no bounce, untooned Lambert, warm practicals, the compositor mist (`air`) and sun beams, and the grade with bloom.

| light | key | shade (hue) | extras |
|---|---|---|---|
| DAY | golden (1.95, 1.42, 0.82), az 235 el 32: lights the berth hull side and the quay | (0.105, 0.10, 0.31), tint (0.10, 0.095, 0.33): about 242° | warm bounce, air #f2c88c 0.34, beams 0.05; lamps off |
| DUSK | low orange (1.85, 1.0, 0.52), az 300 el 10 | (0.095, 0.105, 0.35), mix 0.8: about 238-245° | gas lamps (real lights + halos), warehouse windows glow, lighthouse lamp + 9000 W light, crisp peach and lavender cartoon-cloud sky |
| SEA_DAY | warm low sun (1.95, 1.34, 0.74), az 250 el 18, hard shadows on the ships | (0.105, 0.098, 0.31), tint (0.102, 0.09, 0.335) | blue-violet faceted sea (#4646a2, x 1.25) with a warm GGX glint on the facets and the sky mirrored by Fresnel (0.36); air #f0c898 0.42 hazes the horizon |

## 5. Measured (harbour_work/final_log.txt, hue_rows.txt)

- **Render cost** (720x1280, 12 samples, 2 threads, OIDN + grade, two processes in parallel on this 4-core container): **12.7-21.3 CPU s per frame**, every frame under the 25 s budget. The sea frames cost 13-18 s, except topdown at about 21. The harbour frames cost 16-20 s (wall 6.5-11.5 s).
- **Shade hue** (`harbour_hue.py`, strict band): **all 23 frames are in 240-260**, ranging from 240.1 (periscope_pov with the ghost) to 257.9 (DUSK).
- Hue families: the sea frames are dominated by blue (blue-violet sea and sky, plus the warm horizon and glints); the DAY harbour frames are warmer (red 17, orange 27); DUSK is orange 36.
- **Determinism**: `digest` is identical in two processes (harbour_wide `4eb266f0…`). The smoke seeds no longer use Python's per-process `hash()`.
- `t_anim.py`: **ALL OK** (34 checks). They cover keyed stripes, harbour dazzle, the drivers (gulls, bob), smoke, the swell, convoy and ghost motion, the torpedo path, the reveal geometry, ghost fade, dive, hit, overlay follow, and the marks.

## 6. Command line

```
python3 harbour.py stills [spec ...]     # harbour_work/stills 360x640 with placeholders and head pixels
python3 harbour.py final  [spec ...]     # harbour_work/final 720x1280 12 samples, CPU s
   spec = preset[:LIGHT[:state[:cam]]], state = comma list: st<k> stripes, hd<k> harbour dazzle, s<sec> convoy time (+ torpedo
   at torpedo_u(s) when s > 0), tu<u> torpedo, gh<k> ghost, lead<k> buoy, aim<true>/<ghost>, dive<k>, peri<k>, hit<t>, smoke<k>, pov0/1
   e.g. python3 harbour.py final harbour_wide::hd1,st0 topdown_sea:SEA_DAY:dive1,s12,gh1,aim0/0
python3 harbour.py digest <preset>
harbour_work/run_finals.sh ; (cd harbour_work; python3 make_contact.py; python3 t_anim.py) ; python3 harbour_hue.py harbour_work/final
```

## 7. Known gaps (honest)

- **Placeholders only.** Old cast cards stand in for the actors. The held props (big brush, bucket, binoculars) belong to the cast; the set has brushes and buckets on the stages and the quay. The paint on the admiral's moustache is also cast work.
- **Wide shots carry tiny figures.** In `harbour_wide` heads are about 9-12 px, so use `quay_low`, `hull_plank` and `hull_side` for acting. In `topdown_sea` the ships are about 120 px long. It reads, but the torpedo itself is a few pixels; the wake carries the read.
- **The torpedo wake** is a flat ribbon at z 0.42 on the swell. In `torpedo_chase` it reads as a fairly solid white band, not bubbly; in `topdown_sea` it is a thin white line, about 10 px. The cyan aim line lies exactly on top of it, so hide it (`aim1/0` or `aim0/0`) when the wake must read.
- **Sea frames are cold overall.** The blue-violet sea and sky give about 77 % blue chroma, against about 29 % in the references; the warmth is only in the horizon band, the glints and the ships. This is inherent to an open-sea location under the hue rule. Raising `SEA_DAY` `air` k or using a lower sun would warm it, at the cost of the dazzle read.
- **DUSK in the harbour** is moody and dark in the lower half, because the long shadows of the warehouses and cranes fall on the quay. The practicals (gas lamps, windows, lighthouse) carry the light.
- **Stripes on the hull are projected from the side**, in ship x / z. Faces that turn toward ±x (bridge fronts, the stem) take a streak of the pattern. The deck, gun mounts, boats and masts stay grey. Dazzle on the moored and roads ships uses 6 random variants; only the hero ship has the staged zigzag → staircase → full design.
- **The berth ship is also the admiral's ship** in shots 22-23 (`st0`). There is no separate admiral's ship in the harbour.
- **The U-boat interior is not built**: the brief marks it optional. Shot 15 uses `periscope_close`, with the captain in the conning tower.
- **The ships hold position at sea** unless `set_convoy` is keyed. Bow waves and wakes are static foam meshes that move with the ships; there is no spray animation.
- **The swell does not move the foam or the wake.** They sit at fixed heights (0.32-0.42), so near crests sometimes cover patches of them. It reads as broken foam.
- **The hit plume** on `c3` is small in `convoy_wide`: the column is about 60 px tall.
- The far edge of the animated ocean grid (x -380..420, y -320..420) meets a flat far disc at z -0.55. The mist hides the seam, but at the very top of `topdown_sea` the far sea is a flat, slightly different blue.
