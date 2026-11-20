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
