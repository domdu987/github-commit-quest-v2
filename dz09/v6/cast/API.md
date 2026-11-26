# v6/cast: DEAD ZONE 09 cast built like the ref D puppets

Folder: `PROJ/v6/cast/`. PROJ is `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`.
Built with bpy 5.3 and Cycles on CPU. There is no Freestyle, no EEVEE and no Grease Pencil.
The spec is `spec/refD_chars.md` section 5, and we follow its recipe. We keep the identity from the character sheet: a round white head, a simple black-line face, spiky black hair, an orange RESCUE jacket with silver bands and a Thai flag, black trousers, boots and a backpack.
We copy only the look of ref D. Its uniforms, hats, insignia, logo and subject are not used.

## Files

| file | what |
|---|---|
| `cast6.py` | The builder. Classes `Character`, `Cutter` and `Phone`; the presets; the materials; the ink hulls. |
| `faces6.py` | PIL textures (no bpy). Face decals in angular sphere space, jacket and shirt atlases in cylinder space, the battery gauge (3/2/1/0 bars) and the hair stroke tile. Cached in `tex/`. `python3 faces6.py` writes `tex/faces_sheet.png`. |
| `lookdev.py` | Lookdev renders on neutral ground under soft light at 720x1280, plus measurements. Run `python3 lookdev.py renders` for the 3 characters x front, 3/4 and side, and `python3 lookdev.py extras [--parts driver,wet,faces,props,night]` for the rest. |
| `sheet6.py` | Builds `lookdev.png`. Our renders sit next to ref D crops and the character sheet, all scaled to the same head diameter (164 px). |
| `lookdev.png` | The deliverable sheet. |
| `out/ld_*.png` | Full 720x1280 renders: `ld_{kong,crew,driver}_{front,q,side}`, `ld_kong_wet_{front,q}`, `ld_driver_{seated,head_lift,lunge}`, `ld_props` (1280x720) and `ld_kong_night`. |
| `out/measure_all.json`, `out/measure_extras.json` | Numbers measured from the renders (see below). |
| `tex/` | Generated textures. `phone_screen_v4.png` is copied from `v4/cast_dz09/out/phone_screen.png`; its Thai is shaped with raqm and verified there. |

## Units and conventions

1 BU = 1 D = head diameter = 0.6 m. This is the same scale as `v4/set_expressway`, so the characters drop straight into the set.
The feet sit at the root origin. Z is up and the front faces -Y.
The character's right is -X, which is screen-left in a front view. The flag patch is on that side, like the sheet.

## Quick start

```python
import sys; sys.path.insert(0, PROJ + "/v6/cast")
import cast6 as C
# optional, inside the expressway set: give cloth, limbs and hair the set's ambient term
#   import kit; C.AMBIENT[:] = kit.AMBIENT        (do this BEFORE building characters)
k = C.Character("kong", wet=True, expr="determined", separator=True)   # kind: kong | crew | driver
cut = C.Cutter(bars=3, wet=True, scale=1.3)
k.hold(cut, "r", fwd=(0, -0.3, -1), up=(0, -1, 0.3))   # jaws down and forward, gauge facing the viewer
k.preset("kong_hold_cutter")
k.place((x, y, 0), facing_deg=0)          # 0 faces -Y; +90 faces +X (screen-right)
k.set_face("alarmed")                     # swaps the decal; the sweat drop shows automatically
cut.set_bars(1)                           # green 3, yellow 2, red 1, 0 = all off
k.set_pass_index(2)                       # set post: 2 = actor (kept sharp)
```

`Character(kind, name=None, wet=False, expr=None, coll_=None, ink=True, separator=False)`

- `wet=True` gives a darker jacket atlas (`#c8581b`), a low coat on the cloth (0.15, roughness 0.35), on the hair (0.15 / 0.35), on the limbs (0.08 / 0.5) and on the boots. There is still no shine on the head.
- `separator=True` adds a pale hull 0.008 D outside the ink (`#9aa3b8` at 0.6 emission). Use it against the dark night sky (spec: "pale 1 px separator").
- Each call builds new objects into collection `CAST6`, named after `name`. Pass `name=` when a scene has two of the same kind.
- `k.objects` lists every object, hulls included. `k.inks` lists the ink hulls. `k.head`, `k.bean`, `k.hair`, `k.limbs[...]`, `k.hands[...]`, `k.boots[...]`, `k.root` and `k.body` (the hip pivot) are also exposed.

