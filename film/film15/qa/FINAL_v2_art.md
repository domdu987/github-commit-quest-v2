# FINAL gate v2 — QA-art (opus), film 15 "ไอ้ปลาดิ้น" (fosbury_v2.mp4, 69.8 s, 2095 frames)

Material: fosbury_v2_2fps_1..4.jpg, fosbury_v2_phone.jpg, fosbury_v2_vs_film2.jpg, ref_shorts R2/R5 sheets,
plus frames extracted from fosbury_v2.mp4 (single frames g521-525, g735, g770, g822, g830-845, g842, and
0.1-0.3 s steps around 2.5, 16.6-18.8, 36.3-38.3, 41.6, 46.4-46.7, 55.7-56.4, 59.5-60.05, 60.8-63.2, 66.8-69.6),
and a per-frame scan of the whole film for flat purple pixels.

## VERDICT: FIX

The film is well shot and the story reads. Three problems block release: purple placeholder slabs flash
in six frames of T2, the camera passes through an official twice in T4, and the 1972 bar crosses a face.
All three are local re-renders (T2, T4, T7). The grade, framing and story structure do not change.

### Blocking fixes
1. **Purple placeholder slabs in 6 single frames of T2 (Team 2).** A flat violet rectangle (an
   untextured or missing-material plane) pops in front of the coach, the newspaper reader or the set:
   - g522 (17.40 s)
   - g524 (17.47 s)
   - g735 (24.50 s, under the flash; covers about 70 % of the frame)
   - g770 (25.67 s, behind the newspaper)
   - g822 (27.40 s, a thin strip)
   - g842 (28.07 s, a big block behind the reader, 14 % of the frame)

   The per-frame scan finds no other frames. These break §G.2 (slabs slicing characters) and §A.1
   (magenta/blank frames). They show as a visible flicker even at 30 fps. Fix: find the object in the T2
   scene that toggles visibility (probably the newspaper or flash card proxy) and remove it or give it a
   material. Then re-render T2 (g489-861) and re-run the purple scan.
2. **The camera flies through an official twice in T4.** At 36.6-36.75 s (about g1098-1102) and again at
   38.2-38.35 s (about g1146-1150), an out-of-focus official in a navy or red blazer fills the frame. At
   36.7 s his face and eye fill more than 60 % of the frame height. This is an unplanned extreme close-up
   (§G.3: face <= 35 %) and a person cut by the frame edges. Fix: move the two officials beside the
   standard out of the side-tracking camera path, or lift the camera above their heads, and re-render
   T4 35.27-39.5.
3. **The bar passes through a face in 1972 (T7).** At 61.5-61.7 s (about g1845-1851), the red-haired
   jumper's face is behind the bar, and the red and white stripe crosses his eyes (§G.2: no bar through a
   face). At 62.0 s his head shows over the bar with no visible body, which reads as a floating head (the
   film-15 v1 complaint). Fix: time or offset his flop so that his head passes over the bar, or cross
   behind it from a camera angle where his torso stays visible, and keep his body in view when he lands.
   Re-render T7 60.15-63.0.

### Coordinator item: g833-841 (27.77-28.03 s), the soft frames QA-tech flagged
**Acceptable, not blocking.** Laplacian variance falls only from about 1870 (g826-832) to about 1700-1750
(g833-841). That is a 7-9 % drop, far above the 60 %-of-median blur threshold. Side by side, the frames look
the same at phone and full size: the wide bleacher shot with the coach, the reader and the boy is sharp. The
drop comes from a slight camera drift, not a defocus. The real defect in that stretch is **g842**, the
purple slab (fix 1). Its sharpness of 1383 is what made the run look soft.

## §G — answers
- **Nothing floats (checked on every 0.5 s tile of the phone sheet and the 2 fps sheets).**
  - Every grounded character has a contact shadow: 1963 boys and coach (3-28 s), Mexico runway (33-44 s),
    mat landings (53-57 s), podium (58-59 s), 1972 bench (65-67 s).
  - Airborne bodies appear only over the bar or pit: 5.5, 12.5-13.5, 37.9-39.5, 45-53, 60.8-62.7, 67.5 s.
  - Exception: the 1972 head at 62.0 s (fix 3).
  - The coach buried to the chin in sawdust (68-69.8 s) is intended, and the mound reads as a solid pile.
