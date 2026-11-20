#!/usr/bin/env python3
"""film 17 take s02 = shots 4-6, film frames g 144..335 + 6 handle frames each side (g 138..341).
  shot 4  g 138..221  street_wide DUSK_EXT: Paris at dusk, parked police wagon, a gendarme marches past, crane-down push + snap
  shot 5  g 222..284  street_wagon DUSK_EXT: gendarmes take the thief (prisoner_c) off the wagon; he tips his cap, smirks
  shot 6  g 285..341  measure_door DAY_INT: the same thief at the front desk shrugs, the gendarme shrugs and waves him through
Blender frame = g.  Two locations => two processes:  python3 shot.py <street|desk> probe|draft|final  a:b[:step]  [outdir]
"""
import os, sys, json, math
import bpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import K, cast17, vlerp, mix, snap, lerp, blink
from mathutils import Vector
G0, G1 = 144, 336; HO = 6
S4 = (138, 221); S5 = (222, 284); S6 = (285, 341)
RANGES = {"street": (138, 284), "desk": (285, 341)}
def hs(a): return K.CAST_H[a] / K.CAST_HD[a]

def ez(u): return C.clamp(u)
def idle(g, k=0.012): return (1.0 + k * math.sin(g * 0.21), 1.0 - k * math.sin(g * 0.21))

# ------------------------------------------------------------ cameras
def snaps(g, loc, look, ev):
    for g0, dur, dl, dk in ev:
        k = snap(g, g0, dur); loc = tuple(loc[i] + dl[i] * k for i in range(3)); look = tuple(look[i] + dk[i] * k for i in range(3))
    return loc, look
def cam_s4(g):
    u = mix((g - S4[0]) / (S4[1] - S4[0]))
    loc = vlerp((-2.4, -4.8, 2.6), (-0.9, -1.4, 1.8), u); look = vlerp((3.0, 10.5, 2.0), (3.8, 9.5, 1.9), u)
    return snaps(g, loc, look, [(168, 12, (0.8, 0.9, -0.1), (0.6, -1.5, -0.2)), (198, 12, (-0.9, 0.4, 0.05), (-0.8, 0.8, 0.1))])
def cam_s5(g):
    u = mix((g - S5[0]) / (S5[1] - S5[0]))
    loc = vlerp((WX - 2.4, -0.3, 1.55), (WX - 1.0, 0.5, 1.5), u); look = vlerp((WX, 5.3, 1.5), (WX, 4.6, 1.55), u)
    return snaps(g, loc, look, [(238, 12, (0.8, 0.4, -0.05), (0.2, 0.0, 0.05)), (262, 12, (-0.5, 0.5, 0.0), (-0.5, -0.3, 0.0))])
def cam_s6(g):
    u = mix((g - S6[0]) / (S6[1] - S6[0]))
    loc = vlerp((-3.0, -0.8, 1.45), (-2.0, -1.5, 1.45), u); look = vlerp((1.1, -2.4, 1.3), (1.3, -2.5, 1.3), u)
    return snaps(g, loc, look, [(298, 11, (0.6, -0.3, 0.0), (0.3, -0.1, 0.0)), (322, 11, (-0.5, -0.4, 0.0), (-0.1, -0.2, 0.0))])
def cam_of(g):
    return (snaps(g, *cam_s4(g), []) if False else cam_s4(g)) if g <= S4[1] else cam_s5(g) if g <= S5[1] else cam_s6(g)

# ------------------------------------------------------------ poses
SP = cast17.STORY17
def with_blink(p, g, per=97, off=0):
    p = dict(p); p["blink"] = blink(g, [off + per * k + 40 for k in range(6)]) if False else cast17.blink_at(g, per, off); return p
def pose_walk(cast, g, g0, facing=1):
    base = dict(cast17.STORY17["gendarme_standing_a" if cast == "gendarme_a" else "gendarme_standing_b"][1])
    p = cast17.cycle(cast, (g - g0) / 28.0, "march", facing, base, "both", 1.0); p = cast17.silent(p); return with_blink(p, g, 83)
def pose_stand(name, g, per=89, off=0, **kw):
    p = dict(SP[name][1]); p.update(kw); p["squash"] = idle(g + off)
    p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.13 + off)
    return with_blink(p if "mouth" in kw else cast17.silent(p), g, per, off)

