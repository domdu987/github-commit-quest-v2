#!/usr/bin/env python3
"""deliver.py -- s16: raw/s1..s3 -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv.  python3 deliver.py [--no-mkv]"""
import os, sys, json, glob, shutil, math, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
os.environ.setdefault("S15_NO_BPY", "1")

G0, G1, H = 1707, 1814, 8
B = [G0, 1743, 1779, G1]
RANGES = {1: (G0 - H, B[1] - 1), 2: (B[1], B[2] - 1), 3: (B[2], G1 + H - 1)}
NAME = {1: "16a", 2: "16b", 3: "16c"}
RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames")


def shot_of(g):
    return max(s for s, (a, b) in RANGES.items() if g >= a) if g >= RANGES[1][0] else 1


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


def build_frames():
    os.makedirs(OUT, exist_ok=True)
    src = {}
    for g in range(G0 - H, G1 + H):
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
    return {"take": "s16", "fps": 30, "note": "time = film seconds (g / 30); narration PROJ/film5/audio/narration_bankky.wav at +0.10 s",
            "cues": [
                c(G0 - H, G1 + H, "ambience", "tunnel room tone, a low gas hiss growing a little with each beat"),
                c(G0, B[1], "bird_song", "replay, day 1: a quick bright trill of 5 notes (slightly sped up, a soft 'rewind' whoosh on the cut in)", notes=5),
                c(B[1], B[1], "cut", "hard cut + soft whoosh: day 5"),
                c(B[1], B[2], "bird_song", "replay, day 5: 3 notes, thinner", notes=3),
                c(B[2], B[2], "cut", "hard cut + soft whoosh: day 10"),
                c(B[2], 1797, "bird_song", "replay, day 10: one weak note", notes=1),
                c(1797, G1, "silence", "the song stops: only the hiss; the bird's eyes grow heavy (gentle)"),
            ]}


def main():
    src = build_frames()
    rows = [json.load(open(f)) for f in glob.glob(os.path.join(RAW, "s*", "g_*.json"))]
    meta = {"take": "s16", "film": 5, "shots": [16], "first_g": G0 - H, "n_frames": (G1 + H) - (G0 - H), "g0": G0, "g1": G1,
            "handle_in": H, "handle_out": H,
            "transition_in": {"type": "dissolve_or_cut", "frames": 12, "note": "handle g 1699..1706 rendered in 3D (16a camera keeps moving)"},
            "transition_out": {"type": "dissolve_or_cut", "frames": 12, "note": "handle g 1814..1821 rendered in 3D (16c camera keeps moving)"},
            "transitions": [{"at": G0, "type": "in", "handle": [G0 - H, G0 - 1]}] +
                           [{"at": B[i], "type": "cut", "from_shot": NAME[i], "to_shot": NAME[i + 1]} for i in range(1, 3)] +
                           [{"at": G1, "type": "out", "handle": [G1, G1 + H - 1]}],
            "shot_ranges": dict([("16", [G0, G1 - 1])] + [(NAME[s], [max(a, G0), min(b, G1 - 1)]) for s, (a, b) in RANGES.items()]),
            "events": {"notes": {"16a": 5, "16b": 3, "16c": 1}, "song_stops": 1797, "haze_amp": {"16a": 0.10, "16b": 0.22, "16c": 0.36}},
            "set": "v3/set3d5/mine.py tunnel LAMP; the set's 3D cage on its nail with the canary sprite on the perch behind the front bars; "
                   "set_gas 1 / 2 / 3 plus my own camera-facing haze card (as s15) thickening each beat",
            "dof": "none (client rule: M.setup_dof(scene, None, None, cam) at build and before every render)",
            "denoiser": "OpenImageDenoise albedo+normal, prefilter FAST",
            "cast": "v3/cast5: canary sprite (perch_sing 5 / 3 notes, sing_one 1 note, then a gentle droop: eyes heavy, never closed or X)",
            "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(float(np.mean([r["wall"] for r in rows])), 2) if rows else None,
            "s_per_frame_cpu_mean": round(float(np.mean([r["cpu"] for r in rows])), 2) if rows else None,
            "frame_source": {str(g): v for g, v in sorted(src.items())}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(cues(), open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
    # contact sheet: 16 frames across the take
    picks = [1699, 1707, 1715, 1725, 1735, 1742, 1743, 1752, 1762, 1772, 1779, 1786, 1795, 1803, 1813, 1821]
    sh = [sys.executable, os.path.join(HERE, "..", "s01", "sheet.py"), os.path.join(HERE, "contact.jpg"), "8"] + [os.path.join(OUT, "g_%04d.png" % g) for g in picks]
    subprocess.run(sh, check=True)
    comp = [os.path.join(OUT, "g_1725.png"), "ref113", os.path.join(OUT, "g_1760.png"), "ref115", os.path.join(OUT, "g_1790.png"), "ref117"]
    subprocess.run([sys.executable, os.path.join(HERE, "..", "s01", "sheet.py"), os.path.join(HERE, "compare.jpg"), "4"] + comp, check=True)
    if "--no-mkv" not in sys.argv:
        mkv = os.path.join(HERE, "take.mkv")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G0 - H), "-i", os.path.join(OUT, "g_%04d.png"),
                        "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    print("frames %d..%d" % (G0 - H, G1 + H - 1))


if __name__ == "__main__":
    main()
