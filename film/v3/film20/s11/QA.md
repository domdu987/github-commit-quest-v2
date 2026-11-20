# s11 QA: film 20, take T11 = shots 11+12+13+14 as ONE camera-travel take (QA_TEAM §I) -- SITE, DAY
## Delivered
- take.mkv (split into take.mkv.partaa/ab/ac, 95 MB; `cat take.mkv.part* > take.mkv`): g 745..1003, 259 frames, first_g 745, 720x1280, 8 spp. g 753..995 = the take (25.09-33.21 s); 8 in-handle frames (dissolve 11 in) and 8 out-handle frames g 996..1003 (dissolve 13 out), rendered in 3D. NO cut inside. s/frame wall 10.9 (two processes), cpu 20.9.
- meta.json / cues.json (15 cues) / contact.jpg / phone_sheet.jpg / QA_AUTO.md (PASS; note: soft g 836-838 and 917 = the fast flights) / framediff.json. The old folders s12 s13 s14 are deleted.
- **qa_stats: `saturation 0.565, brightness 99.7, in-shot motion median 4.72 p90 15.45`** (sat >= 0.47, luma 85-110, motion >= 4 / >= 12: all met). **qa_stats2: `sat 0.565, vivid 66.3 %, luma 99.7, warm 37.2 % / cool 47.9 %`** (no cut inside) (sat >= 0.50, vivid >= 45 %: met). deliver.py frame-diff 4.48 / 23.08.
## The travel (what the viewer sees)
| g | beat |
|---|---|
| 745-801 | Fence, eye level 1 m: the lady (parasol), gent (pointing) and child (pointing) laugh (3 Hz squash, 0.10 D bounce, head roll); Eiffel at the gate holds the giant rivet up. Camera pulls back 10 %/s, snap push x1.4 on "เรียกไอเฟลว่า" (778). |
| 802-816 | PUNCH-IN snap onto Eiffel + rivet on "ไอ้ช่างหมุด" (802), 2-frame shake, 6 frames of speed lines (deliver.py, clear area round the face). |
| 817-848 | The camera RISES over the fence (stage 0 -> 1 at g 830, hidden in the fast flight) and flies over the cart yard, the leg foot and its scaffold platform to the red-lead stack. |
| 848-906 | Eye-level truck along the 1.7x stack: two workers carry an I-girder past it (walk, in step with the camera), the derrick's girder swings behind; snap on "เหล็ก 18,000" (856). |
| 906-920 | Flight up and over the stack, under the first-platform arches (dappled sun), to the rivet deck at 17 m. |
| 920-943 | Deck: riveter_tongs throws the glowing rivet (919-929, drawn x3.2), riveter_hammer catches and cheers, riveter_forge hammers every 9 frames with sparks (strength 1.5); push + snap push on the catch (929); forge glow + low sun on the planks. |
| 943-993 | Three crane-up snaps to site_rise_snap1/2/3 on "ชั้นหนึ่ง / ชั้นสอง / จนถึงยอด" (948 / 967 / 981): platform 1 (stage 1), platform 2 (stage 2 at g 969), finished spire (stage 3 at g 985); then a slow drift to g 1003. |
## Checked
- Nobody is still: the Parisians laugh, Eiffel bobs the rivet, carriers walk, riveters work, every frame. Mouths not animated (no Maupassant here). Feet: Parisians / Eiffel / carriers on the ground (ray cast), riveters on the real deck plank surface (0.28 D above the mark z), contact decals; no hanging bodies.
- No DOF, no text. Eiffel's tower (legs / scaffolds / platforms / spire) is in frame in every part except the low stack truck (the derrick and the red-lead stack are the subject there; the tower leg and the stage-1 platform are in the g 906-913 flight).
- Camera never touches geometry in the final frames: flights were routed by hand around the leg footprint and the pile (an earlier route went through the pile / leg: black frames, fixed). 
- Blur flag: the smooth stack / flight frames (g 846-925) got a mild unsharp mask in deliver.py (radius 1.6, 110 %) and the gravel in front of the stack has 130 stones / offcuts (runtime dressing); without these qa_auto flagged 16 soft frames.
## Deviations / notes
- Eiffel is small (~50 px head) in the fence framing; the punch-in snap (g 802) gives the close view. The close-up frames (punch-in, deck) are about 1 s each.
- Hand-held jitter (+-0.07 D) is part of the motion; frame-diff is mostly real camera travel (rise, flights, crane-ups).
- The catcher stands near the set's bucket and cheers; he does not hold it.
- Exposure: no trim needed in this take (luma 100.8).

## TAKE gate r2 fixes (TAKE2_A.md) -- done in this delivery
1. Pop g818-819: the old spline carried the lens through the child's cap. The rise is now: eased punch-in, then up-and-back crane (g817-828) keeping Eiffel and the Parisians in frame, then the flight; no frame-to-frame jump (max in-shot diff at the punch-in snap only).
2. Sand g819-840: the camera looks 8-25 m above the horizon line over the cart yard / leg foot / scaffold platform; ground about 25-35 % (it is the fast flight, ~1 s).
3. Rivet g802-812: a runtime 3-D giant rivet in his fist: round red dome head + a visible cylindrical shank, held head-up and bobbing (the sprite prop is removed).
4. Carriers g848-906: neutral expression, mouths closed.
5. Toss / catch g917-933 (16 frames): own small orange-hot cylinder on a visible arc from the thrower's tongs to a steel bucket held in the catcher's hands (follows his hands, rises with them when he cheers); the camera is closer (9.5 D) and pushes in; sparks every 9 frames.
6. Bowl g908-912: the flight looks down (0.5-2 m targets) while passing under the arches, so the first-platform underside no longer fills the frame; dappled sun on the gravel instead.
7. Ending: after the last snap the camera keeps pushing (+14 %/s) so g993-1003 is not still.
- Also: plank offcuts in front of the stack have distinct thicknesses (no coplanar black slits).

## TAKE gate r3 fixes (TAKE3_A.md) -- done in this delivery
1. Rivet g814-822: rebuilt as a short fat cylinder shank (about as long as the head is wide) + a rounded dome head, dark iron with a red-lead tint, held sideways (25 deg raised) in the raised fist so the shank shows; it bobs.
2. Black unlit box g820-821 = the set's bench at (-4, -104) m seen from above during the rise: its vertices are deleted at runtime (pf_dark / pf_timber / pnoink_plank, 120 vertices).
3. Ground: the looks of the fence-rise flight are 5-38 m high, so sand is the lower 20-30 % at g823-841 (sky + tower leg / stack dominate); g913 looks level (not down) under the arches.
4. Toss / catch g917-933: the thrower stands 1.7 m from the catcher (staging moved, the set's mark was 3.4 m away) so both fit a close deck framing (6.5 D, ~3 m wide); the toss is a bigger orange-hot cylinder (duller orange, no yellow bloom) on a visible arc into the steel bucket in the catcher's hands. The thrower's tongs stay small at this distance.
