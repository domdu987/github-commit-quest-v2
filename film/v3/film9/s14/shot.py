#!/usr/bin/env python3
"""shot.py -- film 9 take s14: shot 14 (g 1041..1152, handles g 1035..1040 and g 1153..1158), BATTLE: "แล้วทัพศัตรูก็มาถึง
ลากปืนใหญ่มาเรียงหน้ากำแพงทั้งสองช่วง".  One location (wall_site, cannon_line build, BATTLE light, army on, smoke), two set-ups:

    id 1  g 1035..1096  wide behind the enemy cannon row (cannon_line camera, slow crane-track to the right and up): six bronze guns
                        in a diagonal into depth toward BOTH wall sections (Lin's creamy one left, the general's taller grey one
                        right), fire pots, black banners, smoke columns rising.  Two gunners stand at guns 2 and 3 with smouldering
                        linstocks, then crouch toward the touch holes (from g 1080).
    id 2  g 1097..1158  medium, low, behind-right of the gunner at gun 3 (aimed at the general's section): he touches the glowing
                        match to the touch hole (g 1112), the fuse spits sparks (g 1113..1138), he ducks and covers his ears
                        (g 1128..), the gun FIRES (g 1140: muzzle flash, light, smoke; wall.set_impact('general', 0, t)); the ball
                        flies toward the wall (handle).  Cut to shot 15 (the macro: the ball hits the plain mortar).
Mouths: nobody speaks (static expression mouths only).  NO depth of field (C.Take).  Blender frame bf(id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py stills 1|2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
QA round 1 fixes: set-up 1 is a wider cannon_line view (20 mm) with 4 gunners (a big one in the foreground at gun 0, heads 75-90 px),
dust at their feet, stronger contact shadows; gunner_a keeps a closed frown; the set's opaque muzzle smoke / ball trail are replaced
by a soft bright muzzle flash at the barrel mouth + soft translucent smoke from the muzzle, and the camera eases up after the ball.
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402
import bpy                                               # noqa: E402

W, actors, cast9 = C.B, C.actors, C.cast9
import puppet                                            # noqa: E402
lerp, clamp, ez, blink = C.lerp, C.clamp, C.ez, C.blink
TMP = os.path.join(HERE, "work")

G0, G1, H = 1041, 1153, 6
G_CUT = 1097
RANGES = {1: (G0 - H, G_CUT - 1), 2: (G_CUT, G1 + H - 1)}
G_CROUCH_A = (1078, 1094)          # set-up 1: both gunners crouch toward the touch holes
G_CROUCH_B = (1100, 1112)          # set-up 2: gunner 3 brings the match down to the touch hole
G_TOUCH = 1112
G_DUCK = (1126, 1134)              # he ducks and covers his ears
G_FIRE = 1140                      # muzzle flash (set_impact t 0.02)

CX = W.CANNON_X; CY = W.CANNON_Y
GUN_A = Vector((CX[2] + 1.3, CY - 1.6, 0.0))      # gunner_a at gun 2 (x -2.5, aims at Lin's section)
GUN_B = Vector((CX[3] - 1.3, CY - 2.3, 0.0))      # gunner_b at gun 3 (x 4.5, aims at the general's section), on the gun's left,
                                                  # in front of its bucket: from both cameras the gun is screen-right of him
TOUCH = Vector((CX[3], CY - 1.05, 1.62))          # gun 3's touch hole (top of the breech)
# set-up 1 only (QA round 1: 'army missing / gunners too small'): two more gunners, one big in the foreground at the hero gun 0
GUN_A0 = Vector((CX[0] + 1.3, CY - 3.7, 0.0))     # gunner_a copy beside the trail of the hero gun 0 (x -16.5), near frame centre, mirrored
GUN_B1 = Vector((CX[1] + 1.3, CY - 1.6, 0.0))     # gunner_b copy at gun 1 (x -9.5), mirrored
CONTACT = dict(width=1.6, depth=0.7, color="#07050a", opacity=0.95)     # QA: visible contact shadows under the gunners

CAM = {1: (((-12.8, -44.0, 9.6), (2.0, -9.0, 1.4)), ((-11.6, -42.4, 9.0), (2.6, -9.0, 1.6))),   # QA r2: high oblique from back-left: ranks, the gun diagonal, Lin's + the general's sections + gate; track
       2: (((7.4, -37.0, 5.2), (1.6, -19.0, 2.4)), ((6.8, -35.8, 4.8), (1.4, -19.0, 2.6)))}   # QA r2: pulled back + up over the ranks (18 mm)
LENS = {1: 20.0, 2: 18.0}
PPD = {1: 160, 2: 288}
CANVAS = (-2.5, -5.25, 2.5, 0.125)


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def cam_of(shot, g):
    a, b = CAM[shot]; lo, hi = RANGES[shot]
    x = (g - lo) / float(hi - lo)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    loc, look = Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u))
    if shot == 2 and g > G_FIRE + 2:               # follow the ball: the look eases up toward it (it climbs out of the frame otherwise)
        w = ez(min(1.0, (g - G_FIRE - 2) / 14.0))
        look = look.lerp(ball_pos(g), 0.26 * w)
    if shot == 2 and g >= G_FIRE:                  # the shot's concussion: a short shake
        k = g - G_FIRE; amp = 0.10 * math.exp(-k / 5.0)
        loc += Vector((amp * math.sin(k * 2.3), 0.0, amp * math.cos(k * 3.1)))
    return loc, look


def ball_pos(g):
    """the set's flying ball at film frame g (set_impact general slot 0: muzzle -> decal centre, +3 D arc)."""
    t = impact_t(g); u = min(1.0, max(0.0, (t - 0.06) / 0.29))
    mz = Vector(W.STATE["muzzles"][3]); c = Vector(W.STATE["decals"]["general"][0]["c"])
    return mz.lerp(c, u) + Vector((0, 0, 12.0 * u * (1 - u)))


