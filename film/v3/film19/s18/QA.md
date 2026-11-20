# s18 QA: film 19, shot 18 (the ship under full sail) -- SHIP ship_hero, NOON  (round 2)

## Delivered
- `take.mkv` (libx264rgb crf 6, 25.6 MB, 30 fps): first_g 1375, 102 frames, 720x1280, 12 spp, 2 threads. No captions / audio.
- g 1375..1383 in-handle, **g 1384..1467 = shot 18 (46.12-48.92 s)**, g 1468..1476 out-handle. Join in: dissolve 11 from shot 17; out: dissolve 13 into shot 19.
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## Round-2 fixes (QA-tech)
- **Ship fully inside the frame on every frame.** The hero camera is pulled back 1.15x horizontally at its own height; the camera path was searched against the real ship mesh silhouette (4000 vertices projected per frame, margin >= 15 px, found 39 px). The ship travels across the frame (centre x 373 -> 522) with an orbit, slide and crane.
- **Gulls hidden** (`gulls_gullt`, `gulls_gullw` keyed off every frame): no clipped gull.
- **Sun glint toned down** (the `glint` light energy x0.3): no blown patch.
- **Snap:** push x1.22 with a pan, 17 f (g 1428..1445) on "จาไมกา" (heard ~g 1438).
- **Sea:** the grid is fitted to a virtual camera 1.8x farther and higher (runtime, no set edit; 900x1300 vertices), so the pulled-back camera sees no grid edge or void. Sea clock x2 (livelier swell and foam).
- DOF off, no text, no caption_shade in every raw json.

## Frame-diff (in-shot g 1385..1467)
median **2.69**, p90 **9.07** (draft 2.71 / 9.32). Target for the take is median >= 4 and p90 >= 10: **p90 is just under, median is under.** With the whole ship inside the frame the camera can only move a little (the ship is ~60 % of the frame width); a hero view of smooth sea with the camera held back gives pair diffs of 1-1.5 away from the snap (the original, ship-clipping framing gave 3.1). A faster sea clock (x3) made it worse (2.48 / 5.58). I kept the framing rule over the number.
