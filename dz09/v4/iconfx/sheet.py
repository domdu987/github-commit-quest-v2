"""sheet.py -- contact sheets of the icon library.

    python3 sheet.py [out_dir]        -> sheet_night.png, sheet_light.png (every icon, hold state, labelled)
                                         strips_night.png (each animated icon at 8 moments + the pop-in frames)
"""
import os, sys, random
import icons as I
import raster
from anim import Cue, pop_state

HERE = os.path.dirname(os.path.abspath(__file__))

# (name, t for the still, kwargs, label)
SHEET = [
    ("battery", 0.0, {"level": 3}, "battery 3"), ("battery", 0.0, {"level": 2}, "battery 2"),
    ("battery", 0.0, {"level": 1}, "battery 1 (blinks)"), ("phone", 0.1, {"n": 4}, "phone badge 4"),
    ("heart", 0.1, {}, "heart: crack"), ("heart", 0.6, {}, "heart: broken"),
    ("pinky", 0.0, {}, "pinky promise"), ("pinky", 0.7, {}, "pinky: broken"),
    ("sound_rings", 0.95, {"mode": "arcs"}, "sound rings (arcs)"), ("sound_rings", 0.95, {"mode": "circle"}, "sound rings (circle)"),
    ("eye", 0.6, {}, "eye, red pupil"), ("stopwatch", 0.0, {"elapsed": 21.0}, "stopwatch 60 s"),
    ("biohazard", 0.0, {}, "biohazard"), ("warning", 0.0, {"symbol": "!"}, "warning !"),
    ("warning", 0.0, {"symbol": "bio", "color": I.RED}, "warning bio, red"), ("exclaim_sparks", 0.3, {}, "! sparks"),
    ("exclaim_sparks", 0.3, {"bang": True}, "! sparks + bang"), ("question", 0.2, {}, "? swirl"),
    ("sweat", 0.0, {}, "sweat drop"), ("light_rays", 0.0, {}, "red light rays"),
    ("x_mark", 0.0, {}, "X (reference)"), ("check", 0.0, {}, "check (reference)"),
    ("tape_label", 0.0, {"label": "0.9 MILE"}, "tape label"), ("tape_label", 0.0, {"label": "ระยะ 200 ม.", "family": "Kanit"}, "tape label, Thai"),
    ("tape", 1.0, {"length": 180}, "tape strip"), ("swoosh", 0.15, {}, "swoosh arc (reference)"),
    ("arc_fan", 0.6, {}, "arc fan (reference)"),
]


def night_bg(W, H, seed=3):
    rnd = random.Random(seed)
    s = ('<defs><linearGradient id="nb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1226"/>'
         '<stop offset="1" stop-color="#1b2140"/></linearGradient>'
         '<radialGradient id="na" cx="0.85" cy="0.1" r="0.6"><stop offset="0" stop-color="#e89a3c" stop-opacity="0.35"/>'
         '<stop offset="1" stop-color="#e89a3c" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="nr" cx="0.1" cy="0.95" r="0.5"><stop offset="0" stop-color="#e2453b" stop-opacity="0.25"/>'
         '<stop offset="1" stop-color="#e2453b" stop-opacity="0"/></radialGradient></defs>')
    s += '<rect width="%d" height="%d" fill="url(#nb)"/><rect width="%d" height="%d" fill="url(#na)"/>' \
         '<rect width="%d" height="%d" fill="url(#nr)"/>' % (W, H, W, H, W, H)
    for _ in range(int(W * H / 2500)):
        x, y, l = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(12, 34)
        s += '<path d="M%.1f,%.1f l-2,%.1f" stroke="#a9b6d6" stroke-opacity="0.22" stroke-width="1"/>' % (x, y, l)
    return s


def light_bg(W, H):
    return '<rect width="%d" height="%d" fill="#e9e5dc"/>' % (W, H)


