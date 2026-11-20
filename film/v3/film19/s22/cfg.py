"""take numbers for deliver.py (s10 = shot 10)"""
TAKE, SHOT = "s22", 22
G0, G1, H_IN, H_OUT = 1756, 1856, 9, 10          # shot 10 = g 773..861 (25.78-28.74 s); handles g 764..772 and g 862..871
CUTS = []                                       # no cut inside the take (DIS 11 in, DIS 15 out)
TRANS_IN = {"type": "dissolve", "frames": 11, "note": "DIS 11 from shot 21 (ship_coast); 9 handle frames g 1747..1755 rendered in 3D"}
TRANS_OUT = {"type": "dissolve", "frames": 15, "note": "DIS 15 into shot 23 (hall_door EVENING); 10 handle frames g 1856..1865"}
SET = "v3/set3d19/h19.py HALL preset hall_table, light DAY; set_candles(1.0) every frame; set_moneybag(half) from g 1770 (bag pivot slid across the baize, scale 0.8: smaller and slack), set_box none/open/closed with the lid keyed by hand (closed from g 1820), box moved to metres (0.2, 1.65), three own round red wax discs (r 0.062 m) dropped and pressed (z squash) onto the lid at g 1821/1826/1831; the set's ribbon sealed state is NOT used; actors lifted 0.05 D so the contact decal shows above the carpet; no caption_shade"
CAST = "harrison19 default, expr sad, standing at the left side of the table; astro19 (smug, mirrored) at the right side: pushes the half bag across the baize with his hand (g 1768-1796), then holds the H4 over the open box and lowers it in (prop h4_watch g 1798-1814), ends smug with the sealed box; all mouths fixed (no quote in this shot)"
CAMERA = "custom 22 mm from the door end (0,-3.9,2.4) looking along the table; c19.CamPath push 8 %/s + slide -12 px/s + crane 15 + arc 2 deg/s, plus a small handheld sway (0.065 D at 2.6 Hz, 0.05 D at 3.4 Hz; added to lift the frame-diff of this calm wide); SNAP x1.7 (peak 1.7, 19 f) g 1818..1837 onto the sealed box + astro19 on 'ขัง' (caption 60.60 = g 1821)"
EV = dict(bag_slide=[1770, 1796], box_open=1798, h4_in=[1807, 1814], lid_close=[1814, 1820], seals=[1821, 1826, 1831], snap=[1818, 1837])
CUES = [
    (1747, 1866, "ambience", "Board room, afternoon: room tone, candle hiss"),
    (1770, 1796, "foley", "cloth money bag scraping across the baize, a few coins clink"),
    (1798, 1806, "foley", "box lid creak open"),
    (1807, 1814, "foley", "the H4 watch set into velvet: a soft tick, then silence"),
    (1814, 1820, "foley", "lid shut: wooden thud"),
    (1821, 1832, "accent", "three wax seals stamped: thump, thump, thump on the beat of ขัง"),
    (1818, 1834, "accent", "snap push whoosh"),
    (1856, 1856, "cut", "dissolve (15 f) to shot 23, hall evening")]
