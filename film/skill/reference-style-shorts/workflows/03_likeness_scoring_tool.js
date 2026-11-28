export const meta = {
  name: 'likeness-harness',
  description: 'Build a repeatable scoring tool that measures how close a clip is to the two reference clips, then adversarially validate it',
  phases: [
    { title: 'Build', detail: 'one scoring command wrapping the analysts measurement code' },
    { title: 'Validate', detail: 'skeptic checks it separates reference from v1 and cannot be gamed' },
  ],
}

// EXAMPLE FROM FILM 1: rewrite the prompt texts (story, shots, lanes, sets, cast, paths) before use; keep the shape.
// A Workflow tool script (see the workflow-authoring skill). Replace __PROJ__ with the project path.
// model: 'opus' is the one-tier-down worker tier; the main conversation runs on the strongest model.
// See references/production.md, section "Adapting to a new film".
const P = '__PROJ__'
const VID_A = '__UPLOADS__/0e17f4fd-Why_Perfect_Railroads_Dont_Work.mp4'
const VID_B = '__UPLOADS__/22ba206d-The_Ancient_Jar_That_Warned_an_Empire.mp4'

const CONTEXT = [
  'CONTEXT',
  'We are making a vertical animated short (720x1280, 30 fps) that must look as close as possible to two reference clips: ' + VID_A + ' (clip A) and ' + VID_B + ' (clip B). Stills every 0.5 s are in ' + P + '/ref/a/ and ' + P + '/ref/b/ (file tSS.S.jpg is video frame 30 x SS.S + 6).',
  'A team measured the reference look. The reconciled specification is ' + P + '/spec/LOOK_SPEC.md (sections 2.2-2.4 character numbers, 3.5 and 4.1 acceptance checks and numeric targets, 5 camera, staging, animation and transitions) with independent corrections in ' + P + '/spec/verify_measurements.md (the corrections win). Single-lens specs: ' + P + '/spec/character_anatomy.md, face_expressions.md, color_light_post.md, environment_materials.md, camera_motion.md, captions.md, production_forensics.md.',
  'Measurement code written by that team, reuse it rather than re-deriving: ' + P + '/spec/measure_color.py, ' + P + '/ref/crops/env/tools/ (metrics.py and others), ' + P + '/ref/extra/camera-motion/ (scripts for global motion, beats, easing, shot definitions; look for .py and .npy files), and the tool folders under ' + P + '/ref/crops/ (face, anatomy, color, captions, production-forensics). Our rejected first attempt v1 (a lit 3D render): ' + P + '/v1/v1_frame20.png and v1_frame45.png, plus about 50 frames in ' + P + '/render/office/ if present.',
  'A new 5 s prototype is being rendered right now by another agent into ' + P + '/v2/out/ (frames f_0001.png ... and proto_v2.mp4). It may not exist yet; do not wait for it and do not touch that folder.',
  '',
  'HARD RULES',
  '- Write files ONLY under ' + P + '/v2/eval/ . Everything else is read-only.',
  '- Python 3 with numpy, Pillow, cv2 (already installed) and ffmpeg. No downloads, no pip installs, no Blender, no MCP or connector tools, no publishing, do not touch the user\'s git repository.',
  '- Shared 4-core machine with another job rendering: at most 2 threads (ffmpeg -threads 2, cv2.setNumThreads(2)), no parallel process pools.',
  '- To look at an image use the Read tool on a PNG or JPG (downscale to at most 1600 px first).',
  '- Your final message is consumed by a script: return the structured result only, with absolute paths.',
].join('\n')

const SCHEMA = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'string' } },
    usage: { type: 'string', description: 'exact command lines and what each output file contains' },
    scores: { type: 'string', description: 'table of group scores and overall index for clip A, clip B and v1 (and the v2 prototype if it existed)' },
    limits: { type: 'array', items: { type: 'string' }, description: 'what the tool cannot measure or measures unreliably' },
  },
  required: ['files', 'usage', 'scores', 'limits'],
}

