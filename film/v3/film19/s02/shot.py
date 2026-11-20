#!/usr/bin/env python3
"""shot.py -- film 19 take s02 = the BIGZOOM (shots 2 + 3 merged, QA_TEAM section H).  g 57..190 (1.91-6.37 s, 134 frames) + 9 handle frames each side
(hard cut in from s01 at g 57; DISSOLVE 13 f out into s04 at g 191): g 48..199.

ONE continuous eased camera move, no cut.  SHIP ship_aerial / NOON (set_sea + set_roll keyed on every frame):
  START  extreme wide from high above and behind: the lone warship on the endless glittering sea, small in the frame; captain19 and astro19_c on the
         quarterdeck are ~6 px tall (under 5 % of the frame), findable
  MIDDLE the camera descends and pushes in toward the stern, passing the spanker sail (a fore-and-aft sail, 1.8 D from the lens) as a parallax foreground
  END    (by ~5.9 s, g 177) a MEDIUM shot on the quarterdeck: captain19 holds a blank sea chart, astro19_c squints through a quadrant at the sky and
         scratches his head (g ~150-165); 35-60 % of the frame height; the camera rides the deck (C.on_ship)
No mouth movement.  NO depth of field, NO text, NO caption_shade.

    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
    python3 deliver.py [draft]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402

H, K, cast19 = C.H, C.K, C.cast19
lerp, clamp, blink, u_of, bf = C.lerp, C.clamp, C.blink, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
TAKE = "s02"
PRESET, LIGHT = "ship_aerial", "NOON"
G0, G1 = 57, 191                                         # shot = g 57..190
H_IN, H_OUT = 9, 9
FIRST_G, G_LAST = G0 - H_IN, G1 + H_OUT - 1              # 48..199
GS = list(range(FIRST_G, G_LAST + 1))
FINAL_SPP = 10
S = 1.85
PPD = 224                                                # sprite px per D (head ~110 px at the end; the start is downsampled)
G_ARRIVE = 152                                           # the medium shot is reached (5.9 s)
G_SCRATCH = (146, 166)       # head scratch; 150-186 the whole puzzled beat                                   # astro19_c scratches his head (comic), 4.9-5.5 s
BLINKS_C, BLINKS_A = [70, 128, 171], [92, 150, 188]

# ----------------------------------------------------------------------------- staging (ship rest frame = world D at t = 0; z of the quarterdeck 14.34)
Z_QD = 14.34 + 0.22                                        # the deck plus the shoe sole (the card base sat 0.2 D low)
CAP_XY = (-0.75, -31.3)                                  # captain19, beside the wheel, camera-left
AST_XY = (1.7, -30.6)                                   # astro19_c, camera-right (short: 2.8 D)

# ----------------------------------------------------------------------------- camera: a spline through key poses in the SHIP's rest frame (D), eased in and out
KEYS = [  # (u, loc, look)
    (0.00, (30.0, -530.0, 395.0), (0.0, -14.0, 14.0)),            # truly extreme wide: ~640 D away, the ship <= 12 % of the frame height, the crew ~4 px
    (0.50, (13.0, -125.0, 96.0), (1.0, -30.0, 15.0)),             # descending
    (0.76, (5.0, -52.0, 46.0), (0.8, -30.5, 16.0)),               # high over the stern, level with the mizzen yards / sails
    (0.91, (1.9, -40.5, 31.0), (0.6, -30.3, 16.0)),               # passes the spanker sail at ~1.9 D and the rigging, then dives
    (1.00, (0.45, -36.3, 16.5), (0.5, -30.0, 15.9)),              # medium on the quarterdeck
]


def _cr(p0, p1, p2, p3, t):
    """Catmull-Rom, uniform"""
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t)


def _spline(g, which):
    """position on the key spline at the eased parameter u(g) (which 1 = loc, 2 = look)"""
    # g -> u: a slow-ish wide start, a fast descent through the stern (the smooth planks / sail frames the blur check punishes), then it SETTLES on the medium
    TM = [(48, 0.0), (66, 0.10), (90, 0.35), (115, 0.70), (135, 0.92), (G_ARRIVE, 1.0)]
    j = max(i for i in range(len(TM) - 1) if TM[i][0] <= g) if g < TM[-1][0] else len(TM) - 2
    (g0_, u0_), (g1_, u1_) = TM[j], TM[j + 1]
    x = clamp((g - g0_) / float(g1_ - g0_))
    sm = x * x * (3 - 2 * x)
    u = u0_ + (u1_ - u0_) * (0.55 * sm + 0.45 * x)                         # eased between the knots, never zero speed
    P = [Vector(k[which]) for k in KEYS]
    us = [k[0] for k in KEYS]
    j = max(i for i in range(len(us) - 1) if us[i] <= u) if u < 1.0 else len(us) - 2
    tt = (u - us[j]) / (us[j + 1] - us[j])
    p0 = P[j - 1] if j > 0 else P[j] * 2 - P[j + 1]
    p3 = P[j + 2] if j + 2 < len(P) else P[j + 1] * 2 - P[j]
    return Vector([_cr(p0[i], P[j][i], P[j + 1][i], p3[i], tt) for i in range(3)])


def cam_rest(g):
    """(loc, look) in the ship's rest frame at film frame g.  After arrival: a slow push so the shot never parks."""
    loc, look = _spline(min(g, G_ARRIVE), 1), _spline(min(g, G_ARRIVE), 2)
    if g > G_ARRIVE:
        # settle on the medium: a slow orbit about the pair (parallax against the rigging) plus a gentle push, so the long hold keeps moving
        d = clamp((g - G_ARRIVE) / 50.0)
        ang = math.radians(17.0) * d * d * (3 - 2 * d)
        c = Vector((0.5, -30.5, loc.z))
        loc = c + Matrix.Rotation(ang, 3, "Z") @ (loc - c)
        loc = loc + (look - loc) * (0.0030 * (g - G_ARRIVE))
    look = look + Vector((0.0, 0.0, 0.30 * clamp((g - 124) / 26.0)))      # aim a little higher so the heads sit at y 450-760 (the camera still rides the deck)
    return loc, look


