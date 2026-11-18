# QA-art RE-CHECK, film 14, s28 v2 (ENDING, shots 28-30, g1908-2104): FIX-FIRST (one item: shot 30 only)
Reviewed: take.mkv every 7th frame (~4 fps, 29 frames) at full 720x1280 and in 360x640 grids; full frames g1940/2025/2050/2100; every-3-frame sting strip g1962-1998; phone_sheet.jpg. Checked against film/film14/qa/s28_QA_ART.md and s28_QA_TECH.md (v1).

## v1 QA-art items
| # | item | status | note |
|---|---|---|---|
| 1 | Shot 28, readable ask | FIXED | The empty hive box is now held chest-high in both hands, with sad raised brows, a wavy mouth and a sweat drop; the farmer has a smug grin, hands on hips. It reads as "the mocker comes to beg" on the phone sheet. He is still frontal rather than 3/4, but that is acceptable. |
| 2 | Shot 28, reframe | PARTLY | Pushed in and lower; the bare soil is now mostly in the caption band (y > 880); the faces are bigger. The trampled field over his shoulder was not added (nice-to-have). |
| 3 | Shot 30, continuity and size | PARTLY | Size FIXED: the face and trunk are big. Continuity NOT fixed: in shot 29 he stands on the trestle stool (feet at y ~760, trestle to y ~950). In shot 30 (g2032-2104) his feet stand on the grass with a contact shadow at y ~900-1000, so he drops by the height of the stool at the cut. It is visible on the phone sheet (g2028 -> g2043). |
| 4 | Shot 30, end on a gesture | FIXED | Blink at g2095-2099, a small change at the trunk tip; the last frame is alive. The trunk reaches full length on "งวงช้าง", the tip stays above y 880, and the hard cut is at g2104. |
| opt | Shot 29, show the hive being hung | PARTLY | The hand rises to the bar at g1971-1985, but the hive stays behind his legs and never visibly lifts. Fine as it is. |

## v1 QA-tech items
| # | status | note |
|---|---|---|
| 1 edge clipping in shot 28 | FIXED | both silhouettes are inside the frame |
| 2 hive box legibility | FIXED | big, in front of his chest |
| 3 loose composition | PARTLY | acceptable |
| 4 static poses in shot 28 | FIXED | small head tilt and hat movement; subtle but alive |
| 5 shot 29 clutter in the caption band | PARTLY | trestle feet at ~y 950 and grass below; minor, acceptable |
| 6 sting timing and contact | FIXED | the bee rises from the hive (g1989) and is on the nose with the nose turned red at g1992 (1-2 frames late, which is fine) |
| 7 stool continuity, cut 29 -> 30 | NOT | see item 3 above |
| 8 hand-to-hive link in shot 30 | FIXED | the hive and pole hook are in frame at the left |
| 9 shot 30 bottom zone | NOT | his legs, feet and grass are in y 880-1000; minor, and it goes away with the fix below |
| 10 handle | n/a | |

## New issues (non-blocking)
- Shot 30: the top of the cap touches or crosses the top edge of the frame (g2034-2104). Acceptable.
- Shot 28: the sky shows a curved bright "dome" arc in the gradient (the same artefact as s07 shot 10). Cosmetic.

## Scores (1-10, v1 -> v2)
| area | v1 | v2 |
|---|---|---|
| Key moment / payoff clarity | 7 | 8 |
| Comic timing | 8 | 8 |
| Character acting | 6 | 8 |
| Composition / framing | 6 | 7 |
| Light and colour | 8 | 8 |
| Set density | 7 | 7 |
| Match to references / client taste | 7 | 8 |

## Verdict: FIX-FIRST, one change (re-render shot 30 only, g2032-2104, 73 frames)
1. **Shot 30, keep him on the stool.** Put the same trestle-stool sprite from shot 29 under his feet (parented, as in shot 29), so its top bar and upper legs show at the bottom of the frame. Or lower and tilt the camera so the frame ends above his knees: no feet, no ground contact. The trunk tip (lowest at y ~840) must stay above y 880 either way. Everything else in this take can SHIP as it is.
(If the director wants to ship without this, rule E applies: an override needs a second, independent Opus reviewer who has seen the frames.)
