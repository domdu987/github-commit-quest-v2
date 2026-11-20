#!/usr/bin/env python3
"""shot.py -- film 17 take s10 = shots 24-26, THE REVEAL.  Film frames g 1342..1514 (+6 handle each side: first_g 1336, last 1520).

  part M  (location 'measure', measure_chair)  g 1336..1374   calipers on dupont's head, then the whip-off to the right
  part R  (location 'reveal')                  g 1375..1520   whip-on to drawer_big (drawer yanked out 0->1), snap-push to drawer_box
                                                              (box lid opens), snap to card_hero (card rises 0->1), push-in.
Narration clock (film = narration + 0.10 s): "หัวยาวระดับนี้" 44.72 -> g1343, "เปิดลิ้นชัก" 45.64 -> g1371, "นิ้วขนาดนี้" 46.78 -> g1406,
"เหลือกล่อง" 47.58 -> g1430, "หูขนาดนี้" 48.60 -> g1461, "เหลือการ์ดใบเดียว" 49.2 -> g1479.
One location per process:   python3 shot.py <M|R> probe|stills|final a:b[:step] [out_dir] [scale] [samples]
"""
import math, os, sys, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17")):
    sys.path.insert(0, p)
import cast17                                   # noqa: E402 (before sprites)
import bpy                                      # noqa: E402
from mathutils import Vector                    # noqa: E402
import bertillon as K                           # noqa: E402
import actors, camrig, render, sprites          # noqa: E402

TMP = os.path.join(HERE, "work")
FIRST, LAST = 1336, 1520
G_M_END = 1374                                  # part M last frame; part R starts 1375
LENS = 22.0


def lerp(a, b, u):
    return a + (b - a) * u


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sine(u):
    u = clamp(u)
    return 0.5 - 0.5 * math.cos(math.pi * u)


def ease_peak(u, k=1.9):
    """snap easing: in-out with a sharp middle (k ~ peak speed / mean speed): smoothstep blended with quintic."""
    u = clamp(u)
    q = 16 * u ** 5 if u < 0.5 else 1 - 16 * (1 - u) ** 5 if False else (16 * u ** 5 if u < .5 else 1 - ((-2 * u + 2) ** 5) / 2)
    s = u * u * (3 - 2 * u)
    return lerp(s, q, clamp((k - 1.5) / 0.6))


def seg(g, a, b, ease=sine):
    return ease((g - a) / float(b - a))


def blink_at(g, starts, n=4):
    for s in starts:
        if s <= g < s + n:
            return 1.0 if s + 1 <= g < s + 3 else 0.5
    return 0.0


def vlerp(a, b, u):
    return tuple(lerp(a[i], b[i], u) for i in range(3))


# ----------------------------------------------------------------------------- cameras  (loc, look) per frame
# part M: measure_chair.  chair (0.7, 2.3), dupont's head (0.7, 2.3, 1.22); bertillon on 'clerk' (1.45, 1.95).
M_A = ((2.15, 0.70, 1.42), (0.45, 2.28, 1.28))
M_B = ((1.35, 1.35, 1.40), (0.40, 2.25, 1.28))
G_WHIP_M = (1367, 1374)                          # camera whips off to the right (pan), blurred in post


def cam_M(g):
    u = seg(g, FIRST, G_WHIP_M[0], lambda x: 0.4 * sine(x) + 0.6 * x)
    loc, look = vlerp(M_A[0], M_B[0], u), vlerp(M_A[1], M_B[1], u)
    # lateral slide sway on top of the push (screen-right drift, a small arc)
    loc = (loc[0] + 0.10 * math.sin(g * 0.11), loc[1], loc[2] + 0.025 * math.sin(g * 0.17))
    if g > G_WHIP_M[0]:
        w = seg(g, G_WHIP_M[0], G_WHIP_M[1] + 1, lambda x: x ** 2.2)
        look = (look[0] + 3.4 * w, look[1] - 0.8 * w, look[2])           # pan right, fast
    return loc, look


