# s02 QA_TECH: FAIL
Shot 2, SHIP ship_aerial NOON, take g48-118 (handles 9+9), 6 fps + cuts g57/g110 +-3 checked. qa_auto: PASS (cuts report "no visible change" = expected, handle continues in 3D). No text, no black/magenta/blank frames, no frozen run, no pop, no blur.
## Issues
1. Whole take (in-shot g57-109): frame-diff median 2.04, p90 2.31 (re-measured 2.04 / 2.31) vs target >= 4 / >= 12. FAIL. Ship barely changes size or position in frame; the orbit/crane is not readable. Fix: raise pull to ~9-10 %/s with a real slide/crane (frame-visible travel >= 30 px/s), add the planned pull-back + rise so the ship visibly shrinks, and let the V-wake lengthen (plan row 17 look). Re-measure on a draft.
2. g48-118 (every frame): hard vertical seam / lighter rectangle in the sea below the ship at x ~435 px (y ~ 600-760 of 1280), a tile edge of the re-fitted sea grid or a glare patch. Reads as a render artifact. Fix: widen/overlap the sea grid or hide the patch (move the sun glitter reflection or the grid join out of frame).
3. g48-118: lower ~45 % of frame (y > 700) is flat empty teal; ship occupies 15 % of frame height. Composition weak for the lone-ship hook of "เรือเรือนเดียว"; the plan wants a high drift. Fix: lower the horizon / put the ship in the lower third and let more sea texture (swell/foam, FG gull) fill the bottom, or frame the pull-back so the ship moves down-frame.
4. meta.json: g1 = 110 is exclusive; plan g1 = round(3.65*30)-1 = 109 (shot_ranges 57-109 is right). g0 = 57 matches. Handles in/out 9/9 present. Note only: state the convention or set g1 = 109.

## Round 2: FAIL
Re-checked at 6 fps + cuts g57/g110 +-3 (take g48-118, handles 9/9 in meta). qa_auto PASS (cut "no visible change" = expected handle). No text, no black/magenta/blank, no frozen, no pop, no blur. Frame-diff (take.mkv, deliver.py method): median 3.87, p90 4.76 vs target >= 4 / >= 12.
Earlier issues: 1 NOT FIXED (diff), 2 FIXED (seam gone), 3 mostly FIXED (ship now ~45 % of frame height, orbit/pull readable), 4 note still true (g1=110 exclusive).
1. g57-109 (whole shot): frame-diff median 3.87 (< 4), p90 4.76 (< 12). Motion is a smooth uniform drift; no eased accent, nothing fast. Fix: raise pull to 9-10 %/s plus a faster slide/orbit (visible travel >= 50 px/s), or add a late eased 1.3x push (13-15 f) so p90 reaches 12; re-measure with deliver.py.
NOTES (not blocking): g48-63 overexposed white glitter patch at the left frame edge (x 0-30, y 100-300) fades by g73; g88-118 a gull is clipped by the left edge (wing, ~x 0-20); bottom ~30 % is still plain teal.

## Round 5: FAIL
Checked 6 fps + cuts g57/g110 +-3 (take g48-118), qa_auto PASS, no text/black/magenta/frozen/blur. Frame-diff (take.mkv, 90x160 grey bilinear, g58-109): median 3.81 / p90 18.07 (rule: median >= 4, p90 >= 10).
Earlier: R2-1 (diff) NOT FIXED on the median (p90 now OK); ship fully in frame throughout.
1. g57-109 (frame-diff): median 3.81 < 4. Fix: raise the mid-shot drift/orbit by about 10 % (or lift the pull speed) so the median clears 4 with margin; keep the late accent, re-measure.
NOTES: g48-75 blown-out white glitter patches at the left edge; gull clipped by the left edge g88-118 (not a key prop).

## Round 10 (director QA-tech): FAIL
Take g48-199 (joined parts -> /tmp/s02q.mkv, 152 frames, 720x1280 30 fps). Frames /tmp/qa19_r10c/s02/. 6 fps sheet plus every frame g147-154 and the swoop checked. Frame-diff (90x160 grey bilinear, pairs g58..g190): median 5.69, p90 18.62 (limits 4 / 10: OK), max 23.8 at g148.
Verified OK: ease-in from g57 (diff 1 to 4 over g58-90), one continuous move, no jump or pop, no black/frozen frames. Start g57: ship ~92 px = 7 % of frame height (limit 12 %), crew 1-2 px (under 5 %, but not really findable). The path goes through sails, shrouds and rigging; the hull wedge is only briefly seen (g~120-130, top-down deck, not a plain hull side). End is a medium on captain19 and astro19_c: chart is BLANK (no coast, no X), both faces puzzled/frowning, shrug g172-186, heads centre y ~470 (captain) and ~540 (astro), inside 450-760. No face over 35 %, nobody cut, feet have contact shadows, no mouths moving, colour sat 0.647 luma 89.
Issues:
1. g152 -> g153: DEAD STOP. Camera speed is at its peak (frame-diff 20-24, background strip 30.8) at g148-152, then 1.5 at g153 and 1.5-3 to g160. The spline arrives at full speed and halts in one frame: the same "stopped dead" failure as round 9 in a smaller form. The ease-out is missing; the table reaches u=1 at g152 while still accelerating. Fix: decelerate over g135-160 (the speed should fall 20 -> 4 over ~15 f), start the orbit from the arrival velocity and re-measure that no consecutive pair changes by more than ~4.
2. g116: speed dips to 3 between two peaks (20 at g106, 20 at g123), a near-stall mid-swoop. Smooth the key pose spacing so it is one hump, not two.
3. Peak frame-diff is 24 at g148 (target ~15-20), caused by issue 1.
4. Acting: the astro "head-scratch" g146-166 reads as holding/wobbling the quadrant at his head, not a free-hand scratch. The chart is blank so "upside down" cannot be seen at all; there is no visible turn of the chart. Shrug g172-186 is readable. NOTE, fix with issue 1 if re-rendering.
Blur judgement (qa_auto flag on g48-85): NOT blur. Laplacian variance is 11-17 % of the take median for g48-81, rising smoothly to 60 % at g85 as the ship grows, with no per-frame spikes: it tracks the amount of detail, not softness. The crop of g57 at 4x shows a crisp ship (sail panels, mast, deck, hull edge are pixel sharp, ~26 x 92 px) over flat gradient sea and sky; the low variance is flat sea and sky plus a tiny subject. Waive it.

## Override: qa_auto "suspected blur" on the s02 extreme-wide frames (QA_TEAM §E), round 10
- Two independent reviewers, QA-tech (Sonnet) and QA-art (Opus, see QA_ART.md "Override review: qa_auto blur flag (s02)"), both judged it a FALSE POSITIVE.
  - The horizon is a crisp 1 px edge, the yards and sail panels resolve to single pixels, and there is no defocus halo.
  - The low Laplacian variance comes from about 90 % smooth sea and sky with a tiny subject.
- The director agrees.
- Waived for g48-90 and g126-146.
- The soft deck texture (g150-199) stays on the polish list.

