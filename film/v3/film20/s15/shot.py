#!/usr/bin/env python3
"""shot.py -- film 20 take s15 = shot 15, THE PERMIT (g 996..1091 + handles: 8 in-dissolve g 988..995, 4 out-cut g 1092..1095).
"แต่ใบอนุญาต ให้หอตั้งอยู่ ได้แค่ 20 ปี ครบแล้วต้องรื้อ" -- the permit lets the tower stand only 20 years, then it must come down.

TOWER tower_fair / DAY 1889 (set_year 1889, crowd level 3).  Eye-level two-shot in depth on the fair ground: Eiffel (proud) in front,
the official in the tricolour sash behind-right offering the sealed document; Eiffel takes it; on "ครบแล้วต้องรื้อ" (event g 1067) his smile
drops (proud -> worried + sweat, swapped on the closed frame of a 3-frame blink) and the camera SNAPS in on him.
Camera (c20.CamPath): push 8 %/s toward Eiffel's head + slide 30 px/s + arc, decay, one snap x1.55 on the drop.  Preset FG (lamp-post,
bench) moved with the camera so they stay 1-2 D from the lens.  Mouths never move (no quote here).
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out> [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
import tower20                                           # noqa: E402  (runtime grade bump, qa_stats wants saturation >= 0.47)
tower20.LIGHTS['DAY']['sat'] = 1.28
tower20.LIGHTS['DAY']['exposure'] = -0.36
tower20.LIGHTS['DAY']['key_dir'] = (0.36, 0.62, -0.34)   # lower, raking sun (motivated key, long shadows)
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(33.21), C.g_bound(36.44)      # 996, 1093 -> shot = g 996..1092 (plan says 996-1092)
H_IN, H_OUT = 8, 4                              # DIS 13 in: 13/2 + 2 = 8 ; hard cut out: 4
GF = G0 - H_IN                                  # first rendered frame
G_LAST = G1 + H_OUT - 1
GS = list(range(GF, G_LAST + 1))
G_PERMIT = C.cap_g("แต่ใบอนุญาต")                # ~1000
G_TWENTY = C.cap_g("ได้แค่ 20 ปี")               # ~1041
G_DROP = C.cap_g("ครบแล้วต้องรื้อ")              # 1067: smile drops + snap
SNAP = (G_DROP - 3, G_DROP + 13)
PUSH1 = (1003, 1011)                             # director: push-in x1.15 over 8 frames on 'ใบอนุญาต'
HAND = (G0 + 12, G0 + 34)                       # document handed over (official arm out, Eiffel reaches)
G_SWAP_DOC = G0 + 24                            # doc prop moves official -> Eiffel (hands meet)
BLINKS = [G0 + 10, G_DROP - 1]
LIGHT, PRESET = "DAY", "tower_fair"
YEAR = 1889
PPD = 256

# staging (world D): Eiffel at the preset mark, the official a step behind and to the right
CAM_BACK = 4.3                                  # D from the camera to Eiffel at the start
CAM_Z = 1.6
TILT0 = -6.0
FG_SHIFT = (40.0, 0.0, 0.0)
BANNER_DEPTH, BANNER_Z, BANNER_W = 9.0, 10.2, 9.6   # banner: D behind Eiffel, centre height, width
FG_AHEAD, FG_SIDE, FG_Z = 3.0, -1.2, -1.6        # foreground head: ahead, left, feet z (underground: only head + hat show)
EIF_Z = 2.55                                    # head centre above the feet


def marks(A):
    e = Vector(A["marks"]["eiffel_fair"])
    return dict(eiffel=e, official=e + Vector((1.25, -0.5, 0.0)))


def cam_path(A):
    m = marks(A)
    subj = m["eiffel"] + Vector((0.8, 0.0, EIF_Z))
    c = Vector((subj.x - 0.3, subj.y - CAM_BACK, CAM_Z))
    return C.CamPath(c, subj, GF, G_LAST, push=0.06, slide_px=-75.0, rise_px=0.0, arc_deg_s=24.0, tilt0=TILT0, tilt_deg_s=1.5,
                     decay=0.25, snaps=[dict(g=PUSH1, k=1.28, peak=1.9, shift=(0.0, 0.0), tilt=0.0),
                           dict(g=SNAP, k=1.35, peak=2.3, shift=(0.0, 0.0), tilt=-3.5)])


def move_fg(A, cam_loc):
    d = Vector(cam_loc) - Vector(A["cams"][PRESET]["loc"])
    d.z = 0.0
    d = d + Vector(FG_SHIFT)                       # (right, forward) D: slide the bench out of the official's way
    for ob in C.bpy.data.objects:
        if ob.name.startswith(("fg_", "shade_casters")):
            ob.location = ob.location + d / CO.SC


def cam_path_static():
    import tower20
    cam = tower20.CAMS_M[PRESET]
    A = dict(marks=dict(eiffel_fair=CO.W((-4.4, -143.8, 0.0))), cams={PRESET: dict(loc=CO.W(cam["loc"]))})
    return cam_path(A)


# ----------------------------------------------------------------------------- poses
C.add_expression("proud_smile", eyes="happy", tilt=0.0, brows=("both", 0.10, 8.0, 0.045, 0.16, 0.012), mouth="smile")


def idle(g, ph=0.0):
    return dict(lean=3.0 * math.sin(g * 0.23 + ph), squash=(1.0, 1.0 + 0.015 * math.sin(g * 0.31 + ph)))


def official_pose(g):
    u = u_of(g, HAND[0], HAND[1])                                       # 0 doc held up, 1 arm stretched toward Eiffel
    held = g < G_SWAP_DOC
    p = dict(yaw=0.35, arm_r="hip", legs="wide")
    if held:
        p["arm_l"] = dict(hand=(lerp(-0.55, -1.15, u), lerp(0.85, 0.68, u)), bend=0.2, stretch=lerp(1.0, 1.25, u))
        p["prop_l"] = "doc_seal"
    else:
        u2 = u_of(g, G_SWAP_DOC, G_SWAP_DOC + 10)
        p["arm_l"] = dict(hand=(lerp(-1.15, -0.4, u2), lerp(0.68, 0.30, u2)), bend=0.2, stretch=lerp(1.25, 1.0, u2))
    p["expr"] = "happy" if g > G_SWAP_DOC else "stern"
    p["pitch"] = -0.05
    p.update(idle(g, 1.3))
    p["blink"] = blink(g, [G0 + 30])
    p["t"] = g / 30.0
    return p


def eiffel_pose(g):
    u = u_of(g, HAND[0], HAND[1])
    p = dict(yaw=0.40, legs=None)
    p.pop("legs")
    got = g >= G_SWAP_DOC
    if g < G_DROP:
        bl, _ = C.blink_swap(g, G_DROP, 0, 0)
    bl, ex = C.blink_swap(g, G_DROP, "proud", "worried")
    p["expr"] = ex
    if got:
        u2 = u_of(g, G_SWAP_DOC, G_SWAP_DOC + 12)
        p["arm_r"] = dict(hand=(lerp(1.0, 0.45, u2), lerp(0.62, 0.75, u2)), bend=-0.2, stretch=lerp(1.2, 1.0, u2))
        p["prop_r"] = "doc_seal"
    else:
        p["arm_r"] = dict(hand=(lerp(0.3, 1.0, u), lerp(0.2, 0.62, u)), bend=-0.2, stretch=lerp(1.0, 1.2, u))
    p["arm_l"] = "hip" if g < G_DROP else dict(hand=(-0.3, 0.98), bend=0.7)
    if g >= G_DROP:
        p["fx"] = ["sweat"]
        p["pitch"] = 0.2
        p["head_roll"] = 4.0
    p.update(idle(g, 0.4))
    p["blink"] = bl if g < G_DROP + 2 else blink(g, [G_DROP + 40])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s15")
        self.path = cam_path(self.A)
        self.extra = self.add_crowd()
        self.add_dressing()
        move_fg(self.A, self.path.loc0)
        self.key_cam(bf(GF), *self.path.at(GF))
        self.scene.frame_set(bf(GF))
        self.M = {k: C.on_ground(v) for k, v in marks(self.A).items()}
        self.eif = self.actors["eif"] = C.make_actor("eif", "eiffel", os.path.join(WORK, "sprites"),
                                                     contact=dict(width=1.3, depth=0.55, opacity=0.8), cam=self.cam)
        self.fgh = C.make_actor("fgh", "gent20", os.path.join(WORK, "sprites"), contact=False, shadow=None, cam=self.cam)
        self.off = self.actors["off"] = C.make_actor("off", "official", os.path.join(WORK, "sprites"),
                                                     contact=dict(width=1.3, depth=0.55, opacity=0.8), cam=self.cam)

    def add_dressing(self):
        """EXPOSITION UNIVERSELLE 1889 banner (Latin letters, sharp) on two poles behind the pair + 6 small fluttering pennant poles
        (the preset flags are merged static meshes; these are keyed every frame)."""
        import bpy
        e = marks(self.A)["eiffel"]
        cx, cy = e.x + 0.9, e.y + BANNER_DEPTH
        def mat(name, col, rough=0.8):
            m = bpy.data.materials.new(name)
            m.use_nodes = True
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Base Color"].default_value = col
            b.inputs["Roughness"].default_value = rough
            return m
        red, gold, wood, white, blue = (mat("bn_red", (0.55, 0.04, 0.05, 1)), mat("bn_gold", (1.0, 0.72, 0.16, 1), 0.4), mat("bn_wood", (0.22, 0.12, 0.06, 1)),
                                        mat("bn_white", (0.92, 0.92, 0.9, 1)), mat("bn_blue", (0.05, 0.12, 0.55, 1)))
        def box(name, loc, sc, m):
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
            o = bpy.context.object
            o.name = name
            o.scale = sc
            o.data.materials.append(m)
            return o
        W_, H_ = BANNER_W, 2.0
        box("bn_board", (cx, cy, BANNER_Z), (W_, 0.14, H_), red)
        box("bn_trim_t", (cx, cy - 0.09, BANNER_Z + H_ / 2 - 0.06), (W_, 0.06, 0.12), gold)
        box("bn_trim_b", (cx, cy - 0.09, BANNER_Z - H_ / 2 + 0.06), (W_, 0.06, 0.12), gold)
        for sx in (-1, 1):
            box("bn_pole%d" % sx, (cx + sx * (W_ / 2 + 0.1), cy, BANNER_Z / 2 - 0.5), (0.14, 0.14, BANNER_Z + 1.4), wood)
        for txt, z, size in (("EXPOSITION UNIVERSELLE", BANNER_Z + 0.34, 0.50), ("1889", BANNER_Z - 0.50, 0.62)):
            cu = bpy.data.curves.new("bn_txt", "FONT")
            cu.body = txt
            cu.size = size
            cu.align_x = "CENTER"
            cu.align_y = "CENTER"
            cu.extrude = 0.03
            ob = bpy.data.objects.new("bn_txt_" + txt[:4], cu)
            bpy.context.scene.collection.objects.link(ob)
            ob.location = (cx, cy - 0.15, z)
            ob.rotation_euler = (math.pi / 2, 0.0, 0.0)               # faces -y (toward the camera)
            ob.data.materials.append(gold)
        # fluttering pennant poles
        self.flags = []
        for i, (dx, dy) in enumerate([(-5.2, 2.5), (-3.0, 5.5), (5.5, 3.0), (3.8, 6.5), (-7.5, 7.5), (7.8, 8.5)]):
            px, py = cx + dx, cy + dy
            pole = box("fl_pole%d" % i, (px, py, 2.6), (0.07, 0.07, 5.2), wood)
            pivot = bpy.data.objects.new("fl_piv%d" % i, None)
            bpy.context.scene.collection.objects.link(pivot)
            pivot.location = (px, py, 4.9)
            for k, m in enumerate((blue, white, red)):
                bpy.ops.mesh.primitive_plane_add(size=1, location=(0.35 + 0.0, 0, 0))
                p = bpy.context.object
                p.scale = (0.35, 1, 0.5)
                p.rotation_euler = (math.pi / 2, 0, 0)
                p.location = (0.18 + 0.36 * k, 0.0, 0.0)
                p.data.materials.append(m)
                p.parent = pivot
            self.flags.append((pivot, i))

    def flutter(self, gs):
        for g in gs:
            f = bf(g)
            for pivot, i in getattr(self, "flags", []):
                pivot.rotation_euler = (0.06 * math.sin(g * 0.45 + i), 0.0, 0.35 * math.sin(g * 0.31 + i * 1.7) + 0.2)
                pivot.keyframe_insert("rotation_euler", frame=f)

    def add_crowd(self):
        """16 extra cast20 crowd cards (lady / gent / child / artists) in the midground behind and beside the pair (QA: thin crowd)"""
        import random
        rr = random.Random(7)
        roles = ["lady20", "gent20", "child20", "painter20", "gent20", "lady20", "composer20", "architect20", "poet20", "lady20"]
        m = marks(self.A)
        e = m["eiffel"]
        cam = self.path.loc0
        out = []
        for i in range(16):
            for _ in range(60):
                x = e.x + rr.uniform(-6.5, 8.0)
                y = e.y + rr.uniform(2.2, 13.0)
                if abs(x - (e.x + 0.7)) < 2.2 and y < e.y + 6.5:
                    continue                                          # keep the area right behind the pair readable
                if any(math.hypot(x - o[0], y - o[1]) < 1.5 for o in out):
                    continue
                break
            out.append((x, y))
        cards = []
        for i, (x, y) in enumerate(out):
            z = C.ground_z(x, y)
            ob = CO.placeholder_actor(roles[i % len(roles)], (x, y, z), face_to=(cam[0] + rr.uniform(-3, 3), cam[1], 1.6), name="xcrowd_%d" % i,
                                      pose=dict(yaw=rr.choice([-0.6, -0.3, 0.3, 0.6]), expr=rr.choice(["neutral", "smile"])))
            cards.append(ob)
        return cards

    def off_pos(self, g):
        """the official steps back and aside after the handover (g 1030..1062), so the snap lands on Eiffel with him small behind-right"""
        u = u_of(g, 1030, 1062)
        p = Vector(self.M["official"])
        return (p.x - 0.1 * u, p.y + 4.6 * u, p.z)

    def fg_pos(self, g):
        """foreground crowd head (back of a gent in a top hat): 2.5 D ahead of the lens, bottom-left corner, feet underground"""
        loc, look = self.path.at(g)
        fw = Vector((look.x - loc.x, look.y - loc.y, 0.0)).normalized()
        rt = Vector((fw.y, -fw.x, 0.0))
        p = loc + fw * FG_AHEAD + rt * FG_SIDE
        return (p.x, p.y, FG_Z)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.fgh, f, self.fg_pos(g))
            C.place(self.eif, f, self.M["eiffel"])
            C.place(self.off, f, self.off_pos(g))
            self.key_set(f, set_year=YEAR, set_crowd=3)
        self.bob_crowd(gs)
        self.flutter(gs)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.eif.pose(f, eiffel_pose(g), camera=self.cam)
            self.off.pose(f, official_pose(g), camera=self.cam)
            self.fgh.pose(f, dict(back=1, yaw=0.35, expr="neutral", arm_l="down", arm_r="down", lean=1.5 * math.sin(g * 0.2), t=g / 30.0), camera=self.cam)
        self.sprites_for([(self.fgh, PPD), (self.eif, PPD), (self.off, PPD)], [bf(g) for g in gs])

    def bob_crowd(self, gs):
        """the fair crowd cards are static placeholders: give each a small idle bob + sway (nobody frozen), keyed every frame."""
        cards = [ob for grp in CO.STATE.get("cards", []) for ob in grp] + list(getattr(self, "extra", []))
        if not hasattr(self, "_card0"):
            self._card0 = [(ob, ob.location.copy(), ob.rotation_euler.copy()) for ob in cards]
        for g in gs:
            f = bf(g)
            for i, (ob, loc0, rot0) in enumerate(self._card0):
                ph = i * 1.9
                ob.location = (loc0.x, loc0.y, loc0.z + 0.10 * abs(math.sin(g * 0.28 + ph)))
                ob.rotation_euler = (rot0.x, rot0.y, rot0.z + 0.05 * math.sin(g * 0.13 + ph))
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("rotation_euler", frame=f)
                for fc in (ob.animation_data.action.fcurves if hasattr(ob.animation_data.action, "fcurves") else []):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR"

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        P = cam_path_static()
        rows, worst = P.report(GS[:-1])
        for r in rows[::4]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
