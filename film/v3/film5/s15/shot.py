#!/usr/bin/env python3
"""shot.py -- film 5 take s15: shot 15, the reveal (g 1502..1706 + 8-frame handles both sides), mine set (tunnel LAMP), diagram look.

The "diagram": the gaffer (a man, mouth closed) stands beside the canary cage, hung high from the cap bar of set 6; his flame lamp
hangs low at his side.  Three heights, top to bottom: bird, man, lamp.  A faint gas-haze layer (my own camera-facing card, wavy
lower edge) sinks from the roof: it reaches the bird first, the man later, the lamp last; only then the flame flares blue.
Breathing: the bird's chest pumps (canary key `breath`, ~4.2 pumps/s) against the man's slow breath (squash, 3.2 s period);
deliver.py draws two crisp breath traces (same time window) beside them in 15a-15c.

    15a g 1494..1539  medium two-shot across the tunnel (in-handle 1494..1501): man left, bird right, lamp low; slow push  ("นกหายใจเร็วกว่าคน")
    15b g 1540..1578  cut, tighter two-shot: the man's head beside the cage                                         ("หลายเท่า")
    15c g 1579..1617  cut, low wide of all three heights: the gas edge sinks past the bird, then the man          ("แก๊สเข้าตัวมันก่อนคน หลายนาที")
    15d g 1618..1653  cut, medium-low on the man and his lamp: gas edge just above the lamp, flame still steady    ("ตะเกียงบอกได้ก็ตอนที่")
    15e g 1654..1676  cut, ECU of the lamp: the gas reaches it, the flame flares tall and blue (g 1656..1663)      ("สายไปแล้ว")
    15f g 1677..1714  cut, ECU of the bird inside the cage bars, breathing fast in the haze (out-handle 1707..1714) ("แต่นกบอกได้ก่อน")

NO depth of field anywhere (client rule): M.setup_dof(scene, None, None, cam=...) at build and before every render.
Sub-shot ids 1..6; Blender frame = 2000 * (id - 1) + (g - 1400).

    python3 shot.py probe <ids> a:b[:step]
    python3 shot.py stills <ids> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <ids> a:b[:step] [scale] [samples]
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast5"), os.path.join(V3, "stage"), os.path.join(V3, "set3d5"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast5                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import mine as M                                        # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, lerp, clamp         # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, G1, H = 1502, 1707, 8                                   # shot 15 = [1502, 1707); handles 8 = 12-f dissolve / 2 + 2
B = [G0, 1540, 1579, 1618, g_of(55.04), 1677, G1]           # sub-shot starts; 15e at "สายไปแล้ว" (g 1654)
RANGES = {1: (G0 - H, B[1] - 1), 2: (B[1], B[2] - 1), 3: (B[2], B[3] - 1), 4: (B[3], B[4] - 1), 5: (B[4], B[5] - 1), 6: (B[5], G1 + H - 1)}
NAME = {1: "15a", 2: "15b", 3: "15c", 4: "15d", 5: "15e", 6: "15f"}
G_FLARE = (B[4] + 2, B[4] + 9)                              # the flame flares (gas reaches the lamp)


def bf(shot, g):
    return 2000 * (shot - 1) + int(g) - 1400


def _ez(u, kind="sine"):
    return ease(clamp(u), kind)


TP = M.TP
Y_CAGE = 16.25
RING = TP(Y_CAGE, -1.86, 3.92)                  # the cage hung high, from a nail under the cap bar of set 6 (bar bottom z 4.05)
GAFFER = TP(14.20, -1.30, 0)
# heights for the gas edge
Z_BIRD, Z_MAN, Z_LAMP = 3.62, 2.62, 1.30


def gas_edge(g):
    """world z of the gas layer's lower edge: roof -> past the bird (g ~1590) -> past the man's mouth (g ~1622) -> the lamp (g 1656)."""
    return keys(g, [(1400, (5.6,), "hold"), (1572, (5.6,), "sine"), (1592, (Z_BIRD - 0.25,), "lin"), (1624, (Z_MAN - 0.25,), "lin"),
                    (1640, (2.05,), "sine"), (1657, (Z_LAMP - 0.30,), "sine"), (1672, (0.55,), "hold")])[0]


def gas_alpha(g):
    return keys(g, [(1400, (0.0,), "hold"), (1566, (0.0,), "sine"), (1580, (0.30,), "hold")])[0]


# cameras (loc, look) per sub-shot, keyed A -> B
CAMS = {
    1: ((TP(12.55, 1.75, 2.60), TP(15.00, -1.60, 2.70)), (TP(12.85, 1.50, 2.60), TP(15.00, -1.60, 2.72))),
    2: ((TP(17.70, 0.40, 3.30), TP(15.55, -1.75, 3.15)), (TP(17.50, 0.25, 3.30), TP(15.55, -1.75, 3.17))),
    3: ((TP(12.20, 1.95, 0.85), TP(15.20, -1.60, 2.45)), (TP(12.40, 1.80, 0.85), TP(15.20, -1.60, 2.35))),
    4: ((TP(12.75, 0.95, 1.55), TP(14.15, -1.50, 1.80)), (TP(12.90, 0.80, 1.52), TP(14.15, -1.50, 1.72))),
}
LENS = {1: 22, 2: 22, 3: 22, 4: 22, 5: 22, 6: 22}


def _pk(a, b):
    return tuple(a) + tuple(b)


def _cam(g, ks):
    k = keys(g, ks)
    return Vector(k[:3]), Vector(k[3:])


# ----------------------------------------------------------------------------- poses
def breath_man(g):
    """the man's slow breath 0..1 (period 3.2 s), 1 = full chest."""
    return 0.5 - 0.5 * math.cos(2 * math.pi * (g - 1490) / 96.0)


