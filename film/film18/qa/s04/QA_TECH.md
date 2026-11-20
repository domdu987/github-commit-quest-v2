# QA_TECH s04 (take g295-391, in-shot g297-383) - FAIL
Checked: 6 fps frames + first/last 3. Frame-diff re-measured: median 5.85, p90 7.34 (min 3.7, max 13.3); eased orbit + push, one held punch ~g355-365; no pulsing. Caption band y880-950: mean 59-96, bright (luma > 200) max 1.13 % (limit 1 %).
## Earlier blockers
- E1 Ju lit: NOT FIXED (no second warm town anywhere in frame).
- E2 pulsing: FIXED. E3 caption band bright <= 1 %: still 1.13 % at g~350-391 (flag/tent faces).
- Flag opaque, no bloom: OK (but see issue 3).
## Issues
1. whole take - mandatory "Ju is lit": not shown; only Jimo is in view and Jimo itself is mostly dark navy roofs with a few small lit windows, so "two towns stay warm-lit" does not read. Fix: a camera or set change that frames a second warm town, and warm the Jimo roofs.
2. g325-391 - rule 2 / bare areas: large flat dark navy polygons (long shadow slabs, crescent road/moat shapes) fill 30-50 % of the frame at g335-375 and the lower third at g385-391; they read as untextured navy slabs. Fix: lighten or texture, or cut the shadow casters.
3. g360-391 - the Jimo flag has a pale/pink triangular patch along its top edge (g385-390), a faceted polygon artifact.
4. g350-391 - caption band bright share 1.13 % > 1 % (mandatory). Fix: dim the tent faces and flag edge.
## Notes
- g295-330 the foreground is a tent field; Jimo is small. Reads as a camp, not a siege view.
- delivered as a CUT in from s03 (last s03 frame is the plain with spikes, first s04 frame is a different camera); plan said same take, snap.
- no text, no characters; DUSK matches s03.
