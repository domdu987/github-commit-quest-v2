# TAKE gate QA-tech, film 16, render team 2 (s04, s05, s06, s07)
Method: qa_auto.py on every take.mkv (all PASS; only note = handle continues past the planned cut, cut is made in the conform); 6 fps (every 5th frame) review at 360x640 incl. in/out handle frames; frame-diff recomputed (90x160 area-scaled grey, in-shot pairs).
Frame-diff recomputed (median / p90, team's own value in brackets): s04 5.99/14.75 [5.00/14.05]; s05 8.38/16.31 [6.55/15.71]; s06 5.48/13.20 [4.87/12.58]; s07 5.32/17.16 [4.95/16.49]. All >= 4 / 12. No frozen runs (min per-pair >= 3.5), no black/magenta, no text, no DOF blur, no head above y 880 (max head bottom 812).

## s04 (shot 4, STUDIO studio_wide) : PASS
Notes (non-blocking)
1. g 159-200: Morse head ~100-115 px, a bit under the "wide 110-135" band; he reads small on the phone sheet. Fix if re-rendered: start ~8 % closer.
2. g 215-264: the FG canvas stack covers the lower-left ~35 % of the frame for 1.5 s; acceptable as FG, keep it lower/less opaque if time allows.
3. Contact shadow under Morse is faint; feet are on the rug, scale OK, brush and palette held in hands, mouth closed, eye-line to the easel OK. Plan beats (window, easel with general, busts, canvases, painting) all visible.

## s05 (shot 5, STUDIO studio_easel) : PASS
Notes
1. g 283-313: after the snap the wife's oval portrait leaves the frame; planned beat is "oval portrait on the side table" (visible g 247-285 only, ~1 s, small). Fix if re-rendered: keep the portrait in frame through g 300.
2. g 290-322: big FG canvas stack covers the lower ~30 % (legs/feet hidden); Morse looks at the camera rather than at the canvas (brush points at the easel but eyes are not on it). Cosmetic.
3. Brush/palette held, mouth closed, head 182-312 px at y 482-539, cut-in/out handles continuous with s04/s06.

## s06 (shot 6, STUDIO studio_door) : FAIL
BLOCKING
1. g ~370-388 (the "เมียก็ตายไป" snap, expression frames 12.3-12.9 s): Morse's mouth is drawn OPEN ("O" shock mouth) for ~20 frames. Brief: mouths move ONLY in 18.32-23.20 s and 38.46-40.80 s. Fix: use a closed-mouth shock/sad face (wide eyes, small closed mouth, sweat optional) on those frames.
2. g 391-400 (sit swap) plus the end of the shot: the "sinks onto a stool" beat is broken. At g 391 the standing sprite is hard-swapped for a seated card (frame-diff pop 15.1 at g 391, head drops ~80 px in one frame); the seated Morse is placed BEHIND the stool (stool in front of his torso, no seat contact) and his legs render as a black curved shadow-like arc to the right of the stool (g 392-400). He neither sits on the stool nor has feet/contact shadow in the right place. Fix: place the seated card on the stool seat (stool under him, feet down), hide the arc/decal for the seated pose, and mask the swap with a 3-frame blink or a quick FG canvas pass; keep the set's second stool out of frame.
NOTES
3. Reacting face only 219 px (plan >= 250); the sad look at the wife's portrait is not readable: the portrait is a tiny object in the background and his eyes go to camera. Consider a push on the face at g 373-386 and a turn of the head toward the portrait.
4. Sweat drop on Morse (g ~376-392): bible lists sweat only for the mocker; harmless but outside the device list.
5. g 314-333: first third has the camera swinging past FG canvases; the messenger's feet look cut/peg-like (legs end without shoes) at g 314-390; palette lands on the floor beside the messenger's foot, fine, no injury.
6. Letter handover (g 333 blink swap) OK; letter, palette and brush all in hands until the drop.

## s07 (shot 7, STUDIO studio_window) : FAIL
BLOCKING
1. g 455-475 (coil + magnet): the copper coil sits pinned at his shoulder/chest (screen-left) with no hand on it; only the magnet is held (right hand). Plan: "he lifts a coil of copper wire AND a horseshoe magnet". Fix: raise the left hand to hold the coil (or use the pose with the coil in the hand), coil clear of the body.
2. g 401-445 coverage: outside the window the plan wants "a long road to the horizon"; the view shows rooftops/hills with no road, and Morse stands facing the camera with eyes forward, not looking out. Fix: aim the window preset so the road is visible, or at least turn his eye-line (gaze) toward the window for g 401-445.
NOTES
3. g 455-475: the grin shows a toothy mouth (face swap from closed to grin); not talking, but if the client reads it as lip movement, swap to a closed smile.
4. g 440-460: wife's oval portrait passes the lens as FG (continuity nice); spark at the magnet is small (~40 px) but visible at g 465-475; hand-over to the s08 dissolve fine.
5. Heads 157-269 px, y 521-591, contact shadow OK, feet on floor.

## Summary
s04 PASS, s05 PASS, s06 FAIL (open mouth outside quote; sit beat broken), s07 FAIL (coil not held; window road/eye-line). Re-render s06 and s07 only.
