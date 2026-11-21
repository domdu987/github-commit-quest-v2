# FINAL QA-art: film 21 "ไอ้ชาวนาบนเนิน" (FINAL gate D3)

Reviewer: QA-art (opus). Inputs: final_2fps.jpg, final_1fps_phone.jpg, full-res frames film21_final_frames/f_0000-f_1847
(graded, no captions), farmers_v1.mp4 (11 caption frames pulled with ffmpeg), narration_timed.txt, final_qa/QA_AUTO.md.
Rule applied: block only for hard defects (visible jump/splice, floating object, broken/black/blank frame, wrong character,
real camera shake). Everything else is a scored note.

## Verdict: SHIP

No hard defects found.

## Scores (1-10)

| Area | Score | Comment |
|---|---|---|
| Set density | 8 | A dense, warm 3D world: hill with forest, looping river, the bridge, tents and parasols in the English camp, the treasury booth with lanterns and coin stacks, grass tufts everywhere. The lower foreground of the false-payoff ground (35-38 s) is the barest set. |
| Lighting & colour | 7 | Warm sun, long contact shadows, teal water against ochre sand and red coats, as COLOUR_SPEC v1.1 asks. Some passages fall off: the tree-dive at 3.4-3.9 s is dark, 6-8 s reads dusky blue-grey, and the bridge at 51-53 s sits on near-navy water. The exteriors outside the band are documented. |
| Composition / phone legibility | 7 | Wides show the set, and medium shots carry the faces. On the phone sheet the bridge mechanism at 46-48 s (aerial) and the mass crossing at 30-34 s are tiny figures. Captions (white with a black outline, around y 900) are crisp, render the Thai correctly, and sit below the heads in every sampled frame. |
| Character acting | 8 | Cressingham's smug laugh, the tears of laughter (21 s), the finger-point (22-25 s) and the snooty close-up (25.6-26.5 s) read at once. The arms-akimbo mocking line at 35-38 s and the goggle-eyed panic at 50.5 s are clear. The swimmers at 60.5-61.3 s are comic and bloodless. |
| Hook (0-5 s) | 7 | A beautiful aerial of the river loop, the bridge and the hill, then a fly-down to the Scots standing still on the hill (4.3-5 s). The idea of soldiers who do nothing reads. The dive at 3.4-4.0 s is very fast (frame diffs of 54-82 every frame), so the trees strobe. |
| Mocker (18-26 s) | 9 | The best passage: the KING'S TREASURY booth, the laugh at the counter, then the point toward the hill with the bridge behind him. The character and his gag read even at phone size. |
| False payoff (35-38 s) | 8 | The English line laughing with their hands on their hips, pushing in on Cressingham. The joke is clear. |
| Reveal (41-50 s) | 7 | The horn on the hill (41 s), the charge down the slope in sun shafts (42-43 s), the pike line holding the bridgehead (44-45 s) and the aerial of the trapped half-army (46-48 s) are all there and in the lit world. The bridgehead block itself is small on phone. The 39.1 s whip through the sun flare washes out for about 4 frames. |
| Ending (55-61.6 s) | 8 | The empty treasury booth ("fast, cheap") is a good visual punchline. The splash-in and swimming helmets give a clean comic last image. The 57-59.5 s shore shot is static in its acting. |
| Overall | 8 | Matches the client's taste: a dense, warm, sharp world, wide and medium framings, few text signs, and the reveal inside the 3D world. |

## Hard defects (blocking)

None.

Checked and cleared:
- **g642 (21.4 s):** a one-frame view with no hill and no character. It is the landing frame of the whip pan into the mocker shot. The chest moves about 40 % of the frame width per frame, and the hill and Cressingham enter from the right on g643. This is continuous motion, not a splice.
- **g117-121 (3.9-4.0 s):** a frame-diff spike as the camera dives between trees. The diffs stay high on every frame (54-82), and there is no object pop.
- **g1173-1176 (39.1 s):** a whip through a sun flare. This is an intentional transition, not a broken frame.
- **Frame scan:** no black or blank frames (minimum mean luma 43), and 0 % magenta. The cuts at 1519, 1640 and 1709 are planned cuts.
- **Character consistency:** costumes and characters are consistent shot to shot. Nothing is floating: contact shadows are present throughout.

## Most visible non-blocking notes

1. **3.4-4.0 s, hook dive.** The fly-down through the trees is too fast and dark, so it strobes for about 15 frames. Slowing the dive or lifting its exposure would make the hook land cleaner.
2. **35.0-37.6 s, false payoff.** A dark cropped object (a banner or flag edge) intrudes at the top-right frame edge. Reframe the shot or remove the object.
3. **44-48 s, reveal mechanism.** On phone, the bridgehead being shut is read mainly from a high aerial where the figures are specks. A closer beat on the pike line across the bridge mouth would make the mechanism unmistakable.
4. **6-8 s and 51-53 s, colour.** These run cool and dark (a dusky valley, and the bridge on navy water) next to the warm rest of the film. This is documented as outside the band, but it is the weakest colour in the cut.
5. **57-59.5 s, ending.** The shore shot holds near-still characters for about 2.5 s before the splash. A small push-in or a reaction would keep the ending moving.
