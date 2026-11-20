# s11 QA: film 20, shot 11 (nickname) -- SITE site_fence, DAY, stage 0  (re-render after TAKE gate A)
## Delivered
- take.mkv g 745..825, 81 frames (8 in-handle for dissolve 11 into this shot, g 753..821 = shot 11, 4 out-handle after the hard cut at g 822), first_g 745, 24.0 MB, 720x1280, 8 spp. s/frame wall 10.5 (two processes), cpu 19.3.
- Frame-diff in-shot: deliver.py median 3.89 p90 8.06; **qa_stats `saturation 0.574, brightness 102.7, in-shot motion median 4.45 p90 9.23`**. Colour met (sat >= 0.47, luma 85-110). Motion: median met by qa_stats (just under by my own 90x160 method), **p90 misses 12**.
- qa_auto PASS (notes: planned cuts g 802 / g 822 show no change within +-2: punch-in is inside the take, g 822 is the handle edge).
## Changes after the TAKE gate (TAKE_A.md s11)
1. Heads now 65-85 px (camera 5.4 m from the group, pitched up 6.5 deg so the ground is about 25 % and the heads sit at y 560-740).
2. The preset's near scatter props (pn_* meshes: the barrels) are hidden at runtime: nothing hides the lady / child / gent any more; foreground = two red-lead girders bottom-right + a timber post at the left edge.
3. Eiffel is in frame A (right of the child, ~45-55 px head, rivet raised) so the pointing / laughing beat reads.
4. Laugh bounce 0.10 D at 3 Hz + squash + head roll on all three.
5. The rivet is drawn dome-up on a raised arm (prop scale 1.8, angle 90) and reads as a giant rivet.
6. Speed lines thinner, with a clear area (r >= 300 px) round the face; punch-in cut g 802, 2-frame shake g 802-803, lines g 802-807. B: push 16 %/s + slide + jitter, Eiffel sways and the rivet bobs.
## Checked
Heads above y 880, nobody half-cut in A (lady touches the left edge only through the camera post for a few frames); feet on the ground (on_ground) with contact decals; mouths not animated; no DOF, no text; tower leg in every frame.
## Deviations
Eiffel is still small in framing A (~50 px, the plan wants him to hold the rivet up beyond the crowd). p90 below 12. Hand-held jitter (+-0.09 D) is part of the motion.
