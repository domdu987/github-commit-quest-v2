# s20 QA: film 19, shot 20 -- HALL hall_low DAY (the mocker shrugs: "ฟลุ๊ค! ต้องลองใหม่!")

## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps): first_g 1572, 102 frames, 720x1280, 8 spp, 2 threads. Frames are not in git.
- g 1581..1664 = shot 20 (52.71-55.49 s); g 1572..1580 in-handle, g 1665..1673 out-handle (9 frames each, in 3D). Hard cut in from shot 19 (ship_coast), hard cut out to shot 21 (ship_coast BARBADOS).
- `meta.json`, `cues.json`, `contact.jpg` (cyan = y 880), `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `framediff.json`; `c19.py`, `shot.py`, `deliver.py`.

## Shot
astro19 stands smug at mark mocker_telescope (arched window, telescope tube behind him), still smirk. On "คนเดิมยักไหล่" (g 1615) he lifts both palms up into the shrug (astro_shrug_fluke, hands pumped out and up), head tilting. The lip-sync window opens at g 1626 (54.25 s -0.15): "ฟลุ๊ค!" from g 1633 with a hop and a shoulder pump, then "ต้องลองใหม่!" with a second smaller pump (g 1651-1663), mouth driven with talk_mouth until the window closes (g 1672); a still smirk before and a still smile after. Camera: hard cut in already moving, from the telescope side (x -4.9) with push 10 %/s + slide 45 px/s + slow orbit 13 deg/s (the Board's chair backs sweep in the foreground); one SNAP x1.5 (g 1628-1646, peak 2.0) with a pan up and left on "ฟลุ๊ค!" (g 1633).

## Checked
- Heads: width 154-263 px, centre y 489-614; chin at most y 701; the wig lappets (head centre + 1.17 x width, checked on the contact sheet) end above y 880 on every frame (re-framed after the director's TAKE gate on s08: snap x1.5 with an upward pan).
- Mouth: moves only for g 1626..1672 (mouth_open_at); `meta.json mouth_moving_outside_window_frames = []`.
- Palms-up shrug readable at g 1625-1665 (hands out at both sides, framed); feet on the floor with contact decal in the wide first half; no DOF, no text, no caption_shade.
- qa_auto PASS; the "no visible change at g 1581, 1665" note is the handle.

## Frame-diff (90x160 grey, in-shot pairs g 1582..1664)
median **3.80**, p90 **10.16** (target >= 4 / >= 12): BELOW TARGET by 0.2 / 1.8. The dark red hall is low in contrast, and a wider orbit or a bigger pan hides the face behind chair backs or the quadrant stand. Reported as a deviation.
