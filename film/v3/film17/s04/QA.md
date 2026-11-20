# film 17 take s04 round 2 (shots 9-12, g 445..650 + 6 handle frames each side, first_g 439, 218 frames)
720x1280, 12 samples + OIDN. Built on team 1's s01 machinery (pinned calipers, ears_svg, hand_svg).

## Numbers
- rhythm.py (cuts 445,493,540,592,651): **in-shot median 5.69, p90 13.18** (>= 4 / >= 12).
- qa_auto.py: PASS (QA_AUTO.md, phone_sheet.jpg), magenta 0.0 %, no blur flag.

## QA_TECH round-1 fixes
1. Prisoner (prisoner_b) stays SEATED in the measuring chair through all four shots; Bertillon's calipers are pinned on his viewer-left ear, held in Bertillon's visible hand (sliding jaw closes during shot 9).
2. Shot 9: camera right-front on the pair (figures ~400 px); inspector strides in from the right (g439-459), stops (g460-466, surprised face, finger out), THEN laughs from g467 (bounce 3 Hz); gendarmes b/a join the laugh in the background.
3. Shot 10: low two-shot, calipers on the ear in frame, Bertillon fully in frame, the inspector (mirrored pose) points his arm across AT the calipers; lips from g493.
4. Shot 11: the inspector's hand is pinned to the caliper bar (visible forearm + hand), approach g548-558, finger touches the bar g558, the bar wobbles g558-567 (caliper angle +-9 deg decaying) while Bertillon still holds it.
5. Shot 12: visible red ear on the inspector (kepi on), arm_l hand pinned on that ear, taps twice (g604-.. second half), chest puff (squash x1.05); hand drawn over the ear, never behind the head. Lips g493-650 only.
6. beam_fx shafts hidden (no translucent diagonal polygon), dust 0.5.

## Self-check (full-res g470, g510, g560, g620 + 5-frame sheet contact.jpg)
- g470: pair (Bertillon with calipers on the prisoner's ear) + laughing inspector with red ears, tears, no shaft wedge; all heads above y 880.
- g510: inspector's arm crosses to the calipers, Bertillon whole head in frame, prisoner seated.
- g560: inspector's blue forearm reaches the caliper bar at the ear (touch frame ~558); camera has just started the snap.
- g620: inspector close-up, red ear + hand at the ear, mouth open (speech), kepi top at y ~ 70.
- Known: the tapping hand is a small blue cuff blob at the ear (reads at phone size, finger detail lost); the ears are large cartoon ears (team-1 style); shot 11 end frames (g585-591) the inspector sits near the right edge (face fully visible).
