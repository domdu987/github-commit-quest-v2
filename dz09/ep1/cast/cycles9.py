"""cycles9.py -- every EP.1 cycle staged in the v11 expressway set at night, 3/4 tracking camera.

python3 cycles9.py probe                      # ray casts: the free corridor and the roof profile -> out/probe.json
python3 cycles9.py measure                    # no render: sole drift of every cycle on ones -> out/drift.json, out/drift_table.md
python3 cycles9.py render --part 0/2          # draft tier 360x640, drawings on twos -> out/cycles/<take>/f_###.png
python3 cycles9.py mp4                        # -> cycles.mp4 (labels + measured drift burned in), out/cycles_sheet.png
"""
import os, sys, json, math, time, argparse, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "out")
FPS = 24
CORR_X = -6.55            # the gap between lanes 1 and 2 (v10 stage.EXTRA_SPOTS)
TAKES = ["run_kong", "run_james", "run_praew", "run_tos", "sprint_infected", "support_walk", "sit_wheel", "stagger_back", "crouch_hide",
         "roof_run", "bang_glass", "pull_out", "throw_flare", "raise_crowbar"]


class W:
    pass


def build(render=True, threads=1):
    import bpy
    from mathutils import Vector
    import stage9 as S9
    FS = S9.film()
    import beauty as B
    w = W()
    w.bpy, w.V, w.S9, w.FS, w.B = bpy, Vector, S9, FS, B
    t0 = time.time()
    w.A = B.build()
    B.setup_render("preview", threads=threads)
    sc = w.sc = bpy.context.scene
    sc.cycles.samples = 2
    B.X._STATE["pct"] = 100
    sc.render.use_motion_blur = False
    sc.cycles.adaptive_min_samples = min(sc.cycles.adaptive_min_samples, sc.cycles.samples)
    sc.cycles.transparent_max_bounces = max(sc.cycles.transparent_max_bounces, 32)
    sc.render.resolution_x, sc.render.resolution_y = 360, 640
    sc.render.resolution_percentage = 100
    sc.render.fps = FPS
    w.cam = B.X.make_camera()
    sc.camera = w.cam
    for ob in bpy.data.objects:
        for con in ob.constraints:
            if con.type == "TRACK_TO":
                con.target = w.cam
    S9.S8.tune_flat(**dict(S9.S8.FLAT_DEFAULT, EXPO=1.6))
    FS.tune_skin()
    print("set built in %.1f s" % (time.time() - t0), flush=True)
    return w


def camera(w, loc, look, lens=30, focus=None):
    cam = w.cam
    loc, look = w.V(loc), w.V(look)
    cam.rotation_mode = "XYZ"
    cam.location = loc
    cam.rotation_euler = (look - loc).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens; cam.data.clip_start = 0.05
    cam["preset"] = "look"; cam["aspect"] = "9:16"
    cam["focus"] = tuple(focus if focus is not None else look); cam["coc_k"] = 5.0; cam["coc_max"] = 16.0; cam["dof_k"] = 1.0
    w.bpy.context.view_layer.update()
    return cam


def top(w, x, y, z0=9.0):
    dg = w.bpy.context.evaluated_depsgraph_get()
    hit, loc, n, i, ob, m = w.sc.ray_cast(dg, w.V((x, y, z0)), w.V((0, 0, -1)))
    return (loc.z if hit else 0.0), (ob.name if hit else None)


def probe(w):
    res = {}
    for x in (-6.55, -12.35, -3.6, -9.45):
        col = []
        for k in range(-40, 160):
            y = k * 0.5
            zs = [top(w, x + dx, y)[0] for dx in (-0.6, 0.0, 0.6)]
            col.append((y, round(max(zs), 2)))
        res[str(x)] = col
        free = [y for y, z in col if z < 0.2]
        print("x", x, "free samples", len(free), "of", len(col))
        runs, cur = [], None
        for y, z in col:
            if z < 0.2:
                cur = [y, y] if cur is None else [cur[0], y]
            elif cur:
                runs.append(cur); cur = None
        if cur: runs.append(cur)
        print("   free runs:", [r for r in runs if r[1] - r[0] >= 4])
    prof = []
    for k in range(-40 * 4, 160 * 4):
        y = k * 0.125
        z, nm = top(w, -9.45, y)
        prof.append((y, round(z, 3), nm))
    res["roof_-9.45"] = prof
    json.dump(res, open(os.path.join(OUT, "probe.json"), "w"))
    last = None
    for y, z, nm in prof:
        key = (nm or "").split("_")[0:2]
        if z > 0.5 and key != last:
            print("  roof line y=%.1f z=%.2f %s" % (y, z, nm)); last = key
        if z <= 0.5: last = None


