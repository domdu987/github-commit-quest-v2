# s14 QA: film 24, shot 14 (sea / aftermath)

Delivered: `take.mkv.partaa/ab` (cat together; libx264rgb crf 6, 30 fps, first_g 1601, 172 frames g 1601..1772: 6-frame handles each side), `meta.json` (g0 1607, g1 1767 EXCLUSIVE),
`cues.json`, `contact.jpg`, `overlay.json` (g 1601..1772), `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `shot.py`, `deliver.py`.

Set state keyed on every rendered frame: set_korean_turn 1, set_spikes 3, set_ports 1, set_dragon_smoke 0, set_cannon_smoke 1 -> 0.35 (g 1600..1670), set_damage 0.35 -> 1.0 over g 1607..1766
(Japanese ships list, masts down, grey smoke columns; no fire, no people, no bodies). Same damage schedule as s13 (hit_g values agree).
Camera: custom slow low push from the preset line (150,-16,6.5) -> (122,-12,7), look (55,0,7) -> (50,0,7.5), 24 mm, calm ease; qa_jitter median 0.23 px; DOF off; nothing parented.

| rule | status |
|---|---|
| nothing floats | ships ride the swell; no people |
| never static > 6 frames | qa_auto PASS |
| cuts | hard cuts in / out |
| tone | smoke only |
| top third free from g 1560 | the upper half of the frame is empty sky; smoke columns top out at y ~ 480; overlay marks fall on the deck centres in overlay.json |

overlay.json: same format as s13 (x, y = deck centre in 720x1280 px of every ship already hit, hit_g = first frame with d > threshold).
Deviation: the turtle ship does not move on its own (no set hook); "sails through" is carried by the camera push along its hull. The aftermath preset keeps the ports open and the spikes at 3.
