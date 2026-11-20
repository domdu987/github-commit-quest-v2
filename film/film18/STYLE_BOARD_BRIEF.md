# Film 18 style board brief (builder: Sonnet; one round with the client)
Film: "ไอ้เสมียนวัว" — Tian Dan's fire oxen at Jimo, Qi vs Yan, 279 BC (Warring States China). Script: film/film18/script/script_th.txt, facts film/film18/FACTS.md.

## Goal
3 quick stills (720x1280, Cycles, 12 samples, NO depth of field, sharp) that show the client the LOOK of the NEW set before it is built in full:
palette, detail level, the key night light preset. Not the final set; but build it in the module that will grow into it:
`film/v3/set3d18/jimo.py` (+ `jimo_tex.py` for painted textures). Output: `film/v3/set3d18/board/board_1.png..board_3.png` and
`film/v3/set3d18/board/style_board.jpg` (the 3 side by side, labelled under each image, cyan line at y 880 on each tile).

## Reuse helpers, never the old set
New set every film: do NOT build/render film 9's wall (set3d9/wall.py) or any older location. You MAY import helpers exactly the way
v3/set3d10/harbour.py does (tower.make_camera/render/mat_lit/mat_emit/setup_grade, mine.obox/rod/lumpy, desert.set_flames/_flame_light,
bakery._halo, wall._air_comp/_billows ...). Read v3/set3d10/API.md and the top of v3/set3d10/harbour.py and v3/set3d9/wall.py first.
Skill references: film/skill/reference-style-shorts/references/bible/sets.md (sections 8-9), colour-light.md (palette, night/fire presets), camera.md.
bpy 5.3 is installed (python3 -c "import bpy"). 4 cores: render with threads 4, one render at a time.

## The three stills
1. **jimo_wall_night** (establishing, from outside, low-ish wide): Jimo city at night. A tall Warring-States RAMMED-EARTH wall (tamped
   layers visible as horizontal bands, warm ochre/sienna earth, battered slope, crenellated parapet of timber/earth), a two-storey timber
   GATE TOWER with dark tiled hip roof and up-turned eaves, red-lacquered posts, round paper lanterns and torches on the wall walk
   (warm practical emitters with small halo), banners (plain shapes, NO text). Big pale-gold moon low in a deep blue-violet night sky with
   a few stars and thin cloud bands; distant roofs of the city peeking above the wall. Foreground: dark grass, a cart wheel or rocks within
   the nearest 15 % of the frame. Ground: packed earth road to the gate, a moat or ditch with smooth layered water reflecting torches.
2. **yan_camp_night** (eye level inside the Yan camp, looking toward the distant wall): rows of canvas/hide tents (tan, ox-blood red trims),
   3-4 campfires with crisp cartoon flames and warm pools of light on the ground, black-and-red Yan pennants (no text), spear racks,
   a war chariot, drums, wine jars and cups on a low table (for the general's toast), a wooden palisade, horses or bundles of fodder.
   Far behind: the lit wall of Jimo with its tiny torches on the horizon under the moon. Dense: 20+ distinct objects in view.
3. **wall_holes_oxen** (key moment test): close-medium of the wall base at night from the inside: a few holes cut through the rammed earth,
   and ONE placeholder ox (simple chunky low-poly ox OR flat card) dressed in red silk with gold five-colour dragon patterns, short blades
   on the horns, a bundle of reeds on the tail with a bright flame (emitter, bloom) lighting the earth wall orange. Tests the fire light
   against the blue night.

## Look rules (client, hard)
- Sharp picture, no DOF, no blur; wide, dense, beautiful lit 3D world; no text anywhere; period-correct, pleasing colours, not harsh black.
- Night = deep blue-violet shade (shade hue 240-260) against WARM fire/lantern light (orange/gold): complementary, readable, not murky.
  Frame brightness: don't go too dark — middle band luma 70-130 on 0-255; dark (V<0.25) share under about 35 %.
- Props have thickness and the 3 px inverted-hull ink like earlier sets; never ink sky, water, fog, grass.
- Water smooth and layered (reflections, glints), not flat triangles.
- Caption band y 880-950 kept free of important detail.
- Measure each still with v3/tools/hue_report.py and print the shade hue (like set3d10/harbour_hue.py); put the numbers in board/NOTES.md.

## Done = the 3 PNGs + style_board.jpg + NOTES.md (numbers, render times, what each still tests) + jimo.py runnable as
`python3 jimo.py board` to rebuild. Commit nothing; the director commits. Report paths and numbers.
