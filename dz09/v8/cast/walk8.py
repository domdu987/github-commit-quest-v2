"""walk8.py -- Kong walking 3 s in the v6 set, camera tracking from the front 3/4; foot-drift measurement.

python3 walk8.py measure [--kind walk|run]          # no render: per-frame planted-foot world positions -> out/walk_drift.json
python3 walk8.py render [--frames 72] [--scale 0.5] [--kind walk]   -> out/walk/f_####.png, walk_kong.mp4

The cards of a walking actor stay in the plane of the motion (Actor8.walk_lock), so a planted foot drawn at
x_land - v t on the card is a fixed world point.  Drift = the largest distance between a planted foot's world
position on any frame of one stance and its position on the stance's first frame.
"""
import os, sys, json, math, time, argparse, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
FPS = 24
D_M = 0.6           # 1 BU = 0.6 m


def build(scale=0.5, q="final", kind="walk", set_=True):
    import bpy
    from mathutils import Vector
    if set_:
        sys.path.insert(0, os.path.join(PROJ, "v6", "set"))
        import beauty as B
        A = B.build()
        B.setup_render(q, threads=4)
    else:
        B, A = None, {"kong_phone_mark": (-5.2, 28.0, 0.0)}
        bpy.ops.wm.read_factory_settings(use_empty=True)
    import stage8 as S, gait8
    sc = bpy.context.scene
    sc.cycles.transparent_max_bounces = max(sc.cycles.transparent_max_bounces, 32)
    a = S.Actor8("kong_walk", "kong_wet", height=2.86)
    a.set_pass_index(2)
    G = gait8.Gait("kong_wet", kind)
    if set_:
        import lookdev8
        md = Vector(A["moon_dir"]); mh = Vector((md.x, md.y, 0)).normalized()
        K = lookdev8.find_spot(Vector(A["kong_phone_mark"]), mh, dist=4.5, spread=3.5)
        dirv = Vector((-mh.y, mh.x, 0.0))
        start = K - dirv * 2.9
        camside = mh
    else:
        start = Vector(A["kong_phone_mark"]) + Vector((0.4, -1.2, 0))
        dirv = Vector((0.0, 1.0, 0.0))
        camside = Vector((1.0, 0.0, 0.0))
    return dict(B=B, A=A, S=S, a=a, G=G, start=start, dir=dirv, camside=camside, scale=scale, kind=kind)


def frame_setup(W, i):
    """pose the walker and the camera for frame i (0-based)."""
    import bpy
    from mathutils import Vector
    a, G, start, d = W["a"], W["G"], W["start"], W["dir"]
    t = i / FPS
    side = W["camside"]                               # the camera's side of the walk (the moon side: no moon behind the head)
    root = start + d * (G.root_x(t) * a.sc)
    fac = math.degrees(math.atan2(d.x, -d.y))
    a.place(tuple(root), fac)
    # camera: tracks from the front 3/4, slightly low, 3.5 m away
    cam_loc = root + d * 2.4 + side * 2.7 + Vector((0, 0, 1.45))
    look = root + Vector((0, 0, 1.30)) + d * 0.3
    B = W["B"]
    if B is not None:
        import kit
        cam = bpy.context.scene.camera
        if cam is None or cam.get("preset") != "walk":
            cam = B.X.make_camera(); cam["preset"] = "walk"
        cam.location = cam_loc
        cam.rotation_euler = kit.look_rot(tuple(cam_loc), tuple(look), 0.0)
        cam.data.lens = 30
        cam["aspect"] = "9:16"; cam["focus"] = tuple(root + Vector((0, 0, 2.4))); cam["coc_k"] = 5.0; cam["coc_max"] = 18; cam["dof_k"] = 1.0
        rs = bpy.context.scene.render
        rs.resolution_x, rs.resolution_y = int(720 * W["scale"]), int(1280 * W["scale"])
        for ob in bpy.data.objects:
            for con in ob.constraints:
                if con.type == "TRACK_TO": con.target = cam
    else:
        cam = bpy.context.scene.camera
        if cam is None:
            cd = bpy.data.cameras.new("c"); cam = bpy.data.objects.new("c", cd); bpy.context.scene.collection.objects.link(cam)
            bpy.context.scene.camera = cam
        cam.location = cam_loc
    # a soft cool fill riding with the camera (as the v6 look shots' look_fill lights), so the dark wet legs read
    fl = bpy.data.objects.get("walk_fill")
    if fl is None:
        ld = bpy.data.lights.new("walk_fill", "POINT"); fl = bpy.data.objects.new("walk_fill", ld); bpy.context.scene.collection.objects.link(fl)
        ld.energy = 45.0; ld.color = (0.72, 0.82, 1.0); ld.shadow_soft_size = 0.8
        fl.visible_glossy = False; fl.visible_camera = False
    fl.location = root + d * 1.6 + side * 1.8 + Vector((0, 0, 0.9))
    bpy.context.view_layer.update()
    rel = a._cam_rel(cam)
    s = -1 if rel > 0 else 1
    a.walk_lock = (rel / abs(rel)) * 90.0 if abs(rel) > 1e-3 else 90.0
    p = G.pose(t, s=s, view="q", base=dict(expr="tired" if W["kind"] == "walk" else "alarmed"))
    planted = p.pop("_planted")
    fig = a.pose(p, camera=cam, view="q")
    # review fix: the walker never got a shadow light, so its proxy cast from every lamp (incl. the low walk_fill)
    # and the shadow showed up detached in front of the feet.  One light, chosen once at the middle of the path.
    if W["B"] is not None and not W.get("shadow_set"):
        import look8
        mid = W["start"] + d * (G.root_x(1.5) * a.sc) + Vector((0, 0, 1.5))
        Ls = look8.dominant_light(mid, exclude=("walk_fill",))
        if Ls is not None:
            W["S"].shadow_link([a], Ls)
            W["shadow_light"] = Ls.name
        W["shadow_set"] = True
    elif W.get("shadow_set"):
        a._place_proxy()
    near = "L" if s > 0 else "R"
    far = "R" if s > 0 else "L"
    zn = [L["z"] for L in fig["layers"] if L["name"] == "leg_" + near][0]
    zf = [L["z"] for L in fig["layers"] if L["name"] == "leg_" + far][0]
    fn = a.world_of(fig["anchors"]["foot_" + near], zn)
    ff = a.world_of(fig["anchors"]["foot_" + far], zf)
    sn = a.sole_world("leg_" + near)
    sf = a.sole_world("leg_" + far)
    return dict(t=t, planted=planted, near=tuple(sn), far=tuple(sf), near_anchor=tuple(fn), far_anchor=tuple(ff), s=s, rel=rel)