# part R: reveal room.  wall y 0, camera side y > 0.  drawer front centre (0.15, 0, 1.2), pulls out toward +y (travel 0.78).
R_DB0 = ((-0.15, 3.0, 1.9), (-0.50, 0.5, 1.2))          # drawer_big start (landing of the whip)
R_DB1 = ((-0.22, 2.40, 1.8), (-0.48, 0.5, 1.2))           # drawer_big end
R_BX0 = ((0.09, 0.99, 1.68), (-0.03, 0.58, 1.2))          # the drawer_box preset
R_BX1 = ((0.20, 1.12, 1.60), (0.0, 0.56, 1.2))            # push + slide inside shot 25
R_CH0 = ((0.30, 1.55, 1.78), (0.0, 0.70, 1.38))           # card_hero preset
R_CH1 = ((0.16, 1.22, 1.70), (0.0, 0.72, 1.47))           # push-in ~9 %/s + slide
G_WHIP_R = (1375, 1383)           # whip-on: pan settles into drawer_big
G_S25 = 1406                      # shot 25 starts: snap push (16 f)
G_S26 = 1461                      # shot 26 starts: snap to card_hero (16 f)
SNAP = 16


def cam_R(g):
    if g < G_S25:                                                           # shot 24b: drawer_big
        u = seg(g, G_WHIP_R[0], G_S25, lambda x: 0.3 * sine(x) + 0.7 * x)
        loc, look = vlerp(R_DB0[0], R_DB1[0], u), vlerp(R_DB0[1], R_DB1[1], u)
        loc = (loc[0] + 0.05 * math.sin(g * 0.13), loc[1], loc[2])
        if g < G_WHIP_R[1]:                                                 # whip-on: start panned away to the left, brake into place
            w = 1 - seg(g, G_WHIP_R[0] - 1, G_WHIP_R[1], lambda x: 1 - (1 - x) ** 2.2)
            look = (look[0] - 3.4 * w, look[1] + 0.6 * w, look[2])
        return loc, look
    if g < G_S26:                                                           # shot 25: snap push to drawer_box, then drift
        e = seg(g, G_S25, G_S25 + SNAP, lambda x: ease_peak(x, 2.0))
        u = seg(g, G_S25 + SNAP, G_S26, lambda x: 0.25 * sine(x) + 0.75 * x)
        a_loc, a_look = vlerp(R_DB1[0], R_BX0[0], e), vlerp(R_DB1[1], R_BX0[1], e)
        loc, look = vlerp(a_loc, vlerp(R_BX0[0], R_BX1[0], u), 1.0 if g >= G_S25 + SNAP else 0.0), vlerp(a_look, vlerp(R_BX0[1], R_BX1[1], u), 1.0 if g >= G_S25 + SNAP else 0.0)
        if g < G_S25 + SNAP:
            loc, look = a_loc, a_look
        return (loc[0] + 0.03 * math.sin(g * 0.15), loc[1], loc[2]), look
    e = seg(g, G_S26, G_S26 + SNAP, lambda x: ease_peak(x, 2.0))              # shot 26: snap to card_hero, push-in
    if g < G_S26 + SNAP:
        return vlerp(R_BX1[0], R_CH0[0], e), vlerp(R_BX1[1], R_CH0[1], e)
    u = seg(g, G_S26 + SNAP, 1521, lambda x: 0.2 * sine(x) + 0.8 * x)
    loc, look = vlerp(R_CH0[0], R_CH1[0], u), vlerp(R_CH0[1], R_CH1[1], u)
    return (loc[0] + 0.04 * math.sin(g * 0.14), loc[1], loc[2]), look


# ----------------------------------------------------------------------------- hooks (reveal)
def drawer_t(g):
    return seg(g, 1376, 1398, lambda x: ease_peak(x, 1.8))


def lid_t(g):
    return seg(g, 1410, 1434)


def lift_t(g):
    return seg(g, 1466, 1500, lambda x: ease_peak(x, 1.6))


LAMP_DB, LAMP_CARD = 28.0, 38.0             # box_lamp watts (card lowered so the card reads, no near-white bloom)


def lamp_w(g):
    return lerp(LAMP_DB, LAMP_CARD, seg(g, G_S26, G_S26 + SNAP + 8))


# ----------------------------------------------------------------------------- actors
def mk_actor(name, cast, extra_scale=1.0):
    a = actors.Actor(name, cast)
    a.build(sprites.DEFAULT_CANVAS[cast], os.path.join(TMP, "sprites"), contact=True)
    a.head_flip = True
    return a


