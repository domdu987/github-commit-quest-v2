export const meta = {
  name: 'dz09-ep1-hook-shot-plan',
  description: 'Three directors plan the DEAD ZONE 09 EP.1 opening hook shot by shot, judges score, a director merges, a checker verifies',
  phases: [
    { title: 'Directors', detail: '3 independent shot plans for EP.1 0:00-0:55' },
    { title: 'Judges', detail: 'score fidelity, hook power, feasibility' },
    { title: 'Merge', detail: 'one merged plan' },
    { title: 'Check', detail: 'adversarial coverage and feasibility check' },
  ],
}
const P = '/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09'
const CONTEXT = `Project folder: ${P}. Read FIRST: ${P}/story/MASTER_SCREENPLAY_V5_EP1_excerpt.md (the screenplay excerpt, Thai), look at the image ${P}/uploads/character_sheet.webp (the cast design: 2D stickman-style characters with round white heads, black line faces, full costumes), ${P}/spec/LOOK_SPEC.md (the measured production look: flat unlit 2D puppet cards inside a lit 3D Blender world, one hard key light, blue-violet shade, 22mm camera at low/eye/high angles, vertical 9:16), ${P}/references/look.md, ${P}/references/story-formula.md, and the example plan format ${P}/plan/shot_plan.md. Also skim ${P}/v3/README.md and ${P}/v2/puppet (the puppet API) so the plan only asks for things this pipeline can build (puppet poses, expressions, props as cards, 3D sets from code, camera moves, particles such as rain via simple cards/streaks, light changes).
TARGET: the opening hook of EP.1 "ทางด่วนนรก" — Scene 01 complete plus the first beat of Scene 02 (the driver lunges and bites), about 50-55 seconds, vertical 9:16, 24 fps. The viewer must not swipe away in the first 3 seconds and must want the next episode at the end. Keep the screenplay's dialogue and events faithful (Thai dialogue, burned-in Thai captions). Night, heavy rain, Bangkok expressway gridlock, red emergency lights. EP.1 grammar: dark blue, grey, emergency red; handheld energy that follows emotion, not constant shake. Production rule: no still image with a camera move standing in for animation; every character acts with face and body.
Do not invent new story events that contradict the screenplay; you may add wordless visual details (rain on the phone screen, battery 3 bars insert, the wrist watch) that set up later payoffs. Do not call any paid API. Do not edit files outside the file you are told to write.`

const PLAN_FORMAT = `Output a Markdown shot plan: a header table (total duration, shot count, average shot length, sets, cast, props), then one row/section per shot with: id, start-end seconds, duration, set, framing and camera angle (low/eye/high, lens), camera move, cast on screen with pose and expression, action, dialogue/caption line (Thai), sound cues (rain, radio, phone vibration, sirens, effects), light notes, transition out, and which later payoff it sets up. End with a list of assets to build (sets, puppets, props, effects) and an honest list of risks.`

const DIRECTORS = [
  { key: 'hook-first', brief: 'Director A: hook-first. Spend the first 3 seconds on the strongest unanswered image you can build from the screenplay (the dying radio over black, then the red-lit gridlock). Fast grammar: average shot 1.5-2.5 s, frequent angle changes.' },
  { key: 'emotion-first', brief: 'Director B: emotion-first. The audience must care about Kong and his broken promise to his daughter before the horror lands. Use close-ups on the phone (4 missed calls), his face, rain. Let the phone call breathe, then hit hard with the driver lifting his head. Average shot 2-3.5 s.' },
  { key: 'lean', brief: 'Director C: the leanest faithful plan. Fewest sets, puppets and new assets that still delivers every screenplay beat and a strong cliffhanger; reuse one expressway set from several angles. Optimise for what a 4-core CPU render budget (about 18 CPU seconds per final 720x1280 frame) can afford.' },
]

phase('Directors')
const plans = await parallel(DIRECTORS.map(d => () =>
  agent(`${CONTEXT}\n\n${d.brief}\n\nWrite your plan to ${P}/plan/ep1_hook_${d.key}.md. ${PLAN_FORMAT} Return a 5-line summary: file path, duration, shot count, the first-3-second image, the final image.`,
    { label: `director:${d.key}`, phase: 'Directors' })))

phase('Judges')
const SCORE = { type: 'object', properties: {
  scores: { type: 'array', items: { type: 'object', properties: {
    plan: { type: 'string' }, fidelity: { type: 'number' }, hook: { type: 'number' }, emotion: { type: 'number' }, feasibility: { type: 'number' }, notes: { type: 'string' } },
    required: ['plan','fidelity','hook','emotion','feasibility','notes'] } },
  best_ideas_to_graft: { type: 'array', items: { type: 'string' } } }, required: ['scores','best_ideas_to_graft'] }
const files = DIRECTORS.map(d => `${P}/plan/ep1_hook_${d.key}.md`).join(', ')
const LENSES = [
  'Lens: screenplay fidelity and setups for later payoffs (battery bars, broken promise, 60-second rule, phone).',
  'Lens: retention. Would a viewer scrolling a vertical feed stop in 3 seconds and stay to the end? Judge pacing, curiosity gaps, cliffhanger.',
  'Lens: feasibility in this exact pipeline and render budget; read the pipeline code before judging. Penalise anything the puppet/3D system cannot do.',
]
const judged = await parallel(LENSES.map((l, i) => () =>
  agent(`${CONTEXT}\n\nYou are judge ${i+1}. ${l}\nRead the three plans: ${files}. Score each 0-10 on fidelity, hook, emotion, feasibility (score all four, but weigh your lens in the notes). List the best ideas from any plan worth grafting into the final.`,
    { label: `judge:${i+1}`, phase: 'Judges', schema: SCORE })))

phase('Merge')
const merged = await agent(`${CONTEXT}\n\nYou are the supervising director. Read the three plans (${files}) and these judge reports:\n${JSON.stringify(judged.filter(Boolean), null, 1)}\nStart from the plan with the best combined score, graft the listed best ideas where they fit, and fix every problem the judges named. Write the final plan to ${P}/plan/ep1_hook_FINAL.md. ${PLAN_FORMAT} Also add a section "Prototype cut (first 5 s)" naming exactly which shots make the first 5 seconds that will be built first. Return a short summary.`,
  { label: 'merge', phase: 'Merge' })

phase('Check')
const CHECK = { type: 'object', properties: {
  pass: { type: 'boolean' },
  problems: { type: 'array', items: { type: 'object', properties: { shot: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } }, required: ['shot','problem','fix'] } } },
  required: ['pass','problems'] }
const check = await agent(`${CONTEXT}\n\nAdversarially check ${P}/plan/ep1_hook_FINAL.md. Try hard to find: screenplay beats missing or out of order; dialogue changed in meaning; contradictions of the world rules; timings that do not add up; shots this pipeline cannot build; assets used but not listed; a first 3 seconds that is not gripping; a weak final image. If you find real problems, fix them directly in the file, then report what you changed.`,
  { label: 'check', phase: 'Check', schema: CHECK })
return { plans, merged, check }
