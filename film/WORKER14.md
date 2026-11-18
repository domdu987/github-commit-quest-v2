# Render-team worker brief, film 14 (ไอ้บ้าผึ้ง — beehive fence vs elephants, Kenya)

Follow film/WORKER.md exactly for section 1 (setup: the PROJ symlink to the repo's film/), section 4 (delivery) and section 5 (rules). The film 14 differences are below. Your branch was checked out from film14/main; push to YOUR outcome branch only.

## Inputs
- **Brief and shots:** PROJ/film14/BRIEF.md, PROJ/film14/shot_plan.md (30 shots; your team's takes are in the table at the bottom), PROJ/film14/NOTES.md (client notes from film 10).
- **Narration:** PROJ/film14/audio/narration.wav (70.0 s) at +0.10 s. **Captions:** PROJ/film14/script/captions.json. **Frames:** N = 2106, g = round(t*30).
- **Look:** wide or medium framings that show the dense set, a calm camera that is always moving, and a warm lit 3D world. Sharp, NO depth of field, no text.

## Set (client-approved 2026-11-18): PROJ/v3/set3d14/farm.py
- READ PROJ/v3/set3d14/API.md first (Round 2 and Round 3 sections), plus QA_RECHECK.md for the open notes.
- Light states: DAY, MORNING, DUSK, NIGHT. Presets are listed in API.md.
- Hooks: set_fence_stage, set_wire_push, set_bees, set_uncle_field, set_uncle_hive, set_crowd_props. Hooks are immediate: call them for EVERY frame.
- **Call bpy.context.view_layer.update() before set_bees**, or the bees are built at the origin and are invisible.
- The placeholder cards in the set are stand-ins. Hide them and put real cast14 cards at the stand points.

## Cast: PROJ/v3/cast14 (read API.md)
- Members: farmer14, uncle14, woman14, kid14, oldman14, youth14, matriarch, elephant_b/c/d, calf, bees, props. STORY14 holds every pose key.
- Canvases:
  - elephants: full CANVAS14 at px_per_D 96-128 (160 for close shots)
  - CANVAS14_STOOL for every stool=1 pose
  - CANVAS14_CLOSE for uncle_stung_close
- Lip-sync: talk mouths ONLY for the uncle, inside 15.38-22.07 and 39.03-40.80 (narration s). Every other mouth is still or a held shape.
- `nose_swell`: re-add it to tweened poses, because lerp_pose drops custom keys.

## THE worked placement code: PROJ/v3/set3d14/cast_test/cast_test.py
This script rendered the client-approved test stills (cast_test/elephants_test.jpg). Copy its `put()` helper (sprite -> metre card, anchor placement, contact shadow) and its cameras into your own helper module in your take folder.
- s1 = fence_low_night, the matriarch arriving.
- s2 = the LOW push_side: push point x 10.25, chest_push on the wire, max bow at wire t about 0.11-0.12.
- s2b = the hive-row cut-away.
- s3 = trunk_close: the camera is pulled back 3.4 m at 24 mm.
- Bee targets must use the REAL puppet anchors (eye about 3.3 m up), not farm.py's MATRIARCH_EYE / bloc constants.
- Also read PROJ/v3/film8/common.py and PROJ/v3/film8/s01/shot.py for the take structure, keyframing and gotchas: moves must move, key every hook every frame, one location per process. Make your OWN helper in your take folder, for example film/v3/film14/sNN/c14.py. No shared common.py.

## Hard rules for this film
- **Elephant cameras:** never look steeply down on an elephant card. Keep the card within about 25° of facing the camera and the camera at 2.5 m or lower when an elephant is in frame. The client rejected a high view because the elephant read as flat.
- **Parenting:** a person on a ladder or stool is parented to it and must not slide.
- **Dust and smoke:** a spray crown with droplets and wisps, never a stack of round white blobs.
- **Bees:** dense bursts that read as "thousands", gold-black with wing blur. They must not cover the elephant's face entirely.
- **Comic only:** no injury, and the elephants are unhurt.
- **Heads above y 880;** a new framing every 1.5-2.5 s; never static for more than 6 frames.
- **Cost:** about 25-45 s per final frame at 24 samples on 4 cores. Run at most 2 processes with 2 threads each.
- **Draft first:** 360x640 at 6 samples, then a contact sheet, then final.

## QA (stricter, film/QA_TEAM.md "Stricter QA")
1. Run `python3 film/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>` and fix every FAIL.
2. Add QA_AUTO.md and phone_sheet.jpg to the take folder.
3. Check every frame yourself at 6 fps, plus every cut ±3 frames, for:
   - heads above y 880
   - contact shadows
   - props held in hands
   - eye-lines
   - continuity with the neighbouring takes
   - mouths only in the quote windows
   - nobody sliding on a ladder or stool
   - no steep down-view on elephants

## Delivery
- Take folders: PROJ/v3/film14/sNN.
- meta.json holds g0, g1, first_g, n_frames and transition_in {"type":"cut"|"dissolve","frames":n}.
- Render 6 handle frames each side.
- If take.mkv is over 45 MB, split it: `split -b 40M take.mkv take.mkv.part`.
- Push each take as soon as it is final. Do not open pull requests.
- Work autonomously. Do not ask for confirmation: the client has already approved the set, the cast and the render (2026-11-18).
- End with a short report: takes, frame ranges, s/frame, and anything that differs from the plan.
