export const meta = {
  name: 'director-shot-plan-v2',
  description: 'Plan every shot of the 65 s film for the new Thai script: three independent shot plans, three judges, one merged plan, one adversarial check',
  phases: [
    { title: 'Plan', detail: 'three shot plans: mirror clip A grammar, mirror clip B grammar, cheapest faithful plan' },
    { title: 'Judge', detail: 'reference fidelity, feasibility and cost, story clarity' },
    { title: 'Merge', detail: 'one shot plan with asset list and build order' },
    { title: 'Verify', detail: 'coverage of every caption phrase, timing, assets, render budget' },
  ],
}

// EXAMPLE FROM FILM 1: rewrite the prompt texts (story, shots, lanes, sets, cast, paths) before use; keep the shape.
// A Workflow tool script (see the workflow-authoring skill). Replace __PROJ__ with the project path.
// model: 'opus' is the one-tier-down worker tier; the main conversation runs on the strongest model.
// See references/production.md, section "Adapting to a new film".
const P = '__PROJ__'
const OUT = P + '/plan'

const BRIEF = [
  'CONTEXT',
  'We are producing a 65 second vertical animated short (720x1280, 30 fps, Thai narration and Thai captions) that must look and feel like two reference clips. Stills of the references every 0.5 s: ' + P + '/ref/a/tSS.S.jpg (clip A, railroad) and ' + P + '/ref/b/tSS.S.jpg (clip B, dragon jar); their English transcripts: ' + P + '/../media/a/script_clean.txt and ' + P + '/../media/b/script_clean.txt.',
  'THE SCRIPT IS FINAL: ' + P + '/script_th_v2/script_th.json (Thai, 21 sentences, each with beat, formula elements, tts text and caption phrases) with an English line-by-line gloss in ' + P + '/script_th_v2/script_en_gloss.txt. THE NARRATION IS RECORDED: ' + P + '/audio/th/full_v2/narration_timing.json gives t0 and t1 in seconds for every one of the 104 caption phrases (field sentence = index of the sentence), total 65.4 s. Picture must be cut to this audio.',
  'THE STORY: September 1938, U.S. Weather Bureau office. The youngest forecaster draws a ruler-straight red hurricane track on the wall map pointing north at New York; his boss rubs it out; he redraws it every time; the office nicknames the line "ทางด่วนพายุ" (the storm expressway); the official forecast says rain; next morning Long Island wakes to a grey drizzle and the boss gloats; meanwhile at sea two walls of high pressure leave one straight corridor north and the wind in it flings the storm north at almost 100 km per hour; people on the beach see a fog bank that is a wall of water taller than a house; the storm rode the expressway into New York while the forecast on the kitchen table still says rain.',
  '',
  'WHAT EXISTS (read these before planning)',
  '- The measured shot grammar of the references: ' + P + '/spec/camera_motion.md (shot tables for both clips with times, framings, moves and transitions; section 1-2) and ' + P + '/spec/LOOK_SPEC.md section 5 (camera, staging, animation, transitions) with corrections in ' + P + '/spec/verify_measurements.md. Key numbers: a framing change every 1.2-1.5 s (transitions plus in-shot snap reframings); 16 shots in clip A and 22 in clip B per 65 s; 81 percent of transitions are 9-23 frame dissolves, the rest hard cuts, punch-ins, whip pans, object wipes; the camera is almost never static; low, eye-level, high and top-down camera heights; two-shots staged in depth; close inserts on props; the mechanism is shown as a cutaway or diagram-like sequence (clip B: inside the jar).',
  '- A real 3D office set with one hard key light (sun through a window), built in Blender from code: ' + P + '/v3/set3d/API.md, REVIEW.md and the stills ' + P + '/v3/set3d/still_*.png (look at them). It has the wall map with the red track as real geometry that can grow and be erased, a sign, calendar, clock, pin board, teletype on a stand, radiator, filing cabinets, desk, pendant lamps, floor rug, and ten ready camera setups.',
  '- A staging system that puts flat 2D puppets into the 3D scene as cards, with pose and hand registration, camera rig with eased drifts, snaps and whip pans, and a render driver: ' + P + '/v3/stage/API.md and REVIEW.md (read its limits: no back views, cards near walls with far off-axis cameras, top-down leans cards back). Cast today: hero (young forecaster, tweed cap, blue argyle vest) and boss (homburg, green pinstripe waistcoat, moustache); the puppet system (' + P + '/v2/puppet/API.md) can make more cast members by changing build, hat, costume and face.',
  '- The first 5 seconds (sentence 1, three shots: raking insert of the pencil drawing the line; low-angle medium of the hero jabbing at New York; high two-shot of the boss erasing while the hero goes wide-eyed) are being rendered right now. Keep them as shots 1-3 of your plan, with these times: sentence 1 phrases from the timing file.',
  '- A flat 2D compositor (' + P + '/v2/README.md) that can make flat inserts and diagram shots quickly (0.2-0.7 s per frame), and the true-3D renderer at roughly 6-9 s per frame on this machine (4 CPU cores, no GPU).',
  '',
  'PRODUCTION CONSTRAINTS',
  '- Every new 3D set costs about 3 hours to build and review. Budget: the office (exists) plus AT MOST two new 3D sets (for example a Long Island beach with houses, and one small interior such as a kitchen table by a window), plus flat or 2.5D inserts (map diagram for the mechanism, newspaper or teletype paper, calendar) which are cheap. Reuse sets from several camera heights and times of day instead of adding sets. A different light on the same set (grey drizzle, storm dark) counts as cheap.',
  '- Total render budget about 2000 frames; prefer shots that hold one set long enough to amortise it, but never break the grammar (a framing change every 1.2-1.5 s, by transition or by in-shot snap).',
  '- Characters never show their backs, mouths move only for quoted lines (the two boss quotes), the hero never speaks.',
  '- Sound effects and music are added later from a cue list, so every shot must name the sounds it needs.',
  '',
  'WHAT TO DELIVER: a complete shot plan as JSON. Fields per shot: n, t0, t1 (seconds, aligned to caption phrase boundaries from the timing file, the picture may lead the word by 2-4 frames), sentences (indices), captions (the phrases it covers), set (office | beach | kitchen | map_diagram | insert:<name> ...), light (for example office_day, grey_drizzle, storm), camera (class: insert, low, eye, high, top_down; start framing; move: drift, snap at time x, whip in or out, orbit; what the camera does on which word), actors and acting beats (poses, expressions, blinks, who moves and who freezes), props and graphics (what must be readable; all on-screen text and its language), transition_in (dissolve N frames, hard cut, punch-in, whip pan, wipe), sfx (list of sound cues with times), new_assets (anything that does not exist yet), reference (which reference shot it imitates, as clip and time, and why). Then top-level lists: sets_needed (with which shots use them and how many frames), cast_needed (every character with build, hat, costume, where used), props_needed, inserts_needed, a build order, and a frame count per renderer (true 3D versus flat).',
  'Design rules: mirror the reference shot grammar honestly (count your framing changes per second and your shot lengths against the measured numbers); give the running gag (erase, redraw) and the nickname a visual life (for example a hand-lettered label pinned on the map that reads the nickname in Thai, the boss tapping it); stage the false defeat and the two gloats with the same framing so the callback lands; show the mechanism as a clear diagram-like sequence on the map itself (two pressure walls, one corridor, the storm symbol shooting up the straight line) the way clip B shows the inside of the jar; make the disaster one strong image; end on the image of the forecast paper.',
  '',
  'RULES: do not call any MCP or connector tools; no network; do not render anything in Blender (another job is rendering; reading images is fine); write files only under ' + OUT + ' ; your final message is consumed by a script, return the structured result only.',
].join('\n')

