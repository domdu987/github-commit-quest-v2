#!/usr/bin/env python3
"""shot.py -- film 9 take s17: shot 17 (plan 47.11-51.79 s = g 1413..1553, handles g 1407..1412 and g 1554..1559):
dawn after the battle.  "ยิ่งนาน ตาข่ายนี้ยิ่งแน่น กำแพงข้าวเหนียวบางช่วงยังตั้งอยู่จนถึงทุกวันนี้".
One location (wall_site, two_sections_out build, light DAWN), one set-up, a wide calm move:

    id 1  g 1407..1559  from the field in front of the wall, looking west along Lin's rice-mortar section: its outer face is dented
          by the three cannonballs (set_impact lin 0..2 at t 1: shallow dents, balls embedded, face whole, hairlines set_cracks 0.6)
          but stands whole, the old finished wall runs on into the pink dawn.  The silent enemy cannons stand abandoned on the field,
          thin smoke still drifting.  Lin stands in the field and looks up at his wall (lin_watch, mirrored: screen-left), turns to us
          with a calm confident smile behind a blink on "ยังตั้งอยู่" (49.97 s).  Camera: slow crane up + push + slight orbit,
          0.35 sine + 0.65 linear (moves must move).  The general's section is behind the camera (not in frame: its fall is shots 18-19).
Mouths: nobody speaks.  NO depth of field (c9.Take).

    python3 shot.py probe 1 a:b[:step]
    python3 shot.py stills 1 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

W, actors, camrig, cast9 = C.W, C.actors, C.camrig, C.cast9
lerp, clamp, blink, ez = C.lerp, C.clamp, C.blink, C.ez
TMP = os.path.join(HERE, "work")

G0, G1, H = C.g_bound(47.11), C.g_bound(51.79), 6        # 1413, 1554
RANGES = {1: (G0 - H, G1 + H - 1)}                       # 1407..1559
G_TURN = C.g_of(49.97)                                    # 1502 "ยังตั้งอยู่": turns to us, calm smile


def bf(shot, g):
    return int(g) - 1300                                  # Blender frame (one set-up)


LIN = Vector((-12.0, -4.2, 0.0))
CAM0 = ((-11.0, -18.6, 4.2), (-11.6, 0.0, 6.0))
CAM1 = ((-12.2, -17.4, 4.0), (-12.0, 0.0, 6.1))
LENS = 14.0
PPD = 200


def cam_of(g):
    x = (g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0])
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector(lerp(CAM0[0], CAM1[0], u)), Vector(lerp(CAM0[1], CAM1[1], u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def pose(g):
    """until the blink at g 1501..1503 Lin looks up at his wall in quiet wonder ('stunned': round eyes, dash mouth, no smile), head
    and gaze up-left; the expression and the turn to the lens change on the closed frame g 1502 ('happy' smile, arms folded)."""
    if g < G_TURN:                                       # g < 1502 (closed eyes frame of the blink 1501..1503)
        p = dict(cast9.STORY9["lin_watch"][1])
        p.update(mirror=True, pitch=-1.15 + 0.06 * math.sin(g * 0.09), gaze=(0.55 + 0.15 * math.sin(g * 0.07), -0.95), expr="stunned", mouth="dash",
                 yaw=0.9, head_roll=9.0 + 2.0 * math.sin(g * 0.11), lean=-3.0 + 0.8 * math.sin(g * 0.06))
    else:
        tu = u_of(g, G_TURN, G_TURN + 10)
        p = dict(cast9.STORY9["lin_calm"][1])
        p.update(expr="happy", mouth="smile", gaze=(0.0, 0.0), yaw=lerp(0.6, 0.2, tu), pitch=lerp(-0.8, -0.2, tu) + 0.05 * math.sin(g * 0.1),
                 head_roll=-5.0 + 2.0 * math.sin(g * 0.11), lean=1.2 * math.sin(g * 0.08))
    p["blink"] = blink(g, [1440, G_TURN - 1, 1545])
    p["t"] = g / 30.0
    return p


SCORCH_D = 5.6                                           # scorch + crack card size (D)


def _scorch_png(i):
    """a painted soot ring (dark, ragged, densest just outside the dent) with 9-12 jagged hairline cracks radiating 1.3-2.7 D out
    from the dent rim, some forking; RGBA 1024 px over SCORCH_D (cached in work/)."""
    import random
    from PIL import Image, ImageDraw, ImageFilter
    p = os.path.join(TMP, "scorch_%d.png" % i)
    if os.path.exists(p):
        return p
    os.makedirs(TMP, exist_ok=True)
    n = 1024; ppd = n / SCORCH_D; c = n / 2.0; r = random.Random(17 + 31 * i)
    soot = Image.new("L", (n, n), 0); ds = ImageDraw.Draw(soot)
    for k in range(260):                                   # soot blobs, densest in a ring r 0.95..1.8 D
        a = r.uniform(0, 2 * math.pi); rr = (0.9 + abs(r.gauss(0, 0.45))) * ppd; s_ = r.uniform(0.12, 0.38) * ppd
        x, y = c + rr * math.cos(a), c + rr * math.sin(a) * r.uniform(0.85, 1.15)
        ds.ellipse([x - s_, y - s_, x + s_, y + s_], fill=int(r.uniform(90, 200)))
    ds.ellipse([c - 1.25 * ppd, c - 1.25 * ppd, c + 1.25 * ppd, c + 1.25 * ppd], fill=235)
    ds.ellipse([c - 0.5 * ppd, c - 0.5 * ppd, c + 0.5 * ppd, c + 0.5 * ppd], fill=60)
    soot = soot.filter(ImageFilter.GaussianBlur(ppd * 0.14))
    cr = Image.new("L", (n, n), 0); dc = ImageDraw.Draw(cr)
    def crack(x, y, a, length, w, depth):
        steps = int(length * ppd / 14)
        for _ in range(steps):
            a += r.uniform(-0.5, 0.5); nx, ny = x + 14 * math.cos(a), y + 14 * math.sin(a)
            dc.line([(x, y), (nx, ny)], fill=255, width=max(2, int(w))); x, y = nx, ny; w *= 0.985
            if depth < 2 and r.random() < 0.06:
                crack(x, y, a + r.choice((-1, 1)) * r.uniform(0.5, 0.9), length * 0.4, w * 0.7, depth + 1)
    for k in range(r.randint(9, 12)):
        a = 2 * math.pi * k / 11.0 + r.uniform(-0.25, 0.25)
        crack(c + 1.15 * ppd * math.cos(a), c + 1.15 * ppd * math.sin(a), a, r.uniform(1.4, 2.9), r.uniform(9, 13), 0)
    # alpha: soot (up to 0.85) + cracks (1.0); colour: soot dark brown-black, cracks near black
    import numpy as np
    sa = np.asarray(soot, dtype=np.float32) / 255.0 * 0.95; ca = np.asarray(cr, dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:n, 0:n]; rad = np.hypot(xx - c, yy - c) / ppd
    sa *= np.clip((SCORCH_D / 2 - rad) / 0.6, 0, 1)        # no hard card edge
    ca *= np.clip((SCORCH_D / 2 - 0.1 - rad) / 0.3, 0, 1)
    al = np.clip(np.maximum(sa, ca), 0, 1)
    rgb = np.zeros((n, n, 3), np.float32); rgb[..., 0] = 0.10; rgb[..., 1] = 0.065; rgb[..., 2] = 0.045
    rgb = rgb * (1 - ca[..., None]) + np.array([0.03, 0.02, 0.02]) * ca[..., None]
    Image.fromarray(np.dstack([rgb * 255, al * 255]).astype(np.uint8), "RGBA").save(p)
    return p


def _scorch_mat(i):
    import bpy
    m = bpy.data.materials.new("s17_scorch_%d" % i); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N("ShaderNodeOutputMaterial"); tx = N("ShaderNodeTexImage"); tx.image = bpy.data.images.load(_scorch_png(i)); tx.image.alpha_mode = "STRAIGHT"
    em = N("ShaderNodeEmission"); tr = N("ShaderNodeBsdfTransparent"); mx = N("ShaderNodeMixShader")
    L(tx.outputs["Color"], em.inputs["Color"]); L(tx.outputs["Alpha"], mx.inputs["Fac"]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2])
    L(mx.outputs[0], out.inputs[0])
    return m


def fix_set():
    """runtime set changes (wall.py untouched), QA-tech round 1 on s17:
    - Lin's three dents 1.35x bigger, a soot scorch disc (r 2.1 D, ragged) behind each, the embedded balls smooth (subsurf);
    - Lin's hairline cracks fully opaque (alpha gain 4);
    - the foreground spent cannonball covered by a smooth 64x32 sphere (the merged dress mesh has a 28x16 one)."""
    import bpy, random
    S = W.STATE
    mats = [_scorch_mat(i) for i in range(3)]
    for d in S["decals"]["lin"]:
        c = d["c"]
        me = d["decal"].data
        for v in me.vertices:
            v.co = c + (v.co - c) * 1.35
        bpy.ops.mesh.primitive_plane_add(size=SCORCH_D, location=(c.x, -0.15, c.z), rotation=(math.pi / 2, 0, 0))
        sc = bpy.context.active_object; sc.name = "s17_scorch"
        for col in list(sc.users_collection): col.objects.unlink(sc)
        S["SET"].objects.link(sc); sc.data.materials.append(mats[S["decals"]["lin"].index(d)])
        sc.visible_shadow = False; sc.visible_diffuse = False; sc.visible_glossy = False
        b = d["ball_in"]
        for poly in b.data.polygons: poly.use_smooth = True
        b.modifiers.new("sub", "SUBSURF").levels = 2
    cm = S["crack_mats"]["lin"]
    for n in cm.node_tree.nodes:
        if n.type == "MATH" and n.operation == "MULTIPLY" and n.use_clamp:
            n.inputs[1].default_value = 4.0
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.512, location=(-12.4, -7.6, 0.3))
    ball = bpy.context.active_object; ball.name = "s17_ball_smooth"
    for col in list(ball.users_collection): col.objects.unlink(ball)
    S["SET"].objects.link(ball)
    for poly in ball.data.polygons: poly.use_smooth = True
    ball.data.materials.append(S["M"]["cannonball"])
    W.no_bounce(ball)


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "wall_site", "aftermath_dawn", quality=quality, lens=LENS, name="cam_s17", light="DAWN")
        fix_set()
        # no proxy shadow (the low sun threw it onto the wall, detached from his feet); a darker contact decal under the feet instead
        self.lin = self.actors["lin"] = C.make_actor("lin", "lin", os.path.join(TMP, "sprites"), shadow=None,
                                                     contact=dict(width=1.6, depth=0.7, color="#140c08", opacity=0.9))
        if self.lin.contact is not None:
            self.lin.contact.location.z = 0.035              # just above the uneven soil

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look, lens=LENS)
            C.place(self.lin, f, LIN)
            W.set_wall_height("lin", 26, frame=f); W.set_wall_height("general", 30, frame=f)
            self.key_set(f, flames=0.7, smoke=0.2, army=False, impact=[("lin", i, 1.0) for i in range(3)] + [("general", i, 0.0) for i in range(3)],
                         cracks=("lin", 1.0), collapse=0.0)
            W.set_cracks("general", 0.0, frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.lin.pose(f, pose(g), camera=self.cam)
        self.sprites_for([(self.lin, PPD)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
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
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
