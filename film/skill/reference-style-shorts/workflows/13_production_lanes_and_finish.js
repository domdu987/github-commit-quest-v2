export const meta = {
  name: 'produce-map-beach-and-finish',
  description: 'Production (Opus): the mechanism on the wall map (shots 19-22) and the beach shots (8, 16, 23, 24), then conform the whole film, mix the sound and review it against the reference',
  phases: [
    { title: 'Shots', detail: 'mechanism lane and beach lane, in parallel', model: 'opus' },
    { title: 'Conform', detail: 'wait for all takes, join with the planned transitions, Thai captions', model: 'opus' },
    { title: 'Sound', detail: 'voice, music and effects from the cue lists', model: 'opus' },
    { title: 'Review', detail: 'independent check against the reference', model: 'opus' },
  ],
}

// EXAMPLE FROM FILM 1: rewrite the prompt texts (story, shots, lanes, sets, cast, paths) before use; keep the shape.
// A Workflow tool script (see the workflow-authoring skill). Replace __PROJ__ with the project path.
// model: 'opus' is the one-tier-down worker tier; the main conversation runs on the strongest model.
// See references/production.md, section "Adapting to a new film".
const P = '__PROJ__'   // replace with the project path before running
const SHOT_SCHEMA = {
  type: 'object',
  properties: {
    takes: { type: 'array', items: { type: 'object', properties: { take: { type: 'string' }, g0: { type: 'number' }, g1: { type: 'number' }, frames_rendered: { type: 'number' }, complete: { type: 'boolean' }, hue_row: { type: 'string' }, notes: { type: 'string' } }, required: ['take', 'g0', 'g1', 'frames_rendered', 'complete', 'notes'] } },
    deviations_from_plan: { type: 'array', items: { type: 'string' } },
    known_gaps: { type: 'array', items: { type: 'string' } },
  },
  required: ['takes', 'deviations_from_plan', 'known_gaps'],
}
const OUT_SCHEMA = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
    numbers: { type: 'string' },
    problems: { type: 'array', items: { type: 'string' } },
  },
  required: ['files', 'summary', 'numbers', 'problems'],
}
const brief = (shots, folders, extra) => [
  'Read ' + P + '/v3/film/BRIEF_SHOTS.md now and follow it exactly; it tells you what else to read.',
  'YOUR TASK: deliver the finished takes of shots ' + shots + ' of the plan, one take folder per shot: ' + folders.map(f => P + '/v3/film/' + f + '/').join(', ') + ' . ' + extra,
  'Order of work: build what is missing, stage and draft your shots, look at the drafts, then start the final renders one take after another and check each finished take. If time or budget runs short, a complete take with a simpler camera path or simpler animation is worth more than an unfinished ambitious one: never return with a take whose final frames are missing; simplify and say so.',
].join('\n')

const M1 = brief('19', ['s19'], 'You also build the mechanism props, build-order steps 2 and 9 of the plan, as an extension module in ' + P + '/v3/set3d_ext/mech/ (office_mech.py + API.md; write only there and in your take folder; import office3d, the props extension and the light extension, edit none of them): on the real wall map, two walls of high pressure that rise out of the paper on each side of the red line as low terraces, the single corridor between them running north along the red line (the line is hand-drawn, see the client change in the brief: build the lane and the inner edges of the walls from the track points of the set so the corridor hugs the line), compass, pictograms and speed sign from the paper registry (' + P + '/v3/paper/API.md), wind arrows that stream up the corridor, ghost spinners for the speed comparison, each with a setter that can keyframe, and the cameras the plan names (corridor_cam and the others of shots 19-22). Do the gate test of step 2 first (one still from the corridor camera 0.35 D above the map with the high-resolution map texture): if the close lens shimmers or the near wall hides the lane, use the fallback the plan gives (the same choreography from 0.7 D or more). Light: office_grey. No characters appear in shots 19-22. Shot 19 is one take of 7.7 seconds with four snap reframings: it must stay readable and never rest. The next worker animates shots 20, 21 and 22 with your module, so document every setter and camera. An interrupted worker already built most of the mechanism module (office_mech.py and API.md, about 40 KB) and the shot script of s19, for a STRAIGHT corridor: read them first, keep the design, the setters and the cameras, and rework the geometry so the lane and the inner edges of the walls follow the hand-drawn track points; then re-check the gate test and the cameras.')
const M2 = brief('20, 21 and 22', ['s20', 's21', 's22'], 'Write only inside those folders. The mechanism props, setters and cameras were just built in ' + P + '/v3/set3d_ext/mech/ (read its API.md and the finished take ' + P + '/v3/film/s19/ first: your shots continue it and must match its look and scale). No characters. Shot 20: the corridor view, wind arrows catch the spinner and it rockets north past the speed sign. Shot 21: the whip pull-out to the whole map with the speed comparison against the ghost spinners. Shot 22: the walls sink back into the paper, the lane fuses into the red pencil line, and the camera comes to rest on the pinned Thai label ทางด่วนพายุ and then the arrow head at Long Island.')
const C1 = brief('16 and 23', ['s16', 's23'], 'You also add what the plan asks of the beach set for all four beach shots, as an extension module in ' + P + '/v3/set3d_ext/beach/ (beach_ext.py + API.md; write only there and in your take folders; import ' + P + '/v3/set3d_beach/beach3d.py and do not edit it; read its API.md and REVIEW.md): the storm_approach preset (GREY_DRIZZLE darkened with a bruise-violet sky and the fog bank), the cameras beach_high, beach_shore_eye (THE BEACH FRAMING, shared by shots 16 and 23) and beach_low_wave, the LONG ISLAND sign from the paper registry, and the small dressing items the plan lists under the beach set. Cast: beach_man and beach_woman (' + P + '/v3/cast/API.md), acting from the acting library (stretch, palm out for rain, shrug, shading the eyes, holding the hat brim). Shot 16 is the false defeat: an ordinary grey drizzle morning, harmless and dull. Shot 23 is the same framing under the approaching storm with the fog bank growing on the horizon. The next worker does shots 8 and 24 with your module. An interrupted worker already built the beach extension and finished s16 (meta.json and all its frames): verify both, keep them, and go on with s23.')
const C2 = brief('8 and 24', ['s08', 's24'], 'Write only inside those folders. The beach extension (presets, cameras, dressing) was just built in ' + P + '/v3/set3d_ext/beach/ (read its API.md and the finished takes ' + P + '/v3/film/s16/ and s23/ first: same axis, same look). Shot 8: the sunny beach before the storm, SUMMER_SUN, the man asleep in his deck chair (reclining asleep pose of the acting library), high view coming down to eye level; this is the one clip-A style exterior with whole-figure cast shadows on the sand. Shot 24: the hard cut to the low angle as the fog bank turns out to be a wall of water taller than the cottages (set_wave), the two shocked faces, the boater flying off; it is left by an object wipe (the foam sheet crossing the lens) that the conform step adds: deliver clean frames plus the handle frames the plan asks for.')

