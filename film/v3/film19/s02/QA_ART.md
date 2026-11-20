# s02 QA-art

## Round 9 (director QA-art): FIX, 6.3

Take: take.mkv.partaa + partab, joined to /tmp/s02_a.mkv (first_g 48, g 48-199, frame index = g - 48). I extracted every frame, viewed them at 3 fps, viewed every frame from g 104 to 127 (the descent), and viewed key frames at 360x640.
Frames: /tmp/qa19_r9art/s02/f_NNN.png (NNN = index + 1). Sheets: /tmp/qa19_r9art/s02_3fps.jpg, s02_dive.jpg, s02_full1.jpg, s02_full2.jpg (360 px wide = phone), s02_astro.jpg.

| Check | Status |
|---|---|
| Start is extreme wide? | **No, it is a wide.** At g 48-57 the ship fills about 30 % of the frame height, with only a thin strip of horizon and sky at the top. The sea is a lovely vivid turquoise with a white wake, but it reads as "a ship from a drone", not "one lone ship on an endless ocean". The characters cannot be found (they are under 5 %, which is right, but nothing guides the eye to them). |
| Move shape | **Badly timed.** From g 48 to 107 (2 s) the camera only pushes slowly; the ship grows from about 30 % to 55 %. Then the whole descent happens in about 10 frames (g 108-117, 0.33 s): frame-diff jumps from about 10 to 27-40. On a phone this reads as a jump cut, not as a swoop. The medium is reached at g 118 (3.93 s) and then the shot holds for 2.4 s with only a slow orbit. |
| Detail passing on the way down? | **Hardly any.** The sails pass in 2-3 frames. For g 111-116 the main thing passing is the plain navy hull side and gunwale, which fills up to half the frame as a dark, flat wedge. The rigging, ratlines, lanterns, cannon, crew and deck life are never seen up close on the way in. |
| Landing / "nobody knows where we are" beat | **Weak.** The landing frame is good: a medium on the quarterdeck, with the wheel shadow and rigging shadows on the orange deck, the sails and shrouds behind, and the bodies about 37 % of the frame height. Nobody is cut and the faces are about 16 %. But: (1) **the chart is not blank.** It shows a coastline and a big red compass-rose/X mark, so on a phone it reads as "we know exactly where we are" (a treasure map), the opposite of the beat. (2) The captain only holds the chart with a stern frown for 2.4 s. He does not look puzzled, turn the chart or look around. (3) The astronomer squints through the quadrant, lowers it with a frown and raises it again (g 142-166). This is fine but small. The planned head-scratch does not read as a scratch. There is no shared "?" moment by 5.5 s. |
| Colour | **Good.** Sat 0.76 to 0.52, luma 106 to 88, vivid 77 % to 54 %. The noon sun gives crisp blue shadows on a warm deck. The sails are a dull grey-lilac and could be warmer or whiter. |
| Grounding / edges | OK. The feet have contact shadows and nobody is cut. |

| Criterion | Score |
|---|---|
| Set | 7.5 |
| Light & colour | 8 |
| Composition / phone | 6 |
| Acting | 5 |
| Key moment (BIGZOOM + "where are we?" beat) | 5 |
| Match to refs (R5 crane up/out over the ship) | 6.5 |
| **Overall** | **6.3 - FIX** |

Fixes (shot.py):
1. **Retime the descent so that it reads as a swoop, not a jump.** Today TM = [(48,0),(80,.26),(108,.57),(114,.84),(118,.97),(150,1)]. Use something like [(48,0),(66,.10),(90,.35),(115,.70),(135,.92),(150,1)]. This gives a clear ease-in, about 1.5 s of fast travel centred on g 100-130, and an ease-out landing at about g 150 (5.0 s). The peak frame-diff should be about 15-20, not 40.
2. **Start wider.** Push KEYS[0] loc out and up about 2x (for example (20, -330, 240)) and lift the look so the horizon sits at about 25 % from the top. Target: ship at or under 12 % of the frame height, with a big glittering sea around it. Add a few sun-glint sparkles near the ship so the eye finds it.
3. **Fly through the rigging, not past the hull.** Raise KEYS[2] and KEYS[3] about 6-8 D in z and route them between the mizzen shrouds and the spanker. Over g 110-140 the frame should pass ratlines, a sail face, a lantern, a flag or pennant, and a sailor on the yard, and the hull side should never be more than about 15 % of the frame.
4. **Make the chart blank** (an empty parchment, or just a big "?" scribble) and remove the red X or compass mark.
5. **Puzzled acting by 5.5 s.** Over g 150-170 the captain turns the chart upside down (rotate the prop 180 degrees, or flip it twice), tilts his head and raises his brows (a puzzled face, not the stern one). The astronomer lowers the quadrant and does a clear head-scratch with the free hand (3 strokes), and they shrug at each other (a 4-frame squash). If allowed, add a small "?" pop over each head on g 160.
6. (Polish) Warm or whiten the sails a little (they read as grey).

