#!/usr/bin/env python3
"""deliver.py -- raw/s<shot>/g_*.png -> frames/g_%04d.png (internal dissolves mixed), meta.json, cues.json, contact.jpg,
take.mkv, qa.json (camera speed, popcheck, hue rows, heads).  The take's config is in take_cfg.py next to this file.
    python3 deliver.py [--no-mkv]"""
import os, sys, json, glob, math, shutil, subprocess, importlib.util
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(V3), "v2", "shots"))
sys.path.insert(0, os.path.join(V3, "tools"))
sys.path.insert(0, HERE)
from anim import smoothstep_mix          # noqa: E402
import take_cfg as C                     # noqa: E402

RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


def source(g):
    """[(shot, weight)] for film frame g."""
    for d in C.INTERNAL:
        if d["type"] == "dissolve" and d["mixed"][0] <= g <= d["mixed"][1]:
            w = smoothstep_mix(g - d["mixed"][0] + 1, d["frames"])
            return [(d["from_shot"], 1 - w), (d["to_shot"], w)]
    for s, (a, b) in sorted(C.SHOT_RANGES_OUT.items()):
        if a <= g <= b:
            return [(s, 1.0)]
    raise KeyError(g)


src = {}
for g in range(C.FIRST_G, C.LAST_G + 1):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    parts = source(g)
    if len(parts) == 1:
        shutil.copyfile(raw(parts[0][0], g), dst); src[g] = "s%d" % parts[0][0]
    else:
        acc = None
        for s, w in parts:
            a = np.asarray(Image.open(raw(s, g)).convert("RGB"), dtype=np.float32) * w
            acc = a if acc is None else acc + a
        Image.fromarray(np.clip(acc + 0.5, 0, 255).astype(np.uint8)).save(dst)
        src[g] = "+".join("s%d*%.3f" % (s, w) for s, w in parts)

rows = []
for js in glob.glob(os.path.join(RAW, "s*", "g_*.json")):
    rows.append(json.load(open(js)))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]

# ---------------------------------------------------------------- QA numbers
spec = importlib.util.spec_from_file_location("shotmod", os.path.join(HERE, "shot.py"))
F = 782.22


def basis(loc, look):
    f = (look - loc).normalized(); from mathutils import Vector
    r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    return f, r, u


def cam_speeds(camf, g0, g1, s=None):
    from mathutils import Vector
    out = []
    for g in range(g0, g1):
        l0, k0 = camf(g); l1, k1 = camf(g + 1); f, r, u = basis(l0, k0)
        m = 0.0
        for sx in (-1, 0, 1):
            for sy in (-1, 0, 1):
                p = l0 + (f + r * (sx * 360 / F) + u * (sy * 640 / F)) * (C.QA_DEPTH[s] if isinstance(C.QA_DEPTH, dict) else C.QA_DEPTH)
                def proj(p, loc, look):
                    ff, rr, uu = basis(loc, look); d = p - loc; z = d.dot(ff)
                    return Vector((360 + F * d.dot(rr) / z, 640 - F * d.dot(uu) / z))
                m = max(m, (proj(p, l0, k0) - proj(p, l1, k1)).length)
        out.append((g, m))
    return out


def runs(flags):
    o, s = [], None
    for i, fl in enumerate(flags + [False]):
        if fl and s is None: s = i
        if not fl and s is not None: o.append((s, i - 1)); s = None
    return o


qa = {"cam": {}, "pops": [], "hue": {}}
mod = None
try:
    import bpy  # noqa: F401
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
except Exception as e:                                  # pragma: no cover
    print("camera QA skipped:", e)
