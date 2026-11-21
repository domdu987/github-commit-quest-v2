# QA_TECH film17 take s04 (shots 9-12, g439-656) — VERDICT: FAIL

Method: 6 fps-equivalent sheets of every extracted frame (f6, 61 frames incl. cuts +-3), full-res on g449, 499, 529, 541, 574, 619; QA.md, QA_AUTO.md, rhythm.txt.
Numbers: rhythm in-shot median 4.01-4.08 / p90 12.02-12.12 (pass, thin margin). qa_auto: only "suspected blur g521-537".

## Blur g521-537: FALSE POSITIVE (confirmed). g529 and g534/537 at full size are crisp (clean outlines, mustache, hat, books, chair all sharp); the Laplacian drop is the smooth wall/chair back. Not an issue.

## Issues
1. g493-539 (shot 10): no calipers anywhere. Inspector's raised hand points at the book shelf (g499, g529: fist/ball over the shelf), not at any instrument; Bertillon is behind, cropped, his hands out of frame. Plan beat "pointing at the calipers" does not read. Fix: put the calipers in Bertillon's (or the inspector's) visible hand and frame them, or aim the pointing arm at them; keep Bertillon's hands in frame.
2. g541-591 (shot 11): calipers are not held in a hand. At g541 they are two loose white sticks crossed (an "X") floating beside Bertillon's torso, below his hand; by g564-574 they are gone entirely. The inspector's arm reaches up at Bertillon's head, not the instrument. The "flick the calipers" beat is not visible. Fix: attach the calipers to the inspector's hand (Actor.pose tip), keep them visible the whole shot, show a flick (tip wobble/rotation) around 17.9-18.5 s.
3. g599-650 (shot 12): the ear-tap does not read. The raised arm goes behind the head; at g619-634 the hand is hidden by the hat/moustache tip and the head sprite has no visible ear, so it reads as a salute / hand behind the head, not "taps his OWN ear". Chest-out is not visible (hand on hip, torso unchanged). Fix: put a visible fingertip on a drawn ear (or on the head side with the face turned 3/4), raise the hand clear of the moustache, add a chest-out scale.
4. g440-490 (shot 9): Bertillon measuring an ear is unreadable. Figures are ~200 px; calipers a thin sliver at g449 near the prisoner's ear, Bertillon's hand not distinguishable. The inspector's shock/see beat before the laugh (g455-466) is just a walk, no visible reaction. Fix: bigger Bertillon/prisoner or a push-in on the measuring pair before the inspector enters; add a 4-6 frame shock pose.
5. g493 cut (shot 9 -> 10): the prisoner vanishes (chair empty in g499-650, g499 clearly). Accepted deviation by the team, but it is a continuity pop across the cut and the measured subject is gone, which also removes the reason for the calipers. Fix: keep the prisoner seated (or have him rise on screen in shot 9/10) so the ear-measuring is the context of the mockery.
6. g509-537 (shot 10): Bertillon's head clipped by the right edge for ~30 frames (only half the face, g534/537). Team-accepted, but with he is the "unmoved" half of the two-shot it breaks the composition. Fix: keep the post-snap framing wide enough to include his whole head, or cut the snap's x offset.
7. g499-537, g574-649: hard-edged translucent blue diagonal polygon laid over the inspector's body/belt (g499, g519-534, g574, g619). Looks like a shadow/ray card artifact, not set lighting. Fix: soften/remove the shadow card or move it off the sprite.
8. Lip-sync: mouth opens/closes inside g493-650 and is visible below the moustache (open brown oval g499, g541, g574, g619), closed at g654 and in the laugh before g493. No outside-quote movement found. Weak point only: shapes cycle between about two (oval / slit), little variety.

## Checked OK
Laugh g467-492 bounce present, gendarmes laugh; no heads over y 880 (inspector chin max ~y 800); no black/blank/magenta, no frozen runs (qa_auto); cuts 493/540/592 present; costume/clock time (9 o'clock) consistent; Thai text: none in take.

## Verdict
FAIL: plan beats 10 (point at calipers), 11 (flick calipers) and 12 (ear tap) do not read; calipers not in a hand in 10-11. Fix issues 1-3 (and 4-6 if possible), re-render shots 10-12 (shot 9 if 4 is addressed).
