# s18 QA: film 19, shot 18 (the ship under full sail) -- SHIP ship_hero, NOON  (round 11)

## Delivered
- `take.mkv` (libx264rgb crf 6, 35 MB, one file, no parts): first_g 1375, 102 frames, 720x1280, 12 spp, 2 threads. No captions / audio.
- g 1375..1383 in-handle, **g 1384..1467 = shot 18 (46.12-48.92 s)**, g 1468..1476 out-handle. Join in: dissolve 11 from shot 17; out: dissolve 13 into shot 19.

## Round-11 fixes
1. **JAMAICA on the snap.** A green island (sand rim, dome, 5 palms, ~10 % of the frame width) is placed on the horizon ahead of the ship, left of the bow; the snap on "จาไมกา" (g 1428-1445) pans TOWARD it, so it ends in frame beside the bow, clear of the sails, and stays visible into the dissolve to s19. (No "JAMAICA" banner.)
2. **William acts.** g 1384-1409 looks down at the H4 on his palm; g 1410-1426 glances up at the sea and turns his head; g 1427-1440 raises the watch (drawn at 2x) toward the island with an excited face, a hop of joy on the word (g 1436-1456); then holds it up. His deck contact is visible (he stands on the forecastle, port side, at 4x scale; head 26-42 px).
3. **Motion.** The quiet start has a faster slide (35 px/s) and orbit (-8 deg/s); the snap carries the camera toward the island. Pair diffs ~5.6 median / ~11.5 p90 (qa_stats).
4. **Bow wave:** the glossy blue tube is now matte white foam (the blue mix is removed from the base / emission colour, emission and specular cut).
5. **Glint:** the sun glint light is off (the lower-third glint blobs are gone); the old pale headland is hidden (JAMAICA is the one island).
- Kept: colour (**luma 100.3, saturation 0.645** by qa_stats), ship fully inside the frame, foreground crests, no gulls. DOF off, no text, no caption_shade in every raw json. `qa_auto` PASS.

## Frame-diff (in-shot g 1385..1467)
median **5.99**, p90 **11.06** (qa_stats on all frames 5.56 / 11.52). Targets median >= 4, p90 >= 10.5: met.

## v2 (round 12 follow-up)
1. **The island is bigger (~20 % of the frame width, ~80 m) and left-ahead of the bow** (it appears on the horizon at the word and stays in frame beside the ship into the dissolve); the snap pans toward it. (No "JAMAICA" sign; the ship's heading is unchanged, +y.)
2. **William:** mirrored to face the island; on the word (g 1434-1437) the H4 goes ABOVE his head on the island side, open-mouthed excited face held to the end of the shot (> 0.5 s), a hop, and one warm sparkle on the watch (g 1436-1454, an emissive 4-point star following the watch anchor).
3. **Bow wave:** the pillow is half its size (x0.5); not turned into toon spray chunks.
4. **Polish:** +0.1 EV eased out over g 1384-1402 (luma ~88 there); lower-third foam lines 28 -> 20.
- **qa_stats: luma 98.2 (band 85-110), saturation 0.659.** Frame-diff (deliver.py, in-shot g 1385..1467): median **5.33**, p90 **10.21** (qa_stats on all frames 4.85 / 10.41): both >= 10. `qa_auto` PASS. DOF off, no text, no caption_shade.

## v3 (round 13 follow-up)
- **Early motion (blocking):** the quiet start now moves: an eased 9 D pan over g 1375-1412 and a faster ship roll (clock x3.5). Mean pair diff g 1385-1404 is 2.7 (was 1.5-1.9); **ffmpeg-gray bilinear 90x160, pairs g 1385-1467: median 6.71, p90 12.17** (target >= 10.3); deliver.py (mean RGB) median 6.90, p90 12.39.
- **Luma:** +0.2 EV eased out over g 1384-1404 (was +0.1). qa_stats: luma **102.1**, saturation 0.628.
- **Foam:** the foreground foam lines are 32 (was 28 -> 20 in an earlier try): 20 failed `qa_auto` "suspected blur" on g 1394-1405 once the early pan was added (the smooth sea there); so the optional thinning of g 1415-1432 was not done.
- **Violet glow under the bow (g 1430-1467): NOT removed.** The bluish bow-mist cards (`skyobj_mist*` under `bow_fx`) are hidden and the foam / sea foam colours warmed, but the violet patch left of the bow is hull-shaded foam lit only by the blue sky ambient; it did not change. Removing it would need a change of the approved scene ambient.
- qa_auto PASS. DOF off, no text, no caption_shade. Island, William's acting, the sparkle and the colour unchanged.
