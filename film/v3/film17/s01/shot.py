#!/usr/bin/env python3
"""shot.py -- film 17 take s01: shots 1-3 (hook), g 0..143 + 6 out-handle frames g 144..149.  One location (measure), DAY_INT.
  S1 g 0..47   measure_chair framing: Bertillon lifts the calipers and closes them on the seated prisoner's ear (push + slide left)
  S2 g 48..92  measure_wide framing: queue on the bench, gendarme at the door, Bertillon at the chair (pull-out + slide right)
  S3 g 93..149 measure_low insert on the ear; SNAP (15 f, x1.6) to the next ear (prisoner_b) on "ทีละหู" (g 128)
Blender frame = g + 1.
    python3 shot.py stills a:b[:s] out_dir [scale] [samples]     python3 shot.py final a:b[:s] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import K, bf, ez, lerp, clamp, blink, bpy, Vector, cast17, actors
TMP = os.path.join(HERE, "work")
SLIDE = [0.46]

def _calipers_body(k):
    """cast17's calipers with an adjustable sliding jaw (SLIDE[0] = x of the jaw tip line; default 0.46) so the jaws can close."""
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
    if g is not None and cast == "bertillon": SLIDE[0] = slide_of(int(round(g * 30)))
    return _orig_svg(cast, pose, *a, **kw)
C.sprites.sprite_svg = _svg

def slide_of(g):
    if shot_of(g) != 1: return 0.50
    return lerp(0.24, 0.50, ez((g - 14) / 26.0))          # jaws wide at g14, closing to g40 (gap 0.64 -> 0.38 prop units)
G_CUT2, G_CUT3, G_SNAP0, G_SNAP1, G_SWAP, G_END, H_OUT = 48, 93, 118, 136, 127, 144, 6
RANGES = {1: (0, 47), 2: (48, 92), 3: (93, 143 + H_OUT)}
CH = (0.70, 2.30, 0.5)

def shot_of(g): return 1 if g < G_CUT2 else (2 if g < G_CUT3 else 3)
def mix(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))
def sm(u): return ez(u, "sine")
def lin(u, k=0.25): return k * sm(u) + (1 - k) * clamp(u)     # mostly linear: never a dead end

# ------------------------------------------------------------------ cameras
S1 = (((1.95, 0.35, 1.42), (0.50, 2.28, 1.28)), ((1.40, 1.05, 1.38), (0.45, 2.22, 1.28)))
S2 = (((-1.00, -2.40, 1.50), (-1.25, 1.9, 1.34)), ((-0.60, -3.30, 1.55), (-1.00, 1.9, 1.30)))
S3A = (((-0.58, 1.46, 1.02), (0.58, 2.20, 1.24)), ((-0.14, 1.80, 1.06), (0.74, 2.20, 1.24)))
S3B = (((0.26, 1.24, 1.07), (0.70, 2.20, 1.25)), ((0.52, 1.48, 1.10), (0.64, 2.20, 1.25)))

def cam_of(g):
    s = shot_of(g)
    if s == 1: u = lin((g - 0) / 47.0); a, b = S1
    elif s == 2:
        K2 = [(48, (-1.00, -2.40, 1.50), (-1.25, 1.9, 1.34)), (60, (-0.80, -2.75, 1.52), (-1.15, 1.9, 1.33)),
              (73, (-0.70, -0.25, 1.42), (0.50, 2.1, 1.30)), (92, (-0.55, 0.05, 1.43), (0.55, 2.1, 1.30))]
        for i in range(len(K2) - 1):
            if K2[i][0] <= g <= K2[i + 1][0]:
                t = (g - K2[i][0]) / float(K2[i + 1][0] - K2[i][0]); t = ez(t, "sine") if i == 1 else lin(t)
                return mix(K2[i][1], K2[i + 1][1], t), mix(K2[i][2], K2[i + 1][2], t)
    else:
        if g < G_SNAP0: u = lin((g - G_CUT3) / float(G_SNAP0 - G_CUT3)); a, b = S3A
        elif g < G_SNAP1:
            t = ez((g - G_SNAP0) / float(G_SNAP1 - G_SNAP0), "sine"); a0 = S3A[1]; b0 = S3B[0]
            return mix(a0[0], b0[0], t), mix(a0[1], b0[1], t)
        else: u = lin((g - G_SNAP1) / float(G_END + H_OUT - 1 - G_SNAP1)); a, b = S3B
    return mix(a[0], b[0], u), mix(a[1], b[1], u)

