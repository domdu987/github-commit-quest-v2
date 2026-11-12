#!/usr/bin/env python3
"""shot.py -- film 2 take s14: shot 14, tower set DAY (the morning after the storm), square_low family of cameras.

    g 1026..1150  padre (smug) holds the pulled-out rod out to nico (padre_smug_hand_rod); nico reaches up and grips it
                  (his hand pinned to the rod, "คืนให้เขา"); padre speaks the quoted line (mouth lip-synced to the narration
                  envelope, g 1071..1155 only); snap reframe onto padre at 35.9 s (g 1080), padre lets go during the snap onto
                  nico at "เก็บไม้จิ้มฟ้า" (g 1112..1120), nico holds the rod alone; the tower behind has no rod (set_rod(0)).
    12-frame dissolves both sides: handles g 1018..1025 and g 1151..1158 (rendered in 3D).

Blender frame = g + 1.
    python3 shot.py probe a:b:step | stills a:b:step <dir> [scale] [samples] | final a:b [scale] [samples]
"""
import math, os, sys, time, json, wave, struct

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast2"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast2                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, G_END, H_IN, H_OUT = 1026, 1151, 8, 8
RANGE = (G0 - H_IN, G_END + H_OUT - 1)           # 1018..1158
G_GIVE = g_of(34.18)                             # 1028 "บาทหลวงยื่น"
G_GRIP = g_of(34.987)                            # 1053 "คืนให้เขา": nico's hand closes on the rod
Q0, Q1 = g_of(35.605), g_of(38.412)              # 1071..1155 the quoted line: mouth moves only here
SNAP1 = (1076, 1084)                             # reframe onto padre (plan 35.9 s)
SNAP2 = (1112, 1120)                             # reframe onto nico + rod, "เก็บไม้จิ้มฟ้า" (g 1115); padre lets go mid-snap
G_LET = 1116
G_LATE = 1146                                    # speed change before the dissolve (plan 38.3)


# ----------------------------------------------------------------------------- lip-sync from the narration envelope
def _envelope():
    w = wave.open(os.path.join(PROJ, "audio", "narration.wav"))
    sr, n = w.getframerate(), w.getnframes()
    data = w.readframes(n)
    sm = struct.unpack("<%dh" % n, data)
    env = {}
    for g in range(RANGE[0], RANGE[1] + 1):
        t = g / 30.0 - 0.10
        a, b = int(max(0, (t - 0.02) * sr)), int(min(n, (t + 0.045) * sr))
        seg = sm[a:b]
        env[g] = math.sqrt(sum(x * x for x in seg) / max(1, len(seg))) / 32768.0 if seg else 0.0
    return env


ENV = _envelope()
_PEAK = max(ENV[g] for g in range(Q0, Q1 + 1)) or 1.0


