# v3/stage: independent review and repair

Reviewer scripts: `review/c*.py` (one fresh process per check; `review/run_all.sh [after|before]`), shared helpers in `review/rv_common.py`. They use their own pinhole projection and measure rendered pixels; they do not use the stage's projection or test helpers. "Before" = the builder's files as found (kept untouched in `v3/tmp/stage_review/orig/`), "after" = the files in `v3/stage/` now. Both columns were produced by the same scripts. Raw numbers: `v3/tmp/stage_review/{before,after}/*.json`, logs in `v3/tmp/stage_review/logs/`. All renders are in the stub room (`stubroom.py`); the real office set was not used.

## Result

Two defects were found and repaired, and one event was seen once and guarded against. None of them shows in the builder's own tests. Everything else passed as built.

1. **Stale sprite (check 3).** Rendering a frame, changing its pose, calling `render_sprites()` and rendering the same frame again showed the OLD drawing. Cause: `render.setup` switched Cycles' persistent data on; Cycles then keys a texture by its file path and never reads the file again, and `Image.reload()` (what the package did) does not reach it. The builder's test rendered each frame once. Persistent data saves no time here (measured), so it is now off by default; with it on, the actors detect rewritten sprites and drop the cache.
2. **Shadow not attached at the feet (check 5).** The shadow caster was one rigid quad turned toward the light about the feet centre, so whenever it had to turn each foot of the shadow stood away from the drawn foot: 5.2 px under the default key with a square-on camera, 14.7 px with the camera 25 degrees off axis, 17.6 px with a side light (59 px, and mirrored, in a reverse shot). Now 0.0 px.
3. **One unexplained event.** In one run of `c3_sequence.py` (repaired code, persistent data still on at that time) two consecutive frames came out with the actor's whole card as a black rectangle (`v3/tmp/stage_review/look_black.png`). It did not happen in the 21 other runs of the same script (about 1550 renders; 14 of the runs with two copies side by side) nor in 1344 renders of two stress scripts (`c3b_stress.py`, `c3c_repeat.py`), on either version of the code. It is not a missing texture (that renders magenta: tested). The cause was not found. Guard: `render_frames` now reads each frame back, and when an actor's head is a black or magenta hole it empties the caches and renders the frame once more (`c3d_card_check.py`).

Confirmed as built: registration (0.45 px worst over 300 moving frames), card colours (exact under every light), ground contact, scale, head roundness, camera easing, the card orientation choice, and the cost.

