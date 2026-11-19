# s17 TAKE-gate QA (film 15, shots 17-20, g932-1124 + handles 924-931 / 1125-1130): KEY take, QA-tech + QA-art

**Verdict: FAIL.** The take is clean and pretty. It fails on one hard-rule beat that the story needs: in shot 20 the bar sits on Dick's hair, so the "bar ~30 cm above his head" gap does not show. Everything else is non-blocking.

Take: origin/render15/team4 @ 317b004, film/v3/film15/s17. take.mkv was rebuilt from parts: 207 frames, 720x1280, 30 fps, EVE.
- Shot ranges: 17 = g932-974, 18 = g975-1013, 19 = g1014-1057, 20 = g1058-1124.
- transition_in is an 11-frame dissolve, with an 8-frame in-handle.

Frames checked:
- 6 fps (every 5th g) plus every cut ±3 (929-935, 972-978, 1011-1017, 1055-1061, 1121-1127), at full size.
- A 360x640 phone sheet.
- Head and bar crops at g968, g974, g1062, g1090, g1110 and g1124.

## Automatic checks
- qa_auto (`--first_g 924 --cuts 932,975,1014,1058,1125`): **PASS.**
  - Soft frames g1014-1016: the whip into shot 19, 3 frames of streak, which is allowed.
  - "No visible change" at g932 and g1125: these are handle boundaries, not cuts in the take.
  - "No visible change" at g975 and g1014: these are real cuts (diff 47 and 24), and the neighbouring frames move too.
  - Magenta 0 %. No black or frozen frames.
- motion_check (`--first_g 924 --cuts 932,975,1014,1058,1125`): median **4.8**, p90 **14.5** (target 4 / 12). **PASS.**
  - Shot 18 is the flattest part (frame diffs 1.7-2.9 over g976-997, 22 frames). It stays under 1 s, so it is not a near-static hold, but it is the weak spot (see note 3).
- **Flashes:** the flash bulbs at g945-948 and g963-966 show as brightness spikes, and they are on plan.

## QA-tech checklist
| check | result |
|---|---|
| Heads above y 880 | **OK, with one marginal spot.** Shot 17 g970-974: Dick's chin reaches y ~885 at the very end of the push (his head centre is at about y 850). Everything else is clear. Officials' heads are at y ~470. Shot 20: the lowest chin is at y ~845 (g1110-1124). See note 1. |
| No text, letters or numbers | OK. The scoreboard shows only colour bars, and the flags are tiny generic tricolours. |
| Grounded, scale, nothing frozen | OK. Contact shadows are present. The crowd mosaic, the camera and Dick's breathing all move. |
| Mouths | OK. Nobody talks, and all mouths are static. |
| 17: grand stadium push, torch, crowd, flags, dissolve in | OK. A wide rise and dolly toward the pit, with the torch, floodlights, a flag ring and two flash bulbs. The officials' table and chairs are a foreground prop at the bottom-right edge. The in-handle g924-931 is the same move extended backwards, which is enough for an 11-frame dissolve centred on g932 (it needs 6). |
| 18: officials raise the bar, tilt up | **weak.** Two officials stand at the standards, and the bar steps up left peg then right peg (it tilts at g1000, level at g1012). The right official points up from g1004. Nobody touches the bar or pegs, and the tilt is hard to see. The right official's card is cut by the frame edge at g975-988. See note 3. |
| 19: rival straddles, knocks the bar, walks off dejected | **mostly.** Whip in (g1014-1016). The rival runs and goes over face-down at g1032-1042, and the bar falls at g1042-1057. He is small: about 8 % of frame height at the bar. The shot ends with him getting up on the mat at g1057, so no dejected walk-off is visible. See note 4. |
| 20: Dick by the standard, gap ~0.55 D head top -> bar | **FAIL.** See fix 1. |
| Continuity | OK. Dick wears a white top with a red/blue band and navy tights, the same as shots 21-22 and 24. The bar is red and white in 17-20. The light is EVE throughout. |
| Join 20 -> 21 (g1124 -> s21 g1125) | OK. Same kit and bar, both EVE. The cut from Dick standing at the standard to his run-up reads. |

## QA-art (phone, 360x640)
- **Clarity 5/10, beauty 7/10.**
- **Shot 17** is the most beautiful opening of the stadium so far: a warm torch, floods, the sky band and the flash pops. Dick, though, is a small figure at the bottom.
- **Shot 18** reads as "two officials standing by a bar". The raise barely reads.
- **Shot 19:** "someone else tries the normal way and knocks it off" reads, but at a small size.
- **Shot 20** should be the "look how high that bar is above him" image. Instead the bar looks like it rests on his hair, so the false-payoff build-up ("he's going to try THAT?") is lost.

## Fixes (numbered; 1 is blocking)
1. **Shot 20, g1058-1124: no visible gap between Dick's head and the bar.**
   - At g1090-1124 the bar underside is at y ~630-640 and his hair tips are at y ~640-655, so the hair touches or overlaps the bar.
   - The skull top is only ~60 px below the bar (about 0.4 head-height).
   - On the phone it reads as "the bar is on his head".
   - Fix:
     - Raise the bar in shot 20 (set_bar_height) by about 0.4-0.5 D. Or move Dick 0.3-0.5 D further from the bar plane and lower the camera slightly below his head height, so the perspective opens the gap.
     - Target from g1075 to the cut: a clear sky/crowd strip of at least 60 px (about half a head-height) between the hair tips and the bar underside, and at least 0.55 D to the skull top.
     - Keep the tilt-up and the two quick pushes. Keep his chin at y <= 860.

