# s26 QA: film 11 shot 26 (ending, the queue; garden_queue / A), g 1630..1718 + handles 1624..1629, 1719..1724 (101 frames)
- 12 samples, 720x1280, 2 threads, 9.5 s wall / frame. QA_AUTO PASS (cut notes = cuts to neighbouring takes).
- Queue of 6 behind the picket fence from the gate (right) to the hut (left): villager_a (pockmarked), d, b (pockmarked), e, c (pockmarked), milkmaid2; James (blister sore card on upper_arm_l) and Jenner (lancet up) at the hut door (small, at the left). Nobody has horns. Idle sway / blinks / glances. Slow drift of the camera. Heads y <= 635.
- Deviations: queue heads are 50-60 px (wide framing to show the whole queue; the plan's "closer" is shot 27); "sleeves rolled" is not expressible on the villager puppets (no sleeve key), so not shown; hens and a basket in the foreground are set dressing.
- Re-rendered 2026-11-18 after the director note: chimney smoke hidden (hide_render in c11.py).

## Gate 2 re-render (QA-art: "chickens on a lane")
- Re-staged: 9 queue figures (a, d, b, e, c pockmarked / plain mixed, milkmaid2, a / d / b repeated, mirrored) from the hut door to the right, staggered in depth (y -3.0 / -4.1) so the heads do not pile up, running out of the frame at the right edge; heads 63-90 px at the front. James (blister card) and Jenner (lancet up) at the hut end (left, small). Camera on the lane side, 2.6 m high, slow drift; the lower band is now plain lane with only one hen at the fence. Nobody has horns. 10.4 s / frame, QA_AUTO PASS.
- Deviation: not a true diagonal (the garden has no clear oblique view: the hay wain on the green, the kitchen wing and the hut wall blocked every oblique camera I tried); the staggered line leaving the frame is the "long queue" read. "Sleeves rolled" still not expressible on the villager puppets.
