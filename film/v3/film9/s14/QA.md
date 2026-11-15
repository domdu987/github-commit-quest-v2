# QA, film 9 take s14 (shot 14, BATTLE: the enemy cannons), worker 4, round 2 (QA-tech round 1 fixes)
Frames g 1035..1158 (124 = 6 in-handle + shot 14 g 1041..1152 + 6 out-handle), 720x1280, 12 samples, 30 fps; take.mkv 40.9 MB (one file).

## QA-tech round 1 -> fixes
1. Army / framing / gunner size: set-up 1 is now a wide cannon_line view (camera (-23, -30.5, 3.3), 20 mm, slow track right + crane):
   the gun row with fire pots runs in front of BOTH sections and the gate, set_army on every frame; 4 gunners (gunner_a x2, gunner_b x2
   at guns 0-3), the foreground one at the hero gun 0 with head 78-88 px; dust round all crews' feet (cast9 'dust' 0.45 -> 0.18).
   One set smoke column (behind gun 0) is hidden in this set-up because it covered Lin's section.
2. Blast: the set's muzzle smoke, flash ball and 9-puff ball trail (the "opaque white cylinder") are hidden every frame; replaced by a
   bright soft muzzle flash + core AT the barrel mouth with a 6000 W flash light (g 1140..1145) and 12 soft translucent smoke billows
   that start at the muzzle, roll forward / up and thin out (fire-lit at first).  The set's dark iron ball (r 0.75) flies at the
   general's section (slower: t +1/75 per frame) and the camera's look eases up after it (g 1143..1158): the ball reads against the
   lit wall through the cut.
3. gunner_a: closed frown under the moustache (mouth 'frown', expr 'determined'; ducking: squeezed eyes + frown).
4. Contact shadows: darker, larger contact decals under every gunner (1.5 x 0.62 D, #100c16 at 0.82).

## Checks (deliver.py -> work/qa.txt)
- Pops: only g 1096 -> 1097 = the set-up cut. Near-still transitions: 0 (median change 2.17).
- Heads (centre px, 720x1280): ga0 w 78-88, y 758-835; gb1 w 45-48; ga w 33-77; gb w 29-116, y 688-774. No head below y 880.
  Set-up 2 main head (gb) centre 0.54-0.60 H; after the shot the camera follows the ball and the gunners move toward the left edge.
- Sprites: no clipping (wide canvas (-2.5, -5.25, 2.5, 0.125)). No mouths move. No DOF, no text, no black / magenta frames.
- Hue: red 32.0 / orange 29.1 / blue 22.3 / violet 6.3 / magenta 6.9, sat 0.35 (BATTLE dusk; magenta from the set's pink-violet horizon).
- s/frame: 14.5 s wall / 24.7 s CPU (two processes, 2 threads).
- Note: a full-disk incident (a 27 GB temp pack from a failed git fetch) stopped the first final at 48 frames; those frames were
  verified intact (all decode, json present) and the rest rendered with the same code.

## Differences from the plan
- "Enemy army arrives" = the cannon line, banners, 4 crews in fresh dust (the set has no marching troops).
- An internal set-up cut (wide -> medium) at g 1097; one gun fires at g 1140 to lead into shot 15's hit.
