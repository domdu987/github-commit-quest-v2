# ROUND 4 (director gate r3) -- g1163-1174 and g1200-1271 re-rendered; qa_auto PASS
1. Coin pass REMOVED (director allowed it): no pop-in disc crosses his face any more; his purse shake and the crowd rush carry g1173.
2. Shot 17 camera aimed further right (look x 5.4/7.2): the coachman stays fully in frame to the cut at g1272 (hat within a few px of the edge on the very last frame only); runners start further away and move less, so nobody crowds the left edge.
Not done: Hanway's face to the left edge at g1339 was optional and not touched (path unchanged since round 3).

# ROUND 3 (director gate r2: QA-art PASS, QA-tech FAIL on 2 breaks) -- all frames re-rendered, qa_auto PASS
1. The diagonal line across the coachman's mouth/chest was the set's rein objects (`coach_i_reins`): hidden in render, his face and chest are clean in all of 15-18 (checked g1085, 1173, 1255, 1307, 1320, 1339).
2. Shot 18 has its own camera (CAM18) re-aimed right and closer: the coachman is fully in frame and larger through g1339, Hanway stays in frame (path x -2.3 -> -2.0), the grin drop at g1307 is clear (the first passenger of coach 0 is skipped in 18 so nothing covers him). Shot 17 camera aimed further right: no hat/head clip at g1252-1262.
Polish: at g1163-1174 a big gold coin arcs from the crowd up to his hand/purse; passenger cards moved to x 2.35 (behind the street-side wall line) so they sit at the window level; the one-frame thunder flash on g1116 was NOT added (optional).
Remaining weaknesses: the coin is a flat yellow disc (no gold glint highlight visible at phone size); passengers are still flat cards; at g1339 the coachman's hat is within ~10 px of the right edge.

# QA s15 (film 12, shots 15-18 REVEAL), g 1043-1345 -- FIX ROUND 2 (director gate: FAIL/FIX-FIRST on round 1)
qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg; its "cuts with no visible change" note is a threshold artefact: frame diff at cuts 27-40 vs ~6 inside shots). 720x1280, 20 samples, OIDN. Whole take re-rendered after the gate.
Fixes made: (1) 16 = one mechanism picture: 24 crowd cards shoving at the doors, passenger cards in the windows (set's black pin silhouettes hidden), coachman big in frame taking coins into the purse at the g1173 clink (purse shake), rain 0.7 -> 1.4/1.5 (hook accepted >1); (2) 17 closer and lower camera, all four coaches roll away with a passenger card per coach, 4 runners chase them; (3) 18 six soaked queue cards, Hanway on a path 2.5 units left of the coach with a soft contact-shadow disc, box_b dropped so no shaft crosses a second face; (4) 15 busy 0.02 keeps coach lanterns lit warm (no black rectangles), coachman looks up from g1083, rain swells 0.7 -> 1.4; (5) coachman is now the SEATED box pose (coach_box=0) at plank z-0.9, same in 15-18, shorter than the cabin; cameras re-aimed so nothing clips at the right edge.
Parenting: coachman and passenger cards use coach_dy(i, g), the exact function behind the coach's linear y keys, so they move with the coach (checked on stills). No splash used.
Heads above y 880 everywhere; nobody speaks; magenta 0.0 %.
Known weaknesses: flat cards (passengers show head and torso over the cabin side, not inside a window pane); in the last frames of 18 (g~1328-1345) queue and passenger heads partly cover the coachman, so his grin drop (g1307) reads best at g1307-1325; horse low-poly; thunder flash on the cut not added; hero umbrella handle/hand is the card art as drawn (not edited).

| shot | g | what | check |
|---|---|---|---|
| 15 | 1049-1115 | coach_close-style push on the head coachman counting coins, looks up at the rain (g~1087), rain swells 0.7 -> 1.0 | face ~120-250 px, purse and coins readable; head y 403-511 |
| 16 | 1116-1199 | 24 cast12 crowd cards run from the left kerb and push in at the doors; coaches fill 0 -> 3 (set_rank_busy keyed); coachman switches to the purse pose at the coin clink (g1173) | crowd large in frame, reads as a rush; coachman head y min 138 (still above 880) |
| 17 | 1200-1271 | low camera, coaches 0-3 roll away full (silhouettes in windows), coachmen b/c cheering | pace 0.11 u/frame; coachman cards use the same linear y-key as the coach |
| 18 | 1272-1339 | Hanway (smug walk, amber rim) strolls dry past two wet wig-wringers; head coachman's grin drops (pose switch at g1307 = 43.55 s) | Hanway head y >= 269 |

- Heads above y 880: all (box_a 138-525, Hanway 269+). Mouths: nobody speaks; poses keep their held mouths. Hue: magenta 0.0 %.
- Director rule (people on moving coaches): coachman cards follow the coach's keyed y exactly (same function as the keys), passengers are the set's silhouettes parented to the coach. Verified by eye on 6 fps frames in 17-18, no slide. No wheel splash used.
- Known weaknesses: cards are flat sprites (the rush crowd bunches at the doors, rolling pose is a held pose); the horse is low-poly and large in shot 15 B; shot 17 street ahead is empty after the rush; wet-queue figures in 18 are small; coachman in 15 does not animate beyond blink, purse jiggle and a bob.
- Not done: no separate 6 fps full contact review beyond phone_sheet and contact.jpg; shot 18 coach continuity: coach 0 ends 4.0 units rolled forward and stays there in 18 (cards follow).
