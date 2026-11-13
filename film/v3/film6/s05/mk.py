#!/usr/bin/env python3
"""mk.py -- helpers shared by the market takes s03 / s05 / s12 of film 6 (an identical copy lives in each take folder, so
every take stays self-contained).  Import AFTER common:

    import common as C; import mk

  crow_svg(uid, pose, flip)  a cartoon crow (plum ink, blue-black body, grey beak) for set dressing: poses 'stand', 'peck',
                             'look', 'caw' (beak open, no "mouth" in the cast sense), 'flap_up', 'flap_down'
  splat_svg(uid, kind, k)    a cartoon splat of rotten veg (tomato red / cabbage olive), comic, no injury
  register_bakers()          extra pilloried bakers for the week-count shots (copies of cast6 'baker2' with other clothes,
                             caps and faces) -> puppet.CAST['baker3'..'baker5'] + sprites.DEFAULT_CANVAS (runtime only;
                             cast6 is not edited)
  Shot                       a small per-shot take: one C.Take (location / light preset), camera keys per film frame g,
                             actors + prop cards, render / report in the format of film6/s01 (raw/s<id>/g_%04d.png + json)
"""
import math, os, sys, copy, json
import common as C
from mathutils import Vector

INK = "#2a1a33"


# ----------------------------------------------------------------------------- crow
def crow_svg(uid, pose="stand", flip=False):
    """crow ~0.75 D long (beak tip to tail), feet at (0, 0), facing +x (flip: -x).  Returns an SVG fragment (D units, y down)."""
    body, dark, beak, ink = "#2c2f45", "#1b1c2c", "#9a96a0", INK
    sw = 0.022
    head_dy = {"peck": 0.16, "look": -0.03, "caw": -0.05}.get(pose, 0.0)
    hx = 0.20 if pose != "peck" else 0.27
    hy = -0.46 + head_dy
    o = []
    # legs
    if pose not in ("flap_up", "flap_down"):
        for dx in (-0.04, 0.05):
            o.append('<path d="M %.3f -0.20 L %.3f 0 M %.3f 0 l 0.07 0 M %.3f 0 l -0.05 0.01" stroke="%s" stroke-width="0.018" '
                     'fill="none" stroke-linecap="round"/>' % (dx, dx + 0.01, dx + 0.01, dx + 0.01, "#4a4450"))
    else:
        o.append('<path d="M -0.02 -0.22 l -0.06 0.10 M 0.04 -0.22 l -0.05 0.11" stroke="#4a4450" stroke-width="0.018" '
                 'fill="none" stroke-linecap="round"/>')
    # tail
    o.append('<path d="M -0.16 -0.30 L -0.48 -0.18 L -0.46 -0.26 L -0.50 -0.24 L -0.20 -0.40 Z" fill="%s" stroke="%s" '
             'stroke-width="%.3f" stroke-linejoin="round"/>' % (dark, ink, sw))
    # body
    o.append('<ellipse cx="0.0" cy="-0.33" rx="0.22" ry="0.14" transform="rotate(-14 0 -0.33)" fill="%s" stroke="%s" '
             'stroke-width="%.3f"/>' % (body, ink, sw))
    # wing
    if pose == "flap_up":
        o.append('<path d="M -0.06 -0.38 Q -0.10 -0.80 -0.38 -0.92 Q -0.30 -0.70 -0.34 -0.62 Q -0.20 -0.56 -0.20 -0.48 Q -0.10 -0.40 0.08 -0.36 Z" '
                 'fill="%s" stroke="%s" stroke-width="%.3f" stroke-linejoin="round"/>' % (dark, ink, sw))
    elif pose == "flap_down":
        o.append('<path d="M -0.06 -0.32 Q -0.14 -0.04 -0.40 0.06 Q -0.30 -0.10 -0.32 -0.16 Q -0.20 -0.20 -0.18 -0.26 Q -0.06 -0.28 0.08 -0.30 Z" '
                 'fill="%s" stroke="%s" stroke-width="%.3f" stroke-linejoin="round"/>' % (dark, ink, sw))
    else:
        o.append('<path d="M 0.10 -0.36 Q -0.08 -0.44 -0.30 -0.30 Q -0.10 -0.24 0.06 -0.27 Z" fill="%s" stroke="%s" '
                 'stroke-width="%.3f" stroke-linejoin="round"/>' % (dark, ink, sw))
    # head + beak
    o.append('<circle cx="%.3f" cy="%.3f" r="0.105" fill="%s" stroke="%s" stroke-width="%.3f"/>' % (hx, hy, body, ink, sw))
    bx = hx + 0.09
    if pose == "caw":
        o.append('<path d="M %.3f %.3f L %.3f %.3f L %.3f %.3f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (bx, hy - 0.035, bx + 0.17, hy - 0.07, bx, hy - 0.005, beak, ink))
        o.append('<path d="M %.3f %.3f L %.3f %.3f L %.3f %.3f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (bx, hy + 0.005, bx + 0.15, hy + 0.06, bx, hy + 0.035, beak, ink))
    else:
        tilt = 0.06 if pose == "peck" else 0.0
        o.append('<path d="M %.3f %.3f L %.3f %.3f L %.3f %.3f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (bx, hy - 0.035, bx + 0.17, hy + 0.01 + tilt, bx, hy + 0.035, beak, ink))
    # eye
    o.append('<circle cx="%.3f" cy="%.3f" r="0.030" fill="#ffffff"/><circle cx="%.3f" cy="%.3f" r="0.015" fill="%s"/>'
             % (hx + 0.035, hy - 0.025, hx + 0.042, hy - 0.025, ink))
    g = "".join(o)
    if flip:
        g = '<g transform="scale(-1 1)">%s</g>' % g
    return '<g id="%s">%s</g>' % (uid, g)


CROW_BOX = (-0.62, -1.02, 0.62, 0.10)


# ----------------------------------------------------------------------------- splat
def splat_svg(uid, kind="tomato", k=1.0, seed=0):
    """flat cartoon splat (radius ~0.22 D at k 1), centred (0, 0)."""
    import random
    rr = random.Random(seed)
    col, dark = (("#d2322a", "#8e1e1e") if kind == "tomato" else ("#8a9a3a", "#5a6626"))
    o = []
    pts = []
    n = 11
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 0.16 * k * (0.75 + 0.5 * rr.random())
        pts.append((math.cos(a) * r, math.sin(a) * r * 0.8))
    d = "M %.3f %.3f " % pts[0] + " ".join("Q %.3f %.3f %.3f %.3f" % (pts[i][0] * 1.25, pts[i][1] * 1.25,
                                                                       (pts[i][0] + pts[(i + 1) % n][0]) / 2,
                                                                       (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)) + " Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.02"/>' % (d, col, INK))
    for i in range(6):
        a = rr.uniform(0, 2 * math.pi); r = 0.26 * k * rr.uniform(0.9, 1.3)
        o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" stroke="%s" stroke-width="0.012"/>'
                 % (math.cos(a) * r, math.sin(a) * r * 0.8, 0.03 * k * rr.uniform(0.7, 1.4), col, INK))
    o.append('<ellipse cx="-0.04" cy="-0.04" rx="%.3f" ry="%.3f" fill="%s" opacity="0.5"/>' % (0.06 * k, 0.03 * k, "#ffffff"))
    if kind != "tomato":
        o.append('<path d="M -0.08 0.02 q 0.06 -0.08 0.14 0 M -0.05 0.07 q 0.05 -0.05 0.1 0" stroke="%s" stroke-width="0.016" fill="none"/>' % dark)
    return '<g id="%s">%s</g>' % (uid, "".join(o))


# ----------------------------------------------------------------------------- extra bakers
BAKERS = {
    # name: (tunic, tunic dark, cap style + colours, moustache, pencil, beard, build tweaks)
    "baker3": dict(sleeve="#8a5a3a", sleeve_d="#5e3c26", base="#8a5a3a", dark="#5e3c26", apron="#efe6d4",
                   hat_style="skullcap", hat_light="#f4ead0", hat_base="#d8c49a", hat_dark="#a8946a", hair="#a8642e",
                   moustache=True, pencil=False, torso_w=0.80, profile="PROFILE_PEAR", seed=91.5, mouth="wavy"),
    "baker4": dict(sleeve="#4f6a8a", sleeve_d="#344a64", base="#4f6a8a", dark="#344a64", apron="#f2ece0",
                   hat_style="skullcap", hat_light="#ffffff", hat_base="#e6e2da", hat_dark="#b0aaa0", hair="#2a2422",
                   moustache=False, pencil=False, torso_w=0.66, profile="PROFILE_ATHLETE", seed=101.5, mouth="wavy",
                   beard=dict(color="#2a2422", dark="#14100e")),
    "baker5": dict(sleeve="#7a4a6a", sleeve_d="#52304a", base="#7a4a6a", dark="#52304a", apron="#ebe2cc",
                   hat_style="skullcap", hat_light="#f0d8a8", hat_base="#c8a46a", hat_dark="#8e7040", hair="#9a9490",
                   moustache=True, pencil=False, torso_w=0.70, profile="PROFILE_PEAR", seed=111.5, mouth="wavy"),
}


def register_bakers():
    import puppet as P
    import sprites
    cast6 = C.cast6
    CE = sys.modules.get("cast_ext")
    base = P.CAST["baker2"]
    for name, v in BAKERS.items():
        c = copy.deepcopy(base)
        c["seed"] = v["seed"]
        c["torso_w"] = v["torso_w"]
        if CE is not None and hasattr(CE, v["profile"]):
            c["profile"] = getattr(CE, v["profile"])
        c["sleeve"] = dict(c["sleeve"], color=v["sleeve"], dark=v["sleeve_d"], cuff=v["sleeve"])
        c["colors"] = dict(c["colors"], base=v["base"], dark=v["dark"], apron=v["apron"])
        c["hat_colors"] = dict(c["hat_colors"], light=v["hat_light"], base=v["hat_base"], dark=v["hat_dark"])
        c["hair"] = dict(c["hair"], color=v["hair"])
        c["moustache"] = v["moustache"]
        c["pencil_moustache"] = v["pencil"]
        if "beard" in v:
            c["beard"] = v["beard"]
        P.CAST[name] = c
        sprites.DEFAULT_CANVAS[name] = sprites.DEFAULT_CANVAS["baker2"]
        if CE is not None and hasattr(CE, "CANVAS"):
            CE.CANVAS[name] = CE.CANVAS["baker2"]


def pillory_pose(cast_name, g, shake=0.0, phase=0.0, expr="sad", flinch=0.0, **kw):
    """a pilloried baker: head + hands through the cast board; shake = 'no, no' head-shake amplitude (yaw), flinch 0..1."""
    W = C.cast6.PILLORY_WRIST_Y
    yaw = shake * math.sin(2 * math.pi * (g / 30.0) * 2.2 + phase)
    p = dict(yaw=yaw - 0.15 * flinch, pitch=0.30 - 0.2 * flinch, expr=expr, head_roll=-6 + 14 * flinch + 3 * math.sin(g * 0.11 + phase),
             arm_r=dict(hand=(0.56, W), bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.56, W), bend=-0.6, stretch=1.3),
             legs="narrow", pillory=True, t=g / 30.0)
    p.update(kw)
    return p


def cut_pillory_board():
    """delete the 3D set's pillory board (two planks, the three hole discs, padlock, hinge pin) from the merged 'pillory'
    mesh at runtime, so the cast6 pillory boards drawn on the actors are the only boards (platform, post, sign, splats stay)."""
    import bpy, bmesh
    obs = [o for o in bpy.context.scene.objects if o.type == "MESH" and o.name.startswith("pillory") and "lamp" not in o.name and "halo" not in o.name]
    n = 0
    for ob in obs:
        bm = bmesh.new(); bm.from_mesh(ob.data)
        mw = ob.matrix_world
        kill = [v for v in bm.verts if (lambda p: -5.80 <= p.x <= -2.20 and 9.50 <= p.y <= 9.76 and 2.68 <= p.z <= 3.42)(mw @ v.co)]
        n += len(kill)
        bmesh.ops.delete(bm, geom=kill, context="VERTS")
        bm.to_mesh(ob.data); bm.free(); ob.data.update()
    return n


# ----------------------------------------------------------------------------- per-framing take
class MShot(C.Take):
    """One framing (internal shot id SID) of a market take: build, camera per film frame g, actors / props per g.
    Subclass: SID, PRESET, G (first, last g rendered incl. handles), camv(g) -> (loc, look, lens), setup(), place(g, f),
    pose(g, f) (the camera is keyed when pose runs), JOBS() -> [(actor, px_per_D)], extra_report(g)."""
    SID, PRESET, G = 1, "AFTERNOON", (0, 0)
    LOC = "market"
    CUT_BOARD = False

    def __init__(self, quality="preview"):
        C.Take.__init__(self, self.LOC, self.PRESET, quality=quality, lens=22.0, name="cam_s%d" % self.SID)
        if self.CUT_BOARD:
            cut_pillory_board()
        print("sharp sky:", sharp_sky(), flush=True)
        self.sd = os.path.join(self.HERE, "work", "sprites_%d" % self.SID)
        self.props_dir = os.path.join(self.HERE, "work", "props")
        self.cards = {}
        self.setup()

    # hooks
    def setup(self): pass
    def place_g(self, g, f): pass
    def pose_g(self, g, f): pass
    def jobs(self): return []
    def extra_report(self, g): return {}
    def set_g(self, g, f): self.key_set(f)

    def bf(self, g): return C.bf(self.SID, g)

    def do_pose(self, gs):
        for g in gs:
            f = self.bf(g)
            loc, look, lens = self.camv(g)
            self.key_cam(f, loc, look, lens=lens)
            self.set_g(g, f)
            self.place_g(g, f)
        for g in gs:
            f = self.bf(g)
            self.scene.frame_set(f)
            self.pose_g(g, f)
        fr = [self.bf(g) for g in gs]
        if self.jobs():
            self.sprites_for(self.jobs(), fr)

    def report(self, g):
        f = self.bf(g)
        self.scene.frame_set(f)
        loc, look, lens = self.camv(g)
        v = Vector(look) - Vector(loc)
        out = dict(sid=self.SID, g=g, cam=[round(c, 3) for c in loc], lens=lens,
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f))
        out.update(self.extra_report(g))
        return out

    def render_g(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [self.bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

    def card(self, name, variants, box, scale=1.0, shadow=True, ppd=256):
        """PropCard from a list of SVG fragments (one per variant)."""
        pngs = C.svg_pngs([(s, box, ppd) for s in variants], self.props_dir)
        pc = C.PropCard(name, pngs, box, scale=scale, shadow=shadow)
        self.cards[name] = pc
        return pc


def run(classes, argv, here):
    """CLI:  probe <sid> a:b  |  stills <sid> a:b <out> [scale] [samples]  |  final <sid> a:b [scale] [samples]"""
    cmd, sid = argv[1], int(argv[2])
    cls = classes[sid]
    cls.HERE = here
    gs = [g for g in C.parse(argv[3]) if cls.G[0] <= g <= cls.G[1]]
    if cmd in ("probe", "stills"):
        Tk = cls("preview")
        Tk.do_pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = argv[4]; os.makedirs(out, exist_ok=True)
                scale = float(argv[5]) if len(argv) > 5 else 0.5
                samples = int(argv[6]) if len(argv) > 6 else 6
                st = Tk.render_g([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (sid, g)))
                print("sid %d g %d  %.1f s wall %.1f cpu" % (sid, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(argv[4]) if len(argv) > 4 else 1.0
        samples = int(argv[5]) if len(argv) > 5 else 12
        out = os.path.join(here, "raw", "s%d" % sid); os.makedirs(out, exist_ok=True)
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: sid %d, %d to render, %d done" % (sid, len(todo), len(gs) - len(todo)), flush=True)
        if not todo:
            return
        Tk = cls("final")
        Tk.do_pose(todo)
        for g in todo:
            st = Tk.render_g([g], out, scale=scale, samples=samples)[0]
            png = os.path.join(out, "g_%04d.png" % g)
            os.replace(st["path"], png)
            rep = Tk.report(g)
            rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
            json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
            print("sid %d g %d  %.1f s wall  %.1f s cpu" % (sid, g, st["wall"], st["cpu"]), flush=True)


def lerpv(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(len(a)))


def sharp_sky(mode=None, px=12288):
    """CLIENT RULE (no blur): the set's sky dome texture draws its clouds through an SVG feGaussianBlur and at 11 px/deg,
    which reads soft in close / long-lens market shots.  Re-draw the same sky (same seed, same clouds, sun, birds) WITHOUT
    the blur filter at `px` px across 360 deg (34 px/deg) and swap it into the sky material at runtime (set not edited)."""
    import inspect, bpy
    import bakery_tex as BT
    mode = mode or ("afternoon" if C.B.STATE.get("preset") == "AFTERNOON" else "morning")
    src = inspect.getsource(BT.sky)
    src = src.replace('<g filter="url(#b)" opacity="0.95">', '<g opacity="0.95">')
    src = src.replace("job('sky_' + mode, 0, 0, W, H, 4096 / 360.0, ''.join(o), defs=g)", "return '<defs>' + g + '</defs>' + ''.join(o)")
    src = src.replace("def sky(mode):", "def _sharp_sky(mode):")
    ns = dict(BT.__dict__)
    exec(src, ns)
    frag = ns["_sharp_sky"](mode)
    png = C.svg_png(frag, (0, 0, 360.0, 105.0), px / 360.0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "work", "sky"))
    img = bpy.data.images.load(png, check_existing=True)
    n = 0
    for ob in bpy.context.scene.objects:
        if ob.name != "sky":
            continue
        for slot in ob.material_slots:
            m = slot.material
            if m is None or not m.use_nodes:
                continue
            for nd in m.node_tree.nodes:
                if nd.type == "TEX_IMAGE" and nd.image is not None and "sky" in nd.image.name:
                    nd.image = img; nd.interpolation = "Cubic"; n += 1
    return n
