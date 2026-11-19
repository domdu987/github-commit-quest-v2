# QA_TECH s16 (film 13, TAKE gate) - FAIL

Checked: qa_auto every frame (plan cuts passed), 6 fps + every cut +-3 frames, full-size key frames, join with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13/s16/ (sheet_*.jpg, full/<g>.jpg). Take files untouched.

Global note G1 (all takes): delivered cuts sit at round(t*30) of the plan table, i.e. 3 frames (0.10 s) EARLIER than the plan's g = round((t+0.10)*30) (e.g. shot 3 at 108 vs 111, shot 11 at 650 vs 653, shot 17 at 1107 vs 1110, s26 cuts 1740/1772/1868/1906 vs 1743/1775/1871/1909). qa_auto reports every planned cut as 'no visible change' or as a pop 3 frames off for that reason. Fix: conform must cut at the plan g (handles cover it) or the take must be re-keyed +3 frames; in-shot cues (e.g. nickname jump g895, splash g1893) are not consistently offset either.

Auto: PASS (no frozen/pop; plan cut 1044 'no change' = G1, shot starts 1041).
1. g 1035-1059 (25 frames): a large translucent pale-tan wedge/triangle with a hard diagonal edge covers the lower right ~45 % of the frame (visible at g 1035-1055, shrinking and sliding out by g 1060). Looks like a stray overlay/shadow-catcher polygon, not scene geometry. Fix: find and hide the offending mesh/plane (likely ground patch/light card) and re-render g 1035-1060.
2. g 1060-1112: flat brown 'mud' blobs lie on top of the plank aisle in the foreground (low-poly, no contact shadow), look like pasted shapes in a floor of planks. Fix: remove or give them contact shadows / proper placement.
3. g 1041-1112: workers' faces all scowl with teeth bared, standing with bars as if fighting; legs are thin spidery lines; rows beyond ~6 workers are not the 'each man by 10 jacks, 500 workers' read. Pullman in the aisle is 40 px tall, hardly visible (centre, behind the lamp). Fix: show Pullman walking toward camera mid-ground; relax faces to neutral.
4. g 1035-1112: lamps, beams, blue-violet shade/warm lamp: good; but upper 35 % is flat timber ceiling pattern. Minor.
5. Heads < 880 (workers heads y 520-700). No mouth flapping beyond cast grimace. Join s16->s17 (under -> suite): hard cut OK. Join in: see s15.
