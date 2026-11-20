# QA s21 (shot 21, g1431..1559, handles 1427-1430 / 1560-1563)
- qa_auto: no FAIL (see QA_AUTO.md). Notes: 'cuts with no visible change' = cut handles are 3-D continuations of the take, expected; soft frames g1427-1432 = near-empty night sky at the summit start (content-low, not blur).
- s/frame 7.55 wall / 14.44 cpu (2 procs x 2 threads, 720x1280, 8 spp). Frame-diff in shot: median 9.34, p90 12.32 (target 4 / 12) PASS.
- Checked at 6 fps + cut +-3: whip from the summit lamp reads, tower is the full Eiffel silhouette with 4 wires, rings (5 arcs always visible) spread over Paris, lattice glow rises on g1530 'เสาอากาศยักษ์'. No text, no DOF, no cast, nobody frozen.
## Gotchas / deviations
- set signal_rings() only emits during half of its cycle (sky empty ~15 f, reads soft to qa_auto): shot.py drives the 6 ring objects itself (ring born every 6 f, radius 30->560 m, halo hidden while age < 0.1). Set module untouched.
- Summit start uses a closer camera (40 m from the lamp, 268 m up) than preset tower_night_summit (80 m): the preset frame is a lone mast over an empty sea (QA-art R6). The whip is already under way when the cut lands (g1431): zero full-hold frames on screen.
- Pull-out/drift is a 5 %/s PULL along the ground (a pull toward a high subject sinks the lens underground), snap x1.22 push on the word; plan said 'drift 6 %'.
- Lamp-post FG from the preset is visible at the left edge in the whip end frames.
