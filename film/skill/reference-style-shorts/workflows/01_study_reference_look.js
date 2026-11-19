export const meta = {
  name: 'study-reference-look',
  description: 'Measure the visual style of the two reference clips through six lenses and produce a Blender-implementable look spec',
  phases: [
    { title: 'Analyze', detail: 'six analysts, one lens each, measuring full-res reference frames' },
    { title: 'Synthesize', detail: 'merge findings into LOOK_SPEC.md with a ranked change list' },
    { title: 'Verify', detail: 'independent re-measurement and Blender 5.3 API check' },
  ],
}

// EXAMPLE FROM FILM 1: rewrite the prompt texts (story, shots, lanes, sets, cast, paths) before use; keep the shape.
// A Workflow tool script (see the workflow-authoring skill). Replace __PROJ__ with the project path.
// model: 'opus' is the one-tier-down worker tier; the main conversation runs on the strongest model.
// See references/production.md, section "Adapting to a new film".
const P = '__PROJ__'
const VID_A = '__UPLOADS__/0e17f4fd-Why_Perfect_Railroads_Dont_Work.mp4'
const VID_B = '__UPLOADS__/22ba206d-The_Ancient_Jar_That_Warned_an_Empire.mp4'

const COMMON = `
CONTEXT
We are recreating the visual style of two reference short videos for a NEW 65-second 9:16 clip (a 1938 weather-bureau story). The production tool agreed with the user is Blender 5.3 used as a Python module (import bpy), headless, CPU only (4 cores, Cycles; EEVEE is very slow here), with SVG drawn by code and rasterised by Chromium for any 2D artwork. There is no internet except PyPI and npm. A first attempt (v1) looks only about 50 percent like the reference. Your job is to study the reference through ONE lens and write a precise, MEASURED spec that a builder can implement without seeing the videos.

MATERIAL
- Reference frames, 720x1280 JPEG, one every 0.5 s, named by timestamp tSS.S.jpg from t00.0 to t64.5:
  clip A (Why Perfect Railroads Don't Work): ${P}/ref/a/
  clip B (The Ancient Jar That Warned an Empire): ${P}/ref/b/
- Source videos (30 fps), use ffmpeg if you need more frames or consecutive frames; write them to ${P}/ref/extra/<your-lens>/ :
  A: ${VID_A}
  B: ${VID_B}
- Our v1 attempt for comparison: ${P}/v1/v1_frame20.png , ${P}/v1/v1_frame45.png , code ${P}/v1/charlib_v1.py and ${P}/v1/scene_office_v1.py
- Useful frames. Clip A characters: t02.0 hero standing, t03.0 hero with train, t12.0-t13.0 workers on a beam, t14.0-t15.5 boss low angle, t16.0-t16.5 boss full body three-quarter, t17.0-t18.5 boss purple face with steam, t19.0-t20.5 two-shot, t23.0 foreman, t27.0-t28.0 tycoon with tea, t29.0-t30.0 sweating passenger, t31.0-t33.5 newspaper kid, t35.0 crowd, t37.0 hero by the gap, t44.0-t47.0 two-shot with smug boss, t53.0 tycoon under umbrella, t55.0-t56.0 hero wide eyes, t58.0-t59.0 hero on the track. Clip A environments and inserts: t04.0-t08.0 canyon and bridge, t09.0-t11.0 desert and station, t24.0-t26.0 construction, t34.0-t35.0 concourse, t36.0-t36.5 calendar insert, t38.0-t43.0 macro rail gap with caliper coin paper, t47.5-t52.5 rail POV with glowing rails, t60.0-t64.5 sunset bridge, snake rail, fireball.
  Clip B characters: t00.0 inventor with jar, t02.0 emperor and guards, t03.0-t04.5 inventor speaking, t06.0-t07.0 court laughing, t17.0 emperor on balcony, t18.0-t19.5 inventor by jar, t21.0-t22.0 and t24.0-t26.0 emperor on throne, t23.0 banquet, t27.0-t29.0 city gate, t33.0-t36.0 night scene, t37.0-t39.5 portcullis, t41.0-t43.0 guards on the wall, t44.0-t45.0 inventor walking. Clip B environments and inserts: t01.0 dragon close-up, t08.0-t13.0 orbit around the jar, t14.0-t16.0 army exterior, t20.0 goblet, t30.0-t32.0 sunset hill and camp, t47.0-t48.0 ruined palace, t49.0-t55.0 pendulum inside the jar, t56.0-t57.5 dragon jaw, t58.0-t60.0 mountain, t62.0-t64.5 underground cross-section.
- A burned-in caption word sits at roughly y 880 to 930 of 1280. Ignore it unless captions are your lens.

METHOD (mandatory)
1. Actually LOOK: open at least 14 frames across BOTH clips with the Read tool (it displays images). Crop and upscale regions with PIL to see fine detail, save crops under ${P}/ref/crops/<your-lens>/ and Read them.
2. MEASURE, do not eyeball: use numpy, PIL or cv2 (all installed) for pixel distances, ratios and colour samples (hex). Every number you report must cite the frame it came from.
3. Compare against v1 and say exactly what differs, ranked by visual impact.
4. Do NOT start Blender renders (other agents share the 4 CPUs). Tiny non-rendering bpy API checks are fine.
5. Only write inside ${P}/spec/ , ${P}/ref/crops/ , ${P}/ref/extra/ (and ${P}/fonts/ if you handle fonts).

OUTPUT
Write your spec as markdown to the file named in your task, with these sections: Observations (with frame citations), Measurements (table), How to reproduce (concrete values: sizes in head-diameter units, hex colours, pixel widths at 720x1280, angles, node or SVG recipes), Differences vs v1 (ranked). Then return the structured result. Be specific and honest; if something cannot be determined, say so.
`

