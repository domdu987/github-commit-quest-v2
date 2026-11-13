#!/usr/bin/env python3
"""shot.py -- film 4 take s07: shot 7 (g 354..479, in-handle g 347..353 for the dissolve from s06), pagoda set DAY.

Narration (sentence 3): "ส่วนเขาเป็นแค่ลูกมือที่อายุน้อยที่สุด วางแต่ละชั้นซ้อนกันหลวม ๆ ไม่ตอกเลย"
(he was only the youngest apprentice; he set each storey loosely on the one below, no nails at all).

    7A  g 347..401  dissolve in (mixed g 349..358).  Medium: kenta on a scaffold deck beside the pagoda at the top storey's level,
                    both fists on the hoist chain, paying it out; the top storey hangs on four ropes behind him and comes down
                    1.6 -> 0.45 D; slow orbit (ref a t0017-t0021: circling the object).
    7B  g 402..441  hard cut, insert raking low over the third roof: a bare wooden dowel on the roof ring, the top storey's balcony
                    deck settles over it; touch-down g 417 (plan 13.8 s) with a bump, then a loose wobble -- no nail (ref t0023/25).
    7C  g 442..479  hard cut, medium from the other side: kenta lets go of the chain, ropes gone, the storey sits loose behind him
                    with a small wobble; on "ไม่ตอกเลย" (g 460) he holds up both open hands (no nails, no hammer).  Cut to s08.

Blender frame of (part k, film frame g) = 1000 * (k - 1) + g + 1.   python3 shot.py probe|stills|final <parts> a:b ...
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


G0, GB, GC, G1, H = 354, 402, 442, 480, 7
RANGES = {1: (G0 - H, GB - 1), 2: (GB, GC - 1), 3: (GC, G1 - 1)}
G_TOUCH = 417                    # plan: loose-joint insert at 13.8 s
G_NONAIL = g_of(15.25)           # 460 "ไม่ตอกเลย"
Z4 = G.STOREYS[4][1]             # 14.4: rest height of the top storey


def bf(k, g):
    return 1000 * (k - 1) + int(g) + 1


def _pk(a, b):
    return tuple(a) + tuple(b)


def _mix(g, ks, share):
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), share)
    return Vector(k[:3]), Vector(k[3:])


# ----------------------------------------------------------------------------- the top storey coming down
def storey_state(g):
    """(dz, dx, roll_deg) of the top storey: hangs 1.6 D up at g 347, lowered (eased) to touch at G_TOUCH, a 0.03 bump, then a
    loose wobble (dx, roll) decaying over ~1.5 s; still a faint wobble in 7C."""
    a = RANGES[1][0]
    if g < G_TOUCH:
        u = (g - a) / float(G_TOUCH - a)
        dz = 1.6 * (1 - ease(u, "sine")) if u < 0.9 else 1.6 * (1 - ease(0.9, "sine")) * (1 - (u - 0.9) / 0.1) ** 1.3
        dx = 0.035 * math.sin(2 * math.pi * (g - a) / 38.0) * (1 - u)
        roll = 0.4 * math.sin(2 * math.pi * (g - a) / 46.0 + 1.0) * (1 - u)
        return dz, dx, roll
    t = g - G_TOUCH
    dz = -0.03 * math.exp(-t / 2.5) * math.sin(math.pi * min(t, 4) / 4.0)
    env = 0.055 * math.exp(-t / 28.0) + 0.012
    dx = env * math.sin(2 * math.pi * t / 17.0)
    roll = -0.5 * env / 0.055 * math.sin(2 * math.pi * t / 17.0 + 0.6)
    return dz, dx, roll


# ----------------------------------------------------------------------------- staging
DECK_Z = 13.95
KENTA = (0.1, -6.05, DECK_Z)
PEGS = [(-1.0, -2.08), (1.0, -2.08), (-2.08, -1.0), (2.08, -1.0)]
PEG_TOP = 14.78

CAM_A0 = (Vector((-2.9, -10.2, 14.6)), Vector((0.45, -4.5, 16.75)))
CAM_A1 = (Vector((-1.6, -10.6, 14.75)), Vector((0.35, -4.5, 16.85)))
CAM_B0 = (Vector((-0.55, -3.55, 14.66)), Vector((-1.0, -2.08, 14.62)))
CAM_B1 = (Vector((-0.68, -3.22, 14.64)), Vector((-1.0, -2.08, 14.6)))
CAM_C0 = (Vector((3.75, -10.0, 15.35)), Vector((0.25, -5.2, 16.15)))
CAM_C1 = (Vector((3.25, -9.55, 15.45)), Vector((0.2, -5.2, 16.2)))


def camA(g):
    a, b = RANGES[1]
    return _mix(g, [(a, _pk(*CAM_A0), "sine"), (b + 1, _pk(*CAM_A1), "hold")], 0.4)


def camB(g):
    a, b = RANGES[2]
    return _mix(g, [(a, _pk(*CAM_B0), "cubic_out"), (b + 1, _pk(*CAM_B1), "hold")], 0.45)


def camC(g):
    a, b = RANGES[3]
    return _mix(g, [(a, _pk(*CAM_C0), "cubic_out"), (b + 1, _pk(*CAM_C1), "hold")], 0.4)


CAMS = {1: camA, 2: camB, 3: camC}


def kenta_pose(k, g):
    if k == 1:
        p = dict(cast4.STORY4["kenta_hang_chain"][1])
        pull = 0.5 - 0.5 * math.cos(2 * math.pi * (g - 347) / 22.0)       # hand over hand, paying the chain out
        p["lean"] = -6 - 4 * pull
        p["head_roll"] = -6 - 2 * pull
        p["squash"] = (1.0 + 0.012 * pull, 1.0 - 0.016 * pull)
        arm_r = dict(p["arm_r"]); arm_l = dict(p["arm_l"])
        arm_r["hand"] = (0.64, -0.16 + 0.12 * pull); arm_l["hand"] = (0.64, 0.18 + 0.10 * pull)
        p["arm_r"], p["arm_l"] = arm_r, arm_l
        p["expr"] = "determined"; p["mouth"] = "clench"
        p["gaze"] = (0.5, -0.9)
        p["blink"] = blink(g, [372, 395])
        return p
    p = dict(cast4.STORY4["kenta_determined"][1])
    p["mouth"] = "frown"
    u = ease((g - (G_NONAIL - 6)) / 6.0, "back_out") if g >= G_NONAIL - 6 else 0.0
    shake = math.sin(2 * math.pi * (g - G_NONAIL) / 9.0) * clamp((g - G_NONAIL + 2) / 4.0) * clamp((G_NONAIL + 16 - g) / 4.0)
    rest_r = (0.40, 0.98)
    p["arm_r"] = dict(hand=(lerp(rest_r[0], 0.78, u), lerp(rest_r[1], 0.05, u)), bend=lerp(0.6, -0.6, u), shape="open" if u > 0.3 else "fist", stretch=1.25)
    p["arm_l"] = "akimbo" if u < 0.3 else dict(hand=(lerp(-0.2, -0.78, u), lerp(0.7, 0.05, u)), bend=0.6, shape="open", stretch=1.25)
    p["yaw"] = 0.15 + 0.18 * shake
    p["gaze"] = (0.1 + 0.3 * shake, 0.0)
    p["head_roll"] = -3 + 3 * shake
    p["expr"] = "smirk" if g >= G_NONAIL + 8 else "determined"
    if g >= G_NONAIL + 8:
        p["mouth"] = "smirk"
    p["lean"] = 2 - 3 * u
    p["blink"] = blink(g, [446, G_NONAIL + 6])
    return p


# ----------------------------------------------------------------------------- runtime set pieces
def _coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


def build_pieces():
    coll = _coll("S07_PIECES"); C = G.STATE["C"]; M = G.STATE["M"]
    bpy.context.view_layer.update()
    pole = C("#8a6a3a"); plank = C("#b08850"); rope = C("#d8c79a"); peg = C("#e0b878"); hole = C("#2a1c18")
    # scaffold on the south side, deck at the top storey's level
    mb = G.MB()
    xs = (-3.6, -2.1, 2.1, 3.6); ys = (-6.75, -5.45)
    for x in xs:
        for y in ys:
            mb.frustum((x, y, 0.0), (x, y, 17.4), 0.085, 0.07, pole, seg=7)
    for z in (5.0, 9.6, DECK_Z - 0.15):
        for y in ys:
            mb.frustum((-3.8, y, z), (3.8, y, z), 0.06, 0.06, pole, seg=6)
        for x in xs:
            mb.frustum((x, -6.95, z - 0.12), (x, -5.3, z - 0.12), 0.055, 0.055, pole, seg=6)
            for y in ys:
                mb.frustum((x, y, z - 0.25), (x, y, z + 0.1), 0.11, 0.11, rope, seg=7)
    y = -6.8; k = 0
    while y < -5.42:
        y1 = min(y + 0.33, -5.42)
        mb.box((-3.85 + 0.06 * (k % 2), y, DECK_Z - 0.09), (3.85 - 0.05 * (k % 3), y1 - 0.025, DECK_Z), plank)
        y = y1; k += 1
    mb.frustum((-3.8, -6.82, DECK_Z + 1.0), (3.8, -6.82, DECK_Z + 1.0), 0.045, 0.045, pole, seg=6)
    sc = mb.obj("s07_scaffold", coll, hull=0.012)
    # dowel pegs on the third storey's roof ring (no nails: the top storey just sits over them)
    mb = G.MB()
    for (x, y) in PEGS:
        mb.frustum((x, y, 14.18), (x, y, PEG_TOP), 0.11, 0.1, peg, seg=12)
        mb.frustum((x, y, 14.18), (x, y, 14.36), 0.16, 0.13, C("#8a6440"), seg=10)
    pg = mb.obj("s07_pegs", coll, hull=0.006)
    pg.parent = G.STATE["storeys"][3]; pg.matrix_parent_inverse = G.STATE["storeys"][3].matrix_world.inverted()
    # holes under the top storey's deck + four hoist ropes from its eave corners up out of frame
    mb = G.MB()
    for (x, y) in PEGS:
        mb.frustum((x, y, Z4 - 0.075), (x, y, Z4 - 0.09), 0.14, 0.14, hole, seg=12)
    ho = mb.obj("s07_holes", coll)
    s4 = G.STATE["storeys"][4]
    ho.parent = s4; ho.matrix_parent_inverse = s4.matrix_world.inverted()
    mb = G.MB()
    for sx in (-1, 1):
        for sy in (-1, 1):
            mb.frustum((sx * 3.55, sy * 3.55, 16.7), (sx * 2.2, sy * 2.2, 60.0), 0.045, 0.045, rope, seg=6)
    ro = mb.obj("s07_ropes", coll)
    ro.parent = s4; ro.matrix_parent_inverse = s4.matrix_world.inverted()
    for o in (sc, pg, ho, ro):
        T.no_bounce(o)
    return dict(scaffold=sc, pegs=pg, holes=ho, ropes=ro)


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = G.build("DAY")
        G.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 4000
        self.P = build_pieces()
        self.cam = camrig.make_camera(scene, name="cam_s07")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.kenta = actors.Actor("kenta", "kenta"); self.kenta.build((-1.9375, -5.8125, 2.0625, 0.25), sd, contact=True)
        self.kenta.head_flip = False
        T.no_bounce(self.kenta.card)
        self.all = [self.kenta]
        self.anch = {}
        if verbose:
            print("s07: built in %.1f s" % (time.time() - t0), flush=True)

    def visible(self, k):
        self.kenta.set_hidden(k == 2)
        self.P["ropes"].hide_render = k == 3

    def pose(self, k, gs):
        self.visible(k)
        s4 = G.STATE["storeys"][4]
        for g in gs:
            f = bf(k, g)
            loc, look = CAMS[k](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.kenta.place(f, KENTA)
            dz, dx, roll = storey_state(g)
            s4.location = (dx, 0.0, Z4 + dz); s4.rotation_euler = (math.radians(roll * 0.5), math.radians(roll), 0.0)
            s4.keyframe_insert("location", frame=f); s4.keyframe_insert("rotation_euler", frame=f)
        if k == 2:
            return
        for g in gs:
            f = bf(k, g)
            self.scene.frame_set(f)
            self.kenta.pose(f, kenta_pose(k, g), camera=self.cam)
        fr = [bf(k, g) for g in gs]
        for f, r in zip(fr, self.kenta.render_sprites(384, frames=fr)):
            self.anch[("kenta", f)] = r["anchors"]
            if r.get("clipped"):
                print("s07: WARNING sprite clipped on frame %d" % f, flush=True)

    def report(self, k, g):
        f = bf(k, g)
        self.scene.frame_set(f)
        loc, look = CAMS[k](g)
        v = look - loc
        out = dict(part=k, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={}, storey=[round(x, 3) for x in storey_state(g)])
        for a in self.all:
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        pts = {"peg": (-1.0, -2.08, PEG_TOP), "storey4_base": (0, -2.25, Z4), "pagoda_top": (0, 0, G.SORIN_TOP)}
        out["pts"] = {n: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for n, p in pts.items()}
        return out

    def dof(self, k):
        foc, fs = {1: (self.kenta.card, 3.5), 2: ((-1.0, -2.08, 14.6), 4.5), 3: (self.kenta.card, 3.5)}[k]
        self.scene.camera = self.cam
        G.setup_dof(self.scene, foc, fs, cam=self.cam)
        return foc, fs

    def render(self, k, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(k)
        self.dof(k)
        self.scene.cycles.samples = samples
        return render.render_frames([bf(k, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
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


def main(Take, RANGES, tag):
    cmd = sys.argv[1]
    parts = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take()
        for k in parts:
            gs = [g for g in parse(sys.argv[3]) if RANGES[k][0] <= g <= RANGES[k][1]]
            if not gs:
                gs = [RANGES[k][0], (RANGES[k][0] + RANGES[k][1]) // 2, RANGES[k][1]]
            Tk.pose(k, gs)
            for g in gs:
                print(json.dumps(Tk.report(k, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(k, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "p%d_g_%04d.png" % (k, g)))
                    print("part %d g %d  %.1f s wall %.1f cpu" % (k, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        Tk = None
        for k in parts:
            gs = [g for g in parse(sys.argv[3]) if RANGES[k][0] <= g <= RANGES[k][1]]
            out = os.path.join(HERE, "raw", "p%d" % k)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: part %d, %d to render, %d done" % (k, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if Tk is None:
                Tk = Take(quality="final")
            Tk.pose(k, todo)
            for g in todo:
                st = Tk.render(k, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(k, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("%s part %d g %d  %.1f s wall  %.1f s cpu" % (tag, k, g, st["wall"], st["cpu"]), flush=True)


if __name__ == "__main__":
    main(Take, RANGES, "s07")
