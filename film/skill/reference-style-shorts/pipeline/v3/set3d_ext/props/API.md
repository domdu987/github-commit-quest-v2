# v3/set3d_ext/props/office_props.py : office props, cameras and marks for the office_day shots (plan build step 4)

An extension module. It imports `v3/set3d/office3d.py` and adds objects to the scene after `office3d.build()`. It does not edit `office3d.py`, `textures.py` or the paper. Paper artwork is read by registry name from `v3/paper/tex/registry.json`. Every item was present, so there are no placeholders (`PA['placeholders'] == []`). A missing name would become a magenta striped card listed in `office_props.PLACEHOLDERS`.

```python
import sys; sys.path.insert(0, PROJ + '/v3/set3d'); sys.path.insert(0, PROJ + '/v3/set3d_ext/props')
import office3d as S, office_props as X
A  = S.build('INTERIOR_DAY')          # the reviewed set
PA = X.build(A)                       # collection PROPS, control empty 'props_ctl'; returns anchors (section 3). Clean map (X.reset()).
cam = S.make_camera(X.all_cams(A, PA)['label_insert'])   # set cameras + the new ones
X.set_chalk(0.4, frame=350)           # every setter: frame=None sets the state statically, frame=N inserts keyframes
```

`build(A, hi_map=False, replace_teletype_sheet=True, ghost_spinners=3)`. It is deterministic and can be rerun: the PROPS collection and the `*_px_*` materials are rebuilt each time. All materials come from `office3d.mat_lit`, so they follow the preset's light model: ambient, key, form and falloff, with no new light. Every prop object gets `no_bounce`. Map decals (chalk, ghosts, smudge, tick) cast no shadow. The spinner, label, ruler, sheet, calendar leaf and stamp cast hard shadows.

Scalar controls are custom properties on `props_ctl`, read by shader nodes and shape keys through simple-expression drivers, the same pattern as the set's `track_ctl`. Transforms and visibility are keyed directly on the objects. Visibility keys use CONSTANT interpolation; all other keys use LINEAR. Check: keyframed states render identically to the same states set statically (`prove.py keyed`: max pixel difference 0). Key every frame while the chalk grows, because its arrow head follows the curve. Key the spinner angle every frame.

## 1. Props and setters

