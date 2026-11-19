# v3/set3d_ext/mech/office_mech.py : the mechanism on the wall map (shot plan build steps 2 and 9; shots 19-22)

An extension module. It imports `v3/set3d/office3d.py` (S), `v3/set3d_ext/props/office_props.py` (X) and uses
`v3/set3d_ext/light/office_light.py` (OL); it edits none of them. Paper artwork (compass, pictograms, speed sign) is read from
the paper registry (`v3/paper/tex/registry.json`) through `X.paper_png`. Textures drawn here (PIL, cached in `tex/`): the Latin H,
the wind arrow, the isobar rings, the sweat drop, the snail shell. Worked example of every setter and camera:
`v3/film/s19/shot.py` (shot 19, 245 frames rendered with it, hand-drawn line).

```python
import sys; sys.path.insert(0, PROJ + '/v3/set3d_ext/mech')
import office_mech as M; S, X = M.S, M.X; import office_light as OL
A  = S.build('INTERIOR_DAY')
PA = X.build(A, hi_map=True)            # 6000 px map: required for every lens under ~1 D (19, 20, 22)
MA = M.build(A, PA, wall_height=0.50)   # collection MECH, control empty 'mech_ctl'; everything hidden / at 0 (M.reset())
OL.apply('office_grey')                 # AFTER M.build: apply() re-tints every lit material that exists, ours included
S.set_track(1, 0); X.set_chalk(1.0); [X.set_ghost(i, 1.0, 0.35) for i in range(1, 7)]; X.set_label(1.0)   # the map after shot 18
M.set_wall('E', rise=4, slide=1, lock=1); M.set_wall('W', rise=4, slide=1, lock=1); M.set_lane(1.0)       # the state at the end of 19
S.make_camera(M.cam('corridor_cam'))    # setups carry loc, look_at, lens, up (and roll); S.make_camera honours up and roll
```

Hand-drawn line: every position below is relative to the LINE (`M.world`), see section 0; re-checked on the gate stills
`gate_hand/` and in the 245-frame take s19.

Every setter: `frame=None` sets the state statically (what s19 does: it calls the setters for every frame g, then renders);
`frame=N` inserts keyframes (LINEAR; visibility CONSTANT) so the same state can be keyed into a Blender timeline. Scalar controls
are custom properties on `mech_ctl` read by simple-expression drivers (no Python at render time), transforms are keyed on the objects.
Arguments a setter does not get keep their last value. Settings that are computed in Python (wind positions, spinner position along
a ghost track, wall step heights) need a key on every frame where they change if you key instead of setting per frame.

## 0. The red line is HAND-DRAWN (client decision, 18 Nov): what changed

The set's track is the freehand stroke (`office3d.TRACK_STYLE = "hand"`, 85 points): it leaves the storm symbol heading north-west,
bows up to **0.154 D west** of the straight chord around u 0.5 and comes back north-north-east into N.Y. (arc length `M.TLEN` = 1.076 D,
chord `M.CHORD` = 1.016 D). Everything of this module that sits on or along the line is now built from `S.track_point(u)`:
lane, inner (corridor) edges of both walls, corridor-face H, pictograms, wind arrows, speed sign orientation, wake, spinner positions
(`M.world`), plan-view truck and the corridor lens. `T0`, `TDIR`, `NDIR` are the CHORD (only the frame the wall meshes are built in;
never place anything on the line with them). The straight version is kept as `office_mech_straight.py.bak` / `API_straight.md.bak`.

## 1. Gate (build step 2): PASSED at 0.35 D with the lens off the line (hand-drawn corridor)

