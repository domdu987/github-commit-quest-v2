#!/usr/bin/env python3
"""shot.py -- film 17 take s13 = shots 31-33, the ending (narration 62.15-68.30 s).  g0 1868, g1 2052, 6 handle frames before g0, none after
(HARD CUT at g 2052).  One location (measure, DAY_INT), three set-ups, hard cuts at 1947 and 2014:

  31  g 1862..1946  measure_wide-style, camera ~55 % closer to the chair; the red-faced inspector sits stiff in the chair, Bertillon beside him
                    raises the calipers, gendarmes + prisoners grin (bounce).  Push-in 8 %/s + lateral slide, a 15 f snap in at g 1906, kepi rack fg.
  32  g 1947..2013  measure_chair-style: Bertillon calmly closes the calipers on the inspector's ear, eyes sideways.  Push 9 %/s, snap at g 1980.
  33  g 2014..2051  the ear insert (callback of shot 3), caliper tips on the ear, quick push-in x1.4.  Last frame 2051; the film ends on the hard cut.
No mouth moves (silent poses everywhere).  Blender frame f = g + 1.

    python3 shot.py stills 31,32,33 a:b[:step] out_dir [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]
"""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import K, bpy, Vector, lerp, clamp, ez, ez_out, blink, cast17, actors, camrig, render, sprites

G0, G1, HANDLE = 1868, 2052, 6
RANGES = {31: (G0 - HANDLE, 1946), 32: (1947, 2013), 33: (2014, G1 - 1)}
SNAP31, SNAP32 = 1906, 1982
PPD = {31: 224, 32: 320, 33: 576}
QUICK = bool(os.environ.get("QUICK"))
if QUICK: PPD = {31: 64, 32: 64, 33: 96}
TMP = os.path.join(HERE, "work")

def shot_of(g): return 31 if g < 1947 else 32 if g < 2014 else 33
def F(g): return int(g) + 1

# ------------------------------------------------------------------ camera
CH = Vector((0.7, 2.3, 1.22))                      # the inspector's head
def unit(v): v = Vector(v); return v / v.length
def drift(g, g0, c0, tgt0, rate, slide, snaps, lift=0.0):
    """camera on the line c0 -> tgt0: push `rate`/s of the distance, lateral slide `slide` m/s (+ right), snaps (g, frames, factor, shift_m)"""
    t = (g - g0) / 30.0
    v = unit(tgt0 - c0); right = Vector((v.y, -v.x, 0)).normalized(); d0 = (tgt0 - c0).length
    push = 1.0 - rate * t; sh = slide * t; dz = 0.0
    for (gs, n, fac, shift) in snaps:
        e = ez(clamp((g - gs) / float(n)))
        push *= lerp(1.0, fac, e); sh += shift * e; dz += lift * e
    loc = tgt0 - v * (d0 * push) + right * sh
    look = tgt0 + right * (0.55 * sh)
    loc.z = c0.z - dz
    return loc, look
def cam31(g):
    return drift(g, RANGES[31][0], Vector((-1.45, -0.35, 1.52)), Vector((0.95, 2.25, 1.22)), 0.11, 0.12, [(1884, 12, 0.78, 0.15), (1917, 12, 0.78, -0.10)], lift=0.05)
def cam32(g):
    c0 = Vector((1.95, 0.35, 1.5)); tgt0 = Vector((0.95, 2.25, 1.28))
    return drift(g, RANGES[32][0], c0, tgt0, 0.12, -0.20, [(1966, 12, 0.80, -0.10), (1993, 12, 0.78, 0.08)], lift=0.04)
_v = unit(Vector((0.7 - 0.25, 2.3 - 1.45, 0))); EAR33 = Vector((0.7, 2.3, 1.27)) + Vector((_v.y, -_v.x, 0)) * 0.27 - _v * 0.28 * 0.0
def cam33(g):
    t = (g - RANGES[33][0]) / 38.0
    c0 = Vector((0.25, 1.45, 0.95))
    look = EAR33.copy()
    d0 = (look - c0).length
    d = d0 / (1.0 + 0.15 * t + 0.25 * ez(clamp((t - 0.30) / 0.45)))      # slow drift, then the quick push-in: x1.4 in all
    loc = look - unit(look - c0) * d + Vector((0.05 * (t - 0.5), 0, 0.02 * t))
    return loc, look + Vector((0.01 * math.sin(g * 0.3), 0, 0))
