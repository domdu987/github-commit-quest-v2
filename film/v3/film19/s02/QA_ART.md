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

## Round 12 (director QA-art): PASS, 7.4 (must-fix closed; no regressions)

Take: take.mkv.partaa + partab joined to /tmp/s02a12.mkv (first_g 48, 152 frames, 720x1280, 30 fps). All 152 frames extracted to /tmp/qa19_r12art/s02/gNNN.png (named by g, so this covers 3 fps and every frame g 150-199). Sheets: sheet_3fps.jpg (every 10th frame), beat.jpg (every 2nd frame g 150-198), beat_phone.jpg (360x640 tiles g 166-198), crop_beat.jpg (full-res g 172-199), faces.jpg (full-res heads g 168-196), hands.jpg (every frame g 178-191). I recomputed the frame-diff myself (90x160 grey); it matches framediff.json.

| Check | Status |
|---|---|
| **Props stay in hand (round-11 must-fix)** | **Fixed.** I checked every frame from g 178 to g 199. The quadrant stays in the astronomer's hand: it is raised for the head-scratch until about g 181, then lowered over g 182-187 to hip height, where it sits under the chart. The chart stays at the captain's hand, low and dark band down, through g 199. Nothing vanishes or jumps in one frame. At g 185 the quadrant is briefly hidden behind the chart; this is plain occlusion, with no pop. Minor: from g 186 the chart, the quadrant and both outstretched hands meet in the gap between the characters, so that area reads a little cluttered and the chart looks almost shared. This is acceptable. |
| Landing soft? | **Yes, softer than in round 11.** The frame-diff falls monotonically: 10.4 (g 158), 8.7 (g 167-170), 7.8 (g 171), 6.4 (g 173), 5.5 (g 174), 3.7 (g 175), then a floor of 2.3 at g 176. That is an ease-out over about 8 frames, where round 11 had a 4-frame touchdown, and there is no second surge in camera speed. The rise to about 6 from g 182 to g 187 comes from the shrug action, not the camera. The slow orbit then holds steady at about 4.4 and never parks. On a phone the crane settles onto the quarterdeck instead of thudding. The 8-10 plateau over g 139-169 is the acting plus parallax, as the team says; it looks fine. |
| Puzzled beat: funnier? | **Slightly.** It is still carried by the captain's round-eyed, open-mouthed shock (g 158-170), which reads at phone size. (a) **Shared look, g 173-180:** the captain's pupils and head slide toward the astronomer, and the astronomer, after a squeezed-eye scratch at g 176, glances back left. You can now see it at full size, but at 360x640 it is subtle, a sideways glance rather than a beat. (b) **Brows:** the captain has brow lines, but his eyelids stay half-lidded and his mouth is wavy, so the face reads "unimpressed / queasy" more than "brows-up puzzled". This is better than round 11, but not a clear "?!" face. (c) **Shrug, g 184-199:** the astronomer is a clean, symmetric arms-out shrug. The captain now has both arms off his body, but his chart arm sits horizontal toward the astronomer while the other arm is low, so it still reads partly as offering or pointing. I cannot make out palms on either character at phone size, because the hands are small dark gloves. There is no shoulder-up squash. **Net: the beat reads clearly as "neither of us knows", gently funny rather than a big laugh.** |
| Regressions | **None found.** Compared with round 11: the opening is the same (lone ship at about 10 %, no slab), the wake, the stern pass, colour and grounding are unchanged, contact shadows are present on every tile, nobody is cut, faces are about 13-15 % of the frame height, and nothing passes through a face (G2/G3 OK). qa_stats: saturation 0.635, luma 93.8 (G1 OK). |
| Still open (polish, unchanged) | The plain grey-lilac sail face on the left, g 118-150, has no seams (the team says this was not done). The soft, smeared plank texture covers the bottom ~30 % of the frame on the landing. |

