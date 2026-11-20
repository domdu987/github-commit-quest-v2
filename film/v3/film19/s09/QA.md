# s09 QA: film 19, shot 9 -- HALL hall_low DAY, closer (the mock-royal bow and "ให้พระราชามาจับเวลาเองเลย!")

## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps): first_g 652, 130 frames, 720x1280, 8 spp, 2 threads. Frames are not in git.
- g 661..772 = shot 9 (22.02-25.78 s); g 652..660 in-handle, g 773..781 out-handle (9 frames each, in 3D). Cut in from shot 8 (same set and mocker), cut out to shot 10 (hall_wide).
- `meta.json`, `cues.json`, `contact.jpg` (cyan = y 880), `QA_AUTO.md` + `phone_sheet.jpg`, `framediff.json`; `c19.py`, `shot.py`, `deliver.py`.

## Shot
astro19 (astro_mock_bow lerped from astro_mock_point, the pocket watch in his right hand wobbling as if timing a shot, left arm swept back) at mark mocker_telescope, closer than shot 8 (head 220-400 px). The bow rocks all shot and goes deepest on "ให้พระราชามา" (g 722); small toe rise. Mouth driven with talk_mouth for the whole window (20.80-25.75 s, i.e. through g 773..777), a still smile afterwards. Camera: moving on frame 0, from the telescope side (x -4.9) with push 7 %/s + slide 25 px/s + slow orbit; one SNAP x1.5 (g 743-762, peak 1.9) with a small pan on "จับเวลาเอง" (g 748).

## Checked
- Heads: width 196-257 px, centre y 489-547, chin at most y 655; the wig lappets (centre + 1.17 x width, max 813) end above y 880 on every frame. Face (without the wig) at most ~26 % of the frame height (client gate: <= ~35 %, brief: <= ~30 %). No black frames.
- Mouth: moves only inside mouth_open_at (g 652..781 are all within the 20.80-25.75 s window +-0.15 s, handles included); `mouth_moving_outside_window_frames = []`.
- The pocket watch (gold, tick marks only, no text) is small at his hand: visible g 690-740. Feet / floor are cropped out after the first ~50 frames (low close-up).
- No DOF, no text, no caption_shade. qa_auto PASS (the "no visible change at the cut g" note is the handle).

## Frame-diff (90x160 grey, in-shot pairs g 662..772)
median **4.99**, p90 **10.57** (12 in-shot pairs >= 10): meets the per-take rule.

## Revision (client gate: no extreme close-ups)
- The old push-in on 'จับเวลาเอง' took the face to ~44 % of the frame. Now: the camera starts 10 % further back and the drift push is 4 %/s; the end is a short FOV punch instead of a long push: lens x1.10 with the deep bow (g 722), x1.06 micro-punches on the bow beats (1.5 Hz), and a snap k 1.12 (peak 2.6, g 744-758) with a x1.06 lens punch on 'จับเวลาเอง' (g 748) that eases back. Head width 196-257 px, face about 25-26 % of the frame at its biggest. The look point is lowered 0.33 D so the wig stays above y 880.
- qa_stats (take.mkv, handles included):
```
take.mkv: 4.3s, shots=1, mean shot 4.33s, median 4.33s, shortest 4.33s, shots<1.5s: 0
   saturation 0.677, brightness 69.6, in-shot motion median 5.87 p90 11.25
```
