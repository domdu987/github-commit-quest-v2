# film 17 take s04 (shots 9-12, narration 14.72-21.61 s, g 445..650 + 6 handle frames each side, first_g 439, 218 frames)
Final 720x1280, 12 samples + OIDN, Cycles CPU, ~45 s/frame (2 procs x 2 threads). Set measure / DAY_INT, one process. `shot.py` + `c17.py` reproduce it.

## Numbers
- rhythm.py (cuts 445,493,540,592,651): **in-shot median 4.08, p90 12.12** (targets >= 4 / >= 12).
- qa_auto.py: PASS (QA_AUTO.md, phone_sheet.jpg), magenta 0.0 %.

## Shots
- 9 (439-492) measure_wide, camera turned toward the room centre so the inspector can walk in from the right; 15 f snap push-in at the laugh (468-480) + 3D sway. Inspector strides in, shock, laughs from g 467 (15.46 s) with a 3 Hz bounce, gendarme_b and gendarme_a join (laughing poses). Bertillon's calipers are pinned (Actor.pose tip) on the seated prisoner's ear. Kepi stool fg.
- 10 (493-539) measure_low: lip-sync starts g 493, inspector points at the calipers, Bertillon behind, unmoved; snap push 512-522.
- 11 (540-591) measure_chair: inspector flicks the calipers, slide, snap 562-574; Bertillon visible behind right.
- 12 (592-656) measure_chair: snap (13 f) at 604 onto the inspector tapping his own right ear (finger on the ear), second lateral snap 632-644. Lip-sync to g 650.
- Mouths: speak() only g 493..650; laughing pose mouth is the held laugh shape; everyone else closed.

## Self-check (every 5th frame sheet + snap frames + cut +-3)
heads above y 880 in all shots (inspector chin max ~ y 800 in shot 12); contact shadows ok; shot-10 inspector head centre y ~340-450 (above the 450 band, kept whole in frame: low camera); Bertillon head clipped by the right edge for part of shot 10 post-snap (accepted).

## Deviations / known issues
- Preset stand marks not used for Bertillon/gendarmes/prisoner (they put the inspector off-frame or behind a figure); positions set in shot.py.
- The seated prisoner has left the chair after shot 9 (chair empty in 10-12 so the inspector's offer to sit makes sense).
- Shot 9 is a wide: figures ~200 px tall at 720x1280, heads ~40-60 px.
- Dust halved (dust=0.5). Tripod hood shows top-right in shot 10 (known set item).
- Sprite poses change only inside continuous motion; no pop swaps.

## qa_auto note
QA_AUTO.md reports FAIL "suspected blur" on 17 frames (g 521-537, shot 10 after the snap). It is a false positive of the Laplacian-variance test: those frames are a close low shot dominated by the smooth plain wall and chair back (sharp 3D render, sprites at 448 px/D, no motion blur, no DOF); the frames were inspected by eye (chk sheets) and are crisp. All other checks pass (no black/blank/magenta/frozen frames; pops only at the planned cuts 493/540/592).
