# QA-tech round 12 s24: FAIL

Checked: all 87 frames extracted; g1807-1882 at 5-frame steps with the y 860 line; band crops (y 560-960) every 4 frames; full-size looks at g1812, g1817, g1857, g1875; chin crops g1860/1867/1875. Pixel measures on the rendered frames.

## Blockers
1. g1837-1882 - prop scale. The tipped chariot (J.prop_chariot) spans x ~40-500 at g1857-1875 (about 60 % of the frame width including the pole; the box alone ~28 %) and sits in the lower third over the fire pit. The flying pots/helmets are far above 20 %: g1857 a pot x 495-690 (27 %), g1871-1875 pots/helmets ~30 % of the width (x ~450-600 and a second at x 560-720). Fix: prop_pot and prop_helmet scale to <= 0.5 of the present size (each <= 20 % of the frame, ~140 px), the chariot at <= 0.4 and the pole shortened or hidden, keep them out of the lower third.
2. g1830-1882 - the rout does not read. About 5-6 soldiers (150 px tall) stay in the centre-left cluster x 0.05-0.65, y 0.45-0.70; nobody crosses the frame and the right half is empty of soldiers. Only ONE soldier visibly falls/sits (g1851-1879, x 0.10-0.25, y ~0.62-0.68); I find no second fall. Fix: at least 4 soldiers running in different directions (left, right, toward and away from the lens, x travel >= 150 px over 20 frames) and at least 2 visibly falling (tumble/sprawl, not just sitting) in g1830-1880; fill the empty right side.

## Previous blockers
- Terracotta and bronze: PARTLY. The chariot is now warm timber (OK) and the pots are warm, but pots and helmets are a flat lemon-yellow glowing fill with a soft translucent look, no texture, no clay red/brown (g1863-1875). Reads as gold/bronze-ish, not grey/navy, so not a placeholder blocker; it is a note (darken to a bronze/terracotta hue and add a texture/outline). Size is blocker 1.
- Plain ground at g1807-1827: dark violet plain ground measured 24-25 % (g1807 24.8 %, g1812 24.2 %, g1817 24.7 %, g1822 24.3 %, g1827 21 %); including the warm lit pool round the fire pit the ground is ~30-32 % (the whole y > 0.68 band is ground except the pit and two stumps). Within the gate as measured, borderline; a note. A dark fg prop low-left (a dropped shield, sacks) would clear it.
- Chins: all faces <= ~y 860. Sitting soldier chin ~855 at g1860, ~852 at g1867, ~858 at g1875 (crops with the y 860 line); standing soldiers' chins y 700-840. Borderline at the sitting soldier; a note: lift him 10-15 px.

## Hard checks
- Placeholders: none grey/navy (pots, helmets, chariot warm). Left white tent slab at g1827-1882 (x 0-250, y 700-900) and right white/grey cloth slab (x 580-720, y 820-1000) are flat pale planes; add cloth texture (note).
- Flames: only the fire pit's flame (a set prop, no tails in this shot); never near a face. OK.
- Subject in frame: soldiers stay in frame. No zoom pulsing (continuous push). Mouths held. No text.
- Frame diff (my re-measure, 90x160): median 9.99, p90 15.00. OK.
