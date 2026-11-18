# QA-ART, FINAL gate, film 12 "ไอ้ร่มเดินได้" (release12/film12_v1.mp4, 720x1280, 30 fps, 59.5 s)
Reviewed: full2fps_01..04 (whole film at 2 fps), phone_sheet.jpg (360x640), 19 full-size frames from the key moments
(0.5 / 1.5 / 3.0 / 4.3 / 13.5 / 17.0 / 18.5 / 26.4 / 26.8 / 27.5 / 30.5 / 36.0 / 38.0 / 41.0 / 43.5 / 47.5 / 51.0 / 56.0 / 59.0 s; deleted afterwards).
Compared with: analysis/sheets bell_0, oil_0, and the approved set v3/set3d12/contact_small.jpg.

## Verdict: SHIP (no blocking issues; the 3 recommended fixes below are optional polish)

## Scores (1-10)
| criterion | score | note |
|---|---|---|
| Set density / ornament | 9 | Georgian terraces, lit sash windows, lamps, awnings, barrows, chimneys and wet setts with puddle reflections in every shot. Matches the approved contact sheet 1:1. |
| Lighting & colour | 8 | Amber windows against blue-violet rain shade throughout, depth through light, magenta 0 %. One jump: the DUSK_RAIN box shot (31.5-35 s) cuts straight to the same coachman in day RAIN light (35-37 s). |
| Composition / framing | 7 | Mostly wide and medium with the set visible, as the client wants. Two weak framings: the "pink lace umbrella" promise (15.5-19 s) is a wide three-coach shot with the speaker's head about 60 px wide; the "ten years, only one umbrella" high shot (28.6-31.5 s) does not show the one umbrella at all. |
| Character acting | 8 | Belly laugh and whip point (10-14 s), Hanway's smug calm (0-3 s), his shocked mud face then deadpan (26.4-28.5 s), the panicking rush (37-40 s), the smug dry stroll past the queue (42.5-44.5 s), the sulk under the lace umbrella (55-59 s). All read. |
| Key moments | 8 | Hook 8 (calm man under umbrella, glaring coachmen, cabbage). Mud splash 9, the best image in the film. Reveal 8 (rush for the coaches, then Hanway dry beside the queue, inside the lit 3D world). Umbrellas 8. Ending 7 (the umbrella reads as coral, not pink, and the face is small on a phone). |
| Overall match to references / client taste | 8 | Sharp, no DOF, no in-picture text, no 2D infographic. Calm camera that is always moving. New framing every 2-3 s. Flat puppets sit in the lit 3D world with contact shadows. Comic hits only, no injury. |

## Continuity across the cuts (takes from different teams)
- Light and colour: one RAIN grade from 0 to 28.6 s and from 35 to 59.5 s. DUSK_RAIN (deeper sky, heavier clouds) runs from 28.6 to 35 s, as planned. Every take matches the others. The only visible jump is the dusk-to-day cut at 35 s on the same coachman (see issue N2).
- Rain: the streak density and angle stay the same in every take, and the puddle ripples are present throughout.
- Costume:
  - Hanway keeps his tricorn, wig, dark-blue coat, cream waistcoat and black umbrella in every shot. After the splash (26.8-28.5 s) he stays mud-spotted, and the next time we see him (42.5 s) he is clean. That is fine, because it is years later.
  - The head coachman keeps his olive caped greatcoat, round hat, red nose and mutton-chops in every shot.
  - In the hook (4.3 s) a second red-nosed coachman stands in the street. He can read as the head coachman twice in one frame. This is minor.
- Props: the black umbrella stays in Hanway's hand. The cabbage (4.3 s, 22-23 s), the egg (24 s) and the coins in the coachman's hand (36 s) are all visible.
- QA_AUTO says 22 planned cuts show no change within ±2 frames, so the cuts are not at the planned frames. By eye, the picture changes fall on the caption and sentence beats, and none of them jars. This is for QA-tech to reconcile with the EDL, not an art problem.

## Captions and phone legibility
- Kanit Black, white with a dark outline, one phrase of 1-3 words at a time, centred near y 900. Every caption is legible on the 360x640 sheet. The Thai renders correctly: no tofu, and the tone marks are intact (e.g. "ข้าจะกางร่ม", "แฮนเวย์", "ลูกค้าสักคน").
- Heads stay above y 880 in every frame I checked. The closest are the rush crowd (about y 770 at 38 s) and Hanway (about y 690 at 43.5 s). Bodies and legs cross the band, which the rule allows.
- What reads on a phone: the hook, the coachman's laugh (10-15 s), the mud splash, the rush for the coaches and the sea of umbrellas.
- What reads poorly on a phone: the speaker in the 15.5-19 s wide shot, the "only one umbrella" in the 28.6-31.5 s high shot (the crowd seen from above turns into pale grey discs), and the coachman's sulky face at the end (he is small, but the lace umbrella carries the joke).

## Issues
Blocking: none.

Non-blocking, in order of value:
1. **N1, ending umbrella colour (55-59.5 s).**
   - Problem: the narration says "ร่มลูกไม้สีชมพู" (pink lace umbrella), but under the warm grade the lace reads coral or salmon.
   - Fix: shift the canopy toward a clear pink (hue about 330-340, lighter, e.g. #F48FB1) in set_pink_umbrella, then re-render or regrade only that take.
   - Optional: a slow push-in in the last 2 s, so his face is about 1.5 times larger on the hard cut.
2. **N2, the promise line is too wide (15.5-19 s, "ข้าจะกางร่มลูกไม้สีชมพูของเมียข้าเอง!").**
   - Problem: this is the setup for the ending payoff, but the speaker is a small figure in the box_trio wide shot.
   - Fix: re-cut to the box_seat push-in that the plan asks for (shot 8), or start a push-in from 17 s onto the head coachman.
3. **N3, the "only ONE umbrella" high shot (28.6-31.5 s).**
   - Problem: from above, the crowd's heads become translucent grey discs, and the single umbrella is not findable.
   - Fix: put Hanway's open black umbrella in the centre-third foreground of the street_high frame, or tilt the crane lower (about 30°) so the bare heads read as people.
4. **N4, light jump at 35.0 s.**
   - Problem: the cut goes from the dusk box shot to the same coachman in day light.
   - Fix: either keep shot 15 in DUSK_RAIN, or bridge it with the thunder cue already planned at 37.2 s. The cheapest option is to accept it, because the reveal is "whenever it rains" and not the same evening.
5. **N5, minor items.**
   - Hook (4.3 s): the second red-nosed coachman makes the mocker ambiguous. Give him no red nose, or recolour his coat.
   - Pivot (8-10.5 s): plan shot 5's "soaked gentleman wringing his wig" is missing. The shot shows a woman under an umbrella with Hanway beside her, so "ผู้ชายแท้ต้องยอมเปียก" (real men had to get wet) has no wet man in it. Fine to leave.

## Summary
The film keeps the approved set look throughout and is sharp and warm-lit. Continuity holds across the takes from different teams, and the captions are clean and well placed. N1 and N2 would raise the ending's punch the most, but neither is required for delivery.
