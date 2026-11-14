# v3/set3d5/mine.py : film 5 set, a British coal mine about 1905 - the tunnel underground and the pithead at the surface (bpy 5.3, Cycles CPU)

Files: `mine.py` (both locations), `mine_tex.py` (all artwork drawn as SVG in Python, rasterised by `v3/set3d/raster.js` into `tex_mine/`,
cached by content hash), `mine_hue.py` (hue rows through `v3/tools/hue_report.py`), `mine_contact.jpg`, `mine_REVIEW.md`. Work files:
`mine_work/` (`stills/<PRESET>_<cam>.png` 360x640 with placeholder actors, `tests/` blast / gas / flame stills, `final/<PRESET>_<cam>.png`
720x1280 12 samples, `final_log.txt`, `hue_rows.txt`, `anim/` keyed-control test, `actors/` placeholder sprites).

Built on the film-4 template `v3/set3d4/pagoda.py` v2, imported, not copied: from `tower` (`mat_lit` / `mat_emit` / `mat_card` / ink hull,
`MB`, `setup_grade`, `make_camera`, `render`, `no_bounce`, `_key` / `_show` / `_fcurves`, `placeholder_actor`), from `pagoda` (`_extra` painted
light, `setup_dof` / `update_dof` (Z-pass layered DOF), `_haze_mat`, `_pivot` / `_parent`, `_kd`, `digest`). `mine_tex` imports `tower_tex`'s
SVG helpers / job registry and `pagoda_tex.pool`. `mine.STATE` is `tower.STATE`. Same module shape as `pagoda.py` (build -> anchors dict,
set_* controls keyed with `frame`, CLI stills / tests / final / digest).

World: 1 unit = 1 D (head diameter), Z up, floor z = 0. Two locations, one at a time (`build` clears the scene).

* **tunnel**: the roadway runs from the pit bottom (y 0) to the coal face (y 40) along the centre line x = 1.8 sin(pi y / 40) (a gentle
  bend to +x, both ends on x = 0). `M.TP(y, s, z)` gives the world point at station y, s across (+ right looking inbye), height z;
  `M.tangent(y)`, `M.right(y)`. Section 5.2 D wide, walls to z 4, arched roof to z 5, rough noise-displaced coal. Timber sets (two legs at
  s +-2.28 + a cap bar at z 4.05..4.39) every 2.5 D at y = 1.25 + 2.5 k (k 0..15), wedges, lagging over the bars and behind the legs.
  Rails (track centre s +0.8, gauge 1.1) from the cage (y -11.5) to the face; the walkway is left of the rails (s -1.9 .. -0.1).
  Pit bottom y -10..0, x +-3.6, 5.6 high (whitewash, steel joists, three electric lamps), the shaft behind it (y -13.5..-10) with the
  cage (two decks, a loaded tub in it) and the half-open lattice gates. Side heading off the left wall at y 19.5..23 (3.5 x 3.5 D, 10 D
  long, own sets, ventilation door frame with its canvas sheet "KEEP THIS DOOR SHUT" just inside the mouth).
* **pithead**: the shaft at (0, 12) under a steel lattice headframe (legs to the sheave platform z 21, two spoked wheels R 2.3 at
  (0, 11.1 / 12.9, 23.6) turning in x-z planes, back-legs raking west); ropes to the brick winding-engine house (x -19..-9, y 5..19, tall lit
  arched windows, "No. 2 PIT" board) and the boiler house + chimney (-23, 27, 36 D high, smoke plume). Bank (deck z 1.4) round the shaft with
  the cage and the lattice cage gate on its south side (y 10.1), steps, railings; rails down a ramp south (x 0.6) and west to the heaps;
  coal heaps, tubs, a timber stack, barrels, sacks, wheelbarrow, gas lamp posts, two railway coal wagons on a siding (x 19), telegraph line,
  fence; the first-aid hut (x 9..14, y -4..0) with its lamp, lit window, FIRST AID board, the bench in front and the brass oxygen box on it;
  a 3D row of terraces at y 52; the painted backdrop (R 120: rows of terraced houses with smoking chimneys, chapels, far headframes and tips)
  and the smoky sky dome (R 140).

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d5"); import mine as M
A = M.build('tunnel')                 # tunnel: preset 'LAMP' (the only one)   -> anchors dict (section 2)
A = M.build('pithead', 'DUSK')        # pithead: 'DUSK' | 'DAWN'.  build(location, preset=None, clear=True, dress=True)
M.lamp_light(pos, strength=1.0, frame=None, name='miner_lamp_0', color=M.WARM, flicker=0.04)
        # a miner's lamp: point light at pos (put it at the flame of the actor's lamp prop), energy strength x LAMP_E (150 W:
        # about 1.0 x the lamp colour on a surface 2 D away), soft flicker deterministic in the frame. One distinct name per actor;
        # call every frame of a moving shot (keys location + energy, linear). Returns the light object. Works in both locations.
