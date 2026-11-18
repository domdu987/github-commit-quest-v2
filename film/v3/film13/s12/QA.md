# QA s12 (film 13, shots 12 + 13), self-check
- Frames g 720..917 (198; g0 726, g1 912; 6 in/out handles), 720x1280, 12 samples, ~13-16 s wall / ~30 s CPU per frame (two processes at once).
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg), 0 % magenta, no frozen/black/pop frames. It reports planned cuts 780 and 843 as "no visible change": false negative (both sides are mostly brick); I checked g 777-782 and 840-845 by eye: 780 is a clear new framing (left, lower, cornice and sky), 843 is a clear cut to the crowd.
- Shot 12: framing A (g 720-779) camera in the air in front of the facade, slow push/orbit; framing B (780-842) starts from the left/low, pushes in, then cranes down the facade (rich leaves the top of frame ~g 815) and arrives on Pullman (fists on hips, looking up) at the street. Rich mouth = talk_mouth on every frame (all inside Q1, 21.68-28.09 s +-0.15).
- Shot 13: crowd of ~32 cast13 townsfolk (bouncing on every frame, bigger shared jump at g 895 = nickname 29.73 s), Pullman strolling past with an iron jack on his shoulder; camera drifts. The two burlap sacks that cluttered the foreground were removed at runtime.
- Heads: all heads in frames are above y 880 (Pullman's lane head ~y 780-810; crowd chins < 870); the rich man is at the top of the frame.
- Checked at ~6 fps and every cut +-3 frames: contact shadows present, props in hands, eye-lines OK, no text.
- Deviations: the plan's "medium two-shot" of rich and Pullman is impossible in one frame (31 D apart vertically at readable head size), so shot 12 reveals Pullman at the end of a crane down instead; the rich man is out of frame for the last ~1 s of Q1 (audio continues). Rich stands in the window (no leaning pose exists).
- take.mkv is split in take.mkv.part* (cat them to rejoin).

## Open item (caption band)
- g 836-840 (5 frames, 0.17 s): Pullman's head slides in from below the frame edge during the last crane move and has its chin below y 880 until g 841 (head y 1190 -> 849 -> final 809 at g 842; shot 13 and the rest of the take keep heads < 880). A figure entering from the bottom edge must cross the band; fixing it needs a different crane end (tilt down instead of up). Flagged for QA-tech: either accept (entering frames) or ask me to re-render g 820-842 with a changed end camera.
