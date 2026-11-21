# s15 QA: film 23, shot S15 (RHINE NIGHT_R)

## Delivered
`take.mkv` (libx264rgb crf 6, 30 fps, 720x1280, 132 frames g 1622..) see meta.json mkv_parts. Also `shot.py` (stills / final / ground), shared `../c23.py` `../deliver.py` `../qa_md.py`, `meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `QA_JITTER.txt`, `GROUND.md`, `numbers.json`. Frames / raw / work stay out of git.

## Clock (ESTIMATED timing: timing_EST.json + plan table)
- g0 1629, g1 1728 (planned, round(t*30)), g1_render 1753 (planned + 25 % tail: the move and the action continue, eased), first_g 1622 (in-handle 7), n_frames 132.
- transition_in: dissolve 11 frames (plan).

## Automatic QA
- `qa_auto.py`: QA_AUTO PASS  (take_full.mkv, 132 frames, 30.00 fps, g 1622-1753)
- `qa_jitter.py` (every second must be <= 2.0 px; no line = clean): ```overall median jitter px 0.21```
- ground_check (`--every 10` equivalent on the built scene, GROUND.md): checked objects: 151   rows: 2114   FAIL rows: 0   **result: PASS**
- frame-diff (90x160 grey, body frames): median 2.72, p90 3.68, min 0.74 (rhythm target median >= 4, p90 >= 12) -- BELOW target: dark, low-contrast night frames with the set's own slow eased camera; the camera never shakes and no frame is static (qa_auto: no frozen runs)
- luma (mean of RGB, every 5th frame): 61.3 .. 72.0 (mean 69.0)
- shade hue (target 240-260; first / mid / last): g1622 236.8, g1688 231.3, g1753 232.4 (night exterior: the director accepted shade hue 227-234 for RHINE in QA_ART_SET.md)
- heads: max head-centre y 770.8 px over the whole take (caption band starts y 880; head radius at most ~14 px): pump0 771, pump1 737, pump2 697, watch 637, carr 644
- render: 720x1280, 12 samples, OIDN, 10.71 s/frame wall (21.05 s CPU), 2 threads while a second render ran.

## Look checks (contact.jpg at 6 fps, phone_sheet.jpg)
- Crane up over the rows (set camera): set_inflate keyed every frame on all 42 decoys with the set's staggered _a15 schedule (0.2 -> 1.0), lantern light, house and poplars at the horizon. Pump crews: three gi pump men pump (pump_frame 20-frame stroke, staggered), a watcher stands and sways, a carrier walks with a crate (carry_pose).
- Two of the three pump men were moved from their marks to 12-18 D from the start lens (beside the lane) so the crews read; the third stays at its mark.

## Rules
- No mouth moves. No weapons. No camera shake. No depth of field.
- Tanks stay snapped while inflating (the shape keys and the z key are evaluated on each frame before `ground_snap`: frame_set(f) at the top of the per-frame state function; without it the first run had 39 float FAILs).

## Deviations from the plan / set
- Pump crew positions changed as above; hoses are not tied to the tank valves (the sprite's own hose end lies on the ground).
- Pump men re-placed twice: first moved near the lens (heads left the frame into the caption band at the crane end, y 1162), then re-placed from the LAST frame camera rays so heads stay above y 880 throughout.
- The crews are small on screen (heads 15-25 px) because the crane camera looks down from 18 D and moves past anything near the lens; they read as working figures among the lamps, not as close characters.
