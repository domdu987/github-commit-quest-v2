# bpy 5.3.0 implementability audit of LOOK_SPEC.md

Audited file: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/spec/LOOK_SPEC.md` (not edited), plus the two helper modules it calls, `lightkit_clp.py` and `grade_compositor.py`, and the keyframe helper it cites from `camera_motion.md` 3.3.

Environment: `bpy 5.3.0` as a Python 3.13 module, 4 CPU cores, no GPU, no display, `libEGL` absent (apt cannot install it), Xvfb + Mesa llvmpipe (OpenGL 4.5) present.

Method: every API call named in section 2 was executed in bpy 5.3.0 by a script that does not render; where a row also quotes a number from a rendered frame it says so. Scripts, logs and outputs are in `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/verify_api/` (`t01_*.py` to `t11_*.py`, `logs/`, `corrected_snippets.py`, `r_timing.py`, `out/`).

Renders used: three `bpy.ops.render.render` calls in total, the allowed maximum. Two completed (720x1280, 16 samples, denoise on, sphere + plane + one sun, with and without Freestyle). One aborted after 3 s: the first Freestyle attempt, started without a display. No other render was run, so anything marked "not rendered" below rests on a non-rendering check or on a measurement taken from the two completed frames.

Status words: WORKS = the call runs in 5.3.0 and does what the spec says. WORKS, CHANGE = runs, but the spec's values give a different result from the one the spec expects; the corrected snippet is given. FAILS = does not do what the spec says in 5.3.0.

---

## 1. What a builder has to change

| # | Problem | Fix |
|---|---|---|
| 1 | A render with Freestyle enabled kills the Python process (SIGABRT, exit 134, no Python exception) when there is no display. Freestyle draws its strokes through a GL context, and here that only exists under Xvfb. | Start every process that renders with Freestyle as `xvfb-run -a -s "-screen 0 1280x1024x24" python3 script.py`. Cycles without Freestyle needs no display. |
| 2 | `bpy.context.preferences.edit.keyframe_new_interpolation_type = 'SINE'` before keying has no effect on `keyframe_insert`: keys come out `BEZIER` / `AUTO`. | Use the helper (set `interpolation` and `easing` on each keyframe point). It works; see 5.6. |
| 3 | `lit` material, Diffuse BSDF roughness 1.0 is Oren-Nayar, not Lambert. The sunlit floor of the test frame reads 0.95 to 1.35 times `albedo x (A + K cos)` depending on where it is in frame. | `Roughness = 0.0`. |
| 4 | `lit` material, emission sampling. With the default `'AUTO'` the ambient emission of one surface lights its neighbours: the shadow next to the test sphere reads 1.07 to 1.36 times `albedo x A`. | `material.cycles.emission_sampling = 'NONE'` on every `lit`, `painted`, `ink` and card material. Not re-rendered. |
| 5 | Inverted hull, geometry. With the spec's four Solidify fields a box hull sticks out 0.0087 for `thickness = 0.015`, so a 3 px line draws about 1.7 px. | Add `use_even_offset = True` (0.0150). |
| 6 | Inverted hull, shader. A ray leaving the prop toward the sun meets the hull on its front face, where the spec's mix selects the opaque ink Emission, so the hull is expected to shade its own prop from the sun and from lamps. Shown by a ray-side check on the evaluated mesh, not rendered. | Make the hull transparent to every ray that is not a camera ray: factor = max(Backfacing, 1 - Is Camera Ray). See 5.3. |
| 7 | Freestyle line sets. The view layer already carries a default `LineSet` (silhouette + border + crease on every object, black, 3 px); in an empty file its line style is `None`. `render.line_thickness` is a unit that multiplies `linestyle.thickness`. | Remove the default line sets, create one, keep `render.line_thickness = 1.0`, put the pixel width in `linestyle.thickness`. See 5.4. |
| 8 | Depth plate by `material_override`: the override replaces every material, so alpha cut-out cards turn into solid rectangles, and pixels with no geometry stay at the world's 0, which reads as nearest (both follow from how the override works; not rendered). | Take the Depth pass from the plate render itself. That route was verified on the test frame. See 5.5. |
| 9 | `scene.compositing_node_group` works in 5.3.0 but is itself deprecated there ("expected to be removed in Blender 6.0"). | Optional: `scene.compositor_effects.new(name=...)`, then `.node_group = group`. See 5.2. |
| 10 | `world_to_camera_view` returns y measured from the bottom of the frame. | `y_px = (1 - y) x 1280`. |
| 11 | `bmesh.ops.create_cube(..., calc_uvs=True)` and the other bmesh primitives write no UV layer unless one exists. | `bm.loops.layers.uv.new('UVMap')` first, or use `bpy.ops.mesh.primitive_*_add`, which create `UVMap`. |

Only item 1 stops a build. Items 2 to 8 run without error and give a result the spec does not intend.

---

## 2. Instruction by instruction

### 2.1 Process and engine

| # | Spec | Instruction | Result | Detail, corrected snippet |
|---|---|---|---|---|
| 1 | header, 4.2 step 1 | Cycles, CPU, 4 threads, headless module | WORKS | `scene.render.engine = 'CYCLES'` (the static enum lists only `BLENDER_EEVEE`; `'CYCLES'` is accepted). `scene.cycles.device = 'CPU'`. `scene.render.threads_mode = 'FIXED'; scene.render.threads = 4`. Rendered without a display. |
| 2 | section 0, 3.1 | Freestyle build flag | FAILS without a display, WORKS under xvfb-run | `bpy.app.build_options.freestyle` is True. `gpu.init()` aborts the process without a display (exit 134) and returns in 0.83 s under `xvfb-run` (llvmpipe). The Freestyle render completed under `xvfb-run`. |

### 2.2 Colour management and render settings (4.2 step 1)

| # | Instruction | Result | Detail |
|---|---|---|---|
| 3 | view transform `Standard`; default is `AgX` | WORKS | `scene.view_settings.view_transform = 'Standard'`. The factory default is `'AgX'`, as the spec says. Also valid: `'Raw'`, `'Filmic'`, `'Khronos PBR Neutral'`. |
| 4 | look `None`, exposure 0.0, gamma 1.0 | WORKS | `view_settings.look = 'None'` (the string), `.exposure`, `.gamma`. |
| 5 | display sRGB | WORKS | `scene.display_settings.display_device = 'sRGB'`. |
| 6 | samples 48 / 16, adaptive sampling on | WORKS | `scene.cycles.samples`, `scene.cycles.use_adaptive_sampling = True` (threshold 0.01, minimum 0 by default). |
| 7 | OpenImageDenoise on for plates | WORKS | `scene.cycles.use_denoising = True; scene.cycles.denoiser = 'OPENIMAGEDENOISE'`. Both frames rendered with it, no warning. |
| 8 | `max_bounces` 1, `diffuse_bounces` 0, `glossy_bounces` 1, `transmission_bounces` 0, `volume_bounces` 0, `transparent_max_bounces` 8 | WORKS | all on `scene.cycles`. |
| 9 | caustics off, `sample_clamp_indirect` 3 | WORKS | `caustics_reflective = False; caustics_refractive = False; sample_clamp_indirect = 3.0`. |
| 10 | film not transparent, default pixel filter, no motion blur | WORKS | `scene.render.film_transparent = False`; `scene.cycles.pixel_filter_type` is `'BLACKMAN_HARRIS'`, width 1.5; `scene.render.use_motion_blur` is False by default. |
| 11 | world black, strength 0 | WORKS | After `read_factory_settings(use_empty=True)` `scene.world` is `None`; create one. A new world already has a node tree with `Background` and `World Output`. `World.use_nodes = True` still runs and warns "expected to be removed in Blender 6.0". Snippet 5.1. |
| 12 | `lightkit_clp.setup_render(scene)` | WORKS | runs as written. |
| 13 | 720x1280, 30 fps, 1950 frames, larger plates | WORKS | `render.resolution_x/y`, `resolution_percentage`, `render.fps = 30`, `scene.frame_end = 1950`. |

### 2.3 Lights (4.2 steps 2 and 3)

| # | Instruction | Result | Detail |
|---|---|---|---|
| 14 | Sun `energy`, `color`, angle 1.5 deg | WORKS | `light.energy`, `light.color`, `light.angle = math.radians(1.5)`. |
| 15 | Elevation and azimuth convention, key from camera-left so shadows fall to screen right and away | WORKS | `rotation_euler = (radians(90 - elev), 0, radians(az))` gives the travel direction (0.646, 0.452, -0.616) for 38 / -55. In the rendered frame the shadow falls to screen right and away. |
| 16 | Sun `energy = pi x max(K)` | CONSISTENT, not exact as rendered | Sunlit floor = 0.95 to 1.35 times the prediction, the spread coming from row 20. The white-card test of 4.3 should be done with roughness 0, or it will read a view-dependent value and the sun will be rescaled wrongly. |
| 17 | Point lamp `energy = g x 4 pi^2 d^2`, colour, radius 0.05 | WORKS (API) | `light.energy`, `light.color`, `light.shadow_soft_size = 0.05`. The formula was not rendered. |
| 18 | `lightkit_clp.add_sun`, `add_lamp`, `set_world`, `apply_preset` | WORKS | run as written; `set_world` and the materials emit the `use_nodes` deprecation warning. |

### 2.4 Materials and shader nodes (3.1, 2.1, 3.3)

| # | Instruction | Result | Detail, correction |
|---|---|---|---|
| 19 | `lit` = Diffuse BSDF + Emission through Add Shader; `lightkit_clp.env_material(name, albedo_hex, A, image=...)` | WORKS | `ShaderNodeBsdfDiffuse`, `ShaderNodeEmission`, `ShaderNodeAddShader`, `ShaderNodeMix` (`data_type='RGBA'`, `blend_type='MULTIPLY'`), `ShaderNodeTexImage`. Built with and without an image, rendered. |
| 20 | Diffuse BSDF "roughness 1" | WORKS, CHANGE | Roughness above 0 switches Cycles to Oren-Nayar. Measured on the flat sunlit floor: red 0.96 to 1.35 and green 0.95 to 1.26 times `albedo x (A + K sin(50 deg))`, darker at screen left, brighter at screen right. Use `dif.inputs['Roughness'].default_value = 0.0` so the spec's formula and every "predicted" colour hold. Not re-rendered at 0. |
| 21 | Ambient as emission: "shade is exactly albedo x A, noise-free" | WORKS, CHANGE | Measured in the sphere's shadow: 1.32 to 1.36 times `albedo x A` beside the sphere, 1.07 to 1.14 at the far end. Something lights the shadow that the model does not contain; with `diffuse_bounces = 0` the only candidate is the sphere's emission (0.09, 0.19, 0.73) being sampled as a light. Set `material.cycles.emission_sampling = 'NONE'` ("Do not use this surface as a light for sampling"; the default `AUTO` decides "based on estimated emission intensity"; other values `FRONT`, `BACK`, `FRONT_BACK`). Not re-rendered. |
| 22 | `painted` = Emission only, strength 1.0 | WORKS | same node; set `emission_sampling = 'NONE'` here too, or a 4.2 x 2.6 D emissive map can light the desks in front of it. |
| 23 | `emitter` = Emission strength 8 (`lightkit_clp.emissive_material`) | WORKS | Under `AUTO` a strength-8 bulb is expected to light the room as well as its paired point lamp (not rendered). Decide which one is the light; `'NONE'` keeps the point lamp as the only one. |
| 24 | `ink` hull: Solidify `offset` 1, `use_flip_normals` True, `use_rim` False, `material_offset` 1 | WORKS, CHANGE | All four exist. Evaluated box: 6 extra faces, material index 1, normals inward. The object needs two material slots. Outward offset for `thickness = 0.015`: 0.0087 on a box and 0.0109 on a cylinder with the default `use_even_offset = False`; 0.0150 and 0.0151 with `use_even_offset = True`. Add it. |
| 25 | `ink` slot 2 = Mix Shader by Geometry > Backfacing between ink Emission and Transparent BSDF | WORKS (API), CHANGE | `ShaderNodeNewGeometry` output `'Backfacing'`, `ShaderNodeMixShader`, `ShaderNodeBsdfTransparent` exist. Ray-side check on the evaluated hull: a camera ray meets the hull's back face first (transparent, correct); a ray from the prop's top face toward the sun meets the hull's front face (`normal . ray = -0.77`), where the mix gives the ink Emission, which is opaque to shadow rays. The prop therefore gets no sun and no lamp light. Fix in 5.3. Not rendered. |
| 26 | Optional Glossy mix 0.1 to 0.3, roughness 0.25 | WORKS | `ShaderNodeBsdfGlossy` (`'Roughness'`), `env_material(..., gloss=0.2)` builds. |
| 27 | `lightkit_clp.character_material` (fallback cards) | WORKS | `ShaderNodeLightPath` output `'Is Camera Ray'`, alpha into the Mix Shader factor. |
| 28 | Socket key `'Fac'` used by the kit | WORKS | The socket is now displayed as "Factor" but `inputs['Fac']` and `outputs['Fac']` still resolve (Mix Shader, Noise, Wave, Gradient, Color Ramp, Hue/Saturation). `'Factor'` resolves too. |
| 29 | `ShaderNodeMix` colour sockets by index | WORKS | factor `inputs[0]`, A `inputs[6]`, B `inputs[7]`, result `outputs[2]`, in shader and compositor trees. |
| 30 | No Principled BSDF | note | `bpy.data.materials.new()` already contains `Principled BSDF` + `Material Output`; delete the nodes before building. `Material.use_nodes` is deprecated and assigning False does nothing. |
| 31 | Sand: Noise (scale 0.4, detail 4) into a ramp, Wave bands (scale 1.5, distortion 3), Camera Data > View Distance tint | WORKS | `ShaderNodeTexNoise` (`'Scale'`, `'Detail'`), `ShaderNodeValToRGB` (`color_ramp.elements.new(pos)`), `ShaderNodeTexWave` (`wave_type='BANDS'`, `bands_direction`, `'Scale'`, `'Distortion'`), `ShaderNodeCameraData` (`'View Distance'`), `ShaderNodeMapRange`. Graph built into the `lit` material, 15 links valid. |
| 32 | Sea: Wave bands through a narrow ramp step, mixed at 0.6, matte | WORKS | same nodes; ramp `interpolation = 'CONSTANT'` is available for the step. |
| 33 | Sky as an emissive card or dome with a gradient, never the Sky Texture node | WORKS | UV.y into a 4-stop Color Ramp into Emission builds; an SVG gradient image works the same way. |
| 34 | Additive shaft and glow cards | WORKS | Add Shader(Transparent BSDF, Emission) builds. |
| 35 | SVG rasterised to PNG as textures, 512 to 2048 px | WORKS | `bpy.data.images.load(path, check_existing=True)`: colour space `sRGB`, `alpha_mode` `STRAIGHT`. For data images use `colorspace_settings.name = 'Non-Color'`. `ShaderNodeTexImage.extension` in `REPEAT`, `EXTEND`, `CLIP`, `MIRROR`; `.interpolation` in `Linear`, `Closest`, `Cubic`, `Smart`. |
| 36 | Image sequence textures (animated sprites on the fallback cards) | WORKS | `image.source = 'SEQUENCE'`; on `node.image_user`: `frame_duration`, `frame_start`, `frame_offset`, `use_auto_refresh = True`. On the evaluated material, scene frame f shows file number f - frame_start + 1 + frame_offset (checked: frames 1, 3, 5 give files 0001, 0003, 0005; start 10 with offset 2 gives 0003 at frame 10). The original (unevaluated) `image_user.frame_current` stays 0; that is not an error. |
| 37 | UVs for textured boxes and cards | WORKS, CHANGE | section 1, item 11. |

### 2.5 Geometry (3.1 to 3.3)

| # | Instruction | Result | Detail |
|---|---|---|---|
| 38 | Boxes, cylinders, planes, cones, spheres, cards | WORKS | `bpy.ops.mesh.primitive_cube_add / cylinder_add / plane_add / cone_add / uv_sphere_add` run in the headless module; `bmesh.ops.create_*` and `mesh.from_pydata` work. `Mesh.use_auto_smooth` no longer exists; use `mesh.shade_smooth()` or per-face `smooth`. |
| 39 | Sand plane with 64 x 64 subdivisions | WORKS | `bpy.ops.mesh.primitive_grid_add(x_subdivisions=64, y_subdivisions=64, size=300)` gives 4225 vertices. |
| 40 | Displace (Clouds, scale 6 D) | WORKS | `tex = bpy.data.textures.new('dunes', 'CLOUDS'); tex.noise_scale = 6.0`; `mod = ob.modifiers.new('dunes', 'DISPLACE'); mod.texture = tex; mod.strength = 0.3; mod.direction = 'Z'; mod.texture_coords = 'LOCAL'`. Evaluated mesh displaced. |
| 41 | Dune band only 15 to 40 D inland | WORKS | second Displace with `mod.vertex_group = 'dune_band'`. |
| 42 | Wire curves sagging 0.7, 1.3 px thick; lamp cords | WORKS | `cu = bpy.data.curves.new('wire', 'CURVE'); cu.dimensions = '3D'`; `sp = cu.splines.new('BEZIER'); sp.bezier_points.add(2)`; `cu.bevel_mode = 'ROUND'; cu.bevel_depth = r; cu.bevel_resolution = 2; cu.use_fill_caps = True`. `bevel_depth` is a radius: for w px at distance d use `r = 0.5 x w x d / 782.2`. |
| 43 | Scatter as instances | WORKS | objects sharing one mesh (`bpy.data.objects.new(name, mesh)`), or an empty with `instance_type = 'COLLECTION'; instance_collection = coll`. |

### 2.6 Freestyle (3.1), plates only

| # | Instruction | Result | Detail |
|---|---|---|---|
| 44 | `select_by_collection` | WORKS | `ls.select_by_collection = True; ls.collection = coll; ls.collection_negation = 'INCLUSIVE'`. Used in the rendered Freestyle frame. |
| 45 | silhouette + border + crease | WORKS | `ls.select_by_edge_types = True; ls.select_silhouette = ls.select_border = ls.select_crease = True`. Crease angle default 134.43 deg (`freestyle_settings.crease_angle`). |
| 46 | "3 px absolute" | WORKS | `scene.render.line_thickness_mode = 'ABSOLUTE'; scene.render.line_thickness = 1.0; ls.linestyle.thickness = 3.0`. Measured with unit 1.0 and `linestyle.thickness = 6.0`: 6 to 7 px. `render.line_thickness` is the unit ("Specify unit line thickness in pixels"; Freestyle logged `Unit line thickness : 1 pixel(s)`), so setting it to 3 as well would give 9 px; a unit other than 1 was not rendered. v1 set both to 2.2. Blender may also scale the unit by `resolution_percentage / 100`; not measured. |
| 47 | (not in the spec) default line set | CHANGE | section 1, item 7. `view_layer.use_freestyle` is True by default; `scene.render.use_freestyle` is False by default and is the switch to turn off for true-3D frames. |
| 48 | Ink colour `#2a1712` | WORKS | `linestyle.color` takes linear RGB. Lines are part of the image the compositor grades: `#2a1712` displays as `#31191f`. |

