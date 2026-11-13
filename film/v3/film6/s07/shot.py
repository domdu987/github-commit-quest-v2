#!/usr/bin/env python3
"""shot.py -- film 6 take s07: shots 7-10 (plan 15.34-26.32 s = g 460..789) + 6 handle frames each side (g 454..795), bakery MORNING.

  shot 7  g 454..548  Henry from BELOW (camera low in the counter opening, just above the sill): huge, squinting at the hand
          balance in the foreground.  A 454..505: he drops a crumb on the loaf pan (g 486) -> the beam swings from -2 (short) past
          level to +2.2 (too heavy).  B 506..548 punch-in (still low): he plucks the crumb back (g 520, beam back to -2), squints at
          it and snaps it in half (g 538).
  shot 8  g 549..641  the hand balance ECU.  A 549..596: level camera across the beam, Henry right behind it at eye level, his
          fat fingers lower the HALF crumb onto the loaf pan (g 572): the beam wobbles (+0.8, -0.3, +0.1) and settles EXACTLY level
          at g 606 ("ไม่ขาด ไม่เกิน" 20.27 s = g 611) and stays there.  B 597..641: tight on the pivot + pointer, perfectly level,
          Henry behind it sighting along the beam with one eye shut, then a smug little nod.
  shot 9  g 642..719  bakery_wide: kit TINY in the big shop, scrubbing a floury baking tray beside a wash tub and a stack of dirty
          trays, the oven roaring behind (oven 1.3), steam off the table loaves.  A 642..680 the preset wide (slow push),
          B 681..719 closer on kit; at the end he looks round toward the steaming table.
  shot 10 g 720..795  table_insert: A 720..752 kit's chin on the far edge of the table, dreamy, watching big white steam wisps rise
          off the fresh loaves (set steam 1.0 + cartoon wisp cards = the steam motif, planted clearly); B 753..795 ECU of the loaves
          and the wisps, the camera tilting up with the rising steam.
Mouths: no quoted line in shots 7-10 -> static expression mouths only (unimpressed / determined / wink / smug / neutral / happy).
NO depth of field anywhere (client rule).

    python3 shot.py stills 7,8,9,10 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 7,8,9,10 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

H = 6
B7, B8, B9, B10, B11 = [C.g_bound(t) for t in (15.34, 18.30, 21.40, 24.00, 26.32)]     # 460 549 642 720 790
RANGES = {7: (B7 - H, B8 - 1), 8: (B8, B9 - 1), 9: (B9, B10 - 1), 10: (B10, B11 + H - 1)}
CUT = {7: 506, 8: 597, 9: 681, 10: 753}          # framing change inside each shot

# ----------------------------------------------------------------------------- staging
SS = Vector((2.4, 0.75, 2.2))                   # small balance pivot
ARM = 0.5
HENRY = (2.80, 1.80)
KIT9 = (-0.6, 5.4)
KIT10 = (5.62, 4.0)
KIT10_Z = -0.20                                  # chin on the far edge of the table (top z 1.3)
CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)

CAMS = {
    (7, 0): (((2.20, -0.32, 1.42), (2.50, 1.8, 2.62)), ((2.22, -0.18, 1.46), (2.50, 1.8, 2.62)), 22.0),
    (7, 1): (((1.75, 0.05, 1.55), (2.45, 1.8, 2.40)), ((1.78, 0.13, 1.57), (2.45, 1.8, 2.40)), 22.0),
    (8, 0): (((2.40, -1.15, 2.18), (2.50, 0.75, 2.02)), ((2.40, -1.00, 2.18), (2.50, 0.75, 2.02)), 24.0),
    (8, 1): (((2.36, -0.42, 2.16), (2.40, 0.75, 2.16)), ((2.37, -0.30, 2.16), (2.40, 0.75, 2.16)), 26.0),
    (9, 0): (((5.75, 0.83, 3.46), (-2.2, 9.6, 2.1)), ((5.45, 1.10, 3.37), (-2.2, 9.6, 2.1)), 22.0),   # starts past the window shaft sheet (crossing it popped the exposure),
    (9, 1): (((2.2, 2.0, 2.5), (-0.7, 5.6, 1.75)), ((2.0, 2.25, 2.45), (-0.7, 5.6, 1.75)), 24.0),
    (10, 0): (((3.1, 2.1, 2.55), (4.85, 3.85, 1.70)), ((3.2, 2.25, 2.5), (4.85, 3.85, 1.70)), 24.0),
    (10, 1): (((3.55, 2.75, 1.75), (4.15, 4.0, 1.75)), ((3.60, 2.85, 1.80), (4.15, 4.0, 2.55)), 26.0),
}
STEAM = {7: 0.3, 8: 0.3, 9: 0.8, 10: 0.45}
OVEN = {7: 1.0, 8: 1.0, 9: 1.3, 10: 1.0}


def cam(shot, g):
    part = 0 if g < CUT[shot] else 1
    a, b, lens = CAMS[(shot, part)]
    g0 = RANGES[shot][0] if part == 0 else CUT[shot]
    g1 = CUT[shot] - 1 if part == 0 else RANGES[shot][1]
    u = ez((g - g0) / float(max(1, g1 - g0)), "sine")
    return Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u)), lens


# ----------------------------------------------------------------------------- the balance + the crumb
def keyed(g, keys):
    """piecewise sine-eased value from [(g, v), ...]."""
    if g <= keys[0][0]:
        return keys[0][1]
    for (g0, v0), (g1, v1) in zip(keys, keys[1:]):
        if g <= g1:
            return lerp(v0, v1, ez((g - g0) / float(g1 - g0), "sine"))
    return keys[-1][1]


BEAM = [(454, -2.0), (486, -2.0), (492, 2.9), (497, 1.9), (502, 2.3), (520, 2.2), (526, -2.4), (531, -1.8), (535, -2.0),
        (572, -2.0), (579, 0.8), (586, -0.3), (593, 0.12), (600, -0.04), (606, 0.0)]


def beam(g):
    if g >= 606:
        return 0.0
    v = keyed(g, BEAM)
    if g < 486:
        v += 0.15 * math.sin(g * 0.35)
    return v


def pan_top(g, side=-1):
    a = math.radians(beam(g))
    end = SS + Vector((side * ARM * math.cos(a), 0.0, side * ARM * math.sin(a)))
    return end + Vector((0.0, 0.0, -0.62 + 0.085))


def crumb_state(g, hold=None):
    """(world point of the crumb or None, held by henry's hand?, variant 0 = whole crumb, 1 = half)."""
    hover7 = lambda g: pan_top(g) + Vector((0.05, -0.05, 0.26))
    if g < 476:
        return hover7(g) + Vector((0.02 * math.sin(g * 0.3), 0, 0.02 * math.sin(g * 0.21))), True, 0
    if g < 486:
        u = ez((g - 476) / 10.0)
        return hover7(g).lerp(pan_top(g) + Vector((0, -0.05, 0.03)), u), True, 0
    if g < 512:
        return pan_top(g) + Vector((0, -0.05, 0.0)), False, 0              # on the pan (hand away)
    if g < 520:
        return pan_top(g) + Vector((0, -0.05, 0.0)), False, 0              # hand comes down (see hand_free)
    face = hold if hold is not None else Vector((2.0, 1.0, 2.0))
    if g < 534:
        u = ez((g - 520) / 14.0)
        return (pan_top(g) + Vector((0, -0.05, 0.03))).lerp(face, u), True, 0
    if g < 549:
        return face + Vector((0.01 * math.sin(g * 0.5), 0, 0)), True, (0 if g < 538 else 1)
    # shot 8: half crumb lowered onto the pan
    hover8 = pan_top(549) + Vector((0.03, -0.05, 0.24))
    if g < 560:
        return hover8 + Vector((0, 0, 0.015 * math.sin(g * 0.4))), True, 1
    if g < 572:
        u = ez((g - 560) / 12.0)
        return hover8.lerp(pan_top(g) + Vector((0, -0.05, 0.02)), u), True, 1
    return pan_top(g) + Vector((0, -0.05, 0.0)), False, 1


def crumb_svg(uid, half=False):
    if half:
        d = "M-0.030,0.010 L-0.022,-0.020 L0.004,-0.028 L0.012,-0.004 L0.002,0.018 Z"
    else:
        d = "M-0.045,0.012 L-0.034,-0.024 L-0.004,-0.036 L0.030,-0.026 L0.046,0.004 L0.026,0.026 L-0.016,0.030 Z"
    return ('<g id="%s"><path d="%s" fill="#e3a65a" stroke="#3a2832" stroke-width="0.008" stroke-linejoin="round"/>'
            '<circle cx="-0.008" cy="-0.010" r="0.006" fill="#fbe8bf"/></g>' % (uid, d))


# ----------------------------------------------------------------------------- shot 9 props
def tray_svg(uid):
    o = ['<g id="%s">' % uid,
         '<ellipse cx="0" cy="0" rx="0.40" ry="0.40" fill="#5d6672" stroke="#3a2832" stroke-width="0.022"/>',
         '<ellipse cx="0" cy="0" rx="0.33" ry="0.33" fill="#7d8792" stroke="#4a5058" stroke-width="0.012"/>',
         '<path d="M-0.20,-0.22 Q-0.05,-0.30 0.12,-0.22" fill="none" stroke="#ffffff" stroke-width="0.025" stroke-linecap="round" opacity="0.6"/>',
         '<circle cx="0.10" cy="0.08" r="0.09" fill="#f4ecdc" opacity="0.85"/>',
         '<circle cx="-0.12" cy="0.12" r="0.06" fill="#f4ecdc" opacity="0.8"/>',
         '<circle cx="0.05" cy="-0.08" r="0.05" fill="#a86a32" opacity="0.7"/>',
         '</g>']
    return "".join(o)


def stack_svg(uid):
    o = ['<g id="%s">' % uid]
    for i in range(7):
        y = -0.07 * i
        dx = 0.02 * math.sin(i * 1.7)
        o.append('<ellipse cx="%.3f" cy="%.3f" rx="0.42" ry="0.11" fill="%s" stroke="#3a2832" stroke-width="0.018"/>'
                 % (dx, y, "#6b7480" if i % 2 else "#5d6672"))
        o.append('<ellipse cx="%.3f" cy="%.3f" rx="0.14" ry="0.035" fill="#f4ecdc" opacity="0.8"/>' % (dx + 0.1, y - 0.01))
    o.append('</g>')
    return "".join(o)


def tub_svg(uid, k=0.0):
    o = ['<g id="%s">' % uid,
         '<path d="M-0.62,-0.42 L0.62,-0.42 L0.52,0.0 L-0.52,0.0 Z" fill="#9a6a3c" stroke="#3a2832" stroke-width="0.024" stroke-linejoin="round"/>',
         '<path d="M-0.58,-0.30 L0.58,-0.30 M-0.55,-0.14 L0.55,-0.14" stroke="#5e3c20" stroke-width="0.03"/>',
         '<ellipse cx="0" cy="-0.42" rx="0.62" ry="0.09" fill="#8fb6c8" stroke="#3a2832" stroke-width="0.022"/>']
    for i in range(6):
        a = i * 1.05 + k * 6.283
        o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#ffffff" opacity="0.85" stroke="#cfe3ec" stroke-width="0.006"/>'
                 % (0.42 * math.cos(a), -0.45 - 0.05 * math.sin(a) - 0.03 * (i % 2), 0.035 + 0.012 * (i % 3)))
    o.append('</g>')
    return "".join(o)


