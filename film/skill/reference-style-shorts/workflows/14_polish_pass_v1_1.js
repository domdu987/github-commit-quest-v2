export const meta = {
  name: 'polish-film-v1-1',
  description: 'Polish pass (Opus): a light and colour grade with small story overlays, a corrected mix, then rebuild the film as v1.1 from the sharp v1 conform and review it against v1 and the reference',
  phases: [
    { title: 'Grade', detail: 'the grade module with the story overlays, measured on the v1 conform', model: 'opus' },
    { title: 'Finish', detail: 'grade, captions, mix, encode v1.1 (no new conform)', model: 'opus' },
    { title: 'Review', detail: 'two independent reviewers: look against the reference, and artifacts against v1', model: 'opus' },
    { title: 'Fix', detail: 'only if a reviewer finds something that must be fixed', model: 'opus' },
  ],
}

// EXAMPLE FROM FILM 1: rewrite the prompt texts (story, shots, lanes, sets, cast, paths) before use; keep the shape.
// A Workflow tool script (see the workflow-authoring skill). Replace __PROJ__ with the project path.
// model: 'opus' is the one-tier-down worker tier; the main conversation runs on the strongest model.
// See references/production.md, section "Adapting to a new film".
// Sharp picture: no depth-of-field blur (client decision). Film 1's first run of this template also built a 2D depth of field;
// the client had it removed, and this template no longer has those workers.
const P = '__PROJ__'   // replace with the project path before running
const F = P + '/v3/film'
const OUT = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
    numbers: { type: 'string' },
    problems: { type: 'array', items: { type: 'string' } },
  },
  required: ['files', 'summary', 'numbers', 'problems'],
}
const REVIEW = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['ship', 'ship_with_notes', 'fix_first'] },
    closer_to_reference_than_v1: { type: 'boolean' },
    must_fix: { type: 'array', items: { type: 'object', properties: { item: { type: 'string' }, where: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } }, required: ['item', 'where', 'evidence', 'fix'] } },
    notes: { type: 'array', items: { type: 'string' } },
    numbers: { type: 'string' },
    files: { type: 'array', items: { type: 'string' } },
  },
  required: ['verdict', 'closer_to_reference_than_v1', 'must_fix', 'notes', 'numbers'],
}
const head = 'Read ' + F + '/BRIEF_POLISH.md now and follow it exactly. It names what is frozen, what must not change and how version 1.1 is built.\n'

const GRADE = head + [
  'YOUR TASK: build the grade of version 1.1 as ' + F + '/out_v11/grade.py with the entry point grade_frame(img, g) -> img (PIL RGB 720x1280 in and out, g = film frame 0..1964), developed and measured on the conformed frames of v1: ' + F + '/out/frames/g_%04d.png (no captions). Write only in ' + F + '/out_v11/ (grade.py, grade_test/, GRADE.md). Another worker will later run your function over the same 1965 frames (v1.1 has no new conform), so it must be stateless and fast.',
  'What it must do is section 3 of the brief: the global light pass (bloom on light sources and bright areas so lamps, windows, the sun-lit sky and white paper glow instead of sitting as flat discs; a gentle S-curve; a light warm haze in the far distance of the exterior shots), the per-shot corrections (s16, s19, s20, s21, s25; shot ranges are in ' + P + '/plan/shot_plan.json and in each take meta.json; the join ranges in ' + F + '/out/work/joins.json: settings cross-fade over each dissolve), the fog bank in s23, the larger ghost storms in s21 only if cheap, and a fine grain only if it does not shimmer.',
  'Measure with the same tools as the review so the numbers are comparable: ' + P + '/v2/eval/score.py (the review output for v1 is in ' + F + '/out/review/score/; read how the review ran it in ' + F + '/out/review/) and ' + P + '/v3/tools/hue_report.py. Work on a sample (for example every 15th frame plus a dense run in each corrected shot), then state the targets reached: contrast p95-p5, share of pixels with V > 0.95, top-third and middle-third luma, saturation mean, head fill V, and the hue rows of the corrected shots, v1 against graded.',
  'Protect: the faces and hands of the characters (flat near-white fills must stay flat and must not clip or pick up a colour cast), the red line (still the same red), every Thai and English text in the picture (bloom must not wash out the forecast sheet, the label, the signs), and the caption band (captions are burned later on top, but the picture under them should not become so bright that white captions lose contrast).',
  'The bloom must be stable in time: no pumping when a bright object enters or leaves, no flicker from frame to frame. Check a strip of 10 consecutive frames in three places and one dissolve between two differently graded shots.',
  'Save before/after pairs for at least 12 shots next to the nearest reference stills (' + P + '/ref/a, ' + P + '/ref/b) in ' + F + '/out_v11/grade_test/ and look at them at full size. Write GRADE.md: what each stage does, its parameters, the numbers, and how long one frame takes (the function will run 1965 times; keep it under about 1.5 s per frame, and say how to run it in parallel).',
].join('\n')

