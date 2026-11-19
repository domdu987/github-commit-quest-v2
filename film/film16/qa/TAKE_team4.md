# TAKE gate QA-tech, team 4 (render16/team4 @ 6cf7efa): s13, s14, s15
Method: all frames decoded (720x1280), viewed at 6 fps + every cut/handle +-3, frame-diff recomputed (90x160 grey, in-shot pairs only), qa_auto.py run on each take.mkv (all 3 PASS, only note = planned out-cut g inside handle).
Frame-diff (median / p90, target >=4 / >=12): s13 8.63 / 30.86 (worker 7.57 / 27.73; p90 is driven by the snap whip g872-879, otherwise 6-9); s14 15.78 / 24.96 (worker 12.90 / 20.22); s15 5.38 / 6.06 (worker 4.84 / 5.56). No camera-park run, no frozen/black/magenta frame, no text, no DOF, no mouth movement anywhere (correct: none of these shots has a quote).

## s13 (shot 13, g831-891) : FAIL
BLOCKING
1. g831-871 plan coverage: the plough, the pipe unrolling into the furrow and the workers following are not visible for the first 40 of 61 frames. Frame shows two small mules (~100 px, tiny hooves) far across the furrow, huge dark tree masses on top and out-of-focus-size grass blades covering the bottom. The "lead pipe unrolls into the furrow" beat is only a thin pale strip at the far right edge from g880. Fix: camera closer/lower alongside the team so plough + furrow + pipe are in the middle third from the first frame (plough behind the mules, pipe visibly leaving the drum), mules >= 170 px tall; crop away the big tree canopy.
2. Morse is absent (plan: "Morse and workers follow"; meta says "mostly out of frame", in fact never visible). Fix: put Morse walking behind the plough in frame at least g860-891.
3. g877-891 Cornell: plough handle reads as a pole/log across his shoulder, hands on a stick; the plough itself is behind/off to the left and cut by a blue box (pipe drum?) so nothing is being pulled by the mules (mules are 100+ px away in g822-871, then gone). Mule-to-plough link not shown. Fix: stage so mules, traces, plough and Cornell share a frame at least once (g872 snap should land on that image, not on Cornell alone).
NOTES
4. Mules g822-871: feet land ~25 px below their shadow, slight float; shadows on a dark strip. Heads/eye-lines fine.
5. Snap g868-881 is a hard whip with frame-diff 26-41 (as planned); legible but a 7-frame near-blur of mid-frame is not characters-sharp: check that characters are sharp at 879-881.
6. Light/palette: s13 trees dark green/shaded, s14 opens on bright lime/yellow trees (same location, same DAY): small continuity jump, note for conform.
7. Heads fine: Cornell head centre ~y 640, bottom of torso crosses y 880 only (allowed).

## s14 (shot 14, g892-957) : FAIL
BLOCKING
1. g898-901 scale/costume pop outside a cut: at g898 (frame-diff 48.5 at 898/899, 33 at 900, 30 at 901) a character (Cornell) fills the lens, head ~420 px wide, torso crossing the caption band, then at g899 he is 120 px, at g900 another character with a straw hat and blue-grey shirt fills the frame again (~380 px head, blush, different costume/hat from Cornell), g901 small. It is the snap-1 crane-up passing through the characters. Fix: move the camera path/staging so no character is within ~1.5 D of the lens during snap 1 (shift workers 3 D sideways or start the snap pose further back); heads must not cross y 880.
2. g938-943 a huge tree (top right, ~40 % of frame) disappears between g938 and g943 (worker admits hiding the tree objects at g941, spike 36 at 941): visible pop. Fix: keep the trees and move the camera path round them, or hide them while they are outside the frame (before g936), not mid-snap.
3. g892-897 plan/composition: opening frames are two mules filling the frame with a grass clump covering the left third; the "furrow longer behind the team" read starts only at g903. Acceptable as a hook of the first snap but shot opens with no furrow; Morse omitted (plan row has no Morse in 14, OK).
NOTES
4. The three counts read (furrow grows 903 -> 923 -> 948, sun goes lower, sky purple at 948+). Snap 3 wide at g948-957: characters 15-25 px, pipe visible. Good.
5. g898 & g900 mouth closed, eyes forward; OK.
6. Light DAY->DUSK only reaches strong dusk after g945; mid shot still warm-day. Fine.
7. Dissolve-out handle g958-966 is a still-ish high wide (diff low but it is handle).

## s15 (shot 15, g958-1006) : FAIL
BLOCKING
1. Frame-diff p90 = 6.06 (recomputed; worker 5.56) vs required >= 12. Camera drifts but the dark static crate scene gives almost no change. Fix: add the planned slide/push strength (>= 60 px/s, 8-10 %/s) and a nearer foreground move (crate edge + coil passing through frame), or the x1.8 snap with real displacement (>= 120 px) at g973-986.
2. Prop/hands (g975-990): Morse never touches the test key. The key lever (grey slab on crate, g965 etc.) is static, Morse's hand is behind the crate edge and nothing shows a press; the "press" is carried only by a pose and the dip. The register is not identifiable anywhere in frame (blue block/blue strip is the coil), so "the register stays silent" has no image. Fix: stand Morse in front of / beside the crate with the key between camera and him, animate the lever (rotate 8-10 deg for g975-981 and g982-987), show the register on the crate with the tape not moving.
3. Eye-lines: Morse looks straight into the lens (g953-1006) instead of at the key/register; Cornell and worker_a look at camera as well. Fix: turn Morse's head/eyes down-left to the key, workers toward the register.
4. Plan "workers lean in, waiting": Cornell (left) leaves the frame by g965 and worker_a/worker_b are small at the right edge from g985; only a lean-shovel pose. Fix: keep Cornell + both workers in frame (pull back ~0.2 D) leaning toward the crate.
5. Brightness dip x0.75 over g986-998 is nearly invisible (frames 985 vs 989 look the same; scene already dark). Fix: dip x0.55-0.6 or add the dip to the sky/foreground too, so it reads as the "เงียบกริบ" beat at g988.
NOTES
6. Morse face bottom ~y 690-800 (hat/hood hair looks like a scarf; costume differs from s13/14 cast, Morse not in those so no direct continuity check); heads OK above y 880. Mouth closed (correct).
7. Mood/tint: dusk is teal-violet vs s14's orange dusk; fine as continuity of falling light, but check in conform.
8. Joins: hard cut out g1007 is inside the handle, as planned.

## Summary
s13 FAIL (3 blocking), s14 FAIL (2 blocking), s15 FAIL (5 blocking incl. p90). qa_auto PASS on all three but it does not catch the g898-901 and g941 pops (spikes were treated as snap motion).