### 2.7 Compositor (4.2 step 5)

| # | Instruction | Result | Detail |
|---|---|---|---|
| 49 | How the compositor tree is created in 5.x | WORKS, deprecated | `ng = bpy.data.node_groups.new(name, 'CompositorNodeTree')`; `ng.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')`; a `NodeGroupOutput` node; `scene.compositing_node_group = ng`. `scene.node_tree` and `CompositorNodeComposite` no longer exist. In 5.3.0 `compositing_node_group` warns that it goes in 6.0; the 5.3 form is in 5.2 below. |
| 50 | Render Layers | WORKS | `CompositorNodeRLayers`, `.scene`, `.layer = view_layer.name`; outputs `Image`, `Alpha`, and `Depth` once `view_layer.use_pass_z = True`. |
| 51 | Glare: Type `Bloom`, Quality `High`, Threshold 1.0, Smoothness 0.1, Size 0.05, Strength 0.5, Saturation 1.0, Tint | WORKS | All are input sockets addressed by name. Menu sockets take the display strings: Type in `Bloom`, `Ghosts`, `Streaks`, `Fog Glow`, `Simple Star`, `Sun Beams`; Quality in `High`, `Medium`, `Low`. The old properties (`glare_type`, `quality`, `threshold`, `size`) are gone. |
| 52 | Color Balance, ASC-CDL: Offset (0.0075, 0.0035, 0.0095), basis 0, Power 1, Slope (1.000, 0.985, 0.970); "black renders `#150919`" | WORKS | `inputs['Type'].default_value = 'Offset/Power/Slope (ASC-CDL)'`. The index addressing in `grade_compositor.py` is right: 9 base offset, 10 colour offset, 11 base power, 12 colour power, 13 base slope, 14 colour slope. Rendered: the black world displays `#140918` to `#150919`. |
| 53 | Hue/Saturation/Value, Saturation 1.12 | WORKS | `CompositorNodeHueSat`, `inputs['Saturation']`. |
| 54 | Vignette chain (off through the preset) | WORKS | `CompositorNodeEllipseMask` (`'Size'`), `CompositorNodeBlur` (`'Type' = 'Gaussian'`, `'Size'` as a 2-vector, `'Extend Bounds'`), `ShaderNodeMath` (`MULTIPLY_ADD`), `ShaderNodeMix`. Built and executed with strength 0. |
| 55 | `grade_compositor.build(scene, preset={'vignette_strength': 0.0})` | WORKS | built (9 nodes, 8 valid links), executed in both rendered frames. Calling it again replaces the group of the same effect, it does not stack a second grade. |
| 56 | CPU compositor | WORKS | `scene.render.compositor_device = 'CPU'`. |
| 57 | Cost 0.3 to 0.4 s per frame | CONSISTENT | 0.46 s for the compositor plus two EXR writes plus the PNG in the timed frame. |
| 58 | `grade_compositor.build(scene, image=img)` (grade an existing image) | WORKS (API) | builds; not executed here. |

