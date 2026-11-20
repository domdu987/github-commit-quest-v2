# QA-tech sH1 v2 (team9 c91a790)
Checked: take.mkv (110 frames, g1239-1348, 720x1280), every-5th f6 stills, full-size stills at n0/5/70-109, phone sheet. Colour-only items waived (conform normalizes). qa_auto PASS; rhythm median 13.58, p90 20.93 (no stills, no cut).

## Verdict: PASS
No blocking issues. The charge, the slam, the English hop and the helmet pops all read at phone size. Ends on P_NECK. The non-blocking notes are for polish or the director.

## Fixed against the old list (QA_TECH v1 + QA_ART)
| old item | status |
|---|---|
| 1 slam unreadable, wall tiny | FIXED. At g1316 (n77) the camera is close, wall figures ~12-15 % of frame height, spears level, tan dust visible at the deck mouth. The snap is visible. Wall formed after g1310, not before. |
| 2 no blue saltire | FIXED. Three tall navy-blue saltire banners (about 20-30 % of frame height) rise g1312-1320. Scots tunics are blue. Blue vs English crimson reads at once. |
| 3 English stand still | FIXED. Turn head, then 8-frame hop back toward the lens from g1313. Wide eyes, open mouths (n77-95). |
| 4 ground slab g1299-1305 | FIXED. No slab; the camera clears the shelf (f6 g1299/g1304 show terrain and river). |
| 5 head over y880 | FIXED. Nearest English heads at y ~500-800 on n79-109; all above 880. |
| 6 static end | OK as is, see note C. |
| QA_ART: helmets visibly pop | FIXED. 5 kettle hats fly up and land crooked on the ground (n79-95). |

## Beat table
| g | n | beat | reads at phone size? |
|---|---|---|---|
| 1239-1275 | 0-36 | Ride behind 5 blue Scots, spears forward, gorse past, shake, sun shafts | YES. Strong and in the R7 ride style. Faces 12-18 %. |
| 1275-1297 | 36-58 | Overtake, swoop over river and sand to the bridge mouth | YES. Travel, nothing floats. |
| 1297-1312 | 58-73 | Descent to the bridge mouth; English on the bank in crimson, blue banners rising | YES. English tiny but legible; Scots flank running in. |
| 1312-1322 | 73-83 | SLAM on "ปิดหัวสะพาน": spears level, dust, banners up, English hop, helmets fly | YES. Key moment readable, comic and bloodless. |
| 1322-1335 | 83-96 | English land, hats crooked, react with shocked faces; Scots wall bristles | YES |
| 1335-1345 | 96-106 | Ease back to P_NECK, wide tableau: crimson English in front, blue wall and banners behind | YES. English boxed in, blue vs crimson. |
| 1346-1348 | 107-109 | Handles start the crane up | OK |

## Checks
- Heads above y880: PASS throughout.
- Nothing floats: PASS. Feet and contact shadows on every card. Hats are in flight only during the pop, then land.
- Frame edges: PASS. Only runners at the left edge in n70 (partial, in motion), fine.
- Face size: PASS. The biggest face is in the ride (n0-36, about 15-18 %), under 35 %.
- Colour story: PASS. English crimson against Scots saltire blue on teal river; the gold is mostly in the ground and pavilions.
- Camera: eased, no clipping after g1299, no cut inside.
- D6 handle at P_NECK: lands on P_NECK per meta.json (cam_out -2,50,4.6 -> 0,22,1.8, 22 mm). Frame n109 shows the P_NECK framing, with 3 handle frames of crane start. PASS.
- No mouths moving in a quote window; no blood.

## Issues
A. NON-BLOCKING, g1322-1345 (n83-106): the wall figures shrink to about 5-6 % of frame height at P_NECK, and the lower 45-50 % of the frame is empty ground. The slam image is carried by the banners. This is dictated by the P_NECK pose; fix if wanted by lowering the camera tilt in H2a, not here.
B. NON-BLOCKING, g1316-1325: some English keep their painted helmet while a card hat flies off (double hat when paused). Known limit declared by the team; reads as a pop at speed.
C. NON-BLOCKING, g1335-1348: the English stand still with sad faces (n100-109), little motion. The camera pull-back and the crane carry it. Optional fix: a 2-frame head shake or a fall onto their rear for the English at x 140-300 over g1335-1345.
D. NON-BLOCKING, g1339-1345: the deck mouth between the wall halves still shows a visible gap (x 340-400 at n109), though Scots flank both sides. H2a must keep this the same (director's call on the continuity).
E. NON-BLOCKING, banners are near-black navy against the sky (n77-95); saltire lines are thin. The conform may lift it; if not, brighten the cloth to saltire blue.
