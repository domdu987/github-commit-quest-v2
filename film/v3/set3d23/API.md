# v3/set3d23 : film 23 set ("ไอ้กองทัพลูกโป่ง", the Ghost Army) — API (bpy 5.3, Cycles CPU, 720x1280)

Grown from the approved style board (board/: board_1..3, NOTES.md, QA_ART.md). Four locations in one world frame, 19 shot cameras with eased keyed moves,
stand marks for every character of every shot, setters render workers key per frame, ground-snap + contact-shadow helpers, placeholder silhouette cards.
**No depth of field anywhere** (`make_camera` forces it off). No haze layer over the frame; lantern halos are small (0.75-0.9 D).

## Files
- `ghost.py` core: light presets, the shared toon material `mat_g`, `build`, locations + world origins, `ground_snap` / `contact_shadow` / `ground_z`,
  cameras (`shot_camera`, `key_camera`), `marks`, placeholder cards (`ph_card`, `place_cards`, `remove_placeholders`), all setters, `quality`, CLI.
- `ghost_fields.py`, `ghost_lane.py`, `ghost_camp.py`, `ghost_rhine.py`: the four locations. `ghost_scenes.py`: shared scenery (hedgerows, poplars, houses,
  church, cows, tents, jeep, lanterns, `outer_ring`) + the old board compositions. `ghost_props.py`: rubber M4 (shape-keyed), trucks + horn, gun, nets,
  crates, sign, pump, bicycle, wall, cards. `ghost_fg.py`: foreground props. `ghost_tex.py` + `ghost_tex2.py`: painted textures (cache `tex_ghost/`, gitignored;
  bump `TEX_V` or the job's `v` after editing a painter). `ghost_shots.py` (move model, pose, marks) + `ghost_shot_table.py` (the 19 rows + `ACTION`, the
  per-shot draft actions). `ghost_sheet.py` (drafts, sheet, finals, numbers), `ghost_ground.py` (ground sweep), `ghost_hue.py` (colour numbers), `board.py`.
- Outputs: `set_sheet.jpg` (19 shots x first / mid / last, 360x640, 6 samples, cyan line at y 880), `set_finals.jpg` + `set_work/final/*.png` (S01 S07 S09
  S12 S14 S17 first frames, 720x1280, 12 samples), `set_work/numbers.json`, `NOTES.md`, `GROUND_SET.md` + `set_work/ground/`.

## Build, cameras, CLI
```python
import sys; sys.path.insert(0, 'film/v3/set3d23')
import ghost as GH
A = GH.build('S07')                   # = GH.build('LANE', 'S07'): the shot's light, fg prop, mid state, placeholder cards, camera at t=0
A = GH.build('S07', cards=False)      # no placeholders (render workers put the cast cards in)
A = GH.build('RHINE')                 # a bare location (its default camera, no shot dressing)
f0, f1 = GH.key_camera('S07', f0=1)   # keys the whole move: one LINEAR key per frame, round(planned x 1.25 x 30) frames, sets frame_start/end
GH.shot_camera('S07', 0.5)            # or pose the camera at t (0 start, 1 planned end, 1.25 end of tail)
GH.quality(None, 'final')             # render settings (720x1280, 12 samples, OIDN, 4 threads, light tree at night, RHINE: one glossy bounce)
GH.T.render('/path/f0001.png')
```
`A` = dict(location, shot, light, key_dir, origin, marks (world, see below), anchors (named set points, world), tanks (names)).
CLI: `python3 ghost.py still S07@0.5 [preview|final] [out]`, `frames S07 [t,t] [dir] [scale] [spp]`, `sheet`, `finals`, `ground`.
Build takes 3-9 s, a 720x1280 12-sample frame about 4-9 s wall on 4 threads (NOTES.md).