### 2.8 Depth plate and occlusion (2.10)

| # | Instruction | Result | Detail |
|---|---|---|---|
| 59 | `view_layer.material_override` | WORKS (API) | property exists and takes a material ("Material to override all other materials in this view layer"). Limits in section 1, item 8. Also turn Freestyle off for this render, and note that depths beyond 40 D clip to 1.0. |
| 60 | Emission of Camera Data > View Z Depth / 40 | WORKS (API) | `ShaderNodeCameraData` output `'View Z Depth'`, `ShaderNodeMath` `DIVIDE`. Not rendered. |
| 61 | 1 sample, no denoise | WORKS | `scene.cycles.samples = 1; scene.cycles.use_denoising = False`; or per layer, `view_layer.samples = 1`. |
| 62 | View transform `Raw`, 16-bit BW PNG | WORKS | `image_settings.file_format = 'PNG'; .color_mode = 'BW'; .color_depth = '16'`. Checked without rendering through `image.save_render`: linear 0.05, 0.1, 0.25, 0.5 are stored as 0.05000, 0.10001, 0.25000, 0.50001; under `Standard` they would be stored sRGB-encoded (0.248, 0.349, 0.537, 0.735). `render.dither_intensity` does not disturb 16-bit output. Set the view transform back to `Standard` afterwards. |
| 63 | `scene.render.use_compositing = False` | WORKS | property exists; restore it for the next plate. |
| 64 | (alternative) Depth pass from the plate render | WORKS, rendered | `view_layer.use_pass_z = True`, Render Layers `Depth` into a File Output node. The pass is planar camera depth, the same quantity as View Z Depth and as `world_to_camera_view().z`: bottom-left pixel 1.5085 (geometry predicts 1.5085 planar, 2.068 radial), sphere front 4.2077 (predicted 4.207), background 1e10. `view_layer.pass_alpha_threshold` (0.5) is described as "Z, Index, normal, UV and vector passes are only affected by surfaces with alpha transparency equal to or higher than this threshold", so cut-out cards should keep their shape; no card was in the test frame. Snippet 5.5. |
| 65 | Fallback: foreground plate with `film_transparent` | WORKS (API) | `scene.render.film_transparent = True`, PNG `color_mode = 'RGBA'`. |

