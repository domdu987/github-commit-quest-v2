"""take numbers for deliver.py (s10 = shot 10)"""
TAKE, SHOT = "s22", 22
G0, G1, H_IN, H_OUT = 1756, 1856, 9, 10          # shot 10 = g 773..861 (25.78-28.74 s); handles g 764..772 and g 862..871
CUTS = []                                       # no cut inside the take (DIS 11 in, DIS 15 out)
TRANS_IN = {"type": "dissolve", "frames": 11, "note": "DIS 11 from shot 21 (ship_coast); 9 handle frames g 1747..1755 rendered in 3D"}
TRANS_OUT = {"type": "dissolve", "frames": 15, "note": "DIS 15 into shot 23 (hall_door EVENING); 10 handle frames g 1856..1865"}
SET = "v3/set3d19/h19.py HALL preset hall_table, light DAY; set_candles(1.0) every frame; set_moneybag(half) from g 1770 (bag pivot slid across the baize), set_box none/open/closed/sealed with the lid keyed by hand and three own wax seals dropped one by one g 1821/1825/1829; the box moved to metres (0.5, 2.05); door leaves hidden not needed; no caption_shade"
CAST = "harrison19 default, expr sad, standing at the table end (right of frame); astro19_b (smirk, mirrored) pushes the bag then holds the H4 over the open box and lowers it in (prop h4_watch g 1798..1814); astro19 smug in the far background; all mouths fixed (no quote in this shot)"
CAMERA = "custom 22 mm from (-1.0,-3.9,3.3) looking at the box; c19.CamPath push 10 %/s + crane 35 px/s + arc -9 deg/s about the box, decay 0.1; SNAP x2.6 (peak 1.5, 16 f) g 1818..1834 on the seals (caption 60.60 = g 1821)"
EV = dict(bag_slide=[1770, 1796], box_open=1798, h4_in=[1807, 1814], lid_close=[1814, 1820], seals=[1821, 1825, 1829], sealed=1833, snap=[1818, 1834])
CUES = [
    (1747, 1866, "ambience", "Board room, afternoon: room tone, candle hiss"),
    (1770, 1796, "foley", "cloth money bag scraping across the baize, a few coins clink"),
    (1798, 1806, "foley", "box lid creak open"),
    (1807, 1814, "foley", "the H4 watch set into velvet: a soft tick, then silence"),
    (1814, 1820, "foley", "lid shut: wooden thud"),
    (1821, 1832, "accent", "three wax seals stamped: thump, thump, thump on the beat of ขัง"),
    (1818, 1834, "accent", "snap push whoosh"),
    (1856, 1856, "cut", "dissolve (15 f) to shot 23, hall evening")]