const SHOT = {
  type: 'object',
  properties: {
    n: { type: 'number' }, t0: { type: 'number' }, t1: { type: 'number' },
    sentences: { type: 'array', items: { type: 'number' } },
    captions: { type: 'array', items: { type: 'string' } },
    set: { type: 'string' }, light: { type: 'string' }, camera: { type: 'string' },
    acting: { type: 'string' }, props_graphics: { type: 'string' }, transition_in: { type: 'string' },
    sfx: { type: 'array', items: { type: 'string' } },
    new_assets: { type: 'array', items: { type: 'string' } },
    reference: { type: 'string' },
  },
  required: ['n', 't0', 't1', 'sentences', 'set', 'light', 'camera', 'acting', 'props_graphics', 'transition_in', 'sfx', 'new_assets', 'reference'],
}
const PLAN_SCHEMA = {
  type: 'object',
  properties: {
    shots: { type: 'array', items: SHOT },
    sets_needed: { type: 'array', items: { type: 'string' } },
    cast_needed: { type: 'array', items: { type: 'string' } },
    props_needed: { type: 'array', items: { type: 'string' } },
    inserts_needed: { type: 'array', items: { type: 'string' } },
    build_order: { type: 'array', items: { type: 'string' } },
    grammar_check: { type: 'string', description: 'your own count: number of shots, mean shot length, framing changes and their mean interval, transition mix, camera height mix, compared with the reference numbers' },
    frames_true3d: { type: 'number' }, frames_flat: { type: 'number' },
    notes: { type: 'string' },
  },
  required: ['shots', 'sets_needed', 'cast_needed', 'props_needed', 'inserts_needed', 'build_order', 'grammar_check', 'frames_true3d', 'frames_flat', 'notes'],
}

