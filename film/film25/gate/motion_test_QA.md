# Motion test QA: film 25, the general mocks the tank (shot plan v2 rows 19-22)

## Scope
- **Range:** g 522-675 (17.40-22.53 s), 154 frames, 5.13 s at 30 fps, 720x1280.
- **Narration:** cut from narration.wav over the same range.
- **Captions:** burnt in the channel style (Kanit Black 88, white, 5 px dark outline, centred at y 900).
- **Rows (hard cuts only):**

  | row | g | content |
  |---|---|---|
  | 19 | 522-551 | belly laugh |
  | 20 | 552-601 | "ถังน้ำเหล็ก จะไปรบเนี่ยนะ!" |
  | 21 | 602-625 | "ของเล่นชัดๆ!" with the toy tank |
  | 22 | 626-675 | over the shoulder, "ถ้ามันข้าม สนามเพลาะได้จริง" |

- **Files:** `motion_test.mp4`, `motion_vs_R11.mp4` (R11 from its beat cut at 7.233 s), `motion_strip.jpg`.
- **Scripts:** in `motion/`:
  - `motion.py`: shot
  - `c25.py`: helpers
  - `post25.py`: post
  - `assemble.py`: deliverables
  - `measure.py`: camera numbers

## Render
- **Settings:** set25 `trial_close_general` with Cycles at 24 adaptive samples (threshold 0.02), OIDN at 75 % (540x960). These are the director's film-24 final settings. Then `post25.py` upscales to 720x1280.
- **Processes:** 2 processes x 2 threads.
- **s/frame:**
  - 50.0 s wall mean (min 38.9, max 70.3) and 95 s CPU, over 154 frames.
  - The first frame took 45.5 s.
- **Earlier attempt:** the set's own final (64 samples, native) measured 245-350 s/frame on the shared CPU. The director stopped it.
- **Frozen set:** the set and cast were frozen for the whole render as a scratch snapshot of set3d25 HEAD 146dd16 plus cast25. Set commits made during the render (muted camo and others) are therefore not in these frames.
- **Runtime dressing:** the set's new framing-reference general card (`general25_point_stick`, added to the preset mid-session) is hidden. Haze stays at the set's 0.0006: 0.0025 was tried and milked the whole sky.

## Post (`post25.py`, replaces `front.grade()`)
1. The set's sharpen and clarity.
2. A gentle grade on the background only:
   - a soft shoulder on luminance, with no channel clipping
   - a global white balance toward mean a* +2, b* +4.5, which keeps the warm key against the blue sky fill
   - gamma 0.95 and an exposure solved to a frame luma of 0.50
   - vibrance 1.25 on low and mid saturation, with no hue shift
   - a slightly darker near-foreground edge
3. The general's cast25 sprite is warped onto his card's screen quad and composited **ungraded**:
   - Faces are exactly #fef7f6 in every frame (more than 2000 exact pixels per frame).
   - Grass in front of the card is kept, by an occlusion test against the rendered card colour.
   - The only 255-value pixels are the sprite's own white highlights.

## light_metrics.py
```
motion_test.mp4 (5 fr)  luma 0.500 p1 0.058 p99 0.974 lc 0.0414 sat 0.416 chroma 29.1 a +2.1 b +3.9 p98 0.89 blue 0.36 warm 0.37 neut 0.08 M 74  PASS  (guides off: p99,warm_frac)
caption-free copy       luma 0.496 p1 0.089 p99 0.963 lc 0.0371 sat 0.423 chroma 29.7 a +2.3 b +4.4 p98 0.89 blue 0.35 warm 0.38 neut 0.06 M 76  PASS
R11 beat (reference)    luma 0.446 p1 0.034 p99 0.995 lc 0.0433 sat 0.249 chroma 11.6 a +4.5 b +6.5 p98 0.88 blue 0.15 warm 0.84 neut 0.47 M 47
```
- **Hard gates:** all pass (luma 0.46-0.56, sat ≥ 0.40, |a*| and |b*| ≤ 6, exact faces, no clipping on the set).
- **M:** 74 is above the 55-70 guide and above R11's 47. With no vibrance at all, M is still 72, because the scarlet sash and cap band and the blue sky carry it. Holding sat ≥ 0.40 needs vibrance of about 1.15 or more.

