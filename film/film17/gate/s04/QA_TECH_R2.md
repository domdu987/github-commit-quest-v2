# QA_TECH R2, film17 s04 (shots 9-12, render17/team4 b3326ff) - VERDICT: FAIL (2 blocking, 4 should-fix)

Viewed at 720x1280: g445 455 466 470 480 491 493 495 510 520 538 540 542 556 558 560 562 566 575 590 592 594 596-616 (every 4) 620 624 630 636 640 645 648 651. Cuts +-2 checked at g493, g540, g592: all three show a visible framing change (QA_AUTO's "no visible change" note is wrong). Rhythm: in-shot median 5.69, p90 13.16, no blur streak over 3 frames seen, no frozen hold, no black/magenta.

## Round-1 items
1. Calipers in shot 10: PARTIAL. Calipers are visible and held in Bertillon's hand (g499-538) and he is whole in frame. But the inspector's pointing arm sweeps over the prisoner's hat/ear (g510), not at the calipers, so "pointing at the calipers" is weak.
2. Shot 11 calipers held: PARTIAL. g558/g560 his dark ball hand sits on Bertillon's bar (touch reads), but no wobble is distinguishable between g556-g566. At g575/g590 his hand holds only a thin grey stick (tip at hand, x 690-720, y 760); the instrument is not recognisable.
3. Shot 12 ear tap: FAIL, see B2.
4. Shot 9 pair size: FIXED. Bertillon + prisoner span about 400 px (g445-470), calipers on the ear are readable. Inspector's shock beat (g455-466) is still just a walk (g455 he is not even in frame; g466 already laughing).
5. Prisoner vanishes: FIXED. Seated in chair g445-651.
6. Bertillon clipped by right edge: FIXED. Whole head in frame g499-538. Later shots crop him by design.
7. Blue translucent diagonal polygon: GONE (g499/510/520/574/620 clean).
8. Lip sync: OK. Inspector mouth open/closed only g467-651 (laugh shape g470 allowed, quote shapes g499-640, closed g651). Bertillon and prisoner mouths closed in every frame. Still only 2 shapes (oval / slit).

## Team claims
- Prisoner seated, calipers pinned on ear in Bertillon's hand: TRUE g445-566.
- Shot 9 inspector stops and looks, laughs from g467: PARTLY. He enters g466 already laughing (tears, closed eyes); no stop/look beat.
- Shot 10 two-shot, pointing at calipers, Bertillon fully framed: TRUE for the two-shot and framing, weak on pointing (item 1).
- Shot 11 finger touches bar at g558, bar wobbles: touch TRUE, wobble NOT visible.
- Shot 12 red ear, fingertip on ear, chest puff: red ear TRUE (large, g596-648, cropped by the left edge from g620). Fingertip on ear FALSE. Chest puff NOT visible (only the push-in scale growth).
- beam_fx hidden, dust 0.5: sparse dust specks visible, no beam seen.

## Blocking
B1. Leftover/floating crossed rods, no hand: g445 (x 630, y 790, white X on the floor/wall), g466-470 (rod tip at x 690-720, y 880 by the belt, floating), g520 and about g512-538 (white crossed rods at x 640, y 710 over his belly; the ball hand is beside it, not gripping). Fix: hide the spare caliper prop outside shot 11 or attach it to the hand pose (g520).
B2. Shot 12 ear tap does not read (g596-648). His arm is bent with the hand on the hip/belt (ball hand at x 340-480, y 950-1000 at g640); no fingertip touches the ear, which is the large red ear at the frame edge. Planned beat "taps his OWN ear" is missing. Fix: raise the hand so the fingertip lands on the ear, held 8+ frames around g610-630; add a chest-out scale.

## Should-fix
S1. g510: point the arm at the calipers, not the prisoner's hat.
S2. g556-566: show the bar wobble (tip rotation 3-4 frames after g558); g575-590 the stick in his hand is unrecognisable as calipers.
S3. g455-466: add a 4-6 frame stop/look shock before the laugh.
S4. Chin margin: inspector chin about y 850-870 at g608-636 (limit 880); keep the push-in from going lower.
S5. g620-640: chest-out missing (see B2); mouth shapes only 2 variants.
S6. QA_AUTO cut-detection note is a false alarm: cuts are visible. Rhythm detects only 2 because one cut is low-contrast (same room), not a defect.

## Checks OK
No see-through cards, no black/magenta, no blur, no frozen holds, blue polygon gone, props held except B1, mouths closed outside window, heads above y 880, costume/clock consistent.