| Criterion | Score |
|---|---|
| Set | 8 |
| Light & colour | 8 |
| Composition / phone | 7 |
| Acting | 7 |
| Key moment (BIGZOOM + "where are we?" beat) | 7.5 |
| Match to refs (R5 crane over the ship onto the deck) | 7.5 |
| **Overall** | **7.4 - PASS** |

Non-blocking polish if time allows (none is needed for FINAL):
1. Captain's face from g 172: open his eyes fully under raised brows (the round shock eyes with a closed, flat mouth). This is the cheapest way to sell "puzzled".
2. Captain's shrug: drop the chart arm to match the other one (both forearms up and out at the same angle) and add a 3-4 frame shoulder lift.
3. Shared look: increase the head yaw to about 20 deg on g 174-180 so it reads at 360x640.
4. Seams or a stripe on the left sail (g 118-150), and a sharper plank texture in the foreground.

## Round 13 (director QA-art): PASS, 7.3, with two must-fix camera items (a regression from round 12)

Take: take.mkv.partaa + partab joined to /tmp/s02a13.mkv (first_g 48, 152 frames, 720x1280, 30 fps). All frames are extracted to /tmp/qa19_r13art/s02/gNNN.png. Sheets:
- sheet_3fps.jpg (every 10th frame)
- descent.jpg (g 148-178)
- beat_phone.jpg (360x640, g 166-198)
- body.jpg (every frame g 178-199)
- faces.jpg
- land.jpg (g 174-178 with a 40-px grid)

My own frame-diff (90x160 grey) for in-shot g 58-190: median 8.12, p90 14.28, max 16.20. I also measured the background shift per frame by phase correlation on the top 300 px.

| Check | Status |
|---|---|
| **Landing: regression** | **Two problems that were not there in round 12.** **(1) A second speed hump.** The frame-diff falls from the swoop peak (15.0 at g 116) to 6.0 at g 141, then rises again to **16.2 at g 156**, the largest value in the take, before easing out. In round 12, g 150-160 ran at 9.5-10.4. The top-down to eye-level drop is now squeezed into about g 148-160 and reads on the phone as a second dive, the "surges" problem from round 10. The ease-out after it (g 156-175, about 20 frames) is soft. **(2) A one-frame hitch at the touchdown.** The background shift goes (3,-6) at g 173, (2,-4) at g 174, **(0,0) at g 175**, **(2,-4) at g 176**, then (0,0) from g 177. So the camera stops, moves once more and stops again; you can see it in the feet and rigging in land.jpg, and the diff jumps to 9.3 at g 176 (full-res), between 5.9 and 3.8. After that the drift starts at g 180 at 1-3 px/frame **in the opposite x direction**. That reversal is slow enough to pass. |
| Props stay in hand | **Yes.** I checked every frame g 178-199. The quadrant stays in the astronomer's hand: raised for the scratch, lowered over g 182-187, held at hip. The chart stays in the captain's hand at chest height through g 199. Nothing pops. |
| Puzzled beat on phone | **Clearly better.** From g 174 the captain has wide round eyes and a flat, open mouth, a dumbfounded "huh?". It reads instantly at 360x640, and it is the best face this beat has had. g 172 is a blink. Shared look: the captain's pupils and head go toward the astronomer at g 176-188, and the astronomer looks back. It reads on the phone, though gently. Shrug, g 183-199: the astronomer is symmetric with arms out. The captain's free arm now lifts out with an open hand, but his chart arm stays horizontal toward the astronomer, so his shrug is still a little lopsided; the shoulder lift is barely visible. The net is a readable, mildly funny "neither of us knows". |
| Other regressions | None. The opening, wake, stern pass, colour (sat 0.639, luma 94.1: G1 OK), contact shadows, framing and face size (13-15 %) are all unchanged (G2/G3 OK). The flat sail g 118-150 and the soft foreground planks are still open polish. |

