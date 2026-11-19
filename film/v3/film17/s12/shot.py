#!/usr/bin/env python3
"""shot.py -- film 17 take s12 = shots 29 + 30 (g 1695..1867 + 6 handle frames each side: first_g 1689, last 1873).
   29 (g 1689..1788) records_low / DAY_INT: Bertillon holds the card up (proud); behind him dupont in a FAKE BEARD dissolves to clean-shaven
      (the card is a prop in his hand: it never changes).  Slow push + lateral slide + one reframe snap.
   30 (g 1789..1873) records_aisle / DAY_INT: high crane pull-out; drawers open one after another, 200+ cards pop up along the aisle, gendarmes
      bring more thieves.
   python3 shot.py stills 29|30 a:b[:step] out_dir [draft|final] [samples]
   python3 shot.py final 29|30 out_dir [draft|final] [samples] [threads]"""
import math, os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import K, bpy, Vector, actors, camrig, cast17, lerp, clamp, ez, blink
TMP = os.path.join(HERE, "work")
RANGES = {29: (1689, 1788), 30: (1789, 1874)}
PRESET = {29: "records_low", 30: "records_aisle"}
PPD = {29: 192, 30: 128}

def smooth(x): x = clamp(x); return x * x * (3 - 2 * x)
def snap(g, g0, n):             # 0 -> 1 over n frames starting g0 (fast eased)
    return smooth((g - g0) / float(n))

# ----------------------------------------------------------------------------- cameras
def cam29(g):
    t = (g - 1695) / 94.0
    P0 = Vector((0.05, -0.8, 0.55)); L0 = Vector((-0.75, 6.0, 2.85))
    fwd = Vector((0.12, 1.0, 0.02)).normalized()
    u = 0.15 * smooth(t) + 0.85 * t
    s = snap(g, 1730, 14)                         # reframe snap: slide right + look shift
    P = P0 + fwd * (1.15 * u) + Vector((0.55 * s - 0.12 * t, 0, 0.18 * t))
    L = L0 + Vector((0.35 * s + 0.15 * t, 0.2 * t, -0.1 * s))
    return P, L

def cam30(g):
    t = (g - 1789) / 84.0
    P0 = Vector((0.55, 1.4, 3.0)); L0 = Vector((-0.1, 8.0, 1.8))
    P1 = Vector((0.75, -3.4, 4.1)); L1 = Vector((-0.2, 6.5, 2.0))
    u = 0.3 * smooth(t) + 0.7 * t
    s = snap(g, 1822, 14)                         # mid snap: swing left and tilt
    P = P0 + (P1 - P0) * u + Vector((-0.5 * s + 0.5 * smooth((g - 1850) / 14.0), 0, 0))
    L = L0 + (L1 - L0) * u + Vector((-0.7 * s + 0.7 * smooth((g - 1850) / 14.0), 0.5 * s, -0.2 * s))
    return P, L

CAMF = {29: cam29, 30: cam30}

# ----------------------------------------------------------------------------- cast
def idle(g, k=0.0):
    return dict(lean=1.5 * math.sin(g * 0.09 + k), head_roll=2.0 * math.sin(g * 0.13 + k * 2))

