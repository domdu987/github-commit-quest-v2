# QA-tech sE2 (film-13 QA, team6 1f68f93)
Checked: all 160 frames (frame diff, no spikes, no frozen run), every 5th frame at 360x640; qa_auto PASS.

**Verdict: FAIL**

## Old fails
1. Scots visible from the start: FIXED. Hill upper left with blue saltires and white-faced cards from g885. They are small and the hill is in shade, but they read.
2. Count grows on the words: FIXED. About 11 men at g885-915, a dense block of about 60-100 from g935-940 (bridge queue and fan), the meadow fills g979-1000.
3. Empty-dirt framing: NOT FIXED for g885-935 (and partly g1005-1044).

## Issues
1. g885-935, BLOCKING: the lower 45-50 % of the frame is bare dirt with a rock and bushes; the men sit in a thin band at y 560-720, and a barrel and bush cover the left edge. This is the old "empty dirt" fail. Fix: pitch the camera down or push it in so the men fill the middle third, and cut the foreground dirt to 20 % or less.
2. g1005-1044, non-blocking: the meadow is a regular grid of tiny cards with dark ellipse shadows; about a third of the heads are below y 880 (g1000-1044), where captions sit. They are background crowd, not cast. Fix if cheap: crop or tilt so the crowd heads stay above y 880.
3. g885-960, non-blocking: the hill and the Scots' saltires are dark navy on a dark slope, with little contrast. Add a rim or warm light on the hill so they read at phone size.
4. g979-991, non-blocking: the 280 cards pop in by scale (no frame-diff spike, but the meadow is sparse at g985 and full at g995). Acceptable.
5. Footmen walk away from the camera with arm swing, no floating feet seen. Mouths closed.

## Director ruling (film-13 workflow, 2026-11-21)
ACCEPTED. At full size, g900 shows the near ground dressed with a barrel, gorse and rocks, and the soldiers at about 15 % of the frame height; the bare-dirt item is not blocking under film-13 QA. The crowd heads below y 880 are background extras, not main characters.
