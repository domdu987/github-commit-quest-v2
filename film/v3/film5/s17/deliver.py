#!/usr/bin/env python3
"""deliver.py -- s17: raw/s1..s2 -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv.  python3 deliver.py [--no-mkv]"""
import os, sys, json, glob, shutil, math, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
os.environ.setdefault("S15_NO_BPY", "1")

G0, G1, H = 1814, 1968, 8
B = [G0, 1872, G1]
RANGES = {1: (G0 - H, B[1] - 1), 2: (B[1], G1 - 1)}
NAME = {1: "17a", 2: "17b"}
RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames")


def shot_of(g):
    return max(s for s, (a, b) in RANGES.items() if g >= a) if g >= RANGES[1][0] else 1


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


def build_frames():
    os.makedirs(OUT, exist_ok=True)
    src = {}
    for g in range(G0 - H, G1):
        s = shot_of(g)
        js = raw(s, g)[:-4] + ".json"
        rep = json.load(open(js)) if os.path.exists(js) else None
        img = Image.open(raw(s, g)).convert("RGB")
        img.save(os.path.join(OUT, "g_%04d.png" % g))
        src[g] = NAME[s]
    return src


def cues():
    def c(g, g2, kind, label, **kw):
        d = dict(time=round(g / 30.0, 3), duration=round((g2 - g) / 30.0, 3), frame=g, end_frame=g2, kind=kind, label=label); d.update(kw)
        return d
    return {"take": "s17", "fps": 30, "note": "time = film seconds (g / 30); narration PROJ/film5/audio/narration_bankky.wav at +0.10 s",
            "cues": [
                c(G0 - H, G1, "ambience", "pithead at dusk: distant winding engine, the sheave wheels creaking, a far train, evening birds very soft"),
                c(1839, 1879, "prop", "the oxygen box: a gentle steady hiss through the rubber tube"),
                c(B[1], B[1], "cut", "cut: closer on the cage and the mask"),
                c(1879, 1891, "bird", "the bird opens its eyes: a tiny soft rustle"),
                c(1894, 1899, "bird", "a little hop up to the perch: wing flutter"),
                c(1899, 1934, "bird_song", "one clear, sweet note", notes=1),
                c(1934, G1, "music", "warm resolving chord under the hold to the end"),
            ]}


def main():
    src = build_frames()
    rows = [json.load(open(f)) for f in glob.glob(os.path.join(RAW, "s*", "g_*.json"))]
    meta = {"take": "s17", "film": 5, "shots": [17], "first_g": G0 - H, "n_frames": G1 - (G0 - H), "g0": G0, "g1": G1,
            "handle_in": H, "handle_out": 0,
            "transition_in": {"type": "dissolve_or_cut", "frames": 12, "note": "handle g 1806..1813 rendered in 3D (17a camera keeps moving)"},
            "transition_out": {"type": "end", "frames": 0, "note": "hold to the end of the film, last frame g 1967"},
            "transitions": [{"at": G0, "type": "in", "handle": [G0 - H, G0 - 1]}, {"at": B[1], "type": "cut", "from_shot": "17a", "to_shot": "17b"},
                            {"at": G1, "type": "end"}],
            "shot_ranges": {"17": [G0, G1 - 1], "17a": [G0, B[1] - 1], "17b": [B[1], G1 - 1]},
            "events": {"mask_at_bars": 1839, "eyes_open": [1879, 1891], "hop_to_perch": [1894, 1899], "one_note": [1899, 1934], "push_ends_hold": 1950},
            "set": "v3/set3d5/mine.py pithead DUSK; the set's oxygen box on the bench, its lying tube+mask removed at runtime and replaced by my "
                   "rubber tube (bevelled curve, keyed) to a small rubber mask in alfie's hand; window emission x0.55 (runtime)",
            "dof": "none (client rule: M.setup_dof(scene, None, None, cam) at build and before every render)",
            "denoiser": "OpenImageDenoise albedo+normal, prefilter FAST",
            "cast": "v3/cast5: alfie (alfie_revive kneel, no held box; right fist pinned to the mask; worried -> happy, mouth never talks), "
                    "canary_in_cage 2D sprite standing on the bench (bars drawn over the bird): fallen eyes closed -> eyes open -> perch -> 1 note",
            "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(float(np.mean([r["wall"] for r in rows])), 2) if rows else None,
            "s_per_frame_cpu_mean": round(float(np.mean([r["cpu"] for r in rows])), 2) if rows else None,
            "frame_source": {str(g): v for g, v in sorted(src.items())}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(cues(), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
    # contact sheet: 16 frames across the take
    picks = [1806, 1814, 1825, 1840, 1855, 1870, 1872, 1880, 1888, 1896, 1902, 1915, 1930, 1945, 1958, 1967]
    sh = [sys.executable, os.path.join(HERE, "..", "s01", "sheet.py"), os.path.join(HERE, "contact.jpg"), "8"] + [os.path.join(OUT, "g_%04d.png" % g) for g in picks]
    subprocess.run(sh, check=True)
    comp = [os.path.join(OUT, "g_1840.png"), "ref121", os.path.join(OUT, "g_1888.png"), "ref125", os.path.join(OUT, "g_1915.png"), "ref127"]
    subprocess.run([sys.executable, os.path.join(HERE, "..", "s01", "sheet.py"), os.path.join(HERE, "compare.jpg"), "4"] + comp, check=True)
    if "--no-mkv" not in sys.argv:
        mkv = os.path.join(HERE, "take.mkv")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G0 - H), "-i", os.path.join(OUT, "g_%04d.png"),
                        "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    print("frames %d..%d" % (G0 - H, G1 - 1))


if __name__ == "__main__":
    main()
