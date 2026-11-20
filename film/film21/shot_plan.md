# Shot plan v3, film 21 (ไอ้ชาวนาบนเนิน, Battle of Stirling Bridge, 11 Sept 1297): CAMERA TRAVEL (QA_TEAM.md §I)
Replaces the cut-based plan v2 (kept as shot_plan_v2_cuts.md) after the client's decision of 2026-11-20 to match his reference Shorts:
"ได้ทุก ทำอะไรก็ได้ที่ออกมาเหมือนคลิปที่ผมส่งให้". Study film/ref_shorts/ first, especially R5_sheet.jpg (storm oil), R3_transition_detail.jpg
(the camera follows a character through the set) and R7 (ride-along).

Narration film/film21/audio/narration.wav (61.25 s), placed at +0.10 s. g = round((t_narr + 0.10) * 30). **N = 1848**: the film ends on a hard cut on the last "ตูม".
Captions film/film21/script/captions.json (narration time). Set film/v3/set3d21 (API.md, including the new `build_world` and `cam_path` for travel). Cast film/v3/cast21.

## The idea in one line
One connected Forth valley. The camera FLIES: it swoops from the sky to the Scots on Abbey Craig, crosses the river to the English camp, rides the narrow bridge,
follows Cressingham to the bank, cranes over the river to the hill, rides down with the charge, rises to show the trap, swoops back to the shocked treasurer,
and ends in the river splash.
- Hard cuts: 8, the target of §I being 4-10. Most other joins are continuous travel: the segments meet at the same camera pose and are joined with a 6-frame dissolve (D6).
- Two joins are whip pans (W): D1->D2 and J1->J2.
- BIGZOOMs (§H): segment A and segment H2b.

## Signature colour (§I 3)
English CRIMSON and GOLD (surcoats, pavilions, banners, the treasury) against Scots SALTIRE BLUE (blue banners with a white saltire on the hill and at the spear wall), on the teal river. Keep both in most frames.

## Render budget (QA-art)
Travel frames render at 32 samples (+ OIDN); close-ups and held frames at 64. Before finals, each team renders a 10 fps draft of its whole camera path (360x640) and pushes it as path_draft.mp4.

## Rules for every segment (§G, §H, §I, camera rhythm)
- **One continuous, eased camera move** with no internal cut, unless the table says so. Never parked: the camera always travels (push, crane, track, ride along). Pass THROUGH set detail (pine branches, banner cloth, tent ropes, reeds) for parallax.
- **Lighting (§I 2):**
  - A motivated key: the low morning sun, light shafts through the pines and through campfire smoke, and a lantern under the money canopy.
  - Warm sun and cool shade in the same frame.
  - A **rim light on every character card**: puppet `rim` (cast API; warm-gold rim on the sun side).
- **Colour (§G/§I):** frame saturation >= 0.50 and vivid % >= 45, luma 85-110. The VIVID grade does it (API §9). On travel, `cam_path` eases the VIVID entry between presets.
- **Text signs (§I 4)**, built into the set: "STIRLING BRIDGE" (bridge, south end), "KING'S TREASURY" (the coin chest), "ENGLISH CAMP" (camp entrance). Let the camera pass them where the table says.
- **Characters always act (§I 5):**
  - Nobody stands still for more than 1.5 s. Use walk cycles, the horses' walk, laughing bounce (0.06 D at 3 Hz), spear shifts, scratching, chewing, counting coins, and the horn.
  - Riders stay on their horses. Feet stay on the ground with contact shadows (§G). Nobody is cut in half by the frame edge.
- **Close-ups (§I 6):** at most 3 fast pushes into a face, about 1 s each. These are marked CU1-CU3. Everything else is wide or medium inside the rich set; no face is over 35 % of the frame height except at CU1-CU3.
- **Content:** comic and BLOODLESS.
  - Spears block and point; nobody is struck, lies still or dies.
  - Cressingham appears ONLY on the south bank.
  - At the ending, only his EMPTY money table is shown.
