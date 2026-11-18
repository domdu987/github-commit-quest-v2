# QA s15 (film 13, shot 15, g 975..1040, take g 969..1046) - reworked after director QA_TECH
- take.mkv is split (take.mkv.partaa/ab): `cat take.mkv.part* > take.mkv`.
- Staged INSIDE the cellar (under_rows): brick walls on four sides, plank ceiling, lamps, jacks on timber blocks; no sky/plain/horizon (camera-only walls + ceiling, shadow-free so the set lighting is unchanged);
  the stretched orange beam slab is hidden; filter width 2.0 against aliasing.
- Count keyed every frame, constant: 12 jacks until g 977, 100 from g 978 (narration 32.52), 1000 from g 996 (33.10), 5000 from g 1011 (33.62). Camera rises (z 5.0 -> 10.8) and pulls the look-at deeper to the end of the take.
- qa_auto: FAIL "suspected blur" on 27 frames (g 969-995): not blur (no DOF, sharp render). The low-count frames show smooth floor/brick, the dense field has very high Laplacian variance, so they fall under 60 % of the take median. Content-driven; needs a director override (second reviewer).
- Notes: workers (one per 10 jacks, neutral faces) are hidden behind the 4 D jack rods in the dense rows, only a few show; heads < 880.