## World frame (1 D = one head; soldier 3.0 D, tank ~11 D long)
| location | light | origin (world) | what is where (local frame of the location) |
|---|---|---|---|
| FIELDS | DAWN | (0, 0, 0) | bocage valley, painted patchwork + 3D hedges/poplars; far patchwork ring to +-1900 D; the column `col0..col8` (+ `jeep_tow`) on the lane heading SSW, lead tank col0 at (-18, -20); farm (-30, 92) with netted tanks `park0..2`, trucks, gun, tents, jeeps, hay, cows; river y ~260; village + church y ~340 |
| LANE | MORNING / DAY | (-700, -260, 0) | the farm lane 700 D west of the column (inside the FIELDS far ring): see ghost_lane.py docstring — hero tank `tank_hero` (-1.1, 16.9), `tank_paint` (12.5, 25), decoy field `field0..11` + flat sheets `flat0..2` (x -26..-62), sign (-14.5, 27.4), `jeep` path up the lane to (8.6, 4.2), `crate_chalk` (10.6, 1.4), lift `tank_lift` (-5, -30) [built only for S12/S13 and the bare location], ending seat (11.2, 9.4) + pile (14.8, 12.2), low hedge on the east verge y -114..-32 (cyclists) |
| CAMP | NIGHT | (760, -180, 0) | tank rows `row0..16` (three rows, broadside, moon rim), `sound_truck` (-7.9, -9.2) + desk with `record`, radio tent (2.4, -5.3), `truck_paint` (13.5, -4.2) with the fresh badge, jeep, 7 lantern poles, crates, cables |
| RHINE | NIGHT_R / PREDAWN (S18) | (0, 9000, 0) | river along +y (centre x = -2 + 6 sin(0.004 y), 76 D wide, water z -0.6); decoy field `decoy0..41` (x -62..-140, y -150..-20), 24 lanterns; `sound_truck_r` (-52, -70) + desk + `record`; radio tent (-52, -36); 30th / 79th INF DIV crates (-57, -60); unloading trucks (-78, -177) / (-93, -172); RHINE sign (-50, -179); convoy park y -205..-246; German OP (60, -60): sandbags, hut, telescope; pontoon bridge y 380; boats `boat0..4` |

Light presets: DAWN (low gold sun from the west-north-west, blue dawn sky), MORNING (board 2), DAY (sun south-west, LANE S11-S19), NIGHT (moon key, warm lamps),
NIGHT_R (the Rhine moon in the south-east), PREDAWN (blue, a pale band low in the east, lamps dimmed). Shade is a painted blue-violet replacement colour (shade_cut).

