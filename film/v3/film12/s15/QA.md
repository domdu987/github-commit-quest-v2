# QA s15 (film 12, shots 15-18 REVEAL), g 1043-1345 (cuts at g1116, g1200, g1272; 6-frame handles)
qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg). Its note "planned cuts with no visible change" is a threshold artefact: measured mean abs frame diff at the cuts is 40 / 27 / 33 against ~6 inside shots.
Renders: 720x1280, 20 samples, OIDN, ~24 s/frame (2 processes x 2 threads). Shot 16 (g1116-1199) re-rendered once after a first pass whose crowd was too small for a phone.

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
