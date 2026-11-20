# T8 QA (g1862-2052, 191 frames)

Checks: `check_take('T8')` hits [], `check_face('T8')` ok. `qa_auto.py --cuts 1868 --first_g 1862`: PASS (notes: no visible change at g1868 because the cut comes from T7 into this shot; magenta share 0.0 %). `rhythm.py`: 191 frames, in-shot median motion 10.44, p90 20.84.
Luma (RGB mean of 90x160 bilinear): part mean 99.5, min 90.8, max 110.1; target 95-110. g1862-1870 sit at about 91-92, the g2036-2050 end about 96. Lights were not changed.
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