## Round 10 (director QA-art): FIX, 6.8 (close; one camera fix away from PASS)

Take: take.mkv.partaa + partab joined to /tmp/s02a.mkv (first_g 48, 152 frames, frame index = g - 48). All frames extracted to /tmp/qa19_r10art/s02/f_NNN.png (NNN = index + 1). Sheets: /tmp/qa19_r10art/s02_sheet.jpg (3 fps), s02_descent.jpg (every 3rd frame g 98-150), s02_flip.jpg and s02_land.jpg / s02_beat.jpg (every frame g 118-127 and g 140-175), s02_beat_phone.jpg (360x640), full-size crops s02_g57_*.png, s02_g135_crop.png, s02_g182_*.png. Per-frame stats: /tmp/qa19_r10art/s02_stats.txt.

| Check | Status |
|---|---|
| Start is extreme wide? | **Yes, fixed.** At g 57 the ship is ~130 px (~10 % of the frame height), alone on a huge sea, with the horizon at ~15 % from the top and a sky band with clouds. The whitecap dashes give the sea scale. The eye goes straight to the ship and its white wake. The two characters are not findable at this distance; that is acceptable because the ship is the subject of the opening. |
| Move shape: smooth? | **Better, but not yet smooth.** g 57-90 is a slow ease-in (frame-diff 1-4; the ship grows from 10 % to ~18 %). It works as an establishing beat. After that the speed comes in **three surges**: g 100-110 (diff ~19, the stern dive), a dip at g 114-118 (~5), g 121-125 (~20, the 90-degree swing over the spanker to top-down), a dip at g 130-139 (~8), then g 143-152 (diff 14 → 21). **The camera then stops dead between g 152 and 153 (diff 18.6 → 2.4 in one frame).** In those last 10 frames the camera drops from top-down to eye level and hits the medium at full speed. On a phone this reads as a slam or landing thud, not an ease-out, so the old "drops in 10 frames" problem has moved to the end of the move. |
| Detail passing by? | **Yes, much better.** The camera passes over the stern with the sails filling the top of the frame (g 104-122), the shrouds and yards, then flies top-down along the quarterdeck. Cannons, lanterns, rails, crates, the wheel and its shadow all pass by (g 125-146), with the two characters visible below at about 8 % of the frame height. The hull side is gone. New issue: for g 125-146 the left 25-35 % of the frame is one big plain grey-lilac sail face. |
| "Nobody knows where we are" beat | **Reads, but it is mild rather than funny.** The chart is now a **blank** parchment with a fold, which is correct. The astronomer's head-scratch with the quadrant (g 160-172) reads clearly. Both characters do a shrug with their arms out (g 176-190), but the palms are not visibly up and the captain's pose reads half as pointing. The captain's face is a half-lidded wavy-mouth "meh" with no brows up, so it looks bored rather than puzzled. The chart flip barely registers at phone size. There is no shared look and no "?" pop, so the beat lands as "uneasy", not as a funny "?!". |
| Colour | **Good.** In-shot mean saturation 0.653 and luma 89.4 (G1: ≥ 0.47 and 85-110). The start is all blue (sat 0.80); the landing has a warm orange deck, blue shadows and a blue sky with dark-navy masts: warm and cool together. The sails are still dull grey-lilac. |
| Grounding / edges / G3 | OK. The feet have contact shadows (the wheel and rigging shadows are on the deck), nobody is cut, and the faces are about 13 % of the frame height. |
| Artefacts | (a) **A pale, flat blue slab ("iceberg" or island) sticks out of the sea at the top right, g 48-~90** (x 550-720, y 330-410 at g 57). It reads as a glitch and contradicts "no land in sight". (b) The foreground deck (bottom ~30 % of the frame, g 150-199) has a smeared, low-resolution plank texture that reads soft at full size, and it is a large empty plane. (c) The sun-glint smears at the lower left of g 48-75 are soft white blobs. |

