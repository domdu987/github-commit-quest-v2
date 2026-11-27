#!/usr/bin/env python3
"""shot.py -- film 24 take s15: shot 15 (g 1767..1949, no out-handle; the film ends on g 1949), sea / shore, the ending.
  g 1767..1866  (58.90-61.9 s) "ส่วนแม่ทัพ ... ต้องเกาะไม้กระดาน ลอยคอ": jp_cmd24_plank_cling, wet, rides the swell in the surf
                 (z = J.swell_z at the card, keyed every frame; the set's half-beached plank is hidden: the card carries its own).
                 Camera: slow eased pull-back.
  g 1867..1949  HARD CUT (62.12 s "แล้วคลานขึ้นฝั่ง"): on the sand, crawl_a / crawl_b alternating every 8 frames, 0.45 D per half step
                 up the beach (ground anchor on the sand height field), wet 1.  Camera: slow eased pull-back.
Mouths: held (no quote).  Blender frame of g = C.bf(15, g).
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out> [scale samples] | final a:b[:step] [scale samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

J, actors, cast24 = C.J, C.actors, C.cast24
if J.LOOK == "C":                                        # look C: warm sun-side rim on the backlit cards (A / B unchanged)
    _story0 = C.story
    C.story = lambda n: (lambda cp: (cp[0], J.card_rim(cp[1])))(_story0(n))
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
SHOT = 15
G0, G1 = C.g_bound(58.90), 1949
G_CUT = C.g_of(62.12)                  # 1867: the sand
H_IN = 6
RANGES = {SHOT: (G0 - H_IN, G1)}
PRESET = "shore"
STEP = 8                               # crawl pose alternates every 8 frames
HALF = 0.45                            # forward travel per half step (D)
PPD = dict(pl=144, cr=144)


def beach_h(x, y):
    return J.S["islands"]["beach"]["h"](x, y)


def sp():
    return J.S["shore_pt"]


# ---- water phase: the card floats seaward of the surf line
def water_pt(g):
    s = sp()
    x, y = s.x + 0.6 + 0.35 * math.sin(g * 0.03), s.y - 5.5 + 0.4 * math.sin(g * 0.021 + 1.0)
    return x, y


# ---- sand phase: start point + direction up the beach (screen-right)
def sand_start():
    s = sp()
    return Vector((s.x - 0.5, s.y + 1.3, 0.0))


DIR = Vector((0.58, 0.81, 0.0)).normalized()


def crawl_k(g):
    """number of half steps done (float): 0.45 D per half step; the body surges forward in the second half of every step."""
    n = (g - G_CUT) / float(STEP)
    i = math.floor(n); p = n - i
    return i + 0.35 * p + 0.65 * ez(p)


def crawl_xy(g):
    d = crawl_k(g) * HALF
    p = sand_start() + DIR * d
    return p.x, p.y


def cam_of(g):
    s = sp()
    if g < G_CUT:
        u = C.calm((g - G0) / float(G_CUT - 1 - G0))
        pl = Vector((water_pt(G0)[0], water_pt(G0)[1], 0.0))
        loc0 = Vector((pl.x + 3.0, pl.y - 8.0, 1.9)); look0 = Vector((pl.x - 0.2, pl.y + 0.5, 1.5))
        loc1 = Vector((pl.x + 5.0, pl.y - 12.5, 2.6)); look1 = Vector((pl.x - 0.2, pl.y + 0.5, 1.7))
        return loc0.lerp(loc1, u), look0.lerp(look1, u), 24.0
    u = C.calm((g - G_CUT) / float(G1 - G_CUT))
    st = sand_start()
    cx, cy = crawl_xy(g)
    mid = st + DIR * 2.4
    px = 0.6 * cx + 0.4 * mid.x + 0.9; py = 0.6 * cy + 0.4 * mid.y
    h = beach_h(cx, cy)
    look = Vector((px, py, h + 1.3))
    off = Vector((-4.2, -6.6, 1.0)).lerp(Vector((-5.8, -9.2, 1.5)), u)
    return look + off, look, 24.0


def pose_pl(g):
    c, p = C.story("jp_cmd24_plank_cling")
    p["wet24"] = 1.0
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.10)
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.07 + 0.5)
    p["blink"] = blink(g, [1790, 1830])
    p["t"] = g / 30.0
    return p


def pose_cr(g):
    k = int(math.floor((g - G_CUT) / float(STEP)))
    c, p = C.story("jp_cmd24_crawl_a" if k % 2 == 0 else "jp_cmd24_crawl_b")
    p["wet24"] = 1.0
    p["blink"] = blink(g, [1900, 1938])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, shot=SHOT):
        C.Take.__init__(self, PRESET, name="cam_s15")
        sd = os.path.join(TMP, "sprites")
        S = J.S
        S["plank"].hide_render = True                    # the set's lying plank: the card carries its own floating plank
        self.pl = self.actors["pl"] = C.make_actor("pl", "jp_cmd24", sd, story="jp_cmd24_plank_cling")
        self.cr = self.actors["cr"] = C.make_actor("cr", "jp_cmd24", sd, story="jp_cmd24_crawl_a")

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(g)
            self.key_cam(f, loc, look, lens=lens)
            if g < G_CUT:
                x, y = water_pt(g)
                C.place(self.pl, f, (x, y, J.swell_z(x, y, f / 30.0)))
                C.place(self.cr, f, (x, y, 0.0))
            else:
                x, y = crawl_xy(g)
                C.place(self.cr, f, (x, y, beach_h(x, y)))
                C.place(self.pl, f, (x, y, beach_h(x, y)))
        self.scene.frame_set(bf(shot, gs[0]))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.pl.pose(f, pose_pl(g), camera=self.cam)
            self.cr.pose(f, pose_cr(g), camera=self.cam)
        fs = [bf(shot, g) for g in gs]
        self.sprites_for([(self.pl, PPD["pl"]), (self.cr, PPD["cr"])], fs)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(g)
        # hide whichever actor is not in this phase for head / feet reports and for the render
        self.pl.card.hide_render = g >= G_CUT
        self.cr.card.hide_render = g < G_CUT
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f), feet=C.feet_report(self, f))

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        for g in gs:
            self.pl.card.hide_render = g >= G_CUT
            self.cr.card.hide_render = g < G_CUT
            self.pl.card.hide_viewport = self.pl.card.hide_render
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[2]) if G0 - H_IN <= g <= G1]
        Tk = Take(); Tk.pose(SHOT, gs)
        for g in gs:
            if cmd == "probe":
                print(json.dumps(Tk.report(SHOT, g)), flush=True)
            else:
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 10
                Tk.report(SHOT, g)
                st = Tk.render(SHOT, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s15_g_%04d.png" % g))
                print("g %d %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else C.RES_PCT
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else C.preset_samples(PRESET)
        C.final_loop(lambda s_: Take(), [SHOT], sys.argv[2], RANGES, HERE, scale=scale, samples=samples)
