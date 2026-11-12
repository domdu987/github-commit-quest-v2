# Render-team worker brief, film 4 (เจดีย์เมา, old Japan pagoda)

Follow film/WORKER.md (setup section 1, delivery section 4, rules section 5) exactly, with these film-4 differences:
- Brief: PROJ/film4/BRIEF.md. Shot plan: PROJ/film4/shot_plan.md — every shot names the reference second of PROJ/ref/a whose framing
  and camera move you must copy (frame tNNNN.jpg, NNNN = 2*s+1, 4 digits): look at it at full size before staging and match camera
  height/angle, subject size, foreground/background layering, move, and a framing change every 1.0-1.5 s.
- Narration PROJ/film4/audio/narration_bankky.wav (65.0 s) at +0.10 s; captions PROJ/film4/script/captions_bankky.json. N = 1968.
- Set: PROJ/v3/set3d4/pagoda.py (v2; read pagoda_API.md incl. section 1b and pagoda_REVIEW2.md). It already has all dressing, the open base,
  the warm interior and the centred runner: do NOT add dressing twice. Use G.setup_dof for close/medium shots (values like s01).
- Worked example of THIS film: PROJ/v3/film4/s01/shot.py + QA.md + compare.jpg (same set, cast, DOF, clock) — copy its structure.
- Cast: PROJ/v3/cast4 (kenta, master, merchant, woman2, farmer). Mouths move ONLY on the quoted lines: master in shot 8 and shot 13,
  the mocking townsman's shout in shot 15. head_flip by key side as in s01.
- Keep set_sway amp <= 1.2. Collapse (shot 16): use set_collapse; dust must read as a big column like ref a t0095/t0097.
- Take folders: PROJ/v3/film4/sNN/ with shot.py, meta.json (first_g, n_frames, transition_in), cues.json, contact.jpg, QA.md,
  compare.jpg (one final frame per shot next to its reference frame), take.mkv. Push each take as soon as it is final.
