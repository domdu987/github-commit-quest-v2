#!/usr/bin/env python3
"""shot.py -- film 4 take s06: shot 6 (g 256..353, in-handle g 249..255, out-handle g 354..360), pagoda set DAY.

Narration (sentence 2, captions_bankky.json): "ช่างใหญ่ประจำเมือง สร้างหอที่ตอกทุกข้อต่อแน่น แข็งเหมือนก้อนหิน"
(the town's master builder built a tower with every joint nailed tight, hard as rock).

    6A  g 249..299  10-frame dissolve in from s01 (mixed g 251..260 by the editor).  Low angle on the master on his tower's
                    scaffold (built here at runtime), hammering the big joint of the tower front at z 11.3; strikes g 270, 286;
                    slow push + rise (ref a t0013 / t0045: authority from below).
    6B  g 300..327  hard cut, ECU insert: the iron joint plate; a 3D mallet drives the long nail home, strike 1 g 306 (plan 10.1 s),
                    strike 2 g 321 on "แน่น" (tight): nail flush.  Push in.
    6C  g 328..360  hard cut, low wide from the courtyard ground up the rigid tower with the scaffold and the master; crane up and
                    push on "แข็งเหมือนก้อนหิน" (g 327..356), one more strike g 343.  Out-handle g 354..360 for the dissolve to s07.

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
from mathutils import Vector, Matrix                    # noqa: E402
import pagoda as G                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, GB, GC, G1, H = 256, 300, 328, 354, 7
RANGES = {1: (G0 - H, GB - 1), 2: (GB, GC - 1), 3: (GC, G1 + H - 1)}
STRIKES_A = (270, 286)
STRIKES_B = (306, 321)          # 10.1 s plan insert; "แน่น" g 321
STRIKE_C = 343                  # "ก้อนหิน"


def bf(k, g):
    return 1000 * (k - 1) + int(g) + 1


# ----------------------------------------------------------------------------- staging
DECK_Z = 9.0
MASTER = (12.95, -3.9, DECK_Z)
JX, JY, JZ = G.JOINT                       # (13.4, -2.6, 11.3)
PLATE_Y = JY - 0.035
NAIL = Vector((JX + 0.30, PLATE_Y - 0.03, JZ + 0.02))        # the hero nail head (flush position)
UP_TIP = Vector((MASTER[0] + 0.35, MASTER[1] + 0.2, MASTER[2] + 3.75))   # mallet head wound up over the shoulder


def _pk(a, b):
    return tuple(a) + tuple(b)


def _mix(g, ks, share):
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), share)
    return Vector(k[:3]), Vector(k[3:])


CAM_A0 = (Vector((14.95, -8.05, 9.25)), Vector((13.05, -3.4, 11.75)))
CAM_A1 = (Vector((14.55, -7.45, 9.65)), Vector((13.0, -3.4, 11.9)))
CAM_B0 = (Vector((14.42, -4.10, 11.68)), Vector((JX + 0.22, JY, JZ - 0.04)))
CAM_B1 = (Vector((14.22, -3.80, 11.60)), Vector((JX + 0.26, JY, JZ - 0.02)))
CAM_C0 = (Vector((5.4, -17.8, 1.25)), Vector((13.2, -3.0, 9.6)))
CAM_C1 = (Vector((6.4, -16.0, 1.55)), Vector((13.6, -2.8, 11.9)))


def camA(g):
    a, b = RANGES[1]
    return _mix(g, [(a, _pk(*CAM_A0), "sine"), (b + 1, _pk(*CAM_A1), "hold")], 0.4)


def camB(g):
    a, b = RANGES[2]
    return _mix(g, [(a, _pk(*CAM_B0), "cubic_out"), (b + 1, _pk(*CAM_B1), "hold")], 0.45)


def camC(g):
    a, b = RANGES[3]
    return _mix(g, [(a, _pk(*CAM_C0), "cubic_out"), (b + 1, _pk(*CAM_C1), "hold")], 0.35)


CAMS = {1: camA, 2: camB, 3: camC}


# ----------------------------------------------------------------------------- the master's hammering
def strike_u(g, strikes, period=14):
    """0 = mallet wound up high, 1 = on the nail. Wind-up eases up, the blow is fast (3 frames), rebound."""
    u = 0.15
    for s in strikes:
        if s - 9 <= g < s - 3:
            u = lerp(0.15, 0.0, ease((g - (s - 9)) / 6.0, "sine"))          # lift back
        elif s - 3 <= g <= s:
            u = ease((g - (s - 3)) / 3.0, "quad_in")                          # the blow
        elif s < g <= s + 6:
            u = lerp(1.0, 0.15, ease((g - s) / 6.0, "quad_out"))             # rebound
    return u


def master_pose(g, strikes):
    p = dict(cast4.STORY4["master_plaster"][1])
    p["expr"] = "determined"
    p["mouth"] = "frown"
    u = strike_u(g, strikes)
    up = dict(hand=(0.48, -0.30), bend=-0.9, stretch=1.25)
    hit = dict(hand=(0.86, 0.22), bend=-0.5, stretch=1.25)
    p["arm_r"] = dict(hand=(lerp(up["hand"][0], hit["hand"][0], u), lerp(up["hand"][1], hit["hand"][1], u)),
                      bend=lerp(-0.9, -0.5, u), stretch=1.25)
    p["prop_r"] = dict(type="mallet", angle=lerp(-95, -8, u))
    hitk = max([pulse(g, s, s + 1, s + 5, 1.0) for s in strikes] + [0.0])
    p["lean"] = 4 + 5 * u
    p["head_roll"] = -3 + 4 * hitk
    p["squash"] = (1.0 + 0.02 * hitk, 1.0 - 0.025 * hitk)
    p["yaw"] = 0.55
    p["gaze"] = (0.8, 0.25)
    p["blink"] = blink(g, [262, 292, 336])
    return p


# ----------------------------------------------------------------------------- runtime set pieces
def _coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


def build_scaffold():
    """Bamboo / timber scaffold on the tower's south face: poles, ledgers, two plank decks (z 4.6, 9.0), a guard rail, rope lashings."""
    coll = _coll("S06_SCAF"); C = G.STATE["C"]; M = G.STATE["M"]
    pole = C("#8a6a3a"); plank = C("#b08850"); rope = C("#d8c79a")
    mb = G.MB()
    xs = (10.0, 11.9, 16.2, 18.0); ys = (-4.55, -2.98)
    for x in xs:
        for y in ys:
            mb.frustum((x, y, 0.0), (x, y, 13.4), 0.085, 0.07, pole, seg=7)
    for z in (4.45, 8.85, 12.4):
        for y in ys:
            mb.frustum((10.1, y, z), (17.9, y, z), 0.06, 0.06, pole, seg=6)
        for x in xs:
            mb.frustum((x, -4.75, z - 0.12), (x, -2.85, z - 0.12), 0.055, 0.055, pole, seg=6)
    for zd in (4.6, DECK_Z):
        y = -4.6
        k = 0
        while y < -2.92:
            y1 = min(y + 0.32, -2.92)
            mb.box((10.05 + 0.05 * (k % 2), y, zd - 0.09), (17.95 - 0.07 * (k % 3), y1 - 0.025, zd), plank)
            y = y1; k += 1
    for z in (DECK_Z + 1.0, 4.6 + 1.0):                   # guard rails on the outer side
        mb.frustum((10.1, -4.62, z), (17.9, -4.62, z), 0.045, 0.045, pole, seg=6)
    for x in xs:                                         # lashings
        for z in (4.45, 8.85, 12.4):
            for y in ys:
                mb.frustum((x, y, z - 0.12), (x, y, z + 0.1), 0.11, 0.11, rope, seg=7)
    for x0, x1 in ((10.0, 11.9), (16.2, 18.0)):          # diagonal braces
        mb.frustum((x0, -4.6, 0.4), (x1, -4.6, 4.4), 0.05, 0.05, pole, seg=6)
        mb.frustum((x1, -4.6, 4.7), (x0, -4.6, 8.7), 0.05, 0.05, pole, seg=6)
    ob = mb.obj("s06_scaffold", coll, hull=0.012)
    T.no_bounce(ob)
    # tools on the deck: a nail box and a spare mallet
    mb = G.MB()
    mb.box((15.6, -3.9, DECK_Z), (16.2, -3.4, DECK_Z + 0.3), C("#6a4a2a"))
    mb.box((15.65, -3.85, DECK_Z + 0.3), (16.15, -3.45, DECK_Z + 0.32), M["iron"])
    o2 = mb.obj("s06_deck_props", coll, hull=0.01)
    T.no_bounce(o2)
    return [ob, o2]


