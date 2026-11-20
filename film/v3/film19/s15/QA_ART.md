# QA-art, TAKE gate: s15 (SHIP ship_deck NOON, "the sun is overhead"): FIX-FIRST, 6.0

Frames checked (take index): 12, 40, 70, 86, 92, 102 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey/s15_*.png

| Criterion | Score |
|---|---|
| Set density / ornament | 8 |
| Lighting & colour | 8 |
| Composition / phone legibility | 6 |
| Acting (aims at the sun) | 4 |
| Key moment ("the sun is right overhead") | 4 |
| Match to refs / client taste | 7 |
| **Overall** | **6.0** |

## What works
- The deck is sunlit, with sails, shrouds, sea, and a cloud. It is sharp and wide at the start. The big sail shadow sweeping off the deck as set_sun_overhead runs is a real 3D cue, and it is the best thing in the shot.

## Why FIX-FIRST
1. **There is no sun in any frame.** The mechanism is "noon, sun straight overhead", but the only evidence is a shadow that leaves, and a phone viewer reads that as a lighting change. Nobody is looking at a sun.
2. **Nobody looks up.** William holds the quadrant beside his hat, but his eyes and head face the lens with a scowl, so he reads as "angry man saluting". The captain also faces the lens, and his pitch -0.35 is not visible. The gaze (0.5, -0.9) does not come across as "up" on these faces.
3. On "อยู่ตรงหัว" the snap goes to a medium of William. His head is cut by the left edge in the last in-shot frames (take index ~100-103) and the quadrant is cut at the top.

## Fixes (shot.py)
1. Put the sun in frame. After the snap (g 1172-1189), tilt up: snap shift (0.8, 0.0) to (0.4, +0.45) with k 1.5 and rise_px 15 to 40, so a sky band with a hot sun disc sits at the top of frame and William's head stays at about y 500-650. If set3d19 has no visible sun disc, add a shot.py dressing: an emissive disc (warm white, strength about 20) on the ship_root up-axis about 40 D above William, plus a soft glow card. Show it only at frame top and keep no text.
2. William's pose: pitch -0.45, head_roll 10, gaze (0.3, -1.0), expression "squint" or "determined". Arm the quadrant vertically: angle about -85 instead of -62, hand y 0.25 on the thrust, so it points UP and not sideways.
3. Captain: pitch -0.5, yaw toward William (0.0), and a hand shading his eyes (arm_l hand (-0.15, 0.95), layer front). Two faces turned up then make the beat.
4. Keep William's head inside x 40-680 through g 1189. Cut slide_px from 40 to 20, or end the arc at the snap.
