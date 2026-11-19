# QA-art, TAKE gate round 2, film 13 key takes s01 (shot 1 hook) and s02 (shots 2-3)
Reviewer: QA-art (Opus). Rules: film/QA_TEAM.md (QA-art + Stricter QA C), production-lessons.md section 2, plus: no round-blob
splashes/dust, and people on moving things move with them. Round 1: film13/qa/QA_ART_keys1.md.
Frames: every frame decoded; 360x640 phone sheets at 1 frame / 0.5 s with a y 880 guide (s01_phone.jpg, s02_phone.jpg), base crops,
dense sip crops, shot-3 full-res frames, phase-correlation and frame-diff measurements.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qaart13r2/
Frame refs: i = take frame index, g = first_g + i (s01 first_g 0, s02 first_g 57).

| take | density | light/colour | composition | acting | key moment | match | verdict |
|---|---|---|---|---|---|---|---|
| s01 hook | 7 | 8 | 6 | 6 | **4** | 6 | **FIX-FIRST** |
| s02 shot 2 | 6 | 7 | 7 | 6 | 6 | 6 | FIX-FIRST (one small fix) |
| s02 shot 3 | 7 | 7 | 8 | n/a | **8** | 8 | PASS |

---------------------------------------------------------------------------------------------------------------
## s01, shot 1 (hook). FIX-FIRST (5.5/10, up from 5)
Improved since round 1:
- Direction is now correct. The cornice stays fixed in frame (y ~90 on the phone from i0 to i62). The plinth lifts about 45-50 px at
  full res (~23 px on the phone) by i50 against the static mud and the foreground crib pier. The building reads as RISING, not sinking.
- A glowing strip of cribbing and jacks opens under the ground floor from ~i25 (0.8 s) and is a full-width band by i50-i62.
- People are on the flanks or in the foreground. Pullman stands in front of the centre of the gap but is small, and the gap reads on
  both sides of him. Nobody stands on the hotel, so the "move with it" rule does not apply here.
- Mud is ~27 % of the frame (target 20-25 %). Light is warm and handsome. No DOF, no text, heads above y 880.

Blocking:
1. **Round-blob dust.** The "dust motes" render as about 70 opaque cream-white SPHERES (8-20 px on the phone) in a row along the
   foundation line (s01_base.jpg, i20-i68). On the phone they read as a row of cotton balls or foam, not dust. They sit exactly over the
   gap and cover the cribbing, which is the key image. This breaks the no-round-blob rule.
   Fix: remove the motes entirely. If you want debris, use a few small DARK grit flecks (<= 3 px on the phone, brown/grey, unlit
   material) or thin falling streaks of soil from the plinth edge. Nothing white or round.
2. **No gap for the first ~0.8 s.** At i0-i20 the hotel still sits on the ground (lift starts at h 0.40). The hook has to show
   "off the ground" right away. Fix: start the lift so that a dark void plus lit cribbing is already ~15-20 px tall on the phone at i0
   (h start ~0.6), then keep the same climb rate to 0.95+. Keep the void under the floor dark so that the lit cribbing stands out
   against it.

Non-blocking (do it if the re-render allows):
- The smeared puddle reflection is still in the lower foreground (i0-i45). Darken it or remove it.
- Tilt up a few degrees so the mud is <= 22 %.

---------------------------------------------------------------------------------------------------------------
## s02, shots 2-3. FIX-FIRST, one small re-render of shot 2's tail only (6.5/10, up from 4.5)
Shot 3 (g 108-164, i51-107): PASS. This is now one of the best frames in the film.
- Camera above the cups: two round, mirror-still tea discs. The window cross is reflected in them. Frame diff in the tea area is
  2.1-3.0 vs 4.4 in the window; the remaining diff is the slow push, with no ripple.
- The window fills the top half. The clock tower and the rooftops slide down about 100 px on the phone (spire tip y ~115 -> ~215
  from i60 to i105). "The tea doesn't move, the street drops" reads in one look.
- The table, cups and pot are locked to the camera, so the things on the hotel move with the hotel. Correct.
- Minor: the tea reads pinkish (it reflects the sky). OK for this stylised look.
Shot 2 (g 63-107, i6-50):
- Good: the lower frontal camera puts the rug at ~27 %. The guests are larger, smiling and calm. The spire outside drifts down
  ~45 px on the phone between them. The lady's cup rises to her chin at i44-50.
- **Blocking: the gentleman's cup vanishes.** He holds the cup and saucer at his chest up to i38 (g 95). From i40-44 (g 97-101) his pose
  switches to arms down/behind, and the cup and saucer are gone (s02_guests_crop.jpg). On the phone this is a prop pop, and he never
  sips, which goes against "guests calmly sipping". Fix: keep his cup in hand through the end of the shot (g 95-107) and raise it to
  his mouth (a slow 8-10 frame lift), or hold the chest pose until the cut. Only g ~95-113 (to the end of the handle) needs a
  re-render. Shot 3 stays as it is.
- Lime cloud slabs (set sky texture): NOT blocking. They show as a band at the top of the window in shot 2 only, and they read as
  stylised cloud layers, not as a glitch at phone size. Cheap improvement for later: a hue/saturation key on the lime band in conform,
  or a slight tilt down so less sky shows.
- No wallpaper wall in the frontal framing: NOT blocking. The window wall is the point of the shot, and the chandelier corner plus rug
  and armchair carry enough "luxury suite". The low-poly brown chandelier fragment at the top-left reads as an object, not a
  chandelier. Optional: crop it out with a slight tilt down, which also helps with the clouds.
- Optional: the half cup on a shelf at the right edge (i0-i50) is a confusing fragment.

---------------------------------------------------------------------------------------------------------------
## Summary
- s01: FIX-FIRST. Direction and gap are fixed, but the white sphere "dust" covers the gap and breaks the round-blob rule, and the
  hotel is still grounded for the first 0.8 s. Remove the spheres and start the lift higher.
- s02: shot 3 PASS (keep it). Shot 2 FIX-FIRST only because the gentleman's cup vanishes at g ~97; re-render g 95-113 with his cup
  kept and a sip. Lime clouds and the missing wallpaper are not blocking.
