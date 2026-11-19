#!/usr/bin/env python3
"""shot.py -- film 13 take s26: shots 26-30, the ENDING (g 1677..1994 + 6 in-handle frames g 1671..1676).  Day 5 MORNING, hotel at lift 1.0.

    26  g1677..1739  front_stair MORNING: the rich man comes out of the raised door, strolls to the edge of the portico and puts one foot
                     forward into the air (step_out).  Three-quarter view from the left, slow push in.
    27  g1740..1771  'ใต้เท้าไม่มีพื้น!': closer, lower: below his foot only air, the old stair 3.6 D (about 2 m) lower; he looks down.
    28  g1772..1867  street wide (street_end side): the hotel high on its jacks and cribs, tiny man at the portico edge, workers' heaps, townsfolk.
    29  g1868..1905  front_stair low: he overbalances, drops (arms up, hat flying, tumble) over the stair into the mud, splash (3D mud blobs).
    30  g1906..1994  mud: sits dazed with stars, then holds the fat purse up; pullman steps in and takes it.  Hard cut on 'เอง' (66.38 s = g 1994).

One location (street, MORNING), one build.  Hooks are static in this take (lift 1.0, fill 0.15): nothing to key per frame.
Blender frame of (id, g) = 1000 * (id - 26) + g + 1 (id = first shot number).
    python3 shot.py probe a:b[:step]
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c13 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

B, bpy, actors, camrig, cast13, puppet = C.B, C.bpy, C.actors, C.camrig, C.cast13, C.puppet
lerp, clamp, ez = C.lerp, C.clamp, C.ez
TMP = os.path.join(HERE, "work")
S13 = cast13.STORY13

# ----------------------------------------------------------------------------- timing
G = {26: C.g_of(55.89), 27: C.g_of(57.99), 28: C.g_of(59.06), 29: C.g_of(62.26), 30: C.g_of(63.53)}   # WORKER13: g = round((t + 0.10) * 30)
G_LAST = C.N_FILM - 1                    # 1994 (hard cut on the last word)
H_IN = 6
RANGES = {26: (G[26] - H_IN, G[27] - 1), 27: (G[27], G[28] - 1), 28: (G[28], G[29] - 1), 29: (G[29], G[30] - 1), 30: (G[30], G_LAST)}
SHOT_OF = lambda g: [s for s in RANGES if RANGES[s][0] <= g <= RANGES[s][1]][0]
CUTS = [G[27], G[28], G[29], G[30]]

G_WALK0, G_WALK1 = G[26] + 2, G[26] + 44             # strolls out of the door to the portico edge
G_FALL0 = G[29] + 4                                  # launch
G_HIT = C.g_of(63.1)                                 # 1896: lands in the mud (sfx splat)
G_PURSE0 = G[30] + 8                                # purse comes up
G_TAKE = G[30] + 60                                  # pullman takes it (1974)
BF = lambda g: C.bf(26, g)


# ----------------------------------------------------------------------------- staging (world D)
EDGE = Vector((0.0, -3.72, 0.0))                     # portico landing slab: y -4.0..0.3, top z 2.65 + lift (3.6)
DOOR = Vector((0.0, -1.0, 0.0))
LIFT = B.LIFT_MAX
Z_PORT = 2.65 + LIFT                                 # 6.25 portico floor
LAND = Vector((1.2, -11.6, 0.0))                     # where he lands (outside the stair footprint y -9..-4, mud)
PULL = Vector((3.5, -12.4, 0.0))

CAMS = {
    26: (((-2.4, -17.0, 4.4), (0.0, -3.0, 7.6)), ((-1.2, -12.6, 5.4), (0.0, -3.3, 7.9)), 22.0),
    27: (((-4.2, -9.5, 7.2), (0.0, -3.8, 6.2)), ((-2.6, -7.8, 7.4), (0.0, -3.8, 6.6)), 22.0),
    28: (((-22.0, -13.5, 3.6), (0.0, -3.8, 7.6)), ((-9.2, -8.6, 4.8), (0.0, -3.9, 7.0)), 22.0),
    29: (((-4.2, -16.8, 2.6), (0.1, -6.5, 5.8)), ((-3.2, -17.2, 1.9), (1.0, -10.2, 2.6)), 22.0),
    30: (((-2.6, -18.0, 1.5), (1.6, -11.2, 2.3)), ((-1.2, -16.4, 1.7), (1.8, -11.0, 2.5)), 22.0),
}
LIGHT = "DAY"
PPD = {"std": 256, "fall": 192, "sit": 256}


def cam_of(g):
    s = SHOT_OF(g)
    a, b, lens = CAMS[s]
    x = clamp((g - RANGES[s][0]) / float(max(1, RANGES[s][1] - RANGES[s][0])))
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector([lerp(a[0][i], b[0][i], u) for i in range(3)]), Vector([lerp(a[1][i], b[1][i], u) for i in range(3)]), lens


# ----------------------------------------------------------------------------- poses
def base(name):
    return dict(S13[name][1])


def idle(g, amp=1.0):
    return amp * math.sin(g * 0.13), amp * math.sin(g * 0.09 + 1.0)


RICH_STEP = dict(base("rich_step_out"), expr="stunned", arm_l=dict(hand=(-0.7, 0.9), bend=0.3, stretch=1.2, shape="open"))
RICH_FALL = dict(base("rich_fall"), expr="stunned")
RICH_FALL.pop("mouth", None)
RICH_SIT = base("rich_sit_in_mud")
RICH_PAY = base("rich_pay_sad")
PULL_CALM = base("pullman_stand_calm")


def rich_walk(g):
    """walking out of the door: cast6 walk cycle (rich member), smug-then-startled."""
    ph = (g - G_WALK0) / 28.0 * 1.0
    p = dict(cast13.cycle("rich", ph, "walk"))
    p.update(yaw=0.45, expr="smug", pitch=-0.05, blink=cast13.blink_at(g, 70))
    p["t"] = g / 30.0
    return p


def rich_edge(g, k):
    """the foot goes out over the edge: ring eyes + closed mouth ('stunned'), then (shot 27, from g+6) he LOOKS DOWN at the void: head down, eyes down."""
    p = dict(RICH_STEP)
    i, j = idle(g, 1.0)
    look = ez((g - (G[27] + 6)) / 10.0) if g >= G[27] else 0.0
    p["lean"] = lerp(-2.0, -9.0, max(k, look)) + 0.6 * i
    p["pitch"] = lerp(0.05, 0.95, look)
    p["gaze"] = (0.1, lerp(0.3, 1.0, look))
    if look > 0.5:
        p["expr"] = "worried"                        # half lids, eyes down, wavy closed mouth; the switch sits behind a blink
    p["blink"] = 1.0 if G[27] + 5 <= g <= G[27] + 7 else cast13.blink_at(g, 90, 7)
    p["t"] = g / 30.0
    return p


def cane_overlay(f, pose):
    """the walking cane (cast13 has no cane prop): drawn into the sprite in the left hand (hand_l), planted at the feet line; gold knob.
    Only until the drop (G_FALL0): afterwards it stays behind on the portico (not drawn)."""
    if f >= BF(G_FALL0):
        return ""
    fig = puppet.figure("rich", pose, "c")
    hx, hy = fig["anchors"]["hand_l"]
    fy = fig["feet_y"]
    tx = hx - 0.12
    return ('<g stroke-linecap="round"><line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="#1b1210" stroke-width="0.115"/>'
            '<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="#7a4a22" stroke-width="0.066"/>'
            '<circle cx="%.3f" cy="%.3f" r="0.125" fill="#e3b53a" stroke="#1b1210" stroke-width="0.03"/></g>'
            % (hx, hy, tx, fy, hx, hy, tx, fy, hx, hy))


def pose_rich(g):
    """-> (variant, pose, place_xyz, flip, hands). variants: std | fall | sit"""
    if g < G_WALK0:                                   # in the doorway
        return "std", rich_walk(g), (DOOR.x, DOOR.y, Z_PORT), False
    if g < G_WALK1:
        u = ez((g - G_WALK0) / float(G_WALK1 - G_WALK0), "sine")
        return "std", rich_walk(g), (lerp(DOOR.x, EDGE.x, u), lerp(DOOR.y, EDGE.y, u), Z_PORT), False
    if g < G_FALL0:                                   # at the edge: step into the air, look down, wobble
        k = clamp((g - G_WALK1) / 30.0)
        if g >= G[29]:
            k = 1.0
        return "std", rich_edge(g, k), (EDGE.x, EDGE.y, Z_PORT), False
    if g < G_HIT:                                     # the drop
        u = (g - G_FALL0) / float(G_HIT - G_FALL0)
        x = lerp(EDGE.x, LAND.x, u)
        y = lerp(EDGE.y, LAND.y, u)
        z0, z1 = Z_PORT, land_z()
        z = lerp(z0, z1, u * u) + 1.1 * math.sin(math.pi * min(1.0, u * 1.25)) * (1.0 - u)
        p = dict(RICH_FALL)
        p["tumble"] = lerp(8.0, 150.0, ez(u, "sine"))
        p["t"] = g / 30.0
        hx = lerp(0.85, 2.7, u)
        hy = -1.35 - 3.2 * math.sin(math.pi * min(1.0, u * 1.0)) * 0.9 - 0.6 * u
        p["hat_fly"] = (hx, hy, 38 + 420 * u)
        p["legs"] = dict(RICH_FALL["legs"], lift_r=1.3 if int(g / 3) % 2 else 0.8, lift_l=0.8 if int(g / 3) % 2 else 1.3)
        p["head_roll"] = 8 + 18 * math.sin(g * 0.8)
        return "fall", p, (x, y, z), False
    return None


def land_z():
    return STATE_GROUND(LAND.x, LAND.y)


SINK = 0.75                                           # waist deep in the mud
STATE_GROUND = None                                   # set in Take: mud height + fill at the landing spot


def rich_sit(g):
    p = dict(RICH_SIT)
    t = g - G_HIT
    # the hat (still in the air at impact) comes down beside the head; stars spin
    k = ez(t / 10.0)
    hf0 = (2.7, -3.4, 38 + 420)
    hf1 = (0.0, -0.1, 0.0)
    if t < 9:
        p["hat_fly"] = (lerp(hf0[0], hf1[0], k), lerp(hf0[1], hf1[1], k), lerp(hf0[2] % 360, hf1[2], k))
    else:
        p.pop("hat_fly", None)                          # the hat is back on his head (askew, as drawn by the pose)
    p["mud"] = clamp(0.35 + t / 20.0)
    p["dizzy"] = 1.0
    p["t"] = g / 30.0
    i, j = idle(g, 1.0)
    p["head_roll"] = RICH_SIT["head_roll"] + 3.0 * i + (10 * math.sin(t * 0.9) * max(0.0, 1 - t / 8.0))
    p["lean"] = RICH_SIT["lean"] + 2.0 * j
    p["blink"] = cast13.blink_at(g, 60, 3)
    return p


def rich_pay(g, hand_local):
    """sitting in the mud, sad, the fat purse held up (right arm up toward pullman); arm placed by a pinned hand."""
    p = rich_sit(g)
    u = ez((g - G_PURSE0) / 14.0)
    p["dizzy"] = 1.0 - clamp((g - G_PURSE0 + 8) / 8.0)
    p["expr"] = "dazed" if g < G_PURSE0 - 6 else "sad"
    p["pitch"] = lerp(0.1, -0.35, u)
    p["head_roll"] = lerp(p["head_roll"], 6.0, u)
    given = g >= G_TAKE
    if given:
        gk = ez((g - G_TAKE) / 8.0)                   # he sulks: arm drops, head sinks, eyes down
        p["arm_r"] = dict(hand=lerp_t((1.3, -0.5), (0.9, 1.3), gk), bend=0.2, stretch=lerp(1.6, 1.2, gk))
        p["pitch"] = lerp(-0.35, 0.55, gk)
        p["head_roll"] = lerp(6.0, 10.0, gk)
    else:
        p["arm_r"] = dict(hand=lerp_t((0.9, 1.3), (1.3, -0.5), u), bend=lerp(0.2, -0.3, u), stretch=lerp(1.2, 1.6, u))
        if u > 0.05:
            p["prop_r"] = {"type": "purse", "scale": 1.7}
    return p


def lerp_t(a, b, k):
    return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))


def pose_pull(g):
    """pullman: stands off to the side, then steps in and holds a palm out under the purse."""
    p = dict(PULL_CALM)
    p["yaw"] = -0.35
    p["blink"] = cast13.blink_at(g, 80, 11)
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- mud splash: ballistic 3D blobs
class Splash(object):
    """mud impact: a wet dark patch with a raised rim, a crown of cone spikes that rises and collapses (t 0..9), stretched droplets."""
    N = 30
    NS = 18

    def _obj(self, ob, name):
        S = B.STATE
        ob.name = name
        for c in list(ob.users_collection):
            c.objects.unlink(ob)
        S["SET"].objects.link(ob)
        ob.visible_shadow = False
        ob.hide_render = True
        return ob

    def __init__(self, centre):
        from mathutils import Matrix
        S = B.STATE
        mat = S["C"]("#946336", 1.1, 1.0)
        mat_dark = S["C"]("#34231a", 0.9, 1.0)
        mat_rim = S["C"]("#6a4a2c", 1.0, 1.0)
        rnd = random.Random(29)
        self.cx = centre
        bpy.ops.mesh.primitive_circle_add(vertices=40, radius=1.0, fill_type="TRIFAN")
        self.patch = self._obj(bpy.context.active_object, "splash_patch"); self.patch.data.materials.append(mat_dark)
        bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.12, major_segments=40, minor_segments=6)
        self.rim = self._obj(bpy.context.active_object, "splash_rim"); self.rim.data.materials.append(mat_rim)
        self.spikes = []
        for k in range(self.NS):
            bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.5, radius2=0.0, depth=1.0)
            ob = self._obj(bpy.context.active_object, "splash_spike_%d" % k)
            ob.data.transform(Matrix.Translation((0, 0, 0.5)))
            ob.data.materials.append(mat)
            self.spikes.append((ob, 2 * math.pi * k / self.NS + rnd.uniform(-0.1, 0.1), rnd.uniform(0.9, 1.6), rnd.uniform(0.9, 1.3)))
        self.obs = []
        self.vel = []
        for k in range(self.N):
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0)
            ob = self._obj(bpy.context.active_object, "splash_%d" % k)
            ob.data.materials.append(mat)
            a = rnd.uniform(0, 2 * math.pi)
            sp = rnd.uniform(0.14, 0.42)
            self.vel.append((math.cos(a) * sp, math.sin(a) * sp * 0.8, rnd.uniform(0.35, 0.8), rnd.uniform(0.04, 0.10)))
            self.obs.append(ob)

    def _keys(self, ob, f, paths=("hide_render", "location", "scale", "rotation_euler")):
        for p in paths:
            ob.keyframe_insert(p, frame=f)
        for fc in camrig.fcurves_of(ob):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"

    def key(self, f, g, ground):
        t = g - G_HIT
        cx, cy = self.cx
        on = t >= 0
        self.patch.hide_render = self.rim.hide_render = not on
        grow = 0.35 + 0.65 * clamp(t / 5.0)
        self.patch.location = (cx, cy, ground + 0.05); self.patch.scale = (2.1 * grow, 1.7 * grow, 1.0)
        self.rim.location = (cx, cy, ground + 0.10); self.rim.scale = (2.0 * grow, 1.6 * grow, 1.0)
        self._keys(self.patch, f); self._keys(self.rim, f)
        for ob, a, H, w in self.spikes:
            son = 0 <= t <= 10
            ob.hide_render = not son
            if son:
                h = H * math.sin(math.pi * clamp(t / 10.0)) ** 0.8
                rr = 1.05 + 0.10 * t
                ob.location = (cx + math.cos(a) * rr * 1.1, cy + math.sin(a) * rr * 0.9, ground + 0.05)
                ob.rotation_euler = (0.0, math.radians(30), a)
                ob.scale = (0.34 * w, 0.34 * w, max(0.01, h))
            self._keys(ob, f)
        for ob, (vx, vy, vz, r) in zip(self.obs, self.vel):
            don = 0 <= t <= 14
            ob.hide_render = not don
            if don:
                ob.location = (cx + vx * t, cy + vy * t, ground + 0.1 + vz * t - 0.05 * t * t)
                rr = r * (1.0 - 0.4 * t / 14.0)
                ob.scale = (rr, rr, rr * 1.5)
            self._keys(ob, f)


# ----------------------------------------------------------------------------- the take
def key_hidden(ob, f, hidden):
    ob.hide_render = bool(hidden)
    ob.keyframe_insert("hide_render", frame=f)
    for fc in camrig.fcurves_of(ob):
        if fc.data_path == "hide_render":
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


def show_actor(a, f, on):
    for o in a.objects():
        key_hidden(o, f, not on)


def swap_cast():
    T = B.T
    P = lambda k: dict(S13[k][1])
    T.PH.update(
        worker=("worker13_a", P("worker_stand_a"), 3.2), foreman=("foreman13", P("foreman_stand"), 3.3), rich=("rich", P("rich_look_window_smug"), 3.4),
        maid=("town_b", P("town_stand_b"), 3.0), clerk=("worker13_b", P("worker_stand_b"), 3.2), kid=("town_c", P("town_stand_c"), 2.5),
        towns_m=("town_a", P("town_stand_a"), 3.2), towns_f=("town_b", P("town_stand_b"), 3.0), towns_o=("worker13_c", P("worker_stand_c"), 3.1))
    # laughing / cheering variants for the onlookers of shots 29-30
    return T


def retint_sky():
    """the low sky band of the dome renders olive/khaki (the sky texture's warm horizon): blend the sky colour toward a pale warm blue (client QA: warm blue sky)."""
    so = B.STATE.get("sky_obj")
    if so is None:
        return
    nt = so.data.materials[0].node_tree
    img = [n for n in nt.nodes if n.bl_idname == "ShaderNodeTexImage"][0]
    st = nt.nodes["strength"]
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MIX"
    mix.inputs[0].default_value = SKY_MIX
    mix.inputs[7].default_value = SKY_TINT
    for l in list(nt.links):
        if l.to_node == st and l.to_socket.name == "Color":
            nt.links.remove(l)
    nt.links.new(img.outputs["Color"], mix.inputs[6])
    nt.links.new(mix.outputs[2], st.inputs["Color"])


SKY_MIX = 0.72
SKY_TINT = (0.52, 0.70, 1.0, 1.0)


def cut_stair():
    """the old stair stops short of the lifted portico: delete everything of it nearer the hotel than y -6.2 (top 3 flights + landing + rail),
    leaving void between the stair top (z ~1.5) and the portico lip (z 6.25); hide the mirror puddles (smeared reflections)."""
    import bmesh
    st = bpy.data.objects["stair"]
    bm = bmesh.new(); bm.from_mesh(st.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > -6.2], context="VERTS")
    bm.to_mesh(st.data); bm.free()
    for n in ("puddles", "scum"):
        if n in bpy.data.objects:
            bpy.data.objects[n].hide_render = True