- **No bar or pole through a face:** OK everywhere except 61.5-61.7 s (fix 3). In the reveal (46.4-50 s),
  Dick's head and legs hang below the bar on the far side, and the bar crosses only his torso, as planned.
- **No grey slabs:** no grey ones, but there are purple slabs at g522, g524, g735, g770, g822 and g842
  (fix 1).
- **Faces <= 35 % except the 3 planned close-ups:**
  - Close-up 1: about 22.9-23.6 s (coach "ดูเอง!", ends in the whip blur at 23.5).
  - Close-up 2: 41.0-41.8 s (coach "ปลาดิ้นก็ได้ / แค่นี้แหละ!", face about 45 %).
  - Close-up 3: 59.85-60.1 s (coach jaw-drop with round glasses). It is very short and falls between
    the 2 fps tiles, so the phone sheet shows only blur at 59.5. It still plays as a punch.
  - Unplanned: 36.6-36.75 s and 38.2-38.35 s (fix 2).
  - Otherwise the largest faces are about 25-30 % (coach medium shots at 20.0-23.0 s, Dick at 47-50 s).
- **At least half wide or medium-wide:** yes, about 70 % of the running time:
  - 0-16 s: town and track wides.
  - 17-22 s and 25-29 s: bleacher medium-wides.
  - 30-40 s: stadium.
  - 42-46 s: runway.
  - 54-59 s: mat and podium wides.
  - 60-67 s: 1972 stadium and the Medford track.

  The tighter stretches are 20-24 s (coach), 25-27 s (newspaper insert), 41 s, 47-53 s (the planned
  arch hold) and 68-69.8 s (sawdust push-in).
- **Nobody cut in half by a frame edge:** OK, apart from the planned over-the-shoulder at 16.3-17.2 s (Dick's
  back at the left edge, which reads as framing) and fix 2. The 1972 jumper entering at the right edge at
  60.8-61.0 s is mid-flop and in motion, so it is acceptable.
- **Colour (measured: saturation 0.692, vivid 74.9 %, luma 97.9):** PASS. This is well above the targets of
  saturation >= 0.47 / 0.50 and vivid >= 45 %, and luma is inside 85-110. There is no peach haze: deep blue
  sky in 1963, night blue with white floodlight beams in 1968.

## §G.4 — "Is it as vivid, wide and grounded as film 2?"
**YES**, on the side-by-side sheet. It is more vivid than film 2, and just as wide: town and stadium
establishing shots and bleacher wides. It is grounded except for the three local defects above, which must
be fixed anyway.

## §H — BIGZOOMs, angles, set
- **BIGZOOM 1, 0.0-4.4 s (Medford):** it starts bird's-eye above the town grid (red roofs, cars, pines, the
  school, the red track), with the athletes as specks on the field (under 5 % at 0.2 s). It descends past
  the pines and the bleachers (TRACK & FIELD and HIGH JUMP signs, 2.0-2.5 s), and ends medium on Dick and a
  straddler at 4.3 s. Dick is about 50 % of the frame height. The move is continuous with ease. PASS.
- **BIGZOOM 2, 31.0-35.3 s (Mexico City):** the camera dissolves from the MEXICO 68 poster (30.5 s) to
  bird's-eye above the night city and the floodlit bowl (31.1 s). No character is findable yet, so it
  starts well under 5 %. It dives through the beams and the crowd (32-33.5 s) to the runway, and ends medium
  on Dick with the 2.24 m board at 35.2 s. Dick is about 36 % of the frame height, at the bottom edge of
  the 35-60 % range. PASS.
- **Angle types used (8, at least 4 needed):**
  - Bird's-eye: 0-2, 31-32.5.
  - Low hero: 4.5-6, 35.3-37.5.
  - Side tracking: 6.5-11, 37-39.5, 44.5-50.
  - Over-the-shoulder: 16.3-17.5.
  - Through a foreground frame: newspaper 20.0-22.5 and 25-27, crowd heads 42.4-44.
  - Whip pan up and down: 39.8-40.3, 42.2.
  - Top-down: 54-57.
  - Crane up and out: 57-59, 63-64.5.

  No more than 2 shots in a row share the same height and angle. PASS.
