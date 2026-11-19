# s01 TAKE-gate QA (film 15, shots 1-4, g0-183 + handle 184-189) — KEY take (hook), QA-tech + QA-art

**Verdict: FAIL**. The take is clean technically, but two of the four story beats do not read on a phone. Shot 1 does not show a clear face-down straddle. Shot 3 has no curve and no back-turn. Shot 4's landing passes through a bystander. Because this is the hook, these problems hurt the film.

Take: origin/render15/team1 film/v3/film15/s01 (take.mkv rebuilt from parts, 190 frames, 720x1280, 30 fps).
Checked frames at 6 fps (g0-185, every 5th) plus every cut ±3 (63, 108, 134, 184), at full size and on a 360x640 phone sheet.

## Automatic checks
- qa_auto (`--first_g 0 --cuts 63,108,134`): **PASS**. Cuts are on plan, magenta 0 %, no frozen, black or pop frames.
- motion_check (`--cuts 63,108,134,184`): median **4.5**, p90 **14.4** (target 4 / 12). **PASS**.
- The low-motion runs are the eased starts g0-4 and g64-69 (each under 0.25 s). No near-static hold is longer than 1 s.

## QA-tech checklist
| check | result |
|---|---|
| Heads above y 880 | OK. The lowest head is about y 700 (shot 4 boys). |
| No text, letters or numbers | OK |
| Sawdust only, no foam | OK. Wooden-frame sawdust pit in shots 1, 3 and 4. |
| Bar where the story says | OK. The bar stays up in all four shots. |
| Frozen or near-static > 1 s | none |
| FG prop at an edge | OK. Hurdle (shot 1), red box (2), post (3), standard pole (4). |
| Mouths | OK. No talking. The boys' static open "O" gape from g155 is an expression, not lip movement. |
| Contact shadows / grounding | OK for standing cards |
| Shot 1 face-down straddle | **weak**. See fix 1. |
| Shot 3 curved approach + back to bar | **missing**. See fix 3. |
| Shot 4 backwards ∩ + sawdust landing with spray | arch **reads** (g145-155). Landing **broken**: see fixes 4 and 5. |
| Staging / overlap | **bystanders stand in the landing pit**. See fixes 2 and 4. |
| Eye-lines | weak. See fix 7. |

## QA-art (phone size)
- **Clarity 4/10, beauty 7/10.**
- The GOLDEN light, the set and the low angle in shot 4 are attractive. The shot 4 arch at g145-155 (head hanging below the bar, torso over it) is the strongest image in the take.
- A viewer would **not reliably** get "everyone jumps face-first, this kid jumps backwards" in 6 s:
  - The face-first half (shot 1) is small, sits on the right edge and is partly covered by the waiting boys. It reads as a horizontal Superman dive with the face turned to the camera, not as a face-down roll.
  - Shot 3 shows a boy jogging toward the camera, with no curve and no turn.
  - In shot 4 Dick drops through the curly boy and lands small at the back of the pit.

## Fixes (numbered; 1-5 are blocking)
1. **g0-50, shot 1: the straddle does not read as face-down, and the jumper is too small and at the edge.**
   - Problems:
     - g0-8 show only the waiting boys, because the jumper is off frame.
     - g5-25: the jumper is cropped by the right edge.
     - g30-40: he flies about 150 px above the bar, horizontal and head-first with his face to the lens.
   - Fix:
     - Reframe or slide so the jumper's whole run and jump happen in the centre half of the frame, with him at least 25 % of frame height.
     - Start the run in frame at g0.
     - Use straddle_a/b with the head and face turned DOWN toward the bar (belly to the bar, one leg leading) and clear the bar by about 0.3 D, not a dive.
2. **g30-62, shot 1: the waiting boys stand in the pit, on the bar line.**
   - The bar runs through the curly boy's head (g35-50).
   - The jumper drops behind him and his landing is hidden (g45-62).
   - Fix: move both boys to the run-up, on the camera side of the bar and away from the pit, as the plan says ("two boys wait at the run-up"). Keep the landing and the spray clear in frame.
3. **g108-133, shot 3: no curved approach and no back-turn.**
   - Dick runs straight at the camera, face front, and is small (head about 35 px on the phone).
   - He stops beside the standard (g125-133).
   - Fix:
     - Push the camera closer so Dick is at least 30 % of frame height.
     - Give him a visible J-curve that starts wide and bends in toward the bar.
     - By g126-133, show him side-on and then with his back or shoulder to the bar. Use a back view or a head turn away from the bar on the plant/takeoff.
     - The plan says WHIP: add a real snap pan of 1-3 frames with streak at the cut-in (g108-111).
4. **g158-168, shot 4: Dick flies through the curly boy, and his descent becomes a head-down dive.**
   - g160: Dick's head covers the curly boy's face.
   - g165: Dick's body is behind the boy's head, with his feet straight up.
   - Fix:
     - Move the boys out of the landing path. Flank wider, at the pit corners or outside the frame of the pit, at least 1 D from Dick's line.
     - Keep the fall back-first and flattening (flop -> flop_flick -> land_back) so he lands on his back, fully visible in the centre of the pit.
5. **g168-183, shot 4: the landing and spray are small and late on the phone.**
   - Dick lies small at the back, partly covered by the boys. The spray only shows at g175-180 and is thin.
   - Fix:
     - Fire sawdust_spray at contact (g168), denser and bigger (chips reaching about 1.5 D high).
     - Place the landing so the lying Dick is at least 35 % of frame width, in front of the boys' line.
6. **g87-101, shot 2: the PUSH! at 2.9 s is not keyed.** The diffs show only the steady push (6-7). Fix: add a quick eased push of 15-25 % over g88-101 on "คนนี้".
7. **(minor) Eye-lines.**
   - Shot 2 (g63-107): the boys look into the lens, but the plan says they glance at Dick.
   - Shot 4 (g150-189): the gaping boys stare into the lens.
   - Fix: turn their pupils toward Dick or his landing.
8. **(minor, non-blocking) g63-107, shot 2: Dick's rocking pose pops every 7 frames** (diff spikes at g70, 77, 84, 91, 98 and 105). It reads as a stutter. Fix: tween the rock/bounce poses.
9. **(note, non-blocking)** The bar in shot 4 reads maroon/lavender in backlight against red/white in shots 1 and 3. That is acceptable, but a little more fill on the bar would help continuity.

Re-check after the fixes: phone sheet of shots 1, 3 and 4. A blind viewer should be able to say "the others go over face-down, this one goes over on his back".
