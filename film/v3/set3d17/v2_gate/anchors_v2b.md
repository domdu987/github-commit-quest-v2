# film 17 v2 re-gate (v2b): per-frame anchor / camera table

Every frame of every take (render ranges with handles), `prefecture17.check_take`: anchors in frame above 75 %H outside the planned OTS shoulders
and P1-P3 (`PLANNED_CLOSE`), anchors whose body centre comes within 1.0 m of the lens, camera speed above 6 m/s (BIGZOOM ranges excluded).

| take | frames | max anchor %H (unplanned, in frame) | hits > 75 %H | lens pass < 1 m | frames > 6 m/s (peak) | planned close (OTS / P1-P3) |
|---|---|---|---|---|---|---|
| T1 | 0-342 | 56 % (bertillon g100) | 0 | 0 | 112 (14.8 m/s, g152-277) | - |
| T2 | 330-657 | 73 % (thief g382) | 0 | gend_corr g403-451 (0.98) | 0 | bertillon g555-625 |
| T3 | 645-856 | 72 % (prisoner_chair g823) | 0 | 0 | 0 | - |
| T4 | 844-1051 | 73 % (clerk g979) | 0 | 0 | 4 (6.1 m/s, g1035-1038) | - |
| T5 | 1039-1383 | 61 % (gend_a g1274) | 0 | 0 | 10 (6.1 m/s, g1141-1150) | bertillon g1100-1150 |
| T6 | 1371-1701 | 72 % (bertillon g1551) | 0 | 0 | 0 | bertillon g1516-1545; dupont g1516-1545; dupont g1546-1616; inspector g1672-1701 |
| T7 | 1689-1874 | 47 % (bertillon g1730) | 0 | 0 | 68 (15.5 m/s, g1800-1867) | - |
| T8 | 1862-2052 | 60 % (bertillon g2017) | 0 | 0 | 0 | gend_a g1958-2052; bertillon g2018-2052; inspector g2018-2052 |

Frames above 6 m/s are the planned crane / swoop moves only: T1 1c pull-out + crane-up (g152-216) and 1d swoop (g227-278), T7 7b crane-up to the top-down (g1800-1867), all <= 15.5 m/s, plus T4 g1035-1038 / T5 g1141-1150 at 6.1 m/s. Render those ranges with motion blur (shutter 0.5).

`report T1 T6`: BIGZOOM 1 start 1.6 %H -> end 36.4 %H PASS; BIGZOOM 2 start 4.4 %H -> end 48.0 %H PASS.

SERVICE D'IDENTIFICATION, whole sign inside the frame (cap height in px on the 360 x 640 phone sheet):
- corridor side, short form IDENTIFICATION (2.9 x 0.6 m, cap 0.37 m), T2 g445-493: whole in 14 of 49 frames (g445-458), cap 81-106 px (it leaves through the top edge as the camera pushes under it into the door).
- room side (3.9 x 0.5 m), T3 g725-760: whole in 25 of 36 frames (g736-760), cap 17-27 px.
