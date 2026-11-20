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
PPD = {31: 224, 32: 320, 33: 512}
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
HEAD = Vector((0.7, 2.3, 1.22))
D_ = 1.66 / 3.21                                   # metres per head D of the inspector card
V31 = unit(Vector((1.54, 2.23, 0))); V32 = unit(Vector((-0.83, 1.83, 0))); V33 = unit(Vector((1.16, 0.74, 0)))
def rt_of(v): return Vector((v.y, -v.x, 0))       # camera-right (horizontal) for a view direction
def ear_of(v):                                     # the inspector's screen-LEFT ear (the card is billboarded to a camera looking along v)
    return HEAD - rt_of(v) * (0.505 * D_) + Vector((0, 0, 0.02))
def cam31(g):
    return drift(g, RANGES[31][0], Vector((-0.99, 0.17, 1.45)), Vector((0.55, 2.40, 1.38)), 0.08, 0.16, [(1884, 11, 0.76, 0.20), (1917, 11, 0.80, -0.20)], lift=0.04)
def cam32(g):
    return drift(g, RANGES[32][0], Vector((1.32, 0.39, 1.45)), Vector((0.46, 2.30, 1.30)), 0.09, 0.14, [(1966, 11, 0.78, 0.15), (1993, 11, 0.80, -0.15)], lift=0.04)
S3A = (((-0.58, 1.46, 1.02), (0.58, 2.20, 1.24)), ((-0.14, 1.80, 1.06), (0.74, 2.20, 1.24)))     # team 1's shot-3 insert (film17/s01 shot.py), start -> end
LOOK_DX = 0.0
def cam33(g):
    t = (g - RANGES[33][0]) / 38.0
    u = 0.3 * t + 0.7 * ez(clamp((t - 0.15) / 0.6))                       # slow drift, then the quick push-in (x1.4)
    (c0, l0), (c1, l1) = S3A
    loc = Vector(c0) + (Vector(c1) - Vector(c0)) * u; look = Vector(l0) + (Vector(l1) - Vector(l0)) * u
    off = ear_of(V33) - Vector((0.58, 2.20, 1.24))               # our ear sits where team 1's ear is: same picture
    return loc + off, look + off
def cam_of(g):
    sh = shot_of(g); loc, look = {31: cam31, 32: cam32, 33: cam33}[sh](g)
    a = {31: 0.012, 32: 0.010, 33: 0.005}[sh]                    # handheld sway
    loc = loc + Vector((a * math.sin(g * 0.83), a * math.cos(g * 0.61), 0.5 * a * math.sin(g * 1.17)))
    return loc, look

# ------------------------------------------------------------------ cast
CAST_STAND = {   # name -> (story pose, cast, mirror)
    "gen_a": ("gendarme_laughing_a", "gendarme_a", False),
    "gen_b": ("gendarme_laughing_b", "gendarme_b", True),
    "pris_b": ("prisoner_standing_b", "prisoner_b", False),
    "pris_c": ("prisoner_standing_c", "prisoner_c", False),
}
POS = {31: {'gen_a': (1.0, 3.4), 'gen_b': (1.95, 3.45), 'pris_b': (-0.6, 3.5), 'pris_c': (2.6, 2.8)},
       32: {'gen_a': (1.5, 3.5), 'gen_b': (2.4, 3.1), 'pris_b': (1.05, 3.75), 'pris_c': (2.1, 2.55)},
       33: {'gen_a': None, 'gen_b': None, 'pris_b': None, 'pris_c': (1.75, 1.7)}}
def pose_inspector(g):
    p = dict(cast17.STORY17["inspector_seated_stiff"][1]); p["seat17"] = None
    p["flush17"] = 1.0
    p["rim"] = K.RIM_FOR["inspector17"]; p["rim_opacity"] = 0.55; p["rim_w"] = 0.02
    gx = -0.9 * ez((g - 1950) / 22.0)                         # eyes slide sideways toward the calipers (screen-left)
    p["gaze"] = (gx, 0.12 * ez((g - 1950) / 22.0))
    tw = 1.8 * math.sin((g - 2028) * 1.3) if 2028 <= g <= 2035 else 0.0     # the moustache twitch ~g2030 (a quick head-roll pulse)
    p["head_roll"] = 0.6 * math.sin(g * 0.21) + tw
    if g >= 2014: p["arm_l"] = dict(p["arm_l"], hand=(-0.42, 1.12))        # shot 33: his near fist tucked in, off the caliper bar
    p["mouth"] = "flat"                                       # never changes (no "t" key: no idle mouth)
    p["blink"] = blink(g, [1880, 1925, 1975, 2005])
    return cast17.silent(p)

