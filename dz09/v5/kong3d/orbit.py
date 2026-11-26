"""orbit.py -- 4 s orbit of the 3D Kong in the expressway set, 360x640, 30 fps -> out/orbit_kong3d.mp4
python3 orbit.py [frames=120] [quality=draft] [threads=4]"""
import os, sys, math, time, json, subprocess, resource
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shots as S
import bpy
from mathutils import Vector
import kong3d as K

N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
Q = sys.argv[2] if len(sys.argv) > 2 else "draft"
TH = int(sys.argv[3]) if len(sys.argv) > 3 else 4
A = S.X.build(); A, right, fwd = S.frame_vectors()
S.X.setup_render(quality=Q, threads=TH)
kong, drv = S.stage(A, right, fwd)
M = Vector(A["kong_phone_mark"]) + Vector((0.3, 0.6, 0))       # a clear spot between lanes 1 and 2
kong.place(M, K.facing_toward(M, M - fwd))
kong.pose(expr="determined", head=(0, -4, 0), legs="wide",
          cutter=dict(at=(-0.36, -0.40, 1.02), fwd=(0.58, -0.22, 0.78), up=(0.15, -0.95, 0.05),
                      pole_r=(-1.0, 0.3, 0.5), pole_l=(1.0, -0.4, 0.2)))
kong.set_pass_index(2)
fill = S.kong_light("k3_fill_orbit", M + Vector((0, 0, 4.0)) - fwd * 2.0, M + Vector((0, 0, 1.5)), 60, (0.62, 0.72, 1.0), 3.0,
                    S.cast_objects(kong))
d = os.path.join(S.OUT, "orbit"); os.makedirs(d, exist_ok=True)
R, Z = 3.7, 1.55
cpu = []
for i in range(N):
    t = i / N
    a = math.radians(-80 + 250 * t)                # 250 deg sweep on the open side (the hero car blocks the rest)
    base = -fwd
    dirv = Vector((base.x * math.cos(a) - base.y * math.sin(a), base.x * math.sin(a) + base.y * math.cos(a), 0))
    loc = M + dirv * R + Vector((0, 0, Z + 0.35 * math.sin(math.pi * t)))
    cam = S.set_cam(loc, M + Vector((0, 0, 1.55)), 26, kong.head_world(), 2.2, "k3_orbit", scale=0.5)
    r = S.X.render_still(os.path.join(d, f"f{i:04d}"), frame=i + 1)
    cpu.append(r["cpu_render"] + r.get("cpu_post", 0))
    for ext in ("_rgb.exr", "_env.exr", "_idx.exr", "_z.exr", "_raw.png", "_depth.png"):
        p = os.path.join(d, f"f{i:04d}{ext}")
        if os.path.exists(p): os.remove(p)
    print(i, round(cpu[-1], 1), flush=True)
mp4 = os.path.join(S.OUT, "orbit_kong3d.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", os.path.join(d, "f%04d.png"), "-c:v", "libx264",
                "-pix_fmt", "yuv420p", "-crf", "18", mp4], check=True)
json.dump(dict(frames=N, quality=Q, threads=TH, cpu_mean=round(sum(cpu) / len(cpu), 2), cpu_max=round(max(cpu), 2)),
          open(os.path.join(S.OUT, "orbit_timing.json"), "w"), indent=1)
print("mp4", mp4)
