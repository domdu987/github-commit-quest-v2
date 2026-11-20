#!/usr/bin/env python3
"""shot.py -- film 20 take s24 = shot 24, BIGZOOM 2 (ending): g 1732..1851 + handles 8 in (dissolve 13) g 1724..1731, 4 out (cut) g 1852..1855.
"ส่วนโมปัสซังต์ เล่ากันว่า หลังหอเปิด เขาขึ้นไป กินข้าวบนหอ": ONE continuous camera move in the TOWER location (preset tower_window_pull, DAY 1889).
Start: EXTREME WIDE and high -- Paris, the fair, the whole finished tower; Maupassant is a 5 px speck in the lit first-floor restaurant window.
Move: eased push (log-distance, direction blended) down across the city, up the lattice, through the gallery girders to the window and land on a MEDIUM
of Maupassant at his window table; he takes his first happy bite on "กินข้าวบนหอ" (60.48 s, g 1817).  Then a slow drift until the cut.
Mouths never move (no quote).

    python3 shot.py probe a:b[:step] | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

SHOT = 24
G0, G1 = C.g_bound(57.75), 1853                 # 1732, 1853 (exclusive): shot = g 1732..1852 (plan 57.75-61.77 s)
H_IN, H_OUT = 8, 6                              # dissolve 13 in (13/2 + 2); 9-frame MATCH-DISSOLVE out into s25 (6 handle frames)
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1     # 1724..1855
GS = list(range(G_FIRST, G_LAST + 1))
G_BITE = C.g_of(60.48 - 0.10)                   # 1817: "กินข้าวบนหอ" starts at 60.48 narration s -> first bite lands here
G_LAND = G_BITE + 2                             # camera lands on the medium
PRESET, LIGHT = "tower_window_pull", "DAY"
SEAT_H, PPD = 0.865, 256
CANVAS = cast20.CANVAS20["maupassant"]

# ---- camera in metres, tower-local (x right, y toward Paris/camera side = -y, z up); window table at (0, -35.8, 58.65), glass y = -36.8
TGT = Vector((0.0, -35.4, 59.2))                 # aim point: his head height
START_OFF = Vector((float(os.environ.get("X0", "-60")), -float(os.environ.get("Y0", "360")), float(os.environ.get("Z0", "130"))))     # camera start relative to TGT (m): far, high, left
END_OFF = Vector((float(os.environ.get("X1", "0.0")), -float(os.environ.get("D1", "4.8")), 0.45))       # camera landing relative to TGT (m)
AIM0 = Vector((0.0, -30.0, float(os.environ.get("AIMZ", "150"))))                                        # initial aim point: mid-tower (whole tower in frame)


AIM_DROP = float(os.environ.get('AIM_DROP', '0.2'))      # m: the landing aim sits below his head (less bare floor, head up in the frame)
DIP = float(os.environ.get('DIP', '0.0'))
LOOK_UP = float(os.environ.get('LOOK_UP', '2.5'))
GAMMA = float(os.environ.get('GAMMA', '1.0'))


def smooth(u):
    u = clamp(u)
    return u * u * u * (u * (6 * u - 15) + 10)    # smootherstep: ease in and out, zero velocity ends


_GG = np.arange(G_FIRST, G_LAST + 1)
_V = 1.0 * np.exp(-0.5 * ((_GG - 1755) / 20.0) ** 2) + 20.0 * np.exp(-0.5 * ((_GG - 1781) / 2.0) ** 2) + 1.0 * np.exp(-0.5 * ((_GG - 1802) / 9.0) ** 2)
_V[_GG > 1822] = 0.0
_C = np.cumsum(_V); _C = _C - _C[0]; _C = np.minimum(_C / _C[np.where(_GG <= 1822)[0][-1]], 1.0)


def prog(g):
    """camera progress 0..1: eased-in approach across the city and up the lattice (g 1724-1777), a fast eased whip into the window gallery
    (g 1778-1784, the flat gallery facade is on screen for only ~5 frames), then a long ease-out settle onto the medium (-> g 1822)."""
    return float(_C[int(clamp(g, G_FIRST, G_LAST)) - G_FIRST])


def cam_at(g):
    """(loc, look) in world D at film frame g."""
    s = prog(g)
    d0, d1 = START_OFF.length, END_OFF.length
    dist = d0 * (d1 / d0) ** s
    dir0, dir1 = START_OFF.normalized(), END_OFF.normalized()
    dr = (dir0 * (1 - s) + dir1 * s).normalized()
    drift = (g - G_LAND) / 30.0 if g > G_LAND else 0.0                   # after landing: slow push + slide, never parked
    bump = math.exp(-(((s - 0.80) / 0.13) ** 2))
    loc = TGT + dr * dist + Vector((0.0, 0.0, -DIP * bump))     # swoops below the window, looking up through the first-platform lattice (texture), then rises to his eye level
    aim = TGT + (AIM0 - TGT) * (1 - s) ** 3.0 + Vector((0.0, 0.0, -AIM_DROP * s + LOOK_UP * bump))
    if drift > 0:
        loc = loc + Vector((0.10 * drift, 0.22 * drift, 0.0)) * (1.0 - 0.3 * drift / 1.2)
        aim = aim + Vector((0.10 * drift, 0.0, 0.0))
    return Vector(CO.W(tuple(loc))), Vector(CO.W(tuple(aim)))


GLOW = float(os.environ.get('GLOW', '40.0'))
EXPO_FAR, EXPO_NEAR = float(os.environ.get("EXPO_FAR", "-1.3")), float(os.environ.get("EXPO_NEAR", "-0.35"))


def lens_at(g):
    """22 mm for the whole approach; during the final settle (progress 0.80 -> 1.0) it eases to the preset tower_window_in lens, 55 mm, so the landing
    is the director's framing (outside the glass, ~4.8 m, through the clear centre pane: little ceiling, no X of beams)."""
    s = prog(g)
    w = smooth((s - 0.80) / 0.20)
    return 22.0 * (55.0 / 22.0) ** w


