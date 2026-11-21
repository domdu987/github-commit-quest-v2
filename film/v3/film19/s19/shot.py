#!/usr/bin/env python3
"""shot.py -- film 19 take s19 = shot 19, SHIP ship_coast DAY_JAMAICA.  Shot g 1468..1580; handles 9 in (g 1459..1467, dissolve 13 in) and
9 out (g 1581..1589, hard cut to shot 20).  First frame of the take g 1459, last 1589, 131 frames.
"ถึงฝั่ง นาฬิกาคลาดไปแค่ห้าวินาที แม่นกว่าที่รางวัลกำหนดซะอีก": the ship has anchored in the bay; William stands on the Jamaican beach
(mark shore_a) and holds the H4 high in one hand and his tricorne in the other; two sailors (shore_b, and one at the left) cheer with
arms up.  Camera on the dry sand (preset ship_coast, world-fixed: the beach is not the ship), moving from the first frame.
    g 1459..1480  William lifts the watch (arm rises), sailors begin to cheer
    g 1496..1509  SNAP push + pan to William's watch on "แค่ห้าวินาที" (caption 49.80 = event g 1497)
    g 1510..1589  hold the cheer: bounce, hats up
Mouths: nobody speaks (expression mouths only).  NO DOF, NO text, NO caption_shade.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector, Matrix                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(48.92), C.g_bound(52.71)   # 1468, 1581: shot 19 = g 1468..1580
H_IN, H_OUT = 9, 9
GF, GL = G0 - H_IN, G1 + H_OUT - 1            # 1459 .. 1589
GS = list(range(GF, GL + 1))
G_WORD = C.cap_g("แค่ห้าวินาที")               # 1497
G_LIFT = (GF, GF + 20)

LIGHT, PRESET = "DAY_JAMAICA", "ship_coast"
FINAL_SPP = 12
PPD = 192
CRATE_H = 0.40                                  # William stands on a wooden crate (set apart from the sailors)
RIM_COL, RIM_K, RIM_OFF = '#ffb24a', 1.5, (0.0045, 0.0035)    # set3d19 H.card_rim: warm rim on the upper-right (sun-glint / sea side) edges

CAM_LOOK0 = (446.0, 61.789, 2.6)                # subject point (found with a projection search so that all three heads, hats and raised
                                                # hands stay inside the frame on every frame)
END_SCALE = float(os.environ.get('ENDS', '1.3'))
LAT_AMP = float(os.environ.get('LAT', '1.13'))                  # round 9: aim right over the last third of the move (D)
CAM_LOC0 = tuple(Vector(CAM_LOOK0) + (Vector((452.0, 61.2, 3.55)) - Vector((446.0, 62.6, 2.6))) * END_SCALE)
SNAP = (G_WORD - 2, G_WORD + 12)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GF, GL, push=0.0226, slide_px=9.87, rise_px=9.4, arc_deg_s=1.3, decay=0.1,
                snaps=[dict(g=SNAP, k=1.108, peak=1.6, shift=(float(os.environ.get('R1', '0.083')), -0.10))])


# ----------------------------------------------------------------------------- BIGZOOM (QA_TEAM section H): one continuous descent
# QA-art r7 fix: starts ~2x further / ~2.3x higher over Port Royal (bay, ship, far headland, red-roofed town, fort with flags), holds the
# wide ~0.45 s (g 1468-1481, a slow creep only), then descends down the town street (set lane, Jamaica) past two palm crowns
# (set zoom_palms, fronds 1-2 D from the lens) onto the beach; long ease-out into the medium shot at GZ.  BIGZOOM g 1468..GZ = 3.67 s.
GH = 1474                                       # end of the hold on the extreme wide
ORBIT_DEG = float(os.environ.get('ORBIT', '0'))
GZ = 1553                                       # 51.87 s: the medium shot is reached (round 9: held ~0.8 s with a little drift); from here on the drift CamPath CAM
Z_L0 = Vector(json.loads(os.environ.get('ZL0', '[562.0, 58.0, 74.0]')))              # start: high over the town, the cast ~1.3 % of the frame height
Z_K0 = Vector(json.loads(os.environ.get('ZK0', '[330.0, 12.0, -20.0]')))             # aimed between the cast and the fort: bay, ship and headland above
Z_LM = Vector(json.loads(os.environ.get('ZLM', '[480.0, 60.5, 22.0]')))              # Bezier control: over the street, then between the two zoom palms
Z_L1, Z_K1 = CAM.at(GZ)
ZOOM_P = float(os.environ.get('ZP', '1.4'))                                    # round 9: > 1 eases on SCREEN speed (perspective makes screen speed grow as the lens nears the cast)
ZOOM_CREEP = 0.012                              # share of the path covered by a linear creep over GF..GZ (the hold never freezes)


def zoom_ease(u):
    u = clamp(u)
    return u * u * u * (u * (6.0 * u - 15.0) + 10.0)          # smootherstep: ease-in and ease-out


def _bez(e):
    a, b = 1.0 - e, e
    return Z_L0 * (a * a) + Z_LM * (2.0 * a * b) + Z_L1 * (b * b)


_CAST = Vector((447.093, 62.271, 3.3))                       # the cast (William's chest on the crate): distance reference
_TAB = [(i / 400.0, math.log((_bez(i / 400.0) - _CAST).length)) for i in range(401)]


def _e_of_logd(ld):
    """path parameter whose camera-to-cast distance has log = ld (the distance falls monotonically along the path)"""
    for (e0, l0), (e1, l1) in zip(_TAB[:-1], _TAB[1:]):
        if (l0 - ld) * (l1 - ld) <= 0 and l0 != l1:
            return e0 + (e1 - e0) * (ld - l0) / (l1 - l0)
    return 0.0 if ld >= _TAB[0][1] else 1.0


def zoom_e(g):
    """path parameter 0..1 over GF..GZ.  Round 9: the move GH..GZ is eased on LOG(camera-to-cast distance) with a smootherstep
    (= a constant-ish, eased ZOOM speed on screen: the cast grows evenly, no late lurch), plus a slow linear creep over GF..GZ."""
    lin = clamp((g - GF) / float(GZ - GF))
    u = clamp((g - GH) / float(GZ - GH))
    l0, l1 = _TAB[0][1], _TAB[-1][1]
    uu = clamp(u ** ZOOM_P)
    e_move = _e_of_logd(l0 + (l1 - l0) * (uu * uu * (3.0 - 2.0 * uu)))          # smoothstep: a flatter speed peak than smootherstep
    return ZOOM_CREEP * lin + (1.0 - ZOOM_CREEP) * e_move


def cam_at(g):
    """the take's camera: the BIGZOOM descent g GF..GZ (hold, then eased), then the drift CamPath."""
    if g >= GZ:
        loc, look = CAM.at(g)
        # JITTER rule: NO oscillating bumps on the held medium; instead one eased, ONE-WAY dolly-in (13 % over 14 frames: a snap on the held medium)
        u = clamp((g - GZ - 2) / 20.0) if not os.environ.get('NODOLLY') else 0.0
        k = 0.09 * (u * u * (3.0 - 2.0 * u))
        loc = loc + (look - loc) * k
        # plus a slow ONE-WAY orbit about the cast (eased in, 11 deg over the hold): the background slides smoothly (parallax), no oscillation
        ua = clamp((g - GZ) / 40.0)
        ang = math.radians(ORBIT_DEG) * (ua * ua * (3.0 - 2.0 * ua))
        d = loc - look
        return look + Matrix.Rotation(ang, 3, "Z") @ d, look
    e = zoom_e(g)
    a, b = 1.0 - e, e
    loc = (Z_L0 * (a * a) + Z_LM * (2.0 * a * b) + Z_L1 * (b * b))      # quadratic Bezier down the street, past the palm fronds
    ek = e ** 0.85
    look = Z_K0 * (1.0 - ek) + Z_K1 * ek
    if LAT_AMP:
        f = (look - loc).normalized()
        r = Vector((f.y, -f.x, 0.0)).normalized()
        look = look + r * LAT_AMP * math.sin(math.pi * clamp((e - 0.45) / 0.55))
    return loc, look