def impact_t(g):
    return 0.0 if g < G_FIRE - 1 else min(0.34, 0.02 + (g - G_FIRE) / 75.0)     # slower: the ball stays in view to the cut


# ----------------------------------------------------------------------------- poses
STAND = {"gunner_a": cast9.STORY9["gunner_stand"][1], "gunner_b": cast9.STORY9["gunner_stand_b"][1]}
LIGHT = {"gunner_a": cast9.STORY9["gunner_light"][1], "gunner_b": cast9.STORY9["gunner_light_b"][1]}
EARS = {"gunner_a": cast9.STORY9["gunner_ears"][1], "gunner_b": cast9.STORY9["gunner_ears_b"][1]}


def blend(cast, a, b, u, extra):
    p = puppet.lerp_pose(cast, a, b, u)
    p.update(extra)
    return p


def pose_gunner(cast, g, crouch, duck=0.0, seed=0.0, mirror=True, dust=0.0):
    """stand (linstock upright) -> light (crouched, match at the touch hole) -> ears (ducking).  Linstock angle tweened."""
    ang = lerp(-80.0, 32.0, crouch)
    if duck <= 0:
        p = blend(cast, STAND[cast], LIGHT[cast], crouch, dict(prop_r=dict(type="linstock", angle=ang)))
    else:
        p = blend(cast, LIGHT[cast], EARS[cast], duck, {})
        if duck < 0.5:
            p["prop_r"] = dict(type="linstock", angle=32.0)
    p["mirror"] = mirror                                   # gunner_a: gun screen-left (mirror); gunner_b: gun screen-right
    p["match_glow"] = 1.0
    p["t"] = g / 30.0
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.17 + seed)
    p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.11 + seed)
    if duck <= 0.3:
        p["blink"] = blink(g, [1050 + int(seed * 7), 1088 + int(seed * 5), 1118])
    if cast == "gunner_a":                                 # QA: his default face read as an open shouting mouth -> closed grimace
        p["mouth"] = "frown"
        p["expr"] = "shouting" if duck > 0.4 else "determined"
    if dust > 0:
        p["dust"] = dust
    return p


# ----------------------------------------------------------------------------- runtime dressing: fuse sparks at gun 3's touch hole
def make_sparks():
    m = bpy.data.materials.new("s14_spark"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (1.0, 0.75, 0.3, 1.0); em.inputs["Strength"].default_value = 30.0
    out = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], out.inputs[0])
    obs = []
    for k in range(9):
        me = bpy.data.meshes.new("s14_spark_%d" % k)
        import bmesh
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=6, v_segments=4, radius=0.035); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new("s14_spark_%d" % k, me); ob.data.materials.append(m)
        ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
        bpy.context.scene.collection.objects.link(ob); obs.append(ob)
    ld = bpy.data.lights.new("s14_fuse", "POINT"); ld.color = (1.0, 0.7, 0.35); ld.shadow_soft_size = 0.1; ld.energy = 0.0
    lo = bpy.data.objects.new("s14_fuse", ld); lo.location = TOUCH + Vector((0, 0, 0.2)); bpy.context.scene.collection.objects.link(lo)
    return obs, lo


