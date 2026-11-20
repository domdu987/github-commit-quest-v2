# QA T3b (take T3, g751-856, 106 frames)

Setup: render17v2/T3 commit 69c6528 (TAKE_OVER T3 gain 1.05, apply_ramp x0.4 to g750 easing to x1.0 at g800) + clear_cast() before each stage_cast2.
16 samples + OIDN, 720x1280. Two processes (751-803, 804-856). ~100 s/frame each.
An earlier run (without clear_cast) showed black slabs from the stage_cast2 leak; all of it was discarded and re-rendered.

## Numbers (luma = RGB mean of 90x160 bilinear, the binding metric)
- part mean 118.9, min 102.1, max 153.7 (g856). takes.md target 95-110: the part is ABOVE target (director decided: finish as is, exposure trim at conform).
- g751 116.6, g770 119.7, g792 109.5, g800 109.6, g830 121.2, g851 147.4, g856 153.7.
- black fraction (max RGB < 8): 0.0 % on every frame. qa_auto: PASS (magenta 0.0 %). rhythm: in-shot median 20.8, p90 33.2, no cut detected.
- g800 of the first (pre-ramp) setup was byte-identical to T3's approved key v2; the final setup differs on purpose (gain and ramp), so that identity no longer applies.
- Hard cut at 850: none inside this range. Frame diff is continuous across g849-851 (19.1, 17.8, 15.3); the clock push eases out through g856.

## Frames viewed (each at 720x1280 full size, and in a 360x640 phone strip)
- g751: bird's-eye-ish room view. Room signs ARCHIVES and SERVICE D'IDENTIFICATION readable. Two gendarmes in front (arms crossed, one mustache stretched), green-coated man and prefect (top hat, tricolour sash, arm raised) behind. Feet on floor with contact shadows. No black slab. Phone size: figures and signs clear. Warm/blue palette strong.
- g770: lower view, gendarmes and prefect in a row, chandelier hanging in frame. Nothing black. (Viewed in phone strip and via luma; full-size individually not opened.)
- g792: a large dark purple wooden upright (vertical post with a crossbar) fills the middle of the frame, about 1/3 of the width. It is a real prop (outlined, textured, lit) and not a shadow slab, i.e. the planned foreground block for g792-812. The SERVICE D'IDENTIFICATION sign is cut by it. Bertillon (glasses, goatee) behind it left, a gendarme right. Phone size: readable as a foreground object.
- g800: Bertillon measuring a head with calipers, desk with instruments left, carpet and floor right, chandelier overhead. Feet on the carpet with shadows. No slab.
- g830: camera looking up the wall: ceiling beams, MESURES chart, clock with pendulum, bookshelf. No people. Smooth, no black areas. Phone size: fine.
- g851: clock face fills the screen (hands near 10:00 position) on bright yellow wall, very saturated; wall near clip. 
- g856: same clock, closer. Bright yellow wall (luma 153.7), likely to need the conform trim. Clock face, hands and pendulum clear.

## Not checked / caveats
- Shimmer: frame diffs include camera motion, so flat-wall OIDN flicker could not be separated numerically. In the full-size views of g830 and g856 the flat yellow and blue walls show faint grain/streaks (OIDN), no obvious blotches. 16 samples kept (director did not request 24).
- Only the 7 frames above were looked at; the rest were checked by numbers (black fraction, luma, frame diff) only.
- Mouths: not examined in this part's frames beyond g751 and g800 where mouths are closed or small.
