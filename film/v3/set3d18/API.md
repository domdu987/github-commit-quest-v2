# v3/set3d18/jimo.py : film 18 set ("ไอ้เสมียนวัว", Tian Dan's fire oxen at Jimo, Qi vs Yan, 279 BC) (bpy 5.3, Cycles CPU)

The production set, grown from the style board (board/NOTES.md). Four locations, three light presets, 26 named shot cameras, state setters keyed per frame, fire that flickers per frame, flame cards for the 2D oxen.
**No depth of field anywhere (`make_camera` forces it off). No text anywhere** (banners and pennants are plain shapes). The 3D placeholder ox is NOT in production: the oxen are 2D puppet cards; `debug_ox()` builds it hidden-by-default for debugging only.

## Files
- `jimo.py`: core (presets, materials incl. the warm / cool wall material, live fires, flame cards, states, cameras, foreground props, placeholders, CLI).
- `jimo_wall.py`: the wall (both faces, 12 breaches, gate leaves, torches, ramps...), gate hall, city roofs, moat (water + dry ditch), bridge, road, fields, far Yan camp (jimo_out).
- `jimo_in.py` (inside Jimo), `jimo_camp.py` (yan_camp), `jimo_vista.py` (the Qi plain), `jimo_ox.py` (debug ox only), `jimo_shots.py` (shot table, motion, marks, herd), `jimo_tex.py` (painted textures, cache `tex_jimo/`, bump `TEX_V` after editing a painter), `jimo_hue.py` (hue rows), `jimo_sheet.py` (contact sheets).
- `contact.jpg` / `contact_small.jpg`: one 720x1280 final (12 samples) per shot camera at the MIDDLE of the move (t = 0.5, the shot's mid state), with flat placeholder cards at the stand marks (`ACTORS=0` leaves them out); label under each tile, cyan line at y 880.
- `set_work/`: `final/` (the 26 PNGs + `sNN.json` meta: head rows, wall polygons), `final_log.txt`, `hue_rows.txt`, `stills/` (drafts).
- Rebuild everything: `python3 jimo.py final` (26 finals, one build + one render each), then `python3 jimo.py meta`, `python3 jimo.py contact`, `python3 jimo_hue.py rows`.

## Build and CLI
```python
import jimo as J
A = J.build('jimo_in', 's01')            # location, preset, light=None;  preset = a shot 's01'..'s26' (location and light come from it) or the location name (default camera 'wide')
cam = J.shot_camera('s01', 0.5)          # pose the scene camera at t of the move (builds the shot's foreground prop, parented to the camera)
J.key_camera('s01')                      # or key the whole move, one LINEAR key per frame from the shot's first film frame (f0)
J.apply_state('h6')                      # or the setters below
J.T.render(path)                         # tower.render
```
`A` = dict(location, preset, light, cams (all cameras of the location, each with start / mid / end poses), cam (the preset start camera), key_dir, render, marks, heights, lights, shot).
`J.build(location, preset, light)`: locations `jimo_in` (NIGHT DUSK), `jimo_out` (NIGHT DUSK DAWN), `yan_camp` (NIGHT DUSK), `vista` (DUSK DAWN). Render settings: 720x1280, Cycles CPU, 12 samples, OIDN, **2 threads**.
CLI: `python3 jimo.py stills [spec ...]` (draft 360x640, 6 samples) | `final [spec ...]` | `digest [spec]` | `meta [spec]` | `contact`. spec = `s16` | `s16@0.3` (t of the move) | `s16:NIGHT` | `s16@0.5:NIGHT:h8,g0.3` (state string) | `jimo_out` (default camera). No spec = all 26 shots.
`digest` prints a hash of the built scene (same in two processes).

## World (D, Z up)
1 D = one head. The wall runs along x at y = 0 (outer face y -5 at the base -> -3 at the top, inner face y +4 -> +3; height 16, walk z 16; 7-8 D thick). Gate in the middle (x +-3.6, 9.6 high). Adult 3.0-3.4 D tall, child 2.0, ox 2.6 D at the withers (card 3.2 with horns, 4.5 long).
- **jimo_in** (y > 4): ring lane y 4.2-12.7 along the wall; ox yard x -50..50, y 12.7-26.7 (trampled earth) with 11 tripod braziers, reed-bundle jars (y 15-17), picks / baskets (y 7); four pens (y 31-41), troughs, hay; east quarter of tiled houses with courtyard gates facing the lane (x 58 / 74 / 89, gate y 23); market lane x -69 (stalls at x -77 facing +x and x -61 facing -x, y 14-62; the clerk's stall at (-77, 22)); two rows of houses and two drum towers beyond; earth ramps up the inner face at x +-62. Dusk / night.
- **jimo_out** (y < -5): wall + gate hall + city roofs behind, berm, moat y -30..-9.5 (water for |x| < 12.5 and |x| > 46, a dry silted ditch with reed tufts between), timber bridge at the gate, 11 D road to y -300 with torch stakes, patchwork fields, 70 trees, hay, the far Yan camp (tents, fires, palisade, pennants at y -150..-215), hills.
- **yan_camp**: tent rows (14 tents, each its own object), the general's pavilion (-27, -47), 5 fires (f0 (3,-99) f1 (5.5,-85) f2 (-6,-72) f3 (7,-68) f4 (-4,-57)), the table with jars and cups (-4.5, -100.5), 2 chariots, drums, spear racks, shields, hay, horses, black-and-red pennants, the **rampart** (-4, -47.5, top z 2.6, marks.rampart), the palisade at y -40 with a gap x +-6.2, the Jimo wall 40 D away (moat and bridge at y -30..-9.5).
- **vista**: terrain 920 x 820 D, river `y = 150 - 0.11 x + 40 sin(x/95)`, 62 ordinary walled towns (20-45 D across) + Jimo (35 x 56 D, near, (30, -30)) with a ring moat and the Yan siege camp (16 tents, fires) to its south, and Ju (far, (-95, 330)). Roads link Jimo to Ju. Plain shapes, no labels.

## Light
NIGHT (moon, blue key), DUSK (low warm sun), DAWN (cartoon-cloud dawn sky). The sun / moon azimuth per location is in `jimo.SUN_AZ` / `MOON_AZ_LOC`; the sky dome and moon follow the camera (handler). Lamps / torches / braziers are real point lights (1.0, 0.50, 0.18) with halos; `lamps` factor dims them at DUSK / DAWN.
**The wall material reads OCHRE where fire-lit and BLUE moon-shade elsewhere.** The wall meshes are subdivided every 2 D and carry a baked `warm` vertex weight computed from the lamp positions (`STATE['warm']`); `mat_lit_warm` fades the blue ambient out and the key term keeps the full ochre where warm -> 1, adds a warm emission (art x fire colour), and the static fires' real light is excluded from the wall by light linking (collection `NOFIRE`): no rose / lavender. Dynamic lights you add later (flame cards) DO light the wall.
Hue numbers are in `set_work/hue_rows.txt` (shade hue 240-260 rule, magenta share, caption band, wall edge density).

## Fire
- Every static fire (braziers, camp fires, torches, lamps) is its own flame object (origin at the flame root) with its light: `J.flicker(frame=None, k=1.0)` varies scale / sway / light energy per frame (deterministic hash of the frame, per-fire phase); with `frame=` it KEYS scale, rotation and light energy (LINEAR) - call it for every frame of a shot. A frame handler (installed by `build`) also calls it for every `frame_change_pre` / `render_pre`. `k` scales all light (0 = out).
- **`flame_card(parent=None, scale=1.0, loc=(0,0,0), name='flame', light=True, lit=1.0, energy=700)`** -> Empty `root`: a camera-facing flame card (painted layered tongues `#b8301a / #e8561c / #ffb238 / #fffeec`, 4 flicker variants chosen per frame through the custom props `fu` / `fk`) plus a warm point light (`energy` W x scale) under `root`. `root.parent = parent` (an ox card, a hand), `loc` is local to the parent, the card's bottom centre is the flame root, scale 1 = 2.2 D tall. The card tracks the scene camera through a TRACK_TO constraint (`make_camera` retargets it). `J.set_flame_card(root, lit, frame=None)` switches it on / off (keyed). `flicker()` drives all flame cards. Lit tails: lit = 1; plain: lit = 0.
- `J.live_flame(base, h, s, lean, seed, n, spread, light, name)` builds a mesh flame + light anywhere.

## State setters (all take `frame=None`; with a frame they KEY, constant for visibility, linear for transforms)
- `set_holes(n)`: ragged breaches in the wall base, n = 0 .. 12 (float: 6.5 = six open, the seventh half dug). 12 centres `HOLE_X` = x -41 .. -13.5 and 13.5 .. 41 (spacing 5.5), 3.4 wide x 4.3 high, on both faces; plug sinks, rim + rubble + props grow, a heap of dug earth + pick + basket appears inside. Available in jimo_in, jimo_out (and invisible far away in yan_camp).
- `set_gate(k)`: gate leaves 0 shut .. 1 open 75 deg outward (0.15 = a crack, with a warm glow behind in jimo_out).
- `set_party(k)` (yan_camp): 16 extra cups (+ jar) pop in one by one; the crowd marks are `marks.party_crowd` of shot s13.
- `set_rout(k)` (yan_camp): tents fold (staggered z-scale to 0.12 + tilt), 30 pots / helmets / fodder bundles / bowls fly in arcs and scatter, chariot `chariot0` rolls away and turns. Comic, nothing gory, no bodies.
- `set_pennants(k, side='yan')` (vista): black Yan pennants pop up one by one over the 62 ordinary towns, k 0 .. 1. `side` = the ORDER: `'yan'` (scattered, fixed), `'ltr'`, `'rtl'`, `'near'`, `'far'`. The two holdouts (Jimo, Ju) never get one.
- `set_qi_return(k)` (vista): the pennants turn to Qi colours (red with teal trim) one by one; the holdouts keep their Qi pennant up from the start and stay warm-lit (windows, halo, gate fires, light pool).
- `animate(setter, f0, f1, v0, v1)` keys any setter over frames, eased: `J.animate(J.set_holes, 1205, 1309, 0, 12)`; for staggered pennants key the setter every frame (the default step 1 does).
- `apply_state('h6,g0.3,pt1,ro0.5,pn0.5,qr0.5,fl1')`: the string form used by the CLI and the shot table.
- Cameras: `shot_camera(name, t)`, `key_camera(name)`, `make_camera(setup)` (setup = {loc, look_at, lens}); every shot has `cams[name] = {loc, look_at, lens, start, mid, end, frames, f0, f1, fg}`.
- Foreground props (1-2 D from the lens, 30 % scale, parented to the camera so they stay put through the move): lantern, wheel, spear_rack, jar, pick_baskets, reeds, counter, torch; built by `shot_camera`.

## Herd helper
`jimo_shots.herd(n, a, b, width=6.0, seed=1)`: N marks `(x, y, 0, yaw_deg, scale)` along a lane / field from point a to point b (x, y) with lateral spread `width` D; rows staggered and jittered, about 3.6 D apart along and 3 D across; yaw = direction of travel (degrees from +x, ox cards in side view), scale 0.93-1.07; sorted far to near (paint order). `J.S.herd` is the same function. The shots use it: s01 (8 dressed oxen along the wall), s02 (34 in the lane), s06 (10 in front of the gates), s07 (120 in the yard + 90 far = 210 visible), s19 (40 + 30 Qi soldiers), s20 (36), s21 (60).

## Marks
Stand marks are world points; heads must stay above y 880: `J.head_rows(shot)` prints (role, t, mark, head top y, chin y, feet y) at t = 0, 0.5, 1; the report numbers are in `set_work/final/sNN.json`.
Heights: tiandan 3.0, general 3.4, soldier 3.2, townsfolk 3.0, child 2.0, envoy 3.0, ox 2.6 (`J.HEIGHT`).

## Cameras and stand marks per shot (generated from jimo_shots.py)

Camera poses are `loc -> look_at` (D) and lens (mm). `start` is the pose at t = 0 of the shot, `end` at t = 1; `J.shot_camera(name, t)` poses the scene camera for any t and `J.key_camera(name)` keys the whole move. Marks are world points (x, y, z) with the card yaw (deg about z; a person card faces -y at yaw 0, the printed yaw turns it to face the START camera; ox / herd cards: yaw = direction of travel from +x, side view), ox marks may carry a scale. For long lists only the first 6 are printed here; `jimo_shots.marks_for("sNN")` returns them all.

### s01  (frames 0-78, jimo_in, NIGHT)
- lantern-lit ox yard, eye, push 8 %/s, slide right; Tian Dan dresses an ox, a row of dressed oxen along the wall behind
- camera start (-14.0, 26.0, 2.5) -> (4.0, 8.0, 5.2) lens 24; end (-12.462, 20.05, 3.062) -> (1.794, 5.794, 5.2); move: push +0.08 /s, slide +40 px/s; fg prop: ('lantern', 'right'); state at mid: `-`
  - tiandan (1): (-4.1, 16.81, 0) yaw -132.9
  - ox (6): (-6.29, 14.62, 0) yaw -145.9; (-6.72, 11.36, 0) yaw -153.6; (-6.58, 7.97, 0) yaw -157.6; (-6.22, 4.79, 0) yaw -159.9; (-5.66, 1.82, 0) yaw -161; (-4.45, -1.22, 0) yaw -160.7
  - herd (8): (0.44, 9.33, 0) yaw 184.4 s1; (2.43, 9.31, 0) yaw 183.1 s1.01; (11.61, 9.3, 0) yaw 174.2 s1.05; (9.62, 9.19, 0) yaw 185.9 s1; (6.87, 9.02, 0) yaw 181.7 s0.95; (14.21, 8.97, 0) yaw 178.4 s1.01 ...

### s02  (frames 78-156, jimo_in, NIGHT)
- low 1.2 D along the ring lane, pull-out reveals dozens of dressed oxen filling the lane (herd helper)
- camera start (-28.0, 11.5, 1.2) -> (12.0, 10.5, 3.0) lens 20; end (-35.28, 11.682, 0.872) -> (12.0, 10.5, 3.0); move: push -0.07 /s, slide +0 px/s; fg prop: ('pick_baskets', 'left'); state at mid: `-`
  - tiandan (1): (-19.02, 10.68, 0) yaw -95.2
  - ox (1): (-17.57, 8.74, 0) yaw -104.8
  - herd (34): (42.67, 10.36, 0) yaw 7.2 s0.99; (44.17, 10.31, 0) yaw 1.3 s0.97; (40.32, 10.29, 0) yaw -0.9 s0.99; (38.8, 10.21, 0) yaw -3.2 s0.99; (34.8, 10.19, 0) yaw -4.1 s1; (29.75, 10.11, 0) yaw -2.5 s0.94 ...

### s03  (frames 156-297, vista, DUSK)
- establishing high, push 6 %/s, slide left; the black Yan pennants pop over the towns one by one (set_pennants 0 -> 1 on 7.32-9.89 s)
- camera start (70.0, -215.0, 105.0) -> (0.0, 70.0, -10.0) lens 20; end (-30.665, -154.506, 72.57) -> (-80.925, 50.124, -10.0); move: push +0.06 /s, slide -40 px/s; fg prop: none; state at mid: `pn0.5`

### s04  (frames 297-384, vista, DUSK)
- high, push-in toward the near lit town Jimo (marks.jimo) on "จี๋โม่" (11.91 s); two towns stay lit (Jimo near, Ju far)
- camera start (52.0, -150.0, 80.0) -> (28.0, -30.0, 6.0) lens 22; end (47.128, -125.64, 64.978) -> (28.0, -30.0, 6.0); move: push +0.07 /s, slide +0 px/s; fg prop: none; state at mid: `pn1`

### s05  (frames 384-459, jimo_in, DUSK)
- market lane, the clerk stall at (-77, 22) faces +x; Tian Dan behind the counter, townsfolk hand him a sash
- camera start (-63.0, 12.5, 2.4) -> (-77.0, 22.5, 4.4) lens 22; end (-65.8, 14.5, 2.8) -> (-77.0, 22.5, 4.4); move: push +0.08 /s, slide +0 px/s; fg prop: ('counter', 'right'); state at mid: `-`
  - tiandan (1): (-76.2, 22, 0) yaw 90
  - townsfolk (3): (-72.6, 20, 0) yaw 130; (-71.6, 23.4, 0) yaw 230; (-70, 21.6, 0) yaw 200
  - child (1): (-72, 25.4, 0) yaw 190

### s06  (frames 459-531, jimo_in, DUSK)
- eye, slides left 40 px/s along the ring lane in front of the house gates (x 58 / 74 / 89, y 23); townsfolk lead oxen out of the gates; ten oxen at "สิบตัว"
- camera start (84.0, 9.0, 2.4) -> (72.0, 23.0, 4.0) lens 22; end (82.275, 7.522, 2.4) -> (70.275, 21.522, 4.0); move: push +0 /s, slide -40 px/s; fg prop: none; state at mid: `-`
  - tiandan (1): (76, 12.5, 0) yaw 180
  - townsfolk (4): (58, 17, 0) yaw 180; (74, 17, 0) yaw 180; (89, 17, 0) yaw 180; (66, 11, 0) yaw 180
  - herd (10): (91.86, 28.8, 0) yaw 4.9 s1; (66.3, 28.73, 0) yaw -0.2 s0.97; (82.92, 28.71, 0) yaw 3.7 s0.99; (71.65, 28.69, 0) yaw -2.7 s1.04; (80.75, 28.63, 0) yaw 4.1 s0.98; (68.38, 28.61, 0) yaw -0.4 s1.04 ...

### s07  (frames 531-597, jimo_in, DUSK)
- high 4-5 D from the north end of the yard, pull-out with a snap x1.6 on "พันกว่าตัว": the whole quarter packed with oxen (herd helper ~200 + silhouettes)
- camera start (3.0, 46.5, 6.0) -> (0.0, 8.0, 1.5) lens 18; end (5.539, 79.086, 9.809) -> (0.0, 8.0, 1.5); move: push -0.07 /s, slide +0 px/s, extra [{'t': 0.55, 'd': 1.6, 'dur': 7}]; fg prop: none; state at mid: `-`
  - herd (120): (34.73, 34.61, 0) yaw 6.1 s0.98; (27.73, 33.48, 0) yaw 5.5 s0.99; (21.96, 32.82, 0) yaw 12.9 s1.02; (37.6, 32.59, 0) yaw 12.6 s1.03; (15.81, 31.34, 0) yaw 11.1 s1.06; (30.94, 31.08, 0) yaw 6.9 s1 ...
  - herd_far (90): (93.27, 78.24, 0) yaw 10.6 s1.04; (59.76, 76.54, 0) yaw 10.6 s0.95; (68.95, 74.47, 0) yaw 5.4 s1; (81.56, 73.27, 0) yaw 7.1 s0.98; (90.04, 71.81, 0) yaw 13.5 s0.97; (31.98, 71.73, 0) yaw 5.5 s0.97 ...

### s08  (frames 597-674, yan_camp, DUSK)
- eye, push 8 %/s, the general on the rampart (marks.rampart, z 2.6) looks at Jimo, bursts out laughing; fg spear rack
- camera start (3.0, -63.0, 2.4) -> (-4.0, -47.5, 5.0) lens 22; end (1.563, -59.817, 2.934) -> (-4.0, -47.5, 5.0); move: push +0.08 /s, slide +0 px/s; fg prop: ('spear_rack', 'left'); state at mid: `-`
  - general (1): (-4, -47.5, 2.6) yaw 24.3
  - soldier (2): (1.5, -48, 2.6) yaw 5.7; (-9, -48.5, 2.6) yaw 39.6

### s09  (frames 674-737, yan_camp, DUSK)
- QUOTE 1a medium, push 9 %/s; the general arms wide, soldiers behind him laugh
- camera start (2.0, -80.0, 2.4) -> (-3.5, -90.5, 4.6) lens 24; end (0.961, -81.984, 2.816) -> (-3.5, -90.5, 4.6); move: push +0.09 /s, slide +0 px/s; fg prop: none; state at mid: `-`
  - general (1): (-3.5, -90.5, 0) yaw 152.4
  - soldier (3): (-7, -96, 0) yaw 30; (0.5, -97, 0) yaw 10; (-4, -99, 0) yaw 15

### s10  (frames 737-853, yan_camp, DUSK)
- QUOTE 1b medium-close, push 10 %/s then a slight slide; thumb at his chest, chin up
- camera start (0.5, -85.0, 2.4) -> (-3.5, -90.5, 4.8) lens 26; end (-0.437, -87.57, 3.328) -> (-2.89, -90.944, 4.8); move: push +0.1 /s, slide -25 px/s; fg prop: none; state at mid: `-`
  - general (1): (-3.5, -90.5, 0) yaw 144
  - soldier (2): (-7, -96, 0) yaw 30; (0.5, -97, 0) yaw 10

### s11  (frames 853-944, yan_camp, DUSK)
- wide eye, pull-out 7 %/s with a push-in on "ไอ้เสมียนวัว" (30.64 s); soldiers round the fire at (5.5, -85) mock-moo, finger horns
- camera start (-2.0, -62.0, 2.4) -> (5.5, -86.0, 3.8) lens 20; end (-1.592, -63.305, 2.476) -> (5.5, -86.0, 3.8); move: push -0.07 /s, slide +0 px/s, extra [{'t': 0.55, 'd': 0.78, 'dur': 8}]; fg prop: ('jar', 'left'); state at mid: `-`
  - soldier (6): (2.5, -81.5, 0) yaw 200; (8.5, -82, 0) yaw 170; (9.8, -86.5, 0) yaw 130; (2, -87.5, 0) yaw 250; (5.5, -89.5, 0) yaw 190; (-1, -84, 0) yaw 230
  - general (1): (-2.5, -92, 0) yaw 200

### s12  (frames 944-1003, jimo_out, DUSK)
- eye low, slides right; the gate opens a crack (set_gate 0.15); the envoy bows on the bridge; old folk and women stand on the wall walk (z 16, no soldiers)
- camera start (-14.0, -42.0, 1.7) -> (2.0, -12.0, 4.6) lens 24; end (-11.224, -43.48, 1.7) -> (4.776, -13.48, 4.6); move: push +0 /s, slide +40 px/s; fg prop: ('wheel', 'left'); state at mid: `g0.15`
  - envoy (1): (0, -22, 0) yaw 180
  - townsfolk (6): (-14, 0.4, 16) yaw 180; (-10, 0.4, 16) yaw 180; (-6.5, 0.4, 16) yaw 180; (6.5, 0.4, 16) yaw 180; (10, 0.4, 16) yaw 180; (14, 0.4, 16) yaw 180
  - child (1): (-16.5, 0.4, 16) yaw 180

### s13  (frames 1003-1071, yan_camp, NIGHT)
- wide high, pull-out 6 %/s; the camp party (set_party 1): cheering-crowd marks round the fires, cups, a sentry drops his spear and joins in
- camera start (0.0, -54.0, 12.0) -> (2.0, -86.0, 2.0) lens 20; end (-0.272, -49.648, 13.36) -> (2.0, -86.0, 2.0); move: push -0.06 /s, slide +0 px/s; fg prop: none; state at mid: `pt1`
  - party_crowd (14): (-6, -92, 0) yaw 200; (-2, -93, 0) yaw 210; (1.5, -90, 0) yaw 190; (8.5, -80, 0) yaw 180; (3, -80, 0) yaw 190; (-4, -76, 0) yaw 200 ...
  - sentry (1): (-14, -50.5, 0) yaw 180

### s14  (frames 1071-1136, yan_camp, NIGHT)
- QUOTE 2a medium, push 9 %/s; the general raises his cup and laughs, bounce; fg wine jar
- camera start (2.0, -86.0, 2.4) -> (-4.3, -96.2, 4.5) lens 24; end (0.772, -87.989, 2.809) -> (-4.3, -96.2, 4.5); move: push +0.09 /s, slide +0 px/s; fg prop: ('jar', 'right'); state at mid: `pt1`
  - general (1): (-4.3, -96.2, 0) yaw 148.3
  - soldier (2): (-8, -101, 0) yaw 30; (0.5, -101.5, 0) yaw 10

### s15  (frames 1136-1205, yan_camp, NIGHT)
- QUOTE 2b medium-close, push 10 %/s; he mimes carving, licks his lips, the cup tilts
- camera start (-1.5, -90.5, 2.4) -> (-4.3, -96.2, 4.6) lens 26; end (-2.144, -91.811, 2.906) -> (-4.3, -96.2, 4.6); move: push +0.1 /s, slide +0 px/s; fg prop: none; state at mid: `pt1`
  - general (1): (-4.3, -96.2, 0) yaw 153.8
  - soldier (1): (-8, -101, 0) yaw 30

### s16  (frames 1205-1309, jimo_in, NIGHT)
- low inside the wall base, slides left along the wall (x 50 -> 25): the holes open one after another (set_holes 0 -> 12); townsfolk dig
- camera start (50.0, 10.5, 1.5) -> (22.0, 4.6, 3.4) lens 22; end (51.048, 5.525, 1.5) -> (23.048, -0.375, 3.4); move: push +0 /s, slide -40 px/s; fg prop: ('pick_baskets', 'left'); state at mid: `h6`
  - townsfolk (6): (13.5, 8.2, 0) yaw 180; (19, 8.2, 0) yaw 180; (24.5, 8.2, 0) yaw 180; (30, 8.2, 0) yaw 180; (35.5, 8.2, 0) yaw 180; (41, 8.2, 0) yaw 180
  - child (1): (21.5, 9.6, 0) yaw 180

### s17  (frames 1309-1388, jimo_in, NIGHT)
- eye medium, push 8 %/s; reed bundles soaked from a jar are tied to the tails; oxen lined up nose-first at the holes (marks face the wall)
- camera start (-4.0, 17.5, 2.4) -> (-27.0, 5.5, 3.6) lens 22; end (-8.845, 14.972, 2.653) -> (-27.0, 5.5, 3.6); move: push +0.08 /s, slide +0 px/s; fg prop: ('reeds', 'left'); state at mid: `h12`
  - ox (6): (-41, 8.4, 0) yaw 180; (-35.5, 8.4, 0) yaw 180; (-30, 8.4, 0) yaw 180; (-24.5, 8.4, 0) yaw 180; (-19, 8.4, 0) yaw 180; (-13.5, 8.4, 0) yaw 180
  - townsfolk (3): (-33.7, 11.5, 0) yaw 200; (-22.7, 11.5, 0) yaw 200; (-17.2, 11.5, 0) yaw 200
  - tiandan (1): (-32.2, 12, 0) yaw 160

### s18  (frames 1388-1427, jimo_in, NIGHT)
- eye, quick push-in: Tian Dan raises a torch, tails light in a ripple (flame_card on each ox card)
- camera start (8.0, 17.0, 2.4) -> (-14.0, 6.0, 4.4) lens 22; end (1.312, 13.656, 3.008) -> (-14.0, 6.0, 4.4); move: push +0.1 /s, slide +0 px/s, extra [{'t': 0.5, 'd': 0.8, 'dur': 6}]; fg prop: none; state at mid: `h12`
  - tiandan (1): (-8.5, 11, 0) yaw 120
  - ox (6): (-41, 8.4, 0) yaw 180; (-35.5, 8.4, 0) yaw 180; (-30, 8.4, 0) yaw 180; (-24.5, 8.4, 0) yaw 180; (-19, 8.4, 0) yaw 180; (-13.5, 8.4, 0) yaw 180

### s19  (frames 1427-1515, jimo_out, NIGHT)
- low wide at the wall base, WHIP pan at the end to follow the herd; oxen burst out of the 12 holes (x 13.5..41 at y -5), cross the dry ditch / bridge and the field toward the camp
- camera start (6.0, -32.0, 1.5) -> (30.0, -5.0, 3.4) lens 18; end (6.0, -32.0, 1.5) -> (34.989, -53.555, 3.4); move: push +0 /s, slide +0 px/s, extra [{'t': 0.9, 'pan': -85, 'dur': 6}]; fg prop: none; state at mid: `h12,g0.3`
  - ox (6): (13.5, -6.6, 0) yaw 0; (19, -6.6, 0) yaw 0; (24.5, -6.6, 0) yaw 0; (30, -6.6, 0) yaw 0; (35.5, -6.6, 0) yaw 0; (41, -6.6, 0) yaw 0
  - herd (40): (24.01, -6.33, 0) yaw -106.1 s0.97; (17.89, -6.41, 0) yaw -103.8 s1; (30.03, -7.6, 0) yaw -107.6 s1.01; (20.69, -8.77, 0) yaw -106.6 s0.95; (36.67, -8.87, 0) yaw -101 s0.99; (26.59, -9.14, 0) yaw -106.3 s1.01 ...
  - qi_soldier (30): (31.55, 6.88, 0) yaw -95.6 s0.94; (37.23, 6.71, 0) yaw -95.7 s1.03; (25.37, 6.61, 0) yaw -85.1 s0.98; (19.27, 5.85, 0) yaw -91.1 s1.07; (22.37, 5.33, 0) yaw -84.6 s0.99; (13.63, 5.15, 0) yaw -86.8 s1.06 ...

### s20  (frames 1515-1596, jimo_out, NIGHT)
- low, tracking beside the herd, push 7 %/s; the herd charges toward the Yan camp (far camp at y -150..-215); oxen never turn back
- camera start (22.0, -56.0, 1.7) -> (-2.0, -92.0, 3.0) lens 20; end (17.464, -62.804, 1.946) -> (-2.0, -92.0, 3.0); move: push +0.07 /s, slide +0 px/s; fg prop: none; state at mid: `h12`
  - herd (36): (3.13, -48.11, 0) yaw -98.1 s1; (9.54, -50.28, 0) yaw -105.7 s0.98; (6.25, -51.06, 0) yaw -96 s1; (12.46, -53.29, 0) yaw -96.2 s0.96; (1.15, -56.99, 0) yaw -93.8 s1.03; (7.96, -58.99, 0) yaw -94.3 s0.98 ...

### s21  (frames 1596-1683, yan_camp, NIGHT)
- eye from the Yan side at the palisade gap (x +-6): a wall of glowing red dragon monsters comes out of the dark field (y -38 .. -6); SNAP push x1.5; soldiers' jaws drop, cups fall
- camera start (0.0, -43.5, 2.2) -> (0.0, -8.0, 5.0) lens 22; end (0.0, -27.646, 3.45) -> (0.0, -8.0, 5.0); move: push +0.06 /s, slide +0 px/s, extra [{'t': 0.45, 'd': 0.67, 'dur': 6}]; fg prop: none; state at mid: `-`
  - soldier (3): (-3, -47, 0) yaw 0; (3.5, -49, 0) yaw 0; (0, -52, 0) yaw 0
  - herd (60): (-10.37, -7.46, 0) yaw -88.4 s1; (1.18, -7.57, 0) yaw -84 s1.03; (7.23, -8, 0) yaw -84.6 s0.98; (-4.68, -8.01, 0) yaw -96 s0.98; (10.72, -8.59, 0) yaw -94.5 s1.06; (-7.3, -8.69, 0) yaw -86.3 s1 ...

### s22  (frames 1683-1742, yan_camp, NIGHT)
- close-medium on ONE ox in full flare (blades, silk, flame tail) with a frozen terrified soldier
- camera start (-8.0, -34.0, 2.0) -> (3.0, -14.0, 3.2) lens 26; end (-6.053, -30.46, 2.212) -> (3.0, -14.0, 3.2); move: push +0.09 /s, slide +0 px/s; fg prop: none; state at mid: `-`
  - ox (1): (3, -22, 0) yaw -42.5 s1
  - soldier (1): (-3.5, -28, 0) yaw -36.9

### s23  (frames 1742-1807, jimo_out, NIGHT)
- high over the wall top, pull-out; fg torch; old men, women and kids beat bronze pots on the walk (walk centre y 0.4, z 16)
- camera start (-31.0, -4.5, 23.0) -> (-2.0, 0.8, 16.8) lens 22; end (-35.398, -5.304, 23.94) -> (-2.0, 0.8, 16.8); move: push -0.07 /s, slide +0 px/s; fg prop: ('torch', 'right'); state at mid: `h12`
  - townsfolk (6): (-16, 0.4, 16) yaw 180; (-11, 0.4, 16) yaw 180; (-6, 0.4, 16) yaw 180; (-1.5, 0.4, 16) yaw 180; (3, 0.4, 16) yaw 180; (7.5, 0.4, 16) yaw 180
  - child (2): (-8.5, 0.6, 16) yaw 180; (5.2, 0.6, 16) yaw 180

### s24  (frames 1807-1882, yan_camp, NIGHT)
- wide high, slide 50 px/s + push; rout (set_rout 0 -> 1): tents fold, soldiers flee, pots and helmets fly, a chariot rolls away empty; nobody hurt
- camera start (-30.0, -48.0, 15.0) -> (0.0, -82.0, 2.0) lens 20; end (-32.467, -57.736, 13.375) -> (-6.217, -87.486, 2.0); move: push +0.05 /s, slide +50 px/s; fg prop: none; state at mid: `ro0.5`
  - soldier (8): (-10, -70, 0) yaw 200; (6, -66, 0) yaw 200; (-3, -84, 0) yaw 200; (10, -88, 0) yaw 200; (-18, -92, 0) yaw 200; (14, -74, 0) yaw 200 ...

### s25  (frames 1882-1958, vista, DAWN)
- establishing high, push 6 %/s; the Qi banners return over the towns one by one (set_qi_return 0 -> 1), warm dawn
- camera start (-50.0, -215.0, 105.0) -> (0.0, 80.0, -10.0) lens 20; end (-42.4, -170.16, 87.52) -> (0.0, 80.0, -10.0); move: push +0.06 /s, slide +0 px/s; fg prop: none; state at mid: `pn1,qr0.5`

### s26  (frames 1958-2112, jimo_out, DAWN)
- low, long tracking pull in front of the running general (he runs -y toward home along the road), push-in at the end; dragon oxen trot after him with smoking tails
- camera start (4.0, -112.0, 1.7) -> (0.0, -62.0, 5.2) lens 22; end (4.29, -115.628, 1.446) -> (0.0, -62.0, 5.2); move: push -0.06 /s, slide +0 px/s, extra [{'t': 0.72, 'd': 0.82, 'dur': 10}]; fg prop: none; state at mid: `-`
  - general (1): (0.8, -72, 0) yaw 0
  - ox (3): (-1.6, -58, 0) yaw 0; (3.2, -55, 0) yaw 0; (-0.6, -49, 0) yaw 0
  - road (2): (0, -30, 0) yaw 0; (0, -150, 0) yaw 0

## Measured (set_work/hue_rows.txt, one row per contact tile; set_work/final_log.txt)
- Render at 720x1280, 12 samples, OIDN, 2 threads, one render at a time: **14.8 s wall / 29.7 s cpu per frame on average** (median 14.9 s; range 9.6-25.5 s wall, 18.8-50.9 s cpu; heaviest: s23 wall top 25 s, s21 / s22 / s07 about 17-20 s). A build is 2-5 s. 26 finals in 7.5 min.
- Magenta share (hue_report) 0.0-3.5 % on every tile (hue guard in the compositor), rose share of the wall pixels 0.01-0.06. Wall pixels at hue 230-255 (moon shade): 0.15-0.71 of the wall pixels on night tiles; ochre (20-45) where fire-lit.
- Wall edge density (own Canny-like count, calibrated on the style board's board_1 = 0.048): 0.057 (s08), 0.078 (s12), 0.043 (s23), 0.040 / 0.038 (s22 / s21), 0.014-0.033 on the others (the wall is a narrow strip or steeply foreshortened there).
- Shade hue: NIGHT 220-245, DUSK 231-265, DAWN 231 (the bible sky H 221-230 counts as shade, as on the board).
- Caption band y 880-950: mean luma 43-137 (0-255); bright (V > 0.7) pixels are lit ground / sky glow, not emitters, except s10 / s02 (sunlit ground, 30 k / 21 k px) which are brighter than the 60-110 target.

## Known weaknesses
- Wall edge density >= 0.05 only on 2 of 14 wall tiles (s08, s12); the others have the wall as a thin foreshortened strip.
- The sunset sky of DUSK (copied from the film-9 painter) is a smooth orange gradient with few clouds; yan_camp DUSK shots look into the sun glow (s09 / s10 / s11 are backlit).
- jimo_out NIGHT fields (s19 / s20) read as a flat blue plane at night: low texture contrast; the far Yan camp is small silhouettes.
- Foreground props are 30 % scale (a 3 D lantern would not fit at 1-2 D from the lens), parented to the camera; s17 reed bundles and s05 counter are chunky.
- Placeholder cards in the contact sheet are crude flat silhouettes (head rows are right, the look is not the cast).
- The wall material's `warm` weights are static (baked from the fixed lamps); the dynamic flame-card lights light the wall with the plain material (orange over blue, fine near the light, mauve at medium distance, which the hue guard pushes toward coral).
- Camp geometry (palisade y -40, wall 40 D away) is closer than the open field of jimo_out (road to y -300, far camp at y -150..-215); the two locations do not share one world.
- `hue_guard` is a compositor trick (hue correct on 255-350 degrees), not a material fix; the material split is the real fix for the wall.
