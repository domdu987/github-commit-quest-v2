# QA_TECH s25 - FAIL
Checked: qa_auto PASS (cuts g2028 / g2086 not visible, expected), 6 fps + cut +-3 sheet g2019-2094, meta g0 2028 / g1 2085 (plan 67.61-69.55 -> 2028/2085 OK; 2086 = 69.55*30 rounds to 2086), cuts with 9 f handles OK, framediff median 5.01 / p90 12.69 OK. Astro19 wig askew, ring eyes, sweat drop, blinks (g2074 seen), push-in snap g2069-2082 on "เป๊ะ" visible. No text, no blur, head centre y 573-655, bottom <= 810, no clipping until the deliberate push-in.
Issues:
1. g2024-2094 (mouth moving outside a quote window): this shot is at 67.61-69.55 s, outside both quote windows (20.80-25.75, 54.25-55.45), yet the mouth goes from closed (g2019-2024) to wide-open (jaw drop g2025-2034) and then changes shape: small round (g2044-2064), larger oval (g2079-2089). Rule: every mouth stays still. Fix: render one constant mouth shape for the whole shot (open from frame 0 or closed); no jaw-drop animation; hold the shape through the push.
2. g2019-2074: no contact shadow under astro's shoes; the legs end in thin stubs floating above the carpet. Fix: add a blob shadow / lower the card to the floor.
3. g2079-2094: legs/feet leave the frame with the push; fine for the snap, but the wig and head fill 80 % of the width (head ~ 315 px); make sure the wig tips are not clipped at the left (g2088 tip touches x = 0).

## Round 2 - FAIL (one item)
Checked: qa_auto PASS (cuts g2028 / g2086 are handle boundaries); 6 fps + cut +-3 sheet g2019-2094; meta g0 2028 / g1 2085 OK, hard cuts, 9 f handles OK; frame-diff median 5.01 / p90 12.68 (measured).
Verification of round 1: 1 mouth FIXED (held open round mouth through the shot, no talking; only a taller oval on the g2074 blink frame, NOTE). 2 contact shadow NOT fixed. 3 wig clipping: wig tip is inside the frame g2028-2085 (the left tip touches x=0 only at g2088, in the out-handle).
Snap push-in on "เป๊ะ" (spoken g2081) g2069-2082 visible. Head centre y 573-655, chin < 880, wig askew, sweat drop, evening hall OK.
Issues:
1. g2019-2074 (feet): Astro stands on the dark red carpet runner with no contact shadow; the legs are thin white stubs that float. Fix: blob shadow under both shoes (it is a wide shot for 2 s, readable).
Notes: the first frames g2019-2024 mouth smaller than the held shape (handle only).