def key_sparks(obs, lo, f, g):
    on = G_TOUCH <= g < G_FIRE
    for k, ob in enumerate(obs):
        ph = ((g * 0.37 + k * 0.29) % 1.0)
        a = k * 2.4 + g * 0.9
        ob.location = TOUCH + Vector((0.45 * ph * math.cos(a), 0.3 * ph * math.sin(a), 0.1 + 0.7 * ph - 0.6 * ph * ph))
        s = 1.0 - ph
        ob.scale = (s, s, s)
        ob.hide_render = not on
        ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f); ob.keyframe_insert("hide_render", frame=f)
    lo.data.energy = (60.0 + 40.0 * math.sin(g * 2.7) ** 2) if on else 0.0
    lo.data.keyframe_insert("energy", frame=f)



# ----------------------------------------------------------------------------- runtime: the shot of gun 3 (QA round 1)
# The set's muzzle smoke + 9-puff ball trail read as an opaque white cylinder from this camera: they are hidden every frame and
# replaced by a bright soft muzzle flash AT the barrel mouth, soft translucent billows that start at the muzzle and roll forward /
# up, and a flash light.  The set's ball (r 0.75, dark iron) flies on its own (set_impact) and now reads against the lit wall.
def _soft_mat(name, rgb, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
    inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
    pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 1.6
    op = nt.nodes.new("ShaderNodeValue"); op.name = "op"; op.outputs[0].default_value = 1.0
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = rgb + (1.0,); em.inputs["Strength"].default_value = strength
    em.name = "em"
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(lw.outputs["Facing"], inv.inputs[1]); nt.links.new(inv.outputs[0], pw.inputs[0])
    nt.links.new(pw.outputs[0], mul.inputs[0]); nt.links.new(op.outputs[0], mul.inputs[1]); nt.links.new(mul.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    return m


def _sphere(name, r, mat):
    import bmesh
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=r); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(mat)
    ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
    bpy.context.scene.collection.objects.link(ob); ob.hide_render = True
    return ob


MUZ_DIR = Vector((0.0, 1.0, 0.12)).normalized()


def make_blast():
    mz = Vector(W.STATE["muzzles"][3])
    fm = _soft_mat("s14_flash", (1.0, 0.82, 0.45), 30.0)
    flash = _sphere("s14_flash", 0.6, fm)
    core = _sphere("s14_flash_core", 0.35, _soft_mat("s14_flash_core", (1.0, 0.95, 0.8), 60.0))
    smoke = []
    for k in range(12):
        sm = _soft_mat("s14_smoke_%d" % k, (0.48, 0.43, 0.42), 0.8)
        smoke.append((_sphere("s14_smoke_%d" % k, 1.0, sm), sm, k))
    ld = bpy.data.lights.new("s14_blast", "POINT"); ld.color = (1.0, 0.72, 0.4); ld.shadow_soft_size = 0.6; ld.energy = 0.0
    lo = bpy.data.objects.new("s14_blast", ld); lo.location = mz + MUZ_DIR * 1.0 + Vector((0, 0, 0.6)); bpy.context.scene.collection.objects.link(lo)
    return dict(mz=mz, flash=flash, fmat=fm, core=core, smoke=smoke, light=lo)


def _key_ob(ob, f):
    ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f); ob.keyframe_insert("hide_render", frame=f)


