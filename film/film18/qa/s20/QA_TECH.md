# QA-tech round 17 s20: PASS
Checked: 6 fps sheet; 1:1 crops g1521/1545/1575/1595; flame-pixel bbox every 4th frame g1509-1601.

## Verified
- Lead head fully in frame. Face, eyes, mouth and both ears are inside the frame on all frames; only the tip of the left horn / ear reaches x 0 near g1575-1595 (0-5 px). Does not matter: nothing readable is lost. NOTE.
- Lead flame: a big, clearly readable red/yellow flame (about 120-130 px wide) on the tail pole, behind the ox. Only the tip touches the right edge (x 712-719) in about 10 of the first 40 frames (g1513, 1529-1533, 1545); the flame body and bright core are always inside (core x about 580-700). Judged: tip cut only, acceptable.
- No flame, pole or bundle on any head; the earlier horn/brow blocker is gone (one lead ox, tail pole is behind).
- Mouth lowest about y 870 at g1521, about y 840-850 later; below no face in y 880-950 (hooves reach y about 940 but they are not faces). Mouth still.
- Ground 0.187 max (director) passes. No pulsing, no placeholders, no pole through a face.
- Frame-diff median 5.94 (director 5.88 / 8.25 reads) passes >= 4; p90 8.41 is a guide only.

## Notes
- Contact shadow is weak: the warm light pool sits to the right of and behind the hooves, and there is no dark ellipse under the hooves. Hooves are dark and rest on the ground so it does not float. Strengthen at the FINAL pass if cheap.
- Sparse herd (one lead ox plus a distant one entering at the right g1520-1545), as the brief asked.
- g1509-1512 whip landing: wall frame, fine.
