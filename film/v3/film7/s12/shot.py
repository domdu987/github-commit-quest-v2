#!/usr/bin/env python3
"""shot.py -- film 7 take s12: shots 12-13 (plan 37.12-44.53 s = g 1114..1335) + 6-frame handles (g 1108..1341).

Shot 12 (g 1114..1214, louvre wall_eye area, GALLERY_DAY, Monday: the museum closed and empty)
    id 1  A1 g 1108..1159  wide from the rope: vincenzo in the white smock walks in from screen-right along the back wall, glancing
                           back over his shoulder, stops under the small Mona Lisa and looks up at her.  Slow push.
          A2 g 1160..1194  CUT, low from the left: he checks left / right (sweat), then reaches up; both hands land on the frame's
                           side edges (pinned to the 3D frame, world points) on "...แบบเดียวกัน".
          A3 g 1195..1220  CUT, low close on the painting: "ยกภาพลงจากผนัง" (39.87 s = g 1199): he lifts the framed painting off its
                           hooks (L.set_mona_lift 0 -> 0.36, g 1197..1211), the four iron hooks come free under it; hold (handle).
Shot 13 (g 1215..1335, louvre staircase area, STAIR_MORNING)
    id 2  B1 g 1209..1255  from the foot of the service stair: he hurries down the flight toward us with the framed painting at
                           his side (cast7 prop mona_framed), glancing back up; set_frame_on_stairs False ("เดินเข้าบันไดหนีไฟ").
          B2 g 1256..1289  CUT, from the lower right: crouched on the steps beside the empty gilt frame and her glass box (set_frame
                           _on_stairs True), the bare panel in his hands ("แกะกรอบทิ้ง" 41.98 s = g 1262), a glance up the stairs.
          B3 g 1290..1341  CUT, front medium, slow push in: he stands, slides the panel under the smock ("แล้วซุกภาพไว้ใต้เสื้อ"
                           42.84 / 43.60 s): the prop goes, the bulge comes (bulge 0 -> 1, g 1300..1309), both hands press it
                           flat, a sly smirk up the stairs.  Out-handle g 1336..1341.
Mouths: nobody speaks (no quoted line): static expression mouths only.  NO depth of field (C.Take).
Blender frame of g = g + 1 (one location per process).

    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0, G1 = C.g_bound(37.12), C.g_bound(44.53)        # 1114, 1336
G12_END = C.g_bound(40.50)                          # 1215: shot 13 starts
H = 6
A2, A3 = 1160, 1195
B2, B3 = 1256, 1290
RANGES = {1: (G0 - H, G12_END - 1), 2: (G12_END, G1 + H - 1)}       # gallery 1108..1214, stair 1215..1341
SHOT_RANGES = {12: (G0, G12_END - 1), 13: (G12_END, G1 - 1)}
LOC = {1: ("louvre", "wall_eye"), 2: ("louvre", "staircase")}
G_LIFT = (1197, 1211)
LIFT_D = 0.32
G_PANEL_OUT, G_BULGE = (1256, 1268), (1300, 1309)
FP = lambda g: g + 1                                # Blender frame of g


def setup_of(g, shot):
    if shot == 1:
        return "A1" if g < A2 else ("A2" if g < A3 else "A3")
    return "B1" if g < B2 else ("B2" if g < B3 else "B3")


# ----------------------------------------------------------------------------- gallery (shot 12)
MONA = Vector((0.0, 21.92, 3.55))
VIN_STOP = Vector((0.0, 21.0, 0.0))
WALK_A = 0.072                                     # D / frame, toward screen-left (-x)
G_STOP = 1148
EDGE_Z = 2.92                                      # where his hands take the frame's side edges (frame bottom 2.62)
EDGE_X = 0.71
FRAME_FRONT_Y = 21.62


def vin_a(g):
    if g >= G_STOP:
        return VIN_STOP
    d = G_STOP - g
    s = d - 2.0 if d > 4 else d * d / 8.0           # eases to the stop
    return VIN_STOP + Vector((WALK_A * s, 0.0, 0.0))


def lift_at(g):
    u = ez((g - G_LIFT[0]) / float(G_LIFT[1] - G_LIFT[0]))
    return LIFT_D * u + (0.012 * math.sin((g - G_LIFT[1]) * 0.5) if g > G_LIFT[1] else 0.0)


def frame_edge(side, g):
    """world point on the frame's side edge (side -1 screen-left / +1 right) at lift(g)."""
    d = lift_at(g)
    return Vector((side * EDGE_X, FRAME_FRONT_Y - 0.9 * d, EDGE_Z + 0.6 * d))


