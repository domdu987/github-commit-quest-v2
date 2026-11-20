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
from mathutils import Vector                             # noqa: E402

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
CAM_LOC0 = tuple(Vector(CAM_LOOK0) + (Vector((452.0, 61.2, 3.55)) - Vector((446.0, 62.6, 2.6))) * 1.1)
SNAP = (G_WORD - 2, G_WORD + 12)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GF, GL, push=0.0335, slide_px=12.6, rise_px=9.4, arc_deg_s=-5.0, decay=0.1,
                snaps=[dict(g=SNAP, k=1.108, peak=1.6, shift=(0.37, -0.10))])


# ----------------------------------------------------------------------------- BIGZOOM (QA_TEAM section H): one continuous descent
# QA-art r7 fix: starts ~2x further / ~2.3x higher over Port Royal (bay, ship, far headland, red-roofed town, fort with flags), holds the
# wide ~0.45 s (g 1468-1481, a slow creep only), then descends down the town street (set lane, Jamaica) past two palm crowns
# (set zoom_palms, fronds 1-2 D from the lens) onto the beach; long ease-out into the medium shot at GZ.  BIGZOOM g 1468..GZ = 3.67 s.
GH = 1481                                       # end of the hold on the extreme wide
GZ = 1578                                       # 52.6 s: the medium shot is reached; from here on the drift CamPath CAM
Z_L0 = Vector(json.loads(os.environ.get('ZL0', '[562.0, 58.0, 74.0]')))              # start: high over the town, the cast ~1.3 % of the frame height
Z_K0 = Vector(json.loads(os.environ.get('ZK0', '[330.0, 12.0, -20.0]')))             # aimed between the cast and the fort: bay, ship and headland above
Z_LM = Vector(json.loads(os.environ.get('ZLM', '[480.0, 60.5, 22.0]')))              # Bezier control: over the street, then between the two zoom palms
Z_L1, Z_K1 = CAM.at(GZ)
ZOOM_P = 0.82                                   # < 1 shifts the speed peak early = a longer, softer ease-out
ZOOM_CREEP = 0.012                              # share of the path covered by a linear creep over GF..GZ (the hold never freezes)


def zoom_ease(u):
    u = clamp(u)
    return u * u * u * (u * (6.0 * u - 15.0) + 10.0)          # smootherstep: ease-in and ease-out


def zoom_e(g):
    """path parameter 0..1 over GF..GZ: a slow linear creep + smootherstep(u^ZOOM_P) of the move GH..GZ"""
    lin = clamp((g - GF) / float(GZ - GF))
    u = clamp((g - GH) / float(GZ - GH))
    return ZOOM_CREEP * lin + (1.0 - ZOOM_CREEP) * zoom_ease(u ** ZOOM_P)


def cam_at(g):
    """the take's camera: the BIGZOOM descent g GF..GZ (hold, then eased), then the drift CamPath."""
    if g >= GZ:
        return CAM.at(g)
    e = zoom_e(g)
    a, b = 1.0 - e, e
    loc = (Z_L0 * (a * a) + Z_LM * (2.0 * a * b) + Z_L1 * (b * b))      # quadratic Bezier down the street, past the palm fronds
    ek = e ** 0.85
    look = Z_K0 * (1.0 - ek) + Z_K1 * ek
    return loc, look


def _mix(a, b, u):
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))


def william_pose(g):
    p = dict(cast19.STORY19["william_cheer_hat"][1])
    u = u_of(g, *G_LIFT, kind="sine")
    hi = _mix((0.5, 0.68), (0.80, -0.72), u)
    p["arm_r"] = dict(hand=(hi[0], hi[1] + 0.20 * math.sin(2 * math.pi * g / 10.0)), bend=-0.4, stretch=1.3, shape="open", layer="top")
    p["prop_r"] = dict(type="h4_watch", scale=1.8)
    p["arm_l"] = dict(hand=(-0.70, -0.62 + 0.20 * math.sin(2 * math.pi * g / 10.0 + 2.5)), bend=-0.5, stretch=1.3, shape="open", layer="top")
    p["prop_l"] = "tricorn_held"
    p["mirror"] = True
    p["expr"] = "happy"
    p["mouth"] = "grin"
    p.pop("fx", None)
    p["yaw"] = 0.25
    p["pitch"] = -0.25
    p["head_roll"] = -4 + 8 * math.sin(g * 0.63)
    p["lean"] = 6 * math.sin(g * 0.63 + 1.0)
    p["blink"] = blink(g, [1470, 1520, 1562])
    p["t"] = g / 30.0
    return p


# sailors: sa JUMPS and throws his tricorne (g 1538..1574), sb throws his tricorne (g 1516..1552) and then HUGS himself for joy.
HAT_FLIGHTS = {"sa": (1558, 1592, 1.3), "sb": (1548, 1584, 1.5)}        # (release g, catch g, arc height D)


def hat_in_hand(name, g):
    r0, r1, _h = HAT_FLIGHTS[name]
    return not (r0 <= g < r1)