### Override review: qa_auto blur flag (s02)
I viewed g 57 and g 78 at full size (720x1280), with 2-3x nearest-neighbour crops of the ship and rigging, a horizon crop and the lower-left sea, plus g 135 and g 182 at full size.
- **Sharp:**
  - The horizon is a crisp 1-px edge.
  - The cloud silhouettes are clean.
  - The whitecap dashes are hard-edged.
  - At g 57 and g 78 the ship's yards, sail panels, mast line, hull rim and stern lights resolve to single pixels, with no smear and no depth-of-field halo.
  - The deck props at g 135 (cannon, lantern, rails) are crisp.
- **Why qa_auto flags it:** the low Laplacian variance (full-res ~32 at g 48-80, against ~2000-3000 mid-swoop) comes from the content: about 90 % of the frame is smooth, untextured sea and sky.
- **Genuinely soft, but small:**
  - the sun-glint smears at the lower left (g 48-75);
  - the deck plank texture in the foreground of the landing (g 150-199), a texture-resolution or filtering issue, not focus.
- **Judgement: a false positive.** Waive the qa_auto blur FAIL for the s02 BIGZOOM opening (g 48-90) and the sail/plank pass (g 126-146). This waiver does not cover the soft foreground deck texture; fix it as polish (fix 5).

| Criterion | Score |
|---|---|
| Set | 8 |
| Light & colour | 8 |
| Composition / phone | 7 |
| Acting | 6.5 |
| Key moment (BIGZOOM + "where are we?" beat) | 6 |
| Match to refs (R5 crane over the ship onto the deck) | 7 |
| **Overall** | **6.8 - FIX** |

Fixes (shot.py), in priority order:
1. **Ease the landing (blocking).**
   - Reparametrise the Catmull-Rom spline by arc length, so that u maps to distance travelled rather than to the key index; today the last 8 % of u covers the whole top-down to eye-level drop.
   - Then use a table such as [(48,0),(66,.08),(90,.30),(115,.60),(140,.86),(160,.97),(170,1)].
   - Spread the top-down to eye-level drop over g 138-165 (about 27 frames, not 10).
   - Targets: in-shot frame-diff ≤ ~16, with no single-frame drop greater than ~4 between neighbouring frames, and a single speed hump rather than three.
   - Shift the beat by about 8-10 frames (it still fits by g 190).
2. **Remove the slab at the top right of the opening.** Hide the ship_aerial island or iceberg object in this take, or rotate the start azimuth until it is out of frame. Nothing should suggest land in "nobody knows where we are".
3. **Make the beat funnier.**
   - Captain: brows up and a puzzled face (not the half-lidded one), and a clear 180-degree flip of the chart in 4-6 frames.
   - Both: a shared look at each other (g ~168), then a shrug with palms up and shoulders up (a 4-frame squash).
   - If allowed, a small "?" pop over each head at the shrug (signs and labels are allowed under I.4).
4. Give the big sail that passes on the left at g 125-146 some detail (seams, reef points, a pennant), or route about 1 D further right so that rigging and deck life fill more of the frame than flat canvas.
5. (Polish) Sharpen the foreground deck texture: use a higher-resolution plank texture, or anisotropic or closest filtering. Optionally drop the camera 0.3 D so that the empty deck takes about 20 % of the frame instead of 30 %. Keep room for the caption band at y 880.
6. (Polish, carried from round 9) Warm or whiten the sails; R5's ships use bold orange or striped sails.

## Round 11 (director QA-art): PASS, 7.3 (with one cheap must-fix: the prop pops at g 182 and g 186)

Take: take.mkv.partaa + partab joined to /tmp/s02a11.mkv (first_g 48, 152 frames, 720x1280, frame index = g - 48). All 152 frames extracted to /tmp/qa19_r11art/s02/f_NNN.png (NNN = g - 47). Sheets: sheet_3fps.jpg (every 10th frame), descent.jpg (every 4th frame g 90-166), beat.jpg (every 2nd frame g 140-190), beat_phone.jpg (360x640 tiles g 160-190), crop_beat.jpg (full-res g 154/158/186), open.jpg (g 57/80), chartgone.jpg (every frame g 180-187). I recomputed the frame-diff myself (90x160 grey) and it matches the team's numbers: median 8.45, p90 14.01, max 15.5.

