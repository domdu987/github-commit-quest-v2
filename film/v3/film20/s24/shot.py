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
G_BITE = 1830                                   # the first bite (fork at the mouth) lands with the camera (g 1824-1830)
PRESET, LIGHT = "tower_window_pull", "DAY"
SEAT_H, PPD = 0.865, 256
CANVAS = cast20.CANVAS20["maupassant"]

# ---- camera in metres, tower-local (x right, y toward Paris/camera side = -y, z up); window table at (0, -35.8, 58.65), glass y = -36.8
TGT = Vector((0.0, -35.4, 59.2))                 # aim point: his head height
START_OFF = Vector((float(os.environ.get("X0", "-8.0")), -float(os.environ.get("Y0", "17.0")), float(os.environ.get("Z0", "4.0"))))   # camera start relative to TGT (m): oblique, high, left
END_DIR = Vector((0.0, -1.0, 0.10)).normalized()                       # landing direction: eye level, straight through the clear pane
AIM_DROP = float(os.environ.get('AIM_DROP', '0.05'))                     # m: the landing aim sits a little below his head
AIM_X = float(os.environ.get('AIM_X', '0.07'))                             # m: aim slightly right of him so his head sits at x ~0.46 W
W0, W1 = float(os.environ.get("W0", "33.5")), float(os.environ.get("W1", "268.0"))      # head width px: ~3.5 % of frame height figure at g 1736 -> ~40 % at the landing
G_ZERO, G_LAND = 1738, 1834                      # steady exponential zoom (figure 5 % at g 1738 -> 35 % at g ~1829 = 3.0 s, 38 % at the landing), then a slow drift to the cut
LENS_AT_LAND = 55.0


def smooth(u):
    u = clamp(u)
    return u * u * u * (u * (6 * u - 15) + 10)    # smootherstep


def ease(g):
    """zoom progress e(g): 0 at G_ZERO, 1 at G_LAND; steady (70 % linear + 30 % smootherstep: eased at the end, already moving at the start); < 0 before, > 1 after."""
    u = (g - G_ZERO) / float(G_LAND - G_ZERO)
    if u <= 0:
        return 0.7 * u
    if u >= 1:
        return 1.0 + 0.05 * (u - 1.0)
    return 0.7 * u + 0.3 * smooth(u)


M_END = float(os.environ.get("M_END", "1.24"))                           # r9: the landing is ~1.2x closer (independent hair-to-tabletop measure was 6-7 points lower than the sprite estimate)
DRIFT = float(os.environ.get("DRIFT", "0.06"))                          # slow push after the landing, 6 %/s
G_M0, G_M1 = 1804, 1822                                                 # g <= 1804 is identical to the r7 render (the move stays continuous)


def closer(g):
    """1.0 up to g 1804, then eases to M_END by g 1830 and keeps the zoom going (no stop): the end pose is closer, the early move is untouched."""
    return 1.0 + (M_END - 1.0) * smooth((g - G_M0) / float(G_M1 - G_M0))


def width_at(g):
    """apparent head width px: exponential in e(g) (constant zoom rate), + a slow 12 %/s drift push after the landing."""
    e = ease(g)
    w = W0 * (W1 / W0) ** e if e <= 1.0 else W1 * (1.0 + DRIFT * (g - G_LAND) / 30.0)
    return w * closer(g)


def lens_at(g):
    """22 mm early; eases to the preset tower_window_in lens (55 mm) from e 0.35 to 1.0."""
    e = clamp(ease(g))
    return 22.0 * (LENS_AT_LAND / 22.0) ** smooth((e - 0.35) / 0.65)


def cam_at(g):
    """(loc, look) in world D at film frame g: distance solved from the wanted head width and the lens, direction blended oblique -> frontal."""
    e = clamp(ease(g))
    lens = lens_at(g)
    dist_d = 782.2 * (lens / 22.0) / width_at(g)                         # D: head = 1 D wide
    dir0 = START_OFF.normalized()
    k = smooth(e)
    dr = (dir0 * (1 - k) + END_DIR * k).normalized()
    tgt_d = Vector(CO.W(tuple(TGT)))
    loc = tgt_d + dr * dist_d
    aim = tgt_d + Vector((AIM_X * CO.SC * k, 0.0, -AIM_DROP * CO.SC * k))
    return loc, aim


ROOM_BOX = ((-3.6, -34.45, 57.95), (3.6, -17.0, 63.0))         # tower-local metres: behind the glass, behind him
ROOM_KILL = tuple(os.environ.get('ROOM_KILL', 'tower_ironlt_t').split(','))
GLOW = float(os.environ.get('GLOW', '0.0'))              # no opaque glow panel: the window stays clear glass, his lit table shows through
EXPO_FAR, EXPO_NEAR = float(os.environ.get("EXPO_FAR", "-0.85")), float(os.environ.get("EXPO_NEAR", "-0.55"))


