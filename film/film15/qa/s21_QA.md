# s21 TAKE-gate QA (film 15, shots 21-23, g1125-1268 + handles 1119-1124 / 1269-1274): KEY take (false payoff), QA-tech + QA-art

**Verdict: FAIL.** Both failed attempts and the coach's shout are there, and the automatic numbers pass. Two things clearly hurt the film on a phone:
- Shot 22: the punch image of attempt 2 (Dick lying on the foam) has his head inside the caption band, and his face is cut off by the right edge.
- Shot 23: the crowd cards beside the coach have purple stand blocks where their faces should be.

Take: origin/render15/team4 @ 9171031, film/v3/film15/s21. take.mkv was rebuilt from parts: 156 frames, 720x1280, 30 fps.
- meta.json lists shots **21-23** only (21 = g1125-1149, 22 = g1150-1189, 23 = g1190-1268).
- **Shot 24 is not in this take.** Team 4 renders it as a separate s24 take (s17/rerun24.sh, g1263-1334), and that take is not on the branch yet. The shot 24 checks are listed under "Pending" below.

Frames checked:
- 6 fps (every 5th g, g1119-1274) plus every cut ±3 (1122-1128, 1147-1153, 1187-1193, 1266-1272), at full size.
- A 360x640 phone sheet (one frame every 0.5 s).
- Mouth crops at g1190-1217 and g1262-1274.

## Automatic checks
- qa_auto (`--first_g 1119 --cuts 1125,1150,1190,1269`): **FAIL on "suspected blur" g1123-1142 only.**
  - I checked these frames at full size and they are sharp. The flag comes from the relative Laplacian test on frames that are mostly smooth track and sky (shot 21 pan). This is a false positive and does not block.
  - Cuts: g1150 (diff 53) and g1190 (diff 73) are on plan. g1125 and g1269 show "no change" because they are handle boundaries, not cuts inside the take.
  - Magenta 0 %. No black, blank or frozen frames.
- motion_check (`--first_g 1119 --cuts 1125,1150,1190,1269`): median **7.3**, p90 **12.7** (target 4 / 12). **PASS.**
  - Shot 23 is the calmest part (frame diffs 3-8), but it never falls under the near-static limit. It has no hold longer than 1 s.

## QA-tech checklist
| check | result |
|---|---|
| Heads above y 880 | **FAIL g1169-1189** (shot 22). Dick's head reaches y ~880 at g1169, then spans y ~850-1010 at g1172 and y ~935-1150 at g1182-1189. See fix 1. Every other shot is OK: the lowest head is the coach, at about y 610 (g1274). |
| No text, letters or numbers | OK. Scoreboards show only colour bars. The flags are tiny generic tricolours (see note 9). |
| Bodies grounded, scale | OK in shots 21 and 23. Shot 22 scale is consistent: he falls toward the lens, and the fallen bar lies at the same depth. |
| Nothing frozen | OK. The crowd mosaic, the coach's bob and the camera all move. |
| Attempt 1 (shot 21): flop backwards + bar_fall | **reads, weakly.** Dick goes up head-down and back to the bar (g1137-1142). The bar tilts and drops from g1143 and is mid-fall at the cut (g1149). Dick is very small. See fix 3. |
| Attempt 2 (shot 22): flop backwards + bar_fall | OK. He is inverted over the bar (g1156-1168), the bar swings down toward the lens (g1166-1181) and lies across the mat (g1182-1189). |
| Dick lies on the foam, hands on face (plan 22) | weak. Only one hand is near his cheek, and the face is half off frame (g1182-1189). See fix 1. |
| Coach in the stands, not hidden | OK. His head and torso are always clear above the rail. The pointing hand passes behind a dark seat block at g1196-1209, which is acceptable. |
| Coach mouth only in 40.38-42.25 s (g1214-1270) | **OK.** The mouth is a still line g1190-1212, talks g1213-1270 and is closed from g1271. g1213 is 1 frame early, which is within the ±0.15 s tolerance. |
| Coach jumps up, points, shouts; PUSH! at 41.7 s (g1254) | OK. He rises at g1197-1206 and points the whole shot. The push spikes at g1255-1260 (diffs 12-16). |
| Crowd faces | **FAIL g1190-1268** (shot 23). The brown-haired card right of the coach has a purple box over its face. The blue-cap man on the left has a box over his mouth and chin (g1194-1254), and so does the left-edge card. See fix 2. |
| Clipping | minor. g1262-1274: the coach's shirt hangs over the front face of the stand rail (bottom right of the shirt, red sliver). See note 6. |
| Continuity: kit | OK. Dick wears a white top with a red/blue band and navy tights in both shots 21 and 22. |
| Continuity: bar colour | OK. The bar is red and white in both shots 21 and 22. |
| Continuity: lighting preset | Shots 21 and 22 are both EVE: an orange horizon band on a blue sky, with floodlights. Shot 22 (the reverse angle) is brighter and more saturated, which is plausible for the reverse. Shot 23 drops to flat cold purple with no warm light. See note 5. |
| Neighbouring takes (shot 20 last frame, shot 24 first frame) | **not checkable.** Neither the s17 nor the s24 take is on the branch yet. |
| Artifacts | minor. Shot 22 (g1150-1189) has a V-shaped kink in the sky gradient at the frame centre (a dome seam) and a dark smudge in the middle of the stands. Shot 23 (g1190-1235) has two stray white diagonal lines in the top-left corner. See notes 7 and 8. |

