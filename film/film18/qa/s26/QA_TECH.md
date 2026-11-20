# QA-tech round 16 s26: FAIL
Checked: 6 fps sheet, 3x crop g1958, Laplacian energy, wide to end frames g1958-2111. Director ground max 0.336 (median 0.23).

## Blockers
1. Ground > 0.30. ground_share frames over 0.30: g2006 0.32, g2008 0.34, g2010 0.33, g2012 0.31 (4 samples, about 8 frames). The camera is mid-swing and the lower 55 % is untextured field panels. Fix: add dark textured props (haystacks, hedges, furrow texture, shadow of the gate) over the lower field at g2000-2016, or lift the horizon.

## Previous blockers verified fixed
- Unsharp at 150 %: no moire or blue halos at g1958-2030; at 3x only faint stripe texture on the roof tiles. Laplacian energy 13.4 (g1958), 8-9 (g1990-2010), lower than before.
- General findable: at g1958 he is a small figure standing in a warm lit pool, about 90 px left of the banner (not under it). Marginal at phone size but readable by the pool.

## Passed
- Move continuous g1958-2066, height 2.2 % to about 45-54 %. No cut, no pulse. Plaque 即墨 readable g1958-1975.
- End: general whole, ox mouths <= 860, feet on ground with shadow. Mouths still, no placeholders.

## Notes
- qa_auto blur on the extreme wide accepted.
- Field panels at g1990-2012 have visible horizontal banding (flat panels).
