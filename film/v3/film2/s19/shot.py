#!/usr/bin/env python3
"""shot.py -- film 2 take s19: shot 19 (g 1585..1659, in-handle g 1578..1584 for the 10f dissolve in), tower NIGHT_STORM.

    The empty finial in the rain, no rod (set_rod(0)). Slow eased push toward the copper spike from the spire_insert side;
    on "ไม่มีไม้จิ้มฟ้าแล้ว" (t 54.21, g 1629) the push quickens and tilts up onto the empty air above the spike, where the
    rod used to stand. A faint far flicker in the clouds at g 1603 (sky bolt, flash 0.3) for the thunder. Rain streaks
    (fx.Rain) all through. Out: hard cut to s20 (no out-handle).

    python3 shot.py stills <a:b:step> <out_dir> [scale] [samples]
    python3 shot.py final <a:b>          (raw/s19/g_%04d.png, resumable)
    python3 shot.py deliver
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fx
from fx import g_of, g_cut

G0, G1 = g_cut(52.84), g_cut(55.35)          # 1585, 1660 (exclusive)
DISS_IN = 10
H_IN = DISS_IN // 2 + 2                       # 7
FIRST, LAST = G0 - H_IN, G1 - 1               # 1578 .. 1659
G_NOROD = g_of(54.21)                         # 1629 "ไม่มีไม้จิ้ม"
G_FAR = g_of(53.37) + 3                       # 1607: far flicker after "บนยอดหอ"
FINIAL = (0.0, 0.0, 28.45)


def cam(g):
    from anim import keys, lerp
    #            dist   yaw    pitch  look z
    ks = [(FIRST, (3.4, 43.0, 4.0, 27.85), "sine"),
          (G_NOROD - 4, (2.7, 46.0, 5.5, 27.95), "quint"),
          (G_NOROD + 10, (2.05, 50.0, 9.5, 28.30), "sine"),
          (LAST + 1, (1.75, 52.0, 11.0, 28.40), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.15)
    dist, yaw, pitch, lz = k
    yr, pr = math.radians(yaw), math.radians(pitch)
    look = (0.02, 0.0, lz)
    d = (math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr))
    loc = (look[0] - d[0] * dist, look[1] - d[1] * dist, look[2] - d[2] * dist)
    roll = 1.2 * math.sin((g - FIRST) * 0.05)       # a slow sway in the wind
    return loc, look, roll


def flick(g):
    return {G_FAR: 0.3, G_FAR + 1: 0.08, G_FAR + 2: 0.22}.get(g, 0.0)


def build():
    import bpy
    import tower as T
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    A = T.build("NIGHT_STORM")
    T.setup_render(scene, "final")
    mk = bpy.data.objects.get("market")
    if mk is not None:
        mk.hide_render = True
    T.set_rod(0)
    c = T.make_camera(A["cams"]["spire_insert"], name="cam_s19"); c.data.clip_start = 0.02
    rain = fx.Rain(n=650, size=(8.0, 8.0, 10.0), ahead=3.5, speed=1.2, length=0.7, width=0.006, strength=0.32, near=0.8)
    return dict(scene=scene, T=T, cam=c, rain=rain)


def apply(ctx, g):
    T = ctx["T"]
    loc, look, roll = cam(g)
    fx.set_cam(ctx["cam"], loc, look, roll)
    s = flick(g)
    T.flash(s)
    T.set_bolt(s >= 0.2, target="sky")
    ctx["rain"].update(g, loc, look)
    ctx["scene"].frame_set(1)


def report(ctx, g):
    return dict(flash=flick(g))


def deliver():
    from PIL import Image
    fr = os.path.join(HERE, "frames"); os.makedirs(fr, exist_ok=True)
    files = {}
    for g in range(FIRST, LAST + 1):
        src = os.path.join(HERE, "raw", "s19", "g_%04d.png" % g); dst = os.path.join(fr, "g_%04d.png" % g)
        import shutil; shutil.copyfile(src, dst); files[g] = dst
    js = [json.load(open(os.path.join(HERE, "raw", "s19", "g_%04d.json" % g))) for g in range(FIRST, LAST + 1)]
    wall = sum(j["wall"] for j in js) / len(js); cpu = sum(j["cpu"] for j in js) / len(js)
    fx.contact(files, os.path.join(HERE, "contact.jpg"), label=lambda g: "handle" if g < G0 else "s19")
    fx.encode(HERE, FIRST)
    meta = {"take": "s19", "shots": [19], "g0": G0, "g1": G1, "handle_in": H_IN, "handle_out": 0,
            "first_g": FIRST, "n_frames": LAST - FIRST + 1,
            "transition_in": {"type": "dissolve", "frames": DISS_IN, "note": "in-handle g %d..%d rendered in 3D (camera continues backward)" % (FIRST, G0 - 1)},
            "transition_out": {"type": "cut", "frames": 0},
            "set": "v3/set3d2/tower.py", "light": "NIGHT_STORM", "camera": "spire_insert (custom push)", "rod": "set_rod(0) throughout",
            "samples": 12, "resolution": [720, 1280], "threads": 2,
            "s_per_frame_wall_mean": round(wall, 2), "s_per_frame_cpu_mean": round(cpu, 2),
            "events": {"far_flicker": G_FAR, "push_quickens_norod": G_NOROD}}
    json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
    t = lambda g: round(g / 30.0, 3)
    ev = []

    def add(a, b, label, kind, **kw):
        e = dict(time=t(a), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label); e.update(kw); ev.append(e)
    add(FIRST, LAST + 1, "steady heavy rain on the spire tiles and copper (bed, carries on under s20)", "ambience")
    add(FIRST, LAST + 1, "wind gusting round the spire top", "ambience")
    add(G_FAR, G_FAR + 3, "faint far flicker in the clouds", "flash")
    add(G_FAR + 14, G_FAR + 60, "low distant thunder roll (after the far flicker)", "thunder")
    add(G_NOROD - 4, G_NOROD + 10, "push quickens onto the empty spike ('mai mi mai chim fa laeo'): soft low whoosh, optional", "camera_move")
    json.dump(dict(take="s19", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev),
              open(os.path.join(HERE, "cues.json"), "w"), indent=1)
    print(fx.hue_rows([("s19 shot 19 (g %d-%d)" % (FIRST, LAST), [files[g] for g in sorted(files)])]))
    d = fx.motion_stats([files[g] for g in sorted(files)])
    print("frame diff min %.2f median %.2f max %.2f" % (min(d), sorted(d)[len(d) // 2], max(d)))
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
            w, c = fx.render_frame(ctx["scene"], os.path.join(out, "s19_g_%04d.png" % g), samples, scale)
            print("g %d %.1f s" % (g, w), flush=True)
    elif cmd == "final":
        fx.run_final(HERE, "s19", gs, build, apply, report=report)
