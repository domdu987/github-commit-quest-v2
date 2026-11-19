TAKE, SHOTS = "s29", [29]
SHOT_RANGES = {"29": [1895, 1979]}
FIRST, LAST = 1886, 1988
G0, G1 = 1895, 1980
TRANS_IN = dict(type="cut", frames=0)
CUTS_QA = [1895, 1980]
EV = dict(instrument_slide=[1930, 1950], blink_swap=[1951, 1953], horror_pose=1952, snap=[1952, 1965], word_in_his_care=1956)
NOTES = dict(light="DAY", set="v3/set3d16 CHAMBER chamber_table DAY; the instrument is cut out of the table meshes at runtime (bmesh, vertices above the baize inside the instrument box) and rebuilt with CH.tg_arm_parts as its own objects, location keyed per frame; the lever follows; tape hidden",
             cast="v3/cast16 mocker_pm_proud -> mocker_horror (sweat, blink swap g 1952; tremble), clerk16 clerk_idle -> clerk_slide_instrument (mirrored); no lip-sync",
             camera="custom 22 mm wide from the front (z 4.4, 3.2 D back), push 10 %/s + slide + arc, snap x3.2 / 14 f with a 3.4 D pan to the mocker on 'ความดูแลของเขา'")
CUES = [(1886, 1989, "ambience", "chamber: hush, a clock ticks"),
        (1930, 1950, "prop", "the heavy brass-and-walnut instrument SCRAPES across the baize (wood-on-cloth slide), ends with a soft thud"),
        (1952, 1960, "accent", "horror sting: a low string stab as the proud smile drops"),
        (1952, 1965, "accent", "snap push whoosh")]
