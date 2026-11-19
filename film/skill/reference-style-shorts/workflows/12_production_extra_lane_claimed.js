export const meta = {
  name: 'produce-office-shots-advance',
  description: 'Production (Opus), extra lane: start shots 12, 13 and 14, 6 now instead of waiting for the first lane to finish',
  phases: [
    { title: 'Shots', detail: 'two workers in parallel, each delivering two finished takes', model: 'opus' },
  ],
}

// EXAMPLE FROM FILM 1: rewrite the prompt texts (story, shots, lanes, sets, cast, paths) before use; keep the shape.
// A Workflow tool script (see the workflow-authoring skill). Replace __PROJ__ with the project path.
// model: 'opus' is the one-tier-down worker tier; the main conversation runs on the strongest model.
// See references/production.md, section "Adapting to a new film".
const P = '__PROJ__'   // replace with the project path before running
const SCHEMA = {
  type: 'object',
  properties: {
    takes: { type: 'array', items: { type: 'object', properties: { take: { type: 'string' }, g0: { type: 'number' }, g1: { type: 'number' }, frames_rendered: { type: 'number' }, complete: { type: 'boolean' }, hue_row: { type: 'string' }, notes: { type: 'string' } }, required: ['take', 'g0', 'g1', 'frames_rendered', 'complete', 'notes'] } },
    deviations_from_plan: { type: 'array', items: { type: 'string' } },
    known_gaps: { type: 'array', items: { type: 'string' } },
  },
  required: ['takes', 'deviations_from_plan', 'known_gaps'],
}
const brief = (lane, shots, folders, extra) => [
  'Read ' + P + '/v3/film/BRIEF_SHOTS.md now and follow it exactly; it tells you what else to read.',
  'YOUR LANE NAME is ' + lane + '. The CLAIMED.txt file in each of your folders names your lane: you own these folders, and the claimed-folder rule of the brief protects them from other workers.',
  'YOUR TASK: deliver the finished takes of shots ' + shots + ' of the plan, one take folder per shot: ' + folders.map(f => P + '/v3/film/' + f + '/').join(', ') + ' . Write only inside those folders. They are empty apart from CLAIMED.txt: nobody has staged these shots yet.',
  extra,
  'Other workers are rendering right now on this 4-core machine (up to four final renders at once), so drafts and finals are slower than the brief says: keep drafts small (360x640, 6 samples, every 4th to 6th frame), and start each final render as a detached, resumable process (nohup, one process, 2 threads) as soon as its draft is right, then stage your next shot while it renders.',
  'Order of work: stage and draft your first shot, start its final render, then stage and draft the second while the first renders, then check each finished take (post, qa, contact sheet, four frames at full size, QA.md). Do not return while a final render of yours is still running: wait for it, run post and qa, and check the frames. If time or budget runs short, a complete take with simpler acting is worth more than an unfinished ambitious one: never return with a take whose final frames are missing; reduce the acting or the camera move instead and say so.',
].join('\n')

const X = brief('ADVANCE-X', '12 and 13', ['s12', 's13'], 'Set: office, light office_day (preset INTERIOR_DAY). Cast: hero, boss, senior_a, senior_b as the plan rows say. Both shots follow shot 11 (the erase-and-redraw running gag) in the same scene and share its marks, cameras and sprites: read ' + P + '/v3/film/s10/shot.py and ' + P + '/v3/film/s11/shot.py first (s10 is a finished take, s11 is rendering now; do not write in those folders) and reuse their marks and the gloat framing so that the people stand where the previous shot left them. Shot 12: the laughers seen past the banker lamp. Shot 13: the punch-in on the Thai label being pinned above the arrow head (label artwork from the paper registry; the label and the pin come from the props extension; register the label on the hand-drawn track through the set API, see the client decision in the brief). The red line shows in both shots: it is the hand-drawn track of the set as it is now.')
const Y = brief('ADVANCE-Y', '14 and 6', ['s14', 's06'], 'Set: office, light office_day (preset INTERIOR_DAY). Do shot 14 first (it is the longer one). Shot 14: the teletype prints the official forecast and the boss stamps it; the take ends on the forecast sheet thrust at the lens, which the next shot (kitchen, already finished in ' + P + '/v3/film/s15/) dissolves from paper to paper: open the first frames of s15 and match your last framing of the sheet to them. Shot 6: the three old hands in a low wide. Shot 6 sits between shots 5 and 7, which are finished (' + P + '/v3/film/s05/ and ' + P + '/v3/film/s07/): it is the morning before, so check the plan row and those two shot.py files for the state of the wall map in that scene (clean map: no red track, no smudge, no label) and make your first and last framings answer their last and first frames across the planned transitions.')

const lanes = await parallel([
  () => agent(X, { label: 'shots:12-13', phase: 'Shots', schema: SCHEMA, model: 'opus' }),
  () => agent(Y, { label: 'shots:14-6', phase: 'Shots', schema: SCHEMA, model: 'opus' }),
])
return lanes.filter(Boolean)