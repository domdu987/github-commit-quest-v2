# QA sJ2 v3 (director gate fixes: B1 lit wall, B2 soft smoke from set e07ceb1), g 1709-1848, 140 frames, 720x1280, 32 samples + OIDN
One travelling camera (`K.cam_path`), no cut inside, hard cut on g1848, no handles. Cast = new default crimson English.
- Whip-in: 4 frames, lands on the group by g1713 (no empty-ground frame); the first frame already shows the group edge and the water.
- g1713-1772: camera looks toward the bridge neck (the Scots spear wall + saltire banners at the far left, small and backlit) with the group right of centre; three head turns: bridge g1713-1730, water g1731-1746, each other g1747+ (sweat drops); nose pinch from g1756.
- Jumps g1773-1792 (moving 14-frame arcs, lift 0.8-1.1 m), thin crowns (`splash2`: 9 petal sheets + 5 streaks + 12 small drops, no hexagon beads), swimmers splutter, three converge to the cluster, floating helmets.
- g1800-1847: camera drops to water level and stays 2.9 m from the swimmers (it does not pass them); three separate crowns beside them at 1821 / 1830 / 1839 (impact 8 frames earlier, age ~0.27). Last frame g1847/1848: three spluttering heads in medium size with a crown beside them.
## Numbers
qa_stats2: sat 0.549, vivid 56.0 %, luma 98.3; motion med 7.7, p90 21.8. rhythm: in-shot median 8.98, p90 25.2. qa_auto PASS.
## Known weak spots
- The bridge/wall is small and backlit in g1713-1760 (dark band at the far left): the south-east view faces the sun.
- A crown very close to the lens at about g1800 covers the left quarter for a few frames.
- The bare bank is about 35-40 % of the frame in the last 45 frames. Faces are large (about 20-25 % of frame height).
- Colour levels are left to the conform (director policy).

## v3 changes (gate B1/B2 + notes)
- B1: the Scots wall's saltire banners are lit by a local warm point light and doubled in size (4.2 x 2.9 m on 9 m poles); the dark trees near the wall (meadow_trees, farms_leaf/bark) are hidden; the camera yaws 27 deg toward the bridge neck. The big saltire flag and the lit wall read at the left of g1713-1745; later the move follows the group so the wall leaves the frame.
- B2: set3d21 / cast21 re-pulled from film21/main (soft smoke puffs); the grey crescent slabs are gone.
- Near-lens crown shards are culled (no crown within 3.0 m / 2.2 m of the camera); the left swimmer is re-centred (offsets computed along the end-camera axis).

## v4 (gate B3, g1788-1848 re-rendered)
- The end camera now floats just over open water 3 m beside the swimmers (no sand between lens and swimmers; sand is out of frame), looking slightly up; three swimmers (all heads fully inside the frame) with floating helmets in the lower-middle third at medium size; swimmer heads are turned (yaw) toward the bridge side.
- The "ตูม" crowns are scaled 1.5x and stand beside the heads: crowns at 1813 / 1822 / 1836 impact, so the third peaks at about g1846-1847 (last frame g1848) while the first two stay on the 1821 / 1830 cues.
- Tall near-lens shards are culled (jump crowns within 4.8 m of the lens are not drawn from g1790); smoke columns are hidden.
- Weak: g1795-1805 is a camera transit shot (sky and water, swimmers re-enter at about g1812); sky is about 40 % at the end; the lower 30 % is flat teal water.
