#!/usr/bin/env python3
"""deliver.py -- take s07 (shots 7-9): raw/s<id>/g_%04d.png -> frames/, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv,
work/qa.txt (heads, caption band, pops, hue rows).   python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as HR                                   # noqa: E402

TAKE = "s07"
SHOTS = {7: (599, 696), 8: (696, 782), 9: (782, 920)}     # [g0, g1)
FIRST, LAST = 593, 925
SETUPS = {1: (593, 648, "shot 7 medium: fitting the pane (wall_eye area)"), 2: (649, 695, "shot 7 ECU insert: the pane settles flush"),
          3: (696, 740, "shot 8 wide: three glaziers carry panes across the salon"), 4: (741, 781, "shot 8 tracking two-shot: vincenzo small between the tall coworkers"),
          5: (782, 835, "shot 9 three-shot: they laugh and point, he shrinks"), 6: (836, 882, "shot 9 low two-shot: the jeer 'ไอ้มักกะโรนี!' lip-synced g 859-880"),
          7: (883, 925, "shot 9 close: mocked -> hurt glare (handle 920-925)")}
DISSOLVES = []                                            # (a, b, sid_from, sid_to) inside the take
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)


def sid_of(g):
    for s, (a, b, _) in SETUPS.items():
        if a <= g <= b:
            return s


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
    add(FIRST, 696, "Salon Carre on a working day: big quiet room tone, distant footsteps on parquet, a far door, skylight hum", "ambience")
    add(600, 648, "a large glass pane flexing (soft wobbly 'wub'), careful breathing, a creak of the step-stool", "prop", peak_frame=620)
    add(649, 649, "cut to the insert", "cut")
    add(668, 684, "glass slides on the gilt frame and seats with a soft 'tock'; a bright glint 'ting' as the light sweeps", "prop", peak_frame=684)
    add(696, 696, "cut to the wide: the three glaziers", "cut")
    for g in range(700, 782, 14):
        add(g, g + 1, "footsteps on the parquet (one small light pair, two heavy pairs), panes wobbling", "foley", peak_frame=g)
    add(741, 741, "cut closer, tracking", "cut")
    add(750, 772, "vincenzo glances up at them: tiny comic 'small man' bassoon blip", "accent", peak_frame=752)
    add(782, 782, "cut: the coworkers stop and turn on him", "cut")
    add(790, 858, "laughter of two French workers (wheezing tall one, booming stout one), knee slaps", "voice", peak_frame=823)
    add(836, 836, "cut to the low two-shot", "cut")
    add(859, 880, "the jeer 'ไอ้มักกะโรนี!' (their mouths are lip-synced to the narration's quote, caption 28.53-29.23 s)", "voice", peak_frame=860)
    add(883, 883, "cut to vincenzo", "cut")
    add(890, 896, "the hurt glare: a low sour string sting / cello note", "accent", peak_frame=890)
    add(896, 926, "laughter fading off-screen, his tense breath through the nose", "voice")
    add(920, 920, "plan: shot 10 (dusk street, new location) starts at g 920 -- dissolve in the conform; handle 920-925 rendered in 3D", "cut")
    json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film7/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
              open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    src, rows = build_frames()
    q, pops = qa(rows)
    hr = hue_rows([("s07 shot 7 (g 599-695)", 599, 695), ("s07 shot 8 (g 696-781)", 696, 781), ("s07 shot 9 (g 782-919)", 782, 919),
                   ("s07 all (g 593-925)", FIRST, LAST)], [("ref a t0046 (they laughed)", (46,)), ("ref a t0001", (1,))])
    open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(q + [""] + hr) + "\n")
    print("\n".join(q + hr))
    walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
    meta = {"take": TAKE, "film": 7, "shots": [7, 8, 9], "first_g": FIRST, "n_frames": LAST - FIRST + 1, "g0": 599, "g1": 920,
            "handle_in": 6, "handle_out": 6, "transition_in": "cut",
            "transition_in_note": "shot 6 (wall_eye, the director) -> shot 7 (same salon): hard cut at g 599; in-handle g 593-598 rendered in 3D",
            "transition_out": "dissolve",
            "transition_out_note": "shot 10 (dusk street, new location) follows at g 920: plan dissolves 9-12 f between locations; out-handle g 920-925 rendered in 3D (the push on his glare continues)",
            "shot_ranges": {str(k): [a, b - 1] for k, (a, b) in SHOTS.items()},
            "setups": {str(s): {"g": [a, b], "what": nm} for s, (a, b, nm) in SETUPS.items()},
            "events": {"pane_flush": 684, "glint_sweep": [668, 690], "coworkers_laugh": [782, 857], "lip_sync_quote": [859, 880],
                       "vincenzo_mocked": [823, 889], "glare": [890, 925]},
            "lip_sync": "only coworker1 + coworker2 in set-up 6, g 859-880 (cast7.talk_mouth, hold 2), the narration's quoted 'ไอ้มักกะโรนี' (caption 28.53-29.23 s); all other mouths are static expression mouths",
            "set": "v3/set3d7/louvre.py louvre gallery_wide build (Salon Carre, GALLERY_DAY) with custom cameras; runtime: the glass pane he fits (+ edges, camera-only glint streaks), the step-stool + glazier's kit, three carried panes, three panes leaned by the divan, the velvet rope + two stanchions before her split into their own object and hidden in shot 7 (unhooked for the work; they crossed his face); her own glass box hidden in shot 7 (he is fitting it); set_mona(True) + set_flames keyed per frame",
            "cast": "v3/cast7: vincenzo (normal clothes), coworker1, coworker2 (STORY7 coworkers_laugh / coworkers_point, vincenzo_mocked -> vincenzo_glare; walk cycles with the hands pinned to the carried panes)",
            "dof": "none (cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30, "denoiser": "OpenImageDenoise, prefilter FAST",
            "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
            "frame_source": {str(g): v for g, v in src.items()}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
    cues()
    sheets([(640, 1), (870, 46), (905, 46)])
    encode()
    print("delivered %d frames, first_g %d, take.mkv" % (LAST - FIRST + 1, FIRST))
