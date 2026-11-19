# Film 16 "ไอ้บ้าลวด" — FINAL gate, QA-art (opus)

Checked: film16_v1b.mp4 (captions burned in), final/f_001..071 at full res (720x1280), final/sheet2fps_phone.jpg (2 fps, 360x640), plus extra 4 fps strips I extracted
at 11.5-13.5 s (shot 6), 14.6-16 s (shot 7), 24.6-26.2 s (shot 11), 43-45 s (rain), 58.9-60.3 s (shot 27). All my working files are in scratchpad/c16/qaart/.
Compared with: analysis/sheets (rail_0 etc.) and release10/zebra_v2.mp4, sampled every 6 s.

## Verdict: FIX-FIRST (one blocking item, a re-render of shot 28 only)

## Scores
| Area | Full res | Phone 360x640 | Notes |
|---|---|---|---|
| Set density / ornament | 7 | 7 | The chamber (columns, crimson drapes, tiered desks, chandelier, globe, inkwells) and the studio (easel, busts, canvases, framed oval portrait) are dense and on-style. LINE is thinner than the film 10 harbour (open fields, simple fences) but has enough FG grass, crates, ladder and wheels. |
| Lighting & colour | 8 | 8 | Warm low sun with blue-violet cloud shade, a good DUSK shift for the false payoff (31-41 s), a cool RAIN palette (42-46 s), and an AFTER_RAIN golden return. The night ending has warm lamp pools and dark windows. Sky-shade hue is on target. |
| Composition / framing | 7 | 6 | Mostly readable medium shots with FG parallax. Weak spots: shot 28 is blocked by sacks (BLOCKER), a big tape-roll log covers the bottom left in shot 26 (57.5-58.8), and Morse is small at the right of the wide chamber in shot 8 (16-18 s). |
| Character acting | 8 | 8 | Mocker laugh tears and blush, chest thumb and finger up (18-23 s); Morse's shocked eyes, then the palette drops and he sinks (12.5-13.3); snap to Morse's hurt face on "ไอ้บ้าลวด" (25.5); jaw drop at 58; horror and sweat at 65; yawn and Z's at the end. |
| Key moments | 7 | 6 | Hook 9 (a glinting green bottle neck on the pole, Morse proud, train behind). False payoff 8 (silent key, an in-3D cut-away of the split pipe with blue leaks, an empty bag, the mocker laughing in the buggy). Crisis 8 (sparks crawl down the wet pole into puddles). Reveal 7 (the pulse crosses the glass and the pole stays dark; small on phone but readable). Aha 8 (the platform waves, then the train arrives late). Ending setup 4 (shot 28, see BLOCKER). Ending 8 (lone mocker yawning, tape piling, Morse peeking in at the door). |
| Overall match to refs / client taste | 7.5 | 7 | Matches film 10's toy-3D look: sharp, no DOF, no flat 2D diagrams, no in-picture text (blank station sign, dots and dashes only on the tape). The camera is always moving. |

## Checklist
- Captions are Kanit-style, one phrase at a time, at y about 900, white with a dark outline, and readable on the phone sheet. No caption covers a face or head; heads stay above y 880 throughout, including the mocker closes at 19-23 s and 65-69 s and the workers at 45 s.
- Thai text: every caption I read matches script_th.txt word for word (sampled across all 10 sentences). Exact spelling is QA-tech/audio's job (D2).
- No flat 2D diagrams: the trench cut-away (33.6-35.8) and the reveal macro (51.3-53.8) are inside the lit 3D world.
- Sharp: there is no DOF. The soft frames qa_auto flagged (g 167-170, 401-404, 474-476, 955-958) all sit on dissolves or snaps, so they are acceptable.
- Continuity: Morse wears the blue coat and fur cap on the LINE and the paint-spotted smock with younger hair in the STUDIO. The mocker wears a top hat and plaid vest, plus the green sash from 60 s on. The money bag is full in shot 12 and empty in shot 17. Time of day runs DAY, DUSK, RAIN, AFTER_RAIN, DAY, NIGHT as planned.
- Camera: every sampled 4 fps strip shows movement, and the snaps land on the beats (25.5, 15.4, 57.7).

## BLOCKING
1. **Shot 28, 60.2-63.2 s ("สองปีต่อมา ผู้แทนคนนั้นได้เป็นนายไปรษณีย์ใหญ่").** This shot sets up the ending joke, but on the phone sheet the mocker is hidden behind 2-3 huge formless burlap sacks.
   - At 60.5-62.5 a sack fills the lower 2/3 of the frame and covers his sash, body and keys. Only his face shows over the sack at y 450-500, and in f_062 the sack's red blob sits where his chest should be.
   - The sacks have no letters, envelopes or stamps. They read as the same money bag from shot 12, so a viewer may take this as "he got money", not "he became Postmaster General".
   - The sash and keys only become readable at 62.6, about 0.5 s before the cut.

   **Fix (re-render shot 28 only, same camera path):**
   - Move the mail sacks out to the left and right thirds and below y 1000. The FG sack must stay under 1/3 of the frame height and never cross the mocker's torso.
   - Open the tops of 2 sacks and spill white envelopes (blank, no text) over the floor and desk.
   - Drop the red tag, or make it a small wax seal on an envelope.
   - Give the mocker a proud chest-out pose, holding the big key ring up at shoulder height, with his sash fully visible from 60.4 s.
   - Keep the 7 %/s push, but end on a medium shot, head 200-230 px, by 61.5 s.

   After the re-render: re-conform, re-run qa_auto, and re-check 60-63.2 on the phone sheet.

## Non-blocking notes (raise the score, not required)
- Shot 26 (57.5-58.9): the foreground tape spool reads as a yellow wooden log and covers the bottom-left third. Shrink it about 30 % or move it lower and right, so the dots-and-dashes tape and the mocker's jaw drop own the frame.
- Shot 22 into shot 23 (46-51 s): the bottles in the crate are dark bottle-green, but the neck on the pole is bright turquoise, as in the hook. Tint the crate bottles toward the turquoise, or make the lifted bottle turquoise, so "this bottle becomes that insulator" reads.
- Shot 7 (15.0-15.8): the blue spark between the coil and the magnet is not visible on the phone sheet. Make it larger and brighter, or use the allowed one white flash.
- Shot 8 (15.9-18.0): Morse is small (about 60 px head) at the screen-left edge, and the empty desk dominates. Slide the camera so Morse sits nearer the centre third.
- Shot 24 reveal (51.3-53.8): the pulse glow is small on the phone. Bump the pulse size and bloom about 1.5x as it parks in the glass.
- Shot 30 (66-69.8): Morse peeking at the door is small (about 40 px head on phone). A slightly brighter door rim or a 2-frame eye glint on him would land "Morse grins" faster.
- LINE set density sits a notch below film 10's harbour. For future LINE shots, add more FG clutter (wire spools, barrels, tool crates).
