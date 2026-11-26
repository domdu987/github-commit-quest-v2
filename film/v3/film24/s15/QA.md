# s15 QA: film 24, shot 15 (the ending): sea / shore

Delivered: `take.mkv.partaa/ab` (cat together; libx264rgb crf 6, 30 fps, first_g 1761, 189 frames g 1761..1949), `meta.json`, `cues.json`, `contact.jpg`
(16 frames, cyan = y 880), `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `shot.py`, `deliver.py`. 6-frame in-handle g 1761..1766; no out-handle (film ends g 1949).
g 1767..1866 plank phase (58.9-61.9 s), HARD CUT at g 1867 (62.12 s "แล้วคลานขึ้นฝั่ง") to the sand, crawl to g 1949.

| rule | how / measured |
|---|---|
| nothing floats, contact shadows | plank card keyed on J.swell_z at its world point every frame (rides the water, plank underside = waterline; the set's lying plank hidden). Crawler's ground anchor keyed on the beach height field each frame, path chosen along the flat sand contour (an earlier line up the steep bank floated over grass). Stage contact decal + shadow proxy. |
| camera | plank phase: eased pull-back (0.35 sine + 0.65 linear); sand phase: slow truck-and-pull-back following the crawler. qa_jitter median 0.13 px. Nothing parented to the camera; DOF off. |
| crawl | crawl_a / crawl_b alternate every 8 frames, 0.45 D per half step, forward travel eased within each step. |
| heads | head bottoms max 742 px (< 880); head width 118 -> 63 px. |
| mouths | held (no quote). wet24 = 1 throughout. |
| cuts | hard cut inside the take at g 1867; qa_auto PASS. |

Cost: 36.4 s wall / 69.4 s CPU per frame (2 processes x 2 threads, 24 samples).
Deviations / limits: crawl travels along the shore (up-slope and screen-right) rather than straight up the beach (steep bank); the card is a side view so the camera looks across; a large foam slab of the set's surf strip sits in the sand-phase foreground; the crawl is a two-pose card alternation with the body eased between steps (feet cannot be strictly planted per step).
