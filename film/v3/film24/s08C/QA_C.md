# QA_C s08C (build-up, look C, preset build_dock), g 734-1125 + 6 handles (728-1131)
- Render: JOSEON_LOOK=C, 24 samples, 540x960 + J.post -> 720x1280, 404 frames, ~47-50 s/frame wall per process (2 procs x 2 threads). No cast (no people in the take).
- Camera: J.build_cam orbit. Changes from the draft, all in shot_C.py: (1) gobo_rig_* shadows off (they cast a dark vertical streak through the haze above the ship; director note); (2) camera tightened up to 18 % toward the look point on stages 2-3 (g 815-888, eased) so oars/guns read; (3) an eased intro slide (2.4 D, g 728-806, ending at the nominal camera) because the orbit's ease-in left g 728-781 frozen (qa_auto frozen-run FAIL).
- qa_auto (QA_AUTO_C.md): frozen runs none. Only remaining FAIL is "suspected blur" (130 frames): the look is soft haze/god-ray by design (sky and water), the ship edges are sharp in full-size frames. Pops at g 899 and 1052 are the planned events (roof drop with dust, mouth-gun flash).
- qa_jitter: overall median jitter 0.2 px, no shake.
- Stage cues follow J.build_schedule (hull 781, oars 830, guns 862, roof 898, spikes 932, gwimyeon 971, dragon 1001, mouth gun 1041 (flash ~1052), hero 1084).
- build_anchors.json: per frame {g, stage, x, y} px at 720x1280 from J.build_anchor.
- Not verified by eye: every frame; reviewed stills of each stage and the contact sheet (contact_C.jpg), phone_sheet_C.jpg.