def key_blast(B, f, g):
    # hide the set's opaque muzzle smoke, its flash ball and the ball trail (keyed after set_impact for this frame)
    S = W.STATE["slots"]["general"][0]; MF = W.STATE["muzzle_fx"][3]
    for o in [MF["smoke"], MF["flash"]] + list(S.get("trail", [])):
        o.hide_render = True; o.keyframe_insert("hide_render", frame=f)
    k = g - G_FIRE; mz = B["mz"]
    fl = math.exp(-max(0, k) / 1.6) if k >= 0 else 0.0
    for ob, s0 in ((B["flash"], 1.0), (B["core"], 1.0)):
        ob.location = mz + MUZ_DIR * (0.35 + 0.5 * min(1, max(0, k) / 2.0))
        s = s0 * (0.6 + 1.6 * min(1.0, (k + 1) / 2.0)) * (0.5 + 0.5 * fl) if k >= 0 else 0.1
        ob.scale = (s, s * 1.25, s)
        ob.hide_render = not (0 <= k <= 5)
        _key_ob(ob, f)
    for ob in (B["flash"], B["core"]):
        node = ob.data.materials[0].node_tree.nodes["op"].outputs[0]; node.default_value = fl; node.keyframe_insert("default_value", frame=f)
    B["light"].data.energy = 6000.0 * fl; B["light"].data.keyframe_insert("energy", frame=f)
    for ob, sm, j in B["smoke"]:
        age = k - 0.6 * j
        on = age > 0
        a = max(0.0, age)
        side = Vector((math.sin(j * 2.3) * 0.5, 0.0, math.cos(j * 1.7) * 0.35))
        ob.location = mz + MUZ_DIR * (0.6 + 4.2 * (1 - math.exp(-a / 7.0))) + side * (a / 10.0) + Vector((0.25 * a / 10.0, 0, 0.09 * a))
        s = 0.35 + 1.35 * (1 - math.exp(-a / 6.0)) + 0.15 * math.sin(j)
        ob.scale = (s, s * 0.9, s * 0.85)
        ob.hide_render = not on
        _key_ob(ob, f)
        op = sm.node_tree.nodes["op"].outputs[0]; op.default_value = (0.72 * math.exp(-a / 26.0)) if on else 0.0
        op.keyframe_insert("default_value", frame=f)
        em = sm.node_tree.nodes["em"].inputs["Strength"]; em.default_value = 0.8 + 4.0 * math.exp(-a / 3.0)   # fire-lit at first
        em.keyframe_insert("default_value", frame=f)


# ----------------------------------------------------------------------------- runtime (QA round 2): the army, shadows, the ball
# Ranks of enemy soldiers behind the gun row: static cards (cast9 gunners standing with upright linstocks / pikes, 8 drawings,
# mirrored, rasterised once) in 3 staggered rows; each card bobs a little (breathing) so the ranks are alive.  Dark soft shadow decals
# under every soldier, gunner and gun wheel.  The flying ball 1.5x with a fiery trail of glowing puffs and a warm rim light.
RANK_Y = (-28.4, -31.2)


