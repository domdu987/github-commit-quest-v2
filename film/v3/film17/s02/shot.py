#!/usr/bin/env python3
"""film 17 take s02 = shots 4-6, film frames g 144..335 + 6 handle frames each side (g 138..341).
  shot 4  g 138..221  street_wide DUSK_EXT: Paris at dusk, parked police wagon, a gendarme marches past, crane-down push + snap
  shot 5  g 222..284  street_wagon DUSK_EXT: gendarmes take the thief (prisoner_c) off the wagon; he tips his cap, smirks
  shot 6  g 285..341  measure_door DAY_INT: the same thief at the front desk shrugs, the gendarme shrugs and waves him through
Blender frame = g.  Two locations => two processes:  python3 shot.py <street|desk> probe|draft|final  a:b[:step]  [outdir]
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import K, cast17, vlerp, mix, snap, lerp, blink
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
    loc = vlerp((-2.4, -4.2, 2.6), (-0.3, 0.6, 1.7), u); look = vlerp((0.4, 11.0, 2.6), (2.0, 11.0, 2.3), u)
    return snaps(g, loc, look, [(166, 12, (0.9, 1.0, -0.15), (1.5, -2.5, -0.4)), (198, 12, (-1.5, 0.6, 0.1), (-2.2, 1.0, 0.3))])
def cam_s5(g):
    u = mix((g - S5[0]) / (S5[1] - S5[0]))
    loc = vlerp((-1.8, 1.3, 1.6), (0.3, 2.6, 1.5), u); look = vlerp((2.6, 7.2, 1.5), (3.2, 6.6, 1.6), u)
    return snaps(g, loc, look, [(238, 12, (0.9, 0.5, -0.05), (0.2, 0.0, 0.05)), (262, 12, (-0.6, 0.6, 0.0), (-0.7, -0.4, 0.0))])
def cam_s6(g):
    u = mix((g - S6[0]) / (S6[1] - S6[0]))
    loc = vlerp((-2.8, 1.6, 1.5), (-2.2, 1.1, 1.45), u); look = vlerp((1.9, -2.6, 1.3), (1.4, -3.0, 1.35), u)
    return snaps(g, loc, look, [(298, 11, (0.35, -0.2, 0.0), (0.3, 0.1, 0.0)), (322, 11, (0.35, -0.3, 0.0), (-0.3, -0.2, 0.0))])
def cam_of(g):
    return cam_s4(g) if g <= S4[1] else cam_s5(g) if g <= S5[1] else cam_s6(g)

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
    return with_blink(cast17.silent(p), g, per, off)

# ------------------------------------------------------------ the take
class Take(C.Take):
    def __init__(self, loc, quality):
        if loc == "street": C.Take.__init__(self, "street_wide", "DUSK_EXT", quality)
        else: C.Take.__init__(self, "measure_door", "DAY_INT", quality)
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
    # ---- street staging
    def stage_street(self, g):
        s4 = g <= S4[1]; f = g
        for a, nm in ((self.ga, "ga"), (self.gb, "gb"), (self.pc, "pc"), (self.gc, "gc")):
            pass
        if s4:                                              # shot 4: wide.  gendarme_a marches +x along street_b line, gendarme_b waits at the wagon door
            x = -2.3 + 0.052 * (g - 138); self.place(self.ga, f, (x, 4.4, 0.0), hs("gendarme_a"))
            wd = self.M["wagon_door"]; self.place(self.gb, f, (wd[0] - 0.5, wd[1] - 0.6, wd[2]), hs("gendarme_b"))
            self.place(self.gc, f, (-0.6, 8.6, 0.0), hs("gendarme_a")); self.place(self.pc, f, (0.0, 30.0, -5.0), hs("prisoner_c"))
            self.hid[g] = ("pc",)
        else:                                               # shot 5: thief steps off the wagon, a gendarme either side
            t = (g - S5[0]) / float(S5[1] - S5[0])
            ws = self.M["wagon_step"]; px = ws[0] - 0.1 + 0.15 * t * 2; py = ws[1] + 0.2 - 0.9 * t
            self.place(self.pc, f, (px, py, 0.0), hs("prisoner_c"))
            self.place(self.ga, f, (px + 0.95, py + 0.15, 0.0), hs("gendarme_a")); self.place(self.gb, f, (px - 0.95, py + 0.1, 0.0), hs("gendarme_b"))
            self.place(self.gc, f, (-0.6, 30.0, -5.0), hs("gendarme_a"))
            self.hid[g] = ("gc",)
    def stage_desk(self, g):
        f = g; t = (g - S6[0]) / float(S6[1] - S6[0])
        x, y, z = self.mark("door_r"); self.place(self.pc, f, (x + 0.45, y + 0.55, z), hs("prisoner_c"))
        x, y, z = self.mark("door_r"); self.place(self.ga, f, (x - 0.15, y - 0.25, z), hs("gendarme_a"))
        x, y, z = self.mark("door_x"); self.place(self.gb, f, (x + 0.2, y + 0.3, z), hs("gendarme_b"))
        self.hid[g] = ("gb",)
    def stage_poses(self, g):
        cam = self.cam
        for a in self.actors.values():
            a.card.hide_render = a.name in self.hid.get(g, ())
            a.card.keyframe_insert("hide_render", frame=g)
        if self.loc == "street":
            if g <= S4[1]:
                self.ga.pose(g, pose_walk("gendarme_a", g, 138, 1), camera=cam)
                self.gb.pose(g, pose_stand("gendarme_standing_b", g, 91, 7, yaw=-0.3), camera=cam)
                self.gc.pose(g, pose_stand("gendarme_standing_a", g, 101, 31, yaw=0.5), camera=cam)
                self.pc.pose(g, pose_stand("prisoner_standing_c", g), camera=cam)
            else:
                tip = C.clamp((g - 250) / 8.0) * (1 - C.clamp((g - 268) / 8.0))        # tips the cap g 250-276
                kw = dict(expr="smirk", yaw=0.15, arm_l="down")
                kw["arm_r"] = "reach_up" if tip > 0.5 else "down"
                self.pc.pose(g, pose_stand("prisoner_standing_c", g, 79, 3, **kw), camera=cam)
                self.ga.pose(g, pose_stand("gendarme_escort_a", g, 97, 11, yaw=-0.2), camera=cam)
                gb = pose_stand("gendarme_escort_b", g, 103, 17, yaw=0.2); gb["mirror"] = True; self.gb.pose(g, gb, camera=cam)
                self.ga.card  # keep
                self.gc.pose(g, pose_stand("gendarme_standing_a", g), camera=cam)
        else:
            sh = C.clamp((g - 292) / 6.0)                                       # thief shrugs g 292..
            self.pc.pose(g, pose_stand("prisoner_standing_c", g, 71, 5, expr="worried", arm_r="shrug", arm_l="shrug", yaw=0.1, mouth="smile"), camera=cam)
            wave = C.clamp((g - 316) / 6.0)
            kw = dict(expr="neutral", yaw=-0.2)
            kw["arm_r"] = "wave" if wave > 0.4 else "shrug" if g > 298 else "behind"; kw["arm_l"] = "shrug" if wave < 0.4 and g > 298 else "behind"
            self.ga.pose(g, pose_stand("gendarme_standing_a", g, 93, 13, **kw), camera=cam)
            self.gb.pose(g, pose_stand("gendarme_standing_b", g, 107, 29, yaw=-0.3), camera=cam)
    def ready(self, gs):
        ppd = 320 if self.loc != "street" else 256
        self.finish_sprites(list(gs), ppd)
    def report(self, g): return dict(g=g, heads=self.heads(g), cam=[round(v, 2) for v in cam_of(g)[0]])

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
