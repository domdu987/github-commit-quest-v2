# s02 QA: film 19, shot 2 (the lone ship) -- SHIP ship_aerial, NOON  (round 2)

## Delivered
- `take.mkv` (libx264rgb crf 6, 29 MB, 30 fps): first_g 48, 71 frames, 720x1280, 10 spp, 2 threads. No captions / audio.
- g 48..56 in-handle, **g 57..109 = shot 2 (1.91-3.65 s)**, g 110..118 out-handle. Joins: hard cut in (from shot 1) and hard cut out (to shot 3).
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## Round-2 fixes (QA-tech: "uniform drift", glare at the left edge g 48-63, gull clipped from g 88)
- **Eased orbit + slide + one fast snap with a pan:** the camera starts behind the ship and orbits (-30 deg/s), slides (140 px/s) and cranes (119 px/s) while pulling back slowly; at g 92..108 (16 f, on "เรืออยู่", caption g 98) a SNAP BACK x0.59 with a pan and rise carries the ship from the lower-left up to the upper-right of the frame, leaving the long white V wake across the lower frame.
- **Ship fully in frame on every frame:** searched under the constraint ship bbox key points >= 30 px inside (found 91 px).
- **Gulls hidden** (no gull clipped at the edge); **sun glint x0.45** (the glare patch is smaller and no longer at the edge: the remaining soft white blobs near the wake are sea glitter).
- **Wake:** a 300 m V wake (10 Kelvin arms + centre line) via the set's own streaks hook, visible from behind.
- **Sea:** grid fitted at runtime to an 11x farther virtual camera at the same azimuth, 1300x1800 vertices (no set edit): no edge, no seam. Sea clock x2.
- DOF off, no text, no caption_shade in every raw json. qa_auto PASS.

## Frame-diff (in-shot g 58..109)
median **3.60**, p90 **17.57** (draft 3.48 / 18.0). **p90 passes (>= 10); the median is just under 4:** the pre-snap part (g 57..91) is a smooth drift over low-contrast sea; I kept the whole ship in frame, so the orbit / slide could not be pushed further.
