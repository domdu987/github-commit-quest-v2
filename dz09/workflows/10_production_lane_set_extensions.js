export const meta = {
  name: 'produce-office-base',
  description: 'Production lane 2 (Opus): straighten the red track and re-render the hook, then in parallel the office props and cameras and the grey and storm light presets',
  phases: [
    { title: 'Track', detail: 'ruler-straight track, anchors, hook re-render and re-mix', model: 'opus' },
    { title: 'Extend', detail: 'office props and cameras; office_grey and office_storm presets', model: 'opus' },
  ],
}

const P = '__PROJ__'

const BASE = [
  'You are one worker on a 65 second animated film (720x1280, 30 fps, Thai narration) that must look like two reference clips (stills: ' + P + '/ref/a/ and ' + P + '/ref/b/). Read FIRST, in this order: ' + P + '/v3/film/CONVENTIONS.md (rules every worker follows), the parts of ' + P + '/plan/shot_plan.md that concern your task (the verified shot plan: shot rows, sets_needed, props_needed, inserts_needed, build order), and ' + P + '/v3/README.md (how the finished first 5 seconds were built). The office set: ' + P + '/v3/set3d/office3d.py, textures.py, API.md, REVIEW.md; its colours were just corrected to the reference hue make-up (' + P + '/v3/out/COLOUR.md explains the new palette, the per-surface ambient tints and the grade keys: keep that palette). The corrected hook is ' + P + '/v3/out/proto_v3.mp4 with contact_v3.jpg.',
  'The story: September 1938, U.S. Weather Bureau. A young forecaster rules a STRAIGHT red hurricane track on the wall map pointing north at New York; his boss rubs it out; he redraws it; the office nicknames the line "ทางด่วนพายุ" (the storm expressway); next morning is a grey drizzle and the boss gloats; then the film shows on the map itself why the line was straight (two walls of high pressure, one corridor) and the storm rides the line into New York.',
  'Rules: Blender 5.3 as a Python module (import bpy), Cycles CPU, no Freestyle; a final 720x1280 frame at 12 samples costs about 4.5-5 s and must stay under 6 s; iterate on 360x640 stills with 2 threads (other workers render at the same time on this 4-core machine); no network, no MCP or connector tools, no paid API calls. To look at an image use the Read tool (downscale to at most 1600 px); always look at your renders next to the reference frames. Your final message is consumed by a script: return the structured result only, with absolute paths.',
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

const TRACK = BASE + '\n\n' + [
  'YOUR TASK: build-order steps 0 and 11 of the plan. You are the ONLY worker allowed to edit ' + P + '/v3/set3d/office3d.py right now (copy it to v3/set3d/backup_before_straight/ first); also write under ' + P + '/v3/out/ and the one deliver file named below.',
  '1. Straighten the red track. The script says the line is ruler-straight ("ตรงเป๊ะ") and that is the point of the story, but the track on the map today is a curved hand-drawn stroke. Make it one dead-straight ruled line from the storm symbol off Florida north to New York with its arrow head at N.Y., drawn as a firm pencil-and-ruler line (thinner than today: the hook QA says the 0.038 D ribbon reads as a marker; follow the plan and props_needed for the width) while every public function keeps working: set_track(line, erase, frame), track_point(u), the anchors map_track and map_ny, the erase smudge. Re-export the anchors the plan asks for in step 0 (for example calendar_rect, label_rect, teletype_sheet) and document them in API.md.',
  '2. Check: render the camera stills, the set_track states 0, 0.25, 0.5, 0.75, 1 and the erase states; the line is straight to within 1 px on a square-on debug view; the N.Y. label and the storm symbol stay readable; hue_report.py on the stills stays inside the colour band.',
  '3. Render the hook again with the straight track exactly as v3/README.md describes (sh make.sh: all 150 frames, 12 samples, post, Thai captions, narration); keep the old outputs in v3/out/before_straight/. Do not change shots, timing, camera or acting; the pencil point must still ride the growing end of the line and the jab must still land on New York (run the registration and track-shadow QA tools of v3/shots and report the numbers). Look at the new contact sheet.',
  '4. Re-mix the sound into the new picture: first copy ' + P + '/deliver/opening_v3_3d_thai_sound.mp4 to ' + P + '/deliver/opening_v3_3d_thai_sound_before_straight.mp4, then run python3 ' + P + '/audio/mixer.py ' + P + '/v3/out/mix_opening.json .',
].join('\n')

const PROPS = BASE + '\n\n' + [
  'YOUR TASK (write only under ' + P + '/v3/set3d_ext/props/): build-order step 4 of the plan: everything the office_day shots (4, 5, 6, 7, 9, 10, 11, 12, 13, 14) need that the office set does not have yet, delivered as an EXTENSION MODULE office_props.py that imports office3d and adds to the scene after office3d.build() without editing office3d.py (the way ' + P + '/v3/cast/cast_ext.py extends the puppet). If one small change inside office3d.py is truly unavoidable, do not make it: describe it exactly in your result.',
  'Contents (read step 4, props_needed and the rows of those shots for the exact list and behaviour): the storm "spinner" symbol as a prop that can turn and travel along the track, the white chalk curve and the fan of ghost tracks that curve out to sea, the tick stamp, the ruler (as a set prop on the map and as something a hand holds), the Thai label quad that gets pinned above the arrow head, smudge control and eraser crumbs, the forecast sheet quad and the rubber stamp, the teletype paper feed, the calendar leaf swap with a flutter, the high-resolution map for the closest lens positions, and the new cameras the plan names (low_three, low_boss, G and G prime the gloat framings, insert_front, label_insert, persist_steps and the others in the shot rows), each as {loc, look_at, lens} in a cams dict, plus the track_shadow_report helper the plan mentions. Every animated thing gets a setter that can insert keyframes (frame=None sets it statically), like office3d.set_track.',
  'Paper artwork comes from ' + P + '/v3/paper/ (paper.py registry and tex/*.png: another worker is making it now). If an item you need is not there yet, check again every few minutes for up to 20 minutes; after that use a clearly marked placeholder card of the right size and list it in your result so it can be swapped by registry name.',
  'Prove it: a still from every new camera with two placeholder actors where the plan has actors (stage system: ' + P + '/v3/stage/API.md; cast: ' + P + '/v3/cast/API.md), a strip per animated prop at 5 states, debug markers for every new anchor, hue_report.py rows, and the cost of a final frame with all props present. Look at the stills next to the reference frames the plan names for those shots. Write API.md.',
].join('\n')

const LIGHT = BASE + '\n\n' + [
  'YOUR TASK (write only under ' + P + '/v3/set3d_ext/light/): build-order step 8 (presets only) of the plan: the two extra lights of the office, delivered as an EXTENSION MODULE office_light.py that imports office3d and changes the built scene without editing office3d.py: apply(preset) for "office_grey" (the next morning: an ordinary dull drizzle day; no sun patch, soft low-contrast daylight from the window, the lamps on and glowing, rain running down the window on an animated card; used by shots 17-22, where the boss gloats and then the camera dives into the wall map) and "office_storm" (shot 25: office_grey darkened, lightning-ready: a flash(amount, frame) setter), plus the window rain card with a setter, and anything else step 8 lists that is light (not props, not shots).',
  'Look: there is no rainy interior in the reference, so stay inside the film palette (' + P + '/v3/out/COLOUR.md and the colour section of CONVENTIONS.md): shade blue-violet, real deep darks, warm red-brown woods still warm, white heads still the brightest large shapes, no neutral grey mud; office_grey must feel flat and a little sad next to the sunny office_day, and it must stay readable for a 7 second take on the wall map (shots 19-22 have no actors: the map must look good in this light from very close). State the numbers you chose and report hue_report.py rows per preset.',
  'Prove it: the main cameras (eye_two_shot, low_medium, insert_rake, high_two_shot, wide_high) in office_day, office_grey and office_storm side by side with two actors from the stage system, a flash strip, the rain card at 4 times, head fill and ink colour on screen in each preset, wall luminance around the heads, and the cost of a final frame per preset (under 6 s). Write API.md.',
].join('\n')

phase('Track')
const track = await agent(TRACK, { label: 'track:straight-line-and-hook', phase: 'Track', schema: SCHEMA, model: 'opus' })
phase('Extend')
const ext = await parallel([
  () => agent(PROPS + '\n\nThe track worker reported (verify, do not trust):\n' + JSON.stringify(track, null, 1).slice(0, 6000), { label: 'extend:office-props-and-cameras', phase: 'Extend', schema: SCHEMA, model: 'opus' }),
  () => agent(LIGHT + '\n\nThe track worker reported (verify, do not trust):\n' + JSON.stringify(track, null, 1).slice(0, 6000), { label: 'extend:office-grey-and-storm-light', phase: 'Extend', schema: SCHEMA, model: 'opus' }),
])
return { track, props: ext[0], light: ext[1] }
