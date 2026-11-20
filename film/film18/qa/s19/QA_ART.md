# QA-art round 16 s19: FIX-FIRST
s19: burning oxen burst out of the wall holes (g 1427-1514). I extracted all 100 frames (g = 1421 + n). I judged a 144x256 phone sheet every 5th frame (about 6 fps), full-size frames at g 1436/1451/1466/1481/1496/1506, a strip of the lead's jaw area (x 420-720, y 620-870) every 2nd frame from g 1456 to 1502, and 2x crops at g 1466/1480/1482/1484/1500. Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa16/ (s19_phone.jpg, s19_fullA.jpg, s19_fullB.jpg, s19_jaw.jpg, s19_jaw2.jpg).

## Checks
1. **Does "oxen burst out of the holes in the wall, glowing tails" read? YES, minimally (note).**
   - On the phone you see a lit wall with broken holes, and a raging ox stepping out of a hole with a small flame trailing behind on its tail stick. The flame is clearly behind the ox, never on its head.
   - The 18 far-lane head-on oxen show as a short column of small red oxen in the distance at about g 1470-1490 (visible on the jaw strip). They are too small to change the read on the phone.
   - It still reads as "an ox comes out, then another", not a burst. With the round-16 bar, that is a note, not a blocker.
2. **Near-lane density of 1 ox every 18 frames: NOTE.** Usually 1 near ox plus a distant cluster is visible. The team's reason (9-frame spacing puts flames on faces) is accepted.
3. **Pot removed from the lead's jaw: NOT DONE. This is a hard-rule break (prop through a face).** A terracotta pot still sits in the lead's path, and its rim covers the lead's lower jaw and open mouth:
   - **g 1482:** the pot rim (about y 800-810) overlaps the bottom of the open mouth.
   - **g 1484:** the pot covers the whole lower jaw. The pot is at x about 615-720, y about 805-890, and the mouth is cut off at the rim.
   - **g 1486:** the same overlap, as the lead exits.
   - **g 1464-1468:** the pot rim touches the chin.
   - **g 1498-1502:** a second ox's mouth (y about 770-790) is partly covered by the same kind of pot at x about 630-700, y 770-820.

   On the phone this reads as "the ox drinks from the pot", which is the exact round-14b gag-killer. The team's QA.md says this was not frame-checked. The pots at (16.6,-10.6) and (18.6,-8.4) were removed, but the pot actually in the lead's path is a different one.
4. **Flames on heads: OK.** Gaps under 15 px appear only at isolated frames (g 1443 and 1475-1477, as the team reports). These were not visible as a burning head on the strips.
5. **Ground looks empty (note only, as instructed):**
   - At g 1466-1501 the lower third (y about 860-1280) is bare pebbled dirt. The "26 rubble props" are not visible in those frames.
   - The opening (g 1421-1441) has big foreground pots and reed bundles, which helps.

## Verdict: FIX-FIRST (1 blocker, small and measurable)
1. **Move the near pot out of the lead's path.**
   - The pot is the one that renders at about x 615-720, y 800-890 at g 1484 (and at x 630-700, y 770-820 at g 1500). Shift it at least 1 D toward the camera or sideways, or drop it.
   - Pass check: no prop pixel over any ox's face or mouth on every frame g 1460-1505, checked at 2x zoom.
2. **Optional, same render:** lay 3-5 dark rubble chunks or broken bricks from the holes in the lower third at g 1460-1500 so it does not look like bare dirt. Keep their tops below y 860.

Everything else passes:
- The wall is rich.
- The fire-against-moon-blue palette is good.
- The rage faces read.
- The rim is clean.
- Frame-diff (median 11.5, p90 15.7) comes from real camera travel.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 5 | 7 | 5 | 7 | 7 |