# ----------------------------------------------------------------------------- the steam motif (cartoon wisps)
def wisp_svg(uid, k, seed=0, h=1.4, op=0.6):
    o = []
    for i in range(2):
        ph = seed * 1.9 + i * 2.6
        x0 = (i - 0.5) * 0.08
        pts = []
        for j in range(17):
            t = j / 16.0
            pts.append((x0 * (1 + 1.2 * t) + 0.11 * math.sin(t * 8.0 + ph - k * 2 * math.pi) * (0.25 + t), -t * h))
        for a in range(4):
            seg = pts[a * 4:a * 4 + 5]
            d = "M%.4f,%.4f " % seg[0] + " ".join("L%.4f,%.4f" % q for q in seg[1:])
            o.append('<path d="%s" fill="none" stroke="#ffffff" stroke-width="%.3f" stroke-linecap="round" stroke-linejoin="round" opacity="%.3f"/>'
                     % (d, 0.085 * (1 - 0.15 * a), op * (1.0, 0.8, 0.5, 0.22)[a]))
    return '<g id="%s">%s</g>' % (uid, "".join(o))


WISP_N = 30
WISP_BOX = (-0.6, -1.6, 0.6, 0.05)
WISP_LOAVES = [(4.05, 3.38), (4.6, 3.82), (5.15, 3.38), (4.6, 4.68), (4.05, 4.68)]


