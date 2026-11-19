# s03 QA: film 16, shot 3 (3.66-5.59 s) -- LINE line_rail, DAY
- Delivered: take.mkv g 101..176 (76 frames; shot = g 110..167, 9 handle frames each side), 720x1280, 7 spp, libx264rgb crf 6. meta.json, cues.json, contact.jpg, phone_sheet.jpg, QA_AUTO.md (PASS), framediff.json.
- Shot: Morse (cast16 morse_tap_wire_grin, grin, sway + tapping finger) stands on the field side of pole 3; the 1840s train (loco + 2 carriages) rolls past behind the pole line toward -x; camera from the field side tracks left (slide 70 px/s), slow push, eased snap x1.7 on "รถไฟ" (event g 160, snap g 157..170), still moving on the last frame.
- Checked at 6 fps: no head above the caption band (head bottom max see meta.json, below y 880); no mouth movement (expression grin only, no speech); contact shadow decal under his boots; the pole 3 ladder is hidden at runtime; the preset's parked pulse is hidden.
- Frame-diff (90x160 grey, in-shot): median 5.39, p90 13.02 (target 4 / 12).
- Differences from the plan: Morse "taps the wire" is a pointing/tapping gesture toward the train (the wire is 9 D up, out of reach); the train is IN FRONT of the poles' depth line from the field-side camera's point of view the poles are nearer the lens, so the train runs "behind the poles" as planned. The set's steam puffs read as a chain of white balls (set design); the smoke speed hook is set low (3.5).
- No streak was added (no frame exceeds ~60 px/frame corner speed outside the snap).

- TAKE-gate follow-up (re-render): Morse's eyes now look to screen right at the train (pose keys gaze (1.0, 0.1) + yaw 0.55), instead of at the camera. Frame-diff in-shot median 5.40, p90 13.02; QA_AUTO PASS. The wire is still not in frame (the tap is a gesture at the train).