const FINISH = head + [
  'YOUR TASK: build version 1.1 from the parts and deliver ' + P + '/deliver/film_v1_1_sharp_thai.mp4. Write only in ' + F + '/out_v11/ and that one file in deliver/ (plus the compare sheets named below).',
  '1. Input: the v1 conform frames ' + F + '/out/frames/g_%04d.png (1965 frames, no captions). There is no new conform and no depth of field: the picture stays sharp (client decision).',
  '2 and 3. Grade and captions in one pass without intermediate files, as ' + F + '/out_v11/make_sharp.py does: grade_frame of ' + F + '/out_v11/grade.py over all 1965 frames in 3 processes (also saved to out_v11/graded/), each frame piped into ffmpeg with the v1 caption file ' + F + '/out/film_silent.ass and the v1 encoder settings (libx264, crf 18, yuv420p) -> out_v11/film_silent_sharp.mp4, 1965 frames.',
  '4. Sound: section 5 of the brief (three changes only), mixed with ' + P + '/audio/mixer.py -> out_v11/film_mix.wav; measure the voice level, the music bed, the loudest non-voice peak while the voice speaks, and the drizzle bed, the same way ' + F + '/out/SOUND.md did. Mux -> ' + P + '/deliver/film_v1_1_sharp_thai.mp4 (video stream copied from out_v11/film_silent_sharp.mp4, AAC 192k).',
  '5. Check and report: ffprobe of the result; the score.py out-of-range rows of QA_film.md section 1.1 measured again on v1.1 beside the v1 numbers; the hue rows of the corrected shots; a contact sheet ' + P + '/deliver/film_v1_1_contact.jpg (48 frames) and a compare sheet ' + P + '/deliver/film_v1_vs_v1_1.jpg (12 moments: v1 frame, v1.1 frame, nearest reference still). Look at both.',
  'The workers before you reported (verify, do not trust):\n',
].join('\n')