def sheet(night, out, cols=6, cell=230, px=150):
    rows = (len(SHEET) + cols - 1) // cols
    W, H = cols * cell, rows * cell + 70
    s = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H)
    s += (night_bg if night else light_bg)(W, H)
    s += I.defs()
    lab = "#e8e4dc" if night else I.INK
    s += I.text(20, 46, "DEAD ZONE 09 icon FX  -  %s background" % ("night" if night else "light"), 28, lab, anchor="start")
    for i, (name, t, kw, label) in enumerate(SHEET):
        c, r = i % cols, i // cols
        x0, y0 = c * cell, 70 + r * cell
        ic = I.make(name, t, **kw)
        k = px / max(ic.w, ic.h, 100.0) * (100.0 / 100.0)
        ppx = px * 100.0 / max(ic.w, ic.h, 100.0)
        cx = x0 + cell / 2 + (ic.anchor[0] - ic.w / 2) * ppx / 100
        cy = y0 + cell / 2 - 14 + (ic.anchor[1] - ic.h / 2) * ppx / 100
        s += I.placed(ic, cx, cy, ppx, name=name)
        s += I.text(x0 + cell / 2, y0 + cell - 16, label, 15, lab)
    s += "</svg>"
    return raster.render([{"svg": s, "w": W, "h": H, "out": out}])[0]


STRIPS = [("battery", {"level": 1}), ("phone", {}), ("heart", {}), ("pinky", {}), ("sound_rings", {"mode": "arcs"}),
          ("sound_rings", {"mode": "circle"}), ("eye", {}), ("stopwatch", {"speed": 30.0}), ("exclaim_sparks", {}),
          ("question", {}), ("sweat", {}), ("light_rays", {}), ("x_mark", {"strike": True}), ("check", {"draw": True}),
          ("tape", {"length": 150}), ("swoosh", {}), ("arc_fan", {})]
TS = [0.0, 0.067, 0.133, 0.2, 0.3, 0.45, 0.7, 1.0]


def strips(out, cell=130, px=96):
    W = (len(TS) + 5) * cell + 160
    H = len(STRIPS) * cell + 110
    s = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H)
    s += night_bg(W, H) + I.defs()
    s += I.text(20, 40, "inner animation at t (s), then the 'brief' pop-in, frames 0..4 (scale 0, .62, 1.15, 1.06, 1)", 22,
                "#e8e4dc", anchor="start")
    for j, t in enumerate(TS):
        s += I.text(160 + j * cell + cell / 2, 88, "t %.2f" % t, 15, "#e8e4dc")
    for j in range(5):
        s += I.text(160 + (len(TS) + j) * cell + cell / 2, 88, "pop f%d" % j, 15, "#ffd23f")
    cue = Cue(0, hold=10)
    for r, (name, kw) in enumerate(STRIPS):
        y = 100 + r * cell
        s += I.text(12, y + cell / 2 + 5, name, 15, "#e8e4dc", anchor="start")
        for j, t in enumerate(TS + [None] * 5):
            if t is None:
                g = j - len(TS)
                st = pop_state(cue, g)
                ic = I.make(name, st.t, **kw)
                sc, rot = st.scale, st.rot_deg
            else:
                ic = I.make(name, t, **kw)
                sc, rot = 1.0, 0.0
            ppx = px * 100.0 / max(ic.w, ic.h, 100.0)
            cx = 160 + j * cell + cell / 2 + (ic.anchor[0] - ic.w / 2) * ppx / 100
            cy = y + cell / 2 + (ic.anchor[1] - ic.h / 2) * ppx / 100
            if sc > 0:
                s += I.placed(ic, cx, cy, ppx, sc, rot, name=name)
    s += "</svg>"
    return raster.render([{"svg": s, "w": W, "h": H, "out": out}])[0]


if __name__ == "__main__":
    od = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out")
    os.makedirs(od, exist_ok=True)
    print("night", sheet(True, os.path.join(od, "sheet_night.png")), "ms")
    print("light", sheet(False, os.path.join(od, "sheet_light.png")), "ms")
    print("strips", strips(os.path.join(od, "strips_night.png")), "ms")
