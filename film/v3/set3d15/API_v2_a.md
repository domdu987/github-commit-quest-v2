# API_v2_a.md : location A v2 (Medford 1963), extension of set15. Files: `v2_a.py`, `v2_a_shots.py`, `work_v2_a/` (stills, tex, sprites, stats.py, sheet.jpg). set15*.py untouched.

```python
import sys; sys.path[:0] = ['.../v3/set3d15']
import v2_a as V, v2_a_shots as SHT
A = V.build_a2('HERO')        # 'HERO' golden hour | 'HERODAY' day. kw: town_on, people, rays, clouds, hills.  ~3 s.  Returns the set15 anchors (+ marks poster, gym_sign, gate_sign, scoreboard, water_tower)
cam, cl = SHT._cam(loc_m, look_m)           # 22 mm camera from metres
```
Units as set15: builders in metres, cameras/marks in D (0.54 m). Registers presets `A_HERO`, `A_HERODAY` in `F.LIGHTS` (set15 `F.build('A','HERO')` works too).

## What is built
Saturated palette (`V.PALETTE`, `V.recolor()`): maroon/gold school, red cinder, green grass, deep blue sky with clouds (`V.sky_clouds`), sun az -105 el 28 (warm key, blue-violet shade, front-lit, long shadows to +x). Terrain with pine hills (`terrain`, `pines`, instanced), 430 houses (red/green/blue roofs), roads with dashed lines, street trees, shops, church, water tower, river, farmland, parked cars, 6 moving cars (keyed 0-140 f), 400 m oval + infield (stripes, tents, long jump, mats, hurdles, runners), school pine groves, gym with MEDFORD HIGH sign, MEXICO 68 poster (`marks['poster']`), TRACK & FIELD gate (west), HIGH JUMP scoreboard, maroon/gold bunting, ~250 low-poly chibi spectators/boys on bleachers, benches, track.
Signs are PIL textures in `work_v2_a/tex/` shown as emission (`V.mat_tex`).

## Light
- Key: warm sun + painted blue-violet shade (shade hue 224-262).
- **God rays**: `V.god_rays(P, n, seed, strength, width, length, where=[(x,y)..])` additive (Transparent+Emission) crossed quads along the sun direction; `V.tune_rays(k)`; stills use `SHT.rays()` (6 beams out of the west grove, k 0.42).
- **Rim / back light for cards**: `V.rim_on(to_light=(-0.7,-0.5), color='#ffb040', width=5, strength=1, glow=0.5)` BEFORE `put`/`ground_card`; to_light = screen direction (x right, y down) from figure to light; `V.rim_off()`.

## Grounding
`V.surface_z(x,y)` (ray cast, D); `V.ground_card(tag,cast,pose,(x,y),cam_loc, z=None, scale, ppd=..)` puts the feet on the surface + contact ellipse + long cast shadow (sprite silhouette projected along the sun). `V.ground_card_anchor(...)` for flop/straddle/buried (anchor + shadow on landing surface zg).

## Props
`V.newspaper(cam_loc, look, dist=0.72, fill=1.0, roll_deg)` MEDFORD MAIL TRIBUNE, FOSBURY FLOPS OVER BAR, halftone sepia photo from the cast15 `flop` sprite, bent mesh facing the camera (animate `dist`/camera for the push-through; hands optional). `V.tex_*` regenerate textures.

## Cameras (v2_a_shots.py)
`bigzoom1_path(t)` (0-4.4 s, eased Catmull-Rom, loc/look in metres: 100 m up -> over east pines -> over bleacher -> Dick medium 40 %), `key_camera(cam, fn, t0, t1)` keys every frame (frame = round(t*30)), `setup_bigzoom1()`, `t1_hero_low(t)`. Stills: `python3 v2_a_shots.py [final|preview] [s1..s7]`.

## Measured / limits
See report. Shot cost ~5 s wall/9 s CPU (preview), build 3 s. Not done: Dick hero flop uses only the cast sprite (no motion), T3 DAY shift not tuned (`HERODAY` preset only), OTS foreground Dick is a 3D stand-in, newspaper hands crude.
