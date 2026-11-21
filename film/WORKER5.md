# Render-team worker brief, film 5 (ไอ้เด็กเลี้ยงนก, coal mine + canary)

Follow film/WORKER.md (setup section 1, delivery section 4, rules section 5) exactly, with these film-5 differences:
- Brief: PROJ/film5/BRIEF.md. Shot plan: PROJ/film5/shot_plan.md — each shot names the reference second of PROJ/ref/a to copy
  (frame tNNNN.jpg, NNNN = 2*s+1): match camera height/angle, subject size, layering, move; a framing change every 1.0-1.5 s.
- Narration PROJ/film5/audio/narration_bankky.wav (65.0 s) at +0.10 s; captions PROJ/film5/script/captions.json. N = 1968.
- Set: PROJ/v3/set3d5/mine.py (mine_API.md, mine_REVIEW.md). Use M.setup_render (denoiser on, prefilter FAST). Actor-carried lamps:
  M.lamp_light keyed per frame.
- CLIENT RULES (mandatory):
  * NO depth of field, no background blur, anywhere: call M.setup_dof(scene, None, None, cam=...) for every camera (several mine cameras
    have DOF defaults — turn them off explicitly). Motion streak only on real whip moves, max 2-3 frames. The image must be sharp.
  * Whenever a character HOLDS the bird cage, use the cast's 2D held cage: pose prop_r="cage" + pose key "bird" (cast5 API, cage_svg /
    "canary_in_cage", bars drawn over the bird) so the bird is visibly inside the bars; hide the set's 3D cage in those shots. Only for a
    cage hanging on its hook / ECU inserts use the set's 3D cage with the canary sprite placed INSIDE the bars (check by eye at full size
    that the bird is behind the front bars and on the perch, never on top of or beside the cage).
  * The canary must stay gentle: fallen = eyes closed, never X eyes; it revives at the end.
- Worked example of THIS film: PROJ/v3/film5/s01/shot.py + QA.md + compare.jpg (same set, cast, clock, no DOF) — copy its structure.
- Cast: PROJ/v3/cast5 (alfie, gaffer, miner1-3, canary, cage, flame_lamp). Mouths move ONLY on the quoted lines: gaffer in shot 7 and
  shot 11, the mocking miner in shot 13. Song countdown via pose key "notes": 5, 3, 1, 0.
- Take folders: PROJ/v3/film5/sNN/ with shot.py, meta.json (first_g, n_frames, transition_in), cues.json, contact.jpg, QA.md,
  compare.jpg (one final frame per shot next to its reference frame), take.mkv. Push each take as soon as it is final.
