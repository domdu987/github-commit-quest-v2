#!/usr/bin/env python3
"""shot.py -- film 2 take s18: shot 18 (t 48.23-52.84 s, g 1447..1584 + 7 handle frames each side), tower NIGHT_STORM, no rod,
inside the bell chamber.

"แต่ถ้าไม่มี มันจะหาทางลงเอง ผ่านหิน ผ่านไม้ ผ่านเชือก ระฆังที่เปียกฝน": without a rod the charge finds its own way down.
    1440-1500  the dark chamber in the storm: rain beyond the arches, the wet rope dripping; a flash outside (1462);
               on "มันจะหาทางลงเอง" (1470) a faint crackle starts in the top corner; slow push up toward it
    1500-1518  snap onto the stone (lands on "ผ่านหิน" 1505): a jagged glow crawls over the north wall, down to the bell frame
    1518-1540  snap onto the wood ("ผ่านไม้" 1523): the glow runs along the frame beam, the bearing, the headstock and the rope lever
    1540-1591  snap onto the rope ("ผ่านเชือก" 1543): the glow runs down the wet rope and the sally (camera tilts down with it);
               the drops on the rope flare as they fall ("ระฆังที่เปียกฝน" 1554-1584); the embers fade
A point light rides the glow head (the only extra light: the charge lights the stone and wood around it).

    python3 shot.py stills 1440:1591:6 <out> [0.5] [6]     python3 shot.py final 1440:1591
"""
import math, os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import T, Vector, bpy, keys, lerp, clamp, pulse, ease, g_of, build, set_cam, cam_track, emit_mat, set_strength, \
    curve, reveal, jag, point_at, path_len, sphere, point_light, BaseTake, run_cli

G0, G1, H = 1447, 1585, 7                       # round(48.23*30), round(52.84*30)
RANGE = (G0 - H, G1 + H - 1)                    # 1440 .. 1591
G_OWN = g_of(48.915)                            # 1470 "มันจะหาทางลงเอง"
G_STONE = g_of(50.083)                          # 1505 "ผ่านหิน"
G_WOOD = g_of(50.657)                           # 1523 "ผ่านไม้"
G_ROPE = g_of(51.317)                           # 1543 "ผ่านเชือก"
G_BELL = g_of(51.693)                           # 1554 "ระฆังที่"
G_WET = g_of(52.079)                            # 1565 "เปียกฝน"
RX, RY = T.STATE.get("rope", (0.93, 1.0)) if T.STATE.get("rope") else (0.93, 1.0)
YN = 1.83                                       # inner face of the north wall (+ 0.02 off it)

# the three sections of the path (world D) and their travel frames
# stone: down the wall above the north arch, then along its voussoir ring to the east springing
STONE_CTRL = [(-0.35, YN, 21.0), (-0.1, YN, 20.75), (0.05, YN, 20.6)] + \
    [(1.44 * math.cos(math.radians(a)), YN, 19.0 + 1.44 * math.sin(math.radians(a))) for a in (80, 62, 44, 26, 10)] + [(1.45, YN - 0.05, 18.95)]
# wood: across to the frame post, up it, along the frame beam, the bearing, the headstock, the rope lever
WOOD_PTS = [(1.39, 1.62, 18.95), (1.39, 1.62, 19.5), (1.39, 1.5, 19.82), (1.45, 1.2, 19.83), (1.45, 0.7, 19.83), (1.45, 0.25, 19.83),
            (1.38, 0.0, 20.1), (1.33, -0.31, 20.45), (1.15, -0.31, 20.5), (0.95, -0.31, 20.42), (0.93, -0.1, 20.33), (0.93, 0.25, 20.48),
            (0.93, 0.6, 20.48), (0.93, 0.98, 20.48)]
ROPE_PTS = [(RX, RY, 20.48), (RX, RY, 18.5), (RX, RY, 16.05)]
TRAVEL = {"stone": (G_STONE - 4, G_STONE + 11), "wood": (G_WOOD - 2, G_WOOD + 14), "rope": (G_ROPE - 1, G_ROPE + 17)}
CORNER_CRACKLE = (G_OWN, G_STONE - 4)           # faint flicker in the top corner before it crawls
FLASH_OUT = {1462: 0.55, 1463: 0.15, 1464: 0.45, 1466: 0.0}

#        cam x, y, z            look x, y, z
C0 = (-1.0, -3.7, 17.5, 0.75, 1.3, 18.7)          # from just outside the south arch: bell, rope, the north arch, rain
C0pre = (-1.12, -3.85, 17.42, 0.82, 1.3, 18.62)    # (slightly wider at the start: the camera creeps in)
C1 = (-0.6, -3.2, 17.7, 0.6, 1.6, 19.6)           # push and tilt up toward the north arch ring
C2 = (1.72, -1.5, 17.7, 0.75, YN, 19.9)           # on the stone ring of the north arch
C2b = (1.7, -1.4, 17.8, 0.95, YN, 19.75)
C3 = (1.0, -1.65, 18.0, 1.25, 0.5, 20.15)       # high under the ceiling: post, frame beam, bearing, headstock, lever
C3b = (1.05, -1.6, 18.15, 1.12, 0.6, 20.22)
C4 = (2.06, -0.3, 18.9, RX, RY, 19.6)             # on the rope top
C5 = (2.04, -0.1, 17.0, RX, RY, 16.75)            # down the rope to the sally and the drips
C6 = (1.95, 0.05, 16.75, RX, RY, 16.3)