const ANALYSIS_SCHEMA = {
  type: 'object',
  properties: {
    lens: { type: 'string' },
    spec_file: { type: 'string' },
    headline_findings: { type: 'array', items: { type: 'string' } },
    measurements: {
      type: 'array',
      items: {
        type: 'object',
        properties: { name: { type: 'string' }, value: { type: 'string' }, evidence_frame: { type: 'string' } },
        required: ['name', 'value'],
      },
    },
    differences_vs_v1_ranked: { type: 'array', items: { type: 'string' } },
    frames_viewed: { type: 'number' },
  },
  required: ['lens', 'spec_file', 'headline_findings', 'measurements', 'differences_vs_v1_ranked'],
}

const LENSES = [
  {
    key: 'character-anatomy',
    task: `LENS: character construction and anatomy. Write ${P}/spec/character_anatomy.md.
Determine exactly how the characters are built: head shape (circle or ellipse, aspect ratio), torso shape (measure its outline: egg, pear, bean; width and height in head diameters), neck or no neck, limb drawing (stroke width in px and in head diameters, straight or rubber-hose curves, where elbows and knees bend), hands, feet, hats (bowler, striped cap, top hat, emperor crown, helmets: geometry, how they sit on the head, how much of the head they cover), hair patches, costume details (buttons, lapels, chains, bandanas, suspenders: how they are drawn), outline width and colour (sample the hex: is it black or dark navy?), inner-detail line width versus silhouette line width. Describe how a character looks in front, three-quarter and profile views and how many distinct views appear, and whether they read as flat 2D artwork or as shaded 3D forms (cite evidence such as gradients and highlights). Catalogue the body poses seen (standing, crouching, leaning, walking, pointing, holding props) with frames. Give overall character height in head diameters, and typical on-screen size (head diameter in px and character height as a fraction of frame height) for close, medium and wide shots. Finish with a build recipe for BOTH options: (a) 3D meshes with toon shading and outlines in Blender, (b) a procedural 2D SVG puppet, with every dimension normalised to head diameter.`,
  },
  {
    key: 'face-expressions',
    task: `LENS: faces, expressions and head rendering. Write ${P}/spec/face_expressions.md.
Catalogue every distinct facial expression in both clips with frame citations (neutral, half-lidded, determined, angry, smug, laughing with tears, shocked wide-eyed, worried and sweating, asleep, shouting, grinning, and any others). For each one give SVG-ready geometry normalised to head diameter with the head centre as origin: eye shape and size, eye spacing, vertical position, eyelid or brow strokes with thickness and angle, pupil size where eyes are white-filled, mouth shape and size, teeth, moustaches, extra marks. Measure how far the features shift when the head turns to three-quarter view. Describe head shading precisely: sample the fill colour at the lit side, the centre and the shadow side (hex), describe where the soft shadow falls, any rim or highlight, and the same for hats. Catalogue the cartoon effects with geometry and colour: purple anger face, steam puffs, sweat drops, tears, sleep Z letters, speed or impact lines. Also describe blinking or mouth movement if visible between neighbouring frames (extract consecutive frames from the video to check). End with a list of at least ten expressions fully specified so a builder can write the SVG directly.`,
  },
  {
    key: 'color-light-post',
    task: `LENS: colour, lighting and post-processing. Write ${P}/spec/color_light_post.md.
Quantify the look with code: for at least 12 reference frames across both clips and for both v1 frames compute mean and percentile saturation and value (HSV), luminance contrast (p5 to p95), dominant palette by k-means (6 to 8 colours as hex with area share), and shadow versus lit colour for the same surface (sample pairs). Describe the lighting: key direction and softness, shadow colour (are shadows tinted?), ambient level, rim light, time-of-day treatments (noon, sunset, night, interior candle or lamp light), sky gradients, atmospheric haze with distance, glow or bloom on bright and emissive things, sharpness of near and far planes (report only: film 1's client chose a sharp picture with no depth-of-field blur), vignette, any film grain or sharpening, and overall colour grade. State how the 2D-looking characters are lit compared with the environment (do they receive scene shadows, do they cast shadows on the ground, how dark and how soft). Then give a concrete Blender 5.3 recipe to hit those numbers on CPU Cycles: view transform and look, exposure, world colour and strength, sun and area light colours, strengths and angles, material value ranges, and a compositor node chain (glare, colour balance, saturation, vignette) with parameter values; plus an equivalent ffmpeg filter chain as a fallback grade. Include a numeric target table (reference versus v1) that a reviewer can re-measure later.`,
  },
  {
    key: 'environment-materials',
    task: `LENS: environments, materials and set dressing. Write ${P}/spec/environment_materials.md.
Analyse how the worlds are built in clip A (canyon, railway, station, train interior) and clip B (throne room, city, hill, jar interior): which parts are true 3D geometry and which look like flat painted or illustrated layers, whether environment objects carry outlines (width and colour), how textures look (painterly, cel, photographic, procedural noise), level of geometric detail, prop density per shot (count props in several frames), colour blocking, scale of props relative to characters, how depth is staged (foreground, midground, background layers, haze), ground surfaces, skies, and how text-bearing props (signs, newspaper, calendar) are designed. Measure ratios where possible. Note differences between the two clips and decide which style is the better target for an interior office scene and for an exterior beach and sea scene. Then write concrete build recipes, using ONLY procedural shader nodes, simple meshes and SVG-to-PNG textures (no asset downloads): (1) a 1938 weather-bureau office (wall treatment, wood floor, wall map in a frame, desks, lamps, teletype machine, filing cabinets, barometer, coat stand, window with light), (2) a beach town with dunes, wooden houses, telegraph poles and sea. For each: geometry list, material recipe per surface (node types and values or SVG pattern description), palette in hex, prop count target, and how to add outlines to the environment if the reference has them.`,
  },
  {
    key: 'camera-motion',
    task: `LENS: camera, staging, motion and editing. Write ${P}/spec/camera_motion.md.
Extract consecutive frames at 30 fps from several segments of both videos (for example 3 seconds each from 6 to 8 different shots) into ${P}/ref/extra/camera-motion/ and analyse them with cv2 (optical flow, frame differences). Determine: apparent lens (wide or long; estimate horizontal field of view from perspective convergence where possible), camera height relative to character heads (low angle, eye level, high), framing rules (where heads sit vertically in the 9:16 frame, how much of the frame a character fills in close, medium and wide shots, where the action sits relative to the caption band), camera moves (push-in, pull-out, pan, tilt, orbit, fly-through) with speed estimates (percent scale change per second, pixels per second) and whether moves are linear or eased, how often the camera is fully static, transition types between shots (hard cut, dissolve length in frames, whip pan, morph) with counts, and shot durations. For character animation: is motion smooth at 30 fps or held on twos or threes, how much do characters move within a shot (idle bob, blinking, arm gestures, mouth movement synced to narration or not), is there motion blur. Then give a staging and animation recipe for Blender: focal length in mm for a 9:16 sensor, camera height and distance in head-diameter units for close, medium and wide shots, default move speeds, transition recipe, and character animation rules (what moves, how often, by how much) that would match the reference on a small budget.`,
  },
  {
    key: 'production-forensics',
    task: `LENS: production forensics. Write ${P}/spec/production_forensics.md.
Determine, as an unbiased investigator, how the reference clips were most likely produced: a real-time 3D engine, an offline 3D render, 2D character animation composited over 3D or painted backgrounds, AI video generation (text or image to video) possibly with character reference sheets, or a hybrid. The main session previously told the user they were real 3D renders and not AI; treat that as a claim to TEST, not to defend. Evidence to gather: (1) temporal stability of fine text and small details across consecutive 30 fps frames (extract runs of 20 to 30 consecutive frames around the newspaper, calendar, signs, chalk marks, buttons, hat stripes, and check whether glyphs or counts morph); (2) cross-shot consistency of a character's design details (button count, chain shape, hat stripe count, hair patch shape, costume colours) measured in several shots; (3) mirrored, garbled or nonsense text; (4) geometry that changes shape impossibly, objects appearing or merging, limb count errors, texture swimming; (5) shot length clustering and where transitions fall (regular multiples of a generation length?); (6) container and stream metadata from ffprobe (encoder tags, creation tool, bitrate, any watermark or logo regions); (7) how the camera moves and whether parallax is physically consistent; (8) audio is out of scope. Save your evidence crops under ${P}/ref/crops/production-forensics/. Give a verdict with a confidence percentage and the three strongest pieces of evidence for it and against it. Then state the practical implications: which properties of the look are easy to reproduce in Blender plus SVG, which are hard, and what the closest honest substitute is for each hard one. If AI generation is likely, say what kind of pipeline (for example image generation for consistent keyframes, then image-to-video) would reproduce it, without recommending anything you cannot support with evidence.`,
  },
]

