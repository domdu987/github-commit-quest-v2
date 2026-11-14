# Film 9: "ไอ้ช่างขนม" (sticky-rice mortar — Ming dynasty city wall, ~1370s)
PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj
Same style, pipeline and rules as film 8 (PROJ/film8/BRIEF.md incl. USER TASTE: wide/medium framings that show the beautiful dense set,
calm but always-moving camera, warm lit 3D world, sharp, NO depth of field, few/no text signs; reveals inside the lit 3D world).
Templates: set PROJ/v3/set3d8/desert.py (+API) and set3d6/set3d7; cast PROJ/v3/cast8; shots PROJ/v3/film8/common.py + film8/s01.
Narration PROJ/film9/audio/narration.wav (58.4 s), script PROJ/film9/script/script_th.txt, timing PROJ/film9/audio/timing.json.
## Story
Ming China, 600 years ago: the emperor orders a city wall finished before the enemy arrives. A mason (Lin) cooks sticky rice in a giant
cauldron and pours the rice soup into the lime mortar. The general in charge laughs: "Sticky rice? You're cooking dessert for the wall!";
the workers nickname him "ไอ้ช่างขนม" (the dessert mason). The general splits the wall in two sections: his section with plain mortar, the
mason's with rice mortar, slowed by cooking rice every day. Month 1 the general's section is 3 courses taller, month 2 six courses taller;
the general stands laughing on top of his wall. False payoff: the first rain comes and the rice mortar is still soft; the general shouts
"See? Dessert gets soggy in the rain!". The enemy army arrives and lines up cannons in front of both sections. Reveal: plain mortar is hard
but brittle — one hit and a whole slab cracks; the rice starch wraps around lime crystals into a sticky mesh (show as a lit 3D close-up
of the mortar between bricks: a glowing fine web around crystals that flexes and holds when a cannonball hits, vs. a brittle crack
spreading through the plain mortar), and the cannonballs only dent it. The mesh gets tighter with age; some rice walls still stand today.
Ending: the general's section — first shot cracks, second shot cracks the whole row, third shot it collapses, with the general (comic,
no injury: he slides down the rubble in a dust cloud, hat flying) still laughing on top.
## Locations
1. wall_site (Ming construction site by a river plain): a long grey-brick city wall under construction in two clearly different
   sections side by side, scaffolding of bamboo, ramps, piles of bricks, lime pits, a giant cooking cauldron on a fire with steam (rice
   soup), baskets, wooden carts, banners, workers' tents, distant mountains and pagoda; a gate tower at one end. Light presets DAY, DUSK,
   RAIN (overcast, wet sheen, rain streaks), BATTLE (smoky dusk, fires). Hooks: set_wall_height(section, courses) for both sections,
   set_cauldron_steam, set_rain, set_mortar_wet(k), set_cracks(section, level 0..1), set_collapse(t 0..1) for the general's section
   (bricks tumble, dust cloud), cannonball impacts (dent / crack decals), smoke.
   Presets: site_wide, cauldron, wall_top (on top of the general's section), two_sections (front view of both), cannon_line (enemy
   cannons in front of the wall), mortar_macro (macro of mortar between bricks for the reveal).
2. enemy_camp/cannons can be part of wall_site (field in front of the wall).
## Cast
lin (young mason, simple blue tunic, cloth headband, sleeves rolled; poses: stir cauldron with big paddle, pour rice soup into mortar,
lay bricks with trowel, calm confident, look up at rain worried, watch calmly as cannons fire), general (big, armour, plumed helmet,
long moustache; poses: laugh big, point & mock with lip-sync, stand arms akimbo on the wall laughing, shouting in rain, comic fall with
helmet flying), workers (2-3 laughing/pointing, carrying bricks), enemy gunners (2, simple, lighting cannon fuses), held props: paddle,
trowel, brick, bucket of rice soup, torch/linstock.
