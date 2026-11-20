# s08 QA: film 19, shot 8 -- HALL hall_low, DAY (the mocker's belly laugh and the quote "นาฬิกาเนี่ยนะ!")

## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps): first_g 536, 134 frames, 720x1280, 8 spp (HALL set samples), 2 threads. Frames are not in git.
- g 545..660 = shot 8 (18.17-22.02 s); g 536..544 = in-handle, g 661..669 = out-handle (9 frames each, rendered in 3D, the move and the laugh continue). Cut in from shot 7, cut out to shot 9.
- `meta.json`, `cues.json`, `contact.jpg` (cyan = y 880), `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `framediff.json`. Scripts: `c19.py` (copy of s01's), `shot.py` (`probe`, `camreport`, `stills`, `final`), `deliver.py`.

## Shot
| g | beat |
|---|---|
| 536-600 | astro19 stands smug at mark mocker_telescope (the telescope tube and the arched window behind him), turns from profile toward the lens; shoulders start to shake. Flat mouth. |
| 603-636 | BELLY LAUGH: cast19.laugh_cycle (3 Hz squash, head-roll rocking, tears) plus a 0.06 D hop of the feet at 3 Hz. Fixed laughing mouth until the window opens. |
| 622-669 | lip-sync window (20.80 s -0.15 = g 622): "ฮ่า ฮ่า ฮ่า!" (driven laugh mouth), then "นาฬิกาเนี่ยนะ!" from g 637 (caption 21.14 s): the mouth is driven with cast19.talk_mouth. |
| 640-669 | he straightens and mock-points (astro_mock_point). |
Camera: low, moving on frame 0; drift push 8 %/s with a slide and a 10 deg/s orbit (parallax of the bookcases, chair-back FG), one SNAP x1.3 (g 632-651, peak 2.2) with a pan on "นาฬิกาเนี่ยนะ" (g 637).

## Checked
- Heads: width 146-314 px, centre y 570-655, lowest head bottom y 807 (caption band y 880 stays clear of heads). Face never covered by a foreground prop (an earlier orbit swung the camera behind the quadrant stand at g 607-634; rejected).
- Mouth: moves only for g 622..669 (inside mouth_open_at); outside: fixed expression (smug flat, laughing). `meta.json mouth_moving_outside_window_frames = []`.
- Contact: feet on the floor with the decal and shadow; true cast19 scale; no DOF, no text, no caption_shade (all keyed false in raw/g_*.json).
- qa_auto: PASS (no black / blank / magenta / frozen frames). The "no visible change at g 545, 661" note is the handle: the real cuts happen in the conform.

## Frame-diff (90x160 grey, in-shot pairs g 546..660)
median **3.39**, p90 **5.93** (target >= 4 / >= 12): BELOW TARGET. Reason: this hall is dark red with low contrast, and every wider orbit that raised the numbers (median 5.4, p90 10) swung the camera behind the quadrant stand, the Board table or a chair back and hid the laughing face, so the clean, face-first camera was kept. Reported as a deviation.