## Camera move model (ghost_shots.py)
Every move runs over **planned length x 1.25** (t = 0 .. 1.25; t = 1 is the planned end) and is eased: s = 0.6 sine-in-out + 0.4 linear of t/1.25, so it
keeps moving into the tail and never holds near-still. Moves: `push` (fraction of the subject distance per second, exponential: 0.06-0.10), `slide`
(px/s at 720 wide, measured at `sdist` D), `rise`, `zoom_rate` (lens push, S17), `end` (crane / reveal to an end pose; the tail extrapolates on the same
eased line), `path` (BIGZOOM key poses, Catmull-Rom with the subject distance interpolated in log space: S01 1693 D up -> 15 D medium on the lead tank;
S12 4.7 D on the cyclists' faces -> 25 D wide on the lift). No random shake anywhere. `GH.key_camera` keys location, rotation and lens per frame (LINEAR).
Foreground props (`fg`): real grounded props placed ('cam', dist, lateral) from the start camera, 1.5-2.2 D from the lens: 12 shots have one (S02 S03 S07 S08 S09 S10 S13 S15 S16 S17 S18 S19), S05 starts on the sign, S06 shoots over the crew, S11 through the low hedge; S01 S04 S12 S14 are high / BIGZOOM moves (S01 sweeps past two poplars).

## Marks
`GH.marks(shot)` -> {role: [(x, y, z, yaw_deg, extra)]} in WORLD coordinates at the built state; z is the surface under the mark (ray cast).
`extra`: `ph` / `pose` (the placeholder silhouette), `parent` (a mover: the card must be parented to it — jeep seats, boats, the lead tank's deck; the mark
in ghost_shot_table is in the parent's local frame), `airborne`. yaw turns a card that faces -y at yaw 0 toward the START camera.
Heights: soldier/major 3.0 D (+ hat), cyclist with bike 4.0 D card, dog 1.8 D. Heads stay above y 880 at first / mid / last (sheet JSON `heads`).

## Setters (frame=None: set now; frame=n: set and key that frame)
| setter | what |
|---|---|
| `set_inflate(tank, v)` | 0 flat rubber sheet .. 1 full (shape keys i0/i25/i50/i75 + basis; every tank has its own mesh) |
| `set_sag(tank, v)` / `set_barrel(tank, deg)` | barrel limp 0..1 / elevation (deg; field tanks 30 = 'pointing at the sky') |
| `set_deflate(v)` | S03: tank_hero pricked: inflate 1 -> 0.18, barrel droops onto the pricker's helmet (mark `pricker`) |
| `set_lift(h)` | S12/S13: tank_lift 0 ground .. 1 overhead (belly 3.55 D on the lifters' hands); `airborne` flag; blob stays on the grass |
| `set_jeep(s)` | LANE: 0 hidden (away) .. 0.78 up the lane .. 1 parked; height follows the ground (re-snapped) |
| `set_column(d)` | FIELDS: the 9 tanks + tow jeep move d D along the lane (S01 draft: 4 D over the planned length) |
| `set_record(deg)` / `spin_record(f0, f1, rpm=78)` | CAMP / RHINE gramophone record `record` |
| `flicker(frame, k=1)` | every lamp's energy keyed with a deterministic flicker (call per frame) |
| `set_boats(t)` | RHINE: boats 0 west bank .. 1 east bank, staggered; cards parented to a boat ride along |
| `set_pile(k)` | LANE: balloon pile 0 .. 1 (core grows, 120 balloons appear bottom-up and sit on it; strays at his feet from 0.5) |
| `set_loose_balloon(t)` | S19 last word: the escaping balloon loops up-left (airborne), hidden at 1 |
| `set_chalk(k)` | S08: 'BALLOON ARMY' chalk on `crate_chalk` 0 .. 1 |
| `animate(setter, f0, f1, v0, v1)` | eased keys of any one-value setter, e.g. `GH.animate(GH.set_deflate, 10, 60, 0, 1)`; for per-tank setters wrap them (see gotchas) |
| `apply_state('deflate=1,jeep=1,lift=0.5,pile=0.8,inflate:field3=0.4')` | the string form the shot table uses (un-keyed) |

## Helpers: nothing floats
- `GH.ground_snap(ob, sink=0.012)`: ray casts from the object's lowest vertices (a card: its lowest visible alpha row) to the first surface below (fine
  dressing hidden: `dress_hidden()`), moves it so it sits 1.2 cm in. Every prop group, tank, truck and card is snapped by `build`.
- `GH.contact_shadow(ob, radius, depth=None)`: soft dark blob `<ob>_contact` (gc_role shadow) on the ground, following the object's XY + yaw.
- `GH.ground_z(x, y)`: world height of the real surface. `Bk.prop(name, shadow_r, main=)`: wrap a builder so its banks become ONE prop object (snapped,
  blob, checked) — use it for any new prop. Movers keep `zoff` and are re-snapped by their setters.
- Check: `python3 ghost.py ground` (film/v3/tools/ground_check.py, results in GROUND_SET.md).

## Replacing the placeholders with the cast23 cards
1. `A = GH.build('S13', cards=False)` (or `GH.remove_placeholders()` after a build with cards).
2. For every role in `GH.marks('S13')`: make the cast card (stage/actors or your sprite card) with its feet at (x, y, z), yaw as given (or face the
   camera per frame), name it `*_card` or set `ob['gc_role'] = 'card'`; if `extra['parent']` is set, parent it (`ob.parent = bpy.data.objects[parent]`,
   identity parent-inverse, location = parent.matrix_world.inverted() @ mark, scale 1/parent scale: col0 is scaled 1.2).
3. `GH.ground_snap(card)` once (cards are emission-only, `no_bounce`), `GH.contact_shadow(card, 0.9, 0.42)`.
4. Key the setters the shot needs (see the row's `note` and `ghost_shot_table.ACTION`), `GH.key_camera(shot, f0)`, `GH.flicker(f)` per frame at night.
5. Run ground_check on your take (`--every 10`); lift-tank lifters and boat riders are expected to touch their prop, the lifted tank is airborne.

## Gotchas
- One build per process is the safe pattern (build clears the scene, actions and SET/LIGHTS/CARDS collections). Render one frame at a time, 4 threads.
- Setters on a keyed property: once you key it, un-keyed calls are overridden by the keys on the next frame change — key every frame you render.
- `set_jeep(0)` hides the jeep (and the Major's / driver's cards parented to it). The default LANE state is jeep away, pile 0, chalk 0.
- `tank_lift` exists only in S12/S13 builds (and the bare LANE build) so it never blocks the lane in other shots.
- Tank names differ per location: `GH.tanks()` lists them. `set_inflate` needs the tank NAME as its first argument (`animate` passes the value first:
  use `lambda v, frame=None: GH.set_inflate('field3', v, frame)`).
- RHINE renders with one glossy bounce (the river reflects lanterns / decoys / moon): call `GH.quality()` after any `setup_render` of your own, or the river turns matte.
- The sky dome follows the camera via a frame handler; FIELDS uses a 2700 D dome (the S01 start is 1693 D up), clip end 3000.
- The ground textures are painted per location; the far ring (fields_far) is shared, so the horizon around LANE / CAMP is the same valley as FIELDS.
- Placeholder cards are FLAT SILHOUETTES (one colour per role: olive soldiers, khaki Major with cigar, blue/brown cyclists with bikes, grey Germans,
  brown dog). They show staging and head rows only.

## Shots, cameras and marks (generated from ghost_shot_table.py; local coordinates of each location; world = local + origin)
### S01  (FIELDS, DAWN, 4.00 s planned -> 150 frames at x1.25, trans per plan)
- BIGZOOM 1: extreme wide high over the patchwork, descend + push along the lane past two poplars, end medium on the lead tank
- camera (local) start (-3.0, -118.0, 1693.0) -> (-3.0, 30.0, 0.0) lens 24; planned end (-32.5, -31.0, 5.6) -> (-19.0, -20.5, 3.2) lens 24.0; tail end (-30.2, -29.3, 5.2); move: BIGZOOM path (4 key poses)
- state at build: `column=0`
  - rider (1): (-2.9, 0.4, z 3.30) soldier/wave on col0
  - walkers (2): (-23.6, -17.0) soldier/wave; (-19.0, -4.0) soldier/stand
### S02  (LANE, MORNING, 4.40 s planned -> 165 frames at x1.25, trans per plan)
- LOW hero angle along the row of tanks, barrels up; side-tracking slide
- camera (local) start (-20.2, -47.5, 1.2) -> (-25.5, -19.0, 4.0) lens 22; planned end (-18.2, -39.8, 1.9) -> (-22.2, -18.4, 4.0) lens 22.0; tail end (-17.8, -38.8, 2.0); move: push 0.06, slide 40, sdist 14.0
- foreground prop: ('crate', ('cam', 1.9, -0.9), 30, 0.8, 'crate_b')
  - polisher (1): (-18.6, -30.4) soldier/polish
  - saluter (1): (-19.4, -21.0) soldier/salute
  - soldier (2): (-20.0, -4.0) soldier/stand; (-34.0, -18.0) soldier/carry
### S03  (LANE, MORNING, 3.50 s planned -> 131 frames at x1.25, trans per plan)
- medium, quick push-in on the pin; the tank deflates, the barrel droops onto his helmet
- camera (local) start (8.8, 1.2, 2.7) -> (3.0, 12.8, 2.3) lens 26; planned end (5.6, 4.1, 2.6) -> (1.6, 12.1, 2.3) lens 26.0; tail end (5.1, 4.5, 2.6); move: push 0.1, slide -30
- foreground prop: ('jerrycan', ('cam', 1.6, 0.75), 60, 1.0)
- state at build: `deflate=0.5`
  - pricker (1): (4.4, 11.2) soldier/point
  - pumpman (1): (-9.0, 20.0) pumpman/pump
  - clipboard (1): (-3.4, 10.2) clipboard/stand
### S04  (LANE, MORNING, 4.30 s planned -> 161 frames at x1.25, trans per plan)
- high crane down over the work area: painter, sound man, designer, pump man
- camera (local) start (3.0, -12.0, 23.0) -> (3.0, 17.0, 0.0) lens 22; planned end (3.5, -2.0, 12.5) -> (3.0, 18.0, 0.5) lens 22.0; tail end (3.6, -0.4, 10.8); move: to an end pose
- state at build: `jeep=0`
  - pumpman (1): (-9.0, 20.0) pumpman/pump
  - clipboard (1): (0.2, 8.4) clipboard/stand
  - soundman (1): (4.6, 13.0) soundman/carry
  - painter (1): (9.4, 21.4) painter/polish
### S05  (LANE, MORNING, 4.35 s planned -> 163 frames at x1.25, trans per plan)
- pull back and up past the 23rd HQ SPECIAL TROOPS sign: a dozen men vs a field filling with rubber tanks
- camera (local) start (-10.5, 20.0, 4.0) -> (-15.0, 27.2, 4.4) lens 24; planned end (2.0, -4.0, 15.0) -> (-34.0, 6.0, 0.0) lens 22.0; tail end (4.0, -7.8, 16.8); move: to an end pose
  - crew (12): (-22.4, -35.2) soldier/pump; (-22.4, -16.7) soldier/carry; (-22.4, 1.8) soldier/stand; (-22.4, 20.3) soldier/pump; (-38.4, -29.2) soldier/carry; (-38.4, -10.7) soldier/stand; (-38.4, 7.8) soldier/pump; (-38.4, 26.3) soldier/carry; (-54.4, -35.2) soldier/stand; (-54.4, -16.7) soldier/pump; (-54.4, 1.8) soldier/carry; (-54.4, 20.3) soldier/stand
### S06  (LANE, MORNING, 2.60 s planned -> 98 frames at x1.25, trans per plan)
- medium-wide OTS from behind the crew toward the jeep (set_jeep 0.55 -> 1)
- camera (local) start (1.6, 16.4, 4.6) -> (6.4, 1.0, 0.6) lens 24; planned end (2.5, 16.7, 4.6) -> (7.3, 1.3, 0.6) lens 29.2; tail end (2.7, 16.7, 4.6); move: zoom_rate 0.07, slide -25, sdist 12.0
- state at build: `jeep=0.8,deflate=1`
  - crew (2): (5.1, 10.2) clipboard/stand; (2.4, 7.8) soldier/stand
  - major (1): (-0.3, -0.8, z 2.10) major/sit on jeep
  - driver (1): (-0.3, 0.8, z 2.10) driver/sit on jeep
### S07  (LANE, MORNING, 4.20 s planned -> 158 frames at x1.25, trans per plan)
- LOW angle on the Major, slow push, crew small behind; he points at the deflated tank and talks
- camera (local) start (2.2, -3.8, 1.0) -> (4.8, 8.6, 3.7) lens 24; planned end (0.9, -0.0, 1.8) -> (2.8, 9.0, 3.7) lens 24.0; tail end (0.7, 0.5, 1.9); move: push 0.07, slide -30
- foreground prop: ('toolbox', ('cam', 1.5, -0.7), 30, 1.3)
- state at build: `jeep=1,deflate=1`
  - major (1): (5.6, 6.0) major/point
  - crew (3): (-2.6, 11.0) soldier/stand; (1.6, 12.2) clipboard/stand; (-6.0, 13.4) pumpman/stand
  - driver (1): (-0.3, 0.8, z 2.10) driver/sit on jeep
### S08  (LANE, MORNING, 2.80 s planned -> 105 frames at x1.25, trans per plan)
- wide high, pull back; the driver chalks BALLOON ARMY on a crate; crew droop
- camera (local) start (11.8, -8.6, 8.0) -> (6.6, 5.4, 1.6) lens 22; planned end (14.5, -11.9, 12.2) -> (7.9, 5.9, 2.3) lens 22.0; tail end (15.0, -12.6, 12.9); move: push -0.08, slide 30, rise 0.8, sdist 12.0
- foreground prop: ('post', ('cam', 2.0, 1.1), 0, 1.4)
- state at build: `jeep=1,deflate=1,chalk=0.6`
  - driver (1): (12.6, 0.6) driver/point
  - major (1): (6.4, 5.4) major/stand
  - crew (3): (-0.6, 9.6) soldier/stand; (2.2, 10.8) clipboard/stand; (-3.2, 12.0) pumpman/stand
### S11  (LANE, DAY, 3.10 s planned -> 116 frames at x1.25, trans per plan)
- side tracking with the two cyclists along the hedgerow (foreground hedge); they ride 4 D/s
- camera (local) start (7.4, -88.0, 3.0) -> (-6.4, -81.0, 2.5) lens 24; planned end (7.6, -75.6, 3.0) -> (-6.2, -68.6, 2.5) lens 24.0; tail end (7.6, -73.6, 3.0); move: to an end pose
  - cyclist_a (1): (-7.6, -83.0) cyclist_a/ride
  - cyclist_b (1): (-6.0, -86.0) cyclist_b/ride
### S12  (LANE, DAY, 2.80 s planned -> 105 frames at x1.25, trans per plan)
- BIGZOOM 2 / reveal: from close on the cyclists pull back and up wide: 4 soldiers lift the tank over their heads (set_lift 1); cyclists brake
- camera (local) start (-4.0, -40.2, 3.5) -> (-6.0, -45.6, 3.2) lens 24; planned end (5.5, -59.0, 7.4) -> (-6.0, -37.0, 3.8) lens 22.0; tail end (3.5, -55.1, 6.8); move: BIGZOOM path (3 key poses)
- state at build: `lift=1`
  - cyclist_a (1): (-7.0, -45.2) cyclist_a/brake
  - cyclist_b (1): (-4.6, -47.6) cyclist_b/brake
  - lifters (4): (-7.0, -27.4) soldier/lift; (-6.9, -32.7) soldier/lift; (-3.1, -27.2) soldier/lift; (-3.0, -32.5) soldier/lift
### S13  (LANE, DAY, 4.50 s planned -> 169 frames at x1.25, trans per plan)
- medium two-shot in depth; quick push on the soldier with the tank overhead; one cyclist falls off gently
- camera (local) start (-11.8, -55.0, 3.4) -> (-5.6, -33.5, 4.4) lens 26; planned end (-10.6, -55.3, 3.4) -> (-4.4, -33.8, 4.4) lens 38.3; tail end (-10.4, -55.4, 3.4); move: zoom_rate 0.08, slide 20, sdist 12.0
- foreground prop: ('hay', ('cam', 2.2, -1.3), 40, 0.7)
- state at build: `lift=1`
  - cyclist_a (1): (-12.5, -46.3) cyclist_a/stand
  - cyclist_b (1): (-11.4, -47.8) cyclist_b/stand
  - lifters (4): (-7.0, -27.4) soldier/lift; (-6.9, -32.7) soldier/lift; (-3.1, -27.2) soldier/lift; (-3.0, -32.5) soldier/lift
### S19  (LANE, DAY, 4.30 s planned -> 161 frames at x1.25, trans per plan)
- wide -> medium push, ends on the Major; huge balloon pile (set_pile); last balloon escapes (set_loose_balloon)
- camera (local) start (13.6, -7.0, 5.6) -> (12.4, 9.8, 2.4) lens 22; planned end (10.6, -0.9, 4.4) -> (9.9, 9.6, 2.4) lens 22.0; tail end (10.2, -0.2, 4.3); move: push 0.1, slide -25
- foreground prop: ('crate', ('cam', 1.8, 1.0), 20, 0.8, 'crate_a')
- state at build: `pile=0.85,jeep=0`
  - major (1): (11.0, 8.6) major/blow
  - crew (3): (6.2, 11.8) soldier/wave; (8.0, 15.6) soldier/stand; (17.8, 6.2) clipboard/stand
### S09  (CAMP, NIGHT, 4.80 s planned -> 180 frames at x1.25, trans per plan)
- crane from the tank rows to the sound truck, push toward the horn; sound man flips switches, record spins (spin_record); moon rim on the tanks
- camera (local) start (-24.0, -2.0, 15.0) -> (-6.0, 22.0, 2.0) lens 22; planned end (3.0, -24.0, 4.2) -> (-7.6, -9.8, 4.8) lens 22.0; tail end (1.2, -21.7, 4.3); move: BIGZOOM path (3 key poses)
- foreground prop: ('lantern', ('camend', 2.0, 1.2), 0, 1.6)
  - soundman (1): (-1.9, -16.6) soundman/point
  - guard (2): (-10.6, -1.6) soldier/stand; (4.0, 2.0) soldier/carry
### S10  (CAMP, NIGHT, 4.70 s planned -> 176 frames at x1.25, trans per plan)
- side tracking through the radio tent and out to a truck; radio man chatters into the handset; painter stencils a division badge on a bumper
- camera (local) start (0.2, -18.2, 3.0) -> (1.6, -4.6, 2.4) lens 24; planned end (7.6, -19.6, 3.0) -> (10.2, -8.0, 2.2) lens 24.0; tail end (8.8, -19.8, 3.0); move: to an end pose
- foreground prop: ('crate', ('cam', 1.9, -1.0), 10, 0.8, 'crate_c')
  - radioman (1): (1.2, -4.6) radioman/sit
  - painter (1): (8.4, -9.8) painter/polish
  - soldier (1): (4.8, -9.0) soldier/carry
### S14  (RHINE, NIGHT_R, 4.00 s planned -> 150 frames at x1.25, trans per plan)
- extreme wide high over the river, slow descend; caption-safe RHINE sign on the bank; soldiers unload crates from trucks
- camera (local) start (-128.0, -268.0, 74.0) -> (-30.0, -96.0, -2.0) lens 22; planned end (-94.0, -226.0, 26.0) -> (-38.0, -132.0, 0.0) lens 22.0; tail end (-88.6, -219.3, 18.4); move: to an end pose
  - unloaders (4): (-73.6, -181.4) soldier/carry; (-75.8, -183.2) soldier/carry; (-88.0, -177.2) soldier/carry; (-86.2, -179.6) soldier/stand
### S15  (RHINE, NIGHT_R, 3.30 s planned -> 124 frames at x1.25, trans per plan)
- crane up over rows inflating in lantern light (set_inflate decoyN staggered); pump crews
- camera (local) start (-52.0, -162.0, 2.6) -> (-84.0, -112.0, 2.8) lens 22; planned end (-40.0, -152.0, 18.0) -> (-92.0, -96.0, 0.0) lens 22.0; tail end (-38.1, -150.4, 20.5); move: to an end pose
- foreground prop: ('reeds', ('cam', 1.7, 0.9), 0, 0.9)
  - pumpcrew (5): (-58.8, -131.4) pumpman/pump; (-72.6, -119.0) pumpman/pump; (-85.4, -128.4) pumpman/pump; (-99.0, -112.0) soldier/stand; (-111.6, -125.0) soldier/carry
### S16  (RHINE, NIGHT_R, 3.30 s planned -> 124 frames at x1.25, trans per plan)
- push along the sound truck and the radio tent; 30th / 79th INF DIV crates; sound truck booming (spin_record), radio chatter
- camera (local) start (-45.5, -104.0, 4.5) -> (-60.0, -58.0, 2.5) lens 22; planned end (-46.1, -93.0, 4.1) -> (-57.4, -57.2, 2.5) lens 22.0; tail end (-46.1, -91.5, 4.0); move: push 0.07, slide 30, sdist 20.0
- foreground prop: ('lantern', ('cam', 1.9, -1.2), 0, 0.8)
  - soundman (1): (-55.0, -80.6) soundman/point
  - radioman (1): (-64.6, -50.0) radioman/sit
  - soldier (1): (-53.0, -55.0) soldier/carry
### S17  (RHINE, NIGHT_R, 2.60 s planned -> 98 frames at x1.25, trans per plan)
- OTS from behind the German observers (binoculars, a telescope) across the river to the glowing decoy field; one drops his sausage
- camera (local) start (69.0, -53.6, 3.8) -> (-90.0, -104.0, 0.5) lens 24; planned end (69.2, -54.4, 3.8) -> (-89.8, -104.8, 0.5) lens 30.0; tail end (69.3, -54.5, 3.8); move: zoom_rate 0.08, slide -25, sdist 10.0
- foreground prop: ('sandbags', ('cam', 1.8, -0.9), 90, 0.9, 3)
  - observers (3): (58.4, -59.0) german/look; (59.6, -61.6) german/point; (61.2, -58.6) german/stand
### S18  (RHINE, PREDAWN, 2.50 s planned -> 94 frames at x1.25, trans per plan)
- wide, slow pan along the assault boats / pontoon crossing in blue pre-dawn shadow (set_boats 0.3 -> 0.6)
- camera (local) start (-37.5, 334.0, 3.2) -> (-2.0, 350.0, -0.2) lens 22; planned end (-36.5, 337.0, 3.1) -> (16.0, 360.0, -0.2) lens 24.0; tail end (-36.3, 337.5, 3.1); move: to an end pose
- foreground prop: ('reeds', ('cam', 1.8, -1.0), 0, 1.0)
  - boat0 (3): (-1.5, 0.0, z -0.76) soldier/paddle on boat0; (0.0, 0.0, z -0.76) soldier/paddle on boat0; (1.3, 0.0, z -0.76) soldier/paddle on boat0
  - boat1 (3): (-1.5, 0.0, z -0.76) soldier/paddle on boat1; (0.0, 0.0, z -0.76) soldier/paddle on boat1; (1.3, 0.0, z -0.76) soldier/paddle on boat1
  - boat2 (3): (-1.5, 0.0, z -0.76) soldier/paddle on boat2; (0.0, 0.0, z -0.76) soldier/paddle on boat2; (1.3, 0.0, z -0.76) soldier/paddle on boat2
  - boat3 (3): (-1.5, 0.0, z -0.76) soldier/paddle on boat3; (0.0, 0.0, z -0.76) soldier/paddle on boat3; (1.3, 0.0, z -0.76) soldier/paddle on boat3
  - boat4 (3): (-1.5, 0.0, z -0.76) soldier/paddle on boat4; (0.0, 0.0, z -0.76) soldier/paddle on boat4; (1.3, 0.0, z -0.76) soldier/paddle on boat4
  - dog (1): (1.9, 0.0, z -0.76) dog/stand on boat2
  - tiptoe (2): (-40.0, 382.0, z 0.52) soldier/carry; (-33.0, 382.6, z 0.52) soldier/stand
