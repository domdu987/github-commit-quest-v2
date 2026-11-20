# QA-art round 16 s26: FIX-FIRST
s26 is BIGZOOM B, the ending (g 1958-2111). I extracted all 162 frames (g = 1950 + n). I judged:
- a 144x256 phone sheet every 5th frame (about 6 fps)
- full-size frames at g 1958/1985/2005/2025/2066/2111
- 2x crops of the roof ridges and horizon at g 1958 and the wall at g 2020
- crops of the background behind the herd every 4th frame from g 2006 to 2066, and at full resolution at g 2025/2034/2042/2054/2090
- HSV saturation and luma per frame

Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa16/ (s26_phone.jpg, s26_A.jpg, s26_B.jpg, s26_halo.jpg, s26_ghost.jpg, s26_ghost2.jpg, s26_zoom.jpg).

## Round-16 checks
1. **Unsharp halos gone? YES.** At 2x zoom, g 1958 (tents, fence, roof ridges) and g 2020 (wall and horizon) show clean ink lines with no bright or dark fringe. The look is no longer crunchy.
2. **General clear of the banner at the start? YES.** At g 1958 he is a small figure beside the smoking red ox cluster, at about x 320, y 650. The gate banner is at x about 80-130. He is findable from the first frame.
3. **Rim brighter? YES.** It is now a clean pale blue-white outline, 6-10 px, on the general and the oxen. It is single, with no doubling, and reads as light on the phone. It looks a little more like a sticker edge than moonlight, but it fits the new dawn sky. Accepted.
4. **Fields less murky? Only at the very start (note).**
   - Measured saturation:
     - g 1958: 0.52 (up from 0.37-0.44)
     - g 1965: 0.50
     - g 1975: 0.45
     - g 1985-2010: still 0.38-0.39, with lower-frame saturation 0.34-0.36 and lower luma 66-68
     - g 2020-2111: 0.45-0.47
   - The new orange dawn sky helps a lot. The mid-descent fields are still slate grey-green, but the warm road pool and the red oxen carry the eye. This is not a blocker; it is the conform grade's job.
5. **Nothing regressed? NO. A new glitch artifact (hard rule).**
   - From about g 2026 to 2058, large pale translucent rectangles sit on the city wall behind the herd. They are flat beige-pink panels with straight edges and blocky stair-step borders, and they wipe out the brick texture:
     - g 2034: one panel about 300 x 230 px at x about 290-590, y about 485-720.
     - g 2042 and g 2054: the same patches along the wall base and beside the gate tower.
     - g 2025: two blocky, pixelated pale humanoid-like shapes at x about 280-440, y about 480-570.
   - At g 2020 the smoke puffs on the ox tails show the same pale card with a straight rectangular top edge. The likely cause is the smoke (or the new emissive rim-copy) cards rendering their full quad at low alpha instead of zero outside the puffs, possibly smeared further by the denoiser.
   - From g 2066 on, the defocused gate behind the general also shows blocky stair-step pale edges (g 2090). That is milder, but it is the same family.
   - On the phone sheet (g 2030-2055) these read as blank, foggy boxes behind the oxen, right on the payoff approach. This is a ghost/glitch artifact, so it blocks.
6. **Kept and good:**
   - One continuous eased move from the extreme wide (general about 2 %) to the medium (about 45 % at g 2066).
   - The 即墨 plaque is crisp at the start.
   - The scream, the cup in his fist, the look-back, and the rage oxen with smoking tails.
   - A strong final composition.

## Verdict: FIX-FIRST (1 blocker)
1. **Remove the pale rectangles:**
   - Make every smoke card and rim-copy card fully transparent outside its drawn shape (alpha clip, or premultiplied alpha with a zero-alpha border).
   - Check that no card quad is visible against the wall.
   - Re-render g 2015-2111, or composite a fix over that range.
   - Pass check: at 2x zoom on g 2020, 2034, 2042, 2054 and 2090, the wall's brick texture is continuous behind the herd and the smoke, with no flat pale patch over 20 px and no straight-edged haze box.

## Notes
- A dark, untextured navy block (a post or stump base) slides through the bottom of the frame at about g 2020-2030 (x about 250-360, y about 1150-1280). It is brief, but it is an §2 placeholder look. Texture it or drop it.
- For the field colour at g 1985-2010, see check 4. The conform grade should lift these frames to saturation 0.48 or more.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 7 | 8 | 8 | 8 |