| # | Check | Result before | Fix | Result after |
|---|---|---|---|---|
| 1 | API.md worked example, copied literally, clean process (`c1_api_example.py`); second import style `from stage import ...` (`c1b`) | runs, 5 frames written, printed tip and target pixels equal | none | runs |
| 2 | Registration: pencil tip pinned to 5 world points on the wall (hero, mirrored hero, boss, hero at scale 1.3, walking hero), low / eye / high camera, 20-frame moves, marker rendered at the world point, every frame (`c2_registration.py`) | 300 frames: max 0.45 px, mean 0.20 px, none over 2 px | none | max 0.45 px, mean 0.20 px |
| 2b | Is the DRAWN pencil point on the target (sprite with and without the pencil, 48 poses with mirror and stretch) (`c2b_tip_in_sprite.py`) | max 1.68 sprite px = 0.0066 D (about 1 screen px), pencil angle within 1.1 deg | none | same |
| 2c | A staging that cannot work (hero 0.3 D from the wall, camera 40 deg off axis: the card's reaching side is behind the wall, the wall hides the tip) | tip hidden (0 px of the tip marker rendered), `pose()` reports nothing | `pose()` now returns `info[side]["clearance"]` and warns when it is negative | clearance -0.43 D reported, warning issued |
| 3 | Sprite sequence, 12 frames with 12 different faces and arms, each rendered frame classified against 12 single-sprite reference renders, head and wall shadow separately (`c3_sequence.py`) | in order 12/12, out of order 12/12, repeats 7/7, animation loop 12/12, single fresh process 3/3. **Wrong:** same frame reposed 0/1 (old drawing shown), rewritten no reload 2/3; after a 384 px/D pass, going back to 256 still showed the 384 sprites | `render.setup` no longer switches persistent data on. For `setup(persistent=True)`: `Actor.reload_sprites()` also drops Cycles' persistent data; `render_sprites()` and `sync()` detect rewritten files of frames already shown (inode, time, size) and call it | default (persistent off): all 11 cases right (same frame reposed 1/1, rewritten no reload 3/3, back at 256 2/2, in order 12/12, out of order 12/12). With `persistent=True`: all right too (same frame reposed 1/1, same frame no reload 1/1, rewritten no reload 3/3, rewritten at 384 3/3, back at 256 2/2, in order 12/12, out of order 12/12). Difference to the own reference 0.000 levels |
| 3d | Post-render card check (`c3d_card_check.py`): frame 2 rendered with the sprite taken off the material (magenta card), frame 3 with the card forced black and opaque, the fault removed before the second attempt | no check: a faulty frame is written as it is | `render_frames(check=True)` (default) + `render.cards_wrong()` | frame 1 untouched (1 attempt); frames 2 and 3 flagged (['hero'], ['hero']), rendered again, equal to the clean render (largest difference 0 levels) |
| 4 | Colour: head fill and ink of hero and boss under a 3x sun, in deep shade, under a 5x frontal sun, beside a strong red lamp, sun off (`c4_colour.py`) | fill #fef7f6, ink #3a2832 in all five; no interior card pixel changes by more than 1 level | none | fill #fef7f6, ink #3a2832; 1 level |
| 5a | Shadow present and hard (`c5_shadow.py` A) | shadow / lit 0.31 to 0.44 in linear light (stub room values), 10-90 % edge 3.3 to 5.6 px (reference 4 to 21 px) | none | 0.31 to 0.44, 3.3 to 5.6 px |
| 5b | Shadow attached at the feet: distance between each drawn sole and the same point of the shadow caster, 9 light / camera cases | **up to 17.6 px** (0.26 D): default key 5.2 px, camera 25 deg off axis 14.7 px, side light 15.7 to 17.6 px; 0 only while the proxy did not have to turn. Reverse shot 59 px and the shadow is the mirror image (caster x . card x = -0.97) | shadow proxy is now a grid with a twist: in the visible card at the ankles, facing the light above the hips; stage-back orientation for cameras on the far side | **0.0 px in all cases**; reverse shot 0.0 px, not mirrored (+0.97) |
| 5c | Shadow stable over a 12-frame, 36 degree orbit: ratio sampled on 1182 fixed world points (`c5_shadow.py` B) | wall points changing by more than 0.15: 0.5 %, floor points 3.1 % | (consequence of 5b) | wall 0.5 % (unchanged), floor 6.1 %: the leg shadows now follow the drawn feet |
| 5d | Key light nearly edge-on to the card (light azimuth 85, 90, 95 deg off the card normal): shadow area against the normal key | proxy 0.86 to 0.97; `shadow="card"` 0.00 (no shadow at all) | none | proxy 0.83 to 0.96 |
| 5e | `bake_facing` + Blender's own animation loop against `render_frames`, 12 moving frames | largest pixel difference 0 (only the card rotation was keyed; enough for a rigid proxy) | `bake_facing` keys everything `sync()` sets, and `sync()` keeps baked keys current | 0 |
| 6 | Ground contact and scale, hero and boss, scale 1.0 and 1.4, low / eye / high (`c6_ground_scale.py`) | lowest ink pixel -1.2 to +0.0 px from the floor line; hero 3.06 D tall, boss 3.61 D (scale 1.4: 4.29 D); head on screen -0.8 to +1.4 % of 782.22 x scale / depth; head V/H 0.983 to 1.012 | none | -1.2 to +0.0 px; 3.06 / 3.61 D; -0.8 to +1.4 %; 0.983 to 1.012 |
| 7 | Easing (`c7_easing.py`): snap peak / mean speed; drift settles; keys carry the easing | snap 1.56 to 2.11 for `peak` 1.5 to 2.1 (default 1.7: 1.71 with pivot, 1.69 without); drift `cubic_out` first step 2.93 x mean, last 0.001 x, no motion after f1; interpolation and easing stamped on every keyframe point, F-curve within 2e-06 of the analytic sine and cubic-out curves | none | same |
| 8 | Card orientation, both modes at the a/t16.0 and a/t58.5 cameras and at a 15 degree high angle at the wall (`c8_orientation.py`) | vertical card + upper-body stretch is the right choice (below) | none | same |
| 9 | Cost (`c9_cost.py`, `c9c_repair_cost.py`), two actors, stub room, no other job running | sprite 24 ms (256 px/D), 33 ms (384); draft 360x640: 0.35 s wall at 4 threads, 1.30 s CPU; final 720x1280, 8 samples: 2.59 s wall at 4 threads, 5.12 s at 2 threads, 10.05 s CPU | (the repairs cost +0.19 s wall per final frame at 4 threads, of which the twisted proxy +0.11 s) | sprite 26 ms, 35 ms; draft 0.42 s wall, 1.53 s CPU; final 2.85 s wall at 4 threads, 5.59 s at 2 threads, 10.93 s CPU |

## Repairs (`actors.py`, `render.py`; no existing signature changed, new arguments are optional and last)

1. **Persistent data off** (`render.setup(..., persistent=False)`). Measured on the stub room and on the stub room with four 2048 px textures and 13000 extra triangles: 5.52 against 5.53 s and 6.06 against 6.08 s per final frame with it on / off. It bought nothing and caused defect 1. With it on, things tried that do NOT make Cycles read a rewritten PNG: `Image.reload()`, `image.update_tag()`, reassigning `filepath`, tagging the material, a new image datablock, taking the image off the node and back. Only dropping the persistent data works.
2. **Stale-sprite guard for `persistent=True`.** `Actor.reload_sprites()` = `Image.reload()` + persistent data switched off and on once. `render_sprites()` no longer reloads blindly: it and `sync()` compare the files of frames already shown with what was shown and reload only when one changed, so writing new frames while rendering costs nothing. `render.drop_cache(scene)` is the same switch for the integrator: a SET texture overwritten in place after it was rendered is stale in the same way (measured on a wall texture: `image.reload()` alone rendered the old picture, with `drop_cache` the new one). This matters for the wall map, whose track is drawn and rubbed out during the shot, if persistent data is ever switched on.
3. **Shadow proxy.** The quad is cut into rows of about 0.15 D across the legs only (hero 36 faces, boss 48) and carries a Simple Deform twist about the vertical through the feet. Below `actor.shadow_twist[0]` (0.12 D) it lies in the visible card, above `actor.shadow_twist[1]` (0.9 x the standing hip height) it faces the light as before. `actor.shadow_twist = None` restores the rigid single quad. For a camera on the far side of the stage the proxy starts from the stage-back orientation, so the shadow is not mirrored. With no sun in the scene the strongest shadow-casting lamp is followed. Rows cost shadow-ray time (a first version with rows over the whole card cost +0.95 s CPU per final frame; this layout +0.36 s CPU, +0.11 s wall at 4 threads).
4. **Post-render card check.** `render_frames(..., check=True)` and `render.cards_wrong(path)`: nine points in every visible actor's head are read from the written PNG; all black or all magenta -> caches emptied, one more render, `"retried"` (and `"still_wrong"`) in the frame's stats.
5. **`bake_facing`** keys card rotation and offset, proxy rotation, offset and twist angle, and the decal rotation (CONSTANT); after a bake, `sync()` rewrites the key of the frame it sets.
6. **`pose()`** adds `info[side]["world"]` and `info[side]["clearance"]` for world targets and warns when the card stands behind the target (the wall would hide the hand).
7. `API.md` updated (4.1 shadow proxy and stale sprites, 4.4 clearance, 6 persistent data, `drop_cache`, `check`; traps 0, 3 and 9). The builder's `tests/` still run (`example.py`, `test_edge.py`, `test_stills.py`, `test_move.py` re-run after the repairs).

## Check 8 in detail: did the builder choose the right card orientation?

Yes. `v3/tmp/stage_review/after/c8_a_t16.jpg`, `c8_a_t58.jpg`, `c8_high15.jpg` show the reference frame beside the three modes.

| Camera | Mode | Head V/H | Figure, head top to soles, in head widths (x flat) | Torso x flat | Legs x flat | Notes |
|---|---|---|---|---|---|---|
| a/t16.0: boss, 190 px, camera 1.16 D high, +15 deg | vertical + stretch (chosen) | 1.001 | 3.86 (x1.146) | x1.141 | x1.250 | upper_k 1.091 |
|  | vertical, no stretch | 0.925 | 3.69 (x1.093) | x1.050 | x1.240 | head visibly flattened |
|  | facing the lens | 1.000 | 3.37 (x1.000) | x1.000 | x1.000 | card leans: head 0.74 D in front of the feet, head 232 px |
| a/t58.5: hero crouching, 125 px, camera 3.2 D high, -8 deg | vertical + stretch (chosen) | 1.000 | 2.13 (x0.970) | x0.957 | x0.912 | upper_k 1.024 |
|  | vertical, no stretch | 0.976 | 2.09 (x0.951) | x0.936 | x0.912 | head visibly flattened |
|  | facing the lens | 1.000 | 2.19 (x1.000) | x1.000 | x1.000 | card leans: head 0.24 D behind the feet, head 120 px |
| high angle -15 deg, hero 0.55 D in front of the wall | vertical + stretch (chosen) | 1.001 | 2.62 (x0.886) | x0.901 | x0.766 | upper_k 1.077 |
|  | vertical, no stretch | 0.924 | 2.50 (x0.844) | x0.843 | x0.770 | head visibly flattened |
|  | facing the lens | 1.000 | 2.96 (x1.000) | x1.000 | x1.000 | card leans: head 0.64 D behind the feet, head 134 px; head centre 0.09 D INSIDE the wall: the head is cut off |

Reference (spec/verify_measurements.md row 12, character_anatomy.md): the chief is 3.05 head widths tall near eye level (a/t13.5) and 3.41 in the low-angle frame a/t16.0, that is x1.118, with a round head (W/H 1.00 to 1.05), a torso of 0.87 to 0.93 D against 0.85 (x1.02 to x1.09) and all the remaining gain in the legs (about x1.25).

- The facing card gives x1.000 everywhere: no leg stretch at the low angle, the opposite of the reference. It also leans 15 degrees: toward the lens at the low angle (the head grows from 190 to 232 px), into the wall at the high angle (an actor standing at the map loses his head, `c8_high15.jpg`).
- The vertical card alone gives the right legs (x1.24) and torso (x1.05) but a flattened head (V/H 0.925 at a/t16.0, 0.924 at the 15 degree high angle; the reference head is round within 2 percent).
- Vertical + stretch gives a round head (1.001) and the right legs (x1.25). Its torso comes out x1.14, a little above the reference range of x1.02 to x1.09, because the stretch covers the whole upper body and not only the head. Left as it is: stretching only the head would put a kink into a pencil or an arm that crosses the chin line, and the hero's pencil works at exactly that height.

## Other measurements worth knowing

- Check 6: the upper-body stretch raises the head centre 0.04 to 0.07 D (up to 11 px on a 150 px head) above `feet_y x scale` at the low and high angles, so a head aimed with `cam_for` lands that much higher in the frame than asked. The figure is also taller in the world: hero 3.06 D at eye level, up to 3.15 D per unit scale with the stretch.
- Check 7: `cam_for` lands the subject within 0.000 px of the asked pixel with the asked head size (42 poses). `whip_off(+40)` turns the view +40.0 degrees toward +X. A pure rotation snap has peak / mean 1.68.
- Check 5: the proxy's light-facing rule still jumps when a light passes exactly edge-on to the stage front (the proxy flips from +50 to -50 degrees and the body shadow mirrors). A fixed sun never crosses that; a lamp carried past an actor would. Not changed.

## Cost (check 9)

| Step | Before (builder's files) | After |
|---|---|---|
| Sprite, 928x1136 / 992x1248 px (256 px/D), wall time each | 24 ms | 26 ms |
| Sprite at 384 px/D | 33 ms | 35 ms |
| First sprite of a process (starts Chromium) | 0.37 s | 0.42 s |
| Pose with a pinned hand and the stretch solve, per actor and frame | 2.2 ms | 2.1 ms |
| Draft 360x640, 4 samples, 2 threads | 0.71 s wall, 1.40 s CPU (1-min load 1.6, no other job) | 0.77 s wall, 1.51 s CPU (1-min load 2.1, no other job) |
| Draft, 4 threads | 0.35 s wall, 1.30 s CPU (1-min load 1.9, no other job) | 0.42 s wall, 1.53 s CPU (1-min load 2.0, no other job) |
| Final 720x1280, 8 samples, 2 threads | 5.12 s wall, 10.06 s CPU (1-min load 1.7, no other job) | 5.59 s wall, 11.01 s CPU (1-min load 2.1, no other job) |
| Final, 4 threads | 2.59 s wall, 10.05 s CPU (1-min load 1.9, no other job) | 2.85 s wall, 10.93 s CPU (1-min load 2.2, no other job) |

What the repairs cost, variants alternating in one process, final quality, 4 threads, best of 3 rounds (`c9c_repair_cost.py`):

| Variant | Wall per frame | CPU per frame |
|---|---|---|
| builder's version | 2.57 s | 10.01 s |
| repaired, defaults (twisted proxy, card check, persistent data off) | 2.76 s | 10.54 s |
| repaired, `check=False` | 2.73 s | 10.52 s |
| repaired, `persistent=True` | 2.76 s | 10.64 s |
| repaired, `shadow_twist = None` (rigid proxy) | 2.65 s | 10.18 s |
| repaired, rigid proxy, no check, persistent on (the builder's configuration) | 2.65 s | 10.20 s |

First table: per frame = median of frames 2 to 6 of a 6-frame move with a new drawing on every frame; wall and CPU seconds of the render call including the PNG write (after: also the card check). Each row says what else was running; the two columns were measured half an hour apart, so use the second table for the difference between the versions: the repairs add about 0.2 s wall per final frame at 4 threads (7 percent); the twisted shadow proxy accounts for 0.1 s of it, the card check for 0.03 s, and the remainder is the size of the spread between rounds. Earlier in the review both versions were also timed while another agent's render used one to two cores: final frame at 2 threads 5.3 s (before) and 5.7 s (after) wall, 10.5 and 11.3 s CPU. The final frame is inside the 6 s target at 2 threads and at about half of it at 4 threads, in the stub room; the real set adds its own cost.

## Remaining differences from the reference, most visible first

1. Low-angle boss proportions. At the a/t16.0 camera our boss is 3.86 head widths tall against 3.41 in the reference. The stage adds the same perspective gain as the reference (legs x1.25); the excess comes from the v2 boss puppet, which is 3.40 D tall flat where the reference chief is 3.05 (its 3.4 was measured on the stretched frame). v2 is read-only, so nothing was changed.
2. Torso x1.14 at the low angle against x1.02 to x1.09 (above).
3. Cards are never lit, so the head ink's thick side and the crescent stay at the lower right (v2 puppet): the key light has to come from the upper left, as the kit's default does.
4. A foot whose card is edge-on to the key light has a hairline shadow for its first 0.12 D (API.md trap 0).
5. A pinned pencil tip is drawn on the card, in front of the wall; its shadow falls where the card's does (API.md trap 6).
6. Top-down and steeper than 50 degree views lean the card back; actors near a wall disappear into it (API.md trap 4).
7. Not a difference but an open point: the black-card event of the Result section has no known cause. The post-render check catches its picture (a head that is entirely black or magenta) and renders the frame again; it would not catch a card that is wrong in some other way.

## Files

- Changed: `v3/stage/actors.py`, `v3/stage/render.py`, `v3/stage/API.md`. Re-generated by the builder's own tests after the repairs: `test_low.png`, `test_eye.png`, `test_high.png`, `test_stills_vs_ref.jpg`, `test_stills.json`, `test_edge.json`, `test_move.jpg`, `test_move.json` (the builder's originals are in `v3/tmp/stage_review/orig/`).
- Added: `v3/stage/REVIEW.md`, `v3/stage/review/` (`rv_common.py`, `c0_crop_align.py`, `c1_api_example.py`, `c1b_package_import.py`, `c2_registration.py`, `c2b_tip_in_sprite.py`, `c3_sequence.py`, `c4_colour.py`, `c5_shadow.py`, `c6_ground_scale.py`, `c7_easing.py`, `c8_orientation.py`, `c9_cost.py`, `c9b_twist_cost.py`, `c9c_repair_cost.py`, `c3b_stress.py`, `c3c_repeat.py`, `c3d_card_check.py`, `run_all.sh`, `make_review.py`).
- Untouched: `sprites.py`, `sprite_page.js`, `camrig.py`, `stubroom.py`, `__init__.py`, `tests/`.
- How to run: `cd v3/stage/review && ./run_all.sh` (all checks on `v3/stage`, about 15 minutes at 2 threads), `./run_all.sh before` (the builder's version), `RV_PERSISTENT=1 RV_TAG=after_persistent python3 c3_sequence.py` (the guarded persistent mode), `python3 make_review.py` (this file).
- Working files: `v3/tmp/stage_review/` (`orig/` = the builder's version, `before/`, `after/`, `logs/`; sheets `after/c5_stills.jpg`, `after/c5_move.jpg`, `after/c5_reverse.jpg`, `after/c8_*.jpg`, `after/c3/in_order_sheet.jpg`, `after/c4_colour_proxy.jpg`, `after/c6_stills.jpg`).
