# QA-tech s10 r2 RE-CHECK (shots 10-12, RAIN, g645-866) - VERDICT: FAIL

Checked: all 44 f6 frames (via phone sheet + montages), consecutive frames g651-666, g664-713 (every 4th), g719-740, g736-776, g776-830 (every frame g782-799), cuts g714 and g774 +-3, per-frame difference over all 222 frames (tmp folders deleted). Image limits: frames were viewed as 4-5 frame montages (360-450 px per frame) plus full-size spot checks (g807 etc.), not every frame at 720x1280.
Cuts: real. Frame diff at g713->714 = 51.5 and g773->774 = 31.6 against a median of 7.6, exactly on the planned g. qa_auto's "no visible change" note is a false flag. No frozen, black or magenta frames. Heads all < y 880. No blur, no text. Light RAIN, coat/umbrella constant.

## Round-1 issues
1. Mud splash is a flat wall of cones plus round balls: PARTLY. g791-g802 is now a real crown: tapered translucent fingers in 2-3 tans with pointed teardrop tips and orange streaks arcing over his hat; no ball clusters; no full-width wall. BUT g803-g816 the falling phase is large flat translucent brown polygon slabs with hard straight edges (g807-816 left of Hanway, a rectangular slab at g813-816), and the whole splash vanishes in one frame g816 -> g817. This is the flat-sheet look the client forbids, for about 14 frames, and it ends in a pop. See N1.
2. Not "head to toe": PARTLY. Now face, hat, coat and legs carry about 25 brown splats from g788 (coat covered in oval blobs, face spotted, tears/drips on face). Coat is still mostly blue; the splats on the coat are fat ovals, closer to blobs than to wet mud, but they read as "mud-covered". The spray itself never visibly lands on him (it falls to the left, behind).
3. g785->786 pop: FIXED. The coach approaches over g776-786, wheel arrives next to him, shock builds g788-791 (no one-frame jump). Minor: mud spots appear on his face at g788 while no spray is visible yet (spray first visible g791-792); causality is 3 frames early.
4. Splash origin: PARTLY. A real coach now charges past him (wheel at his side g786-800) and ripple rings spread on the ground at his feet, but the crown rises behind and to the LEFT of Hanway, while the wheel is on his right; the foreground puddle is still undisturbed.
5. Egg: FIXED. Cream, oval, leaves coachman_c's raised hand at g724, flies a visible arc over the umbrella (g725-731), lands on the dome at g732.
6. Egg splat pop: FIXED. Splat appears at g732 on arrival, egg gone that frame; never both.
7. Cabbage: PARTLY. ONE cabbage leaves coachman_b's hand at g654, 9-frame arc, no pop, no duplicate, same green as the leaf: FIXED. But the leaf never sits on the umbrella (new failure N2).
8. Mouths: FIXED. Spot checks g663, g690, g730, g744, g752, g768: thrower scowl closed, box coachman and coachman_c closed smirk, crowd closed. No open mouths.
9. Leaf size: FIXED (about 100 px wide, readable on the phone sheet).
10. coachman_c cropped by the right edge: PARTLY. He stays in frame until the egg lands, then is cut by the right edge g748-g760 while walking off. Non-blocking.
11. Umbrella hand: FIXED / not re-verified in detail (hand reaches the hook in g719-740).
12. Years not shown: unchanged, non-blocking (captions cover it).

## New failures (blocking)
N1. g803-g816 splash falling phase = flat hard-edged translucent brown slabs (client rule: never a flat sheet), vanishing in a single frame at g816->817. Fix: break the slabs into streaks/teardrops, shrink and fade them over 6-8 frames, no straight polygon edges.
N2. g663-g713 (51 frames, 1.7 s) the "stuck" cabbage leaf hovers 25-40 px ABOVE the umbrella dome and never touches it (clear sky gap at g690, g710), while Hanway walks. The slap never happens. Fix: place the leaf on the canopy surface (centre on the dome, rotated to the dome tangent), riding with the umbrella.

## Notes (non-blocking)
- Mud on the coat/legs is fat ovals; make them smaller/irregular with drips.
- Coach in the distance at g803+ is a second coach; fine.

## Verdict: FAIL (N1, N2; items 1/2/4 partly fixed). Cabbage release, egg, anticipation, mouths and cuts are fixed.
