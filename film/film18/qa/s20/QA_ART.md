# QA-art s20 (reveal A: "ไฟอยู่ข้างหลัง วัวเลยวิ่งไปข้างหน้าอย่างเดียว", 50.51-53.20 s), TAKE gate re-render — FIX-FIRST (reveal, strict)
I reviewed take.mkv at 6 fps (art9/gNNNN.png, g 1509-1599) at full size 720x1280 and on the 360x640 sheets art9_phone_0-2.jpg (cyan line = y 880).

## Earlier changes
1. Brazier behind the lead ox's head: DONE. No set torch is in frame in the shot (g 1519-1599).
2. Lead ox 35-40 % of height, rage face, flame in frame: PARTLY done. The rage face reads well (V brows, red eyes, roaring mouth, steam). The ox is about 25 % of frame height at y 0.25-0.50. Its own tail flame is at x 0.85-0.95 but sits BETWEEN the rump and the bundle, with the narrow end at the bundle. It points forward along the tail toward the body instead of streaming back off the tip (crop_1564.png).
3. Ground warm, no navy lumps: lumps DONE. Warm ground NOT DONE: see the blocker below.

## Blockers
- **Bottom half is empty:** From y about 0.50 to 1.0 (about 50 % of the frame, g 1524-1599) there is only plain cold slate-blue ground with horizontal stripe banding, which reads like a stretched or smeared texture. This is above the 30 % block line.
- **Flame at the lead ox's nose:** The flame of the ox on the left ends at the lead ox's snout, next to its steam puffs (g 1529-1599, x 30-175, y 430-460). On the phone the lead ox looks like it is breathing fire or running into a flame. That is the opposite of "fire behind".
- **Camera:** in-shot frame-diff median 4.03 and p90 6.7 (guide 9). There is no visible dolly or slide. The ox holds the same screen position for 2.5 s.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 4 | 5 | 3 | 6 | 4 |

The phone viewer sees an angry ox standing high in the frame over a big empty blue floor. "Fire behind, so they only run forward" does not read.

## Verdict: FIX-FIRST
1. **Frame + ground:** Re-aim so the lead ox sits at y 0.38-0.68 (chin at y 860 or above), 35 % of height. Fill the near lane below it with a second rank: 2-3 oxen or running Qi silhouettes cropped by the bottom edge, plus dust and a warm pool under every flame. Plain ground should be 30 % or less. Replace the striped slate floor with the s19 dark-earth dirt.
2. **Flames trail back:** Mirror the flame cards along with the mirrored oxen. Root each flame on the bundle tip and taper it backward, screen-right, away from the run direction. The lead ox's flame must be fully in frame at x 0.70-0.92. No flame may come within 60 px of any ox face; move or drop the left neighbour.
3. **Camera recipe:** Add a real eased dolly-in of 8-10 % per second plus a truck of 0.3 D/s against the herd direction, so the background oxen and trees slide. Draft at 180x320 until p90 is 9 or more. Use no pulses.
