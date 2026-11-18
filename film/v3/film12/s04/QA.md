# QA s04 revision 2 (shots 4-5, g 166-321; cut at g 240; 720x1280, 24 samples)
Director gate fixes applied:
- Shot 4: custom lower, closer crane (z 13.5 -> 10.5): 18 crowd cards (hunched, soaked, hats held over heads; 2 women under small umbrellas) + Hanway, all readable; the crowd stays in frame to the end; set puddles only. Heads above y 880 (card heads checked per frame).
- Shot 5: the soaked gentleman wrings his wig with ANIMATED arms (7-stage hand/drip cycle + body wobble); the dry lady walks past under her umbrella; the extra walker was removed so no sprites cross; Hanway stays inside the frame; the jeerer holds a closed mouth.
- Mouths closed everywhere (mouth='flat'); no leaf anywhere; same RAIN light and sky as s01.
- qa_auto PASS (cut-note is a tool quirk).
- Known weaknesses: crowd figures are small from the crane; lower half of the aerial road is cobbles and puddles.

## Revision 3 (shot 5 only, g240-321 re-rendered at 28 samples)
- The yellow-coat man is now a hunched walk-cycle card (crowd_man_d_walk_hat, mouth closed) far down the left pavement; no laughing/shouting face anywhere in shot 5.
- Hanway moved left (x -3.5) and stays fully inside the frame on every frame; lady, gentleman and Hanway no longer overlap. qa_auto PASS.
