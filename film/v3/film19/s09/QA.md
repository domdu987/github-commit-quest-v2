# s09 QA: film 19, shot 9 -- HALL hall_low DAY, closer (the mock-royal bow and "ให้พระราชามาจับเวลาเองเลย!")

## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps): first_g 652, 130 frames, 720x1280, 8 spp, 2 threads. Frames are not in git.
- g 661..772 = shot 9 (22.02-25.78 s); g 652..660 in-handle, g 773..781 out-handle (9 frames each, in 3D). Cut in from shot 8 (same set and mocker), cut out to shot 10 (hall_wide).
- `meta.json`, `cues.json`, `contact.jpg` (cyan = y 880), `QA_AUTO.md` + `phone_sheet.jpg`, `framediff.json`; `c19.py`, `shot.py`, `deliver.py`.

## Shot
astro19 (astro_mock_bow lerped from astro_mock_point, the pocket watch in his right hand wobbling as if timing a shot, left arm swept back) at mark mocker_telescope, closer than shot 8 (head 220-400 px). The bow rocks all shot and goes deepest on "ให้พระราชามา" (g 722); small toe rise. Mouth driven with talk_mouth for the whole window (20.80-25.75 s, i.e. through g 773..777), a still smile afterwards. Camera: moving on frame 0, from the telescope side (x -4.9) with push 7 %/s + slide 25 px/s + slow orbit; one SNAP x1.5 (g 743-762, peak 1.9) with a small pan on "จับเวลาเอง" (g 748).

## Checked
- Heads: width 220-402 px (the last 20 frames are a very tight close-up, wig edges leave the frame by design), centre y 528-603, lowest head bottom y 766 (<880).
- Mouth: moves only inside mouth_open_at (g 652..781 are all within the 20.80-25.75 s window +-0.15 s, handles included); `mouth_moving_outside_window_frames = []`.
- The pocket watch (gold, tick marks only, no text) is small at his hand: visible g 690-740. Feet / floor are cropped out after the first ~50 frames (low close-up).
- No DOF, no text, no caption_shade. qa_auto PASS (the "no visible change at the cut g" note is the handle).

## Frame-diff (90x160 grey, in-shot pairs g 662..772)
median **4.40**, p90 **10.74** (target >= 4 / >= 12): median met, p90 about 1.3 under target. The snap is limited by keeping the face in frame and out of the furniture; a bigger pan sent the mocker off screen.
