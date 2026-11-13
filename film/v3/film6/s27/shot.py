#!/usr/bin/env python3
"""shot.py -- film 6 take s27: shots 27, 28 (plan 73.87-81.58 s = g 2216..2446) + 6-frame handles (g 2210..2215, 2447..2452),
market AFTERNOON.

    shot 27  g 2216..2368  (in-handle g 2210..2215)  "ไอ้สิบสามคว้าก้อนที่สิบสาม วิ่งฝ่าฝูงคน ตะโกนว่า น้ำหนักมันระเหยไปเองครับ"
             a g 2210..2262  down the lane to Henry's glowing bakery front: kit bursts out of the door with the pale 13th loaf held
                             high and runs at us (run cycle, 16 f)
             b g 2263..2316  low tracking in front of him: through the crowd (townsfolk with rotten veg turn to look)
             c g 2317..2368  medium tracking: kit SHOUTS -- lip-sync on the quoted line from 77.27 s (g 2321)
    shot 28  g 2369..2446  (out-handle g 2447..2452)  "ขาดไปเท่าไหร่ ผมชดให้ แล้ววางมันลงบนตาชั่ง"  (hard cut)
             d g 2369..2410  at the big balance: kit skids in beside the bread pan, still shouting up at the inspector (lip-sync
                             to 80.21 s = g 2409), the loaf high
             e g 2411..2452  ECU on the bread pan: kit's hand brings the pale loaf over the pile and plants it on top (g 2424:
                             set_loaves 13), pats it, withdraws; the beam stays at -7 (it tips in the next take)
Mouths: kit's only, on the quoted line 77.27..80.21 s (cast6.talk_mouth); everyone else static.  NO depth of field (common.Take).
Internal shot ids 27, 28: Blender frame of g = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 27 a:b[:step]
    python3 shot.py stills 27,28 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 27,28 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6, render = C.B, C.actors, C.camrig, C.cast6, C.render
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(73.87), C.g_bound(81.58)            # 2216, 2447
H = 6
G_CUT = C.g_of(78.86)                                    # 2369: cut 27 -> 28 at the end of "...ระเหยไปเองครับ"
RANGES = {27: (G0 - H, G_CUT - 1), 28: (G_CUT, G1 + H - 1)}
FR = dict(a=(2210, 2262), b=(2263, 2316), c=(2317, 2368), d=(2369, 2410), e=(2411, 2452))
BEAM = -7.0
TALK = (C.g_of(77.27), C.g_of(80.21))                    # 2321 .. 2409: the quoted line (lip-sync)
G_PLANT = 2424                                           # "วางมันลง" (80.21 .. 80.98 s = g 2409 .. 2432)
RUN_N = 16.0                                             # frames per run cycle

# ----------------------------------------------------------------------------- staging (market world D)
DOOR = (-21.0, 3.5)
KIT_RUN = dict(a=((-20.6, 3.7), (-16.2, 4.4)), b=((-14.6, 4.5), (-10.3, 4.6)), c=((-8.4, 4.55), (-4.2, 4.6)))
KIT_D = ((2.00, 4.05), (4.00, 4.25))                     # skids in from frame-left, stops by the crate right of the pan                     # skids in beside the bread pan (front-left of it)
KIT_E = (3.85, 4.95)                                     # ECU: up on a market crate at the front-right of the bread pan
KIT_E_Z = 1.00
CRATE = (3.85, 4.95, 0.80, 0.60, 1.00)                 # runtime prop: x, y, width, depth, height
INSP = (1.75, 4.75)                                      # where shots 24-25 left him
LOAF13 = Vector((3.05, 5.88, 2.836))                     # the 13th loaf's spot on top of the pile at beam -7 (pan top z 2.216)
CROWD = {"cw1": ("woman1", (-16.0, 3.0), "tomato"), "cm1": ("man1", (-15.0, 6.3), "cabbage"),
         "cw2": ("woman1", (-11.0, 2.9), "tomato"), "cm2": ("man1", (-10.0, 6.4), "cabbage"),
         "cb1": ("baker2", (-6.0, 2.8), None), "cw3": ("woman1", (-5.5, 6.5), "cabbage"), "cm3": ("man1", (-1.0, 3.0), "tomato")}

PALE_BREAD = dict(light="#fcefd2", base="#f0d39c", dark="#c99a5e", crust="#ab7a44", score="#fff6dc")
CROWD_AT = {"a": {"cw1": (-17.5, 2.6), "cm1": (-16.0, 5.6), "cb1": (-19.0, 2.3), "cw3": (-18.6, 6.0)},
            "b": {"cb1": (-6.5, 6.4), "cm3": (-2.2, 6.7), "cw3": (-18.6, 6.0)},
            "c": {"cm3": (-2.2, 6.7), "cb1": (-6.2, 6.5)}}   # push the near-lane figures to the north flank so their heads clear y 880
CAMS = {
    "a": (((-12.6, 4.90, 2.10), (-21.0, 3.70, 2.35)), ((-12.9, 4.95, 2.10), (-21.0, 3.80, 2.30)), 24.0),
    "c": None, "b": None,                                # tracking: computed from kit's position (cam_at)
    "d": (((4.30, 0.90, 2.05), (2.95, 5.30, 2.20)), ((4.20, 1.15, 2.05), (2.95, 5.30, 2.20)), 22.0),
    "e": (((1.60, 2.40, 3.25), (3.60, 5.60, 2.60)), ((1.75, 2.60, 3.20), (3.60, 5.60, 2.60)), 26.0),
}


def framing(g):
    for k, (a, b) in FR.items():
        if a <= g <= b:
            return k
    raise ValueError(g)


def fu(g):
    a, b = FR[framing(g)]
    return (g - a) / float(b - a)


def kit_xy(g):
    k = framing(g)
    if k in KIT_RUN:
        (x0, y0), (x1, y1) = KIT_RUN[k]
        u = fu(g)
        return (lerp(x0, x1, u), lerp(y0, y1, u))
    if k == "d":
        u = ez(clamp((g - FR["d"][0]) / 14.0), "quad_out")           # skids to a stop in 14 frames
        (x0, y0), (x1, y1) = KIT_D
        return (lerp(x0, x1, u), lerp(y0, y1, u))
    return KIT_E


def cam_at(g):
    k = framing(g)
    u = ez(fu(g), "sine")
    if k == "b":                                          # retreating ahead of him, low, from slightly lane-left
        x, y = kit_xy(g)
        d = lerp(4.6, 4.0, u)
        return Vector((x + d, y - 1.25, 1.45)), Vector((x - 2.0, y + 0.10, 1.85)), 24.0
    if k == "c":
        x, y = kit_xy(g)
        d = lerp(3.5, 3.1, u)
        return Vector((x + d, y - 0.95, 1.95)), Vector((x - 1.5, y + 0.20, 1.95)), 24.0
    (l0, t0), (l1, t1), lens = CAMS[k]
    return Vector(lerp(l0, l1, u)), Vector(lerp(t0, t1, u)), lens


def talking(g):
    return TALK[0] <= g <= TALK[1]


# ----------------------------------------------------------------------------- poses
def kit_pose(g):
    k = framing(g)
    bl = blink(g, [2240, 2300, 2380, 2440])
    if k in ("a", "b", "c"):
        base = dict(yaw=0.30, pitch=-0.25, expr="shouting" if talking(g) else "determined", fx=["sweat"], head_roll=-6,
                    arm_r=dict(hand=(0.62, -0.62 + 0.04 * math.sin(g * 0.8)), bend=-0.9, stretch=1.3, layer="top"),
                    prop_r="loaf", t=g / 30.0)
        p = cast6.cycle("kit", (g / RUN_N) % 1.0, "run", base=base, arms="l")
        p["yaw"] = 0.30
        if k == "a" and g < 2222:                         # bursting out of the door: first strides
            p["lean"] = p.get("lean", 12) + 4
    elif k == "d":
        u = clamp((g - FR["d"][0]) / 14.0)
        p = dict(yaw=-0.35, pitch=-0.45, expr="shouting" if talking(g) else "determined", fx=["sweat"],
                 head_roll=lerp(10, 5, u) + 2 * math.sin(g * 0.5), lean=lerp(-14, -4, ez(u)),
                 arm_r=dict(hand=(0.55, -0.70 + 0.05 * math.sin(g * 0.6)), bend=-0.9, stretch=1.3, layer="top"), prop_r="loaf",
                 arm_l=dict(hand=(-0.55, 0.25), bend=-0.6, stretch=1.2, shape="open"),
                 legs=dict(preset="step", stride=lerp(1.0, 0.5, u), crouch=lerp(0.12, 0.03, u)), t=g / 30.0)
    else:                                                 # e: planting the loaf (screen-left hand pinned by the take)
        p = dict(yaw=-0.55, pitch=0.35, expr="determined" if g < G_PLANT + 2 else "grinning", head_roll=6, lean=-16, gaze=(-0.8, 0.4),
                 arm_r=dict(hand=(0.35, 0.60), bend=0.5, stretch=1.1, shape="open"), legs=dict(preset="step", stride=0.4), t=g / 30.0)
    if talking(g):
        p["mouth"] = cast6.talk_mouth(g, level=1.0, seed=27, hold=2)
    p["blink"] = bl
    return p


def plant_path(g):
    """world point of the loaf centre in framing e (None = no loaf in the hand: it is on the pile or the hand is empty)."""
    above = LOAF13 + Vector((0.12, -0.08, 0.10))         # kit can just reach the top of the pile from his crate: come in
    start = LOAF13 + Vector((0.60, -0.35, -0.05))        # from his side, low, then over and down onto the spot
    if g < G_PLANT - 9:
        u = ez((g - FR["e"][0]) / float(G_PLANT - 9 - FR["e"][0]))
        return start.lerp(above, u), True
    if g < G_PLANT:
        u = ez((g - (G_PLANT - 9)) / 9.0, "quad_in")
        return above.lerp(LOAF13, u), True
    return None, False


def hand_after(g):
    """framing e after the plant: the hand pats the loaf (g PLANT..+8) then withdraws."""
    pat = LOAF13 + Vector((0.05, -0.10, 0.12 + 0.05 * abs(math.sin((g - G_PLANT) * 0.9))))
    if g <= G_PLANT + 8:
        return pat
    u = ez((g - G_PLANT - 8) / 12.0)
    return pat.lerp(LOAF13 + Vector((0.75, -0.45, -0.45)), u)


def insp_pose(g):
    k = framing(g)
    u = ez(clamp((g - 2372) / 10.0))
    return dict(yaw=lerp(0.20, 0.45, u), pitch=lerp(-0.2, 0.45, u), expr="determined", head_roll=lerp(0, -5, u),
                gaze=(lerp(0.3, 0.6, u), lerp(-0.2, 0.8, u)), arm_l="akimbo",
                arm_r=dict(hand=(0.62, 1.00), bend=-0.3, stretch=1.2), prop_r="basket", basket=dict(loaves=0, tilt=20),
                legs="wide", blink=blink(g, [2390, 2430]), t=g / 30.0)


def crowd_pose(name, g, kx):
    cast, (x, y), veg = CROWD[name]
    x, y = CROWD_AT.get(framing(g), {}).get(name, (x, y))
    look = clamp((kx - x + 3.0) / 6.0, -1.0, 1.0)           # turn to follow kit as he passes (he runs toward +x)
    side = 1 if y < 4.6 else -1
    p = dict(yaw=0.35 * look, pitch=-0.25, expr="shocked" if abs(kx - x) < 2.5 else "angry", head_roll=4 * look,
             gaze=(0.8 * look, 0.0), legs="stand", blink=blink(g, [2230 + 7 * len(name) + int(x) % 9, 2330 + int(y * 3)]), t=g / 30.0)
    if veg:
        p.update(prop_r=veg, arm_r=dict(hand=(0.60, -0.62 + 0.03 * math.sin(g * 0.5 + x)), bend=-1.0, stretch=1.3, layer="top"),
                 arm_l=dict(hand=(-0.45, 0.45), bend=-0.4, shape="open", stretch=1.2))
    else:
        p.update(arm_r="down", arm_l="down")
    if side < 0:
        p["mirror"] = True
    return p


# ----------------------------------------------------------------------------- the take
def key_vis(actor, f, visible):
    for ob in actor.objects():
        if ob is None:
            continue
        ob.hide_render = not visible
        ob.keyframe_insert("hide_render", frame=f)
        fc = C._fcurve(ob, "hide_render")
        if fc is not None:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


class Take(C.Take):
    CASTING = dict(a=["kit", "cw1", "cm1", "cb1", "cw3"], b=["kit", "cw1", "cm1", "cw2", "cm2", "cb1", "cw3", "cm3"],
                   c=["kit", "cw2", "cm2", "cb1", "cw3", "cm3"], d=["kit", "insp"], e=["kit"])

    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "AFTERNOON", quality=quality, lens=24.0, name="cam_s27")
        sd = os.path.join(TMP, "sprites" + os.environ.get("SPR_TAG", ""))
        self.actors["kit"] = C.make_actor("kit", "kit", sd)
        self.actors["insp"] = C.make_actor("insp", "inspector_royal", sd)
        for n, (cast, xy, veg) in CROWD.items():
            self.actors[n] = C.make_actor(n, cast, sd)
        self.dial = make_dial()
        self.ik_err = {}
        self.crate = make_crate()

    def pose(self, shot, gs):
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(g)
            self.key_cam(f, loc, look, lens)
            B.set_big_scale(BEAM, frame=f)
            B.set_loaves(13 if (framing(g) == "e" and g >= G_PLANT) else 12, frame=f)
            self.key_set(f)
            k = framing(g)
            for n, a in A.items():
                key_vis(a, f, n in self.CASTING[k])
            C.place(A["kit"], f, kit_xy(g), KIT_E_Z if k == "e" else 0.0)
            C.place(A["insp"], f, INSP)
            for n, (cast, xy, veg) in CROWD.items():
                C.place(A[n], f, CROWD_AT.get(k, {}).get(n, xy))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            k = framing(g)
            p = kit_pose(g)
            if k == "e":
                pt, carry = plant_path(g)
                if carry:
                    p["prop_l"] = dict(type="loaf", scale=1.0)
                    hands = C.held_on_palm(A["kit"], self.cam, f, pt, up=C.LOAF_TIP, side="l", bend=0.5, stretch=1.5, layer="top")
                else:
                    hands = {"l": {"hand": tuple(hand_after(g)), "bend": 0.5, "stretch": 1.5, "shape": "open", "layer": "top"}}
                _, inf = A["kit"].pose(f, p, hands=hands, camera=self.cam)
                self.ik_err[g] = round(float(inf.get("l", {}).get("error", 0.0)), 3)
            else:
                A["kit"].pose(f, p, camera=self.cam)
            if "insp" in self.CASTING[k]:
                A["insp"].pose(f, insp_pose(g), camera=self.cam)
            kx = kit_xy(g)[0]
            for n in CROWD:
                if n in self.CASTING[k]:
                    A[n].pose(f, crowd_pose(n, g, kx), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        for n, ppd in [("kit", 448), ("insp", 384)] + [(n, 256) for n in CROWD]:
            ff = [f for f in fr if f in A[n].poses]
            if ff:
                keep = dict(cast6.BREAD)
                if n == "kit":                            # kit's loaf is THE 13th loaf: the paler one (continuity with set_loaves 13)
                    cast6.BREAD.update(PALE_BREAD)
                try:
                    res = A[n].render_sprites(ppd, frames=ff)
                finally:
                    cast6.BREAD.clear(); cast6.BREAD.update(keep)
                for f2, r in zip(ff, res):
                    self.anch[(n, f2)] = r["anchors"]
                    if r.get("clipped"):
                        print("WARNING clipped", n, f2, flush=True)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(g)
        v = look - loc
        out = dict(shot=shot, g=g, framing=framing(g), cam=[round(c, 3) for c in loc], lens=lens,
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   heads=C.head_report(self, f), loaves=13 if (framing(g) == "e" and g >= G_PLANT) else 12, beam=BEAM,
                   mouth=self.actors["kit"].poses.get(f, {}).get("mouth"))
        if framing(g) == "e":
            pt, carry = plant_path(g)
            tgt = pt if carry else hand_after(g)
            out["target_px"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(tgt), f)[:2]]
            out["ik_err"] = self.ik_err.get(g)
            out["loaf13_px"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(LOAF13), f)[:2]]
            an = self.anch.get(("kit", f))
            if an:
                hx, hy = an["prop_tip_l"] if carry else an["hand_l"]
                hp = actors.local_to_screen(self.actors["kit"], self.cam, (hx, hy), f, self.actors["kit"].feet.get(f))
                out["hand_px"] = [round(hp[0], 1), round(hp[1], 1)]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def make_crate():
    """runtime prop: a plain market crate (slatted box) at the front-right of the bread pan; kit stands on it in the ECU (e)."""
    import bmesh
    x, y, w, d, h = CRATE
    m = bpy.data.materials.get("wood") or bpy.data.materials.get("wood_d")
    if m is None:
        m = bpy.data.materials.new("crate_wood"); m.use_nodes = True
        m.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.45, 0.28, 0.14, 1)
    me = bpy.data.meshes.new("crate_me"); bm = bmesh.new()
    from mathutils import Matrix
    # four walls of horizontal slats with gaps + a lid
    for k in range(3):
        z0 = 0.04 + k * h / 3.0; hh = h / 3.0 - 0.05
        for (cx_, cy_, sx, sy) in ((x, y - d / 2, w, 0.04), (x, y + d / 2, w, 0.04), (x - w / 2, y, 0.04, d), (x + w / 2, y, 0.04, d)):
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.LocRotScale(Vector((cx_, cy_, z0 + hh / 2)), None, Vector((sx, sy, hh))))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.LocRotScale(Vector((x, y, h - 0.02)), None, Vector((w, d, 0.04))))
    for sx in (-1, 1):
        for sy in (-1, 1):
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.LocRotScale(Vector((x + sx * (w / 2 - 0.03), y + sy * (d / 2 - 0.03), h / 2)), None, Vector((0.07, 0.07, h))))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("crate", me); ob.data.materials.append(m); bpy.context.scene.collection.objects.link(ob)
    return ob


def make_dial():
    """the same runtime dial + needle as take s24 (continuity: it is on the balance in shots 24-25)."""
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s24"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("s24shot", os.path.join(os.path.dirname(HERE), "s24", "shot.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.Take.make_dial(None)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
