#!/usr/bin/env python3
"""otake.py -- the office take runner shared by takes s10, s11 and s09 (one Blender scene per take, film.py's structure).

A take is a module (shot.py) that defines:
    TAKE, SHOTS, G0, G1 (film frames [G0, G1)), H_IN, H_OUT, TRANSITION_IN (dict), HI_MAP (bool), VERSION (int)
    cam(g) -> (loc, look_at, up)          true 3D camera of film frame g (up=None -> world z)
    props(g, f)                           sets the track and props of frame g, keyed at Blender frame f (= g + 1)
    ACTORS = [dict(name, cast, place=g -> (xyz, flip), pose=g -> (pose, hands or None), ppd=int | g -> int,
                   hidden=g -> bool (optional), yaw_fixed=g -> deg | None (optional), canvas=(..) (optional))]
    CUES = [(clock_s, dur_s, kind, label)]
Commands (python3 shot.py <cmd> [frames a:b[:s]]):
    probe    staging numbers per frame (no render)
    stills   360x640 6-sample stills of the given frames into work/stills
    draft    360x640 6-sample draft of the take (resumable) into work/draft
    render   final 720x1280 12 samples, 2 threads, resumable into work/raw (+ plate/matte of the fast frames)
    post     work/raw -> frames/g_%04d.png (streak of the fast frames as the hook), meta.json, cues.json
    contact  contact.jpg;   qa   numbers for QA.md (work/qa.json)
"""
import json, math, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
V3 = os.path.join(PROJ, "v3")
for p in (os.path.join(V3, "acting"), os.path.join(V3, "stage"), os.path.join(V3, "set3d"), os.path.join(V3, "set3d_ext", "props"),
          os.path.join(PROJ, "v2", "shots"), os.path.join(V3, "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import numpy as np                                      # noqa: E402

FPS = 30
STREAK_MIN = 60.0


def gf(t):
    """film frame of an in-shot event at narration clock t."""
    return int(round((t + 0.1) * FPS))


def gb(t):
    """film frame of a shot boundary at narration clock t."""
    return int(round(t * FPS))


def smooth(a, b, x):
    if b == a:
        return 1.0 if x >= b else 0.0
    u = min(1.0, max(0.0, (x - a) / float(b - a)))
    return u * u * (3 - 2 * u)


def smoother(u):
    u = min(1.0, max(0.0, u))
    return u * u * u * (u * (u * 6 - 15) + 10)


def lerp(a, b, u):
    if isinstance(a, (tuple, list)):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


def parse(s, lo, hi):
    if not s:
        return list(range(lo, hi))
    out = []
    for part in s.split(","):
        if ":" in part:
            q = [int(x) for x in part.split(":")]
            out += list(range(q[0], q[1] + 1, q[2] if len(q) > 2 else 1))
        else:
            out.append(int(part))
    return [g for g in out if lo <= g < hi]


# ----------------------------------------------------------------------------- camera geometry (no bpy)
def cam_basis(loc, look, up=None):
    loc = np.asarray(loc, float); look = np.asarray(look, float)
    f = look - loc; f /= np.linalg.norm(f)
    upv = np.asarray(up if up is not None else (0, 0, 1.0), float)
    r = np.cross(f, upv); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    return f, r, u


def project(c, pts, focal=None):
    loc, look, up = c[:3]
    if focal is None:
        focal = 782.22 * (c[3] if len(c) > 3 and c[3] else 22.0) / 22.0
    f, r, u = cam_basis(loc, look, up)
    d = np.asarray(pts, float) - np.asarray(loc, float)
    z = d @ f
    return np.stack([360.0 + focal * (d @ r) / z, 640.0 - focal * (d @ u) / z], 1), z


def ref_points():
    pts = []
    for x in np.linspace(-3.4, 3.4, 9):
        for z in np.linspace(0.2, 4.6, 7):
            pts.append((x, 0.0, z))
    for x in np.linspace(-1.4, 1.4, 15):                # dense on the map itself (inserts, corridor)
        for z in np.linspace(1.5, 3.5, 11):
            pts.append((x, -0.05, z))
    for x in np.linspace(-3.0, 3.0, 7):
        for y in np.linspace(-3.6, -0.4, 5):
            pts.append((x, y, 0.0))
    return np.array(pts)


_REF = None


def camera_motion(cam_fn, g, g0, g1):
    """as shots/post.camera_motion, with the camera's own up vector."""
    import post
    global _REF
    if _REF is None:
        _REF = ref_points()
    a, b = max(g0, g - 1), min(g1, g + 1)
    if a == b:
        return np.array([[1.0, 0, 0], [0, 1.0, 0]]), 0.0
    P = _REF
    pa, za = project(cam_fn(a), P); pb, zb = project(cam_fn(b), P); pg, zg = project(cam_fn(g), P)
    ok = (za > 0.3) & (zb > 0.3) & (zg > 0.3) & (np.abs(pg[:, 0] - 360) < 900) & (np.abs(pg[:, 1] - 640) < 1500)
    if ok.sum() < 6:
        ok = (za > 0.3) & (zb > 0.3)
    M = post.similarity(pa[ok], pb[ok])
    n = float(b - a)
    a_c = complex(M[0, 0], M[1, 0]); t_c = complex(M[0, 2], M[1, 2])
    a1 = a_c ** (1.0 / n)
    t1 = t_c * (a1 - 1) / (a_c - 1) if abs(a_c - 1) > 1e-9 else t_c / n
    M1 = np.array([[a1.real, -a1.imag, t1.real], [a1.imag, a1.real, t1.imag]])
    corners = np.array([[0, 0], [720, 0], [0, 1280], [720, 1280]], float)
    moved = corners @ M1[:, :2].T + M1[:, 2]
    return M1, float(np.linalg.norm(moved - corners, axis=1).max())


def runs(flags):
    out, s = [], None
    for i, f in enumerate(flags):
        if f and s is None:
            s = i
        if (not f) and s is not None:
            out.append((s, i - 1)); s = None
    if s is not None:
        out.append((s, len(flags) - 1))
    return out


def motion_table(spec):
    r0, r1 = spec.G0 - spec.H_IN, spec.G1 + spec.H_OUT
    rows = []
    for g in range(r0, r1):
        M1, sp = camera_motion(spec.cam, g, r0, r1 - 1)
        rows.append(dict(g=g, speed=round(sp, 2), zoom_pct_s=round((float(np.hypot(M1[0, 0], M1[1, 0])) - 1) * 3000, 2)))
    return rows


# ----------------------------------------------------------------------------- the Blender take
class Take(object):
    def __init__(self, spec, verbose=True):
        import bpy
        from mathutils import Matrix, Vector
        import acting                                   # noqa: F401  registers cast + drawings
        import office3d as S, office_props as X
        import actors, camrig, render, sprites
        self.bpy, self.S, self.X, self.actors_mod, self.camrig, self.R, self.sprites = bpy, S, X, actors, camrig, render, sprites
        self.Vector, self.Matrix = Vector, Matrix
        self.spec = spec
        self.r0, self.r1 = spec.G0 - spec.H_IN, spec.G1 + spec.H_OUT          # rendered film frames [r0, r1)
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = sc = bpy.context.scene
        self.A = S.build("INTERIOR_DAY")
        self.PA = X.build(self.A, hi_map=getattr(spec, "HI_MAP", False))
        sc.render.use_persistent_data = False
        sc.cycles.transparent_max_bounces = 12
        sc.frame_start, sc.frame_end = 1, 2000
        if hasattr(spec, "setup"):
            spec.setup(self)
        self.cam = camrig.make_camera(sc, name="cam_" + spec.TAKE)
        self.cam.data.clip_start = 0.02
        prev = None
        for g in range(self.r0, self.r1):
            f = g + 1
            c = spec.cam(g)
            loc, look, up = c[:3]
            fw, r, u = cam_basis(loc, look, up)
            M = Matrix(((r[0], u[0], -fw[0]), (r[1], u[1], -fw[1]), (r[2], u[2], -fw[2])))
            e = M.to_euler("XYZ", prev) if prev is not None else M.to_euler("XYZ")
            prev = e
            self.cam.location = Vector(loc); self.cam.rotation_euler = e
            self.cam.keyframe_insert("location", frame=f); self.cam.keyframe_insert("rotation_euler", frame=f)
            self.cam.data.lens = c[3] if len(c) > 3 and c[3] else 22.0
            self.cam.data.keyframe_insert("lens", frame=f)
            spec.props(g, f)
        self._constant(self.cam); self._constant(self.cam.data)
        self.actors = []
        self.sprite_dir = os.path.join(spec.DIR, "work", "sprites")
        for d in spec.ACTORS:
            a = actors.Actor(d["name"], d["cast"])
            canvas = d.get("canvas") or sprites.DEFAULT_CANVAS[d["cast"]]
            a.build(canvas, self.sprite_dir, contact=d.get("contact", True), shadow=d.get("shadow", "proxy"))
            a.head_flip = True
            S.no_bounce(a.card)
            a._spec = d
            for g in range(self.r0, self.r1):
                pl = d["place"](g)
                a.place(g + 1, tuple(pl[0]), scale=(pl[2] if len(pl) > 2 else 1.0), flip=pl[1])
            self.actors.append(a)
        self.info = {}
        self.anch = {}
        if verbose:
            print("otake: %s built in %.1f s (render g %d..%d)" % (spec.TAKE, time.time() - t0, self.r0, self.r1 - 1), flush=True)

    @staticmethod
    def _constant(ob):
        ad = ob.animation_data
        if not ad or not ad.action:
            return
        try:
            curves = ad.action.fcurves
        except AttributeError:
            curves = []
            for layer in ad.action.layers:
                for strip in layer.strips:
                    for cb in strip.channelbags:
                        curves += list(cb.fcurves)
        for fc in curves:
            for k in fc.keyframe_points:
                k.interpolation = "CONSTANT"

    # ------------------------------------------------------------------ per-frame python state
    def apply(self, g):
        for a in self.actors:
            d = a._spec
            hid = bool(d["hidden"](g)) if "hidden" in d else False
            if a.card.hide_render != hid:
                a.set_hidden(hid)
            a.yaw_fixed = d["yaw_fixed"](g) if "yaw_fixed" in d else None
        if hasattr(self.spec, "apply"):
            self.spec.apply(self, g)

    def on_frame(self, f):
        self.apply(f - 1)

    # ------------------------------------------------------------------ poses and sprites
    def pose(self, frames, verbose=False):
        A, R, cam = self.actors_mod, self.R, self.cam
        frames = [g for g in frames if self.r0 <= g < self.r1]
        for g in frames:
            f = g + 1
            self.scene.frame_set(f)
            self.apply(g)
            inf = {}
            for a in self.actors:
                if a.card.hide_render:
                    continue
                pose, hands = a._spec["pose"](g)
                pose = {k: v for k, v in pose.items() if not k.startswith("_")}
                st_hands = None
                if hands:
                    st_hands = {}
                    for side, h in hands.items():
                        h = dict(h)
                        if isinstance(h.get("tip"), (tuple, list)) and len(h["tip"]) == 3:
                            h["tip"] = tuple(h["tip"])
                        st_hands[side] = h
                p, info = a.pose(f, pose, hands=st_hands, camera=cam)
                reg = {}
                if hands:
                    for side, h in hands.items():
                        e = info.get(side)
                        if e and isinstance(h.get("tip"), (tuple, list)) and len(h["tip"]) == 3:
                            s = A.local_to_screen(a, cam, e["reached"], f)[:2]
                            w = R.world_to_screen(cam, self.Vector(h["tip"]), f)[:2]
                            reg[side] = dict(px=round(math.hypot(s[0] - w[0], s[1] - w[1]), 3), err_D=round(e["error"], 5),
                                             clearance=round(e.get("clearance", 0.0), 4), screen=[round(s[0], 1), round(s[1], 1)])
                inf[a.name] = reg
            self.info[g] = inf
        for a in self.actors:
            ppd = a._spec.get("ppd", 256)
            groups = {}
            for g in frames:
                if (g + 1) in a.poses:
                    groups.setdefault(ppd(g) if callable(ppd) else ppd, []).append(g)
            for p, gl in groups.items():
                for g, r in zip(gl, a.render_sprites(p, frames=[x + 1 for x in gl], verbose=verbose)):
                    self.anch.setdefault(g, {})[a.name] = r["anchors"]
                    if r.get("clipped"):
                        print("otake: WARNING sprite of %s clipped on g %d" % (a.name, g), flush=True)

    def report(self, g):
        A, cam = self.actors_mod, self.cam
        f = g + 1
        self.scene.frame_set(f)
        self.apply(g)
        loc, look, up = self.spec.cam(g)[:3]
        v = np.asarray(look) - np.asarray(loc)
        out = dict(g=g, cam=[round(c, 3) for c in loc], cam_height=round(loc[2], 3),
                   pitch=round(math.degrees(math.atan2(v[2], math.hypot(v[0], v[1]))), 1), heads={}, reg=self.info.get(g, {}))
        for a in self.actors:
            an = self.anch.get(g, {}).get(a.name)
            if not an or a.card.hide_render:
                continue
            feet = a.feet.get(f)
            hx, hy = an["head"]
            c = A.local_to_screen(a, cam, (hx, hy), f, feet)
            l = A.local_to_screen(a, cam, (hx - 0.5, hy), f, feet)
            r = A.local_to_screen(a, cam, (hx + 0.5, hy), f, feet)
            t = A.local_to_screen(a, cam, (hx, hy - 0.5), f, feet)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1),
                                        top=round(t[1], 1), bottom=round(2 * c[1] - t[1], 1), depth=round(c[2], 3))
        return out

    # ------------------------------------------------------------------ render
    def render_one(self, g, out_dir, scale, samples, threads):
        self.scene.cycles.samples = samples
        return self.R.render_frames([g + 1], out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                    on_frame=self.on_frame, verbose=False)[0]

    def render_layers(self, g, plate, matte, threads):
        sc, R = self.scene, self.R
        f = g + 1
        cards = [a.card for a in self.actors]
        vis = [(c, c.visible_camera) for c in cards]
        for c in cards:
            c.visible_camera = False
        R.render_frames([f], plate, threads=threads, scene=sc, camera=self.cam, on_frame=self.on_frame, verbose=False, check=False)
        for c, v in vis:
            c.visible_camera = v
        decals = [a.contact for a in self.actors if getattr(a, "contact", None) is not None]
        set_obs = [ob for ob in sc.objects if ob not in cards and ob.type in ("MESH", "CURVE") and not ob.name.endswith("_shadow")]
        keep = (sc.render.film_transparent, sc.render.image_settings.color_mode, sc.render.use_compositing, sc.cycles.samples)
        sc.render.film_transparent = True; sc.render.image_settings.color_mode = "RGBA"; sc.render.use_compositing = False; sc.cycles.samples = 4
        hold = [(ob, ob.is_holdout) for ob in set_obs]
        for ob, _ in hold:
            ob.is_holdout = True
        hid = [(d, d.hide_render) for d in decals]
        for d, _ in hid:
            d.hide_render = True
        R.render_frames([f], matte, threads=threads, scene=sc, camera=self.cam, on_frame=self.on_frame, verbose=False, check=False)
        for ob, v in hold:
            ob.is_holdout = v
        for d, v in hid:
            d.hide_render = v
        sc.render.film_transparent, sc.render.image_settings.color_mode, sc.render.use_compositing, sc.cycles.samples = keep


