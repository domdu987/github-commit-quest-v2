#!/usr/bin/env python3
"""d25.py -- film 25 LOOK A pipeline, multi-actor, shared by every T3 take (import from the s21 folder).

Per frame (Rig.render_frame):
  1. BEAUTY: Cycles 24 adaptive samples (thr 0.02), OIDN, 75 % scale; sun disc 0.5 deg (crisp cast shadows), the key sun aimed from
     the camera's left-behind so the characters' shadows land on the near backdrop; mild DOF on close / medium shots.
  2. SHADING pass: every character card re-rendered as a WHITE diffuse surface carrying an INFLATED NORMAL MAP built from its
     sprite (normal_map); shading = lit / white ratio (reduced size, 10 samples).
  3. corners / anchors json (post_d.py composites: background grade, sprite colour x shading, face cap, ink-line occlusion).
Sun / sky numbers follow the approved still (gate/motion/depth.py).
"""
import math, os, sys, json, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                                       # noqa: E402
import c25 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
F, bpy, actors, render = C.F, C.bpy, C.actors, C.render

PPD = 384
SUN_E, SKY_K, SUN_DISC = 8.0, 0.5, 0.5
SCALE, SAMPLES, THRESH = 0.75, 20, 0.03
SH_SCALE, SH_SAMPLES = 0.4, 8


