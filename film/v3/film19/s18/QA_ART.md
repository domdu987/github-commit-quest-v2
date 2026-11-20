# s18 QA-art

## Round 10 (director QA-art): FIX, 6.8

Take: take.mkv used as is (copied to /tmp/s18a.mkv; first_g 1375, 102 frames, frame index = g - 1375). Frames are in /tmp/qa19_r10art/s18/f_NNN.png. Sheets: /tmp/qa19_r10art/s18_sheet.jpg (3 fps), s18_snap.jpg (every frame g 1425-1444), s18_phone.jpg (360x640: g 1390, 1425, 1445, 1467), full frame s18_g1455_full.png. Stats: s18_stats.txt.

| Check | Status |
|---|---|
| Set | **A good hero ship.** The cream sails are fully set and the hull has gold stripes and a white bow wave. Bow-wave rings spread ahead, broken foam crests sweep across the foreground, and big shaded toon clouds fill the sky. There is layered depth (crests, a floating spar, the ship, clouds). |
| Light / colour | **Too bright for G1.** In-shot mean luma is **123.7**, against the 85-110 required by section G.1 (the take's own QA.md checks it against the old 70-135 range). Saturation is 0.535, which is fine. The sky fades to a pale grey-blue haze along the horizon, and the large foam areas at g 1405-1435 push the luma to about 132. |
| Camera / composition | A low hero angle near the water, with the whole ship in frame and slide, orbit and crane on it. A snap push x1.22 lands on "จาไมกา" (g 1428-1445) and reads well. It is close to straight-on and symmetric after the snap, but the low height keeps it heroic. |
| Key moment / story | **Missing the "Jamaica" and "his son carried it".** On "จาไมกา" the snap push only shows the same ship, a little bigger. There is no destination (island, palms, sign) and no sign of the son or the clock. On a phone this is a generic "ship sailing" shot. |
| Artefacts | Glint highlights are a little blobby. The floating spar reads correctly as flotsam. No floating or cut objects. |

| Criterion | Score |
|---|---|
| Set | 7.5 |
| Light & colour | 6 (G.1 luma fail) |
| Composition / phone | 7.5 |
| Acting | n/a (no cast) |
| Key moment ("across the sea to Jamaica") | 6 |
| Match to refs (R5 hero ship, but no signature sail colour) | 7 |
| **Overall** | **6.8 - FIX** |

Fixes:
1. **Luma into 85-110 (blocking, G.1).** Apply about -0.5 EV more, or deepen the sky gradient to a richer blue at the horizon, and thin the foreground foam lines by about 30 %. Target an in-shot mean of about 105.
2. **Sell "Jamaica" on the snap.**
   - A green palm island with a beach rises on the horizon behind or beside the ship as the snap lands (g ~1438).
   - Optionally add a short in-world sign or banner reading "JAMAICA" (I.4 allows it).
   - This gives the push a target.
3. (Recommended, I.5) Show the son. Put a small William card at the bow rail holding the clock box (H4 is in a box), visible after the snap at about 6-10 % of the frame height. This ties the shot to "his son carried it". It needs grounding on the deck and a rim light.
4. (Polish) Lower the glint (x0.2) so the bright blobs in the foreground do not dominate the bottom third.

## Round 11 (director QA-art): FIX, 6.9

Take: take.mkv as delivered (first_g 1375, 102 frames, frame index = g - 1375). Frames: /tmp/qa19_r11art/s18/f_NNN.png (f_001 = g 1375). Sheets: /tmp/qa19_r11art/s18_sheet3fps.jpg (every 10 f), s18_snap.jpg (g 1426-1446 every 2 f), s18_phone.jpg (phone size 360x640: g 1390, 1420, 1438, 1450, 1467). Full frame: s18_g1438_full.png. Crops: s18_g1455_crop.png (son), s18_g1395_horizon.png (island).

Stats (Rec.601 luma, PIL HSV saturation, in-shot g 1384-1467):
- Mean luma **94.4** (min 85.1, max 103.2). The team reports 100.7 with its own meter; either way it is inside the G.1 band of 85-110. The handles reach 104 at g 1471.
- Saturation 0.654.
- Clipped pixels (>250) 0.1-0.7 %.

| Check | Status |
|---|---|
| Set | Same strong hero ship. The R10 haze is fixed: the horizon is now a deep blue sky going into teal water. Foam crests and the spar give foreground depth. **New artefact:** the bow wave is a glossy, glowing blue-white tube at the stem (clearest at g 1438-1476). It reads as a plastic object, not spray. |
| Light / colour | **Passes G.1 / I.3.** Luma is 94 and saturation 0.65, with clear blue sky and water and no haze. The glint is smaller but there are still two hot white blobs in the lower third at g 1395-1405 and g 1460-1476. They are acceptable but distracting. Warm sails against a cool sea give good warm/cool contrast. |
| Camera / composition | The whole ship is in frame, with slide, orbit and crane, and the snap x1.22 on "จาไมกา". The ship is centred and straight-on after the snap, and the second move keeps it alive. Fine, but not an interesting angle. |
| Son / acting (phone) | **william19 reads on a phone** as a figure on the forecastle: tricorn hat, blue coat, smiling, standing on the deck with feet on the planking (no float). At 360x640 he is about 50 px tall with a face of about 15 px. The **watch is about 4 px on a phone**, a grey dot, so "he holds the clock" does not read. The pose is the same smiling card through the whole shot, with no gesture change on "จาไมกา" (I.5 asks for acting). |
| Key moment ("across the sea to Jamaica") | **Half there.** "His son carried it across the sea" now reads. **"Jamaica" still does not.** The "island" is a pale grey-blue mound with no palms and no beach, on the right horizon at g 1375-1432. The snap on "จาไมกา" pushes and pans *away* from it, so it is out of frame from g 1434 on. The word lands on open sea again. |
| Nothing floats / G.2 | OK on every tile. The spar rides on the water, and the son stands on the deck. |

| Criterion | Score |
|---|---|
| Set | 7.5 (bow-wave tube artefact) |
| Light & colour | 7.5 (G.1 pass) |
| Composition / phone | 7 |
| Acting | 6.5 (static card, watch unreadable) |
| Key moment | 6 (Jamaica missing on the snap) |
| Match to refs (R5) | 7 |
| **Overall** | **6.9 - FIX** (close; one targeted re-render) |

Fixes, in priority order:
1. **(Blocking) Make the snap land on Jamaica.**
   - Turn the island into a green palm island: a saturated green mound, a yellow sand rim and 3-5 palm silhouettes, about 8-12 % of the frame width.
   - Place it so the snap pan on "จาไมกา" (g 1428-1445) moves *toward* it. It should end in frame at upper-left or upper-right of the ship, beside the bow, not behind the sails.
   - Optional (I.4): a small "JAMAICA" banner or flag on a pole on the beach.
   - It must stay visible until the dissolve to s19 (ship_coast), so the two shots link.
2. **Make the watch read.**
   - Scale the H4 in his hand by about 2x, or add a warm rim/glint on it at the snap (one sparkle at g ~1438).
   - Have him lift it toward the island on "จาไมกา" (a hand raise, plus an excited mouth or eyes swap) so he is acting (I.5).
3. **Bow wave.** Replace the glossy glowing tube with a matte white foam or spray toon shape, or cut its emission/specular by about 70 %.
4. (Polish) Reduce the two remaining lower-third glint blobs by another x0.5, or move them under the foam.

## Round 12 (director QA-art): FIX, 6.9

Take: take.mkv as delivered (first_g 1375, 102 frames, frame index = g - 1375). Frames: /tmp/qa19_r12art/s18/f_NNN.png (f_000 = g 1375, every frame). Sheets: /tmp/qa19_r12art/s18_sheet3fps.jpg (every 10 f), s18_snap.jpg (every frame g 1425-1450), s18_phone.jpg (360x640: g 1390, 1420, 1438, 1450, 1467), s18_william.jpg (son crops g 1390-1467), s18_g1438_island_bow.png (crop), s18_g1438_phone.png.

Stats (Rec.601 luma, PIL HSV saturation, in-shot g 1384-1467):
- Mean luma **94.2** (min 83.8 at g 1384-1400, max 105.0 at g 1464). The shot mean passes G.1. The opening ~17 frames sit just under 85, which is marginal but not blocking.
- Saturation **0.654** (passes G.1 and I.3).

| Check | Status |
|---|---|
| Island / "Jamaica" | **Improved, but still weak on a phone.** There is now a green dome with a sand rim and 5 palms. It is hidden behind the hull until about g 1430, then the snap brings it into frame at left of the jib, where it stays until the dissolve. That is correct. At full size it is about 90-110 px (13-15 % of width) and reads as "tropical island". At phone size it is about 40 px wide on the horizon line and the palms are 1-2 px specks. It reads as "a green bump", not a destination. There is no sign. **Story logic:** the ship sails TOWARD the camera, and the island is BEHIND it, so the shot reads as the ship *leaving* the island, not arriving at Jamaica. |
| Son / watch | **The watch now reads at full size**: a clear white pocket-watch face, about 25 px. On a phone it is about 6 px, a white dot next to his hip. William reads on a phone (about 40 px tall, hat, blue coat, deck contact OK, no float). |
| Acting | There is some change: a closed-eye smile early (looking down), then round eyes from g 1430 and a small hop. **The "raise toward the island" does not read.** The H4 stays at his right hip/waist (screen-right) through g 1430-1467, while the island is screen-left. There is no arm lift above the shoulder and no point. At most it is a 15-20 px rise. The face goes neutral/flat-mouth at the key word (g 1438-1446), not excited. |
| Foam | **Not fixed.** The bow wave is now matte, so the gloss is gone. But it is still a smooth, solid, shaded white/lavender pillow or tube under the stem, with a hard silhouette. It grows to about 35 % of the frame width by g 1467 and still reads as a plastic cushion, not spray. The crest lines and wake rings are good. Glint blobs are gone. The foreground foam at g 1415-1432 is a busy, noisy white mass across the lower third. It is acceptable, but it pulls the eye. |
| Colour | Vivid. Deep blue sky, teal sea, warm sails, green island. Warm/cool contrast is OK. |
| Composition / camera | There is more motion (slide, orbit, crane), the snap lands at g 1438-1445, and a second move follows. The ship is still centred and close to straight-on throughout (H.2 prefers a non-default angle). Nothing is cut by a frame edge, and nothing floats on any tile. |

| Criterion | Score |
|---|---|
| Set | 7 (bow-wave pillow persists) |
| Light & colour | 7.5 |
| Composition / phone | 7 |
| Acting | 6.5 (no legible raise or point toward the island) |
| Key moment ("across the sea to Jamaica") | 6.5 (island present on the word but tiny on a phone; ship sails away from it) |
| Match to refs (R5) | 7 |
| **Overall** | **6.9 - FIX** (real progress; the remaining issues are targeted) |

Fixes, in priority order:
1. **(Blocking) Make the ship go TO the island, and make the island big on the word.**
   - Option A (preferred): use a 3/4-rear or side-tracking camera, so the ship sails away from the camera toward the island. The snap on "จาไมกา" pushes past the stern and frames the island beside the bow.
   - Option B: keep this camera, but put the island in FRONT of the ship's course (screen-left foreground-mid, nearer), so the ship is clearly heading for it.
   - Either way, the island is at least 20-25 % of the frame width at g 1440-1467, with palms 6+ px thick at phone size.
   - Optional (I.4): a "JAMAICA" banner or flag on the beach.
2. **William's gesture.** At g 1430-1440, raise the H4 above head height on the island side (screen-left arm). Swap the face to open-mouth excitement and hold for 0.5 s or more. Add one warm sparkle on the watch at g ~1438 so it reads as more than 6 px on a phone.
3. **Bow wave.** Replace the solid tube mesh with broken toon spray: 3-6 separate white chunks or a particle spray with an alpha edge. Do not just re-shade it. Alternatively, cap its size at about 15 % of the frame width.
4. (Polish) Lift the first 17 frames by about +0.1 EV (luma 84 → 87). Thin the lower-third foam mass at g 1415-1432 by about 30 %.

## Round 13 (director QA-art): PASS, 7.3 (v2 is better than round 12's 6.9)

Take: take.mkv v2 (first_g 1375, 102 frames, frame index = g - 1375). Frames: /tmp/qa19_r13art/s18/gNNNN.png (every frame, named by g). Sheets: /tmp/qa19_r13art/s18_sheet3fps.jpg (every 10 f), s18_snapA.jpg / s18_snapB.jpg (every frame g 1425-1476), s18_phone.jpg (360x640: g 1385, 1400, 1415, 1430, 1438, 1445, 1455, 1467), s18_william.jpg (son crops), s18_watch_1440_1455.jpg (every frame), s18_g1445_island_bow.png, s18_g1445_phone.png.

Stats (Rec.601 luma, (max-min)/max saturation, in-shot g 1384-1467):
- Mean luma **92.2** (min 83.4 around g 1399, max 100.1). Passes G.1.
- The opening frames are 85.7 falling to 83.4 over g 1384-1400. The +0.1 EV did not get them to 87, but this is not blocking.
- Saturation **0.668**. Passes G.1 and I.3.

| Check | Status |
|---|---|
| Island / "Jamaica" | **Fixed in size.** A green twin-hump island with a sand rim and 5 palms is on screen-left from g ~1400 to the dissolve. At g 1440-1467 it is about 30-36 % of the frame width (260 px at 720). On the phone it is about 100 px wide, and the palms read as palms. It is the clear second subject and the obvious destination, and it hands off well to the s19 beach. **Remaining weakness:** it still sits on the horizon line beside or behind the ship. The ship comes toward the camera rather than turning toward it, so the "heading TO" reading comes mainly from William's gesture, not the ship's course. There is no JAMAICA sign (I.4, optional). |
| Son / watch | **Lands.** From g 1427 the arm goes straight up on the island side (screen-left). The H4 is held above his hat from g ~1436 to the end. A 4-point white sparkle shows at g 1436-1450, and after that the clock face is legible at full size (about 20 px). His face changes to open-mouth excitement with round eyes and a red mouth, and he hops. Hand and watch stay attached on every frame, and the watch stays on the same side, with no jump. On the phone his arm reads as raised with a bright point at its tip, and the read is "showing something, excited". The pose is a stiff single-card arm, but it reads. |
| Bow wave | **Mostly fixed.** It is smaller and no longer a dominant pillow. It is now a thin white skirt plus crest rings. A **lavender/purple underglow** remains at the stem waterline (g 1430-1467), visible on the phone as a violet smudge left of the bow. This is polish only. |
| Lower-third foam | This was not thinned. At g 1415-1432 a large noisy white foam mass fills the bottom third and briefly competes with the ship on the phone. It clears by g 1438, so the key word is clean. |
| Colour / light | Vivid deep-blue sky and teal sea, warm sails, green island: on-brand and the same as round 12. NOON key with a warm/cool split. |
| Composition / camera | There is now a 3/4 front-right angle with a push, orbit and snap. The snap on "จาไมกา" lands at g 1438-1446 with the island and William both in frame. The ship is still roughly centred. Nothing is cut by a frame edge. **Nothing floats on any 0.5 s tile**: the son stands on the deck, and the spar from g 1385-1405 rides on the water. |

| Criterion | Score |
|---|---|
| Set | 7.5 (big island adds a destination; bow underglow and foam mass remain) |
| Light & colour | 7.5 |
| Composition / phone | 7 |
| Acting | 7.5 (raise, excited face, hop and sparkle all read on the phone) |
| Key moment ("across the sea to Jamaica") | 7 (island big on the word and the son presents the watch to it; the ship's course still does not point at it) |
| Match to refs (R5) | 7 |
| **Overall** | **7.3 - PASS** |

**Verdict vs round 12: v2 is clearly better (7.3 vs 6.9).** All three blocking notes from round 12 are addressed: island size, William's raise and reaction, and bow-wave size. On a phone, the shot now tells "his son carried it across the sea to Jamaica".

Optional polish (not blocking):
1. Kill the violet emission or underglow at the bow stem.
2. Thin the lower-third foam at g 1415-1432 by about 30 %.
3. Yaw the ship about 10-15 deg toward the island, or add a small "JAMAICA" flag or banner on the beach, so the ship's course also points at the destination.
4. Lift g 1384-1400 by another +0.1 EV.
