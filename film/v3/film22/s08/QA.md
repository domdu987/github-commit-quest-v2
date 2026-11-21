# s08 QA (render team 3) — g 938-1004 (+8 handles: 930-1013), 720x1280, 13 samples + denoise
- qa_stats2: sat 0.586, vivid 67 %, luma 91.5 (>= 85; lamps raised 20 %); frame-diff median 4.46, p90 5.90 (p90 below the 12 target: the move is a slow side track with a walking Beck, not a fast one). qa_auto PASS, magenta 0 %.
- Side tracking at eye-low height (cam z 3.45) with a slow push (lens 24 -> 30); camera starts at x 4.8 so the fg notice easel does not blank the frame; it ends before the x 13 easel. PUBLICITY door sign readable and not mirrored; Beck walks with cast22 walk_carry_roll (roll under arm, chin up), knocks at 32.29 s (g 972) with the fist alternating, the hand in the door gap reaches in from g ~988 and takes the roll at 33.16 s (g 998), roll leaves Beck's arm. Contact shadow under Beck.
- Deviations: the hand/sleeve is small and partly in shade. Bare floor / wall split not measured (floor about 20 %). Shade hue not measured. Dissolve 11 into s09: 8 handle frames rendered after g 1005.

## Rule checks after the take was rendered
- qa_jitter: overall median 0.32 px, no second above 2.0 px (the slow roll sway that all three first renders had stays in this take: it is below the threshold; re-render only if the director wants it gone).
- hue_report: see below (corridor is bluer than the publicity office).
- GROUND.md PASS (door plaques mounted; Beck has the cast shadow).
s08 take                                        2.3    4.3    3.0    3.0    1.9   36.5   34.1   15.0  0.58 0.52 0.01   OUT: red,orange,blue,violet,magenta,sat,dark
