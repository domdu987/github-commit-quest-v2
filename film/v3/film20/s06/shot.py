#!/usr/bin/env python3
"""shot.py -- film 20 take T06 = s06 = shots 6+7+8 as ONE continuous camera-travel take (WORKER20 §8, shot_plan "§I re-plan").
CAFE cafe_wide scene (1887, tower stub in the window), DAY.  g 404..603 (13.47-20.15 s); in-handle 8 (g 396..403, DIS 13), out-handle 4 (g 604..607).
Travel (waypoints, centripetal-free Catmull-Rom on loc + look, eased, no stop):
  396..440  slide past the outraged artists waving newspapers (sun shafts, gas lamps)           beat 6
  430..446  push-in SNAP on "สี่สิบกว่าคน" (444)
  446..490  descend and push DOWN onto the protest sheet; first signature lands g 471 ("ลงชื่อประท้วง" 469), the second g 496        beat 7
  490..512  hands pass the quill over the sheet (runtime meshes), heading "PROTESTATION" on the sheet
  512..572  rise off the sheet, travel across the café to the window: smoke ramps 0 -> 1 (g 513..572, "เหมือนปล่อง" 572), artists jab at it  beat 8
  572..603  turn toward the banquette where Maupassant sits (end_cam, match framing for T09), 4 handle frames continue
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples] | camreport
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
import bpy                                               # noqa: E402
S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(13.47), C.g_bound(20.15)       # 404, 604
H_IN, H_OUT = 8, 4                                 # DIS 13 -> 8 handle frames (director), cut/match side 4
GA, G_LAST = G0 - H_IN, G1 + H_OUT - 1             # 396 .. 607
GS = list(range(GA, G_LAST + 1))
G_COUNT = C.cap_g("สี่สิบกว่าคน")                  # 444
G_SIGN = C.cap_g("ลงชื่อประท้วง")                  # 469
G_PAPER = C.cap_g("ในหนังสือพิมพ์")                 # 491
G_CHIM = C.cap_g("เหมือนปล่อง")                    # 572
LAND1, LAND2 = G_SIGN + 2, G_PAPER + 5             # 471, 496
PASS = (483, 494)
RAMP0 = C.g_bound(17.10)                           # 513
LIGHT, PRESET, PPD = "DAY", "cafe_wide", 144
SHEET_Z = 0.772                                    # m
N0 = 14

# ----------------------------------------------------------------------------- camera: waypoints (g, loc D, look D)
WP = [
    (396, (-0.1, 0.5, 2.3), (-1.2, 6.9, 2.5)),
    (418, (0.3, 1.1, 2.3), (-1.1, 6.9, 2.45)),
    (430, (0.4, 1.9, 2.25), (-1.0, 6.8, 2.4)),
    (444, (-0.1, 3.1, 2.15), (-1.0, 6.6, 2.0)),       # snap push-in on "สี่สิบกว่าคน"
    (466, (-0.5, 4.9, 2.1), (-0.95, 6.5, 1.55)),      # descend: the artists leave the frame cleanly
    (488, (-0.56, 5.45, 1.97), (-0.92, 6.5, 1.44)),   # the raking insert pose of cafe_table_insert
    (512, (-0.4, 5.5, 2.0), (-0.7, 6.5, 1.5)),        # still over the sheet, starts to rise
    (556, (0.0, 5.3, 2.3), (0.5, 8.2, 2.1)),          # calm rise, the aim swings up toward the window
    (572, (0.9, 4.7, 2.6), (1.55, 12.8, 3.2)),        # stub + black smoke
    (582, (1.3, 5.9, 2.25), (1.7, 13.0, 2.95)),         # sweep down toward the banquette
    (593, (2.25, 8.8, 1.5), (1.7, 13.2, 2.3)),         # slowing
    (598, (2.55, 9.45, 1.38), (1.69, 13.17, 2.1)),
    (603, (2.618, 9.596, 1.334), (1.692, 13.160, 1.999)),     # LAST frame of T06 = team7's exact T09 start (their meta start_cam)
    (604, (2.599, 9.600, 1.350), (1.692, 13.160, 2.000)),     # first out-handle frame, drift (-0.019, +0.004, +0.016) D/frame
    (607, (2.542, 9.612, 1.398), (1.692, 13.160, 2.000)),     # out-handle keeps the same drift
]
END_CAM = dict(g=603, loc=WP[-3][1], look=WP[-3][2], lens=22.0, shift=(0.0, 0.0), note="turned toward the banquette (Maupassant mark (1.69, 13.16), seat (1.69, 14.0)); camera moving +y ~0.07 D/frame; D units")


def _tang(i):
    n = len(WP)
    a, b = max(i - 1, 0), min(i + 1, n - 1)
    dg = float(WP[b][0] - WP[a][0])
    return [(WP[b][k][j] - WP[a][k][j]) / dg for k in (1, 2) for j in range(3)]


def cam_at(g):
    """(loc, look) at film frame g: cubic Hermite through the waypoints (Catmull-Rom tangents) = continuous velocity, no parked frames"""
    g = clamp(g, WP[0][0], WP[-1][0]) if False else min(max(g, WP[0][0]), WP[-1][0])
    i = 0
    while i < len(WP) - 2 and g > WP[i + 1][0]:
        i += 1
    g0, g1 = WP[i][0], WP[i + 1][0]
    h = float(g1 - g0)
    t = (g - g0) / h
    t2, t3 = t * t, t * t * t
    h00, h10, h01, h11 = 2 * t3 - 3 * t2 + 1, t3 - 2 * t2 + t, -2 * t3 + 3 * t2, t3 - t2
    m0, m1 = _tang(i), _tang(i + 1)
    out = []
    for k in range(2):
        p0, p1 = WP[i][1 + k], WP[i + 1][1 + k]
        out.append(Vector(h00 * p0[j] + h10 * h * m0[3 * k + j] + h01 * p1[j] + h11 * h * m1[3 * k + j] for j in range(3)))
    return out[0], out[1]


class PathAdapter(object):
    def at(self, g):
        return cam_at(g)


def corner_speed(g):
    a, b = cam_at(g), cam_at(g + 1)
    dep = max(0.5, (a[1] - a[0]).length * 0.7)
    best = 0.0
    for cx in (0, 720):
        for cy in (0, 1280):
            best = max(best, C._corner_shift(a, b, dep, cx, cy))
    return best


# ----------------------------------------------------------------------------- cast
ART = [("art1", "painter20"), ("art2", "composer20"), ("art3", "poet20"), ("art4", "architect20")]
SPOT = {"art1": (-3.0, 6.9), "art2": (-2.0, 8.9), "art3": (-0.8, 7.9), "art4": (-2.1, 5.2), "wtr": (4.8, 8.5)}
YAW = {"art1": 0.35, "art2": 0.1, "art3": -0.35, "art4": 0.3}
PROP = {"art1": dict(type="news20", angle=-25, scale=0.6), "art2": None, "art3": dict(type="news20", angle=20, scale=0.6), "art4": dict(type="news20", angle=-35, scale=0.6)}
PHASE = {"art1": 0.0, "art2": 1.7, "art3": 3.1, "art4": 4.4}
POINT = {"art1": (0.95, 0.35), "art2": (1.0, 0.25), "art3": (1.0, 0.3), "art4": (0.9, 0.55)}
T_SWAP = 500                                       # while the camera is on the sheet the artists change from waving to pointing (swap not visible)


def pose_of(k, cast, g):
    t = g / 30.0
    ph = PHASE[k]
    base = dict(cast20.STORY20[cast + "_outraged"][1])
    base["expr"] = "outraged_c"
    if g < T_SWAP:                                  # beat 6/7: wave the newspapers
        w = 2 * math.pi * 1.7
        up = u_of(g, G_COUNT - 2, G_COUNT + 11)
        arm = dict(base["arm_r"])
        hx, hy = arm["hand"]
        arm["hand"] = (hx + 0.10 * math.sin(w * t + ph), hy - 0.45 + 0.12 * math.cos(w * t + ph) + 0.12 * up)
        base["arm_r"] = arm
        if PROP[k]:
            pr = dict(PROP[k]); pr["angle"] = pr["angle"] + 22 * math.sin(w * t + ph + 0.8)
            base["prop_r"] = pr
        base["lean"] = 2.0 * math.sin(w * t * 0.5 + ph + 1.0)
        base["yaw"] = abs(YAW[k])
    else:                                           # beat 8: jab fingers at the window
        w = 2 * math.pi * 1.9
        jab = 0.5 + 0.5 * math.sin(w * 1.3 * t + ph)
        up = u_of(g, G_CHIM - 2, G_CHIM + 13)
        hx, hy = POINT[k]
        base["arm_r"] = dict(hand=(hx + 0.30 * jab + 0.10 * up, hy + 0.10 * math.sin(w * t * 0.5 + ph)), shape="point", bend=-0.4, stretch=1.3, layer="top")
        base.pop("prop_r", None)
        base["lean"] = 2.0 * math.sin(w * t * 0.5 + ph + 1.0) + 2.0 * up
        base["yaw"] = 0.45 if k != "art3" else abs(YAW[k])
        base["expr"] = "outraged_c"
    base["head_roll"] = base.get("head_roll", 0) + 4 * math.sin(2 * math.pi * 0.85 * t + ph)
    base["squash"] = (1.0 + 0.012 * math.sin(2 * math.pi * 3.0 * t + ph), 1.0 - 0.012 * math.sin(2 * math.pi * 3.0 * t + ph))
    base["blink"] = blink(g, [420 + 7 * int(ph), 470 + 5 * int(ph), 560 + 3 * int(ph)])
    base["t"] = t
    return base


C.add_expression("outraged_c", eyes="half", tilt=10.0, brows=("both", 0.095, 26.0, 0.054, 0.19, 0.015), mouth="frown", mouth_dy=0.0)   # outraged with a CLOSED mouth


def smooth(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


class Take(C.Take):
    D_SHAFT = Vector((0.5, 0.5, 0.72)).normalized()

    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s06")
        CO.setup_grade(self.scene, dict(sat=float(os.environ.get("SAT", "1.45"))))      # film-wide saturation (QA_TEAM §G/§I)
        self.path = PathAdapter()
        self.scene.view_settings.exposure = self.scene.view_settings.exposure - float(os.environ.get("EXPO", "0.3"))      # luma <= 110, no blown floor patch
        self.key_cam(bf(GA), *cam_at(GA))
        self.scene.frame_set(bf(GA))
        M = CO.STATE["M"]
        sigs = CO.STATE["sigs"]
        self.S1, self.S2 = self.sig_centre(sigs[N0]), self.sig_centre(sigs[N0 + 1])
        self.build_hands(M)
        self.build_heading(M)
        for k, cast in ART:
            self.actors[k] = C.make_actor(k, cast, os.path.join(WORK, "sprites"), cam=self.cam, contact=dict(width=1.2, depth=0.5, opacity=0.7))
        self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), cam=self.cam, contact=dict(width=1.2, depth=0.5, opacity=0.7))
        self.actors["wtr"] = C.make_actor("wtr", "waiter", os.path.join(WORK, "sprites"), cam=self.cam, contact=dict(width=1.2, depth=0.5, opacity=0.7))

    # ---- runtime props (metres under the scaled root)
    @staticmethod
    def sig_centre(objs):
        lo, hi = [9e9] * 2, [-9e9] * 2
        for ob in objs:
            for v in ob.data.vertices:
                lo = [min(lo[0], v.co.x), min(lo[1], v.co.y)]
                hi = [max(hi[0], v.co.x), max(hi[1], v.co.y)]
        return Vector(((lo[0] + hi[0]) / 2.0, (lo[1] + hi[1]) / 2.0, SHEET_Z))

    def build_hands(self, M):
        d = self.D_SHAFT
        mb = CO.MB("rq_quill", parent=CO.root())
        mb.rod(M["i_feather"], (0, 0, 0), d * 0.26, 0.0032, 0.002, 6, smooth=True)
        mb.ell(M["i_feather"], d * 0.20, (0.012, 0.016, 0.085), (10, 6), (0.25, 0.35, 0.0))
        mb.cyl(M["i_ink"], (0, 0, 0.004), 0.0035, 0.008, "z", 6)
        self.quill = mb.finish()
        self.out = {"A": Vector((-0.92, 0.22, 0.34)).normalized(), "B": Vector((0.92, 0.20, 0.36)).normalized()}
        self.hand = {}
        for key, sleeve in (("A", M["cream"]), ("B", M["d_plum"])):
            out = self.out[key]
            h = CO.MB("rq_hand" + key, parent=CO.root())
            h.ell(M["i_skin"], (0, 0, 0), (0.013, 0.012, 0.015), (10, 8))
            h.ell(M["i_skin"], out * 0.025 + Vector((0, 0, 0.012)), (0.010, 0.010, 0.010), (8, 6))
            h.rod(sleeve, out * 0.04, out * 0.75, 0.016, 0.030, 12, smooth=True)
            h.rod(M["white"], out * 0.04, out * 0.075, 0.018, 0.018, 12)
            self.hand[key] = h.finish()

    def build_heading(self, M):
        """"PROTESTATION" (Latin) printed on the sheet's header band: a FONT curve lying flat on the paper"""
        T1 = Vector(self.A["marks"]["table_t1"]) / CO.SC
        cu = bpy.data.curves.new("protest_head", "FONT")
        cu.body = "PROTESTATION"
        cu.size = 0.042
        cu.align_x = "CENTER"
        cu.extrude = 0.0006
        ob = bpy.data.objects.new("protest_head", cu)
        bpy.context.scene.collection.objects.link(ob)
        ob.parent = CO.root()
        ob.location = (-0.5 + 0.02 - 0.02, 3.4 + 0.04 + 0.30, SHEET_Z + 0.002)
        ob.rotation_euler = (0, 0, 0.12)
        ob.data.materials.append(M["i_ink"])
        ob.visible_shadow = False
        self.heading = ob

    def nib(self, g):
        S1, S2 = self.S1, self.S2
        hover = Vector((0, 0, 0.09))
        if g < LAND1 - 6:
            p = (S1 + Vector((0.16, 0.10, 0.07))) + (S1 + hover - (S1 + Vector((0.16, 0.10, 0.07)))) * smooth(u_of(g, GA + 60, LAND1 - 6))
        elif g < LAND1:
            p = S1 + hover * (1 - smooth(u_of(g, LAND1 - 6, LAND1)))
        elif g < LAND1 + 7:
            t = (g - LAND1) / 7.0
            p = S1 + Vector((0.07 * t + 0.012 * math.sin(t * 18), 0.012 * math.cos(t * 14), 0.0))
        elif g < PASS[0]:
            end = S1 + Vector((0.07, 0.0, 0.0))
            tgt = Vector((end.x + 0.07, end.y + 0.07, SHEET_Z + 0.045))
            p = end + (tgt - end) * smooth(u_of(g, LAND1 + 7, PASS[0]))
        elif g < LAND2 - 6:
            end = Vector((S1.x + 0.14, S1.y + 0.07, SHEET_Z + 0.045))
            p = end + (S2 + hover - end) * smooth(u_of(g, PASS[0], LAND2 - 6))
        elif g < LAND2:
            p = S2 + hover * (1 - smooth(u_of(g, LAND2 - 6, LAND2)))
        else:
            t = min(1.0, (g - LAND2) / 8.0)
            p = S2 + Vector((0.06 * t + 0.012 * math.sin(t * 18), 0.012 * math.cos(t * 14), 0.0))
            if g > LAND2 + 8:
                p = p + Vector((0.01, 0.0, 0.07 * smooth((g - LAND2 - 8) / 12.0)))
        return p

    def hands_at(self, g):
        p = self.nib(g)
        d = self.D_SHAFT
        gA, gB = p + d * 0.06, p + d * 0.11
        far = 0.5
        if g < PASS[0]:
            return {"A": gA, "B": gB + self.out["B"] * far * 1.5}
        if g < PASS[1]:
            u = smooth((g - PASS[0]) / float(PASS[1] - PASS[0]))
            return {"A": gA + self.out["A"] * far * u, "B": gB + self.out["B"] * far * 1.5 * (1 - min(1.0, u * 2.0))}
        return {"A": gA + self.out["A"] * far * 1.2, "B": p + d * 0.06}

    def hands_visible(self, g):
        return 452 <= g <= 520

    def smoke_v(self, g):
        return clamp((g - RAMP0) / float(G_CHIM - RAMP0))

    def pose(self, gs):
        M = self.A["marks"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g))
            for k, cast in ART:
                self.actors[k].place(f, (SPOT[k][0], SPOT[k][1], M["artist_1"][2]), scale=1.0, flip=YAW[k] < 0)
            self.actors["mau"].place(f, (M["maupassant"][0], M["maupassant_seat"][1], M["maupassant"][2]), scale=1.0)
            self.actors["wtr"].place(f, (SPOT["wtr"][0], SPOT["wtr"][1], M["waiter"][2]), scale=1.0, flip=True)
            n = N0 + (1 if g >= LAND1 else 0) + (1 if g >= LAND2 else 0)
            self.key_set(f, set_window_view=("stub",), smoke=(self.smoke_v(g),), add_signature=(n,))
            vis = self.hands_visible(g)
            p = self.nib(g) if vis else Vector((0, 0, -5))
            for ob in self.quill:
                ob.location = p
                CO.key(ob, "location", f)
            hp = self.hands_at(g) if vis else {"A": Vector((0, 0, -5)), "B": Vector((0, 0, -5))}
            for kk, obs in self.hand.items():
                for ob in obs:
                    ob.location = hp[kk]
                    CO.key(ob, "location", f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, cast in ART:
                self.actors[k].pose(f, pose_of(k, cast, g), camera=self.cam)
            mp = dict(cast20.STORY20["maupassant_seated_toast_smug"][1])      # he sits on the banquette the whole take (rises in T09); mouth held ('smile')
            mp["seat_h"] = float(M["maupassant_seat"][2]); mp["t"] = g / 30.0
            mp["lean"] = 1.2 * math.sin(g * 0.11); mp["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.25))
            mp["arm_r"] = dict(mp["arm_r"], hand=(0.74, 0.34 + 0.12 * (1 - smooth((g - 585) / 12.0)) * (0.5 + 0.5 * math.sin(g * 0.09))))      # sips: the glass rises and falls
            self.actors["mau"].pose(f, mp, camera=self.cam)
            w = dict(cast20.STORY20["waiter_idle"][1]); w["t"] = g / 30.0; w["lean"] = 2.5 * math.sin(g * 0.13); w["head_roll"] = 3 * math.sin(g * 0.09)
            self.actors["wtr"].pose(f, w, camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    smoke=round(self.smoke_v(g), 3), heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows = [(g, round(corner_speed(g), 2)) for g in GS[:-1]]
        print([r for r in rows[::6]])
        run = worst = 0
        for g, px in rows:
            run = run + 1 if px < 0.25 else 0
            worst = max(worst, run)
        print("longest run under 0.25 px/frame: %d (max 6); min speed %.2f max %.2f" % (worst, min(p for _, p in rows), max(p for _, p in rows)))
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= G_LAST]
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
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