## Round 11 (director QA-tech): FAIL
Take g48-199 (joined parts -> /tmp/s02q11.mkv, 152 frames, 720x1280 30 fps); frames g48-199 in /tmp/qa19_r11/s02/ (f<g>.png). Sheets every 6 frames and every 2 frames over g160-190 checked. Frame-diff (ffmpeg bilinear 90x160 grey, pairs g58-190): median 9.1, p90 14.1, max 15.5 at g110 (team-reported 8.45 / 14.01 is close; my pairs include the ease-in). Limits median >= 4, p90 >= 10: OK. Peak <= 20: OK.
Verified OK:
- Ease-in is smooth: 2.3 at g58 rising to 15.5 at g110, with no stall.
- g58-125 is ONE hump (no dips, no pops).
- Slab at top right is GONE (g48-90 show only sea, sky and clouds).
- Colour: sat 0.630, luma 93.3 (range 71-117 per frame), inside 85-110.
- No black, blank or frozen frames; no pop.
- Start g57: ship ~7 % of frame height, findable.
- Medium landing: nobody cut, faces about 20-25 % of frame height, head centres y ~470-540 (inside 450-760), feet have contact shadows, nothing floating, no props through faces.
Issues:
1. EASE-OUT TOO SHORT (blocking). The camera holds 10-12 until g167 (11.1) and then stops: g168 9.9, g169 7.6, g170 5.3, g171 3.8, then a flat 4.1-4.8 orbit. It falls from about 11 to 4 in 4 frames, so it does not ease out over 10 or more frames. There is no single-frame drop from more than 10 to less than 3 (the floor is 3.8), but it is still a visible brake, the "stops dead" failure of rounds 9 and 10 in a milder form. The speed from the hump (15.5 at g110) down to g134 is gradual, but it then climbs again and stays at 8.2-11.9 through g167. The move is a plateau with a late second rise (8.2 at g134 to 11.9 at g165) rather than a clean fall. Fix: bring the table so that the speed starts to fall by ~g125 and reaches the orbit speed (~4) smoothly at g170 (e.g. 15 -> 11 at g140 -> 7 at g155 -> 4 at g170). The easing table should have u'(g) fall linearly over the last 30-40 frames, not stay near the peak until g167.
2. g134 dip: 8.2 vs neighbours 9.1 / 8.6 (about 90 %), so mid-move there is NO dip below 40 %; but g134 is the minimum of the shoulder before the second rise (g146-165). Folded into issue 1.
3. Acting NOTE (not blocking): captain's mouth is wide open ("O" shock) over g158-168, and again a half-open mouth at g~168-172. The brief says no mouth movement. It is a held shock expression, not talking; the director decides. Chart flip (g160-170) is hard to read at phone size: the chart is a pale slab with no visible header band. Both characters keep moving (scratch, shrug g181-189), nobody is still for more than 1.5 s.
Numbers: median 9.1, p90 14.1, peak 15.5 (g110), final ease-out 11.1 -> 3.8 over g167-171 (4 frames, needs 10+), luma 93.3, sat 0.630.

## Round 12 (director QA-tech): FAIL (camera ease-out still brakes at g170-176; everything else passes)
Take g48-199 (joined parts -> /tmp/s02q12.mkv, 152 frames, 720x1280 30 fps; frame index = g - 48). Frames in /tmp/qa19_r12/r12/ (f<g>.png, 360x640); sheets s1.png, s2.png, sheetA12.png, sheetB12.png checked. I measured camera motion separately from the actors: (a) mean abs frame-diff and textured-pixel Farneback flow (px/frame at 360 wide) in a region that EXCLUDES the character band (x 12-96 %, y 22-72 %); (b) the same on the bottom deck strip (y > 74 %, g130+, floor plane only); (c) LK feature tracks outside the character box (median |flow|). The top 15 % strip turned out NOT to be usable as pure background from g118: it is flat sail / sky (flow ~0) and then carries the near sail's strong parallax (frame-diff up to 20 at g170), so I did not use it for the verdict.

Whole-frame frame-diff (ffmpeg bilinear 90x160 grey, pairs g58-190): median 9.21, p90 14.39, max 15.6, min 2.3. Limits median >= 4, p90 >= 10: OK.
Luma 89.5 mean (per-frame 66.7-110.0), sat 0.646: OK (85-110).

Camera-speed profile, background only (px/frame at 360 wide; bgdiff = mean abs diff outside character band; flow = textured-pixel median flow outside character band; deck = textured flow on the bottom deck strip; LK = tracked-feature median):
| g | whole | bgdiff | flow | deck | LK |
| 100 | 12.7 | 26.6 | 9.5 | 10.9 | 11.1 |
| 112 | 15.5 | 25.0 | 12.4 | 13.4 | 8.7 |
| 120 | 13.8 | 21.5 | 7.0 | 6.6 | 6.8 |
| 128 | 11.4 | 16.4 | 11.3 | 14.8 | 11.4 |
| 136 | 8.5 | 9.8 | 4.0 | 13.2 | 3.5 |
| 144 | 9.3 | 8.6 | 8.0 | 8.9 | 8.0 |
| 150 | 11.0 | 10.2 | 7.5 | 8.7 | 8.7 |
| 156 | 10.8 | 10.7 | 6.1 | 6.9 | 5.9 |
| 160 | 10.9 | 11.8 | 5.8 | 5.8 | 7.0 |
| 164 | 8.5 | 10.5 | 4.5 | 3.5 | 6.3 |
| 168 | 9.2 | 11.8 | 5.3 | 2.6 | 7.0 |
| 170 | 9.2 | 12.0 | 5.4 | 2.2 | 7.2 |
| 171 | 8.1 | 11.0 | 4.7 | 1.9 | 5.7 |
| 172 | 7.9 | 10.1 | 4.3 | 1.5 | 5.0 |
| 173 | 6.7 | 8.6 | 3.4 | 1.3 | 4.3 |
| 174 | 5.8 | 6.7 | 2.6 | 0.9 | 3.0 |
| 175 | 4.0 | 4.3 | 1.8 | 0.8 | 2.0 |
| 176 | 2.5 | 2.1 | 0.6 | 0.7 | 0.6 |
| 177-181 | 2.7-3.2 | 3.2-4.8 | 0.7-1.1 | 0.9-1.2 | 0.7-1.1 |
Findings on the camera:
1. The deck-plane speed does decay smoothly: 14.3 (g157) -> 5.8 (g160) -> 3.5 (g164) -> 2.2 (g170) -> 0.7 (g176), the largest 1-2-frame fall in that stretch is 29 % (g160-162). That part of the team's argument holds: the floor is eased out over ~15-19 frames.
2. The mid/far background (sails, rigging, ship interior, sea windows) does NOT decay. Its speed re-rises from 8.6 (g144) to 12.0 (g170) in bgdiff (flow 4.0 at g136 -> 8.2 at g146, then 5.4 at g170 and flat 4.5-5.4 for g164-170, LK 5.9-7.2 flat g154-170), i.e. a plateau with a late rise, then it falls 12.0 -> 2.1 in six frames (g170-176): 11.0, 10.1, 8.6, 6.7, 4.3, 2.1. The last 1-2-frame steps are 4.3 -> 2.1 (-51 %, bgdiff), flow 1.8 -> 0.6 (-66 % in ONE frame; 2.6 -> 0.6 = -77 % over g174-176), LK 3.0 -> 0.6 (-80 % over 2 frames), whole-frame 5.8 -> 2.5 (-57 %). Same shape as round 11 (plateau, then a brake in ~6 frames to a near stop at g176), only the absolute step is smaller (about 2 px/frame at 360 wide on the last step). This is the orbit parallax of the rigging ending abruptly at the landing; it is camera, not acting (the region excludes the characters and the character-band diff is 2.5 at g176 anyway).
3. Earlier in the move the speed is not monotone either: 12.4 (g114) -> 6.5 (g122) -> 12.3 (g127, flow +89 % in 5 frames, also seen in LK 6.7 -> 14.0) -> 4.0 (g136) -> 8.2 (g147). Whole-frame and bgdiff are smooth there (bgdiff falls 21.3 -> 8.6 over g118-144 with no spike), so the g126-128 spike and g136 dip may be the textured-pixel set changing as the sail edge leaves frame; I count it as a note, not as the blocker.
Verdict on camera: FAIL on the literal rule (single-step brake > 50 % in 1-2 frames at g174-176 in the mid/far background, and no decay of that region from g144-170). Fix (cheap): start the orbit-speed fade at ~g158 and make the orbit/dolly angular speed fall to ~0 as a smoothstep landing exactly at g176 (so rigging parallax 5.4 -> 0 over >= 12 frames, e.g. 5.4 at g164, 3.5 at g168, 2 at g171, 0.8 at g174, 0.3 at g176), rather than keeping 5-7 until g170.

