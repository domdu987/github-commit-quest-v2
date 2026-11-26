export const meta = {
  name: 'office-colour-fix',
  description: 'Correct the office set colours to the reference hue make-up at the source, re-render the 5 s opening and re-mix its sound',
  phases: [
    { title: 'Fix', detail: 'retune materials, ambient and grade against the measured hue targets; re-render and re-mix the opening', model: 'opus' },
  ],
}

// EXAMPLE FROM FILM 1: rewrite the prompt texts (story, shots, lanes, sets, cast, paths) before use; keep the shape.
// A Workflow tool script (see the workflow-authoring skill). Replace __PROJ__ with the project path.
// model: 'opus' is the one-tier-down worker tier; the main conversation runs on the strongest model.
// See references/production.md, section "Adapting to a new film".
const P = '__PROJ__'

const PROMPT = [
  'CONTEXT',
  'We are producing a vertical animated short (720x1280, 30 fps) that must look like two reference clips. Reference stills every 0.5 s: ' + P + '/ref/a/tSS.S.jpg and ' + P + '/ref/b/tSS.S.jpg. The first 5 seconds are finished in true 3D: ' + P + '/v3/out/proto_v3.mp4 (frames in v3/out/frames/, contact sheet contact_v3.jpg, QA.md, README at ' + P + '/v3/README.md explains how the film is built and rendered: shots in v3/shots/, the office set in v3/set3d/office3d.py with API.md and REVIEW.md, the staging system in v3/stage/).',
  'THE CLIENT VERDICT on that clip: very good, but THE COLOURS ARE NOT YET LIKE THE REFERENCE. I measured why with python3 ' + P + '/v3/tools/hue_report.py <frames or stills> (share of chroma per hue family, caption band excluded; it prints the reference rows, the target band and your rows):',
  '  reference A interiors: red 40.1 orange 27.6 blue 21.9 violet 1.1 magenta 8.6, saturation 0.47, value 0.55, dark share 0.09',
  '  reference B interiors: red 36.3 orange 37.7 blue 13.9 violet 4.5 magenta 5.1, saturation 0.38, value 0.45, dark share 0.15',
  '  OUR opening frames:    red 38.8 orange 21.9 blue 8.8 violet 3.1 MAGENTA 24.8, saturation 0.46, value 0.52, dark share 0.04',
  '  OUR set stills:        red 37.4 orange 17.1 blue 11.1 violet 4.8 MAGENTA 28.0, dark share 0.03',
  'So the picture is far too magenta and pink-purple (rose wallpaper, purple ceiling, every shade tinted magenta by the violet ambient: the set review measured shade hues of 302-326 where the reference shade on warm surfaces is about 252), it has too little blue, too little orange-brown, and almost no deep darks. Look at the reference interiors to see the difference with your own eyes: a/t27.5, a/t32.0, a/t34.0, b/t07.0, b/t18.5, b/t24.5 next to v3/set3d/still_*.png and v3/out/contact_v3.jpg.',
  '',
  'YOUR TASK',
  '1. Fix the colour AT THE SOURCE in ' + P + '/v3/set3d/office3d.py (and textures.py if needed), preset INTERIOR_DAY: first copy the current files to v3/set3d/backup_before_colour/. Retune albedos, the ambient term, the key colour and any grade so that, on the ten camera stills with two actors AND on the opening frames, hue_report.py lands inside the target band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10 (aim 5-9), saturation 0.38-0.48, value 0.45-0.63, dark share 0.08-0.15. Directions that follow from the reference: the wall behind the actors warm red to terracotta or red-brown rather than rose-pink; ceiling and woodwork brown and orange-brown rather than purple; shade on warm surfaces must turn BLUE-violet (hue 240-260), not magenta: make the ambient bluer and less red, and check the measured shade hue; give the frame more blue (the navy rug and cabinets as real saturated blue, the window sky, blue-violet floor shade) and real deep darks (plum-navy, not black) in corners, under furniture and at the frame bottom.',
  '2. Do NOT lose what already matches (re-measure with the set review scripts in v3/set3d/review/ and the numbers in REVIEW.md and v3/out/QA.md): same-surface shade at 0.15-0.31 of lit, shadow edges, bloom halo only on emitters, the map readable with the red track and N.Y. label clear, white heads the brightest large shapes (head fill on screen near #fef7f6, ink near #3a2832, identical in sun and shade), wall luminance around heads 95-170, edge density, the render cost (a final frame about 4.5-5 s at 12 samples).',
  '3. Work in passes: change, render the camera stills small, run hue_report.py, VIEW the stills next to the reference interiors, repeat. Numbers alone are not enough: it must also look like the same film as the reference when you look at it. Stop when the band is met and it looks right; say exactly which numbers remain outside.',
  '4. Re-render the whole opening with the corrected set, exactly as v3/README.md describes (all 150 frames, final quality, post, Thai captions, narration mux), so that v3/out/proto_v3.mp4, proto_v3_silent.mp4, frames/, contact_v3.jpg, compare_v3.png and aspects_v3.png are replaced by the corrected versions (keep the old ones in v3/out/before_colour/). Do not change shots, timing, camera or acting.',
  '5. Re-mix the sound into the corrected picture by running: python3 ' + P + '/audio/mixer.py ' + P + '/v3/out/mix_opening.json  (it reads v3/out/proto_v3_silent.mp4 and writes ' + P + '/deliver/opening_v3_3d_thai_sound.mp4; first copy the current deliver file to deliver/opening_v3_3d_thai_sound_before_colour.mp4).',
  '6. Deliver ' + P + '/v3/out/colour_before_after.jpg: three rows (insert, low angle, two-shot), each with the best matching reference interior frame, the frame before the fix and the frame after; and ' + P + '/v3/out/COLOUR.md with the hue_report table before and after, the changes you made (old and new hex values and light settings) and the re-measured light numbers.',
  '',
  'RULES: write only under ' + P + '/v3/ and the two deliver files named above. Do not call any MCP or connector tools; no network. Blender 5.3 as a Python module, Cycles CPU, no Freestyle. Other agents render on this 4-core machine at the same time: iterate on small stills with 2 threads; render the final frames in a way that can resume. To look at an image use the Read tool (downscale to at most 1600 px). Your final message is consumed by a script: return the structured result only.',
].join('\n')

const SCHEMA = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'string' } },
    hue_before: { type: 'string' },
    hue_after: { type: 'string' },
    changes: { type: 'string' },
    light_recheck: { type: 'string' },
    remaining_out_of_band: { type: 'array', items: { type: 'string' } },
  },
  required: ['files', 'hue_before', 'hue_after', 'changes', 'light_recheck', 'remaining_out_of_band'],
}

phase('Fix')
const r = await agent(PROMPT, { label: 'fix:office-colour', phase: 'Fix', schema: SCHEMA, model: 'opus' })
return r
