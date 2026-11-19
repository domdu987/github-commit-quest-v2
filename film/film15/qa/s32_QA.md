# s32 TAKE-gate QA (film 15, shots 32-36, g1804-2095 + handles 1796-1803 / 2096-2101) — KEY take (ending), QA-tech + QA-art

**Verdict: FAIL.** Shots 32-33 are good: three kits flop backwards over the bar and sit up smiling on the foam. The take is clean technically. But the punchline does not land on a phone:
- In shot 36 the coach is small, about 18 % of the frame height against a target of at least 25 %.
- He is sunk to the chest behind the mound, not buried to the chin.
- His thumbs-up is a tiny sideways fist.
- He wears a smug grin instead of a dazed, weak one.
- The lower 55 % of the frame is empty shaded sawdust.

In shot 34 the standard pole cuts through the coach's face for the whole shot. These problems hurt the film's ending, which is a key shot.

Take: origin/render15/team6 @ 5d1ee68, film/v3/film15/s32. take.mkv was rebuilt from 3 parts: 306 frames, 720x1280, 30 fps, first_g 1796.
Checked at 6 fps (every 5th g, 1796-2101) plus every cut ±3 (1804, 1875, 1939, 1988, 2040, 2095), at full size and on a 360x640 phone sheet (1 frame / 0.5 s).

## Automatic checks
- qa_auto (`--first_g 1796 --cuts 1875,1939,1988,2040`): **PASS**.
  - Magenta 0 %. No frozen, black or pop frames.
  - "No visible change ±2 at g1939": expected, because 1939 is the centre of the dissolve baked into the take (g1934-1944).
  - Soft frames:
    - g1935-1941 (the dissolve): OK.
    - g1988-1995 (the shot-35 whip, 8 frames, more than the 1-3 allowed): by eye this is camera-move softness on a wide framing, not DOF. Non-blocking.
- motion_check (`--cuts 1875,1939,1988,2040,2096`): median **4.3**, p90 **17.4** (target 4 / 12). **PASS** for the take.
  - Per shot (team numbers): 32 3.9/5.0, 33 3.6/5.1, 34 3.5/5.7. All three are just under median 4 and carried by 35-36. Non-blocking.

## QA-tech checklist
| check | result |
|---|---|
| Heads above y 880 | OK. The lowest head is about y 700 (shot 36 boys at g2041). |
| No text, letters or numbers | OK. Shot 33 scoreboard (g1926) is blank. |
| Flags in the 1968 stands (32-33) | Small striped tricolours. Same approved set as s17-s31. Non-blocking. |
| 1963 track: sawdust only | OK. Shots 34-36 show a wooden-frame sawdust pit and pile, with no foam. |
| Dissolve at 32 (in) | OK. 8 handle frames (g1796-1803), which is at least half the dissolve + 2. See note D. |
| Dissolve at 34 | Baked into the take (g1934-1944, centred on 1939). **Conform must NOT add a second dissolve here.** |
| Hard cut at the end | OK. g2095 is the last shot frame and the handle g2096-2101 continues the same shot. Conform cuts at 2095. |
| Grounding / scale | OK for 32-35 (contact shadows on track, foam and grass). Shot 36: see fix 1. |
| Frozen | none. In 36 the boys bounce only about 3-5 px. Weak, see note C. |
| Mouths | No quote window. OK: only fixed laugh mouths and the coach's static "O" in the air. |
| 32: different jumpers flop BACKWARDS over the bar | **OK**. Red (g1813-1826), green (1838-1850) and yellow (1856-1880) each go over hips-up, with head and legs hanging below the bar. Their faces stay upright to the lens, but it reads as a flop. |
| 33: land on the foam, smiling, unhurt | **OK**. Yellow lands on its back at g1881-1886. All three sit up smiling (g1896-1938) and the red jumper raises a thumb. The figures are small. See note B. |
| 34: coach sighing at the pit, boys on the bench with arms crossed | Boys: OK, sulky with arms crossed. Coach: **the standard pole cuts through his face from about g1955 to 1987**. See fix 2. |
| 35: coach runs the curve, turns his back, flops clumsily | **Mostly**. The whip-follow run is there (g1988-2016). The take-off is face to the lens (g2019) and he tumbles over the bar head-down with his cap flying and a shocked "O" (g2023-2039), so it reads clumsy. There is no clear back-turn, and he is small (about 8 % of frame height at 1988 and 2036-2039). See fix 3. |
| 36: TUMP into the sawdust, big spray, buried to the chin, weak thumbs-up, boys laugh | Spray: **good**, a dense burst g2045-2075. Boys: **good**, laughing with tears. Coach: **fails**. See fix 1. |
| 36: coach at least about 25 % of frame height | **FAIL**. Cap top is about y 415 and the pile line about y 640 at g2078-2095, so about 225 px = **18 %**. His face alone is about 10 %. |

