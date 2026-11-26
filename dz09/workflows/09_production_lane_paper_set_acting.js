export const meta = {
  name: 'produce-paper-kitchen-acting',
  description: 'Production lane 1 (Opus): shared paper artwork, then the kitchen set with shots 15 and 26; in parallel the new acting poses and cycles for the cast',
  phases: [
    { title: 'Paper', detail: 'forecast sheet, Thai label, calendar, newspaper, signs as textures', model: 'opus' },
    { title: 'Kitchen', detail: 'small 3D kitchen set and the two kitchen shots', model: 'opus' },
    { title: 'Acting', detail: 'talk, walk, whistle, laugh, shock, sleep, run cycles and poses', model: 'opus' },
  ],
}

const P = '__PROJ__'

const BASE = [
  'You are one worker on a 65 second animated film (720x1280, 30 fps, Thai narration) that must look like two reference clips (stills: ' + P + '/ref/a/ and ' + P + '/ref/b/). Read FIRST, in this order: ' + P + '/v3/film/CONVENTIONS.md (rules every worker follows), the rows of your shots in ' + P + '/plan/shot_plan.md (the verified shot plan; also its lists props_needed, inserts_needed and build order), and ' + P + '/v3/README.md (how the finished first 5 seconds were built; ' + P + '/v3/out/proto_v3.mp4 and contact_v3.jpg show the look to match).',
  'The story: September 1938, U.S. Weather Bureau. A young forecaster rules a straight red hurricane track on the wall map pointing at New York; his boss rubs it out; the office nicknames the line "ทางด่วนพายุ" (the storm expressway); the official forecast says rain; next morning Long Island wakes to drizzle; the storm then rides that straight line into New York; the last image is the forecast in a newspaper on a kitchen table that still says rain.',
  'Rules: Blender 5.3 as a Python module (import bpy), Cycles CPU, no Freestyle; artwork is drawn as SVG by Python and rasterised with headless Chromium through Playwright (require("playwright") works from any folder); Thai text only with fonts that are already on this machine (' + P + '/fonts/Kanit_900Black.ttf, Kanit_800ExtraBold.ttf, and ' + P + '/fonts/th/); no network, no MCP or connector tools, no paid API calls. To look at an image use the Read tool (downscale to at most 1600 px). Your final message is consumed by a script: return the structured result only, with absolute paths.',
].join('\n')

const SCHEMA = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'string' } },
    api_summary: { type: 'string' },
    self_check: { type: 'string' },
    known_gaps: { type: 'array', items: { type: 'string' } },
  },
  required: ['files', 'api_summary', 'self_check', 'known_gaps'],
}

const PAPER = BASE + '\n\n' + [
  'YOUR TASK (write only under ' + P + '/v3/paper/): the shared paper artwork of the film, build-order step 3 of the plan. Make every item the plan lists as paper or text artwork (read props_needed and inserts_needed and every shot row that names a readable prop): the official forecast sheet (teletype paper with a U.S. WEATHER BUREAU header and the forecast words "RAIN, GUSTY WINDS"), the hand-lettered Thai label that reads ทางด่วนพายุ (pinned on the map in shot 13 and seen again in shots 18, 22, 25), the tear-off calendar leaves (SEPTEMBER 20 and 21, 1938), the newspaper page with its weather box that repeats the forecast words (kitchen shots 15 and 26: the same words and layout family as the forecast sheet, because shot 14 dissolves paper to paper into shot 15), the speed sign of the mechanism, the rubber stamp impression, pictograms, compass rose, and any other text card the plan names. English for American office and newspaper text, Thai only where the plan says Thai.',
  'Style: the measured text-prop style of the reference (LOOK_SPEC 3.4 and environment_materials.md 1.7 and 3.7: cream paper #fff5df, brown-grey ink #836d4e, one or two large bold slab or fat-face lines, a ruled frame, small text as illegible filler lines), the same hand as the office set artwork (' + P + '/v2/sets/office.py draws the existing sign, calendar and map; reuse its helpers by import). Every item as a function that returns SVG and as a rasterised PNG texture at a resolution good for a close insert (at least 1500 px on the long side), plus any animated variants the plan asks for as numbered frames (for example the newspaper ink bleed).',
  'Deliver: ' + P + '/v3/paper/paper.py (one function per item, a registry dict name -> {svg function, png path, size in D units as it should appear in the scene}), the PNGs in v3/paper/tex/, a contact sheet v3/paper/sheet.jpg of all items next to the reference text props (a/t32.0 newspaper, a/t40.0 calendar, a/t27.5) and API.md. Check Thai shaping (tone marks) on a crop at full size. Self-review twice against the reference text props.',
].join('\n')

