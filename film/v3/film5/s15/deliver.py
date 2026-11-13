#!/usr/bin/env python3
"""deliver.py -- s15: from raw/s1..s6 build frames/g_%04d.png (the breath traces drawn over 15a-15c), meta.json, cues.json,
contact.jpg, compare.jpg, take.mkv.   python3 deliver.py [--no-mkv]

Breath traces (the diagram): two small line graphs over the same 2-second window, scrolling, anchored beside their subjects:
the bird's (warm yellow, ~4.2 pumps/s: many bumps) above the cage, the man's (pale blue, one slow breath per 3.2 s) above his
helmet.  Drawn at 4x and reduced (clean anti-aliased lines, no blur filter), plum ink outline like the cast."""
import os, sys, json, glob, shutil, math, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
os.environ.setdefault("S15_NO_BPY", "1")

G0, G1, H = 1502, 1707, 8
B = [G0, 1540, 1579, 1618, 1654, 1677, G1]
RANGES = {1: (G0 - H, B[1] - 1), 2: (B[1], B[2] - 1), 3: (B[2], B[3] - 1), 4: (B[3], B[4] - 1), 5: (B[4], B[5] - 1), 6: (B[5], G1 + H - 1)}
NAME = {1: "15a", 2: "15b", 3: "15c", 4: "15d", 5: "15e", 6: "15f"}
RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames")
TR_IN, TR_OUT = 1504, B[3] - 1                  # traces on from "นกหายใจเร็ว" (fade in 6 f) to the end of 15c (cut)
WIN = 60                                         # 2 s window
INK = (42, 22, 46)


def breath_man(g):
    return 0.5 - 0.5 * math.cos(2 * math.pi * (g - 1490) / 96.0)


def bird_sig(g):
    ph = 3 * 1.4 * (g - 1490) / 30.0
    return 0.5 - 0.5 * math.cos(2 * math.pi * ph)


def shot_of(g):
    return max(s for s, (a, b) in RANGES.items() if g >= a) if g >= RANGES[1][0] else 1


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


def mix(c0, c1, u):
    return tuple(int(round(a + (b - a) * u)) for a, b in zip(c0, c1))


def trace(dr, cx, cy, fn, g, col, k, alpha):
    """a 210 x 46 px (x k) trace centred on (cx, cy): fn over [g - WIN, g], newest value at the right end with a dot."""
    w, h = 210 * k, 46 * k
    x0, y0 = cx * k - w / 2, cy * k - h / 2
    pts = [(x0 + w * i / WIN, y0 + h - h * fn(g - WIN + i)) for i in range(WIN + 1)]
    sub = []
    for i in range(WIN * 4 + 1):                                 # finer sampling for smooth bumps
        gg = g - WIN + i / 4.0
        sub.append((x0 + w * (i / 4.0) / WIN, y0 + h - h * fn(gg)))
    a = int(255 * alpha)
    dr.rounded_rectangle((x0 - 14 * k, y0 - 12 * k, x0 + w + 14 * k, y0 + h + 12 * k), radius=14 * k, fill=(20, 16, 34, int(120 * alpha)),
                         outline=INK + (a,), width=3 * k)
    dr.line(sub, fill=INK + (a,), width=11 * k, joint="curve")
    dr.line(sub, fill=col + (a,), width=5 * k, joint="curve")
    ex, ey = sub[-1]
    r = 9 * k
    dr.ellipse((ex - r, ey - r, ex + r, ey + r), fill=col + (a,), outline=INK + (a,), width=3 * k)


