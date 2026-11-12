#!/usr/bin/env python3
"""shot.py -- film 2 take s04: shots 4 and 5, tower set NIGHT_STORM.

    shot 4  g 211..304  whip pan in (braking, g 204..219; in-handle g 204..210 still panning fast), bell chamber at eye level from
                        outside the south arch: padre (near), baker (right) and woman (far left) haul on their bell ropes, the bell
                        swings hard, lightning flashes through the north arch.  Snap punch-in on padre at "ต้องตีระฆังรัว ๆ"
                        (g 274), a drift between.
    shot 5  g 305..358  10-frame dissolve (g 300..309, mixed here): the town at night from the town_wide side, the campanile
                        swinging its bell, forked bolts in the sky over the hills to the north-west (away from town), flashes.
                        Out-handle g 359..366 (12-frame dissolve into shot 6).

Ropes: the actors carry no drawn rope; each ringer gets a 3D rope (and a striped sally) hanging from the chamber ceiling 0.1 D behind
his card, keyed up and down with the pull, and both hands are pinned on it (registration from actors.world_to_local).
Blender frame of (shot s, film frame g) = 1000 * (s - 3) + g + 1.

    python3 shot.py probe 4|5 a:b:step
    python3 shot.py stills 4|5 a:b:step out_dir [scale] [samples]
    python3 shot.py final 4|5 a:b [scale] [samples]          (resumable, raw/s<shot>/g_%04d.png + .json)
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast2"), os.path.join(V3, "stage"), os.path.join(V3, "set3d2"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast2                                            # noqa: E402  (first: registers nico, padre, extras)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):                     # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing
G_S4, G_S5, G_S6 = 211, 305, 359          # s01 delivered g1 = 211; 10.18 s -> 305; 11.98 s -> 359
H_IN, H_OUT = 7, 8                         # whip in-handle (still panning), out-handle for the 12-frame dissolve into shot 6
DISS = 10                                  # shot 4 -> 5 dissolve, frames G_S5-5 .. G_S5+4
HD = DISS // 2 + 2
RANGES = {4: (G_S4 - H_IN, G_S5 + HD - 1), 5: (G_S5 - HD, G_S6 + H_OUT - 1)}
WHIP_END = G_S4 + 9                        # 220: the whip has braked
G_RUA = g_of(9.047)                        # 274 "ต้องตีระฆังรัว ๆ"
PUNCH = (G_RUA - 6, G_RUA + 2)             # 268..276
G_LAI = g_of(10.486)                       # 318 "ระฆังจะไล่"
G_PHA = g_of(11.217)                       # 340 "ฟ้าผ่าไปเอง"
# lightning (shot 4: through the north arch + the flash light; shot 5: bolts in the sky over the hills)
FLASH4 = [(232, [1.0, 0.35, 0.8, 0.0]), (258, [0.7, 0.0]), (281, [1.2, 0.5, 1.0, 0.3, 0.0])]
FLASH5 = [(312, [1.1, 0.4, 0.9, 0.0]), (G_PHA - 1, [1.3, 0.6, 1.2, 0.5, 0.0]), (352, [0.8, 0.0])]
BOLT_FRAMES = 3                            # a bolt is visible on the first frames of each flash
PERIOD = 40                                # bell full swing cycle (frames)


def bf(shot, g):
    return 1000 * (shot - 3) + int(g) + 1


def flash_at(g, table):
    for g0, seq in table:
        if g0 <= g < g0 + len(seq):
            return seq[g - g0], g - g0 < BOLT_FRAMES and seq[g - g0] > 0.6
    return 0.0, False


BOLT_SHIFT = {4: [(0, (0.0, 0.0, 0.0))], 5: [(0, (-20.0, 6.0, 6.0)), (G_PHA - 3, (38.0, 4.0, 3.0)), (350, (-26.0, 0.0, 8.0))]}


def bolt_shift(g, shot):
    v = BOLT_SHIFT[shot][0][1]
    for g0, s in BOLT_SHIFT[shot]:
        if g >= g0:
            v = s
    return v


def bell_angle(g, amp=26.0):
    return amp * math.sin(2 * math.pi * (g - 200) / PERIOD)


def pull_u(g, phase):
    """0 = hands up, 1 = rope hauled down; one haul per half bell cycle, fast down, slower up."""
    x = ((g - 200) / (PERIOD / 2.0) + phase) % 1.0
    if x < 0.35:
        return ease(x / 0.35, "cubic_out")
    return 1.0 - ease((x - 0.35) / 0.65, "sine")


# ----------------------------------------------------------------------------- staging (shot 4)
CH = T.Z_CH
RINGERS = {   # name: (cast, story pose, feet, upper hand side, phase)
    "padre": ("padre", "padre_ring", (-0.55, -0.85, CH), "r", 0.0),
    "baker": ("baker", "extras_ring", (1.2, -0.65, CH), "r", 0.45),
    "woman": ("woman", "extras_ring_woman", (0.6, 1.25, CH), "l", 0.2),
}
HAUL = 0.36                                # rope travel per haul (D)
ROPE_TOP = T.Z_CORN + 1.2                  # rope runs up into the ceiling
ROPE_BACK = 0.10                           # rope stands this far behind the card (the hands are drawn over it)


def sph(look, dist, yaw, pitch):
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr)))
    return look - d * dist


CAM4_A = (Vector((0.55, -4.25, CH + 2.35)), Vector((-0.15, 1.9, CH + 2.85)))
CAM4_B = (Vector((0.30, -3.95, CH + 2.45)), Vector((-0.05, 1.9, CH + 2.95)))
PADRE_HEAD = Vector((-0.55, -0.85, CH + 2.95))
PD, PX, PZ, LX, LZ = 2.6, 0.3, 0.0, 0.1, -0.3


def rot_about(loc, look, yaw_deg):
    """turn the look point about the camera position (a pan) by yaw_deg (positive = to the right)."""
    v = look - loc
    a = -math.radians(yaw_deg)
    c, s = math.cos(a), math.sin(a)
    return loc + Vector((v.x * c - v.y * s, v.x * s + v.y * c, v.z))


def whip_pan(g):
    """degrees still to go (pan comes from the left: positive = still turned left of the target), braking into the pose."""
    if g >= WHIP_END:
        return 0.0
    u = (WHIP_END - g) / float(WHIP_END - (G_S4 - H_IN))      # 1 at the first handle frame, 0 at WHIP_END
    return -75.0 * u ** 2.2


def cam4(g):
    head = PADRE_HEAD
    pc = head + (CAM4_B[0] - head).normalized() * PD + Vector((PX, 0.0, PZ))
    c = (pc, head + Vector((LX, 0.6, LZ)))
    d = (pc + Vector((0.12, 0.10, 0.05)), head + Vector((LX + 0.08, 0.6, LZ + 0.05)))
    ks = [(G_S4 - H_IN, tuple(CAM4_A[0]) + tuple(CAM4_A[1]), "sine"),
          (PUNCH[0], tuple(CAM4_B[0]) + tuple(CAM4_B[1]), "quint"),
          (PUNCH[1], tuple(c[0]) + tuple(c[1]), "sine"),
          (RANGES[4][1], tuple(d[0]) + tuple(d[1]), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.3)
    loc, look = Vector(k[:3]), Vector(k[3:])
    # each haul shakes the tower a little
    sh = 0.012 * math.sin(2 * math.pi * (g - 200) / (PERIOD / 2.0)) + 0.006 * math.sin(g * 1.7)
    look = look + Vector((0, 0, sh))
    return loc, rot_about(loc, look, whip_pan(g))


CAM5_A = (Vector((-15.5, -36.5, 6.5)), Vector((0.0, 0.0, 15.2)))
CAM5_B = (Vector((-13.2, -32.0, 7.9)), Vector((0.2, 0.0, 15.6)))


def cam5(g):
    g0, g1 = RANGES[5]
    mid = (CAM5_A[0].lerp(CAM5_B[0], 0.45), CAM5_A[1].lerp(CAM5_B[1], 0.5) + Vector((0, 0, 0.1)))
    ks = [(g0, tuple(CAM5_A[0]) + tuple(CAM5_A[1]), "cubic"),
          (G_PHA, tuple(mid[0]) + tuple(mid[1]), "cubic"),
          (g1, tuple(CAM5_B[0]) + tuple(CAM5_B[1]), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), 0.2)
    loc, look = Vector(k[:3]), Vector(k[3:])
    f, _ = flash_at(g, FLASH5)                   # a thunder jolt on the strongest flashes
    look = look + Vector((0.0, 0.0, 0.05 * f * math.sin(g * 2.3)))
    return loc, look


CAMS = {4: cam4, 5: cam5}


# ----------------------------------------------------------------------------- ringer poses
def ringer_pose(name, g):
    cast, story, feet, up, ph = RINGERS[name]
    p = dict(cast2.STORY2[story][1])
    p.pop("prop_l", None); p.pop("prop_r", None)
    u = pull_u(g, ph)
    s = 1 if up == "r" else -1
    p["lean"] = (p.get("lean", 0) * 1.0) + s * 7.0 * u
    p["squash"] = (1.0 + 0.04 * u, 1.0 - 0.05 * u)
    p["head_roll"] = p.get("head_roll", 0) + s * 4.0 * u + 1.5 * math.sin(g * 0.21 + ph * 5)
    p["head_dy"] = 0.04 * u
    if name == "padre":
        p["expr"] = "determined"; p["mouth"] = "clench"
        p["blink"] = blink(g, [226, 263, 296])
    elif name == "baker":
        p["blink"] = blink(g, [239, 284])
    else:
        p["blink"] = blink(g, [221, 270])
    return p, u


def rest_hands(name):
    """puppet-local hand points of the story pose (upper, lower)."""
    cast, story, feet, up, ph = RINGERS[name]
    p = cast2.STORY2[story][1]
    lo = "l" if up == "r" else "r"
    return p["arm_" + up]["hand"], p["arm_" + lo]["hand"], up, lo


# ----------------------------------------------------------------------------- rope objects
def rope_mats():
    m = T.mat_lit("S04_rope", color="#cfa86a", shade_mul=0.9)
    r = T.mat_lit("S04_sally_r", color="#c8322a", shade_mul=0.8)
    w = T.mat_lit("S04_sally_w", color="#f0e2c0", shade_mul=0.6)
    return m, r, w


def make_rope(name, x, y, z_low, coll, mats, z_top=ROPE_TOP, sally=None):
    """a rope from z_top down to z_low at (x, y); its origin is at (x, y, 0) so it can be keyed up and down by location z.
    sally = (z0, z1): striped woollen grip."""
    m, r, w = mats
    mb = T.MB()
    mb.frustum((0, 0, z_top), (0, 0, z_low), 0.045, 0.042, m, seg=8)
    if sally:
        n = int(round((sally[1] - sally[0]) / 0.1))
        for k in range(n):
            mb.frustum((0, 0, sally[0] + k * 0.1), (0, 0, sally[0] + k * 0.1 + 0.1), 0.07, 0.07, r if k % 2 else w, seg=8)
    ob = mb.obj(name, coll, hull=0.008)
    ob.location = (x, y, 0.0)
    T.no_bounce(ob)
    return ob


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = T.build("NIGHT_STORM")
        T.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 4000
        T.set_rod(0)
        mk = bpy.data.objects.get("market")             # director (s01): striped awning reads as a flag -> hidden
        if mk is not None:
            mk.hide_render = True
        self.cam = camrig.make_camera(scene, name="cam_s04")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(TMP, "sprites")
        self.act = {}
        for n, (cast, story, feet, up, ph) in RINGERS.items():
            a = actors.Actor(n, cast)
            a.build(sprites.DEFAULT_CANVAS[cast], sd, contact=True)
            a.head_flip = False                        # moon key from screen-left
            T.no_bounce(a.card)
            self.act[n] = a
        self.coll = bpy.data.collections.new("S04_ROPES"); scene.collection.children.link(self.coll)
        self.mats = rope_mats()
        self.ropes = {}
        self.rope_xy = {}
        self.hand_z = {}
        self.keyed = set()
        self.info = {}
        self.anch = {}
        if verbose:
            print("s04: built in %.1f s" % (time.time() - t0), flush=True)

    # rope positions are fixed for the shot: found once from the rest pose and the first camera of shot 4
    def place_ropes(self):
        if self.ropes:
            return
        g = G_S4 + 20
        f = bf(4, g)
        loc, look = cam4(g)
        camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
        for n, a in self.act.items():
            a.place(f, RINGERS[n][2])
        self.scene.frame_set(f)
        for n, a in self.act.items():
            cast, story, feet, up, ph = RINGERS[n]
            p = dict(cast2.STORY2[story][1]); p.pop("prop_l", None); p.pop("prop_r", None)
            a.pose(f, p, camera=self.cam)
            fp = sprites.feet_of(cast, p)
            hu, hl, _, _ = rest_hands(n)
            wu = actors.local_to_world(a, hu, f, feet=fp, camera=self.cam)
            wl = actors.local_to_world(a, hl, f, feet=fp, camera=self.cam)
            c = self.cam.matrix_world.to_translation()
            back = (Vector((wu.x, wu.y, 0)) - Vector((c.x, c.y, 0))).normalized() * ROPE_BACK
            x, y = wu.x + back.x, wu.y + back.y
            self.rope_xy[n] = (x, y)
            self.hand_z[n] = (wu.z, wl.z)
            self.ropes[n] = make_rope("rope_" + n, x, y, wl.z - 0.75, self.coll, self.mats, sally=(wl.z - 0.25, wu.z + 0.25))

    def key(self, shot, gs):
        if shot == 4:
            self.place_ropes()
        for g in gs:
            f = bf(shot, g)
            loc, look = CAMS[shot](g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            T.set_bell(bell_angle(g), frame=f, interp="LINEAR")
            fs, bolt = flash_at(g, FLASH4 if shot == 4 else FLASH5)
            T.flash(fs, frame=f)
            T.set_bolt(bolt, frame=f, target="sky")
            for ob in T.STATE["bolts"]["bolt_sky"]:             # move the sky bolt per flash: far over the hills, never near the tower
                if not hasattr(self, "_bolt0"):
                    self._bolt0 = {}
                b0 = self._bolt0.setdefault(ob.name, Vector(ob.location))
                ob.location = b0 + Vector(bolt_shift(g, shot))
                ob.keyframe_insert("location", frame=f)
            if shot == 4:
                for n, a in self.act.items():
                    a.place(f, RINGERS[n][2])
                    r = self.ropes[n]
                    r.location = (self.rope_xy[n][0], self.rope_xy[n][1], -HAUL * pull_u(g, RINGERS[n][4]))
                    r.keyframe_insert("location", frame=f)
            self.keyed.add((shot, g))

    def visible(self, shot):
        for a in self.act.values():
            a.set_hidden(shot != 4)
        for r in self.ropes.values():
            r.hide_render = shot != 4

    def pose(self, shot, gs):
        self.key(shot, gs)
        self.visible(shot)
        if shot != 4:
            return
        cam = self.cam
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for n, a in self.act.items():
                p, u = ringer_pose(n, g)
                hu, hl, up, lo = rest_hands(n)
                x, y = self.rope_xy[n]
                zu, zl = self.hand_z[n]
                dz = -HAUL * u
                hands = {up: {"hand": (x, y, zu + dz), "stretch": 1.3, "bend": -0.6},
                         lo: {"hand": (x, y, zl + dz), "stretch": 1.3, "bend": -0.5}}
                _, inf = a.pose(f, p, hands=hands, camera=cam)
                self.info.setdefault((shot, g), {})[n] = [round(inf[s]["error"], 3) for s in (up, lo)]
        fr = [bf(shot, g) for g in gs]
        for n, a in self.act.items():
            ppd = {"padre": 448, "baker": 320, "woman": 288}[n]
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s04: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = CAMS[shot](g)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads={})
        for a in self.act.values():
            if a.card.hide_render or f not in a.poses:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out["pin_err"] = self.info.get((shot, g), {})
        out["flash"] = flash_at(g, FLASH4 if shot == 4 else FLASH5)[0]
        out["bell"] = round(bell_angle(g), 1)
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(shot)
        self.scene.cycles.samples = samples
        return render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
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


def main(argv, Take=Take, RANGES=RANGES, HERE=HERE):
    cmd = argv[1]
    shot = int(argv[2])
    gs = [g for g in parse(argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    if cmd == "probe":
        Tk = Take()
        Tk.pose(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)))
    elif cmd == "stills":
        out = argv[4]
        scale = float(argv[5]) if len(argv) > 5 else 0.5
        samples = int(argv[6]) if len(argv) > 6 else 6
        Tk = Take()
        Tk.pose(shot, gs)
        for g in gs:
            st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
            dst = os.path.join(out, "s%d_g_%04d.png" % (shot, g))
            os.replace(st["path"], dst)
            print("shot %d g %d  %.1f s wall %.1f cpu  %s" % (shot, g, st["wall"], st["cpu"], json.dumps(Tk.report(shot, g))), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw", "s%d" % shot)
        os.makedirs(out, exist_ok=True)
        scale = float(argv[4]) if len(argv) > 4 else 1.0
        samples = int(argv[5]) if len(argv) > 5 else 12
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
            Tk = Take(quality="final")
            Tk.pose(shot, todo)
            for g in todo:
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)


if __name__ == "__main__":
    main(sys.argv)
