# QA-art round 19 s26: PASS
s26 is BIGZOOM B, the ending (g 1958-2111). I extracted all 162 frames (g = 1950 + n). I checked:
- **Every frame g 2015-2095 at full size (1:1):** the band y 380-1000, the whole wall base and herd area, in 21 sheets.
- **2x crops:** the herd's feet every 2nd frame (g 2016-2094), and other suspect areas.
- **A flat-region detector over g 2015-2095:** 7x7 std < 1.5, desaturated mid-tones, ≥ 20x20 px, ≥ 300 px.
- **Key frames:** g 1960/1975/1990/2005/2066/2075/2100/2111, plus the take's phone sheet.

Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa19/ (s26sheets/, s26_cand.png, s26_feet2.png, s26_feetstrip0/1.png, s26_streak.png, s26_keys.png, s26_flat.txt).

## Round-18 blocker: flat untextured boxes: FIXED
- **g 2027-2051:** the mauve-brown boxes between the horns (x 475-610, y 540-595) and behind the general's raised arm (x 255-340, y 560-605) are gone. Brick texture runs continuously behind the herd's backs on every frame.
- **g 2078-2092:** the tan rectangle behind the ox head is gone. The wall brick and battlements show behind the head.
- **Detector:** every flat region ≥ 20 px it found in g 2015-2095 is legitimate, and I checked each one at 2x:
  - the far hill and plain strip at g 2015-2029
  - flat-shaded puppet fills
  - the dropped helmet at g 2067-2073
  - the general's boots and the road at g 2075-2093
  - the smoke spheres at g 2049-2050
  - None of them is an untextured card.

## Still holds
- **BIGZOOM gag:** one eased crane from the extreme wide to the medium general, with no cut. It has the scream, the fist-gripped cup, the helmet drop and the rage oxen with smoke.
- **Plaque:** 即墨 is readable on the gate at the start (g 1958-1965).
- **Rim:** the pale blue-white rim on the general and the oxen is intact.
- **Framing:** the general's back is no longer clipped by the right edge at g 2078-2090.
- **Hard rules:** no pole through a face, no fire on a head, no half-cut main character.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 7.5 | 8 | 8 | 8 |

## Notes (not blocking)
1. **A faint translucent quad under the front ox's hooves, g ~2018-2044.** This is the round-18 "grey square at the ox's feet", now larger and fainter.
   - **What it is:** a lighter rectangle about 120-170 x 30-40 px (for example x 390-567, y 735-785 at g 2030) with straight right and bottom edges. It is not flat: the ground speckle shows through. It is lifted by about +13/255 in all channels.
   - **Likely cause:** a card or rim-copy quad whose alpha is not exactly 0 below the hooves.
   - **Visibility:** at 1:1 it is visible on careful viewing, strongest at g 2028-2034. It disappears on the phone, and the eye is on the general.
   - **Optional fix:** alpha-clip the ox card and rim-copy materials (alpha < 0.05 → 0) and re-render g 2016-2048.
2. **Thin bright horizontal light bars** in the gate opening behind the smoke at g 2040-2048 (x about 600-720, y about 585-620). They read as lit interior beams, not as a glitch. Keep them.
3. The field saturation at g 1985-2005 is for the conform grade, as noted in round 17.
