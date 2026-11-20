# s10 TAKE-gate QA (film 15, shots 10-16, g489-931 + handles 483-939, team 3)

**Verdict: FAIL.** The technical checks pass and the flop and flash beats read. Two plan beats do not read at all: shot 11 (neck-grab and pointing at Dick) and shot 14 (the big photo of the arched jumper). Shot 16's peg raise is also not legible. Items 1-3 are blocking.

Take: origin/render15/team3 film/v3/film15/s10 (take.mkv rebuilt from 4 parts, 457 frames, 720x1280, 30 fps).
Checked at 6 fps (every 5th frame) plus every cut ±3 (489, 564, 621, 708, 762, 838, 862, 932), at full size and on a 360x640 phone sheet.

## Automatic checks
- qa_auto (`--first_g 483 --cuts 564,621,708,762,838,862`): **PASS**. Magenta 0 %. It reports "no visible change within ±2" at g564, 621, 762 and 838. I looked at those cuts and they are visible: the shot changes between the Shot 10, 11, 12, 14 and 15 frames. This is a false alarm from similar palettes.
- motion_check: median **5.4**, p90 **13.1** (target 4 / 12). **PASS**. Per-shot medians from the team's QA.md are 2.9 for shot 10 and 2.5 for shot 13. Both still move (bounce, sway, orbit). No frozen run longer than 1 s.

## Checklist
| check | result |
|---|---|
| Heads above y 880 | OK. The lowest head is Dick's on the shot 16 DAY landing (about y 800-860, g918-926), just under the line. Nobody else is close. |
| Grounded cards, scale, nobody frozen | Mostly OK. Shot 11: Dick stands on a dark plank and looks like a tiny figure on a platform, with a hard-edged flat green patch under the coach. Shot 14: boy1's head floats above the newspaper "body". |
| No text | OK. The newspaper has grey bars and a grey photo box only. |
| Sawdust only | OK. Pit and mound are sawdust in shots 13 and 16. |
| FG prop at an edge | OK. Shot 10: board and clipboard (left). Shot 11: red box. Shot 12: bar standard and yellow stopwatch. Shot 13: bench (lower right). Shot 15: fence. |
| Coach mouth only in 17.80-23.55 s (g537-710) | **OK.** In shot 10 the mouth is hidden by a closed-eye laugh (g489-534). It opens at g537 and closes by g710. Shot 15 (g838-861) is still. |
| Laugh bounce about 3 Hz | OK. Shot 10 coach and boys bob (visible vertical offset every few frames). Shot 15 boys bob. |
| Bar does not fall | OK. |

## Plan coverage and phone-size read
| shot | beat | reads on the phone? |
|---|---|---|
| 10 (g489-563) | coach laughs with belly bounce | **YES.** Sunset set, laughing coach and two boys, push-in, mouth starts at g537. Good. |
| 11 (g564-620) | over the shoulder, neck-grab mime, pointing at Dick | **NO.** The coach stands facing the lens with his arms folded on his chest and an "o" face. There is no neck grab and no point. Dick is tiny and far, the boys are tiny. Nothing says "broken neck". |
| 12 (g621-707) | finger wag, jab, PUSH! at "ดูเอง" | **YES.** The coach scratches his neck or head at first, then jabs his chest and wags a finger. The push is visible g686-707. The stopwatch is in frame. |
| 13 (g708-761) | photographer FLASH as Dick arches | **YES, small.** The flash bursts at g741 with Dick arched over the bar. Dick is only about 12 % of the height. The arch reads, but the face is tiny. |
| 14 (g762-837) | insert: big photo of the arched jumper | **NO.** The newspaper is a small card under a big boy1 head. The "photo" is a small grey square with one thin arc. It does not read as a fish-like arched Dick. |
| 15 (g838-861) | everyone points and laughs, PUSH! | **Partly.** The boys' arms are out and they laugh with tears. A push-in on the right boy is visible. The coach points but looks stern, not laughing. |
| 16 (g862-931) | training montage, peg raised, GOLDEN to DAY dissolve | Flops: YES. The dissolve: YES (g897-907 is a clean blend, with a ghost Dick). The peg raise: **NO**. The boy is off frame (only a sliver of blonde at g862). |

## Fixes
1. **Shot 11 (g564-620), blocking.** The mime is missing.
   - Re-pose the coach: right hand on his own neck (head tilted, tongue out) for g575-595, then arm out pointing at Dick. Use the over-shoulder framing from the plan: the coach's shoulder is the FG edge prop and the camera looks past him at Dick.
   - Turn the coach's face and eye-line toward Dick, not the lens.
   - Pull Dick, standing on the ground (feet on sawdust or grass, not on the plank), and the laughing boys into the frame at 15-20 % of the frame height each.
   - Remove the flat green patch under the coach.
2. **Shot 14 (g762-837), blocking.** The photo does not read.
   - Make the newspaper at least 60 % of the frame width, held up by the reader.
   - The photo box is the largest block on the page (at least a third of the paper height).
   - Put a clearly arched jumper in the photo: a ∩ body with a head hanging below the bar, red/yellow shirt, tan bar. Use the actual arched Dick card, or a render of the g741 flash frame.
   - Show the reader's hands and thumb, not a floating head. Keep grey bars for the text.