`pose(lean=(fwd, side, twist), head=(yaw, pitch_up, roll), arm_r=..., arm_l=..., legs=..., drop=None, bob=0, expr=None)`

- All angles are in degrees.
- `lean` rotates the whole upper body (bean, head, pack, arms) about the hips.
- `head` rotates the sphere about its own centre. Positive yaw turns toward the character's left (screen-right). The face decal turns with it. There is no view-bin swap.
- Arms take one of three forms:
  - A preset from `ARM_PRESETS`: `down hold_cutter phone_look phone_ear point raise reach claw guard lap wheel hips shout`.
  - `dict(hand=(x, y, z), pole=(...))` in body space, relative to the hip pivot and before lean. It is written for the left side and mirrored for `arm_r`.
  - `dict(hand_root=(x, y, z))` in root space.
- Legs take a preset from `LEG_PRESETS` (`stand wide step lunge crouch seated`) or a dict with `ankle_r/ankle_l/knee/drop/seat`. `seated` puts the bean bottom at `seat` (0.62 D by default; set it to the car seat height).
- Limbs are 3-point auto-handle bezier tubes. They always bend in one smooth arc of their true length, so there is never a sharp elbow or knee.
- `bob` raises or lowers the bean, for the 0.05 D walk bob.

`preset(name)`. Presets in `PRESETS`:

| preset | what |
|---|---|
| `kong_idle` | arms down |
| `kong_hold_cutter` | the sheet pose: cutter in the right hand, jaws down |
| `kong_phone` | guilty face, looking down at the phone |
| `kong_shout` | shouting |
| `kong_alarmed` | alarmed |
| `crew_idle` | crew at rest |
| `crew_shout` | crew shouting |
| `crew_scared` | crew scared |
| `driver_stand` | driver standing |
| `driver_seated` | still face, head hanging |
| `driver_head_lift` | white eyes, head up |
| `driver_lunge` | biting mouth, leaning forward 30 deg, claws forward |

`hold(prop, hand="r"|"l", fwd, up, offset)`: `fwd` and `up` are in root space. The prop follows the hand on every `pose()`.

`set_head_light(emit_mix=None, emit_str=None)`: tunes the self-lit head for each shot (see "Head lighting").

`proportions()`: returns the construction numbers.

Expressions (`faces6.EXPRS`):

| who | expressions |
|---|---|
| Kong | `determined neutral tired guilty alarmed shouting blink`. `alarmed` and `guilty` show the sweat drop. |
| crew | `neutral shouting scared blink`. `scared` shows the sweat drop. |
| driver | `still head_lift lunge` |

Props:

- `Cutter(name, bars, wet, scale)`: orange body, black D-handle and grip, a battery pack with the emissive gauge on top, a black collar, and two steel crescent jaws opened in a V.
  - The grip is at the origin and the jaws point toward +Y.
  - It is not inked. Props stay plain PBR, as in ref D.
  - Use `scale=1.3` next to Kong. That makes it about 1.1 D long, matching the sheet.
- `Phone(name, screen=None, wet)`: a 0.13 x 0.26 D slab.
  - The screen faces -Y and shows `tex/phone_screen_v4.png`: Namnuea's photo and "น้ำเหนือ — 4 สายที่ไม่ได้รับ".
  - Pass `screen=` with another PNG to change it.
  - For an insert, scale `phone.root` to about 2.2.

## How it is built (ref D section 5, numbers in D)

