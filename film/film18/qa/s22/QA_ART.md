# QA-art round 18 s22: FIX-FIRST
Shot: REVEAL close-medium, "หางลุกเป็นไฟ เขาติดมีดวาววับ" (g 1683-1742). Per the round-14 director decision, this is a pure ox hero shot with no soldier. I extracted all 71 frames (g = 1677 + n). I judged:
- a 180x320 phone sheet every 5th frame
- full size at g 1683/1706-1708/1735/1741
- mouth crops with guides at y 840/860/880
- a per-frame strip of the bottom-left props (g 1677-1747)

Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa18r/ (s22_phone.jpg, s22_bot.jpg, s22_pop.png, s22_full.png, s22_mouth.png).

## Director's decision
- **No soldier: DONE.** It is a pure close-medium of the hero ox. The dragon silk (red coat, gold dragon), rage face, gold horn blades and blue moon rim all read.
- **"Tail ablaze": reads.** The flame grows from the lit reed bundle on the tail tip, behind and to the right of the rump. It stays in frame, close to the right edge at the end.
- **"Blades glinting": reads.** A clean 4-point star sits on the blade at g 1732-1739.
- **Mouth:** the chin outline is ≤ about 855 on every checked frame (worst g 1737). No face is in the caption band.
- **Poles, fire on heads, half-cut:** none. The herd behind the hero is cut only at the frame edges, and none of those oxen is the main character.

## Blocker: single-frame prop pops (glitch)
The foreground jar and reed bundle (bottom-left) jump to a different, smaller and higher position for ONE frame at **g 1694, g 1707 and g 1719** (and at g 1677, which is in the handle). The ox and the set are unchanged on those frames, so only the dressing props pop. At 30 fps this is a visible flicker of the biggest object in the lower frame, three times in two seconds. The likely cause is stale prop transforms at render-chunk boundaries.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 7 | 7 | 7 |

## Verdict: FIX-FIRST (1 narrow blocker, 3 frames)
1. Re-render g 1694, 1707 and 1719 with the props at their neighbour positions, and also g 1677 if the handle may be used.
   - **Pass check:** on a per-frame strip of the bottom-left (x 0-720, y 840-1280) for g 1683-1742, the jar and bundle move smoothly with the camera, with no one-frame jump.
   - Nothing else needs to change. With this fixed, the take is a PASS with no further art review.
   - **Stopgap at conform:** replace each bad frame with a 50/50 blend of its neighbours. A plain duplicate also works but adds a stutter.

## Notes (not blocking)
- The hero is about 30 % of the frame height, which reads as medium more than close-medium. The lower 40 % is warm dirt with a jar and a bundle. Accepted.