const R_LOOK = head + [
  'YOUR TASK: an independent review of version 1.1 against the reference and against version 1. Change nothing in the film. Write only in ' + F + '/out_v11/review_look/ and the file ' + P + '/deliver/QA_film_v1_1.md .',
  'Files: v1.1 ' + P + '/deliver/film_v1_1_sharp_thai.mp4, v1 ' + P + '/deliver/film_v1_thai.mp4, the v1 review ' + P + '/deliver/QA_film.md with its working folder ' + F + '/out/review/ (reuse its scripts so the numbers are comparable), reference stills ' + P + '/ref/a and ' + P + '/ref/b.',
  'Answer with evidence: (1) Is v1.1 closer to the reference than v1 in LIGHT (glow, contrast, highlights, top-of-frame brightness) and in DEPTH (3D parallax, cast shadows, overlap, haze in the distance; the picture stays sharp by client decision, so do not ask for background blur)? Re-measure the out-of-range rows of section 1.1 and the hue table for the corrected shots. (2) Go through the 26 shots again with the same yes / partly / no question as section 3 of the v1 review and say which answers changed. (3) Did anything get worse: a shot that now looks less like the reference, colour that left the band, a face that picked up a cast, text that became hard to read, captions that lost contrast? (4) The ranked list of what still differs most from the reference after v1.1.',
  'Look at frames at full size, not only at numbers: at least 30 frames of v1.1 beside the same v1 frames and the nearest reference still. Write the report in the same plain style as the v1 review.',
].join('\n')
const R_ART = head + [
  'YOUR TASK: hunt for artifacts that the polish pass may have introduced. You are the last check before the client sees it: assume something is broken and try to find it. Change nothing in the film. Write only in ' + F + '/out_v11/review_artifacts/ .',
  'Files: v1.1 ' + P + '/deliver/film_v1_1_sharp_thai.mp4 and its frames before captions in ' + F + '/out_v11/graded/; v1 ' + P + '/deliver/film_v1_thai.mp4 and ' + F + '/out/frames/.',
  'Check, each with frame numbers and crops as evidence: halos, ink that turned grey or ghost outlines round the characters and held props; any softness that is not the motion streak of a fast camera move; bloom that flickers, pumps or pops from frame to frame (measure the frame-to-frame change of v1.1 minus the same change in v1 and look at the worst 20 places); a visible step at the start or end of a dissolve where the two takes are graded differently; banding in skies and walls; clipped or tinted faces; text in the picture that became unreadable (the label ทางด่วนพายุ, LONG ISLAND, the calendar, the forecast sheet ฝนตก ลมกระโชก, the 100 กม./ชม. sign); an overlay that looks pasted on (the fog bank in s23, ghost storms in s21); grain that shimmers; captions: same 104, same times, same size and position as v1 (compare the caption boxes of both films on 20 frames) and still clearly readable on the brighter picture; the first frame and the last frame; frame count, duration and audio/video sync against v1; sound: the voice level, any non-voice peak over -10 dBFS while the voice speaks, clicks at edits of the changed effect entries.',
  'For each fault say whether it is visible at normal speed on a phone (must fix) or only when stepping through frames (note). Say exactly which part to revert or weaken to remove it.',
].join('\n')

phase('Grade')
const grade = await agent(GRADE, { label: 'grade:light-and-colour-module', phase: 'Grade', schema: OUT, model: 'opus' })
phase('Finish')
const before = JSON.stringify({ grade }, null, 1).slice(0, 14000)
let finish = await agent(FINISH + before, { label: 'finish:grade-captions-mix', phase: 'Finish', schema: OUT, model: 'opus' })
phase('Review')
let reviews = await parallel([
  () => agent(R_LOOK, { label: 'review:look-against-reference', phase: 'Review', schema: REVIEW, model: 'opus' }),
  () => agent(R_ART, { label: 'review:artifact-hunt', phase: 'Review', schema: REVIEW, model: 'opus' }),
])
const must = reviews.filter(Boolean).flatMap(r => r.must_fix || [])
let fix = null, recheck = null
if (must.length) {
  phase('Fix')
  log(must.length + ' item(s) marked must-fix by the reviewers: one fix round.')
  fix = await agent(head + [
    'YOUR TASK: one fix round on version 1.1. Two reviewers found faults that are visible at normal speed. Remove each one by the smallest change: weaken a grade stage or an overlay in ' + F + '/out_v11/grade.py, or correct a mix entry in ' + F + '/out_v11/mix_film.json. Then rebuild (grade, captions, encode, mux with ' + F + '/out_v11/make_sharp.py) and replace ' + P + '/deliver/film_v1_1_sharp_thai.mp4. Keep a copy of the first v1.1 as ' + F + '/out_v11/film_v1_1_before_fix.mp4. Write in ' + F + '/out_v11/ and that file in deliver/. For every fault show a before/after crop and say what you changed. If a fault cannot be removed, revert that shot or stage to its v1 state.',
    'The faults:\n' + JSON.stringify(must, null, 1).slice(0, 9000),
    'How v1.1 was built:\n' + JSON.stringify(finish, null, 1).slice(0, 5000),
  ].join('\n'), { label: 'fix:remove-visible-artifacts', phase: 'Fix', schema: OUT, model: 'opus' })
  recheck = await agent(R_ART + '\n\nThis is a re-check after a fix round. The faults reported before were:\n' + JSON.stringify(must, null, 1).slice(0, 8000) + '\nConfirm for each whether it is gone, and look for anything the fix broke. Write in ' + F + '/out_v11/review_artifacts_2/ .', { label: 'review:re-check-after-fix', phase: 'Fix', schema: REVIEW, model: 'opus' })
}
return { grade, finish, reviews, fix, recheck }