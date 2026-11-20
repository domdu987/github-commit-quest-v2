# QA-art round 14b s26: PASS (notes)
s26 is BIGZOOM B, the ending: the general runs home chased by oxen (g 1958-2111). I extracted all 162 frames (g = 1950 + n). I judged every 5th frame (about 6 fps) on a 144x256 phone sheet and full-size frames at g 1958/1985/2020/2066/2090/2111. I used 2-3x crops for findability, the plaque, the rim and halos, and computed per-frame 90x160 frame diff. I measured a blue-pixel mask and edge profiles for the rim, HSV saturation and luma per frame, and ran a trial ffmpeg eq grade on g 1990 and g 2005. I compared against R5/R4 (their wide-to-close establishing moves and bold colour).

## Checks
1. **One continuous eased move from extreme wide to medium by g 2066: DONE.**
   - The frame diff rises smoothly: 2.4 at g 1959, 8-12 through the descent, and 6-10 on the tracking push.
   - There are no pulses and no cuts. There is one soft dip, 12 to 7 at g 1986, as the gate hall leaves the frame, which is not a pulse.
   - The general is about 2-3 % of frame height when first visible and about 52 % at g 2066 (plume to foot, y 290-950), inside the 35-60 % range.
   - **Findable: from g 1966.** At g 1958-1964 he is hidden behind the gate banner and hall, so the extreme-wide start shows the set without him. From g 1966 he is a small figure in the warm road pool, and by g 1975-1985 the red ox cluster beside him makes him easy to find.
2. **Rich set detail on the way in: DONE.** The set holds tiled gate hall roofs with lit windows, braziers, the Yan camp tents and palisade with flags, trees, road props (baskets, pots, torches), the moat, a crenellated wall with lamps and banners, and smoke on the ox tails. It is at least as rich as the R4 village sets.
3. **The 即墨 plaque is readable: DONE.** It is gold on dark, about 180 px wide at g 1958, crisp, and readable on the phone tile.
4. **The ending gag reads: DONE.** The general runs at the lens screaming, cup in fist with the cup sloshing, helmet askew, and a wall of rage oxen with smoking tails behind him. The panic look-back is at g 2070-2080. It reads instantly on the phone, and the composition at g 2090-2111 is strong.
5. **The emissive "rim" copy: NO GHOSTING, but it does not read as a light rim.**
   - I found no doubled hats, legs or cups. The stacked plume strands and the dark shoulder guard are the puppet's own drawing (compare s15).
   - The copy renders as one dark navy band about 6-12 px wide outside the black ink line, for example (36,30,57) at the helmet edge at g 2111. It reads as a bolder outline, not as moonlight.
   - A blue mask (b > r+25, b > 120) finds only 300-900 px per frame at g 2066-2111, and those are on the moat and smoke, not on the characters.
   - Clean, but §I's rim is effectively missing on the general at the end (see note 2).
6. **Unsharp-mask halos on the wide frames: VISIBLE (note).** At full size, g 1958-2030 show bright and dark halos along the roof ridges, tent edges, field-tile seams and the horizon line, and a glow edge on the wall at g 2020. It looks crunchy and "HDR". On the phone it reads as crisp and does not block.
7. **Blue-murky wide fields: partly fixable by grade, not a blocker.**
   - Measured saturation is 0.37-0.44 for g 1958-2005 (lower field luma 60-65), against 0.47-0.49 for g 2040-2111.
   - A strong trial grade (eq saturation 1.9, gamma 1.15, warm colour balance) brings g 1990/2005 to saturation 0.40-0.43 and lower luma 72-75. The sky and the warm road pop, but the fields stay slate grey-blue because their albedo has almost no hue.
   - Even so, the warm road pool, braziers and red oxen carry the eye through the wide. The descent lasts about 2.2 s and lands on a strongly coloured medium, so I do not block. It is the main FINAL risk for "as vivid as film 2" (see note 1).

## Phone read
This is a real BIGZOOM in the reference Shorts' sense: a rich set, one move and a funny payoff. The weak part is the first 2 s of muted fields.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 6 | 8 | 8 | 8 |

## Verdict: PASS with notes
Notes, recommended before FINAL, in priority order:
1. **Field colour:** Warm the field tile albedo toward ochre and green-gold, or add a low dawn sun key from screen-left over the fields.
   - Target on the render before the conform grade: saturation ≥ 0.45 and lower-frame (y > 400) luma ≥ 72 on g 1975-2010.
2. **Rim:** Raise the rim copy's emission so it reads as light: luma ≥ 150 and blue-dominant on the top and right edge, 3-6 px visible.
   - Or drop the copy and use a warm dawn back-rim from the sky side, which suits this shot better.
   - Keep it a single outline. The current one is clean.
3. **Halos:** Re-apply the unsharp mask at radius 1, strength ≤ 150 % (now 330 %), or sharpen the raw renders with more samples.
   - Check: no visible bright fringe on the roof ridges and the horizon at g 1958 and g 2020 at 2x zoom.
4. **Start findability:** Shift the start camera or the general's g 1958 position about 40 px so that he is clear of the gate banner from the first frame. Currently he appears from g 1966. The incoming dissolve partly covers this.