# ----------------------------------------------------------------------------- the sea (ONE camera-fitted grid): fit it to a virtual camera far above and behind
def widen_sea(preset, nu, nv):
    import h19_ship as SH
    P = SH.PRESETS[preset]
    look = Vector(P["cam"]["look"])
    P["cam"] = dict(P["cam"], loc=tuple(Vector((14.0, -330.0, 255.0)) * 3.0 / S))   # metres: a virtual camera 3x as far / high as the start pose
    P["sea_nu"], P["sea_nv"] = nu, nv
    P["foam_k"] = float(os.environ.get("FOAMK", "0.55"))                # a calmer wake: less white lace (it dominated the frame statistics)


# ----------------------------------------------------------------------------- the BLANK chart (QA-art: no coastline, no compass, no red mark: "nobody knows where we are")
def _blank_chart_body(k):
    """the unrolled sea chart of cast19.chart19, but BLANK: parchment with a fold crease and a worn edge, nothing drawn on it (no text, no coast, no compass)."""
    g = cast19._g3(k, "ch", cast19.PARCH, 0, 0, 0.74, 0)
    o = ['<path d="M0,-0.26 L0.74,-0.26 L0.74,0.26 L0,0.26 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M0.37,-0.25 L0.37,0.25" stroke="%s" stroke-width="0.006" opacity="0.18"/>' % k.ink)          # the fold
    o.append('<path d="M0.03,-0.02 L0.71,-0.02" stroke="%s" stroke-width="0.005" opacity="0.10"/>' % k.ink)
    return "".join(o)


cast19._chart_body = _blank_chart_body                        # the prop drawer looks it up at call time


# ----------------------------------------------------------------------------- poses
def _ramp(g, a, b):
    return u_of(g, a, b)


