# s05 TAKE-gate QA (film 15, shots 5-9, g184-488, take first_g 176, 319 frames incl. 8 dissolve-in handles + 6 tail handles)

**Verdict: PASS.** Technically clean. All five planned beats are visible and in order. Three weaknesses remain; none breaks the film, so they are non-blocking notes (1-3).

Take: origin/render15/team2 film/v3/film15/s05 (take.mkv rebuilt from 3 parts, 319 frames, 720x1280, 30 fps).
Checked 64 frames at 6 fps (every 5th from g176), every cut +-3 (184, 246, 344, 398, 424) and a 360x640 phone sheet. Compared against s01r2's last frames.

## Automatic checks
- qa_auto (`--first_g 176 --cuts 246,344,398,424`): **PASS**. Magenta 0 %, no frozen, black or pop frames. "No visible change" at 246, 344 and 398 is a flag for same-scene cuts. I confirmed they are visible cuts because the camera angle changes.
- motion_check (`--first_g 176`): median **6.9**, p90 **12.9** (target 4 / 12). **PASS**, but p90 is only just over.
  - Per shot: 5 = 6.6 / 13.8, 6 = 6.5 / 10.2, 7 = 8.3 / 16.7, 8 = 6.7 / 14.9, 9 = 8.0 / 12.3.
  - Only the handle ranges (g176-183, 489-494) are low, by design.

## Checklist
| check | result |
|---|---|
| Heads above y 880 | OK. The lowest head is about y 600 of 1280 (shot 8, Dick sitting up, head at about y 100-300 of 640 on the phone frame). All other heads are higher. |
| Contact shadows / scale | OK. The standing boys and Dick have ground shadows. The sit-up Dick in the sawdust is correctly scaled. |
| Nobody frozen | OK. Boys, coach and crowd on the bench bob in shot 5, and there are no static runs of 6 or more frames. |
| No text, letters or numbers | OK |
| 1963 pit = sawdust only | OK. A wooden-framed sawdust pit in every shot, with chips. No foam. |
| FG prop at an edge | 5: cone and disc at the bottom corners. 6: cone and post. 7: white water cooler at the right bottom. 8: none (the team dropped the prop; the bar and pit wall fill the bottom). 9: standard or post at the bottom right. |
| Shot 5 dissolve-in | `meta.json` says `dissolve` with 11 frames. 8 handle frames are present (g176-183), then 6 after the take. The take holds pure shot-5 frames, so the blend itself is done at conform. The handle frames show the moving crane with no pop. OK. |
| Continuity with the end of s01 | OK. Dick's maroon-and-gold vest is the same. The boys are the same: curly in blue and white stripes, blond in green and white stripes. The red and white bar is the same. The wooden-framed sawdust pit and the warm GOLDEN light match. |
| Mouths | Still throughout. OK, because no quote window falls in g184-489. |

## Plan coverage and phone legibility (360x640)
| shot | plan | in the take | reads on the phone? |
|---|---|---|---|
| 5 (g184-245) | establishing wide, pull-back crane | The camera starts lower and pulls back and up. Bleachers, gym, pines, bunting, cinder track, the pit and the bar, and the boys at the run-up are all in frame. A boy straddles at about g232-240. | The place reads: school track, warm and dense. The people are tiny (about 12 px heads), so the action does not read. This is acceptable for an establishing shot. |
| 6 (g246-343) | boys straddle-roll face-down, 2 clean jumps | Boy 1 jumps at g262-285 and boy 2 at g306-330. Both go over the bar flat and head-first, clear it, land with spray and sit up. | **Yes.** The same read as s01 shot 1: a horizontal roll over the bar, face toward the lens or down. |
| 7 (g344-397) | Dick tries the straddle, knocks the bar off | Dick walks in at g361, takes off at g372, and flies over the bar looking shocked. The bar falls at g380 and tilts down through g386-397. | **Yes.** The falling bar and Dick's wide-eyed shock read clearly. He does not visibly touch the bar, but the bar falling the moment he passes makes it read as a knock. |
| 8 (g398-423) | the bar bounces in the sawdust, Dick sits up sheepish | The bar drops and rests on the front rim of the pit, and Dick sits up with a sweat drop, a half smile and chips in his hair. | **Yes.** Sheepish Dick is the clearest image in the take. The bar mostly lands on the pit wall and does not visibly bounce in the sawdust. |
| 9 (g424-488) | Dick turns his back, clean backward flop | Dick walks in from the right at g441. He takes off at g452 and goes over the bar arched, with his head hanging below the bar and his legs above it (g461-475). He lands in the sawdust (g476-482), then sits up behind the bar. | **Mostly.** The arch with the head under the bar reads. Dick is small (about 30 px). He faces the lens on the approach, so there is no visible back-turn. |

## Failures by frame (all non-blocking)
1. **g246-258, shot 6 opening: empty frame.** The cut lands on bare cinder and a post, and boy 1 only enters at the right edge around g251-256. That is about 0.4 s of nothing on a phone. Fix: start the shot at g252 or later, or put boy 1 in frame at the cut.
2. **g344-360, shot 7 opening: Dick is off frame.** He only appears at the right edge at g361, so about 0.5 s is cinder and the cooler prop. Fix: place Dick at his mark inside the frame at g344, or shorten the lead-in so the knock comes sooner.
3. **g452-475, shot 9: the flop is small and faces the lens.**
   - The plan says "turns his back". The approach shows his face, not his back, and the high-angle orbit shrinks the arch.
   - This is a repeat of shot 4's beat, and the beat is already carried there and in the later reveal.
   - Fix if cheap: push the camera in about 25 % so the arch is at least 40 % of the width, and turn the card to a back or shoulder view on the plant (g448-452), as already suggested for s01 note A.
4. **g398-406, shot 8: the bar rests on the pit rim instead of bouncing in the sawdust.** At g398 the bar is falling diagonally in the frame, and by g400 it lies along the front of the pit with no visible bounce. Fix: add one visible bounce, a short hop of about 0.3 D at g400-404, onto the sawdust.
5. **g486-488 (and handle g489-494), shot 9: the sitting Dick is partly hidden by the bar across his neck.** Fix: seat him about 0.3 D forward or lower the camera.
6. **Motion:** shot 6 p90 is 10.2 on its own, but the take total passes (12.9). Add a slightly stronger slide or push in shot 6 if there is any re-render.
7. **g226-241, shot 5:** the sky is pink to lilac, while s01 is warm orange to yellow. The grade shifts in the dissolve. This is acceptable for the transition and is not a continuity break.

None of these needs a re-render for the gate to pass. Fixes 1 and 2 are the cheapest, and each means only moving the cut or the character start.
