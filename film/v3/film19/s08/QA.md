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
- Heads: width 146-266 px, centre y 484-622, chin at most y 713; the wig lappets (centre + 1.17 x width) end above y 880 on every frame (contact sheet). No black frames.
- Mouth: moves only for g 622..669 (inside mouth_open_at); outside: fixed expression (smug flat, laughing). `meta.json mouth_moving_outside_window_frames = []`.
- Contact: feet on the floor with the decal and shadow; true cast19 scale; no DOF, no text, no caption_shade (all keyed false in raw/g_*.json).
- qa_auto: PASS (no black / blank / magenta / frozen frames). The "no visible change at g 545, 661" note is the handle: the real cuts happen in the conform.

## Frame-diff (90x160 grey, in-shot pairs g 546..660)
median **3.77**, p90 **6.71** (target >= 4 / >= 12): BELOW TARGET. Reason: this hall is dark red with low contrast, and every wider orbit that raised the numbers (median 5.4, p90 10) swung the camera behind the quadrant stand, the Board table or a chair back and hid the laughing face, so the clean, face-first camera was kept. Reported as a deviation.

## Revision
Re-rendered after the director's TAKE gate (QA_TECH.md): the laugh mouth now starts at g 623 (mouth flat and eyes open before; the bounce and shoulder shake start earlier), the turn starts side-on with the gaze at the Board and settles on the lens by about g 598, the snap is framed up and left so the wig lappets end above y 880 and the raised pointing arm shows at g 640-660. Frame-diff stays below target because every camera that moves more either hides the face behind the quadrant stand, the Board table or chair backs, or pushes the wig below y 880; reported as a deviation.

## Revision 2 (director's option 3)
- shot.py now deletes the faces of the Board table's left-row chair that stood between the orbiting camera and the mocker (hide_chairs(): 85 faces in the box x -2.95..-1.35, y 0.7..3.8, z 0.04..2.45; runtime set dressing in this shot only). Orbit +11.5 deg/s round the open (right) side with a slide past the bookcases, 2x belly squash and a 0.08 D hop at 3 Hz, snap x1.3 (g 633-651, peak 2.5) with a pan on 'นาฬิกาเนี่ยนะ'.
- The chair was not the only limit: the Board table itself fills x > -1.3 (top z 1.5), so a camera that pushes in beyond x -1.45 goes inside the table (black frames, seen on drafts with arc 15 and with rise). With the camera kept at x <= -1.45 the frame-diff is 3.77 / 6.71 (a 4.29 / 8.06 draft went inside the table). Still below target (median >= 4, p90 >= 10).
- Not tried: option (2), moving his mark up to +1 D away from the camera.
