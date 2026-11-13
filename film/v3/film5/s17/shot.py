#!/usr/bin/env python3
"""shot.py -- film 5 take s17: shot 17, the ending (g 1814..1967, in-handle 1806..1813), mine set (pithead DUSK).

At the pithead at dusk alfie kneels at the first-aid bench.  The brass oxygen box of the set stands on the bench; its rubber tube
runs (rebuilt at runtime: a bevelled curve from the box's outlet valve) to a small rubber mask alfie holds at the bars of the cage.
The cage stands on the bench right of the box: the cast's 2D `canary_in_cage` (bars drawn over the bird, so the bird is always
visibly inside).  The bird lies on the cage floor, eyes gently closed; it breathes the oxygen, opens its eyes (g 1879, "นกน้อยลืมตา"),
hops back up to its perch, sings one note ("แล้วร้องออกมาอีกหนึ่งโน้ต", g 1899..1934) and stays awake to the end.

    17a g 1806..1871  medium: alfie kneeling holding the mask to the cage, the box on the bench, hut lamp behind; slow push
                      (in-handle 1806..1813)  ("บนปากเหมือง เขาให้นกดมออกซิเจน")
    17b g 1872..1967  cut, closer on the cage + mask + alfie's face: eyes open, hop, one note; slow push, hold to the end
NO depth of field anywhere (client rule).  Sub-shot ids 1..2; Blender frame = 2000 * (id - 1) + (g - 1700).

    python3 shot.py stills <ids> a:b[:step] <out_dir> [scale] [samples] | final <ids> a:b [scale] [samples]
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast5"), os.path.join(V3, "stage"), os.path.join(V3, "set3d5"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast5                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import mine as M                                        # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, lerp, clamp         # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, G1, H = 1814, 1968, 8
B = [G0, 1872, G1]
RANGES = {1: (G0 - H, B[1] - 1), 2: (B[1], G1 - 1)}
NAME = {1: "17a", 2: "17b"}
G_OXY = g_of(61.19)              # 1839 "เขาให้นกดม": the mask comes to the bars
G_EYES = (g_of(62.52), g_of(62.52) + 12)          # 1879..1891 eyes open
G_HOP = (1894, 1899)             # hop from the floor to the perch
G_SING = (g_of(63.32), g_of(64.35))               # 1899..1934 the one note
G_SMILE = 1884

CAGE_AT = Vector((12.30, -4.90, 0.95))                   # cage base bottom on the bench seat, right of the box
ALFIE_AT = Vector((13.25, -5.10, 0.0))
OUTLET = Vector((11.78, -4.65, 1.20))


def _ez(u, kind="sine"):
    return ease(clamp(u), kind)


def bf(shot, g):
    return 2000 * (shot - 1) + int(g) - 1700


CAMS = {
    1: ((Vector((11.00, -8.05, 1.80)), Vector((12.30, -4.95, 1.40))), (Vector((11.20, -7.65, 1.76)), Vector((12.35, -4.95, 1.40)))),
    2: ((Vector((11.72, -6.70, 1.62)), Vector((12.72, -4.95, 1.45))), (Vector((11.86, -6.36, 1.58)), Vector((12.72, -4.95, 1.45)))),
}


def bird_pose(g):
    t = g / 30.0
    if g < G_EYES[0]:
        br = 0.25 + 0.35 * clamp((g - G_OXY) / 30.0)
        return dict(state="fallen", t=t, breath=br, eyes=0.0)
    if g < G_HOP[0]:
        u = _ez((g - G_EYES[0]) / float(G_EYES[1] - G_EYES[0]))
        return dict(state="fallen", t=t, breath=0.6, eyes=u, droop=lerp(0.7, 0.45, u), ruffle=lerp(0.6, 0.4, u))
    if g < G_HOP[1]:
        u = _ez((g - G_HOP[0]) / float(G_HOP[1] - G_HOP[0]), "cubic_out")
        return dict(state="perch_quiet", t=t, lie=1.0 - u, eyes=1.0, droop=0.4 * (1 - u) + 0.2, ruffle=0.35)
    if g <= G_SING[1]:
        return dict(state="sing_one", t=t, notes=1, eyes=1.0, beak=0.55 + 0.2 * math.sin((g - G_SING[0]) * 0.7), droop=0.15, ruffle=0.2)
    u = clamp((g - G_SING[1]) / 6.0)
    return dict(state="perch_quiet", t=t, eyes=1.0, beak=0.0, droop=0.12, ruffle=0.15, notes=1 if u < 0.5 else 0,
                blink=1 if g in (1950, 1951) else 0)


def alfie_pose(g):
    cast, base = cast5.STORY5["alfie_revive"]
    p = dict(base)
    p.pop("prop_r", None)
    p.update(yaw=-0.50, pitch=0.25, lean=8, head_roll=4 + 1.5 * math.sin(g * 0.08), gaze=(-0.85, 0.25))
    happy = _ez((g - G_SMILE) / 10.0)
    p["expr"] = "worried" if happy < 0.5 else "happy"
    p["arm_l"] = dict(hand=(-0.30, 0.55), bend=0.5)              # the other hand on his knee
    p["blink"] = blink(g, [1826, 1862, 1912, 1948])
    if g < G_EYES[0]:
        p["fx"] = ["sweat"]
    return p


CANVAS_ALFIE = (-1.875, -3.875, 1.875, 0.1875)
CANVAS_CAGE = (-1.0625, -1.3125, 1.0625, 0.25)


class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = M.build("pithead", "DUSK")
        M.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 5000
        self.cam = camrig.make_camera(scene, name="cam_s17")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        M.setup_dof(scene, None, None, cam=self.cam)
        sd = os.path.join(TMP, "sprites")
        self.actors = {}
        a = actors.Actor("alfie", "alfie"); a.build(CANVAS_ALFIE, sd, contact=True); self.actors["alfie"] = a
        c = actors.Actor("cage", "canary_in_cage"); c.build(CANVAS_CAGE, sd, contact=True); self.actors["cage"] = c
        for a in self.actors.values():
            a.head_flip = False
            M.no_bounce(a.card)
        self.anch = {}
        self._cut_set_tube()
        for m in bpy.data.materials:                     # the hut / engine windows read as blown flat yellow blocks: calmer
            if m.name.endswith("e_win") and m.node_tree and "strength" in m.node_tree.nodes:
                m.node_tree.nodes["strength"].inputs["Strength"].default_value *= 0.55
        self._mask_and_tube()
        if verbose:
            print("s17: built in %.1f s" % (time.time() - t0), flush=True)

    def _cut_set_tube(self):
        """runtime only: remove the set's lying tube + mask from the oxygen_box mesh (x > 11.79, z < 1.25); my tube replaces them."""
        import bmesh
        ob = bpy.data.objects["oxygen_box"]
        bm = bmesh.new(); bm.from_mesh(ob.data)
        mw = ob.matrix_world
        dead = [v for v in bm.verts if (mw @ v.co).x > 11.79 and (mw @ v.co).z < 1.25]
        bmesh.ops.delete(bm, geom=dead, context="VERTS")
        bm.to_mesh(ob.data); bm.free()
        self.cut = len(dead)

    def _mask_and_tube(self):
        rub = bpy.data.materials.new("s17_rubber"); rub.use_nodes = True
        bsdf = rub.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.12, 0.06, 0.055, 1); bsdf.inputs["Roughness"].default_value = 0.45
        cu = bpy.data.curves.new("s17_tube", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.022; cu.bevel_resolution = 3
        cu.resolution_u = 16
        sp = cu.splines.new("BEZIER"); sp.bezier_points.add(2)
        for bp in sp.bezier_points:
            bp.handle_left_type = bp.handle_right_type = "AUTO"
        cu.materials.append(rub)
        self.tube = bpy.data.objects.new("s17_tube", cu); self.scene.collection.objects.link(self.tube)
        import bmesh
        me = bpy.data.meshes.new("s17_mask"); bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=0.035, radius2=0.085, depth=0.13)
        bm.to_mesh(me); bm.free(); me.materials.append(rub)
        for p in me.polygons:
            p.use_smooth = True
        self.mask = bpy.data.objects.new("s17_mask", me); self.scene.collection.objects.link(self.mask)
        self.mask.rotation_mode = "QUATERNION"
        sol = self.mask.modifiers.new("ink", "SOLIDIFY"); sol.thickness = 0.008; sol.offset = 1; sol.use_flip_normals = True
        sol.material_offset = 1
        ink = bpy.data.materials.new("s17_ink"); ink.use_nodes = True
        ink.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.03, 0.015, 0.03, 1)
        ink.use_backface_culling = True
        me.materials.append(ink)

    def cam_of(self, shot, g):
        g0, g1 = RANGES[shot]
        hold_end = g1 + 1 if shot == 1 else 1950
        u = _ez((g - g0) / float(hold_end - g0), "sine")
        a, b = CAMS[shot]
        return a[0].lerp(b[0], u), a[1].lerp(b[1], u)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = self.cam_of(shot, g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.actors["alfie"].place(f, ALFIE_AT)
            self.actors["cage"].place(f, CAGE_AT)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.actors["cage"].pose(f, bird_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        for f, r in zip(fr, self.actors["cage"].render_sprites(1024 if shot == 2 else 512, frames=fr)):
            self.anch[("cage", f)] = r["anchors"]
        # the mask: its mouth at the bars on the bird's right side, pointing at the bird; the fist behind it
        self.mask_at = {}
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            c = self.actors["cage"]; an = self.anch[("cage", f)]
            bx, by = an.get("bird_body", an["head"])
            fx, fy = an["cage_floor"] if "cage_floor" in an else (0.0, 0.7)
            bob = 0.01 * math.sin(g * 0.15)
            mouth = actors.local_to_world(c, (0.36, fy - 0.15 + bob), f)       # held still at the lower bars
            loc, _ = self.cam_of(shot, g)
            tc = loc - mouth; tc.z = 0; tc.normalize()
            mouth = mouth + tc * 0.06
            X = actors.Actor.basis(c, self.cam)[0]
            axis = (-X).normalized()                            # mask points screen-left (at the bird)
            back = mouth - axis * 0.13
            self.mask_at[f] = (mouth, back, axis)
            self.mask.location = (mouth + back) * 0.5
            self.mask.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(axis)
            camrig.key(self.mask, "location", f, Vector(self.mask.location), "LINEAR", "AUTO")
            camrig.key(self.mask, "rotation_quaternion", f, self.mask.rotation_quaternion.copy(), "LINEAR", "AUTO")
            sp = self.tube.data.splines[0]
            mid = OUTLET.lerp(back, 0.5); mid.z = 0.97
            for bp, p in zip(sp.bezier_points, (OUTLET + Vector((0.04, 0, 0)), mid, back - axis * 0.02)):
                bp.co = p
                bp.keyframe_insert("co", frame=f)
            self.actors["alfie"].pose(f, alfie_pose(g), hands={"r": {"hand": tuple(back - axis * 0.05), "stretch": 1.3}}, camera=self.cam)
        for f, r in zip(fr, self.actors["alfie"].render_sprites(512 if shot == 2 else 256, frames=fr)):
            self.anch[("alfie", f)] = r["anchors"]
            if r.get("clipped"):
                print("s17: WARNING sprite of alfie clipped on frame %d" % f, flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = self.cam_of(shot, g)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads={}, bird=bird_pose(g))
        for a in self.actors.values():
            if (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            hr = 0.5 if a.name == "alfie" else 0.09
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - hr, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + hr, hy), f, res)
            out["heads"][a.name if a.name == "alfie" else "bird"] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        if f in getattr(self, "mask_at", {}):
            m, bk, _ = self.mask_at[f]
            out["pts"] = {"mask": [round(x, 1) for x in render.world_to_screen(self.cam, m, f)[:2]],
                          "fist_target": [round(x, 1) for x in render.world_to_screen(self.cam, bk, f)[:2]]}
            a = self.actors["alfie"]
            hp = actors.local_to_screen(a, self.cam, self.anch[("alfie", f)]["hand_r"], f, a.feet.get(f))
            out["hand_px"] = [round(hp[0], 1), round(hp[1], 1)]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        M.setup_dof(self.scene, None, None, cam=self.cam)        # client rule: no depth of field, ever
        self.scene.cycles.samples = samples
        return render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    Tk = None
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                gs = [RANGES[shot][0], (RANGES[shot][0] + RANGES[shot][1]) // 2, RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            out = os.path.join(HERE, "raw", "s%d" % shot)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if Tk is None:
                Tk = Take("final")
            Tk.pose(shot, todo)
            for g in todo:
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
