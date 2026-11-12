#!/usr/bin/env python3
"""shot.py -- film 3 take s15: shot 15 (the diagram moment), harbor set WARM.

    shot 15  g 1330..1461 (plan 44.35-48.75 s)  10-frame dissolves in (from shot 14) and out (to shot 16); handles
             g 1323..1329 and g 1462..1468 rendered in 3D.
    An elevated three-quarter view of the whole tank from the yard end of Commercial Street (instead of the plan's high_down,
    which looks away from the tank).  The tank turns x-ray: its shell fades to a translucent ghost (g 1328..1342).
      g 1340..1384  "ถังใหม่ต้องเติมน้ำดูก่อนว่ารั่วไหม": a translucent blue WATER TEST fills the tank (what should have happened),
                    bright water line, small ripples; hold to g 1398.
      g 1398..1410  "แต่บริษัทรีบ": the blue ghost drains away (fades out).
      g 1404..1468  "เลยเทกากน้ำตาลลงไปเลย": thick brown molasses pours from the filling pipe's inlet at the rim, the brown
                    level climbs inside the ghost tank (what they did).
    Camera: slow push and orbit in four eased segments (speed changes g 1361, 1398, 1430).

    python3 shot.py probe 15 a:b:step | stills 15 a:b:step <dir> [scale] [samples] | final 15 [a:b] [scale] [samples]
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib3 import *            # noqa: F401,F403

G0, G1 = gb(44.35), gb(48.75)                       # 1330, 1462
HD = 10 // 2 + 2                                     # 7
XR = (1328, 1342)
W_UP = (1340, 1384); W_FADE = (1398, 1410)
M_POUR = 1404; M_UP = (1408, 1468)
TC = Vector(H.STATE.get("A", {}).get("tank", {}).get("center", (14.5, 22.0, 0.0))) if H.STATE.get("A") else Vector((14.5, 22.0, 0.0))
TANK_TOP = 24.0
INLET = None                                         # set in setup from the pipe points

CAMS = [(Vector((1.2, -15.0, 8.0)), Vector((14.2, 22.0, 12.6))),
        (Vector((1.9, -12.6, 8.6)), Vector((14.3, 22.0, 12.7))),
        (Vector((2.8, -10.2, 9.4)), Vector((14.4, 22.0, 12.5))),
        (Vector((3.5, -8.6, 10.0)), Vector((14.5, 22.0, 12.2))),
        (Vector((4.0, -7.6, 10.4)), Vector((14.5, 22.0, 12.0)))]
KEYS = [G0 - HD, 1361, 1398, 1430, G1 + HD - 1]


def xray_material(m, name):
    """copy of a tank material whose surface is mixed with Transparent by a factor (1 = solid)"""
    m2 = m.copy(); m2.name = name; nt = m2.node_tree
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
    lk = out.inputs["Surface"].links[0]; src = lk.from_socket
    nt.links.remove(lk)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); mx.name = "XRAY"
    mx.inputs[0].default_value = 1.0
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(src, mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs["Surface"])
    return m2


class Take(BaseTake):
    PRESET = "WARM"
    SHOTS = {15: (G0 - HD, G1 + HD - 1)}
    SEEP = 0.8

    def setup(self):
        global INLET
        tc = Vector(self.A["tank"]["center"])
        pts = self.A["tank"]["pipe"]
        INLET = Vector(pts[-1])
        # x-ray copies of the tank shell / patch materials
        self.xmats = []
        for on in ("tank_shell", "tank_patch"):
            ob = bpy.data.objects[on]
            for slot in ob.material_slots:
                if slot.material is None or slot.material.name.startswith("ink"):
                    continue
                if not slot.material.name.endswith("_xray"):
                    nm = slot.material.name + "_xray"
                    m2 = bpy.data.materials.get(nm) or xray_material(slot.material, nm)
                    slot.link = "OBJECT"; slot.material = m2
                    if m2 not in self.xmats:
                        self.xmats.append(m2)
        self.shell = bpy.data.objects["tank_shell"]
        # the ghosts: water (blue) and molasses (brown) volumes inside the tank, the pouring stream
        R_ = self.A["tank"]["radius"] - 0.12
        self.wmat = emit_mat("W3_water", hexlin("#66b8ff"), 1.0, 0.55)
        self.wtop = emit_mat("W3_water_top", hexlin("#c8ecff"), 1.15, 0.75)
        self.mmat = emit_mat("W3_mol", hexlin("#6a2a0c"), 1.0, 0.88)
        self.mtop = emit_mat("W3_mol_top", hexlin("#a6521c"), 1.0, 0.92)
        self.smat = emit_mat("W3_stream", hexlin("#7a3410"), 1.0, 1.0)

        def cyl(name, mat, topmat, r):
            mb = H.MB(); mb.frustum((0, 0, 0), (0, 0, 1.0), r, r, mat, seg=72, cap0=False, cap1=False)
            ob = mb.obj(name, self.fx); ob.location = (tc.x, tc.y, 0.36)
            mb2 = H.MB(); mb2.frustum((0, 0, -0.01), (0, 0, 0.0), r, r, topmat, seg=72, cap0=False, cap1=True)
            top = mb2.obj(name + "_top", self.fx); top.location = (tc.x, tc.y, 0.36)
            ring = H.MB(); ring.frustum((0, 0, -0.06), (0, 0, 0.06), r + 0.02, r + 0.02, emit_mat(name + "_rim", hexlin("#ffffff"), 1.3, 0.9), seg=72, cap0=False, cap1=False)
            rim = ring.obj(name + "_rim", self.fx); rim.location = (tc.x, tc.y, 0.36)
            for o in (ob, top, rim):
                o.visible_shadow = False; T.no_bounce(o)
            return ob, top, rim
        self.water = cyl("w3_water", self.wmat, self.wtop, R_)
        self.mol = cyl("w3_mol", self.mmat, self.mtop, R_ - 0.05)
        mb = H.MB(); mb.frustum((0, 0, 0), (0, 0, 1.0), 0.55, 0.75, self.smat, seg=16, cap0=False, cap1=False)
        self.stream = mb.obj("w3_stream", self.fx); self.stream.visible_shadow = False; T.no_bounce(self.stream)
        self.tc = tc

    def cam(self, shot, g):
        ks = [(KEYS[0], tuple(CAMS[0][0]) + tuple(CAMS[0][1]), "sine"),
              (KEYS[1], tuple(CAMS[1][0]) + tuple(CAMS[1][1]), "sine"),
              (KEYS[2], tuple(CAMS[2][0]) + tuple(CAMS[2][1]), "cubic"),
              (KEYS[3], tuple(CAMS[3][0]) + tuple(CAMS[3][1]), "sine"),
              (KEYS[4], tuple(CAMS[4][0]) + tuple(CAMS[4][1]), "lin")]
        v = mkeys(g, ks, 0.3)
        return Vector(v[:3]), Vector(v[3:])

    def cast_in(self, shot):
        return []

    def set_level(self, parts, level, alpha, base_alpha, wobble=0.0):
        ob, top, rim = parts
        show = level > 0.02 and alpha > 0.01
        for o in parts:
            o.hide_render = not show
        if not show:
            return
        ob.scale = (1, 1, level)
        top.location = (self.tc.x, self.tc.y, 0.36 + level)
        top.rotation_euler = (wobble * 0.004, wobble * 0.003, 0)
        rim.location = (self.tc.x, self.tc.y, 0.36 + level)
        set_emit(ob.active_material, alpha=base_alpha * alpha)
        set_emit(top.active_material, alpha=min(1.0, (base_alpha + 0.2) * alpha))
        set_emit(rim.active_material, alpha=0.9 * alpha)

    def per_frame(self, shot, g):
        x = ease(clamp((g - XR[0]) / float(XR[1] - XR[0])), "sine")
        for m in self.xmats:
            m.node_tree.nodes["XRAY"].inputs[0].default_value = 1.0 - 0.68 * x
        for md in self.shell.modifiers:
            md.show_render = False          # the tank's ink hull stays off through the whole take (no pop when the shell turns x-ray)
        full = TANK_TOP - 1.4
        # water test
        wl = full * ease(clamp((g - W_UP[0]) / float(W_UP[1] - W_UP[0])), "sine")
        wa = 1.0 - ease(clamp((g - W_FADE[0]) / float(W_FADE[1] - W_FADE[0])), "sine")
        self.set_level(self.water, wl + 0.08 * math.sin(g * 0.5) * (wl > 1), wa, 0.50, math.sin(g * 0.7))
        # molasses
        ml = (full - 2.5) * ease(clamp((g - M_UP[0]) / float(M_UP[1] - M_UP[0])), "quad_in") ** 0.8
        self.set_level(self.mol, ml, ease(clamp((g - M_UP[0] + 1) / 7.0), "sine"), 0.86)
        # the stream from the inlet down to the brown surface
        if g >= M_POUR:
            k = clamp((g - M_POUR) / 4.0)
            ztop = INLET.z
            zbot = ztop - k * (ztop - (0.36 + max(ml, 0.0)))
            self.stream.hide_render = False
            self.stream.location = (INLET.x + 0.05 * math.sin(g * 0.9), INLET.y, zbot)
            self.stream.scale = (1 + 0.08 * math.sin(g * 1.7), 1 + 0.08 * math.cos(g * 1.3), max(0.05, ztop - zbot))
        else:
            self.stream.hide_render = True


if __name__ == "__main__":
    main(Take, sys.argv)
