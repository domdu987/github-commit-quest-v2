#!/usr/bin/env python3
"""deliver.py -- s15: raw/dusk + raw/storm -> frames/g_%04d.png mixed by a rolling cloud-front mask, take.mkv, meta.json,
cues.json, contact.jpg, work/qa.txt.   python3 deliver.py [g ...]  (with g's: only write those frames to work/mix/, for looking)

Mask: storm where  (P(g) + N(x, y, g) - y) > 0, soft over +-0.07 of the frame height; y = row / 1280 (0 = top).
P(g) eases from -0.2 (front above the frame) at g 1170 to 1.3 (front past the bottom) at g 1242; N is a 4-octave value
noise (amplitude 0.22, drifting 2.5 px per frame to the right): the front is a ragged cloud edge, not a wipe.  Just behind the
front the picture is darkened by up to 22 percent (the leading edge of the cloud bank)."""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "s12"))
import deliver_lib as L
sys.argv_saved = list(sys.argv)
sys.argv = [sys.argv[0]]
sys.path.insert(0, HERE)
import shot as S                                    # noqa: E402

FIRST, LAST = S.RANGE
RAW = os.environ.get("S15_RAW", os.path.join(HERE, "raw")); OUT = os.path.join(HERE, "frames")
F0, F1 = 1170, 1242
W, H = 720, 1280
DRIFT = 2.5


def _noise(seed=15, w=W + 420, h=H):
    r = np.random.RandomState(seed); acc = np.zeros((h, w), np.float32); amp, tot = 1.0, 0.0
    for cell in (220, 110, 55, 27):
        gw, gh = w // cell + 3, h // cell + 3
        g = r.rand(gh, gw).astype(np.float32)
        im = Image.fromarray(g).resize((gw * cell, gh * cell), Image.BICUBIC)
        acc += amp * np.asarray(im, np.float32)[:h, :w]; tot += amp; amp *= 0.5
    acc /= tot
    return (acc - acc.mean()) / (acc.std() + 1e-6)


NZ = _noise()
YY = (np.arange(H, dtype=np.float32)[:, None] + 0.5) / H


def front(g):
    u = min(1.0, max(0.0, (g - F0) / float(F1 - F0)))
    u = u * u * (3 - 2 * u)
    return -0.2 + 1.5 * u


def mask(g):
    off = int(round(DRIFT * (g - FIRST)))
    n = NZ[:, 420 - min(off, 420):420 - min(off, 420) + W] * 0.22 * 0.5
    d = front(g) + n - YY
    m = np.clip((d + 0.07) / 0.14, 0, 1); m = m * m * (3 - 2 * m)
    edge = np.exp(-((d - 0.06) / 0.07) ** 2) * (d > -0.02)
    return m, edge


def frame(g):
    a = L.load(os.path.join(RAW, "dusk", "g_%04d.png" % g)); b = L.load(os.path.join(RAW, "storm", "g_%04d.png" % g))
    m, e = mask(g)
    c = a * (1 - m[..., None]) + b * m[..., None]
    return c * (1 - 0.22 * e[..., None]), float(m.mean())