- **Mouths:**
  - Cressingham's mouth moves ONLY at narration 21.29-26.26 and 36.32-37.89 (±0.15 s).
  - He laughs (laugh drawing and bounce, no lip-sync) at 20.29-21.29.
  - The camp laughs at 34.71-36.32.
  - Nobody else talks. The horn blower's cheeks puff at 39.7-41.1.
- **Handles:**
  - Every segment renders 3 extra frames past each end that joins by D6. These must be the continuation of the same move, so the dissolve blends the same camera path.
  - Segments joined by a cut or a whip need no handles.

## Join poses (shared camera poses where two segments meet; segment ends and starts EXACTLY here)
| pose | camera loc -> look, lens | used at |
|---|---|---|
| P_CAMP | the `camp_wide` preset camera | B1 end / B2 start (g 298) |
| P_HILL | the `hill_low` preset camera, raised 0.8 m | B2 end (g 418, then cut) |
| P_BANK | the `camp_bank` preset camera | D2 end (CU1 pushes out of it) / E1 start |
| P_NECK | the QA-art bridge_end_north camera (-2.0, 50.0, 4.6) -> (0.0, 22.0, 1.8), 22 mm | H1 end / H2a start (g 1345) |
| P_TOP | (-10, -115, 115) -> (0, 70, 0), 22 mm (v2 after the H2a gate: from the south looking north; loop, bridge mouth AND the south-bank camp in frame; VIVID['P_TOP'] = (1.4, 1.1, 0.75)) | H2a end / H2b start (g 1392) |
| P_A | (290, 205, 170) -> (120, 110, 10), 22 mm (mid-swoop of BIGZOOM 1, NE of Abbey Craig, looking SW-down at the hill and the bridge) | A1 end / A2 start (g 80) |
If a team cannot hit a pose exactly, it writes its actual first or last camera into meta.json (`cam_in` / `cam_out`) and the director re-checks the join.