# ----------------------------------------------------------------------------- poses
def henry_pose(g, hand_l=None):
    p = dict(yaw=-0.15, pitch=-0.30, expr="unimpressed", head_roll=3 + 2 * math.sin(g * 0.07), gaze=(-0.35, 0.6),
             arm_r="akimbo", legs="wide", blink=blink(g, [470, 515, 560, 630]), t=g / 30.0)
    if 494 <= g < 512:
        p["expr"] = "determined"
        p["gaze"] = (-0.3, 0.7)
    if g >= 520:
        p["gaze"] = (-0.2, 0.2) if g < 549 else (-0.25, 0.6)
        p["pitch"] = -0.1 if g < 549 else -0.2
    if g >= CUT[8]:
        p.update(expr="wink", yaw=0.0, pitch=0.0, gaze=(0.0, 0.05), head_roll=0)
        if g >= 618:
            p["expr"] = "smug"
            p["pitch"] = 0.12 * pulse(g, 620, 625, 633, 1.0)
            p["blink"] = blink(g, [636])
    return p


def kit9_pose(g):
    ph = (g - 642) * 0.42
    p = dict(yaw=0.30, pitch=0.30, expr="neutral", head_roll=-4 + 3 * math.sin(g * 0.2), gaze=(0.45, 0.6), lean=8,
             legs="stand", blink=blink(g, [655, 690, 712]), t=g / 30.0)
    look = ez((g - 704) / 8.0) if g >= 704 else 0.0
    p["yaw"] = lerp(0.30, 0.55, look)
    p["pitch"] = lerp(0.30, -0.1, look)
    p["gaze"] = (lerp(0.45, 0.9, look), lerp(0.6, -0.3, look))
    if look > 0.5:
        p["expr"] = "happy"
    hands = {"r": dict(hand=(0.48, 0.78), bend=-0.3),
             "l": dict(hand=(0.55 + 0.12 * math.cos(ph), 0.70 + 0.10 * math.sin(ph)), bend=0.6, stretch=1.2)}
    return p, hands


