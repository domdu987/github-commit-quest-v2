export const meta = {
  name: 'assets-beach-and-cast',
  description: 'Build and review the second 3D set (Long Island beach with drizzle, fog bank and wall of water) and the extra cast members for the full film',
  phases: [
    { title: 'Build', detail: 'beach set in 3D; extra cast for the puppet system', model: 'opus' },
    { title: 'Review', detail: 'independent reviewer measures against the reference and repairs', model: 'opus' },
  ],
}

// EXAMPLE FROM FILM 1: rewrite the prompt texts (story, shots, lanes, sets, cast, paths) before use; keep the shape.
// A Workflow tool script (see the workflow-authoring skill). Replace __PROJ__ with the project path.
// model: 'opus' is the one-tier-down worker tier; the main conversation runs on the strongest model.
// See references/production.md, section "Adapting to a new film".
const P = '__PROJ__'

const COMMON = [
  'PROJECT CONTEXT',
  'We are producing a 65 second vertical animated short (720x1280, 30 fps, Thai narration) that must look as close as possible to two reference clips. Full-resolution stills every 0.5 s: ' + P + '/ref/a/tSS.S.jpg (clip A, railroad: a real 3D world under a hard sun, flat unlit puppet characters) and ' + P + '/ref/b/tSS.S.jpg (clip B, dragon jar). Measured specifications (read-only): ' + P + '/spec/LOOK_SPEC.md (section 2 characters, 3.3 the exterior beach town recipe, 4 light and colour with presets, 5 camera), with corrections that WIN in ' + P + '/spec/verify_blender_api.md and ' + P + '/spec/verify_measurements.md; single-lens detail in color_light_post.md (+ lightkit_clp.py), environment_materials.md (section 3.5 beach recipe; the code-drawn beach style frame ' + P + '/spec/env_proto/beach_styleframe.png), camera_motion.md, character_anatomy.md, face_expressions.md.',
  'WHAT EXISTS AND WORKS (read before you build; copy its methods)',
  '- A reviewed 3D office set built in Blender from code: ' + P + '/v3/set3d/office3d.py, textures.py, API.md, REVIEW.md, stills still_*.png. It shows how this project builds a set: 1 Blender unit = 1 D (a character head diameter), real geometry with thickness, per-surface artwork rasterised from SVG by headless Chromium, emission-ambient plus one hard key light, inverted-hull ink on props, the calibration and the verify corrections already applied, tone targets, ready camera setups, a stills command and a timing command.',
  '- A reviewed staging system that puts the flat 2D puppets into a 3D scene as cards, drives the camera and renders: ' + P + '/v3/stage/ (API.md, REVIEW.md). The puppet system: ' + P + '/v2/puppet/puppet.py and API.md (figure(cast, pose, uid) returns an SVG group; CAST defines hero and boss).',
  '- The finished first 5 seconds, as proof of the look: ' + P + '/v3/out/proto_v3.mp4, contact_v3.jpg, aspects_v3.png and QA.md (final frames cost about 4.5-5 s each at 12 samples).',
  'THE STORY: September 1938. A young forecaster in the U.S. Weather Bureau draws a ruler-straight hurricane track pointing at New York; his boss rubs it out; next morning Long Island, New York, wakes to an ordinary grey drizzle; then the hurricane arrives: people on the beach see what looks like a fog bank, and it is a wall of water taller than a house. The film ends on a weather forecast sheet lying on a kitchen table that still says rain.',
  '',
  'COLOUR LESSON (the client says our colours are not yet like the reference; measured with python3 ' + P + '/v3/tools/hue_report.py <frames or stills>, which prints the share of chroma per hue family for the reference and for your images): the reference sits at red 25-40, orange 23-38, blue 14-29, violet 1-5, magenta 5-10 percent, with 8-15 percent of pixels darker than V 0.25. Our office came out magenta 25-28 and blue 9-11 with too few deep darks, because a violet ambient turned every shade magenta. So: shade must read blue-violet (hue 240-260), never magenta (hue 290-345); keep magenta under 10 percent and violet under 5; keep real deep darks. Run hue_report.py on your own stills and report its row.',
  'PIPELINE RULES (decided, do not revisit)',
  '- Blender 5.3.0 as a Python module (import bpy), headless, Cycles on CPU, 4 cores. No Freestyle, no EEVEE, no Workbench, no downloads, no AI generation. Deterministic direct light, low sample counts: a final 720x1280 frame must cost 6 s or less with the machine to itself (hard limit 9 s).',
  '- World convention: 1 unit = 1 D, Z up, ground z = 0 where actors stand, camera lens 22 mm on a 36 mm sensor (focal 782 px on a 720x1280 frame), view transform Standard, 30 fps.',
  '- Characters are flat unlit cards (never lit, never tinted) that cast real hard shadows.',
  'HARD RULES',
  '- Write files ONLY under the folder your task names. Everything else is read-only: import existing modules by path (sys.path.insert), never copy-edit them in place.',
  '- Do not call any MCP or connector tools. Do not publish anything. Do not touch the user\'s git repository.',
  '- Shared 4-core machine: other agents render at the same time. While iterating render small (360x640, low samples) with scene.render.threads_mode = "FIXED" and threads = 2. Measure the final-quality frame time once and say whether other jobs were running.',
  '- To look at an image use the Read tool (downscale to at most 1600 px first). Always LOOK at what you rendered next to the reference frames.',
  '- Your final message is consumed by a script: return the structured result only, with absolute paths.',
].join('\n')

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'string' } },
    api_summary: { type: 'string' },
    self_check: { type: 'string' },
    known_gaps: { type: 'array', items: { type: 'string' } },
  },
  required: ['files', 'api_summary', 'self_check', 'known_gaps'],
}