phase('Analyze')
const analyses = (await parallel(LENSES.map(l => () =>
  agent(COMMON + '\n' + l.task, { label: 'analyze:' + l.key, phase: 'Analyze', schema: ANALYSIS_SCHEMA })
))).filter(Boolean)
log(analyses.length + ' of ' + LENSES.length + ' lens analyses returned')

phase('Synthesize')
const SYNTH_SCHEMA = {
  type: 'object',
  properties: {
    spec_file: { type: 'string' },
    production_method_verdict: { type: 'string' },
    recommended_character_approach: { type: 'string' },
    recommended_pipeline: { type: 'string' },
    prioritized_changes: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          rank: { type: 'number' },
          change: { type: 'string' },
          how: { type: 'string' },
          expected_gain: { type: 'string' },
        },
        required: ['rank', 'change', 'how'],
      },
    },
    contradictions_found: { type: 'array', items: { type: 'string' } },
    open_questions: { type: 'array', items: { type: 'string' } },
  },
  required: ['spec_file', 'production_method_verdict', 'recommended_character_approach', 'recommended_pipeline', 'prioritized_changes'],
}
const synth = await agent(`
You are the look-development lead. Six analysts studied two reference short videos through separate lenses and wrote specs in ${P}/spec/ : character_anatomy.md, face_expressions.md, color_light_post.md, environment_materials.md, camera_motion.md, production_forensics.md. Read ALL of them in full (some may be missing if an analyst failed; say so). Also look yourself at six to eight reference frames (${P}/ref/a/t46.5.jpg, ${P}/ref/a/t16.5.jpg, ${P}/ref/a/t19.5.jpg, ${P}/ref/a/t40.0.jpg, ${P}/ref/b/t24.5.jpg, ${P}/ref/b/t06.5.jpg, ${P}/ref/b/t33.5.jpg, ${P}/ref/b/t09.0.jpg) and at our v1 attempt (${P}/v1/v1_frame20.png, ${P}/v1/v1_frame45.png) so you can judge the analysts' claims rather than just copy them.

Write ${P}/spec/LOOK_SPEC.md : ONE self-contained build specification for reproducing this look with Blender 5.3 as a Python module (headless, CPU Cycles, 4 cores, no internet except PyPI and npm) plus code-drawn SVG rasterised by Chromium, at 720x1280. It must contain:
1. Production-method verdict in two or three sentences (from the forensics lens) and what it means for us.
2. The character system: a decision between 3D toon meshes, a procedural 2D SVG puppet placed in or composited over the 3D scene, or a hybrid, with reasons tied to evidence, then a full dimension table normalised to head diameter, outline widths in px, hex colours, costume detail rules, view handling (front, three-quarter, profile), and the expression list with geometry.
3. The environment system for an interior office and an exterior beach: construction approach, materials, palette, prop density, outlines.
4. Lighting, colour and post: the numeric targets table and the exact recipe.
5. Camera, staging, animation and transition rules.
6. A render-cost budget: target seconds per frame on 4 CPU cores and how the pipeline keeps a 65 second clip feasible (for example layered stills with 2D camera moves versus full 3D per-frame renders), with a recommendation.
7. A ranked list of the changes from v1 that will buy the most likeness, each with how to do it.
8. Contradictions between analysts and how you resolved them, and open questions.
Resolve disagreements by looking at the frames yourself. Do not start Blender renders. Do not edit the analysts' files. Return the structured result.`,
  { label: 'synthesize:look-spec', phase: 'Synthesize', schema: SYNTH_SCHEMA })

