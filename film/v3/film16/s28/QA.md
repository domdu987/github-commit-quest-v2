# s28 QA: film 16, shot 28 (CHAMBER chamber_low, DAY)
## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps, 40.6 MB): first_g 1796, 108 frames (g 1796..1903). Shot 28 = g 1805..1894 (60.18-63.17 s); 9 handle frames each side in 3D. Transition in: **dissolve 15 f** from shot 27 (centred on g 1805; the 9 handle frames before it are in the take).
- 720x1280, 6 spp, 2 threads x 2 processes: **8.52 s/frame wall, 16.59 s CPU**. QA_AUTO.md PASS.
## Shot
| g | beat |
|---|---|
| 1805-1873 | "two years later": the mocker as Postmaster, sash, mail bag on the hip, key ring on the belt, hand on hip, chest out, standing at his front-row desk; low camera (1.3 D below his face), push 8 %/s + slide 85 px/s + 11 deg/s arc round him; a mail sack in the lens at the very start (g 1796-1820) |
| 1868-1883 | **SNAP** x1.8 / 15 f with a 0.9 D pan on "ไปรษณีย์ใหญ่" (g 1874) |
| 1875 | pose swap on a blink to **mocker_pm_keys**: dangling the key ring (visible in the lower right) |
| 1884-1894 | close: head 310 px, smug smile |
## Checks
- Mouths: nobody speaks (smile mouths only). No text, no DOF.
- Heads: mocker 186 -> 310 px, centre y 585-615, bottom <= 749 (< 880).
- Contact: he stands behind the front-row desk (the desk hides the legs; the grey leg seen beside the desk in g 1803-1825 is his own leg).
## Frame-diff (90x160 grey, pairs g 1805..1894)
median **6.28**, p90 **16.45** (targets >= 4 / >= 12). First tuning (slide 40, arc 6, snap x1.5) gave 3.35 / 11.0; the final 85 px/s + 11 deg/s + x1.8 passes.
## Differs from the plan / notes
- **Mail sacks:** set_mailsacks(on) is keyed on, but with the camera heading rotated 18 deg round him (to keep the oversize sacks off the lens) only the first ~1.5 s shows them; later frames show the desk, sash and keys. The plan says "sacks of letters around him": this is not fully met.
- The desk's near edge (walnut) fills the lower third; the "foreground prop 1-2 D" is that desk and the sack, not the inkwell.
- Camera is not exactly the preset pose: it is orbited round the mocker for the sack clearance.

---
# Revision 2 (after the director's TAKE gate) -- re-rendered, take.mkv replaced
Frame-diff now median 6.70 / p90 15.42; 108 frames, 8.9 s/frame; heads 159-304 px, lowest head bottom y 832 (< 880).
- **Gate 1 (sacks): fixed.** The camera is orbited -38 deg (from +18) and pulled back (4.9 D, 1.0 D below the face): a sack stands beside him in the frame for g 1796-1870 (two at g 1800, one large at g 1830-1860), then the snap closes on his face and the key ring. The opening head is 157-165 px (medium) instead of the 190-ish before.
- The low desk still hides his legs for part of the shot (low angle by design).

---
# Revision 3 (after the director's FINAL gate) -- re-rendered, take.mkv replaced (41.4 MB)
Frame-diff median 6.51 / p90 13.94; 108 frames, 8.9 s/frame; heads 173-337 px, lowest head bottom y 841 (< 880). QA_AUTO PASS. Same frame range (g 1805..1894) and the 15 f dissolve-in.
- **The set's closed burlap sacks are off** (`set_mailsacks(False)`): they hid his body and read as the money bag.
- **Two OPEN sacks spilling blank white envelopes** (own geometry: sack, dark mouth, 15 envelopes each with a V flap drawn as two thin lines, some standing in the opening, the rest spilled over the lip) stand on the two desks beside his, in the left and right thirds of the frame, low, never across his torso. No red blob, no text.
- **Pose:** `mocker_pm_keys` from the first frame with the right hand raised beside his head (hand (0.80, 0.10)): the key ring is held UP, the sash and the mail bag are fully visible from the first frame.
- **Camera:** eye level (0.3 D under his face, 4.6 D away) instead of the low camera, so the desk no longer hides him: medium head 173-180 px from g 1805 to 1870 (medium by 61.5 s = g 1845 as asked), then the snap on "ไปรษณีย์ใหญ่" to a 337 px close.
- The sack on the right drifts out of frame as the camera pushes in; at the close only the sash, keys and face remain.
