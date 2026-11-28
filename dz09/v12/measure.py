"""measure.py A B -- sharpness of the 6 proof stills in dirs v12/A and v12/B, by region (masks from the kept passes)."""
import sys, os, glob, json, numpy as np, cv2
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in ("v4/set_expressway", "v11/set"): sys.path.insert(0, os.path.join(PROJ, p))
import render11
SRC = PROJ + "/v10/film/out/final_720x1280/stills_before/"

def masks(name):
    out = {k: f"{SRC}{name}_{k}.exr" for k in ("rgb", "z", "idx", "env")}
    rgb, alpha, env, z, idx = render11.load_passes(out, 720, 1280)
    z = cv2.medianBlur(np.minimum(z, 1e6).astype(np.float32), 5); idx = cv2.medianBlur(idx.astype(np.float32), 5)
    act = np.abs(idx - 2) < 0.5
    er = lambda m, k=7: cv2.erode(m.astype(np.uint8), np.ones((k, k), np.uint8)) > 0
    zf = float(json.load(open(SRC + name + "_info.json"))["focus_z"])
    geo = (z < 1e5) & ~act & (np.abs(idx - 5) > 0.5)
    return dict(principal=er(act, 3), near=er(geo & (z < 1.6 * zf)), mid=er(geo & (z >= 1.6 * zf) & (z < 6 * zf)),
                far=er(geo & (z >= 6 * zf)), sky=er(z >= 1e5, 9)), zf

def stats(png, M):
    im = cv2.imread(png); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    lap = cv2.Laplacian(g, cv2.CV_32F, ksize=3)
    mu = cv2.blur(g, (9, 9)); sd = np.sqrt(np.maximum(cv2.blur(g * g, (9, 9)) - mu * mu, 0))
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV_FULL).astype(np.float32)
    r = {}
    for k, m in M.items():
        if m.sum() < 2000: r[k] = None; continue
        r[k] = dict(lapvar=round(float(lap[m].var()), 1), lc=round(float(sd[m].mean()), 2), p5=round(float(np.percentile(g[m], 5)), 1),
                    p95=round(float(np.percentile(g[m], 95)), 1), area=round(float(m.mean()), 3))
    sh = (g < 60) & (hsv[..., 1] > 60) & (hsv[..., 2] > 12)
    h = hsv[..., 0][sh] / 256 * 360
    r["shade_hue"] = round(float(np.median(h)), 1) if len(h) else None
    r["magenta_frac"] = round(float(((hsv[..., 0] / 256 * 360 > 270) & (hsv[..., 0] / 256 * 360 < 340) & (hsv[..., 1] > 80) & (g < 90)).mean()), 4)
    r["luma_p50"] = round(float(np.percentile(g, 50)) / 255, 3)
    # rain visibility: thin vertical bright streak energy = positive horizontal high-pass that survives a vertical 9-px minimum
    hp = np.maximum(g - cv2.blur(g, (7, 1)), 0); st = cv2.erode(hp, np.ones((9, 1), np.uint8))
    r["streak_sky"] = round(float(st[M["sky"]].mean()), 3) if M["sky"].sum() > 2000 else None
    r["streak_principal"] = round(float(st[M["principal"]].mean()), 3) if M["principal"].sum() > 2000 else None
    return r

if __name__ == "__main__":
    A, B = sys.argv[1], sys.argv[2]
    res = {}
    for f in sorted(glob.glob(SRC + "S*_info.json")):
        n = os.path.basename(f)[:-len("_info.json")]
        M, zf = masks(n)
        res[n] = dict(focus_z=round(zf, 2), before=stats(f"{PROJ}/v12/{A}/{n}.png", M), after=stats(f"{PROJ}/v12/{B}/{n}.png", M))
    json.dump(res, open(PROJ + "/v12/measure_%s_%s.json" % (A, B), "w"), indent=1)
    for n, r in res.items():
        print(n, "zf", r["focus_z"])
        for k in ("principal", "near", "mid", "far", "sky"):
            a, b = r["before"][k], r["after"][k]
            if a: print("   %-9s area %.2f lapvar %7.1f -> %7.1f (x%.2f)  local contrast %5.2f -> %5.2f (x%.2f)  p5/p95 %s/%s -> %s/%s" % (k, a["area"], a["lapvar"], b["lapvar"], b["lapvar"] / max(a["lapvar"], 1e-3), a["lc"], b["lc"], b["lc"] / max(a["lc"], 1e-3), a["p5"], a["p95"], b["p5"], b["p95"]))
        for k in ("shade_hue", "magenta_frac", "luma_p50", "streak_sky", "streak_principal"): print("   %-16s %s -> %s" % (k, r["before"][k], r["after"][k]))
