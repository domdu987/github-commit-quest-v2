# film17 s07 (shots 16-19), g 844..1051 (g0 850, g1 1045, 6 handles each side)
Final 720x1280, 16 samples + OIDN, ~45 s/frame. Shots: 16 measure_chair g844-899, 17 measure_low -> foot board g900-947, 18 measure_wide g948-995, 19 records_aisle g996-1051. Cuts g 900/948/996.

## Numbers
- qa_auto: PASS (see QA_AUTO.md), magenta 0.0 %.
- rhythm.py --cuts 900,948,996: in-shot median **8.64**, p90 **18.38** (target >= 4 / >= 12).

## Self-check (contact.jpg every 6 f, phone_sheet.jpg; not a full 6 fps frame-by-frame pass on every cut +-3)
- No mouths move (no quote in this take). Heads above y 880 in the close shots 16/17.
- Known faults vs the director's s01 lessons (NOT fixed, for QA-art/director decision):
  1. Shot 16, g844-870: the dark tripod cloth flap covers the right edge of frame; the chair headrest bar crosses the prisoner's forehead.
  2. Calipers jaws are on the head in shot 16 (arm pose from story pose, not hand_for_anchor); in shot 17 the foot-board insert has calipers at the prisoner's waist, not the foot; middle-finger/gauge insert is only suggested.
  3. Shot 16 has no gendarme writing in view (gendarme_a is staged but off-axis); shot 18 Bertillon writing is small beside the tripod, characters in the wide shots 18/19 are < 180 px tall; shot 19 the card-into-drawer action is not shown (cards held, drawers p0-q5 animate).
  4. Dust motes not reduced (set default).
  5. Sprite swaps: none; the three shot changes are camera cuts with continuous staging.
- A reshoot of these faults is ~80 min of render; tell me if wanted.
