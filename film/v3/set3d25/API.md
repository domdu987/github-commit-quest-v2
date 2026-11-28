# v3/set3d25/front.py : film 25 set (Britain's first tank, Mark I, Flers-Courcelette 15 Sep 1916, Somme)

bpy 5.x, Cycles CPU, path traced, LIGHT_SPEC v2 look. Nothing older is edited: it imports `set3d24/joseon.py` (NB node helper, MB mesh builder, obox/beam/ell/lump) and `set3d2/tower.py` (card material, `render`).
Units: 1 D = one head (~0.53 m), z up. Textures: ambientCG CC0 (Bricks090, Wood049, Ground049C, Ground048, Ground080, Fabric045, Metal038) in `tex/` (colour 1K + height 512 + roughness 512 jpg).
No text, numbers or labels anywhere.

```python
import sys; sys.path.insert(0, ".../v3/set3d25"); import front as F
A = F.build('cross_hero')          # fresh scene (read_factory_settings): returns anchors(); one location per process
F.render_still(path)               # 720x1280 NATIVE, 64 adaptive samples, OIDN (prefilter Accurate, albedo+normal), then post()
F.render_still(path, 'draft', samples=16, scale=0.4)       # drafts (post still runs)
F.OVR.update(exposure=-0.3, sun_e=5.0)                      # overrides must be set BEFORE build() (S is cleared by build)
```
CLI: `python3 front.py render cross_hero out.png [--draft 0.4] [--samples 64] [--set exposure=-0.3 cam=plan]` writes `out.png` and `out_log.json` (time, settings, card heads, projected anchors).
Debug cameras (`--set cam=`): `plan` (top view), `side`, `back`, `tank` (close-up), `flat`, `flat2`.

