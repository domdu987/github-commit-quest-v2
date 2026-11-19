# QA s20 v3 (shots 20-21 re-done; 22-24 locked from v2)

# QA s20 v2 (shots 20-24, THE REVEAL), g 1301-1683, 383 frames, 720x1280

v2 after the director gate (s20_QA_TECH / s20_QA_ART) and continuity notes.
- Wire: 3 cm radius, matte grey-silver (was a fat white tube); steeper V (bow rises in 0.38 s) at the chest, push point x 10.25.
- Shot 20 (g 1307-1367): camera INSIDE the fence on the field side, close on the matriarch pressing the V-bent wire toward camera (per the latest continuity note), then slides along the wire past 3 large hives; near roof/posts/banana leaves and the mountain peak removed (no blue placeholder, no roof through her body); u4 knocks and starts to swing at g ~1330.
- Shot 21 (g 1368-1452): hive-height cut-away from the row end, roofs removed, 5 hives readable (apparent size boosted with distance), wave with ~16 frame delay hive to hive, swing ~0.7 rad, small bee puff at each knock.
- Shot 22 (g 1453-1502): bees leave the hive entrance from the first frame, ~3x count (cards + 3D), sustained to the cut; foreground lantern pool dimmed.
- Shots 23-24 (g 1503-1683): night-graded card (x0.70, tint 0.78/0.82/1.0, cool top rim, warm hut side), long contact shadow, loose bee clouds (no rope strips) with the eye clear, ears flared + wide eye + trunk swats, mouth CLOSED until g ~1646, trumpet at g 1653 with trunk up and fewer bees on it.
- Checked every frame at 6 fps (contact.jpg, phone_sheet.jpg) and every cut +-3 (g 1368, 1453, 1503, 1599): clean hard cuts. Heads stay above y 880, no steep down-view, no text, no DOF.
- QA_AUTO: only FAIL is "suspected blur" (118 frames, shots 20-22). Known false positive (per-shot Laplacian medians differ: bee-dense s23/24 raise the take median); frames are sharp.
- Known quirks: in shot 20 she is cropped large at the left edge and the V is small against her grey body; bee clouds are dense/clumpy at phone size; u4 hive overlaps her chest in the first frames.

## v3 (shots 20-21 only, g 1301-1452; shots 22-24 unchanged)
- Shot 20: continues team 6's inside-fence shot 19 (push point x 6.0, max bow t 0.11 at g 1307, 3 cm matte grey wire): opens on their wide framing, eases to a low oblique close on her chest + wire, holds ~12 frames (g 1307-1319), then slides left along the bent wire past hives that start to swing (u3/u4 at g ~1320, u2 ~1334). Elephant card night-graded like s23-24; roof undersides x0.62; trees, banana leaves, mountain and u3/u4 roofs removed; her card is hidden once her head leaves frame (no floating trunk).
- Shot 21: tracking cut-away along the row, 41 deg to it and ahead of the wave, hive swing seen side-on, ~16 frames hive to hive (u3 g ~1381, u2 ~1398, u1 ~1415, u0 ~1431), knock puff of bees at each; roofs removed, near-zero grass, orange lamp pools dimmed; hives x1.5; camera stops at the row end.
- qa_auto: only FAIL is the per-shot blur false positive (159 frames, shots 20-21 are low-detail wide frames). Handle frames 1301-1306 drift slightly (no frozen run).
- Known limits: the V is a faint kink in the wire (a bow toward camera cannot be drawn strongly without a high camera); sky in shot 20 is about 30-40 %; far hives in shot 21 are smaller than 120 px (only the 2 nearest are large at any time).

## v4 (shot 21 only, g 1368-1452; per the push re-check)
- No bees before g ~1442 (dormant entrance bees removed); small bee puffs from g ~1442 on at u1 then u0, leading into the shot-22 burst.
- Neighbouring hives swing out of step (alternating direction, hives x2.0) so they overlap/knock around g 1405-1445.
- Camera lower and pitched up: ground about 20 %; roofs and posts kept (undersides darkened), orange lamp pools dimmed.
- qa_auto: only the per-shot blur false positive remains. Shot 20 (g 1301-1367) is the v3 version and will not be used (reassigned to team 2); shots 22-24 unchanged.

## v5 (shot 21 only, g 1368-1452)
- Reframed: camera low (z 0.6), 50 mm, pitched up so the swinging hives sit in the middle band (y ~350-850); sky ~25-30 %, ground ~15 %.
- Knock: as the wave reaches each hive it swings hard and BANGS into its own post/frame: 2-frame jolt of hive, bar, posts and roofs plus a chip/dust spray crown (wood chips, dust specks, small wisps) at g 1388 (u3), 1405 (u2), 1422 (u1), 1438 (u0).
- Bees: none before g ~1442; small puffs at the last hives, then the shot-22 burst.
- qa_auto: only the per-shot blur false positive. Shot 20 (v3) is unused; 22-24 unchanged.

## v6 (shot 21 only, g 1368-1452)
- Knocks: the camera look point follows the hive being knocked (u3 g1388, u2 1405, u1 1422, u0 1438) so every hit lands mid-frame with its post in frame; 2-frame jolt (~0.065 m, ~12 px) of hive, bar, posts and roofs plus a 2-frame ~4 px camera shake; spray at all four, including u2.
- Dust: a spray crown (12 chips + 14 droplets thrown in a ~110 deg upward cone with speed and gravity, shards stretched along their motion, 2 thin wisps), fades over 8 frames; no solid backing cards.
- Night: world sky x0.4 strength (top RGB ~94/87/164 vs shot 22 ~96/90/204), stars boosted, tin roofs and undersides darkened, hut windows hidden and hut lamps dimmed at g1368-1380.
- Bees: none before g ~1442. qa_auto: only the per-shot blur false positive. Shot 20 (v3) unused; 22-24 unchanged.
- Known: stars are barely visible at this camera elevation; the first frame of each spray reads as a small tight clump.