M.set_gas(density, frame=None)        # firedamp haze 0..1 (3 = test only): very faint layered veil, strongest under the roof (z > 0.8, thin
                                      # wavering layers), 7 camera-only slabs along the roadway + 1 in the heading; hidden at 0 (they cost)
M.set_blast(u, frame=None)            # the explosion 0..1: fireball forms at the face (u 0..0.12), front races to y 1 at u 1 (M.blast_front(u)),
                                      # burning tail to 14 D, dark smoke behind, 40 debris (coal, splinters, embers) and 16 dust sprites ahead of
                                      # the front, flash lights riding the front (energy keyed). Per frame with frame=: location / scale /
                                      # rotation linear, visibility constant. No people needed (actors run ahead of it: the front passes
                                      # y 30 at u ~0.2, y 20 at u ~0.38, y 10 at u ~0.6).
M.set_flame(k, frame=None)            # the foreman's lamp (lamp_insert): 0 out, 1 normal, up to 2 tall bright flame (gas). Mesh scale + emission + light
M.set_cage(pos=None, frame=None, swing=0.0)   # the canary cage pivot = its hanging ring: pos world point (the boy's hand), None = on its nail
M.set_drips(frame=None)               # 8 falling drops, each on its own period (call per frame); None = mid-fall still
M.set_lamps(k, frame=None)            # the six fixed hanging lamps 0 out .. 1 (light + flame emission)
M.apply_cam_state(cam, preset)        # contract-still state: blast_wide shows set_blast(0.7); everything else at rest
cam = M.make_camera(A['cams']['tunnel_eye'])  # tower.make_camera (22 mm)
M.apply_dof('tunnel_eye')             # the camera's default DOF (table M.DOF); M.setup_dof(scene, focus, fstop) for a shot's own (pagoda API 1b)
M.setup_render(scene, 'final' | 'preview')    # tower.setup_render (720x1280 12 samples / 360x640 6, 2 threads, direct light only)
                                      # + OpenImageDenoise (albedo/normal, fast prefilter) + light tree off. Call it, not tower's.