class Take(object):
    def __init__(self, quality="preview"):
        global STATE_GROUND
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        swap_cast()
        self.A = B.build("front_stair", light=LIGHT, state="lift1,fill0.15")
        B.setup_render(scene, quality)
        cut_stair()
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name="cam_s26", lens=22.0)
        self.cam.data.clip_start, self.cam.data.clip_end = 0.02, 6000
        self.cam.data.dof.use_dof = False
        scene.camera = self.cam
        gz = B._gnd()
        STATE_GROUND = lambda x, y: gz(x, y) + B.FILL_MAX * 0.15
        sd = os.path.join(TMP, "sprites")
        self.acts = {}
        self.anch = {}
        self.rich = {k: C.make_actor("rich_" + k, "rich", sd, canvas=cv) for k, cv in
                     (("std", None), ("fall", cast13.CANVAS13_POSE["rich_fall"]), ("sit", cast13.CANVAS13_POSE["rich_sit_in_mud"]))}
        self.pull = C.make_actor("pull", "pullman", sd)
        self.acts.update({a.name: a for a in self.rich.values()})
        self.acts["pull"] = self.pull
        self.splash = Splash((LAND.x, LAND.y))
        # onlookers (real cast13 cards), per shot, hidden in the others
        self.crowds = {}
        self._make_crowds()
        self.sprite_dir = sd

    def _make_crowds(self):
        cam_objs = {}
        for shot in (28, 29, 30):
            loc, look, lens = cam_of(RANGES[shot][0])
            cam = camrig.key_camera  # noqa (placeholder to keep names short)
            tmp = bpy.data.objects.new("tmp_cam", bpy.data.cameras.new("tmp_cam"))
            bpy.context.scene.collection.objects.link(tmp)
            tmp.data.lens = lens; tmp.data.sensor_width = 36
            tmp.location = loc
            tmp.rotation_euler = camrig.look_rotation(loc, look, 0.0)
            bpy.context.view_layer.update()
            gz = B._gnd()
            if shot == 28:
                objs = (B.crowd_view(4, [(10, 22, -15, -9)], tmp, seed=31, ground=gz, min_dist=3.0) +
                        B.crowd_view(3, [(-12, -8, -13, -11)], tmp, seed=33, ground=gz, min_dist=3.0))
            elif shot == 29:
                objs = B.crowd_view(5, [(-14, -5, -14, -9), (6, 14, -14, -9)], tmp, seed=35, ground=gz, min_dist=2.6)
            else:
                objs = B.crowd_view(4, [(-9, -4, -14, -10), (6, 11, -14, -10)], tmp, seed=36, ground=gz, min_dist=2.6)
            self.crowds[shot] = objs
            bpy.data.objects.remove(tmp, do_unlink=True)
        for ob in B.STATE.get("cards", []):                # lift every card onto the filled mud
            if ob.location.z < 1.0:
                ob.location.z += B.FILL_MAX * 0.15

    def pose(self, gs):
        scene, cam = self.scene, self.cam
        gs = sorted(set(gs))
        ext = sorted(set(gs) | ({G_TAKE - 1} if any(g >= G_TAKE for g in gs) else set()))
        for g in ext:
            f = BF(g)
            loc, look, lens = cam_of(g)
            camrig.key_camera(f, loc, look, cam=cam, lens=lens, interp="LINEAR", easing="AUTO")
        # crowd cards whose chin would drop below y 850 anywhere in their shot are dropped for the whole shot (caption band y 880)
        low = set()
        for s_ in (28, 29, 30):
            if not any(RANGES[s_][0] <= g <= RANGES[s_][1] for g in ext):
                continue
            from bpy_extras.object_utils import world_to_camera_view
            for g in range(RANGES[s_][0], RANGES[s_][1] + 1, 3):
                loc, look, lens = cam_of(g)
                camrig.key_camera(BF(g), loc, look, cam=cam, lens=lens, interp="LINEAR", easing="AUTO")
                scene.frame_set(BF(g))
                bpy.context.view_layer.update()
                for ob in self.crowds[s_]:
                    p = ob.location
                    c = world_to_camera_view(scene, cam, Vector((p.x, p.y, p.z + 2.0 * ob.scale.z)))
                    if (1 - c.y) * 1280 > 850 and c.z > 0 and -0.1 < c.x < 1.1:
                        low.add(ob.name)
        for g in ext:
            f = BF(g)
            shot = SHOT_OF(g)
            for s_, objs in self.crowds.items():
                for ob in objs:
                    key_hidden(ob, f, s_ != shot or ob.name in low)
            r = pose_rich(g) if g < G_HIT else None
            on = {"std": False, "fall": False, "sit": False}
            if r is not None:
                v, p, xyz, flip = r
                a = self.rich[v]
                C_place(a, f, xyz, flip)
                scene.frame_set(f)
                a.pose(f, p, camera=cam)
                on[v] = True
            else:
                a = self.rich["sit"]
                C_place(a, f, (LAND.x, LAND.y, land_z() - SINK * ez((g - G_HIT) / 6.0)), False)
                scene.frame_set(f)
                a.pose(f, rich_pay(g, None) if g >= G_PURSE0 - 12 else rich_sit(g), camera=cam)
                on["sit"] = True
            for k, a in self.rich.items():
                show_actor(a, f, on[k])
                if not on[k]:
                    C_place(a, f, (0, -60, -50), False)
            self.splash.key(f, g, land_z())
        self.sprites_rich(ext)                         # anchors of the purse hand are needed to pin pullman's hand
        for g in ext:
            f = BF(g)
            pa = self.pull
            if g >= G[30]:
                u = ez((g - (G[30] + 14)) / 30.0)
                px = lerp(PULL.x + 5.0, PULL.x, u)
                C_place(pa, f, (px, PULL.y, land_z()), False)
                scene.frame_set(f)
                walking = 0.0 < u < 0.995
                p = dict(PULL_CALM)
                if walking:
                    p = dict(cast13.cycle("pullman", (g - G[30]) / 24.0, "walk"))
                p.update(yaw=-0.35, expr="neutral", mouth="smile", pitch=0.25 if u >= 0.995 else -0.05, blink=cast13.blink_at(g, 80, 11), t=g / 30.0)
                hands = None
                if g >= G_PURSE0 + 4 and u >= 0.995:
                    gr = min(g, G_TAKE - 1)
                    an = self.anch.get((self.rich["sit"].name, BF(gr)))
                    if an is not None:
                        w = actors.local_to_world(self.rich["sit"], an["hand_r"], BF(gr), camera=cam)
                        k = ez((g - G_TAKE) / 12.0) if g >= G_TAKE else 0.0
                        tgt = (w.x - 0.05, w.y - 0.15, w.z - 0.40 + 0.9 * k)
                        p["arm_l"] = "down"
                        hands = {"l": {"hand": tgt, "bend": 0.2}}
                        if g >= G_TAKE:
                            p["prop_l"] = {"type": "purse", "scale": 1.7}
                else:
                    p["arm_l"] = p.get("arm_l", "akimbo")
                pa.pose(f, p, hands=hands, camera=cam)
                show_actor(pa, f, True)
            else:
                C_place(pa, f, (0, -60, -50), False)
                show_actor(pa, f, False)

    def sprites_rich(self, ext):
        for k, a in self.rich.items():
            fr = [BF(g) for g in ext if BF(g) in a.poses]
            if fr:
                for f, r in zip(fr, a.render_sprites(PPD.get(k, 256), frames=fr, overlay=cane_overlay if k == "std" else None)):
                    self.anch[(a.name, f)] = r["anchors"]

    def sprites(self, gs):
        a = self.pull
        fr = [BF(g) for g in gs if BF(g) in a.poses]
        if fr:
            for f, r in zip(fr, a.render_sprites(PPD["std"], frames=fr)):
                self.anch[("pull", f)] = r["anchors"]

    def report(self, g):
        f = BF(g)
        loc, look, lens = cam_of(g)
        return dict(g=g, shot=SHOT_OF(g), cam=[round(c, 2) for c in loc], heads=C.head_report(self.scene, self.cam, self.acts, self.anch, f))

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        self.cam.data.dof.use_dof = False
        self.scene.cycles.samples = samples
        import render
        return render.render_frames([BF(g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)


def C_place(a, f, xyz, flip):
    a.place(f, (float(xyz[0]), float(xyz[1]), float(xyz[2])), flip=flip)


def parse_spec(spec):
    return [g for g in C.parse(spec) if any(RANGES[s][0] <= g <= RANGES[s][1] for s in RANGES)]


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = parse_spec(sys.argv[2])
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        Tk.sprites(gs)
        out = sys.argv[3] if len(sys.argv) > 3 else None
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        out = os.path.join(HERE, "frames"); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        print("final: %d to render" % len(todo), flush=True)
        if todo:
            Tk = Take("final")
            Tk.pose(todo); Tk.sprites(todo)
            for g in todo:
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                json.dump(Tk.report(g), open(os.path.join(out, "g_%04d.json" % g), "w"))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
