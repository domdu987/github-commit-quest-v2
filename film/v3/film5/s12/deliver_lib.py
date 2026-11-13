#!/usr/bin/env python3
"""deliver_lib.py -- shared delivery of takes s12 / s13 / s14: raw/s<sub>/g_*.png -> frames/g_%04d.png (hard cuts inside the take),
meta.json, cues.json, contact.jpg, compare.jpg, take.mkv, and work/qa.txt (head sizes / positions, pops, black / magenta frames,
hue rows, s per frame)."""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
LIB = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(LIB, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))


def deliver(here, take, shot, subs, g0, g1, h_in, h_out, cues, pairs, transition_in, extra_meta):
    raw = os.path.join(here, "raw"); out = os.path.join(here, "frames"); os.makedirs(out, exist_ok=True)
    first, last = g0 - h_in, g1 + h_out - 1
    src = {}
    for g in range(first, last + 1):
        sid = [s for s, S in subs.items() if S.rng[0] <= g <= S.rng[1]][0]
        shutil.copyfile(os.path.join(raw, "s%d" % sid, "g_%04d.png" % g), os.path.join(out, "g_%04d.png" % g))
        src[g] = subs[sid].name
    rows = [json.load(open(j)) for s in subs for j in glob.glob(os.path.join(raw, "s%d" % s, "g_*.json"))]
    walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
    trans = [{"at": first, "type": "in_handle", "handle": [first, g0 - 1]}] if h_in else []
    for s, S in sorted(subs.items()):
        a = max(S.rng[0], g0)
        if a > g0:
            trans.append({"at": a, "type": "cut", "to": S.name})
    trans.append({"at": g1, "type": "out", "handle": [g1, last]})
    meta = {"take": take, "film": 5, "shots": [shot], "first_g": first, "n_frames": last - first + 1, "g0": g0, "g1": g1,
            "handle_in": h_in, "handle_out": h_out, "transition_in": transition_in,
            "transition_out": {"type": "dissolve_or_cut", "frames": 12, "note": "handle g %d..%d rendered in 3D" % (g1, last)},
            "transitions": trans,
            "shot_ranges": dict([(str(shot), [g0, g1 - 1])] + [(S.name, [max(S.rng[0], g0), min(S.rng[1], g1 - 1)]) for s, S in sorted(subs.items())]),
            "dof": "none (client note: no depth of field anywhere; M.setup_dof(scene, None, None, cam=...) before every render)",
            "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST", "narration": "film5/audio/narration_bankky.wav at +0.10 s; captions film5/script/captions.json",
            "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
            "frame_source": {str(g): v for g, v in src.items()}}
    meta.update(extra_meta)
    json.dump(meta, open(os.path.join(here, "meta.json"), "w"), indent=1)
    ev = []
    for g_a, g_b, label, kind, kw in cues:
        e = dict(time=round(g_a / 30.0, 3), duration=round(max(0, g_b - g_a) / 30.0, 3), frame=int(g_a), end_frame=int(g_b), kind=kind, label=label)
        e.update(kw); ev.append(e)
    json.dump(dict(take=take, fps=30, note="time = film seconds (g / 30); narration film5/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
              open(os.path.join(here, "cues.json"), "w"), indent=1)
    # contact sheet: 16 frames
    N = last - first + 1
    gs = [first + int(round(i * (N - 1) / 15.0)) for i in range(16)]
    w, h, lab, cols = 270, 480, 18, 8
    S_ = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S_)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S_.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g]), fill=(255, 255, 255))
    S_.save(os.path.join(here, "contact.jpg"), quality=88)
    # compare: final frame beside its reference
    w, h, lab = 360, 640, 20
    C = Image.new("RGB", (len(pairs) * 2 * w + (len(pairs) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
    x = 0
    for name, g, tref in pairs:
        C.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
        dr.text((x + 4, 4), "%s  g %d (%.2f s)" % (name, g, g / 30.0), fill=(255, 255, 255))
        C.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
        dr.text((x + w + 4, 4), "ref a t%04d (%d s)" % (tref, (tref - 1) // 2), fill=(255, 220, 160))
        x += 2 * w + 12
    C.save(os.path.join(here, "compare.jpg"), quality=88)
    mkv = os.path.join(here, "take.mkv")
    if os.path.exists(mkv):
        os.remove(mkv)
    subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(out, "g_%04d.png"),
                           "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv])
    qa(here, take, subs, out, first, last)
    print("delivered %s: %d frames g %d..%d; mean wall %.2f s, cpu %.2f s" % (take, N, first, last, np.mean(walls), np.mean(cpus)))


def qa(here, take, subs, out, first, last):
    import hue_report as H
    lines = []
    P = lines.append
    for s, S in sorted(subs.items()):
        rows = sorted([json.load(open(f)) for f in glob.glob(os.path.join(here, "raw", "s%d" % s, "g_*.json"))], key=lambda r: r["g"])
        P("sub %s (g %d..%d, %d frames)" % (S.name, S.rng[0], S.rng[1], len(rows)))
        for n in sorted({n for r in rows for n in r["heads"]}):
            hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
            w = [x["w"] for g, x in hs]; y = [x["y"] for g, x in hs]; xx = [x["x"] for g, x in hs]
            low = [g for g, x in hs if x["y"] + x["w"] / 2 > 880]
            P("  %-7s head w %5.0f..%5.0f px, centre x %5.0f..%5.0f, centre y %5.0f..%5.0f (%.2f..%.2f H); head bottom below 880: %s"
              % (n, min(w), max(w), min(xx), max(xx), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
        if rows:
            P("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                                              [r["g"] for r in rows if r.get("retried")]))
    fs = [os.path.join(out, "g_%04d.png" % g) for g in range(first, last + 1)]
    prev = None; d = []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    pops = []
    for i, v in enumerate(d):
        p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
        if v > 1.8 * p and v > 1.8 * n and v > 1.0:
            pops.append((first + i, first + i + 1, round(v, 1)))
    P("popcheck: pops (g -> g+1, change): %s" % pops)
    P("near-still transitions (< 0.35 levels): %s" % [first + i for i, v in enumerate(d) if v < 0.35])
    still = 0; run = 0
    for v in d:
        run = run + 1 if v < 0.15 else 0; still = max(still, run)
    P("longest run of identical-looking frames (< 0.15 levels): %d" % still)
    bad = []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
        mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean(); blk = (a.max(axis=2) < 6).mean()
        if mag > 0.002 or blk > 0.2:
            bad.append(os.path.basename(f))
    P("magenta / black frames: %s" % bad)
    txt = "\n".join(lines)
    os.makedirs(os.path.join(here, "work"), exist_ok=True)
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
        for s, S in sorted(subs.items()):
            a, b = max(S.rng[0], first), min(S.rng[1], last)
            H.row("%s %s (g %d-%d)" % (take, S.name, a, b), fs[a - first:b - first + 1])
        H.row("%s all (g %d-%d)" % (take, first, last), fs)
    txt += "\n\n" + buf.getvalue()
    open(os.path.join(here, "work", "qa.txt"), "w").write(txt)
    print(txt)
