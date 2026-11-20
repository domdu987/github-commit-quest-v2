# s17 QA: film 19, shot 17 (the ship sails on, the camera pulls back) -- SHIP ship_aerial, NOON  (round 2)

## Delivered
- `take.mkv` (libx264rgb crf 6, 37 MB, 30 fps): first_g 1271, 122 frames, 720x1280, 10 spp, 2 threads. No captions / audio.
- g 1271..1279 in-handle, **g 1280..1383 = shot 17 (42.65-46.12 s)**, g 1384..1392 out-handle. Join in: hard cut from shot 16; out: dissolve 11 into shot 18 (centred on g 1384).
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## Round-2 fixes (QA-tech)
- **Long V wake:** the camera now starts BEHIND the ship (the ship sails away from it), so the wake trails toward the lens. The set's wake fades by ~150 m, so a 300 m wake is added through the set's own `streaks` hook (runtime, no set edit): 10 Kelvin arms (half-angle ~19 deg, 5 per side) plus a turbulent centre line. A long white V is visible in the whole shot.
- **Ship fully in the frame on every frame:** the camera path was searched under a constraint (ship bbox key points >= 30 px inside, found 57 px). The ship travels across the frame (orbit + slide) and sinks as the camera cranes up.
- **Gulls hidden** (no clipped gull); **sun glint x0.45** (the white glare patches at the start are smaller).
- **Snap back** on "ไกล" (g 1377..1392, 15 f, x0.85 with a pan and a rise): lands on the word.
- **Sea edge:** grid fitted at runtime (`widen_sea`) to a virtual camera 11x farther at the same azimuth, 1300x1800 vertices (no set edit). No edge seen.
- DOF off, no text, no caption_shade in every raw json.

## qa_auto
PASS. History: every version with a bigger snap-back (x0.58-0.70) FAILED "suspected blur" on the post-snap frames (a tiny ship over smooth dark sea has little Laplacian variance); the snap is therefore a gentler x0.85 and lands last. Note: soft frames g 1387-1392 (the handle only, not screen time).

## Frame-diff (in-shot g 1281..1383)
median **3.32**, p90 **4.22** (draft of a similar version 3.15 / 3.94). **Below the median >= 4 / p90 >= 10 rule.** A high aerial over smooth sea moves few pixels; larger snaps give pair diffs of 8-11 for a few frames (tested, g 1376-1380) but fail the blur check and shrink the ship below the "fill the frame" brief. I did not find a camera path that meets frame-diff, "whole ship in frame", "long V wake" and qa_auto together.