const KITCHEN = BASE + '\n\n' + [
  'YOUR TASK (write only under ' + P + '/v3/set3d_kitchen/ and ' + P + '/v3/film/s15/ and ' + P + '/v3/film/s26/): build the small kitchen set and deliver shots 15 and 26 of the plan as finished takes.',
  'Set: build-order step 10 of the plan and its "kitchen" entry under sets_needed: a table corner by a four-pane window in a Long Island cottage, 1938, built the way the office was built (' + P + '/v3/set3d/office3d.py, textures.py, API.md, REVIEW.md: import its material, ink, texture and render helpers), with the newspaper from ' + P + '/v3/paper/ (use its registry; the weather box must be readable in the close framing), a coffee cup and saucer, a chair, and what the plan lists. Two lights: kitchen_grey (the dull drizzle morning of shot 15) and kitchen_storm (shot 26: dark, the window filled by the wall of water, lightning). The window view sequences the plan names (drizzle loop, the wave) may be drawn as animated textures on a card behind the panes. Only what the one planned camera sees needs building.',
  'Colour: follow the colour section of CONVENTIONS.md (warm red-brown and orange woods, blue-violet shade, real deep darks, no magenta cast); these two shots are special-light scenes, so report the hue_report rows and explain them.',
  'Shots: follow the plan rows of shots 15 and 26 for camera, timing on the narration clock, the hand that sets the cup down (beach_man is in ' + P + '/v3/cast/: import cast_ext; only his arm and hand enter the frame), the ripple, the creeping cup, and the last frame of the film (hold it readable: the forecast words under the last caption). Approve the last frame of the film as a still before animating. Deliver both takes exactly as CONVENTIONS.md says (frames with handles, meta.json, cues.json, contact.jpg, QA.md). A final frame should cost 6 s or less.',
].join('\n')

const ACTING = BASE + '\n\n' + [
  'YOUR TASK (write only under ' + P + '/v3/acting/): the new poses and cycles of build-order step 5 of the plan, as a library the shot animators will import. The puppet API is ' + P + '/v2/puppet/API.md (pose dicts, presets, expressions, lerp_pose, hand targets); the cast is ' + P + '/v3/cast/API.md (hero, boss, senior_a, senior_b, beach_man, beach_woman); the acting helpers used in the hook are in ' + P + '/v2/shots/anim.py and ' + P + '/v3/shots/film.py (blinks as three one-frame drawings, expression swaps on the closed frame, eased holds). The measured animation grammar is LOOK_SPEC 5.5 and camera_motion.md (bodies move on ones with eased interpolation, faces swap whole drawings, mouth drawings change every 2-6 frames on the speaker only, head rolls 10-20 degrees on a phrase accent, walk cycle head bob 0.47 D with period 0.68 s and sway 0.13 D).',
  'Deliver ' + P + '/v3/acting/acting.py with pure functions of time (seconds or frame) that return puppet pose dicts, each documented with its inputs: for the boss: talk(t, loudness) mouth cycle driven by a loudness envelope (provide a helper that reads the narration WAV ' + P + '/audio/th/full_v2/narration.wav between two times and returns a per-frame loudness list), near-profile walk cycle, held whistle mouth with a strolling body, doubled-over laugh, shocked; for the hero: slumped, sad, stunned, redraw-with-ruler arm cycle; for the two seniors: nodding, laughing as a held drawing with a bouncing body; for beach_man: reclining asleep side-on in a deck chair with the hat over the eyes and a slow chest rise, stretch, palm out feeling for rain, shrug, shading the eyes; for beach_man and beach_woman: holding the hat brim, shocked, jump and run cycle; plus anything else the acting columns of the plan rows ask for that the puppet does not have yet (read every row). Where the puppet lacks a drawing (for example a whistle mouth or a talk mouth set), add it from your module without editing puppet.py, the way cast_ext.py extends it.',
  'Prove it: for every function a strip of 12 frames rendered through the puppet to PNG (acting/strips/<name>.png), one sheet acting/sheet.jpg of all strips, a continuity test (no pops between consecutive frames beyond the intended face swaps), and two of the cycles rendered through the 3D stage sprite path (' + P + '/v3/stage/sprites.py) to confirm they survive it. View the strips next to reference frames with the same kind of acting (a/t46.5 laughing boss, a/t16.0, b/t05.0 shocked, b/t07.0 laughing guards) and fix what looks stiff. Write API.md.',
].join('\n')

const lanes = await parallel([
  async () => {
    const paper = await agent(PAPER, { label: 'paper:artwork', phase: 'Paper', schema: SCHEMA, model: 'opus' })
    const kitchen = await agent(KITCHEN + '\n\nThe paper worker reported (verify, do not trust):\n' + JSON.stringify(paper, null, 1).slice(0, 8000), { label: 'kitchen:set-and-shots-15-26', phase: 'Kitchen', schema: SCHEMA, model: 'opus' })
    return { paper, kitchen }
  },
  async () => {
    const acting = await agent(ACTING, { label: 'acting:poses-and-cycles', phase: 'Acting', schema: SCHEMA, model: 'opus' })
    return { acting }
  },
])
return lanes
