# T3 part QA (g645-750, 106 frames, 720x1280, 16 samples + OIDN)
Setup: render_t3.py on render17v2/T3 (CHAIR_D (-0.4,0), PRIS_D (-0.15,0), apply_ramp lights x0.4 to g750, clear_cast, TAKE_OVER['T3'] gain 1.05). T3b renders g751-856 from the same script.

## Numbers
- Luma (RGB-mean, 90x160 bilinear): mean 110.9, min 94.5 (g736), max 117.5 (g709). Target 95-110: the part mean is 0.9 over; the director said overage goes to the conform trim.
- g740 clip check: no white blow-out (all channels >=250 on 0.000% of warm wall pixels; G>=250 on 0.14%). R is 255 on 65.9% of warm wall pixels (saturated orange, accepted by the director).
- qa_auto.py: PASS (qa_auto.txt). It notes "planned cuts 651, 850 with no visible change": expected, 645-650 are handle frames of the same T3 shot and 850 is outside this part. magenta 0.0 %.
- rhythm.py: 0 cuts detected, in-shot median 11.37, p90 27.14.
- Mouths: all closed or held laugh shapes (no quote window in T3). No lip-sync used.

## Frames viewed at FULL size (720x1280) and at phone size (360x640, phone6 strip of g645/672/700/730/740/750)
- g645 full: bird's-eye over the measuring room. Clock, bookshelf, chair with the sitter (bowler hat, brown coat) at centre, Bertillon (glasses, beard) pointing calipers at right, laughing gendarme above him. Three laughing gendarmes lower left and one lower centre appear upside down (cards seen from directly above). No black slabs. Phone size: the faces and the chair read.
- g672 full: same view, camera lower. Sitter reads as seated, head over the backrest; chair armrest is in front of his lower body and does not cut the card. I could not see the card's lower edge from this angle. Laughing faces (tears) readable.
- g700 full: bird's-eye tilted, "MARS 1882" calendar at upper right, sitter and chair upper left, Bertillon with calipers, laughing gendarmes lower left with closed eyes. Phone size: figures small but readable.
- g730 full: eye-level, door and prefect (top hat, sash) in the doorway, two gendarmes front with arms crossed, a gendarme behind, gasolier crossing the left foreground. The wall is orange-ochre, not clipped. The ceiling in the upper part is a flat dark navy block (the cutaway) for this frame.
- g740 / g750 full: camera near eye height under the beams, "SERVICE D'IDENTIFICATION" sign whole at g750, prefect raising a hand in the door. At phone size I can not tell whether he shows three fingers.
- Gasolier globes are blown-out white blobs in g730-750 (emitters, expected).

## Not seen / not verified
- The pinned "ไอ้ช่างวัดหู" paper on Bertillon's back (optional gag): not visible in any frame I viewed.
- The calendar flip to "3 MOIS": not verified (g700 shows MARS 1882).
- OIDN shimmer on flat walls: not judged. I viewed stills only, not the clip.
- Chair/sitter are out of frame from about g725, so the g750/g751 seam has no chair to match.
- The sitter's card lower edge vs the armrest: not visible from the bird's-eye frames.
