# T1a QA self-check (g0-171). Result: FAIL, awaiting a fix list from the director
Render: 720x1280, 16 samples + OIDN, 2 threads; motion blur 0.5 on g152-171 only. Real cast via stage_cast2 with the g105 key-still assignment on every frame. Viewed: contact.jpg (every 8th frame) plus g0, 29, 60, 76, 86, 95, 105, 120, 155 at full size and at 360x640. Nothing else was viewed frame by frame.

| g | what I see |
|---|---|
| 0, 29 | Rooftop BIGZOOM start: cobalt zinc roofs, red chimneys with smoke, lit windows, orange horizon, Notre-Dame tower top-left. Reads well. The French window is NOT yet the brightest spot. |
| 60-61 | Camera against a lit window: a flat yellow/white block fills the frame (luma 181-216, qa_auto "blank"). Defect. |
| 76 | Close on the French window with the red/white awning. A large black polygon fills the window opening. Defect. |
| 86-93 | Nearly or fully black frames (luma 0-14). The window opening is a black slab. qa_auto black-frame FAIL. Defect. |
| 95 | Camera is inside the room, pointing across it. Clean: clock, calendar MARS 1882, tripod, rug, props. No cast in frame. |
| 105 | Key still, OK'd by the director: Bertillon front-on, prisoners front-facing, feet on the floor. |
| 100-150 | A large flat dark-brown/black rectangle stands behind the bench prisoners. Likely the mirrored back-of-head/coat cover (`_back_cover`) for the back view. It reads as a black slab, which the brief says to report. A prisoner and Bertillon are half hidden by it. Defect. |
| 120 | Same slab covers about 40 % of the frame. Defect. |
| 155-156 | Overexposed yellow-white glow fills the frame (luma 169-202), motion blur on. Defect. |

Luma (my own Rec.601 mean, qa_stats2.py is not in the repo): g0-95 72.4, g96-171 85.5, whole part 78.2. Target 95-112: BELOW.
Shimmer: not checked as a clip. Flat roofs in stills look clean.
qa_auto: FAIL. black frames 87-93, blank 61/88/91, "suspected blur" on 50 frames (g36-50 and later; motion blur is only on in g152-171, so this is probably the camera speed on the roof pass), pops at g94, 131, 155-157.
Not claimed: façade-sign rule (g200-300 belongs to T1b), BIGZOOM report (not re-run).
