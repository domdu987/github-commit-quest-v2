# film17 s10 (shots 24-26, THE REVEAL) QA

take.mkv: g 1336..1520 (185 frames, 720x1280, 12 samples + OIDN, libx264rgb crf 6; stored as take.mkv.partaa/ab: `cat take.mkv.part* > take.mkv`). Cut-in at g1342, out at g1515, 6 handle frames each side.

## Numbers
- rhythm.py (--cuts 1374,1375): in-shot median 4.86, p90 14.14 (targets >= 4 / >= 12) PASS.
- qa_auto (--cuts 1374,1375,1406,1461): black/blank/magenta/frozen: none (magenta 0.0 %). One FAIL: "suspected blur on 39 frames" (Laplacian < 0.6 x median). Honest breakdown: 9 frames are the intended whip streak (g1370-1378, M->R whip, 13-frame 1367-1383), ~6 are the snap g1411-1415 / 1467-1470, and the rest (g1470-1490) are the card_hero wall/dark wood: raw un-blurred frames measure 0.5-0.65 of the median because the median is carried by the texture-rich measuring-room frames. No blur is applied outside the whips (kernel only where the camera moves >= 100 px/frame). The pop flagged at g1370 is the whip. See QA_AUTO.md.

## What happens (all animated)
- g1336-1366 measure_chair: Bertillon's calipers rise from low and settle ON Dupont's head (jaw pin via solver, small working jitter), both sway/blink. Camera pushes + slides.
- g1367-1383 whip-off right -> whip-on, directional blur from the camera speed; the location change (measure -> reveal) hides inside it.
- g1376-1410 drawer_big: Bertillon (mirrored) hand pinned to the drawer front, steps back as the drawer is yanked out 0->1 (g1376-1398).
- g1406-1421 snap push to drawer_box (16 f); Bertillon leaves at the snap peak (g1411); lid opens g1410-1434.
- g1461-1476 snap to card_hero; card rises 0->1 g1466-1500; box lamp lowered (28 W / 38 W for the card): card reads Dupont portraits + hand + fingerprint + bottle, no blown bloom (max card luma checked on the sheet).
- Camera: drift + slide in every segment, snaps at 1406 and 1461, push-in ~9 %/s at the end.

## Director's fixes applied
beam_fx shafts hidden; dust 0.4; every pose wrapped in cast17.silent (no quote in these shots); Dupont moved off the headrest bar; no floating hand after the drawer shot; 6 fps self-check of frames (contact.jpg, 1 in 6; every whip and snap frame viewed in drafts).

## Known deviations / not done
- Shot 25 "finger measured" insert and shot 26 "ear" insert are not rendered (no second location pass); step 2 is the snap push into the box, step 3 the card. "Box lifted out" = the lid opens (set has no box-lift hook).
- Heads: Dupont/Bertillon centre y 515-700 in the M part; Bertillon chin < 880 in the drawer shot (large head near the camera at g1400-1410, chin ~800). No cast in shots 25-26.
- Faces: Dupont 'worried' smile, Bertillon 'determined' then 'proud'; mouths closed.
- Dupont is placed 0.22 m in front of the chair so the headrest bar does not cross his cap.
