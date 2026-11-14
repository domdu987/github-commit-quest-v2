#!/usr/bin/env python3
"""deliver.py -- raw/s8 (shot 8, g 602..719) + raw/s9 (shot 9, g 720..786) -> frames/g_%04d.png, meta.json, cues.json, contact.jpg,
compare.jpg, take.mkv (libx264rgb crf 6), work/qa.txt (heads, popcheck, magenta/black, hue rows).   python3 deliver.py"""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))

TAKE = "s08"
SHOTS = {8: (602, 719), 9: (720, 786)}          # rendered ranges per set-up (incl. handles)
PLAN = {8: (608, 719), 9: (720, 780)}            # plan shot ranges
G0, G1, HANDLE = 608, 781, 6
FIRST, LAST = 602, 786
TRANS_IN = {"type": "dissolve", "frames": 8, "note": "from shot 7 (bazaar, NOON) into the dawn desert time-lapse; in-handle g 602..607 rendered in 3D (wall already rising)"}
TRANS_OUT = {"type": "cut", "frames": 0, "note": "plan: shot 10 (NIGHT channel_ecu) follows at g 781; out-handle g 781..786 rendered in 3D (push continues, dome complete)"}
EVENTS = {"wall_rises_timelapse": [602, 712], "brick_cycle_every_15_frames": [602, 719], "cut_to_dome": 720,
          "dome_grows_timelapse": [718, 762], "farid_proud_at_dome": [720, 786]}
SETUPS = {"8": {"g": [602, 719], "set": "desert_ice plain (wall_low build), DAWN with the key turned to the north-east (travel (-0.55,-0.83), 11 deg) so the wall's north face is lit warm; ice 'water'; wall mesh keyed into the ground and rising 2.2 -> 15 D; custom camera from the north-west looking ESE (az 120 -> 124, pitch 2.5 -> 6.5), 20 mm, push + crane"},
          "9": {"g": [720, 786], "set": "desert_ice plain (wall_low build, separate process), DAWN with the key from the north-west (travel (0.62,-0.78), 13 deg) lighting the dome's face, the painted sunrise behind it; ice (0.06, 0) faint frost; dome + vent z-scale 0.62 -> 1; camera from the west looking east (az 79 -> 80.5, pitch 8.5), 22 mm, push + crane"}}
CAST = "v3/cast8: farid (shot 8: time-lapse brick cycle built from farid_build_wall: crouch to the pile -> heave a mud_brick (panel_grip bottom) up to the wall, 15 frames per brick, sweat on and off; shot 9: farid_smile, arms folded, idle sway)"
SETNOTE = ("v3/set3d8/desert.py desert_ice plain, DAWN (key direction overridden per set-up at runtime through D.LIGHTS['DAWN'] before build); "
           "set_ice keyed per frame, set_flames + set_stars keyed per frame; runtime additions from shot.py: the 'wall' object keyed in z (rises out of "
           "the ground), 'dome' + 'dome_vent' keyed z scale, s08_dress (mud-brick stacks, mould, mud heap, straw, bucket, jars, basket, palms, shrubs, rocks by the dome)")
CUES = [(602, 786, "ambience", "dawn desert, cool morning wind over sand, a few early birds; a light quick time-lapse pulse (plucked strings / ticking) under the montage"),
        (602, 719, "foley", "time-lapse: rapid repeated thud-thud of mud bricks being stacked (one every half second), sped-up shuffles and scrapes", {"peak_frame": 610}),
        (602, 712, "accent", "rising whoosh / ascending tone as the wall climbs to three storeys", {"peak_frame": 712}),
        (712, 719, "accent", "the wall tops out: a solid low 'thoom' settle", {"peak_frame": 713}),
        (720, 720, "cut", "cut to the dome", {}),
        (718, 762, "accent", "soft rising swell as the giant dome finishes growing", {"peak_frame": 760}),
        (762, 786, "accent", "warm sustained chord: the finished dome glowing at sunrise, farid proud", {"peak_frame": 770})]
COMPARE = [(690, 61, "a"), (770, 61, "a")]
HUE = [("s08 shot 8 wall time-lapse (g 608-719)", 608, 719), ("s08 shot 9 dome (g 720-780)", 720, 780), ("s08 all (g 602-786)", 602, 786)]
REFS = [("ref a t0061 (sunrise)", "a", (61,))]


