#!/usr/bin/env python3
"""shot.py -- film 17 take s08: shots 20 + 21 (false payoff).  Narration 34.74-39.76 s, film g 1045..1195 (+6 handle frames each side: 1039..1201).
  id 20  g 1039..1126  records_desk / EVENING_INT: two months later, drawers overflowing, Bertillon tired, comparing cards, no match.  Pull-out + slide + a snap.
  id 21  g 1127..1201  records_aisle / EVENING_INT: the inspector shouts from the doorway (lip-sync g 1128..1195 only), gendarmes snicker.  Push-in.
One location per process: `python3 shot.py <cmd> 20|21 a:b[:step] ...`
cmds: probe | stills <out> [scale] [samples] | final [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C                                       # noqa
import bpy
from c17 import K, cast17, lerp, clamp, smooth, sine, g_of

G_CUT = 1127                                          # shot 21 starts (narration 37.48 s + 0.10 s offset)
H = 6
RANGES = {20: (1039, G_CUT - 1), 21: (G_CUT, 1195 + H)}
PRESET = {20: "records_desk", 21: "records_aisle"}
LIGHT = "EVENING_INT"
Q0, Q1 = g_of(37.48), g_of(39.74)                     # quote window in film frames (1127.4 .. 1195.2): lips move only for g in [Q0+1, Q1]

# ---- camera: (g, loc, look, kind-of-segment-ending-here)
CAM = {
 20: [(1039, (0.80, 1.60, 1.45), (-0.90, 3.30, 1.25), 'drift'),
      (1062, (0.55, 1.15, 1.45), (-0.95, 3.30, 1.25), 'drift'),
      (1075, (-0.85, 0.95, 1.65), (-0.85, 3.30, 1.25), 'snap'),
      (1098, (-0.45, 1.25, 1.60), (-0.95, 3.30, 1.25), 'drift'),
      (1111, (0.95, 1.95, 1.40), (-0.90, 3.30, 1.25), 'snap'),
      (1126, (0.75, 1.65, 1.45), (-0.90, 3.30, 1.25), 'drift')],
 21: [(1127, (0.45, -0.90, 2.25), (-0.15, 5.2, 1.35), 'drift'),
      (1141, (0.15, 1.60, 2.10), (-0.20, 5.2, 1.30), 'snap'),
      (1168, (0.05, 2.00, 2.05), (-0.25, 5.2, 1.30), 'drift'),
      (1181, (0.55, 1.30, 2.00), (-0.05, 5.2, 1.05), 'snap'),
      (1201, (0.45, 1.75, 1.95), (-0.05, 5.2, 1.00), 'drift')],
}
POS21 = dict(bert=(-0.85, 3.9, 0.0), ins=(0.40, 4.3, 0.0), ga=(1.00, 5.5, 0.0), gb=(-0.15, 6.2, 0.0))

def drawer_open(base, i, g, name=None):
    if name == 'p5': return 0.0
    """overflowing: every pulled drawer creeps further out, a little jitter; continuous over both shots."""
    u = clamp((g - 1039) / 160.0)
    return clamp(base + (1.0 - base) * 0.55 * smooth(u) + 0.015 * math.sin(g * 0.21 + i * 1.7))

def key_set(g):
    K.set_flicker(1.5 + 0.8 * sine((g - 1039) / 160.0), frame=g, seed=3)       # the candle burns low: a stronger flicker
    K.set_dust(0.5, frame=g)
    for k, a in K.STATE['anim'].items():
        if k[0] in 'pqx' and k[1:].isdigit():
            K.set_drawer(k, drawer_open(BASE[k], int(k[1:]), g, k), frame=g)
    if 'fan' in K.STATE['anim']: K.set_cards_fan(0.85 + 0.15 * math.sin(g * 0.13), frame=g)

BASE = {}

# ---- poses
def blink(g, per, off=0): return cast17.blink_at(g, per, off)

def pose_bert20(g):
    p = dict(cast17.STORY17["bertillon_tired"][1])
    t = (g - 1039) / 30.0
    per = 1.25                                                       # one card flip every 1.25 s, then a slow head shake
    ph = (t % per) / per
    flip = sine(ph / 0.35) if ph < 0.35 else 1.0                      # 0..1 during the flip
    shake = math.sin(clamp((ph - 0.35) / 0.65) * 2 * math.pi) if ph > 0.35 else 0.0
    p['yaw'] = 0.30 + 0.30 * shake
    p['head_roll'] = -9 + 3.0 * shake
    p['lean'] = 16 + 1.5 * math.sin(t * 2.4)                          # rounded shoulders
    p['pitch'] = 1.15 + 0.08 * math.sin(t * 3.1)                      # head down ~10 deg, eyes on the cards
    p['head_dy'] = 0.16
    p['expr'] = 'sad'
    p['gaze'] = (0.45, 0.55)
    up = 0.5 + 0.5 * math.sin(math.pi * (g % 38) / 38.0)             # lifting each card to eye level
    p['arm_r'] = dict(hand=(0.74, 0.55 + 0.25 * flip - 0.10 * (1 - flip)), bend=-0.3, stretch=1.0, layer='front')
    p['prop_r'] = dict(type='card', scale=1.0, angle=-78 + 22 * flip)
    p['arm_l'] = dict(hand=(-0.08, 0.80 + 0.06 * math.sin(t * 5.0)), bend=0.5, layer='front')
    p['prop_l'] = dict(type='card', scale=1.0, angle=-24)
    p['blink'] = blink(g, 78, 5)
    return cast17.silent(p)

def pose_bert21(g):
    p = dict(cast17.STORY17["bertillon_tired"][1])
    t = (g - G_CUT) / 30.0
    fl = smooth((g - 1130) / 8.0)                                    # flinch g1130-1138, then stays slumped
    hit = math.exp(-((g - 1134) / 3.0) ** 2)
    p['yaw'] = lerp(0.1, -0.45, fl)
    p['head_roll'] = -6 - 5 * fl + 2 * math.sin(t * 3.7)
    p['lean'] = 9 + 9 * fl + 5 * hit + 1.2 * math.sin(t * 3.0)
    p['pitch'] = 0.9 + 0.45 * fl
    p['head_dy'] = 0.12 + 0.1 * fl
    p['expr'] = 'sad'
    p['arm_r'] = dict(hand=(0.40, 1.34), bend=0.4, layer='front'); p['prop_r'] = dict(type='card', scale=0.9, angle=-35)
    p['arm_l'] = dict(hand=(-0.26, 1.30), bend=0.4, layer='front'); p['prop_l'] = dict(type='card', scale=0.9, angle=-145)
    p['blink'] = blink(g, 66, 9)
    return cast17.silent(p)

def pose_ins(g):
    p = dict(cast17.STORY17["inspector_shouting"][1])
    t = (g - G_CUT) / 30.0
    p = cast17.with_expr(p, 'angry') if False else p
    p['mirror'] = True                                                # faces camera-left, toward Bertillon
    p['yaw'] = 0.80 if g >= 1150 else 0.55
    p = cast17.with_expr(p, 'surprised')                              # wide open eyes, brows up (no laugh tears)
    p['gaze'] = (-1.0, 0.1)
    stress = max(0.0, math.sin(t * 2 * math.pi * 2.6)) ** 0.7        # lean forward on each stressed syllable
    p['lean'] = 4 + 14 * stress
    p['pitch'] = -0.1 + 0.25 * stress
    p['head_roll'] = 3 * math.sin(t * 4.3)
    p['blink'] = blink(g, 60, 4)
    p['arm_r'] = dict(hand=(0.46, 0.18 - 0.04 * stress), shape='open', bend=-1.0, stretch=1.0, layer='top')   # cupped beside the mouth
    if g >= 1172:                                                     # "ไอ้ช่างวัดหู": the other hand points at Bertillon
        k = smooth((g - 1172) / 6.0)
        p['arm_l'] = dict(hand=(lerp(-0.2, -0.95, k), lerp(0.9, 0.55, k)), shape='point' if k > 0.5 else 'ball', bend=-0.5, stretch=1.05, layer='front')
    if Q0 < g <= Q1: return cast17.speak(p, g, 1.0)
    return cast17.silent(p)

def pose_gend(who, g, ph):
    p = dict(cast17.STORY17["gendarme_laughing_" + who][1])
    t = (g - G_CUT) / 30.0
    p['lean'] = -5 + 5 * math.sin(t * 2 * math.pi * 3.0 + ph)                   # snicker bounce ~3 Hz
    p['head_roll'] = -6 + 3 * math.sin(t * 2 * math.pi * 3.0 + ph + 0.7)
    p['yaw'] = -0.5                                                              # looking at Bertillon
    p = cast17.with_expr(p, 'smirk')                                             # closed-mouth snicker
    p['fx'] = []
    p['t'] = t
    return cast17.silent(p)

def dress(shot):
    """runtime set dressing (set module untouched): more drawers jammed open, rejected cards on the desk + floor, a stub candle,
    the floating quill removed."""
    import random, bmesh
    B = K.Batch(17); r = random.Random(11)
    for i in range(24):                                              # card pile on the desk (world x -1.19..-0.41, y 1.75..3.45, top z 0.912)
        z = 0.915 + i * 0.0045
        B.box('cream', (-0.50 + r.uniform(-0.03, 0.03), 2.95 + r.uniform(-0.04, 0.04), z), (0.15, 0.10, 0.0035), rot=(0, 0, r.uniform(-25, 25)))
    for i in range(10):
        B.box('cream', (r.uniform(-1.05, -0.45), r.uniform(1.95, 2.55), 0.916), (0.15, 0.10, 0.0035), rot=(0, 0, r.uniform(0, 180)))
    for i in range(22):                                              # spilled on the floor around the stool
        B.box('cream', (r.uniform(-0.65, 0.55), r.uniform(1.9, 3.4), 0.003 + 0.003 * (i % 3)), (0.15, 0.10, 0.003), rot=(0, 0, r.uniform(0, 180)))
    B.cyl('brass', (-0.78, 1.97, 0.917), 0.06, 0.012, seg=16)        # stub candle on a saucer, front edge of the desk
    B.cyl('cream', (-0.78, 1.97, 0.985), 0.024, 0.13, seg=12)
    B.cyl('cream', (-0.757, 1.97, 0.93), 0.012, 0.04, seg=8)         # wax drip
    B.sphere('glow_gas', (-0.78, 1.97, 1.07), 0.022, scale=(1, 1, 1.7))
    B.finalize('s08_dress', ink_t=K.STATE['ink_t'] * 0.7)
    K.point((-0.78, 1.97, 1.08), watts=8, radius=0.02, name='candle')
    x1 = 1.9; CYb = 13.5                                             # more drawers hanging out of the left run beside the desk
    for i, (yw, row) in enumerate([(1.4, 5), (1.95, 12), (3.0, 8), (3.3, 15), (4.45, 6), (4.9, 11), (5.75, 9), (3.9, 13)]):
        xl = (CYb - yw)
        K.drawer_assembly('x%d' % i, K.cab_world((-x1, CYb, 0), -90, xl, 0.55, 0.2 + (row + 0.5) * 0.2), -90, w=0.278, h=0.18, depth=0.5, travel=0.42,
                          open_=0.5 + 0.1 * (i % 3), cards=20, seed=40 + i)
    for ob in bpy.data.objects:                                      # the floating quill by the lamp (a cream stick, desk-local (0.3, 0.25))
        if ob.type != 'MESH' or not any(m and 'cream' in m.name for m in ob.data.materials): continue
        bm = bmesh.new(); bm.from_mesh(ob.data); mw = ob.matrix_world
        dv = [v for v in bm.verts if -1.22 < (mw @ v.co).x < -0.84 and 2.78 < (mw @ v.co).y < 3.16 and (mw @ v.co).z > 0.975]
        if dv:
            bmesh.ops.delete(bm, geom=dv, context='VERTS'); bm.to_mesh(ob.data); print('quill: removed', len(dv), 'verts from', ob.name, flush=True)
        bm.free()

class Take(C.Take):
    def __init__(self, shot, quality="draft"):
        C.Take.__init__(self, PRESET[shot], LIGHT, quality, sprite_dir=os.path.join(HERE, "work", "sprites_s%d" % shot))
        self.shot = shot
        dress(shot)
        for o in bpy.data.objects:                      # director fix: shafts wash over the cast cards -> hidden
            if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or [])): o.hide_render = True
        for k, a in K.STATE['anim'].items():
            if k[0] in 'pqx' and k[1:].isdigit(): BASE[k] = a['slide'].location.y / a['travel']
        if shot == 20:
            self.bert = self.add_actor("bert", "bertillon_tired", "desk_clerk")
        else:
            self.bert = self.add_actor("bert", "bertillon_tired", xyz=POS21["bert"])
            self.ins = self.add_actor("ins", "inspector_shouting", xyz=POS21["ins"])
            self.ga = self.add_actor("ga", "gendarme_laughing_a", xyz=POS21["ga"])
            self.gb = self.add_actor("gb", "gendarme_laughing_b", xyz=POS21["gb"])

    def pose(self, gs, ppd):
        shot = self.shot
        for g in gs:
            loc, look = C.cam_path(CAM[shot], g)
            self.key_cam(g, loc, look)
            key_set(g)
        for g in gs:
            self.scene.frame_set(g)
            if shot == 20:
                self.pose_actor(self.bert, g, pose_bert20(g))
            else:
                self.pose_actor(self.bert, g, pose_bert21(g))
                self.pose_actor(self.ins, g, pose_ins(g))
                self.pose_actor(self.ga, g, pose_gend('a', g, 0.0))
                self.pose_actor(self.gb, g, pose_gend('b', g, 1.9))
        self.sprites_for(gs, ppd)

    def report(self, g, W=None):
        loc, look = C.cam_path(CAM[self.shot], g)
        return dict(shot=self.shot, g=g, cam=[round(c, 3) for c in loc], heads=self.heads(g, self.scene.render.resolution_x))

def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if ":" in part else [a[0]]
    return out

if __name__ == "__main__":
    cmd, shot = sys.argv[1], int(sys.argv[2])
    gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    if cmd in ("probe", "stills"):
        out = sys.argv[4] if cmd == "stills" else None
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        MODE = 'quick' if scale <= 0.25 else ('draft' if scale <= 0.5 else 'final')
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        Tk = Take(shot, 'draft' if scale <= 0.5 else 'final'); Tk.pose(gs, 128 if scale <= 0.5 else 256)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                os.makedirs(out, exist_ok=True)
                dt = Tk.render(g, os.path.join(out, "s%d_g_%04d.png" % (shot, g)), MODE, samples)
                print("g %d %.1f s" % (g, dt), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        MODE = 'quick' if scale <= 0.25 else ('draft' if scale <= 0.5 else 'final')
        out = os.path.join(HERE, "raw", "s%d_%s" % (shot, MODE)); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        print("final: shot %d, %d to render" % (shot, len(todo)), flush=True)
        if todo:
            Tk = Take(shot, 'draft' if scale <= 0.5 else 'final'); Tk.pose(gs, 128 if scale <= 0.5 else 256)
            for g in todo:
                p = os.path.join(out, "g_%04d.png" % g)
                dt = Tk.render(g, p + ".tmp.png", MODE, samples); os.replace(p + ".tmp.png", p)
                json.dump(Tk.report(g), open(p[:-4] + ".json", "w"))
                print("shot %d g %d %.1f s" % (shot, g, dt), flush=True)
