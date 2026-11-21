# s01 QA: film 23, shot S01 (FIELDS DAWN)

## Delivered
`take.mkv` (libx264rgb crf 6, 30 fps, 720x1280, 151 frames g 0..150) is 106 MB, so it is split with `split -b 40M` into `take.mkv.part_aa/ab/ac` (`cat take.mkv.part_* > take.mkv`). Also `shot.py` (stills / final / ground), `../c23.py` + `../deliver.py` + `../qa_md.py` (shared helpers), `meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `QA_JITTER.txt`, `GROUND.md`, `numbers.json`. Frames / raw / work stay out of git.

## Clock (ESTIMATED timing: timing_EST.json + plan table)
- g0 0, g1 120 (planned, round(t*30)), g1_render 150 (planned + 25 % tail: the move and the action continue, eased), first_g 0 (in-handle 0), n_frames 151.
- transition_in: open 0 frames (plan).

## Automatic QA
- `qa_auto.py`: QA_AUTO PASS  (take_full.mkv, 151 frames, 30.00 fps, g 0-150)
- `qa_jitter.py` (every second must be <= 2.0 px; no line = clean): ```overall median jitter px 0.23```
- ground_check (`--every 10` equivalent on the built scene, GROUND.md): checked objects: 39   rows: 624   FAIL rows: 0   **result: PASS**
- frame-diff (90x160 grey, body frames): median 5.56, p90 11.34, min 1.57 (rhythm target median >= 4, p90 >= 12)
- luma (mean of RGB, every 5th frame): 90.1 .. 100.6 (mean 94.8)
- shade hue (target 240-260; first / mid / last): g0 241.3, g75 245.7, g150 246.3
- heads: max head-centre y 817.4 px over the whole take (caption band starts y 880; head radius at most ~30 px): rider 801, walk0 817, walk1 766
- render: 720x1280, 12 samples, OIDN, 11.96 s/frame wall (16.44 s CPU), 2 threads while a second render ran.

## Look checks (contact.jpg at 6 fps, phone_sheet.jpg)
- BIGZOOM 1 as planned: g 0 a high OBLIQUE extreme wide (120 D up, 37 deg down, dawn horizon in the top 15 %) along the lane over the bocage, descend and push past two poplars, end 3/4 on the lead tank with the waving soldier (rider on col0's deck, head centre y 0.48 H at g 150; the QA target was 0.40-0.55).
- Cast: gi_smile rides col0 and waves (wave_frame 12-frame cycle), gi_pump waves from the verge, gi_designer stands and sways (all real cast23 cards, front-3/4: there are no back views). The column rolls 4 D over the planned length (set_column keyed every frame).
- No heads in the caption band; nothing floats (ground_check PASS; the rider stands on the tank deck mark, the walkers on the grass).

## Rules
- No mouth moves (held expression drawings only). No weapons. No camera shake: eased keys only (set's BIGZOOM path, no noise). No depth of field.
- Every character card has the stage contact decal on its surface (rider on the deck, walkers on the grass).

## Deviations from the plan / set
- Frame-diff p90 is 11.3 (target 12): the first 40 frames of the BIGZOOM descend slowly by design (the set's approved move); median 5.6 passes. No camera edits were made.
- Nothing else differs from the plan. The three marks of the set row (rider + 2 walkers) were kept; no extra troops were added.
