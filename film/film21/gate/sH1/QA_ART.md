# QA-art sH1 v3 (TAKE gate, team9 04f3393)
Take: gate/sH1/film/v3/film21/sH1/take.mkv (g1239-1348, 110 frames). Viewed: every 5th frame (f6), every frame g1309-1348 at full size, crops of the slam (g1316/1317/1320) and of the caption band (g1334/g1345), the team's QA.md, contact and phone sheets. D6 check: H2a v3 take frames 0-9 (g1342-1351) against H1 g1342-1348, side by side, plus a simulation of the conform blend (conform_full.py: smoothstep mix on g1342-1347, p = 0.06 / 0.20 / 0.39 / 0.61 / 0.80 / 0.94). Camera code read: h1.py camera() and sH2a shot.py KEYS. Colour level, saturation and yellow are left to the conform. Rim light is the film-wide open item.

## Verdict: FIX-FIRST

The set side of B1 is fixed: the deck now ends at the wall, nobody crimson stands on the deck on the land side, the wall is 5 ranks, and the P_NECK frame (g1345) matches H2a almost pixel for pixel (mean RGB diff 1.9/1.6/1.4). The ride (g1239-1275) and the swoop are still the best travel in the film, and the English reaction (turn, jump back, O-mouths, sweat drops, shuffle home) keeps them acting to the last frame.

Two new blocking problems stop it. (1) The 3 handle frames on each side of the D6 do not follow the same camera path, so the dissolve double-exposes two different moves. (2) From g1317 the slam is buried behind rows of faceless navy slabs that rise out of the ground like gravestones, so the payoff "the Scots seize the bridgehead" reads on a phone as "blue boxes popped up".

## B1 (v2): FIXED (set). The D6 match is NOT fixed: see B2.
| check at g1345 | H1 v3 vs H2a |
|---|---|
| camera pose | identical (P_NECK) |
| deck ends at the wall | yes, both |
| 5-rank blue wall | yes, same layout |
| banners | same big saltire banner, top left (still navy, N1) |
| 12 causeway English | same positions and poses |
| fg props, smoke | same |

## Issues

**B2 (blocking), g1342-1348: the D6 handles are two different moves.** The plan (handles rule) says the 3 extra frames on each side must continue the SAME camera path. They do not:
- H1 arrives at P_NECK with zero velocity, easing BACK from the low slam waypoint (9, 47, 3.3), and its handles g1346-1348 rise only about 0.13 m (h1.py: `loc = NECK_LOC + (0, 0, 0.011k² + 0.012k)`).
- H2a comes IN from (-2.3, 53, 5.6) at g1342 (wider, with the gorse and the green bush at the bottom edge) and leaves P_NECK at speed toward (-34, 36, 30) at g1356. By g1347-1348 it is already high over the bridge.
- In the blend (frame diff vs g1345: 35 at g1342-1344, 50-72 at g1346-1348), g1344 shows doubled English and a doubled cloud, and g1346 shows big ghost English fading out over the bridge view at 80 % H2a. The gorse and bush in H2a's g1342-1344 fade in and out.
Fix (H1 only, H2a stays as passed): for g1342-1348 use H2a's camera exactly (copy its KEYS and `K.cam_path(None, KEYS, g)` for g >= 1342, lens 22). Re-aim H1's Hermite so that it lands on H2a's 1342 key (-2.3, 53.0, 5.6) -> (0, 22, 1.9) with H2a's velocity there, not on P_NECK with zero velocity. In practice: the slam waypoint's ease-out should go back and UP behind P_NECK, then come in. Check: frame diff H1 vs H2a under about 3 on every frame g1342-1348, not just g1345.

**B3 (blocking), g1317-1330 (and the wall to g1348): the slam is buried behind faceless slabs.** At g1316 the blue card Scots slam with faces and level spears, as asked. One frame later (g1317) the "3D body" ranks rise out of the ground ON THE CAMERA SIDE as flat navy slabs with grey ball heads. At g1317 they look like a row of gravestones. By g1318 they hide the card ranks completely: only spear tips and a few helmets show over a navy band. They are untextured primitives, not flat 2D puppet cards, and at this distance (12-18 % of the frame) they read as boxes, not men. In a bloodless comedy, a row of tombstones lifting out of the ground at the climax is the wrong image too. (H2a got away with it because it sees them small and from far away; its own QA-art N1 already flagged the "tombstones".)
Fix (preferred): make the camera-side ranks blue Scots CARDS facing the English (face, blue tunic, spear levelled), and put the 3D bodies BEHIND them as depth filler. Have them rise as figures jumping up (squash and stretch, 4-6 frames), not as slabs sliding out of the ground. Because this changes the wall at P_NECK, ask the H2a team to apply the same swap to their g1342-1357 (it is their N1). Then re-check the D6.
Fallback (if H2a is not reopened): keep the bodies down until g1327 so the slam and the English jump read with the card faces. Raise them behind the card ranks while the camera eases back, and they only need to reach H2a's layout by g1340, where they are small.

**B4 (blocking per the caption-band rule, trivial), g1329-1336: chins in the caption band.** The front English faces dip 6-15 px below y 880 (measured: rows up to 886-895 at g1329, 1330, 1333-1336). qa_auto missed it, probably because it uses the projected anchors. Fix: nudge the front two English 0.3-0.5 m back (toward the wall), or raise the aim point about 2 % in g1326-1340. This falls out naturally from the B2 camera path.

**N1 (non-blocking, open since v2), g1324-1348: the saltire banners still read near-black** (navy with a faint violet X, cropped at the left edge). The team says no lighter blue is available in this staging. It matches H2a, so leave it for the shared set fix (emission about 0.3 or a second-side light, white cross).

**N2 (non-blocking, open since v2), g1309-1326: the bottom half is bare dirt.** The slam plays in a strip at y 430-620 and 45-55 % of the frame below it is empty orange ground. The B2 re-path is the chance to lift the slam: raise the camera or aim so the wall sits around the frame centre, or put a foreground prop at the bottom edge (a dropped helmet, a spear, a gorse bush).

**N3 (non-blocking), g1322-1348: helmets pop off, but the English still wear helmets.** The card helmet flies, the painted helmet stays (team note), so at g1334-1338 there are helmets on the ground while every Englishman still wears one. The gag reads weaker. Fix: swap the hit five to a hatless head drawing (or paint the helmet off the card) from the pop frame on.

**N4 (non-blocking), g1339-1348: the white crescent smoke strokes** above the camp (left of the tree) are still there. They are the same in H2a, so leave them for the set.

Tents: background only (striped pavilions, g1312-1348). Not judged against the tent set fix.

## Checks
- Nothing floats: feet and contact shadows OK. Flying helmets only while in motion. Nobody is sliced.
- Face size: max about 12 % of the frame height (g1330). Frame edges: the banner is cropped at the left from g1326, acceptable as a foreground frame.
- Colour story: crimson English against blue Scots reads well in the second half. The Scots navy needs B3 and N1 to read as BLUE on a phone.
- Characters acting: yes, to g1348.
- Camera clearance: OK. The fg tree crown wipe at g1307-1310 is a deliberate pass.
- Bloodless: nobody down or still. See B3 for the gravestone look at g1317.
- Phone legibility: the charge 8, the slam 4 (it lasts 1-2 frames before the slabs cover it), the spear wall 5 (spear tips over a navy band), the English turning and hopping 7, the helmets 6.

## Scores
phone legibility 6 / set density 7 / light 8 / colour story 7 / acting and comedy 7 / same channel? yes for the ride and swoop / camera travel 8 (the join 3).
