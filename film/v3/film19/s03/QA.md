# s03 QA: film 19, shot 3 (HALL hall_window, DAY) -- revision 3 (round-2 gate)
## Delivered
- take.mkv (99 frames, first_g 101): g 101-109 in-handle (CUT), g 110-190 = shot 3, g 191-199 out-handle (DIS 13). 720x1280, 8 spp. qa_auto PASS.
## Round-2 fixes
- Frame-diff in-shot: median 4.8, p90 13.96 (was 2.98 / 10.99): a lateral camera sway (1.3 D, 2.8 s period) plus push 12 %/s and slide 30 px/s give sustained parallax; the snap is x1.7 over 17 f (g 169-185) on "ทำไม่ได้" (g 177).
- Clipping: the snap shift (+0.95) keeps the right astronomer's wig inside the frame to g 199 and astro_b inside on the left (checked on the finals: both wigs inside on every frame).
- Round-1 items stay fixed (no black tripod wedge, astro_b at the eyepiece, contact shadows, astro19 off the chair).
## Notes
- Head width 100-212 px, head centre y 598-692, lowest head bottom 758.
- 15.35 s/frame wall, 30.11 s CPU.
- A thin dark brass arc (set material) passes the far left edge in g 131-176 (NOTE from the gate).
