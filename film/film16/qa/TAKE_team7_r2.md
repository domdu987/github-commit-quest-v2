# TAKE gate round 2: QA-tech + QA-art, film 16, render team 7 (s01, s22, s23, s24)
Source: render16/team7 @9c6a0a6 (HEAD "film16 s24 v2"; re-checked just before s23 review, s23 not re-pushed yet, so the s23 below is the current one with p90 10.6).
Method: every take decoded at full res; 6 fps sheets plus every cut +-3 (full size and enlarged crops); qa_auto.py re-run (--cuts from meta, --first_g); frame-diff recomputed myself (90x160 bilinear, grey = mean RGB, in-shot pairs only); 360x640 phone sheets read. Round-1 refs: film/film16/qa/TAKE_team7.md (tech) and TAKE_ART.md (art).

| take | qa_auto | frame-diff median / p90 (mine) | team's figure | verdict |
|---|---|---|---|---|
| s01 hook | PASS | 9.11 / 13.81 | 9.12 / 13.85 | PASS (notes) |
| s22 glass answer | PASS | 4.64 / 12.39 (28 of 73 pairs < 4) | 4.64 / 12.4 | PASS (notes) |
| s23 callback | PASS | 6.88 / **10.62** | 6.88 / 10.64 | **FIX** (blocking) |
| s24 reveal | PASS | 4.11 / 12.52 (27 of 74 pairs < 4) | 4.10 / 12.47 | PASS (notes) |

qa_auto's "planned cut with no visible change" notes (s01 g69, s22 g1455, s23 g1455/1540, s24 g1540/1615) are false alarms: the handles render the same shot past the cut, so nothing changes there inside the take. No blur, black, frozen or magenta frames in any take. No DOF, no in-picture text. Heads are always above y 880 (lowest head bottom about 720). Mouths stay still.

---

## s01 hook: PASS (notes)
Round-1 (ART, s01 was not in the round-1 tech file):
- ART-1 bottle merges with the head: **FIXED** for g 0-64. The bottle stands against clean sky to the left of the head. **Regresses slightly** at g 65-68: the head drifts in front of the bottle body's right edge. The bottle is still readable.
- ART-2 the bottle reads as a beer bottle: **FIXED.** The glass is solid green with a clear neck, shoulder and body, mouth down, with a glint and no grain. It reads on the phone sheet as a green bottle.
- ART-3 wire visibly dropped onto the glass: **PARTLY.** No wire is seen dropping on the glass or bouncing. In g 58-64 the wire is a straight dark bar going up out of the top of the frame, above his head. At g 65 a grey wrap ring pops on in one frame and the wire then sticks into the bottle top like a straw. The "drape" is only 4 frames (65-68) before the cut.
- First second: **FIXED.** Ground, fence, trees and ladder fill the lower half, and the bottle is visible above the pole at g 0.
NOTES
1. g 54-56: the forearm crosses his mouth/chin while he reaches for the wire. g 58-68: the raised hand sits on his forehead, which reads like a salute or brow wipe and holds nothing visible. (In the handle, g 69-71, the hand is over his face. That is cut away, but keep it in mind for trims.)
2. g 65 wrap ring and wire spans pop on in a single frame. Ease it in (wire falls 3-4 frames, then the ring appears).
3. The held copy (g 30-46) is a lighter cyan-teal than the set glass after contact (g 47+). The shift is small but visible at full size.
Story beat on the phone: the strange act reads (a man holds an inverted green bottle on the pole top, then is proud). "Drapes the wire over it" reads weakly.

## s22 "the answer is glass": PASS (notes)
Round-1 tech:
- T1 frame-diff below target: **FIXED** (4.64 / 12.39). The tail g 1440-1454 is still a near-static drift (2.6-3.5).
- T2 feet hidden behind the board: **PARTLY.** From g 1397 the camera is higher and the bed and shadows are visible. In g 1372-1392 the lower ~45 % of the frame is still the flat orange side board, with only faint plank lines, and Morse is cut at the knees behind it.
- T3 eye-line: **OPEN (minor).** Eyes are open in g 1383-1411, but the pupils sit low, as a sideways smug look, not up at the bottle above his head. Closed smile arcs from 1412.
- T4 sun disc: not added; the flares carry it. Accepted.
- T5 continuity / heads / mouth: OK.
Round-1 ART:
- Orange wall: **PARTLY** (as T2).
- Bottle cropped at the right edge: **FIXED.**
- Look up at the glint: **OPEN** (as T3).
NOTES
1. Hair is cut by the left frame edge at g 1400-1417 (snap peak). The face stays in frame.
2. Prop continuity: the s22 bottle is a tall, dark, champagne-like bottle, while s01/s23 cap the pole with a light teal, wide-bodied bottle. A viewer may not link "this glass" to "that bottle". Match the glass material and silhouette, or at least the hue.
Story beat on the phone: reads instantly. He raises a green bottle, it flares, he smiles.

