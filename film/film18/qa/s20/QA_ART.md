# QA-art s20 (reveal A: "ไฟอยู่ข้างหลัง วัวเลยวิ่งไปข้างหน้าอย่างเดียว", 50.51-53.20 s), TAKE gate round 8 — FIX-FIRST (reveal, strict)
Reviewed take.mkv at 6 fps (art10/f, g 1509-1599) at full size and on art10/psheet_0-1.jpg (360x640, cyan = y 880).

## Earlier changes
1. Frame + ground: NOT DONE. The take notes say the lead ox is at y 0.38-0.62 and 40 % of height, but the frames show it at y 0.22-0.48 and about 26 % of height (g 1559, art10/f/010.png). From y 0.50 to the bottom (about 50 % of frame, every shot frame) there is only plain cold lavender-slate gravel, not the dark-earth gapfill. The warm pools under the flames are only a few small patches behind the ox. No second rank was added: the notes confirm the Qi cards did not render.
2. Flames trail back: Partly DONE. The lead ox's own flame now roots at the bundle tip and streams back to screen-right, which is good. But the left neighbour's flame still ends at the lead ox's snout, next to the steam puffs, about 30 px away (g 1534-1559 and g 1579, x 0-40, y 420-440). On the phone it still looks like breathing fire.
3. Camera: Partly DONE. There is a visible dolly and sway (median 5.7, p90 6.9). The ox now drifts across the frame. It is still under the 9 guide.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 4 | 4 | 3 | 6 | 5 |

On the phone you see one angry, roaring dragon-ox high in the frame over a huge empty violet floor, with one flame behind it and another at its nose. "Fire behind, so they only run forward" and "the herd charges" do not read.

## Verdict: FIX-FIRST
1. **Re-aim the camera (verify on a still before rendering):** Tilt down or lower the camera so the lead ox's feet sit at y 0.66-0.70 and its back at y 0.36-0.40, about 35 % of height, with its chin above y 860. Measure this on a rendered frame; do not rely on the rig values. Fill the lower band with 2-3 more running oxen (or Qi silhouettes) cropped by the bottom edge, plus dust puffs. Plain ground must be 30 % or less.
2. **Ground colour:** Apply the s19 dark-earth gapfill material to this ground (it is still the cold lavender gravel). Put a warm orange pool under every lit tail, so the bottom half carries firelight.
3. **Nose flame:** Move the left neighbour ox back by at least half a body length, or drop it. No flame may come within 60 px of any ox face in any frame, especially g 1534-1559 and g 1579.
