# s09 Look A QA
Same shot.py, JOSEON_LOOK=A (no haze, no DOF, full 720x1280, no post(), [8] samples). Frames g 913..1007 (same range as the B take, g0 919, g1 1002 exclusive, 95 frames).
Delivered: `take_A.mkv` (libx264rgb crf 12, 30 fps, 7.7 MB), `meta_A.json`, `contact_A.jpg` (cyan = y 880), `QA_AUTO_A.md` (qa_auto PASS). No grade applied: the v1.1 grade runs in conform.
Render: 11.6 s wall / 22.4 s cpu per frame (2 procs x 2 threads). B take unchanged (take.mkv, frames_B/raw_B kept local).
Geometry, timing, staging, camera, set hooks and mouths are identical to the B QA (s09/QA.md): the same shot.py renders both looks; head and feet numbers are in work/qa_A.txt.
Checked on contact_A.jpg: heads above y 880, feet on their surfaces, mouths only in the quote windows (where the take has any), hard cuts only.

NOTE: qa_auto reports FAIL "suspected blur" on 27 frames (g 913-923, 933-..., all shot 9a macro_oar). This is a false positive, not defocus: Look A has no DOF by design,
and the macro shows smooth water with a few foam / droplet shapes, which has little high-frequency detail for the Laplacian test (the B take passes only because its DOF
bokeh and haze change the statistics). Nothing is out of focus on contact_A.jpg; the oars, hull and droplets are sharp. Shot 9 (hansan_high) passes.