### 2.9 Camera and anchors (2.10, 5.1)

| # | Instruction | Result | Detail |
|---|---|---|---|
| 66 | `lens = 22`, `sensor_width = 36`, `sensor_fit = 'AUTO'`: 782 px, 49.4 deg, 78.6 deg | WORKS | measured through `world_to_camera_view`: focal 782.22 px on both axes, 49.43 deg horizontal, 78.58 deg vertical. With `AUTO` on a portrait frame the 36 mm lies along the 1280 px side. `camera.data.angle_y` reports 57.2 deg and is not the vertical field of view. |
| 67 | `bpy_extras.object_utils.world_to_camera_view` | WORKS | returns x from the left (0 to 1), y from the bottom (0 to 1), z = planar depth in Blender units. |
| 68 | `D_px = 782.2 / z` | WORKS | z = 4 gives 195.6 px. |
| 69 | Per-frame anchor export | WORKS | `scene.frame_set(f)` then `world_to_camera_view`; the animated camera matrix is current after `frame_set`. |
| 70 | Never use Cycles depth of field | WORKS | `camera.data.dof.use_dof` is False by default. |

### 2.10 Animation (5.1, 5.3)

| # | Instruction | Result | Detail |
|---|---|---|---|
| 71 | "`action.fcurves` no longer exists" | CONFIRMED | actions are layered: `action.layers`, `action.slots`. |
| 72 | Set `preferences.edit.keyframe_new_interpolation_type` before keying | FAILS | the preference reads back `'SINE'` but `object.keyframe_insert` still writes `BEZIER` / `AUTO` keys on a new F-curve (value at a quarter of a 0-to-2 segment: 0.3125; sine in-out would give 0.2929). |
| 73 | Walk `action.layers[].strips[].channelbag(slot).fcurves` (helper of `camera_motion.md` 3.3) | WORKS | keys at 1 and 25 with `SINE` / `EASE_IN_OUT` evaluate to the sine in-out curve (0.1464 of the way at frame 7). `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot)` returns the same channelbag. The interpolation of a key governs the segment that starts at it. |
| 74 | Easing names for 5.3 | WORKS | `interpolation` in `CONSTANT`, `LINEAR`, `BEZIER`, `SINE`, `QUAD`, `CUBIC`, `QUART`, `QUINT`, `EXPO`, `CIRC`, `BACK`, `BOUNCE`, `ELASTIC`; `easing` in `AUTO`, `EASE_IN`, `EASE_OUT`, `EASE_IN_OUT`. Sine in-out = `SINE` + `EASE_IN_OUT`; cubic ease-out = `CUBIC` + `EASE_OUT`; quintic in-out = `QUINT` + `EASE_IN_OUT`. |
| 75 | Shake: random keys every 3 frames (or a noise modifier) | WORKS | `fcurve.modifiers.new('NOISE')` with `scale`, `strength`, `phase`; plain keys work as in row 73. |

