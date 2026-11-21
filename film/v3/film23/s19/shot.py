#!/usr/bin/env python3
"""shot.py -- film 23 take s19: shot S19 (LANE day), "ending": wide -> medium push ending on the Major, who sits on a crate blowing balloon after balloon, red-faced
(puffed cheeks, steam); the pile grows (set_pile, stepped every STEP frames); the crew grins and waves; on the last word the last balloon escapes and loops away
(set_loose_balloon, the other airborne thing).  Dissolve 17 in (in-handle 11).
QA_ART_SET S19: crate text ("DECOY M4", y ~925 in the first frame) must be out of y 880-950; the shadow under the pile tinted toward hue 248.

    python3 shot.py probe a:b[:s] | stills a:b[:s] out [scale] [samples] | final a:b[:s] [scale] [samples] | ground all
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c23 as C                                                          # noqa: E402
from c23 import GH, cast23, lerp, sm, seg                                # noqa: E402
import bpy                                                               # noqa: E402
S = cast23.STORY23

STEP = 1                  # set_pile is keyed every frame (2 ms per call: measured, so no stepping needed)
ESC_I = 116               # shot-local frame the last balloon leaves the Major's hands (the last word)
ESC_N = 50                # frames of the escape loop
FG = ("crate", ("cam", 1.8, 1.0), 20, 0.8, "crate_a")       # the planned fg prop; QA: lower it / move it so its text clears y 880-950
FG_DY = 0.0               # extra nearer/lower shift is done in tweak()


class T(C.Take):
    SID = "S19"
    D_IN = 17
    HERE_DIR = HERE

    def tweak(self):
        sh = C.SH.SHOTS["S19"]
        sh["fg"] = FGSPEC
        sh["move"] = dict(end=dict(loc=END_LOC, look_at=END_LOOK, lens=END_LENS))

    def __init__(self, quality="preview"):
        C.Take.__init__(self, quality, work=os.path.join(HERE, "work"))
        m = self.marks
        self.pm = m["major"][0][:3]
        self.pc = [c[:3] for c in m["crew"]]
        self.maj = self.add("maj", "major")
        self.c0 = self.add("cr0", "gi_designer")
        self.c1 = self.add("cr1", "gi_pump")
        self.c2 = self.add("cr2", "gi_driver")
        self.loose = bpy.data.objects.get("balloon_loose")
        for nm in ("crate_chalk", "crate_chalk_contact"):          # QA S19: the "DECOY M4" crate text sat at y ~925 in the first frame: that crate (S08's chalk crate) is not needed here: hidden
            ob = bpy.data.objects.get(nm)
            if ob is not None:
                ob.hide_render = True; ob.hide_viewport = True
        self.shadow_all()
        self.tint_shadow()

    def tint_shadow(self):
        """QA S19: shade hue 273 (violet) under the pile: tint the ground shade toward blue (hue 248): per-channel factor on the ground shade colour."""
        for m_ in bpy.data.materials:
            if not m_.name.startswith("GH_morning_ground"):
                continue
            for nd in m_.node_tree.nodes:
                if nd.bl_idname == "ShaderNodeMix" and getattr(nd, "blend_type", "") == "MULTIPLY" and not nd.inputs[7].is_linked:
                    c = nd.inputs[7].default_value
                    nd.inputs[7].default_value = (c[0] * SH_K[0], c[1] * SH_K[1], c[2] * SH_K[2], 1.0)

    # ------------------------------------------------------------ choreography
    def pile_k(self, i):
        return 0.70 + 0.30 * seg(i, -11, ESC_I + 10)

    def pose_major(self, g):
        i = g - self.clk["g0"]
        ph = (i - ESC_I) % 72                                                 # a balloon is full at i = ESC_I (+ 72 k)
        nb = (i - ESC_I - 1) // 72 + 5
        p = cast23.balloon_frame("major", ph, nb, per=72)
        if i > ESC_I:                                                         # the last balloon has gone: hands up after it, jaw dropped
            u = seg(i, ESC_I, ESC_I + 10)
            p["balloon23"] = dict(p.get("balloon23", {}), size=0.0)
            p["puff23"] = 0
            p["expr"] = "shocked"
            p["mouth"] = ("open", 0.16, 0.2)
            p["arm_r"] = dict(hand=(lerp(0.17, 0.5, u), lerp(0.286, -0.9, u)), bend=0.5, stretch=1.2, shape="open", layer="top")
            p["head_roll"] = -5.0 * u
            p["pitch"] = lerp(-0.2, -0.8, u)
        p["blink"] = cast23.blink_at(i, 90, 23)
        return p

    def pose_crew(self, k, g):
        i = g - self.clk["g0"]
        if k == 0:                                                            # waves at the camera, grinning
            p = cast23.wave_frame("gi_designer", i / 12.0, facing=-1, expr="happy")
        elif k == 1:                                                          # belly laugh bounce
            p = cast23.laugh_frame("gi_pump", i / 10.0, S["gi_laugh_pump"][1])
        else:                                                                 # the driver grins, arms akimbo
            p = dict(S["gi_grin_driver"][1])
            p["lean"] = p.get("lean", 0) + 1.2 * math.sin(i * 0.21)
            p["head_roll"] = 2.0 * math.sin(i * 0.13)
        p["blink"] = cast23.blink_at(i, 84 + 11 * k, 9 + 23 * k)
        p["t"] = i / 30.0
        return p

    def staging(self, gs):
        fs = [self.f_of(g) for g in gs]
        last_k = None
        for g in gs:
            f = self.f_of(g); i = g - self.clk["g0"]
            C.place(self.maj, f, self.pm)
            for k, a in enumerate((self.c0, self.c1, self.c2)):
                C.place(a, f, self.pc[k] if k < 2 else (CR2[0] + self.origin.x, CR2[1] + self.origin.y, C.gz(CR2[0] + self.origin.x, CR2[1] + self.origin.y, sink=0.012)))
            kk = self.pile_k(i)
            if last_k is None or (g - gs[0]) % STEP == 0 or g == gs[-1]:
                GH.set_pile(kk, frame=f)
            t = (i - ESC_I) / float(ESC_N)
            tt = 0.0 if t <= 0 else min(1.0, t)
            import ghost_lane as GL
            if self.loose is not None:                       # set_loose_balloon writes WORLD coords onto a parented object (doubled): key the local position instead
                w = GL.loose_path(tt); r = self.loose.parent.matrix_world.translation
                self.loose.location = (w[0] - r.x, w[1] - r.y, w[2] - r.z); self.loose.keyframe_insert("location", frame=f)
            if self.loose is not None:
                self.loose.hide_render = t <= 0 or t >= 1.0
                self.loose.keyframe_insert("hide_render", frame=f)
                self.loose["airborne"] = True
            last_k = kk
        for g in gs:
            f = self.f_of(g)
            self.scene.frame_set(f)
            self.maj.pose(f, self.pose_major(g), camera=self.cam)
            for k, a in enumerate((self.c0, self.c1, self.c2)):
                a.pose(f, self.pose_crew(k, g), camera=self.cam)
        self.sprites_for([(self.maj, 256), (self.c0, 256), (self.c1, 256), (self.c2, 256)], fs)

    def report(self, g):
        f = self.f_of(g)
        self.scene.frame_set(f)
        return dict(g=g, f=f, cam=[round(v, 3) for v in self.cam.location], heads=C.head_report(self, f))


FGSPEC = ("hay", ("cam", 2.0, -1.2), 40, 0.8)
END_LENS = 30.0
SH_K = (1.0, 1.0, 1.0)
END_LOC, END_LOOK = (9.2, 1.9, 3.7), (10.6, 9.3, 2.6)
CR2 = (14.2, 4.4)
CRATE_D = (-4.2, -2.5)

if __name__ == "__main__":
    C.run(T)
