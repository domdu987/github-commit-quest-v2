# Render-team worker brief, film 23 ("ไอ้กองทัพลูกโป่ง": the WWII Ghost Army, 1944-45)

Follow film/WORKER.md for section 1 (setup), section 4 (delivery) and section 5 (rules). The film-23 differences are below.
In WORKER.md, read every `film2` path as `film23`. Takes go in PROJ/v3/film23/sNN (NN = the shot number).
Process: film/skill_film13 (the skill as used for films 1-13). The only checks are the free automatic scripts listed in "QA" below.

## Inputs
- **Shot plan:** PROJ/film23/shot_plan.md has 19 shots; each team renders only its own shots. Read FACTS.md and script/script_th.txt too.
- **Set:** PROJ/v3/set3d23/ghost.py. READ API.md first: locations, the per-shot cameras S01..S19 with their keyed moves, marks, setters,
  and the helpers `ground_snap` and `contact_shadow`. Look at set_sheet.jpg and NOTES.md.
- **Cast:** PROJ/v3/cast23/cast23.py. READ API.md and look at cast_sheet.jpg and cycles.jpg.
- **Worked example of the pipeline:** PROJ/v3/film8/s01/shot.py + QA.md and PROJ/v3/film8/common.py.
  - Copy common.py into your take folder as c23.py, switch it to cast23 and set3d23, and use it.
  - There is no shared film23/common.py.
  - The rules from film 8 hold: moves must move, key every animated hook on every frame, one location per process.

## Clock: TIMING IS AN ESTIMATE
The narration is not recorded yet (fal.ai is out of balance). Shot times come from PROJ/film23/audio/timing_EST.json and the plan table.
- `g0 = round(t0*30)` and `g1 = round(t1*30)`, using the plan's est. times.
- **Render g0 .. g0 + ceil((g1-g0)*1.25)**, then add handles. The camera move continues, eased, into the extra 25 % tail.
  Action must stay alive through the tail, because conform trims it to the real narration later.
- Handles: on each dissolved side, half the dissolve + 2 frames; 6 frames if unsure.
- In meta.json, record g0, g1 (planned), g1_render (with tail), first_g, n_frames, and transition_in {"type":"cut"|"dissolve","frames":n}.
- Lip-sync: only the Major in S07 and the smiling GI in S13 move their mouths.
  - Use a talk cycle over the shot's whole quote part, with `talk_mouth` driven by a synthetic loudness: a 4-6 Hz pattern with pauses.
  - Everywhere else, mouths are still.

## Look (client rules)
- Sharp picture with NO depth of field.
- Wide and medium framings that show the dense lit set. Close-ups only as a quick punch-in.
- Heads must sit fully above y 880, the caption band.
- Text signs are allowed: the set has them.
- Signature colours: olive and khaki against bright green and a blue dawn; warm lanterns at night.
- **Camera rhythm (film 2):** every shot has a clear eased push or pull of 6-10 %/s, plus a lateral slide of about 40 px/s.
  - Quick push-ins on punch lines.
  - Median in-shot frame-diff ≥ 4 and p90 ≥ 12, measured on 90x160 grey frames. Put the numbers in QA.md.
- **NO CAMERA SHAKE.**
  - Eased keys only: no random or noise keys on the camera.
  - Every second must be ≤ 2.0 px in `python3 PROJ/qa_jitter.py take.mkv`. Paste its output in QA.md.
- **NOTHING FLOATS.**
  - Every character card and every free prop touches a surface and has a contact shadow. Use the set's ground_snap/contact_shadow.
  - The ONLY airborne thing is the rubber tank lifted over the heads in S12/S13 (flag it airborne), plus balloons in S19.
- **Characters always act.** Nobody stands frozen: secondary motion, blinks, bounce on laughs.
- **Comic and bloodless.** No weapon is ever fired and nobody is hurt. The cyclist "falls" by sitting down dazed.

## QA (automatic only; fix every FAIL before delivering)
1. Before the final render, run `ground_check.py` on your built scene: PROJ/v3/tools/ground_check.py; read its header for the pip-bpy usage.
   - Use `--every 10`.
   - Fix until it passes, then save the report as GROUND.md in the take folder.
2. After the render, run `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <cut g's inside the take, if any>`.
   - Fix every FAIL.
   - Add QA_AUTO.md and phone_sheet.jpg to the take folder.
3. After the render, run `python3 PROJ/qa_jitter.py take.mkv`. Every second must be ≤ 2.0 px.
4. Look at your own contact sheet at 6 fps. Check:
   - heads above y 880
   - feet and props on the ground
   - props held in hands
   - mouths moving only in the quote windows
   - continuity with the plan: time of day, tank inflation state, costumes
5. Write all of the above in QA.md.

## Delivery
- Push each take to your outcome branch as soon as it is final. Do not open pull requests.
- If take.mkv is over 45 MB, split it with `split -b 40M`.
- Work autonomously and do not ask for confirmation. The look and set were approved by QA-art, and the director's go is this brief.
- Final message: the takes delivered, frame ranges, seconds per frame, and anything that differs from the plan.