### 2.11 Layers, visibility, passes (6.2), gates (6.3)

| # | Instruction | Result | Detail |
|---|---|---|---|
| 76 | Foreground layers rendered with `film_transparent` | WORKS (API) | row 65. Not rendered. |
| 77 | Other objects `visible_camera = False` so they still cast shadows | WORKS (API) | `object.visible_camera`, also `visible_diffuse`, `visible_glossy`, `visible_transmission`, `visible_volume_scatter`, `visible_shadow`. The 2.9x names (`object.cycles_visibility.*`) are gone. |
| 78 | `is_holdout`, `visible_shadow` | WORKS (API) | on the object; per collection: `view_layer.layer_collection.children[name].holdout`, `.exclude`, `.indirect_only`. |
| 79 | Shadow catcher (not used by the spec) | WORKS (API) | `object.is_shadow_catcher = True`; pass through `view_layer.cycles.use_pass_shadow_catcher = True`. |
| 80 | View layers and passes | WORKS | `scene.view_layers.new(name)` (a new layer has no line sets), `view_layer.use_pass_z`, `use_pass_mist`, `use_pass_object_index`, `use_pass_cryptomatte_object`, `view_layer.aovs.add()`, `view_layer.samples`. Two Render Layers nodes can address two view layers in one compositor group. |
| 81 | Gates: drop Freestyle, 12 samples without the denoiser, render at 540x960 | WORKS | `scene.render.use_freestyle = False`; `scene.cycles.samples = 12; scene.cycles.use_denoising = False`; `scene.render.resolution_percentage = 75`. |

