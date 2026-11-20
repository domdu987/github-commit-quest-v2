# s17 QA: film 19, shot 17 (the ship sails on, the camera pulls back) -- SHIP ship_aerial, NOON  (round 5: colour-fixed set + more motion)

## Delivered (ONE format: the split parts; `cat take.mkv.part* > take.mkv`)
- `take.mkv.partaa` + `.partab` (libx264rgb crf 6, 46 MB, 30 fps): first_g 1271, 122 frames, 720x1280, 10 spp (colour-fixed set), 2 threads. No captions / audio. A single `take.mkv` is not committed (gitignored).
- g 1271..1279 in-handle, **g 1280..1383 = shot 17 (42.65-46.12 s)**, g 1384..1392 out-handle. Join in: hard cut from shot 16; out: dissolve 11 into shot 18.

## What changed
- **Colour-fixed set merged** (film19/main ff204d3): **saturation 0.710, brightness 115.4** (qa_stats; target sat >= 0.40, luma 70-135).
- **More motion that really sweeps the frame:** the camera starts behind the ship at 0.7x the aerial distance and orbits (-28 deg/s), cranes (160 px/s) and pulls back while the ship travels across the frame; a SNAP BACK x0.58 with a big pan and rise (15 f, g 1368..1383) lands on "ยิ่งไกล" and carries the ship from the lower-left to the upper-right (found by a constrained search: the whole ship stays >= 30 px inside the frame on every frame).
- **Whitecaps:** 170 broken foam lines over +-320 m, fed through the set's own `streaks` hook by wrapping `LD.scenery` at runtime (no set edit) so crests / foam sweep across the frame; the set's own wake is already a long white V seen from behind.
- Gulls hidden, glint x0.45, sea grid fitted at runtime to an 11x farther virtual camera at the camera's azimuth (no edge seen). DOF off, no text, no caption_shade in every raw json.
- **qa_auto: PASS** (the snap lands inside the shot, so few post-snap soft frames).

## Frame-diff (in-shot g 1281..1383)
median **4.53**, p90 **10.48** (draft 4.46 / 10.86). Targets: median >= 4, p90 >= 10: **met**. (qa_stats on all frames 5.29 / 11.38.)
