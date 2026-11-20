# set3d15/cast_test : real cast15 cards in the set3d15 scene

`python3 cast_test.py [final|preview] [s10 s20 s27 s28 s36]` (no argument = all five + `test.jpg` + `test_phone.jpg`; `python3 cast_test.py sheet` rebuilds only the sheets). Writes only here (`s*.png` 720x1280, `sprites/`, `test.jpg` 5 x full size with the y 880 line, `test_phone.jpg` 5 x 360x640 labelled). Optional `placement.json` overrides the CFG dict.
Set placeholders are never staged (`hide_placeholders()` removes any `actor_*`). No DOF, 12 samples, OIDN (set15.setup_render). Cost per still: **11-14 s wall, 22-28 s CPU** (2 threads; s27 slowest, 14.1 s), sprites cached in `sprites/`.

## put()
```python
put(tag, cast, pose, mark=(0,0,0), cam_loc=(0,0,0), ppd=128, scale=1.0, mirror=False, yaw_off=0.0, canvas=None,
    shadow=(1.4, 0.45), anchor=None, yaw_fixed=None, dz=0.0, shadow_at=None, shadow_a=0.8)
  -> dict(world=fn(local_anchor_xy) -> Vector (D), anchors, res, mk, yaw, scale)
```
- Scene units are **D** (0.54 m); cameras/marks in D, hooks that say metres are metres. (Film 14 multiplied by metres per D; here do NOT.)
- `cast15.pose_for(name, cast)` -> pose; `put` renders the sprite (`sprites.render_sprites`, import cast15 BEFORE sprites), makes a quad of the canvas rect (D, scaled by `scale`) with feet point at `mk`, emission-only material (colour + alpha, no lighting, `visible_shadow` off), rotated about Z only to face `cam_loc`.
- `mark`: feet point (standing poses). `anchor=('bar'|'head'|'apex'|'hip'|..., world_xyz)`: that sprite anchor lands exactly on the world point (yaw is iterated since it depends on the card position). Use anchors for flop / straddle / buried.
- `canvas`: standing default `CANVAS15[cast]`; lying/flop/straddle/buried/airborne need `cast15.CANVAS15_WIDE` (the coach buried also clips the default canvas: assert in put).
- contact shadow: dark-violet soft ellipse (L, W in D, scaled by `scale`) flat at z+0.03 D, never casts. `shadow_at=(x,y,z,L,W)` places it elsewhere (flop/straddle: on the foam top under the body); `shadow=None` off.
- `world(anchor)` converts any sprite anchor to world D, `screen(p)` to pixels (used for the printed JSON).

## Placement and cameras (all 22 mm, 720x1280, caption line y 880; all heads y < 720)
| still | scene | camera (metres) | placement |
|---|---|---|---|
| s10 | A GOLDEN | shot 10 start: loc (6.3,-0.4,1.5) look (10.4,2.6,1.55), FG clipboard from `SH.setup_shot(10)`, frame 489 | `coach` `coach_laugh` + `bob=laugh_bob(f0)` feet on `marks['coach_bleacher']` (19.26,4.82,0), shadow (1.9,0.6) D; head y 519, head top 475. `boy1` laugh at coach + 1.6 D along the view dir, 1.5 D right-of-view-left (feet (19.66,6.97)), `boy2` point_laugh at +1.2 / +1.5 (feet (21.11,4.31)); boys are 3.2 D (head tops y 464 / 446) |
| s20 | B EVE | own camera loc (-2.4,7.4,2.15) look (-1.8,11.4,2.05) (plan start is (-4.5,7.0,1.0)) | `dick_olympic` `stand`, feet (-3.0, 20.2, 0) D = in the bar's plane (bar y 21.48 D) 1.3 D in front, 0.5 D left of the standard region; head y 706, hair top y 647, bar underside about 600 px: bar sits ~0.4 D over the hair, 0.57 D over the 3.76 D head top |
| s27 | B TENSE | own camera loc (-0.20, 9.40, 2.00) m, look (-0.20, 11.60, 2.15) m, lens 22 mm (plan: (-1.0,7.1,1.6) look (0,11.6,2.4); at 4.6 m the arch was only 175 px = 24 %) | `dick_olympic` `flop`, `anchor=('bar', (0.12+0, 21.48, 4.333) moved 0.3 D toward the camera)`, i.e. the bar anchor (the line 0.13 D under the back) is on the crossbar height (bar centre z 2.34 m = 4.333 D) and the card is 0.3 D in front of the bar so the legs crossing the bar line hide it instead of being cut by it. `scale=1.0` (true size), `ppd=192`, `CANVAS15_WIDE`. Anchors on screen: apex (489,446), bar (453,564), head centre (542,706), foot_l (148,747), foot_r (193,869). **Arch = foot to head side about 500 px = 70 % of the width** (>= 50 %). Shadow: 2.6 x 0.9 D ellipse on the foam top (z 1.852 D) under the hip |
| s28 | B EVE | plan start of shot 28 via `SH.setup_shot(28)`: loc (-0.9,7.1,1.6) look (0,11.6,2.4) | `rival1` `straddle_a`, `anchor=('head', (0, 21.48, 4.333+1.9))`: head 1.9 D above the bar centre; body horizontal, leg up, lowest part (hanging hand) about 0.5 D above the bar, y 460-550 vs bar y 660; shadow 3.2 x 1.0 D on the foam |
| s36 | A GOLDEN | shot 36 start via `SH.setup_shot(36)`: loc (-0.8,3.4,0.6) look (-1.35,8.0,1.0), frame 2040 | `coach` `coach_buried`, feet on `marks['coach_end']` (-2.5,16.48,0.815) lowered `dz=-0.6` D so the card's mound base sinks into the set's sawdust heap (the heap hides the lower part; with dz 0 the card mound floated on top). `F.sawdust_spray(f0-9, (x,y,z+0.2 D), strength=1.7, seed=3)`: burst 9 frames (0.3 s) old at frame f0, so chips are mid-air around the head. Boys of the plan stand offscreen at the benches (x -9 D) and are not placed |

