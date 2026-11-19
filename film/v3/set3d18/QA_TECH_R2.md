# QA-tech, SET gate, film 18, round 2 (tiles s01..s26)

VERDICT: FAIL (3 BLOCK items: s04, s24, hay card in s02/s26)

Method: all 26 tiles at 720x1280 and 360x640; head rows from sNN.json at t 0 / 0.5 / 1; hue_rows.txt; framediff_r2.txt; own measurements (Laplacian variance, caption band y 880-950 luma > 200, magenta hue, blown pixels).

## Global checks
- Heads: no person or ox head has chin >= 880 at t 0 / 0.5 / 1 in any shot (max chins: s01 849, s05 843, s09 849, s14 837, s17 839, s18 835, s24 805). PASS. Shots with 0 head rows: s03, s04, s07, s20, s25 (vista / herd-only, rule vacuous); s21 lists 3 heads at t 0 only and none at 0.5 / 1.
- No blank, black or broken frame. Magenta max 5.8 % (s05), limit 10 %. No text anywhere. No DOF look.
- Frame diff start vs end: min mean 7.9 (s11), 11.6 (s09), 14.3 (s14); all moves visible. PASS.
- Blur (Laplacian variance, median 201): below 60 % (< 121): s05 119, s11 103, s20 102, s22 102, s23 120. All flat sky or ground, not DOF (TAKE, no action). s07 is a high outlier, 1179 (5.9x median), from the dense herd detail, not a defect.
- Caption band (880-950) bright (luma > 200) share, own measure: s04 7.04 %, s03 4.98 %, s07 2.55 %, s25 2.04 %, s09 1.82 %, s13 0.61 %, all others 0. Matches the builder's "could not meet" list.

## Round-1 issues
1. s10 heads: FIXED. Chin 728 / 748 / 783, general head top 545-581.
2. s15 heads: FIXED. Chin 715 / 725 / 738.
3. s24 soldier at 880: FIXED. Max chin 770 / 785 / 805.
4. s01 ox head at t 1: FIXED. Chin 759 / 792 / 849.
5. Caption-band emitters: PARTLY. s10, s23, s19, s15, s14 now 0 %. OPEN: s04 7.04 % (was 7.1), s03 4.98 % (was 5.0), s07 2.55, s25 2.04, s09 1.82, s13 0.61.
6. s23 fg brazier and townsfolk: FIXED. No lens-edge flame, 8 townsfolk visible beating pots on the wall walk, chin 753-793.
7. s16 holes: PARTLY. Diggers (7, heads 595-681) and baskets are in frame and the stray pole is gone. The breaches are small ragged outlines, only one reads as a dark opening, and there is no clear rubble heap. A post with a basket is clipped by the left edge. TAKE.
8. s17 / s18 / s19 holes: PARTLY. s17 reed bundle is small, oxen 6 at the holes, ox head chin 839. s18 OK (Tian Dan with torch). s19: oxen are small (heads 641-672) in a row at the wall base, the breach dark openings are barely visible, and a clipped orange block sits at the top-left (x 0-70, y 30-200). TAKE.
9. s07 herd: FIXED. High view, a dense herd of about 190 cards, readable at phone size; the foreground pen fence is still there but does not hide the herd.
10. s22 ox: FIXED. Ox is 391-498 px tall with a soldier beside it. Notes: the ox face is cut by the right edge and the hind legs look detached from the body (card seam). TAKE.
11. s21 herd wall: PARTLY. Oxen now come at the lens against the gate. Tail flames are not lit, the 3 soldier silhouettes are not visible, and a dark seam band runs at y 570-600 on the left. TAKE (re-aim and light the tails).
12. s20: FIXED. 4-5 large oxen in frame, blue 77 %, L 102 (flat road, not a blur).
13. s13: PARTLY. Party crowd 13 heads and cups are visible. A dark block is still clipped at the right edge (x 660-720, y 290-350) and the fg barrel and stump are cut by the bottom edge. TAKE.
14. s24 rout: OPEN, BLOCK. Fg tent roofs fill the lower 60 % of the frame. Soldiers are about 30 px, no flying pots or helmets can be seen (two dark crescents in the sky), no chariot rolling, the tents are not clearly folding. Beat not readable at phone size.
15. s11 / s08: s11 FIXED (7 figures, heads 560-654). s08 PARTLY: general on the rampart is in frame (head 425-656) but the dark block fragment at the top-left (x 0-55, y 95-185) is still clipped and floating, and the red slab behind the general remains. TAKE.
16. s26 / s05: s26 FIXED (general head 483-702, 3 oxen near, readable). s05 PARTLY: stall and townsfolk are in frame, the counting board is not clear, the fg counter is still a chunky block clipped at the right. TAKE.
17. Vista pennants: OPEN. Count unchanged (62 + 2). s04 has a giant flat orange flag quad (about 350 x 180 px) and a blown glow stalk in the middle; towns are still salmon brick. BLOCK for s04 (the flag quad reads as an error and the flare is the 7 % band emitter). s03 / s25 TAKE.
18. Blue murk: PARTLY. s14 92.3 % blue (luma 78), s15 86.4 % (luma 63), s24 94.0 %, s19 90.7 %. Improved from 93 / 94 % on s14 / s15 only slightly. s20 77 %, s21 49 %, s22 44 % are fixed. TAKE (warm grade or practicals in the take).
19. Scale: FIXED. s19 oxen are in scale with the wall (2.6 D).

