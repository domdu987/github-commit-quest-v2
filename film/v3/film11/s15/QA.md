# s15 QA (render team 3)
- g 892..988 (97 frames, 898..982 + 6 handles each side), room_morning / A, transition_in dissolve 8, 12 samples, ~10 s/frame wall.
- QA_AUTO: PASS (an earlier render FAILED a frozen run at g 892-898: static camera before g0; fixed with camera extrapolation + more idle life, re-rendered).
- Heads above y 880. No mouths. Blister overlay on James (lying + standing cards). James lies (lie card) -> sits/leaps (standing card, jump arc bed edge -> floor) -> runs about; mother sit_relieved by the bed, Jenner proud behind (moved to (-0.9, 7.9) so no chair hides him).
- Log noise: Blender prints "Image file ... does not exist" for the hidden card's sprite on frames where it is hidden; harmless.
- Gate fix 2026-11-18: the sore card is hidden while James is standing (upper_arm anchors sit on the torso, the card floated). QA_AUTO PASS.
