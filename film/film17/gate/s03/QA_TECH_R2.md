# QA-tech film17 s03 R2 (shots 7-8, g330-450, commit 3fcb09e): PASS

Method: full-size frames g330,350,370,385,389,390,410,430,450 (f6/) plus extracted all 121 frames from take.mkv, crops of the clerk, and a per-frame diff curve.
Cut: g389 aisle -> g390 desk, hard cut (diff 39 at g390, 4-7 elsewhere). QA_AUTO "cut not visible" note is a coarse metric only.
Auto/manual: no black/blank/magenta frames, no frozen run (every frame diff >= 3.5, no hold anywhere near 1 s), no blur (all sampled frames sharp, no DOF), no see-through cards, mouths closed in all frames (g410 eyes shut, mouth still).

## R1 items
1. White bloom disc g375-389: FIXED. Frames g375/380/385/387-389 show no bracket and no white disc. Only normal wall lamps remain (small, <30 px).
2. Both cards fully in frame g390-450: FIXED. g390 left card x40-355, right x365-650; g430 left 55-410, right (partly behind left card) to 580; g450 right to 575. Margins >= 40 px. Moustache card never cut off.
3. Cards bigger, same tone, bold moustache: FIXED. Both cards ~300 px wide, same frame style and same face tone, front-lit; moustache ~100 px wide at full size, so ~50 px on the 360 phone sheet. "Same face, one has a moustache" reads at phone size.
4. Spilled piles with faces / fg stacks: PARTLY. Piles now carry visible small photo faces (g330, g350). No real foreground card stack, only a pile cut at the bottom-left edge (g330-389). Clerks are Bertillon ~60 px and another ~55 px head: lost-clerk read is OK.
5. Cuff/hand: PARTLY. Cuff is now attached to a sleeve and hand (g395-445), no floating bar. Hand touches hair only from ~g430-445; at g395 it hangs at cheek height and at g410 there is ~10 px gap between the hand knob and the hair.
Claim 5 (light shafts hidden, dust 0.5): shafts gone, a few dust specks in the skylight shaft remain (fine). Highest chin y: head bottom ~585 in shot 8, ~830 max in shot 7 (Bertillon at the carpet, whole body), all below 880 limit for heads (heads y < 700). OK.

## Claim checks
- Claim 1: TRUE re: no bloom. The two "snaps" (g346-355 and g367-375) are 9-10 frame lateral slides, diff ~20 vs ~6 base. Frames are sharp, no blur, no character pop, no ghosting. They read as quick drifts, not snaps; fine.
- Claim 2: TRUE except "clerk head 68-76 px": measured head ~140-150 px wide x ~150 px tall (g390-450). Still well clear of y 880 (head y 440-600) and does not compete, so no action.
- Cards "turn to face camera" / camera orbits: TRUE (trapezoid tilt, camera swing g420-431 diff 9-13, sharp).
- Claim 4 head size ~55 px: TRUE for shot 7.

## Blocking
None.

## Should-fix (non-blocking)
S1. g390-450 shot 8: book stack and box under the cards show jagged inverted-outline / clipped geometry where the left card bottom and the stack meet (about x70-330, y740-900 at g390; same at g450), plus a loose white quill-like scrap at ~(350,850). Reads as messy; clean the overlap or push the stack lower.
S2. g395-410: hand knob not touching the head (see item 5); lift it 20-30 px to the hair so the scratch reads from g395.
S3. g330-389: add one real card stack in the foreground (only an edge-cut pile exists).
S4. g420-431: an unplanned 12-frame camera swing in shot 8 (diff 9-13); not blurred, acceptable, but check it is intended.
S5. Shot 7 camera is nearly eye-level looking down the aisle rather than a clearly high angle; acceptable.

Deviations: Bertillon as scratching clerk in shot 8 ACCEPT; lost clerks ACCEPT.
Verdict: PASS (0 blocking, 5 should-fix).