def mouth(g):
    """lip-sync: new drawing every 2 frames; silent flat, low talk_a, loud talk_b, alternating talk_o for variety."""
    if not (Q0 <= g <= Q1):
        return None
    gg = g - (g - Q0) % 2
    e = ENV[gg] / _PEAK
    if e < 0.12:
        return "flat"
    if e < 0.45:
        return "talk_a" if (gg // 2) % 3 else "talk_o"
    return "talk_b"


# ----------------------------------------------------------------------------- staging
NICO_AT = tuple(float(v) for v in os.environ.get("NICO_AT", "0.3,-11.0,0").split(","))
GRIP_DY = float(os.environ.get("GRIP_DY", "0.30"))           # nico grips the rod this far below padre's fist
PADRE_AT = (1.75, -10.55, 0.0)


def _k(pair):
    return tuple(pair[0]) + tuple(pair[1])


CA = (Vector((0.55, -15.6, 1.25)), Vector((0.80, -8.0, 3.25)))    # two-shot, tower behind (rod gone)
CB = (Vector((0.60, -15.15, 1.28)), Vector((0.85, -8.0, 3.2)))
CC = (Vector((0.66, -14.75, 1.32)), Vector((0.88, -8.0, 3.15)))
CD = (Vector((2.4, -13.9, 1.6)), Vector((2.0, -8.0, 2.95)))      # tighter, onto padre talking
CE = (Vector((2.47, -13.7, 1.62)), Vector((2.03, -8.0, 3.0)))
CF = (Vector((0.15, -14.0, 1.3)), Vector((1.22, -8.0, 3.0)))       # onto nico with the rod
CG = (Vector((0.11, -13.8, 1.3)), Vector((1.19, -8.0, 3.05)))
CH = (Vector((0.08, -13.65, 1.31)), Vector((1.17, -8.0, 3.1)))


def cam(g):
    ks = [(RANGE[0], _k(CA), "sine"), (1048, _k(CB), "sine"), (SNAP1[0], _k(CC), "quint"), (SNAP1[1], _k(CD), "sine"),
          (SNAP2[0], _k(CE), "quint"), (SNAP2[1], _k(CF), "cubic"), (G_LATE, _k(CG), "sine"), (RANGE[1], _k(CH), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.2)
    return Vector(k[:3]), Vector(k[3:])


def padre_pose(g):
    if g < G_LET:
        cast, base = cast2.STORY2["padre_smug_hand_rod"]
        p = dict(base)
        arm = dict(p["arm_r"], hand=(1.06, 0.42), bend=-0.35, stretch=1.3); hx, hy = arm["hand"]   # arm well out: the rod reads on the brick
        lift = 0.10 * ease(clamp((g - RANGE[0]) / 14.0), "sine") - 0.10      # pushes the rod out a little at "ยื่น"
        sw = 1.0 - clamp((g - (G_GRIP - 14)) / 6.0)          # the arm sways only until nico reaches for the rod
        arm["hand"] = (hx + 0.02 * math.sin(g * 0.21) * sw, hy + lift + 0.012 * math.sin(g * 0.37) * sw)
        p["arm_r"] = arm
    else:
        cast, base = cast2.STORY2["padre_smug"]
        p = dict(base)
    p["mirror"] = True
    p["yaw"] = 0.4 if g < G_LET else 0.3
    talk = Q0 <= g <= Q1
    p["head_roll"] = 6 + (3.0 * math.sin(g * 0.29) if talk else 1.2 * math.sin(g * 0.11))
    p["lean"] = -3 + 2.0 * math.sin(g * 0.13)
    p["head_dy"] = 0.012 * math.sin(g * 0.6) if talk else 0.0
    p["blink"] = blink(g, [1036, 1066, 1101, 1137])
    m = mouth(g)
    if m:
        p["mouth"] = m
    else:
        p["mouth"] = "smirk"
    return p


def nico_pose(g, reach_u):
    if g < G_LET:
        cast, base = cast2.STORY2["nico_determined"]
        p = dict(base)
        p["yaw"] = 0.45
        p["arm_r"] = dict(hand=(0.40, 1.02), bend=0.6)
    else:
        cast, base = cast2.STORY2["nico_hold_rod"]
        p = dict(base)
        p["yaw"] = 0.45
    p["expr"] = "determined"
    p["head_roll"] = -4 + 2 * math.sin(g * 0.09)
    p["pitch"] = -0.35                              # looks up at padre
    p["gaze"] = (0.7, -0.5)
    p["blink"] = blink(g, [1040, 1090, 1128])
    p["squash"] = (1.0 + 0.02 * pulse(g, G_GRIP - 2, G_GRIP, G_GRIP + 6, 1.0), 1.0 - 0.02 * pulse(g, G_GRIP - 2, G_GRIP, G_GRIP + 6, 1.0))
    return p


def reach(g):
    """0 = hand at rest, 1 = gripping the rod."""
    return ease(clamp((g - (G_GRIP - 12)) / 12.0), "cubic")


# ----------------------------------------------------------------------------- foreground mass in shade (as s01 shot 2)
def _box(name, lo, hi, mat, coll):
    me = bpy.data.meshes.new(name)
    x0, y0, z0 = lo; x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f); me.update()
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        n = poly.normal
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if abs(n.z) > 0.5:
                uv.data[li].uv = (co.x / 2.0, co.y / 2.0)
            elif abs(n.x) > 0.5:
                uv.data[li].uv = (co.y / 2.0, co.z / 2.0)
            else:
                uv.data[li].uv = (co.x / 2.0, co.z / 2.0)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); T.no_bounce(ob)
    return ob