def _mix(a, b, u):
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))


G_GLINT = ((G_WORD, G_WORD + 13), (1548, 1562))          # the glint on the word, and again when William first reads on screen
THRUSTS = ((1486, 1497), (1536, 1546))                    # (start of the glance down at the watch, start of the thrust up); thrust lasts 7 f


def watch_low(g):
    """0..1: how far William has brought the watch down to look at it (glance DOWN, then THRUST UP on "ห้าวินาที" and again at g 1546)"""
    k = 0.0
    for a, t in THRUSTS:
        k = max(k, u_of(g, a, a + 6) * (1.0 - u_of(g, t, t + 7)))
    return k


def william_pose(g):
    p = dict(cast19.STORY19["william_cheer_hat"][1])
    u = u_of(g, *G_LIFT, kind="sine")
    hi = _mix((0.5, 0.68), (0.80, -0.72), u)
    low = watch_low(g)
    h = _mix((hi[0], hi[1] + 0.20 * math.sin(2 * math.pi * g / 10.0)), (0.46, 0.18), low)
    p["arm_r"] = dict(hand=h, bend=-0.4, stretch=1.3, shape="open", layer="top")
    p["prop_r"] = dict(type="h4_watch", scale=1.8)
    p["arm_l"] = dict(hand=(-0.70, -0.62 + 0.20 * math.sin(2 * math.pi * g / 10.0 + 2.5)), bend=-0.5, stretch=1.3, shape="open", layer="top")
    p["prop_l"] = "tricorn_held"
    p["mirror"] = True
    p["expr"] = "determined" if low > 0.5 else "happy"            # open eyes while he looks at the watch
    p["mouth"] = "grin"
    p.pop("fx", None)
    p["yaw"] = 0.25
    p["pitch"] = -0.25 + 0.65 * low
    p["gaze"] = (0.0, 0.9 * low)
    p["head_roll"] = -4 + 8 * math.sin(g * 0.63)
    p["lean"] = 9 * math.sin(g * 0.63 + 1.0)
    sy = 1.0 + 0.035 * math.sin(2 * math.pi * g / 10.0)                 # the cheer bounce is a squash (the feet stay planted)
    p["squash"] = (1.0 / sy, sy)
    p["blink"] = blink(g, [1470, 1520, 1562])
    p["t"] = g / 30.0
    return p


