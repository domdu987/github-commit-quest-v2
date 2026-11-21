export const meta = {
  name: 'produce-office-shots',
  description: 'Production (Opus): the office shots with actors. Lane 1: shots 10, 11, 9 then 6, 12, 13, 14. Lane 2: shots 4, 5, 7 then 17, 18, 25',
  phases: [
    { title: 'Shots', detail: 'four workers, two at a time, each delivering finished takes', model: 'opus' },
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
const brief = (shots, folders, extra) => [
  'Read ' + P + '/v3/film/BRIEF_SHOTS.md now and follow it exactly; it tells you what else to read.',
  'YOUR TASK: deliver the finished takes of shots ' + shots + ' of the plan, one take folder per shot: ' + folders.map(f => P + '/v3/film/' + f + '/').join(', ') + ' . Write only inside those folders.',
  extra,
  'Order of work: stage and draft all your shots first, look at the drafts, then start the final renders one take after another and check each finished take. If time or budget runs short, a complete take with simpler acting is worth more than an unfinished ambitious one: never return with a take whose final frames are missing; reduce the acting or the camera move instead and say so.',
].join('\n')

const A1 = brief('10, 11 and 9', ['s10', 's11', 's09'], 'These three share marks, cameras and sprites (the gloat framing G grown from the hook marks): build 10 first, then 11, then 9. Set: office, light office_day (preset INTERIOR_DAY). Cast: hero, boss, senior_a, senior_b. Shot 10 holds the first quoted line of the boss (his mouth moves with the narration loudness between the times of that caption group); shot 11 is the erase-and-redraw running gag as one stepped pull-out (freehand, no ruler: see the client change in the brief); shot 9 is one take from the high two-shot into the worm-eye view up the red line. An interrupted worker left staging, sprites, drafts and scripts for these three shots in the folders, staged for a ruled line and a ruler gag: reuse the marks, cameras and sprites, drop the ruler, and re-register whatever touches the line on the hand-drawn track.')
const A2 = brief('6, 12, 13 and 14', ['s06', 's12', 's13', 's14'], 'Set: office, light office_day. Shot 6: the three old hands in a low wide. Shot 12: the laughers seen past the banker lamp. Shot 13: the punch-in on the Thai label being pinned above the arrow head (label artwork from the paper registry). Shot 14: the teletype prints the official forecast and the boss stamps it; the take ends on the forecast sheet thrust at the lens, which the next shot (kitchen, already finished in ' + P + '/v3/film/s15/) dissolves from paper to paper: open s15 first frames and match your last framing of the sheet to them.')
const A3 = brief('4, 5 and 7', ['s04', 's05', 's07'], 'Set: office, light office_day, the morning before (clean map: no red track, no smudge, no chalk curve, no label). Shot 4 dissolves out of the hook (the hook frames are ' + P + '/v3/out/frames/f_%04d.png, f_0001 = film frame 0; look at its last frames so your first framing answers them). Shot 5: the fly-in down the coast to the storm spinner being pinned off Florida. Shot 7: the pointer chalks the usual curved track out to sea and the fan of old ghost tracks appears. Shots 5 and 7 have no faces, only a hand; they are close on the real wall map, so use the high-resolution map of the props extension where the lens is closer than 1 D. An interrupted worker already finished s04 (verify it and keep it) and left a chain of final renders running for the other takes (a run_finals.sh under a work/ folder; the red line appears in none of these three shots, so its frames stay valid): check it with ps, let it finish, then check the takes and complete what is missing.')
const B = brief('17, 18 and 25', ['s17', 's18', 's25'], 'Set: office with the light extension: office_grey for shots 17 and 18 (the dull drizzle morning: the boss strolls in whistling, then gloats; shot 18 holds his second quoted line and the same G framing as shot 10, now in grey light, with the Thai label pinned on the map), office_storm for shot 25 (the storm spinner tears up the red line between the two men and hits New York; lightning flash setter). The label, spinner and pointer come from the props extension. Shot 25 is entered by an object wipe from the beach wave and left by a white flash: deliver clean frames plus the handle frames the plan asks for; the wipe and the flash themselves are added in the conform step.')

const lanes = await parallel([
  async () => {
    const a1 = await agent(A1, { label: 'shots:10-11-9', phase: 'Shots', schema: SCHEMA, model: 'opus' })
    const a2 = await agent(A2, { label: 'shots:6-12-13-14', phase: 'Shots', schema: SCHEMA, model: 'opus' })
    return [a1, a2]
  },
  async () => {
    const a3 = await agent(A3, { label: 'shots:4-5-7', phase: 'Shots', schema: SCHEMA, model: 'opus' })
    const b = await agent(B, { label: 'shots:17-18-25', phase: 'Shots', schema: SCHEMA, model: 'opus' })
    return [a3, b]
  },
])
return lanes.filter(Boolean).flat()