def soldier_pngs():
    items = []
    for k in range(8):
        cast = "gunner_a" if k % 2 == 0 else "gunner_b"
        base = dict(cast9.STORY9["gunner_stand" if cast == "gunner_a" else "gunner_stand_b"][1])
        base.update(mirror=bool(k // 2 % 2), yaw=(0.15, 0.45, -0.2, 0.3)[k // 2], head_roll=(-3, 2, 4, -2)[k % 4],
                    expr=("determined", "angry", "neutral", "determined")[k % 4], mouth="flat" if cast == "gunner_a" else None,
                    prop_r=dict(type="linstock", angle=-84 + 4 * (k % 3)), match_glow=0.0 if k % 3 else 0.6, t=0.3 * k)
        if base.get("mouth") is None:
            base.pop("mouth", None)
        fig = puppet.figure(cast, base, "rk%d" % k)
        x0, y0, x1, y1 = fig["bbox"]; fy = fig["feet_y"]
        frag = '<g transform="translate(0,%.4f)">%s</g>' % (-fy, fig["svg"])
        box = (x0 - 0.1, y0 - fy - 0.1, x1 + 0.1, y1 - fy + 0.05)
        items.append((frag, box, 96))
    return C.svg_pngs(items, os.path.join(TMP, "ranks")), [b for _, b, _ in items]


def _shadow_mat():
    m = bpy.data.materials.get("s14_shadow")
    if m: return m
    m = bpy.data.materials.new("s14_shadow"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 0.35; mr.inputs["From Max"].default_value = 1.0
    mr.inputs["To Min"].default_value = 0.78; mr.inputs["To Max"].default_value = 0.0
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.012, 0.01, 0.02, 1.0); em.inputs["Strength"].default_value = 1.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tc.outputs["Object"], ln.inputs[0]); nt.links.new(ln.outputs["Value"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    return m


def shadow_decal(name, loc, rx, ry):
    import bmesh
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=True, segments=32, radius=1.0); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(_shadow_mat())
    ob.location = (loc[0], loc[1], 0.025); ob.scale = (rx, ry, 1.0)
    ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
    bpy.context.scene.collection.objects.link(ob)
    return ob


def make_army(shot, cam_loc):
    pngs, boxes = soldier_pngs()
    rnd = random.Random(9); cards = []
    for r, y in enumerate(RANK_Y):
        x = -21.5 + 1.15 * (r % 2)
        while x < 22.5:
            xx = x + rnd.uniform(-0.35, 0.35); yy = y + rnd.uniform(-0.4, 0.4)
            x += 1.9
            if shot == 2 and 0.5 < xx < 12.0:          # keep set-up 2's sight line onto gun 3 and its crew clear
                continue
            if any(abs(xx - gx) < 1.7 for gx in CX):     # a clear lane behind every gun: the guns read through the ranks
                continue
            if shot == 1 and (Vector((xx, yy)) - Vector(CAM[1][0][0][:2])).length < 14.5:   # heads of the nearest would cross y 880
                continue
            if any(abs(xx - gx) < 1.6 and abs(yy - gy) < 1.2 for gx, gy in ((GUN_A0.x, GUN_A0.y), (GUN_B1.x, GUN_B1.y))):
                continue
            v = rnd.randrange(len(pngs))
            pc = C.PropCard("s14_rank_%d_%d" % (r, len(cards)), [pngs[v]], boxes[v], scale=rnd.uniform(0.95, 1.05))
            pc.put((xx, yy, 0.0), face=cam_loc)
            shadow_decal("s14_rshadow_%d" % len(cards), (xx, yy), 0.75, 0.38)
            cards.append(dict(pc=pc, loc=Vector((xx, yy, 0.0)), ph=rnd.uniform(0, 6.28)))
    return cards


def key_army(cards, f, g):
    for c in cards:
        c["pc"].root.location = c["loc"] + Vector((0, 0, 0.025 * math.sin(g * 0.21 + c["ph"])))
        c["pc"].root.keyframe_insert("location", frame=f)


def make_static_shadows():
    for i, x in enumerate(CX):                                  # gun wheels (wheel centres x +-0.82, y CANNON_Y + 0.1) + trail end
        for sx in (-1, 1):
            shadow_decal("s14_wshadow_%d_%d" % (i, sx), (x + sx * 0.85, CY + 0.1), 0.42, 1.05)
        shadow_decal("s14_tshadow_%d" % i, (x, CY - 3.0), 0.45, 0.5)
    for k, p in enumerate((GUN_A, GUN_B, GUN_A0, GUN_B1)):          # under the 4 crews' feet
        shadow_decal("s14_gshadow_%d" % k, (p.x, p.y), 0.85, 0.42)


def make_ball_fx():
    trail = []
    for j in range(9):
        m = _soft_mat("s14_trail_%d" % j, (1.0, 0.55, 0.18), 7.0)
        trail.append((_sphere("s14_trail_%d" % j, 0.42 * (1.0 - j / 11.0), m), m, j))
    ld = bpy.data.lights.new("s14_ballrim", "POINT"); ld.color = (1.0, 0.62, 0.3); ld.shadow_soft_size = 0.3; ld.energy = 0.0
    lo = bpy.data.objects.new("s14_ballrim", ld); bpy.context.scene.collection.objects.link(lo)
    return dict(trail=trail, light=lo)


def key_ball_fx(Bf, f, g):
    S = W.STATE["slots"]["general"][0]; ball = S["ball"]
    ball.scale = (1.5, 1.5, 1.5); ball.keyframe_insert("scale", frame=f)
    t = impact_t(g); fly = 0.06 < t < 0.35
    p = ball_pos(g)
    for ob, m, j in Bf["trail"]:
        gj = g - 0.7 * (j + 1)
        q = ball_pos(gj); on = fly and impact_t(gj) > 0.06
        ob.location = q; ob.hide_render = not on
        ob.keyframe_insert("location", frame=f); ob.keyframe_insert("hide_render", frame=f)
        op = m.node_tree.nodes["op"].outputs[0]; op.default_value = 0.85 * (1.0 - j / 10.0) if on else 0.0
        op.keyframe_insert("default_value", frame=f)
    Bf["light"].location = p + Vector((0.6, 1.2, 1.1)); Bf["light"].keyframe_insert("location", frame=f)
    Bf["light"].data.energy = 900.0 if fly else 0.0; Bf["light"].data.keyframe_insert("energy", frame=f)


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        self.shot = shot
        C.Take.__init__(self, "wall_site", "cannon_line", quality=quality, lens=LENS[1], name="cam_s14", light="BATTLE")
        # wider canvas than the default: the linstock + its smoke wisp left the default canvas mid-swing (cast9 API known limit)
        sd = os.path.join(TMP, "sprites")
        self.ga = self.actors["ga"] = C.make_actor("ga", "gunner_a", sd, canvas=CANVAS, contact=CONTACT)
        self.gb = self.actors["gb"] = C.make_actor("gb", "gunner_b", sd, canvas=CANVAS, contact=CONTACT)
        self.ga0 = self.gb1 = None
        if shot == 1:
            self.ga0 = self.actors["ga0"] = C.make_actor("ga0", "gunner_a", sd, canvas=CANVAS, contact=CONTACT)
            self.gb1 = self.actors["gb1"] = C.make_actor("gb1", "gunner_b", sd, canvas=CANVAS, contact=CONTACT)
        self.sparks, self.fuse = make_sparks()
        self.blast = make_blast() if shot == 2 else None
        self.ballfx = make_ball_fx() if shot == 2 else None
        self.army = make_army(shot, CAM[shot][0][0])
        make_static_shadows()

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS[shot])
            C.place(self.ga, f, GUN_A); C.place(self.gb, f, GUN_B)
            if self.ga0 is not None:
                C.place(self.ga0, f, GUN_A0); C.place(self.gb1, f, GUN_B1)
            W.set_flames(1.0, frame=f)
            W.set_smoke(1.0, frame=f)
            if shot == 1:                                     # smoke columns near this high camera (camp fires) hid the view
                for b in W.STATE["smoke"]:
                    if b["base"].y < -30.0:
                        b["ob"].hide_render = True; b["ob"].keyframe_insert("hide_render", frame=f)
            W.set_army(True, frame=f)
            W.set_wall_height("lin", 26, frame=f); W.set_wall_height("general", 30, frame=f)
            W.set_cauldron_steam(0.4, frame=f)
            W.set_impact("general", 0, impact_t(g) if shot == 2 else 0.0, frame=f)
            key_sparks(self.sparks, self.fuse, f, g if shot == 2 else 0)
            if self.blast is not None:
                key_blast(self.blast, f, g)
            if self.ballfx is not None:
                key_ball_fx(self.ballfx, f, g)
            key_army(self.army, f, g)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 1:
                ca = u_of(g, *G_CROUCH_A); cb = u_of(g, G_CROUCH_A[0] + 4, G_CROUCH_A[1] + 4) * 0.55
                dust = 0.22 * (1.0 - 0.6 * u_of(g, 1040, 1096))        # the guns were just dragged up: light dust round the crews' feet
                pa = pose_gunner("gunner_a", g, ca, seed=0.0, dust=dust)
                pb = pose_gunner("gunner_b", g, cb, seed=1.3, mirror=False, dust=dust)
                c0 = u_of(g, G_CROUCH_A[0] - 6, G_CROUCH_A[1] - 6); c1 = u_of(g, G_CROUCH_A[0] + 2, G_CROUCH_A[1] + 2) * 0.8
                self.ga0.pose(f, pose_gunner("gunner_a", g, c0, seed=2.1, mirror=True, dust=dust), camera=self.cam)
                self.gb1.pose(f, pose_gunner("gunner_b", g, c1, seed=3.4, mirror=True, dust=dust), camera=self.cam)
            else:
                pa = pose_gunner("gunner_a", g, 1.0, duck=u_of(g, G_DUCK[0] + 3, G_DUCK[1] + 3), seed=0.0)
                pb = pose_gunner("gunner_b", g, max(0.55, u_of(g, *G_CROUCH_B)), duck=u_of(g, *G_DUCK), seed=1.3, mirror=False)
            self.ga.pose(f, pa, camera=self.cam)
            self.gb.pose(f, pb, camera=self.cam)
        jobs = [(self.ga, PPD[shot]), (self.gb, PPD[shot])] + ([(self.ga0, PPD[shot]), (self.gb1, PPD[shot])] if self.ga0 is not None else [])
        self.sprites_for(jobs, [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        rep = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), impact_t=round(impact_t(g), 4) if shot == 2 else 0)
        an = self.anch.get(("gb", f), {})
        for k in ("match_r", "match_l"):
            if k in an:
                w = actors.local_to_world(self.gb, an[k], f, camera=self.cam)
                rep["match_world"] = [round(v, 2) for v in w]
                rep["match_to_touch"] = round((w - TOUCH).length, 2)
        return rep

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    if cmd in ("probe", "stills"):
        Tk = Take("preview", shot)
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
        Tk.pose(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q, shot), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
