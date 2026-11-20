# QA-art, TAKE gate: s16 (SHIP ship_deck NOON, "but the watch still shows home time"): FIX-FIRST, 5.5

Frames checked (take index): 12, 30, 45, 55, 75, 97 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey/s16_*.png

| Criterion | Score |
|---|---|
| Set density / ornament | 7 |
| Lighting & colour | 7 |
| Composition / phone legibility | 5 |
| Acting (proud, watch out) | 6 |
| Key moment (the watch = home time) | 4 |
| Match to refs / client taste | 5 |
| **Overall** | **5.5** |

## Why FIX-FIRST
1. **The watch is not the subject.** The plan says "push to the watch", but the push lands on William's face (head about 300 px, then 900+ px in the handle). The H4 is about 70 px at 720 and about 35 px on a phone, held off at the right edge beside the bulwark. The dial cannot be read, so "home time" does not come across. Most of the shot is a big smiling face, which is the extreme close-up the client does not want.
2. **Continuity with s15 breaks.** s15 ends with the sail shadow gone (sun at zenith). s16 opens (take index 9-40) with the huge diagonal sail shadow across the deck again. The shadow comes from this camera seeing the near sail's shadow, but to a viewer the sun has dropped again in the very shot that says it is noon.
3. The captain "looks on" only as a small figure for 1.3 s, then leaves.

## Fixes (shot.py)
1. Make the watch the hero. Set William's prop_r to dict(type="h4_watch", scale=2.0). Hold the arm toward the lens and centred: arm_r hand=(0.35, 0.78), stretch 1.3, layer front, yaw toward the lens 0.0. Watch on the palm at face height, just below the chin.
2. Camera: snap k 2.3 to 1.5, aimed at the watch (shift (0.1, -0.15)), not the face. Over g 1218-1279 the watch should be 150-200 px wide at about y 650-760, with William's face above it and some deck and sails around it. Reduce push from 0.10 to 0.06 so the shot ends as a medium, not a face close-up.
3. Home time: set the watch hands to a clearly non-noon hour, such as about 5 o'clock (London afternoon), via hands_t on the h4_watch body. The sun is overhead (12) while the watch says 5, so the gap is visible in one image.
4. Shadow continuity: start CAM_LOC0 where the near sail's shadow is out of frame, or hide or trim the sail shadow on the deck for this shot (sail objects' visible_shadow off for the near course). The deck should look as it does in the last frames of s15.
5. Captain: keep him in frame to about g 1240 (lower slide_px, from 45 to 15) and turn his head down to the watch (gaze (0.9, 0.4), pitch 0.2).

---
## Round 2 (TAKE gate, key takes, re-render): PASS, 6.5

Frames checked (take index): 9, 30, 50, 70, 90, 105 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey6/s16_*.png

| Criterion | R1 | R2 |
|---|---|---|
| Set density / ornament | 7 | 7 |
| Lighting & colour | 7 | 7 |
| Composition / phone legibility | 5 | 6 |
| Acting (proud, watch out) | 6 | 6.5 |
| Key moment (the watch = home time) | 4 | 6.5 |
| Match to refs / client taste | 5 | 6.5 |
| **Overall** | **5.5** | **6.5** |

## Earlier fixes
1. The watch is the hero: **PARTLY FIXED.** The H4 is now a clear white dial with chain bow, about 100-115 px at 720 (about 55 px at 360x640), at chest/shoulder height beside William's smiling face. It reads as "a watch" on a phone. It is still at the right of frame rather than centred, and below the 150-200 px target.
2. The push ends on the watch, not a face close-up: **FIXED.** The shot ends as a two-shot medium, with no extreme close-up.
3. Home time on the dial: **FIXED.** The hands sit at about ten past ten / two o'clock, clearly not noon, and they read at 360x640. Coming right after the s15 sun, the gap reads.
4. Shadow continuity with s15: **FIXED in effect.** s15 now ends with the same diagonal deck shadow at the lower left that s16 opens with, so the cut matches.
5. The captain stays and looks at the watch: **FIXED for presence / OPEN for the look.** He stays in frame all shot, but the push brings him nearest the lens. From f 50 on he is the biggest figure (left half, unimpressed face), he is cut by the left edge from about f 90, and his eyes do not visibly go to the watch.

## Polish notes (not blocking)
- The captain now takes the frame from William and the watch. Move CAP_OFF back about 0.6 D (or slide the camera right about 0.4 D) so William plus the watch are the larger pair, and the captain stays inside x 40.
- A watch scale of about 1.4x would make the dial unmistakable on a phone.
