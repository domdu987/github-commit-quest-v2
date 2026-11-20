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
    u = 0.1 * smooth(t) + 0.9 * t
    s1 = snap(g, 1708, 10); s2 = snap(g, 1740, 10); s3 = snap(g, 1768, 10)
    P = P0 + fwd * (1.2 * u) + Vector((0.42 * s1 - 0.42 * s2 + 0.34 * s3 + 0.35 * t, 0, 0.18 * t + 0.06 * s2))
    L = L0 + Vector((0.25 * s1 - 0.25 * s2 + 0.2 * s3 + 0.3 * t, 0.2 * t, -0.08 * s1 + 0.1 * s2))
    return P, L

def cam30(g):
    t = (g - 1789) / 84.0
    P0 = Vector((0.55, 1.4, 3.0)); L0 = Vector((-0.1, 8.0, 1.8))
    P1 = Vector((0.75, -1.8, 3.7)); L1 = Vector((-0.2, 6.5, 2.0))
    u = 0.45 * smooth(t) + 0.55 * t
    s = snap(g, 1822, 14)                         # mid snap: swing left and tilt
    s4 = snap(g, 1800, 12) - snap(g, 1812, 12); s5 = snap(g, 1862, 10)
    P = P0 + (P1 - P0) * u + Vector((-0.5 * s + 0.5 * smooth((g - 1850) / 14.0) + 0.3 * s4 - 0.3 * s5, 0, 0))
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
        self.ber = self.add("ber", "bertillon", "bertillon", "low_a", dx=-0.3)
        for o in bpy.data.objects:
            if o.name.startswith("fg"): o.hide_render = True
        self.dfb = self.add("dfb", "dupont_fb", "dupont", "wall_look", dx=0.55, dy=-0.33)
        self.dcl = self.add("dcl", "dupont", "dupont", "wall_look", dx=0.55, dy=-0.30)
        self.fn_fb = C.fade_setup(self.dfb)
        self.dcl_cast = "dupont"

    # ---- shot 30
    def setup30(self):
        self.ber = self.add("ber", "bertillon", "bertillon", "aisle1", dx=-0.3)
        # escort pairs (gendarme leads a thief by the arm), three entries staggered: (gendarme, thief, lane x, y end, start g, end g, y start)
        spec = [("a", "gendarme_a", "prisoner_a", 0.55, 6.2, 1789, 1834, 9.0), ("b", "gendarme_b", "prisoner_b", 0.25, 7.2, 1801, 1848, 13.0), ("c", "gendarme_a", "prisoner_c", 0.62, 8.4, 1813, 1862, 13.5)]
        self.WALK = {}
        for tag, gc, pc, lx, ye, g0, g1, ys in spec:
            ga = self.add("g" + tag, gc, gc, "aisle2", dx=lx - 0.5 + 0.33); pa = self.add("p" + tag, pc, pc, "aisle2", dx=lx - 0.5 - 0.33)
            for a in (ga, pa): a.d = (a.d[0], ye - 5.4, 0.0); self.WALK[a.name] = (ys - ye, g0, g1)
            if tag != "a":
                for a in (ga, pa): a.fnode = C.fade_setup(a); a.appear = g0
        self.fade_actors = [a for a in self.acts if hasattr(a, "fnode")]
        self.make_cards()

    def make_cards(self):
        """3 true-size mugshot cards (0.14 x 0.094 m, the hero-card texture) per opened drawer: each pops up out of its drawer in turn, far to near."""
        from bertillon import STATE
        names = [n for n in sorted(STATE["anim"]) if n[0] in "pq" and n[1:].isdigit()]
        ys = {n: STATE["anim"][n]["root"].location.y for n in names}
        self.drawers = sorted(names, key=lambda n: -ys[n]); self.cards = []; self.dstart = {}
        rng = random.Random(30)
        for di, n in enumerate(self.drawers):
            a = STATE["anim"][n]; self.dstart[n] = (1795 + di * 5, a["slide"].location.y / a["travel"])
            for k in range(3):
                r = K.card_plane("pc_%s_%d" % (n, k), (0, 0, 0), (0.34, 0.23), key="card_bertillon")
                self.cards.append(dict(root=r, drawer=n, k=k, t0=self.dstart[n][0] + 7 + k * 3, yaw=rng.uniform(-12, 12), pitch=rng.uniform(8, 18)))

    def key_cards(self, f):
        from bertillon import STATE
        for c in self.cards:
            a = STATE["anim"][c["drawer"]]; mw = a["root"].matrix_world; r = c["root"]; g0, d0 = self.dstart[c["drawer"]]; op = lerp(d0, 1.0, smooth((f - g0) / 8.0))
            u = clamp((f - c["t0"]) / 9.0); e = smooth(u)
            p = mw @ Vector((0.0, op * a["travel"] - 0.12 - 0.07 * c["k"], 0.12 + 0.12 * e))
            r.location = p; r.hide_render = u <= 0
            r.rotation_euler = (math.radians(c["pitch"]), 0, math.radians(180 + c["yaw"]))
            r.scale = (max(e * (1 + 0.35 * math.sin(math.pi * u)), 0.01),) * 3
            r.keyframe_insert("location", frame=f); r.keyframe_insert("scale", frame=f); r.keyframe_insert("rotation_euler", frame=f); r.keyframe_insert("hide_render", frame=f)

    # ---- per-frame keying
    def key_frames(self, gs):
        for g in gs:
            P, Lk = CAMF[self.shot](g); camrig.key_camera(g, P, Lk, cam=self.cam, interp="LINEAR", easing="AUTO")
            K.key_life(g, g, dust=0.45)
            for a in self.acts:
                x, y, z, fz, who = self.A["marks"][a.mark]; sc = a.sc
                bob = 0.0
                dy = self.walk_dy(a, g)
                a.place(g, (x + a.d[0], y + a.d[1] + dy, z + a.d[2] + (0.02 * abs(math.sin(g * 0.36 + sum(map(ord, a.name)) % 5)) if self.shot == 30 and dy > 0.02 else 0.0)), scale=sc)
            if self.shot == 30:
                for a in self.fade_actors: C.key_fade(a, a.fnode, g, smooth((g - a.appear + 2) / 8.0))
                for n in self.drawers:
                    g0, d0 = self.dstart[n]; K.set_drawer(n, lerp(d0, 1.0, smooth((g - g0) / 8.0)), frame=g)
                bpy.context.view_layer.update(); self.key_cards(g)
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

    def walk_dy(self, a, g):
        if self.shot != 30 or a.name not in self.WALK: return 0.0
        d, g0, ge = self.WALK[a.name]; return d * (1.0 - smooth((g - g0) / float(ge - g0)))
    def walk_w(self, a, g):
        if self.shot != 30 or a.name not in self.WALK: return 0.0
        ge = self.WALK[a.name][2]; return 1.0 if g < ge - 8 else clamp(1.0 - (g - (ge - 8)) / 8.0)

    def pose_for(self, a, g):
        k = sum(map(ord, a.name)) % 7
        if a is getattr(self, "ber", None):
            if self.shot == 29:
                u = smooth((g - 1689) / 30.0)
                c, p = C.pose_of("bertillon_holding_card", expr="proud", mirror=True)
                p["prop_r"] = dict(p["prop_r"], scale=2.1)
                p.update(idle(g, k)); p["arm_r"] = dict(p["arm_r"], hand=(0.66 + 0.03 * math.sin(g * 0.2), lerp(0.42, 0.06, u) + 0.03 * math.sin(g * 0.27)))
                p["pitch"] = -0.15 - 0.25 * u; p["blink"] = blink(g, [1706, 1750, 1781]); return c, p
            c, p = C.pose_of("bertillon_pointing"); p.update(idle(g, k)); p["arm_r"] = dict(p["arm_r"], hand=(1.05 + 0.04 * math.sin(g * 0.3), 0.18 - 0.12 * math.sin(g * 0.15) ** 2)); p["blink"] = blink(g, [1810, 1850]); return c, p
        if a in (getattr(self, "dfb", None), getattr(self, "dcl", None)):
            cn = a.cast; _, p = C.pose_of("dupont_innocent", cast=cn); p.update(idle(g, k)); p["blink"] = blink(g, [1700, 1742, 1775]); return cn, p
        gend = a.name[0] == "g"
        story = ("gendarme_escort_a" if a.cast == "gendarme_a" else "gendarme_escort_b") if gend else "prisoner_standing_" + a.cast[-1]
        c, p = C.pose_of(story, mirror=gend, expr="smirk" if gend else "worried")
        p["mouth"] = "flat" if not gend else "smile"
        if not gend: p["sweat"] = 0.6; p["fx"] = ["sweat"]
        p.update(idle(g, k)); p["blink"] = blink(g, [1800 + 7 * k, 1845 + 3 * k])
        w = self.walk_w(a, g)
        if w > 0.02:
            cy = cast17.cycle(c, g / 26.0 + 0.2 * k, "march", base=dict(p), arms="none"); L = dict(cy["legs"])
            for kk in ("stride", "lift_r", "lift_l"): L[kk] = L[kk] * w
            p["legs"] = L; p["lean"] = p.get("lean", 0.0) * (1 - w) + 1.0
        return c, p

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
