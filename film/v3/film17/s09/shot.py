#!/usr/bin/env python3
"""shot.py -- film 17 take s09: shots 22 + 23 (crisis, narration 39.76-44.65 s), g 1196..1342 + 6 handle frames each side (1190..1348).
Set measure (DAY_INT), one process.  Shot 22 g<=1274: measure_door camera, two gendarmes escort dupont (held pose) in, the inspector follows smirking.
Shot 23 g>=1275: measure_chair camera, dupont seated in the chair, innocent shrug + head shake (mouth closed), inspector grins at Bertillon.
Nobody speaks: no quote window falls inside this take.

    python3 shot.py probe a:b [scale]            camera-only low-sample frames -> work/probe  (rhythm tuning)
    python3 shot.py frames a:b[:step] scale samples outdir
"""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C                                       # noqa: E402
from c17 import K, bpy, Vector, cast17, actors, sprites, camrig, render   # noqa: E402

G0, G1, H = 1196, 1342, 6
FIRST, LAST = G0 - H, G1 + H                          # 1190 .. 1348
G_CUT = 1275                                          # shot 23 starts (plan 42.40 s + 0.10 s)
WORK = os.path.join(HERE, "work")
GAIN = float(os.environ.get("GAIN", "1.9"))
DUST = float(os.environ.get("DUST", "0.0"))
SWAY = float(os.environ.get("SWAY", "0.07"))

# ---------------------------------------------------------------- camera
P22 = Vector((-1.7, 0.9, 1.5)); L22 = Vector((3.2, -2.9, 1.3))
P23 = Vector((2.0, 0.2, 1.95)); L23 = Vector((0.7, 2.4, 1.0))


def right_of(pos, look):
    f = (look - pos); f.z = 0; f.normalize()
    return Vector((f.y, -f.x, 0.0))


def snap(g, g0, n=14):
    return C.smooth((g - g0) / float(n))


def mix(u):   # mostly linear, a little ease: no dead ends
    return 0.3 * C.ez(u) + 0.7 * u


def cam_of(g):
    if g < G_CUT:
        u = (g - FIRST) / float(G_CUT - 1 - FIRST)
        fwd = (L22 - P22).normalized(); R = right_of(P22, L22)
        pos = P22 + fwd * (-0.45 * GAIN) * mix(u) + R * (-0.45 * GAIN) * mix(u) + Vector((0, 0, 0.05)) * mix(u)
        s = snap(g, 1236)
        pos += fwd * (0.1 * GAIN) * s + R * (0.35 * GAIN) * s
        s2 = snap(g, 1215); pos += fwd * (0.05 * GAIN) * s2 + R * (-0.25 * GAIN) * s2
        s3 = snap(g, 1258); pos += R * (0.3 * GAIN) * s3
        pos += R * (SWAY * math.sin(g * 0.5)) + Vector((0, 0, SWAY * 0.7 * math.sin(g * 0.77)))
        track = Vector(group_pos(g)) + Vector((0, 0, 1.25))
        look = L22.lerp(track, 0.92 * C.smooth(u)) + R * (0.5 * GAIN) * s * 0.0
        look = look + R * (0.9 * GAIN) * s - R * (0.6 * C.smooth(u))
    else:
        u = (g - G_CUT) / float(LAST - G_CUT)
        fwd = (L23 - P23).normalized(); R = right_of(P23, L23)
        pos = P23 + fwd * (0.15 * GAIN) * mix(u) + R * (0.35 * GAIN) * mix(u)
        s = snap(g, 1311)
        pos += fwd * (0.1 * GAIN) * s + R * (-0.3 * GAIN) * s
        s2 = snap(g, 1290); pos += fwd * (0.08 * GAIN) * s2 + R * (0.3 * GAIN) * s2
        s3 = snap(g, 1331); pos += R * (0.15 * GAIN) * s3
        pos += R * (SWAY * math.sin(g * 0.5)) + Vector((0, 0, SWAY * 0.7 * math.sin(g * 0.77)))
        look = L23 + Vector((0.0, 0.0, -0.3)) + Vector((-0.25, 0.0, 0.1)) * s + Vector((0.2, 0, 0)) * mix(u)
    return pos, look


# ---------------------------------------------------------------- staging
D_START = Vector((2.75, -2.4, 0.0)); D_END = Vector((1.2, -1.95, 0.0))
INS_LAG = 0.8


def path_s(g):
    return C.smooth((g - FIRST) / float(G_CUT - 1 - FIRST)) * 0.35 + 0.65 * (g - FIRST) / float(G_CUT - 1 - FIRST)


def group_pos(g, lag=0.0):
    d = (D_END - D_START); L = d.length; dn = d / L
    s = path_s(g) * L - lag
    return D_START + dn * s


