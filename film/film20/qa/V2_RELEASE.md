# Film 20 rivet_v2: release notes (2026-11-22)

File: film/release20/rivet_v2.mp4 (68.2 s, 720x1280, 91.6 MB, -12.6 LUFS, true peak -1.2 dBTP). The caption (release20/caption.txt) is unchanged from v1.
Narration, music and SFX are identical to v1 (no fal calls). The v1.1 grade (COLOUR_SPEC §5) is applied.
The client decided "กลับไปใช้สกิลแบบเดิมเลยถ้ามันยากนัก": no further fix rounds, so v2 ships with the takes already delivered and accepted.

## Re-rendered takes (client fix list)
- T03 (b851e5e): Eiffel on the ground, canopy legs, floating girders/crates/posts/rod/shovel/gravel disc removed, one riveter pair on a deck, smooth crane.
- T09 (612d960): the tower outside the window is under construction and stands on foundations; the shot ends at a medium.
- T11 (bcc7a79): ghost post removed, wider framing, grounded, carried beam and bucket removed, smooth camera; the camera-parented post was also deleted from the code (§M).
- T18 tail (d5a6bfb): smooth window dive.
- T21 (2bb3d2a): sway removed, no stray lines, glow band or sky edge, visible contact shadows, pickaxes kept in hand.
- T23 (bab87be): giant head removed, no hand-held certificate, hat kept on.

## qa_jitter on the full film (film/qa_jitter.py)
```
 11s shake   2.8px
 12s shake   3.0px
overall median jitter px 0.44
```
v1 read: 10 s 3.9, 12 s 3.1, 27-31 s 2.0-2.5, 46 s 2.1, 48 s 3.0, 52-54 s 3.3-3.6 (median 0.64).
OPEN: 11-12 s (the T03 crane up the tower leg) reads 2.8 / 3.0 px. The camera path is smooth (background track monotonic). The reading comes from near-lattice parallax during a fast crane. A slower re-plan was stopped by the client's decision.

## Known notes, not fixed (final reviewer, V2_FINAL_REVIEW.md; §M audit, V2_SECTION_M.md)
- 15-19 s (T06, café): heads cut at the top edge; a quill hovering over the petition (~16 s); a thin green rod by the window (~18-19 s).
- 33-36.5 s (T15): a foreground head card glued to the camera (bottom-left); the official slides back about 2.4 m without walking (34.3-35.4 s).
- 36 s / 40 s (T15/T16): faces about 50 % of the frame width; a grey slab at the left edge (37-38 s); weak contact shadows on the checkered floor (37-40 s).
- 54.3-55.4 s (T21): the parked wagon (horses, tools) slides behind the group.
- 63 s / 65 s (s26/s27): diner's face about 45 % of the width; a dark over-the-shoulder head fills about 60 %.
