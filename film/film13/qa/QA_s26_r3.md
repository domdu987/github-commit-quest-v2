# QA s26 round 3 (film 13, TAKE gate, combined QA-art + QA-tech) - PASS
Take: film/v3/film13/s26 (321 frames, g 1674-1994, 720x1280 30 fps), shots 26-30, the ENDING. Take files untouched.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13s26r3/
(QA_AUTO.md, phone_sheet.jpg, sheet6a/b.jpg = 6 fps, cuts.jpg = every cut +-3, full/<g>.png + p1-p5.jpg pairs, join.jpg).

## Auto / tech
- qa_auto PASS: no frozen/black/magenta. Its "no visible change" on 1743/1775/1871/1909 is the known handle/first_g quirk:
  own frame-diff scan shows the hard cuts exactly at g 1743 (68), 1775 (63), 1871 (59), 1909 (45); no other spikes.
  Steady diffs 8-13 (shots 26-28 crane/dolly) and 21-34 (shot 29 fall + camera follow) are motion, not pops.
- End: hard cut at g 1994 (frame 321). Handle-in 6 frames are shot 26, fine.
- Heads fully above y 880 in every checked frame (rich in pit: head bottom ~y 800; Pullman ~y 470-700; fall: head above line until
  he is in the pit at g 1898, head ~y 690-800). Mouths: closed in every frame (dash / wavy stunned mouth, no open O) - rule met.
- No DOF/blur, puddle reflections gone, sky blue with clouds, mud sharp.

## Beat checks
1. Shot 26 (g 1674-1742): rich in the doorway from frame 0, top hat, CANE with gold knob in his left hand - OK. Cribbing, jackscrews and
   the void under the portico fill the lower third; front-stair framing reads.
2. Shot 27 (g 1743-1774): close on the portico edge over the lit void, cane planted, sweat drop, closed worried mouth. From ~g 1749 the
   lids drop and the eyes go down; head barely tilts, so the "look down" is soft but readable with the void directly below in frame. OK.
3. Shot 28 (g 1775-1870): side-on/3-quarter wide along the facade, crane-in; the short detached stair (bottom right / centre) stops well
   below the portico with cribbing + void between: the ~2 m drop reads. He stays on the portico edge (continuity with 27). OK.
4. Shot 29 (g 1871-1908): step off, hat off, head-first tumble past the base, lands IN the mud pit to the waist with a dark-brown spiky
   spray crown + mud flecks on coat (no round blobs), dizzy stars, no injury. Comic, readable. OK.
5. Shot 30 (g 1909-1994): purse first in HIS raised (stick) arm beside him (g ~1917-1950), Pullman walks in, takes it (~g 1969) and
   holds it up at shoulder height; rich lowers arm, sulking muddy face, hat on head. Pay-off reads on the phone sheet. OK.
6. Light/continuity: team used DAY (warm low key, lit windows, blue sky with warm clouds). Same preset as s01/s23-24 street; reads as
   a warm morning. Accept (no fix). Lift state 1.0 consistent with s24.
7. Join s25 -> s26: delivered s25 is the older open-pit (sky) version; golden jack field -> hotel portico hard cut, warm palette matches,
   no continuity break. Re-check roughly once the cellar s25 re-render lands (only colour temperature to compare).

## Non-blocking (polish only, do not hold the take)
- g 1775-1800: a thin black diagonal line (cable/pole) hangs from the top frame edge into the sky right of the hotel and leaves as the
  camera cranes; reads like a stray line. Remove/identify if a re-render happens anyway.
- Mud-pit rim is a flat brown oval disc (reads a bit like a manhole) in shot 30.
- Shot 30 starts at nearly the same angle as the end of shot 29 (g 1906 -> 1909): mild jump-cut feel; acceptable as a reaction cut.
- Rich's purse arm is a single stick line with no hand; fine at phone size.
- Shot 28 rich head ~20 px on phone at the start, ~35-40 px after crane-in (accepted in r2).

## Verdict: PASS - no blocking fixes. Ready for conform.
