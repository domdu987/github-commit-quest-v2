#!/usr/bin/env python3
"""shot.py -- film 2 take s10: shot 10 (g 719..798, handles 6 in / 7 out = g 713..805), tower set DAY, spire montage.

Rod in / rod out, alternating with snap reframes between four set-ups on the spire (the same set):
    beat 1  OUT  g 713..739  set-up A (spire_insert, from the south-west): the rod stands in the finial; padre's hand (ink
                             arm out of a black cassock cuff, from frame-right) grabs it and yanks it out (g 722..731, "สั่งถอน")
    beat 2  IN   g 740..771  set-up B (s01's close from the south-east): nico kneels and hammers it back, hits g 746, 756, 767
                             ("ขึ้นไปตอก" 754, "ใหม่" 767); the rod drops one step per hit
    beat 3  OUT  g 772..785  set-up C (low, looking up the spire from the terrace): the hand yanks it out again (g 775..781,
                             "ถอนอีก" 778)
    beat 4  IN   g 786..805  set-up D (wider, from the south): nico hammers again, hits g 790, 801 ("ตอกอีก" 790)
Snaps between set-ups take 4 frames (quint), each set-up drifts; nico is hidden in the OUT beats (he climbed down).
Blender frame = g + 1.
    python3 shot.py probe|stills|final ...   (as s09)
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast2"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast2                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector, Quaternion                # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")
G0, G1, H_IN, H_OUT = 719, 799, 6, 7
RANGE = (G0 - H_IN, G1 + H_OUT - 1)                     # 713 .. 805
BEATS = [("out", 713, 739, "A"), ("in", 740, 771, "B"), ("out", 772, 785, "C"), ("in", 786, 805, "D")]
SNAP = 4                                                # frames of the snap into each set-up (the first beat opens in place)
PULLS = {1: 726, 3: 778}                                # frame the rod leaves the finial
HITS = {2: [746, 756, 767], 4: [790, 801]}
ROD_STEP = 0.15


def beat_of(g):
    for i, (kind, a, b, s) in enumerate(BEATS):
        if a <= g <= b:
            return i + 1, kind, a, b, s
    return (1,) + BEATS[0][0:1] + BEATS[0][1:] if g < BEATS[0][1] else (4,) + BEATS[3]


# ----------------------------------------------------------------------------- nico (from s01)
ROD = Vector(T.ROD_BASE)
HAND_L_W = Vector((0.10, -0.035, 28.05))
STRIKE_W = Vector((0.06, -0.06, 28.68))
YAW_S1 = -48.0
_f = Vector((math.sin(math.radians(YAW_S1)), math.cos(math.radians(YAW_S1)), 0.0))
_r = Vector((_f.y, -_f.x, 0.0))
NICO_FEET = Vector((0.05, 0.0, 26.95)) - _r * 0.52 - _f * 0.45
NH_CAST, NH_POSE = cast2.STORY2["nico_hammer"]
RAISE_HAND = (0.64, -0.08)
RAISE_ANG, STRIKE_ANG = -78.0, -8.0
RAISE_TIP = (RAISE_HAND[0] + 0.36 * math.cos(math.radians(RAISE_ANG)), RAISE_HAND[1] + 0.36 * math.sin(math.radians(RAISE_ANG)))


def hits_all():
    return [h for v in HITS.values() for h in v]


def hammer_u(g):
    u = 0.0
    for s in hits_all():
        if s - 8 <= g <= s + 8:
            if g <= s - 5:
                u = -0.18 * ease((g - (s - 8)) / 3.0, "sine")
            elif g <= s:
                u = -0.18 + 1.18 * ease((g - (s - 5)) / 5.0, "cubic_in")
            else:
                u = 1.0 - ease((g - s - 1) / 7.0, "sine") if g > s + 1 else 1.0
    return u


def rod_state(g):
    """(visible, offset vector, tilt quaternion) of the set rod."""
    i, kind, a, b, s = beat_of(g)
    if kind == "in":
        hs = HITS[i]
        n = sum(1 for h in hs if g >= h)
        return True, Vector((0, 0, ROD_STEP * (len(hs) - n))), Quaternion()
    p = PULLS[i]
    if g < p:
        return True, Vector((0, 0, 0)), Quaternion()
    u = (g - p) / 6.0
    if u > 1.6:
        return False, Vector((0, 0, 0)), Quaternion()
    lift = 1.9 * ease(min(u, 1.0), "cubic_in") + (1.2 * (u - 1.0) if u > 1 else 0)
    side = hand_side(i)
    tilt = Quaternion(Vector((side.y, -side.x, 0)).normalized() if side.length else Vector((1, 0, 0)), math.radians(-25 * clamp(u)))
    return True, Vector((0, 0, lift)) + side * 0.9 * ease(clamp(u - 0.3), "quad_in"), tilt


def shake(g, amp):
    dx = dz = 0.0
    for i, s in enumerate(hits_all()):
        d = g - s
        if 0 <= d <= 6:
            a = amp * math.exp(-0.55 * d)
            dz += a * math.cos(d * 2.2) * (1 if i % 2 == 0 else -1)
            dx += 0.6 * a * math.sin(d * 2.9 + i)
    return dx, dz


def sph(look, dist, yaw, pitch):
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr)))
    return look - d * dist


# ----------------------------------------------------------------------------- set-ups (dist, yaw, pitch, look xyz) start -> end
SETUPS = {
    "A": ((3.1, 47.5, 10.0, 0.05, 0.0, 28.55), (2.8, 44.0, 11.0, 0.08, 0.0, 28.62)),        # spire_insert (from the south-west)
    "B": ((3.55, YAW_S1 - 2.0, -14.0, -0.12, -0.17, 28.30), (3.25, YAW_S1 + 3.0, -12.5, -0.12, -0.17, 28.30)),
    "C": ((2.6, 8.0, 34.0, 0.05, 0.0, 28.75), (2.4, 2.0, 37.0, 0.05, 0.0, 28.85)),           # low, up the spire
    "D": ((4.9, -22.0, -6.0, -0.15, -0.15, 28.20), (4.5, -28.0, -8.0, -0.15, -0.15, 28.22)),
}


def cam_at(g):
    i, kind, a, b, s = beat_of(g)
    s0, s1 = SETUPS[s]
    if i > 1 and g < a + SNAP:                    # snap from the end of the previous set-up
        pa = SETUPS[BEATS[i - 2][3]][1]
        u = ease((g - a + 1) / float(SNAP + 1), "quint")
        k = lerp(pa, s0, u)
    else:
        a2 = a + (SNAP if i > 1 else 0)
        u = clamp((g - a2) / float(max(1, b - a2)))
        k = lerp(s0, s1, 0.82 * ease(u, "sine") + 0.18 * u)
    dist, yaw, pitch, lx, ly, lz = k
    look = Vector((lx, ly, lz))
    if kind == "in":
        dx, dz = shake(g, 0.035 * dist / 3.0)
        look = look + _r * dx + Vector((0, 0, dz))
    return sph(look, dist, yaw, pitch), look


def hand_side(i):
    """screen-right direction (world, horizontal) of the set-up of beat i: the hand comes in from there."""
    s = BEATS[i - 1][3]
    yaw = math.radians(SETUPS[s][0][1])
    f = Vector((math.sin(yaw), math.cos(yaw), 0))
    r = Vector((f.y, -f.x, 0))
    return r if i == 1 else -r                  # beat 1 from the right, beat 3 from the left


def hand_track(g):
    """padre's hand world position (None when off) in the OUT beats: comes in, grips the rod 0.55 D above its base, yanks."""
    i, kind, a, b, s = beat_of(g)
    if kind != "out":
        return None
    p = PULLS[i]
    side = hand_side(i)
    vis, off, q = rod_state(g)
    grip = ROD + Vector((0, 0, 0.55))
    if g < p - 7:
        u = 0.0
    elif g < p:
        u = ease((g - (p - 7)) / 7.0, "cubic_out")
    else:
        u = 1.0
    if g < p:
        return grip + side * 1.6 * (1 - u) + Vector((0, 0, -0.5 * (1 - u)))
    if not vis:
        return None
    return grip + off


