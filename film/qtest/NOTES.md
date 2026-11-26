# R9 quality test: notes

Clip: `r9_test.mp4`, 10 s, 720x1280, 30 fps, no audio or narration. Contact sheet at 1 fps: `r9_test_sheet.jpg`.
Everything comes from one script, `r9_scene.py` (Blender 5.2.5 as the `bpy` Python wheel, Cycles on the CPU), plus a small post step, `post.py`.

| Shot | Frames | Content |
|---|---|---|
| a | 1-90 (3 s) | 60 mm macro on a brass casing. It falls in slow motion with motion blur, lands in the snow and kicks up clumps of snow that land and stay. f/3.2, so the forest behind is bokeh. |
| b | 91-210 (4 s) | 32 mm f/1.4 tracking shot. The character walks through the snowy pines at sunset with the rifle on its shoulder. A young pine passes out of focus in the foreground at the start and again at the end. |
| c | 211-300 (3 s) | POV down the iron sights (front post with ears, rear notch) across the valley to a cabin on the far slope. The lens pushes in from 32 to 42 mm while the camera dollies forward 0.25 m. |

The shots are joined with hard cuts. The camera does not shake. The only object parented to a camera is the POV rifle in shot c.

## Light and look
- **Light:** Cycles path tracing with GI. The key is one warm sunset sun (RGB 1.0, 0.60, 0.33, 10-13° high, 1.6° disc), so its shadows are soft. The fill is a gradient sky: deep blue at the zenith, lavender in the middle and peach at the horizon, plus a glow around the sun. Snow in shade is lit only by that sky, so it turns blue-violet.
- **Forest layout:** trees are kept out of a "sun corridor" toward each set. Without that, a 10° sun in a forest leaves every set in shadow.
- **Haze:** a real volume (Principled Volume, anisotropy 0.55). Density is 0.028 in the forest and 0.0022 across the valley, so the far treeline fades into the haze.
- **Snow:** a principled material with noise bump and mirror "sparkle" facets (Voronoi) that catch the sun.
- **Post (`post.py`):** bloom on hot spots only (threshold 0.8, tint 1, 0.94, 0.84), saturation x1.15, a mild S-curve, a vignette of 5 % or less and a ceiling of 0.985. These follow COLOUR_SPEC §5.
- **Where I followed R9 instead of COLOUR_SPEC:**
  - The characters are lit and shaded by the scene. COLOUR_SPEC §2 says characters are unlit.
  - The exterior frame shares (snow and sky) fall outside the interior hue bands.
- **Set:**
  - 3,600+ pine instances built from 10 procedural meshes. Each has 5-7 star-shaped tiers with drooping branch tips, a smooth snow pad on top, a needle fringe with snow lumps, and a dark underside. The distant pines use a mostly-needle variant so the far treeline reads dark green.
  - Height-field drifts, two snow-capped logs, a footprint trail, and a valley with a cabin whose window glows warm.

## The character and its walk
- **Model:** the character is built in code to match the R9 proportions. It is about 1.25 m tall.
  - The body is a pill-shaped coat (lathe) with a leather belt, a brass buckle and buttons.
  - The head is a white sphere. Its face is drawn in 2D: PIL draws half-lidded eyes, brows and a smirk in ink #3a2832 onto a texture. A shader projects that texture onto the front hemisphere in object space, so it turns with the head.
  - The ushanka is a lathe with a fur shader (noise bump plus sheen) and a turned-up band, ear flaps and a badge.
  - The limbs are thin dark cylinders with ball joints and small boots.
  - The head group turns 42° toward the camera.
- **Walk cycle (analytic, no sliding):**
  - The root moves at a constant 0.55 m/s. The gait has a 1.0 s period with 60 % stance.
  - During stance, each foot is held at a fixed world position, its plant point. The swing moves it to the next plant point along a lifted sine arc.
  - The hip height follows the terrain under the feet, with a small vertical bob plus some sway and roll.
  - Thigh and shin are solved every half frame with two-bone IK (knees toward the walk direction) and keyframed. Half-frame keys keep the motion blur accurate.
  - The left arm holds the rifle by IK to a grip point on the stock. The right arm swings.
- **Footprints:**
  - A 7 x 1.2 m strip of 2 cm ground mesh carries the old trail as dents.
  - Every new plant is a shape key. It switches on at the frame the boot lands, and the boot sinks 2.8 cm into it.
  - The strip's border matches the surrounding 10 cm ground exactly, so there are no cracks.
- **Contact:** feet, casing, snow clumps, logs and trees are all placed from the same height function as the ground, so nothing floats.

## Render time (this container: 4 CPU cores, no GPU)
Each frame was rendered at 540x960 (75 %) with 24 samples, adaptive sampling and OpenImageDenoise, then upscaled with Lanczos to 720x1280 in post. Measured times:

RENDER_TIMES

For reference, one shot-b frame at full 720x1280 with 64 samples took **154 s**. The haze volume is about half of that cost. At that setting the 300 frames would have taken about 13 h on this machine, so I used the reduced setting above. The brief's 64-128 samples at native resolution fit easily on a GPU: a single modern RTX-class card is typically 20-40x faster than these 4 cores, which puts a frame at about 5-8 s.

## What full 60 s films would need
1. **GPU render nodes.**
   - 1,800 frames x ~6 s on one RTX 4090-class GPU is about 3 h per film at native resolution and 64-128 samples.
   - On this CPU box the same film would take about 75 h.
   - Rent GPUs or use a render farm, and render shots in parallel.
2. **An asset library instead of one script.**
   - The pine kit, terrain, rifle, casing and the character rig should become a `.blend` asset library: characters with swappable hats and coats and a face-texture slot driven from `puppet.py` expressions, and sets for forest, valley, cabin interior and trenches.
   - About 2-3 days of work.
3. **A real armature rig.**
   - It needs IK legs, the foot-plant solver from this test turned into a reusable walk generator with any path, speed and terrain, and arm IK targets on props.
   - It also needs face-swap keys for blinks and mouth shapes timed to the narration, plus a handful of reusable actions: sit, prone, aim, fall and point.
4. **Shot list to camera tooling:** helpers for tracking, macro inserts, POV and whip pans with motion blur, so that 25-35 shots per film can be blocked quickly.
5. **Pipeline integration:**
   - Captions and narration from the existing `film/` tools go on top of the rendered plates. Keep caption-safe areas clear when framing.
   - QA checks for floating objects (contact tests) and for colour against COLOUR_SPEC, with the R9 exterior exceptions written down.
6. **Throughput:** about 1 week to set up, after which each film should take 1-2 days of layout and animation plus GPU render time.
