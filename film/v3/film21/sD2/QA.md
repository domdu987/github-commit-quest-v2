# sD2 QA: film 21, segment D2 (the MOCKER), g 642-793 + 3 handle frames (794-796)

Delivered: `take.mkv` (parts `take.mkv.partaa/ab`, 64 MB total: `cat take.mkv.part* > take.mkv`), libx264rgb crf 6, 30 fps, first_g 642, 155 frames, 720x1280, 32 samples, OIDN.
`meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `path_draft.mp4` (10 fps 360x640 path draft). Scripts: `shot.py` (check / draft / final), `c21.py`, `deliver.py`.

## Segment
- World: `K.build_world(['camp_bank'])`, one travelling camera, no cut. transition_in = cut (whip rendered inside).
- g 642-647 whip in (pan 34, 16, 7, 3, 1.2, 0.4 deg settling). g 648-750 side tracking: the camera follows Cressingham as he waddles 4.5 m toward screen-left along the bank, pointing at the hill (walk cycle mirrored, wide stance); Surrey trails tired.
- CU1 g 756-778: fast push (756-765), purse slap at g 758, face about 346 px wide (27 % of frame height); then the camera eases out and arrives EXACTLY at K.POSES['P_BANK'] (loc and look equal) at g 793. g 794-796 continue the pull-out (D6 join to E1).
- Lip-sync via `cast21.speak` only for g 642-791 (narration 21.29-26.26); before and after: smirk, closed.
- Rim light: every pose through `K.with_rim` (gold). Contact shadows on. Cast: cressingham, surrey, two background soldiers (idle sway, blinks, a look shift).
- Set note: the fg banner pole (flag_wood.021, flag_gold.021 and its cloth flag_t_*.014/.015) is hidden because it crossed Cressingham's head while tracking (§G). Surrey ends at cx 570 at P_BANK (QA-art note).

## Numbers
- `qa_stats.py`: saturation 0.618, brightness 105.9. `qa_stats2.py`: sat 0.618, vivid 64.4 %, luma 105.9, still 1.3 %.
- `rhythm.py`: in-shot median 8.18, p90 25.53 (needs >= 4 / >= 12).
- `qa_auto.py`: PASS (soft frame g 642 = whip motion streak, allowed). Magenta 0 %.
- Head check (every 2nd frame): all head centres y 450-760 for Cressingham/Surrey, bottoms < 880, no face above 35 % of frame height.

## Known, for the director
- Surrey (g 754-756, 786) and two background soldiers (g 760, 780-782) cross the side frame edge for 1-3 frames while the camera pushes into / pulls out of CU1. They are fully in or fully out otherwise.
- The pole is hidden for the whole segment (no banner pole at the right edge of D2).
- No readable text appears in this segment.
