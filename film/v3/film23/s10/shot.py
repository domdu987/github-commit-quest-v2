#!/usr/bin/env python3
"""shot.py -- film 23 take s10: shot S10 (CAMP night), "count (radio, fake insignia)": side-tracking through the radio tent and out to a truck;
the radio man chatters into the handset, the painter stencils a division badge on a bumper.  QA_ART_SET: crate text out of y 880-950; the flat
orange tent wall dressed with radio sets and a map in the first frame.   Cut in (no in-handle).

    python3 shot.py probe a:b[:s] | stills a:b[:s] out [scale] [samples] | final a:b[:s] [scale] [samples] | ground all
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c23 as C                                                          # noqa: E402
from c23 import GH, cast23, lerp, sm, seg                                # noqa: E402
S = cast23.STORY23
CRATE_DY = -1.6
END_DX = 2.2


def map_png(path):
    from PIL import Image, ImageDraw
    W, H = 640, 480
    im = Image.new("RGB", (W, H), (222, 205, 160)); d = ImageDraw.Draw(im)
    for x in range(0, W, 40): d.line([(x, 0), (x, H)], fill=(190, 170, 120), width=1)
    for y in range(0, H, 40): d.line([(0, y), (W, y)], fill=(190, 170, 120), width=1)
    d.polygon([(0, 300), (120, 260), (210, 300), (300, 250), (420, 290), (520, 240), (640, 270), (640, 480), (0, 480)], fill=(150, 175, 205))   # river / sea
    d.line([(0, 300), (120, 260), (210, 300), (300, 250), (420, 290), (520, 240), (640, 270)], fill=(70, 80, 110), width=5)
    d.polygon([(60, 60), (260, 50), (330, 120), (250, 190), (90, 170)], fill=(170, 190, 130))
    for (x, y) in ((150, 110), (230, 90), (270, 150), (110, 140)): d.rectangle([x, y, x + 26, y + 16], fill=(120, 120, 130), outline=(60, 50, 70), width=2)
    d.line([(150, 120), (330, 190), (470, 230)], fill=(190, 40, 40), width=7); d.polygon([(470, 218), (500, 238), (466, 246)], fill=(190, 40, 40))
    d.line([(520, 60), (420, 140), (360, 200)], fill=(40, 70, 170), width=7); d.polygon([(350, 190), (380, 196), (362, 218)], fill=(40, 70, 170))
    for (x, y) in ((560, 100), (580, 140), (540, 150)): d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(190, 40, 40), outline=(70, 20, 20), width=2)
    d.rectangle([4, 4, W - 5, H - 5], outline=(90, 70, 50), width=6)
    im.save(path)


def dress_tent_wall(work):
    """QA_ART_SET S10: put radio sets and a map on the flat orange back wall of the radio tent (it is the glowing tent_in face)."""
    import bpy
    from mathutils import Vector
    import ghost_camp as GCP
    T_ = GH.T
    gz = GH.STATE["gz"]
    ox, oy = GCP.TENT[0], GCP.TENT[1]
    o = GH.to_world((ox, oy, gz(ox, oy)))
    F = GCP.PR.BK.Frame(o, GCP.TENT[2])
    hy = 5.0
    SET = GH.STATE["SET"]
    os.makedirs(work, exist_ok=True)
    mp = os.path.join(work, "tent_map.png"); map_png(mp)
    def mk(name, pts, mat):
        me = bpy.data.meshes.new(name); me.from_pydata([tuple(F.p(*p)) for p in pts], [], [tuple(range(len(pts)))])
        uv = me.uv_layers.new(name="UVMap")
        for i, q in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))[:len(pts)]): uv.data[i].uv = q
        me.materials.append(mat); ob = bpy.data.objects.new(name, me); SET.objects.link(ob); ob["gc_role"] = "skip"; ob.visible_shadow = False; GH.no_bounce(ob); return ob
    def box(name, cx, cz, w, h, d, mat):
        y0, y1 = hy - 0.12 - d, hy - 0.12
        x0, x1, z0, z1 = cx - w / 2, cx + w / 2, cz - h / 2, cz + h / 2
        V_ = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        me = bpy.data.meshes.new(name); me.from_pydata([tuple(F.p(*p)) for p in V_], [], [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
        me.materials.append(mat); ob = bpy.data.objects.new(name, me); SET.objects.link(ob); ob["gc_role"] = "skip"; ob.visible_shadow = False; GH.no_bounce(ob); return ob
    olive = T_.mat_emit("tw_olive", "#5b6a3a", strength=0.9); olive_d = T_.mat_emit("tw_olive_d", "#3f4a2b", strength=0.8)
    dial = T_.mat_emit("tw_dial", "#ffe9a8", strength=2.2); red = T_.mat_emit("tw_red", "#e0412c", strength=1.6); dark = T_.mat_emit("tw_dark", "#2b2a2a", strength=0.7)
    mapm = T_.mat_emit("tw_map", image=mp, strength=1.0)
    yf = hy - 0.14
    mk("tw_map", [(-0.7, yf, 1.25), (2.0, yf, 1.25), (2.0, yf, 3.05), (-0.7, yf, 3.05)], mapm)          # the map (UV 0..1), pinned
    mk("tw_map_frame_t", [(-0.8, yf - 0.01, 3.05), (2.1, yf - 0.01, 3.05), (2.1, yf - 0.01, 3.15), (-0.8, yf - 0.01, 3.15)], dark)
    for k, (cx, cz) in enumerate(((-2.6, 1.55), (-2.6, 2.75), (3.1, 1.55), (3.1, 2.75))):               # four radio sets, stacked left and right of the map
        box("tw_set%d" % k, cx, cz, 1.7, 1.05, 0.28, olive if k % 2 == 0 else olive_d)
        mk("tw_panel%d" % k, [(cx - 0.8, yf - 0.28, cz - 0.45), (cx + 0.8, yf - 0.28, cz - 0.45), (cx + 0.8, yf - 0.28, cz + 0.45), (cx - 0.8, yf - 0.28, cz + 0.45)], dark)
        for j, dx in enumerate((-0.45, 0.0, 0.45)):
            d_ = GH.bpy.data.objects.new("tw_dial%d_%d" % (k, j), None)
            mk("tw_knob%d_%d" % (k, j), [(cx + dx - 0.12, yf - 0.29, cz + 0.12), (cx + dx + 0.12, yf - 0.29, cz + 0.12), (cx + dx + 0.12, yf - 0.29, cz + 0.36), (cx + dx - 0.12, yf - 0.29, cz + 0.36)], dial)
            bpy.data.objects.remove(d_)
        mk("tw_led%d" % k, [(cx + 0.55, yf - 0.29, cz - 0.30), (cx + 0.70, yf - 0.29, cz - 0.30), (cx + 0.70, yf - 0.29, cz - 0.15), (cx + 0.55, yf - 0.29, cz - 0.15)], red)


class T(C.Take):
    SID = "S10"
    D_IN = 0
    HERE_DIR = HERE

    def tweak(self):
        sh = C.SH.SHOTS["S10"]
        # (QA_ART_SET S10 crate text: the set crate `crate.019` is moved nearer to the lens after the build, see T.__init__)
        # end the slide a little further left so the painter is framed (planned end ~0.5 W) instead of at the left edge
        e = sh["move"]["end"]
        sh["move"] = dict(end=dict(e, loc=(e["loc"][0] - END_DX, e["loc"][1], e["loc"][2]), look_at=(e["look_at"][0] - END_DX, e["look_at"][1], e["look_at"][2])))

    def __init__(self, quality="preview"):
        C.Take.__init__(self, quality, work=os.path.join(HERE, "work"))
        m = self.marks
        dress_tent_wall(os.path.join(HERE, "work"))
        cr = C.bpy.data.objects["crate.019"]                       # the "U.S. ARMY" crate: its text sat at y ~930 (QA band 880-950): move it nearer, lower in frame
        cr.location.y += CRATE_DY
        GH.ground_snap(cr)
        self.pos = {k: m[k][0][:3] for k in ("radioman", "painter", "soldier")}
        self.radio = self.add("radio", "gi_radio")
        self.paint = self.add("paint", "gi_painter")
        self.sold = self.add("sold", "gi_pump")
        self.shadow_all()

    def pose_radio(self, g):
        i = g - self.clk["g0"]
        p = dict(S["gi_radio_talk"][1])
        p["mouth"] = "talk_a"                                            # held drawing: not a quote
        p["arm_r"] = dict(p["arm_r"], hand=(0.5, 0.06 + 0.02 * math.sin(i * 0.5)))
        p["lean"] = 2.0 * math.sin(i * 0.19)
        p["head_roll"] = 3.0 * math.sin(i * 0.23)
        p["blink"] = cast23.blink_at(i, 90, 17)
        p["t"] = i / 30.0
        p.update(C.tint_for(self.light))
        return p

    def pose_paint(self, g):
        i = g - self.clk["g0"]
        p = cast23.paint_frame("gi_painter", i / 18.0, facing=1)
        p["blink"] = cast23.blink_at(i, 96, 40)
        p.update(C.tint_for(self.light))
        return p

    def pose_sold(self, g):
        i = g - self.clk["g0"]
        p = dict(S["gi_carry_pump"][1])
        p["lean"] = p.get("lean", 0) + 1.0 * math.sin(i * 0.2)
        p["blink"] = cast23.blink_at(i, 110, 5)
        p["t"] = i / 30.0
        p.update(C.tint_for(self.light))
        return p

    def staging(self, gs):
        fs = [self.f_of(g) for g in gs]
        for g in gs:
            f = self.f_of(g)
            GH.flicker(f)
            C.place(self.radio, f, self.pos["radioman"])
            C.place(self.paint, f, self.pos["painter"])
            C.place(self.sold, f, self.pos["soldier"])
        for g in gs:
            f = self.f_of(g)
            self.scene.frame_set(f)
            self.radio.pose(f, self.pose_radio(g), camera=self.cam)
            self.paint.pose(f, self.pose_paint(g), camera=self.cam, upper_k=None)
            self.sold.pose(f, self.pose_sold(g), camera=self.cam)
        self.sprites_for([(self.radio, 256), (self.paint, 256), (self.sold, 256)], fs)

    def report(self, g):
        f = self.f_of(g)
        self.scene.frame_set(f)
        return dict(g=g, f=f, cam=[round(v, 3) for v in self.cam.location], heads=C.head_report(self, f))


if __name__ == "__main__":
    C.run(T)
