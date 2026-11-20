# QA-art round 17 s26: FIX-FIRST
s26 is BIGZOOM B, the ending (g 1958-2111). I extracted all 162 frames (g = 1950 + n). I judged:
- a 144x256 phone sheet every 5th frame
- every frame from g 2015 to g 2062 at full size (as 2-up pairs)
- 2-3x nearest-neighbour crops of the wall behind the herd at g 2021/2025/2028/2031/2034/2038/2039/2045/2046/2054/2066
- full-size frames at g 1958, 1995, 2008, 2075, 2090 and 2111
- a 2x crop of the 即墨 plaque and the fields at g 1958
- a per-frame flat-patch detector on y 420-800 (7x7 local std < 2, mid luma, desaturated, largest connected blob)
- HSV saturation, lower-frame luma and warmth (R-B) per frame

Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa17/ (s26_phone.jpg, s26_wide.png, s26_patch_A.png, s26_patch_B.png, s26_patch_C.png, frames in f/).

## Round-17 checks
1. **Pale rectangles gone? NOT FULLY.**
   - The big translucent panels from round 16 (300 x 230 px over the wall) are gone. The smoke-card rectangles are gone too.
   - But a smaller version of the same artifact is still there, g 2025-2056 (about 32 frames, 1.1 s). It is a flat, untextured, mauve-beige patch with stair-step pixel edges, sitting on the wall base behind the herd. It is now opaque rather than translucent, and it wipes out the brick texture wherever it sits:
     - g 2021-2025: a blocky pale "T" shape (head and arms, like a figure silhouette) at x about 560-660, y about 545-600.
     - g 2027-2038: it grows into a box behind the oxen's backs. The flat blob measures 690 px at g 2027, 1,900 px at g 2031 and 2,600 px at g 2038 (about 100 x 50 px at x 466-565, y 546-596). With the parts hidden behind the horns, the band is about 250 x 55 px (patch_B, g 2038).
     - g 2039-2042: a second patch at x 231-300, y 551-617 (3,100 px at g 2039), right behind the general's helmet (patch_C, top left).
     - g 2043-2048: a stair-stepped flat strip at x 445-540, y 557-598 (patch_C, bottom left).
     - g 2052-2056: a flat vertical panel at x 100-144, y 648-745 (2,350 px at g 2054), beside the wall-base pots (patch_C, top right).
   - Before g 2025 and after g 2058 the detector finds nothing over about 300 px, and those blobs are ground shadow or props.
   - On the phone it reads as a pale beige strip or box behind the herd, which is less loud than round 16. At full size it is plainly a glitch: hard straight edges, blocky stairs and no texture. It fails the round-16 pass check ("no flat pale patch over 20 px").
   - The "T" figure shape at g 2021-2025 suggests one more translucent or emissive object is still live. It could be a distant defender cut-out, a fourth glow quad or a rim copy, smeared into blocks by OIDN at 12 samples.
2. **Smoke: OK.** The tail smoke is now clusters of small white-grey spheres. They read as comic cotton-ball puffs, with no card edge and no rectangle. They are a little grey and flat, but acceptable.
3. **Nothing else regressed: YES.**
   - **Zoom:** one continuous eased crane from the extreme wide down to the low medium, with no pulse.
   - **Plaque:** 即墨 is crisp and readable at g 1958.
   - **Gag:** the scream, the fist-gripped cup with slosh, the dropped helmet from g 2046, the look-back and the rage oxen are all intact.
   - **Rim:** a clean single pale blue-white outline on the general and the oxen.
   - **Halos:** no unsharp fringes at 2x on the roofs, the wall or the figures.
   - **Dark block:** the dark block at the bottom at g 2019-2028 is now an inked post with a wood top. It reads as a set prop. Accepted.
   - **End frames:** g 2066-2111 are clean. The defocused gate at g 2090 no longer shows the round-16 stair-step edges.
4. **Fields vivid enough? Acceptable (note).**
   - Measured saturation:
     - g 1958: 0.54 (was 0.52)
     - g 1965: 0.53
     - g 1975: 0.47
     - g 1985-2005: 0.43-0.44 (was 0.38-0.39)
     - g 2015-2025: 0.49-0.52
   - Warmth (R-B, lower frame) rises from about -13 to +37 by g 2025.
   - The ~420 orange hay, pot and basket props pop well. The ground tiles between them are still slate blue-grey at g 1985-2010, so the plain reads as "cool dawn with warm dressing" rather than vivid. That is still below the 0.48 conform target but no longer murky. It is not a blocker; the conform grade can lift it.

## Verdict: FIX-FIRST (1 blocker, narrow)
1. **Remove the remaining flat pale patches on the wall base, g 2021-2058.**
   - Find the object. Hide objects one at a time on g 2025 and g 2038 only. It is whatever is still rendered between the herd and the wall at the wall base: the T-shaped silhouette at g 2021-2025 is the clue.
   - Then hide it, or make it fully opaque and textured, or composite a clean wall plate over that range.
   - Re-render or patch g 2015-2062 only. Nothing else in the take needs to change.
   - Pass check: at 2x on g 2025, 2031, 2038, 2041, 2046 and 2054, the brick texture is continuous behind the herd and the general, with no flat untextured patch over 20 px and no stair-step edges.
   - If this is the only change, the next round is a quick PASS on that check alone.

## Notes (non-blocking)
- Fields at g 1985-2010 are at saturation 0.43-0.44. The conform grade should take them to 0.48 or more and warm the ground tiles, not only the props.
- The smoke spheres could take a touch more warmth or alpha falloff at the edges so they read as smoke rather than cotton balls. This is optional.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 7.5 | 8 | 8 | 8 |
