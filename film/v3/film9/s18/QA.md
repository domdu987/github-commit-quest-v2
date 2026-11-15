# s18 QA: film 9, shots 18-19 (the ending): wall_site two_sections_out + wall_top_battle, BATTLE

Delivered: `frames/g_1548.png .. g_1766.png` (219 frames, 720x1280, 12 samples, 2 threads, denoise FAST; not in git) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 1548, 219 frames; 74.7 MB, so it is split in git as `take.mkv.partaa` / `partab`:
`cat take.mkv.part* > take.mkv`). g 1548..1553 = in-handle; g 1554..1625 = shot 18; g 1626..1766 = shot 19, which ends on the last
film frame (N 1767), so there is no out-handle. Rendered on the client-approved set (commit 5d511aa). Also `meta.json`, `cues.json`
(15 cues), `contact.jpg`, `qa.txt`. Scripts: `shot.py`, `deliver.py` (+ `take.json`), helper `c9.py`.

## Set-ups (cuts at g 1626 and g 1666; the meta.json transitions list them)
1. **g 1548-1625 (shot 18), `two_sections_out`.** Camera from the field onto the general's grey plain-mortar section, panning right.
   The general laughs arms akimbo on top at (5.4, 1.0, 16), moved clear of the red banner.
   - Shot 1 hits on "นัดแรกร้าว" at g 1592: crater, star crack (cracks 0 -> 0.33).
   - Shot 2 hits on "นัดที่สอง" at g 1613: cracks run along the courses across the whole row (0.33 -> 0.66 by g 1632).
   - Each hit gives a small camera kick and a wobble.
2. **g 1626-1665 (shot 19a), `wall_top_battle`** (preset camera + slow push). The general laughs on the top, head thrown back.
   Shot 3 hits below on "นัดที่สาม" at g 1653: a light burst, the camera shakes, he wobbles and keeps laughing (cracks -> 1).
3. **g 1666-1766 (shot 19b), `two_sections_out`, wide from the field.**
   - The section collapses (set_collapse 0 -> 1 over g 1660-1715). The general drops with the breaking top, still laughing (general_fall
     with expr laughing, flailing arms), and the helmet flies off over his shoulder (g 1672-1690).
   - He slides down the rubble (g 1692-1714) and lands in front of the field gabions, sitting in the dust with a bare topknot.
     He laughs (general_land) through "ที่ยังหัวเราะอยู่ข้างบน"; his helmet lies beside him from g 1691. Cut on the last frame, g 1766.
   - The camera pan leads him to the landing spot and is still moving at the end.

Comic only, no injury. No quote, so mouths are static: the laughing grin is held, with no lip-sync. No DOF.

## Numbers (qa.txt)
- **Heads:**
  - Set-up 1: 34-36 px (on top of the wall, a wide), centre y 283-309.
  - Set-up 2: 68-80 px, centre y 523-553 (0.41-0.43 H).
  - Set-up 3: 31-116 px, centre y 288-801 (falling, then sitting).
  - Every head is above 880 on every frame.
- **Clipped sprite:** a 2-frame warning (g 1684-1685, while the helmet is mid-flight) at the edge of CANVAS9_FALL; nothing visible is
  cut.
- **Popcheck:** pops only at the two planned cuts (1625->1626, 1665->1666); no near-still frames (median change 4.66 levels); no black
  or magenta frames.
- **Render:** 15.4 / 12.0 / 16.0 s wall per frame (29.8 / 23.2 / 29.5 s CPU) per set-up; two processes at once, 2 threads each.
- **Hue:** set-up 1 is red 46.7 / orange 32.7 / blue 16.2; set-up 2 is red 20.9 / orange 35.7 / blue 20.6 / violet 11.5 /
  magenta 11.2 (the BATTLE sky); set-up 3 is orange 64.0 (fire-lit dust). The report's band flags come from the set's BATTLE look,
  which was not re-graded.

## Differences from the plan
- Shot 19 is split into two set-ups (wall_top_battle, then a cut to the wide outer view) instead of one wall_top -> two_sections move.
- The slide path is the set's `slide_out`, bent so that he lands at (7.2, -11.4), in front of the field gabions where he reads.
- The wall-top general stands at x 8 in set-up 2 but at x 5.4 in set-ups 1 and 3 (from the field he is clear of the banner there):
  a small jump across the cuts.
