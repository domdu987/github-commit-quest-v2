#!/usr/bin/env python3
"""depth.py -- ONE still of row 20 (general25 point_stick, g 575) with real shading on the card, a near backdrop for the cast shadow and mild DOF.
    python3 depth.py draft|final
1. the general stands ND D in front of the tank's side plate (plain riveted area), the camera frontal on that plate;
   sun disc 0.5 deg (crisp shadows), aimed from the camera's left so his shadow lands on the plate right behind him.
2. beauty render with slight DOF (focus on the card, the far field soft).
3. SHADING pass: the card re-rendered as a WHITE diffuse surface carrying an INFLATED NORMAL MAP built from the sprite
   (distance to the silhouette and to the interior ink lines -> round height per part -> normals), shadow proxy hidden;
   shading = lit / white ratio.
4. composite (depth_post.py): background gentle grade (post25), sprite colour x shading, face capped (centre exact, rim
   at most 15 % darker), ink-line occlusion at the limb overlaps and under the cap brim."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                                       # noqa: E402
import c25 as C                                          # noqa: E402
import motion as M                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
F, bpy = C.F, C.bpy
G = 575
SUN_LEFT, SUN_EL, SUN_E, SKY_K = 30.0, 22.0, 8.0, 0.5                            # sun behind-left of the camera: his shadow lands right of him on the plate
ND = 2.0                                                 # D in front of the side plate (about 1 m)
LOCAL = (-4.6, -3.15 - ND)                               # tank-local point (x along the hull, y = right side outward)
WORK = os.path.join(HERE, "work", "depth")
os.makedirs(WORK, exist_ok=True)
CAM_D, CAM_Z, LOOK_Z, LENS, FSTOP = 4.8, 2.7, 2.35, 45.0, 1.6


def normal_map(spr_path, out_path, R=0.9, ppd=M.PPD):
    """inflated tangent-space normal map from the sprite: height rises as a circle profile with the distance to the
    nearest edge (outside or an interior ink line), so every drawn part (arm, torso, cap, legs) bulges on its own."""
    import cv2
    from PIL import Image
    a = np.asarray(Image.open(spr_path).convert("RGBA")).astype(np.float32) / 255
    al = a[..., 3]; lum = a[..., :3] @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    inside = (al > 0.5).astype(np.uint8)                              # silhouette only: one round volume (cylinder-like body, round limbs at the edge)
    d = cv2.distanceTransform(inside, cv2.DIST_L2, 5)
    r = R * ppd
    t = np.clip(d / r, 0, 1)
    h = np.sqrt(1 - (1 - t) ** 2) * r
    h = cv2.GaussianBlur(h, (0, 0), 18.0)
    gy, gx = np.gradient(h)
    n = np.stack([-gx, gy, np.ones_like(h)], -1)                    # tangent space: u right, v UP (image y down -> +gy)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    n[al < 0.5] = (0, 0, 1)
    rgb = ((n * 0.5 + 0.5) * 255 + 0.5).astype(np.uint8)
    Image.fromarray(rgb).save(out_path)
    return out_path


class Take(C.Take):
    def __init__(self):
        C.F.OVR.update(haze=M.HAZE)
        C.Take.__init__(self, M.PRESET)
        self.gen = self.make_actor("gen", "general25", os.path.join(HERE, "work", "sprites_d"), contact=dict(width=1.6, depth=0.8, opacity=0.7))
        H = F.S["tank"]
        bpy.context.view_layer.update()
        w = H.root.matrix_world @ Vector((LOCAL[0], LOCAL[1], 0.0))
        self.feet = Vector((w.x, w.y, F.gh(w.x, w.y)))
        self.face = F.S["mark"]["face_deg"]                       # outward normal of the right side plate (deg)
        a = math.radians(self.face)
        self.loc = Vector((w.x + math.cos(a) * CAM_D, w.y + math.sin(a) * CAM_D, self.feet.z + CAM_Z))
        self.look = Vector((w.x, w.y, self.feet.z + LOOK_Z)) + Vector((math.cos(a + math.pi / 2), math.sin(a + math.pi / 2), 0)) * 0.30
        F.S["sun"].data.angle = math.radians(0.5)
        F.S["sun"].data.energy = SUN_E                             # stronger key, weaker sky fill: darker, crisper cast shadows
        for n in bpy.context.scene.world.node_tree.nodes:
            if n.type == "BACKGROUND":
                n.inputs["Strength"].default_value = SKY_K
        import tank25 as TK
        TK.set_stencil(H, 0)                                       # plain riveted plate behind him (no stencil picture)

    def setup(self):
        self.key_cam(G, self.loc, self.look, LENS)
        C.camrig.key(self.gen.root, "location", G, self.feet, "CONSTANT", "AUTO")
        C.camrig.key(self.gen.root, "scale", G, Vector((1, 1, 1)), "CONSTANT", "AUTO")
        self.gen.flips[G] = False
        self.scene.frame_set(G)
        p = M.pose_of(G)
        self.gen.pose(G, p, camera=self.cam)
        self.sprites_for([(self.gen, M.PPD)], [G])
        self.aim_sun(self.loc, self.look)
        d = self.cam.data.dof
        d.use_dof = True; d.aperture_fstop = FSTOP; d.focus_distance = (self.loc - self.feet - Vector((0, 0, 2.3))).length

    def aim_sun(self, loc, look):
        """sun nearly behind the camera, 25 deg to its left, 30 deg up: the shadow lands just right of and below him on the plate"""
        f = (Vector(look) - Vector(loc)); f.z = 0; f.normalize(); a = math.atan2(-f.y, -f.x) - math.radians(SUN_LEFT)
        F.set_sun(math.degrees(a), SUN_EL)

    def on_frame(self, f):
        self.aim_sun(self.loc, self.look)

    def corners(self):
        cv = self.gen.canvas; fx, fy = self.gen.feet[G]
        pts = [(cv[0], cv[1]), (cv[2], cv[1]), (cv[2], cv[3]), (cv[0], cv[3])]
        return dict(quad=[list(C.actors.local_to_screen(self.gen, self.cam, (fx + x, fy + y), G, (fx, fy))) for x, y in pts],
                    head=list(C.actors.local_to_screen(self.gen, self.cam, tuple(self.anch[("gen", G)]["head"]), G, (fx, fy))),
                    anchors=self.anch[("gen", G)], feet=[fx, fy], canvas=list(cv), ppd=M.PPD)

    def shading_pass(self, out_dir, scale, samples, strength=1.6):
        """card as white diffuse + inflated normal map, proxy hidden, no DOF; returns the raw path"""
        spr = self.gen.sprite_path(G)
        nm = normal_map(spr, os.path.join(WORK, "normal.png"))
        mat = bpy.data.materials.new("gen_shade"); mat.use_nodes = True; nt = mat.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial"); dif = nt.nodes.new("ShaderNodeBsdfDiffuse"); dif.inputs["Color"].default_value = (0.8, 0.8, 0.8, 1)
        ti = nt.nodes.new("ShaderNodeTexImage"); ti.image = bpy.data.images.load(nm); ti.image.colorspace_settings.name = "Non-Color"
        ta = nt.nodes.new("ShaderNodeTexImage"); ta.image = bpy.data.images.load(spr)
        uv = nt.nodes.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
        nmn = nt.nodes.new("ShaderNodeNormalMap"); nmn.space = "TANGENT"; nmn.uv_map = "UVMap"; nmn.inputs["Strength"].default_value = strength
        tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader")
        L = nt.links.new
        L(uv.outputs[0], ti.inputs[0]); L(uv.outputs[0], ta.inputs[0]); L(ti.outputs["Color"], nmn.inputs["Color"]); L(nmn.outputs[0], dif.inputs["Normal"])
        L(ta.outputs["Alpha"], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(dif.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs["Surface"])
        card = self.gen.card
        keep = list(card.data.materials); card.data.materials.clear(); card.data.materials.append(mat)
        card.visible_diffuse = True
        self.gen.proxy.hide_render = True
        self.cam.data.dof.use_dof = False
        F.setup_render(self.scene, "final"); self.scene.cycles.samples = samples
        st = C.render.render_frames([G], os.path.join(WORK, "shade"), scale=scale, threads=2, scene=self.scene, camera=self.cam, on_frame=self.on_frame, verbose=False, check=False)[0]
        card.data.materials.clear(); [card.data.materials.append(m) for m in keep]
        self.gen.proxy.hide_render = False; self.cam.data.dof.use_dof = True
        return st["path"]


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "draft"
    scale, samples, thr = (0.4, 12, 0.05) if mode == "draft" else (1.0, 64, 0.012)
    Tk = Take(); Tk.setup()
    st = Tk.render([G], os.path.join(WORK, mode), scale=scale, samples=samples, threshold=thr)[0]
    sh = Tk.shading_pass(WORK, scale, max(16, samples // 2))
    rep = dict(mode=mode, beauty_raw=os.path.join(WORK, mode, "raw", "f_%04d.png" % G), shade_raw=sh, wall=round(st["wall"], 1),
               heads=C.head_report(Tk, G), cam=list(Tk.loc), look=list(Tk.look), lens=LENS, fstop=FSTOP, **Tk.corners())
    json.dump(rep, open(os.path.join(WORK, mode + ".json"), "w"), default=float)
    print(json.dumps(dict(wall=rep["wall"], heads=rep["heads"])), flush=True)
