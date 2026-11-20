# sD2 QA: film 21, segment D2 (the MOCKER), g 642-793 + 3 handle frames (794-796)

Delivered: `take.mkv` (parts `take.mkv.partaa/ab`, 62 MB total: `cat take.mkv.part* > take.mkv`), libx264rgb crf 6, 30 fps, first_g 642, 155 frames, 720x1280, 32 samples, OIDN.
`meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `path_draft.mp4` (10 fps 360x640 path draft). Scripts: `shot.py` (check / draft / final), `c21.py`, `deliver.py`.

## Fix pass after the TAKE gate (QA_TECH / QA_ART sD2), rendered on set e07ceb1 + cast528bf9d colours
1. Purse slap on screen: the unmirrored pose points up-left with the left arm and the right hand comes DOWN onto the purse at g 758 (2-frame jolt of head and lean, coin glint + two hopping coins g 759-764), pressed on the purse to g 780. CU1 face about 33 % of frame height (head width 421 px max), head y 452 so the belt and purse stay in shot.
2. Nobody cut by the frame edge: Surrey trails, steps in BEHIND Cressingham before the CU (hidden by his head, g 756-781) and steps out to his P_BANK mark while the camera pulls back. Surrey starts 0.5 m offset so his head does not merge with the neck (g 642-646). Background soldier reduced to one (e1) kept inside the frame. `shot.py check` per-frame list: no head crosses a side edge; the only flags are Surrey's head centre y < 450 at g 770-778 while he is hidden behind Cressingham.
3. Red barrel gone (barrel body and its iron hoops hidden); a grey strongbox with a gold lock, sacks, spears, pegs dress the near ground, no bare sand. The camera tilts up (head centre y about 620-665 while tracking).
4. The point: the arm is raised about 30 deg (up-left at the hill); the far Scots are 2.7x and the saltire flags 2.5x; the bridge enters the right side of the frame by g ~725 ("ข้ามสะพานนี่แหละ").
5. Handles g 794-796 continue the pull-out at 0.06 m per frame (the move arrives at P_BANK at g 793 at that speed) plus a small slide.
6. Floating pennants removed with `K.hide_near_banners(path, 7)` (4 banners hidden); the fg banner pole stays hidden.

## Numbers (re-render)
- `qa_stats2.py`: sat 0.585, vivid 61.4 %, luma 102.1 (colour is normalised at the conform).
- `rhythm.py`: in-shot median 13.17, p90 30.36. `qa_auto.py`: PASS, magenta 0 %.
- Lip-sync only g 642-791. Whip in g 642-647. No text in this segment.
