#!/usr/bin/env python3
"""deliver3.py -- delivery of a film-3 take of render team 2 (identical copy in s06, s08, s09; the take is the folder name).
From raw/s<k>/g_*.png (+ json) build frames/g_%04d.png (internal dissolves mixed with the smoothstep of film 2), take.mkv
(ffmpeg libx264rgb crf 6), meta.json, cues.json, contact.jpg and work/qa.txt (staging numbers, camera speed, pops, hue rows).
    python3 deliver3.py [--no-mkv]"""
import os, sys, json, glob, math, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
TAKE = os.path.basename(HERE)
V3 = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(V3, "tools")); sys.path.insert(0, os.path.join(os.path.dirname(V3), "v2", "shots")); sys.path.insert(0, HERE)
from anim import smoothstep_mix                          # noqa: E402
import hue_report as HR                                  # noqa: E402

t = lambda g: round(g / 30.0, 3)
TAKES = {
    "s06": dict(shots=[6, 7], g0=422, g1=620, h_in=7, h_out=0,
                tin={"type": "dissolve", "frames": 10, "note": "in-handle g 415..421 rendered in 3D (shot 6 camera runs back)"},
                tout={"type": "cut", "frames": 0},
                segs=[(415, 537, 6), ("mix", 538, 546, 6, 7), (547, 619, 7)],
                shot_ranges={"6": [422, 541], "7": [542, 619]},
                internal=[{"at": 542, "type": "dissolve", "frames": 9, "mixed": [538, 546], "from_shot": 6, "to_shot": 7,
                           "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 6 to g 548, shot 7 from g 536 (raw/)"}],
                state="paint 0 (grey steel), seep 0.75 (shot 6) and 0.35 -> 1 (shot 7), bucket at bucket_mark fill 0.5"),
    "s08": dict(shots=[8], g0=620, g1=747, h_in=0, h_out=6,
                tin={"type": "cut", "frames": 0}, tout={"type": "dissolve", "frames": 9, "note": "out-handle g 747..752 rendered in 3D (shot 8 camera continues)"},
                segs=[(620, 752, 8)], shot_ranges={"8": [620, 746]}, internal=[],
                state="paint 0, seep 0.8, bucket at bucket_mark fill 0.55"),
    "s09": dict(shots=[9, 10], g0=747, g1=918, h_in=6, h_out=8,
                tin={"type": "dissolve", "frames": 9, "note": "in-handle g 741..746 rendered in 3D (shot 9 camera runs back)"},
                tout={"type": "dissolve", "frames": 12, "note": "out-handle g 918..925 rendered in 3D (shot 10 camera continues)"},
                segs=[(741, 779, 9), (780, 831, 19), ("mix", 832, 841, 19, 10), (842, 925, 10)],
                shot_ranges={"9": [747, 836], "10": [837, 917]},
                internal=[{"at": 780, "type": "cut", "from": "shot 9 painting", "to": "shot 9 cut-in (tommy sneaks the bucket back)"},
                          {"at": 837, "type": "dissolve", "frames": 10, "mixed": [832, 841], "from_shot": 9, "to_shot": 10,
                           "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 9 cut-in to g 843 (raw/s19), shot 10 from g 830"}],
                state="9a paint 0 -> 0.142 (z -0.5 -> 3.4: brown climbs past the first seam), 9b paint 1, bucket carried in and set at bucket_mark, fill 0.08 -> 0.13; 10 paint 1, seep 1"),
}
C = TAKES[TAKE]
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "frames")


def raw(k, g):
    return os.path.join(RAW, "s%d" % k, "g_%04d.png" % g)


