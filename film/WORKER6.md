# Render-team worker brief, film 6 (ไอ้สิบสาม, the 13th loaf — medieval bakery + market)

Follow film/WORKER.md (setup section 1, delivery section 4, rules section 5) exactly, with these film-6 differences:
- Brief: PROJ/film6/BRIEF.md. Shot plan: PROJ/film6/shot_plan.md (35 shots; match the reference look PROJ/ref/a, PROJ/ref/b; a framing
  change every 1.0-2.0 s — camera preset switches / punch-ins inside a take are fine and encouraged).
- Narration PROJ/film6/audio/narration_bankky.wav (105.85 s) at +0.10 s; captions PROJ/film6/script/captions.json; sentence times
  PROJ/film6/audio/timing.json. N = 3194 frames (106.45 s). Shot boundaries g = round(t*30); in-shot events g = round((t+0.1)*30).
- Set: PROJ/v3/set3d6/bakery.py (+ bakery_API.md): build("bakery"|"market", preset), light presets MORNING / AFTERNOON, hooks set_steam,
  set_oven (call every frame), set_scale / set_scale_loaf, set_big_scale (story beat: -7 short, then ease to +6 pass), set_loaves.
- Cast: PROJ/v3/cast6 (API.md; cast6.STORY6 poses; props loaf/basket/cabbage/tomato/spear; pillory pose key; hood key; cycles walk/run/
  sneak/march; talk_mouth; blink_at). Standalone SVG pieces (loaf_svg, loaf_pile_svg, basket_svg, tomato_svg, pillory_svg) for set props.
- WORKED EXAMPLE OF THIS FILM: PROJ/v3/film6/s01/shot.py + QA.md + compare.jpg + PROJ/v3/film6/common.py (READ the gotchas at the top
  of common.py: held_on_palm, PropCard, kit on a hidden stool behind the counter, custom counter camera, steam <=0.35 near faces,
  key_set() every frame). Reuse common.py; do not edit it — copy helpers into your shot.py if you need changes.
- CLIENT RULES (mandatory):
  * NO depth of field, no background blur anywhere; the image must be sharp. Motion streak only on real whip moves, max 2-3 frames.
  * Mouths move ONLY on quoted lines: Henry shot 11 (26.32-31.09) and shot 16 (41.29-44.50); kit shot 27 (shout); townsfolk laugh in 12.
  * Heads above the caption band (whole heads above y = 880); main head centre 0.35-0.59 H (wides exempt).
  * Comic, not cruel: rotten veg splats are cartoon splats; the pillory is humiliation, no injury.
  * Continuity: kit = flour-covered boy; Henry = round bald baker; inspector hooded until shot 23 (hood drop -> cut to inspector_royal on
    a blink); the 13th loaf is the paler one (set_loaves 13).
- Take folders: PROJ/v3/film6/sNN/ (NN = first shot number of your take) with shot.py, meta.json (first_g, n_frames, transition_in =
  "cut" or "dissolve"), cues.json, contact.jpg, QA.md, compare.jpg, take.mkv. Push each take as soon as it is final.
- Render handles: render 6 frames before and after your range in 3D (needed for dissolves and trims).
