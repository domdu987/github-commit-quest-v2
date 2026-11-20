# QA-tech sD2 v2 (team4 047cf15)

Method: every 5th frame (31 in f6), full-size frames n0-8, 40, 116-135 (g758-777), 148-154, plus g667/687/692/712/747. 155 frames, 720x1280.

## Verdict: FAIL (1 blocking, easy fix)

## Fixed against the old list
1. Edge cut Surrey (old 1): FIXED. No head or body crosses a frame edge at g754-786. Surrey is hidden behind Cressingham during the CU, then steps back out.
2. Purse slap (old 2): FIXED. The right hand drops to the purse at g758-762, with a glint star and hopping coins, hand held on the belt. Reads with sound off.
3. Red barrel (old 3): FIXED. Replaced by a grey strongbox, sacks, a spear bundle and pegs. His feet stay visible. Near ground is dressed, and the tilt-up cuts the bare sand.
4. Surrey merged into the neck (old 4): FIXED. He is offset and readable g643+.
5. Handles (old 5): FIXED. g793-796 continue to move (RMSE g793 vs g796 about 0.14).
6. Point (QA-art): FIXED. The arm is raised up-left toward the crag, with saltires readable on the hill. The bridge shows as a thin span behind him from about g722 (still tiny, non-blocking).
7. Floating pennants: none seen.

## Beat table
| g | caption / beat | picture | read at phone size |
|---|---|---|---|
| 642-647 | whip in | empty beach, spear pair, strongbox, soft/streaked | OK (whip) |
| 648-690 | "ชาวนาบนเนินไม่กี่คน!" | Cressingham small (about 22 % of frame height) in the mid-ground, arm up pointing at the hill, mouth moving, Surrey tired behind. Tent and campfire. | OK but small |
| 690-720 | "อ้อมไปเปลืองเงินหลวง" | waddle, tilt up, spear pole crosses his face g686-698 | pole is a nuisance |
| 720-750 | "ข้ามสะพานนี่แหละ" | bridge enters behind him, saltires on the crag, point held | OK |
| 750-756 | "เร็วดี" | stop, push begins | OK |
| 756-765 | push, slap g758 | star glint, coins, jolt | strong |
| 765-778 | "ประหยัดดี!" CU1 | face about 25 % of frame height (hat+face about 47 %), purse in shot | OK, under the 35 % face limit. Hat ruff and arm touch the left edge at g764-776. |
| 778-793 | pull-out | hands on hips, smirk, Surrey steps out | OK |
| 794-796 | handles | continue the pull-out | OK |

## Checks
- Mouth: moves only inside g642-791 (open at g790, closed from g792, smirk). PASS.
- Heads: Cressingham head centre y about 440-700, always under 880. PASS.
- CU: only the one CU1, about 0.5 s of full push plus about 0.5 s hold. PASS.
- Colour story: English red/gold only. Blue appears only as the Scots saltires on the crag, the dark spear tips and the purple shadow on the tent. No blue in the camp itself. PASS.
- Bloodless: PASS. No money-counting gag is planned in the D2 row, so none is required.
- End pose: g793 is a hands-on-hips smirk at P_BANK, Surrey at about 77 % of the width. The meta says it is exactly P_BANK. I have no E1 start frame to compare against.

## Issues
1. BLOCKING, g660-755: the background soldier (e1) stands at the water edge directly above Cressingham's hat, so his helmet and face sit on the hat as a stacked head. It reads as a second head on a stick and as floating. Fix: move him 1.5 m or more sideways, or hide him, so the hat has clear water behind it. The simplest option is to hide e1 until g756 or delete him from this take.
2. Non-blocking, g684-700: a foreground spear bundle (two tall poles with tops cut at the frame top) passes over his face for about 0.5 s. It is acceptable as parallax. Better: shift the bundle 0.5 m left so the poles miss his head. The poles also have no visible base after g700, so they look slightly floating. Add a base, or accept it.
3. Non-blocking, g643-700: Cressingham is only about 22 % of frame height and the bridge is not in frame until g720. Fix, if there is time: push the track in 10 % at the start.
4. Non-blocking, g764-778: the hat ruff and pointing arm touch the left frame edge in CU1. Fix: slide the camera 40 px left.
5. Non-blocking: the spear tips are dark blue (English camp). Recolour them to steel or gold.