def expo_at(g):
    """grade exposure follows the distance: the sunlit exterior is bright (-1.3 EV), the lamp-lit room darker (-0.05 EV): keeps luma ~95 through the whole zoom."""
    d = (cam_at(g)[0] - Vector(CO.W(tuple(TGT)))).length / CO.SC
    k = clamp(math.log(150.0 / max(d, 1.0)) / math.log(150.0 / 6.0))
    bump = 0.5 * math.exp(-((math.log(max(d, 0.5)) - math.log(3.8)) / 0.45) ** 2)       # the dark ceiling / beams while the camera crosses the gallery
    return EXPO_FAR + (EXPO_NEAR - EXPO_FAR) * k + bump


TOAST = None
EAT = cast20.STORY20["maupassant_seated_eat"][1]
CHEW = cast20.STORY20["maupassant_seated_eat_chew"][1]
PERIOD = 40.0


def _mouth_hand():
    """arm_r hand target (puppet-local) that brings the fork's prop tip onto the mouth anchor (2 fixed-point iterations on the puppet anchors)."""
    import puppet
    base = dict(EAT); base["prop_r"] = dict(EAT["prop_r"], scale=FORK_SCALE); base["seated"], base["seat_h"], base["napkin"], base["mouth"], base["yaw"] = 1, SEAT_H, 1, "smile", 0.30
    hx, hy = EAT["arm_r"]["hand"]
    for _ in range(3):
        base["arm_r"] = dict(EAT["arm_r"], hand=(hx, hy))
        a = puppet.figure("maupassant", base, "f")["anchors"]
        mx, my = a["mouth"]; tx, ty = a["prop_tip_r"]
        hx, hy = hx + (mx - tx), hy + (my - ty)
    return hx, hy


MOUTH_HAND = None
FORK_SCALE = 1.45