---

## 3. Timing calibration

Scene: sphere (radius 0.5, 48 x 24) on a 40 x 40 plane, one sun (`EXTERIOR_NOON`), the spec's `lit` material, `setup_render` bounce settings, black world, 22 mm camera 4.7 D away, 720x1280, 16 samples, adaptive sampling on, OpenImageDenoise on, 4 threads, the grade compositor, PNG output plus two EXR files from a File Output node. Freestyle: one line set, silhouette + border + crease, 6 px.

| Run | Wall time of `render.render` | CPU time (user + system) | 1-minute load before, after |
|---|---|---|---|
| Without Freestyle (no display) | 7.08 s | 12.2 s | 2.2, 2.7 |
| With Freestyle (under xvfb-run) | 5.72 s | 15.8 s | 1.2, 1.8 |

The first Freestyle attempt, without a display, died 3.2 s after process start, at the moment Freestyle began stroke rendering: `Unable to initialize a Vulkan 1.1 instance`, then `Couldn't open libEGL.so.1`, then `Aborted`. No image was written.

The two wall times cannot be compared directly: other jobs shared the CPUs during the first run and less so during the second (`ps`, a minute before the first run, showed an ffmpeg at about 210 percent CPU and a Python job at 100 percent). Two load-independent readings:

- CPU time: Freestyle adds 3.6 CPU-seconds, about 30 percent.
- Phases inside the Freestyle run, read from `render_stats` handler timestamps (approximate boundaries): scene sync 0.25 s; Cycles + denoise 3.51 s; Freestyle 1.50 s (geometry import and view map 0.16 s for 2211 triangles and 95 view-map edges, stroke rendering 1.32 s); compositor and file writes 0.46 s.

Best estimate for this scene on a mostly free machine: **about 4.2 s per frame without Freestyle, 5.7 s with it**. Freestyle draws its strokes with a second Cycles pass ("Stroke rendering engine : CYCLES"), so its cost grows with resolution and with stroke area; two strokes are a lower bound, a furnished set will cost more. The 1.32 s probably contains a one-time GL start-up of about 0.8 s per process (`gpu.init()` alone took 0.83 s), which an animation render pays once; this split is an inference, not a measurement.

Against the spec's budget: the true-3D target of 6 s per frame leaves about 1.8 s for everything a real set adds over a sphere and a plane. Scaling the Cycles phase by pixels x samples gives about 24 s for a 1080x1920 plate and about 42 s for a 1440x2560 plate at 48 samples, both lower bounds for this trivial scene; the spec's 40 to 60 s and 65 to 110 s are plausible.

---

## 4. What the test frame says about the lighting model

Values are scene-linear, read from the EXR written before the grade; expected values from `albedo x (A + K cos)` with `EXTERIOR_NOON`, floor albedo `#f6b56f`, sphere albedo `#f6f6f6`.

| Place | Measured | Expected | Ratio |
|---|---|---|---|
| Sunlit floor, screen left | (0.697 to 0.754, 0.358 to 0.362, 0.148) | (0.728, 0.377, 0.151) | 0.95 to 1.04 |
| Sunlit floor, screen right | (0.954 to 0.980, 0.454 to 0.474, 0.158) | same | 1.21 to 1.35 |
| Floor in the sphere's shadow, beside the sphere | (0.125, 0.131, 0.166) | (0.092, 0.097, 0.126) | 1.32 to 1.36 |
| Floor in the sphere's shadow, far end | (0.099, 0.106, 0.143) | same | 1.07 to 1.14 |
| Black world after the grade | `#140918` to `#150919` | `#150919` | matches |

