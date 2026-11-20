# QA-art s20 (reveal A: fire behind, they run forward only, 50.51-53.20 s), TAKE gate round 6 — FIX-FIRST (reveal, practical)
I reviewed take.mkv at 6 fps (art8/gNNNN.png, g 1509-1599) at full size 720x1280 and on the 360x640 sheets art8_phone_0-2.jpg.

## Earlier changes
1. Framing (lead ox 40 % of height, tail and flame in frame): NOT DONE. The lead ox is about 20 % of the frame height at y 0.40-0.62. Its own tail flame is small and half hidden (g 1574, x 490-540). The biggest flame is the next ox's round flame, which sits beside or in front of a background ox's face (g 1574, x 630-720, y 570-640).
2. Sky/ground <= 25 %: NOT MET. The sky is about 40 %. The ground (y 780-1280, about 40 %) is dressed with untextured navy rocks and spiky navy tufts, which break rule 2 and read as placeholders on the phone.
3. Tripod brazier: NOT DONE (third round). It stands right behind the lead ox's head/neck, g 1544-1599. At g 1574 its flame rises between the horns, so on the phone the ox's head is on fire. This is the opposite of the film's key image.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 4 | 5 | 3 | 5 | 6 |

The phone viewer sees a calm ox trotting on a cold blue field with a torch on its head. "Fire behind, it runs forward" does not read.

## Verdict: FIX-FIRST
## Changes
1. **Brazier:** Raycast from the camera through g 1574 pixel (x 130, y 560) and g 1589 pixel (x 590, y 640). Hide every hit object, and if needed everything parented to it. If it still cannot be identified, move the herd lane or the camera truck so that no set torch is in frame. The only flames in this take are tail flames.
2. **Lead ox, whole take:** Come about 35 % closer and pitch down. The lead ox should be 35-40 % of the frame height, head at x 0.20-0.30, with the tail, bundle and a LARGE trailing flame (the s22 card, about 1/3 of the body) fully in frame at x 0.65-0.90. The herd band should sit at y 0.40-0.65 and the sky should be 25 % or less. Give the lead ox the new `face='rage'` used in s22, so the charge reads as furious and matches the reveal.
3. **Ground:** Remove the navy/blue-grey rocks and tufts, or recolour them warm brown (earth clods, trampled straw, reed). Add warm light pools on the ground under each tail flame, so the lower third is warm and lit, not cold violet.
