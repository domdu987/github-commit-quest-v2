# film17 s03 (shots 7-8, g 336..445; take.mkv = g 330..450, 121 frames) -- round 2
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg); magenta 0 %; planned cut g390 flagged only by the coarse metric (aisle -> desk is a real hard cut, seen in contact.jpg).
- rhythm.py take.mkv --first_g 330 --cuts 390: in-shot median 4.51, p90 13.28 (pass). Shot 7: drift pull-out + two snaps (g344-356, g366-378, pans right, camera moves away from the left-wall bracket); shot 8: orbit around the cards (-20 deg drift, -14 deg snap g418-431).
- Round-2 fixes (director QA_TECH s03): (1) bracket bloom gone: no white disc in g375-389 (snaps pan away from the bracket); (2) both photo cards fully in frame g390-450, x 40..646 of 720 (>=5 % margin), cards turn to face the camera, bigger, same tone, bold moustache on the right card; no push toward the clerk; clerk head R 68-76 px (<= 20 % of frame); (3) cuff attached to the wrist, hand raised against the hair (arm_l); (4) piles carry small photo-card faces, card stacks in the foreground, clerks ~55 px head diameter (was ~40). Systemic: beam_fx shafts hidden in shot 8, dust 0.5, cast17.silent() on all poses (no mouth moves).
- Heads (render json): centres y 450-745 band checked per frame, max chin 745 (<880), all x inside the frame (min 104).
- Self-check: every 5th frame + g388-392 on contact.jpg, phone_sheet.jpg at 0.5 s; not every frame at 6 fps.
- Stand-ins accepted by director: Bertillon + prisoner_a lost clerks (shot 7), Bertillon scratching his head (shot 8).
- 720x1280, 12 samples + OIDN, ~75 s/frame.
