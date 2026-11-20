#!/usr/bin/env python3
"""shot.py -- film 20 take s27 = shot 27, THE LAST IMAGE (g 1968..2045; 4-frame in-handle g 1964..1967; the film ends on a hard cut at 2046).
TOWER tower_window_pull / DAY 1889: crash pull-out from the lit first-floor restaurant window (Maupassant eating at his table, eyes shut,
smug) to the whole Eiffel Tower (tower_window_end framing).  The camera flies from 6 m in front of the glass to 236 m back, with a
log-like ease (the first frames are the fastest), and the last 12 frames drift almost still.
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(65.60), 2046                  # 1968 .. 2045
H = 4
G_FIRST, G_LAST = G0 - H, G1 - 1                 # 1964 .. 2045 (no out-handle: hard cut at the end of the film)
G_HOLD = 8                                       # g 1968..1975: near-still gentle drift on Maupassant, then the crash pull
G_PULL = (G0 + G_HOLD, 2033)                     # crash pull 1976..2033; 2034..2045 near still (12 frames)                          # the crash pull-out; 2034..2045 near still
G_WORD = C.cap_g("สักครั้ง")                     # 2020: last word
PRESET = "tower_window_pull"
PPD = 256
CLOSE = 0.0
LOOK_DROP = 0.0
CANVAS = cast20.CANVAS20["maupassant"]


def cam_dicts(A):
    return A["cams"]["tower_window_in"], A["cams"]["tower_window_end"]      # start = the set builder's tower_window_in (55 mm medium)


def cam_at(A, g):
    """(loc, look, shift_y) at film frame g.  Crash pull: u runs 0 -> 1 over G_PULL with a fast start / slow finish; the camera moves
    along log-distance (geometric), the aim sweeps from the window to the tower's mid height, the lens shift blends 0 -> end shift."""
    a, b = cam_dicts(A)
    u = min(1.0, (g - G_PULL[0]) / float(G_PULL[1] - G_PULL[0]))
    hold = 0.006 * (min(g, G_PULL[0]) - G0) / float(G_HOLD)                        # gentle drift while he is read (also backwards in the handle)
    if u <= 0:
        e = hold
    else:
        ease = min(1.0, u / 0.09) ** 2 * (3 - 2 * min(1.0, u / 0.09)) if u < 0.09 else 1.0     # smooth ease-in over ~5 frames
        e = hold + (1.0 - (1.0 - u) ** 1.9) * ease                                  # crash ease-out: the fast part lasts only a few frames
    la, lb = Vector(a["loc"]) + Vector((0.0, CLOSE, 0.0)), Vector(b["loc"])
    pa, pb = Vector(a["look_at"]), Vector(b["look_at"])
    # distance to the tower (y axis) in log space, x/z linear in the same fraction
    ya, yb = abs(la.y), abs(lb.y)
    d = ya * (yb / ya) ** e
    f = (d - ya) / (yb - ya)
    loc = la.lerp(lb, f)
    pa = pa - Vector((0.0, 0.0, LOOK_DROP))
    look = pa.lerp(pb, max(f, 0.0) if f < 0 else f)
    if f < 0:
        loc = la.lerp(lb, f * 0.12)
    sh = lerp(a.get("shift", 0.0), b.get("shift", 0.0), f)
    # after the pull: a gentle residual drift (never parked), 0.15 %/s ...
    t_after = max(0.0, (g - G_PULL[1]) / 30.0)
    loc = loc + Vector((0.0, -1.0, 0.0)) * (1.2 * t_after)
    lens = lerp(a.get("lens", 22.0), b.get("lens", 22.0), min(1.0, max(0.0, f) / 0.35) if f > 0 else 0.0)   # 55 mm medium -> 22 mm wide inside the first third of the pull
    return loc, look, sh, lens


