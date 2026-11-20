# v2 location B (Mexico City 1968 stadium + 1972 day) : `v2_b.py`, `v2_b_shots.py`

Extension of set15 (no `set15*.py` edited). Same units: scene = D (0.54 m); builders and the v2 helpers take METRES (`B2.M2D(p)` converts to D). Cycles CPU, OIDN, 720x1280, 12 spl, no DOF, no real volumetrics.

```python
import sys; sys.path.insert(0, '.../v3/set3d15')
import v2_b as B2, v2_b_shots as SHB          # SHB imports cast15 / sprites / cast_test (cards)
A = B2.build('NIGHT')       # 'NIGHT' dusk floodlit (BIGZOOM 2, T3, T4 start) | 'TENSE' darker + beams + dim crowd (T4 hush, T5) | 'DAY72' 1972 day (T7)
cam = SHB.apply_bigzoom2()  # camera keys 31.0 .. 35.3 s (frames 930-1059, 30 fps, eased, per-frame keys)
cam = SHB.apply_t5()        # T5 ride-along 44.38 .. 55.08 s
```
`B2.build(light, city=True, sparkles=True, dress=True, extent=820.0)` calls `F.build('B', light)` then adds the v2 extras; all set15 hooks (`F.set_bar_height`, `F.bar_fall`, `F.flash_bulb`, `F.crowd_mode`, `F.torch_flicker`, `F.flag_wave`, `F.stand_flashes`, `F.clear_keys`) still work. Do NOT use `F.switch_light` on v2 presets (the v2 crowd/foam materials are tuned in place); build the other preset instead. Presets are registered in `F.LIGHTS['B_NIGHT' | 'B_TENSE2' | 'B_DAY72']` and `F.LOC_LIGHTS['B']`. Build is 3-4 s.

## What B now has
- **City for BIGZOOM 2** (night): about 4,000 lit-window blocks on a 72 m street grid (each window cell is a procedural warm/cool lit or dark cell, one material, no textures), a far skyline to 2.5 km (coarser, dimmer windows to avoid shimmer), 2,000+ cars with white head and red tail lights, 3,000 street lamps with ground light pools, a 44 m avenue from the south gate with lamp rows and red pennants, paved plaza with radial strips, lamp ring and trees. Ground is a deep violet plane. Mountains: two ridge rings (3.3 / 4.5 km) plus two volcano cones with a warm orange cap; sky = deep blue-violet with one thin orange horizon band (the sun-glow lobe is off: no haze).
- **Stadium rim:** 120 outer fins, 2 rows of warm lit concourse slots, LED ring on the parapet, 28 inner "MEXICO 68" banners (4 colourways, textured, plain backs) + 18 outer wall banners, 87 waving flags (set15), cauldron with burning flame plus a small gold halo and a faint heat column, **8 floodlight towers** (4 of set15 + 4 new at 200/245/295/340 deg), each with an additive emissive beam cone (alpha = facing x length fade, fades out before the ground so the pit is never hazed) and a lamp flare.
- **Crowd:** 18.5k figures re-coloured vivid (red, white, yellow, blue, orange, green), brighter shade (`crowd_shade_k`), bobbing as before; 3,200 **flash-bulb stars** (frame-driven white-noise twinkle, invisible when off; no keys needed).
- **High jump:** quilted royal-blue foam mat top (`foam_mat` plane, painted PNG) with a red border and quilted skirts on all 4 sides (no blank slab, no grey), red/white thick bar, thin silver standards, bar-height board **"2.24 m"** on a post by the right standard (x +3.05 m, faces -y), scoreboard overlay **"HIGH JUMP / MEN FINAL / BAR 2.24 m"** on the far-rim board, striped pitch, hot red tartan (mottled), officials' table/photographer platforms from set15. Podium (-9, 10 m) gets gold steps / red fronts, a MEXICO 68 backdrop and a spot light.
- **DAY72:** bright blue sky, pastel city, no beams, sparkles and window lights off, big yellow **"1972"** banner (20 x 10 m on posts above the far rim at u = 96 deg).
- Textures are painted by `work_v2_b/v2_b_tex.py` into `work_v2_b/tex/` (regenerated if missing).

