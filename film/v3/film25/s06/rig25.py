#!/usr/bin/env python3
"""rig25.py -- film 25 render rig for LOOK A (client pick): 2D cast25 cards + INFLATED NORMAL-MAP shading pass + near backdrop with a
crisp cast shadow + mild DOF on close / medium shots.  Generalises film25/gate/motion/{depth.py, depth_post.py, post25.py} to
any number of actors and any number of shots per take.

A shot module (shot.py) supplies:
    PRESET, HAZE, G_RANGE (first, last g of the take WITHOUT handles), ROWS
    build(rig)        -> creates actors (rig.actor), backdrop (rig.backdrop), per-take dressing
    state(g)          -> dict(cam=(loc, look, lens), dof=(fstop, focus_dist) or None, sun=(left_deg, elev) or None,
                              actors={name: dict(pos=Vector, pose={...}, flip=False, vis=True)}, hook=callable or None)
CLI (in shot.py):  python3 shot.py probe|draft|final <gspec>
Per frame: beauty (24 adaptive samples, thr 0.02, OIDN, 75 %) + shading pass (white cards with inflated normal maps, ~12 samples)
+ composite (set sharpen / clarity, gentle background grade, sprite colour x shading, face centre exact, rim <= 15 % darker, ink AO).
"""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                                       # noqa: E402
from PIL import Image, ImageFilter                       # noqa: E402
import c25 as C                                          # noqa: E402
import post25 as P                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
F, bpy, cast25 = C.F, C.bpy, C.cast25

SCALE, SAMPLES, THRESH, SH_SAMPLES, SH_SCALE = 0.6, 12, 0.05, 5, 0.35
P.EXP_MAX = 4.5
SUN_E, SKY_K = 8.0, 0.5
NORMAL_R, NORMAL_STRENGTH = 0.9, 1.6