Other checks:
- Props PASS: the quadrant (astronomer) and chart (captain) are in hand in every frame g176-199 (checked every frame g170-199): no pop at g181-182 / g185-186 any more; chart is held out at the end of the captain's extended arm, quadrant hangs at the astronomer's hand at hip height. No frame-diff discontinuity (g176 2.5, g177 2.7).
- Shrug NOT met: astronomer's arms go out to both sides (reads as a shrug), but the captain extends only ONE arm (the chart arm, toward the astronomer); the other hangs. No open palms are readable at phone size on either; it is not symmetric.
- Shared look NOT met: g173-179 both heads stay front-on (no visible head turn toward each other). Brows: the captain's brows are not clearly up, the face is the half-lidded wavy-mouth "worried" look (g172-199) and the astronomer is the same. Held "O" shock g158-171 on the captain is allowed. These are acting misses, not blocking by themselves, but the team's stated change list says they were done.
- No character cut in half (both full figures from g125 on), faces about 20 % of frame height (< 35 %), head centres at y ~490-530 of 1280 at the end (inside 450-760), contact shadows on both characters, nothing floating, no props through faces.
- No pops, black frames or frozen runs (whole-frame diff min 2.3 at g58, never 0); both actors keep moving (blink, scratch, arm swing, bob) so nobody is still > 1.5 s.
- Start: ship ~7-10 % of frame height, findable; ease-in smooth.
Verdict: FAIL, single blocker = the camera/orbit brake at g170-176 and flat-then-late-rise background speed g144-170 (numbers above). Fix per item 3 of findings, then re-measure; acting items (symmetric shrug, head turn) should be fixed in the same re-render.

## Round 13 (director QA-tech): FAIL (landing now decays, but a one-frame camera jerk at g176 and a 4x re-acceleration g142-156 remain)
Take re-joined -> /tmp/s02q13.mkv (152 frames), frames in /tmp/qa19_r13/f/. Same three measures as round 12 (bgdiff = mean abs diff outside the character band; flow = textured Farneback outside the band; deck = bottom strip; LK = tracked-feature median; px/frame at 360 wide). My numbers do not match the team's "4.8-5.2 at g140-152": the background speed there is 3.0-9.7, not flat.
| g | whole | bgdiff | flow | deck | LK |
| 112 | 14.5 | 25.1 | 11.7 | - | 8.2 |
| 124 | 13.0 | 21.1 | 5.9 | - | 5.7 |
| 131 | 10.9 | 16.5 | 11.6 | 14.4 | 13.4 |
| 136 | 8.8 | 11.0 | 6.2 | 7.8 | 6.4 |
| 141 | 6.0 | 7.5 | 3.3 | 8.2 | 2.2 |
| 146 | 8.2 | 9.7 | 4.8 | 9.3 | 4.3 |
| 150 | 9.9 | 9.3 | 8.3 | 9.7 | 8.3 |
| 155 | 17.0 | 14.8 | 11.9 | 14.1 | 16.6 |
| 158 | 16.2 | 15.6 | 9.2 | 10.6 | 10.4 |
| 162 | 11.5 | 12.8 | 6.8 | 6.0 | 8.0 |
| 166 | 10.3 | 12.7 | 6.0 | 3.3 | 8.2 |
| 168 | 8.8 | 11.2 | 4.8 | 2.2 | 6.1 |
| 170 | 7.7 | 10.1 | 4.5 | 1.5 | 5.1 |
| 172 | 5.6 | 7.0 | 2.5 | 1.0 | 3.1 |
| 173 | 4.7 | 6.1 | 2.1 | 0.9 | 2.6 |
| 174 | 3.9 | 4.4 | 1.4 | 0.6 | 1.7 |
| 175 | 3.3 | 3.5 | 1.2 | 0.6 | 1.3 |
| 176 | 5.6 | 6.3 | 2.5 | 1.1 | 2.7 |
| 177 | 2.1 | 1.5 | 0.3 | 0.9 | 0.3 |
| 178-181 | 1.8-2.3 | 1.8-3.0 | 0.3-0.6 | 0.8-1.0 | 0.3-0.6 |
Findings:
1. GOOD: the ramp-down g158-175 is now smooth: flow 9.2 -> 6.0 (g166) -> 4.5 (g170) -> 2.5 -> 2.1 -> 1.4 -> 1.2 (g175); no 1-2 frame step above ~35 % in that stretch. Deck strip likewise (4.6 at g164 -> 0.6 at g174).
2. BLOCKER: g176 is a one-frame camera jerk. g175 -> g176 the speed goes back UP (flow 1.2 -> 2.5, bgdiff 3.5 -> 6.3, whole 3.3 -> 5.6, LK 1.3 -> 2.7) and then drops to 0.3 at g177 (-88 % in one frame; bgdiff 6.3 -> 1.5, -76 %). So the landing frame is an overshoot followed by a dead stop, a visible hitch at the exact landing, and it breaks the "no step > 50 %" rule (also 1.2 -> 0.3 = -75 % over g175-177). The slab of head motion (astronomer head turn) is inside the character band and excluded from these background numbers, so this is the camera/orbit key at g176, not acting.
3. The mid-move is NOT flat or monotone: flow 3.0 (g142) rises to 11.9 (g155) (whole-frame 6.0 -> 18.2 at g156, max of the take), LK 2.2 -> 16.6, i.e. a 4x re-acceleration over 13 frames after the speed had already dropped to ~3 at g140-142, then decays over g156-175. That is the same "late second rise" the round 11 and 12 notes asked to remove. It is camera (deck strip also 8.2 -> 14.3, bgdiff 7.5 -> 16.2).
Fix: remove the g176 overshoot (make the orbit/dolly parameter reach its landing value at g176 with zero slope, monotone: the key at g176 must not be past the g177 pose), and flatten the g142-156 re-rise so speed decays monotonically from the g131 peak (e.g. 6 at g136, 5 at g146, 4.5 at g156).
Other checks:
- Whole-frame frame-diff (pairs g58-190): median 8.45, p90 14.44, max 18.2 (g156), min 1.76. Limits OK (peak <= 20).
- Luma 89.6 (per frame 66.5-110.0), OK.
- Props PASS: quadrant and chart in hand in every frame g170-199 (checked g180-198 every 2); no pop.
- Shrug PASS: captain now raises both arms symmetrically, chart held in one hand, astronomer both arms out; shoulders up visible g184-190. Palms are small but the pose reads as a two-armed shrug.
- Shared look PASS (modest): heads angle toward each other g173-179; captain's eyes open and brows raised from g172 (visible at phone size). Held "O" g158-171 allowed.
- Usual checks PASS: nobody cut, faces ~20 % of frame height, heads at y ~490-530 of 1280, contact shadows, nothing floating, no props through faces, no black or frozen frames, nobody still > 1.5 s.
Verdict: FAIL on the camera only (g176 jerk + g142-156 re-rise). All other round 12 items are fixed.

