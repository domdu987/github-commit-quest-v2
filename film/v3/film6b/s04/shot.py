#!/usr/bin/env python3
"""shot.py -- film 6b take s04: shots 4-7 (plan 4.10-10.48 s = g 123..313) + 6 handle frames each side (g 117..122, 314..319),
market AFTERNOON (warm gold sun vs blue shade).

    shot 4  g 123..179  crane down from the sky over the medieval market (in-handle g 117..122 = the crane a little higher): rooftops,
                        bunting, the pillory and the big balance, townsfolk crossing the square ("อังกฤษยุคนั้น" 4.91 s).
    shot 5  g 180..227  CU the other baker (baker2) beside the big public balance with his 12 loaves: the beam tips to the weights side
                        (g 190-200, short weight), he goes from worried to shocked + sweat; a Thai sign "ขาดน้ำหนัก!" drops in and
                        swings on the pan chain (g 203-209; caption "ขาดน้ำหนัก" 6.91 s = g 210).  Push in.
    shot 6  g 228..272  low push on the pillory: baker2 locked in, struggling; a guard with a spear; sign on the post
                        "ห้ามขายขาดน้ำหนัก!" ("โดนจับใส่" 7.62 s, "ขื่อกลางตลาด" 8.29 s).
    shot 7  g 273..313  CU baker2 in the pillory (+ out-handle g 314..319): a townswoman raises a rotten tomato (g 273-283), throws
                        (g 284), it flies in and SPLATS on his face (g 296, tomato_svg squash 1, "เน่าใส่" 9.90 s); he flinches;
                        a farmer in the foreground laughs.
Mouths: no quote in s04 -> static expression mouths only.  NO depth of field (C.Take).

    python3 shot.py probe 4,5,6,7 a:b[:step]
    python3 shot.py stills 4,5,6,7 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 4,5,6,7 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "film6"))     # v3/film6/common.py (read-only reuse)
import common as C                                       # noqa: E402
import lib6b as L                                        # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G4, G5, G6, G7, GE = 123, 180, 228, 273, 314
H = 6
RANGES = {4: (G4 - H, G5 - 1), 5: (G5, G6 - 1), 6: (G6, G7 - 1), 7: (G7, GE + H - 1)}
TIP = (190, 200)                   # big balance tips to the weights side
SIGN_DROP = (203, 209)
THROW = 284
SPLAT = 296

# ----------------------------------------------------------------------------- staging (market world D)
BAKER_SCALE = (1.55, 5.55)         # baker2 beside the bread pan (pan centre (3, 6), r 1.05)
PIL_FEET = (-4.0, 9.42, 1.05)      # pilloried baker2: card just in front of the 3D board, its drawn board on the 3D one
FACE = Vector((-4.0, 9.30, 3.75))  # his face (splat target), a little in front of his card
GUARD_PIL = (-5.75, 9.0, 1.0)
WOMAN_THROW = (-2.35, 7.35)
MAN_LAUGH = (-5.55, 7.15)
LENS = 22.0


def cam_shot(shot, g):
    if shot == 4:
        u = ez((g - (G4 - H)) / float(G5 - (G4 - H)), "sine")
        loc = lerp((4.0, -13.0, 24.0), (8.5, -9.5, 8.0), u)
        look = lerp((-1.0, 9.0, 21.0), (-0.5, 7.0, 2.6), ez(u * 1.05, "sine"))
        return Vector(loc), Vector(look), LENS
    if shot == 5:
        u = ez((g - G5) / float(G6 - G5), "sine")
        loc = lerp((0.55, 2.55, 2.85), (0.85, 3.05, 2.80), u)
        look = lerp((2.45, 5.85, 2.45), (2.40, 5.85, 2.48), u)
        return Vector(loc), Vector(look), 24.0
    if shot == 6:
        u = ez((g - G6) / float(G7 - G6), "sine")
        loc = lerp((-1.5, 4.2, 1.15), (-2.65, 6.0, 1.75), u)
        look = lerp((-4.0, 9.5, 3.15), (-4.0, 9.5, 3.30), u)
        return Vector(loc), Vector(look), LENS
    u = ez((g - G7) / float(GE + H - G7), "sine")
    loc = lerp((-3.05, 6.55, 3.55), (-3.25, 6.95, 3.60), u)
    look = lerp((-4.0, 9.5, 3.45), (-4.0, 9.5, 3.50), u)
    if g >= SPLAT:                                        # impact jolt
        k = max(0.0, 1.0 - (g - SPLAT) / 6.0)
        loc = (loc[0] + 0.04 * k * math.sin(g * 2.7), loc[1], loc[2] + 0.03 * k * math.cos(g * 3.1))
    return Vector(loc), Vector(look), 24.0


# ----------------------------------------------------------------------------- poses
def baker_scale_pose(g):
    u = ez((g - TIP[0]) / float(TIP[1] - TIP[0]))
    p = dict(yaw=0.40, pitch=0.25, expr="worried", head_roll=-4, gaze=(0.85, 0.55), lean=4,
             arm_l=dict(hand=(-0.10, 0.70), bend=0.6), arm_r=dict(hand=(0.80, 0.35), bend=-0.4, shape="open", stretch=1.2),
             legs="stand", t=g / 30.0)
    if g >= TIP[0] + 4:
        p.update(expr="shocked", fx=["sweat"], yaw=lerp(0.40, 0.05, u), pitch=lerp(0.25, -0.15, u), gaze=(lerp(0.85, 0.2, u), 0.0),
                 head_roll=lerp(-4, 6, u), squash=(0.97, 1.04),
                 arm_l=dict(hand=(-0.62, -0.20), bend=-0.6, shape="open", stretch=1.2),
                 arm_r=dict(hand=(0.66, -0.25), bend=0.6, shape="open", stretch=1.2))
    p["blink"] = blink(g, [184, 222])
    return p


def baker_pillory_pose(g, shot):
    _, base = cast6.STORY6["baker2_pillory"]
    p = dict(base)
    p["t"] = g / 30.0
    p["head_roll"] = -6 + 7 * math.sin(g * 0.55)              # struggling in the board
    p["yaw"] = 0.12 * math.sin(g * 0.31)
    p["fx"] = ["sweat"]
    if shot == 7 and g >= SPLAT:
        _, fl = cast6.STORY6["baker2_pillory_flinch"]
        p = dict(fl); p["t"] = g / 30.0
        p["mouth"] = None
        k = max(0.0, 1.0 - (g - SPLAT) / 10.0)
        p["head_roll"] = 10 + 8 * k * math.sin((g - SPLAT) * 1.6)
        p["blink"] = 2 if g < SPLAT + 8 else blink(g, [316])
        p["expr"] = "shocked" if g < SPLAT + 8 else "sad"
        p["fx"] = ["sweat"]
        return p
    if shot == 7:
        p["expr"] = "worried"
        p["gaze"] = (0.8, 0.2) if g >= THROW - 6 else (0.0, 0.3)
        p["yaw"] = 0.15 if g >= THROW - 6 else p["yaw"]
    p["blink"] = blink(g, [236, 262, 280])
    return p


def woman_pose(g):
    if g < THROW:
        _, p = cast6.STORY6["town_raise_veg"]
        p = dict(p); p["prop_r"] = "tomato"; p["mouth"] = None
        p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = (0.66 - 0.10 * ez((g - 276) / 6.0), -0.74 - 0.10 * ez((g - 276) / 6.0))
    elif g < THROW + 8:
        _, p = cast6.STORY6["town_throw"]; p = dict(p); p["mouth"] = None
    else:
        _, p = cast6.STORY6["town_laugh"]; p = dict(p)
    p["yaw"] = -abs(p.get("yaw", 0.4))                      # faces screen-left, toward the pillory
    p["mirror"] = True
    p["t"] = g / 30.0
    return p


def man_pose(g):
    _, p = cast6.STORY6["town_laugh_man1"]
    p = dict(p); p["t"] = g / 30.0
    p["yaw"] = 0.35; p["mirror"] = False
    p["head_roll"] = -10 + 4 * math.sin(g * 0.9)            # shaking with laughter (no mouth animation)
    if g < SPLAT:
        _, q = cast6.STORY6["town_point_man1"]; p = dict(q); p["t"] = g / 30.0; p["mouth"] = None
        p["yaw"] = 0.35
    return p


def belly_laugh(g, yaw, ph):
    """crowd at the pillory: hands on the belly, smug until the splat, then laughing (expression only, no mouth animation)."""
    p = dict(yaw=yaw, pitch=-0.25, expr="smug" if g < SPLAT else "laughing", head_roll=(6 if yaw < 0 else -6) + 5 * math.sin(g * 0.9 + ph),
             lean=-4, arm_l=dict(hand=(-0.30, 1.00), bend=0.9), arm_r=dict(hand=(0.30, 1.00), bend=-0.9), legs="stand", t=g / 30.0)
    if g >= SPLAT:
        p["fx"] = ["tears"]
    return p


def walker(cast, g, x0, x1, y, g0, speed, facing):
    """townsfolk crossing the square in the establishing shot."""
    x = x0 + facing * speed * (g - g0)
    p = cast6.cycle(cast, (g - g0) / 28.0, "walk", facing=facing, base=dict(expr="happy"))
    return (x, y), p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "AFTERNOON", quality=quality, lens=LENS, name="cam_s04b")
        sd = os.path.join(TMP, "sprites")
        A = self.actors
        A["baker2"] = C.make_actor("baker2", "baker2", sd)
        A["woman"] = C.make_actor("woman", "woman1", sd)
        A["man"] = C.make_actor("man", "man1", sd)
        A["guard"] = C.make_actor("guard", "guard1", sd)
        A["woman_b"] = C.make_actor("woman_b", "woman1", sd)
        A["man_b"] = C.make_actor("man_b", "man1", sd)
        props = os.path.join(TMP, "props")
        # Thai signs
        bs = L.sign_box(1.25, 0.48, 0.45)
        self.sign_short = C.PropCard("sign_short", C.svg_pngs([(L.thai_sign("ขาดน้ำหนัก!", w=1.25, h=0.48, chains=0.45), bs, 420)], props),
                                     bs, scale=1.0, shadow=True)
        bp = L.sign_box(2.5, 0.62)
        self.sign_pil = C.PropCard("sign_pil", C.svg_pngs([(L.thai_sign("ห้ามขายขาดน้ำหนัก!", w=2.5, h=0.62), bp, 360)], props),
                                   bp, scale=1.0, shadow=True)
        # tomato in flight (4 spins) + the splat
        tb = (-0.16, -0.16, 0.16, 0.16)
        tom = C.svg_pngs([(cast6.tomato_svg("tf%d" % i, r=0.075, rot=90 * i), tb, 1600) for i in range(4)], props)
        self.tomato = C.PropCard("tomato", tom, tb, scale=1.6, shadow=True)
        sb = (-0.30, -0.22, 0.30, 0.26)
        spl = C.svg_pngs([(cast6.tomato_svg("ts%d" % i, r=0.11, squash=s), sb, 1400) for i, s in enumerate((0.55, 1.0))], props)
        self.splat = C.PropCard("splat", spl, sb, scale=1.7, shadow=False)

    def hide_far(self, a, f):
        C.place(a, f, (30.0, 40.0), -30.0)

    def pose(self, shot, gs):
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_shot(shot, g)
            self.key_cam(f, loc, look, lens)
            self.key_set(f, oven=1.0)
            for a in A.values():
                self.hide_far(a, f)
            # balance
            if shot == 5:
                u = ez((g - TIP[0]) / float(TIP[1] - TIP[0]))
                B.set_big_scale(-7.0 * u + 1.2 * math.sin(clamp((g - TIP[1]) / 8.0) * math.pi) * (g > TIP[1]), frame=f)
            else:
                B.set_big_scale(-7.0 if shot != 4 else -2.0, frame=f)
            B.set_loaves(12, frame=f)
            far = Vector((30, 40, -10))
            # signs
            if shot == 5 and g >= SIGN_DROP[0]:
                u = clamp((g - SIGN_DROP[0]) / float(SIGN_DROP[1] - SIGN_DROP[0]))
                top = Vector((2.45, 5.10, 3.40 + 1.6 * (1 - u) ** 2))
                self.sign_short.put(top, face=loc, frame=f)
                sw = 6.0 * math.exp(-(g - SIGN_DROP[1]) / 8.0) * math.sin((g - SIGN_DROP[1]) * 0.8) if g > SIGN_DROP[1] else 0.0
                self.sign_short.root.rotation_euler[1] = math.radians(sw)
                self.sign_short.root.keyframe_insert("rotation_euler", frame=f)
                self.sign_short.show(0, frame=f)
            else:
                self.sign_short.put(far, face=loc, frame=f); self.sign_short.show(None, frame=f)
            if shot in (4, 6, 7):
                self.sign_pil.put((-4.0, 9.28, 2.62), face=(loc.x, loc.y, 2.6), frame=f); self.sign_pil.show(0, frame=f)
            else:
                self.sign_pil.put(far, face=loc, frame=f); self.sign_pil.show(None, frame=f)
            # tomato flight + splat
            if shot == 7 and THROW + 1 <= g < SPLAT:
                u = (g - THROW - 1) / float(SPLAT - THROW - 1)
                p0 = Vector((WOMAN_THROW[0] + 0.25, WOMAN_THROW[1] - 0.1, 3.05))
                p = p0.lerp(FACE + Vector((0, -0.05, 0)), u) + Vector((0, 0, 0.55 * math.sin(math.pi * u)))
                self.tomato.put(p, face=loc, frame=f); self.tomato.show((g - THROW) % 4, frame=f)
            else:
                self.tomato.put(far, face=loc, frame=f); self.tomato.show(None, frame=f)
            if shot == 7 and g >= SPLAT:
                slide = 0.012 * max(0, g - SPLAT - 2)
                self.splat.put(FACE + Vector((0.03, -0.06, 0.05 - slide)), face=loc, frame=f)
                self.splat.show(0 if g == SPLAT else 1, frame=f)
            else:
                self.splat.put(far, face=loc, frame=f); self.splat.show(None, frame=f)
            # actors
            if shot == 4:
                C.place(A["baker2"], f, BAKER_SCALE, 0.0)
                C.place(A["guard"], f, (-5.8, 6.0), 0.0)
                (xy, _) = walker("woman1", g, -6.0, 0, 2.2, 117, 0.06, 1); C.place(A["woman"], f, xy, 0.0)
                (xy, _) = walker("man1", g, 2.0, 0, 3.6, 117, 0.06, -1); C.place(A["man"], f, xy, 0.0)
                C.place(A["woman_b"], f, (-8.0, 3.0), 0.0)
                C.place(A["man_b"], f, (8.5, 3.0), 0.0)
            elif shot == 5:
                C.place(A["baker2"], f, BAKER_SCALE, 0.0)
                C.place(A["man"], f, (-1.6, 9.5), 0.0)
                C.place(A["woman_b"], f, (-0.4, 11.5), 0.0)
            elif shot == 6:
                C.place(A["baker2"], f, PIL_FEET[:2], PIL_FEET[2])
                C.place(A["guard"], f, GUARD_PIL[:2], GUARD_PIL[2])
                C.place(A["woman"], f, (-0.9, 7.6), 0.0)
                C.place(A["man"], f, (-6.9, 6.2), 0.0)
            else:
                C.place(A["baker2"], f, PIL_FEET[:2], PIL_FEET[2])
                C.place(A["woman"], f, WOMAN_THROW, 0.0)
                C.place(A["man"], f, (-5.30, 9.05), 1.0)
                C.place(A["woman_b"], f, (-2.72, 9.05), 1.0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            cam = self.cam
            if shot == 4:
                A["baker2"].pose(f, dict(baker_scale_pose(180), expr="neutral", fx=[]), camera=cam)
                A["guard"].pose(f, cast6.STORY6["guard_stand"][1], camera=cam)
                A["woman"].pose(f, walker("woman1", g, -6.0, 0, 2.2, 117, 0.06, 1)[1], camera=cam)
                A["man"].pose(f, walker("man1", g, 2.0, 0, 3.6, 117, 0.06, -1)[1], camera=cam)
                A["woman_b"].pose(f, dict(cast6.STORY6["town_point"][1], mouth=None), camera=cam)
                A["man_b"].pose(f, dict(cast6.STORY6["town_laugh_man1"][1], yaw=-0.3), camera=cam)
            elif shot == 5:
                A["baker2"].pose(f, baker_scale_pose(g), camera=cam)
                A["man"].pose(f, dict(cast6.STORY6["town_point_man1"][1], mouth=None), camera=cam)
                A["woman_b"].pose(f, dict(cast6.STORY6["town_laugh"][1]), camera=cam)
            elif shot == 6:
                A["baker2"].pose(f, baker_pillory_pose(g, 6), camera=cam)
                A["guard"].pose(f, dict(cast6.STORY6["guard_stand"][1], yaw=0.45), camera=cam)
                A["woman"].pose(f, dict(cast6.STORY6["town_point"][1], mouth=None, yaw=-0.45, mirror=True), camera=cam)
                A["man"].pose(f, dict(cast6.STORY6["town_laugh_man1"][1], head_roll=-10 + 4 * math.sin(g * 0.9)), camera=cam)
            else:
                A["baker2"].pose(f, baker_pillory_pose(g, 7), camera=cam)
                A["woman"].pose(f, woman_pose(g), camera=cam)
                A["man"].pose(f, belly_laugh(g, 0.40, 0.0), camera=cam)
                A["woman_b"].pose(f, belly_laugh(g, -0.40, 1.0), camera=cam)
            for k, a in A.items():
                if f not in a.poses:
                    a.pose(f, dict(expr="neutral"), camera=cam)
        fr = [bf(shot, g) for g in gs]
        ppd = {4: dict(baker2=96, guard=96, woman=96, man=96, woman_b=96, man_b=96),
               5: dict(baker2=576, man=128, woman_b=128, guard=32, woman=32, man_b=32),
               6: dict(baker2=448, guard=256, woman=320, man=256, woman_b=32, man_b=32),
               7: dict(baker2=640, woman=448, man=448, woman_b=448, guard=32, man_b=32)}[shot]
        self.sprites_for([(A[k], v) for k, v in ppd.items()], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_shot(shot, g)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc],
                   heads={k: v for k, v in C.head_report(self, f).items() if -200 < v["x"] < 920 and -200 < v["y"] < 1480})
        out["face_px"] = [round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(FACE), f)[:2]]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
