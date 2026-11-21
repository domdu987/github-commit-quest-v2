# ear_v2 (film 17 v2 remake): final checks, 2026-11-21

Workflow: film/skill_film13 (client decision 2026-11-21), free automatic scripts only.

| Check | Result |
|---|---|
| qa_auto (2052 frames, cuts 336, 651, 850, 1045, 1377, 1675, 1695, 1868) | PASS. No black, blank, magenta or frozen frames. Its "no visible change" note on the cuts is wrong: the frame diff at every planned cut is 38-71/255, against 1-23 just before it. The soft frames g0-2 and g27-38 are motion streak on the roof dive. |
| qa_jitter | Overall median 0.46 px. Seconds above 2 px: 2 s (3.0), 5 s (3.4), 27 s (3.2), 33 s (2.7), 51 s (2.8). The seconds checked by eye (window swoop, T3b whip, T4 travel through the door, P1 push) are planned fast camera moves; 2 s is the planned roof dive. Film 17 has no shake code. |
| Loudness | -12.2 LUFS integrated, true peak -1.5 dBTP, LRA 1.9 LU |
| Luma (RGB mean at 90x160) | Film mean 102.7 after the conform trim |
| Format | 68.4 s, 720x1280, 30 fps |
| Ground check | ground_check.py was run on T1a, T6b and T8, with 0 cast-card FAILs. T1a lists the street props wagon_horse and wagon_leather as FAIL by bounding box; neither was seen in the T1a frames checked. It was not run on the 8 parts accepted earlier (T2a, T2b, T3b, T5b, T5b2, T6a, T6a2, T7). |
| 1 fps sheets | ear_v2_sheet1.jpg and ear_v2_sheet2.jpg, viewed by the director |

## Fixes in this version
These are on top of the accepted v2 takes.
- **T1a g172-190:** re-rendered with the street cast, so the gendarmes by the lamp no longer pop in at g191.
- **T3 g651-723 and T8 g1862-1925 (top-down shots):** the cards yaw to the lens and lean back up to 35 deg at the feet, so people no longer lie sideways on the floor. In the T3 frames the light-shaft volume is hidden.
- **T4 g1004-1009:** the stray head at the bottom edge is removed.
- **T6b g1644-1674:** the gendarme's hand grips the bottle.

## Known and accepted
- **T1b:** keeps the puddles. The dark shapes on the cobbles are reflections of the wagon and of a prisoner.
- **T5a:** the archive gasolier hangs on its iron pipe, but the pipe is thin and hard to see.
