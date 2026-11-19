# v3/set3d15/set15.py : film 15 set ("ไอ้ปลาดิ้น", the Fosbury Flop). bpy 5.x, Cycles CPU. Same shape as set3d10/API.md.

Files
- `set15.py`: build, presets, hooks, placeholders, anchors. `set15_lib.py` (house-look materials, root, sky, sun), `set15_a.py` (location A, jump set), `set15_b.py` (location B, crowd, flags, flame), `set15_props.py`, `set15_shots.py` (36-shot table, camera moves, FG props, staging).
- `run15.py`: CLI. `python3 run15.py stills|final [shots]`, `contact [shots] tag`, `sheet` (builds contact.jpg + contact_small.jpg from work/final), `day16`.
- `set15_hue.py` (hue rows + shade hue, as harbour_hue.py), `t_anim.py` (ALL OK, 67 checks), `contact.jpg` / `contact_small.jpg` (37 tiles: every shot's START framing, 720x1280, 12 spl, grey placeholder cards, label under each tile, cyan line y 880), `work/final/` (the 37 PNG), `work/hue_rows.txt`, `work/final_log_*.txt`, `bak_r0/` (first working build). `styleboard/` is the approved board.
- Built on `set3d2/tower.py` (setup_render, setup_grade, make_camera, _key) and the board's `sb.py` (props, MB, sky). The materials keep the board's noise tones but use the house shading (one hard key + painted blue-violet shade, no bounce).

World: 1 unit = 1 D = **0.54 m**; F.HEIGHT = the cast15 heights (dick 3.76, coach 2.99, boy 3.2, rival 3.5, official 3.2, photographer 2.97 D), Z up. Inside the builders metres; everything hangs under `SETROOT` (scale 1/0.6). Hooks that name metres say so; positions, cameras and marks are D. No DOF, no text, no digits anywhere. 1963 = SAWDUST pit, never foam.
- **A** high-school track 1963: pit (0, 7.6) m in a wooden frame, flat sawdust + loose sawdust pile (-4.1, 6.9) m beside it, wooden standards (4 m apart, y 5.3), striped bar on pegs (r 5.5 cm), run-up, cinder track + oval, bleacher (x 11.6.., faces the pit) with coats and bags, benches, coolers, bags, towels, stacked hurdles, cones, tape reels, wheelbarrow, rake, scorer's table, trash cans, bicycle racks with 5+4 bikes, chain-link fence, pennants, road with 7 parked 1960s cars, 2-storey brick gym, maples (green or autumn), tall pines.
- **B** Olympic stadium 1968: bowl centre (0, 8) m, 28 tiers with aisle stairs and rails, press box + roof section (far side), blank scoreboard, 18.5k crowd figures (body + head + arms), 87 flags, cauldron with animated flame, 4 floodlight towers, officials' table (clipboard, small flag), 3-step podium at (-9, 10) m (no numbers), photographers' platforms, foam pit (3 layers of blue-grey blocks, centre (0,15) m, top 1.0 m), tartan fan + apron around the jump, steel standards at y 11.6 (NO hurdles in the jump area), 60 hidden stand flash bulbs.

## Build and render
```python
import sys; sys.path.insert(0, '.../v3/set3d15'); import set15 as F, set15_shots as SH
A = F.build('A', 'GOLDEN')            # build(location=None, light=None, clear=True, dress=True, shot=None) -> anchors
A = F.build(shot=24)                  # location + light of a plan shot
cam = SH.setup_shot(24)               # camera keys (start f0 .. end f1, eased) + FG props; frames default to round(t*30)
F.make_camera(F.cam_from(loc_D, look_D, lens=22))   # your own camera (use F.make_camera: far clip, DOF off)
F.setup_render(scene, 'final' | 'preview'); F.T.render(path)
F.stage_placeholders(24, tuple(cam.location))        # grey cards at the plan's stand points (stills only)
```
Lights: A `GOLDEN | DAY`, B `EVE | TENSE | DAY` (`F.LIGHTS['A_GOLDEN']`...). One sun per preset (A GOLDEN az -60 el 28; B EVE az -48 el 19; TENSE el 15 dim; DAYs el 42-44), crisp shadows. TENSE: darker sky, 4 floodlight pool spots (no shadows) and crowd dimmed to 62 %. DAY A has fresh green leaves, GOLDEN autumn leaves.

## Hooks (frame = scene frame at 30 fps; frame=None sets the value now, frame=N keys it)
| hook | what |
|---|---|
| `set_bar_height(h_m, frame=None, peg='both'\|'L'\|'R', interp='LINEAR')` | top of the bar in METRES (A default 1.72, B 2.24); one peg only tilts the bar (shot 18: L then R). |
| `bar_fall(start_frame, side='back'\|'front'\|'left'\|'right', bounce=True, seed=0) -> rest_frame` | knock-off: gravity, 3 damped bounces, roll, settles on the sawdust (0.44 m) / foam (1.0 m). |
| `bar_reset(frame)` | bar back on the pegs (hard cut). |
| `flash_bulb(frame, where=None, energy=2e4)` | camera flash pulse at the photographer (default mark; where = D xyz): point light + glowing bulb, 3 frames. |
| `stand_flashes(f0, f1, density=0.35)` | bulbs popping in the stands (B). |
| `sawdust_spray(frame, position_D, strength=1, seed=0, floor=None)` | chips/splinters (thin boxes, no blobs): a ring-shaped crown, a faster centre plume, fine specks, tumbling, falling back and landing. One object per burst (geometry nodes keyed on the frame). strength 0.5 = bar bounce, 1 = body. |
| `crowd(amp_m, hz, cheer, frame)` / `crowd_mode('hush'\|'tense'\|'normal'\|'groan'\|'cheer', frame)` | bob amplitude/frequency, cheer = stand up + arms up. Plan: hush 24-30, cheer at 31 (key hush at 28-29, cheer at 59.1 s -> frame 1773). |
| `torch_flicker(level, frame)` | cauldron flame size (it flickers by itself via drivers) + warm light. |
| `flag_wave(amp_m, hz, frame)` | rim flags (geometry-node wave, always running). |
| `switch_light(to, start_frame, n_frames=12)` | smooth blend of the built preset to another of the same location (sun colour/energy/direction, shade of every material, crowd dimming, sky ramp, hills, floods) via drivers. Shot 30: build B TENSE, `switch_light('EVE', round(56.6*30), 10)`. |
| `set_season(k, frame)` | A leaves 0 green .. 1 autumn. For shot 16 render GOLDEN and `build('A','DAY')` plates and dissolve. |
| `clear_keys()` | drops hook keys, keeps drivers / waves. Bar and ctl keys win over un-keyed calls: key every state or clear first. |

## Stand points (`A['marks']`, D, feet; z = floor)
A: `runup_path` (list of 5 points, the curve), `runup_start`, `takeoff`, `bar_centre`, `landing`, `coach_bleacher` (bleacher front), `coach_end` / `pile` (sawdust pile, shot 36), `dick_mark`, `boy_wait_a/b/c`, `boys_bench_a/b/c`, `photographer`, `reader` (bleacher seat), `bench_right`, `cooler`, `scorer`, `rake`.
B: `runup_path`, `runup_start`, `takeoff`, `bar_centre`, `landing`, `dick_mark`, `dick_b2` (by the standard), `coach_stands` (row 8, aisle side), `podium_top`, `podium_2`, `podium_3`, `photographer`, `photographer_b`, `official_a/b`, `official_bar_l/r`, `rival_a/b`, `rival_land`, `table`, `torch`, `foam_edge`.
Heights `F.HEIGHT` (D, cast15): dick 3.76, coach 2.99, boy 3.2, rival 3.5, official 3.2, photographer 2.97.

## Cameras and shots
`F.SHOTS[n]` (n = 1..36): t0, t1, loc, light, `a` (start) and `b` (end) camera in METRES (`SH.cam_dicts(n,'a'|'b')` gives D), fg list, actors, note, `punch`, `whip`. Moves follow the plan (push 6-10 %/s + lateral slide 40 px/s, orbit 15 deg/s shot 9, rise in 5/17, WHIP pans in 3/21/29/35, punch pushes 15-25 % in 0.4 s keyed with Bezier). `SH.setup_shot(n)` makes the camera and builds the FG props (hurdle, cone, bench end, standard base/peg, pine branch, rake, cooler, sawdust edge, bar end, clipboard, stopwatch, camera bag, hurdle stack, rail, sawdust chips, flag pole, table corner, foam edge, bar on mat, crossbar end); they sit 0.8-1.2 m (1.3-2 D) from the lens and follow the camera 90 %. 'shoulder' / 'thumb' FG are cast pieces (nothing built).

## Placeholders
`F.placeholder_actor(role, mark_D, face_to)`: grey rounded card at real scale. `F.head_pixels(n)` gives chin/top y px (caption rule y < 880).

## Measured
- Final 720x1280, 12 samples, OIDN, 2 threads (two processes in parallel): **10.4 s wall / 20.3 s CPU per frame** average (max 25.8 CPU). Build 0.5 s (A), 1.6 s (B).
- Shade hue (chroma-weighted mean of shaded pixels, `set15_hue.py`): A GOLDEN 250.8, A DAY 247.2, B EVE 241.4, B TENSE 240.7, B DAY 241.3 (all 240-260). Magenta: 1.3 / 0.5 / 4.2 / 6.8 / 3.8 %. A few single B tiles read 234-239 (frames with little shade).

## Gotchas / known gaps
- Cards are not part of the set; the placeholders are grey. Lens 22 mm portrait is 49 x 78.6 deg: FG props must sit within about 0.4 m of the lens axis sideways.
- Several A tiles still show plenty of sky (horizon near mid-frame); tall pines/gym fill the lower third of it. Pitch the camera down in post-brief tuning if wanted. A few B tiles (20, 21, 25) are dominated by their FG prop at the start frame.
- Shot 14 (newspaper) and 11/23 (shoulder / spectator) rely on cast FG pieces. Foam-pit dent is not built. Flash bulb pop is a point light under the house shading (flat, no shadows).
- `switch_light` keeps the start preset's sun direction in the toon term (a few degrees). The tartan and foam in B can burn orange/white near the flood pools in EVE.
- Light-blend and hooks use drivers/geometry nodes: render in Blender (not an exporter).

## Round 1 changes (director review)
- A cameras are pitched down (>= 11 deg, camera up to 2.1 m) so the horizon sits in the upper third and sky is about 20-25 %; shot 2 is a low medium (Dick ~40 % of frame height), shot 4 sees the bar against the golden sky and pines, shots 25-29 look at the bar from the front quarter (6 m, bar span across the frame, 1+ D clear above and below, standard in a side third; jumper placeholder feet at 1.15 m).
- FG props are placed at an edge/corner of the frame (0.55-1.2 m from the lens, lateral 0.33 x distance), sized by kind, and never on the centre. The lanyard / rail pieces were shrunk.
- A ground: grass patches, many more tufts, 4 extra lane lines and start ticks on the cinder, chalk dashes along the curved run-up and a take-off tick, rake marks, footprints and a body hollow in the sawdust, scattered leaves (150 autumn / 25 green); golden saturation lowered (grade 1.0, key less orange).
- B: floodlight pools 3.6x weaker with a wide soft cone; B shade redder-violet (hue up); TENSE sky bands made less magenta.
- Measured after round 1 (shade hue / magenta): A GOLDEN 249.1 / 1.7, A DAY 255.1 / 0.7, B EVE 251.3 / 6.5, B TENSE 247.3 / 8.9, B DAY 254.6 / 2.5. Tiles outside: shot 25 (B TENSE, dark sky) 241.3; A tiles 4, 8 slightly over 260 (260.3 / 260.6), 10, 12, 14 at 236-239 (little shade in frame).
- Backup of the pre-round-1 code: `bak_r1/`.

## Round 2 changes (SET gate: QA-art FIX-FIRST, QA-tech FAIL)
- Standards: round silver-grey tubes (r 0.026 m) with small pegs, base plate and ladder pins a third of the old size, both locations; FG standards are 0.95 m from the lens at the frame edge (about 45 px wide). Bar r 0.07 m, white / red stripes with a little emission so it reads in shade; B bar default 2.34 m (0.55 D above Dick's head top, 3.76 D).
- Reveal views 26-29: camera 0.8 m below the bar, 4.6 m from it (5.4 m for 29), tilted up about 10 deg, bar across the frame against the dark upper stand; 26 lateral track (30 deg off), 27 tight (12 deg), 28 = 27 for the EVE contrast, 29 wider + FG foam edge + WHIP down. TENSE crowd dimmed to 37 %, a hard pool spot on the bar area, foam top darker with a noise/seam texture, tartan less saturated (brick red) with its shade kept red-brown (tartan smix 0.25) so it does not turn mauve.
- Shot fixes: 3 / 35 (pit + bar in frame, 35 from high left, actor on the curve), 4 (bar against the sky, sawdust at the bottom, thin standard), 5 (real high crane), 11 (over-shoulder, Dick large), 14 (close on the reader seat), 15 (bleacher foot), 18 (both officials), 19 (dark table, rival on the run-up), 20 (bar above the head with pegs), 21 (bar + foam in start frame), 22 (apron small), 23 (coach on an aisle step), 24 (peg FG only), 25 (bar at 1/3 height, runner visible), 30 (Dick at 1/3), 31 (closer on the podium), 33 (camera raised, foam toned, exposure -1/3 stop, bluer sky), 34 / 36 (sawdust mound INSIDE the pit frame, smooth with chips; boys' bench beside the pit).
- Other: A golden sky ramp warmed (no cool blue zenith), B DAY floodlights dimmed, rim flags and A flag recoloured to non-national stripe sets, pit footprints / rake marks, concrete tones neutral.
- Contact sheets: `contact.jpg`, `contact_small.jpg`, new `contact_phone.jpg` (360x640 tiles). Backups: `bak_r1/` (before round 1 fixes), `bak_r2/` (before this round).
- Measured (shade hue / magenta): A GOLDEN 253.6 / 1.6, A DAY 254.6 / 0.7, B EVE 253.2 / 5.1, B TENSE 249.1 / 3.7, B DAY 254.0 / 3.4. Single tiles: shot 22 shade 243.9 (just under 244), shot 8 260.2, shots 19 and 28 magenta 11.9 / 11.7 %.