| Check | Status |
|---|---|
| Move shape | **Fixed: one swoop.** The frame-diff rises smoothly from 1.3 (g 49) to a single peak of 15.5 (g 110), with no dips at the old knots. The three surges are gone and **there is no dead stop at g 152.** There is a second, gentle swell from 7.5 at g 134 to 11.2 at g 165 (the drop from top-down to eye level, g 142-166), then a decel from 10.4 to 3.7 over g 167-171. That is a 4-frame touchdown, a little brisk but not a slam, and part of that diff is the chart flip. Then the orbit holds a steady ~4.3 (never parked). On a phone it reads as one continuous, impressive crane down: lone ship, wake, over the stern, past the sails and shrouds, down onto the quarterdeck. It lands acceptably soft. |
| Start | Good. The ship is ~10 % of the frame height and alone, the horizon is crisp and the clouds are clean. **The pale slab is gone** (checked g 48-90). |
| Detail on the way in | Wake, stern, yards, shrouds, deck props, lanterns and wheel shadow all pass by. **Still open:** for g 118-150 the left 30-40 % of the frame is one plain grey-lilac sail face. The ~1.2 D route shift did not visibly reduce it. |
| Puzzled beat (phone) | **Much better.** g 158-170: the captain's round-eyed, open-mouthed "shocked" face reads instantly at 360x640; this is the laugh. The chart tilts and turns over g 162-170, and the motion reads, although the 180-degree flip itself (the dark band moving) is hard to parse; it reads as "fumbling the chart", which is fine. The astronomer's head-scratch with the quadrant (g 155-181) is clear. **Weak points:** (a) the "shared look" g 173-179 does not read, because both faces stay front-on with half-lidded eyes and no head turn; (b) after g 172 the captain's face goes back to the half-lidded wavy-mouth "worried" face, which is close to the old "bored" look; (c) the shrug g 184-190: the astronomer's arms go out both sides (it reads as a shrug), but the captain only swings one arm toward the astronomer, so it reads half as pointing; no palms are visible on either. |
| **Regression: prop pops** | **The astronomer's quadrant vanishes between g 181 and g 182, and the captain's chart vanishes between g 185 and g 186**: there one frame, gone the next, with no drop or tuck. At g 183-185 the chart also slides away from the captain's hand. The quadrant pop is at full opacity, just before the s04 dissolve (g 185-197), and is visible on a phone. |
| Colour / light | Unchanged and good (sat 0.634, luma 93.2: G1 OK). Warm orange deck against blue sea, sky and masts; hard sun shadows. The sails are still dull grey-lilac (polish). |
| Grounding / framing (G2/G3) | Contact shadows on every tile, nobody cut, faces ~13-15 % of the frame height, nothing through faces. The foreground deck (bottom ~30 %, g 160-199) is still a soft, smeared plank texture over a large empty plane (polish, carried). |

| Criterion | Score |
|---|---|
| Set | 8 |
| Light & colour | 8 |
| Composition / phone | 7 |
| Acting | 7 |
| Key moment (BIGZOOM + "where are we?" beat) | 7.5 |
| Match to refs (R5 crane over the ship onto the deck) | 7.5 |
| **Overall** | **7.3 - PASS** |

Must-fix before FINAL (cheap, no re-review needed beyond a frame check of g 178-191):
1. **Kill the prop pops.** Keep the quadrant in the astronomer's hand through g 199 (or let it drop or tuck over 4+ frames). Likewise the chart: keep it pinned to the captain's hand, or let him toss it over his shoulder in a visible arc. Nothing may disappear in one frame.

Recommended (non-blocking polish, in priority order):
2. Make the shrug palms-up with both arms and shoulders up, symmetrical for the captain (no single arm toward the astronomer), with a 3-4 frame squash.
3. Make the shared look read: turn the heads ~15-20 deg toward each other (or slide the pupils sideways) on g 173-179, and keep the captain's brows raised (not half-lidded) through the shrug.
4. Break up the flat sail on the left at g 118-150 with seams, reef points or a stripe, or warm or whiten all the sails (R5 style).
5. Sharpen the foreground deck texture, or lower the empty-deck share.
