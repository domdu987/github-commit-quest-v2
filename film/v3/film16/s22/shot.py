#!/usr/bin/env python3
"""shot.py -- film 16 take s22 = shot 22, "ทางออกคือแก้ว" (the answer is glass). g 1381..1454 + 9 handle frames each side (dissolve in 11 f,
cut out at 1455).  LINE line_wagon / AFTER_RAIN.  Morse stands on the wagon bed (mark morse_wagon_bed), takes the nearest bottle out of the
crate by the neck and lifts it to the sun; a sun glint flares on the held glass; snap push on "แก้ว" (event g 1392).

The crate is one baked mesh: the picked bottle is removed from a runtime COPY of the crate glass / glint meshes (bmesh islands) that is
switched on when the hand takes it; the held bottle is a runtime upright copy (LN.beer_bottle, the crate's own glass material) pinned to his fist.
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] out [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector, Matrix, Euler              # noqa: E402
import bmesh                                             # noqa: E402

TG, K, LN, actors, cast16 = C.TG, C.K, C.LN, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(46.02), C.g_bound(48.51)   # 1381, 1455: shot 22 = g 1381..1454
H_IN = H_OUT = 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1   # 1372, 1463
GS = list(range(G_FIRST, G_LAST + 1))
G_WORD = 1392                                  # "แก้ว" (46.3 s + 0.1)
SNAP = (G_WORD - 3, G_WORD + 10)               # 13 frames
G_REACH = (G_FIRST, 1380)                      # hand to the crate neck
G_TAKE = 1382                                  # the crate bottle leaves the crate (copy meshes swap)
G_LIFT = (1383, 1398)                          # lifted to the sun
G_GLINT = (1396, 1410)                         # sun glint flare on the held glass
G_GLINT2 = (1432, 1442)                        # second twinkle
BLINKS = [1405, 1440]

LIGHT, PRESET = "AFTER_RAIN", "line_wagon"
PPD = 256
CANVAS = (-2.25, -4.75, 2.25, 0.125)
GRIP = lambda: 0.15 * 2.9 * K.SC               # neck grip height above the bottle base (world D)

SUN_POINT = lambda mk: Vector(mk) + Vector((0.2, -0.3, 3.6))        # where the held bottle is raised (set from the mark in Take)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s22")
        mk = self.A["marks"]["morse_wagon_bed"]
        mk = (mk[0] - 0.75, mk[1], mk[2])
        self.mark = mk
        self.split_crate()
        cam_loc, cam_look = Vector(self.A["cam"]["loc"]), Vector(self.A["cam"]["look_at"])
        self.subject = Vector((mk[0] - 0.4, mk[1] + 0.1, mk[2] + 2.3))
        start = Vector(self.subject).lerp(cam_loc, 0.60) + Vector((0, 0, 0.8))
        self.cam_path = C.CamPath(start, self.subject, G0, G_LAST, push=0.08, slide_px=-50.0, rise_px=10.0, arc_deg_s=-12.0, decay=0.3,
                                  snaps=[dict(g=SNAP, k=1.9, peak=1.9, shift=(0.15, 0.3))])
        self.key_cam(bf(G_FIRST), *self.cam_path.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", os.path.join(WORK, "sprites"), canvas=CANVAS, contact=True, cam=self.cam)
        mb = K.MB("s22_bottle")
        LN.beer_bottle(mb, TG.STATE["M"], (0.0, 0.0, -0.15 * 2.9), 2.9, G=LN.crate_glass())      # origin = the neck grip
        self.bottle = mb.finish()
        fm = K.MB("s22_flash")
        LN.glint(fm, TG.STATE["M"], (0.0, 0.0, 0.0), 0.32)
        self.flash = fm.finish()[0]
        self.flash.visible_shadow = False
        self.hand_err = {}

    # -- crate: remove one bottle from a copy ------------------------------------------------------------------------------------
    def split_crate(self):
        obs = {ob.name: ob for ob in C.bpy.data.objects if ob.type == "MESH" and ob.name in ("work_glass_crate", "work_glintm", "work_glintrim")}
        self.crate_orig = list(obs.values())
        g = obs["work_glass_crate"]
        bm = bmesh.new(); bm.from_mesh(g.data)
        mw = g.matrix_world
        # islands by connectivity
        seen, isl = set(), []
        for v in bm.verts:
            if v.index in seen:
                continue
            stack, comp = [v], []
            seen.add(v.index)
            while stack:
                a = stack.pop(); comp.append(a)
                for e in a.link_edges:
                    b = e.other_vert(a)
                    if b.index not in seen:
                        seen.add(b.index); stack.append(b)
            isl.append(comp)
        # a bottle = several rod islands on one vertical axis: merge islands whose xy centroids are within 0.25 D
        cl = []
        for c in isl:
            cen = sum((mw @ v.co for v in c), Vector()) / len(c)
            for k in cl:
                if (k["xy"] - cen.xy).length < 0.25:
                    k["v"] += c; break
            else:
                cl.append(dict(xy=cen.xy.copy(), v=list(c)))
        big = [k for k in cl if len(k["v"]) > 150]
        mk = Vector(self.mark)
        pk = min(big, key=lambda k: (k["xy"] - mk.xy).length)
        isl = [pk["v"]]; pick = 0
        base_z = min((mw @ v.co).z for v in pk["v"])
        self.base = Vector((pk["xy"].x, pk["xy"].y, base_z))
        print("crate bottles found:", len(big), "picked", tuple(round(c, 2) for c in self.base), flush=True)
        bmesh.ops.delete(bm, geom=[v for v in isl[pick]], context="VERTS")
        me = g.data.copy(); bm.to_mesh(me); bm.free()
        cp = C.bpy.data.objects.new("crate_glass_minus", me); cp.matrix_world = g.matrix_world.copy()
        for c in g.users_collection:
            c.objects.link(cp)
        self.crate_new = [cp]
        for nm in ("work_glintm", "work_glintrim"):
            o = obs[nm]; bm2 = bmesh.new(); bm2.from_mesh(o.data); mw2 = o.matrix_world
            kill = [v for v in bm2.verts if (mw2 @ v.co).xy.__sub__(self.base.xy).length < 0.45 and (mw2 @ v.co).z > base_z]
            bmesh.ops.delete(bm2, geom=kill, context="VERTS")
            me2 = o.data.copy(); bm2.to_mesh(me2); bm2.free()
            c2 = C.bpy.data.objects.new(nm + "_minus", me2); c2.matrix_world = o.matrix_world.copy()
            for c in o.users_collection:
                c.objects.link(c2)
            self.crate_new.append(c2)

    # -- timeline ---------------------------------------------------------------------------------------------------------------
    def neck0(self):
        return self.base + Vector((0, 0, GRIP()))

    def bottle_at(self, g):
        """world point of the neck grip + tilt deg"""
        n0 = self.neck0()
        up = Vector(self.mark) + Vector((-0.65, -0.35, 3.25))
        u = u_of(g, *G_LIFT)
        p = n0.lerp(up, u)
        p.z += 0.18 * math.sin(math.pi * u)
        if g > G_LIFT[1]:
            t = g - G_LIFT[1]
            p += Vector((0.05 * math.sin(t * 0.17), 0.0, 0.09 * math.sin(t * 0.23)))      # held up: a small live bob
        tilt = lerp(0.0, 10.0, u) + (3.0 * math.sin(max(0, g - G_LIFT[1]) * 0.19) if g > G_LIFT[1] else 0.0)
        return p, tilt

    def pose_of(self, g):
        p = dict(cast16.STORY16["morse_bottle_sun"][1])
        p.pop("prop_r", None)
        p["glint"] = 0.0
        p["expr"], p["mouth"] = "happy", "smile"
        u = u_of(g, *G_LIFT)
        p["pitch"] = lerp(0.1, -0.5, u)
        p["lean"] = 1.5 * math.sin(g * 0.21)
        p["head_roll"] = lerp(0.0, -5.0, u) + 1.5 * math.sin(g * 0.15)
        p["blink"] = blink(g, BLINKS)
        p["gaze"] = (0.6, -0.9) if g >= G_LIFT[0] + 4 else (0.5, 0.2)
        p["legs"] = dict(stride=0.0, crouch=0.10 * (1.0 - u))
        p["t"] = g / 30.0
        return p

    def hands_of(self, g):
        m, _ = self.bottle_at(g)
        return {"r": {"hand": tuple(m)}}

    def flash_scale(self, g):
        s = 0.0
        for a, b in (G_GLINT, G_GLINT2):
            if a <= g <= b:
                u = (g - a) / float(b - a)
                s = max(s, 1.5 * math.sin(math.pi * min(1.0, u * 1.5)) if u < 0.66 else 1.5 * (1 - u) / 0.34 * 0.5)
        return s

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cam_path.at(g))
            C.place(self.mor, f, self.mark)
            taken = g >= G_TAKE
            C.key_vis(self.crate_orig, not taken, f)
            C.key_vis(self.crate_new, taken, f)
            m, tilt = self.bottle_at(g)
            for ob in self.bottle:
                ob.location = m
                ob.rotation_euler = Euler((0.0, math.radians(tilt), 0.0))
                ob.keyframe_insert("location", frame=f); ob.keyframe_insert("rotation_euler", frame=f)
            C.key_vis(self.bottle, taken, f)
            s = self.flash_scale(g)
            rot = Matrix.Rotation(math.radians(tilt), 3, "Y")
            self.flash.location = m + rot @ Vector((-0.10, -0.12, 0.62))
            self.flash.scale = (max(s, 1e-3),) * 3
            self.flash.keyframe_insert("location", frame=f); self.flash.keyframe_insert("scale", frame=f)
            C.key_vis(self.flash, s > 0.02, f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            _, info = self.mor.pose(f, self.pose_of(g), hands=self.hands_of(g), camera=self.cam)
            self.hand_err[g] = round(max([v.get("error", 0.0) for v in info.values()] or [0.0]), 3)
        self.sprites_for([(self.mor, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.cam_path.at(g)
        m, _ = self.bottle_at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), hand_err=self.hand_err.get(g),
                    bottle_px=TG.project(tuple(m)), taken=g >= G_TAKE)

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        Tk = None
        print("run probe instead"); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