def pose_captain(g):
    """captain19: peers at the blank chart; from g 150 he lifts it, turns it round (upside down), brows up, looks at astro19_c and shrugs"""
    p = dict(cast19.STORY19["captain_peer_chart"][1])
    p["lean"] = 8 + 2.0 * math.sin(g * 0.13)
    p["head_roll"] = 4.0 * math.sin(g * 0.09)
    p["blink"] = blink(g, BLINKS_C)
    p["pitch"] = 0.35 + 0.08 * math.sin(g * 0.17)
    p["arm_r"] = dict(hand=(0.6, 0.96 + 0.05 * math.sin(g * 0.2)), bend=0.3, layer="front")
    p["arm_l"] = dict(hand=(1.3, 1.0 + 0.04 * math.sin(g * 0.23 + 1)), bend=0.0, stretch=1.3, layer="front")
    # 150-164: lifts the chart and TURNS it (the hands swing round), brows up, 164-172: looks at astro19_c, 172-186: shrug
    lift = _ramp(g, 148, 158) * (1.0 - _ramp(g, 166, 176))
    if lift > 0.0:
        sw = math.sin((g - 150) * 0.55) * (1.0 if g < 166 else 0.3)             # the chart is turned over: a rocking wrist
        p["arm_r"] = dict(hand=(lerp(0.6, 0.45, lift), lerp(0.96, 1.7, lift) + 0.12 * sw), bend=lerp(0.3, 0.9, lift), layer="front")
        p["arm_l"] = dict(hand=(lerp(1.3, 1.0, lift), lerp(1.0, 1.85, lift) - 0.12 * sw), bend=0.2, stretch=1.2, layer="front")
        p["pitch"] = lerp(0.35, -0.05, lift)
        p["head_roll"] = -9.0 * lift + 3.0 * sw
    wor = _ramp(g, 150, 156)
    if wor > 0.0:
        p["expr"] = "worried"                                                  # brows up
    look = _ramp(g, 164, 170)
    if look > 0.0:
        p["gaze"] = (lerp(0.8, 1.0, look), lerp(0.9, 0.0, look))               # at astro19_c (screen-right)
    shrug = _ramp(g, 172, 180)
    if shrug > 0.0:
        p["arm_r"] = dict(hand=(lerp(0.45, 1.05, shrug), lerp(1.2, 0.75, shrug)), bend=lerp(0.6, -0.2, shrug), shape="open", layer="front")
        p["arm_l"] = dict(hand=(lerp(1.0, -0.15, shrug), lerp(1.4, 0.85, shrug)), bend=lerp(0.2, 0.6, shrug), shape="open", stretch=1.0, layer="front")
        p["prop_r"] = None if shrug > 0.5 else p.get("prop_r")                   # the chart is dropped to the deck hand (chart held low) as he shrugs
        p["head_roll"] = lerp(-9.0 * 0.0, 7.0, shrug) + 2.0 * math.sin(g * 0.8)
        p["lean"] = 8 - 10.0 * shrug
        p["pitch"] = lerp(0.1, 0.15, shrug)
    p["t"] = g / 30.0
    p = {k: v for k, v in p.items() if v is not None}
    return p


