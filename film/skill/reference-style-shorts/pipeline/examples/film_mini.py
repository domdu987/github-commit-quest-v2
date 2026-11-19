#!/usr/bin/env python3
"""film_mini.py : takes -> film for a short film of a few takes (conform, captions, mix), the steps of
v3/film/out/conform.py, assemble.py and audio/mixer.py without film 1's hard-coded take list, hook and overlays.

    python3 film_mini.py conform <out_dir> <take_dir> <take_dir> [...]   frames/f_%04d.png + joins.json + cues_all.json
    python3 film_mini.py grade <out_dir> [shots.json] [--procs N]         graded/f_%04d.png (the v1.1 grade, DEFAULT settings)
    python3 film_mini.py captions <out_dir> <captions.json> [--style th88|th72|en] [--frames frames|graded]
                                                                         film_silent.mp4 (captions burned last, assemble.py)
    python3 film_mini.py mix <out_dir> <mix.json>                        film.wav + film.mp4 (audio/mixer.py)

conform: every take folder must hold meta.json (g0, g1, handle_in, handle_out, transition_in) and frames/g_%04d.png
(the output of the take's `post`). Takes are joined in the order given. If their [g0, g1) ranges follow each other (a real
film, all cut to one narration clock) the film frame is g; otherwise (these examples all sit on g 30..66) each take is laid
after the previous one and the shift is written to joins.json. Transitions: transition_in of the incoming take;
'dissolve' L = smoothstep cross-dissolve on frames gb - L//2 .. gb - L//2 + L - 1, weight of the incoming take
smoothstep((g - a + 1) / (L + 1)) (conform.py's rule), mixed from both takes' handle frames.
'wipe' (or 'object_wipe') = conform.py's 6-frame foam-sheet wipe on gb-3 .. gb+2 (needs 3 handle frames on each side);
'flash' = straight cut at gb, white flash 0.15/0.35/0.60/0.85/1.00 on the last 5 outgoing frames and 0.85/0.55/0.30/0.12 on
the first 4 incoming frames; 'punch_in' = straight cut plus conform.speed_lines on the first 6 incoming frames (strength
0.45, n=40, r_in=300, centre transition_in "centre", default (360, 520)); 'cut', 'hard_cut', 'whip', 'hidden_cut_in_whip'
= straight cut (a whip's streak is in the takes). Any other type stops the conform with an error.
grade: grade.py's grade_frame with its DEFAULT settings only (curve, SAT_GLOBAL 1.18, hot bloom, red protect 0.8, white
protect wsat 0.30, ceiling 0.985); film 1's TAKES/JOINS/SHOT/fog tables are replaced by this film's joins.json, no SHOT
and no fog. shots.json (optional) = {"<take>": {grade.DEFAULT key: value, ...}}: per-take corrections that cross-fade
over the joins as in film 1. Resumable (existing graded frames are skipped).
captions.json: [{"t0": s, "t1": s, "text": "..."}] on the film clock; each text gets a caption style at (360, 900)
(assemble.py places it; fonts from <PROJ>/fonts): th88 = {\\fnKanit Black\\fs88} (film 1, 45 px text height),
th72 = {\\fnKanit Black\\fs72} (37 px, the reference size), en = {\\fnWork Sans Black\\fs58} (36 px measured with score.py,
stroke 3.8 px; the reference is 36-37 px). --frames graded burns over graded/ (after `grade`); default frames/.
mix.json: audio/mixer.py's spec without duration/video (filled in here); cues_all.json is the list to build its "sfx" from.
"""
import json
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
STYLES = {"th88": "{\\fnKanit Black\\fs88}", "th72": "{\\fnKanit Black\\fs72}", "en": "{\\fnWork Sans Black\\fs58}"}
KNOWN = ("dissolve", "wipe", "object_wipe", "flash", "punch_in", "cut", "hard_cut", "whip", "hidden_cut_in_whip")
FLASH_IN = [0.15, 0.35, 0.60, 0.85, 1.00]     # last 5 outgoing frames
FLASH_OUT = [0.85, 0.55, 0.30, 0.12]          # first 4 incoming frames