def cam_of(g):
    return {31: cam31, 32: cam32, 33: cam33}[shot_of(g)](g)

# ------------------------------------------------------------------ cast
CAST_STAND = {   # name -> (story pose, cast, world xy, mirror, expr)
    "gen_a": ("gendarme_laughing_a", "gendarme_a", (-0.05, 3.45), False),
    "gen_b": ("gendarme_laughing_b", "gendarme_b", (2.35, 3.0), True),
    "pris_b": ("prisoner_standing_b", "prisoner_b", (-0.35, 2.75), False),
    "pris_c": ("prisoner_standing_c", "prisoner_c", (2.05, 2.55), False),
}
POS31 = {'gen_a': (1.0, 3.4), 'gen_b': (1.95, 3.45), 'pris_b': (-0.35, 3.3), 'pris_c': (2.6, 2.8)}
def pose_inspector(g):
    p = dict(cast17.STORY17["inspector_seated_stiff"][1]); p["seat17"] = None
    p["flush17"] = 1.0 if g > 0 else 1.0
    p["rim"] = K.RIM_FOR["inspector17"]; p["rim_opacity"] = 0.55; p["rim_w"] = 0.02
    sh = shot_of(g)
    p["gaze"] = (0.0, 0.0) if sh == 31 else (0.9, 0.15)           # eyes sideways at the calipers
    p["head_roll"] = 1.2 * math.sin(g * 0.21)
    p["lean"] = 0.8 * math.sin(g * 0.13)
    p["mouth"] = "flat"
    p["blink"] = blink(g, [1880, 1925, 1975, 2030])
    p["t"] = g / 30.0
    return p

def pose_laugh(story, mirror, g, seed, smirk=False):
    p = dict(cast17.STORY17[story][1]); p["seat17"] = None
    if mirror: p["mirror"] = True
    if smirk: p = cast17.with_expr(p, "smirk")
    p["mouth"] = p.get("mouth", "flat") if not smirk else "smile"
    p["blink"] = blink(g, [1870 + seed * 7, 1930 + seed * 5, 2000 + seed * 3])
    p["t"] = g / 30.0
    return p