M.placeholder_actor(role, mark, face_to=None)  # roles boy (2.4 D), foreman (3.1), miner_a (2.9), miner_b (3.0)
M.stage_placeholders(A, where, cam_loc)       # 'eye' | 'low' | 'run' | 'yard' | 'none'; underground each one carries a lamp_light
M.render(path) -> (wall s, cpu s);  M.digest() -> sha1 of the scene (determinism)
M.TP(y, s, z), M.tangent(y), M.right(y), M.cx(y), M.blast_front(u)
```

Keying note: visibility-type controls (`set_gas` at 0, the blast at u 0) key constant steps: key the starting state too (`set_blast(0, frame=1)`
before `set_blast(0.1, frame=2)`). `build()` leaves gas 0, blast 0, flame 1, cage on its nail, drops mid-fall, and clears all actions.

## 2. Anchors

Tunnel (`build('tunnel')`):

| key | value | meaning |
|---|---|---|
| `tunnel_marks` | TP(5, -0.9), (8.5, -1.1), (12, -0.7), (15.5, -1.2), (24.5, -0.6), (28, -1.0) | on the walkway, in depth from tunnel_eye |
| `boy_mark`, `foreman_mark` | TP(15, -1.0) (beside the cage), TP(9.7, -0.6) (under his lamp) | |
| `run_path` | TP(30..1, -0.5) then (0, -3), (0, -7) | the run outbye to the cage |
| `cage` | hook (nail point), perch (centre of the perch dowel: put the bird sprite's feet here), floor, radius 0.24, height 0.83, perch_axis | the brass canary cage on the left leg of set 6 (y 16.25) |
| `cage_hook` | (cx(16.25) - 1.86, 16.25, 3.3) approx. | the nail |
| `lamp_hook`, `insert_flame` | under the bar of set 3 (y 8.75, s 1.25) ; the flame centre | the foreman's lamp on its chain (lamp_insert) |
| `fixed_lamps` | 6 flame positions (y 6.25, 13.75, 18.75, 26.25, 33.75, 38.75) | hanging safety lamps (point lights + floor pools) |
| `heading` | mouth, axis (into the heading), end, door, half_width 1.75, height 3.5 | side heading + ventilation door |
| `tubs` | y -4.5 (pit bottom), 12.8 / 14.95 / 17.1 (train), 34.5; one in the cage (y -11.75) | |
| `tunnel` | length, centre formula, set_y, leg_s, cap_z, track, face_y, walkway, pit_bottom, shaft (gate y -9.55), exit_point | |
| `lamp`, `blast`, `keep_out`, `cams`, `cam_notes`, `render` | | |

Pithead (`build('pithead', ...)`): `shaft` (centre (0, 12, 1.4), deck_z 1.4, gate (0, 10.1, 1.4)), `wheels`, `headframe`, `engine_house`,
`chimney`, `hut`, `bench` (x 10..12.8, y -4.75, seat z 0.95), `oxygen` (box (11.15, -4.75, 0.95) bottom centre, size 1.1 x 0.6 x 0.59, `window`
(x0, y_front, z0, x1, z1) of the glass, `mask` end of the tube, `bird_spot` on the bench left of the box), `boy_mark` (9.6, -5.9),
`gate_mark` (0.6, 9.4, 1.4), `yard_marks`, `key_dir`, `sun_elevation_deg`, `keep_out`.

## 3. Cameras (22 mm, `A['cams']`)

| name | loc -> look_at | DOF default | shows |
|---|---|---|---|
| `tunnel_eye` | TP(1.6, -0.55, 2.35) -> TP(19, 0.2, 1.85) | 2.5 at TP(8.5, -1.1, 1.6) | eye level inside the mouth looking inbye: actors in depth on the walkway, sets into the bend, lamps, tub train, face |
| `tunnel_low` | TP(4.1, -1.45, 0.55) -> TP(12, 0.2, 2.75) | 4.0 | low among the props: pick and puddle foreground, lamp of set 2 overhead, lagged roof |
| `cage_insert` | TP(15.35, -1.3, 2.88) -> TP(16.25, -1.86, 2.84) | 3.0 on the perch | ECU canary cage on its nail, the lamp of set 7 behind (warm back light), strong DOF |
| `lamp_insert` | TP(8.05, 0.62, 3.42) -> TP(8.75, 1.25, 3.38) | 3.0 on the flame | ECU foreman's flame safety lamp on its chain: bonnet, gauze, glass, flame |
| `tunnel_run` | TP(31.5, -0.5, 0.85) -> TP(4, 0.3, 2.3) | 3.0 | low deep inbye looking outbye at the bright pit bottom (runners away from camera) |
| `blast_wide` | (-0.9, -3.2, 2.6) -> TP(26, 0, 2.3) | off | from the pit bottom down the whole roadway: the fireball comes round the bend at the camera |
| `pithead_wide` | (7.5, -19, 2.4) -> (-2, 12, 11) | off | establishing: headframe + wheels, engine house + chimney, bank and cage gate, heaps, lamps, terraces |
| `oxygen_insert` | (10.35, -6.55, 1.72) -> (11.2, -4.95, 1.2) | 5.0 on the box front | the brass oxygen box on the bench: OXYGEN plate, dial, glass window (green cylinder inside), hut lamp and window behind |

Keep cameras out of: the props (s +-2.3 at every set), the rails / tubs, the timber stack (y 27..31, s -2.4..-1.6), the heap at the face
(y > 37); at the pithead the headframe legs, the bank, the heaps, the hut.

## 4. Light model

Same family as the template (diffuse key + painted blue-violet shade as emission, no bounce, emission_sampling NONE), with these changes:

* **tunnel (LAMP)**: no sun. The key is the lamps: point lights (WARM (1.0, 0.8, 0.5)): 6 fixed hanging lamps (LAMP_E x 1.1), the foreman's
  insert lamp, 2 bright electric lamps + a soft fill at the pit bottom (BULB (1.0, 0.82, 0.58)), the actors' `lamp_light`s, the blast flash.
  The template's toon term (which divides by the sun's N.L) is removed on every tunnel material (`_untoon`): plain Lambert per lamp, real
  shadows. Painted shade (0.13, 0.28, 0.85), tint (0.16, 0.34, 1.1), shade_mix 0.8 (deep blue, hue ~230-250); warm light pools on the floor
  are painted decals (additive, noise free) under each fixed lamp; brass uses the pagoda metal rule (dark-gold shade) and the lamp bodies get
  the painted glow of their own flames (`_extra`), while light linking stops a lamp's light from blowing out its own brass and glass.
  Coal glitters: a GGX lobe weighted by a sparkle mask with a fine Voronoi bump (glints as a lamp passes). Rails, tins, puddles: GGX glints.
  Lamp grain: a dozen point lamps at 12 samples leave light-selection noise, so `setup_render` turns on OpenImageDenoise (about 2.5 CPU s).
  Grade saturation 1.2.
* **pithead**: one hard sun (DUSK: (1.7, 0.92, 0.32) from the west-south-west, 9 deg; DAWN: (1.22, 1.08, 0.86) from the east-south-east,
  11 deg, soft), shade DUSK (0.13, 0.15, 0.44), DAWN (0.17, 0.21, 0.50); warm haze veils (DUSK orange 0.12, DAWN pale lilac-white 0.30);
  sky `sky_dusk` (deep blue to orange, smoke bands, the sun low west) / `sky_dawn` (pale blue to cream); lit windows, gas lamps and the hut lamp
  (point lights, DAWN dimmer 0.35).

## 5. Measured

| quantity | value |
|---|---|
| final 720x1280, 12 samples, 2 threads, denoise + DOF + bloom (CPU s) | tunnel 21.3..23.9 (blast_wide at u 0.7: 22.0), pithead 19.8..24.2 (`mine_work/final_log.txt`); placeholder actors with lamps included |
| determinism | tunnel digest 9faaa55e... (blast 0.5 + gas 0.5), pithead DUSK 2b2853a8..., identical in two processes |
| hue (all LAMP finals) | red 11 orange 27 blue 42 violet 11 magenta 5, sat 0.34 val 0.47 (night: blue-dominant, no magenta cast); DUSK red 31 orange 24 magenta 8; DAWN red 28 orange 32 magenta 2 (`mine_work/hue_rows.txt`) |
| keyed controls | `mine_work/t_anim.py`: lamp_light / blast / gas / flame / cage / drips keyed over 60 frames, values checked between keys: OK |

## 6. Command line

```
python3 mine.py stills [cam ...]                  # mine_work/stills 360x640, placeholder actors, all cameras x presets
python3 mine.py tests                             # mine_work/tests: blast u series (blast_wide, tunnel_run), gas 0/0.5/1/3, flame 0/1/1.8
python3 mine.py final <tunnel|pithead> [PRESET] [cam ...]   # mine_work/final 720x1280 12 samples, prints wall / cpu s
python3 mine.py digest <tunnel|pithead> [PRESET]  # determinism digest (tunnel with blast 0.5 + gas 0.5)
python3 mine_hue.py mine_work/stills/             # hue rows per frame / preset + reference rows
python3 mine_work/t_anim.py $PWD                  # keyed lamp_light / blast / gas / flame / cage over frames
```