def conform_module():
    sys.path.insert(0, os.path.join(PROJ, "v3", "film", "out"))
    import conform as C                        # importing has no side effects
    return C


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def conform(out, dirs):
    tk = []
    for d in dirs:
        m = json.load(open(os.path.join(d, "meta.json")))
        tk.append(dict(dir=os.path.abspath(d), take=m["take"], g0=m["g0"], g1=m["g1"], hi=m.get("handle_in", 0),
                       ho=m.get("handle_out", 0), tin=m.get("transition_in") or {}))
    contiguous = all(a["g1"] == b["g0"] for a, b in zip(tk, tk[1:]))
    pos = tk[0]["g0"] if contiguous else 0
    for t in tk:                                   # film frame = take frame + shift
        t["shift"] = 0 if contiguous else pos - t["g0"]
        pos += t["g1"] - t["g0"]
    N = pos
    F0 = tk[0]["g0"] + tk[0]["shift"]

    def frame(t, gf):                             # film frame gf of take t (handles included), None if not rendered
        p = os.path.join(t["dir"], "frames", "g_%04d.png" % (gf - t["shift"]))
        return p if os.path.exists(p) else None

    joins = []
    for a, b in zip(tk, tk[1:]):
        gb = b["g0"] + b["shift"]
        typ, L = b["tin"].get("type", "cut"), int(b["tin"].get("frames", 0) or 0)
        if typ not in KNOWN:
            raise SystemExit("conform: take %s declares transition_in type %r; known: %s" % (b["take"], typ, ", ".join(KNOWN)))
        if typ == "dissolve" and L > 0:
            kind, rng = "dissolve", (gb - L // 2, gb - L // 2 + L - 1)
        elif typ in ("wipe", "object_wipe"):
            kind, L, rng = "wipe", 6, (gb - 3, gb + 2)
        elif typ == "flash":
            kind, L, rng = "flash", 9, (gb - 5, gb + 3)
        elif typ == "punch_in":
            kind, L, rng = "punch_in", 6, (gb, gb + 5)
        else:
            kind, rng = "cut", (gb, gb)
        joins.append(dict(a=a["take"], b=b["take"], gb=gb, kind=kind, frames=L, range=list(rng),
                          centre=list(b["tin"].get("centre", (360, 520)))))
    C = conform_module() if any(j["kind"] in ("wipe", "punch_in") for j in joins) else None
    os.makedirs(os.path.join(out, "frames"), exist_ok=True)
    held = []
    for g in range(F0, N):
        own = next(t for t in tk if t["g0"] + t["shift"] <= g < t["g1"] + t["shift"])
        img = None
        for j, (a, b) in zip(joins, zip(tk, tk[1:])):
            lo, hi = j["range"]
            if j["kind"] in ("dissolve", "wipe") and lo <= g <= hi:
                pa, pb = frame(a, g), frame(b, g)
                if not (pa and pb):                   # a missing handle: hold the nearest frame (conform.py extends it in 2D)
                    held.append(g)
                    pa = pa or frame(a, min(g, a["g1"] + a["shift"] + a["ho"] - 1))
                    pb = pb or frame(b, max(g, b["g0"] + b["shift"] - b["hi"]))
                A = np.asarray(Image.open(pa).convert("RGB"), np.float32)
                B = np.asarray(Image.open(pb).convert("RGB"), np.float32)
                if j["kind"] == "dissolve":
                    w = smooth((g - lo + 1) / (j["frames"] + 1.0))
                    img = A * (1 - w) + B * w
                else:
                    img = C.foam_wipe(A, B, g - lo)
        if img is None:
            img = np.asarray(Image.open(frame(own, g)).convert("RGB"), np.float32)
        for j in joins:
            lo, hi = j["range"]
            if j["kind"] == "flash" and lo <= g <= hi:
                w = FLASH_IN[g - lo] if g < j["gb"] else FLASH_OUT[g - j["gb"]]
                img = img * (1 - w) + 255.0 * w
            elif j["kind"] == "punch_in" and lo <= g <= hi:
                k = (g - lo) / 5.0
                st = 0.45 * smooth(min(1.0, (g - lo + 1) / 3.0)) * (1 - smooth((k - 0.5) / 0.5))
                img = C.speed_lines(img, j["centre"][0], j["centre"][1], st, seed=2000 + g, n=40, r_in=300, retreat=0.5 * k)
        Image.fromarray(np.clip(img + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(out, "frames", "f_%04d.png" % (g - F0)))
    cues = []
    for t in tk:
        p = os.path.join(t["dir"], "cues.json")
        if not os.path.exists(p):
            continue
        c = json.load(open(p))
        for e in c.get("events") or c.get("cues") or []:
            tt = e.get("time", e.get("t"))
            cues.append(dict(t=round(tt + (t["shift"] - F0) / 30.0, 3), dur=e.get("duration", e.get("dur")), kind=e["kind"],
                             label=e["label"], take=t["take"]))
    cues.sort(key=lambda e: e["t"])
    json.dump(dict(takes=tk, joins=joins, first_film_frame=F0, frames=N - F0, held=held), open(os.path.join(out, "joins.json"), "w"), indent=1)
    json.dump(dict(time="film seconds from the first frame of the conform", cues=cues), open(os.path.join(out, "cues_all.json"), "w"),
              indent=1, ensure_ascii=False)
    print("conform: %d frames (%.2f s), %d joins, %d cues, held %s -> %s" % (N - F0, (N - F0) / 30.0, len(joins), len(cues), held, out))


def grade(out, shots_path=None, procs=1):
    js = json.load(open(os.path.join(out, "joins.json")))
    F0 = js["first_film_frame"]
    takes = [(t["take"], t["g0"] + t["shift"] - F0) for t in js["takes"]]
    joins = [(j["b"], "d" if j["kind"] == "dissolve" else "x", j["range"][0] - F0, j["range"][1] - F0)
             for j in js["joins"] if j["kind"] in ("dissolve", "wipe", "flash")]
    shots = json.load(open(shots_path)) if shots_path else {}
    todo = [g for g in range(js["frames"]) if not os.path.exists(os.path.join(out, "graded", "f_%04d.png" % g))]
    os.makedirs(os.path.join(out, "graded"), exist_ok=True)
    args = [(out, g, takes, joins, shots) for g in todo]
    if procs > 1:
        import multiprocessing as mp
        with mp.Pool(procs) as pool:
            for _ in pool.imap_unordered(_grade_one, args, chunksize=4):
                pass
    else:
        for a in args:
            _grade_one(a)
    print("grade: %d frames graded (%d already there) -> %s" % (len(todo), js["frames"] - len(todo), os.path.join(out, "graded")))


def _grade_one(a):
    out, g, takes, joins, shots = a
    sys.path.insert(0, os.path.join(PROJ, "v3", "film", "out_v11"))
    import grade as G
    if G.TAKES is not takes:                       # this film's clock, no film 1 tables
        G.TAKES, G.JOINS, G.SHOT = takes, joins, shots
        G.FOG_G0, G.FOG_G1 = 10 ** 9, -1           # no fog bank
    unknown = {k for v in shots.values() for k in v} - set(G.DEFAULT)
    if unknown:
        raise SystemExit("grade: unknown keys in shots.json: %s (use grade.DEFAULT keys)" % sorted(unknown))
    im = G.grade_frame(Image.open(os.path.join(out, "frames", "f_%04d.png" % g)), g)
    o = os.path.join(out, "graded", "f_%04d.png" % g)
    im.save(o + ".tmp.png"); os.replace(o + ".tmp.png", o)


def captions(out, caps_path, style="th88", src="frames"):
    if style not in STYLES:
        raise SystemExit("captions: --style must be one of %s" % ", ".join(STYLES))
    caps = json.load(open(caps_path))
    burn = [dict(t0=c["t0"], t1=c["t1"], text=STYLES[style] + c["text"]) for c in caps]
    bp = os.path.join(out, "caps_burn.json")
    json.dump(burn, open(bp, "w"), ensure_ascii=False, indent=1)
    subprocess.run([sys.executable, os.path.join(PROJ, "assemble.py"), os.path.join(out, src), os.path.join(out, "film_silent.mp4"), bp, "30"],
                   check=True)


def mix(out, spec_path):
    spec = json.load(open(spec_path))
    n = len([f for f in os.listdir(os.path.join(out, "frames")) if f.startswith("f_")])
    spec.update(duration=n / 30.0, out_wav=os.path.join(out, "film.wav"), video_in=os.path.join(out, "film_silent.mp4"),
                video_out=os.path.join(out, "film.mp4"))
    sp = os.path.join(out, "mix_spec.json")
    json.dump(spec, open(sp, "w"), indent=1)
    subprocess.run([sys.executable, os.path.join(PROJ, "audio", "mixer.py"), sp], check=True)


if __name__ == "__main__":
    cmd, out = sys.argv[1], os.path.abspath(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    if cmd == "conform":
        conform(out, sys.argv[3:])
    elif cmd == "grade":
        rest = sys.argv[3:]
        procs = 1
        if "--procs" in rest:
            i = rest.index("--procs"); procs = int(rest[i + 1]); del rest[i:i + 2]
        grade(out, rest[0] if rest else None, procs)
    elif cmd == "captions":
        rest = sys.argv[4:]
        opt = dict(zip(rest[::2], rest[1::2]))
        bad = set(opt) - {"--style", "--frames"}
        if bad or len(rest) % 2:
            raise SystemExit(__doc__)
        captions(out, sys.argv[3], opt.get("--style", "th88"), opt.get("--frames", "frames"))
    elif cmd == "mix":
        mix(out, sys.argv[3])
    else:
        raise SystemExit(__doc__)