# sailors (round 9: the reactions must READ, so they happen while the cast is large, g 1540..1580):
#   sb throws his tricorne (g 1540..1566) and then HUGS himself for joy (g 1568..); sa JUMPS high twice (g 1552..1580) and throws his tricorne at
#   the first jump's peak (g 1558..1584).
HAT_FLIGHTS = {"sa": (1560, 1586, 1.5), "sb": (1540, 1566, 1.2)}        # (release g, catch g, arc height D)
JUMPS = ((1552, 1570), (1570, 1588))                                       # sa: two big jumps (0.8 D)


def hat_in_hand(name, g):
    r0, r1, _h = HAT_FLIGHTS[name]
    return not (r0 <= g < r1)


def sa_jump(g):
    if os.environ.get('NOJUMP'):
        return 0.0
    for a, b in JUMPS:
        if a <= g < b:
            return 0.55 * math.sin(math.pi * (g - a) / float(b - a)) ** 1.0
    return 0.0


def sailor_pose(name, g, ph):
    key = "sa" if name == "sailor_a" else "sb"
    p = dict(cast19.STORY19[name + "_cheer"][1])
    s = math.sin(2 * math.pi * g / 10.0 + ph)                     # ~3 Hz cheer
    p["arm_r"] = dict(p["arm_r"], hand=(0.74, -0.74 + 0.70 * s))
    p["arm_l"] = dict(p["arm_l"], hand=(-0.74, -0.7 - 0.70 * s))
    if hat_in_hand(key, g):
        p["prop_r"] = "tricorn_held"
    r0, r1, _h = HAT_FLIGHTS[key]
    if key == "sb" and g >= r1 + 2:                                # the self-hug: both arms across the chest, swaying
        k = u_of(g, r1 + 2, r1 + 8)
        p["arm_r"] = dict(hand=(lerp(0.74, -0.34, k), lerp(-0.74 + 0.30 * s, 0.50, k)), bend=0.9, shape="open", layer="top")
        p["arm_l"] = dict(hand=(lerp(-0.74, 0.34, k), lerp(-0.7 - 0.30 * s, 0.56, k)), bend=0.9, shape="open", layer="front")
        p.pop("prop_r", None)
        p["lean"] = 10 * math.sin(g * 0.3) * k
        p["head_roll"] = -8 + 8 * math.sin(g * 0.3)
        p["expr"] = "happy"
        p["mouth"] = "grin"
    if key == "sa" and any(a <= g < b for a, b in JUMPS):          # in the air: both arms thrown up and out, legs tucked wide
        p["arm_l"] = dict(hand=(-0.85, -0.95), bend=-0.5, shape="open", stretch=1.3, layer="top")
        p["legs"] = "wide"
    if p.get("prop_r") is None:
        p.pop("prop_r", None)
    sy = 1.0 + 0.04 * math.sin(2 * math.pi * g / 10.0 + ph)             # the cheer bounce is a squash (the feet stay planted)
    if not (key == "sa" and any(a <= g < b for a, b in JUMPS)):
        p["squash"] = (1.0 / sy, sy)
    if not (key == "sb" and g >= HAT_FLIGHTS["sb"][1] + 2) and not (key == "sa" and any(a <= g < b for a, b in JUMPS)):
        pass
    p["blink"] = blink(g, [1478 + int(ph * 5), 1540])
    p["t"] = g / 30.0
    return p