## qa_jitter
`python3 PROJ/qa_jitter.py motion_test.mp4`: overall median jitter 0.23 px. No second is flagged as shake (the caption-free copy gives 0.26 px).
For scale: R11's own beat flags 2.5 and 4.4 px "shake" seconds from its cuts and character moves.

## Camera move per shot (measured from the general's head on screen, `measure.py`)
| row | spec | measured scale | punch part | subject pan, % of W per s | head centre y (0-1 H) | head width / W |
|---|---|---|---|---|---|---|
| 19 | PUNCH 20 % g 522-529, then drift | +23.4 % | +19.2 % in 7 frames | -10.5 (drift) | 0.42-0.46 | 0.32-0.40 |
| 20 | PUSH 10 % | +9.9 % | - | -0.4 | 0.40-0.48 | 0.35-0.38 |
| 21 | PUNCH 20 % g 602-609, then drift | +21.2 % | +17.2 % in 7 frames | -7.3 (drift) | 0.44-0.52 | 0.35-0.42 |
| 22 | over-shoulder PUSH 8 % | +4.3 % on the head (the camera dolly is 8 %; the head sits at the left edge and the push slides past it) | - | +6.2 | 0.48 | 0.36-0.38 |

- **Camera:** every move is an eased spline evaluated per frame. Nothing is parented to the camera, there is no shake and no DOF. The sun is re-aimed per shot from the camera's left, and the cast25 setting light25 = -1 matches it (rim25 = 0.6).

## Acting
- **Row 19, laugh:**
  - laugh and laugh_b alternate every 3-4 frames, with a squash bounce and the medals jiggling
  - the head rolls, the body leans
  - laugh mouth from the 'laughing' expression; no lip-sync before g 552
- **Row 20, point_stick:**
  - talk_mouth driven by the narration's loudness, so pauses close the mouth
  - head toward the gun, then he turns to us on "จะไปรบ"
  - blinks at g 565 and 574; smug changes to smirk
  - a stick jab on the noun, the stick wagging, a squash accent on "นะ!"
- **Row 21, toy_dangle:**
  - pose key t advances every frame, so the toy swings
  - squash on the cut; eyes on the toy, then a blink and a sneer ('unimpressed') at us on "ชัดๆ!"; the toy is lifted
- **Row 22:** the head is in profile toward the trench, then turns back after the blink at g 655; a stick jab on "สนามเพลาะ"; lip-sync throughout.
- **Grounding and contact:** the stage contact decal is under him in every row. His cast shadow falls on the hull (rows 19-20) and on the grass (row 22).

## Where ours is still stiffer, duller or more cluttered than R11 (honest list)
1. **Framing is looser than R11.** The general is short (3.3 heads), so a head of 1/3 W with the head at 0.30-0.45 H cannot also crop the legs. The legs show to the shins or boots in rows 19-21, and the whole figure shows in row 22 (feet at or below the frame bottom). Heads reach 0.48-0.52 H in rows 21-22, below the 0.45 target. R11 crops at the waist with the head larger.
2. **The puppet is one flat card per frame.** Body motion is pose swaps and squash only, with no in-betweens. Head turns snap over 5-6 frames, and the stick and arm move less than R11's arm gestures. The stick in row 20 is short and partly hidden against the gun.
3. **Background:**
   - Rows 19-20 show the hull's track horns, rivet rows and plates behind him. That is busier than R11's plain grey wall with two bold stripes.
   - Row 21 has a pale corridor/tail shape at the left edge.
   - Row 22 shows the tank small and far (about 30 D), with the red flagpole in the middle: the trench reads, but the tank is a small shape.
4. **Colour:** M is 74 against R11's 47. Our palette is more saturated (blue sky and scarlet) where R11 is grey steel with navy and pink accents. It does not read as neon, but it is brighter than the reference.
5. **Shadow and depth:** the cast shadow on the hull is soft and partly hidden behind the figure, where R11 shows a crisp wall shadow. The aerial haze is the set's thin default (a stronger volume washed out the sky), so the far tree line separation is mild.
6. **Camera energy:** pans are 6-10 % of W per second. That is calmer than R11's median of about 1.1 % per frame (33 % per second). The punches land but the drifts are gentle.
7. **Row 22's 8 % push** reads as only +4 % on the subject because he sits at the frame edge.