const ANGLES = [
  { key: 'mirror-A', text: 'Your method: MIRROR CLIP A. Take the clip A shot table from camera_motion.md and look at its stills in order. For each of our story beats find the clip A shot that does the same job and copy its framing, camera height, move and transition (low-angle authority shots, long takes with snap reframings inside them, inserts on text props, the wide vista before the catastrophe).' },
  { key: 'mirror-B', text: 'Your method: MIRROR CLIP B. Take the clip B shot table from camera_motion.md and look at its stills in order. For each of our story beats find the clip B shot that does the same job and copy its framing, camera height, move and transition (hard cut, punch-in and whip pan in the hook, close-ups (sharp picture: no depth-of-field blur, client decision), the high-angle shots, the cutaway that explains the mechanism at the end, the last image).' },
  { key: 'lean', text: 'Your method: THE LEANEST FAITHFUL PLAN. Hit every grammar number with the fewest new assets: at most one new 3D set beyond the office if you can make it work (for example only the beach, with the kitchen forecast paper as a flat insert), maximum reuse of the office from all ten camera setups, the mechanism as a flat or 2.5D diagram on the map. Show exactly where each saving costs likeness, so a merger can decide.' },
]

phase('Plan')
const plans = (await parallel(ANGLES.map(a => () =>
  agent(BRIEF + '\n\n' + a.text + '\nBefore returning, check: every caption phrase of the timing file is covered by exactly one shot, shot times are contiguous from 0 to the end of the audio, and count your grammar numbers. Also write your plan to ' + OUT + '/plan_' + a.key + '.json .', { label: 'plan:' + a.key, phase: 'Plan', schema: PLAN_SCHEMA })
    .then(p => p ? { key: a.key, plan: p } : null)
))).filter(Boolean)
log('plans: ' + plans.map(p => p.key + ' ' + p.plan.shots.length + ' shots, 3D frames ' + p.plan.frames_true3d).join('; '))
if (plans.length === 0) { return { error: 'no plans' } }

const LETTERS = ['A', 'B', 'C']
const digest = plans.map((p, i) => 'PLAN ' + LETTERS[i] + ' (method ' + p.key + ', file ' + OUT + '/plan_' + p.key + '.json)\n' + p.plan.shots.map(s => '#' + s.n + ' ' + s.t0.toFixed(2) + '-' + s.t1.toFixed(2) + ' [' + s.set + ' / ' + s.light + '] cam: ' + s.camera + ' | act: ' + s.acting + ' | in: ' + s.transition_in + ' | ref: ' + s.reference).join('\n') + '\nSETS: ' + p.plan.sets_needed.join('; ') + '\nCAST: ' + p.plan.cast_needed.join('; ') + '\nINSERTS: ' + p.plan.inserts_needed.join('; ') + '\nGRAMMAR: ' + p.plan.grammar_check + '\nFRAMES 3D ' + p.plan.frames_true3d + ' flat ' + p.plan.frames_flat).join('\n\n').slice(0, 60000)