# ------------------------------------------------------------ the take
WY = 7.0; WX = 1.1
class Take(C.Take):
    def hide_puddles(self):
        for o in bpy.data.objects:
            if any(m and m.name.startswith("puddle") for m in getattr(o.data, "materials", []) or []): o.hide_render = True
    def make_wagon(self):
        K.point  # noqa
        B = K.Batch(7); root = bpy.data.objects.new("wagon_root", None); bpy.context.scene.collection.objects.link(root); self.wroot = root
        with B.xf((0, 0, 0)):
            B.box('wagon', (0, 0, 1.45), (1.75, 3.5, 1.7), tint=0.95); B.box('wagon', (0, 0, 2.38), (1.85, 3.6, 0.16))
            B.box('wagon_red', (0, 0, 2.5), (1.9, 3.65, 0.07)); B.box('wagon_red', (0, 0, 0.62), (1.82, 3.55, 0.07))
            for sx in (-1, 1):
                for yy in (-0.7, 0.9):
                    B.box('dark', (sx * 0.88, yy, 1.8), (0.02, 0.6, 0.28))
                    for k in range(4): B.cyl('iron', (sx * 0.895, yy - 0.22 + k * 0.145, 1.8), 0.012, 0.3, seg=6)
            B.box('dark', (0, -1.77, 1.4), (1.1, 0.04, 1.45))                         # the opening behind the rear door
            B.box('iron', (0, -2.1, 0.55), (0.9, 0.3, 0.06))                           # step
            B.box('wagon', (0, 1.55, 2.0), (1.6, 0.9, 0.12)); B.box('leather', (0, 1.7, 2.12), (1.2, 0.4, 0.2)); B.box('wagon', (0, 1.95, 2.45), (1.5, 0.08, 0.8))
            for sx in (-1, 1):
                B.box('iron', (sx * 0.4, 2.7, 0.95), (0.06, 2.0, 0.06)); B.box('iron', (sx * 0.4, 3.7, 1.0), (0.1, 0.1, 0.1))
                for (yy, rr) in ((-1.15, 0.52), (1.1, 0.62)):
                    B.cyl('wagon_red', (sx * 0.98, yy, rr), rr, 0.1, axis='x', seg=24); B.cyl('brass', (sx * 1.04, yy, rr), 0.07, 0.08, axis='x', seg=10)
                    for k in range(8): B.box('iron', (sx * 1.03, yy, rr), (0.04, 0.03, rr * 1.8), rot=(k * 22.5, 0, 0))
            B.cyl('iron', (0, -1.15, 0.52), 0.045, 2.0, axis='x', seg=8); B.cyl('iron', (0, 1.1, 0.62), 0.045, 2.0, axis='x', seg=8)
            B.cyl('brass', (-0.9, 1.9, 2.25), 0.07, 0.25, seg=8); B.sphere('glow_gas', (-0.9, 1.9, 2.45), 0.1)
        B.finalize("wag", parent=root, ink_t=K.STATE['ink_t'])
        hinge = bpy.data.objects.new("wagon_hinge", None); bpy.context.scene.collection.objects.link(hinge); hinge.parent = root; hinge.location = (-0.6, -1.9, 0)
        D = K.Batch(8); D.box('wagon', (0.6, 0, 1.45), (1.2, 0.1, 1.5)); D.box('dark', (0.6, -0.06, 1.5), (0.5, 0.02, 0.6)); D.box('brass', (1.0, -0.07, 1.3), (0.06, 0.03, 0.2))
        D.finalize("wagdoor", parent=hinge, ink_t=K.STATE['ink_t']); self.hinge = hinge
    def make_desk(self):
        B = K.Batch(9); K.table(B, (1.2, -2.65), size=(1.7, 0.8), h=0.85, rot=22); self.tpos = (1.2, -2.65)
        with B.xf((1.2, -2.65, 0.85), (0, 0, 22)):
            K.open_ledger(B, (-0.35, 0.0, 0.0), rot=10); K.inkpot(B, (0.55, 0.12, 0.0), quill=False); K.ledger_stack(B, (0.4, -0.15, 0.0), n=3, rot=8)
        B.finalize("desk", ink_t=K.STATE['ink_t'] * 0.8)

    def __init__(self, loc, quality):
        if loc == "street":
            K.police_wagon = lambda B, c, rot=0: None            # the set's wagon is merged into the street batch: drop it, build our own animated one
            C.Take.__init__(self, "street_wide", "DUSK_EXT", quality)
            self.make_wagon(); self.hide_puddles()
        else:
            C.Take.__init__(self, "measure_door", "DAY_INT", quality, fg=False)
            self.make_desk()
        self.loc = loc; sd = os.path.join(HERE, "work", "sprites_" + loc)
        M = self.A["marks"]; self.M = M
        if loc == "street":
            self.ga = self.mk("ga", "gendarme_a", sd); self.gb = self.mk("gb", "gendarme_b", sd); self.pc = self.mk("pc", "prisoner_c", sd); self.gc = self.mk("gc", "gendarme_a", sd)
            self.ga.head_flip = self.gb.head_flip = self.pc.head_flip = self.gc.head_flip = True
        else:
            self.pc = self.mk("pc", "prisoner_c", sd); self.ga = self.mk("ga", "gendarme_a", sd); self.gb = self.mk("gb", "gendarme_b", sd)
        self.hid = {}
    def mark(self, k, dx=0, dy=0): x, y, z, fz, who = self.M[k]; return (x + dx, y + dy, z)
    def pose(self, gs):
        cam = self.cam
        for g in gs:
            f = g; loc, look = cam_of(g); self.key_cam(f, loc, look)
            K.set_flicker(1.0, frame=f); K.set_smoke(1.0, frame=f); K.set_dust(0.5 if self.loc == 'desk' else 1.0, frame=f); K.set_pendulum(frame=f)
            if self.loc == "street": self.stage_street(g)
            else: self.stage_desk(g)
        for g in gs:
            self.scene.frame_set(g); self.stage_poses(g)
    def rvec(self):
        return self.cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
    def stage_street(self, g):
        f = g
        # wagon rolls in from depth, eased stop by g200
        k = C.clamp((g - 128) / (200 - 128.0)); e = 1 - (1 - k) ** 2.2
        wy = WY + 15.0 * (1 - e); self.wroot.location = (WX, wy, 0.012 * math.sin(g * 1.7) * (1 - e) + 0); self.wroot.keyframe_insert("location", frame=f)
        op = C.clamp((g - 218) / 16.0); ang = -math.radians(150) * (1 - (1 - op) ** 2) if g >= 218 else 0.0
        self.hinge.rotation_euler = (0, 0, ang); self.hinge.keyframe_insert("rotation_euler", frame=f)
        self.hid[g] = ()
        if g <= S4[1]:
            x = -1.3 + 0.032 * min(g - 138, 62); self.place(self.ga, f, (x, 4.6, 0.0), hs("gendarme_a"))
            self.place(self.gb, f, (4.9, 8.4, 0.3), hs("gendarme_b")); self.place(self.pc, f, (0, 30, -5), 1.0); self.place(self.gc, f, (0, 30, -5), 1.0)
            self.hid[g] = ("pc", "gc")
        else:
            t = (g - S5[0]) / float(S5[1] - S5[0]); px = WX - 0.1 - 0.2 * t; py = WY - 2.5 - 1.0 * t
            self.tp = (px, py)
            self.place(self.pc, f, (px, py, 0.0), hs("prisoner_c"))
            self.ga.place(f, (px + 0.72, py + 0.05, 0.0), scale=hs("gendarme_a"), flip=True); self.place(self.gb, f, (px - 0.72, py + 0.05, 0.0), hs("gendarme_b"))
            self.place(self.gc, f, (0, 30, -5), 1.0); self.hid[g] = ("gc",)
    def stage_desk(self, g):
        f = g; tx, ty = self.tpos
        self.place(self.pc, f, (0.9, -1.9, 0.0), hs("prisoner_c"))
        self.place(self.ga, f, (1.5, -3.4, 0.0), hs("gendarme_a"))
        self.place(self.gb, f, (0, 30, -5), 1.0); self.hid[g] = ("gb",)
    def stage_poses(self, g):
        cam = self.cam
        for a in self.actors.values():
            a.card.hide_render = a.name in self.hid.get(g, ())
            a.card.keyframe_insert("hide_render", frame=g)
        CL = dict(mouth="flat")
        if self.loc == "street":
            if g <= S4[1]:
                if g < 200: self.ga.pose(g, dict(pose_walk("gendarme_a", g, 138, 1), **CL), camera=cam)
                else: self.ga.pose(g, pose_stand("gendarme_standing_a", g, 83, 5, yaw=0.3, **CL), camera=cam)
                self.gb.pose(g, pose_stand("gendarme_standing_b", g, 91, 7, yaw=-0.3, **CL), camera=cam)
                self.pc.pose(g, pose_stand("prisoner_standing_c", g, **CL), camera=cam); self.gc.pose(g, pose_stand("gendarme_standing_a", g, **CL), camera=cam)
            else:
                px, py = self.tp; r = self.rvec(); cl = self.cam.matrix_world.translation; fwd = Vector((0, 1, 0))
                tw = Vector((px, py, 0.0)); toward = (cl - tw).normalized() * 0.08
                arm_z = 1.0
                tip = C.clamp((g - 246) / 8.0) * (1 - C.clamp((g - 270) / 8.0))
                # thief: both upper arms held; right hand goes to the beret brim while tipping
                kwp = dict(expr="smirk", yaw=0.0, arm_l="down", arm_r="down", mouth="smile")
                pcp = pose_stand("prisoner_standing_c", g, 79, 3, **kwp)
                hands = None
                if tip > 0.5: hands = {"r": {"hand": tuple(tw + r * 0.06 + Vector((0, 0, 1.56)) + toward * 3), "layer": "top", "bend": 0.9}}
                _p, _i = self.pc.pose(g, pcp, hands=hands, camera=cam); self.dbg = _i
                ga = pose_stand("gendarme_escort_a", g, 97, 11, yaw=-0.25, mouth="flat")
                self.ga.pose(g, ga, hands={"r": {"hand": tuple(tw + r * 0.2 + Vector((0, 0, arm_z)) + toward)}}, camera=cam)
                gb = pose_stand("gendarme_escort_b", g, 103, 17, yaw=0.25, mouth="flat")
                self.gb.pose(g, gb, hands={"r": {"hand": tuple(tw - r * 0.2 + Vector((0, 0, arm_z)) + toward)}}, camera=cam)
                self.gc.pose(g, pose_stand("gendarme_standing_a", g, **CL), camera=cam)
        else:
            tw = Vector((0.9, -1.9, 0.0)); r = self.rvec()
            self.pc.pose(g, pose_stand("prisoner_standing_c", g, 71, 5, expr="worried", arm_r="shrug", arm_l="shrug", yaw=0.5, mouth="flat"), camera=cam)
            wave = C.clamp((g - 316) / 10.0)
            kw = dict(expr="neutral", yaw=-0.4, mouth="flat", arm_l="shrug" if g > 300 and wave < 0.3 else "behind")
            kw["arm_r"] = "wave" if wave > 0.3 else "shrug" if g > 298 else "behind"
            self.ga.pose(g, pose_stand("gendarme_standing_a", g, 93, 13, **kw), camera=cam)
            self.gb.pose(g, pose_stand("gendarme_standing_b", g, **CL), camera=cam)
    def ready(self, gs):
        ppd = 320 if self.loc != "street" else 256
        self.finish_sprites(list(gs), ppd)
    def report(self, g): return dict(dbg=str(getattr(self,'dbg',''))[:200], g=g, heads=self.heads(g), cam=[round(v, 2) for v in cam_of(g)[0]])

if __name__ == "__main__":
    loc, cmd, spec = sys.argv[1], sys.argv[2], sys.argv[3]; out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "raw", loc)
    scale = float(os.environ.get("SCALE", "0.5")); samples = int(os.environ.get("SAMPLES", "6"))
    lo, hi = RANGES[loc]; gs = [g for g in C.parse(spec) if lo <= g <= hi]
    if cmd == "final":                                       # resumable
        gs = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
    T = Take(loc, "draft" if scale < 1 else "final")
    if not gs: sys.exit()
    T.pose(gs); T.ready(gs)
    os.makedirs(out, exist_ok=True)
    for g in gs:
        st = T.render([g], out, scale, samples)[0]; os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
        print(json.dumps(dict(T.report(g), wall=round(st["wall"], 1))), flush=True)