def main():
    OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
    rows, src = [], {}
    for sid, (a, b) in SHOTS.items():
        for g in range(a, b + 1):
            raw = os.path.join(HERE, "raw", "s%d" % sid)
            shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
            rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
    N = LAST - FIRST + 1
    walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
    by = {str(s): {"wall": round(float(np.mean([m["wall"] for m in rows if m["shot"] == s])), 2),
                   "cpu": round(float(np.mean([m["cpu"] for m in rows if m["shot"] == s])), 2)} for s in SHOTS}
    meta = {"take": TAKE, "film": 8, "shots": sorted(SHOTS), "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
            "handle_in": G0 - FIRST, "handle_out": LAST - G1 + 1, "transition_in": TRANS_IN, "transition_out": TRANS_OUT,
            "shot_ranges": {str(k): list(v) for k, v in PLAN.items()}, "setups": SETUPS, "events": EVENTS, "set": SETNOTE,
            "dof": "none (client rule: cam.data.dof.use_dof False + D.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST", "narration": "film8/audio/narration.wav at +0.10 s; captions film8/script/captions.json",
            "cast": CAST, "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
            "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2), "s_per_frame_by_setup": by,
            "frame_source": {str(g): v for g, v in sorted(src.items())}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
    ev = []
    for c in CUES:
        g0, g1, kind, label = c[:4]; kw = c[4] if len(c) > 4 else {}
        e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label); e.update(kw); ev.append(e)
    json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film8/audio/narration.wav at +0.10 s, captions.json", cues=ev),
              open(os.path.join(HERE, "cues.json"), "w"), indent=1)
    # contact sheet
    gs = [int(round(FIRST + i * (N - 1) / 15.0)) for i in range(16)]
    w, h, lab, cols = 270, 480, 18, 8
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        tag = " handle" if (g < G0 or g >= G1) else ""
        dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s%s" % (g, g / 30.0, src[g], tag), fill=(255, 255, 255))
    S.save(os.path.join(HERE, "contact.jpg"), quality=88)
    w, h, lab = 360, 640, 20
    Cm = Image.new("RGB", (len(COMPARE) * 2 * w + (len(COMPARE) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
    x = 0
    for g, tref, rs in COMPARE:
        Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
        dr.text((x + 4, 4), "shot %s  g %d (%.2f s)" % (src[g], g, g / 30.0), fill=(255, 255, 255))
        Cm.paste(Image.open(os.path.join(PROJ, "ref", rs, "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
        dr.text((x + w + 4, 4), "ref %s t%04d" % (rs, tref), fill=(255, 220, 160))
        x += 2 * w + 12
    Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)
    mkv = os.path.join(HERE, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    sz = os.path.getsize(mkv)
    for p in glob.glob(mkv + ".part*"):
        os.remove(p)
    if sz > 45e6:
        subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
    # QA numbers
    q = []
    for sid in SHOTS:
        rs = [r for r in rows if r["shot"] == sid]
        for n in sorted({n for r in rs for n in r.get("heads", {})}):
            hs = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"]]
            ww = [hh["w"] for _, hh in hs]; yy = [hh["y"] for _, hh in hs]; xx = [hh["x"] for _, hh in hs]
            low = [g for g, hh in hs if hh["y"] + hh["w"] / 2 > 880]
            q.append("shot %d %s: head w %.0f..%.0f px, centre x %.0f..%.0f, y %.0f..%.0f (%.2f..%.2f H); bottom below 880: %s"
                     % (sid, n, min(ww), max(ww), min(xx), max(xx), min(yy), max(yy), min(yy) / 1280, max(yy) / 1280, (low[0], low[-1], len(low)) if low else "none"))
    q.append("render: wall %.2f s, cpu %.2f s per frame (mean); by set-up %s; retried %s" % (np.mean(walls), np.mean(cpus), by, [r["g"] for r in rows if r.get("retried")]))
    fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(FIRST, LAST + 1)]
    prev, d = None, []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    pops = []
    for i, v in enumerate(d):
        p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
        if v > 1.8 * p and v > 1.8 * n and v > 1.0:
            pops.append((FIRST + i, FIRST + i + 1, round(v, 1)))
    still = [FIRST + i for i, v in enumerate(d) if v < 0.35]
    runs, cur = [], []
    for g in still:
        if cur and g == cur[-1] + 1:
            cur.append(g)
        else:
            if len(cur) > 1: runs.append((cur[0], cur[-1]))
            cur = [g]
    if len(cur) > 1: runs.append((cur[0], cur[-1]))
    q.append("popcheck: pops %s; near-still transitions (< 0.35 levels) %d, runs %s; change median %.2f max %.2f" % (pops, len(still), runs, float(np.median(d)), max(d)))
    bad = []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
        if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
            bad.append(os.path.basename(f))
    q.append("magenta / black frames: %s" % bad)
    q.append("take.mkv %.1f MB" % (sz / 1e6))
    open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(q) + "\n")
    print("\n".join(q))
    try:
        import hue_report as H
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
            for name, a, b in HUE:
                H.row(name, [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)])
            for name, rs, ts in REFS:
                H.row(name, [os.path.join(PROJ, "ref", rs, "t%04d.jpg" % t) for t in ts])
        open(os.path.join(HERE, "work", "hue.txt"), "w").write(buf.getvalue()); print(buf.getvalue())
    except Exception as e:
        print("hue rows failed:", e)


if __name__ == "__main__":
    main()
