# QA, film 9 take s14 (shot 14, BATTLE: the enemy cannons), worker 4
Frames g 1035..1158 (124 = 6 in-handle + shot 14 g 1041..1152 + 6 out-handle), 720x1280, 12 samples, 30 fps; take.mkv 41.2 MB (one file).

## What is on screen
- Set-up 1 (g 1035..1096, "แล้วทัพศัตรูก็มาถึง ลากปืนใหญ่มา"): wall_site cannon_line build, BATTLE; custom wide behind the cannon row
  (moved in from the preset so the gunners read: heads 45-56 px instead of ~30), slow track right + crane up: bronze guns with fire pots in
  a diagonal toward both sections, black banners, gate tower, smoke columns. Gunner_a (gun 2) and gunner_b (gun 3) hold smouldering
  linstocks, then crouch toward the touch holes (g 1078..1098).
- Set-up 2 (g 1097..1158, "เรียงหน้ากำแพงทั้งสองช่วง"): low medium behind-right of gun 3 (aimed at the general's section): gunner_b brings
  the match to the touch hole (g 1100..1112), fuse sparks + flickering light (g 1112..1139), both gunners duck and cover their ears
  (g 1126..1137), gun 3 FIRES at g 1140 (set_impact general slot 0: muzzle flash, smoke, camera shake); the ball and its smoke trail fly
  toward the wall in the handle. Cut to s15 (the ball hits the plain mortar).

## Checks (deliver.py -> work/qa.txt)
- Pops: only g 1096 -> 1097 = the set-up cut (29.8). Near-still transitions: 0 (median change 1.67).
- Heads: gunner_a w 52..75 px, gunner_b w 45..108 px; all heads above y 880 (lowest centre 782). Set-up 2 main head (gb) centre 0.54-0.59 H.
  Set-up 1 is a wide (exempt). gunner_a sits at the left edge in set-up 2 (secondary, head inside frame).
- Sprite clipping: the linstock / smoke wisp clipped the default canvas on g 1088-1091 and 1097-1100; fixed with a wider canvas
  (-2.5, -5.25, 2.5, 0.125) and those 8 frames re-rendered (no visible step: frame change 1.8-3.0 around them).
- No mouths move (static expressions). No DOF, no text, no black / magenta frames.
- Hue: red 34.8 / orange 31.5 / blue 15.8 / violet 7.2 / magenta 7.1, sat 0.34: warm BATTLE dusk vs blue sky; magenta from the
  set's pink-violet BATTLE horizon (set design), below the set's own per-frame max.
- s/frame: 13.7 s wall / 26.0 s CPU (2 threads, two processes): wide 13.8 / 25.4, medium 13.7 / 26.5.

## Differences from the plan
- "Enemy army arrives" is told by the cannon line itself (no marching troops: the set has none) plus the gunners readying.
- Shot 14 has an internal set-up cut (wide -> medium) at g 1097 for the 1.2-1.6 s framing-change rule and to show the fuse lighting.
- One gun fires at the end (g 1140) to lead into the macro hit of shot 15.
