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
