#!/usr/bin/env python3
"""deliver.py -- s12: raw/s12 + raw/s13 -> frames/g_%04d.png (10-frame dissolve 12 -> 13 mixed in), take.mkv, meta.json,
cues.json, contact.jpg, work/qa.txt.   python3 deliver.py"""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deliver_lib as L

G0, G_S13, G_END, H_IN, DISS, H_OUT = 883, 959, 1026, 6, 10, 8
D0 = G_S13 - DISS // 2
FIRST, LAST = G0 - H_IN, G_END + H_OUT - 1        # 877..1033
RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
raw = lambda s, g: os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)

src = {}
for g in range(FIRST, LAST + 1):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    if g < D0:
        L.shutil.copyfile(raw(12, g), dst); src[g] = "s12"
    elif g < D0 + DISS:
        w = L.smoothstep_mix(g - D0 + 1, DISS)
        L.mix_files(raw(12, g), raw(13, g), w, dst); src[g] = "s12*%.3f+s13*%.3f" % (1 - w, w)
    else:
        L.shutil.copyfile(raw(13, g), dst); src[g] = "s13"
out, n = L.encode(HERE, FIRST)
assert n == LAST - FIRST + 1, n

rows = {s: [json.load(open(f)) for f in sorted(glob.glob(os.path.join(RAW, "s%d" % s, "g_*.json")))] for s in (12, 13)}
allr = rows[12] + rows[13]
meta = {"take": "s12", "shots": [12, 13], "g0": G0, "g1": G_END, "first_g": FIRST, "n_frames": n,
        "handle_in": H_IN, "handle_out": H_OUT,
        "transition_in": {"type": "dissolve", "frames": 9, "note": "handle g 877..882 rendered in 3D (shot 12 camera runs back)"},
        "transition_out": {"type": "dissolve", "frames": 12, "note": "handle g 1026..1033 rendered in 3D (shot 13 camera continues)"},
        "internal": [{"at": G_S13, "type": "dissolve", "frames": DISS, "mixed": [D0, D0 + DISS - 1], "from_shot": 12, "to_shot": 13,
                      "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 12 to g 965, shot 13 from g 952 (raw/)"}],
        "shot_ranges": {"12": [G0, G_S13 - 1], "13": [G_S13, G_END - 1]},
        "set": "v3/set3d2/tower.py", "light": "NIGHT_STORM", "rod": "set_rod(1) throughout (shot 13: a 2.2x thicker, moonlit copy so it reads from the town)",
        "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean([r["wall"] for r in allr])), 2),
        "s_per_frame_cpu_mean": round(float(np.mean([r["cpu"] for r in allr])), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

sys.argv = [sys.argv[0]]
import shot as S                                    # noqa: E402  (timing constants only; builds nothing on import)
ev = []
t = lambda g: round(g / 30.0, 3)


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(FIRST, D0 + DISS, "heavy rain on the tower and the stone sills, wind through the open arches (bed under shot 12)", "ambience")
for g in range(FIRST, D0 + DISS):
    a0, a1 = S.bell_angle(g - 1), S.bell_angle(g)
    if g > FIRST and (a0 > 0) != (a1 > 0) and a1 > a0:
        pass
    # the clapper strikes at each end of the swing (angle extremes)
    a2 = S.bell_angle(g + 1)
    if (a1 > a0 and a1 > a2) or (a1 < a0 and a1 < a2):
        add(g, g, "big bronze bell strike (clapper at the end of the swing), loud and close, long ring tail", "bell", impact_frame=g)
for g in range(FIRST, D0 + DISS):
    if abs(S.pull(g, 0.0) - 1.0) < 0.02 and S.pull(g - 1, 0.0) < S.pull(g, 0.0):
        add(g - 4, g, "ropes creak and snap taut as the four ringers haul (rope creak, grunt-free)", "rope", peak_frame=g)
for s, seq in S.FLASH12:
    add(s, s + len(seq), "lightning flash outside the arches (white light through the openings)", "flash")
    add(s + 6, s + 50, "thunder, close and rolling", "thunder")
add(S.SNAP12[0], S.SNAP12[1], "snap reframe onto nico lifted by his rope (short whoosh)", "camera_snap")
add(D0, D0 + DISS, "dissolve to the town in the storm", "dissolve")
add(G_S13 - 5, LAST + 1, "rain over the whole town, distant bells still ringing (soft), wind", "ambience")
for s, seq in S.FLASH13:
    add(s, s + len(seq), "lightning flash lights the clouds over the town", "flash")
    add(s + 10, s + 60, "thunder far away (no strike nearby)", "thunder_far")
for a, b, nm in S.BOLT13:
    add(a, b + 1, "forked bolt far over the hills (%s), far crack" % ("right" if nm.endswith("r") else "left"), "bolt_far")
add(S.SNAP13[0], S.SNAP13[1], "eased reframe up to the tower top: the rod, untouched", "camera_move")
json.dump(dict(take="s12", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (LAST - FIRST) / 15.0)) for i in range(16)]
L.contact(OUT, gs, src, os.path.join(HERE, "contact.jpg"))

q = []
for s in (12, 13):
    a, b = S.RANGES[s]
    q.append("shot %d raw g %d..%d: %d frames, wall %.2f s, cpu %.2f s per frame" % (s, a, b, len(rows[s]), np.mean([r["wall"] for r in rows[s]]), np.mean([r["cpu"] for r in rows[s]])))
    own = [r for r in rows[s] if (G0 <= r["g"] < G_S13 if s == 12 else G_S13 <= r["g"] < G_END)]
    q += ["  " + x for x in L.heads_summary(own)]
    q.append("  camera: %s" % json.dumps(L.cam_report(S.CAMS[s], a, b, depth=4.0 if s == 12 else 30.0)))
    q.append("  retried: %s" % [r["g"] for r in rows[s] if r.get("retried")])
pops, still, bad = L.popcheck(OUT, FIRST, LAST)
q.append("popcheck: %s; near-still transitions: %s; magenta frames: %s" % (pops, still, bad))
fr = lambda a, b: [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)]
q.append(L.hue_rows([("s12 shot 12 (g 883-958)", fr(G0, G_S13 - 1)), ("s12 shot 13 (g 959-1025)", fr(G_S13, G_END - 1)),
                     ("s12 all (g 877-1033)", fr(FIRST, LAST)),
                     ("ref a t0080 t0096", [os.path.join(L.PROJ, "ref", "a", "t%04d.jpg" % k) for k in (80, 96)])]))
open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(q) + "\n")
print("\n".join(q))
print("delivered", len(src), "frames ->", out, n)
