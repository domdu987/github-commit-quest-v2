"""walk_kong.py -- Kong walking 3 s in the hook set (blocky cast), 360x640, camera tracking from the front 3/4,
with the planted-foot drift measured on the evaluated boot-sole meshes.  -> walk_kong.mp4, out/walk_drift.json

    nice -n 5 python3 walk_kong.py [--frames 72] [--tier draft] [--kind walk]
"""
import os, sys, math, json, time, argparse, subprocess, resource
HERE = os.path.dirname(os.path.abspath(__file__))
HC = os.path.join(HERE, "hookcopy"); sys.path.insert(0, HC); os.chdir(HC)
ap = argparse.ArgumentParser(); ap.add_argument("--frames", type=int, default=72); ap.add_argument("--tier", default="draft")
ap.add_argument("--kind", default="walk"); ap.add_argument("--measure-only", action="store_true"); a = ap.parse_args()
import numpy as np
import common as C
import stage
import bpy
from mathutils import Vector
import blockcast as BC

G0 = 903                                   # film clock for rain / beacons (S19's time: the crew walk in the cut)
OUT = os.path.join(HERE, "out", "walk_%s" % a.kind); os.makedirs(OUT, exist_ok=True)


class _Shot:                               # a neutral "shot" for Stage.begin
    ID = "S19"


F = stage.Stage(a.tier, 360, 640, threads=2)
F.begin(_Shot)
for x in F.cast: x.fig.hide(True)
K = F.kong; fig = K.fig
# the path: search start points / directions around the phone mark for a clear deck along the walk and a clear line of
# sight from Kong to the tracking camera on every sampled frame (the first version tracked the lens into the work lamp)
G_ = BC.GAITS[a.kind]
span = G_["v"] * a.frames / 24.0 * fig.scale
dg = bpy.context.evaluated_depsgraph_get()
def cam_for(root, d, side):
    return root + d * 4.6 + side * 2.6 + Vector((0, 0, 1.85)), root + d * 0.4 + Vector((0, 0, 1.45))
def blocked(p, q):
    v = q - p; L = v.length
    hit, loc, n, i, ob, m = F.sc.ray_cast(dg, p, v.normalized(), distance=L)
    return hit and not ob.name.startswith(fig.name)
best = None
for ox, oy in ((0, 0), (2, 0), (-2, 0), (0, 2), (0, -2), (3, 3), (-3, 3), (3, -3), (-3, -3), (5, 0), (-5, 0), (0, 5), (0, -5)):
    for ang in range(0, 360, 20):
        d = Vector((math.sin(math.radians(ang)), -math.cos(math.radians(ang)), 0))
        side = Vector((-d.y, d.x, 0))
        start = Vector((F.PM.x + ox, F.PM.y + oy, 0.0))
        bad = 0
        for k in range(9):
            r = start + d * (span * k / 8.0)
            if not F.free(r.x, r.y, 0.55): bad += 1
            c, lk = cam_for(r, d, side)
            if blocked(lk, c) or blocked(r + Vector((0, 0, 0.6)), c): bad += 1
            if c.z - F.top(c.x, c.y, c.z + 0.5) < 0.6: bad += 1
        score = bad + 0.02 * (abs(ox) + abs(oy))
        if best is None or score < best[0]: best = (score, start, d, ang)
    if best and best[0] == 0: break
score, start, d, ang = best
side = Vector((-d.y, d.x, 0))
print("path from", tuple(start), "dir", tuple(d), "deg", ang, "length %.2f BU" % span, "problems", score, flush=True)


def sole_bottom_world(side_):
    """mean world position of the sole object's lowest vertices (the evaluated mesh, not a rig point)."""
    ob = bpy.data.objects[fig.name + "_sole_" + side_]
    me = ob.data
    co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    low = co[:, 2] <= co[:, 2].min() + 1e-5
    p = co[low].mean(0)
    return np.array(ob.matrix_world @ Vector(p))