# ----------------------------------------------------------------------------- commands
def _done(spec, out, g, scale, samples):
    png = os.path.join(out, "f_%04d.png" % (g + 1)); js = os.path.join(out, "meta", "g_%04d.json" % g)
    if not (os.path.exists(png) and os.path.exists(js)):
        return False
    try:
        m = json.load(open(js))
        return m.get("scale") == scale and m.get("samples") == samples and m.get("version") == spec.VERSION
    except Exception:
        return False


def cmd_render(spec, frames, out, scale, samples, threads, layers):
    os.makedirs(os.path.join(out, "meta"), exist_ok=True)
    r0, r1 = spec.G0 - spec.H_IN, spec.G1 + spec.H_OUT
    todo = [g for g in frames if not _done(spec, out, g, scale, samples)]
    print("otake render %s: %d to do of %d (scale %.2f, %d samples)" % (spec.TAKE, len(todo), len(frames), scale, samples), flush=True)
    if not todo:
        return
    fast = set()
    if layers:
        for g in todo:
            M1, sp = camera_motion(spec.cam, g, r0, r1 - 1)
            if sp >= STREAK_MIN:
                fast.add(g)
    T = Take(spec)
    chunk = 12
    for i in range(0, len(todo), chunk):
        part = todo[i:i + chunk]
        t0 = time.time()
        T.pose(part)
        print("posed g %d..%d in %.1f s" % (part[0], part[-1], time.time() - t0), flush=True)
        for g in part:
            for p in (os.path.join(out, "f_%04d.png" % (g + 1)), os.path.join(out, "meta", "g_%04d.json" % g)):
                if os.path.exists(p):
                    os.remove(p)
            st = T.render_one(g, out, scale, samples, threads)
            if g in fast:
                T.render_layers(g, os.path.join(spec.DIR, "plate"), os.path.join(spec.DIR, "matte"), threads)
            rep = T.report(g)
            rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, version=spec.VERSION,
                       retried=st.get("retried"), still_wrong=st.get("still_wrong"), layers=g in fast)
            tmp = os.path.join(out, "meta", "g_%04d.json.tmp" % g)
            json.dump(rep, open(tmp, "w")); os.replace(tmp, os.path.join(out, "meta", "g_%04d.json" % g))
            print("g %d  %.1f s wall  %.1f cpu%s%s" % (g, st["wall"], st["cpu"], "  +layers" if g in fast else "",
                                                       "  RETRIED" if st.get("retried") else ""), flush=True)