def bounce_z(g, ph, amp=0.16):
    w = 1.0 + 2.6 * math.sin(math.pi * clamp((g - (SNAP[0] - 2)) / 26.0)) ** 1.5      # the cheer erupts on the word: bigger hops
    return amp * w * abs(math.sin(math.pi * g / 10.0 + ph))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s19")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(GF), *cam_at(GF))
        self.scene.frame_set(bf(GF))
        sd = os.path.join(WORK, "sprites")
        self.wil = self.actors["wil"] = C.make_actor("wil", "william19", sd, contact=True, cam=self.cam)
        self.sa = self.actors["sa"] = C.make_actor("sa", "sailor_a", sd, contact=True, cam=self.cam)
        self.sb = self.actors["sb"] = C.make_actor("sb", "sailor_b", sd, contact=True, cam=self.cam)
        M = self.A["marks"]
        self.mw = Vector(M["shore_a"])
        self.ma = self.mw + Vector((-0.2, 1.35, 0.0))
        self.mb = self.mw + Vector((-0.2, -1.35, 0.0))
        for v in (self.mw, self.ma, self.mb):                       # GROUND CHECK: the feet stand ON the terrain (the marks' z are only nominal)
            v.z = self.terrain_z(v.x, v.y)
        self.dress()

    # ------------------------------------------------------------------------- runtime dressing: crate, glint star, flying hats
    def _mat(self, name, rgb, emit=0.0):
        m = C.bpy.data.materials.new(name)
        m.use_nodes = True
        bs = m.node_tree.nodes["Principled BSDF"]
        bs.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        bs.inputs["Roughness"].default_value = 0.7
        if emit:
            bs.inputs["Emission Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
            bs.inputs["Emission Strength"].default_value = emit
        return m

    def make_contact(self):
        """GROUND CHECK / client 'floating': a soft contact-shadow blob under every card (keyed to the feet's XY and the ground z under them),
        real shoes on the left sailor (his cream legs ended in blunt stubs), and the airborne tags the checker reads."""
        sys.path.insert(0, os.path.join(C.V3, "tools"))
        import ground_check as gc
        self.gc = gc
        bpy = C.bpy
        self.blobs = {}
        for key, act, w in (("wil", self.wil, 1.0), ("sa", self.sa, 0.95), ("sb", self.sb, 0.95)):
            me = bpy.data.meshes.new("blob_" + key)
            hw, hd = w / 2.0, w * 0.24
            me.from_pydata([(-hw, -hd, 0.0), (hw, -hd, 0.0), (hw, hd, 0.0), (-hw, hd, 0.0)], [], [(0, 1, 2, 3)])
            uv = me.uv_layers.new(name="UVMap")
            for i, c in enumerate(((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))):
                uv.data[i].uv = c
            me.materials.append(gc._shadow_material((0.04, 0.03, 0.02), 0.85))
            ob = bpy.data.objects.new("%s_gcshadow" % key, me)
            bpy.context.scene.collection.objects.link(ob)
            ob["gc_role"] = "shadow"
            ob.visible_shadow = False
            ob.visible_diffuse = False
            ob.visible_glossy = False
            self.blobs[key] = ob
        # two shoes for the left sailor (dark brown, flat, with a pale buckle): placed at his foot anchors every frame
        self.shoes = []
        for i in range(2):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, segments=14, ring_count=8, location=(0, 0, -50))
            sh = bpy.context.active_object
            sh.name = "shoe_sb_%d" % i
            sh.scale = (0.46, 0.27, 0.15)
            sh.data.materials.append(self._mat("shoe_leather", (0.012, 0.007, 0.004)))
            sh["gc_role"] = "skip"
            self.shoes.append(sh)
        # the left-over airborne tags: the jumper in his two jumps; the thrown hats while they fly
        r = self.sa.root
        r["airborne_frames"] = ",".join("%d:%d" % (bf(a), bf(b)) for a, b in JUMPS)

    def terrain_z(self, x, y):
        """z of the beach terrain under (x, y) by a ray cast straight down (the first hit on the object named 'terrain')."""
        sc = self.scene
        C.bpy.context.view_layer.update()
        dg = C.bpy.context.evaluated_depsgraph_get()
        o, d = Vector((x, y, 40.0)), Vector((0.0, 0.0, -1.0))
        for _i in range(8):
            ok, loc, _n, _idx, ob, _m = sc.ray_cast(dg, o, d)
            if not ok:
                break
            if ob.name.startswith("terrain"):
                return float(loc.z)
            o = loc + d * 0.001
        return 0.5

    def dress(self):
        bpy = C.bpy
        for ob in list(bpy.data.objects):                      # the stray lavender / blue shell blob between the feet (QA_TECH): the set's 'boatw' dressing
            if ob.name.startswith("shoredress_boatw"):
                self.hide_obs = getattr(self, "hide_obs", []) + [ob]
        # the crate William stands on: the set's own plank crate (h19_ship_land.crate: box + dark edge battens, the 'crate' / 'batten' materials)
        import h19_ship_land as L
        K = C.K
        mats = dict(crate=bpy.data.materials["crate"], batten=bpy.data.materials["batten"])
        mb = K.MB("crate_w")
        side_m, h_m = 0.52, CRATE_H / 1.85 + 0.02                          # metres under the 1.85-scaled world root
        L.crate(mb, mats, (self.mw.x / 1.85, self.mw.y / 1.85, (self.mw.z - 0.02) / 1.85), side_m, rz=0.2, h=h_m)
        self.crate = mb.finish()
        # the glint: a four-point white star facing the camera, emissive
        import bmesh
        me = bpy.data.meshes.new("glint_star")
        bm = bmesh.new()
        pts = []
        for i in range(8):
            r = 1.0 if i % 2 == 0 else 0.22
            a = math.pi / 2 + i * math.pi / 4
            pts.append(bm.verts.new((r * math.cos(a), 0.0, r * math.sin(a))))
        bm.faces.new(pts)
        bm.to_mesh(me)
        bm.free()
        st = bpy.data.objects.new("glint_star", me)
        bpy.context.scene.collection.objects.link(st)
        st.data.materials.append(self._mat("glint_white", (1.0, 1.0, 1.0), emit=40.0))
        st.visible_shadow = False
        self.star = st
        tc = st.constraints.new('TRACK_TO')
        tc.target = self.cam
        tc.track_axis = 'TRACK_Y'
        tc.up_axis = 'UP_Z'
        # two flying tricornes: a real three-cornered hat (black triangular brim folded up on all three sides, a gold-trimmed upper edge, a
        # low crown), ~0.95 D across so it reads on a phone
        import bmesh
        self.hats = {}
        self.make_contact()
        for key in HAT_FLIGHTS:
            me = bpy.data.meshes.new("tricorne_%s" % key)
            bm = bmesh.new()
            R, rim_h, fold = 0.46, 0.20, 0.30
            base = [(R * math.cos(math.pi / 2 + i * 2 * math.pi / 3), R * math.sin(math.pi / 2 + i * 2 * math.pi / 3)) for i in range(3)]
            vb = [bm.verts.new((x, y, 0.0)) for x, y in base]
            fb = bm.faces.new(vb)
            fb.material_index = 0
            for i in range(3):
                j = (i + 1) % 3
                (x0, y0), (x1, y1) = base[i], base[j]
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                # the fold: the edge midpoint rises and leans outwards (the brim turned up); two quads: black lower, gold trim upper
                o0 = bm.verts.new((x0 * 1.18, y0 * 1.18, 0.07))
                o1 = bm.verts.new((x1 * 1.18, y1 * 1.18, 0.07))
                t0 = bm.verts.new((x0 * 1.34, y0 * 1.34, rim_h + 0.06))
                t1 = bm.verts.new((x1 * 1.34, y1 * 1.34, rim_h + 0.06))
                q1 = bm.faces.new((vb[i], vb[j], o1, o0)); q1.material_index = 0
                q2 = bm.faces.new((o0, o1, t1, t0)); q2.material_index = 0
                tr = bm.faces.new((t0, t1, bm.verts.new((t1.co.x * 0.985, t1.co.y * 0.985, t1.co.z + 0.035)), bm.verts.new((t0.co.x * 0.985, t0.co.y * 0.985, t0.co.z + 0.035)))); tr.material_index = 1
            bm.normal_update()
            bm.to_mesh(me)
            bm.free()
            h = bpy.data.objects.new("hat_%s" % key, me)
            bpy.context.scene.collection.objects.link(h)
            me.materials.append(self._mat("hat_black", (0.05, 0.05, 0.06)))
            me.materials.append(self._mat("hat_gold", (0.9, 0.68, 0.15)))
            for pl in me.polygons:
                pl.use_smooth = False
            h.scale = (1.0, 1.0, 1.0)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, segments=14, ring_count=7, location=(0, 0, 0.12))     # the crown
            cr = bpy.context.active_object
            cr.name = "hatcrown_%s" % key
            cr.scale = (1.0, 1.0, 0.6)
            cr.data.materials.append(self._mat("hat_black2", (0.05, 0.05, 0.06)))
            cr.parent = h
            em = bpy.data.objects.new("hattilt_%s" % key, None)         # empty: tilts the hat's top towards the camera (camera looks along -x)
            bpy.context.scene.collection.objects.link(em)
            h.parent = em
            em.rotation_euler = (0.0, 0.85, 0.0)
            self.hats[key] = em
            self.hat_obj = getattr(self, "hat_obj", {})
            self.hat_obj[key] = h
            self.hat_crown = getattr(self, 'hat_crown', {})
            self.hat_crown[key] = cr
            em.location = (0, 0, -50)

    def pose(self, gs):
        extra = sorted({x for r0, r1, _h in HAT_FLIGHTS.values() for x in (r0 - 1, r1)} - set(gs))
        for g in list(gs) + extra:                                   # hat release / catch frames are keyed even if another process renders them
            f = bf(g)
            self.key_cam(f, *cam_at(g))
            C.place(self.wil, f, self.mw + Vector((0, 0, CRATE_H)))
            C.place(self.sa, f, self.ma + Vector((0, 0, sa_jump(g))))
            C.place(self.sb, f, self.mb)
            self.key_set(f, sea=(g - GF) / 30.0, roll=(g - GF) / 30.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.wil.pose(f, william_pose(g), camera=self.cam)
            self.sa.pose(f, sailor_pose("sailor_a", g, 1.3), camera=self.cam)
            self.sb.pose(f, sailor_pose("sailor_b", g, 2.6), camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(self.wil, PPD), (self.sa, PPD), (self.sb, PPD)], fr)
        self.key_dressing(gs)

    def _hand_world(self, actor, g, anchor):
        f = bf(g)
        self.scene.frame_set(f)
        loc = self.anch[(actor.name, f)][anchor]
        return C.actors.local_to_world(actor, loc, frame=f)

    def _hand_est(self, key, g):
        """world point of a sailor's raised right (cheering) hand at film frame g: the card-local hand target through the actor's card
        (the actor is placed and the camera keyed for the hat frames in pose() even when this process does not render them)."""
        actor, ph = (self.sa, 1.3) if key == "sa" else (self.sb, 2.6)
        f = bf(g)
        self.scene.frame_set(f)
        s_ = math.sin(2 * math.pi * g / 10.0 + ph)
        return C.actors.local_to_world(actor, (0.74, -0.74 + 0.70 * s_), frame=f, camera=self.cam)

    def key_blobs_shoes(self, gs):
        for g in gs:
            f = bf(g)
            loc, look = cam_at(g)
            fwd, rgt, _u = C._cam_basis(loc, look)
            yaw = math.atan2(rgt.y, rgt.x)
            for key, act, m, top in (("wil", self.wil, self.mw, CRATE_H), ("sa", self.sa, self.ma, 0.0), ("sb", self.sb, self.mb, 0.0)):
                b = self.blobs[key]
                lift_ = sa_jump(g) if key == "sa" else 0.0
                k = 1.0 / (1.0 + 1.2 * lift_)
                b.location = (m.x, m.y, m.z + top + 0.01)
                b.scale = (k, k, 1.0)
                b.rotation_euler = (0.0, 0.0, yaw)
                b.keyframe_insert("location", frame=f)
                b.keyframe_insert("scale", frame=f)
                b.keyframe_insert("rotation_euler", frame=f)
            # the left sailor's shoes at his foot anchors (card-local points through the actor card), flat on the ground
            for i, anc in enumerate(("foot_l", "foot_r")):
                p = C.actors.local_to_world(self.sb, self.anch[("sb", f)][anc], frame=f, camera=self.cam)
                sh = self.shoes[i]
                sh.location = (p.x + fwd.x * -0.06, p.y + fwd.y * -0.06, self.mb.z + 0.075)
                sh.rotation_euler = (0.0, 0.0, yaw)
                sh.keyframe_insert("location", frame=f)
                sh.keyframe_insert("rotation_euler", frame=f)

    def key_dressing(self, gs):
        self.key_blobs_shoes(gs)
        C.key_vis(getattr(self, "hide_obs", []), False, 0 + 1)
        for g in gs:
            f = bf(g)
            C.key_vis(getattr(self, "hide_obs", []), False, f)
            # glints on the watch: on "ห้าวินาที" and again when William first reads on screen.  A white four-point star whose SCREEN size is
            # constant (~44 px radius at 720 wide, ~22 px on a phone), so it reads at any distance; blooms and fades over 14 frames.
            gl = None
            for a0, b0 in G_GLINT:
                if a0 <= g <= b0:
                    gl = (g - a0) / float(b0 - a0)
            C.key_vis(self.star, gl is not None, f)
            if gl is not None:
                p = self._hand_world(self.wil, g, "prop_tip_r")
                loc, _look = cam_at(g)
                dist = (p - Vector(loc)).length
                rad = 44.0 / 782.0 * dist * math.sin(math.pi * gl) ** 0.7 + 0.02
                self.star.location = p
                self.star.scale = (rad, rad, rad)
                self.star.keyframe_insert("location", frame=f)
                self.star.keyframe_insert("scale", frame=f)
            # flying hats
            for key, (r0, r1, hgt) in HAT_FLIGHTS.items():
                actor = self.sa if key == "sa" else self.sb
                fly = r0 <= g < r1
                C.key_vis([self.hats[key], self.hat_obj[key], self.hat_crown[key]], fly, f)
                if fly:
                    u = (g - r0) / float(r1 - r0)
                    p0 = self._hand_est(key, r0 - 1)
                    p1 = self._hand_est(key, r1)
                    pos = p0 * (1 - u) + p1 * u + Vector((0, 0, 4.0 * hgt * u * (1 - u)))
                    self.hats[key].location = pos
                    self.hats[key].keyframe_insert("location", frame=f)
                    self.hat_obj[key].rotation_euler = (0.0, 0.0, math.pi / 6 + 4 * math.pi * u)
                    self.hat_obj[key].keyframe_insert("rotation_euler", frame=f)
        if not getattr(self, "_rim", False):                # warm rim light on the cards (director, QA-art r7)
            for a in (self.wil, self.sa, self.sb):
                H.card_rim(a, color=RIM_COL, k=RIM_K, offset=RIM_OFF)
            self._rim = True

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        print([r["px"] for r in rows][::4])
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= GL]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
