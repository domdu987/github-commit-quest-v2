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