## Segments (t = NARRATION time)
| seg | t0-t1 | g0-g1 | join in | world (build_world presets) | what happens (camera + action) |
|---|---|---|---|---|---|
| A | 0.00-5.19 | 0-159 | - (film start) | valley_wide, hill_over | **BIGZOOM 1, the hook.** See the detail under the table. |
| (A split) | | g80 | D6 at P_A | | A1 = g0-80 (team 1), A2 = g80-159 (team 5); they join by D6 at P_A (table below). |
| B1 | 5.19-9.82 | 159-298 | CUT 1 | valley_wide, camp_wide | "คืออย่างนี้นะ สกอตแลนด์ เจ็ดร้อยกว่าปีก่อน": high over the valley, the camera glides south over the river and swoops DOWN into the English camp. It flies past the "ENGLISH CAMP" sign, banners fluttering and fire smoke with light shafts, and lands at P_CAMP as knights on caparisoned horses parade ("อัศวินม้าเกราะเต็มทุ่ง", 7.74). |
| B2 | 9.82-13.82 | 298-418 | D6 at P_CAMP | camp_wide, hill_low | "ส่วนฝั่งสกอต...": from the parade the camera CRANES UP over the pavilions, flies north across the river (glitter, the bridge at the left), and climbs Abbey Craig. It lands LOW looking up at the Scots spearmen on foot against the sky (low hero angle, light shafts through the pines). They shift their spears; one leans on his. |
| C | 13.82-17.97 | 418-542 | CUT 2 | bridge_high, bridge_end_south | "ระหว่างกลาง มีสะพานไม้แคบ ๆ อยู่สะพานเดียว": high above the bridge, the camera flies along it (the only crossing), then DESCENDS to the south end past the "STIRLING BRIDGE" sign. It rides behind two knights whose horses fill the deck side by side; their knees brush the rails and one knight sucks his belly in on "ม้าสองตัวก็เต็มแล้ว" (16.52-17.97). |
| D1 | 17.97-21.29 | 542-642 | CUT 3 | camp_table | Under the money canopy (warm lantern, "KING'S TREASURY" chest), Cressingham counts coins into the chest (coin clink). The camera arcs around the table. He looks up across the river and bursts out LAUGHING at "หัวเราะลั่นว่า" (20.29): bounce, belly shakes. At the end the camera whips right (W, 6 frames). |
| D2 | 21.29-26.32 | 642-793 | W | camp_bank | Whip in (6 frames), then the camera FOLLOWS Cressingham (side tracking) as he waddles to the bank, pointing across the river at the tiny Scots on the hill. Lip-sync: "ชาวนาบนเนินไม่กี่คน! อ้อมไปเปลืองเงินหลวง ข้ามสะพานนี่แหละ...". Surrey follows behind, tired. **CU1**: on "เร็วดี ประหยัดดี!" (25.11-26.26) a fast push into Cressingham's face as he slaps his purse, then the camera eases back out to P_BANK by g 793. |
| E1 | 26.32-29.39 | 793-885 | D6 at P_BANK | camp_bank, hill_eye | "ทั้งค่ายเลยเรียก...": from the bank, laughing soldiers point across, and one mimes hoeing (bounce). The camera RISES and flies across the river and up the hill. On "พวกไอ้ชาวนาบนเนิน" (27.80) it lands with a SNAP punch-in (6 frames of speed lines, 2-frame shake) on the Scots line: unbothered, Wallace raises an eyebrow. |
| E2 | 29.39-34.71 | 885-1044 | CUT 4 | bridge_end_north, valley_loop | The count, as RIDE-ALONG plus crane: at the north end of the bridge the camera rides just behind the first English footmen stepping off ("ข้ามมาสิบคน", 29.39). They glance up at the hill nervously ("บนเนินเงียบ"). The camera rises as more pour over ("ร้อยคน", 31.17; still silent) and on "เป็นพัน" (32.75) CRANES UP to only 35-45 m, angled back toward the hill (NOT straight up over the loop: that image belongs to the reveal): the meadow fills with hundreds of troops (place_troops meadow), and the Scots on the hill have not moved. |
| F | 34.71-37.94 | 1044-1141 | CUT 5 | camp_bank | FALSE PAYOFF. On the south bank the waiting English laugh and point across, bouncing out of phase; the camera tracks along them. **CU2**: Cressingham, thumbs in his belt, "เห็นไหม กลัวจนขยับไม่ได้!" (36.32-37.89, lip-sync), a fast push into his smug face. |
| G | 37.94-41.19 | 1141-1239 | CUT 6 | hill_over, hill_low | Calm before, then the horn (merged G1+G2: cause before effect). We open BEHIND the Scots on the hill (the hill_over pose, their backs and spear tips in the foreground) looking down at the calm column still crossing the bridge two by two, about half the army over. A knight on the causeway yawns, tiny but readable. The camera ARCS down and around to the LOW hero angle (hill_low) against the sky and pine light shafts. On "เสียงแตร" (39.69) a Scot raises a long cow horn and BLOWS (cheeks puff); Wallace lifts his sword arm. Snap push (14 frames, x1.5) with a 2-frame shake. |
| H1 | 41.19-44.73 | 1239-1345 | CUT 7 | hill_over, bridge_end_north | The CHARGE as a ride-along. The camera rides behind 4-5 running Scots (spears forward, gorse whipping past in the foreground, 5 Hz shake decaying) for about 1.2 s, then OVERTAKES them and swoops down to the bridge mouth (about 195 m: no runner can keep up). There a second, pre-placed group of Scots (blue saltire banner) SLAMS the spear wall across the north end on "ปิดหัวสะพาน" (43.78). The English jump back and their helmets wobble. It ends at P_NECK. |
| H2a | 44.73-46.30 | 1345-1392 | D6 at P_NECK | bridge_end_north, valley_loop | From P_NECK the camera CRANES straight UP fast (about 1 s) to P_TOP and holds-drifts: the bottle-and-cork image (the English boxed inside the loop in crimson, the Scots spear wall plugging the bridge mouth with BLUE saltire banners, the other half on the south bank), "ครึ่งทัพที่ข้ามมาแล้ว ถอยไม่ได้ ติดอยู่ริมน้ำ". Ends at P_TOP (+3 handle frames continuing the drift). |
| H2b | 46.30-50.53 | 1392-1519 | D6 at P_TOP | valley_loop, camp_bank | **BIGZOOM 2 (wide to medium in about 3.3 s):** from P_TOP the camera SWOOPS across the river, past banners and tents, down to a MEDIUM shot of Cressingham and Surrey on the bank watching helplessly. Their jaws drop (shocked swap behind a blink, sweat drop) and soldiers stand on tiptoe ("อีกครึ่ง ข้ามมาช่วยไม่ได้ ได้แต่ยืนดู"). **CU3**: a 1 s push into Cressingham's shocked face on "อยู่อีกฝั่ง" (49.73). |
| I | 50.53-54.55 | 1519-1640 | CUT 8 | bridge_deck, bridge_high | AHA, as a ride-along on the jammed bridge: the column tries to turn back, two horses wedged nose to tail, and a knight's helmet pops off. The camera rides the deck, then CRANES UP to look straight down the bridge: two-by-two all along, nobody moving. Snap pull-out on "เหมือนกัน" (53.5). |
| J1 | 54.55-56.88 | 1640-1709 | CUT 9 | camp_table | ENDING: Cressingham's EMPTY money table (stool with his cloak, the "KING'S TREASURY" chest, the lantern). The camera pushes in. The coin scale TIPS on "เร็วดี" (55.80) and the chest lid SLAMS on "ประหยัดดี" (56.22). Then a whip left (W). |
| J2 | 56.88-61.50 | 1709-1848 | W | riverbank, river_low | Whip in to the north bank inside the loop. The English look at the blocked bridge, then the water, then each other; one pinches his nose ("ขากลับไม่ต้องใช้สะพานสักนิด"). They JUMP (59.0-59.8): cards lifted 0.5-0.8 D, `splash()` crowns, swim cards bob up spluttering, helmets float. The camera DROPS to water level (river_low) and pushes in: "ตูม ตูม ตูม" with 3 big crowns at 60.6, 60.9 and 61.2. HARD CUT on the last one (g 1848). |

