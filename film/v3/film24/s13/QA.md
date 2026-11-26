# s13 QA: film 24, shot 13 (sea / custom top-down): the one-image reveal

Delivered: `take.mkv.partaa/ab` (cat together; libx264rgb crf 6, 30 fps, first_g 1407, 206 frames g 1407..1612: 6-frame handles each side), `meta.json` (g0 1413, g1 1607 EXCLUSIVE),
`cues.json`, `contact.jpg` (16 frames; cyan y 880, magenta y 427 = top third), `overlay.json` (frames 1407..1612), `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `shot.py`, `deliver.py`.

Timeline: set_korean_turn 0 -> 1 over g 1440..1500 ("แล้วเรือเกาหลี ... ก็หันกลับมา"); ports open g 1492..1502; set_cannon_smoke 0 -> 1 over g 1500..1570 ("ยิงปืนใหญ่" g 1563);
set_damage 0 -> 0.35 over g 1545..1607 (ships hit one after another, mast stump + smoke column, listing). All hooks keyed on every rendered frame.
Camera: custom straight-down, slow rise (-54,0,150) -> (-40,0,190), look (-12,0,0) -> (-10,0,0), 18 mm so the whole U (front arc + both arms) and the Japanese fleet sit in frame; qa_jitter median 0.10 px; DOF off; nothing parented to the camera.

| rule | status |
|---|---|
| nothing floats | ships ride the shared swell (set drivers); no people (aerial, cards invisible at this height) |
| never static > 6 frames | qa_auto PASS (swell, turn, smoke and the camera always move) |
| hard cuts | transitions in/out are cuts; no dissolves |
| tone | smoke and muzzle flashes only; no fire, no people, no bodies |
| top third free from g 1560 | the Japanese fleet sits in the lower two thirds; the Korean U arms and smoke occupy the upper part as the shot's subject, so the director may need to place text over smoke/sea. The director's overlay marks land on the deck centres listed in overlay.json |

overlay.json: per frame `{"g", "ships": [{name, hit_g, x, y}]}`; x,y = screen px (720x1280) of the deck centre of every Japanese ship with damage d(g) > its threshold
(world_to_camera_view of the ship root at deck height); hit_g = first film frame with d > threshold (computed over the s13 + s14 damage schedule). 0 ships before g 1553, 13 at g 1606.

Deviations / limits: custom top-down camera instead of the reveal_top preset (the first framing was too tight and the U did not read); cannon smoke/flash scaled 2.6x at runtime from shot.py so it reads from altitude; lens 18. Aerial ships are small; the U and the smoke read as shapes. Korean fleet turn/damage schedules are shared with s14 (same functions in both shot.py).
Cost ~36 s wall (48 s mean logged) / ~64 s CPU per frame (24 samples, 2 processes x 2 threads).
