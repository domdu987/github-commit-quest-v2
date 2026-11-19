VERDICT: FAIL. 3 blockers, all in shot 12 (g821-863). Shot 11 is unchanged and still passes.

Director note: the hive count in shot 14 (fs3, 16 hives) against 10 in shot 12 is accepted. Day 3 = "all hives + the wire", and nobody can count 16 at phone size. Not a blocker.

1. **Shot 12: about ten hives do not read at phone size.** At the end of the crane (g863), you can make out 7 gold dots at 180x320. Two more are 1 px specks (x 212 and x 548, full-res coordinates). You cannot see the hive boxes themselves; each is about 3-6 px wide. At full size there are 9 glows. About 6-7 boxes stand apart; the other 2 are partly hidden behind the palm trunks. The 10th hive is not in frame. The L shape does not read either. At phone size it looks like one slightly bent row of lights along the edge of the maize, not hives "round the field". The crane works against the beat. Moving "up and out" makes the hives smaller over the shot: the glow area at the centre hive drops from 1196 px at g821 to 279 px at g863, so the frame where the count matters most is the frame where the hives are smallest. The director accepts an L only if about ten clearly reads. It does not, so this blocker stands.
   Fix: end the move on a framing where all 10 hives are in frame and each box is at least 8 px wide at phone size (at least 32 px at full size). Use a longer lens (35-50 mm) from further back and higher, about 5-6 m, tilted down 12-18 deg. The long lens squeezes the ring together and puts the maize field behind the hives instead of bare ground. Or reverse the move: crane up while pushing in, so the hives grow as the narration says "ten".
2. **Shot 12: too much sky and too much ground.** At g863 the sky, the mountains and the tree line run from y 0 to about 615, about 47 % of the frame. Bare laterite runs from y 720 to 1280, about 44 %. The hive band (y about 625-720) is only about 8 % of the frame height. At g821 it is about 47 % sky and 37 % ground. This comes from keeping the camera "nearly level" with a 17-20 mm lens.
   Fix: with the lens and tilt from fix 1, put the horizon at about y 300-380 and make the hive band 25-35 % of the frame height. Keep the band between about y 400 and 850, above the caption band at y 900.
3. **The gold "bee-cluster glow" reads as a lamp, and it breaks continuity.** At full size each glow is a flat, bright yellow disc 20-25 px across. It sits in front of the box's bee end and covers it (see g863_glow_4x.png). At phone size the row looks like string lights or lanterns under shelters, not bees. Shot 13 and shot 14 (take s13) show the same hives with no glow, so the cue appears in shot 12 only and then disappears.
   Fix: replace the disc with a cluster of small gold-and-dark bee specks on the box face, plus a warm emissive or rim light on the bee end, and keep the box visible. Either keep the same cue in shots 13 and 14 or rely on box shape and colour alone.

Take: r25/film/v3/film14/s11/take.mkv. 117 frames, g753-869, 720x1280, 30 fps, 3.90 s. meta.json: shot 11 = g759-820, shot 12 = g821-863, handles of 6 frames. Team note: QA.md, section "v3".
Review frames are in scratchpad/takes/qa_s11v3/:
- all/ holds every frame, named by g number.
- s12_phone.jpg is the phone sheet for g818-869, with a cyan line at y 880.
- g863_hiveband_2x.png and g850_hiveband_2x.png are the hive band at 2x.
- g863_phone_band_4x.png and g850_phone_band_4x.png are the hive band at phone size, enlarged 4x.
- g863_glow_4x.png is one glow at 4x.
- continuity.jpg shows shot 11 -> 12 -> 13 -> 14.
- s13/ holds the s13 take, from git archive of origin/render14/team6 film/v3/film14/s13, with parts joined and frames extracted.

Glows were counted with a threshold for bright yellow pixels, at full size and at 180x320:

| g | Glows at full size | Glows at phone size | Clear dots at phone size (more than 1 px) |
|---|---|---|---|
| 821 | 6 | 6 | 6 |
| 840 | 9 | 9 | 7 |
| 850 | 10 blobs (9 hives; 2 blobs are one hive split by a palm) | 9 | 7 |
| 863 | 9 | 9 | 7 |
| 869 | 9 | 8 | 7 |

## Checks
| # | Check | Result |
|---|---|---|
| 1 | Count at the end of the crane | FAIL. At phone size: 7 clear dots, 9 if you count the 1 px specks, and no boxes you can read. At full size: 9 glows and about 6-7 separate boxes. The 10th hive is not visible. Team claim "9-10 countable": not confirmed at phone size. See blocker 1. |
| 2 | Reads as hives all round the field | FAIL. It reads as one row of lights at the front edge of the maize. The near corner is around x 330-455, and the right leg falls behind the palms. Neither the L nor "round the field" reads at phone size. See blockers 1 and 3. |
| 3 | Heads above y 880 | PASS. Shot 11 is unchanged: the farmer's head is at about y 560-760. Shot 12 has no people, only a goat and cattle in the background. |
| 4 | No pops; cut at g821 clean | PASS. The cut at g821 is a single-frame change (diff 40.6), with clean frames on both sides and no black or magenta frame. Shot 12 frame-to-frame diffs run smoothly at 5.3-7.2, with no spikes, through the handle to g869. The g757 handle pop (diff 6.1) is still there but is waived by the director note. |
| 5 | Camera always moves | PASS. Shot 12 changes every frame by 5.3-7.2 and never holds. Shot 11 is as in v2. |
| 6 | No text | PASS. There are no letters or signs. The hut has only a window. |
| 7 | No excess ground or sky | FAIL. About 47 % sky and about 44 % ground at g863. See blocker 2. |
| 8 | Continuity with shots 11 and 13 | Shot 11 to 12: PASS. Both are daylight; shot 12 has a pinker sky, which works as "Day 2". Shot 12 to 13: the hard cut is fine, and the change from day to dusk works as time passing. The hive glow disappears, see blocker 3. Note: the hive roofs in shot 12 are grey tin with tan eaves; check that they match the roofs in shot 14. |

## Shot 11 is unchanged (verified)
- Compared with the v2 frames, g753-781 are identical (diff 0.00).
- g782-820 differ by a mean of 0.12-0.56, with a maximum of 10 per pixel and no pixel over 12. This is re-encode noise only; the content is unchanged.
- All v2 shot 11 results and non-blocking notes still apply: stool contact shadow, caption covering the stool, eye-line, and the veil flipping sides across the 11 -> 13 cut.

## Team claims
- "Crane up and out": confirmed, but the move shrinks the hives (blocker 1).
- "Gold glow on all 10 hives": 9 glows are visible. The 10th is not in frame or is hidden by the palms.
- "9-10 countable": not at phone size, where 7 are clear.
- "L, not a full arc": the geometry is a shallow L, but at phone size it does not read as one.

## Note for the director (outside this take's scope)
The s13 QA.md describes shot 14 as "all 16 hives on ONE thin matte wire". Shot 12 says ten hives, and v1 item 3 asks for the same ring and the same hives in shots 12 and 14. Confirm the intended count before shot 14 is approved.