const BEACH_BUILD = COMMON + '\n\n' + [
  'YOUR TASK: build the 3D beach set  ' + P + '/v3/set3d_beach/beach3d.py  (write only under ' + P + '/v3/set3d_beach/ and ' + P + '/v3/tmp/beach/).',
  'Follow the clip A exterior treatment exactly (look at a/t09.0, a/t13.5, a/t16.0, a/t48.5, a/t53.0, a/t58.5): a real ground plane running to a horizon at 34-50 percent of the frame height, a gradient sky with soft un-inked clouds, hue shift with distance, saturated ground against blue, terrain, sea and sky WITHOUT ink, man-made objects WITH about 3 px ink (inverted hull), strong converging lines (a boardwalk, a row of telegraph poles, a fence, the surf line) that run to the vanishing point.',
  'Scene: a Long Island summer beach colony in 1938. Sand in the foreground where actors stand; a row of small wooden beach cottages on short stilts with shingle roofs receding along one side; a plank boardwalk or sandy road with telegraph poles and wires receding beside them; dune grass, a rope-and-post fence, a rowing boat pulled up on the sand, a striped beach umbrella, a lifeguard chair, a sign; the sea across the far half with a surf line and a clear horizon; 12-18 distinct objects plus ground scatter. Everything period-plain; any text in English.',
  'Public API (the animators rely on it exactly)',
  '1. build(preset="GREY_DRIZZLE", clear=True) builds everything into the current bpy scene and returns anchors. Presets, each a complete light and sky: "GREY_DRIZZLE" (an ordinary dull morning: flat grey-blue sky, soft low-contrast light, wet darker sand, no hard shadows or only faint ones, the world slightly desaturated but still in the film palette: this is the false-defeat scene, it must look harmless and boring), "STORM" (the arrival: dark slate sky, strong wind look, the sea dark with white streaks, a low hard side light breaking under the cloud so the cottages and the wave are edge-lit: dramatic), and "SUMMER_SUN" (a clip A style hard sun at 35-50 degrees with whole-figure cast shadows on the sand and plum shade; useful for a bright establishing variant).',
  '2. anchors (world units): beach_marks (three or more floor points where actors can stand, facing the sea or the camera), cottage positions and sizes (the nearest cottage about 3.5-4.5 D tall to the ridge, so a wave "taller than a house" has a yardstick), horizon direction, sea_dir, and cams: ready camera setups {loc, look_at, lens}: vista_high (like a/t58.5: high wide down the colony to the horizon), low_cottages (low angle looking up past an actor at the cottages and the sky behind them: where the wave will tower), eye_beach (eye-level group of people on the sand looking out to sea), sea_view (their point of view: sand, surf, open sea and horizon filling the frame), plus others you find strong.',
  '3. Animated elements, each with a setter that can insert keyframes (frame=None means set statically): set_fog_bank(amount 0..1, frame) (a low grey band on the horizon that reads as fog and grows), set_wave(progress 0..1, frame) (progress 0 = hidden behind the fog band; 1 = a wall of water with a foaming crest standing taller than the cottages, having advanced across the sea toward the shore; make it a real sculpted mesh or stacked cards that reads as ONE huge wave, stylised like the film, no ink, with a lighter crest and darker face), set_rain(amount 0..1, frame) (drizzle: thin sparse streak cards or particles-free animated planes near the camera; must render deterministically), set_sea(t seconds, frame) (slow drift of the surf line and sea texture so the sea is never frozen), set_wind(amount, frame) (umbrella, flags or grass lean).',
  '4. Command lines: "python3 beach3d.py stills" renders still_<preset>_<cam>.png for the main cameras in all three presets, plus a strip showing set_fog_bank and set_wave at 0, 0.33, 0.66, 1; "python3 beach3d.py timing" prints final-quality seconds per frame.',
  'Requirements',
  '- Reuse the office set modules for materials, ink, texture rasterising and render setup where possible (import them); follow LOOK_SPEC 3.3 and 4.2 with the verify corrections.',
  '- Tone targets for SUMMER_SUN follow the clip A exterior numbers in LOOK_SPEC 4.1; for GREY_DRIZZLE and STORM there is no reference scene, so keep the film palette (plum darks, no neutral grey, no pure black) and state the numbers you chose.',
  '- A final frame in 6 s or less (hard limit 9 s) with two actor cards in the scene, in every preset, including rain and wave.',
  '- Self-review loop, at least three passes: render the stills with two placeholder actor cards (use the stage system: see v3/stage/API.md), VIEW them next to the clip A exterior frames, list the five largest visible differences, fix, repeat. Write API.md.',
].join('\n')