def kit10_pose(g):
    p = dict(yaw=-0.35, pitch=0.25, expr="happy", head_roll=-10 + 3 * math.sin(g * 0.06), gaze=(-0.7, -0.25), lean=0,
             legs="stand", blink=blink(g, [735, 790]), t=g / 30.0,
             arm_l=dict(hand=(-0.35, 0.55), bend=0.5), arm_r=dict(hand=(0.35, 0.55), bend=-0.5))
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=22.0, name="cam_s07")
        sd = os.path.join(TMP, "sprites"); pd = os.path.join(TMP, "props")
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        cb = (-0.06, -0.05, 0.06, 0.045)
        self.crumb = C.PropCard("crumb", C.svg_pngs([(crumb_svg("cr0"), cb, 2400), (crumb_svg("cr1", True), cb, 2400)], pd), cb,
                                scale=1.0, shadow=False)
        tb = (-0.44, -0.44, 0.44, 0.44)
        self.tray = C.PropCard("tray", C.svg_pngs([(tray_svg("tr"), tb, 400)], pd), tb, scale=1.0, shadow=True)
        sb = (-0.46, -0.6, 0.46, 0.14)
        self.stack = C.PropCard("stack", C.svg_pngs([(stack_svg("st"), sb, 400)], pd), sb, scale=1.0, shadow=True)
        ub = (-0.66, -0.62, 0.66, 0.03)
        self.tub = C.PropCard("tub", C.svg_pngs([(tub_svg("tb%d" % i, i / 12.0), ub, 360) for i in range(12)], pd), ub,
                              scale=1.3, shadow=True)
        self.wisps = []
        for j in range(len(WISP_LOAVES)):
            items = [(wisp_svg("w%d_%d" % (j, i), i / float(WISP_N), seed=j * 1.3, h=1.5 - 0.1 * (j % 3)), WISP_BOX, 360)
                     for i in range(WISP_N)]
            w = C.PropCard("wisp%d" % j, C.svg_pngs(items, pd), WISP_BOX, scale=1.0, shadow=False)
            for ob in w.cards:
                ob.visible_shadow = False
            self.wisps.append(w)
        self.props = [self.crumb, self.tray, self.stack, self.tub] + self.wisps

    def hide_actor(self, a, f, hidden):
        for ob in a.objects():
            ob.hide_render = bool(hidden)
            ob.keyframe_insert("hide_render", frame=f)

    def pose(self, shot, gs):
        henry, kit = self.actors["henry"], self.actors["kit"]
        far = Vector((0, -60, 0))
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, steam=(0.9 if (shot == 10 and g >= CUT[10]) else STEAM[shot]), oven=OVEN[shot])
            B.set_scale(beam(g) if shot in (7, 8) else 0.0, frame=f)
            for pr in self.props:
                pr.show(None, frame=f); pr.put(far, face=loc, frame=f)
            C.place(henry, f, HENRY if shot in (7, 8) else (-30, 5), 0.0)
            self.hide_actor(henry, f, shot not in (7, 8))
            if shot == 9:
                C.place(kit, f, KIT9, 0.0)
            elif shot == 10:
                C.place(kit, f, KIT10 if g < CUT[10] else (5.62, 9.0), KIT10_Z)
            else:
                C.place(kit, f, (-30, 5), 0.0)
            self.hide_actor(kit, f, not (shot == 9 or (shot == 10 and g < CUT[10])))
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam(shot, g)
            self.scene.frame_set(f)
            if shot in (7, 8):
                hold = actors.local_to_world(henry, (-0.40, -0.02), f) + (loc - Vector(HENRY + (0,))).normalized() * 0.0
                pt, held, var = crumb_state(g, hold)
                self.crumb.show(var, frame=f)
                self.crumb.put(pt + (loc - pt).normalized() * 0.04, face=loc, frame=f)
                p = henry_pose(g)
                if held:
                    p["fingers_l"] = 2
                    lx, ly = actors.world_to_local(henry, self.cam, tuple(pt), f)
                    hands = {"l": dict(hand=(lx, ly - 0.09), bend=0.6, stretch=1.4, layer="top")}
                elif shot == 7 and 512 <= g < 520:                      # reaching down for the crumb
                    u = ez((g - 512) / 8.0)
                    lx, ly = actors.world_to_local(henry, self.cam, tuple(pt), f)
                    hands = {"l": dict(hand=lerp((-0.75, 0.45), (lx, ly - 0.06), u), bend=0.6, stretch=1.25)}
                else:
                    t0 = 486 if shot == 7 else 572
                    lx, ly = actors.world_to_local(henry, self.cam, tuple(pt), f)
                    u = ez((g - t0) / 8.0)
                    rest = (-0.80, 0.55) if g < CUT[8] else (-0.62, 0.95)
                    hands = {"l": dict(hand=lerp((lx, ly - 0.06), rest, u), bend=0.6, stretch=1.25)}
                henry.pose(f, p, hands=hands, camera=self.cam)
            if shot == 9:
                p, hands = kit9_pose(g)
                kit.pose(f, p, hands=hands, camera=self.cam)
                w = actors.local_to_world(kit, (0.62, 0.72 + 0.02 * math.sin(g * 0.42)), f)
                self.tray.show(0, frame=f); self.tray.put(w + (w - loc).normalized() * 0.06, face=loc, frame=f)
                base = Vector((KIT9[0] - 0.95, KIT9[1] + 0.35, 0.0))
                self.stack.show(0, frame=f); self.stack.put(base + Vector((0, 0, 0.12)), face=loc, frame=f)
                tb = Vector((KIT9[0] + 0.05, KIT9[1] - 0.55, 0.0))
                self.tub.show((g // 3) % 12, frame=f); self.tub.put(tb, face=loc, frame=f)
            if shot == 10:
                if g < CUT[10]:
                    kit.pose(f, kit10_pose(g), camera=self.cam)
                for j, (x, y) in enumerate(WISP_LOAVES):
                    if j not in ((0, 1) if g < CUT[10] else (0, 1, 3)):
                        continue
                    b = Vector((x, y, 1.50))
                    self.wisps[j].show((g * 1 + j * 7) % WISP_N, frame=f)
                    self.wisps[j].put(b, face=loc, frame=f)
            if shot == 9 and g < CUT[9]:
                pass
        fr = [bf(shot, g) for g in gs]
        if shot in (7, 8):
            self.sprites_for([(henry, 448 if shot == 7 else 512)], fr)
        if shot == 9:
            self.sprites_for([(kit, 256)], fr)
        if shot == 10:
            self.sprites_for([(kit, 384)], [bf(shot, g) for g in gs if g < CUT[10]])

    def report(self, shot, g):
        f = bf(shot, g)
        loc, look, lens = cam(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, beam=round(beam(g), 3) if shot in (7, 8) else None,
                    heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            out = sys.argv[4]
            scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
            samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                st = Tk.render(shot, [g], out, scale=scale, samples=samples, threads=int(os.environ.get("THREADS", "2")))[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
