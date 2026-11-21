# QA_TECH film17 take s06 ROUND 2 (render17/team5 6fe61b4) - VERDICT: PASS (with should-fix items)

Method: 21 full-size 720x1280 frames pulled from take.mkv (g740,750,756,760,764,768,772,778,782,783,784,790,796,800,808,815,822,830,838,845,850), crops at 4x on glove (g760) and pince-nez (g815), 360x640 downscales, f6/ + phone_sheet.jpg. Numbers: qa_auto PASS, rhythm 5.38/14.12 (>=4/12 OK). Cut g783 confirmed by eye: g782 desk shot vs g783 low aisle shot, clearly different (detector miss, not a missing cut). Dissolve-in g719-729 clean.

## Claims
1. Glove: CONFIRMED. Bright cream glove ~60 px wide (was ~25 px dark ball), three clearly separated fingers (4x crop g760), still across g756-782, 55-100 px inside the frame (x~415-700 of 720). At 360x640 it is a ~28 px white hand with 3 countable fingers. Reads, but small; see S1.
2. Bent arm / turned toward Bertillon: PARTLY. Arm is bent at the elbow (upper arm out, forearm up) - fixed. But the prefect's face and body are frontal to camera (eyes at lens), not turned toward Bertillon; with palm out at hat height it reads as a wave/"hi" as much as an ultimatum. See S1.
3. Pince-nez: CONFIRMED. g815/830/845: forearm drawn in front of the cheek, dark fingertips on the right lens/bridge, temple arm visible; no hand behind head. Reads as "adjusting glasses" at phone size (g815, g830, g845 phone strip). Fingertips sit on the right lens rim next to the bridge (acceptable).
4. No zoom in shot 15: CONFIRMED. Bertillon head ~110-125 px at g790, 815, 830, 845 (no 2x pop), feet and shoes visible in all frames, no knee crop, no foreground crate covering legs (the right-side crate at g790-830 is at the aisle side, not over him), cabinets tower. Lateral sweeps only.
5. Walk-away: PARTLY. Walk cycle is real (legs spread, g784/g796), no mug-shot card on Bertillon, no chair behind Bertillon (the stool is a foreground set prop, not under him), Bertillon stands. But: the prefect's face stays frontal (not true profile, contrary to the claim), he stays glued to Bertillon's shoulder for g783-800 (overlapped, half hidden behind him at g800), then slides left to the desk (g815-838, head small at left edge) rather than clearly down the aisle, and is almost gone by g845 (only feet near Bertillon). It reads as "he goes away to the left / hides behind Bertillon", acceptable but weak. Known gap (not back to camera) accepted.

## Standard checks
- Mouths: closed on both in all viewed frames. PASS.
- See-through cards: none. Beam shafts: none seen. Dust: faint specks only at skylight (g783, g830), well under 0.5. PASS.
- Chins: Bertillon chin y~770-790, prefect ~780 (g760) to ~790 (g790), max in g725-850 under 880. PASS. Far prefect chin y 882-885 in g852-856 is outside the used range (note only).
- Blur: all frames crisp, none over 3 frames. Frozen hold: none (idle sway; glove still g756-772 is 17 frames = 0.57 s, under 1 s). Black/magenta: none (magenta 0.0 %). PASS.
- Leftover geometry: none. Lamp, books, ladder consistent across cut.

## Blocking
None.

## Should-fix
S1. g756-782 (shot 14 key beat): the glove is ~60 px at hat-brim height beside the head, palm out, face to camera: legible at 360x640 but small (~28 px) and wave-like. Better: ~90 px glove, nearer the face/chin line, hold the head turned toward Bertillon.
S2. g783-800 (shot 15): prefect overlaps Bertillon and is half hidden by him (g790, g800); leaving reads late. Separate them in screen x or have him exit toward the vanishing point; true profile/back would sell it.
S3. g838-850: prefect effectively invisible (feet only at g845); fine as exit, but the "he left" beat lands only via g815-830 left-edge head.
S4. g730-782: Bertillon's right hand holds pen plus a white spike glove tip beside it (g760, g772); odd double hand at desk level. Minor.
S5. Tools: rhythm.py reports 0 cuts and qa_auto warns "no visible change" at g783 though the cut is real; fix the detectors before the final gate.
S6. Glove and pince-nez were checked by the team only at tile size; now verified full size here.
