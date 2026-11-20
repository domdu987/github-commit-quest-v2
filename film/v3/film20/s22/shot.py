#!/usr/bin/env python3
"""shot.py -- film 20 take s22 = shot 22, THE AHA (g 1561..1655 + handles g 1557..1560 in, 1656..1659 out; cuts both sides).
"หอที่ใคร ๆ ว่าไร้ประโยชน์ กลายเป็นของที่ทหารขาดไม่ได้" -- the tower everyone called useless became something the army cannot do without.

TOWER tower_dusk / NIGHT 1909, camera tower_dusk_chars (T14, director note) moved in along its view axis so the heads are >= 40 px.
Cast (cast20 cards at runtime marks bunched near the preset marks): Old Eiffel (centre, hands behind, worried -> proud), the officer
(right, faces him), three demolition men (left) each with a CROWBAR (cast5 'pickaxe' prop: the only long iron tool in the card kit).
    g1561..1585  the men heave their iron bars on their shoulders (idle sway), Eiffel stands worried, officer stern
    g1586        "ไร้ประโยชน์" (52.75): the men freeze and look at Eiffel
    g1606..1618  "กลายเป็นของ" (53.42): ALL THREE DROP THEIR BARS (the prop leaves the hand on a blink; a 3-D bar falls and tumbles to the
                 ground, clatter), the men stand amazed
    g1626..1634  "ที่ทหาร" (54.16 -> g1628): the officer SALUTES old Eiffel (flat hand to the kepi), Eiffel straightens, worried -> proud (blink swap)
    g1628..1655  the demolition wagon + scrap cart ROLL AWAY (set objects keyed along +x), the men tip their caps / cheer a little
    g1642        "ขาดไม่ได้" (54.63): eased SNAP push onto Eiffel's proud face
Mouths: none (no quote).  NO DOF, NO text.
    python3 shot.py probe a:b[:s] | stills a:b[:s] out [scale] [spp] | final a:b[:s] [scale] [spp] | python3 deliver.py
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20, bpy = C.S, C.CO, C.actors, C.cast20, C.bpy
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(52.02), C.g_bound(55.21)      # 1561, 1656 -> shot = 1561..1655
H_IN, H_OUT = 4, 4
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1      # 1557 .. 1659
GS = list(range(G_FIRST, G_LAST + 1))
G_USELESS = C.cap_g("ไร้ประโยชน์")                 # 1586
G_DROP = C.cap_g("กลายเป็นของ")                    # 1606
G_ARMY = C.cap_g("ที่ทหาร")                        # 1628
G_ESS = C.cap_g("ขาดไม่ได้")                       # 1642
DROP = (G_DROP + 1, G_DROP + 13)                  # the bars leave the hands at DROP[0], land by DROP[1]
SALUTE = (G_ARMY - 3, G_ARMY + 2)                 # arm up
SNAP = (G_ESS - 2, G_ESS + 13)
ROLL = (G_ARMY, G_LAST)
PRESET, CAM = "tower_dusk", "tower_dusk_chars"
PPD = 256
EXPO = 0.95                                     # scene exposure: QA-stats night luma >= 70
WHIP_TILT = 12.0                               # deg: the shot opens tilted up at the lit tower and whips down onto the group (continues shot 21)

# runtime marks (metres): bunched so that the group fits the frame at 18 D
M = dict(eiffel_old=(-4.0, -217.6), officer=(-2.2, -217.4), demo_a=(-5.5, -216.6), demo_b=(-6.4, -215.6), demo_c=(-7.3, -216.8))
CAST = dict(eiffel_old="eiffel_old", officer="officer", demo_a="riveter_hammer", demo_b="riveter_tongs", demo_c="riveter_forge")
CAM_BACK = 2.5       # D toward / away along the view, tuned below
HEAD_Z = 2.5


def A_(*a, **k):
    return dict(hand=a, **k)


def pose_of(who, g):
    """the drawn pose of one actor at film frame g."""
    t = g / 30.0
    sway = 2.2 * math.sin(g * 0.31 + hash(who) % 7)
    p = dict(legs="stand", t=t)
    bl = [G_USELESS - 1, DROP[0] - 1, G_ARMY, G_ARMY + 3]      # every expression / prop / arm swap is hidden on the closed frame (start + 1) of a blink
    p["blink"] = blink(g, bl)
    if who == "eiffel_old":
        proud = g >= G_ARMY + 1
        p.update(yaw=0.25, lean=5.0 + 0.6 * sway, pitch=-0.05, arm_r=A_(0.22, 0.90, bend=0.8, layer="top"), arm_l=A_(-0.22, 1.0, bend=0.7))
        p["expr"] = "proud" if proud else "worried"
        if proud:
            p["pitch"] = -0.12 - 0.08 * u_of(g, G_ARMY, G_ARMY + 8)
            p["lean"] = lerp(5.0, 2.0, u_of(g, G_ARMY, G_ARMY + 10)) + 0.5 * sway
        p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.26))
        return p
    if who == "officer":
        sal = u_of(g, *SALUTE)
        p.update(yaw=0.40, pitch=-0.1, expr="stern", legs="stand")
        if g < SALUTE[0]:
            p.update(arm_r=A_(-0.10, 0.95, bend=0.8, layer="top"), arm_l=A_(0.10, 1.00, bend=0.8))
        else:
            hx, hy = lerp(-0.10, 0.42, sal), lerp(0.95, -0.40, sal)
            p.update(arm_r=A_(hx, hy, bend=lerp(0.8, -0.9, sal), shape="open" if sal > 0.5 else "ball", stretch=lerp(1.0, 1.2, sal), layer="top"), arm_l="down")
        p["lean"] = 1.2 * sway * 0.0
        p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.3))
        return p
    # demolition men
    held = g < DROP[0]
    shock = u_of(g, G_USELESS, G_USELESS + 4)
    p.update(yaw=0.40 + 0.1 * sway * 0.0, legs="wide" if held else "stand")
    if held:
        base = {"demo_a": -62, "demo_b": -70, "demo_c": -55}[who]
        p["arm_r"] = A_(0.60, -0.40, bend=-0.6, stretch=1.3, layer="top")
        p["arm_l"] = A_(0.30, 0.90, bend=0.2)
        p["prop_r"] = dict(type="pickaxe", angle=base + 6 * sway)            # bar over the shoulder
        p["expr"] = "working" if g < G_USELESS else "shocked"
        p["lean"] = 6.0 + 1.5 * sway - 5.0 * shock
        p["pitch"] = -0.05 - 0.2 * shock
    else:
        p["arm_r"] = "down"
        p["arm_l"] = "down"
        p["expr"] = "shocked" if g < G_ARMY + 4 else "cheer"
        k = u_of(g, G_ARMY + 4, G_ARMY + 8)
        if g >= G_ARMY + 4:                                                   # hats-off cheer after the salute (hands up, held mouth)
            p["arm_r"] = A_(0.70, -0.60, shape="open", bend=-0.6, stretch=1.3, layer="top")
            p["arm_l"] = A_(-0.70, -0.55, shape="open", bend=-0.6, stretch=1.3, layer="top")
        p["lean"] = -2.0 + 1.0 * sway
        p["pitch"] = -0.05
    p["head_roll"] = 3.0 * sway
    if g >= G_ARMY + 4:
        p["squash"] = (1.0 + 0.02 * math.sin(g * 0.9 + 1), 1.0 - 0.02 * math.sin(g * 0.9 + 1))      # cheer bounce ~ 4.5 Hz is too fast: 0.9 rad/f = 4.3 Hz? keep small
    return p


def cam_path(A, cam):
    ee = Vector(CO.W(M["eiffel_old"] + (0.0,)))
    ee = Vector((ee.x, ee.y, HEAD_Z))
    c = Vector(A["cams"][CAM]["loc"])
    cen = Vector(CO.W((-4.7, -217.0, 0.0))) + Vector((0, 0, HEAD_Z))     # the centre of the bunch
    c = c + (c - cen).normalized() * CAM_BACK
    return C.CamPath(c, cen, G_FIRST, G_LAST, push=0.07, slide_px=0.0, rise_px=0.0, arc_deg_s=10.0, tilt0=TILT0, tilt_deg_s=1.8,
                     decay=0.25, snaps=[dict(g=(G_FIRST + 1, G_FIRST + 15), k=1.0, peak=2.0, tilt=-WHIP_TILT),
                                                          dict(g=(G_USELESS - 2, G_USELESS + 11), k=1.25, peak=1.8, tilt=0.5),
                                                          dict(g=(G_DROP - 1, G_DROP + 12), k=1.0 / 1.25, peak=1.8, tilt=-0.5),
                                                          dict(g=SNAP, k=1.1, peak=1.7, shift=(0.0, 0.0))])


TILT0 = 3.0 + WHIP_TILT
SHIFT = -0.03       # tower_dusk_chars has +0.10 (heads y ~770): lens shift down to the head band


def move_fg(A, cam_loc):
    d = Vector(cam_loc) - Vector(A["cams"][PRESET]["loc"])
    d.z = 0.0
    for ob in bpy.data.objects:
        if ob.name.startswith(("fg_", "shade_casters")):
            ob.location = ob.location + d / CO.SC


def make_bars(mat):
    """3 hidden crowbars (cylinders 1.5 m long); keyed per frame to fall from the hands to the ground."""
    bars = []
    for i in range(3):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.045 * CO.SC, depth=1.5 * CO.SC, vertices=8)
        ob = bpy.context.object
        ob.name = "bar_%d" % i
        ob.data.materials.append(mat)
        ob.visible_shadow = True
        bars.append(ob)
    return bars


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light="NIGHT", quality=quality, name="cam_s22", cam_name=CAM)
        A = self.A
        for k, v in M.items():
            A["marks"][k] = C.on_ground(CO.W(v + (0.0,)))
        self.path = cam_path(A, self.cam)
        self.cam.data.shift_y = SHIFT
        move_fg(A, self.path.loc0)
        for a in ("eiffel_old", "officer", "demo_a", "demo_b", "demo_c"):          # the preset's own stand-in cards, if any
            for ob in bpy.data.objects:
                if ob.name.startswith(("actor_" + a, a + "_card")):
                    ob.hide_render = True
        self.scene.view_settings.exposure = EXPO
        self.dress_fg()
        self.key_cam(bf(G_FIRST), *self.path.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.cast = {}
        for k in M:
            opacity = 0.7
            self.cast[k] = self.actors[k] = C.make_actor(k, CAST[k], os.path.join(WORK, "sprites"), contact=dict(width=1.3, depth=0.55, opacity=opacity), cam=self.cam)
        m = bpy.data.materials.new("barmat")
        m.use_nodes = True
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.35, 0.37, 0.42, 1)
        m.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.6
        self.bars = make_bars(m)
        self.wagon = list(CO.STATE.get("wagon", []))
        self.wagon0 = [Vector(o.location) for o in self.wagon]

    def dress_fg(self):
        """lit foreground props at the SIDES in the lower third (kegs, a crate, a rope coil): they fill the ground slab and give the
        move parallax; camera lateral offsets >= 1.2 m so the push passes beside them (never through)."""
        import kit20 as K
        M_ = CO.STATE["M"]
        loc = self.path.loc0 / CO.SC                      # metres
        cen = Vector(CO.W((-4.7, -217.0, 0.0))) / CO.SC
        f = Vector((cen.x - loc.x, cen.y - loc.y, 0.0)).normalized()
        r = Vector((f.y, -f.x, 0.0))
        mb = CO.MB("s22fg", parent=CO.root())
        def at(fw, ri):
            p = Vector((loc.x, loc.y, 0.0)) + f * fw + r * ri
            return (p.x, p.y, 0.0)
        K.keg(mb, M_, at(5.0, -2.5), 0.9, 0.36)
        K.keg(mb, M_, at(5.9, -3.0), 0.9, 0.36, "timberdk")
        K.keg(mb, M_, at(7.5, -1.9), 0.9, 0.36, "timberdk")
        K.crate(mb, M_, at(7.4, 3.0), (0.9, 0.7, 0.6), 0.5)
        K.crate(mb, M_, at(7.45, 3.05), (0.7, 0.6, 0.5), 0.2)
        K.keg(mb, M_, at(7.0, 3.1), 0.9, 0.36)
        mb.finish(hull=0.00384 * 22.0)

    def bar_pos(self, i, g):
        """(location, euler, visible) of bar i: appears in the hand at DROP[0], falls and tumbles to the ground at DROP[1]."""
        who = ("demo_a", "demo_b", "demo_c")[i]
        mk = Vector(self.A["marks"][who])
        if g < DROP[0] + i:
            return mk, (0, 0, 0), False
        u = clamp((g - DROP[0] - i) / float(DROP[1] - DROP[0] - i))
        hand = mk + Vector((0.8, 0.0, 2.6))
        floor = mk + Vector((1.5 + 0.4 * i, -0.4, 0.06))
        # fall (quadratic) + a tumble from upright to lying along x
        z = lerp(hand.z, floor.z, u * u)
        x = lerp(hand.x, floor.x, u)
        y = lerp(hand.y, floor.y, u)
        bounce = 0.35 * math.sin(math.pi * clamp((u - 0.9) / 0.1)) if u > 0.9 else 0.0
        return Vector((x, y, z + bounce * 0.0)), (0.0, math.radians(lerp(20, 88, ez(u))), math.radians(lerp(0, 20 + 10 * i, u))), True

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            loc, look = self.path.at(g)
            off = Vector((0.07 * math.sin(g * 1.9), 0.0, 0.07 * math.sin(g * 2.6 + 1.0)))      # light handheld sway (~4 px)
            self.key_cam(f, loc + off, look + off)
            for k, a in self.cast.items():
                mk = self.A["marks"][k]
                bz = 0.06 * abs(math.sin(g * 0.52 + hash(k) % 5)) if (k.startswith('demo') and g >= G_ARMY + 4) else 0.0       # cheer bounce ~ 3 Hz
                a.place(f, (float(mk[0]), float(mk[1]), float(mk[2]) + bz), scale=1.0, flip=(k == 'officer'))
            self.key_set(f, set_year=1909)
            S.signal_rings(-1.0, frame=f)
            S.wire_glow(0.0 if False else 0.35, frame=f)
            for i, ob in enumerate(self.bars):
                loc, eul, vis = self.bar_pos(i, g)
                ob.location, ob.rotation_euler = loc, eul
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("rotation_euler", frame=f)
                CO.setv(ob, vis, f)
            u = ez(clamp((g - ROLL[0]) / float(ROLL[1] - ROLL[0])), "sine")
            for ob, p0 in zip(self.wagon, self.wagon0):
                ob.location = p0 + Vector((70.0 * u * u, 0, 0)) / CO.SC if False else p0 + Vector((60.0 * u * u / CO.SC * 1.0, 0, 0))
                ob.keyframe_insert("location", frame=f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, a in self.cast.items():
                a.pose(f, pose_of(k, g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.cast.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
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