const CONFORM = [
  'Read ' + P + '/v3/film/BRIEF_FINISH.md now and follow it.',
  'YOUR TASK: conform the film (build-order step 12 of the plan). Write only under ' + P + '/v3/film/out/ .',
  '1. WAIT FOR THE TAKES. Other workers are still rendering some takes. A take is complete when its meta.json exists and every frame of its range g0..g1-1 (plus the handles it declares) exists in frames/. Check all expected takes; if some are incomplete, start a background shell loop that checks every two minutes and wait for it (up to 5 hours in total, in waits of at most 100 minutes each; while waiting, prepare everything else: the hook conversion, the transition code, the caption file). After 5 hours go on with what exists: for a missing take hold the last frame of the previous take with a slow push-in so the film keeps its length, and list it as a problem.',
  '2. The hook: take film frames from ' + P + '/v3/out/frames/ as BRIEF_FINISH.md explains.',
  '3. Join the takes on the film clock with the transition the plan gives for each join: smoothstep cross-dissolves of the planned length mixed from the handle frames of both takes (where a handle frame is missing, extend with a 2D continuation of the last camera motion), hard cuts, the whip pans already inside the takes, the punch-in with speed lines, the object wipe by the wave foam sheet, the white flash. Overlays the plan lists for the conform step and that no take already contains may be added as simple 2D layers; if one is costly, leave it out and list it.',
  '4. Write the 1965 picture frames to ' + P + '/v3/film/out/frames/g_%04d.png, then burn the 104 Thai caption phrases last and encode ' + P + '/v3/film/out/film_silent.mp4 (H.264, yuv420p, 30 fps). Merge every take cue list and the hook cue list into ' + P + '/v3/film/out/cues_all.json on the film clock (seconds), with the take of each cue.',
  '5. Check: frame count 1965; no pops at joins (look at a strip of 6 frames across every join); captions clear of heads; a contact sheet of 48 evenly spaced frames ' + P + '/v3/film/out/contact_film.jpg (view it); the grammar recount of the plan (shots, transitions, framing changes per second) with the QA tools of ' + P + '/v3/shots/ in ' + P + '/v3/film/out/CONFORM.md together with the list of joins and anything missing.',
].join('\n')

