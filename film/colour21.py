"""Film 21 conform colour normalization (director policy 2026-11-20 19:00, WORKER21.md "Colour policy").
One FIXED correction per segment (yellow pullback -> chroma scale -> gamma), solved on sampled frames so the segment lands at
about luma 100 and sat 0.55 (qa_stats2 definitions). At dissolve (D6) joins the parameters ease over +-EASE frames; at hard cuts
they step. Overrides: film/film21/colour21.json {"sA1": {"gamma":..,"chroma":..,"yellow":..}} (hand values win over the solver).
API: params = solve(takes) ; fix(rgb_uint8, p) -> uint8 ; per_g(takes, params, N) -> list of p per film frame g"""
import json, os, numpy as np
from PIL import Image
LUMA, SAT, YEL, EASE = 100.0, 0.55, 0.40, 12
OVR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "film21", "colour21.json")

def fix(im, p):
    a = im.astype(np.float32) / 255.0
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    yel = np.clip(np.minimum(R, G) - B, 0, 1) * (1 - np.clip(np.abs(R - G) * 4, 0, 1))   # pure yellows only, not orange/red
    a[..., 2] = B + p["yellow"] * yel
    Y = (a @ np.array([0.299, 0.587, 0.114], np.float32))[..., None]
    a = np.clip((Y + (a - Y) * p["chroma"]) * p.get("gain", 1.0), 0, 1) ** p["gamma"]
    return (a * 255 + 0.5).astype(np.uint8)

def stats(ims):
    L, S = [], []
    for im in ims:
        a = im.astype(np.float32); mx, mn = a.max(-1), a.min(-1)
        S.append(((mx - mn) / (mx + 1e-3)).mean()); L.append((a @ np.array([0.299, 0.587, 0.114], np.float32)).mean())
    return float(np.mean(L)), float(np.mean(S))

def solve_one(ims):
    # over-bright segments are pulled down with a linear gain (keeps contrast and hue), dark ones lifted with gamma;
    # chroma is only nudged (0.8-1.25) so a segment never goes grey or neon
    p = dict(gain=1.0, gamma=1.0, chroma=1.0, yellow=YEL)
    small = [np.asarray(Image.fromarray(i).resize((180, 320))) for i in ims]
    for _ in range(8):
        l, s = stats([fix(i, p) for i in small])
        if l > LUMA and p["gamma"] <= 1.0001:
            p["gain"] = float(np.clip(p["gain"] * LUMA / l, 0.72, 1.0))
        else:
            p["gamma"] = float(np.clip(p["gamma"] * np.log(LUMA / 255) / np.log(max(l, 1) / 255), 0.65, 1.0))
        p["chroma"] = float(np.clip(p["chroma"] * SAT / max(s, 1e-3), 0.8, 1.25))
    l, s = stats([fix(i, p) for i in small]); p["result"] = [round(l, 1), round(s, 3)]
    return p

def solve(takes, every=8):
    ovr = json.load(open(OVR)) if os.path.exists(OVR) else {}
    P = {}
    for t in takes:
        gs = [g for g in sorted(t["have"]) if t["g0"] <= g < t["g1"]][::every]
        P[t["name"]] = solve_one([np.asarray(Image.open(t["have"][g]).convert("RGB")) for g in gs])
        P[t["name"]].update(ovr.get(t["name"], {}))
    return P

def per_g(takes, P, N):
    keys = ("gain", "gamma", "chroma", "yellow"); out = [None] * N
    for i, t in enumerate(takes):
        for g in range(max(0, t["g0"]), min(N, t["g1"])): out[g] = {k: P[t["name"]][k] for k in keys}
    for i in range(1, len(takes)):                      # ease across dissolve joins (D6)
        t, pv = takes[i], takes[i - 1]
        if t.get("transition_in", {}).get("type") != "dissolve": continue
        a, b = P[pv["name"]], P[t["name"]]
        for g in range(t["g0"] - EASE, t["g0"] + EASE):
            if 0 <= g < N:
                x = (g - (t["g0"] - EASE) + 0.5) / (2 * EASE); x = x * x * (3 - 2 * x)
                out[g] = {k: a[k] * (1 - x) + b[k] * x for k in keys}
    return out
