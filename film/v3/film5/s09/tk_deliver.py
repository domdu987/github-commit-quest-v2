#!/usr/bin/env python3
"""tk_deliver.py -- delivery engine for takes s08 / s09 / s11 (team 2): from raw/<seg>/g_*.png build frames/g_%04d.png (dissolves mixed
with the smoothstep of v2/shots/anim.py), meta.json, cues.json, contact.jpg, compare.jpg, take.mkv and work/qa.txt.
Each take's deliver.py passes a CFG dict to run(CFG)."""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v2", "shots"))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
from anim import smoothstep_mix          # noqa: E402
import hue_report as HR                  # noqa: E402

RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "frames")


def raw(seg, g):
    return os.path.join(RAW, seg, "g_%04d.png" % g)


def build_frames(C):
    os.makedirs(OUT, exist_ok=True)
    src = {}
    first, last = C["g0"] - C["handle_in"], C["g1"] + C["handle_out"] - 1
    for g in range(first, last + 1):
        dst = os.path.join(OUT, "g_%04d.png" % g)
        mixed = False
        for d in C.get("dissolves", []):
            m0 = d["at"] - d["frames"] // 2
            if m0 <= g < m0 + d["frames"]:
                w = smoothstep_mix(g - m0 + 1, d["frames"])
                a = np.asarray(Image.open(raw(d["from"], g)).convert("RGB"), dtype=np.float32)
                b = np.asarray(Image.open(raw(d["to"], g)).convert("RGB"), dtype=np.float32)
                Image.fromarray(np.clip(a * (1 - w) + b * w + 0.5, 0, 255).astype(np.uint8)).save(dst)
                src[g] = "%s*%.3f+%s*%.3f" % (d["from"], 1 - w, d["to"], w)
                mixed = True
        if not mixed:
            seg = [s for s, g0 in C["segs"] if g >= g0][-1]
            shutil.copyfile(raw(seg, g), dst)
            src[g] = seg
    return src, first, last