# ----------------------------------------------------------------------------- normal map (depth.py, unchanged maths)
def normal_map(spr_path, out_path, R=NORMAL_R, ppd=384):
    import cv2
    a = np.asarray(Image.open(spr_path).convert("RGBA")).astype(np.float32) / 255
    al = a[..., 3]
    inside = (al > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(inside, cv2.DIST_L2, 5)
    r = R * ppd
    t = np.clip(d / r, 0, 1)
    h = np.sqrt(1 - (1 - t) ** 2) * r
    h = cv2.GaussianBlur(h, (0, 0), 18.0 * ppd / 384.0)
    gy, gx = np.gradient(h)
    n = np.stack([-gx, gy, np.ones_like(h)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    n[al < 0.5] = (0, 0, 1)
    Image.fromarray(((n * 0.5 + 0.5) * 255 + 0.5).astype(np.uint8)).save(out_path)
    return out_path


def pick_ppd(member, want=384):
    cv = cast25.CANVAS25[member] if member in cast25.CANVAS25 else None
    for ppd in (want, 352, 320, 288, 256):
        w, h = (cv[2] - cv[0]) * ppd, (cv[3] - cv[1]) * ppd
        if abs(w - round(w)) < 1e-6 and abs(h - round(h)) < 1e-6:
            return ppd
    return 256


class Rig(C.Take):
    def __init__(self, preset, haze=0.0006, work=None):
        F.OVR.update(haze=haze)
        C.Take.__init__(self, preset)
        self.work = work or os.path.join(HERE, "work")
        os.makedirs(self.work, exist_ok=True)
        self.spr_dir = os.path.join(self.work, "sprites"); os.makedirs(self.spr_dir, exist_ok=True)
        self.nrm_dir = os.path.join(self.work, "normals"); os.makedirs(self.nrm_dir, exist_ok=True)
        self.ppd = {}; self.member = {}; self.st = {}; self.shade_mats = {}
        self.sun_cfg = (30.0, 22.0)
        F.S["sun"].data.angle = math.radians(0.5)
        F.S["sun"].data.energy = SUN_E
        self.close = False                                     # close / medium: strong key, weaker sky fill, crisp shadows, mild DOF
        self.hook = None
        self.cur_g = None

    # ------------------------------------------------------------------ scene dressing
    def set_look(self, close=True):
        self.close = close
        if close:
            for n in bpy.context.scene.world.node_tree.nodes:
                if n.type == "BACKGROUND":
                    n.inputs["Strength"].default_value = SKY_K

    def actor(self, name, member, contact=None):
        ppd = pick_ppd(member)
        a = self.make_actor(name, member, self.spr_dir, contact=contact or dict(width=1.6, depth=0.8, opacity=0.7))
        self.ppd[name] = ppd; self.member[name] = member
        return a

    def backdrop(self, center, face_deg, w=14.0, h=10.0, col=(0.30, 0.34, 0.26), rough=0.85, name="bd"):
        """a plain calm plate (grey-olive / steel-grey) standing at `center` (x, y, z base), its face turned toward `face_deg`
        (world azimuth of the outward normal), w x h D; thin box, catches cast shadows."""
        me = bpy.data.meshes.new(name); a = math.radians(face_deg)
        n = Vector((math.cos(a), math.sin(a), 0)); t = Vector((-math.sin(a), math.cos(a), 0)); c = Vector(center)
        vs = [c + t * (-w / 2), c + t * (w / 2), c + t * (w / 2) + Vector((0, 0, h)), c + t * (-w / 2) + Vector((0, 0, h))]
        me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)]); me.update()
        m = bpy.data.materials.new(name + "_m"); m.use_nodes = True
        bs = m.node_tree.nodes["Principled BSDF"]; bs.inputs["Base Color"].default_value = (col[0], col[1], col[2], 1); bs.inputs["Roughness"].default_value = rough
        nz = m.node_tree.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 6.0; nz.inputs["Detail"].default_value = 8.0
        bm = m.node_tree.nodes.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.08
        m.node_tree.links.new(nz.outputs["Fac"], bm.inputs["Height"]); m.node_tree.links.new(bm.outputs["Normal"], bs.inputs["Normal"])
        me.materials.append(m)
        ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
        return ob

    def open_shell(self, lamp_k=0.4, floor_col=(0.20, 0.19, 0.17)):
        """factory interior under the LOOK-A sun: the shed shell stops blocking the sun (visible_shadow off), practical lights dimmed,
        a darker warm-grey floor sheet so the contact shadows read"""
        for ob in bpy.data.objects:
            if ob.name in ("shed_roof", "shed_wood", "shed_walls", "shed_trim"):
                ob.visible_shadow = False
            if ob.type == "LIGHT" and ob.data.type != "SUN":
                ob.data.energy *= lamp_k
        me = bpy.data.meshes.new("fl2"); me.from_pydata([(-26, 0, 0.02), (26, 0, 0.02), (26, 53, 0.02), (-26, 53, 0.02)], [], [(0, 1, 2, 3)]); me.update()
        m = bpy.data.materials.new("fl2m"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*floor_col, 1); b.inputs["Roughness"].default_value = 0.9
        me.materials.append(m); ob = bpy.data.objects.new("fl2", me); bpy.context.scene.collection.objects.link(ob)

    # ------------------------------------------------------------------ per-frame keying
    def stage(self, g, S):
        """key camera + actors for frame g from the shot's state dict S"""
        loc, look, lens = S["cam"]
        self.key_cam(g, loc, look, lens)
        for nm, s in S["actors"].items():
            a = self.actors[nm]
            C.camrig.key(a.root, "location", g, Vector(s["pos"]), "CONSTANT", "AUTO")
            C.camrig.key(a.root, "scale", g, Vector((s.get("scale", 1.0),) * 3), "CONSTANT", "AUTO")
            a.flips[g] = bool(s.get("flip", False))
        self.scene.frame_set(g)
        for nm, s in S["actors"].items():
            if s.get("vis", True):
                self.actors[nm].pose(g, s["pose"], camera=self.cam, hands=s.get("hands"))
        self.st[g] = S

    def sprites(self, gs):
        for nm, a in self.actors.items():
            fs = [g for g in gs if g in a.poses and self.st[g]["actors"][nm].get("vis", True)]
            if fs:
                self.sprites_for([(a, self.ppd[nm])], fs)

    def on_frame(self, f):
        S = self.st[f]
        sun = S.get("sun") or self.sun_cfg
        loc, look, _ = S["cam"]
        fw = (Vector(look) - Vector(loc)); fw.z = 0
        if fw.length > 1e-6:
            fw.normalize(); az = math.atan2(-fw.y, -fw.x) - math.radians(sun[0])
            F.set_sun(math.degrees(az), sun[1])
        d = self.cam.data.dof
        dof = S.get("dof")
        if dof:
            d.use_dof = True; d.aperture_fstop = dof[0]; d.focus_distance = dof[1]
        else:
            d.use_dof = False
        for nm, s in S["actors"].items():
            a = self.actors[nm]; vis = s.get("vis", True)
            a.card.hide_render = not vis; a.proxy.hide_render = not vis
            if a.contact is not None:
                a.contact.hide_render = not vis
        if S.get("hook"):
            S["hook"](f)
        self.cur_g = f

    # ------------------------------------------------------------------ shading pass
    def _shade_mat(self, nm):
        mat = bpy.data.materials.new(nm + "_shade"); mat.use_nodes = True; nt = mat.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial"); dif = nt.nodes.new("ShaderNodeBsdfDiffuse"); dif.inputs["Color"].default_value = (0.8, 0.8, 0.8, 1)
        ti = nt.nodes.new("ShaderNodeTexImage"); ta = nt.nodes.new("ShaderNodeTexImage")
        uv = nt.nodes.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
        nmn = nt.nodes.new("ShaderNodeNormalMap"); nmn.space = "TANGENT"; nmn.uv_map = "UVMap"; nmn.inputs["Strength"].default_value = NORMAL_STRENGTH
        tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
        L = nt.links.new
        L(uv.outputs[0], ti.inputs[0]); L(uv.outputs[0], ta.inputs[0]); L(ti.outputs["Color"], nmn.inputs["Color"]); L(nmn.outputs[0], dif.inputs["Normal"])
        L(ta.outputs["Alpha"], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(dif.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs["Surface"])
        return mat, ti, ta

    def shading_pass(self, g, out_dir, scale, samples):
        S = self.st[g]; keep = {}; loaded = []
        self.scene.frame_set(g); self.on_frame(g)
        for nm, s in S["actors"].items():
            if not s.get("vis", True):
                continue
            a = self.actors[nm]; spr = a.sprite_path(g)
            nmp = normal_map(spr, os.path.join(self.nrm_dir, "%s_%04d.png" % (nm, g)), ppd=self.ppd[nm])
            if nm not in self.shade_mats:
                self.shade_mats[nm] = self._shade_mat(nm)
            mat, ti, ta = self.shade_mats[nm]
            im_n = bpy.data.images.load(nmp, check_existing=False); im_n.colorspace_settings.name = "Non-Color"
            im_a = bpy.data.images.load(spr, check_existing=False)
            ti.image, ta.image = im_n, im_a; loaded += [im_n, im_a]
            keep[nm] = list(a.card.data.materials); a.card.data.materials.clear(); a.card.data.materials.append(mat)
            a.proxy.hide_render = True
        self.cam.data.dof.use_dof = False
        F.setup_render(self.scene, "final"); self.scene.cycles.samples = samples
        st = C.render.render_frames([g], out_dir, scale=scale, threads=2, scene=self.scene, camera=self.cam, on_frame=None, verbose=False, check=False, sync=False)[0]
        for nm, ms in keep.items():
            a = self.actors[nm]; a.card.data.materials.clear(); [a.card.data.materials.append(m) for m in ms]
            a.proxy.hide_render = False
        for im in loaded:
            bpy.data.images.remove(im)
        return st

    # ------------------------------------------------------------------ geometry for the composite
    def card_geo(self, g):
        S = self.st[g]; out = {}
        self.scene.frame_set(g)
        C.actors.sync_all(self.scene, self.cam)
        hr = C.head_report(self, g)
        for nm, s in S["actors"].items():
            if not s.get("vis", True):
                continue
            a = self.actors[nm]; cv = a.canvas; fx, fy = a.feet[g]
            pts = [(cv[0], cv[1]), (cv[2], cv[1]), (cv[2], cv[3]), (cv[0], cv[3])]
            quad = [list(C.actors.local_to_screen(a, self.cam, (fx + x, fy + y), g, (fx, fy))) for x, y in pts]
            xs = [q[0] for q in quad]; ys = [q[1] for q in quad]
            if max(xs) < 0 or min(xs) > 720 or max(ys) < 0 or min(ys) > 1280:
                continue
            h = hr.get(nm)
            out[nm] = dict(quad=quad, sprite=a.sprite_path(g), head=[h["x"], h["y"]], hw=h["w"], z=float(np.linalg.norm(np.array(self.cam.matrix_world.translation) - np.array(a.root.matrix_world.translation))))
        return out


# ----------------------------------------------------------------------------- composite (post25.frame + depth_post.shade_fn, N actors)
def shade_layer(SH, sc, al, hx, hy, hr):
    solid = al > 0.98
    lum = SH @ P.W709
    ref = np.percentile(lum[solid], 97) if solid.sum() > 50 else 1.0
    pick = solid & (lum > ref * 0.95)
    refc = np.median(SH[pick], axis=0) if pick.sum() > 20 else np.ones(3, np.float32)
    s = np.clip(SH / np.maximum(refc, 1e-4), 0, 1.05)
    s = 0.55 + 0.45 * np.clip(s, 0, 1)
    l = sc @ P.W709
    ink = ((l < 0.22) & (al > 0.9)).astype(np.uint8) * 255
    core = np.asarray(Image.fromarray((al > 0.5).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(9))) > 0
    ink = np.where(core, ink, 0).astype(np.uint8)
    ao = np.asarray(Image.fromarray(ink).filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255
    s = s * (1 - 0.35 * np.clip(ao * 1.6, 0, 1))[..., None]
    yy, xx = np.mgrid[0:1280, 0:720].astype(np.float32)
    rr = np.hypot(xx - hx, yy - hy) / max(hr, 1.0)
    h, sat, v = P.rgb2hsv(sc)
    face = (rr < 1.05) & (sat < 0.12) & (v > 0.85) & (al > 0.5)
    cap = 1 - 0.15 * np.clip((rr - 0.55) / 0.45, 0, 1)
    sl = s @ P.W709
    fs = np.where(sl < cap, cap / np.maximum(sl, 1e-4), 1.0)[..., None] * s
    fs = np.where((rr < 0.55)[..., None], 1.0, np.clip(fs, 0, 1))
    s = np.where(face[..., None], fs, s)
    return np.clip(s, 0, 1)


def warp_sprite(path, quad):
    spr = Image.open(path).convert("RGBA"); sw, sh = spr.size
    co = P.persp_coeffs([q[:2] for q in quad], [(0, 0), (sw, 0), (sw, sh), (0, sh)])
    w = np.asarray(spr.transform((720, 1280), Image.PERSPECTIVE, co, Image.BICUBIC)).astype(np.float32) / 255
    al = np.clip(w[..., 3], 0, 1)
    sc = np.where(al[..., None] > 1e-3, np.clip(w[..., :3], 0, 1), 0)
    return sc, al


def composite(g, raw_path, shade_path, geo, out_path, bg_only=False):
    raw = Image.open(raw_path).convert("RGB")
    if raw.size != (720, 1280):
        raw = raw.resize((720, 1280), Image.LANCZOS)
    SH = None
    if shade_path:
        sh_img = Image.open(shade_path).convert("RGB").resize((720, 1280), Image.LANCZOS)
        SH = P.to_lin(np.asarray(sh_img).astype(np.float32) / 255)
    sharp = raw.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2)).filter(ImageFilter.UnsharpMask(radius=5, percent=40, threshold=1))
    rawa = np.asarray(raw).astype(np.float32) / 255
    a = np.asarray(sharp).astype(np.float32) / 255
    m_tot = np.zeros((720 * 0 + 1280, 720), np.float32); sc_tot = np.zeros((1280, 720, 3), np.float32)
    for nm, gg in sorted(geo.items(), key=lambda kv: -kv[1]["z"]):                      # far first
        sc, al = warp_sprite(gg["sprite"], gg["quad"])
        solid = al > 0.98
        pred = np.zeros_like(sc)
        if solid.sum() > 50:
            for ch in range(3):
                xs = (sc[..., ch][solid] * 255).astype(int); ys = rawa[..., ch][solid]
                lut = np.zeros(256, np.float32); cnt = np.zeros(256, np.float32)
                np.add.at(lut, xs, ys); np.add.at(cnt, xs, 1)
                idx = np.where(cnt > 0)[0]; lut = np.interp(np.arange(256), idx, lut[idx] / cnt[idx])
                pred[..., ch] = lut[(sc[..., ch] * 255).astype(int)]
        blur = lambda x: np.asarray(Image.fromarray((np.clip(x, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
        err = np.abs(blur(pred) - blur(rawa)).sum(2)
        occ = ((err > 0.22) & solid).astype(np.uint8) * 255
        occ = Image.fromarray(occ).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.8))
        occ = np.asarray(occ).astype(np.float32) / 255
        m = np.clip(al * (1 - occ), 0, 1)
        s = shade_layer(SH, sc, al, gg["head"][0], gg["head"][1], gg["hw"] / 2.0)
        scs = np.clip(P.to_srgb(P.to_lin(sc) * s), 0, 1)
        sc_tot = sc_tot * (1 - m[..., None]) + scs * m[..., None]
        m_tot = np.maximum(m_tot * (1 - m), 0) + m                                      # union (alpha-over)
        m_tot = np.clip(m_tot, 0, 1)
    m, sc = m_tot, sc_tot
    lin = P.to_lin(a)
    comp = lambda bg: bg * (1 - m[..., None]) + sc * m[..., None]

    def tone(e, gains, gam=P.GAMMA):
        y = lin * gains * e
        L = np.maximum(y @ P.W709, 1e-6)[..., None]; k = 0.70
        Ly = np.where(L > k, k + (0.97 - k) * np.tanh((L - k) / (0.97 - k)), L); y = y * (Ly / L)
        mx = y.max(-1, keepdims=True); y = y * np.minimum(1.0, 0.985 / np.maximum(mx, 1e-6))
        return np.power(np.clip(P.to_srgb(y), 1e-5, 1), gam)
    gains = np.ones(3, np.float32); e = 1.0
    ms = m[::4, ::4, None]; scs4 = sc[::4, ::4]
    for it in range(int(os.environ.get("ITERS", 4)) if not hasattr(P, "ITERS_") else 7):
        lo, hi = 0.8, P.EXP_MAX
        for _ in range(11):
            e = (lo + hi) / 2
            if ((P.vibrance(tone(e, gains)[::4, ::4], P.VIB) * (1 - ms) + scs4 * ms) @ P.W709).mean() > 0.505: hi = e
            else: lo = e
        bgv = P.vibrance(tone(e, gains)[::4, ::4], P.VIB)
        am, bm = P.lab_ab((bgv * (1 - ms) + scs4 * ms)[None])
        gains[2] *= np.exp(0.025 * (bm - P.WB_T[1])); gains[1] *= np.exp(0.02 * (am - P.WB_T[0]))
        gains /= float(gains @ P.W709); gains = np.clip(gains, 0.7, 1.45)
    b = P.vibrance(tone(e, gains), P.VIB)
    yy = np.linspace(0, 1, 1280, dtype=np.float32)[:, None, None]
    b = b * (1 - 0.18 * np.clip((yy - 0.86) / 0.14, 0, 1) ** 1.5)
    out = comp(b)
    Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out_path)
    return dict(exposure=round(float(e), 3), gains=[round(float(x), 3) for x in gains])


# ----------------------------------------------------------------------------- runner
def run(shot, cmd, gs, out_root=None, scale=None, samples=None, sh_samples=None):
    """shot = the shot module (PRESET, HAZE, build(rig), state(g))"""
    TAKE = os.path.dirname(os.path.abspath(shot.__file__))
    out_root = out_root or os.path.join(TAKE, "frames")
    if hasattr(shot, "pre"):
        shot.pre()
    rig = Rig(shot.PRESET, getattr(shot, "HAZE", 0.0006), work=os.path.join(TAKE, "work"))
    shot.build(rig)
    gs = list(gs)
    for g in gs:
        rig.stage(g, shot.state(g))
    rig.sprites(gs)
    if cmd == "probe":
        for g in gs:
            hr = C.head_report(rig, g); fr = C.feet_report(rig, g)
            flag = [k for k, v in fr.items() if 850 < v[1] < 1290 and k in hr]
            print(json.dumps(dict(g=g, heads={k: (round(v["x"]), round(v["y"]), round(v["w"])) for k, v in hr.items()}, feet={k: (round(v[0]), round(v[1])) for k, v in fr.items()}, FEET_IN_BAND=flag)), flush=True)
        return rig
    if cmd == "autograde":                               # pick vibrance / WB target so the take passes the hard colour gates, then regrade all frames in place
        import importlib.util, itertools
        spec = importlib.util.spec_from_file_location("lm", os.path.join(C.PROJ, "film25", "tools", "light_metrics.py"))
        src = open(spec.origin).read().split("for p in sys.argv[1:]:")[0]
        ns = {}; exec(compile(src, "lm", "exec"), ns)
        samp = [gs[0], gs[len(gs) // 2], gs[-1]]
        geos = {g: rig.card_geo(g) for g in samp}
        best = None; P.ITERS_ = 7
        tmp = os.path.join(TAKE, "work", "ag"); os.makedirs(tmp, exist_ok=True)
        for vib, wbb, wba in itertools.product((1.0, 1.3, 1.6, 1.9), (0.0, 3.0), (1.0,)):
            P.VIB = vib; P.WB_T = (wba, wbb); ds = []
            for g in samp:
                shp = os.path.join(out_root, "shade", "f_%04d.png" % g)
                composite(g, os.path.join(out_root, "raw", "f_%04d.png" % g), shp if (geos[g] and os.path.exists(shp)) else None, geos[g], os.path.join(tmp, "s.png"))
                ds.append(ns["m"](Image.open(os.path.join(tmp, "s.png"))))
            d = {k: float(np.mean([x[k] for x in ds])) for k in ds[0]}
            cost = abs(d["sat"] - 0.45) * 6 + max(0, abs(d["a_mean"]) - 4) + max(0, abs(d["b_mean"]) - 4) + 8 * max(0, 0.47 - d["luma"]) * (d["luma"] < 0.47)
            if best is None or cost < best[0]: best = (cost, vib, wbb, wba, d)
        print("AUTOGRADE", best[1:4], {k: round(v, 3) for k, v in best[4].items() if k in ("sat", "a_mean", "b_mean", "luma")}, flush=True)
        os.environ["VIB"], os.environ["WBB"], os.environ["WBA"] = str(best[1]), str(best[2]), str(best[3])
        cmd = "recomp"
    if cmd == "recomp":                                  # re-run only the composite / grade on stored raw + shading renders (env VIB = vibrance)
        P.VIB = float(os.environ.get("VIB", P.VIB)); P.WB_T = (float(os.environ.get("WBA", 2.0)), float(os.environ.get("WBB", 4.5))); P.ITERS_ = 7
        outd = os.environ.get("RECOMP_OUT", out_root)
        os.makedirs(outd, exist_ok=True)
        for g in gs:
            geo = rig.card_geo(g)
            shp = os.path.join(out_root, "shade", "f_%04d.png" % g)
            composite(g, os.path.join(out_root, "raw", "f_%04d.png" % g), shp if (geo and os.path.exists(shp)) else None, geo, os.path.join(outd, "g_%04d.png" % g))
        return rig
    draft = cmd == "draft"
    scale = scale or (0.4 if draft else SCALE); samples = samples or (12 if draft else SAMPLES); sh_samples = sh_samples or (6 if draft else SH_SAMPLES)
    thr = 0.05 if draft else THRESH
    d_out = os.path.join(TAKE, "work", "draft") if draft else out_root
    os.makedirs(d_out, exist_ok=True)
    for g in gs:
        js = os.path.join(d_out, "g_%04d.json" % g)
        if not draft and os.path.exists(js) and os.path.exists(js[:-5] + ".png"):
            continue
        t0 = time.time()
        raw_dir = os.path.join(d_out, "raw"); sh_dir = os.path.join(d_out, "shade")
        F.setup_render(rig.scene, "final"); rig.scene.cycles.samples = samples; rig.scene.cycles.adaptive_threshold = thr
        rig.scene.frame_set(g)
        st = C.render.render_frames([g], raw_dir, scale=scale, threads=2, scene=rig.scene, camera=rig.cam, on_frame=rig.on_frame, verbose=False, check=False)[0]
        t1 = time.time()
        geo = rig.card_geo(g)
        sh = rig.shading_pass(g, sh_dir, min(scale, SH_SCALE) if not draft else scale, sh_samples) if geo else dict(path=None)
        t2 = time.time()
        pr = composite(g, st["path"], sh["path"], geo, os.path.join(d_out, "g_%04d.png" % g))
        wall = time.time() - t0
        rep = dict(g=g, wall=round(wall, 1), beauty=round(t1 - t0, 1), shade=round(t2 - t1, 1), post=round(time.time() - t2, 1), scale=scale, samples=samples,
                   heads=C.head_report(rig, g), **pr)
        json.dump(rep, open(js + ".tmp", "w")); os.replace(js + ".tmp", js)
        print("g %d  %.1f s wall (beauty %.1f shade %.1f post %.1f)" % (g, wall, t1 - t0, t2 - t1, time.time() - t2), flush=True)
    return rig


# ----------------------------------------------------------------------------- small shared helpers for the shot modules
def spline(keys, u):
    """Catmull-Rom through camera keys [(loc, look, lens), ...] at u in 0..1 (u already eased by the caller)"""
    n = len(keys) - 1
    x = max(0.0, min(1.0, u)) * n; i = min(int(x), n - 1); t = x - i
    def comp(k):
        P = [keys[max(0, min(n, j))][k] for j in (i - 1, i, i + 1, i + 2)]
        P = [Vector(p) if k < 2 else p for p in P]
        return 0.5 * ((P[1] * 2) + (P[2] - P[0]) * t + (P[0] * 2 - P[1] * 5 + P[2] * 4 - P[3]) * t * t + (P[1] * 3 - P[0] - P[2] * 3 + P[3]) * t ** 3)
    return comp(0), comp(1), float(comp(2))


def lerp(a, b, t):
    return a + (b - a) * t


def blink(g, at):
    for b in at:
        if g - b in (0, 2): return 1
        if g - b == 1: return 2
    return 0


def story(name):
    return json.loads(json.dumps(cast25.STORY25[name][1]))


def dist(loc, p):
    return (Vector(loc) - Vector(p)).length
