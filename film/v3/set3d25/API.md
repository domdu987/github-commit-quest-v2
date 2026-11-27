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