def expo_at(g):
    """grade exposure follows the distance: the sunlit exterior is bright (-1.3 EV), the lamp-lit room darker (-0.35 EV): keeps luma ~95 through the zoom."""
    d = (cam_at(g)[0] - Vector(CO.W(tuple(TGT)))).length / CO.SC
    k = clamp(math.log(20.0 / max(d, 1.0)) / math.log(20.0 / 4.0))
    bump = 0.35 * math.exp(-((math.log(max(d, 0.5)) - math.log(6.0)) / 0.5) ** 2)      # the dark facade / ceiling while the camera crosses the window
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
        self.clear_room_wedges()
        if GLOW > 0:
            self.make_glow()
        self.key_cam(bf(G_FIRST), *cam_at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.1, depth=0.5, opacity=0.5), shadow=None, cam=self.cam)

    def clear_box(self, box, names):
        import bmesh
        lo, hi = Vector(CO.W(box[0])), Vector(CO.W(box[1]))
        n = 0
        for o in C.bpy.data.objects:
            if o.type != "MESH" or not o.name.startswith(names):
                continue
            bm = bmesh.new(); bm.from_mesh(o.data); mw = o.matrix_world
            dead = []
            for f in bm.faces:
                ws = [mw @ v.co for v in f.verts]
                if all(min(w[k] for w in ws) <= hi[k] and max(w[k] for w in ws) >= lo[k] for k in range(3)):
                    dead.append(f)
            if dead:
                bmesh.ops.delete(bm, geom=dead, context="FACES"); n += len(dead)
                bm.to_mesh(o.data); o.data.update()
            bm.free()
        return n

    def clear_room_wedges(self):
        """the tilted flat iron members (object tower_ironlt_t) that stand just behind Maupassant inside the room copy read as a chevron / X of orange planes
        behind his head from the landing camera: delete the faces of tower_ironlt_t inside the room box (behind the glass, behind him) only: the exterior
        lattice (y < -36 m) is untouched, so the approach frames keep their tower."""
        import bmesh
        C.bpy.context.view_layer.update()
        lo, hi = Vector(CO.W(ROOM_BOX[0])), Vector(CO.W(ROOM_BOX[1]))
        n = 0
        for o in C.bpy.data.objects:
            if o.type != "MESH" or not o.name.startswith(ROOM_KILL):
                continue
            bm = bmesh.new(); bm.from_mesh(o.data); mw = o.matrix_world
            dead = []
            for f in bm.faces:
                ws = [mw @ v.co for v in f.verts]
                if all(min(w[k] for w in ws) <= hi[k] and max(w[k] for w in ws) >= lo[k] for k in range(3)):      # the face's bounding box meets the room box
                    dead.append(f)
            if dead:
                bmesh.ops.delete(bm, geom=dead, context="FACES"); n += len(dead)
                bm.to_mesh(o.data); o.data.update()
            bm.free()
        n += self.clear_box(((-1.9, -42.0, 57.0), (1.9, -36.2, 58.6)), ("gallery_ironlt",))      # the flat gallery slab outside the sill (an orange strip with a black seam) in the landing view
        n += self.clear_box(((-3.7, -38.9, 62.9), (-2.5, -37.7, 64.1)), ("gallery_iron",))      # black unlit post caps beside the RESTAURANT sign (g 1724-1757)
        n += self.clear_box(((2.5, -38.9, 62.9), (3.7, -37.7, 64.1)), ("gallery_iron",))
        n += self.clear_box(((5.0, -34.0, 57.0), (40.0, -4.0, 64.0)), ("tower_ironlt_t",))        # black unlit tower members seen through the window to the right (g 1756-1784)
        print("clear_room_wedges: %d faces deleted" % n, flush=True)

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
            if GLOW > 0:
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
        hr = C.head_report(self, f)
        tb = CO.project(CO.W((0.0, -35.8, 58.65)))
        out = dict(g=g, lens=round(lens_at(g), 1), pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   dist_m=round((loc - Vector(CO.W(tuple(TGT)))).length / CO.SC, 1), heads=hr, upper_k=round(self.mau.upper_k.get(f, 1.0), 3))
        if "mau" in hr:
            h = hr["mau"]
            top = h["y"] - 0.62 * h["w"]
            out["fig_pct"] = round(100.0 * (tb[1] - top) / 1280.0, 1)          # visible figure: hair to tabletop
            out["table_y"] = round(float(tb[1]), 1)
            tbb = CO.project(CO.W((0.0, -35.8 + 0.70, 58.65)))                    # the far (back) edge of the cloth top: the edge a viewer reads as "the table"
            out["fig_pct_back"] = round(100.0 * (tbb[1] - top) / 1280.0, 1)
        return out

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
