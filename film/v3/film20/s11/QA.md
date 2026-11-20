# s11 QA: film 20, shot 11 (nickname) -- SITE site_fence, DAY, stage 0
## Delivered
- take.mkv: g 745..825, 81 frames (8 in-handle for dissolve 11 into this shot, g 753..821 = shot 11, 4 out-handle after the hard cut at g 822), first_g 745, 27.6 MB (not split). 720x1280, 8 spp.
- s/frame: wall 14.4 (two processes, shared CPU), cpu 23.3.
- Frame-diff in-shot (90x160 grey, g 753..821, handles excluded): **median 5.60, p90 10.88** (target 4 / 12): median met, **p90 misses by 1.1** (the punch-in cut + 6 speed-line frames carry the top of the range).
- qa_auto: PASS (notes only: the planned cut g 802 and g 822 show no change within +-2 frames because the punch-in is inside the take and the out cut is the handle edge).
## What is on screen
- g 745-801: eye-level, outside the open timber fence; lady (parasol, hand at mouth), gent (pointing, cane) and child (pointing) laugh (3 Hz squash + 0.08 D bounce, head roll); Eiffel at the gate edge holds the giant rivet up. Camera pulls back 10 %/s with slide + crane + hand-held jitter; snap push x1.4 g 776-792 on "เรียกไอเฟลว่า". Foreground: barrels (set scatter), two red-lead girders, a camera-side timber post.
- g 802 (the nickname, event g 802): PUNCH-IN CUT onto Eiffel + rivet (about 35 % of frame height), 2-frame vertical shake (g 802-803), 6 frames of speed lines (g 802-807, drawn in deliver.py, no text), then push 12 %/s.
## Checked
- Heads: Parisians 50-90 px, Eiffel ~35-45 px in A and 120 px in B; all head centres y 560-760 in A, bottoms < 880 (probe). Feet on the ground (C.on_ground); contact decals on.
- Mouths: none animated (laughing20 drawn mouth only). No DOF, no text. Tower leg (stage 0) in every frame.
## Deviations / known issues
- Eiffel is small in framing A (35-45 px head) and the barrels (set scatter) hide him for part of g 785-801; the punch-in is what reads him. Preset FG mesh (post + high rail) hidden because it is anchored to the preset camera.
- p90 frame-diff 10.88 < 12.
- Hand-held jitter (+-0.09 D) was added for frame-diff.
