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
