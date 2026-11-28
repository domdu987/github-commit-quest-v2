# Phase 4: the look

Read `pipeline/spec/LOOK_SPEC.md` for the numbers and `pipeline/spec/verify_blender_api.md` and `verify_measurements.md` for corrections, which win where they disagree. This file is the short version and the order to work in.

## Characters: flat puppets, never lit 3D

`pipeline/v2/puppet/puppet.py` (API.md beside it): `figure(cast, pose, uid)` returns an SVG group in head-diameter units. Poses are dicts (yaw, head roll, expression, blink, arm and leg presets or hand targets solved by two-bone IK, props, effects). `pipeline/v3/cast/cast_ext.py` shows how to add cast members, hats and costumes from a separate module without editing the puppet.

Rules that carry the likeness: one flat head fill with a single crescent on the side away from the key light; plum ink thin toward the light and thick away from it; no neck; features slide to show a turn while the head stays a full circle; outline wobble baked into the paths with a fixed seed per character (filter noise swims when the camera moves); faces swap whole drawings, a blink is three one-frame drawings, an expression changes on the closed frame.

Design your own cast. A reviewer caught the first cast as recolours of the reference's characters.

## Sets: real geometry, artwork from code

`pipeline/v3/set3d/office3d.py` is the worked example (API.md, REVIEW.md). One Blender unit is one head diameter. Surfaces carry artwork drawn as SVG in Python and rasterised by headless Chromium; props have thickness and an inverted-hull ink line; the set returns anchors (marks for actors, prop positions, ready camera setups) and setters that can keyframe animated things. Dress the places a camera will look first.

Add to a set through an extension module that imports it and adds objects after `build()`. Two workers editing one set file at once will overwrite each other.

## Light and colour

- One hard key light (sun through a window, angle about 0.5 to 1.5 degrees) and an ambient term injected as emission. Direct light only, 12 samples, no denoiser: about 18 CPU seconds per 720x1280 frame.
- Same surface in shade at 0.15 to 0.31 of its lit luminance. Cast-shadow edges 4 to 21 px. Bloom only on values above scene-linear 1.0 so lamps glow and white heads do not.
- Shade must turn blue-violet (hue 240 to 260). The first set used a violet ambient with rose walls and came out 25 percent magenta; the user said "the colours are not like the reference". The fix was at the source: bluer ambient, per-surface ambient tints, terracotta walls, brown woodwork, more real blue, real deep darks.
- Check every set and every batch of frames: `python3 pipeline/v3/tools/hue_report.py <frames or stills>`. Band taken from the references: red 30 to 41, orange 22 to 38, blue 14 to 30, violet 0 to 5, magenta 0 to 10 percent of chroma; saturation 0.38 to 0.48; value 0.45 to 0.63; 8 to 15 percent of pixels darker than value 0.25. Exterior and special-light scenes may sit outside; say why.
- A low sun puts actor shadows on the wall instead of the floor. The references have a 35 to 50 degree sun and whole-figure shadows on the ground; choose the sun height for where you want the shadow.

## Actors in the scene

`pipeline/v3/stage/` (API.md, REVIEW.md): each frame the puppet pose is rasterised to a transparent sprite and shown on a card with an emission-only material; the card casts a real shadow, is hidden by furniture, and is never lit or tinted. A hand or pencil tip is pinned to a world point by cutting the camera's sight line with the card (`world_to_local`), so the tip stays on its target while the camera moves. Known limits: no back views, cards near a wall swing into it when the camera is far off axis, top-down views lean the card.

## Camera and edit grammar

22 mm lens on a 36 mm sensor. Camera heights with a purpose: low (1.2 head diameters above the floor, pitched up about 15 degrees), eye level, high (3 or more above the floor, pitched down 15 to 20 degrees), close raking inserts on props. Never static for more than 6 frames and never linear: slow eased drifts of 6 to 10 percent per second between snap reframings of 13 to 25 frames. A framing change every 1.2 to 1.5 s. Most joins are 9 to 23 frame dissolves with both shots moving; the hook uses the punchier ones (whip pan, punch-in, hard cut). Whole heads stay above the caption band; the main head centre sits at 0.35 to 0.59 of the frame height. On fast frames streak the set and keep the actors sharp (`render_layers.py`, `post.py`).

`pipeline/v3/shots/film.py` is a complete 5 second film in this grammar; `pipeline/v3/README.md` explains how to add a shot.

## Checking a result against the reference

| Tool | Says |
|---|---|
| `pipeline/v3/tools/hue_report.py` | colour make-up against the reference band |
| `pipeline/v3/shots/qa_light.py` | shade against lit, hue shift, shadow edge |
| `pipeline/v3/shots/qa_parallax.py` | share of frame pairs a flat 2D move explains (reference 11 and 43 percent; a flat film reads 91) |
| `pipeline/v3/shots/qa_motion.py` | framing changes, static and linear runs, camera height and pitch |
| `pipeline/v2/eval/score.py` | characters, tone, density, pacing, captions; blind to light direction, shadows and perspective |

Then make a sheet per aspect (reference, previous attempt, current) and look at it at full size. The numbers catch regressions; the sheet is what convinces the user.