def build_joint():
    """The joint detail for the insert: an iron plate across the tower joint with eight driven nails, the hero nail (keyed in z),
    and a 3D mallet on a swing pivot."""
    coll = _coll("S06_JOINT"); C = G.STATE["C"]; M = G.STATE["M"]
    iron = C("#3a3638"); iron_l = C("#5c5658"); head_m = C("#b08a5a"); band = C("#2e2a2c"); handle = C("#c09a62")
    mb = G.MB()
    mb.box((JX - 0.85, PLATE_Y, JZ - 0.32), (JX + 0.85, JY - 0.002, JZ + 0.32), iron)
    for dx in (-0.65, -0.3, 0.05, 0.65):
        for dz in (-0.18, 0.18):
            if abs(dx - 0.30) < 0.1 and abs(dz) < 0.05:
                continue
            c = (JX + dx, PLATE_Y - 0.005, JZ + dz)
            mb.frustum(c, (c[0], c[1] - 0.05, c[2]), 0.075, 0.045, iron_l, seg=4)
    plate = mb.obj("s06_plate", coll, hull=0.008)
    # the hero nail: square shank 0.07, pyramid head; modelled with the head at its origin, shank along +y (into the wall)
    mb = G.MB()
    mb.box((-0.035, 0.0, -0.035), (0.035, 0.75, 0.035), iron_l)
    mb.frustum((0, 0.0, 0), (0, -0.08, 0), 0.14, 0.07, C("#77706e"), seg=4)
    nail = mb.obj("s06_nail", coll, hull=0.006)
    # mallet: pivot at the hand; handle along local +Z to the head at 1.05; head (barrel) along local Y
    piv = bpy.data.objects.new("s06_mallet_pivot", None); coll.objects.link(piv)
    mb = G.MB()
    mb.frustum((0, 0, -0.15), (0, 0, 1.0), 0.05, 0.045, handle, seg=8)
    mb.frustum((0, -0.23, 1.05), (0, 0.23, 1.05), 0.16, 0.16, head_m, seg=14)
    for yy in (-0.2, 0.2):
        mb.frustum((0, yy - 0.025, 1.05), (0, yy + 0.025, 1.05), 0.172, 0.172, band, seg=14)
    mal = mb.obj("s06_mallet", coll, hull=0.012)
    mal.parent = piv
    for o in (plate, nail, mal):
        T.no_bounce(o)
    return plate, nail, piv, mal