## Round 14 (director QA-tech): FAIL (landing g158-182 is now clean; the camera still re-accelerates g140-152 and has surges at g115 and g129-130)
Take re-joined -> /tmp/s02q14.mkv (152 frames); frames in /tmp/qa19_r14/f/. Same measures as rounds 12-13 (px/frame at 360 wide; bgdiff / flow / LK all OUTSIDE the character band x 12-96 %, y 22-72 %; deck = bottom strip; "char band diff" = frame-diff inside that band).
| g | whole | bgdiff | char band diff | flow | deck | LK |
| 112 | 15.1 | 25.3 | 18.9 | 12.6 | - | 8.7 |
| 114 | 16.4 | 25.3 | 20.5 | 14.5 | - | 10.2 |
| 115 | 18.4 | 25.4 | 23.7 | 20.4 | - | 14.1 |
| 116 | 15.9 | 22.9 | 21.2 | 12.6 | - | 9.5 |
| 123 | 12.1 | 20.1 | 13.5 | 5.4 | - | 5.2 |
| 128 | 10.6 | 16.4 | 10.7 | 8.7 | - | 8.9 |
| 130 | 11.7 | 17.2 | 10.1 | 12.2 | 16.3 | 14.4 |
| 134 | 8.9 | 11.4 | 10.6 | 6.3 | 7.3 | 6.0 |
| 140 | 7.5 | 8.9 | 10.5 | 3.5 | 10.9 | 2.9 |
| 144 | 8.5 | 9.3 | 12.4 | 5.9 | 8.8 | 5.4 |
| 148 | 11.0 | 9.6 | 18.8 | 9.8 | 11.1 | 10.1 |
| 151 | 15.1 | 13.1 | 24.3 | 11.0 | 12.3 | 13.9 |
| 152 | 15.9 | 14.2 | 24.9 | 10.4 | 12.6 | 14.5 |
| 156 | 12.1 | 11.9 | 19.7 | 7.0 | 7.3 | 6.4 |
| 160 | 10.2 | 11.2 | 16.5 | 5.4 | 5.2 | 6.8 |
| 164 | 8.4 | 10.2 | 13.0 | 4.4 | 3.1 | 5.9 |
| 168 | 7.7 | 9.8 | 12.1 | 4.0 | 2.1 | 5.3 |
| 172 | 6.7 | 8.8 | 10.6 | 3.2 | 1.3 | 4.1 |
| 174 | 5.7 | 7.3 | 9.7 | 2.5 | 0.9 | 3.2 |
| 176 | 5.5 | 6.4 | 10.6 | 2.5 | 1.0 | 2.7 |
| 178 | 4.1 | 5.1 | 7.9 | 1.8 | 0.9 | 1.9 |
| 180 | 3.3 | 4.2 | 6.0 | 1.2 | 0.5 | 1.3 |
| 181 | 2.6 | 3.3 | 4.6 | 0.8 | 0.5 | 0.8 |
| 182-199 | 1.7-5.1 | 2.5-3.8 | 2.9-11.2 | 0.5-0.6 | 0.9-2.1 | 0.5-0.6 |
Findings:
1. GOOD, landing: from g156 the background decays monotonically 7.0 -> 5.4 (g160) -> 4.4 (g164) -> 3.2 (g172) -> 2.5 -> 2.5 -> 2.1 -> 1.8 -> 1.2 -> 0.8 -> 0.6 (g182), no step above 33 % per frame (largest 1.2 -> 0.8); no zero-then-nonzero, no overshoot (the g176 jerk of round 13 is gone). After g182 the drift is steady 0.5-0.6 (flow and LK agree), continuous and in the same direction. This part PASSES.
2. BLOCKER, the g140-153 hump is CAMERA, not acting. The team's rigging/sail points miss it. Tracked features OUTSIDE the character box move coherently: median vector (dx, dy) = (-2.1, 3.2) at g142, (-3.6, 7.8) at g147, (-5.0, 11.4) at g150, (-5.6, 11.8) at g152, then (-2.9, 4.8) at g156; top-of-frame features (rigging, sky: 4.2 -> 16.1 px/frame over g142-152) and floor features (8.8 -> 14.8) both ramp up together. Visually (sheet g144-159) the camera tilts up/pushes while the characters grow and the horizon and sails slide in: a real second move. Flow goes 3.5 (g140) -> 11.0 (g151) -> 5.4 (g160): a 3x re-acceleration over 11 frames. The character-band diff rises in step (10.5 -> 24.9) because the characters sit in the moving frame, which is why it looks like acting; it is not the cause. The head-scratch/chart-turn contribute some of the whole-frame hump but the background numbers rise by themselves.
3. BLOCKER, earlier surges (not monotone): one-frame spike at g115 (flow 14.5 -> 20.4 -> 12.6, LK 10.2 -> 14.1 -> 9.5, whole 18.4, the max of the take) and a second surge at g129-130 (flow 5.3 at g123-125 -> 12.2 at g130 -> 6.3 at g134, LK 5.2 -> 14.4 -> 6.0). The rise at g130 is the same size as the earlier peak, so "rise to 6.2 at g131-133 then monotone fall" does not describe the picture.
Fix: the camera path/zoom keys in g112-153 still contain the cusp at g115, a bump at g130 and the tilt-up at g143-153; build the move as one monotone ease (e.g. 12 at g112 falling to 4.5 by g156) and re-measure with background points that include the near deck and the top frame, not only far rigging.
Other checks (all PASS):
- Whole-frame frame-diff (pairs g58-190): median 8.47, p90 14.22, max 18.4 (g115), min 1.8.
- Luma 89.65 (per frame 66.5-110.0).
- Props: quadrant and chart in hand in every sampled frame g172-199 (every 2-3), no pop.
- Shrug: two-armed, symmetric, shoulders lifted g183-189; astronomer arms out both sides.
- Shared look: heads angle toward each other g173-179; captain's eyes open, brows raised from g172. Held "O" g158-171 allowed.
- Usual: nobody cut, faces ~20 % of frame height, heads y ~490-530 of 1280, contact shadows, nothing floating, no props through faces, no black or frozen frames, nobody still > 1.5 s.
Verdict: FAIL on camera monotonicity only (g115 spike, g129-130 surge, g142-153 re-acceleration). Landing and everything else PASS.

