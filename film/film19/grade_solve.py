"""Per-take colour grade for film 19 (QA_TEAM §G). Picks the mildest ffmpeg eq (gamma, saturation) that puts
each take inside film 2's per-shot envelope: luma 78-120, saturation >= 0.47. Writes film19/grade.json, used by conform19.py."""
import subprocess, numpy as np, glob, os, json, itertools
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def src(d):
    parts = sorted(glob.glob(d + '/take.mkv.part*'))
    if not parts: return d + '/take.mkv'
    out = '/tmp/' + os.path.basename(d) + '_g.mkv'
    open(out, 'wb').write(b''.join(open(p, 'rb').read() for p in parts)); return out
def stats(f, vf):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", (vf + "," if vf else "") + "fps=3,scale=90:160",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 160, 90, 3).astype(np.float32)
    mx, mn = a.max(-1), a.min(-1); return float(((mx - mn) / (mx + 1e-3)).mean()), float(a.mean())
G = [round(x, 2) for x in np.arange(0.70, 1.61, 0.05)]; S = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
out = {}
for d in sorted(glob.glob(P + '/v3/film19/s[0-9][0-9]')):
    n = os.path.basename(d); f = src(d); s0, l0 = stats(f, '')
    if s0 >= 0.47 and 78 <= l0 <= 120: print(f"{n} ok  sat {s0:.3f} luma {l0:.1f}"); continue
    best = None
    for g, s in sorted(itertools.product(G, S), key=lambda p: abs(p[0] - 1) + 0.5 * (p[1] - 1)):
        vf = f"eq=gamma={g}:saturation={s}"; sa, la = stats(f, vf)
        if sa >= 0.47 and 78 <= la <= 120: best = (vf, sa, la); break
    if best: out[n] = best[0]; print(f"{n} {best[0]:28s} sat {s0:.3f}->{best[1]:.3f} luma {l0:.1f}->{best[2]:.1f}")
    else: print(f"{n} NO GRADE FOUND sat {s0:.3f} luma {l0:.1f}")
json.dump(out, open(P + '/film19/grade.json', 'w'), indent=1)
