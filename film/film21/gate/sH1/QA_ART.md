# QA-art sH1 (TAKE gate, v2)
Take: gate/sH1/film/v3/film21/sH1/take.mkv (g1239-1348). Viewed: every 5th frame at full size, every frame g1309-1326, crops of the bridge mouth at g1334/g1344, the team's contact and phone sheets. Compared with R5, R7 (ride and swoop) and R3. Colour level, saturation and the lemon sand (g1279-1310) are left to the conform. Rim light is ruled on at FINAL.

## Verdict: FIX-FIRST

The ride-along is still the best opening of a beat in the film: running Scots, gorse whipping past, sun shafts. It is the R7 ride feel. The overtake and swoop down the river are clean §I travel. Most of the v1 items are fixed: the Scots now wear saltire-blue tunics, three blue saltire banners rise in the wall, and the helmet pop is a real gag (g1316-1326: helmets fly, the English hop with O-mouths and sweat drops). The crimson-against-blue story finally reads.

One blocking problem is left. The end of the take does not show a corked bridge, and it does not match the H2a frame it dissolves into.

## Old items (v1)
| v1 item | status |
|---|---|
| 1 blue wall + banners | FIXED (tunics blue; banners present but too dark, see N1) |
| 2 wall closer at the slam | PARTLY: the wall is about 10 % of the frame height at g1316, but it sits behind the bridge rail and the English (N2) |
| 3 slam as an event | FIXED: the flank runs in g1310-1316, then the hop and helmets |
| 4 English react, helmets pop | FIXED, funny |

## Issues

**B1 (blocking), g1326-1348: the cork is open, and the end does not match H2a.** In this take the bridge deck still runs past the Scots line into the foreground, and crimson English stand ON it at the mouth (g1334, g1344). The blue Scots are a 2-rank strip behind the English along the waterline. With the sound off it reads as "English in front of some Scots by a bridge", not as "the bridge mouth is plugged". The H2a take was re-rendered on the fixed set: the deck is shortened (K.BRIDGE_Y1 = 31.1) and ends at the wall, the wall is 5 ranks deep, the banners are large, and the smoke uses the soft puffs. That means the D6 at P_NECK (g1345-1348) will blend two different bridges and two different walls.
Fix: re-render H1 on the same set state as the H2a redo (set3d21 e07ceb1 + cast21 528bf9d, the short deck, the 5-rank wall), so that from g1316 the wall stands ACROSS the end of the deck and no English stand on the deck on the land side of the wall. Check the P_NECK frame g1345 against H2a g1345 side by side before submitting.

**N1 (non-blocking), g1312-1348: the saltire banners read near-black.** The banners are backlit by the low sun, so they come out as navy rectangles with a faint violet X. On a phone they read as "dark flags", not as a saltire. Fix: give the banner cloth some translucency or emission (about 0.3) or a second-side light, so the blue is a mid saltire blue with a clearly WHITE cross, like the P_TOP banners in H2a.

**N2 (non-blocking), g1312-1326: the slam is partly hidden, and the lower half is empty.** The bridge rail runs in front of the running Scots, and the bottom 45 % of the frame is bare dirt with a few grass tufts. Fix: lower the camera about 1 m and tilt up slightly, or raise the aim point, so the wall clears the rail and the dirt drops to about 25 % of the frame. Optionally add a foreground prop at the bottom edge for depth: a dropped helmet, a spear, a gorse bush.

**N3 (non-blocking), g1318-1330: the tan dust puffs read as beige sacks or sheep** behind the English. Make them smaller, more transparent and faster to fade (8-10 frames).

**N4 (non-blocking), g1309, g1329-1348: the old crescent smoke "blades".** Grey-beige sickle shapes show above the camp and beside the flags. The B1 re-render on the current set (soft puffs) clears this.

## Scores
phone legibility 6 (ride 8, end 5) / set density 7 / light (sun shafts, low warm sun, violet shadows) 8 / colour story 7 / acting and comedy 8 / same channel? yes for the ride and swoop / camera travel 8.
§G pass: feet and contact shadows OK, nobody sliced, no face over 35 %. Bloodless: helmets on the ground only, nobody down.