## Round 15 (director QA-tech): FAIL (g115 kink fixed and landing still clean, but a one-frame camera jump at g127 and a re-acceleration g137-148 of the mid/far background remain)
Take re-joined -> /tmp/s02q15.mkv (152 frames), frames in /tmp/qa19_r15/f/. Same measures as rounds 12-14 (px/frame at 360 wide; outside the character band x 12-96 %, y 22-72 %; deck = bottom strip y > 74 %, g130+).
| g | whole | bgdiff | flow | deck | LK | LK dx,dy |
| 105 | 13.4 | 26.8 | 15.1 | - | 9.5 | -0.9, 7.7 |
| 112 | 15.2 | 25.4 | 13.2 | - | 9.1 | -1.6, 6.4 |
| 115 | 15.3 | 24.6 | 12.2 | - | 8.7 | -1.4, 6.6 |
| 118 | 14.9 | 21.7 | 9.7 | - | 9.5 | -2.8, 8.1 |
| 122 | 13.6 | 21.0 | 6.5 | - | 6.5 | -2.8, 4.4 |
| 125 | 13.0 | 20.3 | 7.0 | - | 7.0 | -2.3, 5.2 |
| 126 | 13.7 | 20.4 | 9.2 | - | 9.6 | -1.1, 7.7 |
| 127 | 15.3 | 21.3 | 15.2 | - | 16.4 | +2.4, 15.5 |
| 128 | 11.4 | 16.9 | 12.4 | - | 13.4 | +2.9, 12.1 |
| 130 | 10.8 | 15.7 | 10.3 | 13.0 | 8.3 | +0.4, 5.1 |
| 132 | 13.1 | 16.1 | 9.6 | 13.0 | 11.8 | +5.8, 8.1 |
| 136 | 8.6 | 10.1 | 4.7 | 12.8 | 3.4 | -0.8, 2.1 |
| 137 | 8.8 | 10.1 | 4.4 | 12.4 | 3.8 | -1.5, 2.8 |
| 142 | 9.2 | 9.1 | 7.4 | 9.1 | 7.3 | -3.3, 6.3 |
| 146 | 10.3 | 9.5 | 8.7 | 9.8 | 9.1 | -3.7, 8.0 |
| 148 | 11.3 | 10.4 | 8.5 | 9.6 | 9.5 | -3.7, 8.0 |
| 152 | 11.7 | 10.9 | 6.8 | 8.4 | 7.0 | -4.1, 5.1 |
| 156 | 10.2 | 10.4 | 5.5 | 6.2 | 5.6 | -2.4, 4.0 |
| 160 | 9.8 | 10.8 | 5.1 | 5.0 | 6.5 | -2.4, 4.8 |
| 168 | 7.7 | 9.8 | 4.0 | 2.1 | 5.3 | -1.4, 4.7 |
| 172 | 6.7 | 8.8 | 3.2 | 1.3 | 4.1 | -1.0, 3.6 |
| 176 | 5.5 | 6.5 | 2.5 | 1.0 | 2.7 | -0.8, 2.4 |
| 180 | 3.3 | 4.2 | 1.2 | 0.5 | 1.3 | -0.6, 1.1 |
| 182-199 | 1.8-5.1 | 2.5-3.8 | 0.5-0.6 | 0.9-2.2 | 0.5-0.6 | -0.5..-0.3, 0.1-0.2 |
Findings:
1. FIXED: the g115 one-frame spike is gone (flow 12.4, 12.2, 12.1 smooth), and the old g129-130 kink is gone.
2. STILL BLOCKING: a one-frame camera jump at g127. Flow 7.0 (g125) -> 9.2 -> 15.2 (g127) -> 12.4 -> 10.2; LK 7.0 -> 16.4 and its direction flips (dx -2.3 -> +2.4); whole-frame 13.0 -> 15.3 (the take max) -> 11.4. The sheet g125-128 shows the framing of the ship shifting in one step between g126 and g127. It is a surge of 2x in two frames, then -25 % to -50 % back.
3. STILL BLOCKING: the mid/far background re-accelerates after the peak. Flow 4.4 (g137) -> 8.8 (g147) = +100 %; LK 3.4 (g136) -> 9.5 (g148) and global dy 2.1 -> 8.0 (dx -0.8 -> -3.7), bgdiff 8.8 (g144) -> 11.0 (g150) = +25 %, whole-frame 8.6 -> 11.8. Then it decays 8.8 -> 5.1 by g160. The near-deck strip alone is flat (12.8 at g136, 9.1-9.8 over g142-148, no climb), which is why the team's measure (6 deck + 3 horizon points) shows monotone; the sails/rigging/horizon, as seen in the picture, speed up again (limit was no climb-back above ~20 %). The climb is coherent global motion (dx, dy rise together), so it is camera, not gestures.
4. LANDING still PASSES, unchanged: flow 5.1 (g160) -> 4.0 -> 3.2 -> 2.5 (g176) -> 1.2 -> 0.8 -> 0.6 (g182), max step 33 %/frame; no overshoot; drift steady 0.5-0.6 with a constant direction (dx -0.5, dy 0.1) to g199.
Fix: remove the g126-127 key discontinuity (keys 125/126/127 do not agree, pose steps), and make the far-field speed fall from the g131 peak to ~g160 without the second hump at g137-148 (e.g. 9.6 at g132, 7 at g140, 6 at g148, 5.1 at g160); measure with horizon/sail points, not only deck.
Other checks PASS:
- Whole-frame frame-diff (pairs g58-190): median 8.96, p90 14.08, max 15.4 (g127), min 1.8.
- Luma 90.06 (per frame 66.6-110.0).
- Props in hand in every sampled frame g172-199; no pop.
- Shrug two-armed and symmetric with shoulder lift g183-189; shared head turn g173-179; captain's eyes open and brows raised from g172.
- Usual: nobody cut, faces ~20 % of frame height, heads y ~490-530, contact shadows, nothing floating, no props through faces, no black or frozen frames, nobody still > 1.5 s.
Verdict: FAIL (camera: g127 jump and g137-148 far-field re-acceleration). All else PASS.

## §E independent override review (round 15)
Reviewer: independent Opus override reviewer (QA_TEAM §E). I had not seen this shot before. I judged from the frames and my own measurements only.
Take re-joined from partaa + partab -> /tmp/s02ov.mkv (152 frames, 720x1280, 30 fps). Frames g110-165 extracted at full size to /tmp/qa19_ov/s02/gNNN.png (index = g - 48). Sheets: sheet120_132.jpg, full125_128.jpg, phone124_130.jpg (180x320 per frame), sheet132_164.jpg.
Methods:
- Rigid ship features tracked by hand-seeded NCC template chains at full size (px/frame at 720 wide).
- A per-frame similarity fit (RANSAC) on LK points with the SEA MASKED OUT (teal water, white foam and blue foam lines removed), so foam texture cannot enter it.
- Regional LK medians.
- The camera path itself, evaluated from shot.py (_tau_of, _land) outside Blender.

