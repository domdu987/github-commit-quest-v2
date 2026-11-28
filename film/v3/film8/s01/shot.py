#!/usr/bin/env python3
"""shot.py -- film 8 take s01: shots 1 + 2 (g 0..177 + 6 out-handle frames g 178..183), the hook: "this man pours water into
shallow channels in the middle of the desert every night, and tells everyone that this summer he will sell ice".
One location (desert_ice plain, NIGHT, open water in the channels), two set-ups joined by the plan's cut at 2.50 s:

    id 1  g 0..74    shot 1, channels wide: farid on the bank between channels 4 and 5 tips his wooden
                     bucket and pours a long stream into channel 4 (screen-right); ripples spread on the starlit water where it lands.
                     The channels run east to the yakhchal dome with its glowing door, the 15 D shade wall on the right, lantern posts
                     into depth, the starry sky.  Calm slow push the whole set-up.  The bucket empties (g 50..66) and he straightens.
    id 2  g 75..183  shot 2, medium on farid, camera south-west of him looking north-east and up: the Milky Way behind him.  He looks
                     up at the stars with a calm smile (g 75..112), lowers his eyes to us on "หน้าร้อนนี้" (4.08 s), raises one finger on
                     "เขาจะขาย" (4.78 s = g 146) and holds it, a knowing smug tilt on "น้ำแข็ง" (5.37 s = g 164).  Slow push in + slight
                     orbit.  Handle g 178..183: the hold continues (rendered in 3D).
Mouths: nobody speaks (no quote in shots 1-2): static expression mouths only.
NO depth of field anywhere (client rule): C.Take switches it off at build and before every render.

Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402  (paths, cast8 first, bpy, desert, stage)
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast8 = C.D, C.actors, C.camrig, C.cast8
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G_CUT = C.g_bound(2.50)            # 75: shot 2 starts (plan cut)
G_END = C.g_bound(5.92)            # 178: shot 3 starts here
H_OUT = 6                          # out-handle g 178..183
RANGES = {1: (0, G_CUT - 1), 2: (G_CUT, G_END + H_OUT - 1)}
LOC = ("desert_ice", "channels_wide")
LIGHT = "NIGHT"
G_TIP = (0, 8)                     # bucket tips 0.35 -> 0.85
G_EMPTY = (48, 66)                 # tips on to 1.0 while it empties
G_DONE = (62, 74)                  # stream stops, he straightens
G_LOOKUP = (77, 92)                # shot 2: head up to the stars
G_TO_US = (C.g_of(4.08) - 12, C.g_of(4.08))      # 113..125: eyes come down to the lens ("หน้าร้อนนี้")
G_FINGER = (C.g_of(4.78) - 8, C.g_of(4.78) + 2)  # 138..148: the finger goes up ("เขาจะขาย" = g 146)
G_ICE = C.g_of(5.37)               # 164 "น้ำแข็ง": smug tilt

# ----------------------------------------------------------------------------- staging (world D, ground z 0; +x east, +y north)
FARID = Vector((-6.0, 11.6, 0.0))  # bank between channel 4 (y 10.2) and channel 5 (y 13.0): no lantern post near (D's farid_pour mark
                                   # (-6, 8.8) puts the x -9 post's lantern between a west camera and him)
POUR_CH = 3                        # index of the channel he pours into (y 10.2, screen-right of him)
LENS_A, LENS_B = 22.0, 22.0


def aim(loc, az, el, d=30.0):
    """look-at point from a camera position, azimuth (deg from north toward east) and elevation (deg)."""
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


# set-up 1: from the west over channel 4, looking east-north-east along the channels: farid left of centre, the dome and its door
# right of centre, the Milky Way rising over the horizon at the left (its core is at az ~65, not the API's 35).
CAM_A0 = ((-15.2, 10.5, 3.1), aim((-15.2, 10.5, 3.1), 78.0, 2.0))
CAM_A1 = ((-13.4, 10.35, 2.95), aim((-13.4, 10.35, 2.95), 79.0, 2.5))
# set-up 2: low, west-south-west of him looking up north-east: the Milky Way band behind him, the dome at the right edge.
CAM_B0 = ((-9.9, 9.35, 2.05), aim((-9.9, 9.35, 2.05), 70.0, 9.0))
CAM_B1 = ((-9.2, 9.95, 2.0), aim((-9.2, 9.95, 2.0), 72.5, 9.5))       # push ~0.9 D + orbit
PPD = {1: 256, 2: 320}


def cam_of(shot, g):
    if shot == 1:
        x = g / float(RANGES[1][1]); a0, a1 = CAM_A0, CAM_A1
    else:
        x = (g - G_CUT) / float(RANGES[2][1] - G_CUT); a0, a1 = CAM_B0, CAM_B1
    u = 0.35 * ez(x, "sine") + 0.65 * x               # mostly linear: a pure sine ease left near-still frames at both ends
    return Vector(lerp(a0[0], a1[0], u)), Vector(lerp(a0[1], a1[1], u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- poses
POUR = cast8.STORY8["farid_pour"][1]


def pose_a(g):
    p = dict(POUR)
    pour = lerp(0.35, 0.85, u_of(g, *G_TIP)) if g < G_EMPTY[0] else lerp(0.85, 1.0, u_of(g, *G_EMPTY))
    water = 1.0 - 0.85 * u_of(g, 20, G_EMPTY[1])
    d = u_of(g, *G_DONE)
    if d > 0:
        pour = lerp(pour, 0.30, d); water = lerp(water, 0.0, d)
    p.update(pour=pour, bucket_water=water, pour_len=1.35, pour_side=1)
    p["lean"] = lerp(16.0, 7.0, d) + 1.2 * math.sin(g * 0.23)
    p["pitch"] = lerp(0.55, 0.25, d)
    p["head_roll"] = -4.0 + 1.5 * math.sin(g * 0.17)
    p["expr"] = "determined" if g < 66 else "happy"
    p["mouth"] = None if g < 66 else "smile"
    if p["mouth"] is None:
        del p["mouth"]
    p["blink"] = blink(g, [30, 65])
    p["t"] = g / 30.0
    return p


def pose_b(g):
    """shot 2: the emptied bucket stands on the bank beside him (3D prop, BUCKET_B), hands free.  Looking up in wonder ('excited',
    round eyes, gaze up) -> to us ('happy', behind the blink) -> the right index finger up beside the head (screen-right, the free sky
    side) -> 'smug' tilt on 'น้ำแข็ง' (behind the second blink)."""
    up = u_of(g, *G_LOOKUP) * (1.0 - u_of(g, *G_TO_US))
    fin = u_of(g, *G_FINGER)
    smug = u_of(g, G_ICE - 4, G_ICE + 4)
    expr = "excited" if g < G_TO_US[0] + 4 else ("happy" if g < G_ICE - 2 else "smug")      # changes sit behind the blinks
    p = dict(yaw=lerp(0.30, 0.12, u_of(g, *G_TO_US)), expr=expr, mouth="smile",
             pitch=lerp(0.05, -1.0, up) + 0.06 * math.sin(g * 0.11), gaze=(lerp(0.1, 0.4, up) + 0.18 * up * math.sin(g * 0.15), lerp(0.0, -1.0, up)),
             head_roll=lerp(-3.0, 5.0, up) - 6.0 * smug + 2.5 * math.sin(g * 0.13), lean=-2.0 * up + 1.5 * math.sin(g * 0.09),
             legs="stand", arm_l=dict(hand=(-0.40, 1.02), bend=0.3))
    if fin <= 0:
        p["arm_r"] = dict(hand=(0.40, 1.02), bend=0.3)
    else:
        bob = 0.035 * fin * math.sin((g - G_FINGER[1]) * 0.42)          # the raised finger keeps a small emphatic bob
        p["arm_r"] = dict(hand=(lerp(0.40, 0.90, fin), lerp(1.02, -0.10, fin) + bob), bend=lerp(0.3, -1.0, fin), sharp=lerp(0.25, 1.0, fin),
                          stretch=lerp(1.0, 1.05, fin), shape="point" if fin > 0.5 else "ball")
    p["blink"] = blink(g, [G_TO_US[0] + 4, G_ICE - 2])
    p["t"] = g / 30.0
    return p


BUCKET_B = (FARID.x + 0.15, FARID.y + 0.36, 0.0)   # set-up 2: the empty bucket on the bank just behind him, screen-left of his feet


def make_bucket():
    """the wooden bucket of D (staves, iron hoops, rope bail) as a 3D prop; shown in set-up 2 only (keyed)."""
    S = D.STATE; mb = D.MB()
    D._bucket(mb, BUCKET_B, S['M'], s=0.62)
    ob = D._obj(mb, 's01_bucket', S['SET'], hull=0.012); D.no_bounce(ob)
    return ob


# ----------------------------------------------------------------------------- runtime set dressing: the pour's ripples on the water
def make_ripples():
    """Two thin expanding rings on channel 4's water where the stream lands (desert has no splash: 'the splash belongs to the set').
    A soft moon-white emission ring material, camera-visible only."""
    import bpy
    S = D.STATE; SET = S['SET']
    mat = bpy.data.materials.new("s01_ripple")
    mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.75, 0.85, 1.0, 1.0); em.inputs["Strength"].default_value = 0.9
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); out = nt.nodes.new("ShaderNodeOutputMaterial")
    mx.inputs[0].default_value = 0.35; mx.name = "mix"
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    rings = []
    for k in range(2):
        bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.02, major_segments=48, minor_segments=4)
        ob = bpy.context.active_object; ob.name = "s01_ripple_%d" % k
        for c in list(ob.users_collection): c.objects.unlink(ob)
        SET.objects.link(ob)
        ob.data.materials.append(mat); ob.scale = (1, 1, 0.25)
        ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
        rings.append(ob)
    return rings


def key_ripples(rings, f, g, centre, on):
    """ring k: radius grows 0.12 -> 0.85 D over 18 frames, phase-shifted by 6 frames; hidden when no stream."""
    for k, ob in enumerate(rings[:2]):
        ph = ((g + 9 * k) % 18) / 18.0
        r = 0.10 + 0.55 * ph
        ob.location = (centre[0], centre[1], D.CH_Z['water'] + 0.01)
        ob.scale = (r, r * 0.9, 0.25)
        ob.hide_render = not on or ph > 0.8
        ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f); ob.keyframe_insert("hide_render", frame=f)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=LENS_A, name="cam_s01", light=LIGHT)
        self.far = self.actors["far"] = C.make_actor("far", "farid", os.path.join(TMP, "sprites"))
        self.rings = make_ripples()
        self.bucket = make_bucket()
        self.pour_xy = {}

    def pose(self, shot, gs):
        far = self.far
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS_A if shot == 1 else LENS_B)
            C.place(far, f, FARID)
            self.key_set(f, ice="water")
            self.bucket.hide_render = shot == 1; self.bucket.keyframe_insert("hide_render", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            far.pose(f, pose_a(g) if shot == 1 else pose_b(g), camera=self.cam)
        self.sprites_for([(far, PPD[shot])], [bf(shot, g) for g in gs])
        for g in gs:                                   # ripples where the stream end meets the water (from the drawn anchor)
            f = bf(shot, g)
            an = self.anch.get(("far", f), {})
            on = shot == 1 and "pour_end_r" in an
            c = (FARID.x + 0.4, D.CH_Y[POUR_CH] + 0.5)
            if on:
                w = actors.local_to_world(far, an["pour_end_r"], f, camera=self.cam)
                cl = self.cam.matrix_world.to_translation()          # the ray lens -> stream end, cut with the water plane
                t = (D.CH_Z['water'] - cl.z) / (w.z - cl.z) if abs(w.z - cl.z) > 1e-6 else 1.0
                h = cl + (w - cl) * t
                c = (h.x, max(D.CH_Y[POUR_CH] - 0.85, min(h.y, D.CH_Y[POUR_CH] + 0.85)))
                self.pour_xy[g] = (round(w[0], 2), round(w[1], 2), round(w[2], 2))
            key_ripples(self.rings, f, g, c, on)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), pour_end=self.pour_xy.get(g))

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