def pose_of(g):
    global MOUTH_HAND
    if MOUTH_HAND is None:
        MOUTH_HAND = _mouth_hand()
    """fork cycle phase locked so the first bite (fork at his mouth) is at g 1817; mouth a still smile."""
    s = 0.5 - 0.5 * math.cos(2 * math.pi * ((g - G_BITE) / PERIOD) + math.pi)      # 1 at g = G_BITE (+ k * PERIOD)
    p = dict(EAT)
    p["seated"], p["seat_h"], p["napkin"], p["mouth"] = 1, SEAT_H, 1, "smile"
    ae, ac = MOUTH_HAND, CHEW["arm_r"]["hand"]
    p["arm_r"] = dict(EAT["arm_r"], hand=(lerp(ac[0], ae[0], s), lerp(ac[1], ae[1], s)), bend=lerp(CHEW["arm_r"]["bend"], EAT["arm_r"]["bend"], s), layer="top")
    pr = dict(EAT["prop_r"]); pr["scale"] = FORK_SCALE; pr["angle"] = lerp(CHEW["prop_r"]["angle"], EAT["prop_r"]["angle"], s)
    p["prop_r"] = pr
    p["bite"] = 1.0 if s > 0.5 else 0.0
    p["yaw"] = 0.30 + 0.07 * math.sin(g * 0.11)
    p["pitch"] = 0.02 + 0.06 * (1 - s)
    p["head_roll"] = 2.5 * math.sin(2 * math.pi * (g - G_BITE) / PERIOD + 1.0)
    p["lean"] = 2.0 * s + 0.8 * math.sin(g * 0.17)
    ph = ((g - G_BITE) % PERIOD) / PERIOD                       # 0 at the bite; cheek-bulge chewing (3 Hz) for ~16 frames after it
    ch = max(0.0, math.sin(math.pi * clamp((ph - 0.08) / 0.5))) * (0.5 + 0.5 * math.sin(2 * math.pi * 3.0 * (g - G_BITE) / 30.0))
    p["squash"] = (1.0 + 0.06 * ch, 1.0 - 0.05 * ch)
    p["blink"] = blink(g, [1760, 1801, 1838])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s%02d" % SHOT)
        C.grade(self.scene, float(os.environ.get("EXPO", "-1.3")), float(os.environ.get("SAT", "1.2")))
        self.cam.data.shift_x = self.cam.data.shift_y = 0.0
        self.cam.data.clip_start, self.cam.data.clip_end = 0.05, 2000.0
        for ob in [o for o in C.bpy.data.objects if o.name.startswith(("fg_", "shade_casters"))]:      # preset FG iron post (anchored to the preset camera): a black bar through the table
            ob.hide_render = True
        for ob in [o for o in C.bpy.data.objects if o.name.startswith("actor_")]:       # the build's stand-in card at the window
            ob.hide_render = True
            ob.hide_viewport = True
        self.make_glow()
        self.key_cam(bf(G_FIRST), *cam_at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.1, depth=0.5, opacity=0.5), shadow=None, cam=self.cam)

    def make_glow(self):
        """a warm emissive plane just outside the glass of Maupassant's window: in the extreme wide the window + red awning must be the brightest WARM spot
        of the frame (findable from the first frames); it is faded out / hidden before the camera reaches the facade."""
        bpy = C.bpy
        c = Vector(self.A["marks"]["window_centre"])
        yg = c.y - 0.12 * CO.SC
        w, h = 2.7 * CO.SC / 2, 3.4 * CO.SC / 2
        me = bpy.data.meshes.new("win_glow")
        me.from_pydata([(-w, 0, -h), (w, 0, -h), (w, 0, h), (-w, 0, h)], [], [(0, 3, 2, 1)])
        ob = bpy.data.objects.new("win_glow", me)
        bpy.context.scene.collection.objects.link(ob)
        ob.location = (c.x, yg, c.z)
        mat = bpy.data.materials.new("win_glow"); mat.use_nodes = True
        nt = mat.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (1.0, 0.55, 0.18, 1.0); em.inputs["Strength"].default_value = GLOW
        out = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], out.inputs["Surface"])
        me.materials.append(mat)
        ob.visible_shadow = False
        self.glow, self.glow_em = ob, em

    def glow_key(self, g, f):
        k = clamp(1.0 - (g - 1750) / 24.0)                       # full until g 1750, gone by 1774
        self.glow_em.inputs["Strength"].default_value = GLOW * k
        self.glow_em.inputs["Strength"].keyframe_insert("default_value", frame=f)
        CO.show(self.glow, k > 0.01, f)

    def pose(self, gs):
        mark = self.A["marks"]["maupassant_window"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g))
            self.key_set(f, set_year=1889, set_crowd=2)
            self.scene.view_settings.exposure = expo_at(g)
            self.scene.view_settings.keyframe_insert("exposure", frame=f)
            self.cam.data.lens = lens_at(g)
            self.cam.data.keyframe_insert("lens", frame=f)
            self.glow_key(g, f)
            C.place(self.mau, f, mark)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mau.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.mau, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    dist_m=round((loc - Vector(CO.W(tuple(TGT)))).length / CO.SC, 1), heads=C.head_report(self, f), upper_k=round(self.mau.upper_k.get(f, 1.0), 3))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
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
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
