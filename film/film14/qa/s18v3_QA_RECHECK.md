VERDICT: PASS (with notes). All 3 blockers from s18_QA_RECHECK are fixed. No new blockers. Two optional polish notes are listed below.

# QA_RECHECK film 14 take s18 v3 (shot 18 only, g1168-1225), QA-art + QA-tech

Source: scratchpad/r35/film/v3/film14/s18/take.mkv (70 frames, 720x1280, 30 fps, h264), first_g 1162, so n = g - 1162. Shot 18 is n 6-63.
Neighbours:
- s15 from bb8a187: the take.mkv.part* files joined give 179 frames, first_g 995, ending g1173.
- s19 from 5160df0: the joined parts give 154 frames, first_g 1220.

Both were extracted into new folders.
Working files are in scratchpad/qa_s18v3/:
- f/gNNNN.png: all frames
- n15/, n19/: neighbour frames (n15src/, n19src/ hold the archives)
- cut_neigh.jpg: s15 g1165/1167 | s18 g1168/1225 | s19 g1226/1228
- full_1168_1196_1225.jpg
- torch_hand.png, hand_cuff_x3.png
- uncle_mouth.jpg: every frame g1166-1231
- others_mouth.jpg: woman and old man, every 3rd frame
- phone6fps.jpg: every 5th frame at phone size, cyan line at y 880

## Blockers re-checked

1. **Night grade: FIXED.**
   | frame | mean luma | low band (y > 880) |
   |---|---|---|
   | s15 shot 17, g1165 / g1167 | 21.5 / 21.3 | 20.2 / 19.7 |
   | s18, g1168 / 1196 / 1225 | 65.6 / 66.0 / 68.0 | 53.6 / 52.9 / 54.4 |
   | s18 shot mean, g1168-1225 | 66.4 | about 53 |
   | s19, g1226 / 1228 | 74.0 / 74.0 | 35.5 / 35.4 |

   The team's claim of "about 66" is confirmed. The sky is now a violet night sky, the torches read as warm points, and the daylight look is gone. The shot sits between its neighbours: it is lower than s19 (74), and the jump from s17 (21) comes from the close, dark hive shot cutting to a wider torch-lit group. Both cuts read as the same night.
   - Note A (optional): the ground band is 53, against 35 in s19 and the earlier target of 30-40. At the 1225|1226 cut the soil drops from bright orange-red to a shadowed dark red. Setting `GROUND_K` about 0.45 to 0.3 would close that gap. It is not a blocker.
   - Note B (optional): the sky is flat violet with no stars. s19 shows stars and a moon. This is acceptable in a tighter, lower framing.

2. **Lip-sync: FIXED.** I recomputed the narration RMS envelope (10 ms windows, film time = narration time + 0.10):
   - "ตะโกน" fades out to -36 dB at narration time 39.17, which is g1178.1.
   - Silence (-52 to -58 dB) runs from 39.18 to 39.20.
   - "เห็นมั้ย" rises at 39.21-39.25, which is g1179.3-1180.5.
   - The quote ends at 40.78 (-33 dB), followed by digital silence from 40.79, which is g1226.4.

   On uncle_mouth.jpg, the mouth stays a flat smug line through g1177. At g1178 the eyes change to the wide excited look while the mouth stays flat. The first open shape is at g1179-1180, and the talk shapes follow the speech through g1225. The cut is at 1226. There are no O shapes during "ตะโกน" any more. This matches meta.json and cues.json (talk g1179-1227).

3. **Torches and hand: FIXED.**
   - There are 3 separate flames with 3 separate sticks. The uncle's flame is about 70 px from the old man's at g1168 and more than 100 px at g1196 and g1225. The V-shaped shared flame is gone.
   - The uncle's raised torch points up and out to the right, and its stick ends in his fist.
   - The fist now joins the blue cuff through a short dark wrist, about 25-30 px. Before, a 40 px gap showed background. At phone size it reads as attached (hand_cuff_x3.png).
   - Note C (minor): the wrist is a little long and thin compared with the old man's. A hand of about 1.05 would tighten it. It is not a blocker.

## Other checks
- **Heads above y 880: PASS.** Head tops are at about y 450-560 and chins at about y 640-700. Feet sit at about y 880-960, which is allowed.
- **Contact shadows: PASS.** There are soft dark shadows under the uncle on every frame and under the woman's feet. The old man's feet are partly hidden in grass tufts, with a faint shadow.
- **Torch held: PASS.** All three torches end in a fist. The old man's flame goes off the right edge of the frame from about g1213, as the camera pushes in. That is acceptable: the uncle's torch is the subject.
- **Pops: PASS.** Frame-to-frame mean abs diff is 1.99-2.48 on every frame g1163-1231, with no spikes and no black or truncated frames. The only snap is the planned smug-to-excited eye change at g1178.
- **Camera movement: PASS.** CAM18 push. The frame changes on every frame and the group grows about 1.15x from g1168 to g1225. The push continues through the handles.
- **Text: PASS.** None.
- **Other villagers' mouths: PASS.** The woman and the old man keep flat, closed mouths and neutral, half-lidded eyes on every frame checked (others_mouth.jpg).
- **Story at phone size: PASS.** The night village group reads clearly: the uncle is in the middle and largest, eyes wide and mouth shouting, his torch thrust up toward the right. The two villagers hold their own torches, with still faces. The lower 40% is empty ground, so the captions at y about 900 will not cover any faces.

## Summary for the team
Approve for the cut. If someone touches it again (optional):
- darken the ground (`GROUND_K` about 0.3) for a closer match with s19 at 1225|1226
- shorten the uncle's wrist slightly