Rows 1 and 2 are the Oren-Nayar roughness (section 2, row 20). Rows 3 and 4 are extra light in a place the model says has none (row 21). With roughness 0 and `emission_sampling = 'NONE'` the model should hold exactly; that was not re-rendered because the render allowance was used up.

---

## 5. Corrected snippets

All of these ran in bpy 5.3.0 with `DeprecationWarning` turned into an error (`verify_api/corrected_snippets.py`, no render).

### 5.1 Node trees without `use_nodes`; black world

```python
def clean_tree(mat_or_world):            # new materials and worlds already own a node tree
    nt = mat_or_world.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt

def world_black(scene):
    w = bpy.data.worlds.new('W_clp'); scene.world = w
    nt = clean_tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); out = nt.nodes.new('ShaderNodeOutputWorld')
    bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
```

### 5.2 `lit` material, and attaching the compositor group

```python
def lit_material(name, albedo_hex, A, image=None):
    m = bpy.data.materials.new(name); nt = clean_tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 0.0   # Lambert
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Strength'].default_value = 1.0
    add = nt.nodes.new('ShaderNodeAddShader')
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs[0].default_value = 1.0; mul.inputs[7].default_value = (*A, 1.0)
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = image
        L(tex.outputs['Color'], dif.inputs['Color']); L(tex.outputs['Color'], mul.inputs[6])
    else:
        col = (*hex_lin(albedo_hex), 1.0); dif.inputs['Color'].default_value = col; mul.inputs[6].default_value = col
    L(mul.outputs[2], emi.inputs['Color'])
    L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1]); L(add.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'      # the ambient must not act as a light
    return m

def attach_compositor(scene, node_group, name='Grade'):
    if hasattr(scene, 'compositor_effects'):                 # 5.3
        effs = scene.compositor_effects
        eff = effs.active or effs.new(name=name)             # reuse: every extra effect is applied on top of the others
        eff.node_group = node_group
    else:                                                    # 5.0 to 5.2
        scene.compositing_node_group = node_group
```

The two rendered frames went through `scene.compositing_node_group = ng` (what `grade_compositor.build` does); that setter fills the active effect, and the `compositor_effects` form was checked to end in the same state (one effect, same group), not rendered separately.

To keep using `lightkit_clp.env_material` unchanged, patch its result: `dif.inputs['Roughness'].default_value = 0.0` on the Diffuse node and `m.cycles.emission_sampling = 'NONE'`.

### 5.3 Inverted hull

```python
def ink_material(name, ink_hex='#2a1712'):
    m = bpy.data.materials.new(name); nt = clean_tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); geo = nt.nodes.new('ShaderNodeNewGeometry'); lp = nt.nodes.new('ShaderNodeLightPath')
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Color'].default_value = (*hex_lin(ink_hex), 1.0)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    notcam = nt.nodes.new('ShaderNodeMath'); notcam.operation = 'SUBTRACT'; notcam.inputs[0].default_value = 1.0
    fac = nt.nodes.new('ShaderNodeMath'); fac.operation = 'MAXIMUM'
    L(lp.outputs['Is Camera Ray'], notcam.inputs[1]); L(geo.outputs['Backfacing'], fac.inputs[0]); L(notcam.outputs[0], fac.inputs[1])
    L(fac.outputs[0], mix.inputs['Fac'])     # 1 = Transparent: the hull's back side, and every ray that is not a camera ray
    L(emi.outputs['Emission'], mix.inputs[1]); L(tr.outputs['BSDF'], mix.inputs[2]); L(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def add_ink_hull(ob, ink_mat, thickness):    # slot 0 = the surface material
    ob.data.materials.append(ink_mat)
    mod = ob.modifiers.new('ink_hull', 'SOLIDIFY')
    mod.thickness = thickness; mod.offset = 1.0; mod.use_flip_normals = True; mod.use_rim = False
    mod.material_offset = len(ob.data.materials) - 1
    mod.use_even_offset = True               # without it a box hull is 0.58 x thickness
    return mod
```

Each hull crossing should spend one transparent bounce, so `transparent_max_bounces = 8` should cover about four hulled props stacked along one ray (not rendered).

### 5.4 Freestyle for plates

```python
def freestyle_ink(scene, view_layer, collection, px=3.0, ink_hex='#2a1712'):
    scene.render.use_freestyle = True; view_layer.use_freestyle = True
    scene.render.line_thickness_mode = 'ABSOLUTE'; scene.render.line_thickness = 1.0    # unit; width = unit x linestyle.thickness
    fs = view_layer.freestyle_settings
    for ls in list(fs.linesets): fs.linesets.remove(ls)      # drop the default 'LineSet'
    ls = fs.linesets.new('ink')
    ls.select_by_visibility = True; ls.visibility = 'VISIBLE'
    ls.select_by_edge_types = True; ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
    ls.select_by_collection = True; ls.collection = collection; ls.collection_negation = 'INCLUSIVE'
    ls.linestyle.thickness = px; ls.linestyle.thickness_position = 'CENTER'; ls.linestyle.color = hex_lin(ink_hex)
    return ls
```

Run: `xvfb-run -a -s "-screen 0 1280x1024x24" python3 render_plates.py`. For a plate rendered at 1.5 x or 2 x by changing `resolution_x/y`, multiply `px` by the same factor. If the plate is enlarged with `resolution_percentage` instead, measure the width on the first plate: Blender may already scale the unit by the percentage.

### 5.5 Depth from the plate render