def pose_astro(g):
    """astro19_c: squints through the quadrant at the sky; g 148-164 an OBVIOUS head-scratch; 164-172 looks at the captain; 172-186 shrugs, palms up"""
    p = dict(cast19.STORY19["william_quadrant_sun"][1])                    # arms / prop of the quadrant pose
    p["expr"] = "squint"
    p["blink"] = blink(g, BLINKS_A)
    p["lean"] = -3 + 1.2 * math.sin(g * 0.15)
    p["head_roll"] = 3.0 * math.sin(g * 0.11 + 1.0)
    p["glint"] = 0.5 + 0.5 * math.sin(g * 0.2)
    scr = _ramp(g, 146, 152) * (1.0 - _ramp(g, 164, 168))
    if scr > 0.0:
        w = math.sin(g * 1.35)                                                 # the scratching wobble
        p["arm_r"] = dict(hand=(lerp(0.46, 0.5, scr), lerp(0.1, 0.5, scr)), bend=lerp(-0.7, 0.5, scr), stretch=1.1, layer="top")
        p["prop_r"] = dict(type="quadrant19", angle=lerp(-62, -8, scr), scale=0.95)
        p["arm_l"] = dict(hand=(lerp(-0.46, -0.10 + 0.10 * w, scr), lerp(0.96, 2.3 + 0.12 * w, scr)), bend=lerp(0.5, 1.0, scr), shape="open")
        p["pitch"] = lerp(-0.75, 0.2, scr)
        p["expr"] = "unimpressed" if scr > 0.4 else "squint"
        p["head_roll"] = 9.0 * scr * math.sin(g * 1.35 + 0.7)
        p["gaze"] = (0.2, 0.3)
        p["glint"] = 0.0
    look = _ramp(g, 164, 170)
    if look > 0.0:
        p["pitch"] = lerp(p.get("pitch", -0.75), 0.15, look)
        p["gaze"] = (lerp(0.2, -1.0, look), 0.0)                              # at the captain (screen-left; the card is mirrored)
        p["expr"] = "worried" if look > 0.5 else p["expr"]
    shrug = _ramp(g, 172, 180)
    if shrug > 0.0:
        p["arm_r"] = dict(hand=(lerp(0.5, 0.95, shrug), lerp(0.5, 0.7, shrug)), bend=lerp(0.5, -0.2, shrug), shape="open", stretch=1.0, layer="top")
        p["arm_l"] = dict(hand=(lerp(-0.1, -0.9, shrug), lerp(2.2, 0.75, shrug)), bend=lerp(1.0, 0.4, shrug), shape="open")
        p["prop_r"] = None                                                     # the quadrant is lowered / dropped into the free hand
        p["head_roll"] = lerp(0.0, -8.0, shrug)
        p["lean"] = lerp(-3, -8, shrug)
        p["pitch"] = 0.1
    p["t"] = g / 30.0
    p = {k: v for k, v in p.items() if v is not None}
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        widen_sea(PRESET, int(os.environ.get("NU", "1500")), int(os.environ.get("NV", "2000")))
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_" + TAKE)
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        root = self.A["ship_root"]
        self.cap = self.actors["cap"] = C.make_actor("cap", "captain19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.ast = self.actors["ast"] = C.make_actor("ast", "astro19_c", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        for a in (self.cap, self.ast):
            C.ride_ship(a, root)                                           # BEFORE place() and BEFORE any set_roll key: the inverse is taken at rest
        self.cam_pose(FIRST_G, root)

    def cam_pose(self, g, root):
        f = bf(g)
        self.key_set(f, sea=g / 30.0, roll=g / 30.0)                       # same t on every frame
        loc, look = cam_rest(g)
        self.key_cam(f, *C.on_ship(root, f, loc, look))                    # the camera rides the deck (rest-frame pose -> world)

    def pose(self, gs):
        root = self.A["ship_root"]
        for g in gs:
            f = bf(g)
            self.cam_pose(g, root)
            C.key_vis([o for o in (C.bpy.data.objects.get("gulls_gullt"), C.bpy.data.objects.get("gulls_gullw")) if o], False, f)
            C.place(self.cap, f, (CAP_XY[0], CAP_XY[1], Z_QD))
            C.place(self.ast, f, (AST_XY[0], AST_XY[1], Z_QD))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.cap.pose(f, pose_captain(g), camera=self.cam)
            pa = pose_astro(g)
            pa["mirror"] = True
            self.ast.pose(f, pa, camera=self.cam)
        self.sprites_for([(self.cap, PPD), (self.ast, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_rest(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def camreport():
    prev = None
    mx = 0
    for g in GS:
        loc, look = cam_rest(g)
        if prev is not None:
            d = (loc - prev).length
            mx = max(mx, d)
        if g % 12 == 0:
            print(g, [round(c, 1) for c in loc], [round(c, 1) for c in look])
        prev = loc


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        camreport()
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if FIRST_G <= g <= G_LAST]
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
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else FINAL_SPP
        quality = "final" if scale >= 1.0 else "preview"
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