# ------------------------------------------------------------------ the take
class Take(object):
    def __init__(self, quality="draft"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.A = K.build(preset="measure_chair", light="DAY_INT")
        K.clear_keys()
        self.scene = bpy.context.scene; self.cam = self.scene.camera
        self.cam.data.dof.use_dof = False
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        for i, m in enumerate(K.STATE['life'].get('dust', [])):      # half as many motes (odd ones hidden), smaller (k 0.55)
            if i % 2: m['ob'].hide_render = True
        self.fg = {31: [], 32: [], 33: []}
        self.make_fg()
        self.act = {}
        sd = os.path.join(TMP, "sprites"); os.makedirs(sd, exist_ok=True)
        self.act["ins"] = C.make_actor("ins", "inspector17", sd)
        self.act["ber"] = C.make_actor("ber", "bertillon", sd)
        for k, (st, cast, xy, mir) in CAST_STAND.items():
            self.act[k] = C.make_actor(k, cast, sd)
        self.fy = {}
        self.cam_cache = {}

    def make_fg(self):
        B = K.Batch(17); _c0 = Vector((-1.45, -0.35, 1.52)); _v = unit(Vector((0.95, 2.25, 0)) - Vector((-1.45, -0.35, 0))); _l = Vector((-_v.y, _v.x, 0))
        _p = _c0 + _v * 1.55 + _l * 0.42; K.coat_rack(B, (_p.x, _p.y), rot=25, kepis=3)
        self.fg[31] = B.finalize('fg31', ink_t=K.STATE['ink_t'] * 0.7)
        B = K.Batch(17); K.ledger_stack(B, (1.35, 0.85, 0.0), n=6, rot=12); K.crate(B, (2.0, 0.9, 0), size=(0.45, 0.35, 0.3), rot=25)
        self.fg[33] = B.finalize('fg33', ink_t=K.STATE['ink_t'] * 0.7)

    def key_fg(self, f, sh):
        for s, objs in self.fg.items():
            for o in objs:
                o.hide_render = (s != sh); o.keyframe_insert("hide_render", frame=f)

    def sc_of(self, who, cast, H):
        return K.CAST_H[who] / K.CAST_HD[who]

    def place_all(self, g):
        f = F(g); sh = shot_of(g); t = g / 30.0
        # inspector (seated on the chair)
        ins = self.act["ins"]; x, y, z, *_ = self.A["marks"]["chair"]
        pi = pose_inspector(g); fx, fy = sprites.feet_of("inspector17", pi)
        sc = K.CAST_H["inspector17"] / K.CAST_HD["inspector17"]
        self.sc_ins = sc
        cl = cam_of(g)[0]; pos = Vector((x, y, K.HEAD_Z["chair"] - sc * fy))
        r = 1.0 - 0.28 / (pos - cl).length                 # bring the card 0.28 m toward the lens (screen image unchanged): the head rest pad must not cut the face
        ins.place(f, tuple(cl + (pos - cl) * r), scale=sc * r)
        # bertillon
        ber = self.act["ber"]
        scb = K.CAST_H["bertillon"] / K.CAST_HD["bertillon"]
        if sh != 33:
            bx, by = (1.40, 2.0) if sh == 31 else (1.25, 2.05)
        else:   # beside the ear at the same depth, so his arm reaches it; his torso is mostly off the right edge
            v = unit(Vector((EAR33.x - cl.x, EAR33.y - cl.y, 0))); rt = Vector((v.y, -v.x, 0))
            bp = Vector((EAR33.x, EAR33.y, 0)) + rt * 0.62 - v * 0.15; bx, by = bp.x, bp.y
        ber.place(f, (bx, by, 0.0), scale=scb)
        for k, (st, cast, xy, mir) in CAST_STAND.items():
            a = self.act[k]; scx = K.CAST_H[cast] / K.CAST_HD[cast]; xy = POS31[k] if sh == 31 else xy
            bounce = 0.035 * abs(math.sin(2 * math.pi * 3.0 * t + hash(k) % 7))
            a.place(f, (xy[0], xy[1], bounce), scale=scx)
            a.root.hide_render = False
            a.root.keyframe_insert("hide_render", frame=f) if hasattr(a.root, "hide_render") else None
        self.key_fg(f, sh)

    def key_all(self, gs):
        K.set_flicker(1, frame=None)
        for g in gs:
            f = F(g); loc, look = cam_of(g)
            camrig.key_camera(f, loc, look, cam=self.cam, lens=22.0, interp="LINEAR", easing="AUTO")
            self.place_all(g)
            K.key_life(f, f, dust=0.55, pendulum=False); K.set_pendulum(t=g / 30.0, frame=f)

    def poses(self, gs):
        ins, ber = self.act["ins"], self.act["ber"]
        for g in gs:
            f = F(g); self.scene.frame_set(f); sh = shot_of(g)
            pi = pose_inspector(g); ins.pose(f, pi, camera=self.cam)
            # ear (screen-right ear of the inspector, +0.52 D right, 0.10 D above the head centre)
            an = sprites.puppet.figure("inspector17", pi, "q")["anchors"]
            hx, hy = an["head"]
            hip = sprites.hip_y('inspector17', pi); k = ins.upper_k[f]
            ear_loc = (hx + 0.505, hip + (hy - 0.04 - hip) * k)
            ear_w = actors.local_to_world(ins, ear_loc, f, feet=ins.feet[f], camera=self.cam)
            self.ear_w = ear_w
            pb = dict(cast17.STORY17["bertillon_measuring"][1]); pb["mirror"] = True; pb["yaw"] = 0.5; pb["seat17"] = None
            pb["rim"] = K.RIM_FOR["bertillon"]; pb["rim_opacity"] = 0.55; pb["rim_w"] = 0.02
            pb["blink"] = blink(g, [1885, 1950, 2010]); pb["t"] = g / 30.0; pb["mouth"] = "flat"
            # approach: raised in 31, closing in 32, on the ear in 33
            if sh == 31: c = 0.12 + 0.43 * ez(clamp((g - 1862) / 84.0))
            elif sh == 32: c = 0.35 + 0.65 * ez(clamp((g - 1950) / 50.0))
            else: c = 1.0
            off = (1.0 - c)
            tgt_w = Vector(ear_w) + Vector((0.45 * off, -0.1 * off, 0.12 * off)) + Vector((0, 0, 0.012 * math.sin(g * 0.5) * (c > 0.95)))
            tl = actors.world_to_local(ber, self.cam, tgt_w, f, feet=sprites.feet_of("bertillon", pb))
            kb = actors.upper_stretch(ber, self.cam, f, pb); hipb = sprites.hip_y("bertillon", pb)
            tl = (tl[0], hipb + (tl[1] - hipb) / kb)               # the sprite is stretched about the hip: aim the unstretched figure
            pb = cast17.hand_for_anchor("bertillon", pb, "r", "calipers_l", tl)
            ber.pose(f, pb, camera=self.cam)
            for k, (st, cast, xy, mir) in CAST_STAND.items():
                a = self.act[k]; pq = pose_laugh(st, mir, g, hash(k) % 5, smirk=st.startswith("prisoner"))
                a.pose(f, pq, camera=self.cam)

    def ear_overlay(self, f, pose):
        ins = self.act["ins"]; an = sprites.puppet.figure("inspector17", pose, "q")["anchors"]; hx, hy = an["head"]
        hip = sprites.hip_y("inspector17", pose); k = ins.upper_k.get(f, 1.0)
        cx, cy = hx + 0.505, hip + (hy - 0.04 - hip) * k
        return ('<g><ellipse cx="%.4f" cy="%.4f" rx="0.075" ry="0.135" fill="#e2503f" stroke="#2a1b1b" stroke-width="0.022"/>'
                '<path d="M%.4f,%.4f q0.05,0.02 0.02,0.10 M%.4f,%.4f q0.03,-0.04 0.0,-0.09" stroke="#9c2a22" stroke-width="0.016" fill="none" stroke-linecap="round"/></g>'
                % (cx, cy, cx - 0.01, cy - 0.07, cx - 0.01, cy + 0.06))

    def sprites(self, gs):
        by = {}
        for g in gs: by.setdefault(shot_of(g), []).append(F(g))
        for sh, fr in by.items():
            for k, a in self.act.items():
                ppd = PPD[sh] if k in ("ins", "ber") else (PPD[sh] if sh != 33 else (192 if not QUICK else 64))
                a.render_sprites(ppd, frames=fr, overlay=self.ear_overlay if k == 'ins' else None)

    def prepare(self, gs):
        self.key_all(gs); self.poses(gs); self.sprites(gs)

    def render(self, gs, out, scale=0.5, samples=6, threads=2):
        K.setup_render(self.scene, "draft" if scale < 1 else "final", samples)
        self.scene.cycles.samples = samples
        res = render.render_frames([F(g) for g in gs], out, scale=1.0, threads=threads, scene=self.scene, camera=self.cam, verbose=False)
        for g, r in zip(gs, res):
            dst = os.path.join(out, "g_%04d.png" % g); os.replace(r["path"], dst); K.grade(dst, scale=scale)
        return res

def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if ":" in part else [a[0]]
    return out

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "stills":
        gs = parse(a[1]); out = a[2]; scale = float(a[3]) if len(a) > 3 else 0.5; sm = int(a[4]) if len(a) > 4 else 6
        T = Take(); T.prepare(gs); T.render(gs, out, scale, sm)
    elif a[0] == "final":
        gs = parse(a[1]); scale = float(a[2]) if len(a) > 2 else 1.0; sm = int(a[3]) if len(a) > 3 else 12; thr = int(a[4]) if len(a) > 4 else 2
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        gs = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        T = Take(); T.prepare(gs)
        for g in gs:
            t0 = time.time(); T.render([g], out, scale, sm, thr); print("g", g, "%.1fs" % (time.time() - t0), flush=True)