const SOUND = [
  'Read ' + P + '/v3/film/BRIEF_FINISH.md now and follow it.',
  'YOUR TASK: the sound of the film. Write only under ' + P + '/v3/film/out/ and the deliver files named below.',
  'Build the mix spec ' + P + '/v3/film/out/mix_film.json for ' + P + '/audio/mixer.py from ' + P + '/v3/film/out/cues_all.json: the narration at +0.100 s with the stored voice gain; the music bed from the first frame to the end at the measured level with a short fade at the very end; and one effect per cue chosen from the library by what the cue describes (pencil and marker strokes, eraser rubs, whooshes for snaps and whips, thumps for impacts and stamps, the teletype, the whistled tune under the strolling boss, drizzle and room tone under the grey scenes, wind building under the mechanism and the storm, the wave roar and thunder at the disaster, the paper slide, the shimmer for the reveal of the label, the chuckle for the laughing seniors). Trim, fade and place each effect so its onset meets the cue; thin the cues where they would crowd (the reference has an effect every 2.5 to 3 seconds, about 25 in 65 seconds, plus ambiences); keep the first 5 seconds exactly as the approved hook mix. List the cues for which the library has no fitting sound; do not generate or download any sound.',
  'Run the mixer to produce ' + P + '/v3/film/out/film_mix.wav and the film with sound: ' + P + '/deliver/film_v1_thai.mp4 (picture stream copied from film_silent.mp4). Then measure the result and report: overall RMS, voice level, the level in the gaps between words, the number of effects placed, peak, and whether any effect exceeds -10 dBFS while the voice is speaking (use the caption phrase times as the speech map). Write ' + P + '/v3/film/out/SOUND.md with the placed-effects table (time, sound, level, cue).',
].join('\n')

const REVIEW = [
  'Read ' + P + '/v3/film/BRIEF_FINISH.md now.',
  'YOUR TASK: an independent review of the finished film ' + P + '/deliver/film_v1_thai.mp4 against the two reference clips. You built none of it; the client will compare it with his references on light, depth, camera angle, colour, story and sound. Write only under ' + P + '/deliver/ (the three files named below) and ' + P + '/v3/film/out/review/ .',
  'Measure: python3 ' + P + '/v2/eval/score.py on the film (it scores characters, tone, density, pacing and captions but is blind to light, shadows and perspective; read ' + P + '/v2/eval/README.md); python3 ' + P + '/v3/tools/hue_report.py on the frames of each take and of the whole film; the share of frame pairs a flat 2D move explains with ' + P + '/v3/shots/qa_parallax.py (reference 11 and 43 percent); the shot count, shot lengths, transition mix and interval between framing changes against the numbers in ' + P + '/spec/camera_motion.md; caption position and size; audio levels (voice, gaps, peaks) against BRIEF_FINISH.md.',
  'Look: extract a still every 0.5 s, and view contact sheets of the whole film next to contact sheets of the reference stills (' + P + '/ref/a and ' + P + '/ref/b). For each of the 26 shots say in one line whether it reads as the same film as the reference and what is the most visible difference. Check story clarity with the script (' + P + '/script_th_v2/script_en_gloss.txt): can each beat be understood from the picture, do the callbacks (the gloat framing, the label, the beach framing, the forecast paper) land.',
  'Deliver: ' + P + '/deliver/film_contact.jpg (48 frames of the film with time stamps above each frame), ' + P + '/deliver/film_vs_reference.jpg (six rows: light, depth, camera angle, colour, a character close-up, the disaster or exterior; each row one reference frame beside our closest frame), and ' + P + '/deliver/QA_film.md: the measured tables, the 26 one-line verdicts, and the ten largest remaining differences ranked by how much a viewer would notice, each with the take it belongs to and the cheapest fix. Do not change the film.',
].join('\n')

phase('Shots')
const lanes = await parallel([
  async () => {
    const m1 = await agent(M1, { label: 'map:mechanism-props-and-shot-19', phase: 'Shots', schema: SHOT_SCHEMA, model: 'opus' })
    const m2 = await agent(M2 + '\n\nThe previous worker reported (verify, do not trust):\n' + JSON.stringify(m1, null, 1).slice(0, 5000), { label: 'map:shots-20-21-22', phase: 'Shots', schema: SHOT_SCHEMA, model: 'opus' })
    return [m1, m2]
  },
  async () => {
    const c1 = await agent(C1, { label: 'beach:extension-and-shots-16-23', phase: 'Shots', schema: SHOT_SCHEMA, model: 'opus' })
    const c2 = await agent(C2 + '\n\nThe previous worker reported (verify, do not trust):\n' + JSON.stringify(c1, null, 1).slice(0, 5000), { label: 'beach:shots-8-24', phase: 'Shots', schema: SHOT_SCHEMA, model: 'opus' })
    return [c1, c2]
  },
])
phase('Conform')
const conform = await agent(CONFORM, { label: 'conform:join-captions-encode', phase: 'Conform', schema: OUT_SCHEMA, model: 'opus' })
phase('Sound')
const sound = await agent(SOUND + '\n\nThe conform worker reported:\n' + JSON.stringify(conform, null, 1).slice(0, 5000), { label: 'sound:mix-from-cues', phase: 'Sound', schema: OUT_SCHEMA, model: 'opus' })
phase('Review')
const review = await agent(REVIEW, { label: 'review:film-against-reference', phase: 'Review', schema: OUT_SCHEMA, model: 'opus' })
return { shots: lanes.filter(Boolean).flat(), conform, sound, review }