def build_frames():
    os.makedirs(OUT, exist_ok=True)
    src = {}
    for seg in C["segs"]:
        if seg[0] == "mix":
            _, a, b, ka, kb = seg; n = b - a + 1
            for g in range(a, b + 1):
                w = smoothstep_mix(g - a + 1, n)
                A = np.asarray(Image.open(raw(ka, g)).convert("RGB"), dtype=np.float32)
                B = np.asarray(Image.open(raw(kb, g)).convert("RGB"), dtype=np.float32)
                Image.fromarray(np.clip(A * (1 - w) + B * w + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(OUT, "g_%04d.png" % g))
                src[g] = "s%d*%.3f+s%d*%.3f" % (ka, 1 - w, kb, w)
        else:
            a, b, k = seg
            for g in range(a, b + 1):
                shutil.copyfile(raw(k, g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = "s%d" % k
    return src


def cues():
    ev = []

    def add(g0, g1, label, kind, **kw):
        e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)

    import shot as S
    if TAKE == "s06":
        add(415, 548, "dock ambience at the tank foot: harbour gulls far, a distant steam winch, the filling pipe hums", "ambience")
        add(415, 548, "molasses pumping through the filling pipe (low gurgle inside the tank, bed under shot 6)", "pipe")
        add(471, 483, "snap reframe onto tommy (short whoosh in)", "camera_snap", peak_frame=477, peak_time=t(477))
        add(478, 486, "tommy cups his hand behind his ear (cloth rustle)", "gesture")
        for g in S.GROANS:
            add(g, g + 24, "the tank groans: deep metallic creak of the riveted plates (camera jolts)", "groan", impact_frame=g)
        add(536, 619, "drip: molasses drops forming and falling into the bucket", "ambience")
        for g in range(536, 620):
            if (g + 3) % 24 == 0:
                add(g, g, "drip: a thick drop lands in the molasses in the bucket (soft heavy plop)", "drip", impact_frame=g)
        add(538, 546, "dissolve to the seam insert", "dissolve")
        add(550, 619, "slow viscous seeping (wet creak, very soft)", "seep")
    elif TAKE == "s08":
        add(620, 620, "hard cut to the foreman laughing", "cut")
        add(620, 666, "the foreman's big belly laugh (no words: 'ha ha ha'); the workers behind laugh too", "laugh")
        add(620, 752, "dock workers laughing in the background, dock ambience", "ambience")
        add(657, 667, "snap reframe onto the foreman (whoosh in), lands g 663", "camera_snap", peak_frame=663, peak_time=t(663))
        add(666, 741, "the foreman's quoted line (mouth moves g 666..741)", "dialogue")
        add(706, 714, "he points at the tank (sleeve whip)", "gesture")
    else:
        add(741, 779, "brushes slapping paint on the steel (wet strokes, three brushes out of step)", "brush")
        add(741, 779, "dock ambience at the tank foot", "ambience")
        add(780, 780, "hard cut-in: tommy sneaks the bucket back", "cut")
        add(780, 794, "tin bucket set down on the cobbles (soft clank of the bail)", "bucket", impact_frame=794)
        add(800, 830, "tommy glances left, then right (tiny sneaky rustles)", "gesture")
        for g in range(780, 844):
            if g >= S.RELEASE and (g + 7) % 22 == 0:
                add(g, g, "drip: a drop lands in the bucket (plop)", "drip", impact_frame=g)
        add(832, 841, "dissolve to Commercial Street", "dissolve")
        add(830, 925, "dock workers laughing and pointing at the tank, street ambience", "laugh")
        add(887, 893, "crash zoom onto the sweating seam (fast whoosh), lands g 891 on the nickname", "camera_snap", peak_frame=891, peak_time=t(891))
        add(893, 925, "drips on the sweating seam (soft plops), laughter fades under", "drip")
    return ev


def contact(src, gs):
    w, h, lab, cols = 270, 480, 18, 8
    rows = (len(gs) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:14]), fill=(255, 255, 255))
    S.save(os.path.join(HERE, "contact.jpg"), quality=88)


