# s04 QA_TECH: FAIL
Shot 4, SHIP ship_rocks STORM_DUSK, take g182-270 (handles 9+9; in side DIS 13), 6 fps + cuts g191/g262 +-3 checked. qa_auto PASS. No text, no black/magenta, no frozen run, no pop, no blur. Frame-diff re-measured median 6.88, p90 13.16: OK. Mouth fixed: OK. Chart has tick marks only, no text: OK. Heads inside 450-760 band (small and centered).
## Issues
1. g247-261: the captain is clipped by the left frame edge (hat brim, shoulder and cape cut at x=0; at g257-261 more than a third of the head is out). The shot ends on a cropped head. Fix: slide the camera so the push ends centred on him (ease the slide to 0 over the snap), or stop the slide at g229.
2. g182-261: eye-line/action: plan says he "peers into fog over a blank chart". He stands mid-deck facing the lens with a grumpy stare and holds the chart out sideways at hip height; eyes never go to the chart or the fog (the g214-230 "glance" is not visible), not at the rail. Fix: turn the body 3/4 toward the rail, head tilted up into the fog on "กลางทะเล", chart held in both hands in front of him.
3. g182-261: the hand-held chart hangs in the air at arm's length with a straight arm; hand/prop attach reads weak. Fix: bend the elbow and bring the chart to chest height with the fingers on the card edge.
4. g202-217: lantern swings fully out of frame (absent for ~16 frames), so the planned FG lantern vanishes mid-shot; g261 it is clipped at the right edge. Fix: shorten the swing amplitude/offset the lantern 0.3 D toward centre so it stays in the frame.
5. g182-207: dark trapezoid slab at the bottom of frame (y > 1150) reads as a black blob. Fix: light it or remove it.
6. meta.json g1 = 262 is exclusive (plan g1 = 261). Note only.

## Round 3: FAIL
Checked 6 fps + cuts g262 +-3 (take g182-270), qa_auto PASS. No text, no black/magenta, no frozen, no blur. Mouth fixed. Heads in band. Frame-diff (take.mkv, g192-261): median 6.68, p90 12.80: OK.
Earlier issues: R1-1 captain clipped at left edge: FIXED (inside, hat brim x>=60 at g255-270). R1-5 dark slab: now a small dark corner at bottom-left g182-207, NOTE. R1-2 NOT FIXED, R1-3 NOT FIXED, R1-4 PARTLY.
1. g182-261 (R1-2, planned beat "peers into fog over a blank chart"): he still faces the lens with a grumpy stare, body square to camera; eyes never go to the chart or fog; the chart now shows coast lines and a red compass rose, not blank. Fix: turn the body 3/4 to the rail, head up into the fog on "กลางทะเล", chart blank (ticks only) held at chest height.
2. g182-261 (R1-3): chart is held at arm's length, arm straight, horizontal at hip/chest side; attach reads weak. Fix: bend the elbow, fingers on the card edge, chart in front of the body.
3. g205-217 (R1-4): FG lantern swings to the right frame edge and is ~70 % cut at g205-210 and still clipped at g215-217 (and g261-270 at the edge). Fix: shorten the swing / move its mark 0.3 D toward centre so it stays fully inside.

## Round 4: FAIL
Checked 6 fps + cut g262 (take g182-270), qa_auto PASS, frame-diff g192-261 median 6.33 / p90 11.84 OK. No text, black/magenta, frozen, blur; mouth fixed; heads in band. Take unchanged in substance since round 3.
Earlier issues: R3-1 NOT FIXED, R3-2 NOT FIXED, R3-3 NOT FIXED.
1. g182-261 (R3-1, planned beat "peers into fog over a blank chart"): he still faces the lens, grumpy stare, body square to camera; eyes never go to the chart or fog; the chart shows coast lines and a red compass rose (not blank). Fix: turn body 3/4 to the rail, head up into the fog on "กลางทะเล", chart blank (ticks only).
2. g182-261 (R3-2): chart still held out sideways at arm's length, straight arm. Fix: bend the elbow, chart at chest height in front of the body, fingers on its edge.
3. g200-217 and g257-270 (R3-3): FG lantern still swings to the right frame edge and is cut ~half at g200-212 and at the end. Fix: shorten the swing / mark 0.3 D toward centre.