| part | construction |
|---|---|
| Head | UV sphere 64x32, D 1, scale (1, 0.97, 0.98). It sits on the bean with a 0.05 D overlap. There is no neck. |
| Head shader | Mix of Diffuse(C) and Emission(C x lavender (0.84, 0.80, 0.92) x AO remapped 0.78..1, AO distance 0.08 D). The emission share is `HEAD_EMIT_MIX` = 0.60. There is no specular. |
| Face | Decal in angular sphere coordinates: u = 0.5 + theta/126 deg, v = 0.5 + phi/126 deg. It is computed in the shader from object coordinates, so it wraps and foreshortens with the sphere. |
| Face sizes | eyes are lidded half-ovals 9.2 x 5.7 deg (0.08 x 0.05 D); brows are bars 0.17 x 0.035 D; the mouth arc is 0.12 D; the open mouth is 0.16 x 0.11 D in `#8E2430` with a `#E9868F` tongue; ring eyes have a dot pupil; Kong's stubble is 25 dots of 0.01 D at 50 % grey |
| Hair | A scalp shell (r 0.507, solidified 0.03, with a jagged fringe hairline) plus flat jagged tufts. Each tuft is a flattened pyramid 0.045 D thick, wide along the azimuth, rooted in the scalp, arranged in 5-6 rings. |
| Hair finish | The highest tip is 0.21-0.23 D above the crown (v5 was 0.54). Matte `#141418`, roughness 1, specular 0, with painted stroke texture in box projection. Inked. A 0.015 D ink line is drawn along the hairline. |
| Crew hair | very dark brown `#231915`, swept to the character's right, with a long side fringe of 4 tufts lying over the forehead |
| Driver hair | thin and receding, `#3a3836` |
| Bean | Superellipse lathe, p 2.3, bottom 5 % wider. Kong is 1.12 W x 1.45 H x 0.85 depth ratio; the crew is 1.09 x 1.40; the driver is 1.14 x 1.40. |
| Jacket | One cloth over the whole bean, from a cylindrical atlas: orange `#E8732A` (wet `#C8581B`); a black hem band of 0.14 D, which reads as the trousers, with a belt and buckle; two silver bands `#C8CCD3` (mask gives roughness 0.5 and specular 0.3: retro-reflective, not chrome); zip, pockets and side seams at half ink weight; a RESCUE patch on the chest (screen-right); the Thai flag on the upper screen-left side; backpack straps as raised bands |
| Cloth shader | Principled with roughness 0.85, specular IOR level 0.15, sheen 0.25, 2 % painted noise, soft fold strokes, and a fine noise bump. The driver wears a light-blue shirt atlas: a loosened red tie, a V collar, a jagged torn hem over grey trousers, two small rips and stains. |
| Limbs | Bezier tubes of radius 0.028 D (0.056 thick) in `#18171C`, roughness 0.9, specular 0.1. Legs 1.06-1.13 D, arms 0.93-0.95 D. |
| Hands, boots | Hands are balls of r 0.042. Boots are ovals 0.16 x 0.25 x 0.12 in `#1B1D26`, roughness 0.8, with a grey sole. The driver's hands are skin-coloured balls with 3 small claws. |
| Backpack, radio | The pack is a rounded box 0.75 x 0.32 x 0.85 in `#33343B` with a pocket, inked. The radio is a small inked box with an antenna on the screen-right chest strap. |
| Ink | A camera-only inverted hull of the evaluated mesh, displaced along the normals and flipped. Its material is Backfacing ? transparent : emission `#160f12`. It is invisible to shadow, diffuse and glossy rays, so it never darkens the AO or the lighting. |
| Ink thickness | world space: `INK_HEAD` = 0.025 D, `INK_BODY` = 0.021 D (bean, hair, pack), pocket and radio 0.012, sweat 0.010 |
| Head/bean line | An ink tube is drawn along the head/bean intersection. An inverted hull cannot draw the head outline where the head sits in front of the bean. |
| Props | no ink |

## Head lighting (important when dropping into a shot)

The head is about 60 % self-lit, so its falloff stays at or below 18 % under a soft key, as in ref D.
Under the expressway's hard sodium key (see `lookdev.py scene("night")`), the measured drop was 11.5 %.
If a scene's key is much stronger than about 1000 W area or 2.5 sun, raise the self-lit part per shot with `k.set_head_light(emit_str=1.3)`. If the heads look like glowing paper, lower it (0.8).
The body is not self-lit and takes the full scene light. Its shadow side needs the sky/moon fill (spec: fill 60 % or more of the lit side).

## Measured (from `out/measure_all.json` / `measure_extras.json`, 720x1280, front view, head D = 163.7 px)

