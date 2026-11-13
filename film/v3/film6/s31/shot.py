#!/usr/bin/env python3
"""shot.py -- film 6 take s31: shots 31-32 (86.24-94.54 s = g 2587..2835) + 6-frame handles (g 2581..2841), bakery.

    shot 31  g 2587..2714  bakery MORNING / table_insert -- the reveal, "เพราะควันขาว ๆ ที่เด็กเห็นทุกเช้า ไม่ใช่ควัน
             มันคือน้ำในขนมปังที่ระเหยหนีออกมา"
        31a  g 2581..2629  table_insert, slow push over the fresh loaves, full white steam (set_steam 1.0) -- the motif
        31b  g 2630..2672  closer on the front loaf: on "ไม่ใช่ควัน" (88.30 s) the steam thins (1.0 -> 0.25, g 2640..2664)
                           and turns into TINY WATER DROPS (2D droplet cards, clear diagram look: blue drop, white glint,
                           plum ink outline) popping out of the crust and rising, more and more
        31c  g 2673..2714  ECU low on the crust: a column of drops leaving the loaf, three dashed "up" arrows (diagram)
                           pulse up beside it, on "มันคือน้ำในขนมปัง ที่ระเหยหนีออกมา"
    shot 32  g 2715..2835  bakery / small_scale_insert -- "ก้อนที่ชั่งเป๊ะตอนเช้า พอตกบ่ายจึงเบาลงทุกก้อน"
        32a  g 2715..2750  MORNING: the hand balance from behind the counter (street through the opening): the loaf just
                           set down, the beam wobbles and settles LEVEL (g 2735) -- exact at dawn
        32b  g 2751..2792  MORNING: closer on the beam and the loaf pan, level (dissolve out g 2781..2792)
        32c  g 2781..2841  AFTERNOON (same lens, same push continuing; dissolve in g 2781..2792): the same loaf, a few drops
                           drifting off it, and the loaf side of the beam RISES (0 -> -7 deg, g 2796..2826, on
                           "เบาลงทุกก้อน" 93.57 s = g 2810): the weight literally floating away.
    The dissolve is made in deliver.py from two renders (internal shot 32 = MORNING part g 2715..2792, internal shot 33 =
    AFTERNOON part g 2781..2841; the light preset is a different set build).
No people in this take (mouth rule trivially kept).  NO depth of field (C.Take switches it off).

    python3 shot.py probe 31,32 a:b[:step]          (33 needs its own process: AFTERNOON)
    python3 shot.py stills 31 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 31 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")
INK = "#3a2832"

# ----------------------------------------------------------------------------- timing
G0, G1 = C.g_bound(86.24), C.g_bound(94.54)     # 2587, 2836
G32 = C.g_bound(90.50)                          # 2715
H = 6
DIS = (2781, 2792)                              # dissolve morning -> afternoon (12 frames, both sides rendered)
RANGES = {31: (G0 - H, G32 - 1), 32: (G32, DIS[1]), 33: (DIS[0], G1 - 1 + H)}
CUT_A, CUT_B = 2630, 2673                       # 31a | 31b | 31c
CUT_32 = 2751                                   # 32a | 32b
STEAM_FADE = (2640, 2664)
DROP_START = 2638
TILT = (2796, 2826)                             # afternoon: 0 -> -7 (loaf side up)


def framing(shot, g):
    if shot == 31:
        return "31a" if g < CUT_A else ("31b" if g < CUT_B else "31c")
    if shot == 32:
        return "32a" if g < CUT_32 else "32b"
    return "32c"


def bf(shot, g):
    return {31: 0, 32: 2000, 33: 4000}[shot] + int(g) - 2500


# ----------------------------------------------------------------------------- cameras: (loc0, look0), (loc1, look1), lens, (g_a, g_b)
HERO = Vector((4.05, 3.38, 1.35))               # the front cooling loaf (r 0.24, a steam source)
CAMS = {
    "31a": (((3.10, 2.10, 2.55), (4.30, 3.75, 1.20)), ((3.30, 2.32, 2.40), (4.25, 3.70, 1.22)), 26.0, (2581, CUT_A - 1)),
    "31b": (((3.55, 2.50, 2.10), (4.08, 3.40, 1.30)), ((3.66, 2.64, 2.00), (4.07, 3.40, 1.33)), 26.0, (CUT_A, CUT_B - 1)),
    "31c": (((3.56, 2.56, 1.78), (4.06, 3.40, 1.50)), ((3.62, 2.66, 1.76), (4.06, 3.40, 1.53)), 26.0, (CUT_B, G32 - 1)),
    "32a": (((2.42, 3.05, 2.30), (2.42, 0.75, 1.74)), ((2.40, 2.72, 2.20), (2.40, 0.75, 1.76)), 26.0, (G32, CUT_32 - 1)),
    "32b": (((2.14, 2.18, 2.18), (2.14, 0.75, 1.80)), ((2.12, 2.02, 2.16), (2.12, 0.75, 1.82)), 26.0, (CUT_32, 2841)),
    "32c": None,                                                # = 32b continued (matching frame for the dissolve)
}


def cam_at(shot, g):
    fr = framing(shot, g)
    if fr == "32c":
        fr = "32b"
    (l0, k0), (l1, k1), lens, (a, b) = CAMS[fr]
    u = ez((g - a) / float(max(1, b - a)), "sine") if fr != "32b" else clamp((g - a) / float(b - a))   # 32b/c: linear drift
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lens


def steam_at(shot, g):
    if shot != 31:
        return 0.30
    if g < STEAM_FADE[0]:
        return 1.0
    return lerp(1.0, 0.22, ez((g - STEAM_FADE[0]) / float(STEAM_FADE[1] - STEAM_FADE[0])))


def scale_angle(shot, g):
    if shot == 32:
        if g < 2715:
            return 0.0
        d = g - 2715
        return 3.2 * math.exp(-d / 7.0) * math.cos(d * 0.42) if d < 24 else 0.0
    if shot == 33:
        if g <= TILT[0]:
            return 0.0
        return -8.0 * ez((g - TILT[0]) / float(TILT[1] - TILT[0]), "sine") if g < TILT[1] else -8.0
    return 0.0


# ----------------------------------------------------------------------------- 2D diagram pieces
def drop_svg(k):
    """a water drop pointing up (diagram look): pale-blue body, darker lower rim, white glint, plum ink outline.  Box (-0.5,-0.75,0.5,0.55)."""
    sq = [1.0, 0.92, 1.08][k]
    w = 0.36 * sq
    path = ("M 0 -0.62 C %.3f -0.36, %.3f -0.12, %.3f 0.10 A %.3f %.3f 0 1 1 %.3f 0.10 C %.3f -0.12, %.3f -0.36, 0 -0.62 Z"
            % (0.12 * sq, w, w, w, w, -w, -w, -0.12 * sq))
    return ('<defs><radialGradient id="dg%d" cx="0.38" cy="0.35" r="0.75"><stop offset="0" stop-color="#f2fbff"/>'
            '<stop offset="0.45" stop-color="#a9e2ff"/><stop offset="1" stop-color="#4fa6e6"/></radialGradient></defs>'
            '<path d="%s" fill="url(#dg%d)" stroke="%s" stroke-width="0.075" stroke-linejoin="round"/>'
            '<ellipse cx="%.3f" cy="0.02" rx="0.07" ry="0.13" fill="#ffffff" transform="rotate(18 %.3f 0.02)"/>'
            '<circle cx="%.3f" cy="-0.16" r="0.035" fill="#ffffff"/>'
            % (k, path, k, INK, -0.14 * sq, -0.14 * sq, -0.06 * sq))


def arrow_svg():
    """dashed up arrow: three dashes + a chunky head, white with plum ink.  Box (-0.4,-1.1,0.4,1.0)."""
    o = []
    for y0 in (0.55, 0.15, -0.25):
        o.append('<rect x="-0.09" y="%.2f" width="0.18" height="0.28" rx="0.07" fill="#ffffff" stroke="%s" stroke-width="0.06"/>' % (y0, INK))
    o.append('<path d="M 0 -1.0 L 0.32 -0.52 L 0.12 -0.52 L 0.12 -0.38 L -0.12 -0.38 L -0.12 -0.52 L -0.32 -0.52 Z" fill="#ffffff" '
             'stroke="%s" stroke-width="0.06" stroke-linejoin="round"/>' % INK)
    return "".join(o)


DROP_BOX = (-0.5, -0.75, 0.5, 0.55)
ARROW_BOX = (-0.4, -1.1, 0.4, 1.0)


class Drop(object):
    """one droplet: spawn at g0 on a source (a callable g -> (centre, radius)), rise, sway, pop in / shrink out."""

    def __init__(self, rnd, g0, life, size, src):
        self.g0, self.life, self.size, self.src = g0, life, size, src
        self.th = rnd.uniform(0, 2 * math.pi)
        self.rr = rnd.uniform(0.15, 0.85)
        self.vz = rnd.uniform(0.010, 0.016)
        self.out = rnd.uniform(0.0015, 0.004)
        self.ph = rnd.uniform(0, 6.28)
        self.sw = rnd.uniform(0.008, 0.02)
        self.var = rnd.randrange(3)
        self.p0 = None

    def state(self, g):
        """(world point, scale) or None when not alive."""
        t = g - self.g0
        if t < 0 or t > self.life:
            return None
        c, r, h = self.src(self.g0)
        if self.p0 is None:
            s = self.rr
            self.p0 = Vector((c.x + r * s * math.cos(self.th), c.y + r * s * math.sin(self.th) * 0.8,
                              c.z + h * math.sqrt(max(0.0, 1 - s * s)) + 0.03))
        d = Vector((math.cos(self.th), math.sin(self.th), 0.0))
        p = self.p0 + d * (self.out * t) + Vector((0, 0, self.vz * t + 0.00012 * t * t))
        p += Vector((self.sw * math.sin(0.25 * t + self.ph), 0.0, 0.0))
        k = min(1.0, t / 4.0) * min(1.0, (self.life - t) / 8.0)
        k = ez(k, "sine")
        return p, self.size * max(k, 0.0)


def loaf_world():
    """centre of the loaf on the hand balance's loaf pan (the loaf mesh is built in world coordinates under the pan pivot)."""
    pe = B.STATE["small"]["pans"][0]
    return pe.matrix_world.translation.copy() + Vector((0.0, 0.0, -0.62 + 0.05 + 0.05))


