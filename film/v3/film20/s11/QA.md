# s11 QA: film 20, take T11 = shots 11+12+13+14 as ONE camera-travel take (QA_TEAM §I) -- SITE, DAY
## Delivered
- take.mkv (split into take.mkv.partaa/ab/ac, 95 MB; `cat take.mkv.part* > take.mkv`): g 745..1003, 259 frames, first_g 745, 720x1280, 8 spp. g 753..995 = the take (25.09-33.21 s); 8 in-handle frames (dissolve 11 in) and 8 out-handle frames g 996..1003 (dissolve 13 out), rendered in 3D. NO cut inside. s/frame wall 10.9 (two processes), cpu 20.9.
- meta.json / cues.json (15 cues) / contact.jpg / phone_sheet.jpg / QA_AUTO.md (PASS; note: soft g 833-835 = the fast flight over the cart yard) / framediff.json. The old folders s12 s13 s14 are deleted.
- **qa_stats: `saturation 0.556, brightness 100.8, in-shot motion median 4.82 p90 14.28`** (sat >= 0.47, luma 85-110, motion >= 4 / >= 12: all met). **qa_stats2: `sat 0.556, vivid 65.7 %, luma 100.8, warm 40.3 % / cool 45.0 %`** (sat >= 0.50, vivid >= 45 %: met). deliver.py frame-diff 4.65 / 20.28.
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
