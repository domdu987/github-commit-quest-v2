#!/usr/bin/env python3
"""shot.py -- film 17 take s07 (team 1 rework): the measuring montage, shots 16-19, g 844..1051 (first_g 844, 208 frames).
  16   g 844..899   REUSED frames of team 6 (34bb2c8) -- not rendered here
  17a  g 900..923   finger insert: a gloved hand holds the caliper bar, the sliding jaw closes on the middle finger lying on a wooden gauge
  17b  g 924..947   foot insert: a gloved hand pushes the sliding block of the foot board until it touches the toe of a boot
  18a  g 948..971   ear insert (s01 S3A setup) on prisoner_b: jaws pinned to the ear, gloved hand on the bar
  18b  g 972..995   card insert: a gloved hand writes rows of marks on a record card with a plain pen
  19   g 996..1051  drawer wall: the card goes into the medium drawer (disappears), the drawer is pushed shut, pull-out on drawers ajar
One location (measure room, DAY_INT); everything else is 3D props built here.  Blender frame = g.
    python3 shot.py stills a:b[:s] out_dir [scale] [samples]     python3 shot.py final a:b[:s] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import K, bf, ez, lerp, clamp, bpy, Vector, cast17, actors
from mathutils import Euler
TMP = os.path.join(HERE, "work")
CUTS = [900, 924, 948, 972, 996]
RANGE = (900, 1051)

def shot_of(g):
    if g < 924: return "17a"
    if g < 948: return "17b"
    if g < 972: return "18a"
    if g < 996: return "18b"
    return "19"
def t_of(g, a, b): return clamp((g - a) / float(b - a))
def mix(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))
def sm(u): return ez(u, "sine")
def lin(u, k=0.2): return k * sm(u) + (1 - k) * clamp(u)

# ------------------------------------------------------------------ palette additions (skin, glove)
def add_pal():
    P = K.STATE["PAL"]
    base = dict(tex=None, tile=1.0, tint=True, sm=(1, 1, 1), ink=True, gain=1.0, off=(0, 0, 0), mix=None, afl=0.12)
    P["skin"] = dict(base, col="#e6a98c"); P["glove"] = dict(base, col="#e9e0cb"); P["sleeve"] = dict(base, col="#35487a", sm=(0.9, 0.95, 1.2))
    P["pcoat"] = dict(base, col="#6a4a30"); P["pants"] = dict(base, col="#3a4262", sm=(0.9, 0.95, 1.2))
    P["paper"] = dict(base, col="#f1e6c6", ink=True, mix=0.5)

# ------------------------------------------------------------------ small helpers for rigid animated groups
def new_root(name):
    ob = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(ob); ob.rotation_mode = "XYZ"; return ob

def build(name, fn, parent=None, ink=0.0025, seed=5):
    B = K.Batch(seed); fn(B); return B.finalize(name, loc=(0, 0, 0), parent=parent, ink_t=ink)

def kloc(ob, f, loc): ob.location = loc; ob.keyframe_insert("location", frame=f)
def krot(ob, f, rot): ob.rotation_euler = rot; ob.keyframe_insert("rotation_euler", frame=f)
def kvis(obs, f, on):
    allo = []
    for o in obs: allo += [o] + list(o.children_recursive)
    for o in allo:
        o.hide_render = not on; o.keyframe_insert("hide_render", frame=f)

def kids(root): return [o for o in bpy.data.objects if o.parent is root or (o.parent is not None and o.parent.parent is root)]

# ------------------------------------------------------------------ prop geometry (local frames)
def glove_fist(B, c=(0, 0, 0), s=1.0, ax=(1, 0, 0)):
    """a gloved fist (cream leather) with a thumb bump and a short white cuff, at c; the sleeve is a separate cylinder."""
    B.sphere("glove", c, 0.050 * s, scale=(1.15, 0.95, 0.95)); B.sphere("glove", (c[0] - 0.01 * s, c[1] - 0.04 * s, c[2] + 0.012 * s), 0.024 * s, scale=(1.3, 1, 0.9))
    for k in range(4): B.sphere("glove", (c[0] + 0.03 * s, c[1] + (-0.036 + 0.024 * k) * s, c[2] - 0.026 * s), 0.016 * s)

def sleeve(B, a, b, r=0.045, cuff=True):
    """navy sleeve from a toward b (world/local points), white cuff at a."""
    a, b = np_(a), np_(b); d = b - a; L = float(np_norm(d)); mid = (a + b) / 2
    B.cyl("sleeve", tuple(mid), r, L, axis="z", seg=14, rot=rot_to(d))
    if cuff: B.cyl("cardedge", tuple(a + d / L * 0.02), r * 1.12, 0.045, axis="z", seg=14, rot=rot_to(d))

import numpy as np
def np_(v): return np.array(v, float)
def np_norm(v): return np.linalg.norm(v)
def rot_to(d):
    """euler (deg, K.Batch.cyl rot argument) that turns +z onto direction d."""
    d = np_(d) / np_norm(d); ry = math.degrees(math.acos(max(-1, min(1, d[2])))); rz = math.degrees(math.atan2(d[1], d[0]))
    # Batch.cyl applies rotm(*rot): treat as (x, y, z) degrees; a rotation about y by ry then z by rz maps +z to d
    return (0.0, ry, rz)

def caliper_fixed(B, L=0.46, y_b=0.15, z_b=0.08, jx=-0.148):
    """beam + fixed jaw (plate) -- the beam is along x centred on 0.03 in the local frame of the gauge; the plate reaches y -0.03..y_b."""
    cx = 0.03
    B.box("steel", (cx, y_b + 0.012, z_b), (L, 0.024, 0.024)); B.box("brass", (cx, y_b + 0.012, z_b + 0.014), (L * 0.95, 0.008, 0.004))
    for k in range(int(L / 0.03)): B.box("iron", (cx - L / 2 + 0.02 + 0.03 * k, y_b - 0.002, z_b + 0.014), (0.004, 0.006, 0.008 if k % 4 else 0.014))
    B.box("steel", (jx, (y_b - 0.03) / 2, 0.06), (0.02, y_b + 0.03, 0.06))

def caliper_slide(B, y_b=0.15, z_b=0.08):
    B.box("steel", (0, y_b - 0.01, z_b - 0.002), (0.045, 0.05, 0.04)); B.box("steel", (0, (y_b - 0.03) / 2, 0.06), (0.02, y_b + 0.03, 0.06))
    B.cyl("brass", (0, y_b + 0.012, z_b + 0.03), 0.018, 0.03, seg=10); B.cyl("brass", (0, y_b + 0.012, z_b + 0.048), 0.024, 0.012, seg=10)

# ------------------------------------------------------------------ the scene
Z0 = 0.808                         # table top (K.table h 0.80 + baize 0.008)
TBL = (-0.25, -1.90)               # table centre (open floor, camera looks at the window wall)
FB = (-1.10, -1.00)                # foot board centre (open floor)
CAB = (-0.40, 3.40)                # drawer cabinet: front plane at y 3.40, facing -y (the camera)
MED_X, MED_Z = 0.05, 0.87          # the medium drawer that takes the card (relative x to CAB, z)

class Scene(C.Take):
    def __init__(self, quality="draft"):
        C.Take.__init__(self, "measure_chair", quality, fg=False)
        self.q = quality
        add_pal()
        for o in bpy.data.objects:                       # the set's light shafts wash over cards: hide them
            if any(m and m.name.startswith("beam_fx") for m in (getattr(o.data, "materials", None) or [])): o.hide_render = True
        self.build_table(); self.build_17a(); self.build_17b(); self.build_18b(); self.build_19()
        self.build_18a_actors()
        self.lamps = []
        for tag, loc, w in (("17a", LT(-0.30, -0.30, Z0 + 0.55), 80), ("17b", LF(-0.3, -0.4, 0.75), 160), ("18b", LT(-0.30, -0.30, Z0 + 0.55), 80), ("19", (CAB[0] + 0.5, CAB[1] - 0.9, 1.9), 220)):
            L = K.point(loc, watts=w, radius=0.15, name="ins_" + tag, flicker=False); self.lamps.append((tag, L))

    # ---- shared table
    def build_table(self):
        B = K.Batch(7); K.table(B, TBL, size=(1.0, 0.7), h=0.80, mat="oak", top="leather")
        w = lambda lx, ly: (TBL[0] - ly, TBL[1] + lx)           # table-local -> world (turned +90 deg)
        K.ledger_stack(B, (*w(-0.40, -0.25), Z0), n=4, rot=100); K.inkpot(B, (*w(0.36, -0.27), Z0), rot=30); K.inkpot(B, (*w(0.28, -0.29), Z0), quill=False)
        B.finalize("tbl", ink_t=0.004)

    # ---- 17a finger gauge
    def build_17a(self):
        self.r17a = new_root("r17a"); self.r17a.location = (TBL[0], TBL[1], Z0); self.r17a_static = new_root("r17a_s"); self.r17a_static.location = (TBL[0], TBL[1], Z0)
        for o in (self.r17a, self.r17a_static): o.rotation_euler = (0, 0, math.pi / 2)
        def gauge(B):
            B.box("honey", (0, 0, 0.015), (0.64, 0.17, 0.03)); B.box("brass", (0, -0.073, 0.032), (0.58, 0.012, 0.004))
            for k in range(30): B.box("iron", (-0.29 + 0.02 * k, -0.073, 0.035), (0.003, 0.011 if k % 5 else 0.019, 0.004))
            B.box("walnut", (-0.31, 0.0, 0.06), (0.02, 0.17, 0.06))
            # the thief's hand lying flat (palm, middle finger long along the ruler, the other fingers short, thumb), jacket sleeve
            B.sphere("skin", (-0.205, 0.0, 0.052), 0.085, scale=(1.0, 0.82, 0.26)); B.cyl("pcoat", (-0.36, 0.0, 0.052), 0.042, 0.16, axis="x", seg=12)
            B.cyl("cardedge", (-0.275, 0.0, 0.052), 0.047, 0.035, axis="x", seg=12)
            for y, x0, x1 in ((0.0, -0.13, 0.075), (0.034, -0.13, 0.008), (-0.034, -0.13, 0.014), (-0.066, -0.13, -0.045)):
                B.cyl("skin", ((x0 + x1) / 2, y, 0.043), 0.0125, x1 - x0, axis="x", seg=10); B.sphere("skin", (x1, y, 0.043), 0.0125)
            B.cyl("skin", (-0.16, 0.074, 0.043), 0.0135, 0.075, axis="x", seg=10, rot=(0, 0, -35))
        build("g17a", gauge, self.r17a_static, ink=0.0022)
        def fixed(B):
            caliper_fixed(B); glove_fist(B, (0.255, 0.165, 0.084), 0.95); sleeve(B, (0.30, 0.175, 0.09), (0.62, 0.30, 0.20))
        build("c17a_f", fixed, self.r17a, ink=0.0022)
        self.s17a = new_root("s17a"); self.s17a.rotation_euler = (0, 0, math.pi / 2)
        def slide(B):
            caliper_slide(B); B.sphere("glove", (0, 0.162, 0.125), 0.024, scale=(1.2, 1, 0.9))     # the gloved thumb on the thumbscrew
        build("c17a_s", slide, self.s17a, ink=0.0022)
        self.group17a = [self.r17a_static, self.r17a, self.s17a]

    def pose_17a(self, g):
        f = bf(g); u = t_of(g, 900, 923)
        k = sm(clamp(u / 0.8))                       # closes g900..918, then holds with a tiny squeeze
        xs = lerp(0.235, 0.097, k) - 0.002 * math.sin((g - 918) * 0.9) * (1 if u > 0.8 else 0)
        wob = 0.004 * math.sin(g * 0.7)
        kloc(self.r17a, f, (TBL[0] - wob, TBL[1], Z0 + 0.003 * math.sin(g * 0.5)))
        kloc(self.s17a, f, (TBL[0] - wob, TBL[1] + xs, Z0 + 0.003 * math.sin(g * 0.5)))
        kloc(self.r17a_static, f, (TBL[0], TBL[1], Z0))

    # ---- 17b foot board
    def build_17b(self):
        self.r17b = new_root("r17b"); self.r17b.location = (FB[0], FB[1], 0.0); self.r17b.rotation_euler = (0, 0, math.pi / 2)
        def board(B):
            B.box("oak", (0, 0, 0.02), (0.68, 0.22, 0.04)); B.box("walnut", (-0.31, 0, 0.09), (0.04, 0.22, 0.1)); B.box("brass", (0, -0.098, 0.043), (0.62, 0.012, 0.004))
            for k in range(32): B.box("iron", (-0.30 + 0.02 * k, -0.098, 0.046), (0.003, 0.011 if k % 5 else 0.019, 0.004))
            # boot (toe to +x): sole, welt, upper, toe cap, shaft, trouser leg
            B.box("leather", (-0.08, 0.0, 0.0525), (0.34, 0.105, 0.025)); B.box("dark", (-0.08, 0.0, 0.068), (0.345, 0.108, 0.006))
            B.box("leather", (-0.10, 0.0, 0.098), (0.22, 0.098, 0.066)); B.sphere("leather", (0.045, 0.0, 0.092), 0.055, scale=(1.25, 0.95, 0.85))
            B.cyl("leather", (-0.17, 0.0, 0.27), 0.056, 0.30, seg=14); B.cyl("pants", (-0.17, 0.0, 0.78), 0.068, 0.80, seg=14)
            B.cyl("brass", (-0.21, 0.056, 0.30), 0.009, 0.01, axis="y", seg=8)
        build("b17b", board, self.r17b, ink=0.0024)
        self.s17b = new_root("s17b"); self.s17b.rotation_euler = (0, 0, math.pi / 2)
        def block(B):
            B.box("walnut", (0, 0, 0.09), (0.05, 0.22, 0.1)); B.cyl("brass", (0, 0, 0.17), 0.02, 0.06, seg=10)
            glove_fist(B, (0, 0.0, 0.225), 0.95); sleeve(B, (0.03, 0.0, 0.25), (0.34, 0.10, 0.65))
        build("k17b", block, self.s17b, ink=0.0024)
        self.group17b = [self.r17b, self.s17b]

    def pose_17b(self, g):
        f = bf(g); u = t_of(g, 924, 947)
        k = sm(clamp(u / 0.75))
        xc = lerp(0.34, 0.152, k)                    # block inner face meets the toe tip (x ~ 0.125) at 0.152 - 0.025
        kloc(self.r17b, f, (FB[0], FB[1], 0.0))
        kloc(self.s17b, f, (FB[0] - 0.003 * math.sin(g * 0.8), FB[1] + xc, 0.0))

    # ---- 18b card + pen
    def build_18b(self):
        self.r18b = new_root("r18b"); self.r18b.location = (TBL[0], TBL[1], Z0); self.r18b.rotation_euler = (0, 0, math.pi / 2)
        def card(B):
            with B.xf((0, 0, 0), (0, 0, 6)):
                B.box("paper", (0, 0, 0.004), (0.36, 0.24, 0.008)); B.box("oxblood", (-0.11, 0.128, 0.006), (0.06, 0.025, 0.008))
                for x in (-0.125, -0.045):
                    B.box("dark", (x, 0.05, 0.0105), (0.066, 0.078, 0.003)); B.box("cream", (x, 0.05, 0.0125), (0.054, 0.066, 0.003)); B.sphere("dark", (x, 0.058, 0.0145), 0.016, scale=(1, 1, 0.2)); B.sphere("dark", (x, 0.026, 0.0145), 0.024, scale=(1, 0.8, 0.2))
                B.cyl("dark", (-0.085, -0.065, 0.0105), 0.026, 0.003, seg=14); B.cyl("paper", (-0.085, -0.065, 0.012), 0.017, 0.003, seg=14)
                for r in range(5): B.box("ink", (0.0, 0.095 - 0.045 * r, 0.0095), (0.2, 0.0016, 0.0012))           # ruled lines
        build("card18", card, self.r18b, ink=0.0016)
        self.marks = []                                                  # the written marks: 5 rows x 7, shown one by one as the nib passes
        rows = []
        for r in range(5):
            for c in range(7):
                B = K.Batch(r * 7 + c)
                ln = 0.010 + 0.008 * ((r * 3 + c * 5) % 3)
                with B.xf((0, 0, 0), (0, 0, 6)): B.box("ink", (0.020 + 0.0235 * c + ln / 2, 0.095 - 0.045 * r + 0.003 * ((c * 7 + r) % 3 - 1), 0.0112), (ln, 0.0055, 0.0022))
                ob = B.finalize("mk%d_%d" % (r, c), loc=(0, 0, 0), parent=self.r18b, ink=False)
                self.marks.append((r, c, ob))
        self.pen = new_root("pen")
        def pen(B):
            B.cone = None
            B.cyl("steel", (0, 0, 0.012), 0.0042, 0.024, r2=0.0008, seg=10); B.cyl("brass", (0, 0, 0.030), 0.0072, 0.012, seg=12)
            B.cyl("dark", (0, 0, 0.130), 0.0066, 0.19, seg=12); B.cyl("brass", (0, 0, 0.228), 0.0072, 0.008, seg=12)
            glove_fist(B, (0.0, 0.0, 0.16), 0.9); sleeve(B, (0, 0, 0.215), (0.0, -0.02, 0.50))
        build("pen", pen, self.pen, ink=0.0016)
        self.group18b = [self.r18b, self.pen] + [m[2][0] for m in self.marks if m[2]]

    def pose_18b(self, g):
        f = bf(g); u = t_of(g, 972, 995)
        n = 35; idx = u * (n + 1)                     # marks written so far
        # nib path: row after row, left to right
        i = clamp(idx, 0, n - 0.001); r = int(i // 7); c = i - 7 * r
        x = 0.020 + 0.0235 * c + 0.012; y = 0.095 - 0.045 * r
        ang = math.radians(6)
        px = x * math.cos(ang) - y * math.sin(ang); py = x * math.sin(ang) + y * math.cos(ang)
        nib = (TBL[0] - py, TBL[1] + px, Z0 + 0.012 + 0.003 * math.sin(g * 1.9))
        kloc(self.pen, f, nib)
        a = Vector((0.10, 0.42, 0.9)).normalized(); self.pen.rotation_euler = a.to_track_quat("Z", "Y").to_euler(); krot(self.pen, f, tuple(self.pen.rotation_euler))
        kloc(self.r18b, f, (TBL[0], TBL[1], Z0))
        for (rr, cc, ob) in self.marks:
            k = rr * 7 + cc; kvis(ob, f, k < idx)

    # ---- 19 drawer wall
    def build_19(self):
        X0, Yc = CAB
        self.r19 = new_root("r19"); self.r19.location = (X0, Yc, 0.0)
        # carcass
        def carcass(B):
            B.box("walnut", (0.0, 0.26, 0.95), (2.7, 0.52, 1.9)); B.box("walnut", (0.0, 0.0, 0.0225), (2.76, 0.12, 0.045)); B.box("walnut", (0.0, 0.0, 1.925), (2.76, 0.14, 0.05))
        build("cab", carcass, self.r19, ink=0.004)
        # drawer layouts: (size, x, z)
        draws = []
        for i, z in enumerate((0.23, 0.60, 0.97, 1.34)): draws.append(("l", -0.95, z))
        for cx in (-0.40, 0.05):
            for j in range(7): draws.append(("m", cx, 0.15 + 0.24 * j))
        for cx in (0.40, 0.55, 0.70, 0.85):
            for j in range(14): draws.append(("s", cx, 0.075 + 0.12 * j))
        S = dict(l=(0.50, 0.33), m=(0.30, 0.20), s=(0.145, 0.10))
        self.open_ajar = {}
        import random
        rng = random.Random(11); ajar_ids = {}
        for kind, x, z in draws:
            if (kind, x, z) == ("m", MED_X, MED_Z): continue
            if rng.random() < (0.34 if kind != "s" else 0.16): ajar_ids[(kind, x, z)] = rng.uniform(0.08, 0.20) if kind != "s" else rng.uniform(0.05, 0.12)
        def front(B, kind, x, z, pull=0.0, full=False):
            w, h = S[kind]
            B.box("drawer", (x, -pull, z), (w - 0.012, 0.03, h - 0.012)); B.box("brass", (x, -pull - 0.021, z + h * 0.1), (min(0.1, w * 0.4), 0.012, 0.012))
            B.box("cardedge", (x, -pull - 0.017, z - h * 0.18), (w * 0.4, 0.004, h * 0.22))
        def drawer_body(B, kind, x, z, pull, cards=True):
            w, h = S[kind]; dp = 0.36 if kind != "s" else 0.22
            B.box("oak", (x, -pull + dp / 2 + 0.015, z - h / 2 + 0.01), (w - 0.03, dp, 0.012)); B.box("oak", (x - w / 2 + 0.015, -pull + dp / 2 + 0.015, z), (0.012, dp, h - 0.04)); B.box("oak", (x + w / 2 - 0.015, -pull + dp / 2 + 0.015, z), (0.012, dp, h - 0.04))
            B.box("oak", (x, -pull + dp + 0.015, z), (w - 0.03, 0.012, h - 0.04))
            if cards:
                n = 6 if kind != "s" else 4
                for k in range(n):
                    yy = -pull + 0.07 + k * (0.04 if kind != "s" else 0.03); ch = h * 0.78
                    B.box("paper", (x, yy, z - h / 2 + 0.02 + ch / 2), (w - 0.06, 0.006, ch)); B.box("oxblood", (x - (w - 0.06) * (0.25 if k % 2 else -0.15), yy, z - h / 2 + 0.02 + ch + 0.008), (0.03, 0.006, 0.02))
        def static(B):
            for kind, x, z in draws:
                if (kind, x, z) == ("m", MED_X, MED_Z): continue
                pull = ajar_ids.get((kind, x, z), 0.0)
                if (kind, x, z) in ajar_ids: drawer_body(B, kind, x, z, pull)
                front(B, kind, x, z, pull)
            for z in (0.045, 0.225): pass
        build("dr19", static, self.r19, ink=0.0022)
        # the medium drawer that takes the card: separate group, travel 0.34
        self.med = new_root("med"); self.med.location = (X0, Yc, 0.0)
        def med(B):
            drawer_body(B, "m", MED_X, MED_Z, 0.0, cards=False); front(B, "m", MED_X, MED_Z, 0.0)
            for k in range(5):                                       # the cards already in it, a gap left at the front for the new one
                yy = 0.17 + k * 0.035; ch = 0.15
                B.box("paper", (MED_X, yy, MED_Z - 0.1 + 0.02 + ch / 2), (0.24, 0.006, ch)); B.box("oxblood", (MED_X + (0.06 if k % 2 else -0.04), yy, MED_Z - 0.1 + 0.02 + ch + 0.008), (0.03, 0.006, 0.02))
        build("dm19", med, self.med, ink=0.0022)
        # the card being filed + its glove
        self.card19 = new_root("card19")
        def newcard(B):
            B.box("paper", (0, 0, 0.0), (0.24, 0.006, 0.15)); B.box("oxblood", (-0.06, 0, 0.083), (0.03, 0.006, 0.02))
            for x in (-0.07, 0.0): B.box("dark", (x, -0.004, 0.025), (0.05, 0.002, 0.06)); B.box("cream", (x, -0.0055, 0.025), (0.04, 0.002, 0.05))
        build("nc19", newcard, self.card19, ink=0.0016)
        self.glove19 = new_root("glove19")
        def g19(B):
            glove_fist(B, (0, -0.03, 0.0), 1.15); sleeve(B, (0.03, -0.02, 0.03), (0.40, 0.10, 0.50))
        build("gl19", g19, self.glove19, ink=0.0022)
        self.group19 = [self.r19, self.med, self.card19, self.glove19]

    def pose_19(self, g):
        X0, Yc = CAB; f = bf(g)
        TR = 0.34                                                       # medium drawer travel
        zt = MED_Z + 0.10                                              # top rim of the open drawer
        kloc(self.r19, f, (X0, Yc, 0.0))
        if g < 1022: pull = TR
        else: pull = TR * (1.0 - sm(t_of(g, 1022, 1032)))
        kloc(self.med, f, (X0, Yc - pull, 0.0))
        # the card: held above the drawer, lowered into the slot behind the front panel, gone from g1013
        slot_y = -TR + 0.10
        if g < 1000: u = t_of(g, 996, 1000); cx = lerp(0.28, 0.0, sm(u)); cz = zt + lerp(0.24, 0.14, sm(u))
        elif g < 1012: u = t_of(g, 1000, 1012); cx = 0.0; cz = lerp(zt + 0.14, MED_Z - 0.14, sm(u))
        else: cx = 0.0; cz = MED_Z - 0.16
        card_on = g < 1013
        kloc(self.card19, f, (X0 + MED_X + cx, Yc + slot_y, cz)); kvis([self.card19], f, card_on)
        # the glove: holds the card top (centre) until it is down, then lifts away up-right; later pushes the drawer front shut
        if g < 1013:
            gx, gy, gz = X0 + MED_X + cx, Yc + slot_y - 0.02, cz + 0.105
        elif g < 1022:
            u = t_of(g, 1013, 1022); gx = X0 + MED_X + lerp(0.0, 0.32, sm(u)); gy = Yc + slot_y - 0.04; gz = zt + 0.02 + lerp(0.0, 0.28, sm(u))
        else:
            u = t_of(g, 1022, 1032); gx = X0 + MED_X + lerp(0.30, 0.0, sm(u)); gz = lerp(zt + 0.30, MED_Z + 0.02, sm(u)) if u < 0.5 else MED_Z + 0.02
            gy = Yc - pull - 0.06 + 0.0; gx = X0 + MED_X + (0.0 if u > 0.5 else lerp(0.30, 0.0, sm(u * 2)))
        kloc(self.glove19, f, (gx, gy, gz))
        glove_on = g < 1040
        kvis([self.glove19], f, glove_on)

    # ---- 18a ear insert (puppet cast, the s01 S3A setup)
    def build_18a_actors(self):
        self.acts = {}
        self.acts["pb"] = self.make_actor("pb", "prisoner_b", os.path.join(TMP, "sprites_" + self.q))
        self.acts["bert"] = self.make_actor("bert", "bertillon", os.path.join(TMP, "sprites_" + self.q))
        a = self.acts["pb"]
        a.jobs = (lambda orig: (lambda px, frames=None, overlay=None: [dict(j, underlay=ears_svg(j["pose"])[0], overlay=ears_svg(j["pose"])[1]) for j in orig(px, frames, overlay)]))(a.jobs)
        self.ear = {}

    def pose_18a(self, gs):
        cam = self.cam; CH = (0.70, 2.30)
        sc = {n: K.CAST_H[v] / K.CAST_HD[v] for n, v in (("pb", "prisoner_b"), ("bert", "bertillon"))}
        pb_pose = dict(cast17.STORY17["prisoner_sitting_b"][1]); pb_pose["seat17"] = None
        fx, fy = C.sprites.feet_of("prisoner_b", pb_pose); zpb = K.HEAD_Z["chair"] - sc["pb"] * fy
        for g in gs:
            f = bf(g); self.acts["pb"].place(f, (CH[0], CH[1] - 0.14, zpb), scale=sc["pb"]); self.acts["bert"].place(f, (0.30, 2.42, 0.0), scale=sc["bert"])
            C.vis(self.acts["pb"], f, True); C.vis(self.acts["bert"], f, True)
        for g in gs:
            f = bf(g); self.scene.frame_set(f); t = g / 30.0
            p = dict(pb_pose); p.update(yaw=0.88, pitch=0.0, expr="unimpressed", mouth="flat", gaze=(0.9, 0.05), head_roll=1.5 * math.sin(t * 2.1), blink=cast17.blink_at(g, 70, 11))
            p["squash"] = (1.0 + 0.008 * math.sin(t * 2.4), 1.0 - 0.008 * math.sin(t * 2.4))
            self.acts["pb"].pose(f, cast17.silent(p), camera=cam)
        self.sprites_for_all(self.acts["pb"], [bf(g) for g in gs])
        for g in gs:
            f = bf(g); self.scene.frame_set(f); t = g / 30.0
            an = self.anch[("pb", f)]; hx, hy = an["head"]
            ex = hx - 0.52 * math.cos(math.radians(min(0.88, 1.2) * 70.0))
            el = (ex + 0.004 * math.sin(g * 0.8), hy + 0.02)
            w = actors.local_to_world(self.acts["pb"], el, f, camera=cam)
            bp = dict(cast17.STORY17["bertillon_measuring"][1]); bp.update(lean=4 + 1.5 * math.sin(t * 2.1), pitch=0.22, yaw=0.62, gaze=(1.0, 0.25), blink=cast17.blink_at(g, 90, 30), t=t)
            self.acts["bert"].pose(f, cast17.silent(bp), hands={"r": {"tip": w, "prop": "calipers", "angle": -4, "prop_scale": 0.8, "stretch": 1.15}}, camera=cam)
        self.sprites_for_all(self.acts["bert"], [bf(g) for g in gs], hand=True)

    def sprites_for_all(self, a, frames, hand=False):
        base = 128 if self.q == "draft" else 256
        self.sprites_for(a, base * 2, frames)
        if hand:
            ov = lambda f, pose: glove_svg(self.anch[("bert", f)])
            a.render_sprites(base * 2, frames=frames, overlay=ov)


# ------------------------------------------------------------------ puppet bits (ears, glove overlay, jaw slide) -- as in s01
SLIDE = [0.50]
def _calipers_body(k):
    c17 = cast17; dx = SLIDE[0] - 0.46
    g = c17._lin(k, "cb", c17.STEEL["light"], c17.STEEL["base"], c17.STEEL["dark"], 0, -0.05, 0, 0.05)
    o = ['<path d="M-0.12,-0.034 L0.88,-0.034 L0.88,0.034 L-0.12,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    tk = "".join("M%.3f,0.034 L%.3f,%.3f " % (x, x, 0.034 + (0.034 if i % 5 == 0 else 0.020)) for i, x in enumerate([0.02 + 0.04 * j for j in range(20)]))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" fill="none"/>' % (tk, k.c(c17.STEEL["deep"])))
    o.append('<path d="M-0.08,-0.018 L0.84,-0.018" stroke="#ffffff" stroke-width="0.008" opacity="0.7" stroke-linecap="round"/>')
    o.append('<path d="M0.80,0.030 L0.88,0.030 L0.88,0.30 L0.835,0.33 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(c17.STEEL["base"]), k.ink))
    o.append('<path d="M%.3f,-0.050 L%.3f,-0.050 L%.3f,0.30 L%.3f,0.33 L%.3f,0.034 L%.3f,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
             % (0.40 + dx, 0.52 + dx, 0.52 + dx, 0.485 + dx, 0.46 + dx, 0.40 + dx, k.c(c17.STEEL["light"]), k.ink))
    o.append('<circle cx="%.3f" cy="-0.075" r="0.036" fill="%s" stroke="%s" stroke-width="0.014"/>' % (0.46 + dx, k.c(c17.BRASS["base"]), k.ink))
    return "".join(o)
cast17._calipers_body = _calipers_body
_orig_svg = C.sprites.sprite_svg
def _svg(cast, pose, *a, **kw):
    g = (pose or {}).get("t", None)
    if g is not None and cast == "bertillon": SLIDE[0] = lerp(0.28, 0.50, ez((g * 30 - 950) / 10.0))     # jaws close g950..960
    return _orig_svg(cast, pose, *a, **kw)
C.sprites.sprite_svg = _svg

def ears_svg(pose):
    yw = pose.get("yaw", 0.0); r = pose.get("head_roll", 0.0); dx = pose.get("head_dx", 0.0); dy = pose.get("head_dy", 0.0)
    ink, fill = "#3a2832", "#f4d4cb"; th = math.radians(min(abs(yw), 1.2) * 70.0); c = math.cos(th); prof = abs(yw) > 0.5
    def ear(x, big):
        rx, ry = (0.19, 0.27) if big else (0.15, 0.25)
        return ('<g transform="translate(%.3f 0)"><ellipse cx="0" cy="0.02" rx="%.3f" ry="%.3f" fill="%s" stroke="%s" stroke-width="0.035"/>'
                '<path d="M-0.05,-0.13 C0.05,-0.15 0.11,0.02 0.03,0.14" fill="none" stroke="%s" stroke-width="0.03" stroke-linecap="round"/></g>' % (x, rx, ry, fill, ink, ink))
    under = (ear(0.52 * c, False) + ear(-0.52 * c, False)) if not prof else ear(0.52 * c, False)
    over = ear(-0.52 * c, True) if prof else ""
    wrap = lambda g: '<g transform="rotate(%.2f %.3f %.3f) translate(%.3f %.3f)">%s</g>' % (r, dx, dy, dx, dy, g) if g else ""
    return wrap(under), wrap(over)

def glove_svg(an):
    """a gloved hand + navy forearm with a white cuff gripping the caliper bar (puppet-local D, from the sprite's own anchors)."""
    ex, ey = an["elbow_r"]; hx, hy = an["hand_r"]
    dx, dy = hx - ex, hy - ey; L = math.hypot(dx, dy) or 1.0; ux, uy = dx / L, dy / L
    cx, cy = hx - ux * 0.13, hy - uy * 0.13
    return ('<g><path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.17" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#35487a" stroke-width="0.125" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.155" stroke-linecap="butt" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#fbf3ee" stroke-width="0.115" stroke-linecap="butt" fill="none"/>'
            '<ellipse cx="%.3f" cy="%.3f" rx="0.125" ry="0.105" fill="#e9e0cb" stroke="#3a2832" stroke-width="0.03"/>'
            '<path d="M%.3f,%.3f q0.04,0.02 0.0,0.07 M%.3f,%.3f q0.04,0.02 0.0,0.07 M%.3f,%.3f q0.04,0.02 0.0,0.07" stroke="#3a2832" stroke-width="0.016" fill="none"/></g>'
            % (ex, ey, hx, hy, ex, ey, hx, hy, cx - ux * 0.045, cy - uy * 0.045, cx + ux * 0.045, cy + uy * 0.045,
               cx - ux * 0.045, cy - uy * 0.045, cx + ux * 0.045, cy + uy * 0.045, hx, hy, hx - 0.05, hy - 0.04, hx - 0.01, hy - 0.04, hx + 0.03, hy - 0.04))

# ------------------------------------------------------------------ cameras
def LT(lx, ly, z):
    """table-local (x right on screen, y away from the camera) -> world; the table inserts are turned +90 deg so the camera looks at the window wall."""
    return (TBL[0] - ly, TBL[1] + lx, z)

def LF(lx, ly, z): return (FB[0] - ly, FB[1] + lx, z)

def cam_of(g):
    s = shot_of(g)
    if s == "17a":
        u = lin(t_of(g, 900, 923)); a = (LT(-0.02, -0.31, Z0 + 0.15), LT(0.0, 0.03, Z0 + 0.05)); b = (LT(0.06, -0.26, Z0 + 0.12), LT(0.04, 0.03, Z0 + 0.05))
    elif s == "17b":
        u = lin(t_of(g, 924, 947)); a = (LF(-0.06, -0.26, 0.22), LF(0.04, 0, 0.09)); b = (LF(0.08, -0.22, 0.19), LF(0.09, 0, 0.09))
    elif s == "18a":
        u = lin(t_of(g, 948, 971)); a = ((-0.58, 1.46, 1.02), (0.58, 2.20, 1.24)); b = ((-0.30, 1.66, 1.05), (0.70, 2.20, 1.24))
    elif s == "18b":
        u = lin(t_of(g, 972, 995)); a = (LT(0.05, -0.27, Z0 + 0.24), LT(0.10, 0.0, Z0 + 0.01)); b = (LT(0.14, -0.22, Z0 + 0.20), LT(0.12, 0.0, Z0 + 0.01))
    else:
        X0, Yc = CAB
        u = lin(t_of(g, 996, 1051), 0.3)
        a = ((X0 + 0.32, Yc - 0.80, 1.14), (X0 + MED_X + 0.02, Yc, 0.93)); b = ((X0 + 0.10, Yc - 2.25, 1.36), (X0 - 0.02, Yc, 1.02))
        if g < 1022: u = lin(t_of(g, 996, 1022), 0.5) * 0.12
        else: u = 0.12 + 0.88 * sm(t_of(g, 1022, 1051))
    return mix(a[0], b[0], u), mix(a[1], b[1], u)

# ------------------------------------------------------------------ driver
def pose_all(T, gs):
    gs = list(gs)
    for g in gs:
        f = bf(g); T.key_cam(f, *cam_of(g))
        K.set_flicker(1.0, frame=f); K.set_dust(0.3, frame=f); K.set_smoke(1.0, frame=f); K.set_pendulum(frame=f)
        s = shot_of(g)
        for tag, L in T.lamps: L.hide_render = tag != s; L.keyframe_insert("hide_render", frame=f)
        for key, grp in (("17a", T.group17a), ("17b", T.group17b), ("18b", T.group18b), ("19", T.group19)):
            kvis(list(grp), f, s == key)
        if s != "18a":
            for a in T.acts.values(): C.vis(a, f, False)
    for g in gs:
        s = shot_of(g)
        if s == "17a": T.pose_17a(g)
        elif s == "17b": T.pose_17b(g)
        elif s == "18b": T.pose_18b(g)
        elif s == "19": T.pose_19(g)
    g18 = [g for g in gs if shot_of(g) == "18a"]
    if g18: T.pose_18a(g18)

def report(T, g):
    loc, look = cam_of(g); return dict(g=g, shot=shot_of(g), cam=[round(c, 3) for c in loc])

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        os.makedirs(out, exist_ok=True)
        T = Scene("draft" if scale < 1 else "final"); pose_all(T, gs)
        for g in gs:
            print(json.dumps(report(T, g)), flush=True)
            st = T.render([bf(g)], out, scale, samples)[0]; K.grade(st["path"], scale=scale); os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 16
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        T = Scene("draft" if scale < 1 else "final")
        for i in range(0, len(todo), 12):
            ch = todo[i:i + 12]; pose_all(T, ch)
            for g in ch:
                st = T.render([bf(g)], out, scale, samples)[0]; K.grade(st["path"], scale=scale)
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g", g, round(st["wall"], 1), flush=True)