# ================================================================================================= the takes
def make_takes(w, only=None):
    """-> {name: dict(frames, setup(), frame(t), measure=[Take, ...], cam(t))}"""
    S9, V = w.S9, w.V
    import gait9, draw9 as D9
    d = V((0.0, -1.0, 0.0))                                 # down the free gap between lanes 1 and 2, toward the camera; the jam is the backdrop
    side = V((-1.0, 0.0, 0.0))                              # the camera stands in the empty stretch of lane 2
    Y0 = 11.6
    T = {}
    actors = {}

    def act(name, spec, **kw):
        if name not in actors:
            actors[name] = S9.actor(name, spec, **kw)
        return actors[name]

    def hide_all():
        for a in actors.values():
            a.hide(True)
        for o in w.extra_objs:
            o.hide_render = True
    w.extra_objs = []

    def track_cam(root, ahead=3.3, out=3.0, h=1.35, look_h=1.35, lens=30):
        # checker: near side-on (about 15 deg off the card's normal).  The first staging stood 48 deg ahead of the runner, so
        # every card was seen at 2/3 width (oval heads, closed strides); shots must stage travelling figures like this too.
        ahead, out = ahead * 0.25, out * 1.15
        loc = root + d * ahead + side * out + V((0, 0, h))
        camera(w, loc, root + V((0, 0, look_h)) + d * 0.35, lens, focus=root + V((0, 0, 1.6)))

    def fill(root):
        fl = w.bpy.data.objects.get("cyc_fill")
        if fl is None:
            ld = w.bpy.data.lights.new("cyc_fill", "POINT"); fl = w.bpy.data.objects.new("cyc_fill", ld); w.sc.collection.objects.link(fl)
            ld.energy = 520.0; ld.color = (0.86, 0.90, 1.0); ld.shadow_soft_size = 0.8
            fl.visible_glossy = False; fl.visible_camera = False
        fl.location = root + d * 0.9 + side * 3.0 + V((0, 0, 0.8))

    def simple(name, spec, cyc_fn, frames, base=None, y_start=None, cam_kw=None, label=None, view="side"):
        def mk():
            a = act(name, spec)
            cyc = cyc_fn(a)
            tk = S9.Take(a, cyc, V((CORR_X, Y0 - (y_start or 0.0), 0.0)), d, view=view, base=base)
            def frame(t, measure=False):
                r = tk.root_world(t)
                track_cam(V((r.x, r.y, 0.0)), **(cam_kw or {}))
                fill(r)
                tk.frame(t, w.cam, measure=measure)
            return dict(frames=frames, frame=frame, takes=[tk], actors=[a], cyc=cyc, label=label or name)
        T[name] = mk

    simple("run_kong", "kong_ep1_03", lambda a: gait9.Run(a.spec, "kong"), 36, base=dict(expr="alarmed", prop_n=dict(type="cutter", bars=3, wet=True, scale=1.3)))
    simple("run_james", "james_wet", lambda a: gait9.Run(a.spec, "james"), 36, base=dict(expr="terrified"))
    simple("run_praew", "praew_wet", lambda a: gait9.Run(a.spec, "praew"), 36, base=dict(expr="alarmed"))
    simple("run_tos", "tos_wet", lambda a: gait9.Run(a.spec, "tos"), 36, base=dict(expr="panicked"))
    simple("stagger_back", "kong_ep1_02", lambda a: gait9.stagger_back(a.spec), 42, y_start=6.0, cam_kw=dict(ahead=3.6, out=3.2))
    simple("throw_flare", "kong_ep1_04", lambda a: gait9.throw_flare(a.spec), 36, y_start=4.0, cam_kw=dict(ahead=3.8, out=3.4, look_h=1.6))
    simple("raise_crowbar", "kong_ep1_06b", lambda a: gait9.raise_crowbar(a.spec), 40, y_start=4.0, cam_kw=dict(ahead=3.9, out=3.2, look_h=1.75, h=1.2))
    simple("bang_glass", "crew_infected", lambda a: gait9.bang_glass(a.spec), 40, y_start=4.0, cam_kw=dict(ahead=3.2, out=3.0))
    simple("crouch_hide", "kong_ep1_04", lambda a: gait9.hold(a.spec, D9.poses(a.spec, "crouch_hide", view="q"), 1.0, breath=1.0), 24, y_start=4.0,
           cam_kw=dict(ahead=3.0, out=2.6, h=1.0, look_h=0.95), view="q")
    simple("sit_wheel", "crew_grey2", lambda a: gait9.hold(a.spec, D9.poses(a.spec, "sit_wheel", slump=0.5, expr="fading"), 1.25, shiver=1.0), 30, y_start=4.0,
           cam_kw=dict(ahead=2.2, out=3.2, h=0.9, look_h=0.75))

    def mk_sprint():
        specs = D9.infected_crowd(14)
        lead = act("inf_junior", "crew_infected")
        others = [act("inf_%d" % i, specs[i], ppd=200) for i in (2, 6, 9)]
        cyc = [gait9.Sprint(lead.spec, phase=0.0, style="reach", seed=1)] + [gait9.Sprint(o.spec, phase=0.23 * (k + 1), seed=k + 5) for k, o in enumerate(others)]
        offs = [(0.0, 0.0), (-1.55, -0.60), (1.45, 0.55), (-3.0, 0.35)]
        tks = [S9.Take(a, c, V((CORR_X + ox, 9.6 - oy, 0.0)), d) for a, c, (oy, ox) in zip([lead] + others, cyc, offs)]
        sils = [S9.Sil("sil%d" % k, specs[(k * 3 + 1) % 14], seed=k + 11) for k in range(5)]
        w.extra_objs += [s_.ob for s_ in sils]
        def frame(t, measure=False):
            r = tks[0].root_world(t)
            track_cam(V((r.x, r.y + 0.6, 0.0)), ahead=1.2, out=5.6, lens=26)
            fill(r)
            for tk in tks:
                tk.frame(t, w.cam, measure=measure)
            for k, s_ in enumerate(sils):
                s_.ob.hide_render = True          # checker: the far silhouettes read as black smears at this distance; see crowd.png for them
                s_.frame(t, (CORR_X + 3.0 + 0.9 * k, 11.5 - 1.5 * k + 0.8 * (k % 2) - s_.v * t, 0.0), w.cam)
        return dict(frames=36, frame=frame, takes=tks, actors=[lead] + others, cyc=cyc[0], label="sprint_infected")
    T["sprint_infected"] = mk_sprint

    def mk_support():
        k, j = act("kong_s", "kong_ep1_02"), act("jun_s", "crew_treated")
        cyc = gait9.SupportWalk(k.spec, j.spec, k.sc, j.sc)
        tk = S9.Take(k, cyc, V((CORR_X, Y0 - 3.0, 0.0)), d)
        tj = S9.Take(j, cyc, V((CORR_X - 0.42, Y0 - 3.0, 0.0)), d, root_fn=cyc.root_b)
        j.set_glow(None, 0.0)
        def frame(t, measure=False):
            r = tk.root_world(t)
            track_cam(V((r.x, r.y + 0.33, 0.0)), ahead=3.3, out=3.4)          # centred on the pair, not on Kong
            fill(r)
            k.place(tuple(r), S9.facing(d))
            rel = k._cam_rel(w.cam); s = -1 if rel > 0 else 1
            pk, pj = cyc.pose(t, s=s, view="side")
            tk.frame(t, w.cam, p=pk, measure=measure, s=s)
            tj.frame(t, w.cam, p=pj, measure=measure, s=s)
        return dict(frames=54, frame=frame, takes=[tk, tj], actors=[k, j], cyc=cyc, label="support_walk")
    T["support_walk"] = mk_support

    def mk_pull():
        k, tz = act("kong_p", "kong_ep1_03"), act("tos_p", "tos_wet")
        cyc = gait9.pull_out(k.spec)
        tk = S9.Take(k, cyc, V((CORR_X, Y0 - 6.0, 0.0)), d)
        pz = D9.poses(tz.spec, "pulled", s=1)
        def frame(t, measure=False):
            r = tk.root_world(t)
            track_cam(V((CORR_X, Y0 - 6.6, 0.0)), ahead=3.6, out=3.3, h=1.1, look_h=0.95)
            fill(r)
            fig = tk.frame(t, w.cam, measure=measure)
            s = fig["s"]
            near = "L" if s > 0 else "R"
            hand = k.world_of(fig["anchors"]["wrist_" + near], 2.5)
            # Tos: a card rolled about 80 deg (head toward the rescuer), dragged by the wrists; it rights itself a little as he comes out
            u = min(1.0, t / cyc.dur)
            tz.roll_deg = (80.0 - 22.0 * u) * (1 if s > 0 else -1) * -1
            tz.roll_about = 0.0
            tz.place((hand.x, hand.y, 0.0), S9.facing(d))
            tz.walk_lock = k.walk_lock
            f2 = S9.pose(tz, dict(pz, s=-s, blink=0), w.cam, view="q")
            wz = tz.world_of(f2["anchors"]["wrist_" + ("L" if -s > 0 else "R")], 2.5)
            root = w.V(tz.root.location) + (hand - wz)
            tz.root.location = (root.x, root.y, max(root.z, -0.2))
        return dict(frames=40, frame=frame, takes=[tk], actors=[k, tz], cyc=cyc, label="pull_out")
    T["pull_out"] = mk_pull

    def mk_roof():
        import numpy as np
        # proof staging only: car l1_a is slid up behind l1_e (1.2 BU apart) in THIS process, as the EP.1 jam dressing
        # will have them; the roof heights are read by ray casts (light cones and steam are not surfaces)
        if not w.__dict__.get("moved"):
            for ob in w.bpy.data.objects:
                if ob.name.startswith("l1_a") and (ob.parent is None or not ob.parent.name.startswith("l1_a")):
                    ob.location.y -= 5.7
            w.bpy.context.view_layer.update(); w.moved = True
        bad = ("beam", "steam", "cone", "rain", "shaft", "glow", "halo", "smoke")
        RX = -3.55
        ya, za = [], []
        for k in range(-70, 130):
            y = k * 0.125
            z, nm = top(w, RX, y)
            ya.append(y); za.append(z if (nm and not any(b_ in nm for b_ in bad)) else 0.0)
        ya = np.array(ya); za = np.array(za)
        best = -5.6
        dR, sideR = V((0.0, 1.0, 0.0)), V((-1.0, 0.0, 0.0))
        j, i2 = act("james_r", dict(D9.SPECS["james_wet"], canvas_pad=(0.5, 0.8, 2.8))), act("inf_r", dict(D9.infected(6), canvas_pad=(0.5, 0.8, 2.8)), ppd=200)
        def pf(a):
            return lambda x: float(np.interp(best - 0.6 + x * a.sc, ya, np.maximum(za, 0.0))) / a.sc
        span = 15.6
        cj = gait9.roof_run(j.spec, pf(j), 0.0, span / j.sc, stride=1.25, speed=5.4)
        ci = gait9.roof_run(i2.spec, pf(i2), 0.0, span / i2.sc, stride=1.40, speed=6.4)
        st = V((RX, best - 0.6, 0.0))
        tj = S9.Take(j, cj, st, dR); ti = S9.Take(i2, ci, st, dR)
        lag = 0.9
        j.pitch_override = 0.0; i2.pitch_override = 0.0
        def frame(t, measure=False):
            r = tj.root_world(t)
            rr = V((r.x, r.y, 0.0))
            loc = rr + dR * 4.4 + sideR * 5.6 + V((0, 0, 2.2))
            camera(w, loc, rr + V((0, 0, 2.5)) - dR * 0.9, 24, focus=r + V((0, 0, 1.4)))
            fill(r + V((0, 0, 1.0)))
            tj.frame(t, w.cam, measure=measure, p=lambda s_: dict(cj.pose(t, s=s_, view="side"), expr="terrified"))
            t2 = max(0.0, t - lag)
            ti.frame(t2, w.cam, measure=measure, p=lambda s_: dict(ci.pose(t2, s=s_, view="side"), expr="lunging", head=(0, -12, 0.08, 0)))
        fr = int(math.ceil((ci.dur + lag) * FPS))
        return dict(frames=min(fr, 96), frame=frame, takes=[tj, ti], actors=[j, i2], cyc=cj, label="roof_run", falls=dict(james=cj.falls, infected=ci.falls))
    T["roof_run"] = mk_roof
    w.hide_all = hide_all
    return T