def sailor_pose(name, g, ph):
    key = "sa" if name == "sailor_a" else "sb"
    p = dict(cast19.STORY19[name + "_cheer"][1])
    s = math.sin(2 * math.pi * g / 10.0 + ph)                     # ~3 Hz cheer
    p["arm_r"] = dict(p["arm_r"], hand=(0.74, -0.74 + 0.30 * s))
    p["arm_l"] = dict(p["arm_l"], hand=(-0.74, -0.7 - 0.30 * s))
    if hat_in_hand(key, g):
        p["prop_r"] = "tricorn_held"
    r0, r1, _h = HAT_FLIGHTS[key]
    if key == "sb" and 1500 <= g < 1540:                           # the self-hug: both arms across the chest, swaying
        k = u_of(g, 1500, 1508) * (1.0 - u_of(g, 1532, 1540))
        p["arm_r"] = dict(hand=(lerp(0.74, -0.30, k), lerp(-0.74 + 0.30 * s, 0.55, k)), bend=0.8, shape="open", layer="top")
        p["arm_l"] = dict(hand=(lerp(-0.74, 0.30, k), lerp(-0.7 - 0.30 * s, 0.60, k)), bend=0.8, shape="open", layer="front")
        p["prop_r"] = None
        p["lean"] = 8 * math.sin(g * 0.3)
        p["head_roll"] = -8 + 6 * math.sin(g * 0.3)
        p["expr"] = "happy"
        p["mouth"] = "grin"
    if p.get("prop_r") is None:
        p.pop("prop_r", None)
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
        self.ma = self.mw + Vector((-0.2, 1.35, -0.10))
        self.mb = self.mw + Vector((-0.2, -1.35, -0.17))
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

    def dress(self):
        bpy = C.bpy
        for ob in list(bpy.data.objects):                      # the stray lavender / blue shell blob between the feet (QA_TECH): the set's 'boatw' dressing
            if ob.name.startswith("shoredress_boatw"):
                self.hide_obs = getattr(self, "hide_obs", []) + [ob]
        # the crate William stands on (0.9 x 0.9 D x CRATE_H, plank-brown, a darker lid edge)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(self.mw.x, self.mw.y, self.mw.z + CRATE_H / 2.0 - 0.02))
        cr = bpy.context.active_object
        cr.name = "crate_w"
        cr.scale = (1.0, 1.0, CRATE_H + 0.04)
        cr.data.materials.append(self._mat("crate_wood", (0.20, 0.085, 0.02)))
        self.crate = cr
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
        # two flying tricornes (flattened black dome + gold rim)
        self.hats = {}
        for key in HAT_FLIGHTS:
            bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=0.48, depth=0.06, location=(0, 0, -50))      # the three-cornered brim
            h = bpy.context.active_object
            h.name = "hat_%s" % key
            h.rotation_euler = (0, 0, math.pi / 6)
            h.data.materials.append(self._mat("hat_black", (0.05, 0.05, 0.06)))
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, segments=14, ring_count=7, location=(0, 0, -50))  # the crown
            rim = bpy.context.active_object
            rim.name = "hatcrown_%s" % key
            rim.scale = (1.0, 1.0, 0.8)
            rim.data.materials.append(self._mat("hat_black2", (0.05, 0.05, 0.06)))
            rim.parent = h
            rim.location = (0, 0, 0.08)
            self.hats[key] = h

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g))
            C.place(self.wil, f, self.mw + Vector((0, 0, CRATE_H + bounce_z(g, 0.0, 0.10))))
            C.place(self.sa, f, self.ma + Vector((0, 0, bounce_z(g, 1.3, 0.26))))
            C.place(self.sb, f, self.mb + Vector((0, 0, bounce_z(g, 2.6))))
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
        """world point of a sailor's raised right hand (cheer arm): feet + 0.74 D to the camera's right + 3.55 D up."""
        m = self.ma if key == "sa" else self.mb
        loc, look = cam_at(g)
        _f, r, _u = C._cam_basis(loc, look)
        up = bounce_z(g, 1.3, 0.26) if key == "sa" else bounce_z(g, 2.6)
        return m + r * 0.74 + Vector((0, 0, 3.55 + up))

    def key_dressing(self, gs):
        C.key_vis(getattr(self, "hide_obs", []), False, 0 + 1)
        for g in gs:
            f = bf(g)
            C.key_vis(getattr(self, "hide_obs", []), False, f)
            # glint on the watch at the word "ห้าวินาที": a star that blooms and fades over 14 frames
            on = G_WORD <= g <= G_WORD + 13
            C.key_vis(self.star, on, f)
            if on:
                u = (g - G_WORD) / 13.0
                p = self._hand_world(self.wil, g, "prop_tip_r")
                self.star.location = p + Vector((0, 0, 0.0))
                self.star.scale = (0.9 * math.sin(math.pi * u) ** 0.7 + 0.05,) * 3
                self.star.keyframe_insert("location", frame=f)
                self.star.keyframe_insert("scale", frame=f)
            # flying hats
            for key, (r0, r1, hgt) in HAT_FLIGHTS.items():
                actor = self.sa if key == "sa" else self.sb
                fly = r0 <= g < r1
                C.key_vis(self.hats[key], fly, f)
                if fly:
                    u = (g - r0) / float(r1 - r0)
                    p0 = self._hand_est(key, r0 - 1)
                    p1 = self._hand_est(key, r1)
                    pos = p0 * (1 - u) + p1 * u + Vector((0, 0, 4.0 * hgt * u * (1 - u)))
                    self.hats[key].location = pos
                    self.hats[key].rotation_euler = (0.35 * math.sin(6 * math.pi * u), 0.0, math.pi / 6 + 4 * math.pi * u)
                    self.hats[key].keyframe_insert("location", frame=f)
                    self.hats[key].keyframe_insert("rotation_euler", frame=f)
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