## New failures
N1. BLOCK: pale faceted "hay" card with stick spikes, 140-190 px wide in the near foreground of s02 (x 460-640, y 690-900) and s26 (x 430-650, y 790-980). It reads as a floating hand or debris. Remove it (SKIP) or ground it as a hay bale.
N2. BLOCK: s04 giant flat flag quad and blown flare (see 17).
N3. BLOCK: s24 rout unreadable (see 14).
N4. TAKE: s03 floating cloud with a flat line at the top-left (x 0-140, y 60-110).
N5. TAKE: s02 post with bowl clipped by the left edge (x 0-120, y 640-970); s01 dark fg pole and barrel clipped by the right edge.
N6. TAKE: s07 caption band 2.55 %, s09 1.82 %, s25 2.04 %, s13 0.61 % bright emitters (tilt the camera in the take).
N7. TAKE: s02 caption band mean 124 (lit pink lane), above the 60-110 target.

## Missing plan elements
s16 clear breach heap (weak); s19 oxen bursting from holes with dust (weak); s21 soldiers and lit tails; s24 flying pots, helmets and chariot; s05 counting board; s25 70+ pennants (62 + 2). All else present.

## Classification
BLOCK (set must change): N1 hay card (s02 / s26), N2 s04 flag quad and flare, N3 s24 rout.
TAKE (render team): 5 (s03 / s25 / s07 / s09 / s13 band emitters), 7, 8, 11, 13, 15 (s08), 16 (s05), 18, N4, N5, N6, N7.

## Director note (gate decision, 2026-11-19)
QA-art (Opus, independent, saw every frame) PASSED round 2 (QA_ART_SET_R2.md) and classed these three QA-tech BLOCKs as take-level.
They are NOT waived: they are MANDATORY fixes inside the owning takes, done at runtime from shot.py, and QA-tech checks them at the TAKE gate:
1. s04 flag quad + flare -> team owning s04: opaque Qi/Yan flag without bloom, no blown glow stalk, caption band bright share <= 1 %.
2. s24 rout unreadable -> team owning s24: QA_ART_SET_R2 instruction 10 (soldiers >= 70 px, 3-4 flying pots/helmets, chariot, sky <= 30 %).
3. Pale stump/hay card in s02, s26 -> hide it (QA_ART_SET_R2 instructions 5 and 11).
