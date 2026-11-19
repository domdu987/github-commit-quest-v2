# TAKE gate, QA-tech: film 16, render team 3 (branch render16/team3, head 678e953), takes s08-s12

Method: every take decoded to full-res frames; inspected at 6 fps plus every cut +-3 frames; mouth/face crops at 1 fps-per-frame around the quote windows (captions.json, +0.10 s clock); per-frame numbers by script; film/qa_auto.py run on each take (all PASS, 0 black/blank/magenta/frozen; no text, no DOF seen).

## Verdict per take
| take | shot | verdict |
|---|---|---|
| s08 | 8 | PASS (notes) |
| s09 | 9 | PASS (notes) |
| s10 | 10 | FAIL (blocking 1) |
| s11 | 11 | FAIL (blocking 2, 3) |
| s12 | 12 | PASS (notes) |
Overall for team 3: FAIL until s10 and s11 are re-rendered.

## Numbers (90x160 grey, in-shot frames, my measurement; worker's meta in brackets)
- s08 median 5.62 p90 18.14 (4.53/14.78) | s09 7.77/14.39 (6.6/12.4) | s10 5.20/15.96 (4.25/13.67) | s11 6.38/23.06 (5.52/20.82) | s12 6.44/19.99 (5.48/17.75). All meet median >= 4, p90 >= 12.
- Camera parking (phase-correlation shift < 0.25 px/frame for > 6 frames): none in any take.
- Heads vs y 880: all whole heads above 880 (max head bottom: s08 680, s09 666, s10 692, s11 Morse 845, s12 736). Head centres within 403-700.
- Snaps present: s08 g487-501, s09 g552-565, s10 g672-686 (punch-in + focus lines), s11 g764-780, s12 none (1.5 s, allowed).
- Mouths: lip-sync g552/553 onward in s09 and s10 throughout = inside 18.32-23.20 s (+-0.15 s). s10 mouth closed in the last frames. s08, s11, s12 mocker mouth not moving (laugh pose / sour closed). No mouth motion outside the windows except note N2.
- Mocker face (white disc) width: s09 g542-556 140-166 px, g565-596 270-285 px; s10 g597-668 181-225 px, g676 250, g680+ 320-378 px.

## BLOCKING
1. s10 g597-g675 (2.6 s of the 3.35 s quote): the mocker's face is only 200-225 px wide (about 105 px on the 360x640 phone), below the 250 px minimum for reacting faces (Bible addendum: shots 6, 10, 26, 29 >= 250; plan row says "closer", head 300-350). It reaches 250 only at g676 and 320+ after the punch-in. The cut from s09 (face 269 px at g596) to s10 (face 181-209 px at g597) also goes to a SMALLER face, the opposite of "closer". The laugh/boast is legible on the phone sheet (open mouth, blush, chest thump read), but it fails the size rule. Fix: re-render s10 with the camera 2.2-2.6 D from the face (or card scale up) so the face is >= 280 px from g597, keeping the punch-in on g677 to 350+ px; head centre y stays 450-760 (centre 403-520 now, push it down to >= 450), head still above y 880.
2. s11 g772-g777 (flagged by qa_auto, confirmed by eye): the "snap to Morse" is not an eased move but a pop. g772-774 the camera passes through the instrument (a jar and a drum fill the lens), g775 shows a wide view with NO Morse in it, g776 Morse suddenly appears at 265 px (frame diff 64-73 vs median 6, soft frame g774). Fix: keep Morse visible and in frame during the whole fly-in, route the camera so it does not go through the instrument/props, ease the 13-25 f snap on "ไอ้บ้าลวด" (g769) so each frame moves < ~60 px/frame, and land on Morse by about g780.
3. s11 plan coverage g698-g775 (78 of 88 frames): Morse is not in frame until g776, so "Morse clutches his wire coil" and "fingers point at Morse" never show; the lower 40-50 percent of every frame is empty floor/riser; audience heads are 25-60 px so the mocker's laugh tears + blush (Bible addendum, shots 9/11) cannot be read on the phone (the mocker is a ~40 px figure at a far desk, g775). Fix: re-stage the glide so the lower third carries Morse (small, clutching the coil, foreground) or a foreground pointing congressman, tilt up so the tiers fill the frame, and bring the mocker (tears + blush) into a readable size (>= 90 px head) for at least 0.5 s.

## NOTES (non-blocking)
N1. s09 plan: "points at the wire", "inkwell + quill in the foreground", "rises from his desk". Delivered: arm raised with finger up (no wire in shot), no inkwell/quill in the FG (a desk edge at the right only), he is already standing in front of the desk. Fix if the re-render pass allows: FG inkwell+quill in the lower-right 1-2 D from lens.
N2. s09 g541-547 (before the window opens at g548): the mocker's laugh face swaps between open grin with teeth, closed-mouth grin and eyes-shut grin (mouth shape changes at g542-544). It reads as laugh pose, not lip-sync, but strictly the mouth is not still. Fix: hold one laugh frame until g548.
N3. s09 quote 1 close: face is only about 150 px at the first word (g553-558, quote starts g553) and grows to 270 px by g565 through the snap. Readable on the phone from g562; consider starting the shot a little closer.
N4. s08: plan says "high crane down"; delivered camera is near eye level with a push (the first frames show the carpet in the lower 40 percent), no crane-down read. Morse's head 28-98 px (wide, exempt). Mocker (arms folded) is a ~35 px figure, only findable if you know him. Sun shafts faint. Morse presents with his arm toward the instrument and looks to camera, not to the tiers (eye-line).
N5. s08: very large empty red carpet in the lower half for g472-g490; fine as a wide but the table/Morse cluster sits in the middle band.
N6. s10 focus lines (g672-689) are thin white strokes, barely visible at 360x640; the punch-in itself (x1.8, peaks g677) reads. Strengthen the lines (thicker, more of them, radial from the face).
N7. s12 plan: "dropped onto the telegraph table". The bag lands (g788) at the near-left table corner, is large (about 280 px wide vs Morse head 150) and half overhangs the table edge with almost no contact shadow; the telegraph instrument is not in frame (only a paper stack on the green top), so the beat reads as "bag lands on a table corner". The bounces g789-798 and the table jolt at g789 are ok (frame-diff 26 peak). Fix: shift the bag landing 0.3 D right/back so it sits on the table top with a shadow, and keep a corner of the instrument in frame.
N8. Continuity: mocker is standing in the aisle (s09, s10), seated at a far desk (s11 g775), standing near Morse's table (s12). Costume/hat consistent. Morse costume and coil consistent s08 to s12 (his coil is clutched in s11, absent in s12, ok).
N9. s11 g769-773: the sack decoration above the rostrum slides across the top-left of frame during the snap; fine, but it competes with Morse during the fix of blocking 2.
N10. Mocker's boast in s10 reads on the phone (QA-art lite): laugh with tears reads in s09 (g541-565 faces ~150-285 px), boast (finger up, then chest thump, chin up) reads in s10 at about 105 px face; open/closed mouth alternation visible. Passes legibility, fails the 250 px rule (blocking 1).

## Checks with no finding
Heads above y 880; feet/contact shadows (s09 g539-554 shadow under feet; s08/s12 figures stand on the floor beside the table, scale right); hand props attached (Morse coil in s11, mocker hand on chest in s10); no pops except s11 g772-777 and the s09/s10/s11/s12 hard cuts at the planned frames (cuts at g542, 597, 698, 785 show a clear change of view; the handle frames outside g0-g1 were not judged); no blur/DOF, no text, no black/magenta; camera never parked; joins cut-to-cut clean at s09|s10 (apart from the face shrinking, blocking 1).
