# Phase 4: the look

The style bible (`references/bible/`, index in `references/bible/README.md`) holds every number of the look by topic; `pipeline/spec/LOOK_SPEC.md` is the merged measurement it was built from, with `pipeline/spec/verify_blender_api.md` and `verify_measurements.md` as corrections, which win where they disagree. This file is the short version and the order to work in.

Sharp picture: no depth-of-field or background blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. The motion streak on fast camera moves stays.

## Characters: flat puppets, never lit 3D

`pipeline/v2/puppet/puppet.py` (API.md beside it): `figure(cast, pose, uid)` returns an SVG group in head-diameter units. Poses are dicts (yaw, head roll, expression, blink, arm and leg presets or hand targets solved by two-bone IK, props, effects). `pipeline/v3/cast/cast_ext.py` shows how to add cast members, hats and costumes from a separate module without editing the puppet.

Rules that carry the likeness: one flat head fill with a single crescent on the side away from the key light (the puppet draws the crescent and the thick ink at the lower right, which suits a key from screen-left; set `head_flip` on the actor when the key comes from the other side: film 1 set `head_flip=True` in every office take and per frame on the beach); plum ink thin toward the light and thick away from it; no neck; features slide to show a turn while the head stays a full circle; outline wobble baked into the paths with a fixed seed per character (filter noise swims when the camera moves); faces swap whole drawings, a blink is three one-frame drawings, an expression changes on the closed frame.

Design your own cast. A reviewer caught the first cast as recolours of the reference's characters.

## Sets: real geometry, artwork from code

`pipeline/v3/set3d/office3d.py` is the worked example (API.md, REVIEW.md). One Blender unit is one head diameter. Surfaces carry artwork drawn as SVG in Python and rasterised by headless Chromium; props have thickness and an inverted-hull ink line; the set returns anchors (marks for actors, prop positions, ready camera setups) and setters that can keyframe animated things. Dress the places a camera will look first.

Add to a set through an extension module that imports it and adds objects after `build()`. Two workers editing one set file at once will overwrite each other.

### A new set

