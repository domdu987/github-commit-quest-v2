# s19 QA, round 2 (film 12, shots 19-21, g 1340-1578, take g 1334-1584, 251 frames, 26 samples)
Director gate (round 1) fixes:
1. Shot 21: ~105 cast12 men, each under his own adult-scale 3D umbrella (canopy radius 1.1-1.3 head units), colours green / ochre / oxblood / brown / blue / dark / grey; the set's oversized umbrellas are hidden (nothing over the coachman). Crane pulled back/higher so every head stays above y 880 (max head y 835 over all frames, checked from the per-frame json). Hanway (amber rim, smile walk) stands inside the crowd. The crowd drifts slowly with bob and sway, so the last 3.6 s are never still.
2. Continuity at g 1470: same crowd, same sprite gentlemen (open from shot 20), umbrellas ~45 % open at the cut, ramp continues until the street is full (~g 1522).
3. Shot 19: gentleman looks toward Hanway (not the lens) and opens his umbrella from g 1368 with arm, angle and umb_open blended from the furled pose to the open pose over 14 frames (handle always in the hand, no teleport). Closer camera, less empty cobble, no card at the right edge.
4. Shot 20: gentlemen 2-4 open at g 1418 / 1436 / 1452 in the mid-ground and foreground at large size, plus the 3D crowd popping (k 0 -> 0.45); camera moved off the lamp post, red wheel smaller, nothing clipped at the right edge in the checked frames.
5. Mouths: opening gentlemen use mouth flat / neutral expression until open, smile after; crowd uses 'unimpressed' with a flat mouth. No quote in this take. Minor: 26 samples instead of 20.
- qa_auto PASS. Its note 'no visible change at cuts 1410 / 1470' is a false positive (the cuts change camera, set and cast; earlier measured mean abs diff 48 / 64 vs ~18 between rain-only neighbours).
- Light RAIN throughout, magenta 0.0 %, no DOF, no text.
- Not done: contact shadows were not changed; the lower third of shot 21 is still open cobble (cards whose head would fall below y 860 are culled); crowd cards are walk-in-place with bob and drift, not leg cycles.
- Cost: 45.5 s/frame average (2 threads, 26 samples, two processes).
