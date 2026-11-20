#!/usr/bin/env python3
"""shot.py -- film 20 take s07 = shot 7, CAFE cafe_table_insert (1887).  Insert on the protest sheet on the marble table: scribbled signatures (no text),
a quill passes from the painter's sleeve to the poet's sleeve, two more signatures land.
Shot 7 = g 466..512 (15.53-17.10 s); cut in (4-frame handle g 462..465), cut out at 513 (out-handle g 513..516).  Whole take g 462..516 (55 frames).
Hands / sleeves / quill are runtime meshes (core20.MB under the set's scaled root, authored in metres), keyed on every rendered frame.
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples] | camreport
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, ez, u_of, bf = C.lerp, C.clamp, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(15.53), C.g_bound(17.10)       # 466, 513
H_IN, H_OUT = 4, 4
GA, G_LAST = G0 - H_IN, G1 + H_OUT - 1             # 462 .. 516
GS = list(range(GA, G_LAST + 1))
G_SIGN = C.cap_g("ลงชื่อประท้วง")                  # 469: "sign in protest" -> the first signature lands
G_PAPER = C.cap_g("ในหนังสือพิมพ์")                 # 491: "in the newspaper" -> the second lands
LAND1, LAND2 = G_SIGN + 2, G_PAPER + 5             # 471, 496
PASS = (G_SIGN + 14, G_SIGN + 25)                  # 483..494: the quill is handed over (A lets go, B takes it)
LIGHT, PRESET = "DAY", "cafe_table_insert"
N0 = 14                                            # signatures on the sheet when the shot opens (of 24)
SHEET_Z = 0.772                                    # metres: sheet top (table top 0.768 + paper)


def cam_path(A):
    c = Vector(A["cams"][PRESET]["loc"])
    subj = Vector(A["marks"]["protest_sheet"]) + Vector((0.05, 0.0, 0.0))
    return C.CamPath(c, subj, GA, G_LAST, push=0.14, slide_px=float(os.environ.get("SLIDE", "75")), rise_px=0.0, arc_deg_s=12.0,
                     tilt0=float(os.environ.get("TILT", "0")), tilt_deg_s=0.0, decay=0.25,
                     snaps=[dict(g=(LAND1 - 3, LAND1 + 9), k=1.45, peak=1.7, shift=(0.0, 0.0), tilt=0.0)])


def cam_path_static():
    import int20
    cm = int20.CAFE_CAMS_M[PRESET]
    return cam_path(dict(cams={PRESET: dict(loc=CO.W(cm[0]))}, marks={"protest_sheet": (-0.902, 6.467, 1.438)}))


def sig_centre(objs):
    """local (metre) bbox centre of the signature objects (they are authored in the root's metres, identity transform)"""
    lo, hi = [9e9] * 2, [-9e9] * 2
    for ob in objs:
        for v in ob.data.vertices:
            lo = [min(lo[0], v.co.x), min(lo[1], v.co.y)]
            hi = [max(hi[0], v.co.x), max(hi[1], v.co.y)]
    return Vector(((lo[0] + hi[0]) / 2.0, (lo[1] + hi[1]) / 2.0, SHEET_Z))


def smooth(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


class Take(C.Take):
    D_SHAFT = Vector((0.5, 0.5, 0.72)).normalized()     # quill shaft direction from the nib (up, toward the lens, a little right)

    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s07")
        self.path = cam_path(self.A)
        CO.setup_grade(self.scene, dict(sat=float(os.environ.get("SAT", "1.90"))))      # SAT_GRADE: film-wide saturation >= 0.47 (QA_TEAM §G)
        self.key_cam(bf(GA), *self.path.at(GA))
        self.scene.frame_set(bf(GA))
        M = CO.STATE["M"]
        sigs = CO.STATE["sigs"]
        self.S1, self.S2 = sig_centre(sigs[N0]), sig_centre(sigs[N0 + 1])
        d = self.D_SHAFT
        # quill (origin = nib): shaft 0.26 m + feather vane; feather material i_feather, nib i_ink
        mb = CO.MB("rq_quill", parent=CO.root())
        mb.rod(M["i_feather"], (0, 0, 0), d * 0.26, 0.0032, 0.002, 6, smooth=True)
        mb.ell(M["i_feather"], d * 0.20 + Vector((0, 0, 0.0)), (0.012, 0.016, 0.085), (10, 6), (0.25, 0.35, 0.0))
        mb.cyl(M["i_ink"], (0, 0, 0.004), 0.0035, 0.008, "z", 6)
        self.quill = mb.finish()
        # hands: origin = grip point; hand = skin ellipsoid + 2 knuckle balls, sleeve = tapered rod from the wrist backwards, cuff ring
        self.hand = {}
        for key, sleeve, cuff, out in (("A", M["cream"], M["white"], Vector((-0.92, 0.22, 0.34)).normalized()),
                                       ("B", M["d_plum"], M["white"], Vector((0.92, 0.20, 0.36)).normalized())):
            h = CO.MB("rq_hand" + key, parent=CO.root())
            h.ell(M["i_skin"], (0, 0, 0), (0.013, 0.012, 0.015), (10, 8))
            h.ell(M["i_skin"], out * 0.025 + Vector((0, 0, 0.012)), (0.010, 0.010, 0.010), (8, 6))
            h.rod(sleeve, out * 0.04, out * 0.75, 0.016, 0.030, 12, smooth=True)
            h.rod(cuff, out * 0.04, out * 0.075, 0.018, 0.018, 12)
            self.hand[key] = h.finish()
        self.out = {"A": Vector((-0.92, 0.22, 0.34)).normalized(), "B": Vector((0.92, 0.20, 0.36)).normalized()}

    def nib(self, g):
        """nib position (metres) of frame g"""
        S1, S2 = self.S1, self.S2
        hover = Vector((0, 0, 0.09))
        a0 = S1 + Vector((0.16, 0.10, 0.07))                       # the nib hovers up-right of the first signature
        if g < LAND1 - 6:
            u = u_of(g, GA, LAND1 - 6)
            p = a0 + (S1 + hover - a0) * smooth(u)
        elif g < LAND1:
            u = u_of(g, LAND1 - 6, LAND1)
            p = S1 + hover * (1 - smooth(u))
        elif g < LAND1 + 7:                                         # scribbles the signature
            t = (g - LAND1) / 7.0
            p = S1 + Vector((0.07 * t + 0.012 * math.sin(t * 18), 0.012 * math.cos(t * 14), 0.0))
        elif g < PASS[0]:
            u = u_of(g, LAND1 + 7, PASS[0])
            end = S1 + Vector((0.07, 0.0, 0.0))
            tgt = Vector((end.x + 0.07, end.y + 0.07, SHEET_Z + 0.045))
            p = end + (tgt - end) * smooth(u)
        elif g < LAND2 - 6:
            u = u_of(g, PASS[0], LAND2 - 6)
            end = Vector((S1.x + 0.14, S1.y + 0.07, SHEET_Z + 0.045))
            tgt = S2 + hover
            p = end + (tgt - end) * smooth(u)
        elif g < LAND2:
            u = u_of(g, LAND2 - 6, LAND2)
            p = S2 + hover * (1 - smooth(u))
        else:
            t = min(1.0, (g - LAND2) / 8.0)
            p = S2 + Vector((0.06 * t + 0.012 * math.sin(t * 18), 0.012 * math.cos(t * 14), 0.0))
            if g > LAND2 + 8:                                        # lifts slowly again
                p = p + Vector((0.01, 0.0, 0.07 * smooth((g - LAND2 - 8) / 12.0)))
        return p

    def hands_at(self, g):
        """grip points of hand A / B (None = out of frame) for frame g"""
        p = self.nib(g)
        d = self.D_SHAFT
        gA, gB = p + d * 0.06, p + d * 0.11
        far = 0.5
        if g < PASS[0]:
            return {"A": gA, "B": gB + self.out["B"] * far * 1.5}
        if g < PASS[1]:
            u = smooth((g - PASS[0]) / float(PASS[1] - PASS[0]))
            # B comes in and takes the top of the shaft, A lets go and retreats
            return {"A": gA + self.out["A"] * far * u, "B": (gB + self.out["B"] * far * 1.5 * (1 - min(1.0, u * 2.0))) if True else gB}
        return {"A": gA + self.out["A"] * far * 1.2, "B": p + d * 0.06}

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            n = N0 + (1 if g >= LAND1 else 0) + (1 if g >= LAND2 else 0)
            self.key_set(f, set_window_view=("stub",), smoke=(0.0,), add_signature=(n,))
            p = self.nib(g)
            for ob in self.quill:
                ob.location = p
                CO.key(ob, "location", f)
            hp = self.hands_at(g)
            for k, obs in self.hand.items():
                for ob in obs:
                    ob.location = hp[k]
                    CO.key(ob, "location", f)

    def report(self, g):
        loc, look = self.path.at(g)
        v = look - loc
        p = self.nib(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    nib=[round(c, 3) for c in p], heads={})

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = cam_path_static().report(GS[:-1])
        for r in rows[::4]:
            print(r)
        print("longest run under 0.25 px/frame: %d" % worst)
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
