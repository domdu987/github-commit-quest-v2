TAKE, SHOTS = "s26", [26]
SHOT_RANGES = {"26": [1707, 1766]}
FIRST, LAST = 1698, 1775
G0, G1 = 1707, 1767
TRANS_IN = dict(type="cut", frames=0)
CUTS_QA = [1707, 1767]
EV = dict(click1=1733, click2=1742, snap=[1731, 1744], jaw_drop_swap=1745)
NOTES = dict(light="DAY", set="v3/set3d16 CHAMBER chamber_table DAY; hooks set_tape (length grows on the clicks) / set_click / set_flames keyed per frame",
             cast="v3/cast16: morse_read_tape, mocker_sour_arms -> mocker_jaw_drop (blink swap g 1745, held open mouth, sweat), congressman_a/b/c_amazed; no lip-sync",
             camera="custom 22 mm from above the front table; drift push 7 %/s + slide + arc, snap x2.1 (13 f) on click 1, travel to the mocker's face")
CUES = [(1698, 1776, "ambience", "chamber hush; far murmur of congressmen, a floorboard creak"),
        (1733, 1736, "prop", "register CLICK 'ติ๊ด' (bright brass tick) + paper tape spooling out (dry paper rattle)"),
        (1742, 1745, "prop", "second CLICK 'ติ๊ด', tape jumps out again"),
        (1745, 1760, "accent", "crowd gasp, then hush; the mocker's jaw-drop sting"),
        (1731, 1744, "accent", "snap push whoosh")]