## Location `front` (default_world(): all layout constants, edit there)
- Ground: one heightfield mesh (fine cells 0.42 D within x -30..32, y -36..26; coarser outwards to 520 D). `ground_h(X,Y)` / `gh(x,y)` give the exact height (used to seat EVERY prop, card and the tank). Churned noise, 8 shell craters (some with muddy water discs), mud zones, wet attribute (dark glossy mud in craters, trench floor, tank ruts), far attribute (green-gold stripe fields beyond ~60-140 D). Shader: chalk + sand + mud ambientCG mix with bump from the height maps.
- German trench: polyline `S['trench']` (south->north; left of travel = west = British side), 4.7 D deep, 6.6 D wide at the top (batter wall from half-width 2.2 at the floor to 3.3), zig-zag in plan. Per bay: vertical plank revetment (Wood049 + seam bands + bump) or wattle, climbing to the local lip height, posts every 3.4 D and wales, duckboards on rails; west parapet mound (1.5 D) and east parados (0.5 D), sandbag rows on both lips (burlap weave bump), spilled sandbags.
- Barbed wire: picket belts (`S['wire_belts']`, 3 strands + diagonals, twisted wire with barbs) west of the trench and a second belt east of it; pickets and wire inside the tank corridor are snapped / flattened to the ground; loose concertina coils (`S['wire_coils']`, some squashed flat round the tank's tracks).
- Flers: farmhouse + barn (brick walls with ragged tops and window holes, red tile gable roofs with holes and bare rafters), a church-tower stub (24 D), broken walls, rubble heaps, shattered stumps (`S['houses'|'towers'|'walls'|'rubble'|'stumps']`); far poplar line, orchard blobs, thin volumetric haze (density 0.0006, box +-1500: visible only far away).
- Debris: crates, barrels, rock/brick lumps, loose planks, iron pickets, puddles (`S['crates'|'barrels'|'rocks'|'planks'|'stakes'|'puddles']`).
- Sky: world shader with a pastel blue gradient (cream horizon -> #4f90e2) + procedural cumulus (noise on the sky projected onto a plane, white tops, blue-grey bases). Sun: warm (1.0, 0.82, 0.58), energy 5, 1.6 deg disc, elevation 28 deg, aimed per camera by `sun_for_camera` (from the camera's LEFT and a little from the front).
- To add a location (factory yard etc.): write `build_<loc>()` like `build()`, a PRESETS entry with `loc=`, and keep the shared pieces (`make_materials`, `setup_world`, `make_haze`, `setup_render`, `make_camera`, `tommy_card`, `world_at_pixel`).

## `build_tank(name='tank', pos=(0,0,0), yaw=0, pitch=0, roll=0, camo=True, roof_mesh=False, tail=True, tail_angle=0)` -> root empty
Mark I MALE, 15 D long x 4.9 D tall x 8.4 D over the sponsons. Local frame: origin = the FRONT END OF THE STRAIGHT BOTTOM RUN (the point that touches the ground first), x forward, y left, z up. `pos` = world position of that origin, `yaw` degrees CCW from +x, `pitch` degrees (+ = nose up, negative = nose down), `roll` degrees. Parts are children of the root (drive/tilt the root to move it); the steering tail is a child hinge empty `root['tail']` (angle `tail_angle`; `solve_tail(root)` lowers the wheels until the rims touch `gh`).
- Rhomboid outline `TANK_OUT` (x,z) with rounded corners; track plates (0.5 D long, with grouser ribs and bolts) run all round both outlines, mud-streaked steel.
- Hull: riveted steel plates, plate seams from a brick texture on the face UVs (plate 2.6 x 2.0 D); ROWS OF REAL RIVET HEADS (6-sided frusta, r 0.095 D) on both sides of every seam of the side plates, top / slope plates and sponson edges; camouflage = voronoi patches (ochre, olive, brown, khaki) with dark edges, mud on the lower parts (object-space nodes, so it follows the root).
- 2 sponsons (trapezoid bays) with shield plate, bolts, ball mantlet and a 6-pounder barrel (jacket, muzzle ring); cab on the roof front with vision slits, roof hatch, exhaust pipe + silencer, optional anti-grenade wire frame (`roof_mesh=True`), twin spoked wheels on an A-frame tail.
- Crossing a trench: `tank_pose(front_xy, yaw)` returns (pos, pitch) so the bottom run's front end sits on the lip and the rear on the parapet mound (nose down 3-5 deg); `make_tank_crush` flattens / presses the ground under the tracks to the track line (so tracks sit ON earth, bridging only over the trench), and `S['in_tank']` / `in_tank_wide` mark the corridor where sandbags are scattered and wire is crushed.

## Presets (`PRESETS`, `CAMS`, `LOC_PRESETS`)
| preset | shot | camera |
|---|---|---|
| `cross_hero` | gate frame: Mark I nosing over the German trench, yaw -22 deg, front tracks on the east lip, rear on the west parapet; Flers behind; 2 Tommy cards on the east lip | (7.2,-12.4,2.5) -> (2.2,2.0,2.7), 21 mm on a 36 mm sensor (sensor spans the 1280 side: vertical FOV 81 deg, horizontal 53 deg) |
Preset fields: `tank=dict(front=(x,y), yaw=deg)`, `cards=[(name,(x,y) or pixel,'cam')]` (with `pix=1` the pair is a pixel of the 720x1280 frame, resolved to the ground by `world_at_pixel`), `samples`.

## People
`tommy_card(name, mark, face_to, height=3.2, yaw_pose, expr, arm, tilt)`: STAND-IN. The `clerk` puppet (v3/cast, slim/lanky) recoloured khaki (`puppet.CAST['tommy25']`) + a drawn Brodie helmet overlay; there is no film-25 costume yet. Staged like `tower.placeholder_actor`: emission-only to camera rays (`T.mat_card`, no bounce), casts shadows, faces the camera, a soft contact decal on the ground under the feet. `card_report()` prints head top / feet y px (caption band: keep chins above y 880).

## Render + post
`setup_render`: Cycles CPU, 4 threads, 64 samples adaptive (threshold 0.012, min 16), OIDN prefilter Accurate with albedo+normal passes, 6 bounces (diffuse 5, glossy 3, transmission 2), light tree, indirect clamp 8, view transform Standard (exposure -0.25; keeps the cards' colours exact and the highlights crisp), no DOF, no motion blur. `post()`: unsharp r1.1 55 % (threshold 2) + a mild "clarity" unsharp r5 40 % (this is what lifts the 90x160 local contrast from ~0.032 to ~0.040; the light and materials alone give 0.032). No other grade.

## Measured (gate frame, `film25/tools/light_metrics.py`)
see `film25/gate/test_cross_hero_log.json` and the report. ~91 s wall / 360 CPU s per 720x1280 frame at 64 samples on 4 cores.

## Known limits
- Tommy is a recoloured `clerk` (lanky legs) with a flat-drawn Brodie; real costume/pose set still to be made. Cards are upright planes: for a camera much higher than 1.5 m use `tilt`.
- Sandbags / rubble are lumpy ellipsoids; brick bats look like pasted tiles up close (3 D from camera). The trench floor / duckboards are only partly visible in the hero frame (the camera is 3.5 D above the lip; the far wall and a strip of floor show).
- Revetment planes follow the batter wall approximately (0.1 D offset): at bay corners the planks overlap, not mitred. Wire is a modelled strand per span (no simulation).
- Ground is a single heightfield: no overhangs; the tank's right track front hangs over the trench by design (22 deg skew; the front end of the right track only just reaches the lip), the rest of both tracks rests on pressed earth.
- One location per process (build() resets the scene). Haze is a box volume of +-1500 D: keep cameras inside.

# ===== EXTENSION FOR THE FULL FILM (v2 of this set: 33 presets, 6 locations, tank hooks) =====
Entry point: `set25.py` (all locations). `python3 set25.py list` | `python3 set25.py render <preset> out.png [--draft 0.4] [--samples 64] [--set cu=0.4 exposure=-0.3]`; in Python `import set25 as W; W.build('fac_wide'); W.render_still(path)` (one location per process).
`run_finals.sh [preset ...]` renders finals/<preset>.png + metrics. Modules: `front.py` (Front + shared begin/finish/render/post), `tank25.py` (Mark I + hooks), `lib25.py` (materials, props, grass/poppies/bricks dressing), `factory.py`, `trial.py`, `street.py`, `dock.py`, `sky.py`.
New CC0 textures in tex/: grass, cobble, gravel, concrete, dirt (ambientCG Grass001, PavingStones070, Gravel023, Concrete034, Ground037). No text anywhere; the water-tank stencil is a plain silhouette.

## Light recipe (identical for every location, `front.finish`)
Warm key sun 5.0 W (1.0,0.82,0.58), 28 deg from the camera's left / front (factory, street, dock, sky pass an explicit `sun=(azimuth_deg, elev)` that lights the doors / the street axis), the pastel sky + cumulus world, thin far haze 0.0006, Standard view -0.25 EV, Cycles 64 adaptive samples + OIDN, `post()` unsharp r1.1 55 % + clarity r5 40 %. Factory interior adds practical work lamps (8 shaded point lights) and one hidden soft area fill ("practical lights", LIGHT_SPEC 7).

## Producer fixes (FRONT)
1. Source contrast: `dress_front()` adds grass tufts (one triangle per blade, tip/tone attributes), weeds, poppies / daisies / buttercups, red brick bats, broken duckboards, spilled sandbags, iron stakes along every trench lip and crater rim, scattered over the ground and as a dense low carpet in the nearest 14 D of the camera; crates / sandbags (burlap bump) / wire pickets / planks stay.
2. Crossing is staged SIDE-ON: trench dead-ends south of the crossing (`_TP`), near parapet 0.8 D, far parados 1.9 D; `TK.setup_crossing` solves the rest pose of the rhomboid track outline (+ tail wheels) on the ground profile (min centre-of-mass height, no nose dips, smoothed pitch, contact-exact height): nose lifts over the gap (pitch up to ~27 deg), the front horn grips the far lip, the rear stays on the near mound, then it tips level. Corridors (`add_corridor`) flatten the lane across the tracks so the tracks sit level on earth, never as a plank bridge; wire and sandbags in the lane are crushed flat.
3. Colour: green (ground shader `green` attribute: lawn texture at lips, crater rims, patches), tufts and weeds, red brick, poppies, poplars / orchards on the whole horizon ring (`far_ring`), green-gold fields beyond 70 D, blue sky.

## Tank hooks (`tank25.py`; `H = front.build_tank(name, mud=1.0)` or `TK.build_tank(...)` returns TankH: dict + attributes, `H.root` = root empty)
| call | what |
|---|---|
| `TK.set_build(H, {'chassis':1,'plates':.5,'rivets':.3,'tracks':0,'sponsons':0,'guns':0}, frame=None)` | build stages, level 0 (hidden) .. 1 (locked). chassis = bare girder frame + engine + tail; plates drop from above with a swing; rivets punch in chunk by chunk along the hull; tracks drop round the hull; sponsons slide in sideways; guns slide in along the barrel. With `frame=` it keys location / rotation / visibility |
| `TK.set_drive(H, dist, frame=None)` | 2x52 individual track links (objects sharing a mesh) scroll round the loop with distance travelled; tail wheels roll |
| `TK.setup_crossing(H, (x0,y0), yaw, s_a, s_b)` + `TK.set_crossing(H, u, frame=None)` | u 0..1: approach, nose lift, grip, pull across, level on the far side; also drives the tracks. `TK.crossing_pose(H,u)` returns the pose |
| `TK.pose_on_ground(H, x, y, yaw)` | rest the tank on the world heightfield (tilted in a crater, standing on a lane) |
| `TK.set_state(H, 'stuck'|'smoking'|'tilted'|'normal', level, frame)` | stuck = root sunk 1.15 D (+ the preset's `('mud', x, y, yaw)` heaps), smoking = kit volume smoke column from the engine, normal resets; 'tilted' = `pose_on_ground` in a crater (preset `front_halt`) |
| `TK.set_stencil(H, on, frame)` | plain water-tank silhouette decal on both hull sides |
| `TK.set_sparks(H, t_sec, frame)` | bullet pings: 16 emissive stars staggered 0.045 s, each 0.16 s, bloodless; t < 0 hides |
| `TK.tank_silhouette(mb, centre, X, normal, Z, scale, mat, mat_dark)` | the same silhouette for crates / walls |
Other hooks: `factory.set_dial(deg, frame)` (weighbridge needle, no digits), `factory.shipping_crate(...)` + `factory.set_crate(C, open 0..1, frame)` (lid swings up, front wall falls), `sky.build_plane()` + `sky.set_plane(H, t, frame)` (biplane on its own empty flies a straight path, prop spins).

## Locations and presets (see METRICS.md for the table with measured values)
FACTORY (factory.py): brick shed 52 x 52 x 14 D, arched windows, sliding doors open, tin roof with skylights, cobbled yard, gantry crane (rails, bridge, trolley, chain, hook), trestles, weighbridge + dial, benches, tool racks, coal, 2 chimneys, steel plate stacks, rivet buckets, water barrels / tanks, shipping crate. TRIAL (trial.py): lawn park, test trench, oaks, marquee tents, flags (plain colours), staff cars. FRONT (front.py): see above + `mg_nest`, `op_post`, `bucket_at`, `mud_heaps`. STREET (street.py): 14 brick houses per side (shop fronts, awnings, damaged roofs), cobbles, church with tower + spire, trees, rubble. DOCK (dock.py): quay, cargo ship, crate on deck, crane, gulls, French coast. SKY (sky.py): biplane over the street rooftops.

## Final grade (director directive, `front.grade()`, last step of `post()`)
After the sharpen / clarity steps: per image (1) levels p1 -> 0.035, p99 -> 0.925 with a tanh soft knee above 0.85, (2) luma gamma to mean 0.51 (clamped 0.75-1.35), (3) saturation toward 0.31 (factor clamped 0.7-1.3), iterated 3x. Switch off with `F.OVR['grade'] = 0`. Per-preset `tune=dict(cloud_k=, haze=, green_k=, grass_val=)` and `fill=` (hidden bounce light) are source-side dials. Tools: `run_finals.sh`, `tn.sh` (24-sample full-res tuning render), `regrade.py`, `contact.py`.

# ===== SHOT PLAN V2 ADDITIONS (18 more presets, new hooks, colour pipeline) =====
## New hooks
| call | what |
|---|---|
| `factory.set_model_tank(u, frame=None)` | CHART TABLE (`build_chart`, preset `fac_chart`): a small model Mark I (root scale 0.11, full track / tail hooks) slides up to, over and across the groove cut into the green baize (u 0..1: nose lifts onto the far parapet, tips over, off the far side; links scroll) |
| `factory.set_doors(u, frame=None)` | the shed's two sliding doors, 0 = open (parked either side), 1 = shut, eased (`fac_doors`) |
| `tank25.set_steam(H, level, frame=None)` | radiator steam like a leaky kettle at the rear top (soft white puff, grows with level) + a water dribble down the hull; no damage |
| hull tap + hatch | geometry on both hull sides (brass tap with a spout, drain, hinged hatch plate with handle and bolts) at local x = -5, part of the `plates` stage: the drink / watering-can gags |
| `lib25.water_tank_big(mb, c, r, h)` | a REAL riveted water tank on four legs with a ladder, domed lid and a tap at the bottom (`dock_watertank`) |
| `front.close_cam(pos, face_deg, dist, lens, zc, ground, look_dz)` | waist-up camera for a ~3.2 D puppet card: `dist` D from the mark, level at chest height; the mark (position, facing) is returned in `anchors()['mark']`. Close presets render NO puppet |
| `P['cam']` may be a function of the scene state (`cross_close_idler`) | camera placed from the posed tank |
| `front.grade()` | now also: partial gray-world white balance in Lab (a*, b* toward +1.5, clamped +-20), HSV saturation shaping (accents lifted: S p98 >= 0.87, mean S 0.475), warm-up of the greens until >= 43 % of coloured pixels are warm, luma gamma 0.6-1.7, never clips a channel (HSV value untouched), faces / near-white masked |

## New presets (render with `set25.py render <name> out.png`)
`fac_chart` (3/4 top-down on the chart table), `fac_chart_face` (engineer behind the table, mark), `fac_doors` (doors shut, from the yard), `fac_close_hull`, `fac_close_rivet`, `fac_close_engineer`, `trial_close_general`, `camp_close_tank` (tank hull side behind the mark), `dock_watertank`, `dock_deck` (crate on a ship's deck at sea, gulls, white cliffs + poplars ahead), `front_close_britishtrench`, `front_close_germantrench`, `op_close_general`, `cross_close_idler` (links round the front idler against the sky), `cross_close_lip` (track gripping the far lip, clods), `sky_close_cockpit`, `street_close_tail` (tank rear + tail wheels at waist height), `street_high` (pilot's view down the street).
Clouds: every preset has its own cloud seed (offset, scale, aspect) and two noise scales (big and small structures), so no two shots show the same clouds and sizes / spacing vary.
