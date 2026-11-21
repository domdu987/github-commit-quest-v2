# sE2 "the COUNT" g885-1044 v2 (cut in, no handles) - team 6
take.mkv is split in parts <= 40 MB: `cat take.mkv.part* > take.mkv`. 160 frames, 32 samples, libx264rgb crf 6.
Built on film21/main set3d21 + cast21 (colour story: English crimson, Scots blue; valley_loop VIVID).

Gate fixes (QA_TECH sE2 5830dbc):
1. Scots from g885: the hill is in the upper left of every frame; 10 idle Scots cards (fold-spear, chew-grass, scratch-nose, stand-still; mouths closed; oversized x8 for the distance) and 3 giant blue saltire banners on bare terrain.
2. Count steps on the words: 10 men at g885; a dense block of ~100 at g938 (bridge queue + the fan past the mouth, revealed as the camera rises and pans); crane starts g975; 280 real crimson footman cards pop in around g985 (scale pop, 979-991). No pins.
3. No soft streak: the crane never aims at bare ground; the crowd is in frame throughout.
Should-fix: opening camera is close and low (men ~15 % of frame height, lower-middle) with gorse, boulders, barrels and spears; footmen (1 in 3) glance toward the hill; the crowd block is kept off the left edge at the crane top.

Ground (QA §K): GROUND.md PASS (0 FAIL, 390 cards, frames every 10). The men step down at the bridge mouth (deck top 1.75 -> terrain 1.2 at y 38.25), no hover; every card has contact=True shadows. SUNK warnings are heather/rock within ~0.4 m of a Scots foot point.

Numbers (informational; normalized at the conform): qa_stats2 sat 0.473, vivid 49.5 %, luma 100.0. Rhythm median 6.62, p90 11.08 (p90 just under 12). qa_auto PASS.
Known: Scots figures are tiny white-faced cards at 260 m (oversized); the meadow at the crane top is a regular grid of cards (staggered rows, sway).