def walk(cast, pose, g, ph0=0.0, mirror=False):
    # march cycle on top of the escort/stance pose; arms of the pose are kept
    dist = path_s(g) * (D_END - D_START).length
    p = cast17.cycle(cast, dist / 1.0 + ph0, "march", 1, base=pose, arms="none")
    p = dict(p)
    for k in ("expr", "mouth", "yaw", "pitch", "head_roll", "blink", "mirror", "squash", "rim", "rim_opacity", "rim_w", "gaze"):
        if k in pose:
            p[k] = pose[k]
    return p


def bob(g, f=1.9, a=0.03, ph=0.0):
    return a * abs(math.sin(math.pi * f * (g - FIRST) / 30.0 + ph))


CHAIR = (0.7, 2.3, 0.5)
BERT23 = Vector((0.7, 3.3, 0.0))
INS23 = Vector((0.05, 1.9, 0.0))
INS_YAW = float(os.environ.get('INS_YAW', '0.5'))
LEGS = {'narrow': dict(preset='narrow', crouch=0.45, knee_r=0.0, knee_l=0.0), 'wide': dict(preset='wide', crouch=0.35, knee_r=0.0, knee_l=0.0), 'stand': 'stand', 'mid': dict(preset='narrow', crouch=0.3, knee_r=0.25, knee_l=-0.25)}[os.environ.get('LEGS', 'narrow')]
DUP_DZ = float(os.environ.get("DUP_DZ", "-0.3"))
DUP_SEAT = Vector((0.8, 2.13, 0.0))


