"""take numbers for deliver.py (s10 = shot 10)"""
TAKE, SHOT = "s10", 10
G0, G1, H_IN, H_OUT = 773, 862, 9, 10          # shot 10 = g 773..861 (25.78-28.74 s); handles g 764..772 and g 862..871
CUTS = [773]                                    # planned cut inside the take: the hard cut in from shot 9 at g 773 (first_g = 764: handle before it)
TRANS_IN = {"type": "cut", "frames": 0, "at": 773, "note": "hard cut from shot 9 (hall_low) at g 773; 9 handle frames g 764..772 rendered in 3D"}
TRANS_OUT = {"type": "dissolve", "frames": 15, "note": "DIS 15 into shot 11 (WORKSHOP shop_wide); 10 handle frames g 862..871"}
SET = "v3/set3d19/h19.py HALL preset hall_wide, light DAY; set_candles(1.0) every frame; no runtime set changes; no caption_shade"
CAST = "v3/cast19: astro19 (the mocker), astro19_b, astro19_c, astro19_b again (far right) laughing (STORY19 *_laugh poses via cast19.laugh_cycle, 3 bounces/s, bounce 0.06 D at 3 Hz, tears, alternate pointing fingers), mirrored to face the aisle; harrison19 default (greying hair, apron) standing sad with the tricorne held (prop tricorn_held), expr sad (fixed mouth); nobody speaks; Board stands at x +-2.3 D behind the chairs (not at the marks: the narrow 22 mm lens cannot hold x +-3.5 at this distance)"
CAMERA = "custom 22 mm at the door end (0.8,-6.0,3.8) looking up the hall at Harrison (0.15,0.8) with the Board beyond; c19.CamPath drift push 10 %/s + slide -60 px/s + crane 30 px/s + arc -16 deg/s about Harrison, decay 0.05; SNAP x2.85 (peak 1.6, shift 1.9/-1.1) g 843..856 on the caption 'ไอ้ช่างไม้' (28.10 s = g 846) onto his face; still moving at the dissolve handle"
EV = dict(snap=[843, 856], word_nickname_caption=846, laugh="3 Hz bounce 0.06 D all frames", doors_hidden="hdoorleaf_* set objects hidden (camera passes the open door leaves)")
CUES = [
    (764, 872, "ambience", "Board room, afternoon: low room tone, candle hiss, a far clock tick"),
    (773, 846, "voice", "the Board's belly laughs (no words), chairs creak, wigs bounce - one burst, rolling"),
    (843, 856, "accent", "snap push on 'ไอ้ช่างไม้': short airy whoosh"),
    (850, 861, "foley", "the laughter fades under his sad silence; a tricorne brim rustle"),
    (862, 862, "cut", "dissolve (15 f) to shot 11, the workshop")]