def run_measure(w, names):
    T = make_takes(w)
    res = {}
    S9 = w.S9
    for nm in names:
        tk = T[nm]()
        w.hide_all()
        for tt in tk["takes"]:
            tt.rows = []
        n = tk["frames"]
        for i in range(n):
            tk["frame"](i / FPS, measure=True)
        per = []
        for tt in tk["takes"]:
            dr = S9.drift(tt.rows)
            cyc = tt.cyc
            sc = tt.a.sc
            r0, r1 = tt.root_fn(0.0), tt.root_fn((n - 1) / FPS)
            dist = abs(r1[0] - r0[0]) * sc * 0.6
            per.append(dict(actor=tt.a.name, spec=tt.a.spec.get("name"), stances=dr["stances"], max_drift_cm=dr["max_drift_cm"], per_stance_cm=dr["per_stance_cm"],
                            root_travel_m=round(dist, 2), speed_m_s=round(dist / ((n - 1) / FPS), 2),
                            unreachable=len(getattr(cyc, "unreachable", []))))
        res[nm] = dict(frames=n, actors=per, max_drift_cm=max(p["max_drift_cm"] for p in per), falls=tk.get("falls"))
        print(nm, json.dumps([(p["actor"], p["stances"], p["max_drift_cm"], p["speed_m_s"], p["unreachable"]) for p in per]), flush=True)
        for a in tk["actors"]:
            a.hide(True)
    p = os.path.join(OUT, "drift.json")
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(res)
    json.dump(old, open(p, "w"), indent=1)
    lines = ["| take | actor (spec) | frames | stances measured | max sole drift cm | root travel m | speed m/s | unreachable stances |", "|---|---|---|---|---|---|---|---|"]
    for nm in TAKES:
        if nm not in old: continue
        for a in old[nm]["actors"]:
            lines.append("| %s | %s (%s) | %d | %d | %.3f | %.2f | %.2f | %d |" % (nm, a["actor"], a["spec"], old[nm]["frames"], a["stances"], a["max_drift_cm"],
                                                                                   a["root_travel_m"], a["speed_m_s"], a["unreachable"]))
    open(os.path.join(OUT, "drift_table.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


def run_render(w, names, part, step=2, only_frames=None):
    T = make_takes(w)
    i_part, n_part = part
    logf = open(os.path.join(OUT, "cycles_log_%d.jsonl" % i_part), "a")
    for k, nm in enumerate(TAKES):
        if nm not in names or k % n_part != i_part:
            continue
        tk = T[nm]()
        w.hide_all()
        od = os.path.join(OUT, "cycles", nm); os.makedirs(od, exist_ok=True)
        fast = nm.startswith("run_") or nm == "sprint_infected"          # checker: fast gaits on twos, slow actions and holds on fours
        fr = list(range(0, tk["frames"], step if fast else step * 2)) if only_frames is None else only_frames
        linked = False
        for i in fr:
            o = os.path.join(od, "f_%03d" % i)
            if os.path.exists(o + ".png"):
                try:                                         # resume: skip only frames that decode completely
                    from PIL import Image as _I
                    _I.open(o + ".png").load()
                    continue
                except Exception:
                    os.remove(o + ".png")
            t0 = time.time(); c0 = time.process_time()
            for a in tk["actors"]:
                a.hide(False)
            tk["frame"](i / FPS)
            if not linked:
                r = tk["takes"][0].root_world(i / FPS)
                Ls = w.FS.dominant_light(r + w.V((0, 0, 1.5)), exclude=("cyc_fill",))
                if Ls is not None:
                    w.S9.S8.shadow_link(tk["actors"], Ls)
                linked = True
                tk["frame"](i / FPS)
            w.sc.frame_set(100 + i)
            w.B.render6.render(o, frame=100 + i, post_opts={"exposure": 1.6, "sharp_idx": [2]})
            logf.write(json.dumps(dict(take=nm, f=i, wall=round(time.time() - t0, 2), cpu=round(time.process_time() - c0, 2))) + "\n"); logf.flush()
            print("FRAME", nm, i, round(time.time() - t0, 1), flush=True)
        for a in tk["actors"]:
            a.hide(True)


def mp4():
    from PIL import Image, ImageDraw, ImageFont
    dj = json.load(open(os.path.join(OUT, "drift.json"))) if os.path.exists(os.path.join(OUT, "drift.json")) else {}
    fo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    od = os.path.join(OUT, "cycles", "_seq"); os.makedirs(od, exist_ok=True)
    for f in os.listdir(od): os.remove(os.path.join(od, f))
    n = 0; thumbs = []
    for nm in TAKES:
        d = os.path.join(OUT, "cycles", nm)
        if not os.path.isdir(d): continue
        fr = sorted(f for f in os.listdir(d) if f.endswith(".png") and "depth" not in f and "raw" not in f)
        if not fr: continue
        info = dj.get(nm, {})
        for rep in range(2 if int(fr[-1][2:5]) < 32 else 1):
            for k, f in enumerate(fr):
                im = Image.open(os.path.join(d, f)).convert("RGB")
                dr = ImageDraw.Draw(im)
                dr.rectangle([0, 0, 360, 40], fill=(0, 0, 0))
                dr.text((6, 3), nm, fill=(255, 255, 255), font=fo)
                if info:
                    dr.text((6, 23), "sole drift max %.2f cm, %d stances" % (info["max_drift_cm"], sum(a["stances"] for a in info["actors"])), fill=(190, 220, 255), font=fs)
                gap = (int(fr[k + 1][2:5]) - int(f[2:5])) if k + 1 < len(fr) else (int(f[2:5]) - int(fr[k - 1][2:5]) if k else 2)
                for h in range(max(1, gap)):
                    im.save(os.path.join(od, "s_%05d.png" % n)); n += 1
                if rep == 0 and k == len(fr) // 2: thumbs.append(im.copy())
    out = os.path.join(HERE, "cycles.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(od, "s_%05d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "17", out], check=True)
    if thumbs:
        cols = 7; rows = (len(thumbs) + cols - 1) // cols
        sh = Image.new("RGB", (cols * 360, rows * 640))
        for i, t in enumerate(thumbs): sh.paste(t, ((i % cols) * 360, (i // cols) * 640))
        sh.save(os.path.join(OUT, "cycles_sheet.png"))
    print("cycles.mp4", n, "frames", round(n / FPS, 1), "s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--takes", default=""); ap.add_argument("--part", default="0/1"); ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--frames", default="")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    names = a.takes.split(",") if a.takes else TAKES
    if a.mode == "mp4":
        mp4()
    else:
        w = build()
        if a.mode == "probe":
            probe(w)
        elif a.mode == "measure":
            run_measure(w, names)
        else:
            i, n = a.part.split("/")
            run_render(w, names, (int(i), int(n)), a.step, [int(x) for x in a.frames.split(",")] if a.frames else None)
        import rast9
        rast9.close()
