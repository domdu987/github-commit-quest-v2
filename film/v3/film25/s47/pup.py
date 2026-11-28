#!/usr/bin/env python3
"""pup.py -- Look A puppet pipeline for T2 close shots (generalised from film25/gate/motion/depth.py + depth_post.py).
Per frame: (1) beauty render (cast card + shadow proxy, near backdrop plate behind, sun disc 0.5 deg aimed so the shadow lands on the plate, optional mild DOF);
(2) SHADING pass: every actor card re-rendered as a WHITE diffuse surface with an INFLATED NORMAL MAP from its sprite (cached per sprite hash), 8 samples + OIDN, no DOF;
(3) composite = post25 background grade + sprite colour x shading applied to LUMINANCE only (one grey factor, no per-channel tint), ink-line occlusion, face centre
exactly #fef7f6 (shading capped to 1 at the centre, at most 15 % darker at the rim), faces sampled into the take's QA.
Use: PupTake(preset, cam_of, actors=[(name, member, ...)]) ; Tk.render_frame(g, out_dir) ; post_frame(g, out_dir, ...)"""
import os, sys, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
GATE_MOTION = os.path.join(C_ := os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "film25", "gate", "motion")
sys.path.insert(0, GATE_MOTION)
import numpy as np
from PIL import Image, ImageFilter
import t2lib as T
import post25 as P
from mathutils import Vector
C, F = T.C, T.F
bpy = C.bpy
PPD = 384
NM_CACHE = {}


