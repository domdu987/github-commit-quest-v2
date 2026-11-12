#!/usr/bin/env python3
"""deliver.py -- s14: raw/ -> frames/g_%04d.png, take.mkv, meta.json, cues.json, contact.jpg, work/qa.txt.  python3 deliver.py"""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "s12"))
import deliver_lib as L
sys.argv = [sys.argv[0]]
sys.path.insert(0, HERE)
import shot as S                                    # noqa: E402

FIRST, LAST = S.RANGE
RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
src = {}
for g in range(FIRST, LAST + 1):
    L.shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = "s14"
out, n = L.encode(HERE, FIRST)
assert n == LAST - FIRST + 1, n
rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(RAW, "g_*.json")))]
meta = {"take": "s14", "shots": [14], "g0": S.G0, "g1": S.G_END, "first_g": FIRST, "n_frames": n, "handle_in": S.H_IN, "handle_out": S.H_OUT,
        "transition_in": {"type": "dissolve", "frames": 12, "note": "handle g 1018..1025 rendered in 3D"},
        "transition_out": {"type": "dissolve", "frames": 12, "note": "handle g 1151..1158 rendered in 3D"},
        "shot_ranges": {"14": [S.G0, S.G_END - 1]}, "set": "v3/set3d2/tower.py", "light": "DAY (morning after the storm)",
        "rod": "set_rod(0): the tower is bare; the rod is padre's prop, then nico's",
        "mouth": {"who": "padre", "frames": [S.Q0, S.Q1], "note": "lip-sync from the narration envelope, a new drawing every 2 frames; closed (smirk) outside"},
        "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean([r["wall"] for r in rows])), 2),
        "s_per_frame_cpu_mean": round(float(np.mean([r["cpu"] for r in rows])), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []
t = lambda g: round(g / 30.0, 3)


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(FIRST, LAST + 1, "fresh morning in the square after the storm: birds, dripping gutters, a far cart", "ambience")
add(S.G_GIVE - 2, S.G_GIVE + 10, "padre thrusts the iron rod out (cassock rustle)", "gesture")
add(S.G_GRIP, S.G_GRIP, "nico's hand closes on the iron rod: soft metal clink", "metal_clink", impact_frame=S.G_GRIP)
add(S.SNAP1[0], S.SNAP1[1], "reframe onto padre (soft whoosh)", "camera_snap")
add(S.Q0, S.Q1, "padre speaks the quoted line (the narration carries the words; mouth moves here only)", "dialogue")
add(S.SNAP2[0], S.SNAP2[1], "reframe onto nico with the rod (whoosh); padre lets go at g %d, the rod shifts in nico's grip (small iron tick)" % S.G_LET, "camera_snap")
add(S.G_LET, S.G_LET, "rod changes hands (iron tick)", "metal_clink", impact_frame=S.G_LET)
json.dump(dict(take="s14", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (LAST - FIRST) / 15.0)) for i in range(16)]
L.contact(OUT, gs, {g: ("talk " + str(S.mouth(g))) if S.mouth(g) else "" for g in gs}, os.path.join(HERE, "contact.jpg"))

q = ["raw g %d..%d: %d frames, wall %.2f s, cpu %.2f s per frame" % (FIRST, LAST, len(rows), meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"])]
q += L.heads_summary([r for r in rows if S.G0 <= r["g"] < S.G_END])
q.append("hand pin (nico's right hand on the rod, solve error D): max %.4f over g %d..%d" % (max(r.get("err", 0) for r in rows), S.G_GRIP - 11, LAST))
q.append("mouth drawings used: %s" % sorted({str(r.get("mouth")) for r in rows}))
q.append("mouth outside the quote: %s" % [r["g"] for r in rows if r.get("mouth") and not (S.Q0 <= r["g"] <= S.Q1)])
q.append("camera: %s" % json.dumps(L.cam_report(S.cam, FIRST, LAST, depth=5.0)))
q.append("retried: %s" % [r["g"] for r in rows if r.get("retried")])
pops, still, bad = L.popcheck(OUT, FIRST, LAST)
q.append("popcheck: %s; near-still transitions: %s; magenta frames: %s" % (pops, still, bad))
fr = lambda a, b: [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)]
q.append(L.hue_rows([("s14 shot 14 (g 1026-1150)", fr(S.G0, S.G_END - 1)), ("s14 all (g 1018-1158)", fr(FIRST, LAST)),
                     ("ref a t0062 t0040 t0072", [os.path.join(L.PROJ, "ref", "a", "t%04d.jpg" % k) for k in (62, 40, 72)])]))
open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(q) + "\n")
print("\n".join(q))
print("delivered", len(src), "frames ->", out, n)
