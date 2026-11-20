# T6a QA (film 17 v2, T6, g1371-1452, 82 frames)

Staging: `render_t6a.py` (`assign_for`: Bertillon dx +0.45 easing to 0 by g1535; inspector dx -0.4 / dy +3.0 up to g1545). `clear_cast()` runs before every `stage_cast2` (leak fix, commit a7553db).
Frames g1371-1380 come from the first, pre-fix run and the rest from the fixed run. In the fix run, luma was clean over the first 10 frames and I saw no slab.

Checks: `check_take('T6')` no hits, `check_face('T6')` ok, `report T1 T6` PASS (T6 BIGZOOM 4.4 -> 48.0 %H). These read the planned cast path, so they do not see my dx/dy offsets.
`qa_auto.py take.mkv --cuts 1377 --first_g 1371`: PASS (magenta 0.0 %; the planned cut at g1377 shows no visible change inside this range, since g1371-1376 are handle frames of the same camera move).
`rhythm.py`: in-shot median 15.53, p90 18.49, no cuts detected.
Luma (mean of grey): 112.3, min 107.0, max 122.2, 31 of 82 frames above 112 (target 95-112). The climb comes from the PETIT sign and bright floor filling the frame as the camera dives (g1400 onward). Lights are untouched.

Frames viewed. FULL = 720x1280. PHONE = 360x640 in a 6-up sheet.
- g1420 FULL: a huge PETIT sign fills the upper third. Below it the vault runs to the ARCHIVES sign at the far end, with the gallery rails on both sides. Four small figures sit at the far end by the desks, two at the far desk and two on the left, with contact shadows. Two chandelier globes burn in the right foreground. Floor, ladder and desks read clearly.
- g1452 FULL: the MOYEN and GRAND signs are overhead, with ARCHIVES readable, the two gallery rails and the carpet leading to the far group. The figures at the far end are still small (the dive is not finished). A rolling cart and a ladder are grounded on the floor. No slabs, no shimmer on the blue vault.
- g1371 PHONE: the camera is high over the vault with the PETIT sign; the far group is tiny and faint.
- g1377 PHONE: same framing, slightly lower. The far group reads as dark dots by the desk.
- g1400 PHONE: PETIT is larger and cropped at the right edge; the chandelier arms spread over the carpet.
- g1440 PHONE: MOYEN and GRAND overhead; the group reads small near the far desks.
- Shimmer: g1385 and g1400 compared side by side at full size, with no visible OIDN crawl on flat blue or wall areas. 16 samples kept.

Not seen in this part: the real cast cards are only about 4 % of the frame height here (BIGZOOM start), so face quality and the card/box shots are T6a2's (g1453+).