## Colour and light
- Signature: hot tartan red apron/track, deep night-blue sky and shade, white-warm floodlight beams, gold torch. Warm sun key (low, behind the far stand) + cool blue-violet shade + floods on every frame.
- `P` keys added: `beam_k`, `windows`, `day`, `crowd_shade_k`, `crowd_gain_k`. NIGHT exposure -0.1, grade sat 1.08; TENSE exposure -0.5, floods 2.6, crowd_k 0.42 (dark crowd so a rim-lit body pops), beams x1.15.
- **Rim / back light for character cards** (cards are unlit emission, so the rim is baked into the card PNG): 
  ```python
  SHB.rim(True, side='left'|'right', color=(255,244,220), width=0.06, k=0.95, up=0.4, tint=(1,1,1), bright=1.0, cool=0.3)
  SHB.card(...) / SHB.airborne_over_mat(...)      # every card made while rim is on gets the hard bright edge on that screen side
  SHB.rim(False)
  ```
  `side` = screen side of the light; `width` in D (x ppd px); `up` adds a top-edge share; `tint` multiplies the card to match the plate (night: 0.95 0.97 1.0, crowd 0.8 0.82 0.95); `cool` shades the far side blue-violet. Use side opposite to the key torch/tower for a backlit look; T5 key image: `side='left', k=1.0, up=0.5`.

## Grounding helpers (`v2_b_shots.py`)
- `B2.surface_z(x_m, y_m)` : walkable height (m): foam mat top 1.056, podium steps, stand treads, else track.
- `SHB.card(tag, cast, pose, xy_m, cam_m, z=None, ...)` : real cast card, FEET on `surface_z`, contact shadow, faces the camera; `tilt_deg` leans it back for high / top-down cameras (it keeps the flat shadow).
- `SHB.seat_card(tag, cast, pose_name, row, u_deg, cam_m)` : spectator SITTING on a stand tread (hip anchor on the seat, shadow); `B2.stand_pos(row, u_deg)` gives the seat point; `B2.hide_3d_crowd(center_m, r)` and `B2.hide_rails(center_m, r)` clear 3D figures / aisle rails under a card cluster.
- `SHB.airborne_over_mat(tag, cast, 'flop'|'straddle_a', cam_m, over, front, rise)` : jumper by its `bar` / `head` anchor ON the crossbar line, asserts the card is within the bar span, puts the contact shadow on the foam mat (clamped onto the mat). Cards are never placed in the air anywhere else.
- `SHB.check_grounding()` returns problems (feet vs surface, missing shadow, airborne shadow off the mat); empty on all 8 stills.
- `SHB.spot_pool(xy_m, r)` : floodlit pool on the ground under a tiny hero (so he is findable from 300 m).
- Sprite cache: identical (cast, pose, ppd) sprites render once (hundreds of crowd cards cost a few seconds).

## Camera paths (metres, `v2_b_shots.py`)
- `SHB.bigzoom2(t)` -> (loc, look, lens) for t in 31.0-35.3 s: smootherstep time warp over a Catmull-Rom path, 7 waypoints in `BZ_KEYS`: (-52,-262,150) lens 22 -> over the near rim and beams (-18,-66,44) -> over the crowd heads (-9,-36,17) -> medium on Dick (-2.2, 5.0, 1.5) look (0.7, 9.6, 1.95), lens 19 at the end. Dick (`DICK_B` = (-1.0, 7.6)) is about 4 px at the start (< 5 %) and about 45 % of frame height at the end. `SHB.apply_bigzoom2()` keys a per-frame camera (location, rotation, lens), LINEAR between frames, frame range set.
- `SHB.t5_ride(t)` / `SHB.dick_t5(t)` for 44.38-55.08 s: low side ride alongside the run-up (to 46.3 s), hover track across the bar (46.4-47.8), slow orbit on the arch (47.8-50.3: camera 2.4 m from the bar, arch >= 60 % of the width), same framing through the straddle plate (50.35-52.85), drop onto the mat (52.9-55.1). `dick_t5(t)` is the jumper's feet / body path (use it to place cards per frame with `SHB.card` / `airborne_over_mat`). `SHB.apply_t5()` keys it.
- Generic: `SHB.apply_path(fn, t0, t1)` with `fn(t) -> (loc_m, look_m, lens)`; `SHB.spline(keys, t)` Catmull-Rom on timed keys.