def pose_laugh(story, mirror, g, seed, smirk=False):
    p = dict(cast17.STORY17[story][1]); p["seat17"] = None
    if mirror: p["mirror"] = True
    if smirk: p = cast17.with_expr(p, "smirk")
    p["blink"] = blink(g, [1870 + seed * 7, 1930 + seed * 5, 2000 + seed * 3])
    p["t"] = g / 30.0
    return p if not smirk else cast17.silent(p)

VREF = {31: V31, 32: V32, 33: V33}

# ------------------------------------------------------------------ the take
class Take(object):
    def __init__(self, quality="draft"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.A = K.build(preset="measure_chair", light="DAY_INT")
        K.clear_keys()
        for o in bpy.data.objects:
            if "beam_fx" in o.name: o.hide_render = True          # the light-shaft prisms made the see-through wedge across the cast
        for i, m in enumerate(K.STATE['life'].get('dust', [])):  # a quarter of the motes, smaller
            if i % 4: m['ob'].hide_render = True
        self.scene = bpy.context.scene; self.cam = self.scene.camera
        self.cam.data.dof.use_dof = False
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        self.fg = {31: [], 32: [], 33: []}
        self.make_fg()
        self.act = {}
        sd = os.path.join(TMP, "sprites"); os.makedirs(sd, exist_ok=True)
        self.act["ins"] = C.make_actor("ins", "inspector17", sd)
        self.act["ber"] = C.make_actor("ber", "bertillon", sd)
        self.head_cut = self.make_head_cut(self.act["ber"])
        for k, (st, cast, mir) in CAST_STAND.items():
            self.act[k] = C.make_actor(k, cast, sd)

    def make_head_cut(self, actor):
        """alpha mask on Bertillon's card: only below v = cut is drawn (cut 2.0 = everything); shot 33 hides his head disc (arm and hand stay)."""
        mats = [m for m in actor.card.data.materials if m] if actor.card.data.materials else [ms.material for ms in actor.card.material_slots]
        out = []
        for m in mats:
            nt = m.node_tree; mix = [n for n in nt.nodes if n.type == "MIX_SHADER"][0]
            src = mix.inputs["Fac"].links[0].from_socket
            tc = nt.nodes.new("ShaderNodeTexCoord"); sp = nt.nodes.new("ShaderNodeSeparateXYZ")
            def mth(op, a_=None, b_=None):
                n = nt.nodes.new("ShaderNodeMath"); n.operation = op
                for i, v_ in enumerate((a_, b_)):
                    if v_ is None: continue
                    if isinstance(v_, float): n.inputs[i].default_value = v_
                    else: nt.links.new(v_, n.inputs[i])
                return n
            val = nt.nodes.new("ShaderNodeValue"); val.outputs[0].default_value = 2.0
            nt.links.new(tc.outputs["UV"], sp.inputs[0])
            above = mth("GREATER_THAN", sp.outputs["Y"], val.outputs[0]); left = mth("LESS_THAN", sp.outputs["X"], 0.78)
            both = mth("MULTIPLY", above.outputs[0], left.outputs[0]); keep = mth("SUBTRACT", 1.0, both.outputs[0]); mu = mth("MULTIPLY", src, keep.outputs[0])
            nt.links.new(mu.outputs[0], mix.inputs["Fac"]); out.append(val)
        return out

    def key_cut(self, f, g):
        for v in self.head_cut:
            v.outputs[0].default_value = 0.50 if g >= 2014 else 2.0
            v.outputs[0].keyframe_insert("default_value", frame=f)

    def make_fg(self):
        c0 = Vector((-0.99, 0.17, 0)); v = V31; left = Vector((-v.y, v.x, 0))
        p = c0 + v * 1.45 + left * 0.45
        B = K.Batch(17); K.stool(B, (p.x, p.y), h=0.5, rot=15); K.kepi(B, (p.x, p.y, 0.53), rot=40)
        self.fg[31] = B.finalize('fg31', ink_t=K.STATE['ink_t'] * 0.7)
        B = K.Batch(17); K.crate(B, (0.62, 1.05, 0), size=(0.34, 0.26, 0.2), rot=20)
        self.fg[32] = B.finalize('fg32', ink_t=K.STATE['ink_t'] * 0.7)

    def key_fg(self, f, sh):
        for s, objs in self.fg.items():
            for o in objs:
                o.hide_render = (s != sh); o.keyframe_insert("hide_render", frame=f)

    def put(self, actor, f, pos, sc, cl):
        r = 1.0 - 0.28 / (pos - cl).length                  # 0.28 m toward the lens, scale compensated (screen image unchanged): the headrest pad must not cut the face
        actor.place(f, tuple(cl + (pos - cl) * r), scale=sc * r)

    def place_all(self, g):
        f = F(g); sh = shot_of(g); t = g / 30.0; cl = cam_of(g)[0]; v = VREF[sh]
        ins = self.act["ins"]; pi = pose_inspector(g); fx, fy = sprites.feet_of("inspector17", pi)
        sc = K.CAST_H["inspector17"] / K.CAST_HD["inspector17"]
        self.put(ins, f, Vector((HEAD.x, HEAD.y, K.HEAD_Z["chair"] - sc * fy)), sc, cl)
        E = ear_of(v); sep = 0.60
        bp = E - rt_of(v) * sep
        scb = K.CAST_H["bertillon"] / K.CAST_HD["bertillon"]
        self.put(self.act["ber"], f, Vector((bp.x, bp.y, 0.0)), scb, cl)
        for k, (st, cast, mir) in CAST_STAND.items():
            a = self.act[k]; xy = POS[sh][k]; scx = K.CAST_H[cast] / K.CAST_HD[cast]
            if xy is None:
                a.place(f, (0, 0, -10.0), scale=scx); a.root.hide_render = True
            else:
                bounce = 0.035 * abs(math.sin(2 * math.pi * 3.0 * t + hash(k) % 7)) if cast.startswith("gend") else 0.0
                a.place(f, (xy[0], xy[1], bounce), scale=scx); a.root.hide_render = False
            a.root.keyframe_insert("hide_render", frame=f)
        self.key_fg(f, sh)

    def key_all(self, gs):
        K.set_flicker(1, frame=None)
        for g in gs:
            f = F(g); loc, look = cam_of(g)
            camrig.key_camera(f, loc, look, cam=self.cam, lens=22.0, interp="LINEAR", easing="AUTO")
            self.place_all(g); self.key_cut(f, g)
            K.key_life(f, f, dust=0.4, pendulum=False); K.set_pendulum(t=g / 30.0, frame=f)

    def poses(self, gs):
        ins, ber = self.act["ins"], self.act["ber"]
        for g in gs:
            f = F(g); self.scene.frame_set(f); sh = shot_of(g)
            pi = pose_inspector(g); ins.pose(f, pi, camera=self.cam)
            an = sprites.puppet.figure("inspector17", pi, "q")["anchors"]; hx, hy = an["head"]
            hip = sprites.hip_y("inspector17", pi); k = ins.upper_k[f]
            ear_loc = (hx - 0.505, hip + (hy - 0.04 - hip) * k)                 # screen-left ear
            ear_w = Vector(actors.local_to_world(ins, ear_loc, f, feet=ins.feet[f], camera=self.cam))
            self.ear_w = ear_w
            pb = dict(cast17.STORY17["bertillon_measuring"][1]); pb["seat17"] = None
            pb["mirror"] = False; pb["yaw"] = 0.45
            pb["prop_r"] = dict(type="calipers", scale=(1.0 if sh != 33 else 1.0 - 0.45 * ez((g - 2018) / 10.0)), angle=-90)           # bar vertical, jaws pointing at the ear: one tip above, one below
            pb["rim"] = K.RIM_FOR["bertillon"]; pb["rim_opacity"] = 0.55; pb["rim_w"] = 0.02
            pb["gaze"] = (0.9, 0.45); pb["blink"] = blink(g, [1885, 1950, 2010]); pb["mouth"] = "flat"
            if sh == 31: c = 0.15 + 0.35 * ez(clamp((g - 1862) / 84.0))
            elif sh == 32: c = 0.55 + 0.45 * ez(clamp((g - 1960) / 40.0))
            else: c = 1.0 + 0.02 * math.sin(g * 0.9)
            rt = rt_of(VREF[sh]); off = max(0.0, 1.0 - c)
            tgt_w = ear_w + rt * (-0.34 * off) + Vector((0, 0, -0.62 * off)) + rt * (0.04 * (c - 1.0))
            pb = cast17.silent(pb)
            tl = actors.world_to_local(ber, self.cam, tgt_w, f, feet=sprites.feet_of("bertillon", pb))
            kb = actors.upper_stretch(ber, self.cam, f, pb); hipb = sprites.hip_y("bertillon", pb)
            tl = (tl[0], hipb + (tl[1] - hipb) / kb)
            pb = cast17.hand_for_anchor("bertillon", pb, "r", "calipers_r", tl)
            ber.pose(f, pb, camera=self.cam)
            for k2, (st, cast, mir) in CAST_STAND.items():
                a = self.act[k2]; pq = pose_laugh(st, mir, g, hash(k2) % 5, smirk=st.startswith("prisoner"))
                a.pose(f, pq, camera=self.cam)

    def ear_overlay(self, f, pose):
        ins = self.act["ins"]; an = sprites.puppet.figure("inspector17", pose, "q")["anchors"]; hx, hy = an["head"]
        hip = sprites.hip_y("inspector17", pose); k = ins.upper_k.get(f, 1.0)
        cx, cy = hx - 0.505, hip + (hy - 0.04 - hip) * k
        return ('<g><ellipse cx="%.4f" cy="%.4f" rx="0.075" ry="0.135" fill="#e2503f" stroke="#2a1b1b" stroke-width="0.022"/>'
                '<path d="M%.4f,%.4f q0.05,0.02 0.02,0.10 M%.4f,%.4f q0.03,-0.04 0.0,-0.09" stroke="#9c2a22" stroke-width="0.016" fill="none" stroke-linecap="round"/></g>'
                % (cx, cy, cx - 0.01, cy - 0.07, cx - 0.01, cy + 0.06))

    def ber_overlay(self, f, pose):
        if f - 1 < 2014: return ""
        ber = self.act["ber"]; an = sprites.puppet.figure("bertillon", pose, "q")["anchors"]; hx, hy = an["hand_r"]
        hip = sprites.hip_y("bertillon", pose); k = ber.upper_k.get(f, 1.0); hy = hip + (hy - hip) * k
        sc = pose["prop_r"]["scale"]; w = 0.075 * sc
        out = ""
        for i in range(3):                                       # three fingers wrapped round the vertical bar, over the hand ball
            y = hy - 0.075 + i * 0.062
            out += '<rect x="%.4f" y="%.4f" width="%.4f" height="0.052" rx="0.026" fill="#2b2225" stroke="#120d0f" stroke-width="0.012"/>' % (hx - 0.115, y, 0.22 + w)
        out += '<path d="M%.4f,%.4f h0.16" stroke="#6b5a58" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>' % (hx - 0.08, hy - 0.06)
        return out

    def sprites(self, gs):
        by = {}
        for g in gs: by.setdefault(shot_of(g), []).append(F(g))
        for sh, fr in by.items():
            for k, a in self.act.items():
                ppd = PPD[sh] if k in ("ins", "ber") else (PPD[sh] if sh != 33 else (192 if not QUICK else 64))
                a.render_sprites(ppd, frames=fr, overlay=self.ear_overlay if k == 'ins' else (self.ber_overlay if k == 'ber' else None))

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
