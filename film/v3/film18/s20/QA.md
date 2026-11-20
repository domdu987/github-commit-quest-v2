# QA s20 (render team 5, film 18) round 5 - frames g1515-1595 (+6 handles: take.mkv g1509-1601, 93 frames), jimo_out NIGHT
Frame-diff in-shot (n=80): median **4.89**, p90 **6.58**. qa_auto PASS.
- Came in about 25 % (lateral 8.8 -> 6.7 D, slow push 0.9 D): the lead ox is about 40 % of frame height, nose in frame, flame trailing level behind with sparks; flames still attached, none on a head.
- Navy spikes (`tufts`), furrows, the white rock and foreground stones/props hidden; the road posts and the far-camp fires hidden.
- Not fixed: a tripod torch stand still shows behind the lead ox around g1522-1540 and g1569-1590 (it is a set brazier I could not identify among the set's objects, so it is not hidden); sky is about 30 % and plain ground about 35 % (the set's `dress_ground` is not yet available).

## Round 6: ground dressing
Re-rendered with `J.dress_ground` (density 0.45, keep-clear on the herd lanes). `J.ground_share` at g1525 / 1550 / 1575 / 1590 = 0.27 / 0.38 / 0.25 / 0.25 (was 0.35-0.42). Frame-diff median 6.48, p90 9.39. qa_auto PASS. The tripod torch stand behind the lead ox is still present (set brazier, unidentified).
