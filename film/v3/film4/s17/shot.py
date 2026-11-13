#!/usr/bin/env python3
"""shot.py -- film 4, render worker 4: takes s17 (shot 17), s18 (shots 18 + 19), s20 (shot 20); pagoda set v2.
The same file sits in film4/s17, film4/s18 and film4/s20 (one engine for the four shots; each folder renders its own take).

    shot 17  g 1522..1599  NIGHT, the quake still running: the pagoda sways like a snake but stands (sway amp 1.1, 0.8 Hz,
                           lanterns / bells swinging, camera shake).  A g 1515..1553 low wide from the path up the whole
                           pagoda (ref a t0121: the jar standing); cut B g 1554..1606 low at the open base: kenta and the
                           townspeople huddled inside, the storeys dancing above them (ref a t0123).  "ส่ายเหมือนงู" g 1546,
                           "แต่ไม่ล้ม" g 1569.
    shot 18  g 1600..1686  NIGHT cutaway: reveal, the pillar swings opposite to the storeys (the "drunk" dance).  A g 1600..1640
                           the whole pagoda cut open, people in the base, slow push; cut B g 1641 ("เต้นหลบ") close on the middle
                           storeys: floors sliding one way, the pillar the other through the floor holes (ref a t0099-t0103).
    shot 19  g 1687..1835  DAY cutaway, diagram look (12-frame dissolve g 1681..1692): pale veil behind the pagoda, soft arrows
                           on every storey (alternate directions, breathing with the sway) and an orange arrow on the pillar foot.
                           A whole pagoda, slow push; cut B g 1731 the middle storeys ("กันเอง" g 1732); cut C g 1767
                           ("ส่วนเสากลาง") the lower pillar as a pendulum; cut D g 1804 top-down onto the swinging foot
                           ("ลูกตุ้ม" g 1808, ref a t0105-t0111).
    shot 20  g 1836..1967  DAWN: the fallen tower, the master on the timber pile; slow push past him to the open base of the
                           pagoda, the pillar still gently swinging (storeys still); focus pulls from the master to the pillar;
                           slow hold to the end (ref a t0125-t0129: the wide closing image).

Blender frame of (shot s, film frame g) = 1000 * (s - 1) + g + 1.  Narration film4/audio/narration_bankky.wav at +0.10 s.

    python3 shot.py stills <shot> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <shot> a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast4"), os.path.join(V3, "stage"), os.path.join(V3, "set3d4"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast4                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import pagoda as G                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing
G17, G18, G19, G20, G_END = 1522, 1600, 1687, 1836, 1968      # round(t*30) of 50.73, 53.32, 56.22, 61.21; N = 1968
H = 7                                                         # handle for a 10-frame dissolve: 10 // 2 + 2
DISS19 = 12                                                   # shot 18 -> 19 dissolve inside take s18: g 1681..1692
D19 = G19 - DISS19 // 2                                       # 1681
RANGES = {17: (G17 - H, G18 + H - 1), 18: (G18 - H, D19 + DISS19 - 1), 19: (D19, G20 + H - 1), 20: (G20 - H, G_END - 1)}
SHOT_RANGE = {17: (G17, G18 - 1), 18: (G18, G19 - 1), 19: (G19, G20 - 1), 20: (G20, G_END - 1)}
PRESET = {17: "NIGHT", 18: "NIGHT", 19: "DAY", 20: "DAWN"}
CUT17 = 1554                     # shot 17 A -> B
CUT18 = g_of(54.60)              # 1641 "กำลังเต้นหลบ"
CUT19 = (1731, g_of(58.81), 1804)   # B "กันเอง" g 1732, C "ส่วนเสากลาง" g 1767, D just before "ลูกตุ้ม" g 1808
G_SNAKE, G_STAND = g_of(51.44), g_of(52.20)          # 1546, 1569
G_LOOK = g_of(62.86)             # 1889 "มองเสากลาง"


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


# ----------------------------------------------------------------------------- sway clocks
def sway_state(shot, g):
    """(amp, phase) of the storeys."""
    if shot in (17, 18):
        amp = 1.1 if shot == 17 else lerp(1.05, 0.85, clamp((g - G18) / 86.0))
        return amp, 2 * math.pi * 0.8 * (g - 1500) / 30.0
    if shot == 19:
        return 1.0, 2 * math.pi * 0.5 * (g - D19) / 30.0 + 0.3
    return 0.0, 0.0


def quake(shot, g):
    if shot == 17:
        return 0.9
    if shot == 18:
        return lerp(0.8, 0.6, clamp((g - G18) / 90.0))
    return 0.0


def pillar20(g):
    """shot 20: storeys still, the pillar still swinging gently (deg)."""
    a = lerp(1.6, 1.1, clamp((g - G20 + H) / 140.0))
    return a * math.sin(2 * math.pi * 0.42 * (g - 1800) / 30.0)


# ----------------------------------------------------------------------------- cameras
def _pk(a, b):
    return tuple(a) + tuple(b)


def _mix(g, ks, share):
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), share)
    return Vector(k[:3]), Vector(k[3:])


def shake(g, amp, seed=0.0):
    s = Vector((math.sin(g * 1.91 + seed) + 0.6 * math.sin(g * 3.37 + 1.3 + seed), 0.5 * math.sin(g * 2.63 + 0.4 + seed),
                math.sin(g * 2.21 + 2.0 + seed) + 0.5 * math.sin(g * 4.1 + seed)))
    return s * amp


V = Vector
CAM17A = ((V((0.35, -26.0, 2.3)), V((0.0, 0.0, 9.9))), (V((0.3, -24.6, 2.45)), V((0.0, 0.0, 9.9))))
CAM17B = ((V((0.45, -11.4, 2.6)), V((0.0, -1.5, 4.3))), (V((0.4, -10.7, 2.55)), V((0.0, -1.5, 4.7))))
CAM18A = ((V((0.6, -25.5, 8.6)), V((0.0, 0.0, 8.9))), (V((0.6, -23.6, 8.4)), V((0.0, 0.0, 8.7))))
CAM18B = ((V((1.4, -10.6, 9.8)), V((0.0, 0.0, 9.4))), (V((1.2, -9.8, 9.6)), V((0.0, 0.0, 9.2))))
CAM19A = ((V((0.6, -26.0, 9.6)), V((0.0, 0.0, 10.4))), (V((0.6, -24.2, 9.4)), V((0.0, 0.0, 10.2))))
CAM19B = ((V((-1.0, -12.0, 10.6)), V((0.0, 0.0, 10.0))), (V((-0.9, -11.2, 10.4)), V((0.0, 0.0, 9.9))))
CAM19C = ((V((1.3, -8.8, 3.2)), V((0.0, 0.0, 4.4))), (V((1.15, -8.2, 3.1)), V((0.0, 0.0, 4.2))))
CAM19D = ((V((0.35, -3.0, 3.25)), V((0.0, -0.15, 1.25))), (V((0.3, -2.75, 3.15)), V((0.0, -0.15, 1.25))))
CAM20 = [(1829, V((16.6, -15.0, 4.6)), V((7.0, -4.0, 4.6)), "sine"),
         (1880, V((10.4, -15.0, 3.7)), V((1.0, -1.0, 3.2)), "sine"),
         (1926, V((0.7, -13.9, 2.75)), V((0.0, 0.0, 2.3)), "sine"),
         (1968, V((0.1, -11.6, 2.55)), V((0.0, 0.0, 2.2)), "hold")]


def _two(g, g0, g1, AB, kind="sine", share=0.3):
    return _mix(g, [(g0, _pk(*AB[0]), kind), (g1 + 1, _pk(*AB[1]), "hold")], share)


def cam(shot, g):
    if shot == 17:
        if g < CUT17:
            loc, look = _two(g, RANGES[17][0], CUT17 - 1, CAM17A)
        else:
            loc, look = _two(g, CUT17, RANGES[17][1], CAM17B, "cubic_out")
        k = 0.05 if g < CUT17 else 0.035
        return loc + shake(g, k), look + shake(g, k * 2.0, 1.7)
    if shot == 18:
        if g < CUT18:
            loc, look = _two(g, RANGES[18][0], CUT18 - 1, CAM18A)
        else:
            loc, look = _two(g, CUT18, RANGES[18][1], CAM18B, "cubic_out")
        return loc + shake(g, 0.025), look + shake(g, 0.05, 0.9)
    if shot == 19:
        b, c, d = CUT19
        if g < b:
            return _two(g, RANGES[19][0], b - 1, CAM19A)
        if g < c:
            return _two(g, b, c - 1, CAM19B, "cubic_out")
        if g < d:
            return _two(g, c, d - 1, CAM19C, "cubic_out")
        return _two(g, d, RANGES[19][1], CAM19D, "cubic_out")
    ks = [(f, _pk(l, k), e) for f, l, k, e in CAM20]
    return _mix(g, ks, 0.2)


# ----------------------------------------------------------------------------- staging
PZ = G.PLAT_Z
HUDDLE = {"farmer": (-0.95, -2.95, PZ), "woman2": (-0.45, -3.55, PZ), "merchant": (0.3, -3.3, PZ), "kenta": (0.95, -3.8, PZ)}
MASTER20 = G.PILE_MARK


def huddle_pose(name, g):
    if name == "kenta":
        p = dict(cast4.STORY4["kenta_worried"][1])
        p["pitch"] = 0.1; p["yaw"] = -0.35
        p["gaze"] = (-0.3, -0.5)                      # looks up at the storeys swaying over him
    else:
        p = dict(cast4.STORY4["town_shelter" + {"merchant": "", "woman2": "_woman2", "farmer": "_farmer"}[name]][1])
    off = {"kenta": 0.0, "merchant": 1.1, "woman2": 2.3, "farmer": 3.7}[name]
    p["head_roll"] = p.get("head_roll", 0) + 3.0 * math.sin(g * 1.7 + off)        # trembling
    p["squash"] = (1.0 + 0.012 * math.sin(g * 2.3 + off), 1.0 - 0.012 * math.sin(g * 2.3 + off))
    p["blink"] = blink(g, [1530 + int(off * 7), 1580 + int(off * 5), 1620 + int(off * 6)]) if name == "kenta" else p.get("blink", 1)
    return p


def master_pose(g):
    p = dict(cast4.STORY4["master_rubble_look"][1])
    u = ease((g - (G_LOOK - 14)) / 16.0, "sine")
    p["pitch"] = lerp(-0.15, 0.1, u)               # quietly looking at the pagoda's base (not at the sky)
    p["yaw"] = -0.55
    p["gaze"] = (-0.6, lerp(0.0, 0.25, u))
    p["mouth"] = "flat"
    p["expr"] = "stunned"
    p["arm_r"] = dict(hand=(0.30, 1.20), bend=0.8)
    p["arm_l"] = dict(hand=(-0.32, 1.18), bend=0.8)
    p["head_roll"] = 3 + 1.5 * math.sin(g * 0.07)
    p["blink"] = blink(g, [1850, 1902, 1950])
    return p


# ----------------------------------------------------------------------------- diagram pieces (shot 19)
def _ensure_coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


def mat_soft(name, hexcol, strength, alpha):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial"); em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*T.hex_lin(hexcol), 1.0); em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); mx.inputs["Fac"].default_value = alpha
    L(tr.outputs["BSDF"], mx.inputs[1]); L(em.outputs["Emission"], mx.inputs[2]); L(mx.outputs["Shader"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


def _arrow_obj(name, coll, body, rim, w=0.16, hw=0.36, hl=0.42, y=0.0):
    """flat arrow in the x-z plane facing -y, from (0,0) to (1,0) along +x (scale x to set length and direction);
    a darker rim slightly behind for an outline."""
    mb = G.MB()
    def arrow(mat, grow, dy):
        L0 = 1.0 - hl
        yy = y + dy
        mb.oface([(-grow, yy, -w - grow), (L0, yy, -w - grow), (L0, yy, w + grow), (-grow, yy, w + grow)], mat, [(0, 0)] * 4, (0, -1, 0))
        tri = [(L0 - grow * 0.5, y + dy, -hw - grow * 1.6), (1.0 + grow * 1.8, y + dy, 0.0), (L0 - grow * 0.5, y + dy, hw + grow * 1.6)]
        mb.oface(tri, mat, [(0, 0)] * 3, (0, -1, 0))
    arrow(rim, 0.06, 0.02)
    arrow(body, 0.0, 0.0)
    ob = mb.obj(name, coll)
    ob.visible_shadow = False
    T.no_bounce(ob)
    return ob


def build_diagram():
    coll = _ensure_coll("S19_DIAGRAM")
    veil = mat_soft("s19_veil", "#f2e8d4", 1.0, 0.8)
    mb = G.MB()
    mb.oface([(-40, 7.5, -3), (40, 7.5, -3), (40, 7.5, 45), (-40, 7.5, 45)], veil, [(0, 0)] * 4, (0, -1, 0))
    mb.oface([(-40, -60, 0.012), (40, -60, 0.012), (40, 7.5, 0.012), (-40, 7.5, 0.012)], veil, [(0, 0)] * 4, (0, 0, 1))
    v = mb.obj("s19_veil", coll); v.visible_shadow = False; T.no_bounce(v)
    body = mat_soft("s19_arrow", "#fffaf0", 1.6, 0.92); rim = mat_soft("s19_arrow_rim", "#3a2f5a", 1.0, 0.85)
    pbody = mat_soft("s19_parrow", "#ffb43c", 2.2, 0.95)
    arrows = []
    for i, (hw, z0, h, ov) in enumerate(G.STOREYS):
        a = _arrow_obj("s19_arrow_%d" % i, coll, body, rim, y=-hw - 0.6)
        a["z"] = z0 + 0.62 * h
        arrows.append(a)
    pa = _arrow_obj("s19_pillar_arrow", coll, pbody, rim, w=0.07, hw=0.16, hl=0.2, y=-0.75)
    pa["z"] = G.FOOT_Z - 0.18
    return [v] + arrows + [pa], arrows, pa


def key_diagram(f, amp, phase, arrows, pa):
    offs, _ = G.sway_offsets(amp, phase)
    s = math.sin(phase)
    for i, a in enumerate(arrows):
        sign = 1 if i % 2 == 0 else -1
        L = 1.6 * s * sign                                          # same size on every storey, alternating
        a.location = (offs[i] + (0.35 if L >= 0 else -0.35), 0.0, a["z"])
        a.scale = (L if abs(L) > 0.02 else 0.02, 1.0, max(0.25, min(1.0, abs(s) * 1.4)))
        a.keyframe_insert("location", frame=f); a.keyframe_insert("scale", frame=f)
        T._show([a], abs(s) > 0.2, f)
    foot = -0.3 * offs[4]
    L = -1.0 * s * (1 if offs[4] >= 0 or s == 0 else 1)
    L = 0.9 * (1 if foot >= 0 else -1) * min(1.0, abs(s) * 1.3)
    pa.location = (foot + (0.5 if L >= 0 else -0.5), 0.0, pa["z"])
    pa.scale = (L if abs(L) > 0.02 else 0.02, 1.0, 1.0)
    pa.keyframe_insert("location", frame=f); pa.keyframe_insert("scale", frame=f)
    T._show([pa], abs(s) > 0.2, f)


# ----------------------------------------------------------------------------- the take (one shot = one build: presets differ)
def _tower_objs():
    st = G.STATE
    names = ("tower", "rubble", "debris", "dust", "settle", "crack", "patch", "collapse", "stump")
    return [o for o in bpy.data.objects if o.name.lower().startswith(names)]


class Take(object):
    def __init__(self, shot, quality="preview", verbose=True):
        t0 = time.time()
        self.shot = shot
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = G.build(PRESET[shot])
        G.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 30000
        self.cam = camrig.make_camera(scene, name="cam_w4")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        os.makedirs(sd, exist_ok=True)
        self.actors = {}
        if shot in (17, 18):
            for n in ("kenta", "merchant", "woman2", "farmer"):
                a = actors.Actor(n, n); a.build(sprites.DEFAULT_CANVAS[n], sd, contact=True); self.actors[n] = a
        if shot == 20:
            a = actors.Actor("master", "master"); a.build(sprites.DEFAULT_CANVAS["master"], sd, contact=True); self.actors["master"] = a
        for a in self.actors.values():
            a.head_flip = shot == 20              # NIGHT moon from the south-west: screen-left; DAWN sun ESE: screen-right in shot 20
            T.no_bounce(a.card)
        # set state
        sh = bpy.data.objects.get("soseki_shade")
        if sh is not None and shot != 20:
            sh.hide_render = True                 # fixed contact shade would show beside the swinging foot
        self.diag = None
        if shot in (17, 18):
            G.set_collapse(1.0, settle=0.0, dust=False)
        elif shot == 19:
            G.set_collapse(0.0)
            for o in _tower_objs():
                o.hide_render = True
            self.diag = build_diagram()
            for n in ("canopy_pelmet", "yoraku_chains"):          # the top-down view of the foot looks past the canopy
                o = bpy.data.objects.get(n)
                if o is not None:
                    o.hide_render = True
        else:
            G.set_collapse(1.0, settle=0.0, dust=False)
        G.set_cutaway(shot in (18, 19))
        self.focus = None
        if shot == 20:
            self.focus = bpy.data.objects.new("focus20", None); scene.collection.objects.link(self.focus)
        self.anch = {}
        if verbose:
            print("w4: shot %d built (%s) in %.1f s" % (shot, PRESET[shot], time.time() - t0), flush=True)

    def pose(self, gs):
        shot = self.shot
        for g in gs:
            f = bf(shot, g)
            loc, look = cam(shot, g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            amp, ph = sway_state(shot, g)
            if shot == 20:
                G.set_sway(0.0, 0.0, frame=f, pillar=False)
                G.set_pillar_swing(pillar20(g), frame=f)
            else:
                G.set_sway(amp, ph, frame=f)
            G.set_quake(quake(shot, g), frame=f)
            if self.diag:
                key_diagram(f, amp, ph, self.diag[1], self.diag[2])
            if shot in (17, 18):
                for n, a in self.actors.items():
                    a.place(f, HUDDLE[n])
            if shot == 20:
                self.actors["master"].place(f, MASTER20)
                u = ease((g - 1872) / 30.0, "sine")
                self.focus.location = Vector(MASTER20) + Vector((0, 0, 2.6)) if u <= 0 else Vector(MASTER20).lerp(Vector((0.0, 0.0, 2.6)), u) + Vector((0, 0, 2.6 * (1 - u)))
                self.focus.keyframe_insert("location", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for n, a in self.actors.items():
                p = master_pose(g) if n == "master" else huddle_pose(n, g)
                a.pose(f, p, camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        ppd = {17: 160, 18: 96, 20: 256}.get(shot, 96)
        for a in self.actors.values():
            if a.card.hide_render:
                continue
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("w4: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def visible(self, g):
        for a in self.actors.values():
            a.set_hidden(self.shot == 19 or (self.shot == 18 and g >= CUT18))

    def report(self, g):
        shot = self.shot
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam(shot, g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={})
        for a in self.actors.values():
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        pts = {"pillar_foot": (0.0, 0.0, G.FOOT_Z), "base": (0.0, -3.0, 2.4), "pagoda_top": (0, 0, G.SORIN_TOP)}
        out["pts"] = {k: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for k, p in pts.items()}
        return out

    def dof(self, g):
        shot = self.shot
        if shot == 17:
            foc, fs = ((0.0, -2.0, 3.0), 5.0) if g < CUT17 else ((0.0, -2.2, 3.0), 3.5)
        elif shot == 18:
            foc, fs = (None, None) if g < CUT18 else ((0.0, 0.0, 9.0), 5.0)
        elif shot == 19:
            foc, fs = {0: (None, None), 1: (None, None), 2: ((0.0, 0.0, 3.0), 4.0), 3: ((0.0, -0.1, G.FOOT_Z), 5.0)}[sum(g >= c for c in CUT19)]
        else:
            foc, fs = self.focus, 5.0
        self.scene.camera = self.cam
        G.setup_dof(self.scene, foc, fs, cam=self.cam)

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.cycles.samples = samples
        res = []
        for g in gs:
            self.visible(g)
            self.dof(g)
            res += render.render_frames([bf(self.shot, g)], out_dir, scale=scale, threads=threads, scene=self.scene,
                                        camera=self.cam, verbose=False)
        return res


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
    shot = int(sys.argv[2])
    gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    if cmd in ("probe", "stills"):
        Tk = Take(shot)
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
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
        if todo:
            Tk = Take(shot, quality="final")
            Tk.pose(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
