# QA_RECHECK s25 v2 (film 14, shot 25, g 1672-1770, 99 fr) -- round 2 -- VERDICT: FAIL

Method: all 99 frames decoded; every 3rd frame (33, g 1672..1768) viewed at full size (720x1280, cyan line = y 880) and as a phone sheet (180x320). Frame-diff and luminance measured.
Narration: "ทั้งฝูงหันหลังวิ่งหนี และจำเสียงหึ่งนี้ไปตลอด" ("the whole herd turns and runs off, and remembers this buzz forever").

## v1 items (shot 25)
1. Night elephants brighter than soil, no contact shadows: **NOT** (blocking).
   Elephant bodies are still pale lavender. Measured luma: elephant ~101-109 vs adjacent soil ~40-48 (g 1690/1717/1762), i.e. about 2x brighter; they still read as lit cut-outs. No dark contact ellipse is visible under any foot in any frame (feet end in grass/soil with no shadow). The "x0.5 card + tint" in QA.md is not visible in the output.
2. Trotting in place instead of fleeing: **PARTLY** (blocking).
   The herd now shrinks with depth (about 1.0 -> 0.5) and the camera holds, but the lead elephant stays pinned at the left edge (x 0-250) for the whole shot, and at g 1768 the herd plus calf are still fully in frame at mid size, faces toward camera, not specks; the field is not empty. Reads as "running on the spot toward the left edge".
3. Frontal-to-profile swap with no turn: **NOT** (blocking).
   g 1675-1684 is a cross-dissolve of a semi-transparent frontal card and a semi-transparent side card: see-through ghost elephants with double heads/ears overlapping (worst at g 1678-1681). No 3/4 pose and no rotation; the swap is now a dissolve and adds a new ghosting defect.
4. Dust too faint: **FIXED** as to strength (dust is large and clearly visible from g 1687 on) -- but see client rule below.

## Other checks
- Dust is NOT a stack of round white blobs (client rule): **FAIL** (blocking). The "droplet crowns" are piles of round white/cream balls at the feet (clear at g 1690, 1693, 1714, 1717, 1762) plus white spike rays; on the phone sheet they read as a white blob stack and white streaks, not soft dust.
- Heads above y 880: PASS (lowest head ~y 650).
- Pops / frozen frames: PASS (frame-diff 2.1-3.7 every frame, no spikes, no zero-diffs).
- Sky / ground share: PASS (sky ~42 %, ground ~58 % at g 1768).
- No steep down-view on the elephants: PASS (eye-level camera).

## Fixes needed for round 3
1. Darken/cool the elephant cards so mean luma <= the lit soil next to them; add a dark blurred contact ellipse under each foot pair, visible on the soil.
2. Key a real turn (3/4 pose, or squash/rotate the card) at full opacity -- no cross-fade of translucent cards.
3. Move the herd across/out of frame or deeper (to specks) so g 1760-1770 is a nearly empty field; elephants should face away/side, not toward camera.
4. Replace the white-ball crowns with soft, low-opacity warm-grey dust clouds (no round white blobs, no white spikes), kept at the current size.
