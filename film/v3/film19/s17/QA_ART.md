# s17 QA-art

## Round 10 (director QA-art): PASS, 7.4

Take: take.mkv.partaa + partab joined to /tmp/s17a.mkv (first_g 1271, 122 frames, frame index = g - 1271). Frames are in /tmp/qa19_r10art/s17/f_NNN.png. Sheets: /tmp/qa19_r10art/s17_sheet.jpg (3 fps), s17_snap.jpg (every frame g 1365-1384), s17_phone.jpg (360x640: g 1285, 1320, 1360, 1383), full frames s17_g1361_full.png and s17_g1381_full.png. Stats: s17_stats.txt.

| Check | Status |
|---|---|
| Set | **Vivid open sea.** The turquoise sea has scattered whitecaps, a crisp three-masted ship with lit deck props and red pennants, and big toon clouds. The ship carries the shot. The sea is empty apart from the ship and a pale island near the horizon. |
| Light / colour | **Strong.** In-shot saturation 0.717 and luma 106.9 (G1 is met). The noon light gives crisp sail shadows on the water. The snap frames peak at a luma of 136 because the white wake fills the frame, which is fine as a moment. |
| Camera / composition | **The move works.** It starts behind and above the ship (g 1271-1311), orbits and pulls while the ship crosses the frame, and lands with a 15-frame **snap back** on "ยิ่งไกล" (g 1368-1383). The snap reveals the ship small at the upper left with a huge white wake fanning down the frame: a clear "farther and farther" payoff that reads at phone size. Weak spot: g 1331-1367 (~1.2 s, frame-diff ~2.2) is nearly parked, with the ship sitting in the lower-right corner. |
| Story | "Every hour of difference = 15 degrees farther" is carried by the narration only. Nothing in the picture reads as "home". The pale island sits ahead of or beside the ship, so it does not read as a home that is receding. |
| Artefacts | The sun-glint specular appears as soft white blobs left of the ship (g 1271-1330). The island is flat, pale and unshaded and looks like an ice slab. After the snap the wake is three wide bands, much wider than the ship; it is stylised and acceptable. |
| Grounding / G3 | No characters. Nothing floats. The ship's whole silhouette is in frame on every frame. |

| Criterion | Score |
|---|---|
| Set | 7 |
| Light & colour | 8.5 |
| Composition / phone | 7 |
| Acting | n/a (no cast; I.5 is not met in the literal sense, but the ship is the actor here) |
| Key moment (snap back on "ยิ่งไกล") | 7.5 |
| Match to refs (R5 aerial ship shots) | 7 |
| **Overall** | **7.4 - PASS** |

Polish (not blocking):
1. Keep the camera travelling through g 1331-1367: carry on the orbit or crane at about half speed rather than nearly parking before the snap.
2. Make the island read as **home**. Give it a green top, a tiny lighthouse or a flag, and place it behind the ship so that it shrinks in the frame. It could also carry a short in-world "HOME" or "ENGLAND" sign (I.4). Otherwise hide it.
3. Tame the glint blobs (glint x0.3 or tighter roughness) so that the left side of the frame does not look foggy.
4. The sails could be warmer (cream) to match s18.
