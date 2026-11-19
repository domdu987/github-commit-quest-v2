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
G_WORD = C.cap_g("บัลติมอร์")                         # 1646: the pulse overtakes the loco, the loco centred
SNAP = (G_WORD - 3, G_WORD + 10)
WIPE = (G0 - 8, G0 + 10)                             # leading edge enters ... trailing edge leaves
VT, VP = 12.0, 21.0                                  # train, pulse speed (D/s toward -x)
XF0 = 50.0                                           # loco front x at g0 (clear of the station platform, x >= 63)
LOCO_C = 7.0                                         # loco centre behind its front buffer (D)
T_OVER = (G_WORD - G0) / 30.0
RAIL_Y = 13.0
CAM_D, CAM_Z = 17.0, 7.0                             # far side of the track (like the preset): distance to the rail, height
SK = 1.35                                            # snap framing
PULL = 1.9                                           # pull-back factor reached at the end (distance x PULL)
BEAD = 6.0                                           # pulse head / tube size multiplier (the wire is ~25 D behind the train)


def tsec(g):
    return (g - G0) / 30.0


def xf(g):
    return XF0 - VT * tsec(g)


def xp(g):
    return xf(g) + LOCO_C + (VP - VT) * (T_OVER - tsec(g))


def pole_y():
    return float(K.W((LN.px(LN.POLES_Y[1]) + 0.03, LN.POLES_Y[1], 0.0)).y)


def snap_u(g):
    return C.camrig.ease_peak((g - SNAP[0]) / float(SNAP[1] - SNAP[0]), 1.6) if g > SNAP[0] else 0.0


def cam_at(g, py=None):
    """(loc, look): level camera on the far side of the track looking -y; x follows the loco (it stays centred, a little ahead of it);
    a snap push x1.35 over SNAP, then a steady pull-back that keeps loco + carriages in frame until the end."""
    t = (g - GA) / (GB - GA)
    cx = xf(g) + LOCO_C - 0.6 * (g - G_WORD) / 30.0
    u = snap_u(g)
    d = CAM_D * (1.0 + (PULL - 1.0) * t * t) / (SK ** u)
    loc = Vector((cx - 1.0 * u, RAIL_Y + d, CAM_Z + 1.0 * t))
    look = Vector((cx - 1.0 * u, RAIL_Y - 10.0, CAM_Z - 2.05 + 0.6 * t))
    return loc, look


def clear_trees(region):
    """the set's trees are merged meshes (trees_trunk, trees_leaf*): delete the loose islands whose centre lies in region (x0, x1, y0, y1)
    in world D, so a trunk or canopy does not block the camera."""
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
                a_ = stack.pop()
                isl.append(a_)
                for e in a_.link_edges:
                    b_ = e.other_vert(a_)
                    if b_.index not in seen:
                        seen.add(b_.index)
                        stack.append(b_)
            c = ob.matrix_world @ (sum((q.co for q in isl), Vector()) / len(isl))
            if region[0] < c.x < region[1] and region[2] < c.y < region[3]:
                kill += isl
        if kill:
            bmesh.ops.delete(bm, geom=kill, context="VERTS")
            n += 1
        bm.to_mesh(ob.data)
        bm.free()
    return n


def emit_mat(name, hexcol, strength):
    """flat warm emission material (the wipe panel is a few cm from the lens: it must read as a sunlit carriage side whatever the sun does)"""
    m = C.bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out, em = nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeEmission")
    h = hexcol.lstrip("#")
    lin = lambda v: ((v / 255.0 + 0.055) / 1.055) ** 2.4 if v / 255.0 > 0.04045 else v / 255.0 / 12.92
    em.inputs["Color"].default_value = (lin(int(h[0:2], 16)), lin(int(h[2:4], 16)), lin(int(h[4:6], 16)), 1.0)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    return m