## s23 callback: FIX
Round-1 tech:
- T1 drape beat not legible, fist over the face, wire bar across the face: **OPEN.**
  - g 1508-1511: the hand is at his mouth and the wire is a thick dark diagonal bar crossing his face (exactly the v1 frame).
  - g 1514-1521: the hand is on his forehead.
  - g 1526: the forearm crosses his mouth again.
  - The QA.md claim "hand drops to his side instead of crossing his face" is not true for this take.
- T2 noisy mint blob: **FIXED.** Solid green glass, a readable inverted neck, faint grain only at 1511.
- T3 expression turns happy late: **FIXED.** Happy from g 1499.
- T5/T6: OK.
Round-1 ART:
- Bottle merges with the head: **FIXED to g 1525, then OPEN g 1526-1539.** The camera drift brings his head in front of the bottle, and in the final 0.5 s (the frames before the cut to the reveal) only the top third of the glass is visible above his hat.
- Wire on the glass: **PARTLY** (as s01). The wire is a straight bar, the ring pops on at g 1521 in one frame, and no drop or bounce is visible.
- Pinkish salmon pole, should be dark and wet: **PARTLY.** It is now a mauve/copper brown, darker than s01 but clearly lighter than the s24 pole it cuts to, and it has no sheen or drips. The pole colour jumps on the cut to s24.
BLOCKING
1. Frame-diff p90 10.62 < 12 (median 6.88 OK). The team knows this; a fix push is pending. Re-measure on the new push.
2. g 1505-1539: the hand crosses or covers the face (1508-1511, 1526) and the head covers the bottle (1526-1539). The callback's payoff beat ("now with the reason": glass capped and wire draped) is hidden in the last second. Keep his head right of the glass to the cut (stop the arc/slide drift, or slide the camera left), and keep the free hand below chin height when he takes the wire.
NOTES
3. Pole colour: match s24's dark purple-brown and add a wet specular streak, so the cut 1539 to 1540 shows the same pole.
4. Ease the g 1521 wrap-ring pop (as s01 note 2).

## s24 reveal: PASS (notes)
Round-1 tech:
- T1 no dark pole, no non-leak contrast: **FIXED.** The dark pole is in frame from g 1541 to the end. The glass top and neck glow cyan at g 1553-1560 while the pole directly below stays dark. The contrast reads at full size and on the phone sheet (g 1561 tile).
- T2 blur flag: **FIXED** (qa_auto PASS, no Laplacian dips).
- T3 truthful QA_AUTO: **FIXED** (it matches my run).
- T4 flat cut wire stub: **FIXED.** The wire runs over the rim and on to the right.
- T5 static end: **PARTLY.** Slow orbit; diff about 3.8-4.0 in g 1592-1614. It is not parked, but it is a 0.75 s visual hold with nothing happening.
- T6: OK.
Round-1 ART:
- ART-1 wet dark pole + weak spark dying at the rim: **PARTLY.** The pole is dark and slightly glossy, but there are no drips, no puddle and no wet look. The ground is a dry, sunny wheat field (wetness lowered to 0.15). The spark is "not done", as the team states.
- ART-2 light only the neck, then the pulse carries on: **FIXED.** The comet passes through the glass and runs on along the outgoing wire to the right (out of frame about g 1586).
- ART-3 sky <= 40 %: **OPEN.** The horizon sits at about 75-80 % of frame height in g 1546-1614, so sky plus hills is about 70 % of the frame, not "<= 40 %" as QA.md claims. The set is sparse (field, rail, two trees). Density is still low.
NOTES
1. The glass glows for only about 7 frames (1553-1560). On the phone it shows in just one 0.5 s sample. Hold the neck glow 10-12 frames, or add a second smaller pulse.
2. "Wet" is not readable: add a specular streak down the pole plus 2-3 drips, and a dark puddle at the foot, or keep the ground wet beyond 0.15 with the sun glare handled by the camera angle.
3. Frame lower or tilt down so that the ground, the next poles with bottles, and the puddles fill more of the frame (the client's dense-set rule).
Story beat on the phone: the pulse runs along the wire, lights the glass, carries on, and the pole below stays dark. It reads; "wet" does not.

---

## The 3 most valuable fixes
1. **s23 (blocking):** fix the last second of the callback. Keep his head off the glass in g 1526-1539, keep the free hand below chin level (no fist or forearm over his face at 1508-1511/1526), and let the wire visibly fall onto the glass and bounce before the ring appears. Then lift p90 to >= 12 with a stronger push or slide on the drape. Apply the same hand/drape staging to s01 (g 54-68) so the rhyme holds.
2. **s24:** make the reveal read as "wet, yet no leak". Use a wet pole sheen with drips and a puddle, and hold the neck glow 10-12 frames (or add a tiny spark that dies at the rim). Lower the horizon so the sky is about 40 % and add the next capped poles for density.
3. **Prop and colour continuity across s22, s23, s24 and s01:** use one bottle (same green and silhouette in s22's hand as on the pole in s01/s23), and one pole colour (s23's pole as dark as s24's).