### Non-blocking notes
- 1. **Shot 17, g970-974:** tilt the camera down about 20 px at the end of the move so Dick's chin clears y 880.
- 2. **Shot 17:** Dick is about 10 % of frame height at the end. That is fine for an establishing shot.
- 3. **Shot 18:** make the raise read.
  - Let each official put a hand on his standard's peg as it slides up (left at about g985-995, right at about g998-1008).
  - Add the planned tilt-up of about 8-10 % over the shot.
  - Bring the right official fully into frame by g978.
- 4. **Shot 19:**
  - Push in about 30 % so the rival is at least 15 % of frame height at the bar.
  - Let him stand and turn away with slumped shoulders at g1050-1057 (the plan says "walks off dejected").
- 5. **Sky V seam** at the frame centre (shots 19-20). This is a set item, as in s21.

---
## Re-check r2 (render15/team4 @ 968543a, rebuilt in scratch takes/s17r2)

**Verdict: PASS.** The blocking shot 20 problem is fixed: on the phone the bar now reads clearly above Dick's head for the whole shot. Shots 17, 18 and 19 are also better. What remains below is non-blocking.

### Automatic checks
- qa_auto (`--first_g 924 --cuts 932,975,1014,1058,1125`): **PASS.**
  - Soft frames g1014-1016 are the whip into shot 19 (allowed).
  - The cuts at g975, g1014 and g1058 are real (frame diff 50, 31 and 56) and on plan.
  - The "no visible change" notes at g932 and g1125 are handle boundaries.
  - Magenta 0 %. No black or frozen frames.
- motion_check (same cuts): median **5.5**, p90 **13.6** (target 4 / 12). **PASS.**

### Blocking fix 1: shot 20 gap (measured at full size, 1:1 crops with a ruler)
| g | bar underside y | hair tips y | strip above the hair | skull top y | bar -> skull | 0.55 D (D from Dick's height) | chin y |
|---|---|---|---|---|---|---|---|
| 1060 | ~390 | ~425 | ~35 | ~460 | ~70 | ~45 | ~545 |
| 1075 | ~558 | ~590 | ~32 | ~625 | ~67 | ~45 | ~715 |
| 1086 | ~565 | ~595 | ~30 | ~630 | ~65 | ~48 | ~720 |
| 1098 | ~553 | ~600 | ~47 | ~640 | ~87 | ~55 | ~740 |
| 1104 | ~545 | ~605 | ~60 | ~640 | ~95 | ~60 | ~745 |
| 1110 | ~520 | ~595 | ~75 | ~625 | ~105 | ~65 | ~765 |
| 1117 | ~518 | ~600 | ~82 | ~630 | ~112 | ~68 | ~770 |
| 1124 | ~518 | ~610 | ~92 | ~645 | ~127 | ~70 | ~775 |

- **Bar to skull top >= 0.55 D (the hard rule):** met in every frame.
- **Chin y <= 860:** met. The lowest chin is ~775.
- **Strip of at least 60 px above the hair tips:** met only from about g1100 to the cut.
  - In g1060-1095 (the first half, before the pushes) the strip is ~30-35 px. That is ~15-18 px on the phone.
  - It is still a clearly visible band of mat between the tufts and the bar, and the bar no longer touches the hair in any frame.
  - I do not fail the take for this, because the beat now reads. See note A.

### Non-blocking notes from the first review
| # | status | evidence |
|---|---|---|
| 1 shot 17 chin | **done** | g970: chin ~850. g974: chin ~865. Below the caption line (880) in every frame. |
| 3 shot 18 raise | **mostly** | The right official is in frame from g977, after a whip in at g975-983. Both officials point at the bar as the pegs step up (left g984-1000, right g996-1012). The hands on the pegs and the planned tilt-up are not done. g984-1013 is the quietest stretch of the take (frame diffs 1.6-5, about 1 s). It is not frozen, but it is right at the limit. See note B. |
| 4 shot 19 rival | **done** | The camera is closer and the rival bigger. Take-off is at about g1026, he goes over face-down, and the bar falls at g1039-1049. He stands at the right at g1049 and walks out of frame by g1054-1057. |
| 5 sky seam | unchanged | A set item. |

### Continuity
- **Join 20 -> 21** (g1124 -> s21 g1125): same kit, same red/white bar, both EVE. OK.
- Dick's kit and the bar are the same across shots 17-20.

### QA-art (phone)
- **Clarity 7/10** (was 5), **beauty 7/10**.
- Shot 20 now reads as "the bar is set above his head". Shot 19 reads as "another jumper knocks it off and walks away".
- The higher camera in shot 20 (looking slightly down) makes the bar feel a little less towering than the plan's low tilt-up would. That is acceptable.

### Notes (non-blocking; only if the team has a cheap re-render)
- A. **Shot 20, g1058-1098:** open the strip above the tufts to about 60 px. Lower the camera look by about 25 px, or raise the bar 0.2 D, for the first half only.
- B. **Shot 18, g984-1013:** add the planned slow tilt-up (about 8 %/s) so the stretch between the whips is not near-static. A hand on each peg as it rises would make "they raise the bar" read without the pointing.
