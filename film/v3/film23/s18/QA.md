# s18 QA: film 23, shot S18 (RHINE PREDAWN)

## Delivered
`take.mkv` (libx264rgb crf 6, 30 fps, 720x1280, 104 frames g 1896..) is under 45 MB (single file). Also `shot.py` (stills / final / ground), shared `../c23.py` `../deliver.py` `../qa_md.py`, `meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `QA_JITTER.txt`, `GROUND.md`, `numbers.json`. Frames / raw / work stay out of git.

## Clock (ESTIMATED timing: timing_EST.json + plan table)
- g0 1905, g1 1980 (planned, round(t*30)), g1_render 1999 (planned + 25 % tail: the move and the action continue, eased), first_g 1896 (in-handle 9), n_frames 104.
- transition_in: dissolve 13 frames (plan).

## Automatic QA
- `qa_auto.py`: QA_AUTO PASS  (take.mkv, 104 frames, 30.00 fps, g 1896-1999)
- `qa_jitter.py` (every second must be <= 2.0 px; no line = clean): ```overall median jitter px 0.32```
- ground_check (`--every 10` equivalent on the built scene, GROUND.md): checked objects: 158   rows: 1727   FAIL rows: 0   **result: PASS**
- frame-diff (90x160 grey, body frames): median 0.91, p90 1.13, min 0.52 (rhythm target median >= 4, p90 >= 12) -- BELOW target: dark, low-contrast night frames with the set's own slow eased camera; the camera never shakes and no frame is static (qa_auto: no frozen runs)
- luma (mean of RGB, every 5th frame): 77.0 .. 79.9 (mean 78.3)
- shade hue (target 240-260; first / mid / last): g1896 231.4, g1948 231.4, g1999 231.4 (night exterior: the director accepted shade hue 227-234 for RHINE in QA_ART_SET.md)
- heads: max head-centre y 801.7 px over the whole take (caption band starts y 880; head radius at most ~65 px): pad0 751, pad1 745, pad2 750, pad3 786, pad4 792, pad5 790, tip0 699, tip1 733, tip2 758, tip3 768, far0 802, far1 794, far2 799, far3 794, far4 794
- water share of the frame (far water line): 36.2 % .. 38.3 %
- render: 720x1280, 12 samples, OIDN, 8.49 s/frame wall (16.6 s CPU), 2 threads while a second render ran.

## Look checks (contact.jpg at 6 fps, phone_sheet.jpg)
- Director redo (S18): the camera is low and oblique (start z 0.4 = 1.0 D over the water, look up about 11 deg, horizon at 0.62 H, water 36-38 % of the frame), sliding east WITH the boats (boat 1.0 D/s, camera ~1.1 D/s) with a lens push 22 -> 24. Boat3 (3 paddling GIs: gi_pump, gi_radio, gi_designer, + the dog) is ~6.5 D from the lens, heads ~120-130 px wide at y 690-750; boat2 (3 paddlers) ~15 D further back; the pontoon bridge runs diagonally behind with 4 tiptoe soldiers; far-bank troops; warm orange dawn band; bridge-rail lanterns reflect in the water.
- The tall grey columns of the first delivery were three poplars I had added (38 D); they are removed. The camera is 1.0 D over the water, not 2-3 D: at 2-3 D the heads of a boat 6 D away fall below the caption band at this tilt.
- The dog has no cast23 card: own drawing (c23.dog_pngs). Cast `tint` / `ink` pre-dawn grade.

## Rules
- No mouth moves. No weapons (paddles only). No camera shake (eased keys). No depth of field.
- Nothing floats: paddlers kneel on the boat-floor mark of their boat (matrix_world of the moving boat every frame); the paddle blade dips below the knees on purpose (cast23), so the paddlers' card gc_gap tolerance is 1.8 D (the knee/boat contact itself is the mark). Tiptoers stand on the deck top (0.50), far-bank troops on the terrain.

## Deviations from the plan / set
- Camera / boats replaced at runtime as above (camera height 1.0 D instead of 2-3 D, reason above); boats 0, 1, 4 are out of frame and have no cards.
- Frame-diff is low (night water, slow slide).
