# Render-team worker brief, film 3 (ถังเหงื่อแตก, Boston 1919)

Follow film/WORKER.md (setup section 1, delivery section 4, rules section 5) exactly, with these film-3 differences:
- Brief: PROJ/film3/BRIEF.md. Shot plan: PROJ/film3/shot_plan.md. Narration PROJ/film3/audio/narration.wav (65.0 s) at +0.10 s;
  captions PROJ/film3/script/captions.json. N = 1968 frames.
- Set: PROJ/v3/set3d3/harbor.py (+ harbor_API.md, harbor_REVIEW.md: read the "what still differs" list). Cast: PROJ/v3/cast3 (API.md).
- Worked example of a take: PROJ/v3/film2/s01/shot.py (film 2, same pipeline) — copy its structure; build the harbor set instead of the tower.
- Take folders: PROJ/v3/film3/sNN/ (NN = first shot number of the take), same files as film 2 (shot.py, meta.json with first_g/n_frames,
  cues.json, contact.jpg, QA.md, take.mkv).
- Known set weaknesses to fix at runtime in your shot.py where your shots show them (do not edit harbor.py):
  * too few deep darks in sunlit close shots: frame a near foreground mass in shade (trestle girder, barrel, wall edge);
  * tank_low is a bare curved wall: add life (rivet rows in frame, ladder, a worker, the pipe) or pick a better angle;
  * the drip reads as a dark dot: make the drip a glossy elongated drop that falls (animate it);
  * the flood (shots 18-19 only) is a faceted height field: add a rolling front lip, spray/blobs and gloss highlights so it reads
    as a thick glossy molasses wave; people run ahead of it (no casualties shown).
- Characters: tommy (hero, small), foreman (mouth moves ONLY on his two quoted lines: shot 8 ~22.1-24.6 s, shot 12 ~35.3-37.3 s),
  worker1/2, kid1/2. head_flip by key side as in s01.
