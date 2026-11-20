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

---
## Re-check r2 (render15/team1 @ c98f2d1, rebuilt in scratch takes/s01r2)

**Verdict: PASS.** The hook now reads on the phone. Shot 1 shows a boy clearing the bar horizontally, face-first, and landing in the sawdust with a spray. Shot 4 shows Dick going over upside-down and arched, head hanging below the bar, then landing flat on his back in a dense spray, while the boys gape. The remaining items below are non-blocking notes.

### Automatic checks
- qa_auto: **PASS**.
  - It flags g108-111 as soft frames (the planned whip).
  - It reports "no visible change ±2 at g108" because the streak smears the cut frame. The cut is still on plan.
- motion_check: median **5.4**, p90 **21.2** (target 4 / 12). **PASS**. The longest low-motion run is g64-71 (8 frames, the eased start of shot 2).
- Heads above y 880 on every visible card. The team's `wb` boy at 1014 is off frame in shot 3 and is not visible on the phone sheet.

### Fixes 1-8 from the first review
| # | status | evidence |
|---|---|---|
| 1 shot 1 straddle | **done** | The jumper is centred and in frame from g0. He takes off at g20-25 and goes over the bar horizontally, head and leg leading, at g30-46, clearing the bar by about 0.3 D. His face still points at the lens, but on the phone it reads as "goes over face-first". |
| 2 waiting boys | **done** | The boys stand on the run-up (g0-20) and leave the frame. The bar cuts no head, and the landing and spray are clear at g55-62. |
| 3 shot 3 curve + back-turn | **partly** | The camera follows the run, Dick is about 30 % of frame height, and the plant and take-off happen at the standard (g124-133). The curve is slight, and Dick's face stays to the lens the whole time, so no back-turn is visible. See note A. |
| 4 shot 4 path through the curly boy | **mostly** | Dick now passes in front of the boy (g162-166: his head covers about half of the boy's head for about 4 frames). It reads as depth, not as a collision. The legs flick up at g164-166 like a real flop. Back-first landing in the centre at g168-170. |
| 5 landing / spray | **done** | Spray at g168 plus a second burst at g171, dense and high (g175-185). The lying Dick spans about 45 % of the frame width. |
| 6 PUSH! at 2.9 s | **done** | The push runs from g88 to g101, and Dick grows about 22 %. |
| 7 eye-lines | **done (minor)** | The boys turn toward the action. In shot 4 they still mostly face the lens while gaping, which is acceptable. |
| 8 rocking pops | **done** | The 7-frame spikes are gone and the diffs are smooth (g64-107). |

### QA-art (phone, 360x640)
- **Clarity 7/10** (was 4), **beauty 7/10**.
- A first-time viewer gets "the others go over the normal way, this kid goes over backwards, upside down" within the 6 s. The flop arch at g145-155 is the image that sells it.

### g108-110 whip streak
- It is not a smooth streak. It is a stepped multi-exposure of 4-5 discrete copies (trees, bleachers and Dick doubled).
- g108 also carries a large transparent ghost of the shot-2 close-up Dick over the new framing, which looks like a short dissolve glitch.
- At full size it is a little ugly. At phone size and 30 fps it lasts 3 frames (0.1 s) and reads as a whip blur. **Not blocking.**

### Notes (non-blocking; fix if the team has a cheap re-render)
- A. **Shot 3, g118-133:** for the plan's "turns his back to the bar", add a head or shoulder turn away from the bar on the plant (g128-133), using the side or back card if cast15 has one.
- B. **Whip, g108-110:** raise the sub-frame count to about 12-16 so the streak blends smoothly, and drop the samples that fall before the cut so g108 has no shot-2 ghost. This is only 3 frames to re-render.
- C. **Shot 4, g162-166:** move the curly boy about 0.5 D further left so Dick's head clears his face.
- D. **Shot 4 bar fill (not done):** the bar reads maroon/lavender in backlight against red/white in shots 1 and 3. Add a little fill light on the bar for continuity.