3. **Shot 16 (g862-896), blocking.** The raised peg is not legible.
   - Show the boy at the standard (in frame, centre or left) putting the bar peg up one notch after each flop. Run bar_raise slowly enough to see (the take's cue is g886-896).
   - Keep the standard and the bar in frame so the viewer sees the bar get higher.
   - Check that the DAY-plate bar sits visibly higher than the GOLDEN-plate bar relative to the standard (currently the DAY plate has no standard in frame).
4. **Shot 15 (g838-861).** Make the coach laugh: eyes squeezed, tears, a bounce at 3 Hz, mouth still shut (the quote window has ended). He currently looks angry.
5. **Shot 13 (g733-753), minor.** Dick is small. Push the camera in 20-25 % (arch at least 25 % of the frame width) so the head and legs hanging below the bar read on the phone. The flash itself is good.
6. **Shot 14, minor.** The seated spectator at the right edge is cropped to a sliver. Keep him fully in frame or remove him.
7. **qa_auto note, non-blocking.** Four planned cuts (g564, 621, 762, 838) are flagged as no-visible-change although they are real cuts. If the rerender changes these shots, re-check the cut frames.

Re-check after the rerender: shots 11, 14, 15 and 16 on the phone sheet. A viewer should see (a) the coach mime a broken neck and point at Dick, (b) a newspaper with an arched jumper in the photo, (c) the bar going up between flops.

---
## Re-check r2 (render15/team3 @ a6c02b4, rebuilt in scratch takes/s10r2)

**Verdict: PASS, with notes.** Shot 14 now reads clearly. Shot 11 reads as "the coach turns and points at Dick", but the neck mime is marginal. In shot 16 the season-change dissolve and the repeated flops read. The peg raise is weak but present. Nothing here clearly hurts the film.

### Automatic checks
- qa_auto: PASS. Only g621 is flagged as no visible change within ±2.
- motion_check: median 5.4, p90 12.1 (target 4 / 12). PASS, only just on p90.

### Your two questions
- **Cuts g489 and g621.**
  - g621: the cut is **real and clearly visible** (shot 11 is the coach pointing on a green field; shot 12 is a coach against the bleachers). The qa_auto flag is a false alarm. The cause: the coach is a large, similar-coloured card in both frames, and the smooth transition frames are close.
  - g489: this is not a cut inside this take. The take begins at g483 with handle frames of shot 10, so there is nothing to see, and the first cut in the file is g564. This matches meta.json (cut-in at g489 is the take's boundary).
- **Near-static runs in shots 10 and 16.** Neither is near-static on screen. The weakest 15-frame (0.5 s) windows still change a lot (shot 10 min 8.3 on a 0-255 scale, median 18; shot 16 min 21, median 25), and there are no frame-diff runs under 1.0 anywhere. Shot 10 has a visible push-in, and the coach and boys bob. Shot 16 has a long camera move plus the flops, spray and dissolve. The low per-shot medians come from the wide framing, not from stillness.

### Fixes 1-6 from the first review
| # | status | evidence |
|---|---|---|
| 1 shot 11 mime | **partly done, marginal** | g564-596: the coach is at the right of the frame, small and 3/4 turned, mouth an "o", hands up at his chest or collar. On a 360x640 phone it reads as "shocked", not as a clear broken-neck mime (head tilt and hand on the neck are tiny). g606-620: he turns and points with a straight arm at Dick, with an eye-line on Dick. That reads well. Dick is on the grass with the boys beside him, but small (about 10 % of the frame height, not the 15-20 % asked for). The flat green patch is gone. |
| 2 shot 14 photo | **done** | The newspaper is about 70 % of the frame width with a large framed photo of the upside-down arched Dick (head below a tan bar) and grey bars for text. At phone size you can see "a photo of the flop". The reader's face and thumbs are at its edge. The seated spectator is removed. A little static: the push is slow, but each 15-frame window is still above 20. |
| 3 shot 16 peg raise | **weak** | The blond boy now stands in frame at the left standard (good), and the bar visibly rises over g886-906 relative to the pole, and again on the DAY plate. But the boy never moves a hand to the peg (his eyes stay closed, and his pose is static), and the rise is about 35 px on 720, so it is easy to miss on a phone. Dick is small (about 10 % of the frame). The flops, the spray and the GOLDEN to DAY dissolve all read. |
| 4 shot 15 coach laughs | **done** | At g838-861 the coach squeezes his eyes shut and bounces with the boys, mouth shut. The boys point and laugh. Fence at the left edge as FG. |
| 5 shot 13 push-in | **done** | The push-in gives a larger arch at g741, with the flash at the right moment. The arch is clear over the bar. |
| 6 shot 14 spectator | **done** | The seated spectator is gone. |

### Checks that still pass
Heads above y 880 (the lowest is Dick at the shot 16 landing, about y 860). No text anywhere. Sawdust only. The coach's mouth moves only g537-710 (it was closed in shot 10 before g537 and in shot 15). The bounce is about 3 Hz. The bar does not fall.

### Leftover notes (non-blocking; fix if there is a cheap re-render)
1. **Shot 11, g564-596:** make the neck mime bigger. Push the camera in so the coach is the left-of-centre FG card, tilt his head about 30 degrees, and put both hands on his own throat with his tongue out. Keep the point at g606.
2. **Shot 16, g884-906:** animate the boy's hand to the peg (an arm up and a lift) and open his eyes, so the raise reads without the pole. A push-in on the bar and standard at g884-906 would also help.
3. **Shot 11 and 16:** Dick is small in both. Push in about 20 % on his marks if time allows.
4. **qa_auto note:** the cut detector misses g621 and can't see g489 as a cut. This is false-alarm noise, not a defect in the take.