def drift(rows):
    """per stance episode: max distance from the first planted frame, in cm (sole measured on the drawn sprite)."""
    out = {}
    for key, k in (("near", 0), ("far", 1)):
        eps, cur = [], None
        for r in rows:
            if r["planted"][k]:
                if cur is None:
                    cur = [r[key]]
                else:
                    cur.append(r[key])
            elif cur is not None:
                eps.append(cur); cur = None
        if cur:
            eps.append(cur)
        ds = []
        for e in eps:
            p0 = e[0]
            ds.append(max(math.dist(p0, p) for p in e) * D_M * 100.0)
        out[key] = dict(episodes=len(eps), frames=[len(e) for e in eps], drift_cm=[round(x, 4) for x in ds])
    allv = out["near"]["drift_cm"] + out["far"]["drift_cm"]
    out["max_drift_cm"] = round(max(allv) if allv else 0.0, 4)
    return out


def measure(frames=72, kind="walk", set_=False):
    W = build(kind=kind, set_=set_)
    rows = [frame_setup(W, i) for i in range(frames)]
    res = drift(rows)
    res["kind"] = kind
    res["speed_m_s"] = round(W["G"].v * W["a"].sc * D_M, 3)
    res["frames"] = frames
    # contrast: how far the root moved during a stance (what a sliding foot would drift)
    G = W["G"]
    res["root_travel_per_stance_cm"] = round(G.v * G.P["beta"] * G.P["T"] * W["a"].sc * D_M * 100, 1)
    json.dump(dict(res, rows=rows), open(os.path.join(HERE, "out", "%s_drift.json" % kind), "w"), indent=1)
    print(json.dumps(res))
    return res


def render(frames=72, scale=0.5, kind="walk", q="final", only=None):
    import bpy
    W = build(scale=scale, kind=kind, q=q)
    if only:
        for i in only:
            frame_setup(W, i)
            W["B"].render6.render(os.path.join(HERE, "tmp", "walktest_%d" % i), frame=i + 1, post_opts={"exposure": 1.6, "sharp_idx": [2]})
        return
    od = os.path.join(HERE, "out", kind)
    os.makedirs(od, exist_ok=True)
    rows, tt = [], []
    for i in range(frames):
        t0 = time.time()
        r = frame_setup(W, i)
        rows.append(r)
        o = os.path.join(od, "f_%04d" % i)
        rr = W["B"].render6.render(o, frame=i + 1, post_opts={"exposure": 1.6, "sharp_idx": [2]})
        tt.append(dict(wall=round(time.time() - t0, 2), cpu_render=rr.get("cpu_render"), cpu_post=rr.get("cpu_post")))
        print("FRAME", i, tt[-1], flush=True)
    res = drift(rows)
    res["render"] = dict(frames=frames, res=[int(720 * scale), int(1280 * scale)], mean_wall_s=round(sum(x["wall"] for x in tt) / len(tt), 2),
                         mean_cpu_render_s=round(sum((x["cpu_render"] or 0) for x in tt) / len(tt), 2))
    res["shadow_light"] = W.get("shadow_light")
    json.dump(dict(res, rows=rows, times=tt), open(os.path.join(HERE, "out", "%s_render.json" % kind), "w"), indent=1)
    mp4 = os.path.join(HERE, "walk_kong.mp4" if kind == "walk" else "run_kong.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(od, "f_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", mp4], check=True)
    print(json.dumps(res))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("--frames", type=int, default=72); ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--only", default=""); ap.add_argument("--kind", default="walk"); ap.add_argument("--q", default="final"); ap.add_argument("--set", action="store_true")
    a = ap.parse_args()
    if a.mode == "measure":
        measure(a.frames, a.kind, a.set)
    else:
        render(a.frames, a.scale, a.kind, a.q, [int(x) for x in a.only.split(",")] if a.only else None)
