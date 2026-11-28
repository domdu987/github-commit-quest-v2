import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import layout as L, t2lib as T
C, F = T.C, T.F
CX, CY, CZ = float(os.environ.get("CX", 9.5)), float(os.environ.get("CY", 1.5)), float(os.environ.get("CZ", 1.0))
LENS = float(os.environ.get("LENS", 24))
def cam_of(g):
    u = T.umap(g)
    fx, fy, p = L.front_xy(TK, u)
    tx, ty = fx - 2.0 * L.HEAD[0], fy - 2.0 * L.HEAD[1]
    return (CX, CY, CZ), (tx, ty, 2.6), LENS
TK = None
if __name__ == "__main__":
    gs = [int(x) for x in sys.argv[1].split(",")]
    L.preset("t2_lay")
    F.PRESETS["t2_lay"]["cam"] = dict(loc=(CX, CY, CZ), look_at=(0, 4.5, 2.0), lens=LENS)
    def hooks(g, Tk):
        Tk.TK.set_crossing(Tk.H, T.umap(g))
    Tk = T.Take("t2_lay", cam_of, hooks)
    TK = Tk
    L.regime(Tk)
    out = "work_lt"; T.run(Tk, "draft", gs, os.path.join(HERE, out))
    T.post_take(gs, os.path.join(HERE, out, "work/draft/raw"), os.path.join(HERE, out, "post"))