def overlay(img, g, rep):
    if not (TR_IN <= g <= TR_OUT) or not rep:
        return img
    alpha = min(1.0, (g - TR_IN + 1) / 6.0)
    k = 4
    W, Hh = img.size
    lay = Image.new("RGBA", (W * k, Hh * k), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
    gas = min(1.0, max(0.0, (g - 1590) / 20.0))
    bcol = mix((255, 207, 58), (190, 214, 106), 0.6 * gas)
    if "ring" in rep.get("pts", {}):
        rx, ry = rep["pts"]["ring"]
        cx = min(max(rx, 130), W - 130); cy = max(ry - 70, 70)
        trace(dr, cx, cy, bird_sig, g, bcol, k, alpha)
    hd = rep.get("heads", {}).get("gaffer")
    if hd:
        cx = min(max(hd["x"], 130), W - 130); cy = max(hd["y"] - hd["w"] * 0.95 - 40, 70)
        if "ring" in rep.get("pts", {}) and abs(cy - max(rep["pts"]["ring"][1] - 70, 70)) < 90 and abs(cx - min(max(rep["pts"]["ring"][0], 130), W - 130)) < 240:
            cy = max(rep["pts"]["ring"][1] - 70, 70) + 100          # never stack the two traces on top of each other
        trace(dr, cx, cy, breath_man, g, (160, 208, 255), k, alpha)
    lay = lay.resize((W, Hh), Image.LANCZOS)
    out = img.convert("RGBA"); out.alpha_composite(lay)
    return out.convert("RGB")


def build_frames():
    os.makedirs(OUT, exist_ok=True)
    src = {}
    for g in range(G0 - H, G1 + H):
        s = shot_of(g)
        js = raw(s, g)[:-4] + ".json"
        rep = json.load(open(js)) if os.path.exists(js) else None
        img = Image.open(raw(s, g)).convert("RGB")
        img = overlay(img, g, rep)
        img.save(os.path.join(OUT, "g_%04d.png" % g))
        src[g] = NAME[s] + ("+traces" if TR_IN <= g <= TR_OUT else "")
    return src


def cues():
    def c(g, g2, kind, label, **kw):
        d = dict(time=round(g / 30.0, 3), duration=round((g2 - g) / 30.0, 3), frame=g, end_frame=g2, kind=kind, label=label); d.update(kw)
        return d
    return {"take": "s15", "fps": 30, "note": "time = film seconds (g / 30); narration PROJ/film5/audio/narration_bankky.wav at +0.10 s",
            "cues": [
                c(G0 - H, G1 + H, "ambience", "quiet mine tunnel room tone after the blast: settling dust, a slow creak of the timber sets"),
                c(G0, B[3], "music", "soft explanatory pulse: a slow low note on each of the man's breaths, a quick high tick on each of the bird's pumps"),
                c(G0, B[3], "breath", "the man: one slow audible breath in / out every 3.2 s"),
                c(G0, B[3], "breath", "the bird: tiny fast chirp-breaths, about 4 per second (under the narration)"),
                c(B[1], B[1], "cut", "cut: tighter on the bird and the man side by side"),
                c(B[2], B[2], "cut", "cut: low wide, the three heights"),
                c(1572, 1592, "gas", "a faint airy hiss: the gas layer sinks from the roof and reaches the cage first"),
                c(1606, 1626, "gas", "the hiss passes the man's head"),
                c(B[3], B[3], "cut", "cut: the man and his lamp, the flame still steady"),
                c(B[4], B[4], "cut", "cut: ECU of the lamp"),
                c(1656, 1666, "flame", "whump: the flame flares tall and blue (soft, not an explosion)"),
                c(B[5], B[5], "cut", "cut: ECU of the bird inside the bars, breathing fast"),
                c(B[5], G1, "breath", "the bird's quick breaths, a little heavier in the haze"),
            ]}


def main():
    src = build_frames()
    rows = [json.load(open(f)) for f in glob.glob(os.path.join(RAW, "s*", "g_*.json"))]
    meta = {"take": "s15", "film": 5, "shots": [15], "first_g": G0 - H, "n_frames": (G1 + H) - (G0 - H), "g0": G0, "g1": G1,
            "handle_in": H, "handle_out": H,
            "transition_in": {"type": "dissolve_or_cut", "frames": 12, "note": "handle g 1494..1501 rendered in 3D (15a camera keeps moving)"},
            "transition_out": {"type": "dissolve_or_cut", "frames": 12, "note": "handle g 1707..1714 rendered in 3D (15f camera keeps moving)"},
            "transitions": [{"at": G0, "type": "in", "handle": [G0 - H, G0 - 1]}] +
                           [{"at": B[i], "type": "cut", "from_shot": NAME[i], "to_shot": NAME[i + 1]} for i in range(1, 6)] +
                           [{"at": G1, "type": "out", "handle": [G1, G1 + H - 1]}],
            "shot_ranges": dict([("15", [G0, G1 - 1])] + [(NAME[s], [max(a, G0), min(b, G1 - 1)]) for s, (a, b) in RANGES.items()]),
            "events": {"traces_on": [TR_IN, TR_OUT], "gas_reaches_bird": 1590, "gas_reaches_man": 1622, "flame_flares": [1656, 1663]},
            "set": "v3/set3d5/mine.py tunnel LAMP; cage raised to a nail under the cap bar of set 6 (set_cage), tub train hidden (runtime), "
                   "own gas-haze card (camera-facing, wavy lower edge, green-grey, alpha <= 0.30)",
            "dof": "none (client rule: M.setup_dof(scene, None, None, cam) at build and before every render)",
            "denoiser": "OpenImageDenoise albedo+normal, prefilter FAST",
            "cast": "v3/cast5: gaffer (mouth closed, slow breath via squash), canary sprite on the 3D cage perch (breath 1, ~4.2 pumps/s)",
            "overlay": "breath traces drawn by deliver.py over 15a-15c (g %d..%d)" % (TR_IN, TR_OUT),
            "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(float(np.mean([r["wall"] for r in rows])), 2) if rows else None,
            "s_per_frame_cpu_mean": round(float(np.mean([r["cpu"] for r in rows])), 2) if rows else None,
            "frame_source": {str(g): v for g, v in sorted(src.items())}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(cues(), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
    # contact sheet: 16 frames across the take
    picks = [1494, 1505, 1525, 1545, 1565, 1585, 1600, 1612, 1625, 1645, 1655, 1662, 1672, 1685, 1700, 1714]
    sh = [sys.executable, os.path.join(HERE, "..", "s01", "sheet.py"), os.path.join(HERE, "contact.jpg"), "8"] + [os.path.join(OUT, "g_%04d.png" % g) for g in picks]
    subprocess.run(sh, check=True)
    comp = [os.path.join(OUT, "g_1525.png"), "ref99", os.path.join(OUT, "g_1600.png"), "ref103", os.path.join(OUT, "g_1665.png"), "ref107",
            os.path.join(OUT, "g_1690.png"), "ref111"]
    subprocess.run([sys.executable, os.path.join(HERE, "..", "s01", "sheet.py"), os.path.join(HERE, "compare.jpg"), "4"] + comp, check=True)
    if "--no-mkv" not in sys.argv:
        mkv = os.path.join(HERE, "take.mkv")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G0 - H), "-i", os.path.join(OUT, "g_%04d.png"),
                        "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    print("frames %d..%d" % (G0 - H, G1 + H - 1))


if __name__ == "__main__":
    main()