**Segment A, BIGZOOM 1 (the hook).** The film opens already moving, EXTREME WIDE and high over the Forth valley.
- In shot: the river loop, the narrow bridge with English knights crossing two by two (place_troops bridge), the camp and Abbey Craig. The Scots are tiny (under 5 % of the frame height) on the slope.
- One eased swoop down: past pine branches and through a light shaft on the crag, to a MEDIUM shot of the Scots line on the shelf. Wallace is in the centre with arms folded on his spear, and the bridge is still visible far below behind them (at g 125).
- Then a quick push (15 frames, x1.4) onto the Scot chewing a grass stalk, on "อะไรเลยสักอย่าง".
- The others shift their weight but nobody moves forward.

Hard cuts: 8 (G1+G2 merged) plus 2 whips (D1->D2, J1->J2). The E1 punch-in and CU pushes are camera moves, not cuts. BIGZOOMs: A (g 0-125) and H2b (g 1392-1519, wide to medium 3.3 s).
Angle types: bird's-eye/high (A, B1, C, E2, H2, I), low hero (B2, G), over-the-shoulder/ride-along (C, E2, H1, I), through a foreground frame (B1 banners, D2 tent ropes, H1 gorse), side tracking (D2, F), crane up/down (B2, E1, E2, H2, I).

## Sound cues (conform; levels per captions-sound.md, music m1 at -31 dB)
See conform21.py: hooves on planks (A, C, G, I), coin clink (D1), crowd laughs (E1, F), river bed (E2, J2), horn (G), charge (H1), spear wall (H1 43.78), sting (44.42), whooshes on the whips and swoops, wood creak (I), chest slam (J1), splashes (J2).
