# s24 TAKE-gate QA (film 15, shot 24 crisis, g1269-1328 + handles 1263-1268 / 1329-1334), QA-tech + QA-art

**Verdict: PASS.**
- Dick stands alone at his mark under the dark TENSE floods, rocking on his toes, with a set, determined frown. The camera closes in on him.
- It reads as "the stadium holds its breath before attempt 3".
- The notes below are non-blocking.

Take: origin/render15/team4 @ 317b004, film/v3/film15/s24. take.mkv: 72 frames, 720x1280, 30 fps, TENSE, cut in and out.

Frames checked:
- 6 fps (every 5th g) plus the cut ±3 (1266-1272) and the out-handle, at full size.
- A 360x640 phone sheet.

## Automatic checks
- qa_auto (`--first_g 1263 --cuts 1269,1329`): **PASS.**
  - "No visible change" at g1269 and g1329: these are handle boundaries, and the handles continue the same move.
  - Magenta 0 %. No black, frozen or soft frames.
- motion_check (`--first_g 1263 --cuts 1269,1329`): median **5.2**, p90 **12.4** (target 4 / 12). **PASS.** No hold is longer than 1 s.

## QA-tech checklist
| check | result |
|---|---|
| Heads above y 880 | OK. Dick's head is at y ~630-780 and his chin at y <= 850 in every frame. |
| No text | OK |
| Grounded, scale, not frozen | OK. Contact shadow under his feet. Rock and sway tween smoothly, with no pops. |
| Mouths still | OK. Dick holds a static frown line. Nobody else is close enough to read. |
| Hushed, but the crowd breathes | OK, partly verified. The crowd is dimmed under TENSE floods. The camera moves the whole time, so I could not isolate the crowd bob from the frames; the render log sets hush mode (0.006 m, 0.4 Hz). |
| Slow push + slide | **The move is stronger than the plan.** A short whip in (g1269-1275), then two quick pushes (about 26 % at g1281 and 24 % at g1297-1308) on top of a dolly with a lateral slide. The plan asked for a slow 6 %/s push. On the phone it reads as tension building, not as noise. See note 1. |
| Kit vs shot 22 | OK. White top with a red/blue band, navy tights, brown spiky hair. `dick_olympic` is used, but no medal is visible: only the thin V collar, the same as in s17/s21. |
| Bar vs shot 22 | **No bar in frame.** The standard behind Dick (g1269-1295) and the near pole (g1290-1328) carry no bar, and the plan's "bar end" foreground is absent. Nothing contradicts shot 22: there the bar was knocked down, and it is reset off-screen. See note 2. |
| Join 23 -> 24 (s21 g1268 -> g1269) | OK. A cut from the coach close-up to Dick wide at his mark. The EVE -> TENSE light change is planned. Kit matches. |
| Join 24 -> 25 | Not checked: s25 is another team's take. |

## QA-art (phone, 360x640)
- **Clarity 7/10, beauty 6/10.**
- **What works:**
  - The dark blue sky, the floodlights and the hushed crowd under the spot.
  - The push into Dick's set face.
- **What is weaker:**
  - The shot is low in contrast. The track and the crowd are close in value, so Dick's white top carries the frame alone.
  - The two quick pushes are a little loud for a "hush".

## Notes (non-blocking)
1. **Pushes:** soften the two quick pushes to about 12-15 % each, or ease them over 0.6 s instead of 0.3-0.5 s, so the hush feels held. Motion stays above target with the dolly and slide.
2. **Bar:** put the reset bar on the far standards (about g1269-1295), or use the plan's bar-end foreground at a frame edge. This gives the hush its object (the bar he must clear) and keeps continuity with the red/white bar of shots 20-22.
3. **Contrast:** a little warm rim or spot on Dick (or darker stands behind him) would separate him from the background on the phone.
4. **g1325-1334:** a purple-orange blotch in the sky at the top left. Check whether it is a flood flare or a dome artefact.
