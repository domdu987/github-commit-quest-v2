# T3 QA (g 862-1058, file g 856-1064)
Segments: A HERO 856-914 (newspaper-photo push-in 856-877, golden training, Dick flops 873-909), season dissolve 904-914 (11 f, HERO->HERODAY), D HERODAY 904-936 (day training, MEXICO 68 poster rise 918-936), poster->BIGZOOM 2 match dissolve 927-933, B NIGHT 926-1064.
BIGZOOM 2: g 930-1059 (31.0-35.3 s). Bar rises 2.04->2.24 m g972-992 (32.5 s); rival straddles, bar falls g1014 (33.8 s), rival lies on mat then walks off.
Angles: push into newspaper (856-877); low side tracking (873-914); poster crane-up (918-933); bird's-eye/high crane + dive through beams and crowd (930-1040); medium low front (1040-1064). No close-ups.
Numbers (qa_stats2): sat 0.610, vivid 64.4 %, luma 99.5, magenta 0.1 %; motion median 12.8, p90 22.0.
qa_auto: FAIL flags blank/blur on the newspaper halftone frames 857-865, 875-878 and the dissolve frames 902-908 (soft by design: halftone page, cross-dissolves). No other flags.
Render: B ~26 s/frame (2 parallel procs), A/D ~20 s/frame.
Known: team-2 newspaper seam is only approximate (my page framing is my own newspaper() crop); Dick in A training is a card tween without leg detail at the landing; sun-side rim kept simple.

## Re-render v2 (director TAKE-gate fixes)
- Magenta frames were a texture race (two processes regenerating newspaper.png): texture now cached, not regenerated. Scan of all 209 frames for magenta: none.
- g856-868 start on team 2's exact page framing (0.74 m page, d 0.5 m at g862, headline in frame), dolly 0.0125 m/frame; T2 grade applied to plates (A live gain 1.0 sat 1.10 shade 0.35; page gain 0.95 sat 1.30).
- Season dissolve g904-914: Dick (landing / sit-up) is in both plates; falling autumn leaves g893-925.
- Take-off moved to the standard side (x 2.3) so the bar no longer crosses his torso; flop path starts x +1.3.
- BIGZOOM 2 re-timed: medium-wide of the fan (about 8-12 m) by g~990-1000, then a slow push; end camera ~10 % closer; bar 1.80 -> 2.24 m g968-992, rival fails g1014; bloom 0.5 -> 0.28 (0.12 in g994-1030).
- Numbers: sat 0.649, vivid 74.9 %, luma 97.6, motion median 9.6 / p90 20.7. qa_auto: only 'blur' on 14 dissolve/page frames (g876-888, 919-922), no blank/magenta.
- Weak spot: the A training camera is now wider, so Dick is small (~15 % height) there.