A new story needs its own sets and cast: the bundled office, beach and kitchen belong to film 1. Per set, one builder (one tier down) and one independent reviewer-and-repairer; template `workflows/08_assets_second_set_and_cast.js` (its prompts are film 1's beach and cast: rewrite them). In film 1 the beach set plus the extra cast (two builders, then two reviewers, all one tier down) took about 1.5 hours of wall time and about 1.3 M subagent tokens; plan on about that per set with its review.
- Copy the structure of `pipeline/v3/set3d/office3d.py` (or `set3d_kitchen/kitchen3d.py` for a small one): `build()` returns anchors (actor marks, prop positions, named cameras) and setters; artwork is SVG drawn in Python; every prop has thickness and an ink hull; one hard key plus the ambient emission term. Write an `API.md` beside it before any shot uses it.
- Acceptance, measured by the reviewer on stills from the set's named cameras with a stand-in cast: `hue_report.py` inside the band below; `qa_light.py` shade at 0.15 to 0.31 of lit on the same surface, shadow hue 240 to 260, cast-shadow edge 4 to 21 px; real depth in every framing (a dark foreground layer, the lit subject band, a far wall or horizon; `references/bible/sets.md`); no texture finer than the screen (it shimmers); the caption band free of text.
- The reviewer looks at the stills next to named reference frames, lists defects and repairs them in the set file it was handed; reviewers in film 1 found a set too thin on detail, shadows detached from feet and a cast copied from the reference.

## Light and colour

- One hard key light (sun through a window, angle about 0.5 to 1.5 degrees) and an ambient term injected as emission. Direct light only, 12 samples, no denoiser: about 18 CPU seconds per 720x1280 frame.
- Same surface in shade at 0.15 to 0.31 of its lit luminance (the acceptance band; the raw reference measurements in `references/analysis.md` span 0.11 to 0.33). Cast-shadow edges 4 to 21 px. Bloom only on values above scene-linear 1.0 so lamps glow and white heads do not. The first film did not have this in the render: version 1 showed lamps as flat white discs, clipped highlights, low contrast (p95-p5 0.50 against 0.60-0.62) and a dark top of frame, and all of it had to be added in a 2D grade at the end (`references/polish.md`). Put bloom on light sources (never inside white fills such as faces and paper), a gentle S-curve and warm distance haze on exteriors into the opening the user approves.
- Shade must turn blue-violet (hue 240 to 260). The first set used a violet ambient with rose walls and came out 25 percent magenta; the user said "the colours are not like the reference". The fix was at the source: bluer ambient, per-surface ambient tints, terracotta walls, brown woodwork, more real blue, real deep darks.
- Check every set and every batch of frames: `python3 pipeline/v3/tools/hue_report.py <frames or stills>` (it prints the band; film 1's reference rows only when its reference stills are under `ref/a` and `ref/b`). Band taken from the references: red 30 to 41, orange 22 to 38, blue 14 to 30, violet 0 to 5, magenta 0 to 10 percent of chroma; saturation 0.38 to 0.48; value 0.45 to 0.63; 8 to 15 percent of pixels darker than value 0.25. Exterior and special-light scenes may sit outside; say why.
- The colour band is a property of whole scenes with characters. Map inserts, diagrams, night and storm shots fall outside it by design: say so. But light explainer and diagram sequences with the room's warm key; the first film's map sequence went cold (46 to 67 percent blue) for 15 seconds.
- A low sun puts actor shadows on the wall instead of the floor. The references have a 35 to 50 degree sun and whole-figure shadows on the ground; choose the sun height for where you want the shadow.

## Actors in the scene

`pipeline/v3/stage/` (API.md, REVIEW.md): each frame the puppet pose is rasterised to a transparent sprite and shown on a card with an emission-only material; the card casts a real shadow, is hidden by furniture, and is never lit or tinted. A hand or pencil tip is pinned to a world point by cutting the camera's sight line with the card (`world_to_local`), so the tip stays on its target while the camera moves. Known limits: no back views, cards near a wall swing into it when the camera is far off axis, top-down views lean the card.

## Camera and edit grammar

22 mm lens on a 36 mm sensor. Camera heights with a purpose: low (1.2 head diameters above the floor, pitched up 13.5 to 16.5 degrees), eye level (head centre + 0 to 0.3 D, 1 to 3 degrees down), high (3.3 to 4.4 D above the floor, pitched down 20 to 25 degrees: at -15 a quarter of the frame was still ceiling), close raking inserts on props. All values, per named camera: `references/bible/camera.md`. Never static for more than 6 frames and never linear: slow eased drifts of 6 to 10 percent per second between snap reframings of 13 to 25 frames. A framing change every 1.2 to 1.5 s on average (film 1 ran at about 1.06 s by the picture tool: aim at 1.3 to 1.4 s); any single interval between 0.6 and 1.6 s passes. A take checks itself with its runner's `qa` command; the whole film with `pipeline/v3/film/out/grammar.py` (film 1) or the joins of `pipeline/examples/film_mini.py` (`pipeline/v3/shots/qa_motion.py` reads only the opening). Most joins are 9 to 23 frame dissolves with both shots moving; the hook uses the punchier ones (whip pan, punch-in, hard cut). Whole heads stay above the caption band; the main head centre sits at 0.35 to 0.59 of the frame height. On fast frames streak the set and keep the actors sharp (`render_layers.py`, `post.py`).

Depth: Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light: stage two-shots in depth (near head 1.36 to 1.46 times the far one), keep a dark foreground layer near the lens in wides, haze the distance in exteriors. Keep whole heads and any text in the picture out of the caption band (y 880 to 950).

`pipeline/v3/shots/film.py` is a complete 5 second film in this grammar; `pipeline/v3/README.md` explains how to add a shot.

## Checking a result against the reference

| Tool | Says |
|---|---|
| `pipeline/v3/tools/hue_report.py` | colour make-up against the reference band |
| `pipeline/v3/shots/qa_light.py` | shade against lit, hue shift, shadow edge (renders the opening's frames; copy it and swap the scene for a new set) |
| `pipeline/v3/shots/qa_parallax.py` | share of frame pairs a flat 2D move explains (reference 11 and 43 percent, so 10 to 45 passes; a flat film reads 91) |
| `pipeline/v3/shots/qa_motion.py` | framing changes, static and linear runs, camera height and pitch of the opening (a take: its runner's `qa`) |
| `pipeline/v2/eval/score.py` | characters, tone, density, pacing, captions; blind to light direction, shadows and perspective |

Then make a sheet per aspect (reference, previous attempt, current) and look at it at full size. The numbers catch regressions; the sheet is what convinces the user.
