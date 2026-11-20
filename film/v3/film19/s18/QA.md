# s18 QA: film 19, shot 18 (the ship under full sail) -- SHIP ship_hero, NOON  (round 5: colour-fixed set + more motion)

## Delivered
- `take.mkv` (libx264rgb crf 6, 33.6 MB, 30 fps): first_g 1375, 102 frames, 720x1280, 12 spp, 2 threads. No captions / audio.
- g 1375..1383 in-handle, **g 1384..1467 = shot 18 (46.12-48.92 s)**, g 1468..1476 out-handle. Join in: dissolve 11 from shot 17; out: dissolve 13 into shot 19.
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## What changed
- **Colour-fixed set merged** (film19/main ff204d3: NOON exposure -0.3, sat 1.18) plus -0.3 EV in this take (the new foam crests brighten the frame): **luma 128.6 (target 70-135), saturation 0.530 (>= 0.40)** by `qa_stats.py`.
- **Foreground that sweeps across the frame (director round 5, b):** 40 broken swell-crest foam lines (the set's own `streaks` hook, by wrapping `floating_spar` at runtime: no set edit) between the camera and the ship, and the preset's floating spar kept in front of the lens. The camera slide / orbit / pull sweeps them across.
- Ship fully inside the frame on every frame (mesh silhouette search), no gulls, sun glint x0.3, snap push x1.22 with a pan on "จาไมกา", sea clock x2.
- DOF off, no text, no caption_shade in every raw json. `qa_auto` PASS.

## Frame-diff (in-shot g 1385..1467)
median **4.39**, p90 **10.95** (draft 4.55 / 11.21). Targets: median >= 4, p90 >= 10: **met**. (qa_stats on all frames: 4.03 / 11.65.)