# mallet geometry: at the blow the head's face (local y +0.30) touches the nail head (world NAIL + nail out); handle direction
HANDLE_DIR = Vector((-0.50, -0.22, -0.84)).normalized()          # from the head down-right toward the (unseen) hand


def nail_out(g):
    """How far the hero nail head stands out of the plate (D): 0.42 -> 0.17 at strike 1 -> 0 at strike 2."""
    a, b = STRIKES_B
    if g < a:
        return 0.42
    if g < b:
        return 0.17
    return 0.0


def mallet_state(g):
    """(pivot location, rotation matrix) of the mallet for frame g; swing angle 0 = on the nail."""
    out = nail_out(g)                          # at a blow frame the head sits on the just-driven nail
    head_face = NAIL + Vector((0, -out - 0.07, 0))
    head_c = head_face + Vector((0, -0.23, 0))
    hand = head_c + HANDLE_DIR * 1.05
    Z = (head_c - hand).normalized(); Y = Vector((0, 1, 0)); Y = (Y - Z * Y.dot(Z)).normalized(); X = Y.cross(Z)
    base = Matrix((X, Y, Z)).transposed()
    u = strike_u(g, STRIKES_B)
    ang = math.radians(lerp(-78.0, 0.0, u))                    # swing about local X: negative lifts the head away from the wall
    R = base @ Matrix.Rotation(ang, 3, "X")
    hand = hand + Vector((0.05, -0.05, -0.04)) * (1 - u)       # the arm draws back a little in the wind-up
    return hand, R


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
        self.scaf = build_scaffold()
        self.plate, self.nail, self.mpiv, self.mallet = build_joint()
        self.cam = camrig.make_camera(scene, name="cam_s06")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.master = actors.Actor("master", "master"); self.master.build(sprites.DEFAULT_CANVAS["master"], sd, contact=True)
        self.master.head_flip = False                      # DAY key from the south-west: screen-left in 6A and 6C
        T.no_bounce(self.master.card)
        self.all = [self.master]
        self.anch = {}
        if verbose:
            print("s06: built in %.1f s" % (time.time() - t0), flush=True)

    def visible(self, k):
        self.master.set_hidden(k == 2)
        for o in (self.mallet,):
            o.hide_render = k != 2

    def pose(self, k, gs):
        self.visible(k)
        for g in gs:
            f = bf(k, g)
            loc, look = CAMS[k](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.master.place(f, MASTER)
            self.nail.location = NAIL + Vector((0, -nail_out(g), 0))
            self.nail.keyframe_insert("location", frame=f)
            hand, R = mallet_state(g)
            self.mpiv.location = hand; self.mpiv.rotation_euler = R.to_euler("XYZ")
            self.mpiv.keyframe_insert("location", frame=f); self.mpiv.keyframe_insert("rotation_euler", frame=f)
        for o in (self.nail, self.mpiv):
            if o.animation_data and o.animation_data.action:
                for fc in camrig.fcurves_of(o):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"
        if k == 2:
            return
        strikes = STRIKES_A if k == 1 else (STRIKE_C,)
        for g in gs:
            f = bf(k, g)
            self.scene.frame_set(f)
            p = master_pose(g, strikes)
            u = strike_u(g, strikes)
            tip = UP_TIP.lerp(NAIL + Vector((0, -0.12, 0)), u)
            ang = lerp(-95, 15, u)
            self.master.pose(f, p, hands={"r": {"tip": tuple(tip), "prop": "mallet", "angle": ang, "stretch": 1.3, "bend": lerp(-0.9, -0.4, u)}},
                             camera=self.cam)
        fr = [bf(k, g) for g in gs]
        for f, r in zip(fr, self.master.render_sprites(384 if k == 1 else 64, frames=fr)):
            self.anch[("master", f)] = r["anchors"]
            if r.get("clipped"):
                print("s06: WARNING sprite clipped on frame %d" % f, flush=True)

    def report(self, k, g):
        f = bf(k, g)
        self.scene.frame_set(f)
        loc, look = CAMS[k](g)
        v = look - loc
        out = dict(part=k, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={})
        for a in self.all:
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
            tip = self.anch[(a.name, f)].get("prop_tip_r")
            if tip:
                out["mallet_tip"] = [round(x, 1) for x in actors.local_to_screen(a, self.cam, tip, f, res)[:2]]
        pts = {"joint": (JX, JY, JZ), "nail": tuple(NAIL), "tower_top": (14.0, 0.0, 20.8), "pagoda_top": (0, 0, G.SORIN_TOP)}
        out["pts"] = {n: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for n, p in pts.items()}
        return out

    def dof(self, k):
        foc, fs = {1: (self.master.card, 3.5), 2: ((JX + 0.3, JY - 0.2, JZ), 4.0), 3: (None, None)}[k]
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
    main(Take, RANGES, "s06")