- **Set rich and detailed?** YES:
  - The town grid has roofs, cars and a water tower.
  - The school bleachers have bunting, a dense crowd and the MEDFORD HIGH sign, and there are cones,
    hurdles and pines.
  - The night stadium has a city skyline, light beams, a packed crowd, banners and officials.

  Note (not blocking): the 1963 ground is flat low-poly green with little texture (for example
  12.5-15 s), and the 1972 crowd reads as pixel noise at full size.

## §I — reference match
- **Hard cuts:** 6 detector boundaries (16.3, 35.27, 44.38 and the whip and dissolve joins), within the
  target of 4-10 and the maximum of 12. PASS.
- **The camera travels:** PASS.
  - The BIGZOOM descents.
  - Side tracking with the runners.
  - A push THROUGH the flash into the newspaper (24.5-25.0 s), and from the newspaper photo into training
    (28.7-29.3 s).
  - A poster match-dissolve into Mexico (30.5-31.0 s).
  - A crane out of the mat to the podium.
  - A sky-to-sky dissolve from 1972 to Medford (64.5-65.5 s).
- **Motivated light, rim, warm and cool:** PASS.
  - Medford: a low sun throws long shadows (3-16 s), with amber pits and maroon against the blue sky.
  - Mexico: floodlights with visible beams, a hard white rim on Dick (46-50 s), and red track against blue
    mat and night sky.
  - 1963 has the weakest rim light (flat midday look at 12-15 s). This is a note, not a block.
- **Signature colour:** PASS. Maroon and amber against sky blue in 1963. Tartan red, mat blue and night
  blue in 1968.
- **Signs readable on the phone sheet:** PASS. Visible: MEDFORD HIGH, HIGH JUMP, TRACK & FIELD,
  MEDFORD MAIL TRIBUNE "FOSBURY FLOPS OVER BAR", MEXICO 68, BAR HEIGHT 2.24 m and 1972. Facts check:
  - No "world record" board.
  - The 1963 pit is sawdust or wood chips, never foam. The foam mat appears only in 1968 and 1972.
- **Characters always act:** PASS on the sheets. The coach laughs, points and mimes; the reader shakes the
  paper; the boys cheer; the rivals fail; the crowd bobs. No one is frozen across more than 3
  consecutive 0.5 s tiles, except the officials on the 1968 runway, who are background.
- **Close-ups <= 3:** the 3 planned close-ups are at 23.0, 41.4 and 59.9 s. The 2 accidental pass-throughs
  are fix 2.

## §I.7 — "Would a viewer believe this is from the same channel as the reference sheets?"
**YES.** It has the same character design (white round heads, stick limbs, expressive faces), bold
dominant colour, a moving camera, in-world signs and night light beams that echo R5's storm blue and R2's
neon. The 1968 night section matches best. The 1963 daylight is flatter and less textured than R2 and R5;
that is a non-blocking note for future films.

## Story on the phone sheet, beat by beat
All beats read:
1. **Hook (0-6 s):** town, then a boy straddling face-down, then Dick flopping backwards.
2. **1963 failures and flop (6-16 s):** the bar falls on the straddle at 13.5, then a clean flop.
3. **Mockery (16.3-24 s):** the coach laughs, mimes the broken neck and points, with a punch close-up.
4. **Newspaper (24.5-28.7 s):** flash, then FOSBURY FLOPS OVER BAR, then the boys and coach laugh.
5. **Training and season (29-30.5 s).**
6. **BIGZOOM to Mexico 68 (31-35.3 s).**
7. **2.24 m and the rival out (33-35 s).**
8. **Two failures (37.9 and 39.2 s, hands on face).**
9. **Coach shouts, close-up 2 (41 s).**
10. **The hush (42-44 s).**
11. **The reveal arch (45-50 s and 53 s):** head, then back, then legs over the bar, with the body hanging
    below. The contrast with the red straddler lying flat high above the bar (50.5-52.5) is clear.
12. **The bar does not tremble (55-57 s).**
13. **Gold podium (58-59 s).**
14. **Coach jaw-drop (59.9 s).**
15. **1972, everyone flops (60-64 s).**
16. **Back to Medford, the coach flops into the sawdust pile (66.3-69.8 s).**

The one weak spot on the phone sheet: close-up 3 (59.85-60.1 s) falls between the tiles. It is fine in
motion.

