# QA s19 (render team 5, film 18) round 13 - frames g1427-1514 (+6 handles: take.mkv g1421-1520, 100 frames), jimo_out NIGHT
Frame-diff in-shot (n=87): median **11.11**, p90 **13.74**. qa_auto "blur" g1505+ = whip landing (director: false positive).

## Measured per frame (c18.py `shot.py measure`, g1427-1497, before the whip)
- **Flame-to-face on exact card alpha (matte)**: every flame card's alpha is warped to the 720x1280 frame with the card's real quad, and the distance to the face circle (head anchor, radius 0.95 D x scale: head, horns, blades) of every OTHER ox is taken. Worst: **38 px (g1437)**; no frame below 15 px. (Own flame vs own ox excluded.) I used card alpha, not a Cycles object-index pass; it is the same geometry the render uses but it ignores occlusion.
- **Mouths**: worst y **857 (g1484)** (limit 860).
- **Ground** (`J.ground_share` on rendered frames): 0.17 / 0.27 / 0.28 / 0.27 / 0.15 / 0.23 / 0.18 at g1430 / 1442 / 1448 / 1457 / 1470 / 1490 / 1500 (all <= 0.28).
## How (and what it cost)
- Flames: capped at 0.4 x scale (card height 0.8 D), leaned up 30 deg (lean 60). Lane stagger as asked did not work: a follower's head is always next to the leader's tail flame when they share a screen row, whatever the lateral offset. The only layouts with no gap < 15 px (8 layouts searched with the matte) were sparse: **one lane (hole x 30), one ox every 18 frames (9 D)**. So the "dense burst" is gone: 3-4 oxen are on screen at a time, plus the Qi.
- Qi: moved behind the oxen (x 44-48, outside the hole lane); they run behind the ox row.
- Pots: warm lights from round 12 kept; the lower band has pots, bowls and a helmet (all touching the ground with contact shadows from the set's hull / the props' own bottom).
- Not done: nothing else of the list; the pots still look violet-lavender in the lower left at g1430-1447.