if __name__ == "__main__":
    only = [int(x) for x in sys.argv_saved[1:]]
    if only:
        os.makedirs(os.path.join(HERE, "work", "mix"), exist_ok=True)
        for g in only:
            c, mm = frame(g); L.save(c, os.path.join(HERE, "work", "mix", "g_%04d.png" % g)); print(g, round(mm, 3))
        sys.exit(0)
    os.makedirs(OUT, exist_ok=True)
    src = {}
    for g in range(FIRST, LAST + 1):
        c, mm = frame(g); L.save(c, os.path.join(OUT, "g_%04d.png" % g)); src[g] = "dusk*%.3f+storm*%.3f (mask mean)" % (1 - mm, mm)
    out, n = L.encode(HERE, FIRST)
    assert n == LAST - FIRST + 1, n
    rows = {p: [json.load(open(f)) for f in sorted(glob.glob(os.path.join(RAW, p, "g_*.json")))] for p in ("dusk", "storm")}
    allr = rows["dusk"] + rows["storm"]
    meta = {"take": "s15", "shots": [15], "g0": S.G0, "g1": S.G_END, "first_g": FIRST, "n_frames": n, "handle_in": S.H_IN, "handle_out": S.H_OUT,
            "transition_in": {"type": "dissolve", "frames": 12, "note": "handle g 1143..1150 rendered in 3D (pure DUSK)"},
            "transition_out": {"type": "dissolve", "frames": 10, "note": "handle g 1248..1254 rendered in 3D (pure NIGHT_STORM)"},
            "shot_ranges": {"15": [S.G0, S.G_END - 1]}, "set": "v3/set3d2/tower.py", "light": "DUSK -> NIGHT_STORM",
            "method": "two 3D passes of the same camera move (raw/dusk, raw/storm) mixed per pixel by a rolling cloud-front mask (deliver.py); front enters g 1170, covers the frame by g 1242",
            "rod": "set_rod(0) (that night there is no rod)", "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(float(np.mean([r["wall"] for r in allr])) * 2, 2),
            "s_per_frame_cpu_mean": round(float(np.mean([r["cpu"] for r in allr])) * 2, 2),
            "s_per_frame_note": "two passes per frame (sum of both)",
            "frame_source": {str(g): v for g, v in src.items()}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
    ev = []
    t = lambda g: round(g / 30.0, 3)

    def add(g0, g1, label, kind, **kw):
        e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)

    add(FIRST, F0 + 20, "calm summer dusk over the town: swifts, a far dog, evening voices", "ambience")
    add(F0, F1, "the storm front rolls in: low wind rising, a long low thunder rumble under it", "thunder_rumble")
    for i, g in enumerate(S.WIN_ON):
        add(g, g + 5, "window group %d lights up (warm; optional tiny shutter creak)" % (i + 1), "windows")
    add(S.FLICKER[0], S.FLICKER[0] + 4, "far sheet lightning flickers in the clouds", "flash")
    add(S.FLICKER[0] + 8, LAST + 1, "distant thunder", "thunder_far")
    add(S.REFRAME[0], S.REFRAME[1], "camera tilts up to the sky over the tower (no whoosh, slow)", "camera_move")
    json.dump(dict(take="s15", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)
    gs = [int(round(FIRST + i * (LAST - FIRST) / 15.0)) for i in range(16)]
    L.contact(OUT, gs, {g: "storm %.2f" % float(mask(g)[0].mean()) for g in gs}, os.path.join(HERE, "contact.jpg"))
    q = ["raw dusk %d frames, storm %d frames; per pass wall %.2f s / cpu %.2f s" % (len(rows["dusk"]), len(rows["storm"]),
         np.mean([r["wall"] for r in allr]), np.mean([r["cpu"] for r in allr]))]
    q.append("storm share of the frame (mask mean) at g: %s" % {g: round(float(mask(g)[0].mean()), 2) for g in range(FIRST, LAST + 1, 8)})
    q.append("camera: %s" % json.dumps(L.cam_report(S.cam, FIRST, LAST, depth=35.0)))
    pops, still, bad = L.popcheck(OUT, FIRST, LAST)
    q.append("popcheck: %s; near-still transitions: %s; magenta frames: %s" % (pops, still, bad))
    fr = lambda a, b: [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)]
    q.append(L.hue_rows([("s15 dusk part (g 1151-1170)", fr(1151, 1170)), ("s15 front passing (g 1171-1230)", fr(1171, 1230)),
                         ("s15 storm part (g 1231-1247)", fr(1231, 1247)), ("s15 all (g 1143-1254)", fr(FIRST, LAST)),
                         ("ref a t0072 t0080", [os.path.join(L.PROJ, "ref", "a", "t%04d.jpg" % k) for k in (72, 80)])]))
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(q) + "\n")
    print("\n".join(q))
    print("delivered", len(src), "frames ->", out, n)
