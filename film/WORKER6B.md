# Render-team worker brief, film 6b (ไอ้สิบสาม — 65 s remake on the channel formula)

Follow film/WORKER.md (setup section 1, delivery section 4, rules section 5) and film/WORKER6.md (set, cast, common.py gotchas) with these
differences:
- READ FIRST: film/analysis/DIRECTOR_REVIEW.md and look at film/analysis/sheets/*.jpg (1 frame per second of 8 hit reference shorts).
  That is the look and pacing to hit: word-literal pictures every ~1-1.5 s, big faces (head 40-70% of frame width), loud expressions on
  Henry, Thai text signs as props, complementary colour (cool counter-colour in the warm bakery), camera always moving.
- Shot plan: PROJ/film6b/shot_plan.md (31 shots). Narration PROJ/film6b/audio/narration.wav (64.40 s) at +0.10 s; captions
  PROJ/film6b/script/captions.json; N = 1941. g = round(t*30). Our earlier film-6 takes (film/v3/film6/sNN/shot.py) are a code library you
  may copy from, but every frame must be rendered new for this clock.
- Thai signs: render text with the project's SVG -> PNG raster path (cast SVG pieces / PropCard in film/v3/film6/common.py) using the
  Kanit font in film/fonts; bold, readable at phone size, ink outline like the set.
- Expressions: henry_yell (purple face + steam), henry_laugh_smug, henry_pale (+ sweat), henry_in_pillory; tomato_svg(squash) for splats.
- Diagram shots (26-27): a 2D cutaway loaf card on a clean cool-blue backdrop inside Blender (emission cards), tiny blue water-drop cards
  rising out of the crumb into white steam — clear, simple, readable in one glance.
- Ending: cut exactly on the last frame g 1940 (no hold, no fade).
- Take folders PROJ/v3/film6b/sNN (NN = first shot of the take); meta.json with g0, g1, first_g, n_frames, transition_in {"type":"cut"|
  "dissolve","frames":n}. Mostly hard cuts (the references cut hard); dissolves only for time jumps. Render 6 handle frames each side.
- Push each take to your branch as soon as it is final; take.mkv over 45 MB: split with `split -b 40M take.mkv take.mkv.part` (the
  director rejoins parts).
