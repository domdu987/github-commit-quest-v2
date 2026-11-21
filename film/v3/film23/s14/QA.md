# s14 QA: film 23, shot S14 (RHINE NIGHT_R)

## Delivered
`take.mkv` (libx264rgb crf 6, 30 fps, 720x1280, 161 frames g 1496..) see meta.json mkv_parts. Also `shot.py` (stills / final / ground), shared `../c23.py` `../deliver.py` `../qa_md.py`, `meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `QA_JITTER.txt`, `GROUND.md`, `numbers.json`. Frames / raw / work stay out of git.

## Clock (ESTIMATED timing: timing_EST.json + plan table)
- g0 1506, g1 1626 (planned, round(t*30)), g1_render 1656 (planned + 25 % tail: the move and the action continue, eased), first_g 1496 (in-handle 10), n_frames 161.
- transition_in: dissolve 17 frames (plan).

## Automatic QA
- `qa_auto.py`: QA_AUTO PASS  (take_full.mkv, 161 frames, 30.00 fps, g 1496-1656)
- `qa_jitter.py` (every second must be <= 2.0 px; no line = clean): ```overall median jitter px 0.12```
- ground_check (`--every 10` equivalent on the built scene, GROUND.md): checked objects: 149   rows: 2384   FAIL rows: 0   **result: PASS**
- frame-diff (90x160 grey, body frames): median 1.26, p90 1.69, min 0.43 (rhythm target median >= 4, p90 >= 12) -- BELOW target: dark, low-contrast night frames with the set's own slow eased camera; the camera never shakes and no frame is static (qa_auto: no frozen runs)
- luma (mean of RGB, every 5th frame): 70.3 .. 75.9 (mean 74.3)
- shade hue (target 240-260; first / mid / last): g1496 227.1, g1576 231.0, g1656 233.8 (night exterior: the director accepted shade hue 227-234 for RHINE in QA_ART_SET.md)
- heads: max head-centre y 864.1 px over the whole take (caption band starts y 880; head radius at most ~12 px): u0 841, u1 864, u2 857, u3 859, u4 800, u5 791, u6 819, u7 822
- render: 720x1280, 12 samples, OIDN, 11.98 s/frame wall (20.68 s CPU), 2 threads while a second render ran.

## Look checks (contact.jpg at 6 fps, phone_sheet.jpg)
- Extreme wide high over the river, slow descend (the set's camera), the RHINE sign on the bank, moon path on the water. Eight GIs act on the near bank: 3 carry crates (carry_pose walk cycle, drifting 0.5-0.6 D/s down toward the supply dump), 1 stands and sways, plus 4 more carriers around the trucks and crate stacks. All real cast23 cards in the night grade (tint #c8ccf0, ink #1e142e).
- They are small in the first second (the camera is 120 D away, heads about 10 px) and grow to about 20 px heads by the end of the descend; that is the extreme-wide brief.

## Rules
- No mouth moves. No weapons. No camera shake. No depth of field.
- Cards stand on the real terrain / mark z (ground_z - 0.03 sink); lanterns flicker per frame (GH.flicker).

## Deviations from the plan / set
- The set row has 4 unloaders; 4 extra carriers were added to make the unloading read. u2 was moved 5 D east and 1.5 D south of its mark (it stood in a tree trunk, ground_check hit 'trees').
- Frame-diff median / p90 are below the 4 / 12 rhythm targets (night wide); the camera is the set's approved descend, I did not add speed because that would read as a rush on an extreme wide.