LZ1, LZ2, LZ3 = (float(os.environ.get(k, v)) for k, v in (("LZ1", 2.8), ("LZ2", 2.75), ("LZ3", 2.9)))
CAMS_A = {
    "A1": (((2.30, 15.6, 2.55), (0.15, 21.9, LZ1), 22.0), ((1.95, 16.4, 2.50), (0.05, 21.9, LZ1), 22.0)),
    "A2": (((-1.35, 16.9, 1.95), (0.15, 21.8, LZ2), 22.0), ((-1.15, 17.3, 1.95), (0.12, 21.8, LZ2), 22.0)),
    "A3": (((0.85, 17.3, 1.85), (-0.05, 21.8, LZ3), 22.0), ((0.78, 17.6, 1.85), (-0.05, 21.8, LZ3), 22.5)),
}
SPAN = {"A1": (1108, 1159), "A2": (1160, 1194), "A3": (1195, 1220), "B1": (1209, 1255), "B2": (1256, 1289), "B3": (1290, 1341)}


def cam_lin(s, g):
    a, b = SPAN[s]
    u = ez((g - a) / float(b - a), "sine")
    (l0, k0, f0), (l1, k1, f1) = CAMS[s]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lerp(f0, f1, u)


def vin_pose_a(g):
    p = None
    if g < G_STOP:
        ph = g / 28.0
        u = clamp((G_STOP - g) / 6.0)                          # eases out of the stride into the stop
        base = dict(expr="worried", sweat=0.15, yaw=lerp(0.15, 0.45, u), gaze=(lerp(0.0, 0.85, u), lerp(-0.6, 0.0, u)),
                    head_roll=4, pitch=lerp(-0.35, -0.05, u))
        p = cast7.cycle("vincenzo_smock", ph, "walk", facing=-1, base=base, speed=lerp(0.3, 0.8, u))
        if isinstance(p.get("legs"), dict) and u < 1.0:
            p["legs"] = dict(p["legs"], stride=p["legs"]["stride"] * u, lift_r=p["legs"]["lift_r"] * u, lift_l=p["legs"]["lift_l"] * u)
        p["blink"] = blink(g, [1122, 1145])
    else:
        # stands under her, looks up; A2: glances left / right, then reaches up
        p = dict(expr="worried" if g < 1178 else "determined", sweat=lerp(0.15, 0.6, clamp((g - 1150) / 30.0)), legs="narrow",
                 mirror=True, yaw=0.18, pale=0.1)
        if g < 1162:
            p.update(pitch=-0.55, gaze=(0.0, -0.9), head_roll=-3)
        elif g < 1178:                                         # look left .. right (eyes + head)
            k = (g - 1162) / 16.0
            p.update(pitch=-0.05, gaze=((-0.9 if k < 0.5 else 0.9), 0.0), yaw=(0.45 if k < 0.5 else -0.25), head_roll=2)
        else:
            p.update(pitch=-0.6, gaze=(0.0, -0.95), head_roll=-4, lean=-3)
        p["arm_r"] = dict(hand=(0.20, 1.02), bend=0.6)
        p["arm_l"] = dict(hand=(-0.20, 1.02), bend=0.6)
        p["blink"] = blink(g, [1170, 1205])
        if g >= 1200:
            p["expr"] = "determined"; p["sweat"] = 0.7
    p["t"] = g / 30.0
    return p


def reach_u(g):
    return ez((g - 1178) / 12.0) if g >= 1178 else 0.0


