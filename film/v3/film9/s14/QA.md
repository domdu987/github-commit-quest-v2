# QA, film 9 take s14 (shot 14, BATTLE: the enemy cannons), worker 4, round 3 (QA-tech round 2 fixes)
Frames g 1035..1158 (124 = 6 in-handle + shot 14 g 1041..1152 + 6 out-handle), 720x1280, 12 samples, 30 fps; take.mkv 41.4 MB (one file).

## QA-tech round 2 -> fixes
1. Army: two staggered ranks of enemy soldiers behind the gun row (~30 static cast9 gunner cards standing with upright linstocks / pikes,
   8 drawings incl. mirrored, a small breathing bob each), plus the 4 animated gun crews, banners, fire pots (set_army on every frame).
2. Both sections: set-up 1 is a high oblique wide from behind the army ((-12.8, -44, 9.6) -> (-11.6, -42.4, 9.0), 20 mm, slow track):
   Lin's creamy lower section left with blue banners, the general's taller grey section right with red banners, the gate tower; clear
   lanes behind every gun so a gun reads in front of each section. Camp-fire smoke columns near this camera hidden. (Camera placed by
   ray casts: the camp trees are one merged 'scenery' mesh.)
3. Set-up 2 widened: pulled back + up over the ranks behind gun 3 ((7.4, -37, 5.2), 18 mm): both sections, guns 2 and 3 with crews,
   foreground soldiers; fuse, duck, the shot (soft muzzle flash + soft smoke kept from round 2), the look eases up after the ball.
4. Shadows: dark soft shadow decals under every gunner, soldier, gun wheel (both wheels) and gun trail; crews' contact decals darker;
   the dust reduced to a light haze (0.22 -> 0.09).
5. Ball: the set's flying ball scaled 1.5x, with a fiery trail of 9 glowing orange puffs and a warm rim light (g 1143..1158).

## Checks (deliver.py -> work/qa.txt)
- Pops: g 1096 -> 1097 = the set-up cut; g 1111 -> 1112 (1.9) = the fuse sparks + light switching on. Near-still transitions: 0.
- Heads: no head below y 880 (ranks nearest the camera left out for this). Gun crew heads 28-53 px (wide framings now, per QA round 2).
- No mouths move (gunner_a closed frown). No DOF, no text, no black / magenta frames, no clipped sprites.
- Hue: red 44.6 / orange 35.0 / violet 5.6 / magenta 10.7, sat 0.32: warm BATTLE dusk; magenta from the set's pink-violet horizon sky.
- s/frame: 14.0 s wall / 25.7 s CPU (two processes, 2 threads).

## Differences from the plan
- The army is staged as static ranks (the set has no troops); one gun fires at g 1140 to lead into shot 15's hit.
- QA round 1 asked for >= 80 px gunner heads; round 2 asked for wide framings showing the army and both sections: the wide wins here.
