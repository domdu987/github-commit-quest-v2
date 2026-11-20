# QA s20 (render team 5, film 18) round 14 - g1515-1595 (+6 handles: take.mkv g1509-1601, 93 frames), NIGHT
Redesign per director round 13/14: side-view gallop, lead ox ~17 % frame height, `face='rage'`, tail flame lean 60.
- Frame-diff in-shot (n=80, 90x160 grey): median **4.32**, p90 **6.01**, min 3.00, max 20.59 (median gate >= 4 met; p90 >= 9 NOT reached).
- Camera follows at 0.97 x herd speed; lead ox head x ~83 px at minimum, lead flame max x ~651 px (<= 680) measured in measure mode.
- Foreground: ~70 world props (jars, reed bundles) on the lower field, field planks/posts sunk, halo quads removed; plain field fraction on rendered PNGs (rough low-chroma mask) ~0.5 - not a strict colour-mask check, honest note.
- Contact shadows present under oxen; Qi not in shot. Comic, bloodless.
- Deviations: p90 below 9; ground plain-share not verified with a proper field-colour mask; whip-in handle 6 frames.
- qa_auto PASS (QA_AUTO.md).

## Section I rim light (final render)
- Frame-diff in-shot (n=80): median **4.73**, p90 **6.56** (p90 < 9 not reached). qa_auto PASS.
- Moon-blue rim (120,175,255) painted into every character/ox card on the upper/right silhouette edge (cards are unlit emission, so scene lights cannot rim them); plus two blue point lights per frame behind the nearest oxen for the ground. Warm fire key and saturated reds unchanged, no haze added. Layout unchanged; the other s19 caveats above still apply.

## Round 15 (director follow-up, rim version)
Herd and camera speed raised 8 % (V_OX 16.2). Frame-diff n=80: median **4.92**, p90 **6.75** (aim p90 >= 7 narrowly missed). Lead head min x about 134, lead flame max x about 650. qa_auto PASS.

## Round 16 (gate 14b)
Layout: two rows (front spacing 10 D = 2.2 ox lengths, rear row +3 D back, offset half a spacing), flame capped 0.8 D tilted up 30 deg. Camera closer (LAT 12) and tilted up (look z 3.3 from z 4.0); 340 world props (reed bundles, jars, bowls) in the lower and mid ground, all low (never at head height).
- Frame-diff n=80: median **6.00**, p90 **7.69**. qa_auto PASS.
- Lead ox: height ~20 % (not 25-30 %): the side-view ox with flame is ~2.6x wider than tall, so at 25-30 % height it cannot stay inside 720 px with the flame at x <= 680. I kept the whole lead + flame in frame: lead x 143-642 at g1525 drifting to 24-531 at g1595; lead flame max x ~699 at g1525 (flame tongue ends x 639-699 at the very start, <= 668 from g1545) - the first ~20 frames exceed 680 by up to ~20 px.
- Ground (RENDERED frames, my gshare.py: pixels below y 580 within tolerance of the modal field colour and locally smooth): median **0.50**, max 0.54. My estimator reads higher than QA's, so this is not directly comparable to the 0.28 target; the lower 45 % of the frame is now covered by props.
- Not measured: the 30 px flame-to-any-head rule on every frame (head-to-head distances not projected for non-lead oxen).
