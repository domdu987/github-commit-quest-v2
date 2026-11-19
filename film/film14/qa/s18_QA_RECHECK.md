VERDICT: FAIL. 3 blockers: (1) night grade, (2) lip-sync starts 5-6 frames early, (3) the uncle's torch merges with the old man's and his fist floats off the sleeve.

# QA_RECHECK film 14 take s18 r33 (shot 18 only, g1168-1225), TAKE gate, QA-art + QA-tech

Source: scratchpad/takes/r33/film/v3/film14/s18/take.mkv (151 frames, 720x1280, 30 fps; byte-identical to take.mkv.partaa), first_g 1162, so n = g - 1162 and shot 18 is n 6-63.
Shot 19 in this file was ignored because take s19 r18 replaces it. That take was used only as the outgoing neighbour.
Working files are in scratchpad/takes/qa_s18/:
- f/gNNNN.png: all frames
- phone6fps.jpg: every 5th frame at phone size, cyan line at y 880
- uncle_mouth.jpg: every frame g1166-1225, uncle's face
- others_mouth.jpg: woman and old man, every 2nd frame
- torch_*.png, hand1200.png: torch crops
- shadows.png: contact shadow crops
- cut_neigh.jpg: s15 g1165/1167 | s18 g1168/1225 | s19 r18 g1226/1228
- n15/, n19/: neighbour frames

## Blockers

1. **Night grade does not match the neighbours (FAIL).** Shot 18 is lit like late afternoon: bright orange soil, sunlit yellow corn and roof, and a flat lavender sky with no stars.
   | frame | mean luma | low band (y > 880) |
   |---|---|---|
   | s15 shot 17, g1167 | 22 | 22 |
   | s18 shot 18, g1168 / 1225 | 108 / 111 | 106 |
   | s19 r18, g1226 | 83 | 37 |

   The cut at 1168 jumps from deep night to day, and the cut at 1226 goes back to night.
   Cause: `setup_shot` applies the night darkening only to shot 17 (`scale_light bounce/lamp 0.3`, `exposure -0.7`, `darken_mats tinunder`). Shot 18 gets the plain `fs3` set light, and `c14._grade` tints only elephants.
   **Fix:** for shot 18, apply the shot 17 treatment as a starting point: bounce and lamp x0.3, exposure about -0.7 to -1.0, and darker soil. The torches should be the key light: keep or raise the `torch_light` strength so the faces stay readable as warm pools. Show the same starry sky and moon as s19 if the sky stays in frame.
   Targets: mean luma about 45-60, ground band about 30-40, faces lit warm by the torches. Check on a 1167|1168 and 1225|1226 strip.

2. **Lip-sync starts about 5-6 frames before the quote (FAIL).** The ffmpeg RMS envelope of narration.wav (10 ms windows) shows:
   - the narrator's word "ตะโกน" runs to narration time 39.17
   - true silence at 39.18-39.20 (31-38 dB)
   - "เห็นมั้ย" begins at about 39.21-39.24, which is film time 39.31-39.34, so g1179-1180
   - the quote ends at narration time 40.78 (silence 40.79-40.82), which is film time 40.88, so g1226.4

   The captions' 39.03 is the end of "ตะโกน", not the start of the quote.
   The uncle's mouth opens wide (O shapes) at g1174-1177, while the narrator is still saying "ตะโกน". His eyes also snap from smug to wide O at g1173 to g1174. Mouth movement from 1182 onward follows the speech, and the end is fine: small shapes through 1225, with the cut at 1226.
   **Fix:** in shot.py, set `G_LIP = (1179, 1227)` and keep the smug, flat mouth through g1178. Move the smug-to-excited expression switch to g1178 or g1179 so the eye change lands on the first syllable. Re-render only g1174-1179 (6 frames).

3. **Torch reading (FAIL, art).** At full size and on the phone sheet:
   - The uncle's torch head sits on top of the old man's torch head, so one flame has two sticks in a V, one from each man (g1168-1225, see torch_1170.png and torch_1200.png). It reads as one torch held by two men, not the uncle's torch held up.
   - The uncle's raised fist floats about 40 px beyond the end of his blue sleeve cuff (hand1200.png). His lowered hand sits right at its cuff.

   The torch does point out and up to the right, as stated.
   **Fix:**
   - Separate the flames by at least 60 px. Either move the old man's mark (for example x -1.25 to -0.9 and y 3.6 to 3.9) or lower his torch angle, or give him the torch in his other hand.
   - Shorten `arm_r.hand` (for example 1.25 to about 1.12) or reduce `bend` until the fist meets the cuff.
   - Re-check at g1168, 1196 and 1225.

## Other checks (pass)
- **Heads above y 880:** PASS. Head tops are at about y 450-600, eyes about y 520-560. Feet at about y 900-940 cross the band, which is allowed.
- **Contact shadows:** PASS. There are soft dark shadows under the uncle and the woman. The old man's feet are mostly hidden by grass tufts, so his shadow can hardly be seen (minor).
- **Pops:** PASS. Frame-to-frame mean abs diff is 3.5-4.5 for every frame g1163-1225, with no spikes, no black frames and no truncated frames. The only snap is the expression change at 1174 (covered by blocker 2).
- **Camera movement:** PASS. CAM18 pushes linearly from (-3.1, -1.9, 1.35) to (-2.9, -1.1, 1.4) over the shot, so the frame moves on every frame and the people grow about 1.15x. No static run.
- **Text:** PASS. None.
- **Others' mouths:** PASS. The woman and the old man keep a flat, closed mouth on every frame checked (`mouth flat`, `expr neutral`).
- **Story read at phone size:** PARTLY. Three villagers with torches and the uncle in the middle shouting read clearly. But the day look (blocker 1) loses "night", and the shared flame (blocker 3) blurs "his torch". No elephant is in frame, which is fine for this beat.
- **Note:** this take was rendered at 12 samples, while the brief says 24. Grain is acceptable at phone size.