def normal_map(spr_path, out_path, R=0.9, ppd=PPD):
    import cv2
    a = np.asarray(Image.open(spr_path).convert("RGBA")).astype(np.float32) / 255
    al = a[..., 3]
    inside = (al > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(inside, cv2.DIST_L2, 5)
    r = R * ppd; t = np.clip(d / r, 0, 1)
    h = np.sqrt(1 - (1 - t) ** 2) * r
    h = cv2.GaussianBlur(h, (0, 0), 18.0)
    gy, gx = np.gradient(h)
    n = np.stack([-gx, gy, np.ones_like(h)], -1); n /= np.linalg.norm(n, axis=-1, keepdims=True); n[al < 0.5] = (0, 0, 1)
    Image.fromarray(((n * 0.5 + 0.5) * 255 + 0.5).astype(np.uint8)).save(out_path)
    return out_path


def backdrop(pos, face_deg, dist=2.0, size=(9.0, 7.0), col=(0.30, 0.37, 0.35), gz=0.0):
    """a plain grey-olive plate `dist` D behind the figure (opposite to the camera side), facing the camera: the near backdrop that catches the cast shadow"""
    a = math.radians(face_deg)
    c = Vector((pos[0] - math.cos(a) * dist, pos[1] - math.sin(a) * dist, gz + size[1] / 2 - 0.5))
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=c)
    ob = bpy.context.active_object; ob.name = "near_backdrop"
    ob.scale = (size[0], size[1], 1.0)
    ob.rotation_euler = (math.pi / 2, 0, a - math.pi / 2)             # plane normal -> toward the camera side (face_deg)
    m = bpy.data.materials.new("backdrop"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = 0.9
    ob.data.materials.append(m)
    return ob


class PupTake(T.Take):
    def __init__(self, preset, cam_of, hooks=None, haze=0.0006):
        T.Take.__init__(self, preset, cam_of, hooks, haze=haze)
        self.acts = []                                    # [(actor, pose_fn, feet_fn)]
        F.S["sun"].data.angle = math.radians(0.5)
        F.S["sun"].data.energy = 8.0
        for n in bpy.context.scene.world.node_tree.nodes:
            if n.type == "BACKGROUND":
                n.inputs["Strength"].default_value = 0.5

    def add(self, name, member, pose_fn, feet_fn, sprite_dir, contact=None, flip=False):
        a = self.make_actor(name, member, sprite_dir, contact=contact or dict(width=1.6, depth=0.8, opacity=0.7))
        self.acts.append((a, pose_fn, feet_fn, flip))
        return a

    def pose(self, gs):
        for g in gs:
            loc, look, lens = self.cam_of(g)[:3]
            self.key_cam(g, loc, look, lens)
            for a, pf, ff, fl in self.acts:
                C.camrig.key(a.root, "location", g, Vector(ff(g)), "CONSTANT", "AUTO")
                C.camrig.key(a.root, "scale", g, Vector((1, 1, 1)), "CONSTANT", "AUTO")
                a.flips[g] = fl
        for g in gs:
            self.scene.frame_set(g)
            for a, pf, ff, fl in self.acts:
                a.pose(g, pf(g), camera=self.cam)
        self.sprites_for([(a, PPD) for a, *_ in self.acts], list(gs))

    def on_frame(self, f):
        T.Take.on_frame(self, f)
        loc, look, _ = self.cam_of(f)[:3]
        ff = Vector(look) - Vector(loc); ff.z = 0; ff.normalize()
        az = math.atan2(-ff.y, -ff.x) - math.radians(30.0)               # sun behind-left of the camera: the shadow lands right of / below the figure on the plate
        F.set_sun(math.degrees(az), 22.0)

    def shade_mats(self, a, g):
        spr = a.sprite_path(g)
        key = hashlib.md5(open(spr, "rb").read()).hexdigest()
        wd = os.path.join(os.path.dirname(spr), "nm"); os.makedirs(wd, exist_ok=True)
        nm = os.path.join(wd, key + ".png")
        if not os.path.exists(nm):
            normal_map(spr, nm)
        mat = bpy.data.materials.new("shade_" + a.name); mat.use_nodes = True; nt = mat.node_tree
        for n in list(nt.nodes): nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial"); dif = nt.nodes.new("ShaderNodeBsdfDiffuse"); dif.inputs["Color"].default_value = (0.8, 0.8, 0.8, 1)
        ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = bpy.data.images.load(nm, check_existing=True); ti.image.colorspace_settings.name = "Non-Color"
        ta = nt.nodes.new("ShaderNodeTexImage"); ta.image = bpy.data.images.load(spr, check_existing=True); ta.image.reload()
        uv = nt.nodes.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
        nmn = nt.nodes.new("ShaderNodeNormalMap"); nmn.space = "TANGENT"; nmn.uv_map = "UVMap"; nmn.inputs["Strength"].default_value = 1.6
        tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
        L = nt.links.new
        L(uv.outputs[0], ti.inputs[0]); L(uv.outputs[0], ta.inputs[0]); L(ti.outputs["Color"], nmn.inputs["Color"]); L(nmn.outputs[0], dif.inputs["Normal"])
        L(ta.outputs["Alpha"], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(dif.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs["Surface"])
        return mat

    def shading_pass(self, g, out_dir, scale, samples=8):
        keeps = []
        for a, *_ in self.acts:
            keeps.append((a, list(a.card.data.materials)))
            a.card.data.materials.clear(); a.card.data.materials.append(self.shade_mats(a, g)); a.card.visible_diffuse = True; a.proxy.hide_render = True
        dof = self.cam.data.dof.use_dof
        F.setup_render(self.scene, "final"); self.scene.cycles.samples = samples
        saved = self.on_frame
        st = C.render.render_frames([g], out_dir, scale=scale, threads=2, scene=self.scene, camera=self.cam, on_frame=lambda f: self._frame_nodof(f), verbose=False, check=False)[0]
        for a, m in keeps:
            a.card.data.materials.clear(); [a.card.data.materials.append(x) for x in m]; a.proxy.hide_render = False
        return st["path"]

    def _frame_nodof(self, f):
        self.hooks(f, self); loc, look, _ = self.cam_of(f)[:3]
        ff = Vector(look) - Vector(loc); ff.z = 0; ff.normalize()
        F.set_sun(math.degrees(math.atan2(-ff.y, -ff.x) - math.radians(30.0)), 22.0)
        self.cam.data.dof.use_dof = False

    def corners(self, g):
        out = {}
        for a, *_ in self.acts:
            cv = a.canvas; fx, fy = a.feet[g]
            pts = [(cv[0], cv[1]), (cv[2], cv[1]), (cv[2], cv[3]), (cv[0], cv[3])]
            hx, hy = self.anch[(a.name, g)]["head"]
            out[a.name] = dict(quad=[list(C.actors.local_to_screen(a, self.cam, (fx + x, fy + y), g, (fx, fy))) for x, y in pts],
                               head=list(C.actors.local_to_screen(a, self.cam, (hx, hy), g, (fx, fy))))
        return out

    def render_frame(self, g, out, scale=T.SCALE, samples=T.SAMPLES, sh_samples=8):
        """beauty -> out/raw/f_g.png ; shading -> out/shade/f_g.png ; json with corners / heads"""
        self.scene.frame_set(g)
        st = self.render([g], out, scale=scale, samples=samples, threshold=T.THRESH, keep_raw=True, post=False)[0]
        sh = self.shading_pass(g, os.path.join(out, "shade"), scale, sh_samples)
        hd = C.head_report(self, g)
        rep = dict(g=g, wall=round(st["wall"], 1), corners=self.corners(g), heads=hd, samples=samples, scale=scale, threshold=T.THRESH, sh_samples=sh_samples)
        return rep


def luminance_shading(SH, sc, al, hx, hy, hr):
    """shading as ONE grey factor per pixel (luminance only: no per-channel tint), 0.55..1; ink-line occlusion; face disc capped"""
    solid = al > 0.98
    lum = SH @ P.W709
    ref = np.percentile(lum[solid], 97) if solid.any() else 1.0
    s = np.clip(lum / max(ref, 1e-4), 0, 1.05)
    s = 0.55 + 0.45 * np.clip(s, 0, 1)
    l = sc @ P.W709
    ink = ((l < 0.22) & (al > 0.9)).astype(np.uint8) * 255
    core = np.asarray(Image.fromarray((al > 0.5).astype(np.uint8) * 255).filter(ImageFilter.MinFilter(9))) > 0
    ink = np.where(core, ink, 0).astype(np.uint8)
    ao = np.asarray(Image.fromarray(ink).filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255
    s = s * (1 - 0.35 * np.clip(ao * 1.6, 0, 1))
    yy, xx = np.mgrid[0:1280, 0:720].astype(np.float32)
    rr = np.hypot(xx - hx, yy - hy) / hr
    h, sat, v = P.rgb2hsv(sc)
    face = (rr < 1.05) & (sat < 0.12) & (v > 0.85) & (al > 0.5)
    cap = 1 - 0.15 * np.clip((rr - 0.55) / 0.45, 0, 1)
    fs = np.where(s < cap, cap, s)
    fs = np.where(rr < 0.55, 1.0, fs)
    s = np.where(face, fs, s)
    return np.clip(s, 0, 1)[..., None] * np.ones(3, np.float32)


def post_frame(g, out, rep, sprite_dirs, names):
    """composite one frame: post25 background grade + the first actor via post25.frame (shade_fn = luminance-only shading); more actors are laid on after.
    returns the stats dict; image -> out/post/g_g.png"""
    os.makedirs(os.path.join(out, "post"), exist_ok=True)
    sh_img = Image.open(os.path.join(out, "shade", "f_%04d.png" % g)).convert("RGB").resize((720, 1280), Image.LANCZOS)
    SH = P.to_lin(np.asarray(sh_img).astype(np.float32) / 255)
    n0 = names[0]
    hx, hy = rep["corners"][n0]["head"][:2]; hr = rep["heads"][n0]["w"] / 2.0
    fn = lambda sc, al: luminance_shading(SH, sc, al, hx, hy, hr)
    st = P.frame(g, os.path.join(out, "raw"), os.path.join(out, "post"), {str(g): dict(quad=rep["corners"][n0]["quad"])}, sprite_dirs[0], shade_fn=fn)
    return st