# ------------------------------------------------------------------ staging
def sc_of(cast): return K.CAST_H[cast] / K.CAST_HD[cast]
SPOT = dict(                       # name: (cast, story pose, place xy, seated)
    pa=("prisoner_a", "prisoner_sitting_a", (CH[0], CH[1] - 0.14), "chair"),
    pcc=("prisoner_c", "prisoner_sitting_c", (CH[0], CH[1] - 0.14), "chair"),
    pb1=("prisoner_b", "prisoner_sitting_b", (-2.35, 1.35), "bench"),
    pc1=("prisoner_c", "prisoner_sitting_c", (-2.35, 1.95), "bench"),
    pa1=("prisoner_a", "prisoner_sitting_a", (-2.35, 2.55), "bench"),
    gd=("gendarme_b", "gendarme_standing_b", (-1.15, 0.95), None),
    bert=("bertillon", "bertillon_measuring", (1.45, 1.95), None))
BERT_XY = {1: (0.42, 1.96), 2: (0.12, 2.02), 3: (0.30, 2.42)}
VIS = {1: ("pa", "bert"), 2: ("pa", "bert", "pb1", "pc1", "pa1", "gd"), 3: ("pa", "pcc", "bert")}

def visible(name, g):
    s = shot_of(g)
    if name not in VIS[s]: return False
    if s == 3 and name == "pa": return g < G_SWAP
    if s == 3 and name == "pcc": return g >= G_SWAP
    return True

def base_pose(name):
    cast, story, xy, seated = SPOT[name][:4]
    p = dict(cast17.STORY17[story][1]); p["seat17"] = None
    return p

def yaw_of(name, g):
    return 0.88 if shot_of(g) == 3 else 0.25

def pose_of(name, g, ear=None):
    p = base_pose(name); cast = SPOT[name][0]; t = g / 30.0
    sway = math.sin(t * 2.1 + hash(name) % 7)
    if name in ("pa", "pcc"):
        yw = yaw_of(name, g)
        p.update(yaw=yw, pitch=0.0, expr="worried" if name == "pa" else "unimpressed", mouth="flat", gaze=(0.9 if yw > 0.5 else -0.95, 0.05),
                 head_roll=1.5 * sway, blink=cast17.blink_at(g, 70 if name == "pa" else 83, 11))
        p["squash"] = (1.0 + 0.008 * math.sin(t * 2.4), 1.0 - 0.008 * math.sin(t * 2.4))
    elif name == "bert":
        p.update(lean=4 + 1.5 * sway, pitch=0.22, yaw=0.62, gaze=(1.0, 0.25), blink=cast17.blink_at(g, 90, 30), t=g / 30.0)
    elif name in ("pb1", "pc1", "pa1"):
        k = {"pb1": 0, "pc1": 1, "pa1": 2}[name]
        p.update(yaw=0.3 + 0.1 * k, head_roll=2.0 * math.sin(t * 1.8 + k), blink=cast17.blink_at(g, 77 + 6 * k, 20 + 9 * k))
        p["squash"] = (1.0 + 0.01 * math.sin(t * 2.6 + k), 1.0 - 0.01 * math.sin(t * 2.6 + k))
    elif name == "gd":
        p.update(head_roll=1.2 * sway, blink=cast17.blink_at(g, 95, 40)); p["squash"] = (1 + 0.01 * math.sin(t * 2.2), 1 - 0.01 * math.sin(t * 2.2))
    return p

def theta_of(yaw): return math.radians(min(abs(yaw), 1.2) * 70.0)

def ear_local(an, g, name, s):
    """target for the caliper jaws (puppet-local D): the viewer-left ear (the near ear in profile).  Shot 1 approaches from below-left."""
    hx, hy = an["head"]
    yw = yaw_of(name, g)
    ex = hx - 0.52 * math.cos(theta_of(yw))
    u = clamp((g - 1) / 13.0) if s == 1 else 1.0
    k = 1.0 - sm(u)
    tap = 0.015 * math.sin(g * 0.8) * (1 if u >= 1 else 0)
    return (ex - 0.5 * k, hy + 0.02 + 1.0 * k + tap)

