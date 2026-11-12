#!/usr/bin/env python3
"""qa_parallax.py -- share of frame pairs 0.5 s apart that a flat 2D zoom or pan explains.

    python3 qa_parallax.py ref              # calibrate on the reference stills (129 pairs per clip), writes tmp/shots/parallax_ref.json
    python3 qa_parallax.py seq <frames_dir> [step]   # pairs (g, g + 15) of a rendered sequence, every `step` frames

Method (production_forensics.md 7, the F-versus-H test): SIFT matches between the two frames (ratio 0.7, caption band
masked), then three RANSAC fits at 1 px: a fundamental matrix (any rigid 3D scene), a homography (one plane) and a
similarity (zoom + pan of a flat picture).  A pair is "explained by a flat 2D zoom or pan" when the similarity keeps
at least RATIO of the matches that the fundamental matrix keeps.  A pair with fewer than 30 matches (a cut, a whip)
is not explained by anything and counts as not flat.  RATIO is calibrated once so that the reference stills give the
published shares (clip A 16 of 129 = 12 percent, clip B 55 of 129 = 43 percent).
"""
import json, os, sys
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
TMP = os.path.join(PROJ, "v3", "tmp", "shots")
THR = 1.0
_sift = cv2.SIFT_create(nfeatures=4000, contrastThreshold=0.015)


def feats(path):
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if im.shape[:2] != (1280, 720):
        im = cv2.resize(im, (720, 1280), interpolation=cv2.INTER_AREA)
    mask = np.full(im.shape, 255, np.uint8)
    mask[830:975, :] = 0
    return _sift.detectAndCompute(im, mask)


def pair(fa, fb):
    (k1, d1), (k2, d2) = fa, fb
    if d1 is None or d2 is None or len(k1) < 30 or len(k2) < 30:
        return dict(n=0)
    ms = cv2.BFMatcher().knnMatch(d1, d2, k=2)
    good = [m[0] for m in ms if len(m) == 2 and m[0].distance < 0.7 * m[1].distance]
    if len(good) < 30:
        return dict(n=len(good))
    a = np.float32([k1[m.queryIdx].pt for m in good]); b = np.float32([k2[m.trainIdx].pt for m in good])
    Fm, fin = cv2.findFundamentalMat(a, b, cv2.FM_RANSAC, THR, 0.999)
    Hm, hin = cv2.findHomography(a, b, cv2.RANSAC, THR)
    Sm, sin = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=THR)
    f = float(fin.mean()) if fin is not None else 0.0
    h = float(hin.mean()) if hin is not None else 0.0
    s = float(sin.mean()) if sin is not None else 0.0
    return dict(n=len(good), F=round(f, 3), H=round(h, 3), S=round(s, 3), disp=round(float(np.median(np.linalg.norm(b - a, axis=1))), 1))


def flat(r, ratio):
    return r.get("n", 0) >= 30 and r["F"] > 0 and r["S"] >= ratio * r["F"]


def share(rows, ratio):
    return sum(1 for r in rows if flat(r, ratio)) / float(len(rows))


def run_ref():
    res = {}
    for clip in "ab":
        d = os.path.join(PROJ, "ref", clip)
        fs = sorted(f for f in os.listdir(d) if f.startswith("t") and f.endswith(".jpg"))
        fe = [feats(os.path.join(d, f)) for f in fs]
        res[clip] = [dict(pair(fe[i], fe[i + 1]), a=fs[i], b=fs[i + 1]) for i in range(len(fs) - 1)]
        print(clip, len(res[clip]), "pairs", flush=True)
    # one RATIO for both clips: minimise the distance to (16/129, 55/129)
    best = None
    for ratio in np.arange(0.30, 1.001, 0.01):
        sa, sb = share(res["a"], ratio), share(res["b"], ratio)
        err = abs(sa - 16 / 129.0) + abs(sb - 55 / 129.0)
        if best is None or err < best[0]:
            best = (err, float(ratio), sa, sb)
    out = dict(ratio=round(best[1], 2), share_a=best[2], share_b=best[3], target_a=16 / 129.0, target_b=55 / 129.0, pairs=res)
    json.dump(out, open(os.path.join(TMP, "parallax_ref.json"), "w"), indent=0)
    print("calibrated RATIO %.2f: clip A %.1f %% (published 12.4), clip B %.1f %% (published 42.6)" % (best[1], 100 * best[2], 100 * best[3]))
    for ratio in (0.5, 0.6, 0.7, 0.8, 0.9):
        print("  ratio %.1f: A %.1f %%  B %.1f %%" % (ratio, 100 * share(res["a"], ratio), 100 * share(res["b"], ratio)))
    return out


def run_seq(d, step=1, gap=15, ratio=None, cuts=()):
    if ratio is None:
        ratio = json.load(open(os.path.join(TMP, "parallax_ref.json")))["ratio"]
    fs = sorted(f for f in os.listdir(d) if f.startswith("f_") and f.endswith(".png"))
    idx = list(range(0, len(fs) - gap, step))
    need = sorted(set(idx) | set(i + gap for i in idx))
    fe = dict((i, feats(os.path.join(d, fs[i]))) for i in need)
    rows = [dict(pair(fe[i], fe[i + gap]), g=i) for i in idx]
    n_flat = sum(1 for r in rows if flat(r, ratio))
    matched = [r for r in rows if r.get("n", 0) >= 30]
    out = dict(dir=d, pairs=len(rows), flat=n_flat, share=n_flat / float(len(rows)), ratio=ratio, matched=len(matched),
               F_median=float(np.median([r["F"] for r in matched])) if matched else None,
               H_median=float(np.median([r["H"] for r in matched])) if matched else None,
               S_median=float(np.median([r["S"] for r in matched])) if matched else None, rows=rows)
    return out


if __name__ == "__main__":
    if sys.argv[1] == "ref":
        run_ref()
    else:
        o = run_seq(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1)
        print("%s: %d pairs 0.5 s apart, %d flat-2D (%.1f %%), matched %d; medians F %.2f H %.2f S %.2f (RATIO %.2f)" % (
            o["dir"], o["pairs"], o["flat"], 100 * o["share"], o["matched"], o["F_median"] or 0, o["H_median"] or 0, o["S_median"] or 0, o["ratio"]))
        tag = os.path.basename(os.path.dirname(os.path.dirname(os.path.normpath(os.path.abspath(sys.argv[2])))))      # .../v3/out/frames -> v3
        json.dump(o, open(os.path.join(TMP, "parallax_%s.json" % tag), "w"), indent=0)