| Criterion | Score |
|---|---|
| Set | 8 |
| Light & colour | 8 |
| Composition / phone | 7 |
| Acting | 7.5 |
| Key moment (BIGZOOM + beat) | 7 |
| Match to refs | 7.5 |
| **Overall** | **7.3 - PASS (must-fix 1-2 before FINAL)** |

Must-fix (cheap; a frame check of g 140-190 is enough to confirm it):
1. **Restore the round-12 camera curve for g 140-176.** Round 12 had one hump, a diff of about 8-10 through the descent and a monotone settle, and none of its acting depended on this change. Keep all the round-13 acting. No in-shot diff should come back above about 11 after the first peak.
2. **Remove the g 175 stall.** The camera's last moves must decrease frame by frame (for example 4, 3, 2, 1, 0 px) with no zero frame followed by a non-zero one. Start the hold drift in the same x direction as the landing, or start it from 0 with a smooth ease-in.

Optional: lower the captain's chart arm so that both forearms match in the shrug.

## Round 14 (director QA-art): PASS, 7.4. The touchdown is fixed; the late re-acceleration is only partly fixed (must-fix 1 stays open)

Take: take.mkv.partaa + partab joined to /tmp/s02a14.mkv (first_g 48, 152 frames). All frames are extracted to /tmp/qa19_r14art/s02/gNNN.png. Sheets:
- sheet_3fps.jpg
- descent.jpg (every 2nd frame, g 130-182)
- beat_phone.jpg (360x640, g 170-198)
- spike115.jpg (g 112-116)

Measurements:
- Whole-frame diff (90x160 grey), in-shot: median 8.47, p90 14.21, max 18.39 (g 115).
- To test the team's claim that "the hump is the gestures", I also measured a **deck-only band**: the bottom 19 % of the frame, which contains no characters. I measured it for rounds 12, 13 and 14.
- I measured the background shift per frame by phase correlation.

| Check | Status |
|---|---|
| Touchdown hitch (g 175-176) | **Fixed.** The background shift per frame falls monotonically: (3,-7) g 170-175, (3,-6) g 176, (2,-5) g 177, (2,-4) g 178-179, (2,-3) g 180, (1,-1) g 181, (1,0) from g 182. There is no zero frame followed by a move. The deck band falls smoothly from 7.6 at g 170 to 0.5 at g 180. On a phone the landing is the softest so far. |
| Opposite drift | **Fixed.** The hold drift is +1 px/frame in x, the same direction as the landing, and it eases in from the landing. It reads as a living hold, not a park. |
| Second dive (around g 150) | **Smaller, not gone, and it is the camera, not the gestures.** The deck-only band (no characters in it) dips to 6.5 at g 148, then climbs to **16.4 at g 153** before the long settle. For comparison, round 13 went from 6.4 to 18.7 at g 157, and round 12 from 5.7 to 12.2, ramping over about 12 frames. The descent sheet shows why: from g 136 to g 148 the camera hovers almost top-down over the quarterdeck, then from g 148 to g 158 it pitches down to eye level, with the horizon and sea popping up behind the rail. On a phone it reads as "hover, then a step down, then a soft settle". The final settle is lovely, but the move is not yet one continuous swoop. So the team's statement that background speed "falls steadily after g 133" does not match the frames. |
| g 115 whole-frame diff spike (18.4) | Not a defect. At g 112-116 the ship's position steps evenly. The spike comes from the spanker sail sweeping across the centre plus the foam texture; there is no visible jump. |
| Round-13 acting | **Intact.** The captain has his wide-eyed dumbfounded face from g 174; the shared look is at g 176-188; there is an arms-out shrug from g 184; the astronomer's head-scratch with the quadrant is there. Props stay in hand through g 199 with no pops (checked every 2nd frame on the phone sheet and g 178-199). The captain's chart arm is still level, so his shrug is a little lopsided (optional polish, as before). |
| Regressions | None. The opening, wake, stern pass, colour (qa_stats sat 0.635+, luma ~94: G1 OK), grounding and framing are unchanged (G2/G3 OK). The flat sail and soft planks are still open polish. |