## Stills (`python3 v2_b_shots.py final [still ...]`, `work_v2_b/stills/`, `work_v2_b/sheet.jpg`, numbers in `work_v2_b/stills_log.json`)
bz_start, bz_mid, bz_end, t4_low, t4_coach, t5_arch, t6_top, t7_day. `python3 v2_b_shots.py sheet` rebuilds the sheet. Colour numbers by `work_v2_b/stats.py` (qa_stats2 formulas on 90x160).

## Notes / limits
- The bar of T4 low is set to 2.46 m so it sits about 30 cm over Dick's head (skull 2.03 m, hair 2.19 m); the "2.24 m" board is a sign (BIGZOOM 2 end uses the real 2.24 m bar).
- The apron and mat: bar at y 11.6 m, mat front edge at y 12.3 m (set15 geometry), so a flop's shadow is placed on the front of the mat, not directly under the arch.
- Far windows shimmer a little at 12 samples when the camera moves; the far skyline uses 3x larger cells to limit it.
- **Render cost (solo, final 720x1280, 12 spl, 2 threads, wall s per frame).** Before: bz_end 128 s (255 CPU-s), t4_low 81 s, t5_arch 87 s (QA-tech measured 142 / 107 s under load). Cause: the 8 beams were double-sided cones, so a ray crossed ~16 transparent layers (and 6 transparent bounces turned the frame black); culling the city / skyline / cars alone only gave 128 -> 115 s. Fix: each beam (and the torch column) is now ONE camera-facing ribbon (LOCKED_TRACK constraint to the camera, one transparent hit per ray; `B2.bind_beams(cam)` is called by `make_camera_m`, so a camera made any other way needs `B2.bind_beams(cam)`), transparent bounces 12. After: bz_end 25.5 s, t4_low 29.5, t4_coach 40 (600+ cards), t5_arch 25.1, t6_top 30.3, t7_day 12.7; far views bz_start 12.7, bz_mid 14.2. `B2.build(..., fast=True)` (default for pit/stand stills via `V2B_FAST=1`) also drops the city, skyline, cars and lamps and uses 900 sparkles instead of 3,200; use `fast=False` for any frame that sees the city (BIGZOOM 2 frames above about 40 m: city off is only safe inside the bowl).
- `card()` / `put()` face the camera at the CALL frame only (yaw about Z, fixed afterwards): for an animated camera re-orient each card per frame (set `rotation_euler.z` from the camera position) or place per frame.
- Frame ownership: frame 1059 (BIGZOOM 2's last frame, 35.3 s) belongs to T4 (35.27 s start); frame 1652 (55.08 s) belongs to T6. T3 renders 31.0-35.27 (frames 930-1058).
- v2 fixes after QA-art: orange sky arc removed (the horizon band is violet now), tartan mottle finer and calmer, coach still uses randomised crowd cards (6 casts, mirrored, jittered) with a clear space around him and no sparkles, bz_end camera is higher (z 2.45) so the bar clears Dick's head, t6_top wider with 3 photographers and no stray shoes on the mat, t7 has jumpers in green (flop), gold (sitting thumbs-up) and red (waiting) kits.
