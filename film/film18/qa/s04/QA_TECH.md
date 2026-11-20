# QA_TECH s04 (take g295-391) - FAIL (round 4)
Checked: 6 fps (24 frames) + first/last 3. Director 12.46 / 14.68: OK, orbit + push, no pulsing. Caption band bright share max 0.04 % (880-950), 0.01 % (880-1100): mandatory <= 1 % MET.
## Earlier blockers
- Ju lit as a second warm town: NOT FIXED. Navy slabs / bare ground: NOT FIXED. Jimo roofs warm-lit g370-391: OK. Flag opaque, no bloom: OK.
## Issues
1. g295-325 - Ju: no second warm-lit walled town exists. The only warm item is a red flag with a small torch flame on a pole at the top right (g295-310), which drifts, shrinks and at g315-325 leaves a lone flame floating in the sky. It reads as a stray flame, not a town. Mandatory item missed. Fix: frame a distinct warm lit town (lit windows, torches) as Ju before the push to Jimo and delete the loose flame.
2. g330-375 - bare ground: 45-60 % of the frame is plain tiled green-grey field with huge flat navy shadow shapes and a navy arc ring (g345-365 worst, g355 about 60 %). Over 30 % blocks. Fix: keep towns filling the lower half, or lift/texture the field.
3. g295-340 - lower half is dominated by dark navy shadow areas between rows of walls (untextured dark navy read, rule 2); the black slab pennants cross the lens g320-345.
## Notes
- Jimo end frame g375-391 is the best part: lit windows, red flag, readable. Cut in from s03 has a different camera, acceptable.
