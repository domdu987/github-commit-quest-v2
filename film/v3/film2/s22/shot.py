#!/usr/bin/env python3
"""shot.py -- film 2 take s22: shot 22 (g 1844..1967, the end of the film; in-handle g 1835..1843 for the 15f dissolve in),
room DAWN push_rod.

    Quiet attic at dawn: a slow push from the push_rod camera to the iron rod leaning beside the bed, where he left it; held to
    the end of the film. The push is three eased segments joined on the words (speed / aim changes are the framing changes):
    g 1835 -> 1880 ("ยังพิงอยู่"), 1880 -> 1914 ("ตรงที่เขาวางไว้"), 1914 -> 1968 (slow creep, never parks). Out: end of film.

    python3 shot.py stills <a:b:step> <out_dir> [scale] [samples]
    python3 shot.py final <a:b>
    python3 shot.py deliver
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s19"))
import fx
from fx import g_of, g_cut

G0 = g_cut(61.45)                 # 1844
G1 = 1968                         # end of film (exclusive)
DISS_IN = 15
H_IN = DISS_IN // 2 + 2           # 9
FIRST, LAST = G0 - H_IN, G1 - 1   # 1835 .. 1967
G_LEAN = g_of(62.582)             # 1880 "ยังพิงอยู่"
G_PUT = g_of(63.713)              # 1914 "ตรงที่เขาวางไว้"


def cam(g):
    from anim import keys, lerp
    ks = [(FIRST, (-1.60, -5.85, 1.95, 1.45, -3.55, 0.55), "sine"),
          (G_LEAN, (-0.95, -5.45, 1.80, 1.52, -3.70, 0.52), "sine"),
          (G_PUT, (-0.55, -5.15, 1.68, 1.56, -3.80, 0.50), "sine"),
          (G1 + 6, (-0.30, -4.95, 1.62, 1.58, -3.86, 0.50), "hold")]
    v = lerp(keys(g, ks), keys(g, [(f, x, "lin") for f, x, e in ks]), 0.25)
    roll = 0.6 * math.sin((g - FIRST) * 0.035)
    return v[:3], v[3:], roll


def build():
    import bpy
    import room as R
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    A = R.build("DAWN")
    R.setup_render(scene, "final")
    c = R.make_camera(A["cams"]["push_rod"]); c.data.clip_start = 0.02
    return dict(scene=scene, cam=c, A=A)


def apply(ctx, g):
    loc, look, roll = cam(g)
    fx.set_cam(ctx["cam"], loc, look, roll)
    ctx["scene"].frame_set(1)


def deliver():
    import shutil
    fr = os.path.join(HERE, "frames"); os.makedirs(fr, exist_ok=True)
    files = {}
    for g in range(FIRST, LAST + 1):
        src = os.path.join(HERE, "raw", "s22", "g_%04d.png" % g); dst = os.path.join(fr, "g_%04d.png" % g)
        shutil.copyfile(src, dst); files[g] = dst
    js = [json.load(open(os.path.join(HERE, "raw", "s22", "g_%04d.json" % g))) for g in range(FIRST, LAST + 1)]
    wall = sum(j["wall"] for j in js) / len(js); cpu = sum(j["cpu"] for j in js) / len(js)
    fx.contact(files, os.path.join(HERE, "contact.jpg"), label=lambda g: "handle" if g < G0 else "s22")
    fx.encode(HERE, FIRST)
    meta = {"take": "s22", "shots": [22], "g0": G0, "g1": G1, "handle_in": H_IN, "handle_out": 0,
            "first_g": FIRST, "n_frames": LAST - FIRST + 1,
            "transition_in": {"type": "dissolve", "frames": DISS_IN, "note": "in-handle g %d..%d rendered in 3D (the push continues backward)" % (FIRST, G0 - 1)},
            "transition_out": {"type": "end", "frames": 0, "note": "last frame of the film g 1967"},
            "set": "v3/set3d2/room.py", "light": "DAWN", "camera": "push_rod (custom three-segment push)",
            "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(wall, 2), "s_per_frame_cpu_mean": round(cpu, 2),
            "events": {"push_segment_lean": G_LEAN, "push_segment_put": G_PUT}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
    t = lambda g: round(g / 30.0, 3)
    ev = []

    def add(a, b, label, kind, **kw):
        e = dict(time=t(a), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label); e.update(kw); ev.append(e)
    add(FIRST, LAST + 1, "quiet dawn attic: early birds outside the window, soft room tone (after the explosion: silence first, birds fade in)", "ambience")
    add(G0 + 20, G0 + 60, "a single bird call close to the window", "birds")
    add(G_PUT, LAST + 1, "very soft wind on the roof tiles, a beam creaks once (optional); hold to the end", "ambience")
    json.dump(dict(take="s22", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev),
              open(os.path.join(HERE, "cues.json"), "w"), indent=1)
    print(fx.hue_rows([("s22 shot 22 (g %d-%d)" % (FIRST, LAST), [files[g] for g in sorted(files)])]))
    d = fx.motion_stats([files[g] for g in sorted(files)])
    print("frame diff min %.3f median %.3f max %.3f" % (min(d), sorted(d)[len(d) // 2], max(d)))
    print("s/frame wall %.2f cpu %.2f" % (wall, cpu))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "deliver":
        deliver(); sys.exit()
    gs = [g for g in fx.parse(sys.argv[2]) if FIRST <= g <= LAST]
    if cmd == "stills":
        out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        ctx = build()
        for g in gs:
            apply(ctx, g)
            w, c = fx.render_frame(ctx["scene"], os.path.join(out, "s22_g_%04d.png" % g), samples, scale)
            print("g %d %.1f s" % (g, w), flush=True)
    elif cmd == "final":
        fx.run_final(HERE, "s22", gs, build, apply)