### (a) g127: REAL visible defect (a velocity hitch plus an aim reversal; not foam)
The sea is masked out of every number below, so foam cannot be the cause.
Rigid features on the ship, position (x, y) and per-frame displacement d:
| g | capstan (deck) | d | grate (main deck) | d | lantern (rail) | d | boat block (hull side) | d |
| 120 | 275.0, 770.0 | - | 435.0, 435.0 | - | 458.0, 572.0 | - | 520.0, 625.0 | - |
| 121 | 266.5, 780.3 | -8.5,+10.3 | 440.9, 424.3 | +5.9,-10.7 | 465.2, 568.8 | +7.2,-3.2 | 528.7, 624.8 | +8.7,-0.2 |
| 122 | 258.4, 790.8 | -8.1,+10.5 | 447.6, 413.2 | +6.7,-11.2 | 472.5, 565.9 | +7.3,-2.9 | 538.2, 624.7 | +9.5,-0.1 |
| 123 | 249.0, 802.9 | -9.4,+12.1 | 455.2, 401.9 | +7.6,-11.2 | 481.1, 562.8 | +8.6,-3.1 | 547.8, 625.0 | +9.6,+0.3 |
| 124 | 237.4, 815.1 | -11.6,+12.1 | 462.8, 390.8 | +7.6,-11.1 | 489.2, 559.7 | +8.1,-3.0 | 558.7, 625.2 | +10.9,+0.1 |
| 125 | 225.3, 828.9 | -12.1,+13.9 | 470.0, 379.3 | +7.2,-11.6 | 497.3, 556.4 | +8.2,-3.4 | 571.0, 625.1 | +12.3,-0.1 |
| 126 | 214.1, 846.9 | -11.2,+18.0 | 477.5, 366.6 | +7.5,-12.7 | 506.6, 551.8 | +9.2,-4.6 | 585.0, 624.4 | +14.0,-0.7 |
| 127 | 218.2, 877.9 | **+4.1,+31.0** | 481.2, 354.6 | +3.7,-12.0 | 518.1, 546.1 | **+11.5,-5.7** | 603.3, 620.2 | **+18.2,-4.2** |
| 128 | 215.7, 896.1 | -2.5,+18.1 | 476.7, 351.4 | **-4.5,-3.3** | 523.3, 541.7 | +5.2,-4.3 | 614.2, 614.6 | +11.0,-5.7 |
| 129 | 211.9, 909.0 | -3.8,+13.0 | 471.5, 351.0 | -5.2,-0.3 | 526.4, 538.7 | +3.1,-3.1 | 622.7, 609.5 | +8.5,-5.1 |
| 130 | 209.0, 925.0 | -3.0,+16.0 | 467.2, 350.9 | -4.3,-0.1 | 530.0, 535.6 | +3.6,-3.1 | 632.8, 603.2 | +10.0,-6.3 |
(g131+ capstan and boat-block chains are lost under the sail tip and the frame edge, so they are not used.)

Ship-only similarity fit, per frame (sea masked):
| g | image rotation (deg/frame) | median point speed (px/frame) | median dx |
| 124 | +0.56 | 12.4 | +7.7 |
| 125 | +0.52 | 13.3 | +7.8 |
| 126 | +0.33 | 13.2 | +8.4 |
| 127 | -0.33 | 12.5 | +3.9 |
| 128 | -0.86 | 6.0 | -1.0 |
| 129 | -0.83 | 4.7 | -1.5 |

Camera path from shot.py, per frame:
| g | tau step | pitch rate (deg/frame) | yaw rate (deg/frame) |
| 125 | 1.15 | -0.67 | +0.50 |
| 126 | 1.28 | -0.54 | +0.33 |
| 127 | **1.65** | +0.09 | -0.35 |
| 128 | 1.09 | +0.80 | -0.91 |
| 129 | 0.87 | +1.04 | -1.03 |

Reading:
- The hull does not jump in position: no frame moves 2-3x its neighbours.
- But g127 is a one-frame overshoot followed by a hard brake. Rigid-feature speed is 1.3-1.7x the neighbours at g127. At g128 it drops by 40-75 % (grate dy -12.0 -> -3.3; lantern 12.9 -> 6.8 px). The x direction flips (capstan dx -11.2 -> +4.1 -> -2.5; grate dx +7.5 -> +3.7 -> -4.5).
- The camera aim reverses in pitch and in yaw within 2 frames, while the warp gives g127 a 1.65-frame time step against 1.28 and 1.09 either side.
- In the phone-size flip g124-130, the hull's clockwise swing stops and swings back between g126 and g128. It reads as a catch or bump in the middle of the fastest part of the swoop.
- QA-art's "foam noise" reading does not hold: the effect is on the deck, rail and hull with the sea masked out.

### (b) g137-152: REAL second acceleration; breaks §H.1 "one continuous move with ease"
Ship-only median point speed (sea masked), px/frame at 720 wide:
| g | 132 | 134 | 136 | 137 | 138 | 140 | 142 | 144 | 146 | 148 | 150 | 152 | 154 | 156 | 158 | 160 |
| speed | 6.7 | 4.5 | 4.3 | **4.2** | 4.6 | 5.2 | 5.2 | 5.4 | 6.1 | 7.4 | 7.4 | **7.8** | 7.6 | 7.2 | 7.6 | 6.9 |
The climb-back from the g137 trough is +86 %, against the director's ~20 % limit.

Regional speed, top frame (y < 35 %: sail, rigging, then horizon/sea), px/frame:
| g | 135 | 137 | 140 | 142 | 145 | 148 | 150 | 152 | 156 | 160 |
| speed | **1.6** | 4.3 | 9.9 | 12.1 | 15.5 | 17.6 | 18.4 | **18.9** | 18.1 | 16.6 |
dx stays at -4 to -6 and dy rises from 0 to +18: one coherent downward slide of the whole top frame, which is the camera tilting up. It is not the head-scratch, which starts at g146.
Near rail / deck sides (y 35-75 %, outside the cast): 10.6 (g130) -> 4.7 (g141) -> 3.7 (g145) -> 5.1 (g151) -> 6.0-7.2 (g153-160). This also dips, then climbs again.

Camera path from shot.py:
- Translation speed falls monotonically: |dloc| 1.28 (g132) -> 0.68 (g137) -> 0.41 (g147) -> 0.20 (g160).
- Angular speed of the aim falls to 0.64 deg/frame at g133, then climbs to 1.0 (g137), 1.37 (g142), 1.52 (g145) and 1.65 (g151). That is **+158 %**, held at 1.4-1.6 deg/frame until g157.
- Pitch goes from -58.7 deg (g127) to -18.4 deg (g160), with the tilt-up concentrated in g137-160.
- The round-14 warp measure (6 deck points + 3 horizon points at y = 300 D) under-weights this rotation, which is why the team's numbers read monotone.

Visually (sheet132_164.jpg), g132-138 is a near-hold: the framing barely changes. From g140 the camera visibly tips up: the horizon, sea and rail slide in from the top, and the move peaks again around g150-156. On a phone this reads as "swoop, settle, then a second tilt-up move", not one swoop with a breath. The trough (4.2) drops below the speed the landing starts from at g160 (6.9), so this cannot be an ease-out.

### Decision: UPHOLD the QA-tech FAIL. No override.
- (a) g127: REAL visible defect.
- (b) g137-152: REAL second acceleration that breaks §H.1.
- The landing g160-199 was not re-judged.

Root cause (one cause for both points): the aim pitches DOWN to -58.8 deg at g126 and then back UP. The down-to-up reversal is squeezed into 2 frames at g127, amplified by a time-warp kink (tau step 1.65 against 1.28 and 1.09). Most of the following up-pitch is then left until after g137, which produces the second hump.

