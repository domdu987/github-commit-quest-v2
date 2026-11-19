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
G_CUT2, G_CUT3, G_SNAP0, G_SNAP1, G_SWAP, G_END, H_OUT = 48, 93, 120, 135, 127, 144, 6
RANGES = {1: (0, 47), 2: (48, 92), 3: (93, 143 + H_OUT)}
CH = (0.70, 2.30, 0.5)

def shot_of(g): return 1 if g < G_CUT2 else (2 if g < G_CUT3 else 3)
def mix(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))
def sm(u): return ez(u, "sine")
def lin(u, k=0.25): return k * sm(u) + (1 - k) * clamp(u)     # mostly linear: never a dead end

# ------------------------------------------------------------------ cameras
S1 = (((1.95, 0.35, 1.42), (0.50, 2.28, 1.28)), ((1.28, 1.20, 1.36), (0.40, 2.20, 1.28)))
S2 = (((-2.15, -3.45, 1.50), (0.15, 2.45, 1.36)), ((-1.75, -4.05, 1.58), (0.75, 2.30, 1.30)))
S3A = (((0.50, 1.36, 1.04), (0.60, 2.30, 1.26)), ((0.62, 1.58, 1.08), (0.58, 2.30, 1.26)))      # ear A framing: drift 
S3B = (((0.30, 1.58, 1.06), (0.56, 2.30, 1.26)), ((0.42, 1.34, 1.10), (0.60, 2.30, 1.26)))      # ear B: after the snap (closer, other side)

def cam_of(g):
    s = shot_of(g)
    if s == 1: u = lin((g - 0) / 47.0); a, b = S1
    elif s == 2: u = lin((g - G_CUT2) / 44.0); a, b = S2
    else:
        if g < G_SNAP0: u = lin((g - G_CUT3) / float(G_SNAP0 - G_CUT3)); a, b = S3A
        elif g < G_SNAP1:
            t = sm((g - G_SNAP0) / float(G_SNAP1 - G_SNAP0)); a0 = S3A[1]; b0 = S3B[0]
            return mix(a0[0], b0[0], t), mix(a0[1], b0[1], t)
        else: u = lin((g - G_SNAP1) / float(G_END + H_OUT - 1 - G_SNAP1)); a, b = S3B
    return mix(a[0], b[0], u), mix(a[1], b[1], u)

# ------------------------------------------------------------------ staging
def sc_of(cast): return K.CAST_H[cast] / K.CAST_HD[cast]
SPOT = dict(                       # name: (cast, story pose, place xy (z handled), seated, opts)
    pa=("prisoner_a", "prisoner_sitting_a", (CH[0], CH[1]), "chair"),
    pbc=("prisoner_b", "prisoner_sitting_b", (CH[0], CH[1]), "chair"),
    pbq=("prisoner_b", "prisoner_standing_b", (-1.55, 1.2), None),
    pc=("prisoner_c", "prisoner_sitting_c", (-2.35, 0.85), "bench"),
    gd=("gendarme_b", "gendarme_standing_b", (1.3, -1.5), None),
    bert=("bertillon", "bertillon_measuring", (1.45, 1.95), None))
BERT_XY = {1: (0.30, 2.08), 2: (0.30, 2.08), 3: (-0.02, 1.98)}
VIS = {1: ("pa", "bert"), 2: ("pa", "bert", "pbq", "pc", "gd"), 3: ("pa", "pbc", "bert")}

def visible(name, g):
    s = shot_of(g)
    if name not in VIS[s]: return False
    if s == 3 and name == "pa": return g < G_SWAP
    if s == 3 and name == "pbc": return g >= G_SWAP
    return True

def base_pose(name):
    cast, story, xy, seated = SPOT[name][:4]
    p = dict(cast17.STORY17[story][1]); p["seat17"] = None
    return p

def pose_of(name, g, ear=None):
    p = base_pose(name); cast = SPOT[name][0]; t = g / 30.0
    sway = math.sin(t * 2.1 + hash(name) % 7)
    if name in ("pa", "pbc"):
        p.update(yaw=0.25, pitch=0.0, expr="worried" if name == "pa" else "unimpressed", mouth="flat", gaze=(-0.95, 0.05),
                 head_roll=2.0 * sway, blink=cast17.blink_at(g, 70 if name == "pa" else 83, 11))
        p["squash"] = (1.0 + 0.008 * math.sin(t * 2.4), 1.0 - 0.008 * math.sin(t * 2.4))
        p = cast17.with_expr(p, "worried" if name == "pa" else "unimpressed") if False else p
    elif name == "bert":
        p.update(lean=4 + 1.5 * sway, pitch=0.18, gaze=(0.8, 0.15), blink=cast17.blink_at(g, 90, 30))
    elif name == "pbq":
        p.update(yaw=0.35, head_roll=2.5 * sway, blink=cast17.blink_at(g, 64, 5)); p["squash"] = (1 + 0.012 * math.sin(t * 3), 1 - 0.012 * math.sin(t * 3))
    elif name == "pc":
        p.update(head_roll=2.0 * math.sin(t * 1.8 + 1.0), blink=cast17.blink_at(g, 77, 20))
    elif name == "gd":
        p.update(head_roll=1.2 * sway, blink=cast17.blink_at(g, 95, 40)); p["squash"] = (1 + 0.01 * math.sin(t * 2.2), 1 - 0.01 * math.sin(t * 2.2))
    return p

