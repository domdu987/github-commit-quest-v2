# v3/kit: grounded set pieces for the lit looks

`kit.py` is a small bpy 5.x library of cheap, grounded set pieces for the path-traced looks: the R9/R10 "lived-in" dressing, practical light pools,
off-screen gobos, cannon fire and explosions. It has no dependency on any one set, and film 24's `set3d24/joseon.py` uses it for look C.

```python
import sys; sys.path.insert(0, PROJ + '/v3/kit'); import kit as K
K.use(collection)          # where new objects go (default: the scene collection)
```

Units are D (1 D = one head, about 0.53 m) and z is up. Positions are in world space, or in the parent's local space when you pass `parent=`
(for example a ship's ride empty, so the prop sails and heaves with the ship). Materials are Principled and their names start with `K_`.

## Rules every piece follows

- **Nothing floats.** You pass the floor height `z` (or a `zfun(x, y)`), and every piece sits on it and casts shadows. Debris lands on `ground(x, y)`
  or splashes into `water_z` and sinks.
- **Nothing is parented to the camera.** Pieces are world-fixed or ship-parented.
- **Everything can be keyed per frame.** Each animated call takes `t` (seconds since the event; `t < 0` means it has not happened yet) or a `level`, plus an optional
  `frame=`. With `frame=` it keys visibility, location, scale and light energy. Call it on every rendered frame.

## Ground and wear

| call | what |
|---|---|
| `planks_ground(rect, z, seed, along='x', w=0.55, gap=0.05)` | individual planks with gaps, mixed tones and wear |
| `stones_ground(rect, z, size=0.75, seed)` | cobbles set in mud |
| `wet_patches(rect, z, n, r)` / `mud_patches(...)` | glossy puddles and dark mud (thin decals, no shadow) |
| `grass_cracks(rect, z, n)` | grass tufts in the cracks |

`rect = (x0, y0, x1, y1)`. Each call returns one merged object, so it stays cheap.

## Props

`rope_coil(c, r, layers)`, `crate(c, s, yaw)`, `barrel(c, r, h, lying, yaw)`, `net_pile(c, r)`, `net_hang(p0, p1, drop)`, `rock_cluster(c, n, radius, zfun)`,
`pine_cluster(c, n, radius, zfun)` and `cannon(c, yaw, pitch)`. `cannon` returns `dict(ob, muzzle, dir)`.

## Practical light pools

- `lantern(c, h=2.6, power=70, post=True)`: a post or hanging lantern. It has a point light with a flicker driver and returns `dict(ob, light, pos)`.
- `brazier(c, power=260)`: a fire basket on legs, with flames, embers and a warm point light.

Use them where the story is. The look C yard has 3 braziers and 5 lanterns. At sea, each lantern on a Japanese upper deck (light 0 by day) and the fires
on the damaged ships throw the pools.

## Off-screen shadows (gobos)

- `gobo_rigging(c, yaw, scale, masts=2)`: masts, yards, shrouds and ratlines.
- `gobo_canopy(c, n, radius)`: tree crowns.

Both are invisible to the camera. They cast shadows and cut the sun shafts in the haze. Place them between the subject and a low sun, off screen.
`joseon._gobos_for(cam)` puts them about 20 D from the subject toward the sun.

## Cannon fire

```python
rig = K.muzzle_rig(pos, dir, parent=ride)     # flash star + flash point light + smoke ring + recoil puff
K.fire_muzzle(rig, t, frame=f)                # flash and light 0-0.1 s, ring flies out and grows over 1.6 s, puff swells and drifts up over 2.5 s
```

## Explosions, splashes and fire

```python
ex = K.explosion_rig(pos, water_z=0.0, ground=None, scale=1.0, n_debris=22, column=True)
K.set_explosion(ex, t, frame=f)
```

`set_explosion` animates these parts:

- 3 fireball layers swell (0-0.25 s), then roll up and darken (to 1.2 s). A fire light peaks at 0.06 s.
- Plank and splinter debris fly on ballistic arcs. They land flat on `ground`, or splash and sink.
- The water column rises (0-0.5 s) and collapses (to 1.6 s).
- The shockwave ring runs out over the water (0-0.8 s).
- 36 embers rise.
- The smoke column builds from 0.4 s and stays.

The other calls:

- `explosion_rig(..., n_debris=0)` builds a water column only (a near miss).
- `splash_rig(pos)` + `set_splash(rig, t)` is a person-sized splash for a comic jump into the sea.
- `fire_patch(points, size, light=True)` + `set_fire(fr, level)` puts flame tongues, embers and one warm light on a sail, a yard, the rigging or a deck.

## Cost

Everything is plain mesh with Principled or emission, plus soft alpha for smoke. There are no simulations and no volumes. In the look C board, 12 samples at
75 % cost 50-75 CPU s per frame and 24 samples cost 90-120 CPU s per frame (22-30 s on 4 cores).