class Take(object):
    def __init__(self, mode="draft", samples=6):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.A = K.build(preset="measure_door", light="DAY_INT")
        self.sc = bpy.context.scene
        K.clear_keys()
        self.cam = self.sc.camera
        self.cam.data.dof.use_dof = False
        self.cam.data.clip_start = 0.02
        self.sc.frame_start, self.sc.frame_end = 1, 9999
        K.setup_render(self.sc, "final", samples)
        self.sc.cycles.denoising_prefilter = "FAST"
        self.sc.render.use_persistent_data = False
        for o in bpy.data.objects:      # director's systemic fix: the additive light shafts wash over the cast cards
            if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or [])):
                o.hide_render = True
        self.remove_rods()
        self.fg = [o for o in bpy.data.objects if o.name.startswith("fg")]
        self.act = {}

    def remove_rods(self):
        # the loose spreading calipers on the small table read as floating white rods: delete their geometry (world sphere r 0.3 at (2.10, 1.70, 0.81))
        import bmesh
        ctr = Vector((2.10, 1.70, 0.81)); ctr2 = Vector((1.55, 1.64, 0.97)); ctr3 = Vector((2.44, 1.27, 1.10)); ctr4 = Vector((2.12, 2.01, 0.81)); n = 0
        for o in bpy.data.objects:
            if o.type != 'MESH' or o.name.startswith('fg') or not o.data.vertices:
                continue
            mw = o.matrix_world
            bm = bmesh.new(); bm.from_mesh(o.data)
            dv = [v for v in bm.verts if ((mw @ v.co - ctr).length < 0.3 and 0.78 < (mw @ v.co).z < 1.0) or (o.name.endswith('cream') and ((mw @ v.co - ctr2).length < 0.25 or (mw @ v.co - ctr3).length < 0.3)) or (o.name.endswith('steel') and (mw @ v.co - ctr4).length < 0.12)]
            if dv:
                n += len(dv); bmesh.ops.delete(bm, geom=dv, context='VERTS'); bm.to_mesh(o.data)
            bm.free()
        print('removed rod verts', n, flush=True)

    def add(self, key, name, cast):
        self.act[key] = C.make_actor(name, cast, os.path.join(WORK, "sprites"))

    def key_set(self, f, g):
        K.key_life(f, f)

    def build_cast(self):
        for k, n, c in (("dup", "dup", "dupont"), ("ga", "ga", "gendarme_a"), ("gb", "gb", "gendarme_b"),
                        ("ins", "ins", "inspector17"), ("ber", "ber", "bertillon")):
            self.add(k, n, c)

    def hscale(self, cast):
        return K.CAST_H[cast] / K.CAST_HD[cast]

    def place(self, key, f, xy, cast, pose, seated=None, dz=0.0):
        a = self.act[key]; sc = self.hscale(cast)
        if seated:
            fx, fy = sprites.feet_of(cast, pose); zz = K.HEAD_Z[seated] - sc * fy
        else:
            zz = 0.0
        a.place(f, (float(xy[0]), float(xy[1]), zz + dz), scale=sc)

    # poses ---------------------------------------------------------------
    def poses(self, g):
        """returns {key: (xy, cast, pose, seated, dz, visible)} for frame g"""
        out = {}
        if g < G_CUT:
            gp = group_pos(g); cam, _ = cam_of(g); Rr = right_of(cam, L22)
            c, p = C.story("dupont_held"); p["blink"] = C.blink(g, [1213, 1251]); p["head_roll"] = 4 + 3 * math.sin(g * 0.2)
            p["yaw"] = 0.35; p = cast17.silent(p)
            out["dup"] = (gp, c, walk(c, p, g, 0.0), None, bob(g, f=2.0), True)
            c, p = C.story("gendarme_escort_a"); p["yaw"] = 0.3
            out["ga"] = (gp - Rr * 0.6, c, walk(c, p, g, 0.5), None, bob(g, f=2.0, ph=0.4), True)
            c, p = C.story("gendarme_escort_b", mirror=True); p["yaw"] = -0.3
            out["gb"] = (gp + Rr * 0.6, c, walk(c, p, g, 0.25), None, bob(g, f=2.0, ph=0.2), True)
            ip = group_pos(g, 0.25 + 0.65 * C.smooth((g - FIRST) / 60.0))
            c, p = C.story("inspector_arms_crossed", expr="proud"); p["blink"] = C.blink(g, [1224, 1262]); p["yaw"] = 0.5
            p["head_roll"] = -6 + 2 * math.sin(g * 0.15); p = cast17.silent(p)
            out["ins"] = (ip + Rr * (1.4 + 0.5 * C.smooth((g - FIRST) / 40.0)), c, walk(c, p, g, 0.75), None, bob(g, f=2.0, ph=0.6), True)
            c, p = C.story("bertillon_neutral"); out["ber"] = (BERT23, c, p, None, 0.0, False)
        else:
            c, p = C.story("dupont_innocent")
            p = cast17.silent(p); p["mouth"] = "flat"; p["expr"] = "worried"; p.pop("gaze", None)
            t = (g - 1290) / 30.0
            burst = 1.0 if (1290 <= g < 1311 or 1318 <= g < 1339) else 0.0
            sh = max(-1.0, min(1.0, 1.7 * math.sin(2 * math.pi * 2.5 * (g - (1290 if g < 1315 else 1318)) / 30.0))) * burst
            p["yaw"] = 0.1 + 0.5 * sh; p["head_roll"] = -2 + 12 * sh
            p["lean"] = 2 + 5 * sh; p["blink"] = C.blink(g, [1288, 1330])
            p["legs"] = LEGS
            out["dup"] = (DUP_SEAT, c, p, "chair", DUP_DZ, True)
            c, p = C.story("inspector_arms_crossed"); p["expr"] = "happy"; p["mouth"] = "smile"
            ch = math.sin(2 * math.pi * 3.0 * g / 30.0)
            p["squash"] = (1 + 0.02 * ch, 1 - 0.02 * ch); p["head_roll"] = -10 + 2 * ch; p["yaw"] = INS_YAW; p["pitch"] = -0.25; p["gaze"] = (0.9, 0.0)
            p["blink"] = C.blink(g, [1292, 1334]); out["ins"] = (INS23, c, p, None, 0.03 * abs(ch), True)
            c, p = C.story("bertillon_neutral"); p["yaw"] = -0.3; p["head_roll"] = 2 * math.sin(g * 0.11); p["blink"] = C.blink(g, [1300])
            out["ber"] = (BERT23, c, cast17.silent(p), None, 0.0, True)
            c, p = C.story("gendarme_standing_a"); out["ga"] = (Vector((-1.0, 3.2, 0)), c, p, None, 0.0, False)
            out["gb"] = (Vector((-1.0, 3.2, 0)), c, p, None, 0.0, False)
        return out

    def pose_frames(self, gs):
        self.build_cast()
        for g in gs:
            f = g
            pos, look = cam_of(g)
            camrig.key_camera(f, pos, look, cam=self.cam, lens=22.0, interp="LINEAR", easing="AUTO")
            for o in self.fg:
                o.hide_render = g >= G_CUT; o.keyframe_insert("hide_render", frame=f)
            K.key_life(f, f, dust=DUST)
            P = self.poses(g)
            for k, (xy, c, p, seat, dz, vis) in P.items():
                a = self.act[k]; self.place(k, f, xy, c, p, seat, dz); C.hide_keys(a, f, not vis)
        for g in gs:
            self.sc.frame_set(g)
            P = self.poses(g)
            for k, (xy, c, p, seat, dz, vis) in P.items():
                if vis:
                    self.act[k].pose(g, p, camera=self.cam)
        ppd = int(os.environ.get("PPD", "256"))
        for k, a in self.act.items():
            fr = [g for g in gs if self.poses(g)[k][5]]
            if fr:
                a.render_sprites(ppd, frames=fr)

    def render(self, gs, out, scale, threads=2):
        os.makedirs(out, exist_ok=True)
        st = render.render_frames(list(gs), out, scale=scale, threads=threads, scene=self.sc, camera=self.cam, prefix="g_", verbose=True)
        for s in st:
            K.grade(s["path"], scale=scale)
        return st


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    gs = parse(a[1]); scale = float(a[2]); samples = int(a[3]); out = a[4]
    T = Take(samples=samples)
    T.pose_frames(gs)
    T.render(gs, out, scale)
