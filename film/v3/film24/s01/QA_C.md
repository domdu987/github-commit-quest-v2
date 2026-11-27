# s01 QA, look C (shots 1 + 2, relight only, same shot.py, JOSEON_LOOK=C)
- Render: 24 samples at 540x960 + J.post (C grade) -> 720x1280, g 0-156 (157 frames, 6 out-handle), ~55 s/frame wall (shot 2 with the dragon smoke volume about 80 s). Shots rendered in separate processes (a second build in one process crashes in look C); hard cut at g 78.
- qa_auto: PASS with --cuts 78 (QA_AUTO_C.md). qa_jitter: overall median 0.06 px, no shake windows.
- Reviewed contact_C.jpg (every 6th frame): shot 1 has the low warm sun, Yi on the quay with a contact shadow, the hammerer kneeling and the carrier standing on the roof edge; shot 2 shows the sculpted dragon head with the smoke plume rising from g 85 on. No mouths move (no quote window).
- Note: a dark shape sits in the bottom-left corner of shot 1. It is a world-fixed shadow on the quay planks from the set's gobo/prop lighting, not a floating object. The director may want a look.
- meta_C.json: g0 0, g1 151, first_g 0 (unchanged, no shift).
