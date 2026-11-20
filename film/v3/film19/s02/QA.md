# s02 QA: film 19, shot 2 (the lone ship) -- SHIP ship_aerial, NOON  (re-rendered after the director's QA-tech fail)

## Delivered
- `take.mkv` (libx264rgb crf 6, 22 MB, 30 fps): first_g 48, 71 frames, 720x1280, 10 spp, 2 threads. No captions / audio.
- g 48..56 in-handle, **g 57..109 = shot 2 (1.91-3.65 s)**, g 110..118 out-handle. Joins: hard cut in (from shot 1) and hard cut out (to shot 3).
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## Shot
No actors. Fix of the three QA-tech findings:
1. **Camera:** starts close (0.5x the aerial distance) and 30 deg off the preset azimuth, so the ship and its bow wave / wake arcs fill the frame; pulls back (9 %/s), cranes up (110 px/s), slides (150 px/s) and orbits (-18 deg/s) so the ship drifts across the frame and shrinks; a small snap pull-back (x0.8, 14 f, g 79..93) mid-shot. Moving on frame 0 and on the last frame; never parked.
2. **Seam:** the earlier vertical tile / glitter step is gone: the camera no longer looks at the glitter strip's hard edge, and the sea grid is fitted at runtime (`widen_sea`) to a virtual camera 11x farther at the same azimuth, 1300x1800 vertices (no set module edited). Checked on stills and the full contact sheet: no vertical seam, no grid edge.
3. **Composition:** the lower half is no longer empty: the ship and the wake foam arcs occupy it throughout.
- DOF off, no text, no caption_shade in every raw json. `set_sea` / `set_roll` with t = g/30 on every frame.

## Frame-diff (in-shot g 58..109)
median **3.87**, p90 **4.77** (draft 3.99 / 4.92). Median is just under 4; p90 is far under 12: a shot under 2 s over smooth sea with a gentle snap. A harder snap shrinks the ship onto empty water (the QA-tech composition complaint).
