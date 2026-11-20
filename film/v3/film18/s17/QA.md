# QA s17 (render team 5, film 18) round 11 - frames g1309-1387 (+6 handles: take.mkv g1303-1393, 91 frames), jimo_in NIGHT
Frame-diff in-shot (n=78): median **10.62**, p90 **16.78**. qa_auto PASS.
- Ground measured on rendered frames (`J.ground_share`): 0.15 / 0.14 / 0.09 / 0.11 at g1315 / 1340 / 1360 / 1380 (previously 34-37 % by the QA's reading).
- Bundles: three world-placed `J.prop_reed_bundle` (60 stalks each) at (-25.2, 14.2), (-27.6, 12.8), (-24.0, 12.0) plus three `prop_pot` (jar / pot / bowl) so one prop is in the lower band through the whole camera path (see the phone sheet: a bundle or pot at the bottom in every tile). Each bundle has a contact-shadow quad and a warm point light (260 W) near the first.
- The flat `mygap` plane is removed; ground is the set's `J.gapfill` + v2 dressing.
- The tie (old man, `reed_tail_l` on ox 4's tail tip) is unchanged; he looks toward the lens, not the tail (the pose has no gaze key I set), and he leaves the frame around g1370-1380 when the camera sway swings away.
