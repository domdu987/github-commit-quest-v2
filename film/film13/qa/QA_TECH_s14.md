# QA_TECH s14 (film 13, TAKE gate) - FAIL

Checked: qa_auto every frame (plan cuts passed), 6 fps + every cut +-3 frames, full-size key frames, join with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13/s14/ (sheet_*.jpg, full/<g>.jpg). Take files untouched.

Global note G1 (all takes): delivered cuts sit at round(t*30) of the plan table, i.e. 3 frames (0.10 s) EARLIER than the plan's g = round((t+0.10)*30) (e.g. shot 3 at 108 vs 111, shot 11 at 650 vs 653, shot 17 at 1107 vs 1110, s26 cuts 1740/1772/1868/1906 vs 1743/1775/1871/1909). qa_auto reports every planned cut as 'no visible change' or as a pop 3 frames off for that reason. Fix: conform must cut at the plan g (handles cover it) or the take must be re-keyed +3 frames; in-shot cues (e.g. nickname jump g895, splash g1893) are not consistently offset either.

Auto: PASS (no frozen/pop/blur). Plan cut 915 'no change' (G1: shot starts 912).
1. g 906-980 (shot 14, plan street_wide 'workers file in carrying iron jacks down into the trench under the hotel'): the Tremont House is not in frame at all. A different small brick shop with a striped awning fills the top 45 %, the trench belongs to it. Fix: street_wide with the hotel visible and the trench at its base.
2. g 906-980: only 3-4 workers, they stand/shuffle on the spot beside a short ramp, one walks the plank down; no 'file' of men. Count drops 4 -> 3 at g ~915-926 (a worker vanishes behind the doorway pillar, another enters from left at g 926 clipped at the frame edge). Fix: 8-12 workers in a continuous line, each with a jack on shoulder.
3. g 906-980: bottom 45 % (y > 700) is an empty smooth mud plane with a few tiny puddles - dead composition, soft-looking. Fix: crop/tilt or fill with fill piles, carts, planks.
4. g 906-980: worker feet: stilt legs on the plank without shadow contact for the left worker (g 951-980 foot just at ramp edge, shadow detached). Minor.
5. Frames at g 975-980 (handle) match end of shot 14; join to s15: outdoor trench -> s15 open rectangular pit on a bare plain with no building: location continuity break.
Heads all < 880 (head y 560-700). No mouth flapping (grimace faces only). No text.
