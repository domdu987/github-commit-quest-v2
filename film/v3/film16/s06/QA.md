# s06 QA: film 16, shot 6 (STUDIO studio_door, DAY: the letter, the palette), re-render after the TAKE gate
- Frames g 305..409 (105): shot g 314..400 (10.45-13.37 s), 9 handle frames each side, hard cuts both sides. take.mkv 40.9 MB (libx264rgb crf 6), 720x1280, 6 spp, 2 threads: 11.4 s wall / 22.1 s CPU per frame.
- Frame-diff in-shot: median 4.90, p90 19.27 (target 4 / 12). qa_auto PASS.
- Fixes for the gate's blocking notes:
  1. Mouth: the shocked frames keep the wide eyes but the mouth is "flat" (closed); the sinking and seated frames use the "sad" face (closed). No open "O" mouth anywhere; mouths still in the whole shot.
  2. Sweat drop removed (no fx).
  3. Sit: Morse no longer walks to the set's stool. He stands where he will sit (M0 = seat position, set stool stays 1.7 D behind him). g 381-387 the pose tweens (hands drop, knees bend) from palette_drop to the stool pose; the stool card + seated pose appear on the CLOSED frame of a blink (g 387-389, swap at g 388), so there is no 80 px head pop; the seated card is mirrored so he faces screen-left toward the wife's portrait on the side table. Legs use crouch 0.36 / spread -0.12 (less splayed). The FG canvas stack covers the lower edge in the last second.
  4. Reacting face: snap push x1.5 (g 373..386) takes his head to 262-279 px (>= 250).
- Beats: g 314-333 messenger holds out the letter; g 333-335 blink, the letter changes hands; g 376 "เมียก็ตายไป" snap + palette tips; g 381-387 palette falls to the floor with one bounce (no injury); g 388 sits.
- Notes / still open:
  * The seated drawing is the cast's own stool pose: the stool seat is hidden behind the coat and the bent legs still show as dark arcs at the very bottom of the frame (y > 1000 at g 389-409); they are partly hidden by the FG canvases.
  * The wife's portrait sits left-background; his look at it is by the mirrored pose and gaze, small in frame. Messenger's legs end in stubs (cast card), partly hidden.
- Heads 148-279 px, centre y 487-718, bottom <= 858 (< 880). DOF off, no text.
