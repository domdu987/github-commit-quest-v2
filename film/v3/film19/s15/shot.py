#!/usr/bin/env python3
"""shot.py -- film 19 take s15 = shots 15 + 16 MERGED into one continuous take (SHIP ship_deck NOON, no cut inside).
Shot 15 (36.52-39.67 s): "ความลับคือ เที่ยงวันกลางทะเล ดวงอาทิตย์อยู่ตรงหัว": william19 aims the brass quadrant straight up at the sun,
  captain19 shades his eyes; set_sun_overhead 0 -> 1 keyed every frame; the camera tilts up toward the sun on "อยู่ตรงหัว" (g 1172) and a
  sun glare disc (camera-parented) fades in.
Shot 16 (39.67-42.65 s): with NO cut the camera cranes back down and pushes to William, who lowers the quadrant and holds the H4 out on his
  palm toward the lens ("แต่นาฬิกายังบอกเวลาที่บ้าน", snap on "บอกเวลาที่" g 1218); the captain leans in to look at it.  Two sailors haul a rope
  in the background (nobody still for more than 1.5 s).
Cards ride the ship (C.ride_ship, parent inverse at t = 0), the camera rides the deck (C.on_ship); set_sea / set_roll / set_sun_overhead keyed
with the same t on EVERY frame.  No DOF, no text, no caption_shade.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")


def _patch_h4_hands(hour=8, minute=0):
    """the H4 shows HOME time far from 12 (8:00): replace the two hand paths of cast19's watch body at runtime (cast19 itself is read-only)"""
    import re
    orig = cast19._h4_body
    rd = 0.12 - 0.022
    ah = math.radians(hour * 30.0 + minute * 0.5 - 90.0)
    am = math.radians(minute * 6.0 - 90.0)

    def body(k):
        o = orig(k)
        hands = ['<path d="M0,0 L%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (0.55 * rd * math.cos(ah), 0.55 * rd * math.sin(ah), k.ink),
                 '<path d="M0,0 L%.4f,%.4f" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % (0.82 * rd * math.cos(am), 0.82 * rd * math.sin(am), k.ink)]
        it = iter(hands)
        return re.sub(r'<path d="M0,0 L[-0-9.,]+" stroke="[^"]+" stroke-width="0.0(?:16|10)" stroke-linecap="round"/>', lambda m: next(it), o)
    cast19._h4_body = body


_patch_h4_hands()

G0, G1 = C.g_bound(36.52), C.g_bound(42.65)              # shots 15 + 16: g 1096 .. 1279 (184 frames); DIS 15 in, CUT out to s17
G_FIRST, G_LAST = G0 - 10, G1 + 9 - 1                     # 1086 .. 1288
GS = list(range(G_FIRST, G_LAST + 1))
G_SNAP = C.cap_g("อยู่ตรงหัว")                            # 1172: the sun
G_SNAP2 = C.cap_g("บอกเวลาที่")                            # 1218: "tells the time at home"
SNAP = (G_SNAP - 8, G_SNAP + 12)
SNAP2 = (G_SNAP2 - 10, G_SNAP2 + 10)
G_SWAP = (G_SNAP + 14, G_SNAP + 34)                       # quadrant lowered, H4 raised (1186..1206)
LIGHT, PRESET = "NOON", "ship_deck"
FINAL_SPP = 11
PPD = 384
BLINKS_W = [1118, 1167, 1214, 1262]
BLINKS_C = [1105, 1156, 1230, 1270]


def sun_k(g):
    return clamp((g - (G0 - 10)) / float(G_SNAP + 4 - (G0 - 10)), 0.0, 1.0)


# ---- camera (rest frame of the deck: world D at t = 0) ------------------------------------------------------------
CAM_LOC0 = (-1.11, -39.59, 17.1125)
CAM_A = C.CamPath(CAM_LOC0, (0.55, -31.4, 15.5), G_FIRST, G_LAST, push=0.12, slide_px=-40.0, rise_px=0.0, arc_deg_s=6.5, decay=0.2,
                  snaps=[dict(g=SNAP, k=1.25, peak=1.4, shift=(2.0, 2.35))])
G_B = G_SNAP + 14                                         # 1186: the sun snap has settled; B starts from A's pose there
_lb, _kb = CAM_A.at(G_B)
CAM_B = C.CamPath(_lb, _kb, G_B, G_LAST, push=0.09, slide_px=15.0, rise_px=25.0, arc_deg_s=3.0, decay=0.15,
                  snaps=[dict(g=(G_B + 2, G_B + 20), k=0.65, peak=1.8, shift=(0.0, -0.8)),      # crane back down and away from the sun
                         dict(g=SNAP2, k=1.79, peak=2.0, shift=(-0.5, 0.0)),                     # push in on "บอกเวลาที่": the dial ~170-190 px
                         dict(g=(1230, 1250), k=0.72, peak=1.5, shift=(0.0, 0.0))])               # ease back to a medium shot


class _Cam(object):
    def at(self, g):
        return CAM_A.at(g) if g <= G_B else CAM_B.at(g)

    def report(self, gs, depth=None):
        rows, worst = [], 0
        run = 0
        for g in gs:
            a, b = self.at(g), self.at(g + 1)
            sp = max(C._corner_shift(a, b, depth or (a[1] - a[0]).length, cx, cy) for cx in (0, C.W_PX) for cy in (0, C.H_PX))
            rows.append(dict(g=g, px=round(sp, 2)))
            run = run + 1 if sp < 0.25 else 0
            worst = max(worst, run)
        return rows, worst


CAM = _Cam()
CAP_OFF = Vector((1.7, 1.15, 0.0))          # the captain stands close beside William for the whole shot (both fit at the pushes)
G_END = (1236, 1262)                          # the captain leans 0.2 D toward the watch


def cap_off(g):
    return CAP_OFF + Vector((-0.2, 0.0, 0.0)) * u_of(g, G_END[0], G_END[1], kind="sine")


# ---- poses ---------------------------------------------------------------------------------------------------------
W_Q = cast19.STORY19["william_quadrant_sun"][1]
W_H4 = cast19.STORY19["william_show_h4"][1]
C_IDLE = cast19.STORY19["captain_idle"][1]
SAIL = {"c": cast19.STORY19["sailor_c_haul"][1], "a": cast19.STORY19["sailor_a_haul"][1]}


def watch_scale(g):
    """the H4 pops big on the 'บอกเวลาที่' snap (g 1218: dial ~180 px), then settles"""
    return 2.4 + 0.6 * math.exp(-((g - 1219) / 7.5) ** 2)


def william_pose(g):
    t = g / 30.0
    sway = math.sin(2 * math.pi * g / 40.0)
    ua = u_of(g, G_SNAP - 4, G_SNAP + 8)                       # the quadrant thrusts up on "อยู่ตรงหัว"
    us = u_of(g, *G_SWAP, kind="sine")                         # 0 = quadrant up, 1 = H4 held out
    p = dict(W_Q)
    if us >= 0.5:                                              # second half: the H4 pose keys (expression, legs, other arm)
        p = dict(W_H4)
    adj = math.sin(2 * math.pi * g / 33.0)                     # he sights and adjusts the quadrant (a move every ~0.5-1 s)
    adj2 = math.sin(2 * math.pi * g / 51.0 + 1.0)
    hq = (0.40 + 0.03 * adj, 0.05 - 0.12 * ua + 0.05 * adj2)     # quadrant hand
    hw = (0.30 + 0.02 * math.sin(g * 0.2), 0.86 + 0.03 * math.sin(g * 0.23))   # H4 hand: chest height, in front
    p["arm_r"] = dict(hand=(lerp(hq[0], hw[0], us), lerp(hq[1], hw[1], us)), bend=lerp(-0.7, -0.2, us), shape="open" if us >= 0.5 else None,
                      stretch=lerp(1.1, 1.15, us), layer="top")
    if p["arm_r"]["shape"] is None:
        del p["arm_r"]["shape"]
    if us < 0.5:
        p["prop_r"] = dict(type="quadrant19", angle=-85 + 6.0 * adj - 3.0 * ua + 40.0 * us, scale=0.95)
        p["glint"] = (0.5 + 0.5 * math.sin(2 * math.pi * g / 12.0)) if g >= G_SNAP - 6 else 0.4 + 0.4 * max(0.0, adj)
    else:
        p["prop_r"] = dict(type="h4_watch", scale=watch_scale(g))
    glance = u_of(g, 1238, 1246, kind="sine") * (1.0 - u_of(g, 1252, 1262, kind="sine"))   # a glance up at the sun, then back to the watch
    p["pitch"] = lerp(-0.45 + 0.08 * adj2, -0.30 * glance, us)
    p["gaze"] = (lerp(0.2, 0.0, us), lerp(-1.0, 0.2, us) - 1.1 * glance)
    p["yaw"] = lerp(0.40 + 0.05 * adj2, 0.10, us)
    p["lean"] = lerp(-3 - 1.5 * ua + 1.6 * adj, 2.0 * math.sin(g * 0.13) + 1.5 * glance, us)
    p["head_roll"] = -3.0 + 2.5 * math.sin(g * 0.11) + 1.5 * adj
    if us >= 0.5:                                              # eyes OPEN (neutral) with the smile: he looks at the watch, up at the sun, back
        p["expr"] = "neutral"
        p["mouth"] = "smile"
    p["blink"] = blink(g, BLINKS_W)
    p["t"] = t
    return p


def captain_pose(g):
    us = u_of(g, G_SWAP[0] + 4, G_SWAP[1] + 6, kind="sine")    # he drops the hand and leans in to look at the watch
    ue = u_of(g, G_END[0] - 4, G_END[1], kind="sine")          # then he turns, leans toward the watch and looks surprised
    sh = math.sin(2 * math.pi * g / 37.0)
    p = dict(C_IDLE)
    p["yaw"] = lerp(0.25 + 0.12 * math.sin(2 * math.pi * g / 47.0), 0.35, us) + 0.15 * ue
    p["lean"] = lerp(1.0 * math.sin(g * 0.09) + 2.0 * sh, 6.0, us) + 3.0 * ue + 0.8 * math.sin(g * 0.15) * us
    p["head_roll"] = 2.0 * math.sin(g * 0.07 + 1.0) + 1.5 * sh
    p["pitch"] = lerp(-0.40, 0.10, us) + 0.12 * ue
    p["gaze"] = (lerp(0.2, 0.9, us), lerp(-1.0, 0.3, us))
    p["expr"] = "determined" if us < 0.5 else ("shocked" if ue > 0.5 else "neutral")
    if us < 0.5:
        k = clamp(1.0 - us * 2.0, 0.0, 1.0)
        pump = 0.07 * math.sin(2 * math.pi * g / 29.0)            # the shading hand moves (he shifts and re-shades his eyes)
        p["arm_r"] = dict(hand=(lerp(0.30, 0.34, k) + 0.03 * sh, lerp(0.9, -0.02, k) + pump * k), bend=-0.9 * k + 0.1 * (1 - k), shape="open", stretch=1.0, layer="top")
    p["blink"] = blink(g, BLINKS_C)
    p["t"] = g / 30.0
    return p


SAILORS = [("sa", "sailor_a", "c", (3.1, -25.0, 14.338), False, 0.0), ("sb", "sailor_b", "a", (-2.7, -24.6, 14.338), True, 0.45)]


def sailor_pose(key, mirror, ph, g):
    p = dict(SAIL[key])
    cyc = math.sin(2 * math.pi * (g / 36.0 + ph))            # a haul every 1.2 s: lean back and pull, then ease
    p["lean"] = p["lean"] + 5.0 * cyc
    p["head_roll"] = 2.0 * math.sin(2 * math.pi * (g / 36.0 + ph) + 1.0)
    p["mirror"] = mirror
    p["blink"] = blink(g, [1100 + int(30 * ph) + 52 * i for i in range(6)])
    p["t"] = g / 30.0
    return p


# ---- the take --------------------------------------------------------------------------------------------------------
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s15")
        self.grade()
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.root = self.A["ship_root"]
        f0 = bf(G_FIRST)
        H.set_sea(G_FIRST / 30.0, frame=f0)
        H.set_roll(G_FIRST / 30.0, frame=f0)
        self.key_cam(f0, *C.on_ship(self.root, f0, *CAM.at(G_FIRST)))
        self.scene.frame_set(f0)
        sp = os.path.join(WORK, "sprites")
        import shutil
        shutil.rmtree(os.path.join(sp, "_cache"), ignore_errors=True)
        self.wil = self.actors["wil"] = C.make_actor("wil", "william19", sp, contact=True, cam=self.cam)
        self.cap = self.actors["cap"] = C.make_actor("cap", "captain19", sp, contact=True, cam=self.cam)
        self.sail = []
        for name, cast, key, mark, mir, ph in SAILORS:
            a = self.actors[name] = C.make_actor(name, cast, sp, contact=True, cam=self.cam)
            self.sail.append((a, key, Vector(mark), mir, ph))
        # the parent inverse must be taken with the ship LEVEL (t = 0): key set_roll(0) on frame 1 and evaluate it there
        H.set_roll(0.0, frame=1)
        self.scene.frame_set(1)
        for a in [self.wil, self.cap] + [s[0] for s in self.sail]:
            C.ride_ship(a, self.root)
        self.dress_deck()
        for ob in self.dress:
            ob.parent = self.root
            ob.matrix_parent_inverse = self.root.matrix_world.inverted()
        self.sun_fade = []                                    # the sun is composited in deliver.py (sunfx.py): no card in the scene (a card made a faint square in the denoiser)

    def grade(self):
        """round 8 colour: -0.3 EV more (target luma ~105), deeper blue sky, darker sails, saturation 1.32 (all from this script, the set is untouched)"""
        bpy = C.bpy
        self.scene.view_settings.exposure = -0.62
        K.setup_grade(self.scene, 1.32)
        w = bpy.data.worlds[0].node_tree
        r = w.nodes["skyramp"].color_ramp
        for e in r.elements:
            c = list(e.color)
            e.color = (c[0] * 0.78, c[1] * 0.82, min(1.0, c[2] * 1.0), c[3])
        for ob in bpy.data.objects:
            if ob.name.startswith("ship6_sail"):
                for m in ob.data.materials:
                    if m and m.use_nodes:
                        b = m.node_tree.nodes.get("bsdf")
                        if b is not None:
                            c = list(b.inputs["Base Color"].default_value)
                            b.inputs["Base Color"].default_value = (c[0] * 0.82, c[1] * 0.82, c[2] * 0.84, c[3])
        self.sails = [ob for ob in bpy.data.objects if ob.name.startswith(("ship6_sail", "ship6_spanker", "ship6_jib"))]

    def key_sail_shadows(self, f, g):
        """noon shadows: the sails / spanker / jibs stop casting one after another from g 1146 to ~1172 (the big diagonal shadow shortens
        and goes: the sun climbing); a pool under the feet remains"""
        for i, ob in enumerate(self.sails):
            on = g < 1146 + 2 * i
            ob.visible_shadow = on
            ob.keyframe_insert("visible_shadow", frame=f)
            try:
                for fc in ob.animation_data.action.fcurves:
                    if fc.data_path == "visible_shadow":
                        for kp in fc.keyframe_points:
                            kp.interpolation = "CONSTANT"
            except Exception:
                pass

    def dress_deck(self):
        """foreground dressing: two rope coils and a bucket on the quarterdeck planks in front of the camera (parented to ship_root at t = 0)"""
        bpy = C.bpy
        import bmesh

        def mat(name, rgb, rough=0.8):
            m = bpy.data.materials.new(name)
            m.use_nodes = True
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
            b.inputs["Roughness"].default_value = rough
            return m
        rope, wood, iron = mat("dk_rope", (0.55, 0.38, 0.18)), mat("dk_wood", (0.30, 0.17, 0.08)), mat("dk_iron", (0.08, 0.08, 0.10), 0.5)
        z0 = 14.338
        objs = []

        def add(me_name, build, loc, m):
            me = bpy.data.meshes.new(me_name)
            bm = bmesh.new()
            build(bm)
            bm.to_mesh(me)
            bm.free()
            ob = bpy.data.objects.new(me_name, me)
            self.scene.collection.objects.link(ob)
            ob.location = loc
            ob.data.materials.append(m)
            for poly in me.polygons:
                poly.use_smooth = True
            objs.append(ob)
            return ob

        def coil(R, r, turns, name, loc):
            def b(bm):
                for i in range(turns):
                    mtx = __import__("mathutils").Matrix.Translation((0, 0, r * 1.7 * i))
                    bmesh.ops.create_torus if False else None
                    # ring of a torus built from a circle of circles
                    n1, n2 = 28, 10
                    verts = []
                    for a in range(n1):
                        th = 2 * math.pi * a / n1
                        ring = []
                        for c in range(n2):
                            ph = 2 * math.pi * c / n2
                            rr = R * (1.0 - 0.05 * i) + r * math.cos(ph)
                            ring.append(bm.verts.new((rr * math.cos(th), rr * math.sin(th), r * 1.7 * i + r * math.sin(ph))))
                        verts.append(ring)
                    for a in range(n1):
                        for c in range(n2):
                            bm.faces.new((verts[a][c], verts[(a + 1) % n1][c], verts[(a + 1) % n1][(c + 1) % n2], verts[a][(c + 1) % n2]))
            return add(name, b, loc, rope)

        def bucket(name, loc):
            def b(bm):
                n = 24
                bot, top = [], []
                for a in range(n):
                    th = 2 * math.pi * a / n
                    bot.append(bm.verts.new((0.30 * math.cos(th), 0.30 * math.sin(th), 0.0)))
                    top.append(bm.verts.new((0.40 * math.cos(th), 0.40 * math.sin(th), 0.55)))
                for a in range(n):
                    bm.faces.new((bot[a], bot[(a + 1) % n], top[(a + 1) % n], top[a]))
                bm.faces.new(bot)
            return add(name, b, loc, wood)
        def grating(name, loc):
            def b(bm):
                from mathutils import Vector as V
                for i in range(7):                       # slats along x
                    x0 = -0.62 + i * 0.2
                    vs = [bm.verts.new((x0 + dx, -0.5 + dy, dz)) for dz in (0.0, 0.12) for dx, dy in ((0, 0), (0.1, 0), (0.1, 1.0), (0, 1.0))]
                    bm.faces.new((vs[0], vs[1], vs[2], vs[3])); bm.faces.new((vs[4], vs[7], vs[6], vs[5]))
                    for a_, b_ in ((0, 1), (1, 2), (2, 3), (3, 0)):
                        bm.faces.new((vs[a_], vs[b_], vs[4 + b_], vs[4 + a_]))
                for j in range(2):                       # two cross bars
                    y0 = -0.48 + j * 0.9
                    vs = [bm.verts.new((-0.62 + dx, y0 + dy, dz)) for dz in (0.0, 0.14) for dx, dy in ((0, 0), (1.34, 0), (1.34, 0.08), (0, 0.08))]
                    bm.faces.new((vs[0], vs[1], vs[2], vs[3])); bm.faces.new((vs[4], vs[7], vs[6], vs[5]))
                    for a_, b_ in ((0, 1), (1, 2), (2, 3), (3, 0)):
                        bm.faces.new((vs[a_], vs[b_], vs[4 + b_], vs[4 + a_]))
            return add(name, b, loc, wood)
        grating("dk_grating", (-0.5, -34.9, z0))
        coil(0.62, 0.075, 5, "dk_coil_a", (-2.0, -36.4, z0))
        coil(0.46, 0.065, 4, "dk_coil_b", (2.5, -35.2, z0))
        bucket("dk_bucket_b", (1.5, -34.6, z0))
        bucket("dk_bucket", (0.55, -37.0, z0))
        self.dress = objs

    def build_sun_disc(self):
        """a visible sun: a bright disc + soft halo parented to the camera (top right of frame), camera rays only (it lights nothing);
        fade keyed by frame."""
        bpy = C.bpy
        d = 2.5                                               # D from the lens: in FRONT of the sails (the main sail is ~8 D away)
        self.sun_fade = []
        for name, px, py, rpx, soft in (("sun_halo", 360.0, 125.0, 250.0, 1), ("sun_disc", 360.0, 125.0, 52.0, 0)):
            me = bpy.data.meshes.new(name)
            r = rpx / 782.2 * d
            me.from_pydata([(-r, -r, 0), (r, -r, 0), (r, r, 0), (-r, r, 0)], [], [(0, 1, 2, 3)])
            uv = me.uv_layers.new(name="uv")
            for i, (u, v) in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
                uv.data[i].uv = (u, v)
            ob = bpy.data.objects.new(name, me)
            self.scene.collection.objects.link(ob)
            ob.parent = self.cam
            ob.location = ((px - 360.0) / 782.2 * d, (640.0 - py) / 782.2 * d, -d)
            for a in ("visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter", "visible_shadow"):
                setattr(ob, a, False)
            mat = bpy.data.materials.new(name)
            mat.use_nodes = True
            nt = mat.node_tree
            for n in list(nt.nodes):
                nt.nodes.remove(n)
            out = nt.nodes.new("ShaderNodeOutputMaterial")
            mix = nt.nodes.new("ShaderNodeMixShader")
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            em = nt.nodes.new("ShaderNodeEmission")
            em.inputs["Color"].default_value = (1.0, 0.93, 0.72, 1.0) if soft else (1.0, 0.98, 0.90, 1.0)
            em.inputs["Strength"].default_value = 3.0 if soft else 30.0
            tc = nt.nodes.new("ShaderNodeTexCoord")
            sub = nt.nodes.new("ShaderNodeVectorMath"); sub.operation = "SUBTRACT"
            sub.inputs[1].default_value = (0.5, 0.5, 0.0)
            ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
            mr = nt.nodes.new("ShaderNodeMapRange")
            mr.inputs["From Min"].default_value = 0.0 if soft else 0.46
            mr.inputs["From Max"].default_value = 0.5 if soft else 0.5
            mr.inputs["To Min"].default_value = 1.0
            mr.inputs["To Max"].default_value = 0.0
            if soft:
                mr.interpolation_type = "SMOOTHSTEP"
            fade = nt.nodes.new("ShaderNodeValue"); fade.name = "fade"; fade.outputs[0].default_value = 0.0
            mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
            if soft:
                mul2 = nt.nodes.new("ShaderNodeMath"); mul2.operation = "MULTIPLY"; mul2.inputs[1].default_value = 0.55
            nt.links.new(tc.outputs["UV"], sub.inputs[0]); nt.links.new(sub.outputs[0], ln.inputs[0])
            nt.links.new(ln.outputs["Value"], mr.inputs["Value"])
            nt.links.new(mr.outputs["Result"], mul.inputs[0]); nt.links.new(fade.outputs[0], mul.inputs[1])
            last = mul.outputs[0]
            if soft:
                nt.links.new(last, mul2.inputs[0]); last = mul2.outputs[0]
            nt.links.new(last, mix.inputs["Fac"])
            nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
            nt.links.new(mix.outputs[0], out.inputs["Surface"])
            ob.data.materials.append(mat)
            ob.visible_camera = True
            self.sun_fade.append((mat, fade))

    def key_sun_disc(self, f, g):
        v = u_of(g, G_SNAP - 8, G_SNAP + 4, kind="sine")
        for mat, fade in self.sun_fade:
            fade.outputs[0].default_value = v
            fade.outputs[0].keyframe_insert("default_value", frame=f)

    def key_sun_disc(self, f, g):
        v = u_of(g, G_SNAP - 8, G_SNAP + 4, kind="sine") * (1.0 - u_of(g, G_SWAP[0], G_SWAP[1] + 4, kind="sine"))
        v = max(v, 0.9 * u_of(g, 1226, 1250, kind="sine"))                   # the sun comes back at the top for the last 2 s (sun + watch in one frame)
        for mat, fade in self.sun_fade:
            fade.outputs[0].default_value = v
            fade.outputs[0].keyframe_insert("default_value", frame=f)

    def pose(self, gs):
        M = self.A["marks"]
        for g in gs:
            f = bf(g)
            t = g / 30.0
            H.set_sea(t, frame=f)
            H.set_roll(t, frame=f)
            H.set_sun_overhead(sun_k(g), frame=f)
            self.key_cam(f, *C.on_ship(self.root, f, *CAM.at(g)))
            self.key_sun_disc(f, g)
            self.key_sail_shadows(f, g)
            C.place(self.wil, f, Vector(M["william_deck"]))
            C.place(self.cap, f, Vector(M["captain_wheel"]) + cap_off(g))
            for a, key, mark, mir, ph in self.sail:
                C.place(a, f, mark + Vector((0, 0, 0.03 * abs(math.sin(2 * math.pi * (g / 36.0 + ph))))))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.wil.pose(f, william_pose(g), camera=self.cam)
            self.cap.pose(f, captain_pose(g), camera=self.cam)
            for a, key, mark, mir, ph in self.sail:
                a.pose(f, sailor_pose(key, mir, ph, g), camera=self.cam)
        frames = [bf(g) for g in gs]
        self.sprites_for([(self.wil, PPD), (self.cap, 256)] + [(a, 192) for a, _, _, _, _ in self.sail], frames)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], sun=round(sun_k(g), 3), heads=C.head_report(self, f),
                    dof=self.cam.data.dof.use_dof, caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
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
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