# ----------------------------------------------------------------------------- staircase (shot 13)
RUN, RISE = 0.6, 0.36


def step_z(y):
    if y < 0:
        return 0.0
    return (int(y / RUN) + 1) * RISE


def slope_z(y):
    """smooth descent line just above the nosings (a card has no feet that find the treads)."""
    return max(0.0, y / RUN * RISE + 0.18)


B1_Y0, B1_Y1 = 8.9, 4.7
VIN_B = Vector((1.20, 3.30, step_z(3.30)))           # step 5 (z 2.16): crouch / stand beside the frame


def vin_b(g):
    if g < B2:
        u = (g - SPAN["B1"][0]) / float(B2 - 1 - SPAN["B1"][0])
        y = lerp(B1_Y0, B1_Y1, u)
        x = lerp(0.15, 0.55, u)
        z = min(5.04, y * RISE / RUN + RISE)
        return Vector((x, y, z))
    return VIN_B


CAMS_B = {
    "B1": (((0.80, -1.0, 3.2), (0.15, 8.0, 5.6), 26.0), ((0.80, -0.2, 3.2), (0.30, 7.0, 5.15), 26.0)),
    "B2": (((1.50, 0.55, 3.45), (0.45, 3.9, 3.95), 22.0), ((1.42, 0.85, 3.42), (0.45, 3.9, 4.0), 23.0)),
    "B3": (((1.20, -0.30, 4.05), (1.10, 3.6, 4.25), 25.0), ((1.20, 0.55, 4.00), (1.12, 3.6, 4.45), 26.0)),
}
CAMS = dict(CAMS_A); CAMS.update(CAMS_B)
WIDE = (-2.5, -4.6875, 2.5, 0.125)                   # the framed painting carried at his side does not fit the default canvas


