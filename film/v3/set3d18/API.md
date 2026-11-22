# v3/set3d18/jimo.py : film 18 set ("ไอ้เสมียนวัว", Tian Dan's fire oxen at Jimo, Qi vs Yan, 279 BC) (bpy 5.3, Cycles CPU)

The production set, grown from the style board (board/NOTES.md). Four locations, three light presets, 26 named shot cameras, state setters keyed per frame, fire that flickers per frame, flame cards for the 2D oxen.
**No depth of field anywhere (`make_camera` forces it off). No text anywhere** (banners and pennants are plain shapes). The 3D placeholder ox is NOT in production: the oxen are 2D puppet cards; `debug_ox()` builds it hidden-by-default for debugging only.

## Files
- `jimo.py`: core (presets, materials incl. the warm / cool wall material, live fires, flame cards, states, cameras, foreground props, placeholders, CLI).
- `jimo_wall.py`: the wall (both faces, 12 breaches, gate leaves, torches, ramps...), gate hall, city roofs, moat (water + dry ditch), bridge, road, fields, far Yan camp (jimo_out).
- `jimo_in.py` (inside Jimo), `jimo_camp.py` (yan_camp), `jimo_vista.py` (the Qi plain), `jimo_ox.py` (debug ox only), `jimo_shots.py` (shot table, motion, marks, herd, per-shot `sun` azimuth), `jimo_r2.py` (round 2: real 2D cast cards at the marks, ox card yaw, contact shadows / warm pools, per-shot skips / dressing / lamp dimming), `jimo_cards.py` (cast18 figures rasterised to PNG, cache `set_work/cards/`), `jimo_tex.py` (painted textures, cache `tex_jimo/`, bump `TEX_V` after editing a painter), `jimo_hue.py` (hue rows), `jimo_sheet.py` (contact sheets).
- `contact.jpg` / `contact_small.jpg`: one 720x1280 final (12 samples) per shot camera at the MIDDLE of the move (t = 0.5, the shot's mid state), with REAL cast18 cards at the stand marks (people poses from STORY18, the dragon / plain ox from `ox_figure`, rasterised by Playwright through `puppet._raster`; `ACTORS=0` leaves them out); label under each tile, cyan line at y 880.
- `set_work/`: `final/` (the 26 PNGs + `sNN.json` meta: head rows, wall polygons), `final_r1/` (round 1 finals, contact, hue rows, API backup), `final_log.txt`, `hue_rows.txt`, `framediff_r2.txt`, `cards/`, `stills/` (drafts), `r2draft.py` / `r2heads.py` / `r2proj.py` / `r2measure.py` (round 2 tools).
- Rebuild everything: `python3 jimo.py final` (26 finals, one build + one render each), then `python3 jimo.py meta`, `python3 jimo.py contact`, `python3 jimo_hue.py rows`.

## Build and CLI
```python
import jimo as J
A = J.build('jimo_in', 's01')            # location, preset, light=None;  preset = a shot 's01'..'s26' (location and light come from it) or the location name (default camera 'wide')
cam = J.shot_camera('s01', 0.5)          # pose the scene camera at t of the move (builds the shot's foreground prop, fixed in the WORLD at the shot start pose: v3)
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
- `set_holes(n)`: ragged breaches in the wall base, n = 0 .. 12 (float: 6.5 = six open, the seventh half dug); OPENING ORDER (round 2): hole 11 (x 41) first, then 10 ... 0, so s16 (camera x 50 -> 25) sees them open one after another. 12 centres `HOLE_X` = x -41 .. -13.5 and 13.5 .. 41 (spacing 5.5), 3.4 wide x 4.3 high, on both faces; plug sinks, rim + rubble + props grow, a heap of dug earth + pick + basket appears inside. Available in jimo_in, jimo_out (and invisible far away in yan_camp).
- `set_gate(k)`: gate leaves 0 shut .. 1 open 75 deg outward (0.15 = a crack, with a warm glow behind in jimo_out).
- `set_party(k)` (yan_camp): 16 extra cups (+ jar) pop in one by one; the crowd marks are `marks.party_crowd` of shot s13.
- `set_rout(k)` (yan_camp): tents fold (staggered z-scale to 0.12 + tilt), 30 pots / helmets / fodder bundles / bowls fly in arcs and scatter, chariot `chariot0` rolls away and turns. Comic, nothing gory, no bodies.
- `set_pennants(k, side='yan')` (vista): black Yan pennants pop up one by one over the 62 ordinary towns, k 0 .. 1. `side` = the ORDER: `'yan'` (scattered, fixed), `'ltr'`, `'rtl'`, `'near'`, `'far'`. The two holdouts (Jimo, Ju) never get one.
- `set_qi_return(k)` (vista): the pennants turn to Qi colours (red with teal trim) one by one; the holdouts keep their Qi pennant up from the start and stay warm-lit (windows, halo, gate fires, light pool).
- `animate(setter, f0, f1, v0, v1)` keys any setter over frames, eased: `J.animate(J.set_holes, 1205, 1309, 0, 12)`; for staggered pennants key the setter every frame (the default step 1 does).
- `apply_state('h6,g0.3,pt1,ro0.5,pn0.5,qr0.5,fl1')`: the string form used by the CLI and the shot table.
- Cameras: `shot_camera(name, t)`, `key_camera(name)`, `make_camera(setup)` (setup = {loc, look_at, lens}); every shot has `cams[name] = {loc, look_at, lens, start, mid, end, frames, f0, f1, fg}`.
- Foreground props (1-2 D from the lens, 30 % scale; v3: fixed in the WORLD at the shot start pose, so they parallax; J.unparent_from_camera(cam) re-parents any camera child to the world): lantern, wheel, spear_rack, jar, pick_baskets, reeds, counter, torch; built by `shot_camera`.

## Herd helper
`jimo_shots.herd(n, a, b, width=6.0, seed=1)`: N marks `(x, y, 0, yaw_deg, scale)` along a lane / field from point a to point b (x, y) with lateral spread `width` D; rows staggered and jittered, about 3.6 D apart along and 3 D across; yaw = direction of travel (degrees from +x, ox cards in side view), scale 0.93-1.07; sorted far to near (paint order). `J.S.herd` is the same function. The shots use it: s01 (8 dressed oxen along the wall), s02 (34 in the lane), s06 (10 in front of the gates), s07 (120 in the yard + 90 far = 210 visible), s19 (40 + 30 Qi soldiers), s20 (36), s21 (60).

## Marks
Stand marks are world points; heads must stay above y 880: `J.head_rows(shot)` prints (role, t, mark, head top y, chin y, feet y) at t = 0, 0.5, 1; the report numbers are in `set_work/final/sNN.json`.
Heights: tiandan 3.0, general 3.4, soldier 3.2, townsfolk 3.0, child 2.0, envoy 3.0, ox 2.6 (`J.HEIGHT`).

## Cameras and stand marks per shot (generated from jimo_shots.py)

Camera poses are `loc -> look_at` (D) and lens (mm). `start` is the pose at t = 0 of the shot, `end` at t = 1; `J.shot_camera(name, t)` poses the scene camera for any t and `J.key_camera(name)` keys the whole move. Marks are world points (x, y, z) with the card yaw (deg about z; a person card faces -y at yaw 0, the printed yaw turns it to face the START camera; ox / herd cards: yaw = direction of travel from +x, side view), ox marks may carry a scale. For long lists only the first 6 are printed here; `jimo_shots.marks_for("sNN")` returns them all.

### s01  (frames 0-78, jimo_in, NIGHT)
- lantern-lit ox yard, eye, push 8 %/s, slide right; Tian Dan dresses an ox, a row of dressed oxen along the wall behind
- camera start (-14.0, 26.0, 2.5) -> (4.0, 8.0, 4.2) lens 24; end (-12.455, 20.057, 2.854) -> (1.801, 5.801, 4.2); move: push +0.08 /s, slide +40 px/s; fg prop: ('lantern', 'right'); state at mid: `-`
  - tiandan (1): (-4.1, 16.8, 0) yaw 0
  - ox (7): (-1.2, 15.2, 0) yaw 165 s1; (-15, 7.4, 0) yaw 180 s1; (-9.5, 7.9, 0) yaw 180 s1; (-4, 7.4, 0) yaw 180 s1; (1.5, 7.9, 0) yaw 180 s1; (7, 7.4, 0) yaw 180 s1 ...

### s02  (frames 78-156, jimo_in, NIGHT)
- low 1.2 D along the ring lane, pull-out reveals dozens of dressed oxen filling the lane (herd helper)
- camera start (-28.0, 11.5, 1.2) -> (12.0, 10.5, 3.0) lens 20; end (-35.28, 11.682, 0.872) -> (12.0, 10.5, 3.0); move: push -0.07 /s, slide +0 px/s; fg prop: ('pick_baskets', 'left'); state at mid: `-`
  - tiandan (1): (-24.5, 10.2, 0) yaw 0
  - ox (1): (-21.8, 8.4, 0) yaw 180 s1
  - herd (34): (4.94, 12.42, 0) yaw 176.4 s1.04; (-7.78, 12.41, 0) yaw 182.3 s1.07; (-19.94, 12.4, 0) yaw 174.3 s1; (20.74, 12.39, 0) yaw 174.4 s1; (28.17, 12.35, 0) yaw 185.7 s0.99; (2.39, 12.34, 0) yaw 174.2 s1.04 ...

### s03  (frames 156-297, vista, DUSK)
- establishing high, push 6 %/s, slide left; the black Yan pennants pop over the towns one by one (set_pennants 0 -> 1 on 7.32-9.89 s)
- camera start (70.0, -215.0, 105.0) -> (0.0, 70.0, -10.0) lens 20; end (-30.665, -154.506, 72.57) -> (-80.925, 50.124, -10.0); move: push +0.06 /s, slide -40 px/s; fg prop: none; state at mid: `pn0.5`

### s04  (frames 297-384, vista, DUSK)
- high, push-in toward the near lit town Jimo (marks.jimo) on "จี๋โม่" (11.91 s); two towns stay lit (Jimo near, Ju far)
- camera start (52.0, -150.0, 80.0) -> (28.0, -30.0, 6.0) lens 22; end (47.128, -125.64, 64.978) -> (28.0, -30.0, 6.0); move: push +0.07 /s, slide +0 px/s; fg prop: none; state at mid: `pn1`

### s05  (frames 384-459, jimo_in, DUSK)
- market lane, the clerk stall at (-77, 22) faces +x; Tian Dan behind the counter, townsfolk hand him a sash
- camera start (-69.5, 18.5, 2.6) -> (-76.5, 22.5, 2.8) lens 24; end (-70.9, 19.3, 2.64) -> (-76.5, 22.5, 2.8); move: push +0.08 /s, slide +0 px/s; fg prop: ('counter', 'right'); state at mid: `-`
  - tiandan (1): (-76, 22, 0) yaw 90
  - townsfolk (3): (-75.2, 20.6, 0) yaw 130; (-75.2, 23.8, 0) yaw 230; (-76, 25.6, 0) yaw 200
  - child (1): (-76.8, 24.6, 0) yaw 190

### s06  (frames 459-531, jimo_in, DUSK)
- eye, slides left 40 px/s along the ring lane in front of the house gates (x 58 / 74 / 89, y 23); townsfolk lead oxen out of the gates; ten oxen at "สิบตัว"
- camera start (84.0, 9.0, 2.4) -> (72.0, 22.0, 2.6) lens 22; end (82.404, 7.527, 2.4) -> (70.404, 20.527, 2.6); move: push +0 /s, slide -40 px/s; fg prop: none; state at mid: `-`
  - tiandan (1): (76, 12.5, 0) yaw 180
  - townsfolk (4): (58, 19.5, 0) yaw 180; (74, 19.5, 0) yaw 180; (86, 19.5, 0) yaw 180; (66, 11, 0) yaw 180
  - herd (10): (92.81, 16.3, 0) yaw 194.9 s1; (89.91, 15.97, 0) yaw 186.4 s1.02; (81.47, 15.86, 0) yaw 193.7 s0.99; (78.72, 15.7, 0) yaw 194.1 s0.98; (85.15, 15.55, 0) yaw 191.6 s0.97; (74.27, 15.47, 0) yaw 193.7 s0.97 ...

### s07  (frames 531-597, jimo_in, DUSK)
- high 4-5 D from the north end of the yard, pull-out with a snap x1.6 on "พันกว่าตัว": the whole quarter packed with oxen (herd helper ~200 + silhouettes)
- camera start (0.0, 46.0, 20.0) -> (0.0, 14.0, 0.0) lens 20; end (0.0, 70.832, 35.52) -> (0.0, 14.0, 0.0); move: push -0.05 /s, slide +0 px/s, extra [{'t': 0.55, 'd': 1.6, 'dur': 7}]; fg prop: none; state at mid: `-`
  - herd (120): (33.99, 30.75, 0) yaw -20 s1; (31.45, 30.39, 0) yaw -17.8 s1.03; (29.53, 29.5, 0) yaw -17.3 s1.02; (26.36, 29, 0) yaw -24.9 s0.99; (24.12, 28.72, 0) yaw -22.8 s1.06; (21.99, 28.26, 0) yaw -25.3 s0.95 ...
  - herd_pen (40): (7.47, 38.33, 0) yaw -57 s0.96; (-8.12, 38.29, 0) yaw -65.8 s0.98; (2.93, 38.29, 0) yaw -56.3 s0.94; (-5.26, 38.2, 0) yaw -63.7 s1.01; (-6.78, 38.19, 0) yaw -55.6 s0.96; (-14.46, 38.14, 0) yaw -58.1 s0.95 ...
  - herd_far (100): (-0.71, 8.73, 0) yaw -0.7 s0.94; (7.33, 8.73, 0) yaw 3.1 s1; (-34.11, 8.72, 0) yaw -4.5 s1.03; (14.46, 8.72, 0) yaw 3.4 s0.97; (13.2, 8.71, 0) yaw 4.2 s1; (31.86, 8.7, 0) yaw -4.9 s1.01 ...

### s08  (frames 597-674, yan_camp, DUSK)
- eye, push 8 %/s, the general on the rampart (marks.rampart, z 2.6) looks at Jimo, bursts out laughing; fg spear rack
- camera start (1.5, -59.0, 2.4) -> (-4.0, -47.5, 4.8) lens 22; end (0.371, -56.639, 2.893) -> (-4.0, -47.5, 4.8); move: push +0.08 /s, slide +0 px/s; fg prop: ('spear_rack', 'left'); state at mid: `-`
  - general (1): (-4, -47.5, 2.6) yaw 25.6
  - soldier (2): (3.6, -48.5, 2.6) yaw -11.3; (-9, -48.5, 2.6) yaw 45

### s09  (frames 674-737, yan_camp, DUSK)
- QUOTE 1a medium (camera on the far side of the general, looking +y toward the camp and Jimo; the table is the fg), push 9 %/s; the general arms wide, soldiers behind him laugh
- camera start (-7.0, -99.0, 2.8) -> (-3.5, -90.5, 4.2) lens 24; end (-6.338, -97.394, 3.065) -> (-3.5, -90.5, 4.2); move: push +0.09 /s, slide +0 px/s; fg prop: none; state at mid: `-`
  - general (1): (-3.5, -90.5, 0) yaw -22.4
  - soldier (3): (-8.2, -85, 0) yaw 0; (0.8, -84.2, 0) yaw 0; (-3.8, -81.5, 0) yaw 0

### s10  (frames 737-853, yan_camp, DUSK)
- QUOTE 1b medium-close (reverse angle, the camp behind him), push 10 %/s then a slight slide; thumb at his chest, chin up
- camera start (-1.5, -96.5, 3.1) -> (-3.5, -90.5, 3.0) lens 26; end (-2.901, -94.389, 3.061) -> (-4.127, -90.709, 3.0); move: push +0.1 /s, slide -25 px/s; fg prop: none; state at mid: `-`
  - general (1): (-3.5, -90.5, 0) yaw 18.4
  - soldier (2): (-8, -85, 0) yaw 0; (0.8, -84, 0) yaw 0

### s11  (frames 853-944, yan_camp, DUSK)
- wide eye, pull-out 7 %/s with a push-in on "ไอ้เสมียนวัว" (30.64 s); soldiers round the fire at (5.5, -85) mock-moo, finger horns
- camera start (-1.0, -73.0, 2.6) -> (5.5, -86.0, 2.2) lens 22; end (-0.647, -73.707, 2.578) -> (5.5, -86.0, 2.2); move: push -0.07 /s, slide +0 px/s, extra [{'t': 0.55, 'd': 0.78, 'dur': 8}]; fg prop: ('jar', 'left'); state at mid: `-`
  - soldier (6): (2.5, -81.5, 0) yaw 0; (8.5, -82, 0) yaw 0; (9.8, -86.5, 0) yaw 0; (2, -87.5, 0) yaw 0; (5.5, -89.5, 0) yaw 0; (-1, -84, 0) yaw 0
  - general (1): (-2.5, -92, 0) yaw 0

### s12  (frames 944-1003, jimo_out, DUSK)
- eye low, slides right; the gate opens a crack (set_gate 0.15); the envoy bows on the bridge; old folk and women stand on the wall walk (z 16, no soldiers)
- camera start (-14.0, -42.0, 1.7) -> (2.0, -12.0, 4.6) lens 24; end (-11.224, -43.48, 1.7) -> (4.776, -13.48, 4.6); move: push +0 /s, slide +40 px/s; fg prop: ('wheel', 'left'); state at mid: `g0.15`
  - envoy (1): (0.2, -29, 0) yaw 180
  - townsfolk (6): (-13.1, -2.2, 16) yaw 180; (-9.7, -2.2, 16) yaw 180; (-6.3, -2.2, 16) yaw 180; (7.3, -2.2, 16) yaw 180; (10.7, -2.2, 16) yaw 180; (14.1, -2.2, 16) yaw 180
  - child (1): (-16.5, -2.2, 16) yaw 180

### s13  (frames 1003-1071, yan_camp, NIGHT)
- wide high, pull-out 6 %/s; the camp party (set_party 1): cheering-crowd marks round the fires, cups, a sentry drops his spear and joins in
- camera start (0.0, -54.0, 12.0) -> (2.0, -86.0, 2.0) lens 20; end (-0.272, -49.648, 13.36) -> (2.0, -86.0, 2.0); move: push -0.06 /s, slide +0 px/s; fg prop: none; state at mid: `pt1`
  - party_crowd (14): (-6, -92, 0) yaw 200; (-2, -93, 0) yaw 210; (1.5, -90, 0) yaw 190; (8.5, -80, 0) yaw 180; (3, -80, 0) yaw 190; (-4, -76, 0) yaw 200 ...
  - sentry (1): (-14, -76, 0) yaw 180

### s14  (frames 1071-1136, yan_camp, NIGHT)
- QUOTE 2a medium (reverse angle: the party fires, tents and crowd behind him), push 9 %/s; the general raises his cup and laughs, bounce; fg wine jar
- camera start (-9.0, -106.0, 2.8) -> (-4.3, -96.2, 4.4) lens 24; end (-8.084, -104.089, 3.112) -> (-4.3, -96.2, 4.4); move: push +0.09 /s, slide +0 px/s; fg prop: ('jar', 'right'); state at mid: `pt1`
  - general (1): (-4.3, -96.2, 0) yaw -25.6
  - soldier (2): (-9.2, -90.8, 0) yaw 0; (1.2, -90, 0) yaw 0
  - party_crowd (6): (6.5, -85, 0) yaw 0; (9.5, -80.5, 0) yaw 0; (2, -78, 0) yaw 0; (-3, -74.5, 0) yaw 0; (-9, -72, 0) yaw 0; (8, -74, 0) yaw 0

### s15  (frames 1136-1205, yan_camp, NIGHT)
- QUOTE 2b medium-close (reverse angle), push 10 %/s; he mimes carving, licks his lips, the cup tilts
- camera start (-1.5, -103.0, 3.1) -> (-4.3, -96.2, 3.0) lens 26; end (-2.144, -101.436, 3.077) -> (-4.3, -96.2, 3.0); move: push +0.1 /s, slide +0 px/s; fg prop: none; state at mid: `pt1`
  - general (1): (-4.3, -96.2, 0) yaw 22.4
  - soldier (1): (-9, -91, 0) yaw 0
  - party_crowd (3): (6, -86, 0) yaw 0; (9.5, -81, 0) yaw 0; (2, -79, 0) yaw 0

### s16  (frames 1205-1309, jimo_in, NIGHT)
- low inside the wall base, slides left along the wall (x 50 -> 25): the holes open one after another (set_holes 0 -> 12, hole order from x 41 down); townsfolk dig between the holes
- camera start (50.0, 16.0, 2.6) -> (30.0, 4.0, 2.2) lens 22; end (52.128, 12.454, 2.6) -> (32.128, 0.454, 2.2); move: push +0 /s, slide -40 px/s; fg prop: ('pick_baskets', 'left'); state at mid: `h6`
  - townsfolk (6): (43.75, 7.4, 0) yaw 180; (38.25, 7.4, 0) yaw 180; (32.75, 7.4, 0) yaw 180; (27.25, 7.4, 0) yaw 180; (21.75, 7.4, 0) yaw 180; (16.25, 7.4, 0) yaw 180
  - child (1): (27.25, 9.2, 0) yaw 180

### s17  (frames 1309-1388, jimo_in, NIGHT)
- eye medium, push 8 %/s; reed bundles soaked from a jar are tied to the tails; oxen lined up nose-first at the holes (marks face the wall)
- camera start (-9.0, 16.5, 2.6) -> (-27.0, 5.5, 2.4) lens 22; end (-12.792, 14.183, 2.558) -> (-27.0, 5.5, 2.4); move: push +0.08 /s, slide +0 px/s; fg prop: ('reeds', 'left'); state at mid: `h12`
  - ox (6): (-41, 8.4, 0) yaw -90 s1; (-35.5, 8.4, 0) yaw -90 s1; (-30, 8.4, 0) yaw -90 s1; (-24.5, 8.4, 0) yaw -90 s1; (-19, 8.4, 0) yaw -90 s1; (-13.5, 8.4, 0) yaw -90 s1
  - townsfolk (3): (-33.7, 11.5, 0) yaw 200; (-22.7, 11.5, 0) yaw 200; (-17.2, 11.5, 0) yaw 200
  - tiandan (1): (-32.2, 12, 0) yaw 160

### s18  (frames 1388-1427, jimo_in, NIGHT)
- eye, quick push-in: Tian Dan raises a torch, tails light in a ripple (flame_card on each ox card)
- camera start (-1.0, 15.5, 2.4) -> (-22.0, 5.5, 4.0) lens 22; end (-7.384, 12.46, 2.886) -> (-22.0, 5.5, 4.0); move: push +0.1 /s, slide +0 px/s, extra [{'t': 0.5, 'd': 0.8, 'dur': 6}]; fg prop: none; state at mid: `h12`
  - tiandan (1): (-6.8, 12.6, 0) yaw 120
  - ox (6): (-41, 8.4, 0) yaw -90 s1; (-35.5, 8.4, 0) yaw -90 s1; (-30, 8.4, 0) yaw -90 s1; (-24.5, 8.4, 0) yaw -90 s1; (-19, 8.4, 0) yaw -90 s1; (-13.5, 8.4, 0) yaw -90 s1

### s19  (frames 1427-1515, jimo_out, NIGHT)
- low wide at the wall base, WHIP pan at the end to follow the herd; oxen burst out of the 12 holes (x 13.5..41 at y -5), cross the dry ditch / bridge and the field toward the camp
- camera start (6.0, -32.0, 1.5) -> (30.0, -5.0, 3.4) lens 18; end (6.0, -32.0, 1.5) -> (34.989, -53.555, 3.4); move: push +0 /s, slide +0 px/s, extra [{'t': 0.9, 'pan': -85, 'dur': 6}]; fg prop: none; state at mid: `h12,g0.3`
  - ox (6): (13.5, -7.2, 0) yaw -100 s1; (19, -7.2, 0) yaw -100 s1; (24.5, -7.2, 0) yaw -100 s1; (30, -7.2, 0) yaw -100 s1; (35.5, -7.2, 0) yaw -100 s1; (41, -7.2, 0) yaw -100 s1
  - herd (40): (32.93, -8.4, 0) yaw -101.6 s1.01; (26.75, -9.45, 0) yaw -100.1 s0.97; (30.16, -10.33, 0) yaw -100.3 s1.01; (20.93, -11.32, 0) yaw -97.8 s1; (24.39, -11.87, 0) yaw -100.5 s0.95; (34.62, -16.46, 0) yaw -99.3 s0.95 ...
  - qi_soldier (30): (31.55, 6.88, 0) yaw -95.6 s0.94; (37.23, 6.71, 0) yaw -95.7 s1.03; (25.37, 6.61, 0) yaw -85.1 s0.98; (19.27, 5.85, 0) yaw -91.1 s1.07; (22.37, 5.33, 0) yaw -84.6 s0.99; (13.63, 5.15, 0) yaw -86.8 s1.06 ...

### s20  (frames 1515-1596, jimo_out, NIGHT)
- low, tracking beside the herd, push 7 %/s; the herd charges toward the Yan camp (far camp at y -150..-215); oxen never turn back
- camera start (22.0, -56.0, 1.7) -> (-2.0, -92.0, 3.0) lens 20; end (17.464, -62.804, 1.946) -> (-2.0, -92.0, 3.0); move: push +0.07 /s, slide +0 px/s; fg prop: none; state at mid: `h12`
  - herd (36): (10.5, -59.46, 0) yaw -106.4 s1; (13.22, -62.3, 0) yaw -104.3 s1; (16.45, -62.58, 0) yaw -114 s0.98; (7.77, -65.18, 0) yaw -102 s1.03; (18.98, -65.41, 0) yaw -104.5 s0.96; (14.13, -68.28, 0) yaw -102.6 s0.98 ...

### s21  (frames 1596-1683, yan_camp, NIGHT)
- eye from the Yan side at the palisade gap (x +-6): a wall of glowing red dragon monsters comes out of the dark field (y -38 .. -6); SNAP push x1.5; soldiers' jaws drop, cups fall
- camera start (0.0, -58.0, 2.2) -> (0.0, -8.0, 4.0) lens 22; end (0.0, -38.585, 2.899) -> (0.0, -8.0, 4.0); move: push +0.03 /s, slide +0 px/s, extra [{'t': 0.45, 'd': 0.67, 'dur': 6}]; fg prop: none; state at mid: `-`
  - soldier (3): (-3, -51.5, 0) yaw 0; (3.5, -49.5, 0) yaw 0; (0.2, -47, 0) yaw 0
  - herd (60): (-3.2, -7.82, 0) yaw -88.4 s1; (3.15, -8, 0) yaw -96 s0.98; (0.2, -8.23, 0) yaw -86.3 s1; (-3.63, -9.57, 0) yaw -86.5 s0.96; (3.41, -9.73, 0) yaw -95.6 s0.98; (-0.32, -9.77, 0) yaw -84 s1.03 ...

### s22  (frames 1683-1742, yan_camp, NIGHT)
- close-medium on ONE ox in full flare (blades, silk, flame tail) with a frozen terrified soldier
- camera start (-2.0, -52.0, 1.6) -> (0.5, -45.0, 2.0) lens 26; end (-1.558, -50.761, 1.671) -> (0.5, -45.0, 2.0); move: push +0.09 /s, slide +0 px/s; fg prop: none; state at mid: `-`
  - ox (1): (0.4, -46.5, 0) yaw -60 s1
  - soldier (1): (-1.4, -47, 0) yaw 0

### s23  (frames 1742-1807, jimo_out, NIGHT)
- high over the wall top, pull-out; fg torch; old men, women and kids beat bronze pots on the walk (walk centre y 0.4, z 16)
- camera start (-31.0, 0.6, 21.5) -> (-2.0, 0.6, 16.5) lens 22; end (-35.398, 0.6, 22.258) -> (-2.0, 0.6, 16.5); move: push -0.07 /s, slide +0 px/s; fg prop: ('torch', 'right'); state at mid: `h12`
  - townsfolk (6): (-21.5, 1.7, 16) yaw 180; (-17, -0.9, 16) yaw 180; (-12.5, 1.7, 16) yaw 180; (-8, -0.9, 16) yaw 180; (-3.5, 1.7, 16) yaw 180; (1, -0.9, 16) yaw 180
  - child (2): (-19.2, 0.3, 16) yaw 180; (-10.2, 0.3, 16) yaw 180

### s24  (frames 1807-1882, yan_camp, NIGHT)
- wide high, slide 50 px/s + push; rout (set_rout 0 -> 1): tents fold, soldiers flee, pots and helmets fly, a chariot rolls away empty; nobody hurt
- camera start (-34.0, -44.0, 15.0) -> (-4.0, -82.0, 2.0) lens 20; end (-37.166, -54.21, 13.375) -> (-10.916, -87.46, 2.0); move: push +0.05 /s, slide +50 px/s; fg prop: none; state at mid: `ro0.5`
  - soldier (8): (-10.21, -59.62, 0) yaw 200; (-17.93, -70.81, 0) yaw 200; (-9.01, -67.59, 0) yaw 200; (-18.3, -80.02, 0) yaw 200; (1.44, -69.53, 0) yaw 200; (-7.07, -81.34, 0) yaw 200 ...

### s25  (frames 1882-1958, vista, DAWN)
- establishing high, push 6 %/s; the Qi banners return over the towns one by one (set_qi_return 0 -> 1), warm dawn
- camera start (-50.0, -215.0, 105.0) -> (0.0, 80.0, -10.0) lens 20; end (-42.4, -170.16, 87.52) -> (0.0, 80.0, -10.0); move: push +0.06 /s, slide +0 px/s; fg prop: none; state at mid: `pn1,qr0.5`

### s26  (frames 1958-2112, jimo_out, DAWN)
- low, long tracking pull in front of the running general (he runs -y toward home along the road toward the camera), push-in at the end; dragon oxen trot after him with smoking tails
- camera start (2.5, -84.0, 1.5) -> (0.5, -70.0, 2.6) lens 24; end (2.645, -85.016, 1.42) -> (0.5, -70.0, 2.6); move: push -0.06 /s, slide +0 px/s, extra [{'t': 0.72, 'd': 0.82, 'dur': 10}]; fg prop: none; state at mid: `-`
  - general (1): (0.8, -77, 0) yaw 0
  - ox (4): (-1.8, -71, 0) yaw -90 s1; (3.2, -69, 0) yaw -90 s1; (-0.6, -66.5, 0) yaw -90 s1; (4, -63.5, 0) yaw -90 s1
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
- Foreground props are 30 % scale (a 3 D lantern would not fit at 1-2 D from the lens), world-fixed (v3); s17 reed bundles and s05 counter are chunky.
- Placeholder cards in the contact sheet are the real cast18 drawings (card-yawed 30-45 deg off the camera axis), but still flat 2D cards: back views do not exist (silhouette tint is used in s21 / s22), the ox 3/4 is the cast's side-body with a turned head.
- The wall material's `warm` weights are static (baked from the fixed lamps); the dynamic flame-card lights light the wall with the plain material (orange over blue, fine near the light, mauve at medium distance, which the hue guard pushes toward coral).
- Camp geometry (palisade y -40, wall 40 D away) is closer than the open field of jimo_out (road to y -300, far camp at y -150..-215); the two locations do not share one world.
- `hue_guard` is a compositor trick (hue correct on 255-350 degrees), not a material fix; the material split is the real fix for the wall.

## Round 2 fixes (set builder, after the SET gate FAIL: QA_ART_SET.md 1-14 + non-blocking, QA_TECH.md 1-19)

Cards: `jimo_cards.py` + `jimo_r2.py`. People = cast18 STORY18 poses, scaled so the head top meets `HEIGHT`, billboarded to the camera at t; oxen = `ox_figure(state, 'three_quarter', gait, phase, flame, blades=True)`, 8 gallop phases, flame variants 1 / 2 on lit tails, mirrored so the head points to the direction of travel, plane yawed 30-45 deg (+-6 jitter) off the camera axis (never edge-on); soft contact shadow under every card; warm pool decals under lit oxen + real tail lights on the 6 nearest. No flat placeholders remain.
Per-shot sun azimuth (`shot(..., sun=)`), build-time skips (`jimo_r2.SKIP`, `BSKIP`) and `POST` tweaks are the mechanism for most items below.

| fix | what was done | number (final, mid t unless said) |
|---|---|---|
| ART 1 / s02 herd | `herd(34, (-21,10.6),(30,10.6), 6)` travelling toward the camera (yaw 180), ground dressing (silk scraps, rope coils, hay) in x -38..-14 | nearest ox ~9 D from the lens at t 0.5; heads chin 632; herd reads in the lane; caption mean 119, 21.8k px V>0.7 (the pink lit lane: still brighter than the 60-110 target) |
| ART 2 / s05 | camera (-69.5,18.5,2.6)->(-76.5,22.5,2.8) lens 24, townsfolk beside the counter; DUSK sky repainted without the sun disc (no halo ring, painter `dusk_sky`, with cartoon clouds); sun 325 deg (behind the camera); fg counter 22 % scale | Tian Dan 402 px, townsfolk 300-590 px, chin 808 / 824 / 843 |
| ART 3 / s06 | 10 plain oxen at y 15-16 in front of the gates, townsfolk (86,19.5), camera look z 2.6, sun 320 | ox heads readable, chin max 698; caption mean 50 |
| ART 4 / s07 | camera (0,46,20)->(0,14,0), pull -0.05 + snap x1.6; herd 170 in the yard (x -28..28) + 40 in the pens + 60 ring lane + 40 east quarter, 1/3 dragon coats, sun 80 deg (shaft gone) | 170 + 40 + 60 + 40 marks, 188 ox cards inside the frame at t 0.5 (176 at t 0, 270 at t 1; >= 150 target met); caption bright (>200) 2.4 % |
| ART 5 / s09 s10 s14 s15 | reversed: cameras on the far side of the general looking +y (s09 (-7,-99,2.8), s10 (-1.5,-96.5,3.1)->look z 3.0, s14 (-9,-106,2.8), s15 (-1.5,-103,3.1)->look z 3.0), camp behind him, party crowd marks behind in s14 / s15, soldiers moved north; tent (-9.6,-90) and oil lamps moved >= 3 D from the general; table moved out of the s14 / s15 view; scatter pots hidden; sun behind (322 deg vs view 90) | general chin: s09 812-849, s10 728-783, s14 804-837, s15 715-738 (all < 880 at t 0 / 0.5 / 1); s10 head top 545-581 (<= 600); caption bright: s09 1.8 %, s10 0 %, s14 0 %, s15 0 % |
| ART 6 / s11 | camera (-1,-73,2.6)->(5.5,-86,2.2) lens 22; drums moved to (-21,-80) / (16,-83.5); sun 100 deg | 7 cards visible, heads 560-654, 150-210 px tall |
| ART 7 / s16 | camera (50,16,2.6)->(30,4,2.2); hole opening order from x 41; diggers placed between the holes; 3 braziers in the lane removed (SKIP); breaches rebuilt as dark openings (dark backing, warm glow, ground pools, ragged clods instead of the pale stacked blocks) | 7 diggers, heads 595-681; holes read dark with warm glow |
| ART 8 / s17 | fg reeds 15 % scale (was 30 %), no fg jar; camera (-9,16.5,2.6)->(-27,5.5,2.4) so the six oxen at the holes are 2x larger | ox heads 566-839 (chin < 880 at t 1) |
| ART 9 / s19 | breach interiors dark + warm glow + dust puffs (`hglow%d`, `dust`), tunnel side faces dark; ox cards 3/4 gallop with flame tails; moat water calmer (painter `water`), `grass` painter calm, streak decals hidden; herd re-marked (27,-10)->(34,-58), furrows + stubble + stakes | ox heads 641-672; caption bright 0 % |
| ART 10 / s20 | herd (15,-62)->(-3,-108) so 4-5 oxen are large in frame (3-10 D); furrows, stones, hay, baskets, 3 torch stakes; warm pools under oxen | blue+violet 77.8 % (<= 85 % met), caption bright 0 % |
| ART 11 / s21 | camera (0,-58,2.2) -> (0,-8,4.0), push 0.03 + snap x0.67; 3 soldier silhouettes at y -47..-51.5 between lens and palisade; herd 60 through the gap in 3/4 gallop cards; rampart and horse removed for s21 / s22; Jimo wall lamps x 0.3 (lights, flames, halo faces, wall pools, baked warm weights) | blue 48.8 %, lamps 0.3, herd comes out of the dark at the gap |
| ART 12 / s22 | ox (0.4,-46.5) in the gap, soldier silhouette left (-1.4,-47.0), camera (-2,-52,1.6)->(0.5,-45,2.0) lens 26 (the rampart used to enclose this camera), no bridge rail | ox card 391 / 438 / 498 px tall = 31 / 34 / 39 % of the frame (ox body incl. horns 38-48 %), soldier 600-830 px |
| ART 13 / s23 | camera (-31,0.6,21.5)->(-2,0.6,16.5); all fire bowls and lamps within 9.5 D of the lens skipped; fg torch 13 % scale; townsfolk marks x -21.5..1 on the walk | townsfolk visible beating pots, chin 753-793; caption bright 0 %, 62 px V>0.7 (< 2 k) |
| ART 14 / s26 | camera (2.5,-84,1.5)->(0.5,-70,2.6) lens 24, general (0.8,-77), 4 oxen y -71..-63.5; DAWN sun 262 deg (behind the camera: warm wall, no washed sky); road dressing (ruts, plume, pots, hay, silk, wheel, 3 torch stakes) | general 351-403 px (head top 483-520, chin 696-702); wall ochre 40 % blue 11 % |
| ART 15 | cast (done elsewhere) | - |
| ART non-blocking | s01 oxen spread along the wall, fg lantern 20 %; s08 soldier (3.6,-48.5), pennant cloth banners hidden; s12 envoy (0.2,-29) in front of the rail, wall folk in crenel gaps; s13 pennants near the lens skipped; s18 Tian Dan (-6.8,12.6), camera (-1,15.5)->(-22,5.5); s24 flying items x2.6, pennants skipped, soldiers moved into view; vista fields = aligned grid of 4 close greens (painter `patchwork`); Jimo bloom blob removed (halo 0.75 s / 0.38 s, pool off), pennants x1.5 and higher; cartoon clouds on DUSK; wall breach rim blocks replaced | see per-shot status |
| TECH 1 2 | s10 / s15 heads (see ART 5) | max chin 783 / 738 |
| TECH 3 | s24 soldier marks re-placed (`ahead()` along the view) | max chin 770 / 785 / 805 |
| TECH 4 | s01 look_at z 4.2 | max chin 759 / 792 / 849 |
| TECH 5 caption band | s09 sky (1.8 %), s10, s14, s15, s23, s19 at 0 %; vista s03 4.2 %, s04 5.7 %, s25 1.9 % and s07 2.4 %, s13 0.4 % are NOT met | see "could not meet" |
| TECH 6 | s23 fg torch 13 %, bowls skipped, townsfolk in view | blown pixels in the band 0 |
| TECH 7 8 | holes dark + glow + rubble + dust (s16 s17 s18 s19); reeds smaller | - |
| TECH 9 | s07 high camera, fence out of the foreground, cards re-yawed, herd tinted by the dusk light | 188 cards visible |
| TECH 10 11 | s22 / s21 re-aimed (see ART 11 12) | - |
| TECH 12 | s20 herd 3-10 D from the lens, horizon lowered by the look_at z 3.0 | - |
| TECH 13 | s13 party_crowd cards (14), cut objects removed (pennants within 30 D of (14,-62)); `HEIGHT` now has `party_crowd`, `sentry`, `qi_soldier` so head rows test them | s13 chin 727-744 |
| TECH 14 | s24 rout state 0.5: items x2.6, soldiers on screen, fg poles removed | - |
| TECH 15 16 | s08 / s11 actors in frame; s26 general 351-403 px; s05 aimed at the stall | - |
| TECH 17 | vista pennants x1.5 and raised, Jimo halo reduced | count unchanged (62 towns + 2); still low in s25 |
| TECH 18 | warm practicals: pools under oxen, fire halos kept; s14 / s15 still 92 % / 86 % blue (night plain), table / jar lamps kept | see could-not-meet |
| TECH 19 | scale: herd cards use scale 0.93-1.07 x 1.08 (2.6 D withers) | s19 ox vs wall rubble now 2.6 D |

Measured, finals (720x1280, 12 samples, 2 threads, one render at a time): 15.8 s wall per frame on average (log `final_log.txt`). Head rows: every person head chin < 880 at t 0 / 0.5 / 1 in all shots with marks (s05 max 843, s09 849, s17 839, s01 849, s18 835). Frame diff start vs end (mean abs luma diff, 0-255; fraction of pixels > 20): `set_work/framediff_r2.txt`: min s11 7.9 / 8.6 %, s09 11.6 / 15.8 %, s14 14.3 / 25.1 %, s06 14.9 / 17.4 %, all others 16-50 mean and 21-77 %: every move is clearly visible (state held at the mid value). Caption band (y 880-950), bright (luma > 200) share: 0 on 20 shots; s03 4.16 %, s04 5.71 %, s25 1.87 %, s07 2.42 %, s09 1.76 %, s13 0.36 %. jimo_hue rows regenerated: `hue_rows.txt` (shade hue 221-261, magenta share <= 4.4 %).

### Could not meet / still weak
- Vista s03 / s04 / s25: caption band still has 2-6 % bright pixels (tent torch glints, town glow); the vista flag is still a plain quad and Ju is not visibly lit in s04; pennant count is the same 62 + 2 (bigger, not more). Towns are still salmon brick.
- s02: caption band mean 119 (pink lit lane, 21.8 k px V > 0.7) is over the 60-110 target; s07 (2.4 %) and s09 (1.8 %): sky / lit wall glints in the band.
- s14 / s15: 92 % / 86 % blue (night plain, moon); only the camp fires and crowd add warm. The party behind the general is small.
- s24: rout reads (folding tents, flying pots, fleeing soldiers) but soldiers and pots are small at 25-45 D; the tent canvas is bright under the moon.
- s12: the wall-walk folk are mostly hidden by the parapet from the low camera; the envoy is small. s05: Tian Dan is a 400 px card between the counter and the old man; the fg counter is still chunky.
- s08: the far wall top still carries a flat red slab (gate-tower lintel colour) behind the general.
- Ox cards: the cast has no head-on front-3/4 view yet (ART 15, cast fixer): in s21 / s22 the oxen are drawn side-body with the head turned; horn blades are the current cast (long). Re-run `jimo_cards.py` (delete `set_work/cards/*_ox.*`) when cast18 changes, then `python3 jimo.py final`.
- Period: rammed-earth tiling, the pagoda finial of the towers and the panelled tents were not touched.

## Ground dressing (render teams: call this)
QA keeps failing shots because 35-55 % of the frame is bare tiled field, dirt lane or road. Do NOT dress shots one by one: call this once per shot, after the camera is posed / keyed AND the actor cards are placed (and keyed).

```python
A = J.build('jimo_out', 's20'); J.apply_state(...); J.key_camera('s20')        # or J.shot_camera('s20', t)
info = J.dress_ground(frames=range(f0, f1 + 1), actors=cards)                     # keyed move: the union of the frustums; cards = your actor card objects
share = J.ground_share('frame.png')                                              # 0..1, plain-ground share of a render
```
**`J.dress_ground(cam=None, density=1.0, seed=0, keep_clear=None, frames=None, actors=None)`** (`jimo_dress.py`) scatters a FEW larger, recognisable, warm props ONLY where the camera sees the ground (near plane to 42 D; vista: 520 D, props scaled by distance) and keeps them clear of the actors. Returns `dict(n, kinds, stat, poses, actors, ...)` (`stat` counts the rejections: occ / keep / actor / lens / dup / pruned_r2). Calling it again replaces the previous dressing (`J.clear_dressing()` removes it).
- `cam`: camera object or its name, default the scene camera (pose it first: `shot_camera` / `key_camera` / `make_camera`).
- `frames`: film frames of a keyed camera; up to 40 samples spread evenly over them. The ground is the UNION of the frustums, and EVERY sample is also used for the actor / lens checks (a whip pan is covered by passing the whole frame range). None = the current pose only.
- `density`: 1.0 is now about 40 % of the old (v1) helper's grid (one candidate per ~20 px square of visible ground on a 360 x 640 frame; vista unchanged), then thinned by keep-clear, actor boxes, existing objects and spacing, so a crowded shot ends with 2-10 props (s02 5, s05 2, s19 16, s26 6; the old helper gave 118 / 251 / 179 / 186). 0 = nothing; hard cap 400 objects (vista 1100).
- `keep_clear`: `[(x, y, radius)]` world circles that stay empty. `None` = `default_keep_clear()`: the shot's stand marks, herd positions and road path from `jimo_shots` (z <= 3), each **2.5 D** (`jimo_dress.ACTOR_CLEAR`). A given list REPLACES the default.
- `actors`: the actor CARDS of the render team: objects or names (a root with children counts, hidden-for-render objects are skipped). At every sampled frame the helper projects the cards' bounding boxes (feet included) to screen rectangles, adds a margin of 3.5 % x 3 % of the frame, and no prop's screen rectangle may overlap any of them (props in front of, behind or beside the actor alike). Also projected: a box for every stand mark of the shot (people 0.55 x HEIGHT half width, oxen 3.2 D half width x 3.7 D tall). `None` = auto: `ph_*` placeholders, objects named `card*` / `puppet*` / `actor*` / `cast*`, objects with the custom property `actor` (ob['actor'] = 1). **Pass `actors=[card objects]` whenever your cards are not at the shot's marks** (a woman moved to the lower-left foreground, say): the marks alone cannot know.
- Lens: nothing is placed whose surface is within **3 D** of the lens at any sampled pose, nor one that straddles the lens plane; props within 14 D of the camera are smaller (0.3-1.0 x), none is tall (> 1 D) or wide (> 1.2 D) there, stones are cut to a quarter.
- `seed`: deterministic (same scene + camera + seed = same result).
- Look: warm ochre / brown / straw earth tones (display value 0.35-0.6) with painted textures (`tex_jimo/dg2_stone|straw|grass|clay.png`, canvas for sacks, planks for carts), smooth rounded shapes, smooth shading. The shade side is a warm brown with only a touch of violet (`SHADE_TGT`), never the set's navy; props inside a fire's warm radius use an ochre shade; props that project into the caption band (y > 0.66 H) are dimmed. Every object keeps the 3 px ink hull and `no_bounce`.
- Library (what is placed): cart (some loaded), sacks and sack piles, baskets (heaped), water jars, straw heaps, soft straw / dry-grass clumps (rounded lumps, no blades), tied sheaves, rounded boulders. yan_camp: firewood, rolled mats, rope coils, helmets, a few spent arrows, jars, sacks. vista: hedgerows, tree clumps, haystacks, field ridges, huts. REMOVED in this version: ruts, puddles, broken-pot shards, spiky blade tufts, reeds, any flat decal.
- Not dressed: water / moat / berm / bridge (only the dry ditch floor at z -1.2), the wall footprint, the vista river, towns and Jimo's ring, and any cell where an existing set object stands (0.5 D grid, z 0.35-2.4).
- Per-shot round-2 dressing (`jimo_r2.POST`: s02 / s19 / s20 / s26, `jimo_r2.dress`) now uses the same props (named `dgr_*`, 40 % of the old count, 2.5 D from the marks); `dress_ground()` removes any `dgr_*` that would touch an actor or the lens and re-inks the rest. If you do not call `dress_ground()`, the `dgr_*` props are only kept off the world marks.
- Cost: 2-20 objects for a shot, about 1 s to build, render time within noise.
- Known: dark blue spikes on the moat bank in s19 (left of the ditch) are set objects, not part of the dressing.

**`J.ground_share(png, thr=1.5, detail=False)`** estimates the share of plain ground in a frame: resized to 360 px wide, Gaussian 1.5 px (so 6 / 12 spp noise, OIDN blotches and h264 blocks do not count as texture), Laplacian, fraction of 24 x 24 blocks whose top is below y = 0.4 H with variance < 1.5. Calibrated on 6 frames of the s20 take: mean 0.40 (0.29-0.47); target for a dressed frame <= 0.25. `detail=True` returns the block mask. CLI: `python3 jimo_dress.py share a.png b.png`. Note: the s20 take is plainer than a build of the current set (the take lacks the round-2 furrows), so a draft of the CLI build already reads 0.13-0.2; compare before / after of the same build.

## Vista round 3
The vista (s03, s04, s25) failed QA on four things that were all in the set: flat navy shadow polygons and a navy arc ring on the fields (40-60 % "bare" read), plain tiled fields, no readable Ju, a loose flame on a pole. `jimo_vista3.py` (called by `jimo_vista.build_vista`) fixes them. **`J.build('vista', ...)` / `J.build('s03' | 's04' | 's25')` applies the whole round by itself; a render team needs no call.** `J.vista_r3()` (= `jimo_vista.vista_r3`) is the idempotent finisher: call it once more after you add your own flame cards / poles to the vista, it re-sets the shadow flags and removes flame cards that hang free in the sky (returns `dict(shadow_off, swept)`). `VISTA_R3=0` in the environment gives the old round-2 vista (before / after). Drafts: `set_work/vista_r3/before|after/sNN_tT.png` (360x640, 12 spp, t = 0.2 / 0.6 / 1.0), `before_sheet.png`, `after_sheet.png`, script `set_work/vista_r3/drafts.py <outdir> [s03,s04 [0.2,0.6]]`.

**What made the navy** (raycast from the shot cameras through the navy pixels, `set_work/vista_r3/raycast_navy.py`: surface hit = `terrain` / `river`; shadow caster = `towns`, `townroofs`, `siegetents`, `pen_yan_* / pen_qi_*`, `vtrees`): the fields (`terrain`) fell to the set's SHADE (0.06 0.10 0.27) x (1.5 2.1 1.0) wherever a low sun (15 deg) was blocked, the long shadows of the curtain walls, the 16 siege tents, the 124 pennant cloths (flat slabs) and the 380 `vtrees` cones; the ring is the Jimo moat (`river` object, `vwater` = #4a78b0).
- **Removed**: `vtrees` (380 dark cones: spiky shadows), `siegetents` (16 faceted two-slope shards), the hard cast shadows of `pen_yan_*`, `pen_qi_*`, `wood`, `cloth` (visible_shadow off), the Ju `flame_townfire_*` objects (and Ju's 45 D pole: now 24 D).
- **Changed**: the `terrain` materials (8 variants `JM_vista_*_r3_field_<texture>_<crop>`: warm shade art x (0.58 0.46 0.50), a light violet-brown, never navy; furrow stripes every 3 D; 4 crop tints), `vwater` (dusk grey-teal; `river` ribbon and Jimo ring, ring narrowed to R 39-44), `towns` / `townroofs` materials (`rammed`, `rammed_d`, `tiles`, `tiles_d`, `plaster`, `plaster_d` get the same warm shade: no navy wall faces), sun disc 0.9 -> 3.5 deg (softer edges), the `sky` dome radius 330 -> 1400 and camera clip_end 900 -> 2600 on the vista. **The old 330 D dome hid everything farther than 330 D from the camera: that is why Ju (450-560 D from the s03 / s04 / s25 cameras) was never seen in three rounds.**
- **New (all Geometry Nodes instances: one hidden prototype `r3p_*` + one points object per kind, 1 draw each; the whole vista is 160 objects / 130 k vertices, render time unchanged, 2.5 s per 360x640 draft)**: `r3_hedge0-2` (1625 hedge blobs along the 70 D field edges), `r3_tree0-2` (255 trees: lines on the edges and willows on the river), `r3_hay` / `r3_rick` (778 haystacks and ricks), `r3_hut` / `r3_hut_lit` (78 farm huts, 41 with a warm window), `r3_cart` (11 ox carts), `r3_fig0-3` (55 tiny figures on the roads), `r3glints` (442 warm flecks on the river and the moat), `r3_tent` / `r3_tent_b` (the 16 siege tents: smooth-shaded canvas / hide barrels with a dark doorway and a ridge pole, warm shade). The ordinary towns are now 51 (was 62: 11 fell in Ju's 100 D clearing and the sight line, so the pennant pop-ups count 51 towns; the holdouts are `towns[51]` Jimo and `towns[52]` Ju). Props far from the cameras are scaled up to 2.3 x so they read at phone size. Nothing is placed on towns, the river, the Jimo ring / siege camp, the Ju ground or the roads.
- **Ju** (`towns[-1]`, `marks.ju`, (-95, 330), now 80 D across instead of 40): a clear sight line (no ordinary town) from the cameras, ordinary towns kept 100 D away; 26 houses with warm windows, a watch tower (33 D) with a fire basket and big halo, 28 emissive wall lamps with halos (`julamps`, `halos`), two gate fire stakes and a glowing gate (static flame meshes inside `townglow`, not separate flame objects), a glow dome of two additive halo cards (r 116 / 68 D) and a warm ground pool (`r3pool`). Ju carries only a small Qi pennant (24 D pole), no Yan pennant. Seen from s04 it is the lit tower with the lamp row on the horizon left of Jimo; s03 and s25 see it on the horizon too (`pen_qi_52` = Ju's pennant).
- **The flame on the pole** (s04, g315-325): the red flag and the flame were Ju's `pen_qi_<n>` pennant and Ju's two `flame_townfire_*` objects (separate objects with their own scale / rotation flicker); when the camera orbit took the flag out of the frame the fire stayed. Now there is no separate flame at Ju at all (static flame meshes inside the town object); `vista_r3()` additionally deletes any flame card with no parent that is more than 6 D above the terrain, and re-seats a flame object whose origin drifted.

**Numbers** (360x640, 12 spp, `J.ground_share`; before / after, 9 drafts each): max 0.046 -> 0.008 (mean 0.022 -> 0.003). Note the metric is blind to the old problem (a tiled patchwork has Laplacian texture); the navy measure used instead (share of pixels below 0.4 H with b > r + 12, b > g + 4, mean < 110): mean 0.32 / max 0.50 before, mean 0.045 / max 0.077 after (the rest are the black pennants and the dark gate leaves).
**Render teams**: use `J.build('s03'|'s04'|'s25')` as before. Do NOT call `J.dress_ground()` on the vista any more (the instanced farmland replaces it). Keep the vista cameras from `J.shot_camera` / `J.key_camera` (clip_end 2600 is set in `make_camera`); a camera made elsewhere needs `clip_end >= 2000` or the far plain and Ju are clipped. If the old `pn*` / `qr*` states are keyed they work unchanged.

## Vista round 4
QA-art (s03, s04) asked for set-level fixes in the vista; s25 (passed) is the regression check. All of it is in `jimo_vista3.py` / `jimo_vista.py` and is applied by `J.build('vista' | 's03' | 's04' | 's25')`; `VISTA_R3=0` still gives the round-2 vista.
- **Pennants = silk.** Each pennant is now two objects: the pole (`pen_<yan|qi>_<town>`, origin at the pole foot) and the cloth (`pcl_<yan|qi>_<town>`, origin at the pole top, no cast shadow). Cloth: 12 x 7 grid, swallow tail, a travelling fold and a slight curve (two-sided); Yan = lit black silk (`silk_blk`, dusk-warm shade, GGX sheen) with a red silk border (`silk_red`); Qi = crimson silk (`silk_qi`) with a gold border (`silk_gold`). The border is separate cells (the old coplanar trim faces z-fought: that was the orange speckle). The Siege camp banners use the same silk.
- **Moat / river** (`vwater`, `r4_water` material): dark teal body, a sky-coloured emission (DUSK orange, DAWN peach; the sky dome is not visible to glossy rays, so it is faked) weighted by facing, ripple streaks and warm glints; the `r3glints` flecks remain. It reads as a pale gold ring at dusk.
- **Plank**: the navy slab in Jimo's yard was the town gate block (`M['black']`); gate leaves are now warm timber (`r3_gate`, planks texture, warm shade).
- **Helpers** (`J.*`, also `jimo_vista.*`):
  - `J.vista_pennant_order(cam=None, kind='yan')`: town indices of the 51 ordinary towns sorted near to far (ground distance) from `cam` (Blender camera object, Vector / (x, y, z), or None = the scene camera). Holdouts excluded.
  - `J.set_pennant_scale(idx, k, kind='yan', frame=None)`: `idx` = a town index from the order list; k 0..1. The pole stands from k > 0 and the cloth scales uniformly about the pole top (hangs, never flat or diagonal). Key it per frame (`frame=`) for the pop-up; staggered: `for n, idx in enumerate(order): J.set_pennant_scale(idx, ramp(f - n * step), frame=f)`. `set_pennants` / `set_qi_return` keep working (the pole is shown at once, the cloth grows with the pop value); they override a manual `set_pennant_scale` on the next call.
- Drafts: `scratchpad/r4/before|after` (360x640, 12 spp, t 0.3 / 0.9), `after_sheet.png` (6 frames + a s25 take frame). Script: `set_work/vista_r3/drafts.py <outdir> s03,s04,s25 0.3,0.9`.
- Not changed (QA items outside the set): the pennant count and scale on screen (near cloths are still about 20 D wide; s03 shot-side decision: use the order helper with a smaller cloth scale, e.g. `set_pennant_scale(idx, 0.4)`), Ju bloom.

## Round-8 shared assets (`jimo_props.py`, exposed as `J.prop_*` and `J.gapfill`)

All need a built scene (`J.build(...)`, they use its materials and its NIGHT / DUSK / DAWN light). `loc` = world point, `rot` = Euler (x, y, z) in RADIANS (one number = yaw). Local frame +Z up; every prop is ONE object (the chariot: a root empty + 3 children) with the 3 px inverted ink hull, hidden from bounce rays, so teams can key `location` / `rotation_euler` / `scale` on it with `J._xf(ob, loc, rot, scl, frame)`. They are NOT part of any `build()` yet: call them from your shot script (and key them, e.g. for the s24 rout).

- `J.prop_reed_bundle(loc, rot=None, scale=1, n=60, seed=1, cd=4.0)` : 40-80 (`n`) thin tapered 5-sided reed stalks (8 ochre-to-straw tones, random splay, fatter in the middle, fanned at the +X end), tied with 2 red cords (rings + a knot tail); 1.2 D long (along +X), 0.35 D thick at scale 1. `cd` = the camera distance the 3 px hull is tuned for (kept low so the hull does not swallow the stalks).
- `J.prop_pot(loc, rot=None, kind='jar'|'bowl'|'pot', scale=1, cd=10)` : lathe profiles in warm terracotta (`#b9552a`) with a darker shoulder band, a lighter lip and a real inner wall: jar 1.45 D tall x 1.3 wide (foot, belly, shoulder, neck, flared lip), bowl 0.5 x 1.3 (foot ring, rim), pot 1.07 x 1.35 (round belly, rolled rim, two lug handles). Origin at the foot centre.
- `J.prop_helmet(loc, rot=None, scale=1, cd=10)` : bronze Warring-States helmet: dome with brow band and 12 rivets, lamellar neck guard flaring at the back (+Y; the face / front is -Y), two ear flaps, crown socket and a red plume tuft (11 strands); open underneath. Origin: the neck guard's lower edge on z 0 (brim at 0.4).
- `J.prop_chariot(loc, rot=None, tumble=0.0, scale=1, cd=14)` : NEW two-wheeled wooden war chariot (the camp's `chariot0/1` meshes are baked into the camp and cannot tumble; leave them for the rout): open red box with gold rails, long pole and yoke, standard pole with a red pennant, two spoked wheels R 1.5 D (gap 4.2 D); forward +X, about 8.5 D long at scale 1 (use 0.5-0.9). Returns the ROOT empty; children `<root>_body`, `<root>_wheel_a` (y +), `<root>_wheel_b`. `J.prop_chariot_set(root, tumble, frame=None)` re-poses it (key one call per frame to animate): 0 upright, ~0.35 tipping about the +Y wheel's ground contact, 0.7 on its side with wheel a rolling off ahead (+X, spinning, hopping, toppling), 1 wrecked on its side, wheel b dropped. Everything stays z >= 0. Move / spin the whole thing by keying the root.
- `J.gapfill(cam=None, frames=None, z=0.026, mat='bank', maxd=130, pad=4, retint=True)` : lays a dark-earth plane with the lane dirt texture (`M['bank']`, 8 D tile) at z 0.026 (above the base ground and the `fields` quads at 0.02, under the lane quads 0.03, furrows 0.05, props, herd and wall) under the convex hull of the ground the camera sees (up to 130 D, padded 4 D; `frames` = film frames of a keyed move, up to 40 samples; default the current frame; the moat strip y -30..-9.5 is cut out in jimo_out / yan_camp). `retint=True` also swaps the violet `tunnel` material of the s19 / s20 `furrows` strips for dark earth. Idempotent. No gapfill existed (s19 only has `furrows` / `dress`), so this is new and general. Call it AFTER `J.key_camera(shot)` and after the shot's POST dressing: `J.gapfill(frames=range(f0, f0 + frames + 1))`. Effect (`set_work/props_r8/gapfill_compare_s02_s20_s19.png`, base | gapfill pairs): s20 the pale lilac field and violet stripes become warm dark earth with brown furrows; s19 the flat lilac ground becomes textured earth; s02 is unchanged (its lane is already lane texture).
- Test sheet: `python3 jimo_props_sheet.py NIGHT abc` -> `set_work/props_r8/props_a.png` (3 pots, reed bundle, helmet), `props_b.png` (chariot upright + tumble 0.8), `props_c.png` (helmet front and back), `props_sheet.png` (the three side by side, 360x640 each, night light).
- Known weaknesses: at night the red plume / cords shade towards purple (the set's navy shade); the helmet is faceted by 24 segments; the tumbled chariot is a pose, not a physics sim (teams can add a hop by keying the root).