def run(C):
    src, first, last = build_frames(C)
    n = last - first + 1
    rows = {}
    for js in glob.glob(os.path.join(RAW, "*", "g_*.json")):
        m = json.load(open(js)); rows[(m["shot"], m["g"])] = m
    used = [rows[(s, g)] for g, s in src.items() if (s, g) in rows]
    walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]
    meta = dict(take=C["take"], film=5, shots=C["shots"], first_g=first, n_frames=n, g0=C["g0"], g1=C["g1"],
                handle_in=C["handle_in"], handle_out=C["handle_out"], transition_in=C["transition_in"],
                transition_out=C["transition_out"], transitions=C["transitions"], shot_ranges=C["shot_ranges"],
                set=C["set"], dof="none (client rule: no depth of field anywhere; M.setup_dof(scene, None, None, cam=...) before every render)",
                denoiser="OpenImageDenoise, albedo+normal, prefilter FAST",
                narration="film5/audio/narration_bankky.wav at +0.10 s; captions film5/script/captions.json",
                light="LAMP (tunnel)", cast=C["cast"], cage=C["cage"], samples=12, resolution=[720, 1280], threads=2,
                raw_frames_rendered=len(rows),
                s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
                frame_source={str(g): v for g, v in sorted(src.items())})
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

    ev = []
    for c in C["cues"]:
        g0, g1, label, kind = c[:4]
        kw = c[4] if len(c) > 4 else {}
        e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
        e.update(kw); ev.append(e)
    json.dump(dict(take=C["take"], fps=30, note="time = film seconds (g / 30); narration PROJ/film5/audio/narration_bankky.wav at +0.10 s, captions.json",
                   cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

    gs = [first + int(round(i * (n - 1) / 15.0)) for i in range(16)]
    w, h, lab, cols = 270, 480, 18, 8
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:16]), fill=(255, 255, 255))
    S.save(os.path.join(HERE, "contact.jpg"), quality=88)

    P = C["pairs"]
    w, h, lab = 360, 640, 20
    Cm = Image.new("RGB", (len(P) * 2 * w + (len(P) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
    x = 0
    for shot, g, tref in P:
        Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
        dr.text((x + 4, 4), "shot %s  g %d (%.2f s)" % (shot, g, g / 30.0), fill=(255, 255, 255))
        Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
        dr.text((x + w + 4, 4), "ref a t%04d (%d s)" % (tref, (tref - 1) // 2), fill=(255, 220, 160))
        x += 2 * w + 12
    Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

    mkv = os.path.join(HERE, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    qa(C, src, first, last, rows)
    print("delivered %d frames g %d..%d; mean wall %.2f s, cpu %.2f s" % (n, first, last, np.mean(walls), np.mean(cpus)))


def qa(C, src, first, last, rows):
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    out = open(os.path.join(HERE, "work", "qa.txt"), "w")
    old = sys.stdout; sys.stdout = out
    try:
        for seg, (a, b) in C["seg_ranges"].items():
            rs = sorted([r for (s, g), r in rows.items() if s == seg and a <= g <= b], key=lambda r: r["g"])
            print("segment %s (g %d..%d, %d frames)" % (seg, a, b, len(rs)))
            for nme in sorted({k for r in rs for k in r["heads"]}):
                hs = [(r["g"], r["heads"][nme]) for r in rs if nme in r["heads"]]
                wv = [hh["w"] for _, hh in hs]; yv = [hh["y"] for _, hh in hs]; xv = [hh["x"] for _, hh in hs]
                low = [g for g, hh in hs if hh["y"] + hh["w"] / 2 > 880]
                print("  %-7s head w %5.0f..%5.0f px, centre x %4.0f..%4.0f, centre y %4.0f..%4.0f (%.2f..%.2f H); head bottom below 880: %s"
                      % (nme, min(wv), max(wv), min(xv), max(xv), min(yv), max(yv), min(yv) / 1280, max(yv) / 1280,
                         (low[0], low[-1], len(low)) if low else "none"))
            if rs:
                print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rs]),
                      np.mean([r["cpu"] for r in rs]), [r["g"] for r in rs if r.get("retried")]))
        fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(first, last + 1)]
        prev = None; d = []
        for f in fs:
            a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
            if prev is not None:
                d.append(float(np.abs(a - prev).mean()))
            prev = a
        pops = []
        for i, v in enumerate(d):
            p = d[i - 1] if i else v; nx = d[i + 1] if i + 1 < len(d) else v
            if v > 1.8 * p and v > 1.8 * nx and v > 1.0:
                pops.append((first + i, first + i + 1, round(v, 1)))
        print("popcheck (g -> g+1, change):", pops)
        still = [first + i for i, v in enumerate(d) if v < 0.35]
        print("near-still transitions (< 0.35 levels):", still)
        bad = []
        for f in fs:
            a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
            mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean()
            blk = (a.max(axis=2) < 6).mean()
            if mag > 0.002 or blk > 0.2:
                bad.append(os.path.basename(f))
        print("magenta / black frames:", bad)
        print()
        print(f"{'set':44s} " + " ".join(f"{nm[:6]:>6s}" for nm in HR.NAMES) + "   sat  val dark")
        fr = lambda a, b: [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)]
        for seg, (a, b) in C["seg_ranges"].items():
            HR.row("%s %s (g %d-%d)" % (C["take"], seg, max(a, first), min(b, last)), fr(max(a, first), min(b, last)))
        HR.row("%s all (g %d-%d)" % (C["take"], first, last), fr(first, last))
        R = os.path.join(PROJ, "ref", "a")
        HR.row("ref a " + " ".join("t%04d" % t for _, _, t in C["pairs"]), [os.path.join(R, "t%04d.jpg" % t) for _, _, t in C["pairs"]])
    finally:
        sys.stdout = old
        out.close()
    print(open(os.path.join(HERE, "work", "qa.txt")).read())
