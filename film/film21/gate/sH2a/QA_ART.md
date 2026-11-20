# QA-art, TAKE gate, film 21 sH2a (H2a crane up to the trap, g1345-1392, KEY take for the reveal)
Inputs: take.mkv (54 f, 720x1280), contact.jpg, phone_sheet.jpg, full-size frames n0/3/6/9/12/18/30/50 and a strip of n12-20 (in the scratchpad gate dir), refs R5_sheet / R7_sheet, shot_plan row H2a, QA_TEAM.md QA-art + G/H/I.

## Scores (1-10)
| item | score | note |
|---|---|---|
| set density / ornament | 7 | Bridge-mouth start is rich: tents, banners, smoke, tree, river glints, long shadows. At P_TOP the woods outside the loop are dense, but the loop floor is an empty sand plane with a grid of pegs. |
| lighting & colour | 4 | The start (g1342-1354) is lovely: low warm sun, violet shadows, blue river, close to the reference look. From about g1358 the same sun turns the sand LEMON yellow and the river edges a NEON cyan glow. The top view looks like a different time of day and is acid, not "signature colour". |
| composition / framing | 6 | The bottle silhouette at P_TOP is a strong graphic (bulb, neck, bridge as a stopper line). But the camera passes the nadir and the world spins about 180 deg in 4 frames (n14-17, about 0.13 s), which is disorienting. |
| character acting | 6 | Neck frames are good: worried faces, sweat drops, helmets, rim gold. At P_TOP everyone is a peg, which is expected. |
| key moment (reveal) clarity | 4 | BOTTLE reads. CORK and CRIMSON do not: see below. |
| match to references (R5/R7) | 5 | The first third would sit in the channel. The top third does not: R5 keeps one dominant deep blue with warm accents, and this is yellow plus cyan at equal strength. |

## Answers
1. **Does the trap read in about 1.5 s on a phone?** Only half. The river loop and bottle shape read instantly on the phone sheet (g1372, g1387). The cork does not. The Scots wall at the bridge mouth is a dark comb of shadows about 8 px deep, with no blue (Scots wear green/orange/brown, and there is one saltire at n9-12 that is about 3 px at top). The bridge deck also sticks past the wall into the loop, so the mouth does not look plugged. The English inside are grey/white pegs with tiny red AND blue caps plus long black shadows. They read as "dark stubble", not a crimson army, and the blue caps fight the Scots colour code. The other half on the south bank is cut off at the bottom edge: only tent tops show, and nobody is visible.
2. **Beautiful and in the reference style?** The first 0.4 s, yes. The end hold, no: it is a clean diagram on a garish ground.
3. **Too garish at 0.75 saturation?** Yes, at the top. Mean 0.75 and 84 % vivid hide the issue: the problem is the lemon sand (near-pure yellow, high luma) next to neon cyan rims, with no dominant hue. The early frames are also highly saturated and look fine, because the warm/cool split is controlled.
4. **Early-frame "blur": acceptable motion or a real problem?** Not a problem. At full size n0, n3, n9 and n12 are crisp (faces, helmet rims, spear tips, plank edges, grass blades). The flag comes from smooth stylised sky, water and sand at 90x160 thumbnails, and there is no DOF. Override the qa_auto blur FAIL for this take. The real motion problem is the nadir flip (n14-17), not blur.

## Verdict: FIX-FIRST
This is a KEY reveal take, and the reveal's two story colours (blue cork, crimson English) are not visible.

## Fixes (max 4)
1. **Make the cork a cork.** Move the spear wall so it closes the land end of the bridge mouth: the deck should end AT the wall, not run past it. Make it about 3x deeper (4-5 ranks, or scale the formation at P_TOP), dress the Scots in blue tunics, and put 4-6 large saltire banners on the wall (at least 25-30 px at P_TOP, flying toward camera). Optional: a thin bright spear-tip highlight line.
2. **Make the bottle crimson.** Recolour the 280 English placeholders as solid crimson bodies (no blue caps, no white tops), packed tighter, so they read as one red mass at P_TOP. Shorten or soften their shadows at the top so the mass is not black stubble. Recolour the blue-tunic English in the neck group too, so blue means only Scots.
3. **Tame the top colour; keep the golden-hour look of the start.** Grade the loop sand from lemon toward the warm ochre/orange of n9-12 (lower the albedo/value about 20-25 %, and move the hue toward orange). Cut the cyan shoreline emission/glow by about half. Push the river to the deep blue of n9 so the frame has ONE cool dominant (river) against ONE warm field. Target mean sat about 0.60 and luma at or below 105.
4. **Kill the nadir spin and frame the south bank.** Keep the camera's up-vector heading constant through the crane: tilt up and over without passing straight down, or pre-rotate the yaw during the first 0.3 s, so the image never rolls about 180 deg in 4 frames. Adjust P_TOP (lower aim point / slightly wider, or move it back toward the south) so the south-bank half shows as a visible crimson block (about 15 % of frame height) above the caption band. The H2b join at P_TOP must then be re-checked by the director.
