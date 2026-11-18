# s19 QA (film 12, shots 19-21, g 1340-1578, take g 1334-1584, 251 frames)
- qa_auto: PASS (see QA_AUTO.md). Its note 'no visible change at cuts 1410/1470' is a false positive: measured mean abs diff 48 / 64 across the cuts vs ~18 between rain-only neighbours.
- Heads: every card head projects above y 880 (max head y 795 over all frames; wides exempt from the 0.35-0.59 H rule, gentleman/Hanway at y 690-760 = 0.54-0.59 H).
- Mouths: all still (no quote in this take); blink only.
- Light RAIN throughout, shade blue-violet, magenta 0.0 %. No DOF, no text. Camera moves continuously (0.35 sine + 0.65 linear), cards sway so nothing is static.
- Acting: shot 19 gentleman (furled umbrella, staring) opens it at g 1368 (cue 45.5 s) as Hanway passes; shot 20 three more sprite gentlemen open at g 1418/1436/1452 plus 3D crowd umbrellas popping by set_crowd_umbrellas (k 0->0.45); shot 21 crane, k 0.45->1.0 by g ~1522, Hanway smiling, coach rank full.
- Deviations: shots 19 and 20 use closer custom camera moves (s19_wide, s20_rev) instead of the presets; crowd cards at the umbrella slots are men only (a, c, d) standing, 3D umbrellas from the set; take ends at g 1584 (shot 21 last frame 1578 + 6 handles). 3D umbrellas of slots outside the shot's culled range are hidden.
- Known weak: crowd cards are static (sway only); the 3D umbrellas read dark at street_high distance; red coach wheel large at left of shot 20.
- Cost: 35.9 s/frame (2 threads, 20 samples, two processes).