def ears_svg(pose):
    """cartoon ears (the puppet has none) -> (underlay, overlay) SVG, puppet-local D, y down.  Near ear in profile is drawn OVER the head."""
    yw = pose.get("yaw", 0.0); r = pose.get("head_roll", 0.0); dx = pose.get("head_dx", 0.0); dy = pose.get("head_dy", 0.0)
    ink, fill = "#3a2832", "#f4d4cb"
    c = math.cos(theta_of(yw)); prof = abs(yw) > 0.5
    def ear(x, sx, big):
        rx, ry = (0.19, 0.27) if big else 0.15, (0.25)
        if big: rx, ry = 0.19, 0.27
        else: rx, ry = 0.15, 0.25
        return ('<g transform="translate(%.3f %.3f) scale(%d 1)"><ellipse cx="0" cy="0.02" rx="%.3f" ry="%.3f" fill="%s" stroke="%s" stroke-width="0.035"/>'
                '<path d="M-0.05,-0.13 C0.05,-0.15 0.11,0.02 0.03,0.14" fill="none" stroke="%s" stroke-width="0.03" stroke-linecap="round"/></g>' % (x, 0, sx, rx, ry, fill, ink, ink))
    under = ear(0.52 * c, 1, False) + ear(-0.52 * c, 1, False) if not prof else ear(0.52 * c, 1, False)
    over = ear(-0.52 * c, 1, True) if prof else ""
    wrap = lambda g: '<g transform="rotate(%.2f %.3f %.3f) translate(%.3f %.3f)">%s</g>' % (r, dx, dy, dx, dy, g) if g else ""
    return wrap(under), wrap(over)

