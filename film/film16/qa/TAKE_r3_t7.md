# TAKE gate round 3: QA-tech + QA-art, film 16, render team 7 (s01 hook, s23 callback)
Source: render16/team7 @0415be5 ("film16 s23 + s01 round 2: free hand below the chin, wire falls and bounces on the glass, head clear of the glass, darker pole").
Method: each take decoded at full res (one at a time, deleted after). Sheets at 6 fps, plus every cut +-3, plus every frame of the drape beat, with enlarged crops of the glass and the face. qa_auto.py re-run (--cuts from meta, --first_g). Frame-diff recomputed by me (90x160 bilinear, grey = mean RGB, in-shot pairs only). 360x640 phone sheets read. Neighbour frames: s22 g1453-1454, s24 g1540-1543.
Sheets: qa16/r3t7/*.jpg (s01_6fps, s01_drape, s01_top, s01_face, s01_phone, s23_6fps, s23_drape, s23_top, s23_phone, cuts, pole).

| take | qa_auto | frame-diff median / p90 (mine) | team's figure | verdict |
|---|---|---|---|---|
| s01 hook | PASS | 7.67 / 16.79 (68 pairs, min 5.77) | 7.67 / 16.8 | **PASS (notes)** |
| s23 callback | PASS | 6.11 / **12.03** (84 pairs, min 4.07) | 6.12 / 12.04 | **PASS (notes)**: p90 clears 12 by only 0.03 |

qa_auto's "planned cut with no visible change" notes (s01 g69; s23 g1455/1540) are false alarms: the handles render the same shot past the cut. No blur, black, frozen or magenta frames. No DOF, no in-picture text. Heads stay well above y 880 (meta head bottom max 831 / 855; visually far higher). Mouths are still (a fixed closed smile from the blink on).

QA.md hygiene: s23/QA.md gives two different frame-diff results ("Round 2": 6.12 / 12.04; old "v3" section below it: 7.18 / 12.73), and s01/QA.md still carries the old 9.12 / 13.85 section. The true figures are 6.12 / 12.04 and 7.67 / 16.8. Delete the stale sections. Both QA.md files also claim "falls onto the glass and bounces twice". That claim is not true (see below).

---

## s01 hook: PASS (notes)
Round-2 items:
- ART-3 wire visibly dropped onto the glass: **OPEN.**
  - g 57: the wire is a thick dark bar from the right whose end touches his cheek.
  - g 58: the wire swings up diagonally behind his head.
  - g 59-68: it is a straight, rigid rod rising from the top of the glass out of the top of the frame, like an antenna or a straw. It does not sag or come down on either side, and no fall or bounce shows in the enlarged crops.
  - g 67: the grey wrap ring pops on in one frame.
  - Compare s24, where the wire passes over the glass and sags on both sides. That is what "draped" looks like.
- Hand on forehead (note 1): **FIXED.** From g 59 the hand holds the coil at chest height. **Remaining:** the forearm rises to chin level at g 55-58 and covers his mouth at g 58 (one frame). The wire end touches his cheek at g 57.
- Ring pop (note 2): **OPEN** (g 67, one frame).
- Held copy colour vs set glass (note 3): **OPEN.** At g 30-46 the held bottle is a pale cyan/blue. At contact (g 47+) it turns deep green. This is clear on the phone sheet (g 30 and g 45 vs g 60).
- Head vs bottle at g 65-68: **FIXED.** His head stays right of the glass to the cut, and the whole bottle body stands against the sky.

NOTES
1. Make the drape real: the wire should come down over the glass and hang on both sides (as in s24), with a visible fall and settle over 3-4 frames, before the ring. Then ease the ring in.
2. Match the held bottle's hue to the set glass (the same deep green from g 0).
3. The g 52 pose swap (on the blink) jumps the arm from the bottle to the chest in one frame (diff spike 17.1). It is hidden by the blink only partly. Consider a 2-3 frame blend.
4. A fixed 4-point star glint sits on the glass every frame from g 50 to the end. It reads like a sticker. Let it travel or fade.

Phone read: an old man on a ladder holds an inverted green bottle on the pole top, then smiles proudly. That reads at once and is the strange hook. "Drapes the wire over it" reads only as "a wire sticks up out of the glass".

## s23 callback: PASS (notes)
Round-2 items:
- BLOCKING 1, p90 10.62 < 12: **FIXED, at the limit.** p90 is 12.03, so any retime or trim of this take can drop it below 12. Re-measure after any change. A slightly stronger end truck (g 1522-1536 peaks at 12.8) would give margin.
- BLOCKING 2a, hand at mouth / fist over face: **MOSTLY FIXED.** There is no fist on the face and no hand on the forehead. From g 1512 the hand holds the coil at chest height. **Remaining:** the forearm crosses at chin/mouth level at g 1509-1511 (3 frames), and the wire bar's end touches his brow at g 1509. This is too short to read on the phone, so it is now a note.
- BLOCKING 2b, head covering the bottle (g 1526-1539): **FIXED.** The whole glass body is visible against the sky to the cut. Only the hat brim touches the neck collar (g 1503-1523 and g 1534-1539), which is harmless.
- Pole colour / wet (note 3): **PARTLY.** The pole is darker and has a vertical specular streak. It is still a red-brown, about 1.6x brighter than the s24 pole at the cut (sampled mean RGB about 98/60/90 vs 62/39/61). There are no drips. The ground is dry wheat and the sky is the same sunny sky as s01 with a lilac grade, so "after rain" does not read.
- Ring pop (note 4): **OPEN** (g 1524, one frame).
- Wire drape: **OPEN** (as s01). It is a rigid rod straight up from the glass, with no fall or bounce. QA.md says otherwise.
- Cut out to s24 (g 1539 to 1540): OK as a cut. The bottle stays green and the pulse runs along the wire, but the wire direction changes from straight up (s23) to horizontal over the glass (s24). That is acceptable with the new angle.
- Cut in from s22 (g 1454 to 1455): OK. Prop note carried from round 2: s22's bottle is the tall dark champagne-like bottle, which differs from the pole glass.

NOTES
1. Drape and ring: the same as s01 notes 1. This matters more here, because the callback's payoff is "wire draped over the glass".
2. Pole: multiply it down to about s24's value (about 0.6x of now), and push it toward purple-brown. Add 2-3 drips and a wet sheen, plus some wet or dark ground patches, so AFTER_RAIN reads.
3. Remove the 3 forearm-at-chin frames (1509-1511) and keep the wire end off his face at 1508-1509.
4. Held copy hue (pale cyan at 1485) vs set glass (green): the same fix as s01 note 2.

Phone read: the same man, the same pole, the same green bottle, the same smile. The callback is instantly recognisable. "Wet dark pole" does not read: it looks like a sunny pole with a brown-red tint.

## Rhyme s01 / s23
**Strong.** They have the same opening wide (ladder, pole, bottle at the left of his head, fence and wheat below), the same snap on the same word, the same contact, blink and smile, and the same final close with the glass top-left and his head right. Frames at matching offsets are near-identical, so the viewer will clearly see "this again". The difference that should carry the meaning (wet dark pole after rain) is too weak. It now reads as a colour-grade change only.

## The 3 most valuable fixes (none blocking)
1. A real drape in both takes: the wire falls over the glass, sags on both sides and settles, then the ring eases in. Correct the QA.md claims.
2. s23 wet pole: match s24's darkness and add drips and wet ground, so the rhyme carries the "after rain" difference. Re-measure p90 (it is at 12.03 now).
3. Hold the bottle in one hue (deep green) from the first frame in both takes, and kill the static glint sticker.
