# s04 QA: film 24, shot 4 (yard yard_wide)
Delivered: take.mkv (libx264rgb crf 6, 38.7 MB), first_g 282, 155 frames g 282..436 (6 in-handle, shot g 288..430, 6 out-handle), meta.json, cues.json, contact.jpg, QA_AUTO.md (PASS), phone_sheet.jpg.

| rule | result |
|---|---|
| floating / shadows | all four on the quay z 2.25 with stage contact decal + shadow proxy |
| camera | preset push-in 8 % along its view line (0.35 sine + 0.65 linear); qa_jitter median 0.04 px; no frozen run (qa_auto) |
| movement | nobody walks: Yi and workers planted with slight sway; Yi nods once at g 347 |
| duplicates / size | yi24 + kor_a24 (carry_spikes, mirrored) + kor_b24 (carry_spikes) + kor_c24 (stand_rope, mirrored): four members. Head widths: Yi 61-81, wa 51-64, wb 36-42, wc 26-29 px (near > far) |
| heads above y 880 | max head bottom 821 (Yi) |
| mouths | no quote: fixed |
| tone | comic, bloodless |

Render: R9, 24 samples, 540x960 + post, 40.7 s wall / 78.5 s CPU per frame (two processes x 2 threads).
Deviations: preset state shows the spiked roof (sp3) as in the set's yard_wide; workers are small (the wide framing), Yi is placed at (8.9, 14.5) near the bow so he is the nearest figure.