| Criterion | Score |
|---|---|
| Set | 8 |
| Light & colour | 8 |
| Composition / phone | 7 |
| Acting | 7.5 |
| Key moment (BIGZOOM + beat) | 7.25 |
| Match to refs | 7.5 |
| **Overall** | **7.4 - PASS** |

Status of the must-fixes:
- **Must-fix 2 (stall / drift): closed.**
- **Must-fix 1 (one swoop): still open, but softened.**

How to fix 1: start pitching the camera down from top-down to eye level earlier, around g 132-136, and spread it to about g 170, so that it overlaps the end of the over-the-stern travel instead of starting after a hover. Target: the deck-only band, once it has passed its first peak, never rises again by more than about 20 % (for example, no climb from 6.5 to 16). Keep everything from g 160 onward exactly as it is now (the settle, the drift and the acting). A frame check of g 130-170 is enough to confirm the fix.

## Round 15 (director QA-art): PASS, 7.5. Must-fix 1 is downgraded to polish: the strip target is not met, but on a phone the drop to eye level now reads as a gentle second push

Take: take.mkv.partaa + partab joined to /tmp/s02a15.mkv (first_g 48, 152 frames). All frames are extracted to /tmp/qa19_r15art/s02/gNNN.png. Sheets:
- sheet_3fps.jpg
- descent.jpg (every 3rd frame, g 110-182)
- beat_phone.jpg
- j127.jpg (g 125-129)

Measurements:
- Whole-frame diff, in-shot g 58-190: median 8.97, p90 14.08, max 15.40 (g 114).
- The deck-only strip (bottom 19 %, no characters) for g 110-182, as asked.
- As a cross-check: the median optical-flow speed of the background, excluding the characters' band (Farneback at 180x320, scaled to full-res px/frame), for rounds 12, 14 and 15. The deck strip turned out to be content-biased: the bare plank texture at g 137-145 under-reads motion, and the wheel shadow entering at g 146 over-reads it. The optical flow is the fairer speed measure.

