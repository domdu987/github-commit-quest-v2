#!/usr/bin/env python3
"""probe.py -- staging numbers without rendering.  python3 probe.py A|B <g list or a:b:step> [out.json]
Prints, per output frame g: camera height / pitch / yaw, every head (centre x, y; width px), prop registration (px)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def run(take, gs, quiet=False):
    F = film.Film(take, verbose=not quiet)
    F.pose(gs)
    rows = [F.report(g) for g in gs if F.g0 <= g <= F.g1]
    return F, rows


if __name__ == "__main__":
    take, gs = sys.argv[1], parse(sys.argv[2])
    F, rows = run(take, gs)
    for r in rows:
        hd = "  ".join("%s (%4.0f,%4.0f) w%3.0f" % (n, h["x"], h["y"], h["w"]) for n, h in r["heads"].items())
        rg = ("reg %.2f px err %.4f" % (r["reg"]["px"], r["reg"]["solve_err_D"])) if "reg" in r else ""
        print("g %3d  cam z %.2f pitch %+5.1f yaw %+5.1f  %s  %s  line %.2f erase %.2f" % (r["g"], r["cam_height"], r["pitch"], r["yaw"], hd, rg, r["line"], r["erase"]))
    if len(sys.argv) > 3:
        json.dump(rows, open(sys.argv[3], "w"), indent=1)