Minimal fix (camera only, g112-159; leave g >= 160 exactly as it is):
1. Remove the g127 kink by smoothing the _TAU2 increments over g120-134 so the per-frame tau step changes smoothly, with no 1.65 spike.
2. Make the aim's pitch and yaw rates cross zero over at least 8 frames, not 2. The cheapest way is to actually switch on the Gaussian time smoothing in cam_rest: `w` is hard-coded to 0.0, so the sigma-3 smoothing its docstring describes never runs. Blend it in over g112-128 and fade it out before g156, so g >= 160 stays bit-identical.
3. Re-time g128-159 so that the TOTAL image speed of the ship falls monotonically from the g125-127 peak (~12.5 px/frame at 720 wide) to the g160 value (~6.9). Total means rotation included: the top-frame sails/rigging and the rail, not only deck and far-horizon points. Two conditions must hold:
   - no trough below ~7 between g128 and g160;
   - no rise of more than 20 % after any local minimum.
   In practice: start the tilt-up right after g127 at about 1.0 deg/frame and keep the angular rate steady or falling (about 1.3-1.4 deg/frame into g160), instead of 0.64 deg/frame at g133 climbing to 1.65 deg/frame at g151.
4. Re-measure with the sea masked out (ship-point similarity fit plus top-band and rail medians).

## Round 16 (director QA-tech): FAIL (aim reversal fixed; the second move g133-152 remains)
Take re-joined -> /tmp/s02q16.mkv (152 frames); g110-165 extracted at 720x1280 to /tmp/qa19_r16b/s02/ and the §E scripts re-run on them (copies in /tmp/qa19_r16b/sc/: reg.py regional LK, sim.py sea-masked ship-only similarity fit, stub.py camera path from the current shot.py). Rigid-feature NCC tracks were not re-seeded (feature positions changed), I relied on the sea-masked similarity fit, regional LK and the path.
(a) Aim reversal / step in g120-135: FIXED. Camera path from shot.py: pitch rate -0.75 (g120) -> -0.44 (g125) -> -0.15 (g127) -> -0.03 (g128) -> +0.16 -> +0.27 -> +0.39 (g131) -> +0.56 -> +0.71 (g134) -> +0.87 (g136): it crosses zero over ~8 frames, no 2-frame reversal; yaw rate +0.36 -> 0.03 (g127) -> -0.14 -> -0.51 (g132), smooth; tau step 1.11-1.17 over g119-130 (no 1.65 spike); |dloc| 2.07 -> 1.17 falls monotonically. Sea-masked ship fit, median point speed px/frame at 720 wide: 9.5 (g122), 9.0 (g125), 8.0 (g126), 7.5 (g127), 6.8 (g128), 5.9, 5.0, 4.7 (g131): monotone with no spike, rotation +0.28 -> -0.03 -> -0.28 deg/f smooth. Frames g122-134 (sheet a.png) show a continuous swing, no catch. Whole-frame diff has no step (14.3 g110 ... 12.5 g125, 11.1 g128, 9.4 g131).
(b) Second move before g160: STILL THERE.
| g | ship-only speed (720w) | top band <35 % (LK) | deck >75 % (LK) | mid-sides (LK) | whole-frame diff | path ang rate deg/f | |dloc| |
| 123 | 9.8 | - | - | - | 13.7 | 0.63 | 1.74 |
| 128 | 6.8 | - | - | - | 11.1 | 0.08 | 1.31 |
| 131 | 4.7 | 3.2 | 21.4 | 6.6 | 9.4 | 0.45 | 1.11 |
| 133 | 3.5 | 1.4 | 19.8 | 5.8 | 9.4 | 0.62 | 0.99 |
| 136 | 4.1 | 2.8 | 15.7 | 5.8 | 8.1 | 0.92 | 0.83 |
| 140 | 5.2 | 5.2 | 12.1 | 3.7 | 7.2 | 1.22 | 0.67 |
| 144 | 5.9 | 7.8 | 10.3 | 5.8 | 7.7 | 1.50 | 0.52 |
| 148 | 6.5 | 9.4 | 8.5 | 3.7 | 9.2 | 1.64 | 0.42 |
| 152 | 7.3 | 11.4 | 8.2 | 2.2 | 9.1 | 1.65 | 0.33 |
| 156 | 5.3 | 14.7 | 6.1 | 4.0 | 8.4 | 1.55 | 0.26 |
| 160 | 6.9 | 16.9 | 9.3 | 6.8 | 9.4 | 1.34 | 0.20 |
Ship-only speed trough 3.5 at g133 -> 7.3 at g152 = +109 % (limit 20 %); top band (sails/rigging) 1.4 -> 16.9 (12x, one coherent downward slide, dx -4 to -5, dy 0 -> +16: the tilt-up); mid-sides trough 0.2 at g154; whole-frame diff trough 7.2 (g140) -> 9.7 (g158) = +35 %. So the team's rigid-feature figure (25 -> 16 -> 29) reading is right in kind: it is a visible second move, i.e. (b) exists. The team's explanation (rotation adds image speed while translation falls) is accurate but is exactly the problem: translation falls fast (|dloc| 2.07 -> 0.33) while the angular rate collapses to ~0.1-0.6 deg/f at g128-133 (the zero crossing) and only then climbs to 1.65 at g148-152, so the sum dips at g133 and climbs back. The zero crossing is too late (g128): it falls just when translation image speed is already dying.
Concrete schedule to resolve (camera only, g108-160; g160+ unchanged, the g160 values stay: pitch +1.31, ang ~1.34 deg/f, |dloc| 0.20):
1. Move the pitch-rate zero crossing EARLIER, to ~g112-116, where the translation image speed is still 25+ px/f and hides the reversal: pitch rate -0.87 (g109) -> -0.3 (g111) -> 0 (g114) -> +0.3 (g117) -> +0.6 (g120) -> +0.8 (g124) -> +0.95 (g130) -> +1.05 (g136) -> +1.15 (g142) -> +1.25 (g150) -> +1.31 (g160). Keep yaw rate magnitude 0.3-0.5 through the same span (do not let it go to 0 and back).
2. Result: the angular rate (image speed from rotation) never drops below ~0.6-0.8 deg/f after g117 and rises slowly to 1.3, so ship-only speed = falling translation + rising rotation stays within +-15 % of ~7-8 px/f (720 w) from g128 to g160 instead of 3.5 -> 7.3. If the director prefers to keep the zero crossing at g124, the alternative is a slower tilt-up: hold the angular rate at >= 0.8 deg/f from g128 (do not let it dip to 0.08) and cap it at 1.34 (the g160 value) with NO rise above that, i.e. pitch rate 0 (g124), +0.8 (g128), 1.0 (g134), 1.15 (g142), 1.25 (g150), 1.31 (g160); this keeps the trough above ~6 and the climb-back below ~20 %.
3. Re-measure with the same sea-masked sim.py fit plus reg.py top-band and mid-side medians; targets: ship-only median monotone non-increasing within 20 % from g124 (9.5) to g160 (6.9, no trough below ~6), top-band speed rising smoothly without a flat 1.4-2.8 hold at g132-136.
Other checks PASS:
- Whole-frame frame-diff (pairs g58-190): median 8.13, p90 13.68, max 14.55, min 1.80 (limits median >= 4, p90 >= 10).
- Luma 89.6 (per frame 67.4-110.0).
- Props: g160+ is unchanged from round 14; quadrant and chart in hand in every sampled frame g170-199 (sheet p.png), no pop.
- Shrug two-armed and symmetric g183-190, shared head turn g173-179, captain's eyes open with brows raised; held "O" g158-171 allowed.
- Usual: nobody cut, faces ~20 % of frame height, heads at y ~490-530, contact shadows, nothing floating, no props through faces, no black or frozen frames (min diff 1.8), nobody still > 1.5 s. Landing g160-199 still clean (unchanged).
Verdict: FAIL (single blocker: the second move g133-152; the g127 aim reversal is fixed).

