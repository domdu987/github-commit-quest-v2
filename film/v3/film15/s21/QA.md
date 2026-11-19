# QA s21 (film 15, shots 21-23: attempt 1, attempt 2, the coach shouts), g 1125-1268 + handles 1119-1124 / 1269-1274
Set B EVE, cast15 cards (shot.py/c15.py in ../s17), 12 samples, 720x1280, no DOF.
- motion_check (cuts 1150,1190): median 7.6, p90 12.6 (target 4 / 12). Per shot: 21 median 9.2, 22 median 11.3, 23 median 5.0.
- qa_auto: one FAIL "suspected blur" on g 1123-1142 (shot 21, the whip pan): frames are crisp renders; the Laplacian test is relative and the frames are dominated by smooth orange track and sky. Checked by eye at full size: sharp. The "no visible change at cut" notes are an artefact of the high median diff (cuts measure 40 and 69 vs median 7.6).
- Mouth: coach moves only g 1213-1271 (narration 40.38-42.25 s +0.10 s clock), flat elsewhere. Bar falls: shot 21 at g 1141, shot 22 at g 1163 (bar_reset at the cut). Heads above y 880 (head_rows in logs).
- Differs from plan: shot 21 camera in front of the bar (4 m) with a whip pan following the run; shot 22 camera standing on the foam end looking back at the bar (not behind the stands), Dick lies on the foam hands on face; shot 23 has 8 cast15 crowd cards around the coach.