rec = []
t_all = time.time()
for i in range(a.frames):
    t = i / 24.0
    g = G0 + i
    F.sc.frame_set(g + 1)
    info = fig.gait_pose(t, a.kind, path0=tuple(start), direction=tuple(d))
    fig.hide(False); fig.set_pass_index(2)
    bpy.context.view_layer.update()
    root = Vector(fig.root.location)
    # camera: front 3/4, tracking the root (eye a little above his chest), slow
    cam_loc, look = cam_for(root, d, side)
    F.camera(cam_loc, look, 32.0, focus=root + Vector((0, 0, 1.6)), k=6.0, kmax=16)
    rowd = dict(i=i, t=round(t, 4), phase=info["phase"], beta=info["beta"])
    for s_ in ("L", "R"):
        rowd["sole_" + s_] = [round(float(x), 6) for x in sole_bottom_world(s_)]
    rec.append(rowd)
    if a.measure_only: continue
    if int(os.environ.get("WALK_EVERY", "1")) > 1 and i % int(os.environ["WALK_EVERY"]): continue
    out = os.path.join(OUT, "f_%04d" % (i + 1))
    if os.path.exists(out + ".png"): continue
    if i == 0:                                   # the work lamp off to his left, behind the camera line, aimed at the path
        lb = start + d * span * 0.5 - side * 7.0
        F.lamp((lb.x, lb.y), tuple(start + d * span * 0.5 + Vector((0, 0, 1.2))), 8000.0, heads=[K.head()])
    r0 = resource.getrusage(resource.RUSAGE_SELF); w0 = time.time()
    r = F.render(out, g, {"exposure": 1.6, "sharp_idx": [2]})
    r1 = resource.getrusage(resource.RUSAGE_SELF)
    rowd["cpu"] = round((r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), 2); rowd["wall"] = round(time.time() - w0, 2)
    for suf in ("_rgb.exr", "_z.exr", "_idx.exr", "_env.exr", "_shafts.pkl", "_info.json", "_raw.png", "_depth.png"):
        if os.path.exists(out + suf): os.remove(out + suf)
    print("frame", i, rowd.get("cpu"), flush=True)

# ------------------------------------------------------------------------------------------------ drift
BU_CM = 60.0                                   # 1 stage unit = 0.6 m
drift = {"L": [], "R": []}
travel = []
for s_ in ("L", "R"):
    seg = None
    for r_ in rec:
        ph = r_["phase"][s_]
        if ph < r_["beta"]:
            p = np.array(r_["sole_" + s_])
            if seg is None: seg = dict(start=p, i0=r_["i"], max=0.0, n=0, root0=None)
            dd = float(np.linalg.norm((p - seg["start"])[:2])) * BU_CM
            dz = abs(float(p[2] - seg["start"][2])) * BU_CM
            seg["max"] = max(seg["max"], math.hypot(dd, dz)); seg["n"] += 1
        else:
            if seg is not None and seg["n"] > 1: drift[s_].append(dict(first_frame=seg["i0"], frames=seg["n"], max_cm=round(seg["max"], 4)))
            seg = None
    if seg is not None and seg["n"] > 1: drift[s_].append(dict(first_frame=seg["i0"], frames=seg["n"], max_cm=round(seg["max"], 4)))
allmax = max([x["max_cm"] for v in drift.values() for x in v] or [0])
v_ms = G_["v"] * fig.scale * 0.6                # stage speed in real metres per second (1 BU = 0.6 m)
res = dict(kind=a.kind, frames=a.frames, gait=G_, speed_set_m_s=round(v_ms, 3), stances=drift, max_planted_drift_cm=allmax,
           root_travel_per_stance_cm=round(G_["v"] * G_["T"] * G_["beta"] * fig.scale * BU_CM, 1),
           method="sole object's lowest vertices (evaluated mesh) in world space, every frame of every stance vs the stance's first frame",
           cpu_per_frame=[r_.get("cpu") for r_ in rec if r_.get("cpu")], wall_s=round(time.time() - t_all, 1))
json.dump(dict(res, per_frame=rec), open(os.path.join(HERE, "out", "walk_drift_%s.json" % a.kind), "w"), indent=1)
print("DRIFT", json.dumps({k: v for k, v in res.items() if k != "cpu_per_frame"}))
if not a.measure_only and int(os.environ.get("WALK_EVERY", "1")) == 1:
    mp4 = os.path.join(HERE, "walk_kong.mp4" if a.kind == "walk" else "run_kong.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "24", "-i", os.path.join(OUT, "f_%04d.png"), "-c:v", "libx264", "-crf", "16",
                    "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4], check=True)
    print("wrote", mp4)