def afternoon_look():
    """runtime light tweak for the AFTERNOON half of shot 32 (set module untouched): a warmer, stronger low sun and brighter
    sun shafts, so the dissolve reads as 'later in the day' on this tight insert."""
    sun = B.STATE["sun"]
    sun.data.energy *= 1.30
    r, g, b = sun.data.color
    sun.data.color = (r, g * 0.92, b * 0.75)
    for m in C.bpy.data.materials:
        if m.node_tree and "shaft" in m.name:
            n = m.node_tree.nodes.get("shaft_k")
            if n is not None:
                n.outputs[0].default_value = 0.55


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, preset="MORNING", quality="preview"):
        C.Take.__init__(self, "bakery", preset, quality=quality, lens=26.0, name="cam_s31")
        self.preset = preset
        if preset == "AFTERNOON":
            afternoon_look()
        pd = os.path.join(TMP, "props")
        items = [(drop_svg(k), DROP_BOX, 256) for k in range(3)] + [(arrow_svg(), ARROW_BOX, 256)]
        self.pngs = C.svg_pngs(items, pd)
        self.drops, self.cards = [], []
        rnd = random.Random(31 if preset == "MORNING" else 33)
        if preset == "MORNING":
            hero = lambda g: (HERO + Vector((0, 0, 0.06)), 0.19, 0.15)
            g, acc = DROP_START, 0.0
            while g < G32:
                rate = lerp(0.30, 1.1, ez((g - DROP_START) / 40.0))         # drops per frame, ramping up
                acc += rate
                while acc >= 1.0:
                    acc -= 1.0
                    self.drops.append(Drop(rnd, g, rnd.randint(30, 46), rnd.uniform(0.032, 0.050), hero))
                g += 1
        else:
            def pan_loaf(g):
                return self.pan_loaf_at(g), 0.12, 0.08
            g, acc = 2783, 0.0
            while g <= RANGES[33][1]:
                acc += 0.45
                while acc >= 1.0:
                    acc -= 1.0
                    self.drops.append(Drop(rnd, g, rnd.randint(30, 44), rnd.uniform(0.028, 0.040), pan_loaf))
                g += 1
        for i, d in enumerate(self.drops):
            pc = C.PropCard("drop%03d" % i, [self.pngs[d.var]], DROP_BOX, scale=0.0001, shadow=False)
            pc.cards[0].hide_render = True
            self.cards.append(pc)
        self.arrows = []
        if preset == "MORNING":
            for i in range(2):
                pc = C.PropCard("arrow%d" % i, [self.pngs[3]], ARROW_BOX, scale=0.0001, shadow=False)
                pc.cards[0].hide_render = True
                self.arrows.append(pc)
        self.pan_cache = {}

    def pan_loaf_at(self, g):
        if g not in self.pan_cache:
            B.set_scale(scale_angle(33, g))
            C.bpy.context.view_layer.update()
            self.pan_cache[g] = loaf_world()
        return self.pan_cache[g]

    def drop_layout(self, shot, g, f, camloc):
        """key every droplet card at Blender frame f (location, scale, visibility)."""
        live = 0
        for d, pc in zip(self.drops, self.cards):
            st = d.state(g) if (shot == 31 or shot == 33) else None
            ob = pc.cards[0]
            if st is None:
                ob.hide_render = True
                pc.root.scale = (0.0001,) * 3
                pc.put(tuple(camloc + Vector((0, 0, -50))), face=tuple(camloc), frame=f)
            else:
                p, s = st
                ob.hide_render = s < 0.004
                pc.root.scale = (max(s, 0.0001),) * 3
                pc.put(tuple(p), face=tuple(camloc), frame=f)
                live += 1
            pc.root.keyframe_insert("scale", frame=f)
            ob.keyframe_insert("hide_render", frame=f)
        # dashed arrows (31c): beside the drop column, pulsing upward
        for i, pc in enumerate(self.arrows):
            ob = pc.cards[0]
            on = shot == 31 and g >= CUT_B + 2 + 3 * i
            if on:
                ph = ((g - (CUT_B + 2) + 9 * i) % 27) / 27.0
                side = [-1, 1][i]
                base = HERO + Vector((side * 0.21, -0.10, 0.40 + 0.22 * ph))
                a = min(1.0, (g - (CUT_B + 2 + 3 * i)) / 4.0)
                s = 0.15 * a * (1.0 - 0.25 * ph)
                ob.hide_render = False
                pc.root.scale = (s,) * 3
                pc.put(tuple(base), face=tuple(camloc), frame=f)
            else:
                ob.hide_render = True
                pc.root.scale = (0.0001,) * 3
                pc.put(tuple(camloc + Vector((0, 0, -50))), face=tuple(camloc), frame=f)
            pc.root.keyframe_insert("scale", frame=f)
            ob.keyframe_insert("hide_render", frame=f)
        return live

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(shot, g)
            self.key_cam(f, loc, look, lens)
            self.key_set(f, steam=steam_at(shot, g), oven=1.0)
            B.set_scale(scale_angle(shot, g), frame=f)
            B.set_scale_loaf(True, frame=f)
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(shot, g)
            self.drop_layout(shot, g, f, loc)
        for fc_ob in [pc.cards[0] for pc in self.cards + self.arrows]:
            fc = C._fcurve(fc_ob, "hide_render")
            if fc is not None:
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(shot, g)
        live = sum(1 for d in self.drops if (shot in (31, 33)) and d.state(g) is not None)
        out = dict(shot=shot, g=g, framing=framing(shot, g), cam=[round(c, 3) for c in loc], steam=round(steam_at(shot, g), 3),
                   scale_deg=round(scale_angle(shot, g), 2), drops=live, preset=self.preset)
        tgt = HERO if shot == 31 else loaf_world()
        out["loaf_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(tgt), f)[:2]]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def preset_of(shots):
    return "AFTERNOON" if 33 in shots else "MORNING"


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if 33 in shots and len(shots) > 1:
        raise SystemExit("shot 33 (AFTERNOON) needs its own process")
    if cmd in ("probe", "stills"):
        Tk = Take(preset_of(shots), "preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(preset_of(shots), q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
