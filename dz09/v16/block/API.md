# v16/block: the DEAD ZONE 09 blocky 3D cast (sheets_v3), built by code

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Folder: `PROJ/v16/block/`.
Only this folder was written. Read-only imports: `v11/set` (the approved set, lights, post), `v8/cast` (only through the
hook copy's stage; no puppet is posed in block mode, and the raster cache is redirected into `hookcopy/tmp`).
No image generation, no network, no paid API: every mesh, texture and face is drawn by code (bpy, numpy, PIL).

## Files

| file | what |
|---|---|
| `blockcast.py` | the system: `SPECS` (proportions per character), `Figure` (rig + meshes + materials + face + pose + gait), `GAITS`, `BlockAct` (drop-in for the hook's `stage.Act`), `compat_facing`, star-of-life and ID-card textures |
| `bc_geom.py` | mesh builders: rounded box with an angle-even bevel band (welded, smooth), rounded-rectangle bands, sweeps (hair clumps, straps, tie), rounded-box SDF projection (straps and tie lie on the torso), exact boolean (the C-hand tunnel), the `rest` attribute |
| `bc_mat.py` | procedural Cycles materials: fabric (weave bump, grime, blood, tears, wet + rain beads), solids (leather, webbing, metal, hair), plastic skin (subsurface, coat, fine noise, face decal, glowing eyes), retro-reflective tape |
| `bc_face.py` | flat decal faces drawn with PIL: expressions, lip-sync mouths, blink, gaze, stubble, scars, zombie veins / blood / teeth / glow mask; cached in `tex/faces/` |
| `bc_studio.py` | the cream studio (cyclorama, soft key, fill, rim) for the proofs |
| `measure_sheets.py` | proportions measured on the sheet turnarounds -> `out/proportions.json`, `out/proportions_annot.png`; summary in `proportions.md` |
| `turnaround.py` | -> `turnaround.png` (sheet crops left, our renders right, same figure height) |
| `faces.py` | -> `faces.png` (sheet expression rows above our 3D heads; hook names, blink, 5 mouth levels) |
| `hookcopy/` | copy of `v10/film` (code only) switched to the blocky cast (see below) |
| `in_hook.py` | -> `in_hook.png` (approved clip frame beside our final-tier frames) |
| `walk_kong.py` | -> `walk_kong.mp4` + `out/walk_drift_walk.json` (Kong walking 3 s in the hook set, 3/4 tracking camera) |
| `t_gait.py` | geometry-only drift check of the walk / run cycles (no render) |
| `dbg_hook.py` | stage hook frames with the blocky cast, print head / roof facts, draft render |

## Units and frames

- Model metres (Kong 1.80 m, office zombie 1.75 m, crew 1.78 m). The root empty carries the stage scale: `Figure(height=h)` makes the figure `h` stage units tall (1 BU = 0.6 m in the set). The hook keeps the puppets' heights (Kong 2.86, crew 2.80, driver out of the car 2.70, seated driver 2.03 x 0.88), so the approved cameras frame the same height of figure.
- Rest frame: soles at z = 0, the figure faces -Y (stage facing 0), the character's LEFT is +X.
- Every mesh carries a point attribute `rest` = its rest-space position in metres. All dirt / blood / wet masks read it, so they stay on the cloth when the limbs move.

## Rig (`Figure`)

Parts are separate objects parented to joint empties (quaternion rotations, identity in rest):

```
root (soles, facing, scale)
 └ pelvis (hip height)            trousers seat, belt, pouches, shirt tail
    ├ waist (belt height)         torso / jacket / shirt, collar, tape, straps, radio, tie, ID card, neck
    │  ├ neck (shoulder top)      head (face decal), hair cap + clumps, helmet
    │  └ sh_L / sh_R              upper sleeve, arm tape, star patch (left)
    │     └ el_L / el_R           forearm sleeve, cuff / rolled cuff, bare forearm
    │        └ wr_L / wr_R        hand variants: fist (C-shaped: a tunnel through the grip, thumb above it), open, claw, point; phone prop
    └ hip_L / hip_R               thigh, cargo pockets
       └ kn_L / kn_R              shin, leg tape, torn hem (zombie)
          └ an_L / an_R           boot / shoe, sole, collar, laces
```

Neck is hidden (inside the collar; the rescue kit's neck is the black tee). Arms and legs are 2-bone IK chains (`limb_quats`): elbows bend about local -X, knees about +X; the feet are kept flat (ankle = inverse of the leg rotation).

### Figure API

```python
import blockcast as BC
f = BC.Figure("kong", "kong", height=None, wet=False, gloves=None)   # height None = metres; wet 0..1; gloves None = spec default
f.place((x, y, z), facing_deg)
f.pose(dict(expr="determined", mouth=0.5, blink=0, gaze=(0, 0), head=(yaw, tilt, dx, dy), lean=deg, hip=(dx, dy),
            arm_r="down", arm_l=dict(hand=(0.3, 0.5), elbow=1, hand_shape="open"), legs="wide", prop_r=dict(type="phone")), camera=cam)
f.set_face(expr, mouth, blink, gaze)        # only the decal
f.gait_pose(t, "walk" | "run", path0, direction)
f.head_world(); f.sole_world("L"); f.objects; f.hide(True); f.set_pass_index(2)
```

## Hook compatibility (`BlockAct`, `hookcopy/stage.py`)

`hookcopy` is `v10/film` (code, `tex/`, README, captions) with three edits: `common.PROJ` points three levels up; `stage.py`
builds `BC.BlockAct` figures for kong / crew / driver / driver_out when `DZ09_CAST=block` (the default in the copy), does
not build the 10 background extras (they are puppets), skips the puppets' shadow proxies (3D figures cast real shadows),
and redirects the `raster8` cache to `hookcopy/tmp/_cache8` (read-through from v8's cache) so nothing under v8 is written.
The shot files `shots/s*.py` and `shots/base.py` are unchanged.

```
cd PROJ/v16/block/hookcopy
DZ09_CAST=block BLOCK_VIEW=ignore nice -n 5 python3 run.py --frames 636,1030,1049 --tier final --size 720x1280 --threads 2 --tag block
DZ09_CAST=block BLOCK_VIEW=compat ... --tag block_compat
```

`BlockAct(F, name, kind, height, seated=False, wet=True)` has the same `set(loc=, face=, view=, s=, idx=, **pose)`, `hide()`,
`apply(cam)`, `head()`, `pt()`, `.breath`, `.pidx`, `.visible`, `.posed`, `.loc`, `.face`, and an `.a` shim with what the stage,
run.py and the shots read: `sc` (stage units per puppet D), `ppd`, `spec["legs"]` (so `base.driver_seated` puts the hip on the
seat), `walk_lock`, `pitch_override`, `pitch_anchor`, `set_glow()` (no-op: the card halo has no 3D equivalent),
`set_pass_index()`, `objects`, `hide()`, `head_world()`, `world_of()`.

### What each pose key does on the 3D figure

| key | 3D meaning |
|---|---|
| `loc`, `face` | soles point and facing (stage convention) |
| `view`, `s` | **ignored** (`BLOCK_VIEW=ignore`, the default): the model is truly 3D. `BLOCK_VIEW=compat`: a forced view turns the figure so the camera sees what the puppet drawing showed (front 0 deg, q 38 deg, side 90 deg, back 180 deg from the camera axis, toward screen-right for s = +1), unless the shot's own facing already shows that view within 16 deg |
| `expr` | face decal (table below) |
| `mouth` | level 0..1 (shape a) or `(shape, level)`, shapes a / o / e; 5 drawings (0, .25, .5, .75, 1). Zombies always use the snarl (`zopen`) at max(level, 0.15) |
| `blink` | 0 open, 1 half, 2 shut |
| `gaze` | (dx, dy) eye offset on the decal: 0.07 / 0.05 face units per 1.0 |
| `head` | (yaw deg about Z, tilt deg about X: + = chin down, dx, dy in D: neck offset, + dy = down) |
| `lean` | degrees: the waist joint pitches the torso forward (the pelvis stays) |
| `hip` | (dx, dy) in D: pelvis forward / down |
| `breath` | z scale of the waist joint (the stage's 0.6 % breathing) |
| `arm_r` / `arm_l` | the character's right / left arm (as in the puppets' front view) |
| `arm_n` / `arm_f` | the arm nearer / farther from the camera, from the real camera position (not from `s`) |
| `prop_r/_l/_n/_f` | `dict(type="phone")`: a phone in that fist; other props are not built (cutter, umbrella, bag, helmet) |
| `legs` | presets below; `dict(seated=True)`; `dict(foot_n=(x, y), foot_f=(x, y), hip=(dx, dy))` in D |
| `_hold` | (the two-handed cutter of `kong_cutter`) both fists forward at the hips; no cutter prop yet |

D (the puppets' drawing unit) is taken as H / 4.31 of each figure, so a dict `hand=(dx, dy)` lands about where the puppet's hand was.

### Named arm poses -> joint targets

Fist-centre target relative to the shoulder joint in the chest frame, fractions of H: (out = away from the body midline,
forward, down); the elbow pole; the hand shape. The IK (`limb_quats`, upper arm 0.105 H, forearm + fist 0.162 H) turns them
into shoulder and elbow quaternions; the wrist stays straight except `claw` (wrist -25 deg).

| name | out, fwd, down | elbow | hand |
|---|---|---|---|
| down | 0.012, 0.010, 0.262 | back | fist |
| hang | 0.016, 0.020, 0.258 | back | fist |
| hips | -0.050, 0.000, 0.180 | out | fist |
| hold_cutter | -0.070, 0.110, 0.190 | back | fist |
| phone_ear | beside the head: head half width + fist half width + 0.03 H out, ear height | out | fist (+ phone) |
| phone_look | -0.110, 0.160, 0.080 | down | fist |
| point | 0.010, 0.250, 0.010 | down | point |
| raise | 0.040, 0.030, -0.255 | out | open |
| wave | 0.110, 0.040, -0.190 | down | open |
| reach | -0.020, 0.245, 0.050 | down | open |
| claw | -0.030, 0.240, 0.040 | down | claw |
| claw_up | -0.020, 0.215, -0.080 | down | claw |
| lap | -0.050, 0.120, 0.220 | back | fist |
| wheel | -0.055, 0.235, 0.070 | down | fist |
| cross | -0.200, 0.120, 0.140 | out | fist |
| head | -0.120, 0.030, -0.220 | out | open |
| pocket | 0.010, 0.000, 0.200 | back | fist |
| carry | -0.040, 0.060, 0.200 | back | fist |
| umbrella | -0.050, 0.120, 0.100 | down | fist |
| shout | -0.120, 0.100, -0.120 | down | open |
| guard | -0.050, 0.170, 0.020 | down | open |

Dict arms: front / back keys (`arm_r`, `arm_l`): out = dx D, down = dy D, forward = 0.04 H (+0.08 H when the hand is above
the shoulder, +0.10 H when it crosses the body); `elbow=1` -> pole out, `-1` -> pole down. Near / far keys: forward = dx D,
down = dy D, the hand comes in toward the midline by up to 30 % of the shoulder offset as it reaches forward. A phone held
above the shoulder snaps to the ear target. A target inside the torso block is pushed in front of it. Poles: back =
(0.35 out, 1 back, -0.2), out = (1 out, 0.25 back, -0.3), down = (0.45 out, 0.2 back, -1).

### Leg presets

(spread = extra lateral foot offset, near / far = forward offset of the near / far foot, drop = pelvis lowered, all x H;
the pelvis is then lowered further until both ankles are reachable at 98.5 % of the leg length.)

| name | spread | near fwd | far fwd | drop | pelvis fwd |
|---|---|---|---|---|---|
| stand | 0 | 0 | 0 | 0 | 0 |
| wide | 0.040 | 0.010 | -0.010 | 0.012 | 0 |
| step | 0.010 | 0.075 | -0.065 | 0.020 | 0 |
| lunge | 0.025 | 0.140 | -0.120 | 0.045 | 0.020 |
| crouch | 0.035 | 0.030 | -0.020 | 0.090 | 0 |
| seated | ankles 1.15 x hip width apart, thigh length forward, a shin below the hip: thighs level, shins vertical, knees forward-up |

### Expressions

| character | names | sheet row |
|---|---|---|
| Kong / crew | determined, angry, surprised, worried, sad, pain (the sheet's six); neutral, serious, guilty (worried brows, eyes down), tired, alarmed, shouting, scared, joy, blink | `kong.png` "Expressions / 6 Key Moods" |
| zombie | idle, roar (= the sheet's scream), attack, growl; hook names: still (eyes shut, no glow), head_lift (eyes open, glow), lunge (= attack), bite (= roar) | `z_office.png` "Expressions - Infected" |

Zombie eyes are white in the decal and drive an emission mask (`eye_glow`, strength 7) through the head shader; `still` sets it to 0.

## Walk and run (`Figure.gait_pose`, `GAITS`)

The root moves at constant speed along a straight line. Each foot lands `v T beta / 2` ahead of the root and stays at that
world point for the stance share `beta` of the period; the swing eases to the next landing with a sine lift and a toe pitch.
The pelvis is lowered so both legs stay bent (IK never pulls a planted foot); it bobs twice per cycle; the arms swing opposite
the legs; the torso leans and twists a little.

| gait | v (model m/s) | period | stance | lift | lean |
|---|---|---|---|---|---|
| walk | 0.78 | 0.92 s | 60 % | 0.040 H | 4 deg |
| run | 2.10 | 0.64 s | 36 % | 0.075 H | 13 deg |

## Materials (procedural, `bc_mat.py`)

- Skin: Principled, subsurface 0.12 (radius 1.0 / 0.45 / 0.25 x 12 mm), coat 0.25 (toy plastic sheen), fine noise bump; the head adds the face decal mapped from object coordinates onto the front face only (object-space normal mask).
- Fabric: two crossed band waves + fibre noise as bump (weave 4.5 mm, webbing 2.2 mm), low-frequency colour variation, sheen (0.04 on black).
- Grime: height falloff from the soles (boots, hems), a knee band on the front of the legs, all-over mottling (the sheet's jacket), noise broken; multiplicative so the orange keeps its hue.
- Blood: code-placed splats (centre, radius, drip length) in rest space with noisy edges; drips run down as thin noise stripes; voronoi specks in zones. Zombie: 26 shirt splats, 3 on the slacks, 3 on the skin, 1 on the tie; Kong and the crew: none.
- Tears (zombie): code-placed holes painted as dark skin with a dark red rim; torn hems are geometry (jagged shirt tail, trouser bottoms, rolled cuffs).
- Wet (variant 0..1): darker base, lower roughness, a clear coat, voronoi rain beads (bump on coat and base). Black kit gets a thinner film (coat <= 0.1-0.18) so it stays black under the blue sky.
- Reflective tape: yellow edges, silver centre (`tapev` attribute across the band), micro-prism bump, plus a GGX lobe whose normal is the incoming (view) vector, gain 1.7, roughness 0.26: lights within roughly 15-20 deg of the camera direction are sent straight back to the lens.
- Hair: near-black, coat; the zombie's is always wet.

## Measured

See `proportions.md` (sheet proportions and the model's), the report at the end of the task for render cost and drift.
