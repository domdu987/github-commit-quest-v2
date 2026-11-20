# QA-tech s12 ROUND 2 (shots 29-30, g1689-1874, commit aceb5fc) — FAIL (one blocking item, plus claim gaps)
Checked 6 fps + cut g1786-1792 (44 frames, 10+ viewed full size as 3-up montages and chin crops). Auto: PASS. My own all-frame diff: cut spike 40.8 at g1788->1789 (planned cut OK); every other pair 4.0-6.0, so no pops, no frozen run, no blank/black/magenta (mean luma 80 constant at head), dissolve-in is a conform-side handle (g1689-1694 handle, take opens opaque; mean luma/diff flat). Post-cut camera ease is now smooth (diff 5-6, was 7.8-8.2 in R1).

## Round-1 items
1. Dark slab foreground in shot 29: FIXED. Lower third is clear carpet. Desk edge and stool still visible at left (g1689-1779), small, not occluding; claim "crates and stool hidden" is only partly true (back crates behind Dupont's legs remain, stool visible). Non-blocking.
2. Small card / Dupont cropped: FIXED. Card ~95x110 px frontal, mugshots + bottle readable at full size; Dupont right of Bertillon, full body. Minor: Dupont's right hand touches the right frame edge g1689-1709 (~5 px).
3. Shot 30 gendarmes bring thieves, stagger: PARTLY. Three groups are already present at g1789 (foreground blue gendarme + thief, mid brown-hat thief + green gendarme, far beret + blue gendarme) and sit in the same places g1794-1804. No visible entry at g1801/g1813 (should-fix S1). Foreground pair does walk toward camera and grows, reads OK.
4. Giant floating cards / pile: FIXED. No pile, no oversized cards. Drawers stick out along both walls and 3-card mugshot clusters sit on drawer tops/mouths from far to near (g1829-1874). BUT cards are ~12-18 px wide, unreadable at phone size, and I cannot see a drawer opening-and-popping in the 5-frame samples; beat "cards found one after another" is weak at phone size (S2).
5. Cards bury characters: FIXED. Characters unobstructed.
6. Card continuity: shot-30 cards are tiny, cannot verify texture; no mismatch seen.
7. Open-mouth shouting faces: FIXED. Mouths closed. But thief (foreground) is half-lidded/bored with blush, gendarme angry-frowning; "closed, worried" is not what reads (S3).
8. Cut vs narration: cut at g1789, ~3 frames early vs 1792; acceptable (stated caveat).
9. Camera head jerk: FIXED (see above).

## Claims
- Shot 29 card 2.1x, frontal, in raised hand: TRUE. Hand sits under the card bottom edge g1689-1784, card follows hand; not floating. Beard dissolve: TRUE (full goatee g1689-1729, half g1734, ghost + smile g1744, clean by g1749), card unchanged. Bertillon's own goatee stays (correct).
- 14 drawers open far to near, 3 true-size cards each: NOT VERIFIABLE/doubtful at sampled frames; I count ~8-10 open drawers visible with cards on only ~6. Not blocking.
- No pile: TRUE. Bertillon points: TRUE (arm out toward drawers, g1789-1874); he holds a red book/folder, not a card, in the other hand, attached to hand. Camera eased: TRUE.
- Far figures ~60 px: TRUE (head ~45-60 px), readable as figures. Bertillon himself is small and, g1814-1869, partly hidden behind the thief's head (S4).

## Other checks
No see-through cards, no beam shafts on characters (light shafts only on ceiling), no leftover rings/rods, dust sparse (<=0.5), no blur (sharp throughout), no mouth movement. Props held by hands: yes.

## BLOCKING
B1. Chins below y 880 in the foreground pair, approx g1824-1844: gendarme chin about y 885-890 and thief chin about y 890-895 (g1829 crop: both ~10-15 px over the band; g1819 ~845, g1849 ~865 are fine). Fix: raise camera/pair end position or stop the pair's approach ~8 % earlier (scale <=0.9 at its nearest point) so chins stay <= 870.

## SHOULD-FIX
S1. g1789-1813: stagger not visible; all three groups on screen from the cut. Start groups B and C out of frame/behind far end and walk in at g1801/1813.
S2. g1829-1874: cards 12-18 px; at phone size reads as drawers only. Enlarge the pop cards (~25 px at far end) or add a visible pop motion/ highlight per drawer.
S3. Thief expression: swap sleepy/blushing for worried (brows up, sweat).
S4. g1814-1869: shift Bertillon off the thief/gendarme overlap so his face and pointing arm read.
S5. Dupont hand touching right edge g1689-1709.

Verdict: FAIL on B1 only (fix is small, one re-render of shot 30 tail); shot 29 passes.
