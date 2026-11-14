#!/usr/bin/env python3
"""deliver.py -- raw/s10 (g 775..839) + raw/s11 (g 840..881) + raw/s12 (g 882..969) -> frames/g_%04d.png, meta.json, cues.json, contact.jpg,
compare.jpg, take.mkv (libx264rgb crf 6), work/qa.txt (heads, popcheck, magenta/black, hue rows).   python3 deliver.py"""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))

TAKE = "s10"
SHOTS = {10: (775, 839), 11: (840, 881), 12: (882, 969)}  # rendered ranges per set-up (incl. handles)
PLAN = {10: (781, 839), 11: (840, 881), 12: (882, 963)}
G0, G1, HANDLE = 781, 964, 6
FIRST, LAST = 775, 969
TRANS_IN = {"type": "cut", "frames": 0, "note": "plan cut from shot 9 (dome at dawn) to night 1; in-handle g 775..780 rendered in 3D (open water, push already moving)"}
TRANS_OUT = {"type": "cut", "frames": 0, "note": "plan: shot 13 (NOON channels_wide, farid oversleeps) follows at g 964; out-handle g 964..969 rendered in 3D (the carry walk continues)"}
EVENTS = {"night1_open_water": [775, 789], "freezes_to_thin_sheet": [790, 830], "cut_night10": 840, "finger_taps": [850, 858, 866],
          "pleased_smile": [870, 881], "cut_dawn_wide": 882, "saws_block": [882, 911], "lifts_block": [912, 921], "carries_toward_dome": [922, 969]}
SETUPS = {"10": {"g": [775, 839], "set": "desert_ice plain (channel_ecu build), NIGHT, ice keyed 0 -> 0.25 (g 790..830); low camera over channel 3 (y 7.4, no sawn hole) looking east (az 80, pitch -6 -> -5), 22 mm, slow push 1.1 D; no actor"},
          "11": {"g": [840, 881], "set": "desert_ice plain (channel_ecu build), NIGHT, ice 1.0 (thick); farid crouched on the north bank of channel 3 (1.55, 8.78), right index finger pinned to the ice point (2.75, 7.75) via actors.world_to_local; camera over channel 3 (az 66 -> 70, pitch -4), 22 mm, push + orbit"},
          "12": {"g": [882, 969], "set": "desert_ice plain (channels_wide build, separate process), DAWN with the key from the north-west (as s08 shot 9), ice 'thick'; farid on the south bank of channel 2 at the sawn hole, saws (mirrored farid_saw), lifts, walks east with an ice block; camera over channel 3 from the west (az 108.5 -> 106, pitch -4 -> -3), 20 mm, push"}}
CAST = "v3/cast8: farid (shot 11: crouch + pointing right hand pinned to the ice, 3 taps, excited -> happy; shot 12: farid_saw (mirror, saw stroke every 10 frames) -> farid_carry_ice rising from the crouch -> cycle walk (facing -1, arms none) carrying the ice block)"
SETNOTE = ("v3/set3d8/desert.py desert_ice plain, NIGHT (shots 10-11) / DAWN with runtime key direction (shot 12); set_ice keyed per frame, set_flames + "
           "set_stars keyed per frame; runtime additions from shot.py: s10_dress (shot 11: bucket, jar, rock on the banks; shot 12: three cut ice blocks "
           "on the bank, straw, plank, bucket, jar)")
CUES = [(775, 881, "ambience", "desert night, deep quiet, faint cold wind, distant crickets; a crystalline high pad"),
        (790, 830, "accent", "freezing: delicate crackling / tinkling of ice crystals spreading over the water", {"peak_frame": 812}),
        (840, 840, "cut", "cut to night ten (ambience continues, colder)", {}),
        (850, 850, "foley", "fingertip tap on thick ice: a solid 'tok'", {"peak_frame": 850}),
        (858, 858, "foley", "second tap 'tok'", {"peak_frame": 858}),
        (866, 866, "foley", "third tap 'tok' (on 'หนาเท่านิ้ว')", {"peak_frame": 866}),
        (870, 881, "accent", "pleased little 'hm!' sting", {"peak_frame": 872}),
        (882, 969, "ambience", "pre-dawn to sunrise desert: cool wind, first birds, a warm rising pad"),
        (882, 911, "foley", "ice saw rasping through thick ice, rhythmic strokes every third of a second", {"peak_frame": 890}),
        (912, 921, "foley", "the block cracks free and is lifted with a grunt, water drips", {"peak_frame": 914}),
        (922, 969, "foley", "footsteps on packed earth carrying the heavy block, a slight strain", {"peak_frame": 935})]
COMPARE = [(812, 72, "a"), (860, 83, "a"), (930, 61, "a")]
HUE = [("s10 shot 10 freeze (g 781-839)", 781, 839), ("s10 shot 11 tap (g 840-881)", 840, 881), ("s10 shot 12 dawn carry (g 882-963)", 882, 963), ("s10 all (g 775-969)", 775, 969)]
REFS = [("ref a t0072 t0073 (night wide)", "a", (72, 73)), ("ref a t0083 t0084 (night medium)", "a", (83, 84)), ("ref a t0061 (sunrise)", "a", (61,))]


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
