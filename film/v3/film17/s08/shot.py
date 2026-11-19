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
 20: [(1039, (1.15, 2.40, 1.45), (-0.90, 3.40, 1.30), 'drift'),
      (1062, (0.70, 1.20, 1.50), (-0.95, 3.40, 1.30), 'drift'),
      (1075, (-1.00, 0.00, 1.90), (-0.80, 3.40, 1.30), 'snap'),
      (1098, (-0.40, 0.70, 1.80), (-0.95, 3.40, 1.30), 'drift'),
      (1111, (1.15, 2.50, 1.25), (-0.90, 3.40, 1.30), 'snap'),
      (1126, (0.90, 1.90, 1.35), (-0.90, 3.40, 1.30), 'drift')],
 21: [(1127, (1.00, -0.60, 2.30), (0.0, 6.4, 1.50), 'drift'),
      (1148, (0.35, 0.00, 2.20), (0.0, 6.4, 1.50), 'drift'),
      (1161, (-0.95, 1.40, 1.70), (0.0, 6.4, 1.50), 'snap'),
      (1180, (-0.40, 1.80, 1.80), (0.0, 6.4, 1.50), 'drift'),
      (1193, (0.15, 2.20, 2.50), (0.0, 6.4, 1.50), 'snap'),
      (1201, (0.10, 2.35, 2.45), (0.0, 6.4, 1.50), 'drift')],
}
POS21 = dict(bert=(-0.55, 4.4, 0.0), ga=(0.80, 4.6, 0.0), gb=(0.80, 7.6, 0.0), ins=(-0.05, 5.8, 0.0))

def drawer_open(base, i, g):
    """overflowing: every pulled drawer creeps further out, a little jitter; continuous over both shots."""
    u = clamp((g - 1039) / 160.0)
    return clamp(base + (1.0 - base) * 0.55 * smooth(u) + 0.015 * math.sin(g * 0.21 + i * 1.7))

def key_set(g):
    K.set_flicker(1.5 + 0.8 * sine((g - 1039) / 160.0), frame=g, seed=3)       # the candle burns low: a stronger flicker
    K.set_dust(0.5, frame=g)
    for k, a in K.STATE['anim'].items():
        if k[0] in 'pq' and k[1:].isdigit():
            K.set_drawer(k, drawer_open(BASE[k], int(k[1:]), g), frame=g)
    if 'fan' in K.STATE['anim']: K.set_cards_fan(0.85 + 0.15 * math.sin(g * 0.13), frame=g)

BASE = {}

# ---- poses
def blink(g, per, off=0): return cast17.blink_at(g, per, off)

def pose_bert20(g):
    s, w = cast17.STORY17["bertillon_tired"][1], None
    p = dict(s)
    t = (g - 1039) / 30.0
    cyc = math.sin(t * 2 * math.pi * 1.1)
    p['yaw'] = 0.15 + 0.35 * math.sin(t * 2 * math.pi * 0.45)              # shakes his head: no match
    p['head_roll'] = -7 + 3.0 * math.sin(t * 2 * math.pi * 0.45 + 0.8)
    p['lean'] = 12 + 2.5 * math.sin(t * 2 * math.pi * 0.35) + 1.2 * cyc
    p['pitch'] = 0.9 + 0.12 * math.sin(t * 2 * math.pi * 0.9)
    p['expr'] = 'sad'
    p['arm_r'] = dict(hand=(0.56, 1.10 + 0.10 * cyc), bend=0.5, layer='front')
    p['prop_r'] = dict(type='card', scale=1.0, angle=-60 + 16 * cyc)
    p['arm_l'] = dict(hand=(-0.16, 1.12 + 0.07 * math.sin(t * 2 * math.pi * 1.1 + 2.0)), bend=0.5, layer='front')
    p['prop_l'] = dict(type='card', scale=1.0, angle=-30 - 12 * cyc)
    p['blink'] = blink(g, 78, 5)
    return cast17.silent(p)

def pose_bert21(g):
    p = dict(cast17.STORY17["bertillon_tired"][1])
    t = (g - G_CUT) / 30.0
    p['yaw'] = -0.35 + 0.05 * math.sin(t * 5)
    p['head_roll'] = -6 + 2 * math.sin(t * 4.1)
    p['lean'] = 9 + 1.5 * math.sin(t * 3.0)
    p['blink'] = blink(g, 66, 9)
    return cast17.silent(p)

def pose_ins(g):
    p = dict(cast17.STORY17["inspector_shouting"][1])
    t = (g - G_CUT) / 30.0
    p['lean'] = -4 + 3 * math.sin(t * 6.5)                                    # bounce while shouting
    p['head_roll'] = 3 * math.sin(t * 4.3)
    p['blink'] = blink(g, 60, 4)
    p['arm_r'] = dict(p['arm_r'], hand=(0.6, 0.3 + 0.04 * math.sin(t * 6.5)))
    if Q0 < g <= Q1: return cast17.speak(p, g, 1.0)
    return cast17.silent(p)

def pose_gend(who, g, ph):
    p = dict(cast17.STORY17["gendarme_laughing_" + who][1])
    t = (g - G_CUT) / 30.0
    p['lean'] = -6 + 6 * math.sin(t * 2 * math.pi * 3.0 + ph)                   # snicker bounce ~3 Hz
    p['head_roll'] = -8 + 3 * math.sin(t * 2 * math.pi * 3.0 + ph + 0.7)
    p['t'] = t
    return cast17.silent(p)

class Take(C.Take):
    def __init__(self, shot, quality="draft"):
        C.Take.__init__(self, PRESET[shot], LIGHT, quality, sprite_dir=os.path.join(HERE, "work", "sprites_s%d" % shot))
        self.shot = shot
        for o in bpy.data.objects:                      # director fix: shafts wash over the cast cards -> hidden
            if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or [])): o.hide_render = True
        for k, a in K.STATE['anim'].items():
            if k[0] in 'pq' and k[1:].isdigit(): BASE[k] = a['slide'].location.y / a['travel']
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