def normal_map(spr_path, out_path, R=0.9, ppd=PPD):
    """inflated tangent-space normal map from the sprite silhouette (gate/motion/depth.py): height rises as a circle profile with
    the distance to the edge, so the figure reads as one round volume; light direction gives form shading."""
    import cv2
    from PIL import Image
    a = np.asarray(Image.open(spr_path).convert("RGBA")).astype(np.float32) / 255
    al = a[..., 3]
    inside = (al > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(inside, cv2.DIST_L2, 5)
    r = R * ppd
    t = np.clip(d / r, 0, 1)
    h = np.sqrt(1 - (1 - t) ** 2) * r
    h = cv2.GaussianBlur(h, (0, 0), 18.0)
    gy, gx = np.gradient(h)
    n = np.stack([-gx, gy, np.ones_like(h)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    n[al < 0.5] = (0, 0, 1)
    Image.fromarray(((n * 0.5 + 0.5) * 255 + 0.5).astype(np.uint8)).save(out_path)
    return out_path


def shade_material(name, spr, nm, strength=1.6):
    mat = bpy.data.materials.new(name); mat.use_nodes = True; nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); dif = nt.nodes.new("ShaderNodeBsdfDiffuse"); dif.inputs["Color"].default_value = (0.8, 0.8, 0.8, 1)
    ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = bpy.data.images.load(nm, check_existing=False); ti.image.colorspace_settings.name = "Non-Color"
    ta = nt.nodes.new("ShaderNodeTexImage"); ta.image = bpy.data.images.load(spr, check_existing=False)
    uv = nt.nodes.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    nmn = nt.nodes.new("ShaderNodeNormalMap"); nmn.space = "TANGENT"; nmn.uv_map = "UVMap"; nmn.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
    L = nt.links.new
    L(uv.outputs[0], ti.inputs[0]); L(uv.outputs[0], ta.inputs[0]); L(ti.outputs["Color"], nmn.inputs["Color"]); L(nmn.outputs[0], dif.inputs["Normal"])
    L(ta.outputs["Alpha"], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(dif.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs["Surface"])
    return mat


def plate_material(name="backdrop", color=(0.36, 0.40, 0.33), seam=0.42, scale=(1.6, 1.0)):
    """calm grey-olive riveted-plate wall: diffuse, faint panel seams, a little grain.  colour is linear-ish RGB (b* stays low)."""
    mat = bpy.data.materials.new(name); mat.use_nodes = True; nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); bs = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bs.inputs["Base Color"].default_value = (*color, 1); bs.inputs["Roughness"].default_value = 0.78
    tc = nt.nodes.new("ShaderNodeTexCoord"); br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0; br.offset = 0.0; br.inputs["Mortar Size"].default_value = 0.012; br.inputs["Mortar Smooth"].default_value = 0.2
    br.inputs["Brick Width"].default_value = scale[0]; br.inputs["Row Height"].default_value = scale[1]
    br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (0.94, 0.94, 0.94, 1); br.inputs["Mortar"].default_value = (seam, seam, seam, 1)
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 9.0; nz.inputs["Detail"].default_value = 6.0
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"; mix.inputs[0].default_value = 1.0
    mp = nt.nodes.new("ShaderNodeMapping")
    bmp = nt.nodes.new("ShaderNodeBump"); bmp.inputs["Strength"].default_value = 0.12
    L = nt.links.new
    L(tc.outputs["Object"], mp.inputs[0]); L(mp.outputs[0], br.inputs["Vector"]); L(mp.outputs[0], nz.inputs["Vector"])
    # base colour = plate colour x brick (seams) x faint grain
    mc = nt.nodes.new("ShaderNodeMix"); mc.data_type = "RGBA"; mc.blend_type = "MULTIPLY"; mc.inputs[0].default_value = 1.0
    mc.inputs[6].default_value = (*color, 1)
    L(br.outputs["Color"], mc.inputs[7])
    m2 = nt.nodes.new("ShaderNodeMix"); m2.data_type = "RGBA"; m2.blend_type = "MIX"; m2.inputs[0].default_value = 0.10
    L(mc.outputs[2], m2.inputs[6]); m2.inputs[7].default_value = (0.0, 0.0, 0.0, 1)
    L(nz.outputs["Fac"], m2.inputs[0])
    m2.inputs[0].default_value = 0.0
    L(m2.outputs[2], bs.inputs["Base Color"])
    L(nz.outputs["Fac"], bmp.inputs["Height"]); L(bmp.outputs[0], bs.inputs["Normal"]); L(bs.outputs[0], out.inputs["Surface"])
    return mat


def add_wall(name, centre, face_deg, width, height, mat, thick=0.3, z0=None, yaw_extra=0.0):
    """a free-standing backdrop slab: centre (x, y) on the ground, its front face looking along face_deg (toward the camera side)."""
    me = bpy.data.meshes.new(name)
    hw, t = width / 2.0, thick
    v = [(-hw, -t, 0), (hw, -t, 0), (hw, 0, 0), (-hw, 0, 0), (-hw, -t, height), (hw, -t, height), (hw, 0, height), (-hw, 0, height)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    # local +y points to the camera side: rotate so that +y = (cos face, sin face)
    ob.rotation_euler = (0, 0, math.radians(face_deg) - math.pi / 2 + math.radians(yaw_extra))
    gz = F.gh(centre[0], centre[1]) if z0 is None else z0
    ob.location = (centre[0], centre[1], gz - 0.05)
    for p in me.polygons:
        p.use_smooth = False
    return ob


class Rig(C.Take):
    """one location build + any number of cards; every per-frame value is computed by the shot and set through key_frame()."""

    def __init__(self, preset, work, haze=0.0006, sun_left=30.0, sun_el=22.0, fstop=None, sun_e=SUN_E, sky_k=SKY_K, sun_disc=SUN_DISC, sun_col=(1.0, 0.9, 0.74), ev=0.0):
        C.F.OVR.update(haze=haze)
        C.Take.__init__(self, preset)
        self.work = work
        os.makedirs(work, exist_ok=True)
        self.spr_dir = os.environ.get("SPRITES", os.path.join(work, "sprites"))
        os.makedirs(self.spr_dir, exist_ok=True)
        self.sun_left, self.sun_el, self.fstop, self.ev = sun_left, sun_el, fstop, ev
        F.S["sun"].data.angle = math.radians(sun_disc)
        F.S["sun"].data.energy = sun_e
        F.S["sun"].data.color = sun_col
        for n in bpy.context.scene.world.node_tree.nodes:
            if n.type == "BACKGROUND":
                n.inputs["Strength"].default_value = sky_k
        self.cams = {}
        self.focus = {}
        self.order = []

    # ----------------------------------------------------------------------------- actors
    def actor(self, name, cast, contact=dict(width=1.6, depth=0.8, opacity=0.7), canvas=None):
        a = self.make_actor(name, cast, self.spr_dir, canvas=canvas, contact=contact)
        self.order.append(name)
        return a

    def key_frame(self, g, cam, lens, per_actor, focus=None):
        """cam = (loc, look); per_actor = {name: dict(feet=Vector, pose=dict, scale=1.0, flip=False, hide=False)}"""
        loc, look = Vector(cam[0]), Vector(cam[1])
        self.key_cam(g, loc, look, lens)
        self.cams[g] = (loc, look, lens)
        self.focus[g] = Vector(focus) if focus is not None else None
        for n, st in per_actor.items():
            a = self.actors[n]
            C.camrig.key(a.root, "location", g, Vector(st["feet"]), "CONSTANT", "AUTO")
            sc = st.get("scale", 1.0)
            C.camrig.key(a.root, "scale", g, Vector((sc, sc, sc)), "CONSTANT", "AUTO")
            a.flips[g] = bool(st.get("flip", False))
        self._st = getattr(self, "_st", {})
        self._st[g] = per_actor

    def pose_frames(self, gs):
        for g in gs:
            self.scene.frame_set(g)
            for n, st in self._st[g].items():
                if st.get("hide"):
                    continue
                p = dict(st["pose"])
                if st.get("flip"):
                    p["mirror"] = True
                self.actors[n].pose(g, p, camera=self.cam)
        for n, a in self.actors.items():
            fr = [g for g in gs if g in a.poses]
            for f, r in zip(fr, a.render_sprites(PPD, frames=fr)):
                self.anch[(n, f)] = r["anchors"]

    # ----------------------------------------------------------------------------- sun / camera per frame
    def aim_sun_g(self, g):
        loc, look, _ = self.cams[g]
        f = Vector(look) - Vector(loc); f.z = 0; f.normalize()
        a = math.atan2(-f.y, -f.x) - math.radians(self.sun_left)
        F.set_sun(math.degrees(a), self.sun_el)

    def on_frame(self, f):
        self.aim_sun_g(f)
        d = self.cam.data.dof
        if self.fstop and self.focus.get(f) is not None:
            d.use_dof = True; d.aperture_fstop = self.fstop
            d.focus_distance = max(0.5, (self.cams[f][0] - self.focus[f]).length)
        else:
            d.use_dof = False

    # ----------------------------------------------------------------------------- meta
    def meta(self, g):
        self.scene.frame_set(g)
        out = dict(g=g, cam=[list(self.cams[g][0]), list(self.cams[g][1]), self.cams[g][2]], actors={})
        for n, st in self._st[g].items():
            if st.get("hide"):
                continue
            a = self.actors[n]
            fx, fy = a.feet[g]
            cv = a.canvas
            pts = [(cv[0], cv[1]), (cv[2], cv[1]), (cv[2], cv[3]), (cv[0], cv[3])]
            quad = [list(actors.local_to_screen(a, self.cam, (fx + x, fy + y), g, (fx, fy))) for x, y in pts]
            hd = self.anch[(n, g)]["head"]
            hc = actors.local_to_screen(a, self.cam, tuple(hd), g, (fx, fy))
            hl = actors.local_to_screen(a, self.cam, (hd[0] - 0.5, hd[1]), g, (fx, fy)); hr = actors.local_to_screen(a, self.cam, (hd[0] + 0.5, hd[1]), g, (fx, fy))
            feet = actors.local_to_screen(a, self.cam, (fx, fy), g, (fx, fy))
            dist = (a.root.matrix_world.to_translation() - self.cams[g][0]).length
            out["actors"][n] = dict(quad=quad, head=list(hc), hw=math.hypot(hr[0] - hl[0], hr[1] - hl[1]), feet=list(feet), dist=dist, sprite=a.sprite_path(g), ppd=PPD, scale=st.get("scale", 1.0))
        return out

    # ----------------------------------------------------------------------------- render
    def render_frame(self, g, out_dir, scale=SCALE, samples=SAMPLES, thr=THRESH, shade=True, sh_scale=SH_SCALE, sh_samples=SH_SAMPLES):
        """beauty + shading raw into out_dir/beauty/f_%04d.png, out_dir/shade/f_%04d.png, meta json out_dir/meta/g_%04d.json"""
        t0 = time.time()
        F.setup_render(self.scene, "final"); self.scene.cycles.samples = samples; self.scene.cycles.adaptive_threshold = thr
        self.scene.view_settings.exposure += self.ev
        st = render.render_frames([g], os.path.join(out_dir, "beauty"), scale=scale, threads=2, scene=self.scene, camera=self.cam, on_frame=self.on_frame, verbose=False)[0]
        t1 = time.time()
        md = self.meta(g)
        if shade:
            self.shading_pass(g, os.path.join(out_dir, "shade"), sh_scale, sh_samples)
        md["wall_beauty"], md["wall_total"] = round(t1 - t0, 1), round(time.time() - t0, 1)
        os.makedirs(os.path.join(out_dir, "meta"), exist_ok=True)
        json.dump(md, open(os.path.join(out_dir, "meta", "g_%04d.json" % g), "w"), default=float)
        return md

    def shading_pass(self, g, out_dir, scale, samples, strength=1.6):
        mats, saved = [], []
        os.makedirs(os.path.join(self.work, "nm"), exist_ok=True)
        for n, st in self._st[g].items():
            if st.get("hide"):
                continue
            a = self.actors[n]
            spr = a.sprite_path(g)
            key = hashlib.sha1(open(spr, "rb").read()).hexdigest()[:16]
            nm = os.path.join(self.work, "nm", key + ".png")
            if not os.path.exists(nm):
                normal_map(spr, nm)
            m = shade_material("sh_" + n, spr, nm, strength); mats.append(m)
            saved.append((a, list(a.card.data.materials), a.card.visible_diffuse, a.proxy.hide_render if a.proxy else None))
            a.card.data.materials.clear(); a.card.data.materials.append(m); a.card.visible_diffuse = True
            if a.proxy is not None:
                a.proxy.hide_render = True
        dof = self.cam.data.dof.use_dof
        self.cam.data.dof.use_dof = False
        F.setup_render(self.scene, "final"); self.scene.cycles.samples = samples
        render.render_frames([g], out_dir, scale=scale, threads=2, scene=self.scene, camera=self.cam, on_frame=lambda f: (self.aim_sun_g(f)), verbose=False, check=False)
        for a, ms, vd, ph in saved:
            a.card.data.materials.clear(); [a.card.data.materials.append(m) for m in ms]; a.card.visible_diffuse = vd
            if a.proxy is not None:
                a.proxy.hide_render = ph
        for m in mats:
            for n in m.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image:
                    bpy.data.images.remove(n.image)
            bpy.data.materials.remove(m)
        self.cam.data.dof.use_dof = dof


def run_final(Tk, gs, out_dir, shade=True, sh_scale=SH_SCALE, sh_samples=SH_SAMPLES, scale=SCALE, samples=SAMPLES):
    """resumable: skips frames whose meta json exists"""
    for g in gs:
        js = os.path.join(out_dir, "meta", "g_%04d.json" % g)
        if os.path.exists(js):
            continue
        md = Tk.render_frame(g, out_dir, scale=scale, samples=samples, shade=shade, sh_scale=sh_scale, sh_samples=sh_samples)
        print("g %d  %.1f s beauty  %.1f s total" % (g, md["wall_beauty"], md["wall_total"]), flush=True)


# ----------------------------------------------------------------------------- shared shot helpers
def orbit(P, az, d, cz, lz, side=0.0, lx=0.0):
    """camera orbiting the world point P (feet): azimuth az deg, distance d, camera height cz, look height lz, lateral slide `side`
    (D along the camera's right axis), look offset lx.  -> (loc, look)"""
    A = math.radians(az)
    loc = Vector((P.x + math.cos(A) * d, P.y + math.sin(A) * d, P.z + cz))
    fwd = Vector((-math.cos(A), -math.sin(A), 0.0)); right = fwd.cross(Vector((0, 0, 1))).normalized()
    look = Vector((P.x, P.y, P.z + lz)) + right * (side * 0.6 + lx)
    return loc + right * side, look


def story(name):
    c, p = C.cast25.STORY25[name]
    return json.loads(json.dumps(p))


def blink(g, at):
    for b in at:
        if g - b in (0, 2): return 1
        if g - b == 1: return 2
    return 0


def squash_accent(g, g0):
    seq = {0: 0.93, 1: 0.92, 2: 0.98, 3: 1.05, 4: 1.03, 5: 1.0}
    k = g - g0
    if k not in seq:
        return None
    s = seq[k]
    return [round(2.0 - s, 3) if s < 1 else round(1.0 - (s - 1.0) * 0.6, 3), s]


_LEVEL = None


def lvl(g):
    global _LEVEL
    if _LEVEL is None:
        _LEVEL = C.audio_level()
    return _LEVEL[g] if g < len(_LEVEL) else 0.0


def talk(g, inside=True):
    return C.cast25.talk_mouth(g, lvl(g)) if inside else "flat"


def lerp_poses(a, b, u, cast="general25"):
    """in-between of two pose dicts via the puppet's lerp_pose (cast25 keys re-added from the nearer pose)"""
    import puppet
    p = puppet.lerp_pose(cast, a, b, u)
    src = a if u < 0.5 else b
    for k in ("t", "light25", "rim25", "hat_off25", "hat_up25", "pour25", "dirt25", "paint_col25", "mg_gy25"):
        if k in src and k not in p:
            p[k] = src[k]
    return p


def cli(make, G0, G1, argv=None, work=None):
    """probe | draft <gspec> [scale] | final <gspec>.   make(work) -> Rig with .setup(gs)"""
    argv = argv or sys.argv
    cmd, gs = argv[1], C.parse(argv[2])
    work = work or os.path.join(os.path.dirname(os.path.abspath(argv[0])), "work")
    Tk = make(work)
    Tk.setup(gs)
    if cmd == "probe":
        for g in gs:
            md = Tk.meta(g); print(g, {k: [round(v, 1) for v in a["head"][:2]] + [round(a["hw"], 1)] + [round(a["feet"][1], 0)] for k, a in md["actors"].items()}, flush=True)
    elif cmd == "draft":
        sc = float(argv[3]) if len(argv) > 3 else 0.4
        for g in gs:
            md = Tk.render_frame(g, work + "_draft", scale=sc, samples=12, thr=0.05, sh_scale=0.3, sh_samples=6); print(g, md["wall_total"], flush=True)
    else:
        run_final(Tk, gs, work, shade=getattr(Tk, "SHADE", True), scale=getattr(Tk, "SCALE", SCALE), samples=getattr(Tk, "SAMPLES", SAMPLES))


def flatten_hull(H, color=(0.34, 0.38, 0.31)):
    """runtime dressing: the camo hull becomes ONE calm grey-olive riveted plate (diffuse, rough: no sky sheen), rivets / tap / hatch keep their own materials"""
    new = plate_material("hull_calm", color, seam=0.38, scale=(2.6, 2.0))
    n = 0
    for ob in bpy.data.objects:
        if ob.type != "MESH":
            continue
        for s in ob.material_slots:
            if s.material is not None and s.material == H.mats.get("hull"):
                s.material = new; n += 1
    return n


def olive_steel(name="tail_olive", color=(0.20, 0.22, 0.15)):
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    bs = mat.node_tree.nodes["Principled BSDF"]; bs.inputs["Base Color"].default_value = (*color, 1); bs.inputs["Roughness"].default_value = 0.7; bs.inputs["Metallic"].default_value = 0.0
    return mat


def dull_tail(H):
    """runtime dressing: the tail A-frame and wheels (blue-grey steel in the set) become dark olive steel, so the whole tank reads olive"""
    m = olive_steel()
    for ob in bpy.data.objects:
        if ob.type == "MESH" and ("tailframe" in ob.name or "tailwheel" in ob.name):
            ob.data.materials.clear(); ob.data.materials.append(m)
