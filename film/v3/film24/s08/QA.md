# QA s08 (shots 8a + 8b), g 728-924, 197 frames, 134 deliverable g 734-918
- 8a macro_spikes g 728-860 (DOF, world-fixed slide, no characters); spikes appear 1/2/3 at g 795/831/852; 8b roof_top g 861-924, push 16 %, two kneeling hammerers, ports open ~g 891.
- qa_auto PASS, magenta 0 %, jitter median 0.11 px. Kneeler heads y<=644 (band 880).
- Render 38.1 s wall / 73.3 s CPU per frame. Hard cut at 861 checked on cut_861 sheet.
- Deviation: kneelers camera-facing (no yaw_fixed, edge-on otherwise).
