# s17 QA: film 19, shot 17 (the ship sails on, the camera pulls back) -- SHIP ship_aerial, NOON

## Delivered
- `take.mkv` (libx264rgb crf 6, 26.7 MB, 30 fps): first_g 1271, 122 frames, 720x1280, 10 spp (ship_aerial's own), 2 threads. No captions / audio.
- g 1271..1279 in-handle, **g 1280..1383 = shot 17 (42.65-46.12 s)**, g 1384..1392 out-handle (dissolve 11 into shot 18 is centred on g 1384). Join in: hard cut from shot 16.
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## Shot (re-rendered after the director's QA-tech fail: frame-diff 1.88 / 2.73)
No actors. The camera starts close (0.45x the aerial distance) and 45 deg off the preset azimuth, so the ship runs diagonally across the frame with its bow wave and wake foam arcs filling the lower frame; it pulls back (8 %/s), cranes up (120 px/s), slides (120 px/s) and orbits (-14 deg/s) so the ship travels across the frame and shrinks; a SNAP BACK (x0.62, 16 f, g 1370..1386, with a pan) on "ยิ่งไกล" (caption 45.56 s = g 1370). `set_sea` / `set_roll` with t = g/30 on every frame. Never parked (camreport).

## Checked
- DOF off, no text, no caption_shade in every raw json. No characters.
- **Sea edge:** the grid is fitted at runtime (`widen_sea`) to a virtual camera 11x farther on the same azimuth, 1300x1800 vertices (denser than before, so the wake foam is clean). Stills at g 1271, 1330, 1370, 1392: no edge (the far horizon slopes slightly at the very end of the handle).
- **QA_AUTO PASS** (an intermediate version with a harder, earlier snap FAILED "suspected blur" after the snap: a tiny ship on smooth sea; the snap now lands later and gentler).

## Frame-diff (in-shot g 1281..1383)
median **3.99**, p90 **5.03** (draft 4.14 / 5.03). Median is at the target (rounds to 4.0); p90 is still below 12: a bigger snap shrinks the ship onto smooth water and fails the blur check.
