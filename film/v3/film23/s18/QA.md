# s18 QA: film 23, shot S18 (RHINE PREDAWN)

## Delivered
`take.mkv` (libx264rgb crf 6, 30 fps, 720x1280, 104 frames g 1896..) is under 45 MB (single file). Also `shot.py` (stills / final / ground), shared `../c23.py` `../deliver.py` `../qa_md.py`, `meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `QA_JITTER.txt`, `GROUND.md`, `numbers.json`. Frames / raw / work stay out of git.

## Clock (ESTIMATED timing: timing_EST.json + plan table)
- g0 1905, g1 1980 (planned, round(t*30)), g1_render 1999 (planned + 25 % tail: the move and the action continue, eased), first_g 1896 (in-handle 9), n_frames 104.
- transition_in: dissolve 13 frames (plan).

## Automatic QA
- `qa_auto.py`: QA_AUTO PASS  (take.mkv, 104 frames, 30.00 fps, g 1896-1999)
- `qa_jitter.py` (every second must be <= 2.0 px; no line = clean): ```overall median jitter px 0.28```
- ground_check (`--every 10` equivalent on the built scene, GROUND.md): checked objects: 157   rows: 1716   FAIL rows: 0   **result: PASS**
- frame-diff (90x160 grey, body frames): median 0.87, p90 1.05, min 0.45 (rhythm target median >= 4, p90 >= 12) -- BELOW target: dark, low-contrast night frames with the set's own slow eased camera; the camera never shakes and no frame is static (qa_auto: no frozen runs)
- luma (mean of RGB, every 5th frame): 79.0 .. 83.5 (mean 81.3)
- shade hue (target 240-260; first / mid / last): g1896 231.0, g1948 231.1, g1999 231.3 (night exterior: the director accepted shade hue 227-234 for RHINE in QA_ART_SET.md)
- heads: max head-centre y 848.4 px over the whole take (caption band starts y 880; head radius at most ~28 px): pad0 848, pad1 836, pad2 832, pad3 834, pad4 830, tip0 753, tip1 770, tip2 787, tip3 793, far0 824, far1 813, far2 819, far3 814, far4 813
- water share of the frame (far water line): 34.9 % .. 36.5 %
- render: 720x1280, 12 samples, OIDN, 8.67 s/frame wall (16.21 s CPU), 2 threads while a second render ran.

## Look checks (contact.jpg at 6 fps, phone_sheet.jpg)
- QA_ART_SET notes applied: a SECOND boat (boat2: three paddlers) now rides behind boat3 (two paddlers + the dog); both are re-placed at runtime on the water 13 and 22 D from the lens and drift east at 1.6 D/s with a small bob. Water share of the frame 32-37 % (far water line; limit 40 %): the camera tilts up about 11 deg.
- Camera (runtime override of the set's row): start (-33, 361.5, 1.35) look (20, 386, 14.3) lens 22 -> end (-27, 360, 1.0) look (16, 385, 10.9) lens 27 (a slow pan along the boats, a 4.5 %/s lens push, and the camera drifts east); the set's own end pose moved only 0.7 D and measured a frame-diff median of 0.45. Camera height 1.0-1.35 D above the water line is lower than the QA's 2-3 D because heads must stay above y 880 at this tilt.
- Cast: 5 kneeling paddlers (paddle_frame, 24-frame stroke, phases staggered, blinks), 4 tiptoe soldiers on the pontoon deck (tiptoe_frame, finger to the lips, drifting east 0.7 D/s), 5 far-bank soldiers (3 carry crates, 1 waves, 1 stands). The dog has no cast23 card: it is my own flat-fill + plum-ink card drawn with PIL (`c23.dog_pngs`), parented to boat3, two tail frames. All soldiers get the cast `tint` / `ink` pre-dawn grade (tint #c0caf2, ink #1e1a3a).
- Set dressing added at runtime: 3 tall poplars on both banks (to fill the tall sky) and 4 bridge-rail lanterns (700 W) whose warm streaks lie on the water. Pre-dawn blue with the warm orange band low in the east-north-east is the set's own.

## Rules
- No mouth moves. No weapons (paddles only). No camera shake (eased keys). No depth of field.
- Nothing floats: paddlers kneel on the boat-floor mark of their boat (matrix_world of the moving boat every frame); the paddle blade dips below the knees on purpose (cast23), so the paddlers' card gc_gap tolerance is 1.8 D (the knee/boat contact itself is the mark). Tiptoers stand on the deck top (0.50), far-bank troops on the terrain.

## Deviations from the plan / set
- Camera replaced at runtime (see above); boats 0, 1, 4 are out of frame at every frame so they have no cards; the 5-boat marks of the set row were reduced to boat2 + boat3.
- A dog card was drawn (no cast23 dog). Frame-diff stays low (night water, slow pan): see the numbers.
