#!/usr/bin/env python3
"""shot.py -- film 8 take s15: shots 15 + 16 (g 1174..1346, in-handle g 1168..1173, out-handle g 1347..1352), summer:
"then summer came; the water in every well in town turned warm; but in the dome with its 2 m thick mud walls the ice was still
full".  Two locations (two processes; final_loop take_key rebuilds), three set-ups:

    id 1  g 1168..1208  shot 15a, bazaar SUMMER, the water merchant's stall: he sits on his takht sweating and fanning himself
                        (sweat + heat), steam curling up from the mouths of his five great water jars.  Slow push + orbit.
    id 2  g 1209..1274  shot 15b, bazaar SUMMER, the square by the well (well_eye): the woman tips the well bucket into a jar --
                        the water steams; the old man fans himself, the boy flaps a hand at his face; steam over the well water.
                        Slow push + orbit.  g 1267..1274 = dissolve handle (rendered in 3D).
    id 3  g 1258..1352  shot 16, inside the yakhchal SUMMER (dome_interior): cool blue, ice blocks stacked high (runtime stacks on
                        the ice), farid on the ice holding up a lantern (warm point light at the drawn lantern), calm smile.  Slow
                        crane down + push.  g 1258..1265 = dissolve handle.
The plan's shot 15 -> 16 transition is a 12-frame DISSOLVE centred on g 1266 (frames 1260..1271 blended in deliver.py).
No quote in shots 15-16: no lip motion (static mouths).  NO depth of field anywhere (client rule).

Blender frame of (id, g) = 1000 * (id - 1) + g + 1.
    python3 shot.py probe|stills 1,2,3 a:b[:step] [<out_dir> scale samples]
    python3 shot.py final 1|2|3 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
import bpy                                               # noqa: E402

D, actors, camrig, cast8 = C.D, C.actors, C.camrig, C.cast8
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0 = C.g_bound(39.14)              # 1174 shot 15
G_DIS = C.g_bound(42.20)           # 1266 shot 16 (dissolve centre)
G_END = C.g_bound(44.89)           # 1347 shot 17
H = 6
DIS = 12                           # dissolve length (frames 1260..1271)
DH = DIS // 2 + 2                  # 8 handle frames each side of the dissolve centre
G_B = C.g_of(40.19) - 3            # 1206.. "น้ำในบ่อทั้งเมือง": cut to the well (just before the phrase)
RANGES = {1: (G0 - H, G_B - 1), 2: (G_B, G_DIS + DH), 3: (G_DIS - DH, G_END + H - 1)}
LOCS = {1: ("bazaar", "merchant_stall"), 2: ("bazaar", "merchant_stall"), 3: ("desert_ice", "dome_interior")}
LIGHT = "SUMMER"
LENS = 22.0


def take_key(shot):
    return LOCS[shot][0]


def aim(loc, az, el, d=30.0):
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


# ----------------------------------------------------------------------------- staging
MERCH = Vector((3.3, 8.1, 0.9))                       # on the takht
JARS = [(1.2, 12.1, 2.0), (1.05, 10.35, 1.7), (1.2, 8.6, 2.0), (1.05, 6.85, 1.7), (1.2, 5.1, 2.0)]   # the merchant's jar mouths
WOMAN = Vector((2.4, 33.4, 0.0))
OLDMAN = Vector((-0.8, 38.0, 0.0))
BOY = Vector((-0.9, 34.0, 0.0))
WELL = (1.5, 37.5, 0.0)
FARID_D = Vector((-4.2, -0.9, -0.8))                  # on the ice top inside the dome

CAMS = {1: (((-0.7, 3.3, 3.7), (3.3, 8.6, 3.3)), ((0.0, 4.4, 3.6), (3.2, 8.8, 3.4))),
        2: (((-3.5, 27.2, 2.55), (3.7, 40.0, 3.6)), ((-2.6, 28.5, 2.5), (4.0, 40.0, 3.5))),
        3: (((-9.4, -1.6, 2.9), (2.0, 1.4, -0.3)), ((-8.4, -0.2, 2.2), (2.4, -0.4, 0.5)))}
LENSES = {1: 22.0, 2: 22.0, 3: 20.0}
PPD = {1: 256, 2: 256, 3: 288}


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    (l0, k0), (l1, k1) = CAMS[shot]
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- poses
M_SWEAT = cast8.STORY8["merchant_sweat"][1]
FAN = {"woman": cast8.STORY8["town_fan"][1], "oldman": cast8.STORY8["town_fan_oldman"][1], "boy": cast8.STORY8["town_fan_boy"][1]}


def fan_angle(g, base=-70.0, ph=0.0):
    return base + 25.0 * math.sin((g + ph) * 2 * math.pi / 8.0)        # one fan beat every 8 frames


def pose_merchant(g):
    p = dict(M_SWEAT)
    p["prop_r"] = dict(type="fan", angle=fan_angle(g))
    p["arm_r"] = dict(M_SWEAT["arm_r"], hand=(0.52 + 0.04 * math.sin(g * 2 * math.pi / 8.0), -0.02))
    p["head_roll"] = -6 + 2.0 * math.sin(g * 0.21)
    p["pitch"] = -0.1 + 0.05 * math.sin(g * 0.17)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [1190])
    p["mouth"] = "talk_a"                                   # panting, static
    return p


def pose_fan(cast, g, ph):
    p = dict(FAN[cast])
    if cast == "boy":
        p["arm_r"] = dict(FAN["boy"]["arm_r"], hand=(0.42 + 0.06 * math.sin((g + ph) * 2 * math.pi / 6.0), -0.05 + 0.05 * math.cos((g + ph) * 2 * math.pi / 6.0)))
    else:
        p["prop_r"] = dict(type="fan", angle=fan_angle(g, -75.0, ph))
    p["head_roll"] = -6 + 2.0 * math.sin((g + ph) * 0.19)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [1225 + int(ph), 1262 + int(ph)])
    p["mouth"] = "talk_a"
    if cast == "oldman":
        p["mirror"] = True                                  # faces the well (screen-right)
    return p


POUR_LEN = 0.62


def pose_woman_pour(g):
    """tips the well bucket into a jar at her right (screen-right): pour 0.3 -> 0.85, stream into the jar, sweat + heat."""
    a, b = RANGES[2]
    tip = u_of(g, a + 4, a + 16)
    p = dict(yaw=0.3, pitch=0.25, expr="worried", mouth="talk_a", sweat=1.0, heat=0.8, head_roll=-4 + 2 * math.sin(g * 0.2), t=g / 30.0,
             arm_r=dict(hand=(0.48, 0.72), bend=-0.3, stretch=1.15), prop_r=dict(type="bucket", scale=1.25), pour=lerp(0.3, 0.86, tip), pour_side=1,
             pour_len=POUR_LEN, bucket_water=1.0 - 0.3 * u_of(g, a + 16, b), arm_l=dict(hand=(0.25, 1.05), bend=-0.2), legs="stand",
             lean=6, blink=blink(g, [1240]))
    return p


def pose_farid_d(g):
    """on the ice with the lantern held up at the right, calm confident smile, looking over the stacked ice, then to us."""
    a, b = RANGES[3]
    to_us = u_of(g, 1300, 1314)
    return dict(yaw=lerp(-0.35, 0.2, to_us), pitch=lerp(-0.15, -0.05, to_us) + 0.04 * math.sin(g * 0.13), expr="happy" if to_us < 0.5 else "smug",
                mouth="smile", head_roll=lerp(4, -5, to_us) + 1.5 * math.sin(g * 0.11), gaze=(lerp(-0.6, 0.15, to_us), lerp(-0.2, 0.0, to_us)),
                arm_r=dict(hand=(0.62, -0.05 + 0.02 * math.sin(g * 0.19)), bend=-0.6, stretch=1.2), prop_r="lantern",
                arm_l=dict(hand=(-0.32, 0.95), bend=0.3), legs="stand", lean=1.2 * math.sin(g * 0.09), blink=blink(g, [1280, 1308, 1338]))


# ----------------------------------------------------------------------------- steam (camera-only scrolling wisp cards)
def _side_fade(mat):
    """multiply the card alpha by sin(pi * frac(2 u)) ** 1.5: the steam fades out at the card's left and right edges (the wisp
    texture runs to the sides; without this the cards showed hard vertical edges)."""
    nt = mat.node_tree; N = nt.nodes.new; L = nt.links.new
    kv = nt.nodes['steam_k']
    st = [l.to_node for l in kv.outputs[0].links][0]             # the alpha x k multiply
    other = [i for i in st.inputs if i.links and i.links[0].from_node != kv][0]
    src = other.links[0].from_socket
    uv = N('ShaderNodeUVMap'); sp = N('ShaderNodeSeparateXYZ'); L(uv.outputs['UV'], sp.inputs[0])
    m2 = N('ShaderNodeMath'); m2.operation = 'MULTIPLY'; m2.inputs[1].default_value = 2.0; L(sp.outputs['X'], m2.inputs[0])
    fr = N('ShaderNodeMath'); fr.operation = 'FRACT'; L(m2.outputs[0], fr.inputs[0])
    mp = N('ShaderNodeMath'); mp.operation = 'MULTIPLY'; mp.inputs[1].default_value = math.pi; L(fr.outputs[0], mp.inputs[0])
    sn = N('ShaderNodeMath'); sn.operation = 'SINE'; L(mp.outputs[0], sn.inputs[0])
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.5; L(sn.outputs[0], pw.inputs[0])
    mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; L(src, mu.inputs[0]); L(pw.outputs[0], mu.inputs[1])
    L(mu.outputs[0], other)


def make_steam(name, mouths, w=0.7, h=2.4, k=0.5, crossed=True):
    S = D.STATE
    mat = D.BK._mat_add("s15_steam_" + name, S['tx']['wisp'], (1.0, 1.0, 1.0), k, node='steam_k', scroll=True, fade=True)
    _side_fade(mat)
    wb = D.MB()
    for i, (x, y, z) in enumerate(mouths):
        u0 = 0.5 * i                                    # each card spans exactly half a texture width (side fade)
        dirs = ((1, 0), (0, 1)) if crossed else ((1, 0),)
        for (dx, dy) in dirs:
            wb.face([(x - dx * w / 2, y - dy * w / 2, z), (x + dx * w / 2, y + dy * w / 2, z), (x + dx * w / 2, y + dy * w / 2, z + h), (x - dx * w / 2, y - dy * w / 2, z + h)],
                    mat, [(u0, 0), (u0 + 0.5, 0), (u0 + 0.5, 1), (u0, 1)])
    ob = D._obj(wb, "s15_steam_" + name, S['SET'], shadow=False)
    return ob, mat


def key_steam(mat, f, g, k=None, speed=1.0):
    nt = mat.node_tree
    sc = nt.nodes['scroll'].inputs['Location']
    sc.default_value = (0.004 * math.sin(g * 0.07), -0.02 * speed * g, 0.0)
    sc.keyframe_insert('default_value', frame=f)
    if k is not None:
        kv = nt.nodes['steam_k'].outputs[0]; kv.default_value = k; kv.keyframe_insert('default_value', frame=f)


# ----------------------------------------------------------------------------- runtime dressing
def dress_bazaar():
    S = D.STATE; M = S['M']; mb = D.MB()
    for k, (x, y, h, r) in enumerate(((5.0, 34.0, 1.1, 0.38), (-1.8, 38.6, 0.9, 0.33), (-4.6, 35.2, 1.0, 0.35), (4.6, 38.6, 1.2, 0.4))):
        D._jar(mb, (x, y, 0.0), M, h=h, r=r, mat=M['terra_l'] if k % 2 else M['terra'], seed=20 + k)
    D._pot(mb, (-2.2, 33.2, 0.0), M, r=0.32)
    D._pot(mb, (5.8, 32.2, 0.0), M, r=0.28, mat=M['brass'])
    ob = D._obj(mb, 's15_dress', S['SET'], hull=0.012); D.no_bounce(ob)
    return ob


def make_pour_jar():
    """the jar the woman pours into (keyed under the stream end each frame)."""
    S = D.STATE; M = S['M']; mb = D.MB()
    D._jar(mb, (0, 0, 0), M, h=0.8, r=0.34, mat=M['terra'], seed=31)
    ob = D._obj(mb, 's15_pour_jar', S['SET'], hull=0.012); D.no_bounce(ob)
    return ob


def dress_dome():
    """ice blocks stacked high on the ice top round farid: columns 3-5 blocks high (0.8 D each) behind and beside him."""
    S = D.STATE; M = S['M']; mb = D.MB(); top = -0.8; bw, bd, bh = 1.5, 0.95, 0.78
    import random
    r = random.Random(5)
    cols = [(-2.4, 1.2, 5), (-0.8, 1.3, 4), (0.8, 1.1, 5), (2.4, 1.3, 3), (-2.6, 2.4, 4), (-1.0, 2.5, 5), (0.6, 2.4, 4),
            (-6.6, 2.0, 3), (-6.4, 3.1, 4), (-5.0, 3.6, 5), (1.8, -3.4, 3), (0.2, -3.6, 4), (-1.4, -3.5, 2)]
    for (x, y, n) in cols:
        for j in range(n):
            dx, dy = r.uniform(-0.06, 0.06), r.uniform(-0.05, 0.05)
            z0 = top + j * (bh + 0.03)
            mb.box((x + dx, y + dy, z0), (x + dx + bw, y + dy + bd, z0 + bh), M['ice_block'], tile=(2, 2))
            if j % 2 == 1:
                mb.box((x + dx + 0.05, y + dy + 0.05, z0 - 0.03), (x + dx + bw - 0.05, y + dy + bd - 0.05, z0), M['straw'])
    ob = D._obj(mb, 's16_ice_stacks', S['SET'], hull=0.012); D.no_bounce(ob)
    return ob


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        loc, preset = LOCS[shot]
        self.loc_key = loc
        C.Take.__init__(self, loc, preset, quality=quality, lens=LENSES[shot], name="cam_s15", light=LIGHT)
        sd = os.path.join(TMP, "sprites_" + loc)
        if loc == "bazaar":
            self.mer = self.actors["mer"] = C.make_actor("mer", "merchant", sd + "_mer")
            self.wom = self.actors["wom"] = C.make_actor("wom", "woman", sd + "_wom", canvas=(-1.5, -4.3125, 2.0, 0.3125))
            self.old = self.actors["old"] = C.make_actor("old", "oldman", sd + "_old")
            self.boy = self.actors["boy"] = C.make_actor("boy", "boy", sd + "_boy")
            dress_bazaar()
            self.jar = make_pour_jar()
            self.st_jars, self.m_jars = make_steam("jars", JARS, w=1.1, h=2.8, k=0.45)
            self.st_well, self.m_well = make_steam("well", [(WELL[0] - 0.6, WELL[1] - 0.4, 0.6), (WELL[0] + 0.5, WELL[1] + 0.3, 0.6), (WELL[0], WELL[1] - 0.1, 0.6)], w=1.4, h=3.2, k=0.8)
            self.st_pour, self.m_pour = make_steam("pour", [(0, 0, 0)], w=0.7, h=2.0, k=0.9)
        else:
            self.far = self.actors["far"] = C.make_actor("far", "farid", sd + "_far")
            dress_dome()
            self.lamp = D.BK._light("s16_lantern", (0, 0, 0), (1.0, 0.66, 0.3), 120.0, radius=0.12, shadow=True)
            hb = D.MB(); D._halo(hb, (0, 0, 0), 0.75, D.STATE['M'], key='halo_big')
            self.halo = D._obj(hb, 's16_halo', D.STATE['SET'], shadow=False)
        self.extra = {}

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENSES[shot])
            self.key_set(f)
            if self.loc_key == "bazaar":
                C.place(self.mer, f, MERCH)
                C.place(self.wom, f, WOMAN); C.place(self.old, f, OLDMAN); C.place(self.boy, f, BOY)
                for a in (self.mer,):
                    a.card.hide_render = shot != 1; a.card.keyframe_insert("hide_render", frame=f)
                for a in (self.wom, self.old, self.boy):
                    a.card.hide_render = shot != 2; a.card.keyframe_insert("hide_render", frame=f)
                key_steam(self.m_jars, f, g, 0.45 if shot == 1 else 0.0)
                key_steam(self.m_well, f, g, 0.8 if shot == 2 else 0.0, speed=0.8)
                for ob in (self.st_jars,):
                    ob.hide_render = shot != 1; ob.keyframe_insert("hide_render", frame=f)
                for ob in (self.st_well, self.st_pour, self.jar):
                    ob.hide_render = shot != 2; ob.keyframe_insert("hide_render", frame=f)
            else:
                C.place(self.far, f, FARID_D)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 1:
                self.mer.pose(f, pose_merchant(g), camera=self.cam)
            elif shot == 2:
                self.wom.pose(f, pose_woman_pour(g), camera=self.cam)
                self.old.pose(f, pose_fan("oldman", g, 3.0), camera=self.cam)
                self.boy.pose(f, pose_fan("boy", g, 1.0), camera=self.cam)
            else:
                self.far.pose(f, pose_farid_d(g), camera=self.cam)
        fs = [bf(shot, g) for g in gs]
        ppd = PPD[shot]
        jobs = [(self.mer, ppd)] if shot == 1 else ([(self.wom, ppd), (self.old, ppd), (self.boy, ppd)] if shot == 2 else [(self.far, ppd)])
        self.sprites_for(jobs, fs)
        for g in gs:
            f = bf(shot, g)
            if shot == 2:                                  # the jar and the stream's steam under the drawn stream end
                an = self.anch.get(("wom", f), {})
                if "pour_end_r" in an:
                    w = actors.local_to_world(self.wom, an["pour_end_r"], f, camera=self.cam)
                    cl = self.cam.matrix_world.to_translation()
                    d = (cl - w); d.z = 0; d = d.normalized() * 0.3
                    base = Vector((w.x + d.x, w.y + d.y, 0.0))
                    self.extra[g] = [round(v, 2) for v in w]
                else:
                    base = Vector((WOMAN.x + 0.9, WOMAN.y - 0.3, 0.0))
                self.jar.location = base; self.jar.keyframe_insert("location", frame=f)
                self.st_pour.location = base + Vector((0, 0, 0.8)); self.st_pour.keyframe_insert("location", frame=f)
                key_steam(self.m_pour, f, g, 0.9 * u_of(g, RANGES[2][0] + 8, RANGES[2][0] + 16), speed=1.3)
            if shot == 3:                                  # the lantern light at the drawn lantern
                an = self.anch.get(("far", f), {})
                tip = an.get("prop_tip_r")
                if tip:
                    w = actors.local_to_world(self.far, tip, f, camera=self.cam)
                    self.lamp.location = w; self.lamp.keyframe_insert("location", frame=f)
                    self.halo.location = w; self.halo.keyframe_insert("location", frame=f)
                    self.extra[g] = [round(v, 2) for v in w]
                fl = 1.0 + 0.08 * math.sin(g * 1.7) + 0.05 * math.sin(g * 3.1)
                self.lamp.data.energy = 120.0 * fl; self.lamp.data.keyframe_insert("energy", frame=f)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), extra=self.extra.get(g))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = None
        for shot in shots:
            if Tk is None or Tk.loc_key != LOCS[shot][0]:
                Tk = Take("preview", shot)
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
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
        C.final_loop(lambda q, s: Take(q, s), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples, take_key=take_key)