def cmd_probe(spec, frames):
    T = Take(spec, verbose=False)
    T.pose(frames)
    rows = [T.report(g) for g in frames]
    for r in rows:
        hs = "  ".join("%s w%.0f (%.0f,%.0f) top %.0f bot %.0f" % (k, v["w"], v["x"], v["y"], v["top"], v["bottom"]) for k, v in r["heads"].items())
        rg = "  ".join("%s.%s %.2fpx cl%.3f" % (k, s, e["px"], e["clearance"]) for k, d in r["reg"].items() for s, e in d.items())
        print("g %d  cam z %.2f pitch %5.1f | %s | %s" % (r["g"], r["cam_height"], r["pitch"], hs, rg), flush=True)
    return rows


def sheet(paths, labels, out, w=180, cols=None):
    from PIL import Image, ImageDraw
    n = len(paths)
    cols = cols or min(n, 8)
    rows_ = (n + cols - 1) // cols
    h = int(w * 16 / 9)
    strip = 22
    S = Image.new("RGB", (cols * w, rows_ * (h + strip)), (20, 20, 20))
    d = ImageDraw.Draw(S)
    for i, (p, lb) in enumerate(zip(paths, labels)):
        x, y = (i % cols) * w, (i // cols) * (h + strip)
        try:
            im = Image.open(p).convert("RGB").resize((w, h))
            S.paste(im, (x, y + strip))
        except Exception:
            pass
        d.text((x + 4, y + 5), lb, fill=(255, 255, 255))
    S.save(out, quality=88)


def cmd_post(spec):
    from PIL import Image
    import post
    raw = os.path.join(spec.DIR, "work", "raw")
    out = os.path.join(spec.DIR, "frames")
    os.makedirs(out, exist_ok=True)
    r0, r1 = spec.G0 - spec.H_IN, spec.G1 + spec.H_OUT
    log = []
    for g in range(r0, r1):
        src = os.path.join(raw, "f_%04d.png" % (g + 1))
        if not os.path.exists(src):
            raise SystemExit("missing raw frame g %d" % g)
        dst = os.path.join(out, "g_%04d.png" % g)
        M1, sp = camera_motion(spec.cam, g, r0, r1 - 1)
        row = dict(g=g, corner_speed_px=round(sp, 1), streaked=False)
        im = Image.open(src).convert("RGB")
        if sp >= STREAK_MIN:
            pl = os.path.join(spec.DIR, "plate", "f_%04d.png" % (g + 1)); mt = os.path.join(spec.DIR, "matte", "f_%04d.png" % (g + 1))
            if os.path.exists(pl) and os.path.exists(mt) and g not in getattr(spec, "WHOLE_STREAK", ()):
                post.over(post.streak(Image.open(pl).convert("RGB"), M1, sp), im, Image.open(mt)).save(dst)
                row["streaked"] = "plate"
            else:
                post.streak(im, M1, sp).save(dst)
                row["streaked"] = "whole"
        else:
            im.save(dst)
        log.append(row)
    json.dump(log, open(os.path.join(spec.DIR, "work", "post_log.json"), "w"), indent=0)
    meta = dict(take=spec.TAKE, shots=spec.SHOTS, g0=spec.G0, g1=spec.G1, handle_in=spec.H_IN, handle_out=spec.H_OUT,
                transition_in=spec.TRANSITION_IN, set="office", light="office_day", samples=12, frames_dir="frames",
                first_rendered=r0, last_rendered=r1 - 1, resolution=[720, 1280], fps=30)
    if getattr(spec, "META_NOTE", None):
        meta["note"] = spec.META_NOTE
    json.dump(meta, open(os.path.join(spec.DIR, "meta.json"), "w"), indent=1)
    ev = []
    for clock, dur, kind, label in spec.CUES:
        t = round(clock + 0.1, 3)
        ev.append(dict(time=t, duration=dur, frame=int(round(t * 30)), end_frame=int(round((t + dur) * 30)), kind=kind, label=label, clock=clock))
    json.dump(dict(fps=30, time_base="film seconds (narration clock + 0.100); frame g starts at g / 30", take=spec.TAKE, events=ev),
              open(os.path.join(spec.DIR, "cues.json"), "w"), indent=1, ensure_ascii=False)
    print("post: %d frames, streaked %s" % (len(log), [(r["g"], r["streaked"]) for r in log if r["streaked"]]))


def cmd_contact(spec, n=16):
    from PIL import Image, ImageDraw
    r0, r1 = spec.G0 - spec.H_IN, spec.G1 + spec.H_OUT
    gs = [int(round(spec.G0 + (spec.G1 - 1 - spec.G0) * i / (n - 1))) for i in range(n)]
    w, h, strip, cols = 270, 480, 26, 8
    S = Image.new("RGB", (cols * w, ((n + cols - 1) // cols) * (h + strip)), (16, 16, 16))
    d = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + strip)
        S.paste(Image.open(os.path.join(spec.DIR, "frames", "g_%04d.png" % g)).convert("RGB").resize((w, h)), (x, y + strip))
        d.text((x + 6, y + 7), "g%d  %.2f s" % (g, g / 30.0), fill=(255, 255, 255))
    S.save(os.path.join(spec.DIR, "contact.jpg"), quality=88)
    print("contact:", gs)


def cmd_qa(spec):
    from PIL import Image
    import subprocess
    r0, r1 = spec.G0 - spec.H_IN, spec.G1 + spec.H_OUT
    rows = motion_table(spec)
    sp = np.array([r["speed"] for r in rows])
    moves = []
    for a, b in runs(sp > 12.0):
        seg = sp[a:b + 1]; pk = a + int(np.argmax(seg))
        moves.append(dict(g=[r0 + a, r0 + b], peak_g=r0 + pk, peak_px=round(float(seg.max()), 1), film_s=[round((r0 + a) / 30.0, 2), round((r0 + b + 1) / 30.0, 2)]))
    static = [(r0 + a, r0 + b) for a, b in runs(sp < 0.25)]
    rel = np.abs(np.diff(sp)) / np.maximum(sp[:-1], 1e-6)
    lin = [(r0 + a, r0 + b + 1) for a, b in runs((rel < 0.02) & (sp[:-1] > 1.0))]
    # popcheck on the final frames
    prev, diffs = None, []
    for g in range(r0, r1):
        a = np.asarray(Image.open(os.path.join(spec.DIR, "frames", "g_%04d.png" % g)).convert("RGB").resize((180, 320)), np.float32)
        if prev is not None:
            diffs.append(float(np.abs(a - prev).mean()))
        prev = a
    pops = []
    for i, v in enumerate(diffs):
        a_ = diffs[i - 1] if i > 0 else v; b_ = diffs[i + 1] if i + 1 < len(diffs) else v
        if v > 1.8 * a_ and v > 1.8 * b_ and v > 1.0:
            pops.append((r0 + i, r0 + i + 1, round(v, 2)))
    metas = {}
    md = os.path.join(spec.DIR, "work", "raw", "meta")
    for g in range(r0, r1):
        try:
            metas[g] = json.load(open(os.path.join(md, "g_%04d.json" % g)))
        except Exception:
            pass
    heads = {}
    regmax = {}
    for g, m in metas.items():
        for k, v in m.get("heads", {}).items():
            heads.setdefault(k, []).append((g, v["w"], v["x"], v["y"], v["top"], v["bottom"]))
        for k, d in (m.get("reg") or {}).items():
            for s, e in d.items():
                regmax[k + "." + s] = max(regmax.get(k + "." + s, 0.0), e["px"])
    secs = [m["cpu"] for m in metas.values() if "cpu" in m]
    walls = [m["wall"] for m in metas.values() if "wall" in m]
    hue = subprocess.run([sys.executable, os.path.join(V3, "tools", "hue_report.py"), os.path.join(spec.DIR, "frames")],
                         capture_output=True, text=True).stdout
    out = dict(moves=moves, static_runs=static, linear_runs=lin, pops=pops, max_diff=round(max(diffs), 2), median_diff=round(float(np.median(diffs)), 2),
               heads={k: dict(n=len(v), w=[min(x[1] for x in v), max(x[1] for x in v)], y=[min(x[3] for x in v), max(x[3] for x in v)],
                              bottom_max=max(x[5] for x in v)) for k, v in heads.items()},
               reg_max_px=regmax, cpu_s=[round(min(secs), 1), round(float(np.median(secs)), 1), round(max(secs), 1)] if secs else None,
               wall_s=[round(min(walls), 1), round(float(np.median(walls)), 1), round(max(walls), 1)] if walls else None,
               retried=[g for g, m in metas.items() if m.get("retried")], still_wrong=[g for g, m in metas.items() if m.get("still_wrong")],
               hue=hue, speed=[(r["g"], r["speed"]) for r in rows])
    json.dump(out, open(os.path.join(spec.DIR, "work", "qa.json"), "w"), indent=0)
    for k in ("moves", "static_runs", "linear_runs", "pops", "max_diff", "median_diff", "heads", "reg_max_px", "cpu_s", "wall_s", "retried", "still_wrong"):
        print(k, out[k])
    print(hue)
    return out


def run(spec, argv):
    cmd = argv[0] if argv else "probe"
    r0, r1 = spec.G0 - spec.H_IN, spec.G1 + spec.H_OUT
    fr = argv[1] if len(argv) > 1 else None
    if cmd == "probe":
        cmd_probe(spec, parse(fr or "%d:%d:6" % (r0, r1 - 1), r0, r1))
    elif cmd == "stills":
        out = os.path.join(spec.DIR, "work", "stills")
        gs = parse(fr, r0, r1)
        cmd_render(spec, gs, out, 0.5, 6, 2, False)
        sheet([os.path.join(out, "f_%04d.png" % (g + 1)) for g in gs], ["g%d" % g for g in gs], os.path.join(spec.DIR, "work", "stills.jpg"))
    elif cmd == "draft":
        out = os.path.join(spec.DIR, "work", "draft")
        gs = parse(fr, r0, r1)
        cmd_render(spec, gs, out, 0.5, 6, 2, False)
        sel = gs[::max(1, len(gs) // 24)]
        sheet([os.path.join(out, "f_%04d.png" % (g + 1)) for g in sel], ["g%d" % g for g in sel], os.path.join(spec.DIR, "work", "draft_sheet.jpg"))
    elif cmd == "sheet":
        out = os.path.join(spec.DIR, "work", argv[2] if len(argv) > 2 else "draft")
        gs = parse(fr, r0, r1)
        sheet([os.path.join(out, "f_%04d.png" % (g + 1)) for g in gs], ["g%d" % g for g in gs], os.path.join(spec.DIR, "work", "sheet.jpg"))
    elif cmd == "render":
        cmd_render(spec, parse(fr, r0, r1), os.path.join(spec.DIR, "work", "raw"), 1.0, 12, 2, True)
    elif cmd == "post":
        cmd_post(spec)
    elif cmd == "contact":
        cmd_contact(spec)
    elif cmd == "qa":
        cmd_qa(spec)
    elif cmd == "motion":
        for r in motion_table(spec):
            print(r["g"], r["speed"], r["zoom_pct_s"])
    else:
        raise SystemExit("unknown command " + cmd)