def dress_table():
    """fine runtime detail on his window table (director: more fine interior detail at the start framing): fruit bowl with 14 fruits, 4 candles with flames,
    a wine bottle + cork, 8 cutlery rods, bread rolls.  Table top is at the cloth (furn_i_clothtop) z; centre = the table in front of him."""
    import bpy, math
    top = [o for o in bpy.data.objects if o.name == "furn_i_clothtop"]
    z0 = 110.33
    cx, cy = 0.0, -67.2
    def mat(name, col, em=0.0):
        m = bpy.data.materials.new(name); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = col; b.inputs["Roughness"].default_value = 0.5
        if em:
            b.inputs["Emission Color"].default_value = col; b.inputs["Emission Strength"].default_value = em
        return m
    mats = dict(wine=mat("d_wine", (0.05, 0.12, 0.05, 1)), gold=mat("d_gold", (0.85, 0.65, 0.2, 1)), orange=mat("d_orange", (0.95, 0.45, 0.05, 1)),
                red=mat("d_red", (0.7, 0.08, 0.06, 1)), yellow=mat("d_yellow", (0.95, 0.8, 0.2, 1)), bread=mat("d_bread", (0.75, 0.5, 0.25, 1)),
                flame=mat("d_flame", (1.0, 0.7, 0.2, 1), 8.0), white=mat("d_white", (0.95, 0.95, 0.9, 1)))
    def add(kind, m, loc, size, rot=(0, 0, 0)):
        if kind == "sph":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=loc, segments=12, ring_count=8)
        else:
            bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, location=loc, vertices=10)
        ob = bpy.context.active_object; ob.scale = size; ob.rotation_euler = rot; ob.data.materials.append(mats[m]); ob.name = "dress_" + m
        return ob
    # fruit bowl centre
    add("cyl", "gold", (cx, cy, z0 + 0.05), (0.42, 0.42, 0.10))
    for i in range(14):
        a = i * 2.4; r = 0.10 + 0.22 * ((i % 5) / 5.0)
        add("sph", ("orange", "red", "yellow")[i % 3], (cx + r * math.cos(a), cy + r * math.sin(a), z0 + 0.13 + 0.07 * (i % 3)), (0.085, 0.085, 0.085))
    # wine bottle + cork and four candles
    add("cyl", "wine", (cx + 1.0, cy + 0.15, z0 + 0.32), (0.09, 0.09, 0.64)); add("cyl", "white", (cx + 1.0, cy + 0.15, z0 + 0.68), (0.035, 0.035, 0.10))
    for sx in (-1, 1):
        for sy in (-0.9, 0.9):
            add("cyl", "white", (cx + sx * 0.85, cy + sy * 0.55, z0 + 0.14), (0.035, 0.035, 0.28)); add("sph", "flame", (cx + sx * 0.85, cy + sy * 0.55, z0 + 0.32), (0.03, 0.03, 0.055))
    # cutlery rods + bread rolls in a ring
    for i in range(8):
        a = i * math.pi / 4.0 + 0.2; r = 1.05
        add("cyl", "gold", (cx + r * math.cos(a), cy + r * math.sin(a), z0 + 0.012), (0.012, 0.012, 0.32), (math.pi / 2, 0, a))
    for i in range(4):
        a = i * math.pi / 2.0 + 0.7
        add("sph", "bread", (cx + 0.78 * math.cos(a), cy + 0.78 * math.sin(a), z0 + 0.07), (0.14, 0.10, 0.07))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light="DAY", quality=quality, name="cam_s27")
        for ob in C.bpy.data.objects:                      # the preset FG (iron post, 1 m ahead of the PRESET camera) rides with our closer start
            if ob.name.startswith(("fg_", "shade_casters")):
                if ob.name.startswith("fg_"):
                    ob.hide_render = True                  # director F1: the iron post slashing the opening is hidden
                    print("hid FG", ob.name, flush=True)
        dress_table()
        self.scene.frame_set(bf(G_FIRST))
        self.key_cam(bf(G_FIRST), *cam_at(self.A, G_FIRST)[:2])
        self.cam.data.lens = cam_at(self.A, G_FIRST)[3]
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.0, depth=0.4, opacity=0.5), cam=self.cam)

    def pose(self, gs):
        mark = self.A["marks"]["maupassant_window"]
        for g in gs:
            f = bf(g)
            loc, look, sh, lens = cam_at(self.A, g)
            self.key_cam(f, loc, look)
            self.cam.data.shift_y = sh
            self.cam.data.keyframe_insert("shift_y", frame=f)
            self.cam.data.lens = lens
            self.cam.data.keyframe_insert("lens", frame=f)
            C.place(self.mau, f, mark)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mau.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.mau, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look, sh, lens = cam_at(self.A, g)
        return dict(g=g, cam=[round(c, 2) for c in loc], shift=round(sh, 3), lens=round(lens, 1), heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def pose_of(g):
    """eating blissfully with his eyes shut (smug_shut): the fork hand travels plate -> mouth on a ~1.3 Hz cycle (never still)."""
    p = dict(cast20.STORY20["maupassant_seated_eat_chew"][1])
    cyc = 0.5 - 0.5 * math.cos(2 * math.pi * 1.3 * g / 30.0)
    p.update(seated=1, seat_h=SEAT_H, yaw=0.35, expr="smug_shut", mouth="smile")
    p["arm_r"] = dict(hand=(lerp(0.55, 0.62, cyc), lerp(0.98, 0.60, cyc)), bend=lerp(0.3, -0.2, cyc))
    p["prop_r"] = dict(type="fork20", angle=lerp(-30, -155, cyc))
    p["pitch"] = -0.15
    p["head_roll"] = 3.0 + 1.8 * math.sin(g * 0.2)
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.3))
    p["t"] = g / 30.0
    return p


SEAT_H = 0.865
if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        print("marks", {k: v for k, v in Tk.A["marks"].items() if "window" in k}, "cams", Tk.A["cams"][PRESET], Tk.A["cams"]["tower_window_end"])
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
