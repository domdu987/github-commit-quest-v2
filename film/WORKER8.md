# Render-team worker brief, film 8 (ไอ้บ้าน้ำแข็ง — ice in the Persian desert)

Follow film/WORKER.md (setup section 1, delivery section 4, rules section 5) exactly, with these film-8 differences:
- Brief PROJ/film8/BRIEF.md (READ "USER TASTE": the user prefers the original look — wide/medium framings that show the beautiful set,
  calm but always-moving camera, warm lit 3D world, sharp, NO depth of field, few/no text signs). Shot plan PROJ/film8/shot_plan.md.
- Narration PROJ/film8/audio/narration.wav (60.8 s) at +0.10 s; captions PROJ/film8/script/captions.json; N = 1839; g = round(t*30).
- Set PROJ/v3/set3d8/desert.py (+ desert_API.md and its gaps), cast PROJ/v3/cast8 (+ API.md).
- WORKED EXAMPLE OF THIS FILM: PROJ/v3/film8/s01/shot.py + QA.md + compare.jpg + PROJ/v3/film8/common.py (READ its 10 gotchas: real Milky
  Way direction az 60-75 deg, lantern posts blocking the set's marks, narrow bank lanes, key everything every frame incl. ice state, pour
  ripples, looking-up expression, raised finger, medium camera height, moves must move, one location per process).
- DENSITY: the desert is sparse compared with the reference; dress every framing at runtime (palms, rocks, water jars, baskets, rope,
  campfire, tools, mud-brick piles, camel/donkey silhouettes far away, footprints) with the desert helpers — never edit desert.py.
- Mouths move only on quotes: merchant 14.4-17.9 and 37.0-38.9 s; merchant sheepish "ข้าจะซื้อหมดเลย" 59.8-60.8 s.
- Reveal (shot 17-19) inside the lit 3D world: heat wisps rising from the channel to a brilliant starry sky; make them soft shimmering
  ribbons, not long hard streaks (fade them, shorter, translucent).
- Take folders PROJ/v3/film8/sNN; meta.json with g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n}; render 6
  handle frames each side. take.mkv over 45 MB: split -b 40M take.mkv take.mkv.part . Push each take as soon as it is final.
