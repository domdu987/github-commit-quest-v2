# T8 QA (g1862-2052, 191 frames)

Checks: `check_take('T8')` hits [], `check_face('T8')` ok. `qa_auto.py --cuts 1868 --first_g 1862`: PASS (notes: no visible change at g1868 because the cut comes from T7 into this shot; magenta share 0.0 %). `rhythm.py`: 191 frames, in-shot median motion 10.44, p90 20.84.
Luma (RGB mean of 90x160 bilinear): part mean 100.0, min 90.8, max 110.1; target 95-110. g1862-1870 sit at about 91-92, the g2036-2050 end about 96. Lights were not changed.
Render: 16 samples + OIDN, 720x1280, no motion blur, no haze, no saturation boost.
Shimmer: I did not measure it numerically (the camera moves, so a frame difference on a wall mixes in motion). I only looked at the frames below and did not notice shimmer on the walls.

Frames viewed at full size, and the same six at 360x640 on one phone sheet. At phone size the red inspector, the white glove and the calipers stay readable in g2000 and g2030; in g1862 and g1958 the calipers are too small to read, and at g2052 the glove and calipers are a small shape at the left edge.

- g1862: bird's-eye of the room. Red-faced inspector in the chair at the centre, Bertillon beside it on the rug, the crowd around, gasolier pole at left. A flat navy band fills the top fifth of the frame (set cutaway above the room). It reads as a dark header, not as a prop.
- g1910: crane-down. Bertillon's face with glasses and goatee at the left-centre holds the calipers in a white glove hand, the inspector with clenched teeth and a sweat drop behind him. A gasolier arm and lamp pass in the foreground left, bright but they do not cover a face.
- g1958: over-the-shoulder arc. The gendarme's back (kepi, brown hair, nape, cape, epaulettes) fills the right: reads as hair and coat, not a flat slab. The camera on a tripod is at left and covers part of a crowd face. The red inspector is in the middle, small.
- g2000: Bertillon's white-gloved hand holds the calipers and the open jaws reach toward the inspector's red ear at the left of his head. The camera tripod crosses the left edge. The inspector's mouth is shut with clenched teeth.
- g2030 (key still): inspector in the chair, red face, sweat drop, red ears at both sides of the head. Bertillon at the left edge with the white-gloved hand holding the calipers at the inspector's left ear, jaws touching the ear. The top-hat man is partly cut by the left edge behind him.
- g2052 (last frame): close on the inspector's red face and ears. Of Bertillon only the white glove and the calipers are visible at the left edge, jaws closed, a small gap away from the ear. His head is out of the frame.

Known weaknesses (what I could not fix inside the rules):
- At g2052 the calipers sit beside the ear with a small gap, not on it, because the push-in moves the camera away from Bertillon.
- At g2052 Bertillon's head is out of the frame; the glove and calipers are in frame.
- The bird's-eye start has the empty navy band at the top.
- At g1958 the camera tripod hides part of one crowd face on the left.

## Fix pass (director fix list, frames g1862-1892 and g2009-2052 re-rendered)
- Opening: camera shift_y -0.14 eased to 0 over g1868-1892. The navy band above the room is gone at g1862 and g1868; a dark wall and door strip shows at the bottom edge instead.
- Punchline: Bertillon is full height again and stands slightly closer to the chair; g2052 (viewed at full size) shows the white glove at the left edge with the open calipers around the camera-side ear, tips at ear height. The calipers do not cross a face. The ear stays visible between the tips.
- Top-hat prefect walks off to screen-left over g2010-2030 (not seen on screen in the frames I viewed there).
- Bertillon's face leaves through the left edge between about g2036 and g2041 (6 frames, face partly cut on the edge during that time); from g2042 only the glove and calipers remain in frame.
- Luma after the fix: mean 100.0, min 90.8, max 110.1. qa_auto PASS, rhythm in-shot median 10.84.

## Fix pass 2 (director gate list 2)
Re-rendered g1877-1932 and g2040-2052 (69 frames); the rest is unchanged.
- g1876→1877 jump: the stock `_lookrot` flips its up-vector from +y to +z near a straight-down view, which snapped the roll. It is replaced by a smoothstep slerp between the two up-vectors (camera positions unchanged). Frame step at 1876→1877 is now 16.5 against 16.0 for the next step (90x160 mean abs diff), so no visible jump. The roll eases slowly over g1877-1915.
- Crane vs crowd: crowd2 (laughing gendarme) and gend_b (tilted card) walk off left slowly over g1866-1906 and return over g1922-1932. They never glide fast. Checked at g1914-1928: the crane path is clear. The crying gendarme at g1896-1906 is no longer cut by the rod.
- Ending: BDX3 holds the hand and sleeve in frame to g2052 (glove on the calipers at the ear).
- Luma, RGB mean 90x160: take mean 100.0, min 90.8, max 112.9 (target 95-110). A few frames at the extremes sit just outside the band; the mean is in.
- qa_auto: PASS (cut 1868 shows no change within ±2 frames, as before). rhythm.py: in-shot median 10.84, p90 16.76.
- Honest notes: Bertillon's head leaves the frame at g2036-2041 (accepted earlier). The returning crowd members touch the left edge at g1928-1932.

## Fix pass 3 (director: float hunter, client rule K)
Whole take re-rendered (191 frames) because the contact blobs apply to every frame.
- Top-down cards: for camera pitch steeper than 40-45 deg down (g1862 to about g1925), each card is yawed to the camera (blend from the face-key yaw over pitch 40-50 deg) and leaned back by 35 deg x smoothstep((pitch-45)/45), pivot at the feet (`render.py` `_basis_steep`). Before, the cards leaned 40 deg at a random yaw and read as people lying on the floor. Checked g1862, 1880, 1890, 1900, 1920, 1930: people stand and face the lens.
- Contact shadows: every card keeps its decal (alpha 0.5), now 1 mm above the floor; props: the room furniture is batched into one mesh per material, so each measure_* mesh is split into loose pieces, floor-touching pieces are merged by footprint, and one soft ellipse (alpha 0.5, 1 mm up) goes under each cluster: 79 blobs.
- g1920 dark blob: not a stray. It is the photographer's camera on its tripod with its dark focusing cloth (`measure_cloth`), a real prop of the room; kept.
- Ground check (`GROUND.md`, `ground.py` + `film/v3/tools/ground_check.py`, every 30 frames, 7 frames, 81 objects): 0 FAIL. Cards are measured by their feet point (the sprite alpha was unreadable for the checker, so its bbox fallback would be too lenient). Dust motes, the pendulum bob and stove smoke are tagged airborne; wall and ceiling mounted items are listed as MOUNTED. Honest note: the gendarme `gend_b` stands 19 cm inside a brass base (sunk, not floating).
- Numbers: luma (RGB mean 90x160) mean 99.9, min 90.5, max 112.7 (target 95-110); qa_jitter median 0.49 px; qa_auto PASS; rhythm in-shot median 10.60, p90 16.68.
- Honest notes: at g1894-1910 the walking-out gendarmes cross the left frame edge for about 12 frames (same staging the director accepted at f432f9a).
