# QA-art round 19 s22: PASS
s22 is the REVEAL close-medium, the hero ox only (g 1683-1742). I extracted all 71 frames (g = 1677 + n). I checked:
- a per-frame strip of the bottom-left props for g 1677-1726
- full-size frames at g 1677/1678, 1693-1695, 1706-1708 and 1718-1720
- per-frame tracking (template match) of the jar, the reed bundle, three ground patches and the wall for g 1677-1747

Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa19/ (s22_strip.png, s22_rerender.png, s22_grid.png).

## Round-18 blocker: single-frame prop pops: FIXED
- **Jar steps (g 1677-1747):** they follow the camera sway smoothly, about ±8 px per frame in a ~10-frame cycle. Each frame lies between its neighbours, with no one-frame excursion. The match error is 0.7-3.6 on every frame (mean 1.4), so the jar's shape and size are the same on every frame. In round 18, a popped frame changed size and position.
- **Jar and bundle together:** the bundle moves with the jar on every frame. There is no relative jump.
- **Re-rendered frames:**
  - g 1694, 1707, 1719 and 1677 (the handle) sit on the smooth curve: g 1693→1694→1695 = (-7,-4)→(-3,-2)→(+2,+1); g 1706→1707→1708 = (-4,0)→(+2,-5)→(+5,-6); g 1718→1719→1720 = (-4,-5)→(+2,-1)→(+4,+5).
  - Their brightness, sharpness and noise match their neighbours. The flame-light flicker is the same as on other frames.
  - No re-render seam is visible.

## Nothing else regressed
These all hold as in round 18:
- the hero ox with the dragon silk and rage face
- the blue moon rim
- the tail flame in frame at the right
- the star glint at g 1732-1739
- the mouth well above the caption band
- no soldier, poles, fire on heads or half-cut main character

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 7 | 7 | 7 |

## Notes (not blocking)
- **The props are one frame out of phase with the set.** The jar and bundle's per-frame motion matches the ground and wall motion of the NEXT frame:
  - At lag -1, the correlation is 0.85 and the residual about 2 px per frame.
  - At lag 0, the correlation is 0.5 and the residual about 4 px.
  - So within the camera sway, the props slide against the dirt by a few pixels.
  - This was already in every frame I passed in round 18; only the four pop frames were re-rendered, so it is not a regression. It reads as part of the camera shake and I did not see it on the phone.
  - If the shot is ever re-rendered, parent the jar and bundle to the world, or place them from the current frame's camera, not the previous one.