BIRD_RATE = 1.4                                                     # t units per second: 3 pumps / unit -> 4.2 pumps / s


def bird_phase(g):
    return 3 * BIRD_RATE * (g - 1490) / 30.0                        # pumps since the start


def gaffer_pose(g, shot):
    p = dict(cast5.STORY5["gaffer_smug"][1])
    p.update(expr="smug", yaw=0.32, pitch=-0.15, head_roll=2 + 1.5 * math.sin(g * 0.07))
    b = breath_man(g)
    p["squash"] = (1.0 + 0.012 * b, 1.0 + 0.020 * b)
    p["lean"] = -1.0 - 2.0 * b
    p["head_dy"] = -0.02 * b
    p["arm_l"] = dict(hand=(-0.62, 1.05), bend=0.3)                 # the lamp hangs low at his side
    p["gaze"] = (0.6, -0.35) if shot in (1, 2, 3) else (0.2, 0.7)
    if shot == 4:
        p["pitch"] = 0.10
    fl = _ez((g - G_FLARE[0]) / float(G_FLARE[1] - G_FLARE[0]), "cubic_out") if g >= G_FLARE[0] else 0.0
    p["flame"] = 1.0 + 0.9 * fl
    p["flame_blue"] = 0.9 * fl
    p["t"] = g / 30.0
    p["blink"] = blink(g, [1512, 1561, 1600, 1636])
    return p


def bird_pose(g, shot):
    gas_on = clamp((g - 1588) / 30.0)                               # a little drowsy once the gas is in (never fallen here)
    return dict(state="perch_quiet", mirror=True, breath=1.0, t=BIRD_RATE * (g - 1490) / 30.0, beak=0.0,
                eyes=1.0 - 0.25 * gas_on, droop=0.15 * gas_on, ruffle=0.25 * gas_on, notes=0)


CANVAS_BIRD = (-0.75, -1.25, 0.875, 0.125)
CANVAS_GAFFER = (-2.125, -4.75, 2.125, 0.125)


