# T3 part QA (g645-750, 106 frames, 720x1280, 16 samples + OIDN), after the TAKE-gate fix round
Setup: render_t3.py on render17v2/T3. CHAIR_D (-0.4,0), PRIS_D (-0.15,0), apply_ramp (lights x0.4 to g750), clear_cast, TAKE_OVER['T3'] gain 1.05, plus the gate fixes below. T3b renders g751-856.

## Gate fixes in this round
1. g663->664 jump: cause was _lookrot switching the camera up vector (+y -> world-Z) when |look.z| crossed 0.995 (a 9.5 deg roll in one frame). Fixed with _lookrot_smooth (blend over g645-675). Frame diff 663->664 is now 8.2-10.4 in a smooth run (was 37.6 vs median ~6).
2. Ceiling void g726-736 + pop at g737: the camera was above the ceiling until g736. Camera z lowered by 0.85*sin^2(pi*(g-700)/45) over g700-745 (zero value and slope at both ends, g746+ untouched). The ceiling switch moved from z 5.25 to z 5.15 (below the beam bottoms; at 5.25 the camera sat inside a beam for one frame, g722, showing a slab flash). Ceiling is hidden to g723 and shown from g724, when the top ray still points down, so it enters from the top edge. g722/g723 re-rendered.
3. Gasolier through the green gendarme (gend_b): gasolier at room-local (-0.35, 1.0) raised GAS_DZ 0.6 m (pendant drop 1.45 -> 0.85). Face clear at g745 and g750 (viewed). The same constant is given to T3b.
4. Optional idle sway on the blue gendarmes: not done (director: leave out).

## Numbers
- Luma (RGB-mean, 90x160 bilinear): mean 112.9, min 107.3 (g646), max 119.6 (g734). Target 95-110: the part mean is 2.9 over; ceiling now visible in g724-750 raises it. Goes to the conform trim.
- qa_auto.py: PASS (qa_auto.txt/QA_AUTO.md). Its note "cuts 651, 850 with no visible change" is expected: g645-650 are handle frames of the same T3 shot, 850 is outside this part. magenta 0.0 %.
- rhythm.py: 0 cuts detected, in-shot median 10.01, p90 29.90.
- Motion: frame diffs run 36-47 over g715-728 (planned crane plus my z dip); the old render ran 29-36 there. The planned crane is fast; I did not slow it.
- Mouths: closed or held laugh shapes; no lip-sync in T3.

## Viewed at FULL size (720x1280) in this render
- g664: bird's-eye, clock and bookshelf, sitter (bowler hat) at the chair, Bertillon with calipers, laughing gendarmes; framing normal, no jump, no black slabs.
- g745: ceiling beams and blue ceiling across the top, no navy void; SERVICE D'IDENTIFICATION sign; prefect in the doorway; green gendarme's face is clear of the gasolier lamps (lamps to his upper left); two blue gendarmes with arms crossed in front.
## Viewed at PHONE size (360x640): strip of g645, 664, 700, 722, 730, 745, 750, and g722-725
- g645/664: figures and laughing faces read. g700: tilted high view, calendar "MARS 1882" at upper right.
- g722-725: no slab flash; the ceiling enters at the top edge at g725.
- g730/g745/g750: ceiling visible, green gendarme's face clear of the lamps.

## Not seen / not verified
- The pinned "ไอ้ช่างวัดหู" paper on Bertillon's back (optional gag): not visible in any frame I viewed.
- The "3 MOIS" calendar flip: not verified (g700 shows MARS 1882).
- OIDN shimmer: judged from stills only, not the clip.
- Sitter's card lower edge vs the armrest: not visible from the high frames; at g664 he reads as seated.
- Whether the prefect's three fingers read at phone size: not clear.
- Chair/sitter are out of frame from about g725; the g750/g751 seam has no chair.
