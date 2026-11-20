# QA-art TAKE gate round 9, film 20: s24 (BIGZOOM 2 re-render, take g1724-1858)
Reviewer: QA-art (opus). Viewed full size (g1724, 1736, 1750, 1764, 1778, 1830) and as 180/360 px sheets: every 8 f overview, every 3 f g1736-1802 (zoom), every 4 f g1780-1858 (landing/bites), 360x640 at g1736/1748/1760/1772, simulated dissolves s23->s24 (g1726-1738) and s24->s25 (g1849-1857).
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/qa9s24/ (ov, zoom, bite, s360, din, dout .jpg).
Stats (every 3rd frame): saturation 0.75, luma 90 -> §G.1 / §I.3 OK.

## Verdict: PASS with notes

The §E blocker (zoom too short, he not findable at the start) is fixed. This is now one smooth BIGZOOM: he is findable from the first clean frame, the move takes ~3.3 s, and it lands on a happy bite. Remaining items are polish and do not block.

## Do we understand we go INTO the tower's restaurant?
- Yes, mostly. The opening (g1724-1757) shows red-orange riveted lattice overhead, the iron girders of the first platform, green park far below (so we are high up on the tower), a red facade band, a striped red awning and the RESTAURANT sign above a lit window full of white tables and chandeliers. Coming out of s23 (officials in front of the tower's base and the EXPOSITION 1889 banner), "up the tower, into its restaurant" reads.
- Tower context is implied (lattice + height), not shown. There is no silhouette of the tower in this shot. That is acceptable because s23 carries the tower. A wider first frame would make it stronger but is not needed.
- The sign is readable at 360x640, but the word is never shown whole after the dissolve: the foreground red lattice post covers the R (and at times the E) from g1736 to g1757, so it reads "ESTAURANT"/"STAURANT". At g1763-1769 the R returns, but the right end is cropped ("RESTAURA..."). Viewers will still read it as RESTAURANT.

## Findable early?
- Yes. At g1736 his white face and blue coat are already clear in the window, left of centre at x ~0.47 W. He is about 5 % of frame height and is the brightest, most central figure in the window. He is already eating: his mouth is open with a forkful at g1736-1750 and g1784-1796.

## One smooth BIGZOOM?
- The frame-difference curve is one clean bell, 12 -> peak 26 at g1765 -> eases to 8 by g1834 -> hold at 3. There are no cuts, jumps or stalls. A small step at g1773-1774 (21 -> 16) comes from the window frame leaving the shot and is invisible in playback.
- Path: facade and sign -> sign grows huge (g1760-1769) -> the X-braced window frame wipes past on the left -> into the room along the red/blue carpet runner -> medium on him. The window frame wiping past is a good §I.1 "through the opening" moment.
- Subject goes from ~5 % (g1736) to ~40 % figure / head ~250 px (g1834) in ~3.3 s, which satisfies §H.1 and the §E ruling.

## Landing and bite
- He is centred under the chandeliers at the end of the carpet runner. The first full bite at landing is g1824-1838: an orange forkful at his mouth, eyes squeezed shut, blush. He then grins with knife and fork up (g1840-1858). There is a pre-bite during the zoom (g1784-1796), which helps. This is pure contentment and reads at phone size.
- Landing size: head ~20 % H, under the 35 % cap. It is a medium, not a face close-up.

## Set richness
- The room still has: red trusses, three tiers of gilt chandeliers, ~15 diners in top hats/bonnets, tables with glasses and plates, bentwood chairs, a coat stand, palms and the carpet runner. The interior is rich.
- The back wall (g1800-1858) is still a plain khaki plane, as noted in round 6 (non-blocking).

## Defects (all non-blocking; conform or next re-render)
1. **Black squares on post caps, g1724-1757:** two black rectangles at the tops of the window posts. At g1724 they are at about (243,393) and (598,408). At g1750 there is a larger one at about (100-165,105-220). It is in the first second the viewer sees, so paint them out in conform (fill with the orange beam colour). In the scene, these are missing or unlit faces on the post tops.
2. **Black void inside the room, right side, g1756-1784:** the area beyond the red pillars (g1778 x 600-720, y 400-650; g1764 x 480-640, y 400-560) is pure black, an unlit or unbuilt part of the set. It is in motion and ~1 s long. At the next re-render, light it or close it with a wall or window. Otherwise leave it.
3. **Sign (blocky pixel letters), g1760-1769:** at this size the extruded letters show stair-step edges, so they read as a pixel font rather than painted Belle Epoque lettering. They stay sharp and readable, so this is a style note. At the next re-render, use a smooth serif font. Also move the foreground post or the camera ~40 px so the R is not covered at g1736-1757.
4. **Orange slabs:** the facade band and the sill below the window (g1760-1790, up to ~35 % of the bottom of the frame) are big flat orange planes with sparkly noise grain (8 samples). The sill wipes past fast, and the grain is only visible at full size. Optional: denoise/grain-match in conform.
5. **Floating or seams:** none found. The round-6 vertical seam (g1787-1796) is gone. The diners are seated, and nothing hovers.

## Joins
- **In (s23 -> s24, 13-frame dissolve at g1732):** the ground-level officials in front of the tower base dissolve into the orange iron facade, with RESTAURANT appearing behind their heads (g1730-1734). The warm orange iron continues the tower colour from s23's background, and reading it as "up the tower" works. The mid-dissolve is busy for ~4 frames (faces over the post and sign), which is acceptable for a dissolve.
- **Out (s24 -> s25, 9-frame dissolve at g1853):** the warm room becomes the blue-sky window reverse. His head is in the same column (x ~0.45 W). The s25 head sits ~60 px lower and is a little smaller, so g1853-1855 shows a mild double face. This was already ruled acceptable in round 6. It stays acceptable.
