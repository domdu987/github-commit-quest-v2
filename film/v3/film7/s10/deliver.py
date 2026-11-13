#!/usr/bin/env python3
"""deliver.py -- take s10 (shots 10-11): raw/s<id>/g_%04d.png -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv,
work/qa.txt (heads, caption band, pops, hue rows).   python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as HR                                   # noqa: E402

TAKE = "s10"
SHOTS = {10: (920, 1020), 11: (1020, 1114)}               # [g0, g1)
FIRST, LAST = 914, 1119
SETUPS = {1: (914, 949, "shot 10 the rue at dusk, the gas lamps come on (paris notre_dame_view area, STREET_DUSK, papers 0)"),
          2: (950, 990, "shot 10 the storage closet: vincenzo crouched by the brooms, hand on the storm lantern"),
          3: (991, 1014, "shot 10 punch-in on his worried face; glances at the door (g 987+)"),
          4: (1025, 1062, "shot 11 Monday: the empty salon from high, three workers in white smocks"),
          5: (1063, 1119, "shot 11 closer: two smocked workers walk toward her wall (out-handle 1114-1119)")}
DISSOLVES = [(1015, 1024, 3, 4)]                          # closet -> gallery, 10 frames centred on g 1020
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)


def sid_of(g):
    for s, (a, b, _) in SETUPS.items():
        if a <= g <= b:
            return s


def grade_magenta(src, dst, k=14.0):
    """dusk street only: the set's pink-lit facades read magenta 12.8 (> 10); pull the 290-345 deg band ~28 deg toward violet."""
    import cv2
    im = cv2.imread(src); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
    h = hsv[..., 0]; w = np.clip(1.0 - np.abs(h - 160.0) / 18.0, 0, 1) * (hsv[..., 1] > 30)
    hsv[..., 0] = h - k * w
    cv2.imwrite(dst, cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR))


def build_frames():
    src, rows = {}, []
    for g in range(FIRST, LAST + 1):
        dst = os.path.join(OUT, "g_%04d.png" % g)
        dz = [d for d in DISSOLVES if d[0] <= g <= d[1]]
        if dz:
            a, b, s0, s1 = dz[0]
            w = (g - a + 1) / float(b - a + 2)
            A = np.asarray(Image.open(os.path.join(HERE, "raw", "s%d" % s0, "g_%04d.png" % g)).convert("RGB"), dtype=np.float32)
            B = np.asarray(Image.open(os.path.join(HERE, "raw", "s%d" % s1, "g_%04d.png" % g)).convert("RGB"), dtype=np.float32)
            Image.fromarray(np.clip(A * (1 - w) + B * w + 0.5, 0, 255).astype(np.uint8)).save(dst)
            src[g] = "%d>%d %.2f" % (s0, s1, w)
            for s in (s0, s1):
                rows.append(json.load(open(os.path.join(HERE, "raw", "s%d" % s, "g_%04d.json" % g))))
        else:
            s = sid_of(g)
            if s == 1:
                grade_magenta(os.path.join(HERE, "raw", "s1", "g_%04d.png" % g), dst)
            else:
                shutil.copyfile(os.path.join(HERE, "raw", "s%d" % s, "g_%04d.png" % g), dst)
            src[g] = str(s)
            rows.append(json.load(open(os.path.join(HERE, "raw", "s%d" % s, "g_%04d.json" % g))))
    return src, rows


def qa(rows):
    out = []
    for s, (a, b, nm) in SETUPS.items():
        rs = [r for r in rows if r["shot"] == s]
        out.append("set-up %d g %d..%d (%s): %d frames" % (s, a, b, nm, len(rs)))
        for n in sorted({n for r in rs for n in r["heads"]}):
            hs = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"] and -60 < r["heads"][n]["x"] < 780]
            if not hs:
                continue
            w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]
            low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
            out.append("   %-4s head w %4.0f..%4.0f px, centre y %4.0f..%4.0f (%.2f..%.2f H), head bottom > 880: %s"
                       % (n, min(w), max(w), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
    out.append("render: wall %.2f s, cpu %.2f s per frame (mean); retried %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
               [r["g"] for r in rows if r.get("retried")]))
    fs = sorted(glob.glob(os.path.join(OUT, "g_*.png")))
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
            pops.append((FIRST + i, FIRST + i + 1, round(v, 1)))
    cuts = [b + 1 for s, (a, b, nm) in SETUPS.items()][:-1]
    out.append("popcheck (g -> g+1, change): %s ; planned cuts at %s" % (pops, cuts))
    out.append("near-still transitions (< 0.35): %s" % [FIRST + i for i, v in enumerate(d) if v < 0.35])
    out.append("frame change median %.2f, max %.2f" % (float(np.median(d)), max(d)))
    bad = []
    for f in fs:
        a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
        if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
            bad.append(os.path.basename(f))
    out.append("magenta / black frames: %s" % bad)
    return out, pops


def hue_rows(groups, refs):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
        for lab, a, b in groups:
            HR.row(lab, [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)])
        for lab, ts in refs:
            HR.row(lab, [os.path.join(PROJ, "ref", "a", "t%04d.jpg" % t) for t in ts])
    return buf.getvalue().rstrip().split("\n")