# ----------------------------------------------------------------------------- poses
def nico_pose(g):
    p = dict(NH_POSE); p.pop("prop_l", None)
    u = hammer_u(g)
    sq = sum(pulse(g, s - 1, s + 1, s + 6, 1.0) for s in hits_all())
    p["squash"] = (1.0 + 0.03 * sq, 1.0 - 0.035 * sq)
    p["head_roll"] = -6 + 4 * u
    p["lean"] = 8 - 6 * clamp(u)
    p["blink"] = blink(g, [762, 795])
    p["gaze"] = (0.8, -0.2)
    p["prop_r"] = dict(type="hammer", angle=-105.0)
    return p, u


# ----------------------------------------------------------------------------- padre's arm (3D)
def _tube(name, r, mat, coll, seg=14):
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=1.0); bm.to_mesh(me); bm.free()
    for poly in me.polygons:
        poly.use_smooth = True
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); ob.rotation_mode = "QUATERNION"
    return ob


def _sphere(name, r, mat, coll):
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=r); bm.to_mesh(me); bm.free()
    for poly in me.polygons:
        poly.use_smooth = True
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob)
    return ob


def place_tube(ob, a, b):
    a, b = Vector(a), Vector(b); d = b - a
    ob.location = (a + b) / 2
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    ob.scale = (1.0, 1.0, max(d.length, 1e-3))