const CAST_BUILD = COMMON + '\n\n' + [
  'YOUR TASK: extend the cast of the puppet system  ' + P + '/v3/cast/cast_ext.py  (write only under ' + P + '/v3/cast/ and ' + P + '/v3/tmp/cast/).',
  'Read fully first: ' + P + '/v2/puppet/API.md, puppet.py (how CAST, builds, hats, hair, costumes and faces are defined), REVIEW.md, and the character sections of LOOK_SPEC.md. Look at the reference characters (a/t02.0, a/t16.0, a/t27.0, a/t45.0, b/t03.0, b/t07.0, b/t42.0) and at our two existing ones in ' + P + '/v2/puppet/sheet.png: the new people must be the same species (same proportions, ink, head, limbs, face vocabulary) and clearly different individuals.',
  'Deliver a module that, when imported, registers these new cast members so that puppet.figure(name, pose, uid) and the stage system work with them unchanged (do not edit puppet.py; add entries and any new hat, hair, moustache, glasses or costume drawing code from your own module):',
  '- senior_a and senior_b: two older senior forecasters of the 1938 Weather Bureau (the "old hands" who all agree the storm will curve): regular and stout builds, for example one with round glasses and a fedora and a brown tweed waistcoat, one with a grey bowler, white walrus moustache and a burgundy cardigan; both must read apart from the boss (homburg, green pinstripe waistcoat) and from each other at a head size of 110 px.',
  '- clerk: one more young office junior (so "the whole building" can react): slim, a green eyeshade or a flat cap in another colour, sleeve garters.',
  '- beach_man, beach_woman, beach_kid: a Long Island family on the beach in 1938: a man in a straw boater and a striped one-piece bathing suit or rolled shirt-sleeves, a woman in a wide sun hat with a ribbon and a summer dress, a child at 0.6 scale with a sailor cap and a tin bucket prop. They must separate from sand (#d9b27a), sea blue-grey (#5d7fa3) and a grey sky (#9aa3b5).',
  '- Any new props the story needs in hands: bucket, folded newspaper or forecast sheet, coffee mug.',
  'Also deliver: "python3 cast_ext.py sheet" writes sheet.svg and sheet.png: every new member in front, three-quarter and near-profile views, four expressions each (neutral, smug or amused, worried, wide-eyed shocked) and three poses each (standing, pointing or looking out to sea with a hand shading the eyes, startled); "python3 cast_ext.py lineup" writes lineup.png: all eight cast members (hero, boss and the six new ones) side by side at the same scale on the office wall colour and on the sand colour, at a head size of 110 px and of 220 px.',
  'Quality bar: every number of LOOK_SPEC section 2 holds for the new members (run v2/puppet review or measure tools on them); costumes are fully drawn (5-7 elements each: collar, buttons, stripes, pockets and so on); own designs, no copies of the reference cast; animation-safe (reuse v2/puppet/test_puppet.py on the new names: no exception, no pops). Check the new members through the stage sprite renderer (' + P + '/v3/stage/sprites.py) for at least two poses each. Self-review loop, at least three passes with the sheet next to reference crops. Write API.md listing the names, their options and the new props.',
].join('\n')

