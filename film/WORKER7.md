# Render-team worker brief, film 7 (ไอ้มักกะโรนี, the Mona Lisa theft — Louvre 1911, Paris, attic room)

Follow film/WORKER.md (setup section 1, delivery section 4, rules section 5) exactly, with these film-7 differences:
- Brief: PROJ/film7/BRIEF.md. Shot plan: PROJ/film7/shot_plan.md (31 shots; match the reference look PROJ/ref/a, PROJ/ref/b; a framing
  change every 1.0-2.0 s — preset switches / punch-ins / hard cuts inside a take are fine).
- Narration PROJ/film7/audio/narration_bankky.wav (106.70 s) at +0.10 s; captions PROJ/film7/script/captions.json; sentence times
  PROJ/film7/audio/timing.json. N = 3219 frames (107.30 s). Shot boundaries g = round(t*30); in-shot events g = round((t+0.1)*30).
- Set: PROJ/v3/set3d7/louvre.py (+ louvre_API.md): build("louvre"|"paris"|"room", preset); hooks set_mona, set_mona_lift, set_queue,
  set_papers, set_door, set_frame_on_stairs, set_trunk, set_panel, set_flames (every frame); clear_keys() after build.
- Cast: PROJ/v3/cast7 (API.md; STORY7 poses; keys bulge, sweat, lie, panel_grip, panel_side, flip_text; props mona_panel, mona_framed,
  newspaper, key, lantern; SVG pieces mona_svg, hooks_svg, newspaper_svg, poster_svg, easel_svg).
- WORKED EXAMPLE OF THIS FILM: PROJ/v3/film7/s01/shot.py + QA.md + compare.jpg + PROJ/v3/film7/common.py (READ the gotchas at the top
  of common.py: hook keys, theft headlines (papers 0 before the theft is known = shots 1-17 except shot 3 which is a flash-forward),
  exit_door dressing via dress_corridor(), the corridor's two framed notices use headline textures — cover them at runtime in shots
  14-15, street gas lamps, vincenzo's height, walk-cycle tips, one location per process). Reuse common.py; do not edit it.
- CLIENT RULES (mandatory):
  * NO depth of field, no background blur anywhere; the image must be sharp. Motion streak only on real whip moves, max 2-3 frames.
  * Mouths move ONLY on quoted lines: the director in shot 6 (14.70-19.96), the coworkers' "ไอ้มักกะโรนี!" in shot 9 (~26.05-28.5).
  * Whole heads above y = 880; main head centre 0.35-0.59 H (wides exempt).
  * The young painter questioned in shot 20 is generic (striped shirt) — no likeness of a real person, no name on screen.
  * Dense sets: dress bare corners at runtime like s01 did.
- Take folders: PROJ/v3/film7/sNN/ (NN = first shot number of your take) with shot.py, meta.json (first_g, n_frames, transition_in =
  "cut" or "dissolve"), cues.json, contact.jpg, QA.md, compare.jpg, take.mkv. Push each take as soon as it is final.
- Render handles: 6 frames before and after your range in 3D.
