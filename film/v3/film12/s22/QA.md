# QA s22 (film 12, ending: shots 22-23), g 1573-1784 (212 frames; in-handle 1573-1578; no out-handle, end of film)
Render: RAIN, 20 samples, 720x1280, OIDN, ~43 s/frame (shot 22) and ~26 s/frame (shot 23) at 2 threads.
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg). It reports "no visible change" at the planned cut g 1656; I checked g 1655/1656 by eye: the cut is
  clearly visible (rank wide -> box_seat close, pink umbrella), the auto detector misses it because both shots share sky/palette.
- Shot 22 (g 1573-1655): custom linear push, camera (-2.6,0.5,1.9)->(2.4,30,3.6) to (-1,7.5,2.3)->(3.2,26,4.3), lens 22; set_rank_busy(0) (dark lanterns,
  horses hang heads, no passengers); coachmen a/b/c cards (sulk, glare, glare), no smiles. Heads px y: box_a 459->398, box_b 562->580, box_c 601->631 (all above 880).
  Deviation: box_a head centre reaches ~0.31 H at the end of the push (slightly above the 0.35 band; wide shot, exempt).
- Shot 23 (g 1656-1784): box_seat A->B linear push, set_pink_umbrella(1), pole in the card's hand (pink_to_hand), head y 568->535 (0.42 H). Gentle breathing sway on the card
  so it is never frozen. Mouth closed throughout (no quote). Last word ends g 1770; picture holds to 1784 (59.5 s) as the take range requires.
- Mouths still, no text, no magenta (0.0 %), no floating feet (cards stand on the plank z 4.22 / coach box), rain continuous.
- Known weak points (set-level, accepted by the client): flat horse faceting, faint grain in puddle reflections at the bottom of shot 22, pink canopy reads
  salmon-pink (hue guard), canopy slightly cropped at the right edge at the end of the push, the lace is partly aliased.
- Framing change: shot 22 is one 2.6 s continuous push, shot 23 one 3.8 s push per the plan (no extra cut was added).