class Take(object):
    def __init__(self, shot, mode):
        self.shot = shot; self.mode = mode
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.A = K.build(preset=PRESET[shot]); self.scene = bpy.context.scene; self.cam = self.scene.camera
        K.clear_keys()
        self.sd = os.path.join(TMP, "sprites_%d" % shot); os.makedirs(self.sd, exist_ok=True)
        self.acts = []
        getattr(self, "setup%d" % shot)()

    def add(self, name, cast, who, mark, dx=0.0, dy=0.0, dz=0.0):
        a = C.make_actor(name, cast, who, self.sd); a.mark = mark; a.d = (dx, dy, dz); a.sc = C.scale_of(who); self.acts.append(a); return a

    # ---- shot 29
    def setup29(self):
        self.ber = self.add("ber", "bertillon", "bertillon", "low_a", dx=-0.25)
        self.dfb = self.add("dfb", "dupont_fb", "dupont", "wall_look", dx=-0.8, dy=-0.03)
        self.dcl = self.add("dcl", "dupont", "dupont", "wall_look", dx=-0.8)
        self.fn_fb = C.fade_setup(self.dfb)
        self.dcl_cast = "dupont"

    # ---- shot 30
    def setup30(self):
        self.ber = self.add("ber", "bertillon", "bertillon", "ladder_foot")
        self.g1 = self.add("g1", "gendarme_a", "gendarme_a", "aisle2", dx=0.35)
        self.p1 = self.add("p1", "prisoner_a", "prisoner_a", "aisle2", dx=-0.45, dy=0.1)
        self.g2 = self.add("g2", "gendarme_b", "gendarme_b", "aisle1", dx=-0.35)
        self.p2 = self.add("p2", "prisoner_b", "prisoner_b", "aisle1", dx=0.45, dy=0.1)
        self.g3 = self.add("g3", "gendarme_a", "gendarme_a", "aisle_far", dx=0.5)
        self.p3 = self.add("p3", "prisoner_c", "prisoner_c", "aisle_far", dx=-0.3)
        self.make_cards()

    def make_cards(self):
        """14 drawers x 16 cards = 224 cream cards that pop out of the opened drawers and hover (a swarm along the aisle)."""
        from bertillon import STATE, Batch
        B = Batch(5); B.box("cream", (0, 0, 0), (0.30, 0.004, 0.20)); B.box("oxblood", (-0.09, -0.003, 0.108), (0.07, 0.004, 0.02)); B.box("navy", (0.06, -0.003, 0.0), (0.10, 0.004, 0.10))
        protos = B.finalize("popcard", ink_t=0.0)
        rng = random.Random(30); self.drawers = [n for n in sorted(STATE["anim"]) if n[0] in "pq" and n[1:].isdigit()]
        self.cards = []; self.dstart = {}
        for di, n in enumerate(self.drawers):
            a = STATE["anim"][n]; self.dstart[n] = (1789 + 3 + di * 4, a["slide"].location.y / a["travel"])
            for k in range(16):
                root = bpy.data.objects.new("pc_%s_%d" % (n, k), None); bpy.context.scene.collection.objects.link(root)
                for pr in protos:
                    o = pr.copy(); o.data = pr.data; bpy.context.scene.collection.objects.link(o); o.parent = root; o.visible_shadow = False; o.visible_glossy = False
                    o.matrix_parent_inverse = o.parent.matrix_world.inverted() if False else o.matrix_parent_inverse
                self.cards.append(dict(root=root, drawer=n, k=k, t0=self.dstart[n][0] + 4 + k * 1.3, side=1 if n[0] == "p" else -1,
                                       off=(rng.uniform(0.15, 1.0), rng.uniform(-1.0, 1.0), rng.uniform(0.3, 2.8)), yaw=rng.uniform(-35, 35), roll=rng.uniform(-14, 14), ph=rng.uniform(0, 6.3)))
        for pr in protos: pr.hide_render = True; pr.hide_viewport = True

    def key_cards(self, f):
        from bertillon import STATE
        for c in self.cards:
            a = STATE["anim"][c["drawer"]]; mw = a["root"].matrix_world; trav = a["travel"]
            mouth = mw @ Vector((0, trav * 1.0 + 0.05, 0.0)); u = clamp((f - c["t0"]) / 11.0)
            r = c["root"]
            if u <= 0: r.hide_render = True; r.scale = (0.01,) * 3; r.location = mouth
            else:
                e = ez(u, "out") if False else smooth(u)
                tx = mouth.x - c["side"] * c["off"][0]; ty = mouth.y + c["off"][1]; tz = mouth.z + c["off"][2]
                bob = 0.03 * math.sin(f * 0.17 + c["ph"])
                arc = 0.25 * math.sin(math.pi * u)
                r.location = (lerp(mouth.x, tx, e), lerp(mouth.y, ty, e), lerp(mouth.z, tz, e) + arc + bob)
                s = 1.0 * e; r.scale = (s, s, s); r.hide_render = False
                r.rotation_euler = (0, math.radians(c["roll"] + 20 * (1 - e)), math.radians(c["yaw"] + 180 * (1 - e) * 0 + 40 * (1 - e)))
            r.keyframe_insert("location", frame=f); r.keyframe_insert("scale", frame=f); r.keyframe_insert("rotation_euler", frame=f); r.keyframe_insert("hide_render", frame=f)

    # ---- per-frame keying
    def key_frames(self, gs):
        for g in gs:
            P, Lk = CAMF[self.shot](g); camrig.key_camera(g, P, Lk, cam=self.cam, interp="LINEAR", easing="AUTO")
            K.key_life(g, g)
            for a in self.acts:
                x, y, z, fz, who = self.A["marks"][a.mark]; sc = a.sc
                bob = 0.0
                a.place(g, (x + a.d[0], y + a.d[1], z + a.d[2]), scale=sc)
            if self.shot == 30:
                for n in self.drawers:
                    g0, d0 = self.dstart[n]; K.set_drawer(n, lerp(d0, 1.0, smooth((g - g0) / 8.0)), frame=g)
                self.key_cards(g)
            else:
                u = smooth((g - 1722) / 34.0)
                C.key_fade(self.dfb, self.fn_fb, g, 1.0 - u)
        for g in gs:
            self.scene.frame_set(g)
            for a in self.acts:
                cn, p = self.pose_for(a, g); a.cast = cn if a.cast != cn else a.cast
                a.pose(g, p, camera=self.cam)
        for a in self.acts:
            for g, r in zip(gs, a.render_sprites(PPD[self.shot], frames=gs)): pass

    def pose_for(self, a, g):
        k = hash(a.name) % 7
        if a is getattr(self, "ber", None):
            if self.shot == 29:
                u = smooth((g - 1689) / 30.0)
                c, p = C.pose_of("bertillon_holding_card", expr="proud")
                p.update(idle(g, k)); p["arm_r"] = dict(p["arm_r"], hand=(0.66 + 0.03 * math.sin(g * 0.2), lerp(0.42, 0.06, u) + 0.03 * math.sin(g * 0.27)))
                p["pitch"] = -0.15 - 0.25 * u; p["blink"] = blink(g, [1706, 1750, 1781]); return c, p
            c, p = C.pose_of("bertillon_pointing"); p.update(idle(g, k)); p["blink"] = blink(g, [1810, 1850]); return c, p
        if a in (getattr(self, "dfb", None), getattr(self, "dcl", None)):
            cn = a.cast; _, p = C.pose_of("dupont_innocent", cast=cn); p.update(idle(g, k)); p["blink"] = blink(g, [1700, 1742, 1775]); return cn, p
        story = {"g1": "gendarme_escort_a", "g2": "gendarme_escort_b", "g3": "gendarme_laughing_a", "p1": "prisoner_standing_a", "p2": "prisoner_standing_b", "p3": "prisoner_standing_c"}[a.name]
        c, p = C.pose_of(story, mirror=(a.name == "g1")); p.update(idle(g, k)); p["blink"] = blink(g, [1800 + 7 * k, 1845 + 3 * k]); return c, p

    def render(self, gs, out, mode, samples):
        return C.render_frames(self.scene, self.cam, gs, out, mode, samples)

def parse(s):
    a = s.split(":"); st = int(a[2]) if len(a) > 2 else 1; return list(range(int(a[0]), int(a[1]) + 1, st))

if __name__ == "__main__":
    cmd, shot = sys.argv[1], int(sys.argv[2])
    if cmd == "stills":
        gs = parse(sys.argv[3]); out = sys.argv[4]; mode = sys.argv[5] if len(sys.argv) > 5 else "draft"; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 8
        T = Take(shot, mode); T.key_frames(gs); T.render(gs, out, mode, samples)
    else:
        out = sys.argv[3]; mode = sys.argv[4]; samples = int(sys.argv[5]); gs = list(range(RANGES[shot][0], RANGES[shot][1] + 1))
        if len(sys.argv) > 6: gs = parse(sys.argv[6])
        T = Take(shot, mode); T.key_frames(gs); T.render(gs, out, mode, samples)
