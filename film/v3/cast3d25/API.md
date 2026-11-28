# cast3d25/toon25.py: film-25 cast as 3D toon characters (first pass: general25 and tommy_a25)

This module uses bpy only. Everything is procedural and nothing else is edited. It keeps our cast25 designs and colours.
Units: 1 D = one head diameter (the set's units). The root empty sits at the feet, and the character faces local -Y.

```python
sys.path.insert(0, PROJ + "/v3/cast3d25"); import toon25 as T
gen = T.build_general("gen")          # Char
tom = T.build_tommy("tom")
gen.root.location = feet_xyz; gen.root.rotation_euler = (0, 0, yaw)  # yaw = atan2(dx, -dy) faces the direction (dx, dy)
gen.set_pose("point_stick", shoulder_r=(62, 8, 0))                  # preset + per-joint overrides
gen.set_pose("walk", phase=0.25); gen.set_pose("march", phase=0.5)
gen.set_mouth("talk_b")                                             # talk_a | talk_b | talk_o | flat | laugh
```

## Build

| part | general25 | tommy_a25 |
|---|---|---|
| **body** | a lathe "bean": radius profile from the hip to the collar, plus a forward belly bulge | a slim lathe body |
| **uniform** | PIL texture on the body UV, which is cylindrical (u 0.5 = front, v 0 = hip line): collar, Sam Browne belt and buckle, 4 brass buttons, scarlet sash (screen-right shoulder to screen-left hip), gorget tabs, one block of 12 plain ribbons | PIL texture: buff webbing belt and braces, pouches, buttons, red muffler |
| **hat** | peaked cap: flat-topped olive crown, broad scarlet band, black peak, brass button | Brodie: a flattened dome and a wide brim, drab green #5f8c2a |
| **limbs** | khaki sleeves, tall brown boots | khaki sleeves, puttee-coloured shins |
| **prop** | swagger stick (wood and a brass knob), a child of the right hand, continuing the forearm line | none |

- **Head:** a sphere 0.5 D across, scaled (1, 0.92, 0.96). Its base colour is #fef7f6.
- **Face decal:**
  - The decal is projected from the front: object coords x, z become uv on the y < -0.05 half.
  - The decals are cast25's own faces: `face_decal()` rasterises the puppet head (no hat, finish off) through `v3/set3d/raster.js`.
  - Alpha is the distance from the skin colour, clipped inside 0.80 of the head disc, so only the eyes, brows, cheeks, moustache strands and mouth remain.
  - The decals are cached in `decals/`. The general uses the expression smug and the Tommy determined; the "laugh" decal uses laughing.
- **Limbs:**
  - Capsules on joint empties: shoulder → elbow → hand sphere (dark mitt), and hip → knee → boot blob.
  - The joints are `shoulder_r/l`, `elbow_r/l`, `hip_r/l` and `knee_r/l`. The character's right side is -X, which is screen-left in a front view.
- **Pose values:** `(forward, out, twist)` in degrees.
  - forward + swings a hanging limb to the front; negative knee values bend the knee back.
  - out + swings the limb away from the body on either side.
  - The presets in `POSES` are stand, point_stick, laugh, walk(phase) and march(phase).
- **Shading:** Principled shaders, roughness about 0.5, a light sheen and a low specular, lit by the scene sun (real terminator, cast shadows and contact).
- **Outline:** an inverted hull. A Solidify modifier (thickness 0.018 D, which is 1.8 % of the head, offset +1, flipped normals) uses the outline material: emission #3a2832 on the hull's front faces and transparent on its back faces (Cycles has no backface culling). Camera rays only, so the outline casts no shadow.

## First still (film25/gate)
- `motion/char3d.py` and `motion/char3d_post.py` make `char3d.png`, `char3d_tommy.png` and `char3d_vs_R11.jpg`.
- **Grade:** the background takes the gentle grade. The characters are masked out of it (a character-only, film-transparent pass) and get one exposure gain, so that the lit forehead reads #fef7f6.

## Known limits (first pass)
- There is no skinning. Limbs are rigid capsules meeting at spheres-ish ends, the elbows show seams, and the hands are mitts with no fingers.
- The face decal is flat-projected: it stretches toward the sides in a 3/4 view. The walrus moustache is only its ink strands (its white fill equals the skin), so it reads weaker than on the card.
- The cap crown is a simple frustum. Medals are a texture block.
- The poses are hand-set. There are no presets for the rest of the cast yet.