## Re-check after the fixes
- Purple scan: zero frames.
- 2 fps tiles: 17-28.5, 36-39 and 60.5-63 s.
- The g-range checks in qa_auto.

## Director follow-up (21:45 UTC)
- Fix 1 (T2 purple placeholder slabs): repaired in post on the take. A per-frame scan for the slab colour (RGB about 108,0,165, ±30) found 7 frames: g487 (handle), 522, 524, 735, 770, 822 and 842. Each was replaced with a time-weighted blend of its nearest clean neighbours, and T2 was re-encoded (386 frames, libx264rgb crf 6). Rescan after the repair: 0 frames. The other takes have no slab frames; the only hits, T5 g1784-1785, are the directional whip blur mixing the blue banner and the red track, not a slab.
- Fix 2 (T4 camera through an official, g1098-1102 and g1146-1150): sent to team 4.
- Fix 3 (T7 bar across the 1972 jumper's eyes and floating head, g1845-1860): sent to team 6.
- g833-841 soft run: QA-art says acceptable (sharpness down only 7-9 %).

- Fix 2 verified by director (21:40 UTC): T4 swaps at g1100 and g1148 are now 6-frame directional whip blurs with no person in frame (checked g1096-1110 and g1144-1152).

---

## Re-check (new conform: 2095 frames; sat 0.694, vivid 75.0, luma 98.1, LUFS -12.2)

### RE-CHECK VERDICT: FIX (T7 only)
Fixes 1 and 2 pass. Fix 3 does not: the re-rendered 1972 part still passes the bar across a face for all
three jumpers. It also has a new head hanging below the bar.

### 1. T2 purple slabs: PASS
- **Whole-film scan:** I re-ran the per-frame violet scan (b >= r, b > 0.55, g < 0.15, sat > 0.8) on all
  2095 frames. No frame has more than 0.4 % coverage. Earlier the worst frames had 2.6-26 %. The 68 frames
  at 0.2-0.37 % (g1276-1887) are scattered crowd pixels in the night and 1972 stands, not slabs.
- **Repaired frames:** I looked at g486-489, g521-524, g734-736, g769-771 and g841-842. They are clean and
  there is no visible ghosting at phone size. g770 is slightly soft on the newspaper type, which is
  acceptable for one frame.
- **g487:** it sits 2 frames before the T1→T2 cut at g489 and blends T1 frames only, so nothing bleeds
  across the cut.
- **Pops:** the pop detector finds no single-frame pops.

### 2. T4 camera through the official: PASS
- **g1100-1105:** a directional whip blur. The only figure in it is Dick, smeared and far away (under 25 %
  of the frame height). The landing frame g1103 is clean, with Dick, the official and the 2.24 m board.
- **g1148-1150:** a whip blur that lands sharp on Dick at g1151.
- No face over 35 % appears and nobody is cut by an edge. Both read as deliberate whips.
- The whips add 2 transitions. The cut and transition count stays inside the §I target of 4-10.

### 3. T7 1972 re-render (g1796-1965): FIX
**What is OK:**
- The seam into close-up 3 at g1795→1796 works as a punch-in on the jaw-drop. The face is about 31 % of
  the frame height and the close-up lasts until about g1803.
- The dissolve to the 1972 banner (g1803-1808) and the crane-out (g1905-1935) are clean.
- The sky dissolve to Medford (g1935-1966) works, and the end seam at g1965/1966 is continuous.
- Colour and grounding hold: the officials and photographers on the track have shadows, and each jumper
  sits or stands on the mat after landing.

**Blocking problems:**
- **Bar through a face, all three jumpers.**
  - Jumper 1 (red hair, green kit): g1848-1852. The bar covers his eyes at g1850 and g1852.
  - Jumper 2 (dark, yellow kit): g1880-1887. The bar crosses his eyes and mouth at g1882-1886.
  - Jumper 3 (red kit): g1915-1918.
- **Heads hanging below the bar on the take-off side.**
  - Jumper 3 hangs in the arch for about 0.8 s, g1892-1915. His head dangles below the bar, in front of
    the mat's side wall on the run-up side, and barely moves. It reads as a head hanging in mid-air
    (§G.2).
  - Jumper 1 does the same at g1830-1852.
- **Disembodied head at the frame edge.** Jumper 1 enters at the right edge at g1818-1829 as a big head
  with his body off-frame.
- **Root cause.** The camera is on the run-up side, but the jumpers are posed so that the head trails on
  that side, below the bar. To reach the mat, every head has to pass under or through the bar in screen
  space. A real flop leads with the head over the bar onto the mat.
- **Fix (Team 6):** pick one.
  - Mirror the flop so that the head goes over the bar first and drops onto the mat (far side), with the
    legs flicking last, as Dick does in T5.
  - Or move the camera to the mat side or high enough that every head stays clearly above the bar line on
    screen.

  Either way, keep the full body in frame on entry and cut the hang to at most about 8 frames. Re-render
  g1810-1925 and check every frame from g1815 to g1925 for any bar across a face.

### 1972 landings (first mat contact in the current conform)
| jumper | first touches mat | current SFX cue | offset |
|---|---|---|---|
| 1 (red hair, green) | **g1853** (61.77 s) | g1831 | +22 |
| 2 (dark, yellow) | **g1888** (62.93 s) | g1858 | +30 |
| 3 (red kit) | **about g1919, ±1** (63.97 s; he is small in frame while the crane rises) | g1892 | about +27 |

The cues are early in this conform. These landing frames will move again once T7 is fixed, so re-time the
cues after that re-render, not now.

---

## Re-check 2 (T7 only; new conform: 2095 frames, sat 0.694, luma 98, LUFS -12.2)

### RE-CHECK 2 VERDICT: PASS
I checked every frame from g1810 to g1925 (full frame, plus every-frame crops of each jump) and the seam
from g1934 to g1972.

### Landing frames (first mat contact): confirmed
| jumper | landing | what the frames show |
|---|---|---|
| 1 (red hair, green) | **g1831** | g1830 head passing behind the bar, g1831 lying on the mat |
| 2 (dark, yellow) | **g1865** | g1864 behind the bar, g1865 lying |
| 3 (red kit) | **g1900** | g1899 behind the bar, g1900 lying |

The sound cues at g1831, g1865 and g1900 match.

### Team 6's flags
- **(a) Head crosses the bar line: not blocking.**
  - Jumper 1: the bar covers part of the face only in g1829-1830.
  - Jumper 2: only in g1863-1864.
  - Jumper 3: g1899, plus a partial cover at g1900-1902 while he lies just behind the bar (the bar covers his
    mouth and chin, the eyes stay visible).
    His face there is about 2 % of the frame height because the crane is rising, so you cannot see it at
    phone size.
  - During each arch the bar touches the hairline, but the eyes and mouth stay clear: g1819-1828,
    g1854-1862 and g1888-1898, about 10 frames each. Torso and legs show over the bar all the time, so this
    reads as a body draped over the bar, not a floating head.
  - The old problems are gone. The 5-8 frame bar-across-eyes runs are gone, and so is the 0.8 s hang.
- **(b) Right-hand official at the frame edge, g1819-1824: not blocking.** He leaves the frame by the right
  edge as the camera moves. He is whole at g1815-1818 and a sliver by g1822. This is a normal exit during
  a camera move, not a person framed cut in half.
- **Head showing with the body missing:** none. Jumper 1 enters at the right edge (g1817-1818) and jumper
  2 at the right edge (g1853), each with the torso visible. Jumper 3 enters at the bottom right
  (g1886-1887) with his red kit visible.
- **Floating heads or people cut in half:** none.

### Rest of the stadium part and the seam: OK
- From g1905 the crane-out is clean. All three jumpers sit on the mat with thumbs up, and the officials
  and photographers have shadows.
- The sky dissolve from g1935 to g1958 is smooth. Frame-to-frame differences rise and fall evenly
  (0.06-0.15). There is no spike at g1965/1966 and the Medford move continues.

### Non-blocking note: pose pop on standing up
Each jumper goes from lying flat to sitting upright with thumbs up in a single frame:
- g1835→1836
- g1869→1870
- g1904→1905

The figures are only 5-10 % of the frame height and the moment sits under the crowd cheer, so it is minor.
**The cheapest polish is in post:** a 3-frame crossfade over each pop (g1834-1837, g1868-1871,
g1903-1906), limited to the mat area if needed. This is optional and does not block release.
