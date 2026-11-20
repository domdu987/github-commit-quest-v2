#!/usr/bin/env python3
"""shot.py -- film 20 take s11 = shot 11, SITE site_fence / DAY stage 0 (nickname).  g 753..821 + in-handle 8 (g 745..752, dissolve 11
into this shot) + out-handle 4 (g 822..825; hard cut to shot 12).
"ไอ้ช่างหมุด": Parisians (lady with parasol, top-hat gentleman, child) at the building-site fence laugh and point at Eiffel, who holds
up a giant rivet.  A: eye level, pull back 8 %/s + slide; B: PUNCH-IN CUT at the nickname word (g 802) onto Eiffel + the rivet
(+ 2-frame shake, 6 frames of speed lines added by post.py), then a slow push to the cut.
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp] | hue g ..
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(25.09), C.g_bound(27.39)       # 753, 822
H_IN, H_OUT = 8, 4                                 # dissolve 11 -> 5.5 + 2 -> 8 ; cut side 4
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1        # 745 .. 825
GS = list(range(G_FIRST, G_LAST + 1))
G_NICK = C.cap_g("ไอ้ช่างหมุด")                     # event frame of the nickname (26.62 narr +0.10)
G_CALL = C.cap_g("เรียกไอเฟลว่า")                   # 778: 'they call Eiffel ...' -> snap push in A
G_PUNCH = G_NICK                                   # punch-in cut on this frame
G_SPEED = (G_PUNCH, G_PUNCH + 5)                   # 6 frames of speed lines (post.py)
G_SHAKE = (G_PUNCH, G_PUNCH + 1)
LIGHT, PRESET = "DAY", "site_fence"
PPD = 256
BARREL_BOX = (-15.5, -8.8, -107.5, -102.0, 2.0)       # the scatter barrels near the camera path (metres)
RIV_ANGLE = float(os.environ.get('RIVA', '90'))                                    # giant rivet held vertically, dome up (to be checked on stills)

# ---- staging (metres, site20 marks); cards at ground z 0
M_ = CO.W
LADY, GENT, CHILD = (-12.2, -101.1), (-10.9, -101.3), (-9.8, -101.2)      # outside the fence, y -103
EIF = (-7.9, -100.2)                                                      # inside, 7 m behind them


def mk(xy, A):
    return (CO.W((xy[0], xy[1], 0.0))[0], CO.W((xy[0], xy[1], 0.0))[1], 0.0)


# camera A: eye level, outside the fence at the left, pulling back; B: tight on Eiffel
CAM_A0 = (-14.6, -105.6, 1.0)          # metres, start
SUBJ_A = (-10.1, -100.6, 1.45)           # between the group and Eiffel
CAM_B0 = (-9.0, -103.4, 0.95)
SUBJ_B = (-7.9, -100.2, 1.6)


def cam_a():
    return C.CamPath(CO.W(CAM_A0), CO.W(SUBJ_A), G_FIRST, G_PUNCH - 1, push=-0.10, slide_px=-70.0, rise_px=-35.0, arc_deg_s=-2.0,
                     tilt0=6.5, tilt_deg_s=0.0, decay=0.25,
                     snaps=[dict(g=(G_CALL - 2, G_CALL + 14), k=1.4, peak=1.7, shift=(0.0, 0.0), tilt=1.5)])


def cam_b():
    return C.CamPath(CO.W(CAM_B0), CO.W(SUBJ_B), G_PUNCH, G_LAST, push=0.16, slide_px=110.0, rise_px=-30.0, arc_deg_s=6.0, tilt0=0.0,
                     tilt_deg_s=0.0, decay=0.3)


def cam_at(g, pa, pb):
    loc, look = (pa if g < G_PUNCH else pb).at(g)
    if G_SHAKE[0] <= g <= G_SHAKE[1]:                                   # 2-frame shake on the punch-in
        k = 1 if g == G_SHAKE[0] else -1
        d = Vector((0.0, 0.0, 0.05 * k))
        loc, look = loc + d, look + d * 0.3
    j = Vector((0.09 * math.sin(g * 1.9), 0.09 * math.cos(g * 1.3), 0.06 * math.sin(g * 2.3 + 1.0)))   # hand-held energy
    return loc + j, look + j * 0.4


def bounce(g, ph=0.0, amp=0.10, hz=3.0):
    return amp * 0.5 * (1.0 + math.sin(2 * math.pi * hz * g / 30.0 + ph))


def base(name):
    return dict(cast20.STORY20[name][1])


def pose_of(who, g):
    t = g / 30.0
    if who == "eiffel":
        p = base("eiffel_giant_rivet")
        p["expr"] = "proud" if g < G_PUNCH else "determined"
        up = 0.5 + 0.5 * math.sin(t * 3.0)
        p["arm_r"] = dict(hand=(1.0, -0.35 + 0.22 * up), bend=-0.1, stretch=1.4)       # the rivet bobs up and down in his fist
        p["prop_r"] = dict(p["prop_r"]); p["prop_r"]["angle"] = RIV_ANGLE + 7 * math.sin(t * 3.0); p["prop_r"]["scale"] = 1.8
        p["yaw"] = -0.45 + 0.04 * math.sin(t * 1.7)                                         # faces screen-left, to the Parisians
        p["lean"] = 4.0 * math.sin(t * 2.6)
        p["blink"] = blink(g, [757, 790, 812])
    else:
        p = base({"lady": "lady_parasol", "gent": "gent_cane", "child": "child_point"}[who])
        p["expr"] = "laughing20"
        ph = {"lady": 0.0, "gent": 1.3, "child": 2.4}[who]
        s = math.sin(2 * math.pi * 3.0 * t + ph)
        p["squash"] = (1.0 + 0.02 * s, 1.0 - 0.02 * s)
        p["yaw"] = 0.5 + 0.05 * math.sin(t * 2.0 + ph)
        p["head_roll"] = 4.0 * math.sin(2 * math.pi * 1.5 * t + ph)
        p["lean"] = 2.0 * math.sin(2 * math.pi * 3.0 * t + ph)
        if who == "gent":
            p["arm_r"] = dict(hand=(0.9, 0.1), shape="point", bend=-0.4, stretch=1.25)          # pointing at Eiffel (cane under the arm)
            p.pop("prop_r", None)
            p["prop_l"] = dict(type="cane20", angle=75, scale=0.7); p["arm_l"] = "hip"
        if who == "lady":
            p["arm_l"] = dict(hand=(0.1, -0.2 + 0.05 * s), bend=0.6, shape="open")             # hand at her mouth while she laughs
        if who == "child":
            p["arm_r"] = dict(hand=(0.75, -0.1 + 0.05 * s), shape="point", bend=-0.5, stretch=1.3)
    p["t"] = t
    p["blink"] = p.get("blink", blink(g, [760 + 11 * ("lady gent child".split().index(who) if who != "eiffel" else 0)]))
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s11")
        self.pa, self.pb = cam_a(), cam_b()
        self.clear_box(BARREL_BOX)
        self.add_fg()
        self.add_girders()
        self.key_cam(C.bf(G_FIRST), *cam_at(G_FIRST, self.pa, self.pb))
        self.scene.frame_set(C.bf(G_FIRST))
        self.marks = dict(lady=mk(LADY, self.A), gent=mk(GENT, self.A), child=mk(CHILD, self.A), eiffel=mk(EIF, self.A))
        for k in self.marks:
            self.marks[k] = C.on_ground(self.marks[k])
        for who, cast in (("lady", "lady20"), ("gent", "gent20"), ("child", "child20"), ("eiffel", "eiffel")):
            self.actors[who] = C.make_actor(who, cast, os.path.join(WORK, "sprites"), cam=self.cam,
                                            contact=dict(width=1.2, depth=0.5, opacity=0.8))

    def clear_box(self, box=None):
        """hide the preset's NEAR prop band (pn_*: the scatter barrels / sacks around the preset camera): they are merged meshes and would
        stand in front of my cast.  The mid / far props (pm_, pf_) stay."""
        n = 0
        for ob in C.bpy.data.objects:
            if ob.name.startswith("pn_"):
                ob.hide_render = True
                n += 1
        print("clear_box: %d pn_ objects hidden" % n, flush=True)

    def add_fg(self):
        """the preset FG (one mesh: post + high rail) belongs to the preset camera: hide it, build a timber post at the lens's left edge
        (1.5 D ahead) in the camera A frame; it stays in the world (camera pulls away from it = parallax)."""
        for ob in C.bpy.data.objects:
            if ob.name.startswith("fg_"):
                ob.hide_render = True
        C.bpy.ops.mesh.primitive_cube_add(size=1.0)
        ob = C.bpy.context.active_object
        ob.name = "fg_post_s11"
        ob.scale = (0.16, 2.6, 0.16)
        ob.parent = self.cam                                     # camera-relative: stays at the lens's left edge, 1.7 D ahead
        ob.location = (-0.78, -0.35, -1.7)
        ob.rotation_euler = (0.0, 0.0, math.radians(4.0))
        ob.data.materials.append(CO.STATE["M"]["timber"])

    def add_girders(self):
        """two red-lead girders lying on the ground bottom-right of frame A (world fixed, 3-5 D from the lens): fills the empty ground"""
        loc, look = self.pa.at(G_FIRST)
        d_ = look - loc
        f = Vector((d_.x, d_.y, 0.0)).normalized()
        r = Vector((f.y, -f.x, 0.0))
        for i, (fw, rt, ln, rot) in enumerate(((4.6, 1.7, 3.4, 0.28), (5.6, 3.1, 3.0, 0.45))):
            c = loc + f * fw + r * rt
            C.bpy.ops.mesh.primitive_cube_add(size=1.0)
            ob = C.bpy.context.active_object
            ob.name = "fg_girder_s11_%d" % i
            ob.scale = (0.30 * CO.SC, ln, 0.34 * CO.SC)
            ob.location = (c.x, c.y, 0.17 * CO.SC)
            ob.rotation_euler = (0, 0, math.atan2(f.y, f.x) - math.pi / 2 + rot)
            ob.data.materials.append(CO.STATE["M"]["redlead"])

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g, self.pa, self.pb))
            for who, a in self.actors.items():
                m = list(self.marks[who])
                if who != "eiffel":
                    m[2] += bounce(g, {"lady": 0.0, "gent": 1.3, "child": 2.4}[who])
                C.place(a, f, m)
            self.key_set(f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for who, a in self.actors.items():
                a.pose(f, pose_of(who, g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        Tk = Take("preview")
        for P, a, b in ((Tk.pa, G_FIRST, G_PUNCH - 2), (Tk.pb, G_PUNCH, G_LAST - 1)):
            rows, worst = P.report(range(a, b + 1))
            print(min(r["px"] for r in rows), max(r["px"] for r in rows), "longest parked", worst)
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
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