| Setter | What it does (shots) |
|---|---|
| `reset()` | Clean map of shot 4: everything hidden or at 0, teletype feed in, calendar leaf 20 flat. The red track is still `S.set_track`. |
| `set_spinner(u=None, xz=None, angle=None, wobble=0, squash=1, scale=1, show=1, fast=None, pin_out=0, which='spinner', frame)` | Storm spinner: `spinner_disc` art, 0.16 D, 0.022 D proud of the paper on a brass pin, hard shadow on the map. Position is `u` along the track or `xz` on the map. `angle` in degrees, clockwise. `wobble` in degrees. `squash` keeps the area. `show` 0/1 doubles as a pop scale. `fast` 0..1 blends in a rotationally blurred disc. `pin_out` is the depth the thumb pushes the pin in. `which='ghost1..3'` are the grey ghost copies (shared opacity `props_ctl['ghost_spinner_alpha']`). `spinner_angle(t)` gives (angle, wobble) for 0.5 rev/s with a 3 deg wobble (shots 5-11, 19-22, 25). |
| `set_chalk(grow, crumble=0, alpha=1, head=True, frame)` | White dashed chalk curve, 0.020 D wide, 0.055 D dashes. It runs from the storm up the coast, bends north-east at `CHALK_BEND` (0.29, 2.06), where the ruled red line passes it at u about 0.45, and sails out to sea. The arrow head rides the growing tip. `crumble` breaks the chalk up. `chalk_point(g)` gives the point and heading (shot 7 on). |
| `set_ghost(i, grow, alpha=None, frame)`, `ghost_fan_keys(f_first, every=3)` | Six faded grey-blue old tracks (fountain, each recurving out to sea, none reaches N.Y.). Small arrow heads show with the last 3 %. Alpha rests at 0.35. `ghost_fan_keys` keys the shot 7 fan: one track every 3 frames, a flash to 0.75, then settle at 0.35. |
| `set_tick(alpha=1, scale=1, xz=None, rot_deg=-12, frame)` | Tick-stamp impression (`tick_stamp`, 0.20 D) next to the chalk bend. `scale` 1.25 -> 1 gives the thunk (12.95). |
| `set_ruler(on, side=0, frame)` | Wooden ruler, 1.30 x 0.11 x 0.014 D, maple face with tick marks and no lettering (`tex/ruler_face.png`). `on=1` lays it flat on the map with its east edge on the red line, west of the line, so it never covers the line or the chalk. `on=0` lifts it 0.45 D into the room, swung and tipped; it is hidden below 0.02. Key 0 -> 1 for the slap-on (18.22) and 1 -> 0 for the whip-off (19.1) (shots 9, 11b). |
| `set_ruler_hand(loc, angle_deg=0, facing=(0,-1,0), show=1, frame)` | A second copy for the hand (11d "like a rifle"): centre at `loc`, which is the hand point the shot solved, in the plane facing `facing`. |
| `set_label(show=1, tilt_deg=4, swing_deg=0, away=0, scale=1, curl=0, flutter=0, pin=1, pin_out=0, res=None, raise_d=0, frame)` | Nickname label 'ทางด่วนพายุ' (`nickname_label`, 1.15 x 0.34 D) on `label_rect`. It hangs and swings about its red pin at the paper's `LB_PIN` (0.50, 0.045 from the top-left: world (0.05, -0.054, 3.395); see section 5). `away` + `scale` give the slap. `swing_deg` is the 4 deg rock or the tap swing. `curl` is the lower-right corner shape key; `flutter` is a ripple toward the room. `pin` / `pin_out` thumb the pin home (28.25). `res='hi'` uses the 2400 px art for label_insert; the default is 1200 px. `raise_d` = the plan's 0.1 D fallback. `label_corners()` gives the world corners and pin. |
| `set_smudge(level, frame)` | Pink smudge halo round the line, `level` 0..3 continuous: 1 = N.Y. end, 2 = upper half, 3 = whole line (shot 11). The set's own erase smudge stays `S.set_track(line, erase)`. |
| `set_crumbs(amount, frame)` | 70 pink eraser crumbs (3D) on the chalk ledge under the N.Y. end, revealed in a fixed random order (11d). |
| `set_sheet(loc=None, facing=None, roll_deg=0, show=1, scale=1, word1=1, word2=1, stamp=1, pop1=0, pop2=0, bow=0, frame)` | Forecast sheet quad, 1.08 x 1.40 D. Layers: `forecast_sheet_base` + `forecast_stamp` + `forecast_word_1/2` + an ink-bloom halo per word. `pop` 1 -> 0 over 4 frames = scale 1.08 + bloom (30.85, 31.30). `bow` 0..1 bends it (alternate small values to tremble). It faces `facing`, which is a world point. `sheet_fill_camera(center, facing, fill)` gives the square-on end camera. Finger balls are the shot's sprites (shot 14). |
| `set_teletype(feed=1, stamp=0, yaw_deg=0, show=1, frame)` | Paper feed. The forecast art at half size (0.54 x 0.70 D) rises out of the slot (z 1.88); a shader clips everything below the slot. `stamp` = stamp layer. `yaw_deg` turns it toward the camera: -45 reads well from `window_tt` (default 0 faces -y). `show=0` after the tear. By default `build` deletes the set's blank paper box from the `teletype` mesh, at runtime only (`STATE['tt_removed_faces']`). |
| `set_stamp(loc=None, face_dir=(0,0,-1), roll_deg=0, scale=1, show=1, frame)` | 3D rubber stamp: wooden base, neck and knob, rubber face `stamp_face`, 0.17 D across at scale 1 (scale 2 matches the full-size sheet's impression). `loc` = face centre; `face_dir` = into the paper (29.82). |
| `set_calendar(day=20, lift=0, flutter=0, tear=0, frame)` | The set's `calendar_face` is hidden. In its place: pad `calendar_pad_21` on `calendar_rect` plus a leaf `calendar_leaf_20` hinged at its top edge, with two shape keys, `lift` and `flutter` (alternate them for the 5.6 s flutter). `tear` 0..1 makes the leaf fly off. `day=21` shows the pad only, with WEDNESDAY on top (shots 17, 18, 25). |
| `set_map_res(hi)` | Swaps the map paper image to `tex/map_6000.png` (2000 px per D, the set's own `textures.wall_map` drawing re-rastered by `make_hi_map.py`) and back. One setting per take: use `hi=True` only for lens positions under about 1 D (9c corridor_cam, 19, 20, 22). It does not draw Long Island; that is step 9. |
| `track_shadow_report()` | `office3d.track_shadow_report()` plus the pinned label. Returns `track_shadowed` (actors), `track_prop_shadowed` (our own spinner on u 0-0.05, expected), `ny_label_shadowed`, `label_shadowed`, `label_by_blocker`, `label_actor_shadowed`, `ok` (no actor shadows any of them). |
| `add_markers(PA)` | Camera-only debug spheres on every new anchor (yellow = map props, white = chalk control points, orange = label corners and pin, cyan = marks, magenta = sheet / teletype, green = calendar). |
| `push(setup, factor, toward)`, `all_cams(A, PA)` | Helpers. |

## 2. Cameras (`PA['cams']`, {loc, look_at, lens} (+ `up`)) with projected heads (from `prove.py stills`, 720x1280)

| name | shot | loc | look_at | measured |
|---|---|---|---|---|
| `calendar_cam` | 4 landing | (-1.605, -1.152, 3.921) | (-1.84, -0.048, 3.99) | Calendar about 410 px wide, 12 deg rake, centre y 551; lens under the shades (z 3.92) |
| `spinner_rake` | 5 end of fly-in | `_aim(storm, 0.92 D, yaw 48, pitch 10)` | | insert_rake family, lens below-left |
| `coast_rake` | 5 pull-back | (-1.198, -0.906, 1.578) | (0.022, -0.052, 2.126) | FLA. at left, N.Y. in the top half (the measured Storm y 924, N.Y. y 424 were taken on an older pose and are unverified for this one) |
| `low_three` | 6 | (2.40, -6.20, 1.0) | yaw 22 deg off the normal, +17 deg | senior_a 129 px x 230, chief 142 px x 343, senior_b x 501; sign above the hats, partly overlapped (see section 5) |
| `chalk_rake`, `chalk_wide` | 7a, 7b | `_aim(CHALK_BEND, 0.92, 58, 18)`, `_aim((0.30, 2.32), 2.05, 12, 4)` | | 7b: whole western Atlantic, sign edge at top |
| `high_wide` | 9a | (-0.45, -6.45, 4.0) | (-0.5, -0.6, 1.4) | Hero 127 px between senior_a 194 px (x 153) and the chief 198 px (x 535); senior_b 211 px cropped at the right edge |
| `insert_front` | 9b | 1.5 D from the track at u 0.42, yaw 10, pitch 6 | | Storm y 864, N.Y. y 346 |
| `corridor_cam` | 9c (19, 20 and 22 used the mechanism module's camera of the same name, at another position: see mech/API.md) | (0.273, -0.45, 1.398) | track_point(0.8), `up` (0, -1, 0) | 0.40 D off the paper on the line's extension below the storm; N.Y. at (360, 596), the line runs up the frame centre |
| `low_boss` | 10(1) | (1.92, -4.40, 1.2) | (1.45, -0.42, 2.27) | Chief 181 px at (333, 536) = 0.42 H |
| `G` | 10, 18, 25 | (1.55, -4.95, 2.85) | (1.25, -0.40, 2.62) | Chief 173 px (368, 597), hero at `gloat_near` 244 px (619, 696), ratio 1.41, far head 99 px higher; N.Y. (178, 637) |
| `G_prime` | 18 | G's loc, lens 30.36 | (0.95, -0.40, 2.80) | x1.38 as a zoom from G's exact pose, centred between the chief (442, 623) and the label; hero cut at the right edge. `G_prime_dolly`: the same x1.38 as a dolly (hero mostly out) |
| `insert_rake_ny` | 11a/b | (-1.30, -0.66, 2.55) | (0.30, -0.05, 2.74) | |
| `low_two_wall` | 11c | (0.40, -3.70, 1.2) | (0.40, 0, 2.12) | Hero 224 px x 147, chief 218 px x 556, +14 deg |
| `label_insert` | 13 | (-0.249, -1.811, 2.887) | (0.125, -0.05, 2.87) | Label about 470 px wide centred at y 465; arrow head and N.Y. at y 750 |
| `window_tt` | 14a | (-3.2, -2.6, 2.1) | (2.6, -1.0, 1.85) | Hero at `hero_tt` 340 px x 189, chief at `chief_tt` 146 px x 479, teletype between them |
| `sheet_full` | 14c | square-on 1.17 D in front of `sheet_hold` | | Sheet fills the width |

`PA['paths']`: `persist_steps` = [a `insert_rake_ny`, b the same 0.4 D lower, c `low_two_wall`, d `high_two_shot`]; also `flight_shot4`, `shot5`, `shot7`, `shot9`, `shot10`, `shot14` (camera name lists for each shot's key poses).

## 3. Marks and anchors (`PA`)

`marks`:
- `teletype_mark` (2.25, -1.70): shot 4 chief.
- `hero_tt` (-1.10, -1.50) and `chief_tt` (2.20, -1.95): shot 14.
- `senior_a_row` (-0.70, -1.20), `chief_row` (0.35, -1.45), `senior_b_row` (1.40, -1.20): shot 6.
- `senior_a_front` (-1.55, -2.62), `chief_front` (0.40, -2.62), `senior_b_front` (1.25, -3.05): 9a.
- `gloat_near` (2.40, -1.70): G.
- `senior_a_desk` (-1.95, -3.00), `senior_b_desk` (0.20, -2.80), `chief_wall12` (0.0, -0.55): 12, with the hero at `hero_mark`.

Other anchors: `sheet_hold` (1.75, -2.20, 2.05) and `sheet_face` (its normal points to (-0.6, -0.8, 0), so the sheet is in the sun beam and lit), `teletype_feed`, `chalk_ctrl`, `chalk_bend`, `ghost_ctrl`, `tick_xz`, `label_pin`, `ruler`, `spinner_d`, `stamp_face_d`, `calendar_leaf_hinge`, `crumbs_area`, `placeholders`.

## 4. Proof (`prove.py`, outputs in `out/`)

- Stills: `out/stills/*.png` and `stills.json` (20 cameras, 360x640, 8 samples, 2 threads, placeholder actors where the plan has actors). Sheets: `sheet_stills_a.jpg`, `sheet_stills_b.jpg`, `sheet_fix1.jpg`. Reference frames compared: `ref_sheet.jpg` (a/t36.0 calendar, t10.0 fly-in, t12.5 row of old hands, t16.0 low boss, t20.0 two-shot, t39.5 macro, t48.5 rail view, t32.0 paper held up, b/t05.0 punch-in, t22.5 laughers, t19.0, a/t45.0).
- Strips, 5 states per prop: `out/strips/strip_*.jpg`; overview in `strips_1.jpg`, `strips_1b.jpg` (after the fixes), `strips_2.jpg`.
- Markers: `sheet_markers.jpg` (41 markers on 6 cameras).
- Final frame: `final_G_prime_all_props.png`.
- Shadow report: `shadow_report.json`.
- Timing: `timing.json`.
- hue_report:

| Set | red | orange | blue | violet | magenta | sat | val | dark | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 20 stills | 36.3 | 28.4 | 20.8 | 0.9 | 4.4 | 0.42 | 0.49 | 0.14 | all in band (cyan 7.7: map ocean) |
| 40 strip frames | 36.1 | 32.6 | 18.7 | 0.4 | 3.3 | 0.41 | 0.50 | 0.11 | all in band |

- Cost of a final frame (720x1280, 12 samples, all props present, two placeholder actors, `G_prime`): 19.7-20.6 CPU s, against 17.9 for the bare set (COLOUR.md), about 10 % more. That projects to about 5.0 s wall on 4 idle threads. Measured wall time here was 10.0-13.3 s on 4 threads and 13.8-14.8 s on 2 threads, with load 5-5.9 from other workers' renders.

## 5. Notes and deviations

- **Label pin.** The label pin uses the paper's `LB_PIN`: world x 0.05, z 3.395. The set's `label_rect.pin` says x 0.125, z 3.40. The artwork's clear spot decides.
- **Label shadow.** `label_rect` is used unchanged. `track_shadow_report`: the chief at `boss_mark` (hat) shadows 17 % of the label, its right end. With the chief 0.2 D right, at (1.50, -0.42), it is 0 and `ok`. Raising the label 0.1 D still leaves 14 %. The window bars shadow about 28-45 % of the label in INTERIOR_DAY; that is the room's light and not an actor. No actor shadows the track or N.Y. with the chief at `boss_mark` and the hero at `near_mark` or `gloat_near`.
- **label_insert distance.** The plan asks for 1.1 D from the map and a label about 480 px wide. Those two cannot both hold at 22 mm: 1.1 D would make the label about 820 px wide. The camera is 1.84 D away, keeping the 480 px width and the 12 deg rakes.
- **G'.** It is a zoom (lens 30.36) because a dolly x1.38 throws the near hero out of frame. The hero is cut at the right edge either way.
- **sheet_full.** It faces the sheet square-on. The sheet is turned toward the window so that it is lit; from `window_tt` it would be backlit and blue-grey. The crash push therefore also swings about 34 deg.
- **low_three.** It is 6 D from the trio because the sign clears the hats only from that far at 1.0 D lens height. The heads are 129-142 px. The sign is still partly overlapped until the crane-up of shot 6.
- **Not in this module (cast lane):** pencil stub and worn eraser sprites, the puppet paper tape, hand close-up sprites, the puppet-drawn ruler.
- **office3d.py edits:** none were needed.