## QA-art (phone size, 360x640)
- **Shots 32-33: clarity 8/10, beauty 7/10.**
  - Bright DAY stadium, a clear rhythm of flop after flop, three kits, the match-on-action cut at 1875, and a smiling line-up on the foam.
  - "Everyone does it now" reads at once.
- **Shots 34-36 (the payoff): clarity 5/10, funny 4/10, beauty 6/10.**
  - On a phone the setup in 34 is muddied by the pole through the coach's face.
  - Shot 35 is a fun tumble, but it is tiny in a wide frame.
  - The TUMP at 2040-2046 works (big body crashing in from the top, spray).
  - Then the final 1.6 s, the image the film ends on, shows the coach **standing chest-deep behind a sand mound among the standing boys, smirking**. It reads like a group photo, not "the coach who mocked the backward jump is now stuck head-out in the sawdust".
  - The thumbs-up is a 15-px sideways fist and is invisible on the phone.
  - The bottom 55 % of the frame is purple-shaded sawdust with plank-sized chips.
  - The promise "ข้าจะหงายหลังให้ดูเอง" is technically paid off: he does jump backwards and lands in sawdust. But the last image does not sell the humiliation and the good-sport thumbs-up, so the button is weak.

## Fixes (numbered; 1-2 are blocking)
1. **Shot 36, g2046-2095: rebuild the end frame around the buried coach.**
   - Size and framing:
     - Lower and push the camera so the coach's head plus the mound top fill the middle of the frame.
     - The coach (cap to mound) should be at least 25 % of frame height. Aim for a face of about 18-20 % of the height, centred around y 450-650.
     - Keep the mound's front edge just above the caption band (y < 880) and cut the empty foreground sawdust.
   - Burial: sink the coach card so the sawdust line sits at his chin or jaw, with no shoulders or windbreaker visible. Put him IN the mound top, in front of the boys, not behind it at their depth.
     - Optionally show his two sneakers sticking out of the pile at one side for the gag.
     - If he stays only head-out, add a mound of chips on his head and cap (already partly there).
   - Thumbs-up: raise one arm straight up out of the sawdust next to his head, with a big readable thumb (at least about 4 % of frame width) facing the camera, from about g2060 to the end. Give it a small wobble so it reads "weak".
   - Expression: dazed and sheepish (half-closed eyes, wobbly smile, or a spit of sawdust), not the current smug smirk.
   - Boys: keep them laughing, but place them behind and beside the mound, and raise the laugh bounce to the 0.06 D / 3 Hz spec.
2. **Shot 34, g1950-1987: the standard pole runs through the coach's face.** Slide the camera or the coach about 0.4 D so the pole clears him by at least one head width. Keep the pole as FG at a frame edge, not on the subject. Show the "sigh" with a shoulder drop or a head shake (a 0.5 s pose change) so the beat reads.
3. **Shot 35, g1988-2039: the coach is too small and never turns his back.**
   - Tighten the whip-follow so he is at least 20 % of frame height through the run.
   - On the plant (about g2016-2020), show a back or shoulder turn to the bar before the tumble, so it reads as the coach copying Dick's backward jump, not a random fall.
   - Keep the flailing tumble and the flying cap: they are funny.

## Notes (non-blocking)
- A. **Whip soft frames g1988-1995 (8 frames).** Acceptable at phone size. Trimming the streak to 3-4 frames would be cleaner.
- B. **Shot 33, g1875-1938:** the jumpers are small (heads about 60 px) and the bottom half is empty foam side and track. A lower camera or a push of about 15 % toward them would make the smiles and the thumbs-up read better. The thumbs from green and yellow are hard to see.
- C. **Shot 36 boys' bounce:** only 3-5 px. Raise it to spec (see fix 1).
- D. **Handle g1796-1803:** a white prop (disc) slides out across the bottom edge (y about 1200). It sits in the dissolve and below the caption band, so it is almost invisible. OK to leave.
- E. **Per-shot motion in 32-34 is median 3.5-3.9.** The take passes overall. If 34 is re-rendered for fix 2, add a little more push or slide there.

Re-check after the fixes: phone sheet of g1940-2095. A blind viewer should say "the coach who mocked the backward jump tried it himself and ended up stuck in the sawdust, giving a weak thumbs-up while the boys laugh".
