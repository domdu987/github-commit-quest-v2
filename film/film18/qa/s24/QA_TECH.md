# QA-tech round 11 s24: FAIL
Checked: 20 frames (6 fps g1807-1882 + cut +-3: g1804/1806/1807/1810/1812, last g1879/1882), phone strips with y 860/880 lines. Director 10.07/15.59: OK (median >= 4, p90 >= 9), one continuous push, no pulsing. NIGHT, no text, mouths held. No head/chin/mouth below y 860 (lowest soldier chin about y 815-846 at g1857-1877): MET. Previous blockers: heads below 880 FIXED.

## Blocking
1. g1837-1882 - untextured grey/navy placeholder props. The flying "pots/helmets" are large flat grey-navy domes with rivets and navy bells (g1862-1872 at x 140-420, y 700-900; g1877 a grey-navy bell about 36 % of frame width, x ~210-330 of 330 on the phone strip, y 820-1000; g1882 another at the bottom-right, x 560-720, y 1060-1250). The tipped chariot is a flat dark grey-navy planked box with spoked wheels (g1847-1882, x 40-480, y 880-1180) with no wood or bronze texture. They read as grey placeholder lumps, not terracotta pots. Fix: give prop_pot a terracotta/bronze lit material and prop_helmet bronze with a plume, cap their scale at 1.0x (about 8 % frame width) and keep them out of the lower third; give the chariot a warm timber texture and a rim light from the fire pit.
2. g1807-1830 - bare ground. Below the horizon of the camp (y > 0.70) about 33-36 % of the frame is plain blue-violet pebbled ground with only the fire pit and two tiny stumps (measured on g1807, 1817, 1827). Over 30 %. Fix: tilt the camera up 3-4 degrees (horizon to y ~0.62) or lay two or three dark lit props (dropped shields, a tent, sacks) in the lower corners from g1807, and slide them with the push.
3. g1830-1882 - the rout does not read. Soldiers (about 150 px tall) still stand and huddle in the same place around x 0.45-0.9, and the tents at the left/right edges remain standing or are white flat slabs, so "tents fold, soldiers flee in all directions" is only carried by the big flying grey pieces. Fix: 4-5 soldiers must visibly run across the frame in different directions (x move >= 150 px over 20 frames) and at least one tent must collapse in view.

## Notes
- Fire pit flame (g1807-1882) is the scene's own fire (a prop, not an ox tail); no flame near a face. Fine.
- Faces read as panic; torches give warm practicals; night mood good.
- Bottom-right strip of bright white cloth (g1827-1857, x 580-720, y 820-1000) reads as a flat folded sheet; add cloth texture.