def sheets(compare_pairs):
    gs = [int(round(FIRST + i * (LAST - FIRST) / 15.0)) for i in range(16)]
    w, h, lab, cols = 270, 480, 18, 8
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        shot = [k for k, (a, b) in SHOTS.items() if a <= g < b]
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s set-up %s" % (g, g / 30.0, ("shot %d" % shot[0]) if shot else "handle", sid_of(g)), fill=(255, 255, 255))
    S.save(os.path.join(HERE, "contact.jpg"), quality=88)
    w, h, lab = 360, 640, 20
    Cm = Image.new("RGB", (len(compare_pairs) * 2 * w + (len(compare_pairs) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
    x = 0
    for g, tref in compare_pairs:
        Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
        dr.text((x + 4, 4), "%s g %d (%.2f s)" % (TAKE, g, g / 30.0), fill=(255, 255, 255))
        Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
        dr.text((x + w + 4, 4), "ref a t%04d" % tref, fill=(255, 220, 160))
        x += 2 * w + 12
    Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)


def encode():
    mkv = os.path.join(HERE, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)


def cues():
    t = lambda g: round(g / 30.0, 3)
    ev = []

    def add(g0, g1, label, kind, **kw):
        e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)
    add(FIRST, 950, "Paris at dusk, Sunday: last birds, a far church bell, a fiacre trotting away, the hiss and pop of gas lamps lighting one by one", "ambience")
    for k, g in enumerate((918, 926, 934, 942)):
        add(g, g + 1, "a gas lamp catches: soft 'fwoomp' + hiss", "prop", peak_frame=g)
    add(950, 950, "hard cut into the closet: the sound closes in", "cut")
    add(950, 1025, "closet room tone: muffled, the storm lantern's flame flutter and a tiny tin creak, his held breath", "ambience")
    add(985, 1000, "distant footsteps of a night guard passing in the corridor; he freezes (glance at the door)", "foley", peak_frame=990)
    add(991, 991, "cut: punch-in on his face", "cut")
    add(1015, 1024, "DISSOLVE to Monday morning (10 frames, centred on g 1020)", "transition")
    add(1015, LAST + 1, "the closed museum on Monday: big empty echo, skylight hum, a broom somewhere, workmen whistling far off", "ambience")
    for g in range(1030, LAST + 1, 14):
        add(g, g + 1, "workmen's boots on the parquet, smocks rustling", "foley", peak_frame=g)
    add(1063, 1063, "cut closer", "cut")
    add(1114, 1114, "plan: shot 12 (wall_eye, he lifts the painting) starts at g 1114; out-handle 1114-1119 rendered in 3D", "cut")
    json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film7/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
              open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    src, rows = build_frames()
    q, pops = qa(rows)
    hr = hue_rows([("s10 street dusk (g 914-949)", 914, 949), ("s10 closet (g 950-1014)", 950, 1014), ("s10 gallery Monday (g 1025-1119)", 1025, 1119),
                   ("s10 all (g 914-1119)", FIRST, LAST)], [("ref a t0061 (sunset)", (61,)), ("ref a t0046 (interior)", (46,))])
    open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(q + [""] + hr) + "\n")
    print("\n".join(q + hr))
    walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
    meta = {"take": TAKE, "film": 7, "shots": [10, 11], "first_g": FIRST, "n_frames": LAST - FIRST + 1, "g0": 920, "g1": 1114,
            "handle_in": 6, "handle_out": 6, "transition_in": "dissolve",
            "transition_in_note": "shot 9 (salon) -> shot 10 (dusk street, new location): plan dissolves 9-12 f between locations; in-handle g 914-919 rendered in 3D (lamps already lighting, crane continues)",
            "transition_out": "cut",
            "transition_out_note": "shot 12 (wall_eye, same salon, Monday) follows at g 1114; out-handle g 1114-1119 rendered in 3D",
            "transitions": [{"at": 950, "type": "cut", "note": "street -> closet, inside shot 10, on 'ซ่อนตัวในตู้'"},
                            {"at": 991, "type": "cut", "note": "punch-in inside the closet"},
                            {"at": 1020, "type": "dissolve", "frames": [1015, 1024], "note": "closet -> Monday gallery (shot 11), baked into the take"},
                            {"at": 1063, "type": "cut", "note": "closer on the smocked workers"}],
            "shot_ranges": {str(k): [a, b - 1] for k, (a, b) in SHOTS.items()},
            "setups": {str(s): {"g": [a, b], "what": nm} for s, (a, b, nm) in SETUPS.items()},
            "events": {"lamps_light": [914, 943], "cut_to_closet": 950, "glance_at_door": [987, 994], "dissolve": [1015, 1024]},
            "lip_sync": "none (no quoted line in shots 10-11): static expression mouths",
            "grade": "set-up 1 (dusk street) only: deliver.py grade_magenta() pulls the 290-345 deg hue band 28 deg toward violet (magenta 12.8 -> ~9)",
            "set": "v3/set3d7/louvre.py: (1) paris notre_dame_view build (STREET_DUSK) with a custom crane camera, papers 0 keyed, set_flames ramp 0.15 -> 1.2 keyed per frame; (2) louvre closet (CLOSET_NIGHT), custom cameras, set_flames keyed; (3) louvre gallery_wide (GALLERY_DAY), custom cameras, set_mona(True) keyed",
            "cast": "v3/cast7: vincenzo (vincenzo_hide_closet without the hand-held lantern: his hand pinned to the set's storm lantern); three workers in white smocks = runtime copies of coworker1 / coworker2 / guard bodies re-dressed in cast7's smock7 (white, as vincenzo_smock) with flat caps (worker7_a/b/c, registered in shot.py, cast7 untouched)",
            "dof": "none (cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30, "denoiser": "OpenImageDenoise, prefilter FAST",
            "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
            "frame_source": {str(g): v for g, v in src.items()}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
    cues()
    sheets([(930, 61), (1000, 46), (1090, 46)])
    encode()
    print("delivered %d frames, first_g %d, take.mkv" % (LAST - FIRST + 1, FIRST))