def qa(src):
    out = []
    P = lambda *a: out.append(" ".join(str(x) for x in a))
    for k in sorted({s[2] for s in C["segs"] if s[0] != "mix"}):
        rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(RAW, "s%d" % k, "g_*.json")))]
        used = [r for r in rows if src.get(r["g"], "").find("s%d" % k) >= 0]
        if not used:
            continue
        P("shot key %d: %d frames used (g %d..%d)" % (k, len(used), used[0]["g"], used[-1]["g"]))
        names = sorted({n for r in used for n in r["heads"]})
        for n in names:
            hs = [(r["g"], r["heads"][n]) for r in used if n in r["heads"]]
            on = [(g, h) for g, h in hs if -100 < h["x"] < 820 and h["y"] < 1400]
            if not on:
                P("  %-8s off screen" % n); continue
            w = [h["w"] for g, h in on]; y = [h["y"] for g, h in on]; x = [h["x"] for g, h in on]
            low = [g for g, h in on if h["bottom"] > 880 and 0 < h["x"] < 720]
            P("  %-8s on screen %3d frames: head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %.3f..%.3f H, flip %s; head bottom below 880 (in frame): %s"
              % (n, len(on), min(w), max(w), min(x), max(x), min(y) / 1280, max(y) / 1280, sorted({h["flip"] for g, h in on}), (low[0], low[-1], len(low)) if low else "none"))
        errs = {}
        for r in used:
            for n, d in r.get("hands_err", {}).items():
                for s_, e in d.items():
                    errs.setdefault(n + "." + s_, []).append(e)
        for kk, v in errs.items():
            P("  pin %-12s error max %.3f D, mean %.3f D, frames > 0.05 D: %d" % (kk, max(v), float(np.mean(v)), sum(1 for e in v if e > 0.05)))
        P("  render: wall %.2f s, cpu %.2f s per frame (mean of %d)" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]), len(rows)))
        P("  retried frames: %s" % [r["g"] for r in rows if r.get("retried")])
    # camera speed from the shot functions (fastest of 9 screen points at depth 8 D), static / constant-speed runs
    import shot as S
    from mathutils import Vector
    F = 782.22
    for k, sh in S.SHOTS.items():
        a, b = sh["rng"]
        sp = []
        for g in range(a, b):
            r0 = sh["cam"](g); r1 = sh["cam"](g + 1)
            l0, k0 = Vector(r0[0]), Vector(r0[1]); l1, k1 = Vector(r1[0]), Vector(r1[1])
            f0 = F * (r0[2] if len(r0) > 2 else 22.0) / 22.0; f1 = F * (r1[2] if len(r1) > 2 else 22.0) / 22.0

            def basis(l, kk):
                f = (kk - l).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); return f, r, r.cross(f)

            def proj(p, l, kk, ff):
                f, r, u = basis(l, kk); d = p - l; z = d.dot(f); return Vector((360 + ff * d.dot(r) / z, 640 - ff * d.dot(u) / z))
            f, r, u = basis(l0, k0)
            m = 0.0
            for sx in (-1, 0, 1):
                for sy in (-1, 0, 1):
                    p = l0 + (f + r * (sx * 360 / f0) + u * (sy * 640 / f0)) * 8.0
                    m = max(m, (proj(p, l0, k0, f0) - proj(p, l1, k1, f1)).length)
            sp.append((g, m))
        v = [m for g, m in sp]
        static = [g for g, m in sp if m < 0.25]
        P("camera shot key %d: px/frame min %.2f median %.2f peak %.1f (g %d); frames under 0.25 px: %d" % (k, min(v), float(np.median(v)), max(v), sp[int(np.argmax(v))][0], len(static)))
    # pops: mean abs frame difference
    gs = sorted(src)
    prev = None; d = []
    for g in gs:
        a = np.asarray(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("L").resize((180, 320)), dtype=np.float32)
        if prev is not None:
            d.append((g, float(np.abs(a - prev).mean())))
        prev = a
    vv = np.array([x for g, x in d]); med = float(np.median(vv))
    P("frame-to-frame mean abs diff (180x320 luma): median %.2f, max %.2f at g %d" % (med, vv.max(), d[int(vv.argmax())][0]))
    P("pops (> 4 x median and > 6): %s" % [(g, round(x, 1)) for g, x in d if x > max(6.0, 4 * med)])
    P("near-still transitions (< 0.15): %s" % [g for g, x in d if x < 0.15])
    P("hue rows:")
    return "\n".join(out)


def hue_rows(src):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
        for k, (a, b) in C["shot_ranges"].items():
            HR.row("%s shot %s (g %d-%d)" % (TAKE, k, a, b), [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)])
        gs = sorted(src)
        HR.row("%s all (g %d-%d)" % (TAKE, gs[0], gs[-1]), [os.path.join(OUT, "g_%04d.png" % g) for g in gs])
    return buf.getvalue()


if __name__ == "__main__":
    src = build_frames()
    gs = sorted(src)
    if "--no-mkv" not in sys.argv:
        mk = os.path.join(HERE, "take.mkv")
        if os.path.exists(mk):
            os.remove(mk)
        subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-start_number", str(gs[0]), "-i",
                               os.path.join(OUT, "g_%04d.png"), "-frames:v", str(len(gs)), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mk])
    rows = [json.load(open(f)) for f in glob.glob(os.path.join(RAW, "s*", "g_*.json"))]
    meta = {"take": TAKE, "shots": C["shots"], "g0": C["g0"], "g1": C["g1"], "handle_in": C["h_in"], "handle_out": C["h_out"],
            "first_g": gs[0], "n_frames": len(gs), "transition_in": C["tin"], "transition_out": C["tout"], "internal": C["internal"],
            "shot_ranges": C["shot_ranges"], "set": "v3/set3d3/harbor.py", "light": "WINTER", "set_state": C["state"],
            "cast": "v3/cast3", "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(float(np.mean([r["wall"] for r in rows])), 2),
            "s_per_frame_cpu_mean": round(float(np.mean([r["cpu"] for r in rows])), 2),
            "encode": "ffmpeg -framerate 30 -start_number %d -i frames/g_%%04d.png -c:v libx264rgb -crf 6 -preset slow take.mkv" % gs[0],
            "frame_source": {str(g): v for g, v in src.items()}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
    json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=cues()),
              open(os.path.join(HERE, "cues.json"), "w"), indent=1)
    n = 16
    contact(src, [gs[int(round(i * (len(gs) - 1) / (n - 1.0)))] for i in range(n)])
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    txt = qa(src) + "\n" + hue_rows(src)
    open(os.path.join(HERE, "work", "qa.txt"), "w").write(txt)
    print(txt)
    print("delivered %s: %d frames g %d..%d" % (TAKE, len(gs), gs[0], gs[-1]))
