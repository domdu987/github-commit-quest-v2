# s27 QA: film 11 shot 27 (towndoc in the queue; garden_queue / A, closer), g 1719..1805 + handles 1713..1718, 1806..1811 (99 frames)
- 12 samples, 720x1280, 2 threads, 12.0 s wall / frame. QA_AUTO PASS (cut notes = cuts to neighbouring takes).
- Towndoc hat off (hat_off), sleeve_sheepish: blush, sweat rising, right hand tugs at the left cuff (g 1740-1780), mouth still (not in a quote window). Jenner waits at the hut with the lancet up (small, left), James (blister card) beside him; villagers c / a / e queue behind the towndoc (c, pockmarked, cut by the right edge). Camera inside the garden (the fence posts blocked it from the lane), slow push 3.7 D.
- Heads on screen y <= 660 (the 9000 values in raw/*.json are off-screen queue cards); towndoc head 83-130 px.
- Deviation: the towndoc stands at x -3 (near the head of the queue), not at the tail (x 6.6), to be in one frame with Jenner; the camera is in the garden, not the preset's lane-side camera.
- Re-rendered 2026-11-18 after the director note: chimney smoke hidden (hide_render in c11.py).

## Gate 2 re-render (QA-art: villager c stole the shot, sleeve roll)
- Pockmarked villager c (with e and a) now stands behind (farther than) the towndoc on the hut side, hidden by his body: the towndoc is the biggest, unblocked figure (head 107-167 px). James (blister card, by the hut stool) and Jenner (lancet up) beside the hut.
- Sleeve roll: from g 1745 to 1775 a cream turned-back cuff (climbing from wrist to mid-forearm) and a bare skin forearm are drawn on his left arm as a sprite overlay built from the elbow_l / hand_l anchors; held to the end of the take. His right hand still tugs at it. The hat is not in his hand (no prop for it), hat_off stays.
- 11.2 s / frame, QA_AUTO PASS. Heads on screen y <= 645.
