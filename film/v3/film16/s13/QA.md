# s13 QA: film 16, shot 13 (LINE line_trench, DAY) -- mule team, plough, lead pipe unrolling
- take.mkv: g 822..900 (79 f; shot = g 831..891, handles 9 each side), 720x1280, 7 spp, libx264rgb crf 6, 33 MB. transition_in dissolve 15 f, hard cut out (g 892).
- Camera: custom, 10 D off the furrow, 3.4 D up, tracks the plough; push 7 %/s + slide + arc; one snap x1.2 with a 13 D pan from the mules to Cornell + pipe on "ตะกั่วใต้ดิน" (g 868-881).
- Scene: set_trench / set_pipe keyed per frame (plough 0.50 -> 0.57); 2 mules (cycle pull, harness), Cornell with plough handles, 2 workers, Morse following; runtime foreground grass/crate/shovel.
- Checked at 6 fps on the draft + final contact: heads whole and above y 880, centre ~y 450-760; contact shadows present; nobody speaks; no DOF, no text.
- qa_auto PASS (note: the planned cut g 892 sits in the handle, expected).
- Frame-diff (90x160 grey, in-shot): median 7.57, p90 27.73 (target 4 / 12).
- s/frame: 10.85 wall, 21.2 cpu (two processes at once).
- Differs from plan: the preset line_trench camera sits behind the team (mules off-frame), so a custom side camera is used; the pipe reads as a pale grey strip in the furrow, small at the end frames; Morse is mostly out of frame.