def build_foreground():
    coll = bpy.data.collections.new("S14_FG"); bpy.context.scene.collection.children.link(coll)
    tex = os.path.join(V3, "set3d2", "tex_tower")
    stone = T.mat_lit("S14_stone", image=os.path.join(tex, "stone.png"), gain=0.0, shade_mul=0.42, form=(0.0, -0.05, 0.22))
    obs = []                                   # (a shade pier was tried: it either leaves the frame or blocks nico in the later set-ups)
    for o in obs:
        o.visible_shadow = False
    return obs


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = T.build("DAY")
        T.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 3000
        T.set_rod(0)                                             # the rod was pulled out: the spire is bare
        mk = bpy.data.objects.get("market")
        if mk is not None:
            mk.hide_render = True
        self.fg = build_foreground()
        self.cam = camrig.make_camera(scene, name="cam_s14")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.nico = actors.Actor("nico", "nico"); self.nico.build(sprites.DEFAULT_CANVAS["nico"], sd, contact=True)
        self.padre = actors.Actor("padre", "padre"); self.padre.build(sprites.DEFAULT_CANVAS["padre"], sd, contact=True)
        for a in (self.nico, self.padre):
            a.head_flip = False                                  # key from screen-left
            T.no_bounce(a.card)
        self.info = {}
        self.anch = {}
        if verbose:
            print("s14: built in %.1f s" % (time.time() - t0), flush=True)

    def pose(self, gs):
        for g in gs:
            f = g + 1
            loc, look = cam(g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            self.nico.place(f, NICO_AT)
            self.padre.place(f, PADRE_AT)
        c = self.cam
        for g in gs:
            f = g + 1
            self.scene.frame_set(f)
            self.padre.pose(f, padre_pose(g), camera=c)
            # the grip point: on padre's rod, 0.42 D above his fist, from the hand-rod drawing of this frame (also after he lets
            # go: nico's hand stays where it gripped, on padre's card of that frame)
            vp = padre_pose(min(g, G_LET - 1))
            vp["mirror"] = True
            an = sprites.puppet.figure("padre", vp, "q")["anchors"]
            hand = an["hand_l"] if an["hand_l"][0] < an["hand_r"][0] else an["hand_r"]
            k = self.padre.upper_k.get(f, 1.0)
            hip = sprites.hip_y("padre", vp)
            hy = hip + (hand[1] + GRIP_DY - hip) * k                       # the drawing above the hip is stretched by upper_k
            grab = actors.local_to_world(self.padre, (hand[0], hy), f)
            u = reach(g) if g < G_LET else 1.0
            np_ = nico_pose(g, u)
            if u <= 0.0:
                self.nico.pose(f, np_, camera=c)
                self.info[g] = dict(reach=0.0)
            else:
                gl = actors.world_to_local(self.nico, c, tuple(grab), f)
                r0 = (0.40, 1.02)
                tgt = (r0[0] + (gl[0] - r0[0]) * u, r0[1] + (gl[1] - r0[1]) * u)
                _, inf = self.nico.pose(f, np_, hands={"r": {"hand": tgt, "stretch": 1.55, "bend": -0.4}}, camera=c)
                self.info[g] = dict(reach=round(u, 3), err=round(inf["r"]["error"], 4))
        fr = [g + 1 for g in gs]
        for a, ppd in ((self.nico, 384), (self.padre, 384)):
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s14: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, g):
        f = g + 1
        self.scene.frame_set(f)
        out = dict(g=g, heads={}, mouth=mouth(g))
        for a in (self.nico, self.padre):
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            cc = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(cc[0], 1), y=round(cc[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out.update(self.info.get(g, {}))
        return out

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.cycles.samples = samples
        return render.render_frames([g + 1 for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
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


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]
    if cmd == "probe":
        Tk = Take(); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)))
    elif cmd == "stills":
        out = sys.argv[3]
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take(); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d  %.1f s  %s" % (g, st["wall"], json.dumps(Tk.report(g))), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw")
        os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: %d to render, %d done" % (len(todo), len(gs) - len(todo)), flush=True)
        if todo:
            Tk = Take(quality="final"); Tk.pose(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("g %d  %.1f s wall  %.1f s cpu" % (g, st["wall"], st["cpu"]), flush=True)
