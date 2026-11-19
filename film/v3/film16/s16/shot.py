#!/usr/bin/env python3
"""shot.py -- film 16 take s16 = shot 16, TRENCH CUT-AWAY (LINE trench_cut / DUSK): the lead pipe split open, cloth torn, sparks leaking.
Shot g 1007..1074 (33.57-35.82 s), handles 9 frames each side (g 998..1083).  Hard cut in and out.
    g 998..1012  whip-tilt DIVE: the camera starts high above the pit looking steeply down and tilts / drops to the elevation view
    g 1012..     slow slide along the pipe + push 7 %/s; SNAP x1.7 with a sideways pan on "ไฟรั่วหายลงดิน" (35.07 s -> g 1052)
Split framed at ~45 % of the frame height (QA_ART note); the empty pit floor is cut by the push.  Nobody in frame: no mouths.
    python3 shot.py camreport | probe a:b | final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
import random
import bpy
from mathutils import Vector
TG = C.TG
K, LN = C.K, C.LN
bf, u_of, lerp = C.bf, C.u_of, C.lerp
G0, G1 = C.g_bound(33.57), C.g_bound(35.82)      # 1007, 1075 (exclusive)
H = 9
GA, GZ = G0 - H, G1 + H - 1                       # 998 .. 1083
GS = list(range(GA, GZ + 1))
G_WORD = C.cap_g("ไฟรั่วหาย")                      # 1052
SNAP = (G_WORD - 2, G_WORD + 11)                  # 1049..1064 (15 f)
DIVE = (GA + 2, GA + 18)                              # dive tilt window (the cut falls at G0 = GA + 9: the dive is already half done)
PRE = C.Vector((22.2, -96.2, 0.0))
CAM0 = Vector((20.905, -95.645, 0.278))           # preset camera
LOOK0 = Vector((24.42, -96.293, -1.85))
# split centre is ~42 % down the preset frame: tilt the look point DOWN a little so the split rises to ~45 % ... then the push drifts it
SUBJ = Vector((24.3, -96.25, -1.50)) + Vector((0.0, 0.7 * 0.995, 0.0)) * 0 
START = 0.55                                       # start 0.55 of the way from subject to preset camera: already close
LOOKC = SUBJ + Vector((-0.03, -0.75, 0.0))      # looks right of the split at g0: it starts left of centre, the slide carries it across
CAM = C.CamPath(LOOKC + (CAM0 - SUBJ), LOOKC, GA, GZ, push=0.12, slide_px=-110.0, rise_px=0.0, arc_deg_s=0.0, decay=0.15,
                snaps=[dict(g=SNAP, k=1.9, peak=1.75, shift=(0.0, 0.0))])
HIGH = Vector((-1.0, 0.4, 3.6))                    # dive start: offset from the drift pose (high above, a little behind)


def cam_pose(g):
    loc, look = CAM.at(g)
    u = u_of(g, DIVE[0], DIVE[1], "quad_out") if hasattr(C.ease, "__call__") else 0.0
    k = 1.0 - u
    if k > 0:
        loc = loc + HIGH * (k ** 1.6)
        look = look + Vector((0.0, 0.0, -0.3)) * k
    return loc, look


# ----------------------------------------------------------------------------- electric sparks (runtime set dressing, director's TAKE gate)
CX, CY = LN.PIT
FY = CY + LN.PIT_HL
R_, Z0 = 0.17, -0.72
YA = FY - R_ * 0.8
X0, X1 = CX - 0.56, CX + 0.56
FLOOR = -LN.PIT_D + 0.04


def bolt_pts(rng, x, length, lean):
    """zig-zag polyline (sb metres) from the lower lip of the tear down the soil face: electric, not a water drop."""
    y = YA - 0.16
    p = [(x, y, Z0 - 0.10)]
    n = rng.randint(9, 14)
    z, xx = Z0 - 0.10, x
    for i in range(n):
        z -= length / n * rng.uniform(0.5, 1.5)
        xx += lean / n + rng.uniform(-0.075, 0.075)
        p.append((xx, y - rng.uniform(0.0, 0.05), max(z, FLOOR)))
    return p


def build_sparks(g):
    """a fresh set of bolts per frame (random seed = frame): white-hot core rod + cyan halo rod, hot spots at the ends, flying beads."""
    rng = random.Random(g * 7919 + 13)
    M = TG.STATE["M"]
    core = TG._emit_mat("bolt_core", "#ffffff", 40.0)
    halo = TG._emit_mat("bolt_halo", "#38d8ff", 7.0, alpha=0.30)
    mb = K.MB("s16_bolts_%04d" % g)
    nb = rng.randint(5, 8)
    for b in range(nb):
        x = X0 + (X1 - X0) * rng.uniform(0.08, 0.92)
        ln = rng.choice([0.25, 0.4, 0.6, 0.85]) * rng.uniform(0.7, 1.2)
        pts = bolt_pts(rng, x, ln, rng.uniform(-0.35, 0.35))
        for a, c in zip(pts[:-1], pts[1:]):
            mb.rod(halo, a, c, 0.012, 0.012, 5, caps=True)
            mb.rod(core, a, c, 0.0045, 0.0045, 5, caps=True)
        e = pts[-1]
        mb.ell(core, e, (0.016, 0.016, 0.016), (6, 4))                      # hot spot where it bites into the soil
        mb.ell(halo, e, (0.035, 0.026, 0.035), (6, 4))
        for _ in range(rng.randint(1, 3)):                                   # flying spark beads
            q = (e[0] + rng.uniform(-0.22, 0.22), e[1] - rng.uniform(0, 0.04), e[2] + rng.uniform(-0.02, 0.2))
            mb.ell(core, q, (0.008, 0.008, 0.008), (5, 3))
    for k in range(rng.randint(2, 3)):                                       # arcs jumping from the lip to the wire inside the mouth
        x = X0 + (X1 - X0) * rng.uniform(0.15, 0.85)
        a = (x, YA - 0.14, Z0 - 0.09)
        c = (x + rng.uniform(-0.12, 0.12), YA - 0.03, Z0 + 0.05)
        m = ((a[0] + c[0]) / 2 + rng.uniform(-0.05, 0.05), YA - 0.11, (a[2] + c[2]) / 2)
        for u, v in ((a, m), (m, c)):
            mb.rod(halo, u, v, 0.009, 0.009, 5, caps=True)
            mb.rod(core, u, v, 0.0035, 0.0035, 5, caps=True)
    obs = mb.finish()
    for o in obs:
        o.visible_shadow = False
        o.visible_glossy = False
        o.visible_diffuse = False
    return obs


def plain_copper():
    """the set's copper has a wood-grain wave: swap the pit wire for flat bright copper."""
    m = bpy.data.materials.new("s16_copper")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out, em, df, mx = (nt.nodes.new(t) for t in ("ShaderNodeOutputMaterial", "ShaderNodeEmission", "ShaderNodeBsdfDiffuse", "ShaderNodeMixShader"))
    df.inputs["Color"].default_value = (0.80, 0.38, 0.15, 1.0)
    em.inputs["Color"].default_value = (0.95, 0.52, 0.22, 1.0)
    em.inputs["Strength"].default_value = 0.35
    mx.inputs[0].default_value = 0.45
    nt.links.new(df.outputs[0], mx.inputs[1])
    nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    for o in bpy.data.objects:
        if o.name.startswith("pitwire") and o.type == "MESH":
            for i, sl in enumerate(o.material_slots):
                if sl.material and "copper" in sl.material.name:
                    o.material_slots[i].material = m


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "trench_cut", light="DUSK", quality=quality, name="cam_s16")
        self.key_cam(bf(GA), *cam_pose(GA))
        plain_copper()
        self.spark = [o for o in bpy.data.objects if o.name == "pitspark"][0]
        self.bolts = {}

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_pose(g))
            TG.set_leak("pipe", 0.0, frame=f)                         # hide the set's cyan drips
            obs = self.bolts[g] = build_sparks(g)                     # the set's cyan drip ovals are NOT used (they read as water)
            for ob in obs:
                ob.hide_render = True
                if f > 1:
                    C.key_vis(ob, False, f - 1)
                C.key_vis(ob, True, f)
                C.key_vis(ob, False, f + 1)
            rg = random.Random(g * 31 + 5)
            self.spark.data.energy = (25.0 + 120.0 * rg.random() ** 2) * TG.SC * TG.SC          # crackling cyan light on the soil
            self.spark.data.keyframe_insert("energy", frame=f)

    def report(self, g):
        self.scene.frame_set(bf(g))
        loc, look = cam_pose(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads={}, split_px=TG.project(tuple(SUBJ + Vector((0, 0, 0.0)))))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = C.CamPath.report(CAM, GS[:-1])
        for r in rows[::4]: print(r)
        print("longest run under 0.25 px/frame: %d frames" % worst); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GZ]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                st = Tk.render([g], out, scale=scale, samples=6)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK if False else HERE + "/work", "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
