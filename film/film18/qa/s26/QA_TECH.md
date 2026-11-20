# QA-tech round 14b s26: FAIL
Checked: all 162 frames extracted; 6 fps sheet; full-size and 3-4x crops at g1958 (plaque, props, roofs, banner), g1959-1984 every 5, general height g2066 and g2111, mouth/ground at the end, frame-diff 90x160 (median 8.70, p90 11.76; no pulsing, one eased move).

## Blockers
1. Unsharp-mask artefacts in the wide, g1958-~2000 (strength 330 %). Visible on the 180x320 phone tile, not only at zoom: moire/striped hatching on every roof, the field patches and the road (3x crops of g1958 show regular vertical banding); dark and blue halo fringes around every orange prop, torch flame and the gate lantern (cyan/blue ring ~3 px); crunchy, over-contrasted edges (Laplacian energy 25 at g1958/1970 vs 14.5 at g2010). Looks like a rendering fault, not a dawn mood. Fix: re-render the wide frames with more samples/denoise or a plain Lanczos upscale, and apply the unsharp at <= 120 % (radius 1) or drop it; blur flag can be handled as a "wide soft" note.
2. General not findable at the extreme wide (g1958-~1966). He is ~28 px tall (2.2 %), standing small at the left of the wall by the banner at g1958 (x~40, y~810, half hidden behind the banner); at phone size no figure is readable, and the claimed pool of light is not visible until ~g1969. Fix: place the dawn pool and a bright marker (gold helmet glint) so he reads on the open road, not under the banner; put him on the road with a visible contact shadow from g1958.

## Passed
- Height: g1958 ~2.2 % (< 5), g2066 ~51 % (35-60; head top y 285, feet y 945), g2111 ~54 %.
- Move: g1958 to g2066 = 108 frames = 3.6 s (3-6), one continuous eased crane/swing, no cut, no pulsing; held push after g2068.
- Ox mouths at the end <= y 830 (<= 860). Ground at the end 0.22-0.26.
- Plaque 即墨 readable at g1958-1975 (about 160 px wide, gold on dark; slight edge ringing from the sharpening but legible).
- Rim: a thin blue outline on oxen and general, clean; no doubled legs, hats or plume at 1x or 2x (the plume has its own parallel painted lines, not a ghost). Lens and feet: general's feet on the road with a long blue cast shadow from g2040 on.
- Set rich through the zoom (roofs, lanterns/torches, flags, oxen, smoke). No placeholders, mouths held, no cut-off characters (the helmet prop at lower left is partly cut by the edge, fine).

## Notes
- Fields in the wide are blue-murky and low-saturation (conform grade expected).
- Oxen in the wide read as a small red cluster at g1974-2000; acceptable.
- Frame-diff in-shot p90 11.8 (< 12 film target, guide met).