| Check | Status |
|---|---|
| Deck strip climb-back after the first peak | **Still more than 20 %.** The peak is 29.9 at g 131 (the team's single peak is confirmed). The strip falls to **5.9 at g 145**, then climbs to **13.0 at g 151**, a ratio of 2.2x, before a smooth, monotone settle to 0.4 at g 180. Round 14 was 6.5 to 16.4 (2.5x). The strict target is not met. |
| Optical-flow background speed (px/frame) | **Round 15:** about 13 at g 131-132, a trough of **6-7 at g 134-137**, a ramp to **12-13 over g 142-149**, then a steady fall: 11 (g 151), 9 (g 156), 7 (g 161), 5 (g 165), 4 (g 168-171), 3 (g 172-177), 2 (g 178-180), 1 (g 181 on). **Round 14:** trough 5, then a sharp peak of 16 at g 151. **Round 12** (passed): trough 7, then a plateau of 12-13 at g 142-148. Round 15 is now the same shape as round 12, with no sharp peak. |
| Phone read: one swoop? | **Close.** It is no longer "hover, then step". At g 134-140 the camera slows over the top of the quarterdeck while the characters keep growing; at g 142-158 it rolls forward and tilts down to eye level at an even speed; then the long, soft settle follows. It reads as one move with a breath in it, a gentle second push rather than a dive. The g 126-127 flow blip (17-21) is foam-texture noise; the stern steps evenly in j127.jpg, with no visible jerk. |
| Landing, drift, acting (g 160 onward) | **Unchanged and intact.** The whole-frame diff for g 160-199 is identical to round 14, value for value. The landing eases monotonically to zero; the drift is +1 px/frame in the same direction; the dumbfounded captain, the shared look, the shrug and the head-scratch are all there; props stay in hand through g 199. |
| Regressions | None. The opening, wake, stern pass, colour (sat 0.638, luma 94.4: G1 OK), grounding and framing are unchanged (G2/G3 OK). |

| Criterion | Score |
|---|---|
| Set | 8 |
| Light & colour | 8 |
| Composition / phone | 7 |
| Acting | 7.5 |
| Key moment (BIGZOOM + beat) | 7.5 |
| Match to refs | 7.5 |
| **Overall** | **7.5 - PASS** |

Status of the must-fixes:
- **Must-fix 1 (one swoop): downgraded to optional polish.** The literal 20 % strip target is still missed (2.2x). But the true background speed now ramps gently and has the same shape as round 12, which passed, and it no longer reads as a step on a phone. I do not think another re-time pays for itself.
- If the team wants it perfect: start the tilt-down at about g 128, so that the speed trough at g 134-137 stays at about 10 instead of dipping to 6.
- **Must-fix 2: closed in round 14.**

Nothing blocks conform. The open polish is unchanged: the captain's level chart arm in the shrug, seams on the left sail, and the soft foreground planks.

## Round 16 (director QA-art): FIX. The g 127 catch is fixed, but the "settle, then second tilt-up" (§H.1) is still there

**Correction to my round 15 note.** I called the g 127 flow blip "foam-texture noise". That was wrong. Re-running my own sea-masked feature tracker on the round-15 frames reproduces the §E reviewer's finding:
- median rigid speed: 15.1 → 12.8 → 6.4 px/frame at g 126 → 127 → 128;
- median dx: +8.2 → +4.8 → -0.8;
- similarity-fit rotation: +0.29° → -0.32° → -0.86°.

That is a real two-frame catch-and-swing-back on the hull. My downgrade of must-fix 1 in round 15 was also too generous: the second tilt-up was real, and the deck-strip and optical-flow numbers I leaned on under-read the rotation in the top band. The QA-tech FAIL and the §E uphold were right.

**Round 16 method.** Take: take.mkv.partaa + partab joined to /tmp/s02a16.mkv (152 frames, first_g 48). All frames are extracted to /tmp/qa19_r16art/s02/gNNN.png. I viewed every frame g 115-165 (f115_140.jpg and f140_165.jpg, 150 px wide tiles, i.e. smaller than phone size). I tracked them with a sea-masked rigid-feature tracker: Shi-Tomasi corners outside teal water and foam, pyramidal LK with a forward/backward check, and a RANSAC similarity fit per frame. The script is /tmp/claude-0/qa16/track.py. It reports:
- median speed and dx/dy;
- rotation and scale;
- the median speed of the top band (y < 35 %);
- the median speed of the rail strips (x < 150 or x > 570, y 35-75 %).

**Rigid-feature table, round 16** (px/frame at 720 wide):

| g | 116 | 120 | 124 | 126 | 127 | 128 | 130 | 132 | 133 | 135 | 137 | 140 | 143 | 146 | 149 | 152 | 155 | 158 | 160 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| median speed | 12.2 | 10.0 | 10.4 | 8.4 | 7.8 | 7.0 | 5.2 | 4.4 | **3.8** | 4.0 | 4.7 | 5.4 | 5.8 | 6.0 | 7.2 | **7.3** | 6.6 | 6.6 | 7.0 |
| median dx | 4.4 | 2.0 | 3.3 | 3.7 | 3.3 | 3.1 | 2.3 | 1.4 | 0.8 | -0.3 | -0.8 | -1.5 | -2.5 | -2.3 | -2.6 | -2.9 | -2.3 | -2.2 | -1.6 |
| median dy | 4.6 | 5.9 | 2.9 | -0.1 | -1.0 | -1.4 | -1.8 | -1.3 | -0.9 | -0.7 | -1.4 | -2.6 | -3.4 | -2.9 | -1.8 | -0.3 | 1.1 | 4.4 | 6.2 |
| top band | 14.1 | 10.3 | 12.8 | 14.1 | 10.6 | 7.5 | 4.8 | 2.1 | **1.6** | 2.5 | 3.3 | 5.3 | 7.1 | 8.7 | 9.6 | 11.7 | 14.2 | 16.3 | **16.8** |

| Check | Status |
|---|---|
| 1. Hull catch or swing-back, g 115-165 | **Fixed.** The rotation runs +0.26° (g 115-121), +0.11° (g 126), -0.05° (g 127), -0.20° (g 129), -0.38° (g 133), -0.58° (g 136-137), then about -0.2° to 0°. That is a smooth zero crossing over about 6 frames. dx eases from +3.7 through 0 at g 134-135 to -2.5 over about 12 frames, with no reversal inside 2 frames and no speed spike at g 127. The upstream re-time (g 97-109, which differs from round 15) is also smooth: the dy zero crossing is spread over g 111-114. Frame by frame on the sheets, the stern swings and slides continuously through g 115-131 with no visible catch. |
| 2. One move on a phone? | **No: it is still "swoop, settle, then a second tilt-up".** g 131-139 is a near-hold. The tiles barely change, with the top band at 1.6-3.3 px/frame and the median at 3.8-4.7. From g 140 the camera tips up: the rail, sea and horizon slide in from the top (horizon at about g 150, sky at about g 158), and the top band climbs **1.6 → 16.8 px/frame (10x)** and the median **3.8 → 7.3 (+92 %)** by g 152-160. The image vertical motion also reverses twice (dy + → − at g 126, then − → + at g 153). The team's "tilt-up starts around g 127" is not visible in the frames: the top band is still decelerating until g 133. Compared with round 15 (median trough 4.3, top-band trough 3.1), the trough is now even deeper. The ease-out cannot start from the g 160 speed (about 7 median, about 17 top band) after dropping to 3.8 / 1.6, so §H.1 ("one continuous move with ease") is still broken. |
| 3. Regressions | **None.** g 48-96 are bit-identical to round 15. g 159-199 differ only by render noise (mean absolute difference about 0.6/255; g 158 is 3.6, the warp seam), so the landing, drift, acting, props and the s04 dissolve handle are unchanged. Colour: sat 0.634, luma 94.1 (G1 OK). Grounding and framing are unchanged. |

| Criterion | Score |
|---|---|
| Set | 8 |
| Light & colour | 8 |
| Composition / phone | 7 |
| Acting | 7.5 |
| Key moment (BIGZOOM + beat) | 6 |
| Match to refs (R5 continuous crane) | 7 |
| **Overall** | **7.25 on average, but the verdict is FIX: a blocking §H.1 defect is confirmed (upheld by §E)** |

**Must-fix (camera only, g 127-159; g ≥ 160 untouched).** The landing begins at g 160 with the camera already tilting up fast (top band about 17 px/frame, about 1.4°/frame of pitch). Because g 160 onward is frozen, the only monotone solution is to **have the tilt-up already running at about that rate from about g 128 onward**, instead of letting it decay to nearly nothing at g 133 and re-accelerating.

Concretely: the pitch rate should cross zero at g 120-127 (it does now), rise to about 1.0°/frame by g 130 and about 1.3-1.4°/frame by g 135, and then hold or fall gently into g 160. Translation keeps falling monotonically, as it does now.

Acceptance on the sea-masked tracker, g 128-160:
- the top-band speed never drops below about 10 px/frame;
- the median rigid speed never drops below about 6;
- neither rises more than 20 % after a local minimum.

If that pushes the horizon into frame too early, it is acceptable to let the g 160-176 tilt ease out a bit more slowly. Unfreezing the start of the landing is better than keeping a dead hold.

Not blocking: the captain's level chart arm in the shrug, the left-sail seams, the soft foreground planks.
