# TAKE8 QA-art: T03 = s03, round 6 (partial re-render g 170-215 and g 340-411)

**Verdict: PASS with notes.** All four round-5 notes are dealt with, and nothing new breaks. One small leftover: the start glow has a hard-edged core. Fix it only if the take is re-rendered for some other reason.

## Inputs
- Contact sheets of g 170-215 (every 3 frames) and g 330-405 (every 5).
- Phone-size (360x640) strips at g 170-198, 186-196, 360-380, the range edges, and the s06 dissolve.
- 2x crops of the glow at g 170, 176, 182 and 186.
- Per-frame luma and frame-to-frame difference over g 200-231 and g 330-391.
- s03->s06 join: a 13-frame dissolve built from s03 g 398-411 over s06 g 396-410.

## Changes checked
1. **Start marker (warm glow): works, slightly graphic.**
   - Eiffel is findable. At 360x640 the glow is the only saturated yellow on the brown yard, sitting between the two legs, so the eye finds it at g 170 without the old pin.
   - It is gone by g 188, two frames before the target, with no visible cut-out.
   - Motivation is only partial. The glow has two parts:
     - a soft, warm bloom on the tent, which reads as lamplight;
     - a flat, hard-edged yellow disc above the tent.
   - As the camera drops (g 180-186), parallax separates the two by about 60 px at full size. For those frames the disc reads as a small yellow ball floating over the tent rather than light.
   - At phone size and running speed it is brief and harmless. **Note (optional):** soften or remove the hard core so only the bloom is left.
2. **Pale gravel disc: fixed (hidden).**
   - The bottom-left of g 194-215 is now plain ground.
   - A few small pale ovals (about 10-15 px at phone size) still dot the yard at g 182-192. They read as scatter. Non-blocking.
3. **Brighter deck underside: natural, no pop.**
   - The underside reads as warm, mid-tone olive-brown planking. It is not washed out, and the railing and lattice keep their contrast against the deep blue.
   - The underside face is a little flat and uniform, but it is acceptable for this style.
   - Dark share (luma below 60) at g 378 drops from 54 % to 45 %.
   - Luma follows the tilt smoothly (119 at g 360, 85 at g 378, 91 at g 390). Frame-to-frame differences rise and fall evenly across g 362-376, with no spike, so the +18 % ramp is invisible.
4. **Source-less smoke puffs: fixed (gone)** from g 366-382.

## Range edges
- **g 215/216:** the difference stays flat at about 7 against a 6-8 baseline. Tent, barrels, table and Eiffel are identical in position and light. No seam.
- **g 339/340:** the difference is 24.3 to 24.2, the same as the motion baseline. The lattice, sky and clouds continue cleanly. No seam.

## Join s03 -> s06
- The dissolve from riveters against deep blue sky into the warm café is clean.
- The riveter cards and the café figures overlap only in passing mid-dissolve, with no awkward face-on-face hold.
- The warm/cool swap reads as intended.

## Carried over (unchanged frames, not re-judged)
- The crane-up drift at g 318-365.
- The riveter cards stacked in pairs at g 395-411.
- The far bank is a flat grey-lavender plane.