phase('Verify')
const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    notes_file: { type: 'string' },
    claims_checked: { type: 'number' },
    corrections: {
      type: 'array',
      items: {
        type: 'object',
        properties: { claim: { type: 'string' }, spec_value: { type: 'string' }, corrected_value: { type: 'string' }, evidence: { type: 'string' } },
        required: ['claim', 'corrected_value'],
      },
    },
    confirmed: { type: 'array', items: { type: 'string' } },
    blocking_problems: { type: 'array', items: { type: 'string' } },
  },
  required: ['notes_file', 'claims_checked', 'corrections'],
}
const verify = (await parallel([
  () => agent(`
You are an independent measurement auditor. Read ${P}/spec/LOOK_SPEC.md. Pick the 15 numeric or factual claims that matter most for visual likeness (character proportions, outline width and colour, face feature sizes, colour and contrast targets, caption-free framing sizes, production-method verdict). For each, RE-MEASURE it yourself from the reference frames in ${P}/ref/a/ and ${P}/ref/b/ (720x1280 JPEG every 0.5 s, named tSS.S.jpg) using numpy, PIL or cv2, on frames of your own choosing, not necessarily the ones cited. Default to distrust: a claim counts as confirmed only if your number is within about 15 percent or clearly the same category. For the production-method verdict, check the two strongest pieces of evidence by extracting consecutive frames from the source videos (${VID_A} and ${VID_B}) into ${P}/ref/extra/verify/ . Write ${P}/spec/verify_measurements.md with a table: claim, spec value, your value, frames used, verdict, corrected value. Do not edit LOOK_SPEC.md. Do not start Blender renders. Return the structured result.`,
    { label: 'verify:measurements', phase: 'Verify', schema: VERIFY_SCHEMA }),
  () => agent(`
You are a Blender 5.3 implementability auditor. Read ${P}/spec/LOOK_SPEC.md. The builders will use Blender 5.3 as a Python module (python3 -c "import bpy" works here; headless, CPU, Cycles available; Freestyle available; EEVEE and Workbench need a display and xvfb-run is installed but EEVEE is very slow). Blender 5 changed parts of the Python API (for example Action.fcurves no longer exists; World.use_nodes is deprecated). For EVERY concrete Blender instruction in the spec (render settings, colour management names, light properties, shader node type names and socket names, compositor node types and how the compositor node tree is created in 5.x, Freestyle line set and line style properties, curve bevel settings, image sequence textures, shadow catcher, film transparent, view layers and passes), write and run a tiny NON-RENDERING python script that performs the call and reports whether it works in bpy 5.3, and find the correct 5.3 equivalent when it does not. Also time ONE small test render to calibrate cost: a 720x1280 Cycles frame, 16 samples, denoise on, with a sphere, a plane, one sun, Freestyle on with a 6 px line; report seconds with and without Freestyle (keep this to at most three short renders, other work shares the CPUs). Write ${P}/spec/verify_blender_api.md listing each instruction, works or not, and the corrected snippet. Do not edit LOOK_SPEC.md. Return the structured result, with anything that would stop a builder listed in blocking_problems.`,
    { label: 'verify:blender-api', phase: 'Verify', schema: VERIFY_SCHEMA }),
])).filter(Boolean)

return { analyses, synth, verify }
