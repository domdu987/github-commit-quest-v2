# FINAL QA-art R2: film 17 "ไอ้ช่างวัดหู" (final2/ear_v1.mp4, 68.4 s, 720x1280, 2052 frames)

This review follows up the R1 report, film/film17/gate/FINAL_QA_ART.md, which gave FIX-FIRST on shot 33.

What I looked at:
- ear_v1_frames g1990-2051, every frame, at full res and at 1:1 crops of the jaw and ear
- end.png, the phone strip
- burned-in frames from ear_v1.mp4 over the last 10 s
- a frame-by-frame PSNR of final/ear_v1_silent.mp4 (R1) against final2/ear_v1_silent.mp4 (R2), plus 6 spot frames shown side by side with a diff

My working sheets are in final2/qa2/: end_sheet.jpg, hand_crops.png, jaw_seq.png, mid.jpg, cap_sheet.jpg, spot.jpg and psnr.log.

## Verdict: SHIP

The R1 blocker is fixed. Nothing new blocks delivery.

## R1 blocker: shot 33 ending punch (g2014-2051). FIXED
- **Hand:** Bertillon's hand is now the white cartoon glove, the same rig as in the hook and in shot 32. It grips the caliper beam in every frame. The black bars are gone: dark pixels make up 0.1-0.6% of each frame, with no blobs.
- **Action:**
  - g2014-2026: Bertillon is in frame. His glove holds the calipers level, with the sliding jaw at the edge of the red ear.
  - g2027: the calipers snap across the ear, with the near jaw at the front edge of the ear and the far jaw on the other side.
  - g2027-2051: the clamp holds while the camera pushes in on the inspector's sweating red face.
  - The caliper_click SFX at 67.5 s (g2025) lands within 2 frames of the snap, so the clamp reads as "click, shut".
- **Phone size (end.png and 270x480 sheets):** the callback reads at a glance. You see Bertillon, his glove, the calipers and the inspector's own ear, then a tight hold on the red face with a sweat drop and the calipers clamped on the ear. The comic payoff lands.
- **Full res:** clean line work. No warping of the face or moustache, and no flicker in the hold.

## Other checks
- **Cut at g2014:** clean hard cut. There is one diff spike at g2014 (55.7). g2013 and g2015 are normal (4.4 and 5.7). No blend frame, no flash, no black frame.
- **Film end:** the video has exactly 2052 frames and the audio runs 68.4 s. g2051 is a full shot 33 picture: no fade, no black, no repeated frames. The film ends on the hard cut.
- **Caption band, last 10 s (pos 360,900, band about y 855-945):**
  - The words sit on chests and torsos (the inspector's tunic, Bertillon's coat, the records hall in the payoff).
  - The caliper and ear action is at y 560-720 and the faces are above it, so nothing important is covered.
  - The last caption, "วัดหูตัวเอง", ends at 68.04 s, so the final 0.36 s is clean picture.
- **Nothing else changed:**
  - Before g2014, the R1 and R2 conforms differ only in short runs of frames at word boundaries.
  - In the side-by-side spot frames (g90, 960, 1435, 1890) and the diff maps (g90, 517, 960, 1435, 1755, 1890), the only real change is the caption word in the band. That is the retime. Everything else is codec noise at about 1-2 mean levels, and g1755 differs by zero pixels.
  - The picture is the same as the R1 review.

## Notes (non-blocking)
1. **g2026→2027 depth pop.** Before g2027 the far end of the caliper beam is hidden behind the ear and head. At g2027 it appears in front, with the second jaw on the far side, in a single frame; the jaws are not seen sliding shut. It sits on the click SFX and reads as a comic snap-shut, so I accept it. If s13 is ever re-rendered, a 3-4 frame slide of the jaw would be smoother.
2. **Bertillon leaves frame.** The push takes his head out of frame by about g2036. From about g2040 only his glove and the calipers remain, cut by the left edge of the frame. It still reads, because the grip is established in g2014-2035.
3. R1 non-blocking notes 2-7 are unchanged and still ship-acceptable: the lamp clip in shot 13, the three fingers in shot 14, the foot-board insert, the small wagon at dusk, the beard gag, and the 4 streak frames at the hook snap.

## Scores (updated)
| area | score |
|---|---|
| Set density / ornament | 8 |
| Light / colour | 8 |
| Composition / phone legibility | 7 |
| Acting | 7 |
| Key moments: hook 8, reveal 7, ending 8 | 7.7 |
| Overall | 8 |
