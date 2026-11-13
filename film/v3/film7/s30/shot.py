#!/usr/bin/env python3
"""shot.py -- film 7 take s30: shot 30 (99.33-103.20 s = g 2980..3095) + handles 6 frames each side (g 2974..3101), rendered in 3D.
Plan: louvre / empty_wall_queue, 'modern feel: bigger crowd' -- tens of thousands queueing, period-ambiguous (just a huge crowd).
Dissolve in from shot 29.  Narration: "ทุกวันนี้ มีคนต่อแถวดู โมนาลิซ่าวัน ละหลายหมื่นคน และเธอยัง ยิ้มอยู่หลัง..."
Here she is BACK on the wall (set_mona True), the queue ropes up (set_queue True), and the Salon Carre is packed.

    id 1  g 2974..3038  side angle from the right of the room (camera crane x 5.6 -> 5.0, slow push): the packed queue lane pressing
                        toward the small painting (screen-left, above the crowd), more people waiting outside the ropes, everyone
                        staring up at her.  "มีคนต่อแถวดู โมนาลิซ่า" (99.80 / 100.59 s).
    id 2  g 3039..3101  CUT just before "ละหลายหมื่นคน" (101.27 s = g 3041): the reverse from beside her frame, high, looking back
                        down the gallery over a sea of hats and bowlers that fills the room to the far wall, all faces up at her
                        (behind the lens, screen-right); slow crane up + back to reveal more (the 'tens of thousands').
Nobody speaks (no quoted line): static expression mouths only.  NO depth of field anywhere (C.Take).

Blender frame of (id, g) = 1000 * (id - 1) + (g - 2900) + 1.
    python3 shot.py probe 1|2 a:b[:step]
    python3 shot.py stills 1|2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, ez = C.lerp, C.clamp, C.blink, C.ez
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(99.33), C.g_bound(103.20)              # 2980, 3096
H = 6
G_CUT = C.g_of(101.27) - 2                                # 3039: cut just before "ละหลายหมื่นคน"
RANGES = {1: (G0 - H, G_CUT - 1), 2: (G_CUT, G1 + H - 1)}
MONA = Vector((0.0, 21.80, 3.55))
FACE = Vector((0.0, 21.80, 3.90))
LENS = {1: 22.0, 2: 20.0}


def bf(shot, g):
    return 1000 * (shot - 1) + (g - 2900) + 1


def cam_of(shot, g):
    a, b = RANGES[shot]
    u = ez((g - a) / float(b - a), "sine")
    if shot == 1:      # side angle, slow crane-in toward the wall
        loc = Vector(lerp((4.7, 13.4, 5.1), (4.0, 14.9, 4.9), u))
        look = Vector(lerp((-0.6, 21.6, 3.1), (-0.4, 21.6, 3.3), u))
    else:              # reverse from beside her, crane up + back
        loc = Vector(lerp((2.3, 21.3, 4.9), (2.6, 21.0, 5.7), u))
        look = Vector(lerp((-1.0, 6.0, 3.0), (-0.9, 6.0, 2.9), u))
    return loc, look


# ----------------------------------------------------------------------------- the crowd
CASTS = ["lady"] * 9 + ["gentleman"] * 8 + ["newsboy"] * 2 + ["coworker1", "coworker2", "painter", "plumber"]
KEEP_OUT = [((0.0, 10.0), 2.3),               # the round divan
            ((-6.2, 13.5), 1.4),              # the copyist's easel
            ((11.0, 16.0), 1.6)]              # the picture ladder


def crowd_spots(shot, seed):
    """feet spots (x, y) of the crowd: a packed queue lane (x -2.3..2.3, y 14.9..20.0) + the waiting crowd outside the ropes."""
    rnd = random.Random(seed)
    pts = []

    def ok(p, dmin):
        if any((p - Vector(c)).length < r for c, r in KEEP_OUT):
            return False
        return all((p - q).length >= dmin for q in pts)

    def fill(x0, x1, y0, y1, n, dmin):
        tries = 0
        while n > 0 and tries < 4000:
            tries += 1
            p = Vector((rnd.uniform(x0, x1), rnd.uniform(y0, y1)))
            if ok(p, dmin):
                pts.append(p); n -= 1

    fill(-2.25, 2.25, 14.8, 19.4 if shot == 1 else 20.0, 26, 0.62)   # inside the lane (shot 1: keep her sight line)
    if shot == 1:
        fill(-8.5, -2.95, 11.0, 20.6, 34, 0.72)        # left of the lane (beyond it from this camera)
        fill(-2.25, 2.25, 8.0, 14.6, 14, 0.72)           # the tail of the lane
        fill(2.95, 6.5, 15.5, 20.6, 12, 0.72)           # right of the lane, near side
        fill(-12.0, 3.0, 2.5, 11.0, 24, 0.85)          # deep back-left
    else:
        fill(-9.0, -2.95, 12.5, 20.4, 28, 0.72)
        fill(2.95, 9.0, 12.0, 19.0, 22, 0.72)
        fill(-11.5, 11.5, 2.5, 14.8, 95, 0.74)         # the far room, packed to the front wall
    return pts


def to_cam_space(cam_loc, cam_look, p):
    f = (cam_look - cam_loc).normalized()
    r = f.cross(Vector((0, 0, 1))).normalized()
    u = r.cross(f)
    d = p - cam_loc
    return d.dot(r), d.dot(u), d.dot(f)


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "louvre", "empty_wall_queue", quality=quality, lens=LENS[shot], name="cam_s30_%d" % shot)
        self.shot = shot
        self.scene.cycles.transparent_max_bounces = 160      # ~60 stacked crowd cards + proxies: the default limit renders black
        self.scene.cycles.max_bounces = max(self.scene.cycles.max_bounces, 4)
        sd = os.path.join(TMP, "sprites%d" % shot)
        rnd = random.Random(300 + shot)
        loc, look = cam_of(shot, (RANGES[shot][0] + RANGES[shot][1]) // 2)
        self.crowd = []
        for k, p in enumerate(crowd_spots(shot, 30 + shot)):
            if (Vector((p.x, p.y, 0)) - Vector((loc.x, loc.y, 0))).length < 3.0:
                continue
            if self.head_low(shot, p):
                continue
            cast = rnd.choice(CASTS)
            a = C.make_actor("c%02d" % k, cast, sd, shadow="proxy")
            self.actors[a.name] = a
            self.crowd.append(dict(a=a, p=p, cast=cast, seed=rnd.random(), kind="point" if rnd.random() < 0.13 else "stare",
                                   scale=rnd.uniform(0.95, 1.04), roll=rnd.uniform(-7, 7), phase=rnd.randint(0, 40)))
        print("s30: %d crowd actors in set-up %d" % (len(self.crowd), shot), flush=True)

    def head_low(self, shot, p):
        """True if this spot's head (z ~3.0, bottom ~2.55) falls below the caption line y 880 (or behind the lens) on any
        frame of the set-up -- such people are left out (whole heads above y 880)."""
        from bpy_extras.object_utils import world_to_camera_view
        a, b = RANGES[shot]
        for g in range(a, b + 1, 4):
            loc, look = cam_of(shot, g)
            self.key_cam(bf(shot, g), loc, look)
            self.scene.frame_set(bf(shot, g))
            v = world_to_camera_view(self.scene, self.cam, Vector((p.x, p.y, 2.45)))
            if v.z > 0 and -0.15 < v.x < 1.15 and (1 - v.y) * 1280 > 872:
                return True
        return False

    def crowd_pose(self, m, g, loc, look):
        a, p = m["a"], m["p"]
        head = Vector((p.x, p.y, 2.7))
        dx, dy, dz = to_cam_space(loc, look, MONA - head)          # where she is, seen from this person in camera terms
        hor = math.hypot(dx, dz) + 1e-6
        side = dx / max(hor, 1e-6)                                   # +1 = screen-right of the person
        up = clamp((MONA.z - 2.7 + 1.2) / max((MONA - head).length, 0.5) * 2.0, 0.2, 1.0)
        cast = m["cast"]
        if cast in ("lady", "gentleman", "newsboy"):
            nm = ("crowd_point" if m["kind"] == "point" else "crowd_stare") + ("" if cast == "lady" else "_" + cast)
            pose = dict(cast7.STORY7[nm][1])
        else:
            pose = dict(cast7.STORY7["crowd_point" if m["kind"] == "point" else "crowd_stare"][1])
        mirror = side < 0
        yaw = clamp(0.12 + 0.55 * abs(side), 0.10, 0.65)
        step = ((g + m["phase"]) // 11) % 4                         # small idle head moves every 11 frames (sprite cache friendly)
        pose.update(mirror=mirror, yaw=yaw, gaze=(0.25 + 0.6 * abs(side), -0.55 - 0.4 * up),
                    pitch=-0.25 - 0.35 * up + (0.04 if step == 2 else 0.0),
                    head_roll=m["roll"] + (0, 2.5, -1.5, 1.0)[step])
        if m["seed"] < 0.35:
            pose["expr"] = "happy"
        elif m["seed"] < 0.55:
            pose["expr"] = "excited"
        bl = [b for b in range(2900 + int(m["seed"] * 60), 3200, 47 + int(m["seed"] * 20))]
        pose["blink"] = blink(g, bl)
        pose["t"] = g / 30.0
        return pose

    def pose(self, shot, gs):
        assert shot == self.shot
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look)
            self.key_set(f, mona=True, queue=True)
            for m in self.crowd:
                C.place(m["a"], f, (m["p"].x, m["p"].y), 0.0, scale=m["scale"])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            loc, look = cam_of(shot, g)
            for m in self.crowd:
                m["a"].pose(f, self.crowd_pose(m, g, loc, look), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = []
        for m in self.crowd:
            dist = (Vector((m["p"].x, m["p"].y, 1.5)) - cam_of(shot, gs[0])[0]).length
            jobs.append((m["a"], 224 if dist < 7 else (160 if dist < 12 else 112)))
        self.sprites_for(jobs, fr)
        # exact caption-band cull: anyone whose real head (sprite head anchor, 1 D) dips below y 875 on ANY frame of the set-up
        # is hidden for the whole set-up (pose() gets every frame of the set-up before the first render: final renders the set-up
        # in one call of pose)
        self.culled = getattr(self, "culled", set())
        for g in gs:
            for k, h in C.head_report(self, bf(shot, g)).items():
                if 0 <= h["x"] <= 720 and h["y"] + h["w"] / 2 > 875:
                    self.culled.add(k)
        for k in self.culled:
            a = self.actors[k]
            for ob in (a.card, a.proxy, a.contact):
                if ob is not None:
                    ob.hide_render = True
        print("s30: culled for the caption band: %s" % sorted(self.culled), flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        loc, look = cam_of(shot, g)
        v = look - loc
        heads = C.head_report(self, f)
        low = {k: h for k, h in heads.items() if h["y"] + h["w"] / 2 > 880 and 0 <= h["x"] <= 720}
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    n_heads=len(heads), heads_below_880=low,
                    biggest=max(heads.items(), key=lambda kv: kv[1]["w"]) if heads else None)

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
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
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: shot)
