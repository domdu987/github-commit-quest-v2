# s17 QA: film 19, shot 17 (the ship sails on, the camera pulls back) -- SHIP ship_aerial, NOON

## Delivered
- `take.mkv` (libx264rgb crf 6, 26.7 MB, 30 fps): first_g 1271, 122 frames, 720x1280, 10 spp (ship_aerial's own), 2 threads. No captions / audio.
- g 1271..1279 in-handle, **g 1280..1383 = shot 17 (42.65-46.12 s)**, g 1384..1392 out-handle (dissolve 11 into shot 18 is centred on g 1384). Join in: hard cut from shot 16.
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## Shot
No actors. The camera starts fairly close behind-above the bow (azimuth -35 deg from the aerial preset, 0.7x its distance), the V of the bow wave and the wake fans around the hull, then pulls back (9-10 %/s) and cranes up (190 px/s) so the ship sinks and shrinks, with a slow orbit; a SNAP BACK (x0.65, 16 f, g 1368..1384, with a small pan) lands on "ยิ่งไกล" (caption 45.56 s = g 1370). Camera never parked (camreport). `set_sea` / `set_roll` keyed with the same t = g/30 on every frame.

## Checked
- DOF off, no text, no caption_shade in every raw json. No characters: no heads / mouths to check. Ship stays clear of the caption band.
- **Sea edge:** the sea grid is fitted to one camera, so pull-backs show its edge. Fixed at runtime (`widen_sea`: grid fitted to a virtual camera 9x farther at the same azimuth, 800x1150 vertices); no set module edited. Checked on stills at g 1271, 1340, 1384, 1392. The coarser grid makes the wake foam slightly rougher near the lens.
- **QA_AUTO:** a first version (closer start, snap x0.45) FAILED "suspected blur" (17 frames after the snap: a tiny ship on a smooth dark sea gives low Laplacian variance). Fixed by a farther start and a gentler snap; PASS now.

## Frame-diff (in-shot g 1281..1383)
median **1.88**, p90 **2.73** (draft 1.89 / 2.72). **Below the 4 / 12 target.** Deviation: a high aerial over a smooth sea barely changes per frame; stronger moves cut the sea-edge safety or the blur QA. The snap pairs reach ~4.4.
