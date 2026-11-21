"""Film 21 final grade = the client's COLOUR_SPEC v1.1 grade (film/grade_v11.py, copied unchanged from the skill at 2596dd8).
Only the film clock is ours: TAKES (segment start g), JOINS (the conform's dissolves) and SHOT (per-segment gain / gamma / sat, the v1.1
grade's own stage-1 correction). SHOT is solved per segment toward the spec's centre (brightness V 0.54, saturation 0.43) on sampled
frames, then clamped (gain 0.70-1.15, gamma 0.85-1.25, sat 0.55-1.25). Hand overrides: film/film21/grade21_shots.json.
usage (from conform_full.py, env GRADE21=1):  P = grade21.setup(takes, N) ; im = grade21.grade(im_uint8, g)
"""
import json, os, sys, numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade_v11 as G
TV, TS = 0.54, 0.43
OVR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "film21", "grade21_shots.json")


def _sv(ims):
    S, V = [], []
    for a in ims:
        x = a.astype(np.float32) / 255
        x = np.concatenate([x[:1060], x[1200:]])          # caption band excluded, as hue_report does
        mx, mn = x.max(-1), x.min(-1)
        S.append(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0).mean()); V.append(mx.mean())
    return float(np.mean(S)), float(np.mean(V))


def setup(takes, N):
    """takes: conform_full's list (sorted by g0, with 'name', 'g0', 'have', 'transition_in')."""
    G.TAKES = [(t["name"], t["g0"]) for t in takes]
    if G.TAKES[0][1] > 0:
        G.TAKES.insert(0, (G.TAKES[0][0], 0))
    G.JOINS = []
    for t in takes:
        ti = t.get("transition_in", {})
        if ti.get("type") == "dissolve" and t is not takes[0]:
            n = ti["frames"]; a = t["g0"] - n // 2
            G.JOINS.append((t["name"], "d", a, a + n - 1))
    G.FOG_G0, G.FOG_G1 = 10 ** 9, -1
    ovr = json.load(open(OVR)) if os.path.exists(OVR) else {}
    G.SHOT = {}
    for t in takes:
        gs = [g for g in sorted(t["have"]) if t["g0"] <= g < t["g1"]][::10]
        ims = [np.asarray(Image.open(t["have"][g]).convert("RGB")) for g in gs]
        p = dict(gain=1.0, gamma=1.0, sat=1.0)
        for _ in range(4):
            G.SHOT[t["name"]] = p
            outs = [G.grade_array(a, g) for a, g in zip(ims, gs)]
            s, v = _sv(outs)
            p = dict(p)
            if v > TV:
                p["gain"] = float(np.clip(p["gain"] * TV / v, 0.70, 1.15)); p["gamma"] = 1.0
            else:
                p["gamma"] = float(np.clip(p["gamma"] * np.log(TV) / np.log(max(v, 0.05)), 0.85, 1.25))
            p["sat"] = float(np.clip(p["sat"] * TS / max(s, 1e-3), 0.55, 1.25))
        p.update(ovr.get(t["name"], {}))
        G.SHOT[t["name"]] = p
    return {k: dict(v) for k, v in G.SHOT.items()}


def grade(a, g):
    return G.grade_array(a, int(g))
