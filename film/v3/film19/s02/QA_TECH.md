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