| quantity | Kong | crew | driver | ref D target |
|---|---|---|---|---|
| head / body width | 0.893 | 0.917 | 0.877 | 0.83-0.92 |
| bean height (D) | 1.45 | 1.40 | 1.40 | 1.40-1.48 |
| legs (D) | 1.10 | 1.12 | 1.05 | 1.0-1.2 |
| crown to sole (D) | 3.49 | 3.46 | 3.39 | 3.4-3.6 |
| hair above crown (D) | 0.23 | 0.14 | 0.10 | at most 0.22 (v5: 0.54) |
| head share of height | 0.287 | 0.289 | 0.295 | about 0.29 (v5: 0.43) |
| limb thickness (D) | 0.056 | 0.056 | 0.056 | 0.045-0.06 |
| ink, measured FWHM on render | 4.1 px = 2.49 % D | 3.9 px = 2.41 % | 3.95 px = 2.41 % | 2.3-2.5 % D |
| head lit to shadow (soft key) | (242,235,234) to (199,194,201), **17.2 %** | 17.3 % | 17.4 % | 8-18 %, lavender shadow |
| head drop under the night sodium key | 11.5 % | | | 18 % or less |
| body lit to shadow | (235,127,73) to (138,88,69), **34 %** | 35 % | 42 % | 30-40 % |
| legs: median L / p95 L | 16 / 18 | 26 / 27 | 26 / 27 | 24-26 / 66 (v5 p95: 118) |
| glove hand: max L | 24 | 25 | (skin hand) | no highlight (v5: 255) |
| full figure on the lookdev frame | 565 px = 0.44 H at head D 164 px | | | ref MS 0.34-0.47 H, head 150-166 px |

Render cost at 720x1280, 32 spp + OIDN, 4 threads, soft lookdev set: 11-13 s per frame (Kong with the cutter: about 12-22 s). In the expressway set the set dominates.

## Gaps / known limits

- **Hair from the side and back** reads as a smooth black helmet with spikes on top and at the rim, because tufts over the black cap are black on black. Ref D hats carry painted hatch strokes. Our stroke texture is there (about 10 % contrast) but barely visible under dim light. It could be pushed if the hair needs inner detail at MCU.
- **Kong's sheet details not carried over**:
  - The sheet has orange sleeves with bands, cargo pockets, knee pads and big boots. Ref D construction uses black stick limbs, so the uniform lives only on the bean: the flag moved from the sleeve to the upper screen-left side of the bean.
  - The trousers are a 0.14 D black hem band plus black legs. This is a deliberate choice from the spec.
- **The ink is an inverted hull**:
  - Overlaps such as the head in front of the bean need the drawn join tube.
  - An arm crossing in front of the bean has no outline. That is fine because the arm is ink-black anyway.
  - Inner seams are painted into the atlas, so their weight scales with the texture and not with the screen.
- **Driver**:
  - The seated thighs are hidden inside the bean, so only the shins show, like the ref's sitting puppets.
  - The torn hem and rips are painted, not modelled.
  - The lunge reads through the lean, the face and the forward claws. It has no stretch or squash.
  - The car seat height must be passed with `legs=dict(LEG_PRESETS["seated"], seat=<cushion z>)`.
- **Head self-lighting is per scene**. The 60 % emission share was calibrated here (17 % drop under soft light, 11.5 % under the hard night key). In very dark shots the heads will glow. Use `set_head_light`.
- **Night body falloff**: on the night check, the bean's shadow side fell 76 %, because the test had no sky bounce. The spec's floor (shadow side at least 60 % of the lit side) has to come from the set's sky/moon fill and AO, not from the characters.
- **No rig, no walk cycle yet**. `pose()` is a procedural pose function. For animation, keyframe `pose()` per frame (limb curves are rebuilt from points). A noodle-walk helper with a 0.05 D bob and head-shake motion blur (shutter 0.5) still has to be written.
- **Cutter**: the gauge is 0.16 x 0.066 D on top of the battery (0.21 x 0.086 D at scale 1.3). It reads in a macro insert and only as a coloured dot at the full figure.
- **The crew member and the driver are not on the character sheet**. The crew keeps v4's "dark-brown swept fringe"; the driver keeps v4's pale grey-green skin, light-blue shirt and red tie.