def emit(name, hexc):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); e = nt.nodes.new("ShaderNodeEmission")
    h = hexc.lstrip("#"); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    e.inputs["Color"].default_value = (c[0], c[1], c[2], 1.0); nt.links.new(e.outputs[0], out.inputs[0])
    return m


class Take(object):
    def __init__(self, quality="preview"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = sc = bpy.context.scene
        self.A = T.build("DAY")
        T.setup_render(sc, quality)
        sc.render.use_persistent_data = False
        sc.cycles.transparent_max_bounces = 12
        sc.frame_start, sc.frame_end = 1, 3000
        T.set_rod(1)
        mk = bpy.data.objects.get("market")
        if mk is not None:
            mk.hide_render = True
        self.rod = T.STATE["rod_objs"][0]
        self.rod.rotation_mode = "QUATERNION"
        self.cam = camrig.make_camera(sc, name="cam_s10")
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.nico = actors.Actor("nico", "nico"); self.nico.build(sprites.DEFAULT_CANVAS["nico"], sd)
        self.nico.head_flip = False; T.no_bounce(self.nico.card)
        coll = bpy.data.collections.new("S10_ARM"); sc.collection.children.link(coll)
        ink, edge, black = emit("S10_ink", "#3a2832"), emit("S10_edge", "#8a7f9a"), emit("S10_cassock", "#24212b")
        self.arm = _tube("p_arm", 0.05, ink, coll); self.arm_e = _tube("p_arm_edge", 0.062, edge, coll)
        self.hand = _sphere("p_hand", 0.11, ink, coll); self.hand_e = _sphere("p_hand_edge", 0.125, edge, coll)
        self.cuff = _tube("p_cuff", 0.12, black, coll, seg=18)
        self.arm_objs = [self.arm, self.arm_e, self.hand, self.hand_e, self.cuff]
        for o in self.arm_objs:
            o.visible_diffuse = False; o.visible_glossy = False
        self.info = {}
        self.anch = {}

    def _vis(self, objs, v, f):
        for o in objs:
            o.hide_render = not v; o.keyframe_insert("hide_render", frame=f)

    def key(self, gs):
        for g in gs:
            f = g + 1
            loc, look = cam_at(g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            vis, off, q = rod_state(g)
            self.rod.location = off; self.rod.rotation_quaternion = q
            self.rod.keyframe_insert("location", frame=f); self.rod.keyframe_insert("rotation_quaternion", frame=f)
            # rotate about the rod base: compensate location so the base pivots
            base = ROD
            self.rod.location = off + (base - q @ base)
            self.rod.keyframe_insert("location", frame=f)
            self.rod.hide_render = not vis; self.rod.keyframe_insert("hide_render", frame=f)
            self.nico.place(f, tuple(NICO_FEET))
            i, kind, a, b, s = beat_of(g)
            h = hand_track(g)
            if h is not None:
                side = hand_side(i)
                cam_back = (loc - look).normalized()
                elbow = h + side * 0.9 + Vector((0, 0, -0.55)) + cam_back * 0.2
                cuff_a = elbow + (elbow - h).normalized() * 0.05
                cuff_b = cuff_a + (elbow - h).normalized() * 2.0
                place_tube(self.arm, h, elbow); place_tube(self.arm_e, h, elbow - cam_back * 0.0)
                self.arm_e.location -= cam_back * 0.02; self.hand_e.location = h - cam_back * 0.02
                self.hand.location = h
                place_tube(self.cuff, cuff_a, cuff_b)
                for o in self.arm_objs:
                    o.keyframe_insert("location", frame=f)
                    if o.rotation_mode == "QUATERNION":
                        o.keyframe_insert("rotation_quaternion", frame=f); o.keyframe_insert("scale", frame=f)
            self._vis(self.arm_objs, h is not None, f)
        for ob in [self.cam, self.rod] + self.arm_objs:
            ad = ob.animation_data
            if ad and ad.action:
                for fc in _fcurves(ad.action):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT" if fc.data_path == "hide_render" else "LINEAR"

    def pose(self, gs):
        self.key(gs)
        cam = self.cam; n = self.nico
        feet = sprites.feet_of("nico", nico_pose(0)[0])
        ins = []
        for g in gs:
            f = g + 1
            i, kind, a, b, s = beat_of(g)
            off_ = kind != "in" or (i > 1 and g < a + SNAP - 1)     # hidden while the snap flies the camera past him
            n.card.hide_render = off_; n.card.keyframe_insert("hide_render", frame=f)
            for o in n.objects()[1:]:
                o.hide_render = off_; o.keyframe_insert("hide_render", frame=f)
            if off_:
                continue
            ins.append(g)
            self.scene.frame_set(f)
            p, u = nico_pose(g)
            k = actors.upper_stretch(n, cam, f, p)
            vis, off, q = rod_state(g)
            hl = actors.world_to_local(n, cam, tuple(HAND_L_W), f, feet=feet)
            st = actors.world_to_local(n, cam, tuple(STRIKE_W + off), f, feet=feet)
            if u >= 0:
                bb = math.sin(math.pi * clamp(u))
                tip = (RAISE_TIP[0] + (st[0] - RAISE_TIP[0]) * u + 0.22 * bb, RAISE_TIP[1] + (st[1] - RAISE_TIP[1]) * u - 0.10 * bb)
                ang = RAISE_ANG + (STRIKE_ANG - RAISE_ANG) * u
            else:
                tip = (RAISE_TIP[0] + 0.25 * u, RAISE_TIP[1] + 0.12 * u); ang = RAISE_ANG + 45.0 * u
            hands = {"l": {"hand": hl, "stretch": 1.3, "bend": -0.5},
                     "r": {"tip": tip, "prop": "hammer", "angle": ang, "stretch": 1.3, "bend": -0.7, "layer": "front"}}
            _, inf = n.pose(f, p, hands=hands, camera=cam, upper_k=k)
            self.info[g] = dict(nico_l=inf["l"]["error"], nico_r=inf["r"]["error"], u=round(u, 3))
        for ob in n.objects():
            ad = ob.animation_data
            if ad and ad.action:
                for fc in _fcurves(ad.action):
                    if fc.data_path == "hide_render":
                        for kp in fc.keyframe_points:
                            kp.interpolation = "CONSTANT"
        fr = [g + 1 for g in ins]
        if fr:
            for f, r in zip(fr, n.render_sprites(512, frames=fr)):
                self.anch[f] = r["anchors"]

    def report(self, g):
        f = g + 1
        self.scene.frame_set(f)
        out = dict(g=g, beat=beat_of(g)[:2])
        if f in self.anch:
            res = self.nico.feet.get(f); hx, hy = self.anch[f]["head"]
            c = actors.local_to_screen(self.nico, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(self.nico, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(self.nico, self.cam, (hx + 0.5, hy), f, res)
            out["nico_head"] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out["rod_tip"] = [round(x, 1) for x in render.world_to_screen(self.cam, T.ROD_TIP, f)[:2]]
        out.update(self.info.get(g, {}))
        return out

    def render(self, gs, out, scale=1.0, samples=12):
        self.scene.cycles.samples = samples
        return render.render_frames([g + 1 for g in gs], out, scale=scale, threads=2, scene=self.scene, camera=self.cam, verbose=False)


def _fcurves(action):
    try:
        return list(action.fcurves)
    except AttributeError:
        out = []
        for layer in action.layers:
            for strip in layer.strips:
                for cb in strip.channelbags:
                    out += list(cb.fcurves)
        return out


def parse(spec):
    a = [int(v) for v in spec.split(":")]
    return list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]
    if cmd == "probe":
        Tk = Take(); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)))
    elif cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take(); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d %.1f s" % (g, st["wall"]), json.dumps(Tk.report(g)), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.json" % g))]
        print("final s10: %d to render" % len(todo), flush=True)
        if todo:
            Tk = Take(quality="final"); Tk.pose(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g); os.replace(st["path"], png)
                rep = Tk.report(g); rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples)
                json.dump(rep, open(png[:-4] + ".json", "w"))
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
