"""take numbers for deliver.py (s10 = shot 10)"""
TAKE, SHOT = "s10", 10
G0, G1, H_IN, H_OUT = 773, 862, 9, 10          # shot 10 = g 773..861 (25.78-28.74 s); handles g 764..772 and g 862..871
CUTS = [773]                                    # planned cut inside the take: the hard cut in from shot 9 at g 773 (first_g = 764: handle before it)
TRANS_IN = {"type": "cut", "frames": 0, "at": 773, "note": "hard cut from shot 9 (hall_low) at g 773; 9 handle frames g 764..772 rendered in 3D"}
TRANS_OUT = {"type": "dissolve", "frames": 15, "note": "DIS 15 into shot 11 (WORKSHOP shop_wide); 10 handle frames g 862..871"}
SET = "v3/set3d19/h19.py HALL preset hall_wide, light DAY; set_candles(1.0) every frame; no runtime set changes (door leaves visible, they frame Harrison); no caption_shade"
CAST = "v3/cast19: astro19 (right of the aisle), astro19_b and astro19_c (both left, separated in depth and screen x) laughing (*_laugh poses via cast19.laugh_cycle, 3 Hz bounce 0.06 D, tears), each pointing at Harrison in turn (arms alternate every 9 frames); harrison19 at the door (0,-5.0), hands clasped (harrison_hopeful_door pose, no hat), expr sad; nobody speaks; three Board members only (the fourth, a second astro19_b, was removed in round 2: it stacked on astro19_c)"
CAMERA = "custom 22 mm from the window end (0,9.4,3.6) looking down the hall at the door; c19.CamPath push 3 %/s (low: the Board stays in frame until the snap), plus a small handheld sway (0.065 D at 2.6 Hz, 0.05 D at 3.4 Hz, translation only); SNAP x3.0 (peak 3.0, steep ease, shift 0.0/0.7, 14 f) g 836..850, whip peak about g 843, on the caption 'ไอ้ช่างไม้' (28.10 s = g 846) onto Harrison in the doorway; the Board leaves as a motion-blurred smear in 1-2 frames (Cycles camera motion blur, shutter 0.9, on g 835..852 only)"
EV = dict(snap=[843, 857], word_nickname_caption=846, laugh="3 Hz bounce 0.06 D all frames", pointing="alternating arm every 9 frames")
CUES = [
    (764, 872, "ambience", "Board room, afternoon: low room tone, candle hiss, a far clock tick"),
    (773, 846, "voice", "the Board's belly laughs (no words), chairs creak, wigs bounce - one burst, rolling"),
    (843, 856, "accent", "snap push on 'ไอ้ช่างไม้': short airy whoosh"),
    (850, 861, "foley", "the laughter fades under his sad silence; a tricorne brim rustle"),
    (862, 862, "cut", "dissolve (15 f) to shot 11, the workshop")]
