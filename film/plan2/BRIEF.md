# Film 2: "ไม้จิ้มฟ้า" (the sky-poker) — Brescia, Italy, 1769

PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj

A 67 s vertical (720x1280, 30 fps) Thai-narrated short in the style measured in PROJ/spec/LOOK_SPEC.md: flat unlit 2D puppet
characters (PROJ/v2/puppet, PROJ/v3/cast) standing on emission-only cards inside a real lit 3D Blender world (PROJ/v3/stage),
one hard key light, blue-violet shade, 22 mm restless camera. The bundled film (1938 weather office, PROJ/v3/set3d/office3d.py,
PROJ/v3/shots/film.py) is the worked example of everything: copy its structure, do not edit it.

Reference frames (the look to match): PROJ/ref/a/tNNNN.jpg (clip A: a medieval/oriental empire, castle exteriors, throne room,
night scenes in blue with moon and warm windows, golden sunset, painted backdrop plates of cities and hills behind real 3D
foreground) and PROJ/ref/b/tNNNN.jpg (clip B: desert railroad, saturated red rock, blue sky). Frame tNNNN is at (NNNN-1)*0.5 s.
Useful in A: t0010 throne room interior, t0030 jar insert, t0040 wide city plate with army, t0062 castle gate day,
t0072 sunset village, t0080 night village moonlight, t0096 night castle gate, t0104 explosion/rubble wide, t0112 top-down insert.

## Story (Thai narration already recorded: PROJ/audio/narration.wav, 65.0 s; phrase times PROJ/script/captions.json)
A small boy, the youngest bell-ringer of the church of San Nazaro in Brescia, nails an iron rod to the top of the bell tower.
The priest orders it pulled out. People believe ringing bells drives lightning away. Under the church the army stores ~90 tonnes
of gunpowder. The boy read that lightning likes to run down iron. Priest laughs; boy keeps nailing it back; the town nicknames
the rod "ไม้จิ้มฟ้า" (the sky-poker). A big storm comes, everyone rings, lightning flashes all night but never strikes; next
morning the priest hands the rod back, smug. One August night clouds gather again. Mechanism: lightning seeks the highest point;
a pointed rod wired to the ground sends it quietly into the earth; without one it finds its own way down through stone, wood,
and the wet bell rope. That night there is no rod. Lightning hits the top of the tower, runs down the wall into the vault, and the
whole bell tower lifts into the sky (one image: tower rising on a column of fire and smoke; no bodies, no casualties).
Ending image: the rod leaning beside the boy's bed, where he left it.

## Cast (new, our own designs; build with PROJ/v3/cast/cast_ext.py conventions, in a NEW extension module, never edit puppet.py)
- boy "nico": the hero. Smallest figure (about 0.8x the adults' height), white round head like all puppets, a short brown
  cap, oversized rust-orange tunic with a rope belt, bare dark legs. Default face: determined half-lid. Rarely speaks.
- priest "padre": tall and round, black cassock with a row of small red buttons, wide flat black round hat (saturno) drawn over
  the head, rosy cheeks, smug half-lid, laughs with closed eyes. Speaks the two quoted lines.
- townspeople: 3-4 extras recoloured from existing cast (aprons, shawls, a baker), for the square and the bell chamber.
- one soldier (blue coat, tricorn) can appear by the gunpowder barrels.

## Sets (each is one module under PROJ/v3/set3d2/, API like office3d.build(preset) -> anchors dict with marks and ready cameras)
1. tower.py — the church bell tower (campanile) of warm ochre/terracotta brick and stone with an OPEN bell chamber on top (four
   arched openings, one big bronze bell on a wooden headstock, ropes), a short pointed spire/cupola above it where the rod goes
   (anchor rod_tip / rod_base; rod object with set_rod(state) 0 = absent, 1 = nailed), a church facade beside it, a cobbled square
   at its foot with a few houses, and a painted backdrop plate ring of a hilly Italian town (roofs, other towers, cypresses, hills).
   Presets: DAY (hard sun 40-50 deg high), DUSK (golden low sun, like ref a t0072), NIGHT_STORM (no sun; cold blue moon key from
   behind clouds, bluish ambient, warm windows, and a flash light that can be keyed for lightning frames), NIGHT_CALM.
   Must offer cameras: low angle up the tower from the square, high angle down from the bell chamber to the square, bell chamber
   interior eye level (actors stand under the bell), spire close insert, wide town establishing.
2. vault.py — the low stone vault under the church: brick barrel vault, rows of stacked wooden gunpowder barrels with a stencil
   mark, a lantern (warm key, the only light), a stair from above, a crack line where fire will run. Presets: LANTERN, BURN
   (orange glow + light pulse for the disaster).
3. room.py — the boy's tiny attic bedroom: slanted wooden roof, small window with dawn light (hard key through the window),
   straw bed, the rod leaning beside it, a stool with a book. Presets: DAWN, NIGHT.

## Rules for every worker
- Read first: PROJ/v3/README.md, PROJ/v3/set3d/API.md + REVIEW.md, PROJ/v3/stage/API.md (sections 1-4, 10),
  PROJ/spec/LOOK_SPEC.md (skim; sections on light/colour/environment/camera), PROJ/spec/verify_blender_api.md, and look at the
  reference frames named above at full size.
- Blender is `import bpy` (bpy 5.3 module), Cycles CPU, NO Freestyle, NO EEVEE/Workbench. Max 2 render threads per process.
- Colour check: python3 PROJ/v3/tools/hue_report.py <frames>. Interior/day band: red 30-41, orange 22-38, blue 14-30, violet 0-5,
  magenta 0-10 percent of chroma; shade blue-violet (hue 240-260), never magenta; 8-15 percent of pixels darker than V 0.25.
  Night presets: blue-dominant is expected; still no magenta cast. Shade at 0.15-0.31 of lit on the same surface (day).
- Write ONLY in the folder(s) you own. No network, no MCP/connector tools, no paid APIs.
- Finish with: the module, API.md (functions, anchors, cameras, presets), stills of every camera x preset at 360x640 with
  placeholder actors where actors will stand (PROJ/v3/set3d/office3d.py placeholder_actor shows how), a contact sheet, the
  hue_report rows, and a short REVIEW.md of what still differs from the reference frames.