def cam_at(g):
    ks = [(RANGE[0], C0pre, "sine"), (G_OWN - 4, C0, "sine"), (G_STONE - 6, C1, "quint"), (G_STONE, C2, "sine"),
          (G_WOOD - 6, C2b, "quint"), (G_WOOD, C3, "sine"), (G_ROPE - 6, C3b, "quint"), (G_ROPE, C4, "sine"),
          (G_ROPE + 4, C4, "sine"), (G_WET, C5, "sine"), (RANGE[1] + 1, C6, "hold")]
    loc, look = cam_track(g, ks, 0.15)
    for s in (G_STONE, G_WOOD, G_ROPE):                # a small jolt when the charge lands on each beat
        d = g - s
        if 0 <= d <= 6:
            a = 0.025 * math.exp(-0.5 * d)
            look = look + Vector((a * math.sin(d * 2.7), 0.0, a * math.cos(d * 2.2)))
    return loc, look


def prog(name, g):
    a, b = TRAVEL[name]
    return ease((g - a) / float(b - a), "cubic_out" if name != "rope" else "sine") if g >= a else 0.0


def rain_mesh(name, region, n, seed, face):
    """vertical streak quads in a box, replicated over 5 periods of 3 D in z (the object is moved down per frame)"""
    r = random.Random(seed)
    (x0, x1), (y0, y1), (z0, z1) = region
    verts, faces = [], []
    base = [(r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(0, 3.0), r.uniform(0.35, 0.7)) for _ in range(n)]
    for k in range(int((z1 - z0) / 3.0) + 2):
        for (x, y, z, l) in base:
            zz = z0 + z + 3.0 * k
            w = 0.008
            if face == "y":
                q = [(x - w, y, zz), (x + w, y, zz), (x + w + 0.06, y, zz + l), (x - w + 0.06, y, zz + l)]
            else:
                q = [(x, y - w, zz), (x, y + w, zz), (x, y + w + 0.06, zz + l), (x, y - w + 0.06, zz + l)]
            i = len(verts); verts += q; faces.append((i, i + 1, i + 2, i + 3))
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.visible_shadow = False; T.no_bounce(ob)
    return ob


