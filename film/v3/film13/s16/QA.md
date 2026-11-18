# QA s16 (film 13, shot 16, g 1041..1106, take g 1035..1112)
- qa_auto: PASS (78 frames, no frozen/black/magenta/blur flags). Camera dollies forward along the aisle every frame.
- ~520 worker cards (3 per aisle slot, A/B bar poses cycling every 20-60 frames, hidden when chin y > 862), pullman walks the central aisle toward the camera
  (walk cycle, head turns, scale 0.78 so his head clears the 2.8 D crawlspace beams), foreman with whistle at the far end (tiny).
- Set fix at runtime: the oil lamps' 2.6 D halos washed out actors in the aisle, so 'cellar_lamps' is hidden and rebuilt without halos (lights unchanged).
- Notes: pullman's charcoal coat is dark against the shadowed aisle; the near workers at the frame edges are large (head ~80-120 px) but above y 880;
  a pale light cone from the vent at the lower left of the first frames comes from the set.
