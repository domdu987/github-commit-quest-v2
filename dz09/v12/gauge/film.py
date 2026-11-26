"""film.py -- builds the film's gauges from the cue table (v10/film/cues.py) for a given output size.

    import film;  gauges = film.build(Q, W, H, level=lambda t: 0..1, avatar_png=path)     # Q = the cues module
    L = layer.Layer(gauges, W, H)
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gauge as G


def _count_poly(v):
    return 0.42 + (1 - v) * 2.4            # the countdown starts amber and runs to red


def build(Q, W, H, level=None, avatar_png=None):
    wide = W > H
    out = []
    for c in Q.GAUGES:
        pos = c["pos169"] if wide else c["pos"]
        keys = list(c.get("keys", []))
        number = None
        dsc = c.get("delta_scale", 100)
        pol = c.get("polarity", "good")
        if "countdown" in c:
            t0, n0, step = c["countdown"]
            nsec = int(math.ceil(c["t_out"] - t0))
            keys += [(t0 + i, 1.0 - step * i, "hit", 0.45) for i in range(1, nsec)]
            number = (lambda t, t0=t0, n0=n0: "%d" % (n0 - max(0, int(math.floor(t - t0)))))
            pol = _count_poly; dsc = 1.0 / step
        if "count" in c:
            n = c["count"]
            number = (lambda t, tr_keys=keys, n=n: "%d" % round(n * max([0.0] + [k[1] for k in tr_keys if k[0] <= t])))
        out.append(G.Gauge(c["id"], G.Track(c["v0"], keys), c["t_in"], c["t_out"], x=pos["x"], y=pos["y"], length=pos["length"],
                           w=pos.get("w", c.get("w", 72)), orient=c.get("orient", "v"), segments=c.get("segments", 0), polarity=pol,
                           crit=c.get("crit", 0.9), picto=c["picto"], label=c.get("label"), number=number, side=(c.get("side169", c.get("side", 1)) if wide else c.get("side", 1)),
                           quiet=c.get("quiet", ()), delta_scale=dsc,
                           moves=c.get("moves169" if wide else "moves", ())))
    v = getattr(Q, "VOICE", None)
    if v and avatar_png and os.path.exists(avatar_png):
        pos = v["pos169"] if wide else v["pos"]
        img = G.data_uri(avatar_png)
        for i, (a, b) in enumerate(v["spans"]):
            out.append(G.Gauge("%s%d" % (v["id"], i), None, a, b, x=pos["x"], y=pos["y"], r=pos["r"], kind="avatar", image=img, level=level, label=v["label"]))
    m = getattr(Q, "TITLE_MARK", None)
    if m:
        pos = m["pos169"] if wide else m["pos"]
        out.append(G.Gauge(m["id"], None, Q.TITLE, 1e9, x=pos["x"], y=pos["y"], r=pos["r"], kind="badge", picto=m["picto"], color=G.AMBER, pop_out=False))
    return out


def cue_table(Q):
    rows = []
    for c in Q.GAUGES:
        rows.append((c["id"], c["t_in"], c["t_out"], c["v0"], [(round(k[0], 2), round(k[1], 2), k[2]) for k in c.get("keys", [])], c["pos"], c["pos169"]))
    return rows