class Take(BaseTake):
    def __init__(self, quality="preview"):
        self.scene, self.A, self.cam = build("NIGHT_STORM", quality)
        T.set_rod(0); T.set_bolt(False); T.flash(0.0); T.set_bell(0.0)
        global RX, RY
        RX, RY = T.STATE["rope"]
        self.m_core = emit_mat("S18_core", "#f2f4ff", 6.0)
        self.m_glow = emit_mat("S18_glow", "#90a4ff", 0.7, additive=True)
        self.m_ember = emit_mat("S18_ember", "#b8c6ff", 2.2)
        self.m_rain = emit_mat("S18_rain", "#8c9cd8", 0.55, additive=True)
        self.m_drop = emit_mat("S18_drop", "#c8d4ff", 0.9)
        self.secs = {}
        stone = jag(STONE_CTRL, 21, 0.09, sub=5)
        wood = jag(WOOD_PTS, 22, 0.018, sub=2)
        rope = ROPE_PTS
        for nm, pts, rc, rg in (("stone", stone, 0.022, 0.1), ("wood", wood, 0.02, 0.06), ("rope", rope, 0.033, 0.05)):
            self.secs[nm] = dict(pts=pts, L=path_len(pts), core=curve("s18_%s_core" % nm, pts, rc, self.m_core),
                                 glow=curve("s18_%s_glow" % nm, pts, rg, self.m_glow), ember=curve("s18_%s_ember" % nm, pts, rc * 0.8, self.m_ember))
        # forks creeping over the stone
        self.forks = []
        for i, (u, end) in enumerate(((0.25, (-0.6, YN, 20.55)), (0.5, (0.85, YN, 21.0)), (0.72, (1.75, YN, 20.15)))):
            s = point_at(stone, u)
            pts = jag([tuple(s), end], 30 + i, 0.06, sub=5)
            self.forks.append((u, curve("s18_fork%d" % i, pts, 0.014, self.m_core)))
        cc = jag([(-0.8, YN, 20.95), (-0.35, YN, 21.0), (0.1, YN, 20.9)], 40, 0.05, sub=4)
        self.corner = curve("s18_corner", cc, 0.012, self.m_ember)
        self.head = sphere("s18_head", (0, 0, 0), 0.06, self.m_core)
        self.head_glow = sphere("s18_head_glow", (0, 0, 0), 0.09, self.m_glow)
        self.light = point_light("s18_light", (0.72, 0.8, 1.0), 0.0, radius=0.05)
        self.rain = [rain_mesh("s18_rain_n", ((-3.5, 3.5), (2.6, 7.0), (12.0, 24.0)), 140, 5, "y"),
                     rain_mesh("s18_rain_e", ((2.7, 7.0), (-3.5, 3.5), (12.0, 24.0)), 140, 6, "x")]
        for o in self.rain:
            o.data.materials.append(self.m_rain)
        self.drops = [sphere("s18_drop%d" % i, (RX, RY, 17), 0.028, self.m_drop) for i in range(5)]
        self.fx = [self.head, self.head_glow, self.corner] + [c for u, c in self.forks] + \
            [s[k] for s in self.secs.values() for k in ("core", "glow", "ember")]

    def cam_at(self, g):
        return cam_at(g)

    def marks(self):
        return {"stone_start": Vector(STONE_CTRL[0]), "bearing": Vector(WOOD_PTS[3]), "lever": Vector(WOOD_PTS[-1]),
                "rope_top": Vector(ROPE_PTS[0]), "sally": Vector((RX, RY, 16.85)), "rope_end": Vector(ROPE_PTS[-1])}

    def state(self, g):
        return {k: round(prog(k, g), 3) for k in TRAVEL}

    def drop_pos(self, i, g):
        """drop i: slides down the lower rope, falls from its end to the floor; period 26 frames, phases spread"""
        per = 26; ph = (g + i * 11 + (i * i * 3) % 7) % per
        if ph < 14:                                         # sliding 17.3 -> 16.05 on the rope surface
            z = 17.3 - 1.25 * (ph / 14.0) ** 1.6
            return Vector((RX + 0.035, RY - 0.02, z)), False
        t = (ph - 14) / 30.0                                # falling (seconds)
        z = 16.0 - 0.5 * 9.8 * 0.35 * t * t * 9.0
        return Vector((RX + 0.01, RY, max(15.02, z))), True

    def on_frame(self, g):
        loc, look = cam_at(g)
        set_cam(self.cam, loc, look)
        for o in self.fx:
            o.hide_render = True
        fo = 0.0
        for f in sorted(FLASH_OUT):
            if g >= f:
                fo = FLASH_OUT[f]
        T.flash(fo)
        for k, o in enumerate(self.rain):
            o.location = (0.0, 0.0, -((g * (0.95 + 0.05 * k)) % 3.0))
        flick = 0.8 + 0.2 * math.sin(g * 3.3) * math.cos(g * 1.7)
        if CORNER_CRACKLE[0] <= g < CORNER_CRACKLE[1] and (g * 7) % 5 < 3:
            a = (g - CORNER_CRACKLE[0]) / float(CORNER_CRACKLE[1] - CORNER_CRACKLE[0])
            reveal(self.corner, 0.0, 0.3 + 0.7 * a)
        head = None; amp = 0.0
        for nm in ("stone", "wood", "rope"):
            S = self.secs[nm]; a, b = TRAVEL[nm]
            if g < a:
                continue
            u = prog(nm, g)
            if g <= b + 1:
                w = 0.9 / S["L"]
                reveal(S["core"], max(0.0, u - w), u); reveal(S["glow"], max(0.0, u - 1.8 * w), u)
                head = point_at(S["pts"], u); amp = 1.0
            done = max(0, g - b)
            k = math.exp(-done / 14.0)
            if k > 0.05:
                reveal(S["ember"], 0.0, u)
            if nm == "stone":
                for fu, c in self.forks:
                    if u >= fu and (g - a) % 4 != 3 and done < 10:
                        reveal(c, 0.0, min(1.0, (u - fu) * 4.0))
        lastb = max(b for a, b in TRAVEL.values())
        ek = 2.2 * flick * (math.exp(-max(0, g - lastb) / 14.0))
        set_strength(self.m_ember, ek)
        set_strength(self.m_core, 6.0 * flick); set_strength(self.m_glow, 0.7 * flick)
        if head is not None:
            self.head.hide_render = self.head_glow.hide_render = False
            self.head.location = head; self.head_glow.location = head
            self.light.location = head
            self.light.data.energy = 6.0 * flick * amp
        else:
            self.light.data.energy = 0.0
        # drops: dim and wet, flaring white once the charge is in the rope
        lit = g >= TRAVEL["rope"][0] + 6
        for i, d in enumerate(self.drops):
            p, falling = self.drop_pos(i, g)
            d.location = p
            d.scale = (1.0, 1.0, 1.6 if falling else 1.15)
        set_strength(self.m_drop, (5.0 * flick * math.exp(-max(0, g - TRAVEL["rope"][1]) / 20.0) + 0.9) if lit else 0.9)


if __name__ == "__main__":
    run_cli(Take, RANGE, HERE)