def pose_with(story, g, mirror=False, expr=None, rim=True, sway=1.0, phase=0.0, **over):
    cast, pose = cast17.STORY17[story]
    pose = dict(pose)
    if expr:
        pose = cast17.with_expr(pose, expr)
    pose = cast17.silent(pose)
    pose["seat17"] = None
    if mirror:
        pose["mirror"] = True
    if rim and cast in K.RIM_FOR:
        pose["rim"] = K.RIM_FOR[cast]; pose["rim_opacity"] = 0.55; pose["rim_w"] = 0.02
    pose["head_roll"] = pose.get("head_roll", 0) + sway * 2.2 * math.sin(g * 0.19 + phase)
    pose["lean"] = pose.get("lean", 0) + sway * 1.6 * math.sin(g * 0.13 + phase * 2)
    pose["blink"] = blink_at(g, [1352 + int(phase * 5), 1402, 1447, 1493 + int(phase * 3)])
    pose.update(over)
    return cast, pose


class Take(object):
    def __init__(self, part, quality="draft"):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.part = part
        self.A = K.build(preset="measure_chair" if part == "M" else "card_hero")
        self.scene = sc = bpy.context.scene
        K.clear_keys()
        self.cam = camrig.make_camera(sc, name="cam_s10", lens=LENS)
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 400
        self.cam.data.dof.use_dof = False
        sc.camera = self.cam
        sc.frame_start, sc.frame_end = 1, 9000
        for o in bpy.data.objects:                    # director fix: the additive light shafts wash over the cards
            if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or [])):
                o.hide_render = True
        self.acts = {}
        self.anch = {}
        self.A_marks = self.A["marks"]
        if part == "R":
            self.lamp = bpy.data.objects["box_lamp"]
        print("take %s built in %.1f s" % (part, time.time() - t0), flush=True)

    # one actor card on a mark (seated 'chair' or standing); scale so the true height is CAST_H
    def put(self, key, cast, mark, dx=0.0, dy=0.0, dz=0.0):
        a = self.acts.get(key) or mk_actor("c_" + key, cast)
        self.acts[key] = a
        x, y, z, fz, who = self.A_marks[mark]
        sc = K.CAST_H[cast] / K.CAST_HD[cast]
        a.root_scale = sc
        return a, (x + dx, y + dy, z + dz), sc

    def pose_frames(self, gs):
        sc = self.scene
        f_of = lambda g: g - FIRST + 1
        for g in gs:
            f = f_of(g)
            loc, look = (cam_M if self.part == "M" else cam_R)(g)
            camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=LENS, interp="LINEAR", easing="AUTO")
            if self.part == "R":
                K.set_drawer("big", drawer_t(g), frame=f)
                K.set_box_lid("box", lid_t(g) if g >= 1410 else 0.0, frame=f)
                K.set_card_lift(lift_t(g), frame=f)
                self.lamp.data.energy = lamp_w(g) * K.LAMP_W * K.STATE["P"]["lamp_k"]
                self.lamp.data.keyframe_insert("energy", frame=f)
            K.set_flicker(1.0, frame=f); K.set_dust(0.4, frame=f); K.set_smoke(1.0, frame=f)
            if self.part == "M":
                K.set_pendulum(frame=f)
        self.stage(gs)

    def stage(self, gs):
        cam = self.cam
        if self.part == "M":
            self.stage_M(gs)
        else:
            self.stage_R(gs)

    # ---- part M: dupont seated in the measuring chair, bertillon (mirrored) holds the calipers on his head
    def stage_M(self, gs):
        d_cast, b_cast = "dupont", "bertillon"
        da, dpos, dsc = self.put("dup", d_cast, "chair", dy=-0.22)
        ba, bpos, bsc = self.put("ber", b_cast, "clerk", dx=-1.0, dy=-0.15)
        # dupont: seated on the chair: head centre at HEAD_Z['chair']
        _, dpose0 = pose_with("dupont_innocent", 1)
        fx, fy = sprites.feet_of(d_cast, dpose0)
        dzz = K.HEAD_Z["chair"] - dsc * fy
        for g in gs:
            f = g - FIRST + 1
            da.place(f, (dpos[0], dpos[1], dzz), scale=dsc)
            ba.place(f, bpos, scale=bsc)
        for g in gs:
            f = g - FIRST + 1
            self.scene.frame_set(f)
            _, dp = pose_with("dupont_innocent", g, expr="worried", phase=1.0, sway=0.6)
            dp["legs"] = "stand"
            da.pose(f, dp, camera=self.cam)
            u0 = seg(g, FIRST, 1350, lambda x: 1 - (1 - x) ** 2)       # the calipers come up from low and settle on the head, then keep working
            head_w = Vector((dpos[0], dpos[1], K.HEAD_Z["chair"] + 0.03))
            # jaw tip target: the calipers pin on the side of dupont's head (screen-left of Bertillon's hand)
            bp_cast, bp = pose_with("bertillon_measuring", g, mirror=False, sway=0.5)
            bp["prop_r"] = dict(bp["prop_r"], angle=-10 + 6 * math.sin(g * 0.3)); bp["gaze"] = (0.95, 0.35); bp["pitch"] = 0.25
            ba.pose(f, bp, hands={"r": {"tip": (head_w.x - 0.10 - 0.45 * (1 - u0), head_w.y - 0.05, head_w.z + 0.09 - 0.40 * (1 - u0) + 0.012 * math.sin(g * 0.9)), "prop": "calipers", "angle": -4}}, camera=self.cam)
        for a, ppd in ((da, 320), (ba, 320)):
            for f, r in zip([g - FIRST + 1 for g in gs], a.render_sprites(ppd, frames=[g - FIRST + 1 for g in gs])):
                self.anch[(a.name, f)] = r["anchors"]

    # ---- part R: bertillon at the drawer (yanks it out and steps back); nobody else is staged (the camera is on the drawer)
    def stage_R(self, gs):
        ba, bpos, bsc = self.put("ber", "bertillon", "drawer_r")
        for g in gs:
            f = g - FIRST + 1
            t = drawer_t(g)
            ba.place(f, (-0.47, 1.12 + 0.36 * t, 0.0) if g < 1411 else (60.0, 60.0, -60.0), scale=bsc)   # leaves during the snap peak (no floating hand in shots 25-26)
        for g in gs:
            f = g - FIRST + 1
            self.scene.frame_set(f)
            t = drawer_t(g)
            _, bp = pose_with("bertillon_neutral", g, mirror=True, sway=0.7, expr="determined" if g < 1395 else "proud"); bp["lean"] = bp.get("lean", 0) - 9 * min(1.0, t * 1.5)
            hand = (0.14, t * 0.78 + 0.03, 1.10)
            ba.pose(f, bp, hands={"r": {"hand": hand}}, camera=self.cam)
        for a, ppd in ((ba, 256),):
            for f, r in zip([g - FIRST + 1 for g in gs], a.render_sprites(ppd, frames=[g - FIRST + 1 for g in gs])):
                self.anch[(a.name, f)] = r["anchors"]

    def heads(self, g):
        f = g - FIRST + 1
        self.scene.frame_set(f)
        out = {}
        for a in self.acts.values():
            if (a.name, f) not in self.anch:
                continue
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, a.feet.get(f))
            out[a.name] = (round(c[0]), round(c[1]))
        return out

    def render(self, gs, out_dir, scale=1.0, samples=12):
        sc = self.scene
        K.setup_render(sc, "final", samples)
        sc.camera = self.cam
        self.cam.data.dof.use_dof = False
        res = []
        for g in gs:
            f = g - FIRST + 1
            st = render.render_frames([f], out_dir, scale=scale, threads=int(os.environ.get("THREADS", "2")), scene=sc, camera=self.cam, verbose=False)[0]
            png = os.path.join(out_dir, "g_%04d.png" % g)
            os.replace(st["path"], png)
            K.grade(png, scale=scale)
            res.append((g, st["wall"], self.heads(g)))
            print("g %d  %.1f s  heads %s" % (g, st["wall"], res[-1][2]), flush=True)
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
    part, cmd, spec = sys.argv[1], sys.argv[2], sys.argv[3]
    out = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "raw")
    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    gs = [g for g in parse(spec) if (FIRST <= g <= G_M_END if part == "M" else G_M_END < g <= LAST)]
    os.makedirs(out, exist_ok=True)
    if cmd == "final":
        gs = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
    if not gs:
        print("nothing to do"); sys.exit(0)
    T = Take(part)
    T.pose_frames(gs)
    T.render(gs, out, scale=scale, samples=samples)
