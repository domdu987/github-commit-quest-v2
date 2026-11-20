# s20 QA: film 19, shot 20 -- HALL hall_low DAY (the mocker shrugs: "ฟลุ๊ค! ต้องลองใหม่!")

## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps): first_g 1572, 102 frames, 720x1280, 8 spp, 2 threads. Frames are not in git.
- g 1581..1664 = shot 20 (52.71-55.49 s); g 1572..1580 in-handle, g 1665..1673 out-handle (9 frames each, in 3D). Hard cut in from shot 19 (ship_coast), hard cut out to shot 21 (ship_coast BARBADOS).
- `meta.json`, `cues.json`, `contact.jpg` (cyan = y 880), `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `framediff.json`; `c19.py`, `shot.py`, `deliver.py`.

## Shot
astro19 stands smug at mark mocker_telescope (arched window, telescope tube behind him), still smirk. On "คนเดิมยักไหล่" (g 1615) he lifts both palms up into the shrug (astro_shrug_fluke, hands pumped out and up), head tilting. The lip-sync window opens at g 1626 (54.25 s -0.15): "ฟลุ๊ค!" from g 1633 with a hop and a shoulder pump, then "ต้องลองใหม่!" with a second smaller pump (g 1651-1663), mouth driven with talk_mouth until the window closes (g 1672); a still smirk before and a still smile after. Camera: hard cut in already moving, from the telescope side (x -4.9) with push 10 %/s + slide 45 px/s + slow orbit 13 deg/s (the Board's chair backs sweep in the foreground); one SNAP x1.4 (g 1628-1646, peak 2.6) with a pan on "ฟลุ๊ค!" (g 1633).

## Checked
- Heads: width 154-289 px, centre y 467-612, chin at most y 704; wig lappets end above y 880 on every frame.
- Mouth: moves only for g 1626..1672 (mouth_open_at); `meta.json mouth_moving_outside_window_frames = []`.
- Palms-up shrug readable at g 1625-1665 (hands out at both sides, framed); feet on the floor with contact decal in the wide first half; no DOF, no text, no caption_shade.
- qa_auto PASS; the "no visible change at g 1581, 1665" note is the handle.

## Frame-diff (90x160 grey, in-shot pairs g 1582..1664)
median **4.22**, p90 **10.68**: meets the per-take rule (median >= 4, p90 >= 10; the film-wide p90 target of 12 is the director's).

## Revision (director's QA-art / TAKE gate round 2)
- Shrug: both hands now go to about (+-1.30, 0.95), palms open, layered in FRONT of the wig and gown, so the palms-up pose reads from g 1615 and stays in frame through the snap (the hand tips touch the frame edges in the tightest frames g 1639-1666). Snap k 1.6 -> 1.4 with the pan keeping him centred (head x 345-377).
- Mouth: smaller smug talk (small ('open', 0.15, 0.09) / flat ('open', 0.20, 0.05) shapes blended with the smirk) instead of the wide shouting mouth; still driven only inside the window (g 1626..1672), smirk elsewhere.
- Smug rocking on the heels before the shrug lifts the median to 4.16.
- Round 4: during the snap the hand targets come in from +-1.30 to +-1.00 (g 1628-1641) so both palms stay inside the frame on every frame (g 1640 to the end checked on the contact sheet); squash 0.04 and head_roll -10 on the shrug. Snap k stays 1.4 (peak 2.6).
- Round 5: hand targets come in from +-1.15 to +-0.72 over the snap (g 1628-1641), no sideways pump; checked on every frame g 1609-1673 from the raw head positions (hand centre = head x +- hx*width, fingertips +0.3 D): both hands stay inside x 40-680 (0 frames outside; the projection matched the mitt positions seen on the contact sheet to within ~5 px).
