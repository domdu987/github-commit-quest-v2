# film17 s02 (shots 4-6) QA, round 2
Frames g138..341 (g0 144, g1 336, 6 handle each side), 720x1280, 12 samples + OIDN. take.mkv split: `cat take.mkv.part* > take.mkv`.
Cuts 222 (hard, wide -> medium), 285 (street -> front desk). transition_in dissolve 11.
## qa_auto: PASS.  Rhythm: in-shot median 4.18, p90 12.52 (targets >= 4 / >= 12; thin margin)
## Round-2 fixes (director gate s02 round 1)
1. Shot 4: own animated wagon (set wagon removed at runtime) rolls in from depth, eased stop by g200; station door + lantern glowing behind it; gendarme marches in, stops left of the wagon, stays fully in frame; puddles hidden (no reflection/slab).
2. Shot 5: rear door opens (hinged leaf, g218-234), thief steps down, gendarmes grip his upper arms (hand pins, error 0), his right hand goes to the beret brim, closed smile. The cap does not lift (sprite limit).
3. Shot 6: set-prop front desk (table, open ledger, inkpot, ledger stack) between thief and gendarme; the foreground stool is out of frame; thief shrugs, gendarme shrugs then waves.
4. Mouths fixed per character per shot (flat; thief smile in shot 5), no changes.
5. White puddle blob / blue ghost: puddles removed; no light shafts over cast; no dust visible.
## Self-check: contact.jpg (every 6 f), phone_sheet.jpg, draft sheet every 4 f, cuts +-3 in draft
Heads above y 880; shot 6 heads ~0.5 H. Not every frame at 6 fps was viewed individually.
## Known weaknesses
- Shot 4: marching gendarme stands centred in front of the wagon rear around g190-218; thief absent (plan has him from shot 5).
- Cut 222 is a hard cut but both shots show the wagon (qa_auto notes low change); camera moves differ.
- Blue gendarme's grip is mostly hidden behind the thief; shot 5 end heads are large (~130 px).

## Round 3 (director gate R2, shot 5 + extras)
- Blue gendarme: mirrored card (place flip) with a pinned hand on the thief's other upper arm, visible.
- Thief: hand on the 'top' layer reaches the beret brim in front of his face, held g246-270, closed smile. full/g_0240.png, full/g_0260.png are full-res.
- Shot 6 re-rendered with the inkpot quill removed (floating quill gone). The thief's shot-6 face is unchanged (fixed flat mouth, 'worried' eyes; blink only).
