# TAKE6 QA s03 (T03, round 4, team4) - verdict: FAIL (3 blockers, all fixable)

Checked: 49 frames at 6 fps (contact sheets 240x427), full-size frames 171/200/240/268/280/300/318-350/368-376/404-411, both dissolve joins (s02 g172-184, s06 g398-410), qa_stats2, QA_AUTO.

## Measured
- qa_stats2 (take.mkv, post-grade): sat 0.535 (>=0.50 ok), vivid 56.5 % (>=45 ok), luma 98.9 (85-110 ok), motion med 4.85 / p90 12.97, still 0.4 %. No hard cut inside (QA_AUTO: 1 shot, PASS; soft frames g174,176,357-365 = motion blur, ok).
- BIGZOOM 1: g171 Eiffel ~1 px (0.1 %, NOT findable: only a glow sphere marks the spot); ~6 % at g200; 23 % at g268 (8.84 s, "วิศวกรไอเฟล"); ~29 % g280; ~44 % (head ~180 px) g300; 35 % reached ~g288 = 9.8 s. Move lasts g171-300 = 4.3 s, ease ok, passes over roofs/scaffold (good). Faces <=35 % ok (head 180 px of 1280 ok). Ground <=25 % ok.
- Narration: Eiffel introduced 5.93 s while the frame is a Paris wide (good); but on the 8.84 s point he is only 23 % and just standing; the arm goes up g266-274 at 23-27 %, the medium (35 %+) lands ~1 s after the beat. Soft miss: bring landing ~25 frames earlier or keep the point-up gesture until g ~290.

## BLOCKERS
1. BLACK SLAB: g366-411 (worst g370-390): the platform deck underside is a pure-black polygon filling 25-35 % of the frame top (see g372, g376, also g398-411 still black top-right). Fix: give the deck underside mesh a lit/emissive-lifted material (min albedo/ambient fill ~0.25, or a warm bounce light under the platform), or raise the camera/pitch so the underside is not seen. Also a translucent white "bulb" ghost on the deck at g366-376 (hide or fix that prop).
2. WHITE BLOB bottom-left g186-206 (large white dome with black dots, ~12 % of frame, plus clipped brown thing on it): still there, reads as a broken object. Hide it (or move the camera path so it is out of frame) for g184-210.
3. Eiffel NOT findable at start (g171-185 his figure is ~1 px; only a glow ball). §H says tiny but findable. Add a clear locator: scale the glow to a ring/arrow-like marker for g171-195, or start slightly closer (target 3-4 % = ~40 px).

## Other notes (non-blocking unless fixed cheaply)
- g266-300 Eiffel's raised arm and hat overlap the orange diagonal beam (hat tip touches the beam at g285-300); busy background behind the focal character; shift the camera yaw a few degrees so the white concrete pier / sky is behind his head.
- g318-350: the swing across the yard: leg bases look cut/hovering (g334: leg foot floats above the shadow, concrete footing barely visible), the leg still bananas (curved) at g334-345; crane hook floats beside it (reads ok as crane). Acceptable but weak.
- Dark scatter props on dirt g170-250 still present (many small black/dark boxes, wheelbarrow-like prop with a black outline at g240-285 in the shot centre under Eiffel). Cosmetic; the black wheelbarrow near his feet competes with him: remove or recolour.
- Flag pole g200-230: bare white pole, no flag (flag hidden); reads as a stick through the frame. Add a visible flag or hide the pole.
- White awning (g215-300) large, blown out, takes ~15 % of frame: reduce exposure/albedo.
- Dissolve in (s02 resto -> s03 wide of Paris): ok, no hard pop, tone shift blue interior -> warm exterior but is a dissolve. Dissolve out (g398-410 -> s06 cafe): ok. Both joins clean.
- Heads: riveters at the end (g385-411) are ~100-130 px, ok.
- Eiffel reads as the red-orange scaffold; the Paris backdrop (domed hall, minarets) is OK. Colours OK. No Latin sign, no smoke (known).

## Fix list
black deck underside g366-411; white blob g186-206; findable start marker g171-195; optional: earlier landing, remove black wheelbarrow, flag/pole, awning exposure.