const BEACH_REVIEW = COMMON + '\n\n' + [
  'YOUR TASK: independent review and repair of the 3D beach set at ' + P + '/v3/set3d_beach/ (beach3d.py, API.md, stills). You did not build it; assume it has flaws the builder could not see. Write only under ' + P + '/v3/set3d_beach/ and ' + P + '/v3/tmp/beach_review/.',
  'Step 1, look: render every main camera in all three presets at 720x1280 final quality with two actor cards from the stage system at the beach marks, and the fog and wave strips. Put them next to a/t09.0, a/t13.5, a/t16.0, a/t48.5, a/t53.0, a/t58.5 in review_compare.jpg and look hard. Does SUMMER_SUN read as clip A (horizon height, converging lines, hard whole-figure shadows on the ground, plum shade, saturated ground against blue, no ink on terrain)? Does GREY_DRIZZLE look like a harmless dull morning of the same film, not like another film? Does STORM look threatening? Is the wave ONE readable wall of water, clearly taller than the cottages at progress 1, and does the fog band at low progress really pass for fog? Is the sea alive (compare two frames 1 s apart)? Do white heads read against every sky?',
  'Step 2, measure with your own scripts on your renders and on the reference frames: horizon position, vanishing-point convergence, lit-to-shadow ratio and hue shift and whole-figure shadow length in SUMMER_SUN, tone statistics per preset (' + P + '/ref/crops/env/tools/metrics.py, ' + P + '/spec/measure_color.py), head fill and ink colour on screen, wave height against the cottage ridge in pixels along its progress, rain streak visibility, and the final-quality cost per frame for each preset with wave and rain on (6 s or less; cut cost if over).',
  'Step 3, contract: every anchor and camera is right (debug markers), every setter keyframes correctly and is deterministic (render the same frame twice, identical), build() is repeatable.',
  'Step 4, repair beach3d.py directly, keeping the API backward compatible; re-render, look again, re-measure; write REVIEW.md with tables and what remains.',
].join('\n')

const CAST_REVIEW = COMMON + '\n\n' + [
  'YOUR TASK: independent review and repair of the extended cast at ' + P + '/v3/cast/ (cast_ext.py, API.md, sheet.png, lineup.png). You did not build it; assume it has flaws. Write only under ' + P + '/v3/cast/ and ' + P + '/v3/tmp/cast_review/.',
  'Checks: (1) likeness to the reference species: crop reference figures and render the new members at the same head size on the same background, side by side in review_compare.jpg; measure outline widths, eye spacing, torso sizes, limb width, total height with the v2 puppet measuring tools against the LOOK_SPEC ranges. (2) Individuality: can all eight cast members be told apart in silhouette and in colour at a head size of 110 px, on the office wall colour and on sand; are the seniors clearly older than the hero and clerk; is anyone a copy of a reference character? (3) Robustness: run the v2 puppet test suite on every new name; sweep yaw, poses, expressions, hand targets far beyond reach; no exception, no NaN, no pops. (4) Stage integration: render each new member as a sprite through v3/stage/sprites.py and put two of them on cards in the stub room or the office set; colours arrive unchanged, feet on the floor, shadow attached. (5) Props attach to hands in every pose. Repair cast_ext.py directly (keep names and API), re-render sheet and lineup, and write REVIEW.md.',
].join('\n')

phase('Build')
const built = await pipeline(
  [
    { key: 'beach', build: BEACH_BUILD, review: BEACH_REVIEW },
    { key: 'cast', build: CAST_BUILD, review: CAST_REVIEW },
  ],
  (item) => agent(item.build, { label: 'build:' + item.key, phase: 'Build', schema: RESULT_SCHEMA, model: 'opus' }),
  (buildResult, item) => agent(
    item.review + '\n\nThe builder reported this (verify, do not trust):\n' + JSON.stringify(buildResult, null, 1).slice(0, 12000),
    { label: 'review:' + item.key, phase: 'Review', schema: RESULT_SCHEMA, model: 'opus' }
  ).then(r => ({ key: item.key, api: r.api_summary, self_check: r.self_check, known_gaps: r.known_gaps, files: r.files }))
)
return { components: built.filter(Boolean) }
