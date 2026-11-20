# QA sJ2 (ending splash), g 1709-1848, 140 frames, 720x1280, 32 samples + OIDN
One travelling camera, no cut inside, hard cut on g1848 (no handles). transition_in cut/whip (whip in: g1709-1714, yaw 48 deg decaying).
World: `K.build_world(['riverbank','river_low'], over foam_k 0.5)`; camera = `K.cam_path` through riverbank -> drift -> drop to river_low (g1821) -> push.
- g1709-1772: English look at the bridge, the water, each other; footman_b pinches his nose from g1731.
- Jumps (cards lifted 0.85-1.1 m, parabolic arc over 14 frames): take-offs 1773 / 1777 / 1781 / 1784 / 1788 / 1792; `K.splash()` crown at each entry; swim cards (spluttering, then paddling) and 3 floating helmets.
- Camera drops to water level for the three big crowns: impacts 1813 / 1822 / 1831, so each is at age ~0.27 on the words (g1821 / 1830 / 1839). Last frame g1848 = crown age 0.6.
- Rim: every cast pose goes through `K.with_rim`. Contact decals hidden while airborne / swimming.
## Numbers
- qa_stats2: sat 0.537, vivid 54.2 %, luma 114.6 (over 110: the bright river_low half; QA-art colour exception for river_low: VIVID gamma 1.9, luma up to 150 allowed with sat >= 0.47). Motion med 10.4, p90 27.2.
- rhythm: in-shot median 11.64, p90 31.05 (limits 4 / 12). qa_auto PASS (soft frame g1709 = whip).
## Known weak spots
- The near-bank white foam band is still at the bottom of frame g1815-1832; out of frame by g1839 (not by the second splash).
- A swimmer's face is big at the bottom of frame at g1821-1832 (under 35 % of frame height). Bank-phase swimmers within 2.3 m of the lens are hidden.
- Sky about 25-30 % in the later bank frames. Splash droplets are hexagonal beads (set material).
- English are crimson / blue cards as in the cast sheet. Nobody speaks; open mouths are the flagged jump yells and splutters. Bloodless.