if mod is not None:
    for s, (a, b) in sorted(C.QA_RANGES.items()):
        camf = C.camfun(mod, s)
        sp = cam_speeds(camf, a, b, s)
        v = [m for g, m in sp]
        st = [(sp[x][0], sp[y][0] + 1) for x, y in runs([q < 0.25 for q in v]) if y - x >= 6]
        rel = [abs(v[i + 1] - v[i]) / max(v[i], 1e-6) for i in range(len(v) - 1)]
        lin = [(sp[x][0], sp[y][0] + 1) for x, y in runs([(rel[i] < 0.02 and v[i] > 1.0) for i in range(len(rel))]) if y - x >= 3]
        pk = max(sp, key=lambda x: x[1])
        qa["cam"][s] = dict(min=round(min(v), 3), median=round(sorted(v)[len(v) // 2], 2), peak=[pk[0], round(pk[1], 1)],
                            static_runs_ge6=st, constant_speed_runs_ge4=lin)
# popcheck: mean absolute frame difference (on 180x320), flag > 3.5 x the running median
prev = None; diffs = []
for g in range(C.FIRST_G, C.LAST_G + 1):
    a = np.asarray(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("L").resize((180, 320)), dtype=np.float32)
    if prev is not None:
        diffs.append((g, float(np.abs(a - prev).mean())))
    prev = a
dv = [d for g, d in diffs]
for i, (g, d) in enumerate(diffs):
    med = float(np.median(dv[max(0, i - 8):i + 9]))
    if d > max(3.5 * med, 6.0):
        qa["pops"].append([g, round(d, 2), round(med, 2)])
qa["diff_median"] = round(float(np.median(dv)), 2)
qa["near_still_runs_ge6"] = [(diffs[x][0], diffs[y][0]) for x, y in runs([d < 0.15 for d in dv]) if y - x >= 6]
import hue_report as HR
for lab, (a, b) in list(C.HUE_ROWS.items()):
    fl = [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)]
    sh, sat, val, dark = HR.stats(fl)
    qa["hue"][lab] = dict({k: round(v, 1) for k, v in sh.items()}, sat=round(sat, 2), val=round(val, 2), dark=round(dark, 2))
qa["heads"] = {}
for m in rows:
    for nm, h in (m.get("heads") or {}).items():
        d = qa["heads"].setdefault("%d:%s" % (m["shot"], nm), dict(w=[1e9, 0], y=[1e9, 0], x=[1e9, 0], below_880=0, n=0))
        d["w"] = [min(d["w"][0], h["w"]), max(d["w"][1], h["w"])]; d["y"] = [min(d["y"][0], h["y"]), max(d["y"][1], h["y"])]
        d["x"] = [min(d["x"][0], h["x"]), max(d["x"][1], h["x"])]; d["n"] += 1
        if h["y"] + h["w"] / 2 > 880 and 0 <= h["x"] <= 720:
            d["below_880"] += 1
        if "ahead" in h and h["ahead"] is not None:
            d["min_ahead_D"] = min(d.get("min_ahead_D", 1e9), h["ahead"])
qa["s_per_frame_wall"] = round(float(np.mean(walls)), 2); qa["s_per_frame_cpu"] = round(float(np.mean(cpus)), 2)
json.dump(qa, open(os.path.join(HERE, "qa.json"), "w"), indent=1)

# ---------------------------------------------------------------- meta, cues
meta = dict(C.META)
meta.update({"first_g": C.FIRST_G, "n_frames": C.LAST_G - C.FIRST_G + 1, "samples": 12, "resolution": [720, 1280], "threads": 2,
             "s_per_frame_wall_mean": qa["s_per_frame_wall"], "s_per_frame_cpu_mean": qa["s_per_frame_cpu"],
             "frame_source": {str(g): v for g, v in src.items()}})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
ev = []
for (g0, g1, kind, label, kw) in C.CUES:
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    e.update(kw); ev.append(e)
json.dump(dict(take=C.META["take"], fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- contact sheet: 16 frames, labels above the picture
n = 16; gs = [int(round(C.FIRST_G + i * (C.LAST_G - C.FIRST_G) / (n - 1.0))) for i in range(n)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:16]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

if "--no-mkv" not in sys.argv:
    mkv = os.path.join(HERE, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(C.FIRST_G), "-i",
                    os.path.join(OUT, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    pr = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                         "-of", "csv=p=0", mkv], capture_output=True, text=True)
    print("take.mkv frames:", pr.stdout.strip(), "size MB %.1f" % (os.path.getsize(mkv) / 1e6))
print("delivered %d frames g %d..%d; wall %.2f s/frame, cpu %.2f" % (len(src), C.FIRST_G, C.LAST_G, qa["s_per_frame_wall"], qa["s_per_frame_cpu"]))
print(json.dumps({k: v for k, v in qa.items() if k != "hue"}, indent=0)[:3000])
for lab, r in qa["hue"].items():
    print(lab, r)