const JUDGE_SCHEMA = {
  type: 'object',
  properties: {
    scores: { type: 'array', items: { type: 'object', properties: { plan: { type: 'string' }, score: { type: 'number' }, problems: { type: 'array', items: { type: 'string' } }, best_shots: { type: 'array', items: { type: 'string' } } }, required: ['plan', 'score', 'problems', 'best_shots'] } },
    winner: { type: 'string' },
    advice_for_merger: { type: 'string' },
  },
  required: ['scores', 'winner', 'advice_for_merger'],
}
const LENSES = [
  { key: 'reference-fidelity', text: 'Your lens: fidelity to the reference shot grammar. Re-derive the reference numbers from camera_motion.md yourself, look at the reference stills named in each plan, and check each plan: number of shots, shot lengths, interval between framing changes, transition mix, camera heights and their purposes, depth staging, inserts, how the mechanism is shown, the last image. Name the shots that would not look like the reference and why.' },
  { key: 'feasibility-cost', text: 'Your lens: can this be built and rendered with what exists. Read v3/set3d/API.md and REVIEW.md, v3/stage/API.md and REVIEW.md. For each plan list every new asset, how hard it is, and where the plan asks for something the staging system cannot do (back views, cards against walls at far off-axis angles, top-down on actors, talking mouths outside quotes, text that cannot be typeset, effects like rain, fog and a wall of water: say how each could be done cheaply). Estimate build hours and render hours. Name the cheapest change that keeps the look.' },
  { key: 'story-clarity', text: 'Your lens: would a first-time Thai viewer follow the story with the sound off and with it on. Check each plan beat by beat against the script: is the running gag (erase, redraw) visible, does the nickname get a visual, do the false defeat and the two gloats rhyme visually, is the mechanism understandable from the picture alone, is the disaster one strong image, does the last image land. Name confusing shots and missing visuals.' },
]

phase('Judge')
const verdicts = (await parallel(LENSES.map(l => () =>
  agent(BRIEF + '\n\nYOU ARE A JUDGE, not a planner. ' + l.text + '\nRead the three plan files in full. Score each plan from 0 to 10 on your lens only, name a winner, and list the best individual shots across all plans that the merger should keep.\n\n' + digest, { label: 'judge:' + l.key, phase: 'Judge', schema: JUDGE_SCHEMA })
    .then(v => v ? { lens: l.key, verdict: v } : null)
))).filter(Boolean)
log('judges: ' + verdicts.map(v => v.lens + ' -> ' + v.verdict.winner).join(', '))

phase('Merge')
const merged = await agent(BRIEF + '\n\nYOU ARE THE DIRECTOR. Write the final shot plan: start from the plan the judges prefer overall, take the best shots of the others, and fix every problem the judges listed (fidelity wins on grammar, feasibility wins on what can be built: at most two new 3D sets, story clarity wins on what the viewer must see). Read the three plan files in full first. Write ' + OUT + '/shot_plan.json (the structured plan) and ' + OUT + '/shot_plan.md (a readable table: shot, time, captions in Thai, set and light, camera, acting, transition, sounds, new assets; then the asset lists, the build order with hour estimates, and the frame budget).\n\nPLANS (digest)\n' + digest + '\n\nJUDGES\n' + JSON.stringify(verdicts, null, 1).slice(0, 30000), { label: 'merge:shot-plan', phase: 'Merge', schema: PLAN_SCHEMA })

phase('Verify')
const verified = await agent(BRIEF + '\n\nYOU ARE THE LAST CHECK before sets get built from this plan, and you did not write it. Work from ' + OUT + '/shot_plan.json and shot_plan.md. Check with a script and by reading: (1) coverage: every one of the 104 caption phrases in the timing file falls inside exactly one shot, shot times are contiguous from 0 to the end of the audio, no shot shorter than 0.4 s; (2) grammar against the reference numbers you re-derive from camera_motion.md: shot count, mean shot length, interval between framing changes (count transitions plus the in-shot snaps the plan names), transition mix, camera height mix; (3) shots 1-3 match what is already being rendered; (4) feasibility against v3/set3d and v3/stage API and REVIEW files: nothing the staging system cannot do, at most two new 3D sets, every on-screen text named with its language; (5) the asset lists are complete: every set, cast member, prop, insert and effect that any shot uses appears in the lists and in the build order; (6) the sound cue list covers every visible action; (7) frame budget arithmetic. Repair the two files directly for every real defect, re-run your checks, and return the final plan exactly as it stands in the file.\n\nThe director reported:\n' + JSON.stringify({ grammar_check: merged && merged.grammar_check, sets: merged && merged.sets_needed, cast: merged && merged.cast_needed, build_order: merged && merged.build_order, notes: merged && merged.notes }, null, 1).slice(0, 12000), { label: 'verify:shot-plan', phase: 'Verify', schema: PLAN_SCHEMA })

const fin = verified || merged
return { shots: fin ? fin.shots.length : 0, sets_needed: fin && fin.sets_needed, cast_needed: fin && fin.cast_needed, inserts_needed: fin && fin.inserts_needed, build_order: fin && fin.build_order, grammar_check: fin && fin.grammar_check, frames_true3d: fin && fin.frames_true3d, frames_flat: fin && fin.frames_flat, notes: fin && fin.notes, files: [OUT + '/shot_plan.json', OUT + '/shot_plan.md'] }
