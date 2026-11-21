# QA_TECH R3, film17 s04 (shots 9-12, render17/team4 f62d987) - VERDICT: FAIL (1 blocking, 3 should-fix)

Viewed at full size (720x1280) and phone-size montages: g445 455 460 466 468 470 491 493 495 499 505 510 520 530 538 540 542 556 558 560 562 564 566 567 575 590 592 594 604-651 (g604 607 609 611 613 615 618 622 625 626 630 633 636 638 640 642 645 651). All three cuts +-2 visible (frame diff g493 41, g540 50, g592 38; rhythm's 2 is a detector miss).
Auto checks over all 218 frames: no black, no magenta, no duplicate/frozen frames, no blur streak over 3 frames (motion bursts 4-6 frames at g466-472, 485-488, 514-518, 531-534, 568-573, 606-610, 634-638 are camera/arm moves, not blur). Rhythm 5.59 / 12.60 OK.

## Team claims
- B1 stray rods/spare calipers: FIXED. g445, g466-470, g468, g520, g512-538 show only Bertillon's calipers, held in his hand (x ~50-240, y ~700-780 at g505). No floating crossed rods anywhere.
- B2 glove in front of ear, tap every 9 frames from g604: FALSE. See B2 below.
- Chest puff x1.05: not distinguishable; torso outline looks the same g604 vs g630.
- Camera wider at end: TRUE (g604 wider, red ear/head fully inside frame; ear touches left edge from g620).
- Chin above y 850: TRUE, chin about y 830-860 at g615-645 (limit 880 OK).
- g505 forearm ends at calipers: PARTIAL, see S1.
- g558-567 bar wobble +-9 deg: NOT READABLE, see S2.
- g460-466 stop-and-look then laugh g467: TRUE. g455 he enters, g460 stands and looks, g466 laughing.

## Blocking
B2. Shot 12 (g604-651) ear tap still absent. At every checked frame (g604-651) the dark ball glove sits on the hip/belt at about x 440-520, y 990-1040 (g615 x 460 y 1040; g630 x 450 y 1020). The arm is a loop: elbow at x ~600, y ~850, forearm back down to the hip. The red ear (x 0-170, y 560-800, g615/630) has no glove, finger or cuff near it. The 9-frame "tap" is only the whole arm/torso bob (arm bursts g606-610 and g634-638, glove travels y 1015->990 only, never up to the ear). At phone size it reads as "hand on hip, grinning/talking", NOT "taps his OWN ear". Fix: move the glove to the ear: target about x 90-130, y 640-700 at g610-632 (in front of the ear card, z above the head card), 2-3 visible taps, hold 8+ frames. Planned beat missing, so blocking.

## Should-fix
S1. g505-510: the pointing forearm ends at x ~300, y ~660 on the prisoner's hat brim/ear; calipers end at x ~240, y ~710. Gap about 60 px and arm overlaps the prisoner's face, so it reads as "poking the prisoner" rather than pointing at the calipers. Shorten/aim the hand to about x 230, y 710.
S2. g558-567: the glove sits on the bar, bar tilt is not distinguishable between g556 and g567 (hidden under the glove, under about 3 degrees seen). Show the +-9 deg wobble on the visible left bar end (x 60-250, y 640-720 at g560).
S3. Shot 12 mouth: only 2 shapes (oval / slit); chest puff x1.05 not visible.

## Other checks
- Floating objects: none. New foreground set pieces (dark panel left edge g520-540, round dome g558-640 top left) are set geometry, fixed to the room, not floating cards.
- Props held: Bertillon's calipers in hand g445-575; no see-through cards, no beam shafts, blue polygon gone.
- Dust: sparse specks, at or under 0.5.
- Mouths: inspector only; Bertillon and prisoner closed in every checked frame. Laugh shape g466-492 only in the allowed window. Inspector mouth open g499-640, closed g651.
- Chins above y 880: pass.
- No frozen hold over 1 s: pass.
