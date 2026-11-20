# film 17 take s04 round 2 (shots 9-12, g 445..650 + 6 handle frames each side, first_g 439, 218 frames)
720x1280, 12 samples + OIDN. Built on team 1's s01 machinery (pinned calipers, ears_svg, hand_svg).

## Numbers
- rhythm.py (cuts 445,493,540,592,651): **in-shot median 5.70, p90 13.33** (>= 4 / >= 12).
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

## Round 3 (QA_TECH_R2 blockers) -- full-res self-check, sheet selfcheck_R3.jpg (g445, 468, 520, 505, 560, 564, 615, 630)
- B1 stray rods: they were thin cream faces of a set prop hovering at z~1.02 above the small table (plus the table's steel calipers). Both deleted at runtime (cut_table_calipers). g445, g468, g520: no floating rods; the only calipers are the pair in Bertillon's hand.
- B2 ear tap: pin converged (err 0.0 all frames); the earlier failure was the hand drawn UNDER the red ear and the akimbo fist at the belt mistaken for the tapping glove. Now the glove (skin circle, 1.5x) is drawn in front of the ear (g615, g630: hand ON the ear, mouth open and clear), taps every 9 frames from g604 (+-0.05 D), chest puff x1.05, camera 0.1 m wider at the end of the push (chin well above y 850).
- Shot 10 g505: the pointing forearm now ends at ear height on the calipers (not the hat).
- Shot 11 g560/g564: arm on the bar; bar wobble g558-567 (+-9 deg decaying) is small but visible in the sprite.
- Shot 9: surprised stop-and-look g460-466, laugh from g467.

## Round 4 (QA_TECH_R3: ear tap) -- shot 12 re-rendered (g592-656), phone-size check selfcheck_R4.jpg (g610, 620, 630, 645)
- The tapping arm is now a big visible blue sleeve rising from the chest, a white glove (>= 55 px) and an extended index finger whose tip is ON the lower rim of the red ear, drawn in front of it; taps 3x (+-0.05 D, ~15 px, period 11 f) g606-640, then holds to the end. The glove sits below the ear, mouth clear.
- The fist at the belt is gone (both puppet arms are 'behind' during the tap; only the drawn arm is visible). Chest puff: torso squash x1.09 eased from g592 (visible as a wider torso vs g592).
- Camera/chin unchanged from R3 (chin well above y 850).
- Shots 9-11 unchanged from R3 (optional point/wobble tweaks not made).