`gate_hand.py <out> <scale> <samples> names` and `cams_hand.py <out> names` render the gate stills (office_grey, 6000 px map, walls
0.50, up = wall normal): `gate_hand/sheet.jpg` (plan_debug, corridor_cam, corridor_a0, corridor_far) and `gate_hand/cams.jpg`
(every named camera). Result:
- Lens straight behind the storm ON the line (`corridor(a=0)`, `gate_hand/corridor_a0.png`): FAILS: the corridor bends west and
  back, so the inside of the bend (the east wall's face near u 0.5) hides the far lane and N.Y.
- Lens 0.155 D west of the chord (`corridor(a='auto')`, the default, `gate_hand/corridor_cam.png`): PASSES: the sight line to N.Y.
  clears both bent faces by 0.027 D; the walls tower on both sides and leave the top of the frame, the lane with the red line
  snakes away between them to the red arrow head at N.Y., the label beyond it; the spinner sits at the bottom edge. `a='auto'`
  computes that lens offset (`M.clear_lateral(u_lens, h)` -> (lateral, margin)); compute it ONCE per shot and pass it as a number
  while the lens creeps (the search is on a 0.005 D grid and would jitter frame to frame).
- No shimmer on the 6000 px map in the s19 corridor creep (g1308-1328, see film/s19/QA.md).
- Wall height stays **0.50 D** (tops 0.15 D above the lens). Fallback `corridor_far` (0.7 D, auto lens) kept as a camera, not used.

## 2. Geometry (D)

`M.world(a, s, h, u=None)` = the point `a` D east of the HAND-DRAWN line (negative = west, measured across the line), `s` D along it
from the storm symbol by arc length (or `u` = track fraction as `S.track_point`, 0 storm .. 1 N.Y.), `h` D proud of the paper (toward
the room). `world(0, 0, 0, u)` is on the red line (within 0.1 mm of `S.track_point(u)`). For |a| >= `LANE_HALF` it follows the line
smoothed with a 0.035 D gaussian (`dev_s`; it differs from the stroke by at most 3.7 mm), so lane edges and corridor faces are smooth.
For u < 0 or u > 1 the frame continues along the chord. Helpers: `M.frame(u)` -> (point, tangent north, east) of the line at u;
`M.tangent(u)`, `M.east(u)`; chord frame `M.sc_of_u(u)`, `M.u_of_sc(sc)`, `M.dev(sc)` (line offset from the chord, + east),
`M.dev_s(sc)`, `M.lateral(a, sc)`, `M.world_sc(lateral, sc, h)`; `M.YDIR` (+y, into the wall; the wall normal toward the room is
`-M.YDIR`). Paper plane y = -0.05.

- Walls flank the line from u 0.05 to 0.92 (`U_WALL`); locked corridor faces exactly 0.11 D across the (smoothed) line on both sides
  (`LANE_HALF`, lane 0.22 D wide), so the corridor bends with the line.
- Each wall = four stacked terraces. The corridor face of each terrace follows the line; the OUTER edge of the bottom terrace is a
  straight contour parallel to the chord, pushed out by `M.wall_shift(side)` (W 0.151 D, E 0) so no terrace is narrower than its
  nominal width where the line bows toward it; upper terraces half follow the line (`M.warp(side, a, sc)`), like contour lines.
  Nominal widths east (Atlantic) 0.72 / 0.56 / 0.42 / 0.30, west (land) 0.50 / 0.40 / 0.31 / 0.23 (+ the bow), each 0.055 shorter
  at both ends than the one under it, height 4 x 0.125 = 0.50. Material: pale blue-grey paper (`#c4c6d4` east, `#cac6d2` west) in the
  office light model (S.mat_lit + form), ink edges (inverted hull 3.5 mm, camera rays only), Latin H (navy) on the top terrace and,
  bent along the corridor face, on each corridor face. Even locked, terrace k stands k x 6 mm back (no coplanar faces).
- The east wall at slide 0 covers the printed H of the map (x 1.04, z 2.15) with its lower terraces; the white chalk curve (east of the
  line) disappears under the east wall as it rises (19 crumbles it at 43.70).
- Lane u 0.04-0.95 on the paper (0.6 mm proud, under the red track tube, so the line stays its centre line; 180 segments).
- Speed sign default: u 0.62, a +0.085 (roadside, foot of the east wall), disc centre wall height + 0.12 = 0.62 D proud, facing south
  along the local line.
- Compass default `COMPASS_XZ` = (0.50, 2.86) world (x, z): north-east of the lane end, above the N.Y. label, clear of the walls.

## 3. Setters

| Setter | What it does |
|---|---|
| `build(A, PA, wall_height=0.50)` | Builds everything (hidden), returns `MA` = {cams, wall_height, lane_half, u_wall, sign_u, compass_xz, track_dir, east_dir}. Rerunnable. |
| `reset()` | Walls sunk, lane at 0, compass / pictograms / sign / wind / wake / spinner extras / shell hidden. |
| `set_wall(side, rise, slide, lock, fade, pulse, frame)` | `side` 'E' (Atlantic) or 'W' (land). `rise` 0..4: terrace k grows out of the paper during rise k..k+1 (eased; 4 = full height; key 0 -> 4 over 18 frames for four thuds). `slide` 0..1: 0 = the wall 0.15 D further out, 1 = corridor face on the lane edge (the squeeze). `lock` 0..1: 0 = stepped corridor face (k x 0.035 D set back), 1 = vertical face; the corridor-face H is stamped on as it locks (lock 0.3 -> 1, needs rise > 3). `fade` 0..1 opacity of body, ink and H (shot 22: fade to faint outlines). `pulse` = height x (1 + 0.15 pulse) (lock boom in 19, the reveal pulse at 53.62 in 22). |
| `set_lane(grow, red, fuse, alpha, glow, frame)` | Pale lane with white dashes on both edges. `grow` 0..1 unrolls it from the south. `red` 0..1 turns the dashes red; `fuse` 0..1 slides the two dash lines into the centre and closes the gaps while the pale body fades (shot 22: "dashes turn red and fuse into the pencil line": key red 0->1 then fuse 0->1). `glow` = neon emission on the dashes (19 uses 0.9 at hum-on, 0.2 after). |
| `set_compass(show, scale=0.8, rot_deg, ping, xz, frame)` | Compass rose (red N) flat on the map. `show` doubles as a pop scale; `ping` 0..1 = scale bump x(1 + 0.35 ping). |
| `set_picto(side, show, scale, s, h, yaw_deg, wobble_deg, tilt_deg, frame)` | No-turn pictogram on a bracket standing out of a corridor face ('E' no right turn, 'W' no left turn), `s` D along the line, `h` D up, card turned `yaw_deg` toward the south. 19 uses scale 0.5, s 0.22, h 0.30, yaw 22 (E) / yaw 60 + tilt 35 (W, so the camera south-west and above sees its face), and a 1.25 overshoot pop with a decaying wobble. |
| `set_wind(progress, amount, span, frame)` | 14 pale arrowhead cards streaming north up the corridor (tilted 35-60 deg off the paper, 0.05-0.30 D up, a within +-0.075). `progress` 1.0 = every arrow crosses the span once (advance about 0.9 per second for a gust; set it every frame); `amount` 0.33 / 0.66 / 1 = the three waves of shot 20; `span` u range (default -0.45 .. 1.05: from behind a corridor lens at u -0.12 to past N.Y.). |
| `set_speed_sign(show, spin_deg, scale=0.8, u=0.62, a, height, frame)` | Round '100' sign with THAI 'กม./ชม.' on a post at the roadside, disc above the east wall top, facing south (upright for an up = wall-normal camera). `spin_deg` turns it about the post (0 = face south; key the spin in the wake at 49.10 and settle on 0 or 360 by 50.30). scale 0.8 = 0.21 D across. |
| `set_spinner_fx(ring, ring_pulse, drop, drop_slide, frame)` | On office_props' spinner root: isobar ring card (alpha `ring`, scale x(1 + 0.25 ring_pulse)) and one sweat drop (alpha `drop`, `drop_slide` 0..1 runs it 0.06 D down the disc). The spinner itself stays `X.set_spinner(u or xz, angle, wobble, squash, fast)`: squash > 1 = tall and thin, key angle every frame. |
| `set_wake(head_u, length_u, alpha, frame)` | Red-hot wake streak on the line from u head-length (thin, faint) to head (full width, bright, glows). Shots 20, 21, 25. |
| `set_ghost_spinner(i, s, angle, show, alpha, scale, frame)` | Grey ghost spinner i (1..3) at fraction `s` of its faded curved track (`GHOST_FOR` = {1: track 3, 2: track 1, 3: track 6} of office_props); `alpha` = shared ghost opacity. For shot 21: crawl s at about a sixth of the storm's speed, overtaken at 50.9, 51.3, 51.7; brighten the tracks with `X.set_ghost(k, 1.0, alpha=0.6)`. `ghost_point(i, s)` gives (x, z) and heading. |
| `set_shell(show, which=2, frame)` | Snail shell card on ghost spinner `which` (does not spin). |
| `face_basis(nrm, up)` | Rotation for a card that faces `nrm` with image-up `up` (helper for extra cards). |

Not here (by design): the speed-line overlay (conform), the label (`X.set_label`), the red line (`S.set_track`), the chalk crumble
(`X.set_chalk(1, crumble, alpha)`; 19 keys crumble 0 -> 1 and alpha 1 -> 0.45 at 43.70). Long Island: the map art already has the
island shape east of the N.Y. dot (6000 px raster, x 0.08..0.18, z 2.62); nothing was added.

## 4. Cameras (`M.cams()` or `M.cam(name)`, all 22 mm; dicts for `S.make_camera`)

Parametric builders: `M.corridor(u_lens, h, look_u, look_h, a='auto', look_a, lens, roll, target_u=1.0)` (up = wall normal;
a = 'auto' puts the lens where it sees N.Y. down the bent corridor, or pass the east offset from the line), `M.plan(u_center, dist,
a, roll)` (square-on, north up), `M.rake(target, dist, elev_deg, az_deg, up=None)` (az 0 = from straight south of the target along
the line, + = from the east; elevation above the paper). `M.lerp_setup(a, b, t)` blends two setups (use an eased t; s19 blends
target / log-distance / direction / up instead, see `blend` in `film/s19/shot.py`, which keeps snaps from cutting corners).

| name | for | definition | measured in s19 / stills |
|---|---|---|---|
| `rake_spinner` | 19 (0) | rake(world(0.02, u 0.12, h 0.03), 0.80, elev 30, az -55) | spinner 108 px at (352, 750) |
| `rake_north` | 19 (1) | rake(world(0.05, u 0.40), 1.80, 35, -12) (s19 aims at a -0.04 so the land wall is not cropped) | both walls in frame, N.Y. at y 520 |
| `corridor_cam` | 19 (2), 20, 22 (not the same camera as office_props' `corridor_cam`, which sits elsewhere) | corridor(u_lens -0.12, h 0.35, look_u 0.85, look_h 0.06, a 'auto' = lens 0.155 D west of the chord) (s19: a = clear_lateral(-0.15, 0.35) fixed, u_lens -0.17 creeping to -0.13) | hand-drawn corridor: N.Y. at (378, 652), sight-line clearance 0.027 D; spinner 410-440 px at the bottom right edge (530, 1210) |
| `corridor_far` | fallback | corridor(-0.20, 0.70, 0.95, 0.10), auto lens | not used (gate passed at 0.35) |
| `plan_view_start`, `plan_view` | 19 (3) | plan(0.03, 1.2, roll -12) -> plan(0.62, 1.2) | N.Y. y 363 (upper third) at the end of the truck |
| `spinner_high` | 19 (4) | rake(world(0, u 0.17), 0.80, 52, -8) (s19: u 0.20) | spinner 164 px at y 630 |
| `launch_end` | 20 | corridor(u_lens 0.33, ...), auto lens: 0.45 D of travel after the launch | starting value; inside the bend, re-aim it along `M.frame(u)` (see the note below) |
| `sign_cam` | 20 end | from world(-0.04, u 0.42, h 0.30) at the sign centre, up = wall normal (a world-z up is degenerate looking along the line) | starting value |
| `atlantic_rake` | 21 | rake(world(0.35, u 0.55), 1.90, 30, +40, up z) | starting value: tilted frame, tune az / up for north up-frame |
| `label_end` | 22 start | (0.10, -1.55, 2.85) -> label centre (0.10, -0.054, 3.26) | label about 530 px wide (>= 430) |
| `whole_map` | 22 pull-out | (-0.45, -4.30, 2.55) -> (0.05, -0.05, 2.50), about 8 deg yaw | whole map, frame, sign edge and ledge |
| `ny_arrow` | 22 end | (-0.05, -1.30, 2.45) -> (0.07, -0.05, 2.60) | arrow head at N.Y. and the island |

Keep every camera south of the walls' south ends (u < 0.05) or above their tops (h > 0.55) when it is not inside the lane:
the walls are solid and the lens would pass through them. Inside the lane keep |a| < 0.08 measured from the LINE (`M.world(a, 0, h,
u=...)`), never from the chord: the lane is up to 0.154 D west of the chord. A camera that travels up the corridor (shot 20's launch)
must follow the line: lens at `M.world(a, 0, h, u=u_lens(t))` and look at `M.world(0, 0, look_h, u=u_lens(t) + 0.3..0.6)`; a straight
blend of two corridor setups cuts through the inside of the bend (east wall around u 0.3-0.7). From inside the lane the far end is
hidden round the bend until about u 0.3 (that is the corridor; the line visibly wanders, against the narration's 'straight north':
keep the white chalk curve, which bends right out to sea, in contrast where both show). Check a new camera with
`M.sight_margin(lens_lat, lens_sc, lens_h, tgt_lat, tgt_sc)` (D of clearance, < 0 = a wall hides the target).

## 5. Light, colour, cost

office_grey only (`OL.apply('office_grey')` after `M.build`). The walls read pale blue-grey with navy shade; in close views they take
most of the frame, so the blue share runs above the band (s19 hue row in `film/s19/QA.md`): a map-only special shot. The violet
share stays under 1 percent and magenta under 6 (the first lavender wall colour gave 30 percent magenta in the corridor; replaced).
Cost: 720x1280, 12 samples, 2 threads: about 23 s wall per frame with the machine loaded (load 6-8 from other workers).