## QA-art (phone, 360x640)
- **Clarity 5/10, beauty 6/10.**
- Does the take read as "he fails twice, the coach gloats, the stadium holds its breath"? **Partly.**
- **Fail twice:**
  - Fail 2 reads well. The bar swinging down at the lens and Dick flat on the foam make a funny image. However, the captions will cover his face and the frame cuts it in half.
  - Fail 1 reads only as "the bar tilted". Dick's head is about 20 px tall on the phone at g1144-1149.
- **The coach gloats:** the coach is clear, colourful and well placed, and the push on the punch word lands. His face is an angry frown, though, not a gloat.
  - The faceless crowd cards beside him look like a glitch at phone size.
  - The lower ~45 % of the frame is empty purple boxes.
- **The stadium holds its breath (shot 24):** not in this take.

## Fixes (numbered; 1-2 are blocking)
1. **Shot 22, g1169-1189: Dick's head is in the caption band and his face is cut by the right edge.**
   - At g1182-1189 the head spans y ~935-1150 and about half the face is off frame at x 720.
   - This is the "ร่วงอีก" punch image, and the captions will cover it.
   - Fix (any of these):
     - Tilt the camera down / raise the framing, or land him further from the lens, so his head stays at y <= 820 and fully inside x 60-660 from g1169 to the cut.
     - Turn the lie so his head is toward frame centre and his legs go off the edge, not the head.
     - Put both hands over his face (plan: "hands on face"). This will read on the phone.
   - Keep the bar swinging past the lens. It works.
2. **Shot 23, g1190-1268: the crowd cards' faces are covered by stand blocks.**
   - The brown-haired card right of the coach has a purple rectangle where its face should be (visible on every phone frame).
   - The blue-cap man and the left-edge card have blocks over their mouths and chins.
   - Fix (either):
     - Move those cards one row up or 0.3-0.5 D toward the camera so their heads clear the seat backs.
     - Hide the set's crowd blocks that sit in front of them.
   - A crowd member is fine partly behind a shoulder, but never with a box over the face.
3. **(strongly advised) Shot 21, g1134-1149: Dick is too small for the first fail to read.**
   - His head is about 5 % of frame height. On the phone he is a speck under the tilting bar.
   - Fix:
     - Push or slide the camera so Dick is at least 25 % of frame height at the bar (g1137-1149).
     - Let the bar_fall start at contact (about g1141), so the bar is clearly on its way down before the cut.
     - The plan says WHIP. Right now the move is a steady pan (frame diffs 9-12 throughout). Add a 2-3 frame snap at g1125-1127.
4. **(advised, art) Shot 23: make it a gloat.** In the frames outside the quote, swap the angry frown for a smug grin (g1190-1212, and the closed-mouth beat after g1271). Keep coach_shout + talk_mouth inside g1214-1270.

### Non-blocking notes
5. **Shot 23 light and composition.**
   - The stands are flat, cold purple boxes, with no warm practical. It does not match the warm EVE of shots 21-22, nor the client's "dense, warm lit set".
   - Fix:
     - Add warm fill or a floodlight key from the field side onto the coach and the rows around him.
     - Frame a little lower (or raise the coach) so the empty foreground boxes take less than 30 % of the frame.
     - Put a few colourful crowd cards in the rows behind him.
6. **g1262-1274: the coach card clips over the front of the rail.** Move the card 0.05 D back, or raise the rail edge.
7. **Shot 22: sky dome seam.** The orange band kinks at the frame centre (g1150-1189), and a dark smudge sits in the middle of the stands. Rotate the dome or move the camera yaw slightly so the seam is off frame. Check whether the smudge is a light-tower shadow.
8. **Shot 23, g1190-1235: two stray white diagonal lines in the top-left corner** (a rig or edge). Hide them or reframe.
9. **The tiny flag tricolours** in shots 21-22 should stay generic (not real national flags). At this size they are fine.

## Pending (not in this take)
- **Shot 24 (TENSE, g1269-1328)** goes to the s24 take gate. Checks there:
  - Hushed, but the crowd still breathes (crowd_mode bob on every frame).
  - Slow push 6 %/s + slide.
  - Dick rocking at his mark.
  - Still mouths.
  - TENSE preset with the spot pool not blowing the bar.
  - Kit and bar continuity with shot 22.
- **Continuity cut 20 -> 21:** check Dick's kit and the bar against the s17 take's last frame when it is delivered.

Re-check after the fixes: phone sheet of g1165-1190 (head above the band, face in frame) and g1190-1268 (no boxed faces). Shot 21 should be checked again if fix 3 is done.