class Take(C.Take):
    def __init__(self, quality="draft", ppd=None):
        C.Take.__init__(self, "measure_wide", quality, fg=False)
        self.q = quality
        self.cut_stool()
        # own foreground: an unlit-looking gas lamp stand at the right third (shot 2 only)
        mark = set(o.name for o in bpy.data.objects)
        Bf = K._fgB(); K.gas_stand(Bf, (0.10, -1.35, 0), h=1.9, watts=40); K.stool(Bf, (-1.35, -1.45), h=0.5, rot=25); K.ledger_stack(Bf, (-1.35, -1.45, 0.53), n=3, rot=15); Bf.finalize("fg2", ink_t=K.STATE["ink_t"] * 0.7)
        self.fg2 = [o for o in bpy.data.objects if o.name not in mark and o.type == "MESH"]
        self.acts = {n: self.make_actor(n, v[0], os.path.join(TMP, "sprites_" + quality)) for n, v in SPOT.items()}
        for n, a in self.acts.items():
            if n != "gd" and n != "bert":
                a.jobs = (lambda orig: (lambda px, frames=None, overlay=None: [dict(j, underlay=ears_svg(j["pose"])[0], overlay=ears_svg(j["pose"])[1]) for j in orig(px, frames, overlay)]))(a.jobs)
        self.ear = {}

    def cut_stool(self):
        """delete the room's stool + ledger pile at (-0.9, -0.6) (merged into the room meshes) so it is not a foreground block in shot 2."""
        import bmesh
        n = 0
        for ob in bpy.data.objects:
            if ob.type != "MESH" or ob.name.startswith(("c_", "s01")): continue
            mw = ob.matrix_world; me = ob.data
            bm = bmesh.new(); bm.from_mesh(me)
            dead = [v for v in bm.verts if -1.25 < (mw @ v.co).x < -0.55 and -0.95 < (mw @ v.co).y < -0.25 and -0.05 < (mw @ v.co).z < 1.02]
            if dead:
                bmesh.ops.delete(bm, geom=dead, context="VERTS"); n += len(dead); bm.to_mesh(me)
            bm.free()
        print("cut_stool: removed", n, "verts", flush=True)

    def pos_of(self, name, g):
        cast, story, xy, seated = SPOT[name][:4]
        s = shot_of(g)
        if name == "bert": xy = BERT_XY[s]
        p = base_pose(name); sc = sc_of(cast)
        if seated:
            fx, fy = C.sprites.feet_of(cast, p); z = K.HEAD_Z[seated] - sc * fy
        else: z = 0.10 if name == "bert" and s != 3 else 0.0
        return (xy[0], xy[1], z), sc

    def pose(self, gs):
        gs = list(gs); cam = self.cam
        for g in sorted(set(gs) | set(x for y in gs for x in (y - 1, y + 1))):
            if g < 0 or g > 149: continue
            self.key_cam(bf(g), *cam_of(g))
        for g in gs:
            f = bf(g)
            for ob in self.fg2: ob.hide_render = shot_of(g) != 2; ob.keyframe_insert("hide_render", frame=f)
            for n, a in self.acts.items():
                on = visible(n, g); C.vis(a, f, on)
                if on:
                    pos, sc = self.pos_of(n, g); a.place(f, pos, scale=sc)
            K.set_flicker(1.0, frame=f); K.set_dust(0.3, frame=f); K.set_smoke(1.0, frame=f); K.set_pendulum(frame=f)
        for g in gs:                                    # sitters, extras (no hands)
            f = bf(g); self.scene.frame_set(f)
            for n, a in self.acts.items():
                if n != "bert" and visible(n, g): a.pose(f, pose_of(n, g), camera=cam)
        for n, a in self.acts.items():
            if n == "bert": continue
            fr = [bf(g) for g in gs if visible(n, g)]
            if fr: self.render_spr(n, a, fr)
        for g in gs:                                    # Bertillon: jaws pinned on the ear of whoever sits in the chair
            if not visible("bert", g): continue
            f = bf(g); s = shot_of(g); self.scene.frame_set(f)
            sit = "pa" if visible("pa", g) else "pcc"
            an = self.anch[(sit, f)]
            el = ear_local(an, g, sit, s)
            w = actors.local_to_world(self.acts[sit], el, f, camera=cam)
            self.ear[g] = tuple(round(v, 3) for v in w)
            ang, psc = (-52, 1.45) if s != 3 else (-4, 1.1)
            p, info = self.acts["bert"].pose(f, pose_of("bert", g), hands={"r": {"tip": w, "prop": "calipers", "angle": ang, "prop_scale": psc, "stretch": 1.15}}, camera=cam)
            self.ear[(g, "err")] = round(info.get("r", {}).get("error", -1), 3)
        fr = [bf(g) for g in gs if visible("bert", g)]
        if fr: self.render_spr("bert", self.acts["bert"], fr)

    def blur(self, g):
        sc = self.scene; on = G_SNAP0 + 3 <= g <= G_SNAP1 - 3
        sc.render.use_motion_blur = on
        if on: sc.render.motion_blur_shutter = 1.0

    def render_spr(self, n, a, frames):
        # sprite resolution: close-up shot 3 needs more px per D
        hi = [f for f in frames if shot_of(f - 1) == 3]; lo = [f for f in frames if shot_of(f - 1) != 3]
        base = 128 if self.q == "draft" else 256
        if lo: self.sprites_for(a, base, lo)
        if hi: self.sprites_for(a, base * 2, hi)

    def report(self, g):
        f = bf(g); self.scene.frame_set(f); loc, look = cam_of(g); out = dict(g=g, shot=shot_of(g), cam=[round(c, 3) for c in loc], ear=self.ear.get(g), err=self.ear.get((g, "err")))
        heads = {}
        for n, a in self.acts.items():
            if a.card.hide_render or (a.name, f) not in self.anch: continue
            hx, hy = self.anch[(a.name, f)]["head"]; c = actors.local_to_screen(a, self.cam, (hx, hy), f, a.feet.get(f))
            heads[n] = (round(c[0]), round(c[1]))
        out["heads"] = heads; return out

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        os.makedirs(out, exist_ok=True)
        T = Take("draft" if scale < 1 else "final"); T.pose(gs)
        for g in gs:
            print(json.dumps(T.report(g)), flush=True)
            T.blur(g); st = T.render([bf(g)], out, scale, samples)[0]; K.grade(st["path"], scale=scale); os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        T = Take("draft" if scale < 1 else "final")
        for i in range(0, len(todo), 12):                # pose in chunks (sprites) to keep memory low
            ch = todo[i:i + 12]; T.pose(ch)
            for g in ch:
                T.blur(g); st = T.render([bf(g)], out, scale, samples)[0]; K.grade(st["path"], scale=scale)
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); json.dump(T.report(g), open(os.path.join(out, "g_%04d.json" % g), "w"))
                print("g", g, round(st["wall"], 1), flush=True)