```python
def add_depth_output(scene, view_layer, node_group, directory, file_name):
    """Writes <directory>/<file_name>z.exr (32-bit float, planar camera depth in Blender units) with the plate."""
    view_layer.use_pass_z = True
    rl = next(n for n in node_group.nodes if n.bl_idname == 'CompositorNodeRLayers')
    fo = node_group.nodes.new('CompositorNodeOutputFile')
    fo.directory = directory; fo.file_name = file_name
    fo.format.media_type = 'IMAGE'            # first: the default is MULTI_LAYER_IMAGE and then only OPEN_EXR_MULTILAYER is accepted
    fo.format.file_format = 'OPEN_EXR'; fo.format.color_depth = '32'; fo.format.color_mode = 'RGB'
    fo.file_output_items.new('FLOAT', 'z')    # 5.x: file_output_items, directory, file_name (base_path and file_slots are gone)
    node_group.links.new(rl.outputs['Depth'], fo.inputs['z'])
    return fo

def exr_to_depth16(exr_path, png_path, far=40.0):          # OpenCV here cannot read EXR; bpy can
    im = bpy.data.images.load(exr_path); w, h = im.size
    a = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(a); bpy.data.images.remove(im)
    z = a.reshape(h, w, 4)[::-1, :, 0]                      # bpy rows start at the bottom
    cv2.imwrite(png_path, (np.clip(z / far, 0.0, 1.0) * 65535.0 + 0.5).astype(np.uint16))
```

The EXR route was rendered and read back. A File Output item set to PNG, BW, 16-bit (`item.override_node_format = True; item.format...`) also builds, but was not rendered. The compositor must stay on (`use_compositing = True`) for the File Output node to write.

### 5.6 Keys with easing, anchors

```python
def fcurves_of(obj):
    ad = obj.animation_data; out = []
    for layer in ad.action.layers:
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot)
            if cb: out += list(cb.fcurves)
    return out

def key(obj, path, frame, value, interp='SINE', easing='EASE_IN_OUT'):
    setattr(obj, path, value); obj.keyframe_insert(path, frame=frame)
    for fc in fcurves_of(obj):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.5: kp.interpolation = interp; kp.easing = easing

def anchor_px(scene, cam, world_point):      # -> x from the left, y from the TOP, planar depth z
    co = world_to_camera_view(scene, cam, Vector(world_point))
    return co.x * scene.render.resolution_x, (1.0 - co.y) * scene.render.resolution_y, co.z
```

---

## 6. Blender 5.x changes next to the spec, easy to hit while building

| Old | 5.3.0 |
|---|---|
| `scene.node_tree`, `scene.use_nodes`, `CompositorNodeComposite` | a node group with a `NodeGroupOutput`, attached as in 5.2. `scene.use_nodes` still exists and warns. |
| `CompositorNodeMixRGB`, `CompositorNodeMath`, `CompositorNodeValToRGB`, `CompositorNodeMapRange`, `CompositorNodeMapValue`, `CompositorNodeGamma`, `CompositorNodeValue` | undefined. Use `ShaderNodeMix`, `ShaderNodeMath`, `ShaderNodeValToRGB`, `ShaderNodeMapRange`, `ShaderNodeGamma`, `ShaderNodeValue` inside the compositor tree. |
| Compositor node options as properties (`glare_type`, `correction_method`, `filter_type`, `size_x`) | input sockets; menus take display strings (`'Bloom'`, `'Offset/Power/Slope (ASC-CDL)'`, `'Gaussian'`). |
| File Output `base_path`, `file_slots` | `directory`, `file_name`, `file_output_items.new(socket_type, name)`; set `format.media_type = 'IMAGE'` before `file_format`. Still frames are named `<file_name><item name>.<ext>`. |
| `action.fcurves` | layered actions, see 5.6. |
| `Material.use_nodes`, `World.use_nodes`, `Light.use_nodes` | deprecated, always True. |
| `object.cycles_visibility`, `object.cycles.is_shadow_catcher` | `object.visible_*`, `object.is_shadow_catcher`. |
| `Mesh.use_auto_smooth` | gone. |
| Socket "Fac" | displayed "Factor"; the key `'Fac'` still resolves. |
| `bpy.app.handlers.composite_pre / composite_post` | exist but did not fire during these renders; use `render_stats` timestamps to split a frame. |
| EXR in OpenCV | `cv2.imread` returns None for EXR here, with or without `OPENCV_IO_ENABLE_OPENEXR`; read with `bpy.data.images.load`. |

---

## 7. Not verified here

1. The two material fixes of section 1 (roughness 0, emission sampling off) and both hull fixes were not rendered. The deviations they address were measured (items 3 and 4), shown by a geometric check (item 6) or measured on the evaluated mesh (item 5).
2. The point-lamp energy formula and the exactness of the sun formula at roughness 0: do the white-card test of 4.3 with the corrected material.
3. The `material_override` depth plate, the foreground plate with `film_transparent` and `visible_camera = False`, and the PNG variant of the depth output were checked at API level only.
4. Freestyle cost on a furnished set, the per-process share of its start-up, and the `resolution_percentage` scaling of the line width.
5. The grade on a transparent foreground plate: the CDL offset is added to premultiplied colour, which may tint semi-transparent edge pixels. Check the first multiplane plate.
6. The `scene.compositor_effects` way of attaching the grade: the rendered frames used the deprecated setter, which ends in the same state.
7. Render time without Freestyle on an idle machine was derived from the phases of the Freestyle run (4.2 s); the direct measurement (7.08 s) was taken under load.
