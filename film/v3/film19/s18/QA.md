# s18 QA: film 19, shot 18 (the ship under full sail) -- SHIP ship_hero, NOON

## Delivered
- `take.mkv` (libx264rgb crf 6, 31.9 MB, 30 fps): first_g 1375, 102 frames, 720x1280, 12 spp (ship_hero's own), 2 threads. No captions / audio.
- g 1375..1383 in-handle, **g 1384..1467 = shot 18 (46.12-48.92 s)**, g 1468..1476 out-handle. Join in: dissolve 11 from shot 17; join out: dissolve 13 into shot 19 (handles cover half + 2 or more).
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## Shot
No actors. The hero preset pose: the full-sail warship ahead, bow wave and wake, a swell crest and bright glitter in the foreground. Camera push 6 %/s with a slide 70 px/s, crane 20 px/s and orbit -4 deg/s (moving on frame 0 and on the last frame), plus a SNAP push x1.15 with a small pan (16 f, g 1430..1446) on "จาไมกา" (caption "ไปจาไมกา" 47.68 s = g 1433, the word ~g 1438). `set_sea` / `set_roll` keyed with t = g/30 on every frame. Camera never parked (camreport).

## Checked
- DOF off, no text, no caption_shade in every raw json. No characters: no heads / mouths. The bow wave "sled" (set QA note) stays small / behind the swell crest at the start and the camera slides away from it.
- **Sea edge:** the grid is fitted to one camera; the slide would show its edge, so shot.py (runtime, no set edit) fits it to a 1.5x farther virtual camera. Checked on stills at g 1384, 1420, 1446, 1476: no edge.
- Camera path tuned so the ship stays in frame: harder push / slide (tried 8 %/s with a x1.5 snap) ran the camera into the hull or the ship off the right edge.
- qa_auto PASS.

## Frame-diff (in-shot g 1385..1467)
median **3.11**, p90 **7.85** (draft 3.12 / 7.95). Below the 4 / 12 target: stronger moves (median ~5 at 150 px/s slide) pushed the ship out of frame; I kept the framing.
