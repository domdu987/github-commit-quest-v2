# QA-tech FINAL-fix s06: FAIL

Checked every frame g495-530 (36 frames, montage plus 1:1 crops) and the 6 fps sheet for g459-530.

## Blocker fixed
- Tian Dan (yellow robe, flat cap) stays fully inside the frame at g495-530. His cap, body and feet are clear of both edges, and nothing stands in front of him. He is now small and mid-frame. **PASS.**

## New regression (why FAIL)
- The basket-carrying child added at lower left grows as the camera pushes in. His chin passes the caption line.
  - Lowest skin pixel, measured by skin-colour mask: g517 y830, g521 y850, g523 y867, g525-529 y880-881.
  - With the outline the chin reaches about y887. This is at or past the y 860 head limit, and the face enters the caption band (880-950) for about g523-530.
- The child and the old man behind him are also cut by the left edge from about g500 to the end, and the child's body is cut by the bottom edge. They are secondary characters, so this is a note.
- Suggested fix: lower the child's scale or move him back or left so his chin stays above y 860 through g530, or drop the carriers from about g515.

## Other checks
- No pole through any face. The hairpin on the old man's cap is part of the cap. The child's hair buns overlap the old man's chin, which is a layering note only.
- Oxen are still plain: no blades and no coats.
- Frame diff, measured on the take: median 6.47 and p90 10.85 with area downscale (bilinear 5.65 / 9.75). This matches the team's 6.47 / 10.84. OK.
- The team's claim "heads above y 880" is not borne out. The child's face does reach about 881-887.
