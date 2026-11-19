#!/usr/bin/env python3
"""shot.py -- film 16 take s25 = shot 25 (53.83-56.90 s): LINE line_rail / DAY.  g 1615..1706 + 9 handle frames each side (g 1606..1715).
THE RACE: the 1840s train rolls along the rail beside the pole line; the glowing wire pulse starts behind it, overtakes it (over the
carriages and the loco, around "บัลติมอร์" g 1646) and runs on ahead, leaving the train far behind.  Camera on the field side, level,
tracking LEFT with the pulse (25 D/s, the pulse is 28 D/s so it drifts leftward on screen), snap push x1.6 with a lateral shift at the
overtake (g 1643..1656), slow drift push.  The OBJECT WIPE into the shot (the plan's one wipe): a carriage side sweeps across the lens
right-to-left (g 1607..1626, fully covering the frame g 1609..1624), built at runtime as a panel ~1.8 D in front of the camera.
Hides: pole ladder, the preset's parked pulse.  No characters, no text, no DOF.

    python3 shot.py camreport | probe a:b[:s] | stills a:b[:s] out_dir [scale] [spp] | final a:b[:s] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402

TG, K, LN = C.TG, C.K, C.LN
lerp, clamp, ez, u_of, bf = C.lerp, C.clamp, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(53.83), C.g_bound(56.90)          # 1615, 1707 (exclusive)
H_IN, H_OUT = 9, 9
GA, GB = G0 - H_IN, G1 - 1 + H_OUT                   # 1606 .. 1715
GS = list(range(GA, GB + 1))
PRESET, LIGHT = "line_rail", "DAY"
G_WORD = C.cap_g("บัลติมอร์")                         # 1646: the pulse overtakes the loco
SNAP = (G_WORD - 3, G_WORD + 10)
WIPE = (G0 - 8, G0 + 11)                             # leading edge enters ... trailing edge leaves
VT, VP, VC = 12.0, 28.0, 26.6                        # train, pulse, camera speed (D/s toward -x)
XF0 = 84.0                                           # loco front x at g0
SK = 1.4
T_OVER = (G_WORD - G0) / 30.0
CAM_DY, CAM_Z = 15.0, 3.6                            # camera distance in front of the pole line (D), height


def tsec(g):
    return (g - G0) / 30.0


def xf(g):
    return XF0 - VT * tsec(g)


def xp(g):
    return xf(g) + 4.0 + (VP - VT) * (T_OVER - tsec(g))


def pole_y():
    return float(K.W((LN.px(LN.POLES_Y[1]) + 0.03, LN.POLES_Y[1], 0.0)).y)


def snap_u(g):
    return C.camrig.ease_peak((g - SNAP[0]) / float(SNAP[1] - SNAP[0]), 1.6) if g > SNAP[0] else 0.0


def cam_at(g, py):
    """(loc, look): level camera heading +y; x tracks leftward at VC; a snap push (distance /1.6, shift 1.5 D left) over SNAP."""
    t = (g - GA) / 30.0
    cx = xp(GA) - 2.4 - VC * t
    u = snap_u(g)
    d = (CAM_DY + 21.0) * (1.0 - 0.08 * t / 3.4) / (SK ** u)        # distance to the train depth (+ pole line 20): slow push
    cx -= 1.5 * u
    loc = Vector((cx, py - CAM_DY, CAM_Z))
    look = Vector((cx, py - CAM_DY + 30.0, CAM_Z + 4.2))
    # zoom by moving the camera along its axis
    fwd = (look - loc).normalized()
    loc = loc + fwd * (CAM_DY * (1.0 - 1.0 / (SK ** u)) + 4.0 * t / 3.4)
    return loc, look


def make_wipe():
    """a carriage side (panel 14 D long) built in WORLD axes about its centre: red body, cream window frames, dark glass, brass + black trim."""
    M = TG.STATE["M"]
    mb = K.MB("wipe")
    mb.T = Matrix.Identity(4)
    mb.box(M["carriage"], (0, 0, 0), (14.0, 0.22, 4.4))
    mb.box(M["cream"], (0, -0.12, -1.1), (14.04, 0.06, 0.18))
    mb.box(M["black"], (0, -0.1, -1.95), (14.0, 0.3, 0.5))
    mb.box(M["gold"], (0, -0.13, 1.05), (14.04, 0.05, 0.1))
    for i in range(5):
        wx = -5.6 + i * 2.8
        mb.box(M["cream"], (wx, -0.12, 0.2), (1.9, 0.05, 1.5))
        mb.box(M["dark"], (wx, -0.15, 0.2), (1.6, 0.05, 1.2))
    mb.box(M["dark"], (0, -0.1, 2.12), (14.4, 0.5, 0.3))
    obs = mb.finish()
    for ob in obs:
        ob.visible_shadow = False
    return obs


def wipe_xz(g, loc, py):
    """panel centre for frame g: sweeps right -> left across the lens (x = camera x + offset), 1.8 D in front of it."""
    u = clamp((g - WIPE[0]) / float(WIPE[1] - WIPE[0]))
    off = lerp(7.0 + 0.83, -(7.0 + 0.83), u)
    return Vector((loc.x + off, loc.y + 1.8, loc.z)), 0.0 < u < 1.0


def clear_trees(region):
    """the set's trees are merged meshes (trees_trunk, trees_leaf*): delete the loose islands whose centre lies in region (x0, x1, y0, y1)
    in world D, so the camera path (field side of the pole line) is not blocked by a trunk or a canopy."""
    import bmesh
    n = 0
    for ob in list(C.bpy.data.objects):
        if ob.type != "MESH" or not ob.name.startswith("trees_"):
            continue
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        seen, kill = set(), []
        for v in bm.verts:
            if v.index in seen:
                continue
            stack, isl = [v], []
            seen.add(v.index)
            while stack:
                a = stack.pop()
                isl.append(a)
                for e in a.link_edges:
                    b = e.other_vert(a)
                    if b.index not in seen:
                        seen.add(b.index)
                        stack.append(b)
            c = ob.matrix_world @ (sum((q.co for q in isl), Vector()) / len(isl))
            if region[0] < c.x < region[1] and region[2] < c.y < region[3]:
                kill += isl
        if kill:
            bmesh.ops.delete(bm, geom=kill, context="VERTS")
            n += 1
        bm.to_mesh(ob.data)
        bm.free()
    return n


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s25")
        TG.set_ladder(False, 3)
        clear_trees((-20.0, 140.0, -40.0, -12.0))
        self.py = pole_y()
        self.front0 = TG.STATE["train"]["front0"]
        self.key_cam(bf(GA), *cam_at(GA, self.py))
        self.scene.frame_set(bf(GA))
        self.wipe = make_wipe()

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            loc, look = cam_at(g, self.py)
            self.key_cam(f, loc, look)
            TG.set_train(xf(g) - 0.0, frame=f, speed=1.2)
            s = TG.pulse_s_at_y(xp(g) / 1.85)
            TG.set_pulse(s, frame=f)
            p, vis = wipe_xz(g, loc, self.py)
            for ob in self.wipe:
                ob.location = p
                ob.keyframe_insert("location", frame=f)
            C.key_vis(self.wipe, vis, f)

    def report(self, g):
        self.scene.frame_set(bf(g))
        loc, look = cam_at(g, self.py)
        sp = TG.project((xp(g), self.py + 0.0, 9.3))
        return dict(g=g, cam=[round(c, 2) for c in loc], pulse_px=sp, train_px=TG.project((xf(g) + 6.0, 13.0, 2.5)), heads={})

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        import types
        py = -7.9
        pv = [cam_at(g, py) for g in GS]
        for g, (a, b) in zip(GS[:-1], zip(pv[:-1], pv[1:])):
            sp = max(C._corner_shift(a, b, CAM_DY + 21.0, cx, cy) for cx in (0, 720) for cy in (0, 1280))
            print(g, round(sp, 1))
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GB]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