phase('Build')
const built = await agent(CONTEXT + '\n\n' + [
  'YOUR TASK: build the likeness scoring tool  ' + P + '/v2/eval/score.py',
  'Usage: python3 score.py INPUT --out DIR [--label NAME], where INPUT is an MP4 or a folder of frames (f_0001.png ... at 30 fps) or a single still. It writes DIR/scorecard.json, DIR/scorecard.md (a readable table: metric, our value, reference range, score, verdict) and DIR/report.jpg (a visual sheet: sampled frames, detected heads with measured outline, detected cuts and reframings on a timeline, caption boxes). It must finish in under 4 minutes for a 65 s clip and under 1 minute for a 5 s clip.',
  '',
  'Metric groups (mask the caption band y 850-960 for picture statistics, as the specs do)',
  '1. Colour and tone: mean saturation, luma p50, black point (luma p1), contrast p95 - p5, colourfulness, share of pixels with S > 0.5, hue of the darkest tenth, share of V > 0.95.',
  '2. Density and light structure: Canny edge density (60/140), share of featureless 40 px blocks, mean luminance of the top, middle and bottom thirds, thin-dark-line share.',
  '3. Characters (detect heads automatically: large near-circular near-white blobs ringed by dark plum ink): head fill colour and its flatness (luma spread), ink colour, outline width as a fraction of head diameter on the thin side and on the thick side, head diameter per shot class, head centre height, whole head above y = 880, limb stroke width where measurable. Report how many heads were found; never score a group on zero detections, mark it "not measured".',
  '4. Camera and edit (videos and frame folders only): per-frame global motion (zoom rate in percent per second and pan in px per second), share of static frames, longest static hold, interval between framing changes (transitions plus in-shot snap reframings), number of shots, transition types (hard cut, dissolve and its length in frames), peak-to-mean speed ratio of snap moves (easing).',
  '5. Animation life (videos and frame folders only, best effort): blink count per second on detected heads, face-drawing change rate, share of frames in which a character region changes while the camera is steady.',
  '6. Captions: horizontal centre, vertical centre (target about 900-903), fill colour, stroke width, cap height, words per caption (OCR is not available, so estimate from the width of the white text mask), caption duration in frames, hard swap versus animated scale.',
  '',
  'Scoring',
  '- Each metric gets a reference range taken from LOOK_SPEC.md and verify_measurements.md (quote the source section in the table), and a score from 0 to 1: 1 inside the range, falling linearly to 0 at a stated distance outside it. Where clip A and clip B differ, the range spans both and the table also shows each clip value.',
  '- Group score = mean of its measured metrics. Overall index = weighted mean: characters 0.30, colour and tone 0.15, density and light structure 0.15, camera and edit 0.20, animation life 0.10, captions 0.10 (re-normalise over the groups that were measured and say which were not).',
  '- Print plainly in scorecard.md that the index only covers measurable properties and is not a perceptual similarity score.',
  '',
  'Calibrate and prove it',
  '- Run it on clip A, on clip B, on the two v1 stills and on the v1 frame folder if it exists. Both reference clips must score high on every group (they define the ranges; if a group scores under 0.8 on a reference clip, the metric or its range is wrong: fix it). v1 must score clearly lower, for the reasons the specs give (lit pale characters, thin neutral outline, empty pale set, parked camera).',
  '- Look at report.jpg for each run: are the head detections really heads, are the detected cuts real? Fix false detections.',
  '- If ' + P + '/v2/out/proto_v2.mp4 or frames exist when you finish, run the tool on them too and include the scores, but do not wait.',
  '- Write ' + P + '/v2/eval/README.md: usage, every metric with its definition, range and source, and known blind spots.',
].join('\n'), { label: 'build:score-tool', phase: 'Build', schema: SCHEMA })

phase('Validate')
const validated = await agent(CONTEXT + '\n\n' + [
  'YOUR TASK: adversarial validation and repair of the likeness scoring tool at ' + P + '/v2/eval/ (score.py, README.md, the scorecards its builder produced). You did not build it. Assume it is wrong until you have shown otherwise, and repair what you can.',
  'Checks, in order',
  '1. Re-run it yourself on clip A, clip B, the v1 stills (and v1 frames in ' + P + '/render/office/ if present), and on ' + P + '/v2/out/proto_v2.mp4 or the frame folder there if it exists by now. Does it complete inside the time limit with 2 threads?',
  '2. Truth of each metric: for at least 12 metrics across all six groups, measure the same quantity independently on a few frames by a different route (your own short script or by eye on a zoomed crop) and compare. In particular: head detection (open report.jpg: are all marked blobs heads, are obvious heads missed?), outline thick and thin widths, shot and transition detection against the transition table in camera_motion.md and its shot definition script, zoom rates, caption centre and stroke.',
  '3. Ranges: are the reference ranges copied correctly from LOOK_SPEC.md with the corrections of verify_measurements.md applied? List any wrong range.',
  '4. Discrimination: build degraded variants of a 10 s piece of clip A with ffmpeg (desaturated to 60 percent; brightened and washed out; frozen camera: one still repeated; captions covered; blurred) and confirm the matching group score drops while unrelated groups stay about the same. A metric that does not move, or moves the wrong way, is broken.',
  '5. Gaming: could a clip score high while looking nothing like the reference (for example a flat colour card with the right statistics, or random white discs)? Try two such synthetic inputs. Add guards where cheap (for example minimum detections, plausibility checks) and document the rest as blind spots.',
  '6. Stability: run twice on the same input, results must be identical; run on the first 5 s and the full clip, group scores should not swing wildly for groups that do not depend on length; say which metrics need a minimum duration and make the tool mark them "not measured" below it instead of scoring noise.',
  'Repair score.py directly, re-run everything, and write ' + P + '/v2/eval/VALIDATION.md with a table per check (what you did, result, fix). Finish with the final score table for clip A, clip B, v1 and the v2 prototype if available.',
  '',
  'The builder reported (verify, do not trust):',
  JSON.stringify(built, null, 1).slice(0, 14000),
].join('\n'), { label: 'validate:score-tool', phase: 'Validate', schema: SCHEMA })

return { built, validated }
