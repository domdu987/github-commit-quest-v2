VERDICT: FAIL. 1 blocker: (1) the trunk pose pops every 14 frames in shot 27 (g1854, 1868, 1882, 1896, 1910).

# QA_RECHECK s26 (film 14, shots 26-27, g1758-1919, 162 frames): TAKE gate

Take: scratchpad/takes/r21/film/v3/film14/s26/take.mkv (720x1280, 30 fps, h264; take.mkv.partaa+partab byte-identical to take.mkv).
meta.json: first_g 1758, n_frames 162, shot 26 starts g1764, shot 27 starts g1840 (cut), g1 1913, 6 handles each side, 8-frame dissolve in from shot 25 NOT baked. These match shot_plan.md rows 26-27 (58.81-61.34 s = g1764-1840, 61.34-63.79 s = g1840-1914).

Method: all 162 frames decoded to scratchpad/takes/qa_s26/all/ (f000 = g1758). Every 5th frame (6 fps) viewed on a phone sheet (180x320, cyan = y 880; qa_s26/phone_6fps.jpg). Full-size frames viewed at g1764, 1808, 1839, 1840, 1865, 1913. 4-frame strip of the stalk fall at g1840-1876 (stalks.jpg). Zoom and contrast-boosted ground crops for grade and contact shadows. Per-frame metrics in qa_s26/metrics.txt: luma, Laplacian variance, Laplacian std normalised by contrast, mean frame diff, and max 16x16 block diff above y 880. Camera and card angles taken from shot.py CAM27/EAT and checked against the frames.

## Blocker

1. **The trunk pose pops in shot 27.** `shot27()` picks `trunk = 'reach' if (k//14 + len(cast)) % 2 == 0 else 'sniff'`, a hard switch with no tween. Every 14 frames (g1854, 1868, 1882, 1896, 1910) the tusked middle elephant's trunk jumps in one frame between "down to the calf" and "raised diagonally across the face of the elephant behind it, up to that elephant's eye". At phone size it reads as a flicker every 0.47 s. The block diff bumps at those frames too (38-41 against about 28-30 around them). The matriarch, elephant_b/c/d all have len 10 or 9, so most of the herd toggles on the same frames.
   **Fix:** replace the switch with a tween. Either lerp_pose the trunk between 'reach' and 'sniff' over 6-8 frames, with a per-elephant phase offset (e.g. `k + 5*EAT index`) so they do not all move together, or hold one trunk pose per elephant for the whole shot ('reach', grazing down). Do not let the raised 'sniff' trunk cross the face of the elephant behind it. For the tusked elephant, use 'reach' only, or swap its depth with its neighbour. Re-render shot 27 only (g1840-1919). Shot 26 can stay as it is.

## Checklist

