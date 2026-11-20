# s04 QA_TECH: FAIL
Shot 4, SHIP ship_rocks STORM_DUSK, take g182-270 (handles 9+9; in side DIS 13), 6 fps + cuts g191/g262 +-3 checked. qa_auto PASS. No text, no black/magenta, no frozen run, no pop, no blur. Frame-diff re-measured median 6.88, p90 13.16: OK. Mouth fixed: OK. Chart has tick marks only, no text: OK. Heads inside 450-760 band (small and centered).
## Issues
1. g247-261: the captain is clipped by the left frame edge (hat brim, shoulder and cape cut at x=0; at g257-261 more than a third of the head is out). The shot ends on a cropped head. Fix: slide the camera so the push ends centred on him (ease the slide to 0 over the snap), or stop the slide at g229.
2. g182-261: eye-line/action: plan says he "peers into fog over a blank chart". He stands mid-deck facing the lens with a grumpy stare and holds the chart out sideways at hip height; eyes never go to the chart or the fog (the g214-230 "glance" is not visible), not at the rail. Fix: turn the body 3/4 toward the rail, head tilted up into the fog on "กลางทะเล", chart held in both hands in front of him.
3. g182-261: the hand-held chart hangs in the air at arm's length with a straight arm; hand/prop attach reads weak. Fix: bend the elbow and bring the chart to chest height with the fingers on the card edge.
4. g202-217: lantern swings fully out of frame (absent for ~16 frames), so the planned FG lantern vanishes mid-shot; g261 it is clipped at the right edge. Fix: shorten the swing amplitude/offset the lantern 0.3 D toward centre so it stays in the frame.
5. g182-207: dark trapezoid slab at the bottom of frame (y > 1150) reads as a black blob. Fix: light it or remove it.
6. meta.json g1 = 262 is exclusive (plan g1 = 261). Note only.
