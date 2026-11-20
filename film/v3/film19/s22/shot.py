#!/usr/bin/env python3
"""shot.py -- film 19 take s22 = shot 22 (g 1756..1855 + handles g 1747..1755 in, 1856..1865 out).
"แต่คณะกรรมการจ่ายให้แค่ครึ่ง แล้วยึดนาฬิกาไปขังในกล่อง" -- but the Board paid only half, and locked the watch in a box.
HALL hall_table / DAY.  The camera stands at the door end looking along the baize table (candelabra, charts) toward the King's empty chair.
    g 1747..1777  Harrison (harrison19, sad, tricorne down) stands at the near end of the table; astro19 smug in the background
    g 1770..1796  the half-full money bag (set_moneybag('half')) is pushed along the baize by astro19_b's hand ("จ่ายให้แค่ครึ่ง", g 1778 / 1796)
    g 1800..1814  the box opens (set_box('open'), lid keyed up); astro19_b holds the H4 over it and lowers it in ("ยึดนาฬิกา", g 1807)
    g 1814..1820  the lid closes (keyed), set_box('closed')
    g 1821..1832  three red wax seals stamp down one after another on "ขัง" (caption 60.60 = g 1821); SNAP push on the seals; set_box('sealed')
Nobody speaks (still expression mouths).  NO depth of field, NO text, NO caption_shade.
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <dir> [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, cast19 = C.H, C.K, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(58.53), C.g_bound(61.86)      # 1756, 1856
H_IN, H_OUT = 9, 10
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1      # 1747..1865
G_BAG = C.cap_g("จ่ายให้แค่")                    # 1778
G_HALF = C.cap_g("ครึ่ง")                        # 1796
G_TAKE = C.cap_g("แล้วยึด")                      # 1807
G_SEAL = C.cap_g("นาฬิกาไปขัง")                  # 1821
SNAP = (G_SEAL - 3, G_SEAL + 13)
LIGHT, PRESET, FINAL_SPP = "DAY", "hall_table", 8

BAG_A, BAG_B = (0.55, 1.75), (-0.12, 1.15)       # money bag path (metres, table top), pushed from the right end toward Harrison
BOX_M = (0.5, 2.05)                              # the box moved nearer the right edge (metres) so astro19_b can reach it
STAND = dict(har=(0.3, 0.4, 0.0), bq=(2.3, 3.7, 0.0), mock=(-2.8, 6.0, 0.0))

CAM_LOC0 = (-1.0, -3.9, 3.3)
CAM_LOOK0 = (0.85, 3.8, 1.95)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.10, slide_px=0.0, rise_px=35.0, arc_deg_s=-9.0, decay=0.1,
                snaps=[dict(g=SNAP, k=2.6, peak=1.5, shift=(0.0, -0.2))])


def harrison_pose(g):
    p = dict(cast19.STORY19["harrison_idle"][1])
    p["expr"] = "sad"
    p["yaw"] = 0.3
    p["lean"] = 2.0 + 1.0 * math.sin(g * 0.11)
    p["head_roll"] = 2.0 * math.sin(g * 0.09)
    p["pitch"] = 0.15
    p["blink"] = blink(g, [1760, 1800, 1840])
    p["t"] = g / 30.0
    return p


def mock_pose(g):
    p = dict(cast19.STORY19["astro_idle"][1])
    p["expr"] = "smug"
    p["mouth"] = "flat"
    p["head_roll"] = 4 * math.sin(g * 0.07)
    p["lean"] = 2 * math.sin(g * 0.05)
    p["blink"] = blink(g, [1770, 1830])
    return p


def bq_pose(g):
    """astro19_b (mirrored: faces the table at screen-left): pushes the bag, then holds the H4 over the open box and lowers it in"""
    p = dict(cast19.STORY19["astro_b_idle"][1])
    p["mirror"] = True
    p["expr"] = "smirk"
    p["mouth"] = "flat"
    p["yaw"] = 0.3
    down, push, hold, drop = (0.35, 1.15), (0.95, 0.95), (0.95, 0.5), (0.9, 0.95)
    keys = [(0, down), (G_BAG - 8, down), (G_BAG, push), (G_HALF, push), (G_HALF + 8, down), (1796, down), (1804, hold), (1807, hold),
            (1814, drop), (1818, drop), (1826, down), (9999, down)]
    a = down
    for (g0, h0), (g1, h1) in zip(keys, keys[1:]):
        if g0 <= g < g1:
            u = u_of(g, g0, g1)
            a = tuple(lerp(h0[i], h1[i], u) for i in range(2))
            break
    p["arm_r"] = dict(hand=a, bend=-0.2, shape="open", stretch=1.35, layer="top")
    if 1798 <= g < 1814:
        p["prop_r"] = "h4_watch"
    p["blink"] = blink(g, [1765, 1812, 1850])
    p["t"] = g / 30.0
    return p


def bag_xy(g):
    u = u_of(g, G_BAG - 8, G_HALF)
    return (lerp(BAG_A[0], BAG_B[0], u), lerp(BAG_A[1], BAG_B[1], u))


def lid_angle(g):
    """lid rotation about x (deg): up (-105) while open, closes g 1814..1820"""
    return -105.0 * (1.0 - u_of(g, 1814, 1820))


SEAL_G = [G_SEAL, G_SEAL + 4, G_SEAL + 8]          # three stamps


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s22")
        assert self.final_samples() == FINAL_SPP
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        sd = os.path.join(WORK, "sprites")
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", sd, contact=True, cam=self.cam)
        self.bq = self.actors["bq"] = C.make_actor("bq", "astro19_b", sd, contact=True, cam=self.cam)
        self.mock = self.actors["mock"] = C.make_actor("mock", "astro19", sd, contact=True, cam=self.cam)
        Hk = K.STATE["hooks"]
        self.bag, self.box, self.lid = Hk["bag_half"], Hk["box"], Hk["boxlid"]
        self.tz = self.box.location.z
        # my own three seals (same dimensions as the set's sealed state) so they can drop one at a time
        M = K.STATE["M"]
        self.seals = []
        for i, x in enumerate((-0.17, 0.0, 0.17)):
            em = C.bpy.data.objects.new("seal22_%d" % i, None)
            C.bpy.context.scene.collection.objects.link(em)
            em.parent = self.box
            em.location = (x, -0.17, 0.2 + 0.012)
            b = K.MB("seal22")
            b.cyl(M["wax"], (0, 0, 0.0), 0.032, 0.014, seg=12)
            b.cyl(M["wax"], (0, 0, 0.010), 0.022, 0.012, seg=12)
            b.finish(parent=em)
            self.seals.append(em)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            for a, k in ((self.har, "har"), (self.bq, "bq"), (self.mock, "mock")):
                C.place(a, f, Vector(STAND[k]))
            self.key_set(f, candles=1.0)
            # money bag: appears at the start of the push, slides across the baize
            self.key_set(f, moneybag="half" if g >= G_BAG - 8 else "none")
            bx, by = bag_xy(g)
            self.bag.location = (bx, by, self.tz)
            K._keyxf(self.bag, f, loc=True, rot=False)
            # box: open from g 1798, closed after the lid shuts (g 1820), sealed once the three seals are down
            st = "none" if g < 1798 else ("open" if g < 1820 else ("closed" if g < SEAL_G[2] + 4 else "sealed"))
            self.key_set(f, box=st)
            self.box.location = (BOX_M[0], BOX_M[1], self.tz)
            K._keyxf(self.box, f, loc=True, rot=False)
            self.lid.rotation_euler = (math.radians(lid_angle(g)) if st != "none" else 0.0, 0, 0)
            K._keyxf(self.lid, f, loc=False, rot=True)
            for em, sg in zip(self.seals, SEAL_G):
                vis = (sg <= g < SEAL_G[2] + 4)
                C.key_vis([em] + list(em.children), vis, f)
                drop = 0.35 * (1.0 - u_of(g, sg - 3, sg)) if g >= sg - 3 else 0.35
                em.location = (em.location.x, -0.17, 0.212 + drop)
                K._keyxf(em, f, loc=True, rot=False)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.har.pose(f, harrison_pose(g), camera=self.cam)
            self.bq.pose(f, bq_pose(g), camera=self.cam)
            self.mock.pose(f, mock_pose(g), camera=self.cam)
        self.sprites_for([(self.har, 320), (self.bq, 320), (self.mock, 192)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(list(range(G_FIRST, G_LAST)))
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
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        samples = samples or FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft" if scale == 0.5 else "q%g" % scale)
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