| # | check | result |
|---|---|---|
| 1 | Story read at phone size | PASS. Shot 26: warm dawn, the full green maize field intact behind the rope fence and tin-roof hives, and the farmer in front of a hive with bees, hands on hips and smug (farmer_proud). The camera pushes and cranes down from a wide to a medium-full. Shot 27: a blue night with the moon, the herd behind tall maize. The stalks are down by about g1858 and the elephants graze, mouths chomping. The beat reads. Note: shot 27 is not recognisably the UNCLE's field, because the cans are hidden in setup and his fence and house are not in frame, so it relies on the narration ("but that night"). |
| 2 | Heads above y 880 | PASS. Farmer head y about 600 (g1764) to 690 (g1839). Elephant heads y about 450-570, calf head about 680. The farmer's feet reach y about 1010 by g1839 (legs under the caption, which is fine). |
| 3 | Contact shadows / no floating | PASS. A dark night contact ellipse is under each card (c14 `_contact`, 7.4x3.4 m x scale, offset along the key). Under the calf and the front elephant it shows in the boosted crops as a dark blue-black pool. Most feet are in the fallen leaves, and no foot reads as floating. |
| 4 | No pops; cut at g1840 clean | **FAIL**, see blocker 1. Otherwise: one clean hard cut at g1840 (diff 70, no flash or duplicate frame either side), no luma jumps, and shot-26 frame diffs rise and fall smoothly (4.6 to 8.3). |
| 5 | Camera always moves (no static run over 6 frames) | PASS. The only near-static frames are g1758-1760 (diff 0.37 and 0.02; cam26 starts at g1760), a 3-frame run inside the handle and the conform dissolve. Shot 27's camera trucks left 2 m over g1840-1918, with diffs of 2.9 or more on every frame. |
| 6 | No text | PASS |
| 7 | Dust is a spray crown, not round blobs | N/A: there is no dust in shots 26-27 (no dust cards in shot26/shot27). There are no white blobs anywhere. |
| 8 | Stalks visibly fall in shot 27 | PASS. Tall maize hides the herd at g1840. The stalks fall outward from the herd over g1840-1858 (most) and finish by g1894, leaving leafy stumps. It is clear at phone size. |
| 9 | Elephants unhurt | PASS. They are calm and content, chewing, with no injury marks. (The raised trunk touching the other elephant's eye is covered under blocker 1.) |

## Earlier s25 / s25v2 issues re-checked (shots 26-27)
- **The night tint did not take effect on the elephants:** FIXED. The sprite grade `_night_grade` (x0.52, tint 0.78/0.82/1.0) is applied for NIGHT. The elephants are dark slate grey with a blue bias, and nothing like the earlier pale cards: body luma about 50-54 against the earlier 101-109, and B is higher than R. They are still about 1.3x the nearby soil (soil luma 32-41), so they are not quite at the s25v2 numeric target of "≤ the lit soil", but they read as night-graded and not as bright daytime cards. Optional: x0.45 instead of x0.52.
- **Cross-fade turns:** none in this take. No translucent or ghost cards; every elephant is a single opaque profile card walking left.
- **Dust as round blobs:** N/A (no dust in shots 26-27).
- s25_QA_ART nice-to-haves: the shot-26 hold on the proud farmer is now better (he is readable from g1764 and medium by about g1820). The hard pale-green ground patch is gone (the ground mask now uses a softer blur). The salmon rings in the shot-27 midground are the set's mud and foot rings at y about 640-700. They read as trampled ground and are fine.

## Elephant camera rule (at most 2.5 m high, card within about 25° of facing)
- Height: CAM27 is 2.40 to 2.45 m with a look-at height of 1.55 m. The down angle to the card centres is about 5-7°. PASS. There is no steep down-view.
- Yaw (cards are yaw_fixed=0): matriarch 2-10°, elephant_c 25° at g1840 then 9-18°, elephant_d 4-15°, calf 2-17°, all PASS. **elephant_b goes over the limit: 27° at g1866, 30° at g1893, 34° at g1913.** It is mostly outside the 20 mm frame (half-FOV about 27°), and only its head and ear show at the left edge, where it does not read as flat. Non-blocking. While re-rendering for blocker 1, start elephant_b about 1.5 m further right (x0 -34.1) or give it `yaw_fixed` = atan2 toward the camera, clamped to 20°.

## Sharpness (team 3's "blur" flag on shot 27)
**Confirmed false positive.** The raw Laplacian variance is 205-270 in shot 26 against 66-105 in shot 27 because shot 27 is half as bright (mean luma 67 against 133-139), and the auto check is relative to the take median. Normalised by local contrast (Laplacian std / luma std, above y 880), shot 26 is 0.196-0.268 and shot 27 is 0.180-0.229: the same range. Within shot 27 it drops from 0.229 to about 0.185 over g1840-1858, as the fine-detailed maize falls, and then holds steady. There is no progressive softening. At full size, the outlines, eyes, tusks and leaf edges are crisp; there is no DOF and no motion smear.

## Non-blocking notes
- The foreground grass in shot 27 (y 950-1280) has a warm golden light pool that looks like daylight or a lantern in a night shot. It is mostly under the caption band. Cool it, or drop that fill, if re-rendering.
- Elephant mouths snap open and closed every 5 frames (munching). This is acceptable as limited animation; it is not a talk mouth.
- Take-folder hygiene: QA_AUTO.md is the result for s27only.mkv, not for the delivered take.mkv. contact.jpg and phone_sheet.jpg are the same file. QA.md says no 6 fps eyeball was done, which is how blocker 1 got through. Next time, run qa_auto on take.mkv with `--cuts 1840` and keep the note.

Artifacts: scratchpad/takes/qa_s26/ (all/, metrics.txt, phone_6fps.jpg, full_a.jpg, full_b.jpg, stalks.jpg, trunk_toggle.png, trunk_toggle2.png, ground_boost.png, zoom_f107.png, zoom_f155.png).