## Check numbers
Head top y: coach 475 (s10), dick 647 (s20), 604 (s27 flop, hanging), rival 460 (s28), coach 549 (s36): all < 880. Standing scale at card: coach 2.99 D, boys 3.2 D, dick 3.76 D (hair 4.05), rival 3.5 D: `Vector(mk)` + sprite height from `CANVAS15`; px check s20 dick feet 1083 / hair 647 = 436 px at a 0.5-1 D nearer camera plane.

## Gotchas for the render teams
- Units: scene = D. The sprite canvas rect is feet-relative (y down) in D; do not multiply by metres per D.
- Standing cards: `CANVAS15[cast]` is enough; **flop, straddle, buried (`coach_buried`), lie_*: use `CANVAS15_WIDE`** and place by anchor. The sprite `feet` is just the lowest sole there.
- `flop`: bar anchor is on the crossbar line, so put the card 0.2-0.3 D in front of the bar plane (toward the camera). Coplanar the round bar cuts the card; behind the bar the legs wrongly show the bar in front.
- The flop card is big at a close camera: head disc about 200 px at 2.2 m. At the plan camera (4.6 m) the arch is 24 % of the frame: to reach >= 50 % come to about 2.2 m (loc y 9.4 for the 11.6 bar) or scale the card (breaks the 3.76 D rule). Do this from y 9.4 with look slightly under the bar (z 2.15 m): head at y 706 stays above 880 and the foam fills the lower third.
- TENSE: the bar sits in the spot pool and blooms to white left of the arch (set look, not the card); the card stays unlit (emission) so the figure is brighter than the dark stand around it. EVE/GOLDEN cards are unlit too, so the key light does not shade them. Contact ellipses are the only grounding: for the flop and straddle put the shadow on the foam top (`shadow_at`).
- s20: bar 0.57 D over a 3.76 D head, hair tufts reach 4.05 D, so tufts are 0.28 D from the bar centre. A low camera (z 1.1-1.5 m) puts the tufts on the bar when Dick stands in the bar plane (parallax of the nearer figure). To read a gap: stand him ~1.3 D in front and use a camera at about head / bar height (2.15 m) as here. A camera far above the bar (2.7 m) shows too much foam and the bar leaves his head.
- Straddle: place by the head anchor; with `ppd=160` the card is sharp. The face-down reading comes from the face and hanging arms: it reads as a flat bar with one leg up even at 360 px.
- s36: the coach is small (head about 40 px at 360 wide, 7 m camera) and the set's own heap dwarfs the card mound; spray chips are thin (0.1 m) so they read as flecks. Raise `strength` 2+ or key the burst earlier for more. FG `sawdust_chips` are big boxes in the lower third: part of the plan.
- s10: the FG clipboard (red, plan prop 0.9 m from the lens) covers the bottom third; the coach is in the upper third (head y 519) at 2.99 D, boys behind him. `bob` moves the card, not its shadow: pass the same frame to `laugh_bob`.
- `F.build` wipes all objects: place cards after `build` and `setup_shot` (which makes the camera); `SH.setup_shot` keys the camera, so call `sc.frame_set(f0)` before reading screen positions. Hooks (spray) key on frames: `sawdust_spray(frame, ...)` object is at the burst start, the still is rendered `frame + 9`.
- Cards load PNGs with `alpha_mode STRAIGHT` and `extension CLIP`; edges look clean at 12 samples with OIDN (no halos seen).
