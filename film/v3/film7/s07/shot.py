#!/usr/bin/env python3
"""shot.py -- film 7 take s07: shots 7-9 (plan 19.96-30.66 s = g 599..919) + 6-frame handles (g 593..925), all in the Salon Carre
(louvre gallery area, GALLERY_DAY), seven camera set-ups (a framing change every 1.3-1.9 s):

  shot 7 "vincenzo (normal clothes) fitting a glass pane on the painting, careful"
    id 1  g 593..648  medium: vincenzo on a little step-stool beside the Mona Lisa offers a big glass pane to her frame, careful,
                      tongue-in-cheek concentration; slow push.                       ("ส่วนเขาคือ วินเชนโซ ช่างกระจกชาวอิตาลี")
    id 2  g 649..695  ECU insert: the pane settles flush on her frame, a glint sweeps across it, his fingertips smooth the edge.
  shot 8 "vincenzo small among tall coworkers carrying glass panes"
    id 3  g 696..740  wide across the salon: three glaziers walk screen-right carrying panes, the tall thin one leading, the small
                      Italian in the middle, the stout one behind; the camera pans with them.        ("กระจกกันภาพให้ลูฟวร์")
    id 4  g 741..781  closer tracking two-shot: vincenzo dwarfed between the two, glancing up at them.  ("รวมถึงภาพนี้ด้วย")
  shot 9 "coworkers laugh and point ('ไอ้มักกะโรนี!' lip-sync), vincenzo_mocked, then a glare (hurt)"
    id 5  g 782..835  three-shot: panes leaned on the divan, the two point and laugh at him (static laughing mouths), he shrinks.
    id 6  g 836..882  low two-shot of the coworkers: laughing, then the jeer "ไอ้มักกะโรนี!" LIP-SYNCED on the narration's quote
                      (caption 28.53-29.23 s -> g 859..880, the only moving mouths of the take).
    id 7  g 883..925  close on vincenzo: head down, blush (mocked), then the hurt side-glare at them (g 890..), fists; slow push.
                      Handle g 920..925 continues the push.
NO depth of field anywhere (client rule): C.Take switches it off at build and before every render.  Blender frame = 1000*(id-1)+g+1.

    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1,2,.. a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector, Matrix, Euler              # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0, G1 = C.g_bound(19.96), C.g_bound(30.66)          # 599, 920
G8, G9 = C.g_bound(23.20), C.g_bound(26.05)          # 696, 782
H = 6
RANGES = {1: (G0 - H, 648), 2: (649, G8 - 1), 3: (G8, 740), 4: (741, G9 - 1), 5: (G9, 835), 6: (836, 882), 7: (883, G1 + H - 1)}
G_QUOTE = (C.g_of(28.53), C.g_of(29.23))             # 859..880 "ไอ้มักกะโรนี" -> coworkers' lip-sync
G_TEASE = C.g_of(27.33)                              # 823 "ชอบล้อเขา"
G_HURT = C.g_of(29.23)                               # 880 "เขาเจ็บใจ"
G_GLARE = (890, 896)

# ----------------------------------------------------------------------------- shot 7: the pane on her frame
MC = Vector(L.MONA_C)                                # (0, 21.92, 3.55)
PANE7 = (1.36, 1.82)                                 # w, h (D) -- covers her frame
STOOL = (Vector((1.42, 21.15, 0.0)), Vector((2.14, 21.72, 0.56)))
VIN7 = Vector((1.75, 21.44, 0.56))                   # feet on the stool top
G_SET = 684                                          # the pane is flush


def pane7_state(g, yF):
    """(centre, rot_z rad) of the pane.  id 1 (g ..648): he carries it from before him toward her frame (still 0.45 D short, tilted);
    id 2 (649..): the insert -- it slides the last 0.45 D and settles flush on the frame front (yF) at G_SET."""
    if g <= RANGES[1][1]:
        u = ez((g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0]), "sine")
        off = Vector(lerp((1.02, -0.48, -0.95), (0.55, -0.22, -0.55), u))
        rz = math.radians(lerp(22.0, 9.0, u))
    else:
        u = ez((g - RANGES[2][0]) / float(G_SET - RANGES[2][0]), "sine") if g < G_SET else 1.0
        off = Vector(lerp((0.50, -0.20, -0.50), (0.0, 0.0, 0.0), u))
        rz = math.radians(lerp(8.0, 0.0, u))
    wob = 0.010 * math.sin(g * 0.5) * (1.0 if g < G_SET else 0.0)
    return Vector((MC.x, yF, MC.z)) + off + Vector((0, 0, wob)), rz


def cam7(sid, g):
    if sid == 1:
        u = ez((g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0]))
        return (Vector(lerp((0.45, 16.4, 3.40), (0.50, 17.2, 3.35), u)), Vector(lerp((0.95, 21.9, 2.62), (0.95, 21.9, 2.66), u)), 24.0)
    u = ez((g - RANGES[2][0]) / float(RANGES[2][1] - RANGES[2][0]))
    return (Vector(lerp((0.42, 19.35, 3.62), (0.36, 19.62, 3.60), u)), Vector(lerp((-0.02, 21.9, 3.50), (-0.02, 21.9, 3.52), u)), 40.0)


# ----------------------------------------------------------------------------- shot 8: carrying the panes across the salon
WALK_Y = 15.6
SPD = 0.056                                          # D per frame (walk cycle 28 f)
X8 = {"cw1": 1.55, "vin": 0.0, "cw2": -1.55}         # offsets along x in the file (cw1 leads, screen-right)
X8_0 = -3.4                                          # vincenzo's x at g 696


def x8(name, g):
    return X8_0 + X8[name] + SPD * (g - G8)


def cam8(sid, g):
    vx = x8("vin", g)
    if sid == 3:
        return (Vector((vx * 0.55 - 1.5, 10.6, 3.45)), Vector((vx * 0.85 - 0.2, 17.0, 2.25)), 22.0)
    return (Vector((vx + 0.55, 12.55, 2.30)), Vector((vx + 0.35, 17.0, 2.55)), 22.0)


PANE_C = {"vin": (1.10, 1.32), "cw1": (1.25, 1.55), "cw2": (1.25, 1.45)}     # carried pane w, h
GRIP_Z = {"vin": 1.22, "cw1": 1.62, "cw2": 1.42}


def carried_pane(name, g):
    """centre of the pane a walker carries: in front of him (toward the lens), hands on its side edges; bobs with the step."""
    w, h = PANE_C[name]
    bob = 0.025 * math.cos(2 * math.pi * ((g - G8) / 14.0 + (0.3 if name != "vin" else 0.0)))
    return Vector((x8(name, g), WALK_Y - 0.32, GRIP_Z[name] + bob))


# ----------------------------------------------------------------------------- shot 9: the mockery
P9 = {"cw1": Vector((-1.95, 16.15, 0)), "cw2": Vector((-0.55, 15.55, 0)), "vin": Vector((1.15, 15.85, 0))}


def cam9(sid, g):
    if sid == 5:
        u = ez((g - RANGES[5][0]) / float(RANGES[5][1] - RANGES[5][0]))
        return (Vector(lerp((2.35, 12.0, 2.75), (2.15, 12.35, 2.72), u)), Vector((-0.45, 16.0, 1.95)), 18.0)
    if sid == 6:
        u = ez((g - RANGES[6][0]) / float(RANGES[6][1] - RANGES[6][0]))
        return (Vector(lerp((0.35, 11.75, 1.75), (0.20, 12.15, 1.75), u)), Vector((-1.20, 16.0, 2.95)), 22.0)
    u = ez((g - RANGES[7][0]) / float(RANGES[7][1] - RANGES[7][0]))
    return (Vector(lerp((2.15, 12.75, 2.32), (1.95, 13.25, 2.32), u)), Vector((0.95, 16.0, 2.12)), 24.0)


def cam_of(sid, g):
    if sid <= 2:
        return cam7(sid, g)
    if sid <= 4:
        return cam8(sid, g)
    return cam9(sid, g)


# ----------------------------------------------------------------------------- props built at runtime
def _glass_edge_mats():
    M = L.STATE['M']
    edge = L.mat_lit('s07_pane_edge', '#cfe9ee')
    glint = L.mat_emit('s07_glint', '#ffffff', strength=0.55, camera_only=True, additive=True)
    return M['glass'], edge, glint


def make_pane(name, w, h, glints=True):
    """a loose glass pane centred on its origin, in the x-z plane (faces -y): the louvre glass sheen + thin pale-green edges
    (glass seen edge-on) + two diagonal camera-only glint streaks."""
    gm, em, gl = _glass_edge_mats()
    mb = L.MB(); eb = L.MB(); gb = L.MB()
    x0, x1, z0, z1 = -w / 2, w / 2, -h / 2, h / 2
    mb.oface([(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], gm, [(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], (0, -1, 0))
    e = 0.022
    for lo, hi in (((x0, -0.012, z0), (x1, 0.012, z0 + e)), ((x0, -0.012, z1 - e), (x1, 0.012, z1)),
                   ((x0, -0.012, z0), (x0 + e, 0.012, z1)), ((x1 - e, -0.012, z0), (x1, 0.012, z1))):
        eb.box(lo, hi, em)
    o = L._obj(mb, name, L.STATE['SET'], shadow=False)
    oe = L._obj(eb, name + "_edge", L.STATE['SET'])
    oe.parent = o
    parts = [o, oe]
    if glints:
        for k, (a, wd) in enumerate(((0.18, 0.10), (0.42, 0.045))):
            # a slanted band across the pane, clipped to it (x from the left edge fraction a)
            xa = x0 + a * w; s = 0.55 * h
            pts = [(xa, -0.014, z0 + 0.06), (xa + wd, -0.014, z0 + 0.06), (min(x1 - 0.03, xa + wd + s), -0.014, z1 - 0.06),
                   (min(x1 - 0.03, xa + s), -0.014, z1 - 0.06)]
            gb.oface(pts, gl, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        og = L._obj(gb, name + "_glint", L.STATE['SET'], shadow=False)
        og.parent = o
        og.visible_diffuse = og.visible_glossy = False
        parts.append(og)
    o.rotation_mode = "XYZ"
    return o


def key_obj(o, f, loc, rz=0.0, rx=0.0):
    o.location = Vector(loc); o.rotation_euler = (rx, 0.0, rz)
    o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)


def pane_point(o, f, lx, lz):
    """world point of pane-local (x, z) at frame f (from the keyed transform)."""
    bpy.context.scene.frame_set(f)
    bpy.context.view_layer.update()
    return tuple(o.matrix_world @ Vector((lx, 0.0, lz)))


def split_rope():
    """the velvet rope + its brass stanchions before her (x -0.55..2.8, y 20.4; 2.3 D tall: they cut across him in shot 7) go to
    their own object so shot 7 can hide them (unhooked for the glaziers' work).  Returns that object."""
    import bmesh
    ob = bpy.data.objects['gallery_dressing']
    cp = ob.copy(); cp.data = ob.data.copy(); cp.name = 's07_rope_part'
    for c in ob.users_collection:
        c.objects.link(cp)
    def inband(fc):
        c = fc.calc_center_median()
        return 20.0 < c.y < 20.8 and -0.55 < c.x < 2.85
    for o, keep_band in ((ob, False), (cp, True)):
        bm = bmesh.new(); bm.from_mesh(o.data)
        dead = [f for f in bm.faces if inband(f) != keep_band]
        bmesh.ops.delete(bm, geom=dead, context='FACES')
        bm.to_mesh(o.data); bm.free()
    return cp


def build_stool():
    M = L.STATE['M']; mb = L.MB()
    lo, hi = STOOL
    mb.box((lo.x, lo.y, hi.z - 0.08), (hi.x, hi.y, hi.z), M['wood_l'])
    for xx in (lo.x + 0.05, hi.x - 0.1):
        for yy in (lo.y + 0.05, hi.y - 0.1):
            mb.box((xx, yy, 0), (xx + 0.05, yy + 0.05, hi.z - 0.08), M['wood'])
    mb.box((lo.x + 0.05, lo.y + 0.05, 0.25), (hi.x - 0.05, lo.y + 0.1, 0.3), M['wood'])
    # the glazier's kit on the floor beside it: toolbox, putty tin, a rag, a spare pane leaning on the dado
    mb.box((2.0, 21.2, 0), (2.75, 21.6, 0.38), M['wood'])
    L.rod(mb, (2.05, 21.4, 0.38), (2.7, 21.4, 0.38), 0.025, M['iron'], seg=4)
    L.rod(mb, (1.85, 20.85, 0), (1.85, 20.85, 0.16), 0.11, M['zinc'], seg=10)
    L.lumpy(mb, (2.3, 20.95, 0.06), 0.16, M['rag'], 17, seg=8, rings=4, rough=0.3, squash=0.5)
    L._obj(mb, 's07_stool', L.STATE['SET'], hull=0.012)


def build_props9():
    """shot 9: the three panes leaned against the divan / bench behind the coworkers' spot (they put them down to laugh)."""
    out = []
    for k, (x, y, rz) in enumerate(((-3.1, 16.9, 0.25), (-2.85, 17.05, 0.15), (2.6, 16.9, -0.3))):
        o = make_pane("s07_lean_%d" % k, 1.2, 1.5, glints=True)
        o.location = (x, y, 0.74); o.rotation_euler = (math.radians(-12), 0, rz)
        out.append(o)
    return out


# ----------------------------------------------------------------------------- poses
def _hands_side(mirror, left_pt, right_pt, **kw):
    """pin the screen-left / screen-right hands (mirror=True puts arm_r on screen-left)."""
    a, b = ("r", "l") if mirror else ("l", "r")
    d = {a: dict(hand=tuple(left_pt), layer="front", shape="open"), b: dict(hand=tuple(right_pt), layer="front", shape="open")}
    for s in d:
        d[s].update(kw)
    return d


def vin_pose7(g):
    p = dict(cast7.STORY7["vincenzo_stand"][1])
    p.update(mirror=True, yaw=0.42, expr="determined", pitch=-0.12 if g < 649 else -0.05, head_roll=-4 + 2 * math.sin(g * 0.13),
             gaze=(0.85, -0.35 if g < 640 else -0.15), lean=-3, legs="narrow", t=g / 30.0)
    p["blink"] = blink(g, [612, 662, 692])
    p.pop("arm_r", None); p.pop("arm_l", None)
    return p


def walker_pose(name, g, cast):
    ph = (g - G8) / 28.0 + {"vin": 0.0, "cw1": 0.37, "cw2": 0.71}[name]
    if name == "vin":
        base = dict(expr="worried" if g >= 750 else "determined", yaw=0.30, gaze=(0.6, -0.55) if 745 <= g < 772 else (0.8, 0.0),
                    pitch=-0.25 if 745 <= g < 772 else 0.0, head_roll=-3)
        base["blink"] = blink(g, [744, 773])
    elif name == "cw1":
        base = dict(expr="smirk", yaw=0.35, gaze=(0.7, 0.2), pitch=0.15, head_roll=4)
        base["blink"] = blink(g, [718, 760])
    else:
        base = dict(expr="smirk", yaw=0.35, gaze=(0.9, 0.0), pitch=0.05, head_roll=-2)
        base["blink"] = blink(g, [705, 766])
    p = cast7.cycle(cast, ph, "walk", facing=1, base=base, arms="none", speed=0.8)
    p["t"] = g / 30.0
    return p


def cw_pose9(name, g, sid):
    key = "coworkers_laugh" if name == "cw1" else "coworkers_laugh_coworker2"
    if G_TEASE - 6 <= g < G_QUOTE[0] - 4 and sid == 5:
        pass
    p = dict(cast7.STORY7[key][1])
    quote = G_QUOTE[0] - 2 <= g <= G_QUOTE[1]
    if quote:                                         # the jeer: the pointing pose, lip-synced
        p = dict(cast7.STORY7["coworkers_point" if name == "cw1" else "coworkers_point_coworker2"][1])
        p["mouth"] = cast7.talk_mouth(g, 1.0, seed=3.0 if name == "cw1" else 7.0, hold=2) if g >= G_QUOTE[0] else "talk_a"
        p["expr"] = "shouting" if name == "cw2" else "smug"
        p["mouth"] = p["mouth"]
    else:                                             # laughing: the static open laugh (no lip movement), the body shakes
        p["mouth"] = "talk_b"
    shake = math.sin(g * (1.9 if name == "cw1" else 1.6))
    if not quote:
        p["head_roll"] = p.get("head_roll", 0) + 4.0 * shake
        p["lean"] = p.get("lean", 0) - 3.0 * abs(shake)
        p["squash"] = (1.0 + 0.02 * shake, 1.0 - 0.02 * shake)
    p["blink"] = 0
    p["t"] = g / 30.0
    return p


def vin_pose9(g, sid):
    if g < G_GLARE[0]:
        p = dict(cast7.STORY7["vincenzo_mocked"][1])
        if sid == 5 and g < G_TEASE - 8:                 # first a puzzled look at them, then he shrinks
            p.update(pitch=0.10, expr="worried", fx=[], gaze=(-0.8, 0.0), head_roll=2)
        p["blink"] = blink(g, [G_TEASE - 9, 870])
    else:
        a = dict(cast7.STORY7["vincenzo_mocked"][1]); b = dict(cast7.STORY7["vincenzo_glare"][1])
        u = ez((g - G_GLARE[0]) / float(G_GLARE[1] - G_GLARE[0]))
        p = dict(b)
        for k in ("yaw", "pitch", "head_roll", "lean"):
            p[k] = lerp(a.get(k, 0.0), b.get(k, 0.0), u)
        p["gaze"] = (lerp(a["gaze"][0], b["gaze"][0], u), lerp(a["gaze"][1], b["gaze"][1], u))
        sa, sb = a.get("squash", (1.0, 1.0)), b.get("squash", (1.0, 1.0))
        p["squash"] = (lerp(sa[0], sb[0], u), lerp(sa[1], sb[1], u))
        p["legs"] = a.get("legs", "narrow")              # no stance switch (it popped at g 890)
        p["expr"] = "sad" if g < G_GLARE[0] + 2 else "angry"
        p["fx"] = ["blush"]
        if u < 1.0:
            for s in ("arm_r", "arm_l"):
                ha, hb = a[s]["hand"], b[s]["hand"]
                p[s] = dict(b[s], hand=(lerp(ha[0], hb[0], u), lerp(ha[1], hb[1], u)))
        p["blink"] = blink(g, [G_GLARE[0] + 1, 912])     # the sad -> angry change sits behind this blink
        p["head_roll"] = p["head_roll"] + 1.2 * math.sin(g * 0.7) * (1 if g > G_GLARE[1] else 0)   # trembling with the grudge
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=None):
        C.Take.__init__(self, "louvre", "gallery_wide", quality=quality, lens=24.0, name="cam_s07")
        sd = os.path.join(TMP, "sprites")
        S = self.scene
        self.mona_glass = bpy.data.objects.get("mona_glass")
        fr = bpy.data.objects.get("mona_frame")
        bpy.context.view_layer.update()
        ys = [(fr.matrix_world @ Vector(c)).y for c in fr.bound_box]
        self.yF = min(ys) - 0.03                         # the frame's front face
        build_stool()
        self.pane7 = make_pane("s07_pane", *PANE7)
        self.panes = {n: make_pane("s07_carry_" + n, *PANE_C[n]) for n in ("vin", "cw1", "cw2")}
        self.lean = build_props9()
        self.actors["vin"] = C.make_actor("vin", "vincenzo", sd)
        self.actors["cw1"] = C.make_actor("cw1", "coworker1", sd)
        self.actors["cw2"] = C.make_actor("cw2", "coworker2", sd)
        self.stool = bpy.data.objects.get("s07_stool")
        self.rope = split_rope()

    def _vis(self, f, sid):
        def kv(o, hide):
            o.hide_render = hide; o.keyframe_insert("hide_render", frame=f)
            for c in o.children:
                c.hide_render = hide; c.keyframe_insert("hide_render", frame=f)
        kv(self.pane7, sid > 2)
        kv(self.stool, sid > 2)
        kv(self.rope, sid <= 2)
        for o in self.panes.values():
            kv(o, sid not in (3, 4))
        for o in self.lean:
            kv(o, sid < 5)
        if self.mona_glass is not None:
            kv(self.mona_glass, sid <= 2)               # he is fitting it right now
        a = self.actors
        kv(a["cw1"].card, sid <= 2)
        kv(a["cw2"].card, sid <= 2 or sid == 7)
        kv(a["vin"].card, sid in (2, 6))

    def pose(self, shot, gs):
        S = self.scene
        a = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, mona=True)
            self._vis(f, shot)
            if shot <= 2:
                c, rz = pane7_state(g, self.yF)
                key_obj(self.pane7, f, c, rz)
                C.place(a["vin"], f, VIN7, 0.0)
                C.place(a["cw1"], f, (-6, 30, 0)); C.place(a["cw2"], f, (-7, 30, 0))
            elif shot <= 4:
                for n in ("vin", "cw1", "cw2"):
                    C.place(a[n], f, (x8(n, g), WALK_Y, 0.0))
                    key_obj(self.panes[n], f, carried_pane(n, g))
            else:
                for n in ("vin", "cw1", "cw2"):
                    C.place(a[n], f, P9[n], 0.0)
        S.frame_set(bf(shot, gs[0]))
        self.info = {}
        for g in gs:
            f = bf(shot, g)
            S.frame_set(f)
            if shot <= 2:
                o = self.pane7; w, h = PANE7
                pl = pane_point(o, f, w / 2 - 0.04, -0.40)
                pr = pane_point(o, f, w / 2 - 0.30, -h / 2 + 0.04)
                if shot == 2 and g > G_SET:                 # fingertips smooth the edge after it sits
                    s = ez((g - G_SET) / 10.0)
                    pl = pane_point(o, f, w / 2 - 0.04, -0.30 + 0.25 * s)
                hands = {"r": dict(hand=pl, layer="front", shape="open", stretch=1.25), "l": dict(hand=pr, layer="front", shape="open", stretch=1.25)}
                _, info = a["vin"].pose(f, vin_pose7(g), hands=hands, camera=self.cam)
                self.info[g] = {k: round(v["error"], 3) for k, v in info.items()}
                a["cw1"].pose(f, cast7.STORY7["coworkers_walk"][1], camera=self.cam)
                a["cw2"].pose(f, cast7.STORY7["coworkers_walk_coworker2"][1], camera=self.cam)
            elif shot <= 4:
                for n, cast in (("vin", "vincenzo"), ("cw1", "coworker1"), ("cw2", "coworker2")):
                    o = self.panes[n]; w, h = PANE_C[n]
                    lp = pane_point(o, f, -w / 2 + 0.02, 0.0)
                    rp = pane_point(o, f, w / 2 - 0.02, 0.0)
                    hands = {"r": dict(hand=rp, layer="front", shape="fist"), "l": dict(hand=lp, layer="front", shape="fist")}
                    _, info = a[n].pose(f, walker_pose(n, g, cast), hands=hands, camera=self.cam)
                    self.info.setdefault(g, {})[n] = {k: round(v["error"], 3) for k, v in info.items()}
            else:
                a["vin"].pose(f, vin_pose9(g, shot), camera=self.cam)
                a["cw1"].pose(f, cw_pose9("cw1", g, shot), camera=self.cam)
                a["cw2"].pose(f, cw_pose9("cw2", g, shot), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        ppd = {1: 320, 2: 400, 3: 240, 4: 320, 5: 288, 6: 336, 7: 400}[shot]
        self.sprites_for([(a["vin"], ppd), (a["cw1"], ppd), (a["cw2"], ppd)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens,
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), hand_err=self.info.get(g))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