## Round 17 (director QA-tech): FAIL on the written acceptance (narrowly: ship-only floor g139-157 and climb-back +35-39 %); the picture itself reads as ONE continuous push, no stall
Take re-joined from take.mkv.part* -> /tmp/s02q17.mkv (152 frames); I extracted my own frames to /tmp/qa19_r17/s02/gNNN.png (g48-199; g130 byte-identical to /tmp/qa19_ov) and ran film/film19/qa_tools sim.py, reg.py, stub.py with FRAMES=/tmp/qa19_r17/s02/. stub.py only evaluates the raw `_land` path, NOT `_aim_design` (the new pitch schedule), so I also called `_aim_design` directly to get the real aim. My sim.py numbers equal the coordinator's.
Ship-only median point speed (sea masked, px/frame at 720 wide, sim.py mag_med):
| g | 119 | 122 | 125 | 128 | 130 | 132 | 134 | 136 | 138 | 140 | 142 | 144 | 145 | 146 | 148 | 150 | 152 | 154 | 156 | 158 | 160 | 161 | 162 | 164 |
| ship | 15.7 | 18.8 | 17.5 | 13.1 | 10.1 | 8.5 | 7.6 | 7.5 | 6.7 | 5.6 | 5.3 | 5.1 | 5.1 | 5.5 | 5.5 | 5.6 | 6.3 | 6.1 | 5.8 | 6.9 | 6.9 | 7.1 | 6.9 | 5.4 |
Top band y<35 % (reg.py): 7.9 (g130), 6.7 (g133), 7.0 (g134), 7.9 (g136), 9.2 (g138), 10.8 (g140), 12.4 (g144), 13.5 (g148), 14.3 (g152), 15.6 (g155), 16.9 (g160), 18.8 (g161): monotone rise from g133. Deck strip 36.7 (g130) -> 22.5 (g140) -> 15.4 (g146) -> 12.1 (g152) -> 9.1 (g159): monotone fall. Mid-sides: 21.8 (g133) -> 8.2 (g136) -> 4.1 (g144) -> 1.2 (g151) -> 1.8 (g153) -> 5.2 (g155) -> 6.8 (g160) (a dip, minor, the sail edge leaving the side regions).
Whole-frame frame-diff (pairs g58-190): ffmpeg bilinear 90x160 grey: median 9.00, p90 19.34, max 20.62 (g116), min 1.80; cv2 INTER_AREA on full-res frames: median 10.01, p90 22.39, max 23.87, min 2.14. Both well over median >= 4 / p90 >= 10. Note the max 20.6 is just over the old ~20 peak cap, but it is a plateau (19.4-20.6 over g110-122), not a pop; per-frame ratio extremes 0.70-1.41 (g88/g89, g182/g184, the acting, not camera). g140-158 plateau 8.8-9.9, no trough/hump.
Luma 91.1 (per frame 66.6-109.8), sat 0.656. Blur: Laplacian variance median 364 (min 29 on the flat sail), g128 200 / g136 220 / g144 259 / g152 280 / g160 280 in the descent: no blur issue.
Aim (real, from `_aim_design`): pitch rate -1.61 (g105) ... -0.68 (g110) -> -0.20 (g113) -> 0.00 (g115) -> +0.40 (g118) -> +0.67 (g120) -> +0.93 (g123) -> +1.10 (g127) -> +1.23 (g134) -> +1.30 (g142-156) -> +1.31 (g157-161); yaw rate +0.37 (g110) -> +0.26 (g118) -> 0.00 (g126.5) -> -0.49 (g138-142) -> -0.26 (g160). The pitch reversal takes ~9-10 frames (g110-119) and the yaw reversal ~20: >= 8 frames, no step. One small rate notch: -0.73 (g108), -0.28 (g109), -0.68 (g110): a 0.4 deg/f wobble at g109 from the knot smoothing; not visible in the images. |dloc| falls monotonically 3.95 (g108) -> 0.20 (g160).
Rule check (written acceptance g128-160):
1. No aim reversal in < 8 frames: PASS.
2. Ship-only median >= ~6: FAIL for g139-148 and g150-151, g155-156 (5.1-5.9; lowest 5.1 at g144-145). Frames g128-138 (13.1 -> 6.7) PASS.
3. Top band >= ~10: FAIL for g130-139 (6.7-9.6); PASS from g140 (10.8). It is monotone and rising from g133, so it is a late start of the top-band motion rather than a dip.
4. No climb-back > 20 % after a local low: FAIL by the letter. Low 5.1 (g144-145) -> 7.1 (g161) = +39 % (6.9 at g158-160 = +35 %; 5.1 -> 6.3 at g152 = +24 %); smaller local lows 5.3 (g142) -> 5.6 (g147). It is a slow ramp (about +0.12 px/f per frame, ~2 %/frame over 16 frames), not a step.
Does it still read as a stall followed by a second move? Frame sheets g126-160 every 3 frames and g138-160 every 2 frames (/tmp/qa19_r17/seq.png, seq2.png), played in order: NO. The round-16 pattern (dead hold 3.5 at g133 then a visible second tilt-up to 7.3, +109 %) is gone. Speed falls smoothly and fast from the fast descent, flattens to a steady 5-6 at g140-157 with the tilt-up already visibly running (sail slides off the top, horizon and rails come in from g138), the characters grow steadily, the top band rises monotonically, and the whole-frame diff stays flat at 9-10. There is no frame where the picture stops moving and then re-starts; the residual +35-39 % is a gentle 16-frame swell that rejoins the unchanged g160 tail (6.9-7.1). It reads as one continuous push with a slightly slow middle.
Verdict: FAIL on the written acceptance, rules 2-4 above, with the failing frames exactly g130-139 (top band < 10), g139-151 and g155-156 (ship-only < 6) and g144/145 -> g158-161 (+35-39 %). I am not loosening the rule myself: the director can decide to waive the ~20 % climb-back (my own approximate guidance, written for the round-16 hold) given the visual result.
Fix I would ask for (small, camera only, g132-156; g160+ unchanged): the ship-only speed is rotation dominated here (about 4 px/f per deg/f of pitch rate, translation is down to 0.5 -> 0.2), so lift the pitch-rate plateau slightly and let it relax into the g160 value instead of holding 1.30: knots 130 +1.2, 136 +1.35, 142 +1.5, 150 +1.5, 156 +1.4, 160 +1.31. Expected ship-only median ~6.0-6.4 over g140-156 (floor >= 6, climb-back to 6.9 at g160 about +8-15 %) and the top band reaches >= 10 about 3 frames sooner. Re-measure with sim.py/reg.py (and `_aim_design` for the aim). If the director prefers not to re-render, the alternative is a written waiver of rules 2-4 for g130-157 on the strength of the playback evidence above.
Other checks (all PASS): props in hand in g160-199 (g >= 160 bit-identical to round 14/16; sampled frames show quadrant and chart in hand), two-armed symmetric shrug g183-190 and shared head turn g173-179, nothing floating, contact shadows on both characters, faces about 20 % of frame height (Laplacian and sheets show no blur), nobody cut in half, heads at y ~490-530 of 1280 at the end, no black or frozen frames, landing g160-182 smooth (unchanged).
