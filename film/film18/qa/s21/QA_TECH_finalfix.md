# QA-tech FINAL-fix s21: FAIL

Checked every frame g1596-1682 (87 frames; montage plus 1:1 crops) and the 6 fps sheet.

## (a) Foreground pots: PASS
- The pots, bowl and helmet are opaque clay or bronze, with outline, rim and texture.
- They are not glowing and not see-through. There is only a mild warm gradient at g1596-1620.

## (b) Cups: FAIL
- The held cup at g1645-1650 (top right, above the herd) reads as a gold jue cup with posts.
- The falling cup at g1654-1680 does not read as a bronze cup.
  - g1654-1658: a flat mid-orange disc, like a gong or plate, mostly cut by the right edge.
  - g1660-1666: a flat orange wedge or bowl, again at the right edge.
  - g1668-1674: a thin post and stub, cut by the edge.
- Flat orange with no metallic highlight, mostly off-frame. It is no longer beige, but it reads as an orange blob, not a bronze cup.
- Suggested fix: keep the cup inside the frame (x < 650) while it falls, add specular highlight and a darker bronze base colour, and show the bowl opening and legs in a side view.

## (c) Palette: PASS
- The sky is flat cobalt, the ground navy, with warm fire and red cloaks on the oxen.
- Measured by me over the shot: saturation 0.654 and luma 58.9. This matches the team's 0.655 / 58.9.
- It sits next to s22's moon blue.
- Note: the sky is a very flat saturated cobalt (25,80,175), a bit synthetic. The team's note says the sky is a flat colour.

## Regressions
- Hero mouth is at y 770 or above in the last frames, so within the y 840 limit.
- Flames are on the tail tips and behind the herd from g1645.
- Soldiers are black silhouettes with a yellow rim and arms thrown up. The shock reads by pose, but there is no facial detail.
- No face in y 880-950: the band holds only ground and pots at g1682.
- Ground is textured or dark navy.
- Frame diff on the take: median 6.03 and p90 13.64 with bilinear downscale (7.42 / 15.09 with area). This matches the team's 6.04 / 13.64.
