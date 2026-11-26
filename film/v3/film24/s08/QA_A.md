# QA_A s08 (Look A), g 728-924, 197 frames (g1 919 exclusive)
- JOSEON_LOOK=A, 8 samples, 720x1280 direct, no post/DOF/haze, ungraded. Cut at 861 checked on the contact sheet.
- Deviation: shot.py got one guard (`if self.focus is not None`) because Look A builds no DOF focus empty (macro shot 8a crashed otherwise); frames are otherwise identical in camera/animation to B.
- qa_auto PASS on take_A.mkv; jitter median 0.11 px.
- take_A.mkv crf 12 (17.5 MB), 15.2 s wall / 29.9 s CPU per frame.