def vin_pose_b(g):
    s = setup_of(g, 2)
    if s == "B1":
        ph = (g - SPAN["B1"][0]) / 20.0 + 0.1        # hurried steps down
        base = dict(expr="worried", sweat=0.7, pale=0.2, yaw=0.22, gaze=(-0.8 if (g // 9) % 2 == 0 else 0.0, -0.3), head_roll=-4,
                    pitch=0.05, panel_grip="side", panel_side=1)
        p = cast7.cycle("vincenzo_smock", ph, "walk", facing=1, base=base, arms="l", speed=0.9)
        p["arm_r"] = dict(hand=(0.62, 1.18), bend=-0.2, stretch=1.15)
        p["prop_r"] = dict(type="mona_framed", scale=1.85)
        p["blink"] = blink(g, [1230])
    elif s == "B2":
        k = clamp((g - G_PANEL_OUT[0]) / float(G_PANEL_OUT[1] - G_PANEL_OUT[0]))
        p = dict(expr="determined", sweat=0.8, pale=0.2, yaw=0.30, pitch=lerp(0.45, 0.15, k), head_roll=-4, lean=lerp(10, 4, k),
                 gaze=(0.3, 0.7) if g < 1276 else (-0.6, -0.8), legs=dict(preset="crouch", crouch=0.22),
                 panel_grip="bottom", panel_side=0)
        p["arm_r"] = dict(hand=(lerp(0.30, 0.18, k), lerp(1.55, 0.98, ez(k))), bend=-0.3, stretch=1.2, layer="front")
        p["prop_r"] = dict(type="mona_panel", scale=2.0)
        p["arm_l"] = dict(hand=(lerp(-0.30, -0.36, k), lerp(1.55, 1.0, ez(k))), bend=0.4, layer="front")
        if g >= 1276:
            p["expr"] = "worried"; p["pitch"] = -0.25; p["head_roll"] = 5
        p["blink"] = blink(g, [1275])
    else:
        up = ez((g - B3) / 6.0)                        # rises out of the crouch
        k = ez((g - 1292) / 8.0)                       # panel to the belly
        b = ez((g - G_BULGE[0]) / float(G_BULGE[1] - G_BULGE[0]))
        p = dict(expr="worried" if g < 1312 else "smirk", sweat=lerp(0.8, 0.5, clamp((g - 1310) / 20.0)), pale=0.15,
                 yaw=lerp(0.30, 0.20, up), pitch=lerp(0.15, 0.1, up), head_roll=lerp(-4, 4, b), lean=lerp(4, 0, up),
                 gaze=(-0.75, -0.35) if g >= 1312 else (0.0, 0.6), bulge=b,
                 legs=dict(preset="crouch", crouch=0.22 * (1 - up)) if up < 1 else "narrow",
                 panel_grip="bottom", panel_side=0)
        if g < G_BULGE[0] + 3:
            p["prop_r"] = dict(type="mona_panel", scale=2.0)
            hy = lerp(0.98, 1.30, k) + 0.30 * ez((g - G_BULGE[0] + 1) / 3.0)
            lay = "front" if g < G_BULGE[0] else "back"       # the panel slides down BEHIND the smock front: the tuck
            p["arm_r"] = dict(hand=(0.18, hy), bend=-0.3, stretch=1.2, layer=lay)
            p["arm_l"] = dict(hand=(-0.36, hy + 0.02), bend=0.4, layer=lay)
        else:
            p["arm_r"] = dict(hand=(0.22, 0.95), bend=0.7, shape="open", layer="front")
            p["arm_l"] = dict(hand=(-0.20, 1.02), bend=0.7, shape="open", layer="front")
        if g >= 1318:
            p["pitch"] = -0.15
        p["blink"] = blink(g, [1303, 1328])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- runtime dressing
def dress_gallery():
    """nothing to fix in wall_eye's hang; a worker's dust sheet and a bucket by the wall (Monday maintenance) to fill the floor
    left of her in the low angles."""
    S = L.STATE; M = S['M']; SET = S['SET']
    mb = L.MB()
    L.lumpy(mb, (-2.2, 21.3, 0.25), 0.55, M['rag'], 12, seg=10, rings=5, rough=0.25, squash=0.55)
    L.rod(mb, (-1.55, 21.2, 0), (-1.55, 21.2, 0.62), 0.27, M['zinc'], seg=12, r1=0.32)
    L.chain_rod(mb, [(-1.87, 21.2, 0.62), (-1.55, 21.2, 0.95), (-1.23, 21.2, 0.62)], 0.015, M['iron'])
    L._obj(mb, 's12_dressing', SET, hull=0.012)
    for ob in SET.objects:
        if ob.name.startswith('s12_'):
            L.no_bounce(ob)
    unhook_rope()


def unhook_rope():
    """Monday, museum closed: the red rope in front of her is unhooked (it crossed his face in the low angles).  Deletes the rope
    faces of the two catenaries x -0.9..2.6 (y 20.4) and the two right-hand stanchions (x 0.9, 2.6: one crossed his face in A1) from
    this scene's gallery_dressing mesh; the left stanchions and their rope span stay."""
    import bmesh
    ob = bpy.data.objects.get('gallery_dressing')
    bm = bmesh.new(); bm.from_mesh(ob.data)
    mw = ob.matrix_world
    kill = []
    for fc in bm.faces:
        c = mw @ fc.calc_center_median()
        if 20.25 < c.y < 20.56 and 1.3 < c.z < 2.45 and -0.75 < c.x < 2.45 and abs(c.x - 0.9) > 0.22:
            kill.append(fc)
        elif any((c.x - sx) ** 2 + (c.y - 20.4) ** 2 < 0.55 ** 2 for sx in (0.9, 2.6)) and c.z < 2.8:
            kill.append(fc)                          # the two right-hand stanchions, set aside with the rope
    bmesh.ops.delete(bm, geom=kill, context='FACES')
    bm.to_mesh(ob.data); bm.free()
    print("s12: rope faces removed", len(kill), flush=True)


def dress_stair():
    """the flight is bare stone: a workman's bucket and rag on the bottom step, a coil of rope and a broom against the right wall."""
    S = L.STATE; M = S['M']; SET = S['SET']
    mb = L.MB()
    L.rod(mb, (-1.6, 0.3, 0.36), (-1.6, 0.3, 0.98), 0.27, M['zinc'], seg=12, r1=0.32)
    L.lumpy(mb, (-1.1, 0.35, 0.5), 0.3, M['rag'], 5, seg=8, rings=4, rough=0.25, squash=0.6)
    L.beam(mb, Vector((1.95, 1.5, 1.08)), Vector((2.12, 1.4, 4.4)), 0.05, 0.05, M['wood_l'], up=(1, 0, 0))
    L.lumpy(mb, (1.85, 1.5, 1.25), 0.25, M['straw'], 7, seg=8, rings=4, rough=0.3, squash=1.5)
    L._obj(mb, 's12_stair_dressing', SET, hull=0.012)
    for ob in SET.objects:
        if ob.name.startswith('s12_'):
            L.no_bounce(ob)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        loc, preset = LOC[shot]
        C.Take.__init__(self, loc, preset, quality=quality, lens=24.0, name="cam_s12_%d" % shot)
        self.shot = shot
        sd = os.path.join(TMP, "sprites%d" % shot)
        if shot == 1:
            dress_gallery()
            self.actors["vin"] = C.make_actor("vin", "vincenzo_smock", sd)
        else:
            dress_stair()
            self.actors["vin"] = C.make_actor("vin", "vincenzo_smock", sd, canvas=WIDE)

    def pose(self, shot, gs):
        assert shot == self.shot
        vin = self.actors["vin"]
        for g in gs:
            f = FP(g)
            loc, look, lens = cam_lin(setup_of(g, shot), g)
            self.key_cam(f, loc, look, lens)
            if shot == 1:
                C.place(vin, f, vin_a(g), 0.14 * ez((g - 1196) / 10.0))         # up on his toes for the lift
                self.key_set(f, mona=True, mona_lift=lift_at(g))
            else:
                v = vin_b(g)
                C.place(vin, f, (v.x, v.y), v.z)
                self.key_set(f, frame_on_stairs=(g >= B2))
        for g in gs:
            f = FP(g)
            self.scene.frame_set(f)
            if shot == 1:
                p = vin_pose_a(g)
                u = reach_u(g)
                hands = None
                if u > 0:
                    # mirrored figure: arm_r is the screen-left arm; targets in puppet-local (screen) coords, blended from rest
                    hands = {}
                    for arm, side in (("r", -1), ("l", 1)):
                        tl = actors.world_to_local(vin, self.cam, tuple(frame_edge(side, g)), f)
                        h0 = (0.22 * side, 1.02)
                        hands[arm] = dict(hand=(lerp(h0[0], tl[0], u), lerp(h0[1], tl[1], u)), bend=lerp(0.5, -0.3, u),
                                          stretch=lerp(1.0, 2.0, u), layer="front")
                    self.scene.frame_set(f)
                p2, info = vin.pose(f, p, hands=hands, camera=self.cam)
                if hands and os.environ.get("DBG"):
                    print("reach", g, {k: (round(v.get("error", 0), 3)) for k, v in info.items()}, flush=True)
            else:
                vin.pose(f, vin_pose_b(g), camera=self.cam)
        fr = [FP(g) for g in gs]
        self.sprites_for([(vin, 320)], fr)

    def report(self, shot, g):
        f = FP(g)
        self.scene.frame_set(f)
        loc, look, lens = cam_lin(setup_of(g, shot), g)
        v = look - loc
        out = dict(shot=shot, g=g, setup=setup_of(g, shot), cam=[round(c, 3) for c in loc], lens=round(lens, 1),
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f))
        if shot == 1:
            out["lift"] = round(lift_at(g), 3)
            d = lift_at(g)
            out["ptop"] = round(C.render.world_to_screen(self.cam, Vector((0, 21.6 - 0.9 * d, 4.55 + 0.6 * d)), f)[1], 1)
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [FP(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take("preview", shot)
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: LOC[shot])
