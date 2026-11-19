#!/usr/bin/env python3
"""shot.py -- film 16 take s24 = shot 24, THE REVEAL MACRO (g 1540..1614 + 9 handle frames each side; hard CUT in at 1540 and out at 1615).
"ไฟเลยวิ่ง อยู่แต่ในลวด ไม่รั่วลงเสา สักหยด" -- the current runs only inside the wire, does not leak down the pole, not one drop.

LINE bottle_macro / AFTER_RAIN: ONE glowing pulse (TG.set_pulse, keyed per frame) runs along the wire from the left, slides over the
bottle neck and PARKS inside the glass (TG.pulse_s_at_pole(1)); the wet pole below stays dark (the pulse's cyan light is linked to the
glass only).  Camera: whip follow -- the look point rides the pulse head from the left edge, then settles on the bottle -- on top of a
drift push + slide + arc, plus one eased SNAP push on "ไม่รั่วลงเสา" (event g 1582).  No cast, no text, no DOF.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, LN = C.TG, C.K, C.LN
lerp, clamp, ez, u_of, bf = C.lerp, C.clamp, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(51.32), C.g_bound(53.83)   # 1540, 1615: shot 24 = g 1540..1614; shot 25 (cut) starts at 1615
H_IN = H_OUT = 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1   # 1531, 1623
GS = list(range(G_FIRST, G_LAST + 1))
G_RUN0 = G_FIRST - 4                           # the pulse is already on the wire, left of the pole, on the first frame
G_GLASS = 1556                                 # the head reaches the glass ("ไฟเลยวิ่ง" 1543 .. "อยู่แต่ในลวด" 1561)
G_SNAP_WORD = 1582                             # "ไม่รั่วลงเสา": snap push to the neck + the dark pole below
SNAP = (G_SNAP_WORD - 3, G_SNAP_WORD + 10)    # 13 frames
SPARKS = (1568, 1600)                          # weak sparks at the rim try to creep down and die (the pole stays dark)
DS_FRAME = 0.016                               # pulse path (fraction of the whole wire) per ~16 D of line is 0.0588: 0.024 = ~6.5 D = the frame half width
HOLD = 11                                      # frames the head stays inside the glass (QA-art: neck glow held 10-12 frames)
FOLLOW_END = 1568                              # the look point stops riding the head


def darken(mat, tint, rough):
    """multiply the (texture-driven) base colour of a material by `tint` and make it glossier (wet)."""
    nt = mat.node_tree
    bs = [n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"][0]
    bs.inputs["Roughness"].default_value = rough
    lk = [l for l in nt.links if l.to_socket == bs.inputs["Base Color"]]
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type, mix.blend_type = "RGBA", "MULTIPLY"
    mix.inputs[0].default_value = 1.0
    mix.inputs[7].default_value = (tint[0], tint[1], tint[2], 1.0)
    if lk:
        src = lk[0].from_socket
        nt.links.remove(lk[0])
        nt.links.new(src, mix.inputs[6])
    nt.links.new(mix.outputs[2], bs.inputs["Base Color"])


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bottle_macro", quality=quality, name="cam_s24")
        S = TG.STATE
        M = S["M"]
        darken(M["pole"], (0.34, 0.31, 0.38), 0.24)                    # wet dark pole (QA-art): the contrast for "no leak"
        bs = [n for n in M["glass"].node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
        bs.inputs["Alpha"].default_value = 1.0
        bs.inputs["Transmission Weight"].default_value = 0.8
        bs.inputs["Base Color"].default_value = (0.02, 0.30, 0.07, 1.0)
        for ob in bpy_objects():                                       # the ladder leans on the field side: out of this camera's way
            if ob.name.startswith("ladder"):
                ob.hide_render = True
        for ob in bpy_objects():                                       # the low field-side camera looks into the sun glare on the wet ground / puddles
            if ob.name.startswith("puddles"):
                ob.hide_render = True
            if ob.name.startswith("ground"):
                for ms in ob.data.materials:
                    for n in ms.node_tree.nodes:
                        if n.type == "BSDF_PRINCIPLED":
                            n.inputs["Roughness"].default_value = 0.85
                            if "Specular IOR Level" in n.inputs:
                                n.inputs["Specular IOR Level"].default_value = 0.1
        TG.set_wet(0.15)                                               # the sun glare on the wet ground washed out the first frames; the pole stays dark (multiplied above)
        self.s_park = TG.pulse_s_at_pole(1)
        self.pts, self.cum = S["wire_pts"]["bottle"]
        self.top = Vector(K.W((LN.px(LN.POLES_Y[1]) + 0.03, LN.POLES_Y[1], LN.POLE_H + 0.01)))      # pole top / glass mouth (world D)
        self.glass = self.top + Vector((0, 0, 1.8))
        sub = self.top + Vector((0.0, 0.0, -3.0))                      # subject: the neck and the dark pole top
        # field-side camera (looks along +y with the line along +x: the pulse travels screen-RIGHT), low, glass in the upper third
        loc0 = self.top + Vector((0.0, -8.5, -3.0))
        self.cam_path = C.CamPath(loc0, sub, G0, G_LAST, push=0.07, slide_px=70.0, arc_deg_s=-15.0, decay=0.3,
                                  snaps=[dict(g=SNAP, k=1.35, peak=1.8, shift=(0.0, 1.5))])
        self.sparks = self.make_sparks()
        self.wet_props()

    def wet_props(self):
        """wet look on pole 1 (runtime geometry): a specular streak down the pole, a few drips crawling down it, a small dark puddle at its foot."""
        import bpy
        from math import atan2
        M = TG.STATE["M"]
        def mat(name, col, rough, emit=0.0, trans=0.0, alpha=1.0):
            m = bpy.data.materials.new(name)
            m.use_nodes = True
            b = [n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
            b.inputs["Base Color"].default_value = col
            b.inputs["Roughness"].default_value = rough
            if emit:
                b.inputs["Emission Color"].default_value = col
                b.inputs["Emission Strength"].default_value = emit
            if trans:
                b.inputs["Transmission Weight"].default_value = trans
            return m
        base = Vector((self.top.x, self.top.y, 0.0))
        cam_dir = Vector((0.0, -1.0, 0.0))                         # toward the camera (field side)
        left = Vector((1.0, 0.0, 0.0))                              # screen-left is +x for this camera? the pulse runs to +x = screen right, so left is -x
        left = Vector((-1.0, 0.0, 0.0))
        out = []
        # puddle: a flat dark glossy ellipse at the foot, a little toward the camera
        bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=1.0, depth=0.02, location=(base.x - 0.2, base.y - 0.45, 0.05))
        p = bpy.context.object
        p.name = "s24_puddle"
        p.scale = (1.15, 0.70, 1.0)
        p.data.materials.append(mat("puddle_dark", (0.006, 0.007, 0.014, 1.0), 0.32))
        p.visible_shadow = False
        # specular streak: a thin pale strip up the pole on its sun-lit side
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.022, depth=8.4, location=(base.x - 0.035, base.y - 0.108, 4.6))
        st = bpy.context.object
        st.name = "s24_sheen"
        st.data.materials.append(mat("sheen", (0.75, 0.82, 1.0, 1.0), 0.05, emit=2.6))
        st.visible_shadow = False
        # drips: small clear beads that creep down the pole
        self.drips = []
        for i, (z0, dxy) in enumerate(((7.4, 0.05), (5.9, -0.06), (4.2, 0.02), (6.6, -0.1))):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=8, radius=1.0, location=(0, 0, 0))
            d = bpy.context.object
            d.name = "s24_drip%d" % i
            d.scale = (0.04, 0.04, 0.11)
            d.data.materials.append(mat("drip", (0.55, 0.65, 0.85, 1.0), 0.02, trans=0.6))
            d.visible_shadow = False
            d["z0"], d["dxy"] = z0, dxy
            self.drips.append(d)
            out.append(d)

    def make_sparks(self):
        import bpy
        m = bpy.data.materials.new("spark")
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        out, em = nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (0.35, 0.85, 1.0, 1.0)
        em.inputs["Strength"].default_value = 30.0
        nt.links.new(em.outputs[0], out.inputs["Surface"])
        obs = []
        for i, (dx, dz) in enumerate(((0.10, 0.05), (-0.14, 0.12), (0.02, 0.22))):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=6, radius=0.13, location=(0, 0, 0))
            ob = bpy.context.object
            ob.name = "s24_spark%d" % i
            ob.data.materials.append(m)
            ob.visible_shadow = False
            ob["dx"], ob["dz"] = dx, dz
            obs.append(ob)
        return obs

    def head_world(self, s):
        d0 = min(1.0, max(0.0, s)) * self.cum[-1]
        p = TG._wire_at(self.pts, self.cum, d0)
        head, _ = TG._pulse_head_target(p)
        return TG.W(head)

    def s_of(self, g):
        # constant speed: DS_FRAME per (G_GLASS - G_RUN0) frames; the head reaches the glass at G_GLASS and runs on along the wire
        v = DS_FRAME / float(G_GLASS - G_RUN0)
        if g <= G_GLASS:
            return self.s_park + v * (g - G_GLASS)
        if g <= G_GLASS + HOLD:
            return self.s_park + 0.0006 * (g - G_GLASS) / float(HOLD)          # sits in the glass: the neck glows (barely creeping)
        return self.s_park + 0.0006 + v * (g - G_GLASS - HOLD)

    def cam_at(self, g):
        loc, look = self.cam_path.at(g)
        w = 1.0 - u_of(g, G_FIRST, FOLLOW_END, kind="sine")            # 1 = riding the head, 0 = settled on the pole
        h = self.head_world(self.s_of(max(g, G_FIRST) - 6))             # lags the head by 6 frames: the pulse runs ahead of the camera
        off = Vector((h.x - self.top.x, 0.0, 0.0)) * w
        off.x = clamp(off.x, -3.2, 3.2)
        return loc + off * 0.15, look + off

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cam_at(g))
            TG.set_pulse(self.s_of(g), frame=f)
            for d in self.drips:
                z = d["z0"] - 0.012 * (g - G_FIRST) - 0.06 * math.sin(0.4 * (g - G_FIRST) + d["z0"])     # creeping down the wet pole, a slight wobble
                r = 0.14 - 0.0058 * (z + 0.2)                           # pole radius at that height
                d.location = (self.top.x - 0.04 + d["dxy"] * 0.5, self.top.y - r - 0.004, z)
                d.keyframe_insert("location", frame=f)
            for i, ob in enumerate(self.sparks):
                a, b = SPARKS
                u = (g - a - i * 4) / float(b - a - i * 4)
                on = 0.0 < u < 1.0
                sc = (0.9 * (1 - u) ** 1.5) * (0.55 + 0.45 * math.sin(g * 1.9 + i * 2.1)) if on else 0.0
                ob.location = self.top + Vector((ob["dx"] * (1 - 0.6 * u), 0.0, 0.05 + ob["dz"] * (1.0 - u)))
                ob.scale = (max(sc, 1e-3),) * 3
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("scale", frame=f)
                C.key_vis(ob, on and sc > 0.02, f)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, s=round(self.s_of(g), 4), head_px=TG.project(tuple(self.head_world(self.s_of(g)))), top_px=TG.project(tuple(self.top)),
                    cam=[round(c, 3) for c in self.cam_at(g)[0]])

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def bpy_objects():
    return C.bpy.data.objects


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST] if len(sys.argv) > 2 else []
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
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