def make_wipe():
    """a carriage side (panel 20 D long, 6 D high) built in WORLD axes about its centre, detail on its +y face (the camera looks -y):
    red body, vertical boards, two rows of small cream-framed dark windows, gold lining, black skirt, brass rivets."""
    M = {k: emit_mat("wipe_" + k, c, st) for k, c, st in (("carriage", "#c8452a", 0.85), ("cream", "#efe0b0", 0.95), ("dark", "#2a1d22", 0.9),
                                                     ("black", "#15101a", 0.9), ("gold", "#e0b040", 0.95))}
    mb = K.MB("wipe")
    mb.T = Matrix.Identity(4)
    mb.box(M["carriage"], (0, 0, 0), (20.0, 0.22, 6.0))
    for i in range(39):
        mb.box(M["black"], (-9.75 + i * 0.5, 0.12, 0.0), (0.08, 0.04, 6.0))
    for zz, wz in ((1.1, 0.9), (-0.6, 0.9)):
        for i in range(14):
            wx = -9.1 + i * 1.4
            mb.box(M["cream"], (wx, 0.14, zz), (1.1, 0.05, wz + 0.2))
            mb.box(M["dark"], (wx, 0.17, zz), (0.9, 0.05, wz))
    for zz in (-1.5, 2.3):
        mb.box(M["gold"], (0, 0.15, zz), (20.0, 0.05, 0.12))
    mb.box(M["black"], (0, 0.15, -2.5), (20.0, 0.1, 0.9))
    for i in range(40):
        mb.box(M["gold"], (-9.75 + i * 0.5, 0.17, -1.9), (0.12, 0.05, 0.12))
    obs = mb.finish()
    for ob in obs:
        ob.visible_shadow = False
    return obs


def wipe_xz(g, loc, py=None):
    """panel centre for frame g: sweeps screen-right -> screen-left across the lens (the camera looks -y, so screen-right = -x),
    1.8 D in front of it."""
    u = clamp((g - WIPE[0]) / float(WIPE[1] - WIPE[0]))
    off = lerp(10.0 + 1.2, -(10.0 + 1.2), u)
    return Vector((loc.x - off, loc.y - 2.6, loc.z)), 0.0 < u < 1.0


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
        clear_trees((-30.0, 140.0, 12.0, 60.0))                      # camera side of the track
        for ob in C.bpy.data.objects:                                # no birds on the wire: they sit on the pulse path
            if "_bird" in ob.name:
                ob.hide_render = True
        self.key_cam(bf(GA), *cam_at(GA))
        self.scene.frame_set(bf(GA))
        self.wipe = make_wipe()

    def pose(self, gs):
        pu = TG.STATE["pulse"][0] if "pulse" in TG.STATE else None
        for g in gs:
            f = bf(g)
            loc, look = cam_at(g)
            self.key_cam(f, loc, look)
            TG.set_train(xf(g), frame=f, speed=1.2)
            TG.set_pulse(TG.pulse_s_at_y(xp(g) / 1.85), frame=f)
            pu = TG.STATE["pulse"][0]
            for o in pu[:2]:                                         # bigger head + glow (far wire, phone legibility)
                o.scale = (BEAD, BEAD, BEAD)
                o.keyframe_insert("scale", frame=f)
            for o in TG.STATE["pulse_tube"]:
                if not o.hide_render:
                    o.scale = (BEAD, BEAD, o.scale.z)
                    o.keyframe_insert("scale", frame=f)
            p, vis = wipe_xz(g, loc)
            for ob in self.wipe:
                ob.location = p
                ob.keyframe_insert("location", frame=f)
            C.key_vis(self.wipe, vis, f)

    def report(self, g):
        self.scene.frame_set(bf(g))
        return dict(g=g, cam=[round(c, 2) for c in cam_at(g)[0]], pulse_px=TG.project((xp(g), -7.9, 9.3)),
                    loco_px=TG.project((xf(g) + LOCO_C, RAIL_Y, 2.5)), tail_px=TG.project((xf(g) + 28.0, RAIL_Y, 2.5)), heads={})

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        pv = [cam_at(g) for g in GS]
        for g, (a, b) in zip(GS[:-1], zip(pv[:-1], pv[1:])):
            sp = max(C._corner_shift(a, b, CAM_D + 20.0, cx, cy) for cx in (0, 720) for cy in (0, 1280))
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
