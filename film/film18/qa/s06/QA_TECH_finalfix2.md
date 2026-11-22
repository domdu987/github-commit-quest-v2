# QA-tech FINAL-fix s06: PASS

Checked: take.mkv (72 frames, g459-530), all frames extracted. 6 fps montage of the whole take, a 3-frame step montage for g495-530 with y 860/880/950 guide lines, 1:1 crops of the lower-left at g500/515/523/527/530, and a skin-mask scan of every frame.

1. Tian Dan fully in frame g495-530: PASS. Cap, body and feet are inside the frame on every checked frame (x about 360-520 of 720). Nothing stands in front of him. No edge clipping.
2. Carrier child chin at g500-530: PASS. The drifting carriers are gone. One child (with a basket) and a woman in a blue robe stand behind the lead oxen, locked left of Tian Dan. The child's chin measures y 758-785 on g500-530 (lowest skin row 753-785 over the whole take). That is far above y 860 (last round 867-887). The woman is behind oxen, not cut by an edge.
3. Other characters: PASS. No half-cut character. Only ox bodies are clipped by the side edges, which is allowed. No face in y 880-950. The skin-mask scan shows a lowest face pixel of y 794 on any frame. No pole through a face. Oxen are plain (no blades, no coats).
4. Frame-diff (area 90x160, in-shot g459-530, n=71): median 5.70, p90 8.38, min 1.89, max 10.70. This matches the claim. p90 is below 9, so I checked the move: there is a visible eased move. The camera dollies in and tilts, the lead ox slides across the right, and the oxen crowd grows. The tilt lowers the horizon. A punch-in at about g497-502 shows as diff 10, then holds. No pulsing.

Notes (non-blocking):
- Ox muzzle and head sit at about y 700-850 at the end, above the caption band.
- The woman behind the child is mostly hidden by oxen. The child and woman remain fixed to the camera, so they do not shrink with depth, but nothing glitches.
- Colour: dusk palette is vivid, with an orange horizon and blue sky.
