# s12 Look A QA
Same shot.py, JOSEON_LOOK=A (no haze, no DOF, full 720x1280, no post(), [8] samples). Frames g 1251..1418 (same range as the B take, g0 1257, g1 1412 exclusive, 168 frames).
Delivered: `take_A.mkv` (libx264rgb crf 12, 30 fps, 23.5 MB), `meta_A.json`, `contact_A.jpg` (cyan = y 880), `QA_AUTO_A.md` (qa_auto PASS). No grade applied: the v1.1 grade runs in conform.
Render: 10.9 s wall / 20.7 s cpu per frame (2 procs x 2 threads). B take unchanged (take.mkv, frames_B/raw_B kept local).
Geometry, timing, staging, camera, set hooks and mouths are identical to the B QA (s12/QA.md): the same shot.py renders both looks; head and feet numbers are in work/qa_A.txt.
Checked on contact_A.jpg: heads above y 880, feet on their surfaces, mouths only in the quote windows (where the take has any), hard cuts only.