def ear_local(an, g, name, s):
    """target on the sitter's card for the caliper jaws (puppet-local D): on the screen-right ear; approach in shot 1 from below-right."""
    hx, hy = an["head"]
    u = clamp((g - 2) / 18.0) if s == 1 else 1.0
    k = 1.0 - sm(u)
    tap = 0.03 * math.sin(g * 0.9) * (1 if u >= 1 else 0)
    return (hx - 0.56 - 0.9 * k + tap, hy + 0.06 + 0.9 * k)

def ears_svg(pose):
    """two big cartoon ears behind the head disc (underlay, puppet-local D, y down): the puppet has none."""
    r = pose.get("head_roll", 0.0); dx = pose.get("head_dx", 0.0); dy = pose.get("head_dy", 0.0)
    ink, fill, inner = "#3a2832", "#f4d4cb", "#d9a89f"
    parts = []
    for sx in (-1, 1):
        parts.append('<g transform="translate(%.3f %.3f) scale(%d 1)"><ellipse cx="0.52" cy="0.02" rx="0.15" ry="0.25" fill="%s" stroke="%s" stroke-width="0.035"/>'
                     '<path d="M0.50,-0.12 C0.60,-0.14 0.65,0.02 0.58,0.13" fill="none" stroke="%s" stroke-width="0.03" stroke-linecap="round"/></g>' % (dx, dy, sx, fill, ink, ink))
    return '<g transform="rotate(%.2f %.3f %.3f)">%s</g>' % (r, dx, dy, "".join(parts))

class Take(C.Take):
    def __init__(self, quality="draft", ppd=None):
        C.Take.__init__(self, "measure_wide", quality)
        self.q = quality
        mark = set(o.name for o in bpy.data.objects)
        K.PRESETS["measure_low"]["fg"](self.A)
        self.fg_low = [o for o in bpy.data.objects if o.name not in mark and o.type == "MESH"]
        self.acts = {n: self.make_actor(n, v[0], os.path.join(TMP, "sprites_" + quality)) for n, v in SPOT.items()}
        for n, a in self.acts.items():
            if n != "bert" and not n.startswith("gd"):
                a.jobs = (lambda orig: (lambda px, frames=None, overlay=None: [dict(j, underlay=ears_svg(j["pose"])) for j in orig(px, frames, overlay)]))(a.jobs)
        self.ear = {}

    def pos_of(self, name, g):
        cast, story, xy, seated = SPOT[name][:4]
        s = shot_of(g)
        if name == "bert": xy = BERT_XY[s]
        p = base_pose(name); sc = sc_of(cast)
        if seated:
            fx, fy = C.sprites.feet_of(cast, p); z = K.HEAD_Z[seated] - sc * fy
        else: z = 0.0
        return (xy[0], xy[1], z), sc

    def pose(self, gs):
        gs = list(gs); cam = self.cam
        for g in gs:
            f = bf(g); loc, look = cam_of(g); self.key_cam(f, loc, look)
            for ob in self.fg_low: ob.hide_render = shot_of(g) != 3; ob.keyframe_insert("hide_render", frame=f)
            for n, a in self.acts.items():
                on = visible(n, g); C.vis(a, f, on)
                if on:
                    pos, sc = self.pos_of(n, g); a.place(f, pos, scale=sc)
            K.set_flicker(1.0, frame=f); K.set_dust(1.0, frame=f); K.set_smoke(1.0, frame=f); K.set_pendulum(frame=f)
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
            sit = "pa" if visible("pa", g) else "pbc"
            an = self.anch[(sit, f)]
            el = ear_local(an, g, sit, s)
            w = actors.local_to_world(self.acts[sit], el, f, camera=cam)
            self.ear[g] = tuple(round(v, 3) for v in w)
            p, info = self.acts["bert"].pose(f, pose_of("bert", g), hands={"r": {"tip": w, "prop": "calipers", "angle": -22, "prop_scale": 1.35}}, camera=cam)
            self.ear[(g, "err")] = round(info.get("r", {}).get("error", -1), 3)
        fr = [bf(g) for g in gs if visible("bert", g)]
        if fr: self.render_spr("bert", self.acts["bert"], fr)

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
            st = T.render([bf(g)], out, scale, samples)[0]; K.grade(st["path"], scale=scale); os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        T = Take("draft" if scale < 1 else "final")
        for i in range(0, len(todo), 12):                # pose in chunks (sprites) to keep memory low
            ch = todo[i:i + 12]; T.pose(ch)
            for g in ch:
                st = T.render([bf(g)], out, scale, samples)[0]; K.grade(st["path"], scale=scale)
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); json.dump(T.report(g), open(os.path.join(out, "g_%04d.json" % g), "w"))
                print("g", g, round(st["wall"], 1), flush=True)