class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = M.build("tunnel")
        M.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 14000
        self.cam = camrig.make_camera(scene, name="cam_s15")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        M.setup_dof(scene, None, None, cam=self.cam)
        sd = os.path.join(TMP, "sprites")
        self.actors = {}
        a = actors.Actor("gaffer", "gaffer"); a.build(CANVAS_GAFFER, sd, contact=True); self.actors["gaffer"] = a
        b = actors.Actor("bird", "canary"); b.build(CANVAS_BIRD, sd, shadow=None); self.actors["bird"] = b
        for a in self.actors.values():
            a.head_flip = False
            M.no_bounce(a.card)
        c = self.A["cage"]
        self.perch_off = Vector(c["perch"]) - Vector(c["hook"])
        self.anch = {}
        self.lamps = {}
        self._dress()
        self._haze_card()
        if verbose:
            print("s15: built in %.1f s" % (time.time() - t0), flush=True)

    def _dress(self):
        """runtime only: a small iron nail + hook under the cap bar for the raised cage; the cage moved up (set_cage)."""
        me = bpy.data.meshes.new("s15_nail")
        import bmesh
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.022, radius2=0.022, depth=0.16)
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new("s15_nail", me)
        ob.location = RING + Vector((0, 0, 0.09))
        mat = bpy.data.materials.new("s15_iron"); mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.045, 0.06, 1)
        me.materials.append(mat)
        self.scene.collection.objects.link(ob)
        M.set_cage(RING, frame=None)
        for ob in bpy.data.objects:                     # the tub train would stand in the cameras across the roadway
            if ob.name.startswith(("tubs", "couplings")):
                ob.hide_render = True; ob.hide_viewport = True

    # -- the gas haze: a camera-facing card, a faint green-grey veil above a wavy lower edge (world z), drifting
    def _haze_card(self):
        me = bpy.data.meshes.new("s15_haze")
        W, Hh = 14.0, 9.0
        me.from_pydata([(-W / 2, 0, -Hh / 2), (W / 2, 0, -Hh / 2), (W / 2, 0, Hh / 2), (-W / 2, 0, Hh / 2)], [], [(0, 1, 2, 3)])
        ob = bpy.data.objects.new("s15_haze", me)
        self.scene.collection.objects.link(ob)
        ob.visible_shadow = False
        try:
            ob.visible_diffuse = False; ob.visible_glossy = False; ob.visible_transmission = False
        except Exception:
            pass
        mat = bpy.data.materials.new("s15_haze_mat"); mat.use_nodes = True
        nt = mat.node_tree; N = nt.nodes; L = nt.links
        for n in list(N):
            N.remove(n)
        out = N.new("ShaderNodeOutputMaterial")
        geo = N.new("ShaderNodeNewGeometry")
        tco = N.new("ShaderNodeTexCoord")
        sep = N.new("ShaderNodeSeparateXYZ"); L.new(geo.outputs["Position"], sep.inputs[0])
        edge = N.new("ShaderNodeValue"); edge.name = "edge"; edge.outputs[0].default_value = 5.6
        amp = N.new("ShaderNodeValue"); amp.name = "amp"; amp.outputs[0].default_value = 0.0
        tim = N.new("ShaderNodeValue"); tim.name = "time"; tim.outputs[0].default_value = 0.0
        noi = N.new("ShaderNodeTexNoise"); noi.noise_dimensions = "4D"; noi.inputs["Scale"].default_value = 0.55
        noi.inputs["Detail"].default_value = 2.0
        L.new(tco.outputs["Object"], noi.inputs["Vector"]); L.new(tim.outputs[0], noi.inputs["W"])
        # wave = (noise - 0.5) * 0.7 ; zz = z + wave - edge
        w1 = N.new("ShaderNodeMath"); w1.operation = "SUBTRACT"; w1.inputs[1].default_value = 0.5; L.new(noi.outputs["Fac"], w1.inputs[0])
        w2 = N.new("ShaderNodeMath"); w2.operation = "MULTIPLY"; w2.inputs[1].default_value = 0.7; L.new(w1.outputs[0], w2.inputs[0])
        z1 = N.new("ShaderNodeMath"); z1.operation = "ADD"; L.new(sep.outputs["Z"], z1.inputs[0]); L.new(w2.outputs[0], z1.inputs[1])
        zz = N.new("ShaderNodeMath"); zz.operation = "SUBTRACT"; L.new(z1.outputs[0], zz.inputs[0]); L.new(edge.outputs[0], zz.inputs[1])
        # body: smoothstep(0, 0.6, zz) * (0.65 + 0.35 * noise2) * amp
        mr = N.new("ShaderNodeMapRange"); mr.interpolation_type = "SMOOTHSTEP"
        mr.inputs["From Min"].default_value = 0.0; mr.inputs["From Max"].default_value = 0.6
        L.new(zz.outputs[0], mr.inputs["Value"])
        n2 = N.new("ShaderNodeTexNoise"); n2.noise_dimensions = "4D"; n2.inputs["Scale"].default_value = 1.6
        L.new(tco.outputs["Object"], n2.inputs["Vector"]); L.new(tim.outputs[0], n2.inputs["W"])
        m2 = N.new("ShaderNodeMapRange"); m2.inputs["To Min"].default_value = 0.55; m2.inputs["To Max"].default_value = 1.15
        m2.inputs["From Min"].default_value = 0.3; m2.inputs["From Max"].default_value = 0.7
        L.new(n2.outputs["Fac"], m2.inputs["Value"])
        bo = N.new("ShaderNodeMath"); bo.operation = "MULTIPLY"; L.new(mr.outputs[0], bo.inputs[0]); L.new(m2.outputs[0], bo.inputs[1])
        # edge line: exp(-(zz/0.05)^2) * 0.9
        e1 = N.new("ShaderNodeMath"); e1.operation = "DIVIDE"; e1.inputs[1].default_value = 0.06; L.new(zz.outputs[0], e1.inputs[0])
        e2 = N.new("ShaderNodeMath"); e2.operation = "MULTIPLY"; L.new(e1.outputs[0], e2.inputs[0]); L.new(e1.outputs[0], e2.inputs[1])
        e3 = N.new("ShaderNodeMath"); e3.operation = "MULTIPLY"; e3.inputs[1].default_value = -1.0; L.new(e2.outputs[0], e3.inputs[0])
        e4 = N.new("ShaderNodeMath"); e4.operation = "EXPONENT"; L.new(e3.outputs[0], e4.inputs[0])
        e5 = N.new("ShaderNodeMath"); e5.operation = "MULTIPLY"; e5.inputs[1].default_value = 0.85; L.new(e4.outputs[0], e5.inputs[0])
        tot = N.new("ShaderNodeMath"); tot.operation = "ADD"; tot.use_clamp = True; L.new(bo.outputs[0], tot.inputs[0]); L.new(e5.outputs[0], tot.inputs[1])
        fac = N.new("ShaderNodeMath"); fac.operation = "MULTIPLY"; fac.use_clamp = True; L.new(tot.outputs[0], fac.inputs[0]); L.new(amp.outputs[0], fac.inputs[1])
        em = N.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.50, 0.70, 0.46, 1); em.inputs["Strength"].default_value = 0.55
        tr = N.new("ShaderNodeBsdfTransparent")
        mix = N.new("ShaderNodeMixShader")
        L.new(fac.outputs[0], mix.inputs[0]); L.new(tr.outputs[0], mix.inputs[1]); L.new(em.outputs[0], mix.inputs[2])
        L.new(mix.outputs[0], out.inputs["Surface"])
        me.materials.append(mat)
        self.haze, self.haze_nodes = ob, nt

    def key_haze(self, f, g, center, cam_loc, edge, amp):
        d = cam_loc - center; d.z = 0; d.normalize()
        ob = self.haze
        ob.location = center + d * 0.45
        ob.rotation_euler = (0.0, 0.0, math.atan2(d.y, d.x) - math.pi / 2)        # card normal (local -y.. +y) toward the camera
        camrig.key(ob, "location", f, Vector(ob.location), "LINEAR", "AUTO")
        camrig.key(ob, "rotation_euler", f, Vector(ob.rotation_euler), "LINEAR", "AUTO")
        N = self.haze_nodes.nodes
        for nm, v in (("edge", edge), ("amp", amp), ("time", g / 30.0 * 0.35)):
            s = N[nm].outputs[0]; s.default_value = v; s.keyframe_insert("default_value", frame=f)
        ob.hide_render = amp <= 1e-4
        ob.keyframe_insert("hide_render", frame=f)

    # -- cameras
    def lamp_world(self, f):
        a = self.actors["gaffer"]; an = self.anch.get(("gaffer", f))
        return actors.local_to_world(a, an["prop_tip_l"], f) if an else None

    def cam_of(self, shot, g):
        g0, g1 = RANGES[shot]
        u = _ez((g - g0) / float(g1 + 1 - g0), "sine")
        if shot in CAMS:
            a, b = CAMS[shot]
            return a[0].lerp(b[0], u), a[1].lerp(b[1], u)
        perch = RING + self.perch_off
        if shot == 5:                                    # ECU of the lamp (its world point from the probe pass)
            L = self.lamp_pt
            d = TP(14.2, 1.0, 0) - TP(14.2, -1.0, 0); d.z = 0; d.normalize()
            loc = L + d * lerp(1.15, 0.95, u) + Vector((0.0, 0.0, lerp(0.10, 0.16, u)))
            look = L + Vector((0, 0, lerp(0.10, 0.16, u)))
            return loc, look
        if shot == 6:                                    # ECU of the bird between the front wires, level with the perch
            d = TP(Y_CAGE, 1.0, 0) - TP(Y_CAGE, -1.0, 0); d.z = 0; d.normalize()
            sr = Vector((-d.y, d.x, 0.0))
            loc = perch + d * lerp(1.05, 0.80, u) + sr * 0.05 + Vector((0, 0, 0.06))
            look = perch + sr * 0.05 + Vector((0, 0, lerp(0.24, 0.20, u)))
            return loc, look

    # -- the lamp position (needed for the ECU camera before its own poses): from a gaffer pose fitted to the 15d camera
    def _lamp_point(self):
        f = bf(4, B[3]); g = B[3]
        loc, look = self.cam_of(4, g)
        camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
        self.actors["gaffer"].place(f, GAFFER)
        self.scene.frame_set(f)
        self.actors["gaffer"].pose(f, gaffer_pose(g, 4), camera=self.cam)
        r = self.actors["gaffer"].render_sprites(256, frames=[f])[0]
        self.anch[("gaffer", f)] = r["anchors"]
        self.lamp_pt = self.lamp_world(f)

    def visible(self, shot):
        self.actors["gaffer"].set_hidden(shot == 6)
        self.actors["bird"].set_hidden(shot in (4, 5))

    def pose(self, shot, gs):
        if shot == 5 and not hasattr(self, "lamp_pt"):
            self._lamp_point()
        self.visible(shot)
        for g in gs:
            f = bf(shot, g)
            loc, look = self.cam_of(shot, g)
            camrig.key_camera(f, loc, look, lens=LENS[shot], cam=self.cam, interp="LINEAR", easing="AUTO")
            M.set_drips(f)
            M.set_cage(RING, frame=f)
            self.actors["gaffer"].place(f, GAFFER)
            perch = RING + self.perch_off
            self.actors["bird"].place(f, tuple(perch))
            centre = TP(15.1, -1.55, 2.4) if shot != 6 else perch
            if shot == 5:
                centre = self.lamp_pt
            self.key_haze(f, g, centre, loc, gas_edge(g), gas_alpha(g))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.actors["gaffer"].pose(f, gaffer_pose(g, shot), camera=self.cam)
            self.actors["bird"].pose(f, bird_pose(g, shot), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        ppd = {1: (320, 320), 2: (512, 512), 3: (320, 320), 4: (512, 256), 5: (1280, 256), 6: (256, 2048)}[shot]
        for a, px in ((self.actors["gaffer"], ppd[0]), (self.actors["bird"], ppd[1])):
            for f, r in zip(fr, a.render_sprites(px, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("s15: WARNING sprite of %s clipped on frame %d" % (a.name, f), flush=True)
        self.key_lamps(shot, gs)

    def key_lamps(self, shot, gs):
        """the gaffer's flame lamp (keyed lamp_light at the flame; brighter and a cold blue light once it flares), a soft warm key on
        the bird for the ECU."""
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            loc, _ = self.cam_of(shot, g)
            on = {}
            p = self.lamp_world(f)
            if p is not None:
                tc = loc - p; tc.z = 0; tc.normalize()
                fl = _ez((g - G_FLARE[0]) / float(G_FLARE[1] - G_FLARE[0]), "cubic_out") if g >= G_FLARE[0] else 0.0
                on["lamp_gaffer"] = (p + tc * 0.10, 1.0 + 0.6 * fl, M.WARM)
                on["lamp_blue"] = (p + tc * 0.10 + Vector((0, 0, 0.25)), 0.9 * fl, (0.45, 0.65, 1.0))
            perch = RING + self.perch_off
            d = loc - perch; d.z = 0; d.normalize()
            on["lamp_bird"] = (perch + d * 0.9 + Vector((0.0, 0.0, 0.6)), 0.22 if shot == 6 else 0.10, M.WARM)
            for name in ("lamp_gaffer", "lamp_blue", "lamp_bird"):
                pos, s, col = on.get(name, (Vector((0, -30, 1)), 0.0, M.WARM))
                L = M.lamp_light(tuple(pos), s, frame=f, name=name)
                L.data.color = col
                self.lamps[name] = L

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = self.cam_of(shot, g)
        v = look - loc
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   heads={}, gas_edge=round(gas_edge(g), 3), gas_alpha=round(gas_alpha(g), 3))
        for a in self.actors.values():
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            hr = 0.5 if a.name != "bird" else 0.09
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - hr, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + hr, hy), f, res)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
            if a.name == "bird":
                ch = self.anch[(a.name, f)].get("chest", (hx, hy))
                c2 = actors.local_to_screen(a, self.cam, ch, f, res)
                out["bird_chest"] = [round(c2[0], 1), round(c2[1], 1)]
            if a.name == "gaffer":
                ch = self.anch[(a.name, f)].get("chest", (hx, hy + 1.0))
                c2 = actors.local_to_screen(a, self.cam, ch, f, res)
                out["man_chest"] = [round(c2[0], 1), round(c2[1], 1)]
        perch = RING + self.perch_off
        pts = {"ring": RING, "perch": perch, "cage_bottom": perch + Vector((0, 0, -0.35))}
        lp = self.lamp_world(f)
        if lp is not None:
            pts["lamp"] = lp
        out["pts"] = {k: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for k, p in pts.items()}
        out["breath_man"] = round(breath_man(g), 4)
        out["bird_pumps"] = round(bird_phase(g), 4)
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(shot)
        self.scene.camera = self.cam
        M.setup_dof(self.scene, None, None, cam=self.cam)        # client rule: no depth of field, ever
        self.scene.cycles.samples = samples
        return render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    Tk = None
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                gs = [RANGES[shot][0], (RANGES[shot][0] + RANGES[shot][1]) // 2, RANGES[shot][1]]
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
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            out = os.path.join(HERE, "raw", "s%d" % shot)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if Tk is None:
                Tk = Take("final")
            Tk.pose(shot, todo)
            for g in todo:
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
