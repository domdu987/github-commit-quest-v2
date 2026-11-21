# s17 QA: film 23, shot S17 (RHINE NIGHT_R)

## Delivered
`take.mkv` (libx264rgb crf 6, 30 fps, 720x1280, 106 frames g 1820..) see meta.json mkv_parts. Also `shot.py` (stills / final / ground), shared `../c23.py` `../deliver.py` `../qa_md.py`, `meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `QA_JITTER.txt`, `GROUND.md`, `numbers.json`. Frames / raw / work stay out of git.

## Clock (ESTIMATED timing: timing_EST.json + plan table)
- g0 1827, g1 1905 (planned, round(t*30)), g1_render 1925 (planned + 25 % tail: the move and the action continue, eased), first_g 1820 (in-handle 7), n_frames 106.
- transition_in: dissolve 11 frames (plan).

## Automatic QA
- `qa_auto.py`: QA_AUTO PASS  (take.mkv, 106 frames, 30.00 fps, g 1820-1925)
- `qa_jitter.py` (every second must be <= 2.0 px; no line = clean): ```overall median jitter px 0.18```
- ground_check (`--every 10` equivalent on the built scene, GROUND.md): checked objects: 145   rows: 2166   FAIL rows: 0   **result: PASS**
- frame-diff (90x160 grey, body frames): median 0.80, p90 1.17, min 0.46 (rhythm target median >= 4, p90 >= 12) -- BELOW target: dark, low-contrast night frames with the set's own slow eased camera; the camera never shakes and no frame is static (qa_auto: no frozen runs)
- luma (mean of RGB, every 5th frame): 70.4 .. 76.0 (mean 73.0)
- shade hue (target 240-260; first / mid / last): g1820 233.7, g1873 234.1, g1925 234.6 (night exterior: the director accepted shade hue 227-234 for RHINE in QA_ART_SET.md)
- heads: max head-centre y 796.7 px over the whole take (caption band starts y 880; head radius at most ~35 px): tall 739, round 797
- render: 720x1280, 12 samples, OIDN, 16.53 s/frame wall (17.33 s CPU), 2 threads while a second render ran.

## Look checks (contact.jpg at 6 fps, phone_sheet.jpg)
- OTS from the German OP with the sandbag foreground; both observers whole in frame (QA_ART_SET note), heads at y 660-800, far decoy field glowing across the river. cast23 has no back views, so the two Germans are front-3/4 cards facing the lens, a known cast weakness.
- Comic action: the tall one (ger_tall) lowers his binoculars, nudges and then points south; the round one (ger_round) eats his sausage, then drops it (`ger_drop_sausage`), the sausage (cast23 `sausage_svg`, 12 rotation variants) falls 0.3 s from his drawn hand anchor, lands flat on the ground next to his boot, and he turns to stunned. Expression swaps sit behind blinks.

## Rules
- No weapons (binoculars only) and nobody is hurt. Mouths are held expression drawings only (`stunned` open mouth is one drawing). No camera shake. No depth of field.
- The sausage is flagged `airborne_frames` for its fall only, then rests on the ground (ground_check PASS).

## Deviations from the plan / set
- The set row has 3 observer marks; 2 cards are used (QA_ART_SET: 'both Germans whole'); their feet were put at chosen screen spots rather than the OP marks.
- Frame-diff median / p90 are far below the targets: the OTS lens push is the set's 0.06 zoom + 15 px/s slide on a 98-frame shot; the action (nudge, point, sausage drop) carries the shot.
