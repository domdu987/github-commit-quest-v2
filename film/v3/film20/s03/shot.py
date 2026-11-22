#!/usr/bin/env python3
"""shot.py -- film 20 take T03 = s03 = shots 3+4+5 as ONE continuous take (g 178..403; dissolve-in handle g 170..177, dissolve-out handle g 404..411). BIGZOOM 1 Paris -> Eiffel at the table (lands g 268), then the camera TRAVELS and CRANES up the scaffolded front-left leg past working riveters to the sky.
"วิศวกรไอเฟล" (event g 268): SITE site_table / DAY / stage 0.  EIFFEL at the plank plan table under a front leg, a rolled blueprint in hand,
looks at the plan, then points UP proudly (arm raises g 266..274, expression determined -> proud on the closed frame of a blink).
Camera: the preset lowered ~0.4 m and tilted up ~8 deg so the curved leg + scaffold (not the blank pier wall) fill the background; push 8 %/s
toward his head + 40 px/s slide; girder end FG in the nearest 15 %.   (1.77 s: no snap needed, < 2 s)
    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp] | hue g ..
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
import puppet                                            # noqa: E402

G0, G1 = C.g_bound(5.93), C.g_bound(13.47)     # 178, 404 (take = g 178..403)
H_IN, H_OUT = 8, 8                             # dissolve 13 in and out: 8 handle frames each side (director)
GF, G_LAST = G0 - H_IN, G1 + H_OUT - 1         # 170..411
G_TRAVEL = int(os.environ.get('GT', 314))                                 # the camera leaves Eiffel (after the point has landed)
G_MOST = C.cap_g("สูงที่สุดในโลก")                # 346: snap up
SNAP = (G_MOST - 2, G_MOST + 13)
GS = list(range(GF, G_LAST + 1))
G_WORD = C.cap_g("วิศวกรไอเฟล")                   # 268
G_LAND = 300                                   # the zoom lands on the medium ~g 300 (4.3 s push; at g 268 the point is already in a medium-wide)
RAISE = (G_WORD - 2, G_WORD + 6)               # arm rises to the point
G_SWAP = G_WORD + 2
PRESET, LIGHT, MARK = "site_bigzoom_land", "DAY", "eiffel_table"
PPD = 256
D0, D1 = 620.0, 4.6                            # camera distance to Eiffel (D): extreme wide -> medium
EL0, EL1 = 45.0, 8.0                          # elevation (deg): high over Paris -> low
AZ0, AZ1 = 261.0, 248.0                        # azimuth from the table (deg): ends south-south-west of him, wall to the side
SITE_CTR = CO.W((0.0, -90.0, 0.0))            # the middle of the four legs (D) the far start looks at
TILT1 = 16.0                                   # aim tilts UP by the end so the leg + scaffold fill the background



def dress(A):
    """runtime set dressing around the landing (never edits the set modules): brick texture on the pier, cream plans on the table, a warm
    lamp so Eiffel is findable from far away, a ladder, crates, a girder and rope coils against the pier face (y -67 m)."""
    import bpy
    M = CO.STATE["M"]
    # pier: brick texture on the stonedk material (object coordinates in metres)
    mt = M["stonedk"]
    nt = mt.node_tree
    bsdf = [n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"][0]
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Color1"].default_value = (0.70, 0.52, 0.36, 1)
    br.inputs["Color2"].default_value = (0.55, 0.38, 0.27, 1)
    br.inputs["Mortar"].default_value = (0.30, 0.22, 0.17, 1)
    br.inputs["Scale"].default_value = 1.1
    br.inputs["Mortar Size"].default_value = 0.025
    br.inputs["Brick Width"].default_value = 0.6
    br.inputs["Row Height"].default_value = 0.22
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["X"], add.inputs[0])
    nt.links.new(sep.outputs["Y"], add.inputs[1])
    nt.links.new(add.outputs["Value"], comb.inputs["X"])         # faces facing x or y both get (x+y, z): bricks on every wall
    nt.links.new(sep.outputs["Z"], comb.inputs["Y"])
    nt.links.new(comb.outputs["Vector"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], bsdf.inputs["Base Color"])
    # the plans: cream sheet instead of the saturated blue block
    mb = M["bluep"]
    for n in mb.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            n.inputs["Base Color"].default_value = (0.93, 0.87, 0.72, 1)
        if n.type == "MIX":                                          # the base colour is fed by a noise-driven Mix of two blues: make both cream
            n.inputs["A"].default_value = (0.80, 0.72, 0.52, 1)
            n.inputs["B"].default_value = (0.95, 0.88, 0.70, 1)
    mb.diffuse_color = (0.93, 0.87, 0.72, 1)
    R = CO.root()
    mbld = CO.MB("dressing", R)
    tx, ty = 50.7, -71.3
    # ladder against the pier face (x 44.5, leaning on y -67.2)
    for dx in (-0.25, 0.25):
        mbld.rod(M["timber"], (44.5 + dx, -69.0, 0.0), (44.5 + dx, -67.3, 5.0), 0.06, 0.06, 5)
    for i in range(1, 11):
        z = i * 0.46
        y = -69.0 + (-67.3 + 69.0) * z / 5.0
        mbld.box(M["timberdk"], (44.5, y, z), (0.55, 0.05, 0.05))
    # crates + sacks / girder lying + rope coils
    for (x, y, z, s_) in ((38.5, -68.2, 0.35, 0.7), (39.3, -68.4, 0.35, 0.7), (38.9, -68.3, 1.05, 0.7), (53.0, -68.0, 0.3, 0.6), (54.0, -68.2, 0.3, 0.6)):
        mbld.box(M["plank"], (x, y, z), (s_, s_, s_))
    mbld.box(M["redlead"], (47.0, -68.4, 0.2), (4.5, 0.3, 0.4), rz=0.12)
    mbld.box(M["redlead"], (47.0, -68.4, 0.55), (4.5, 0.1, 0.3), rz=0.12)
    for (x, y) in ((43.0, -69.5), (56.0, -70.0)):
        mbld.cyl(M["rope"], (x, y, 0.15), 0.45, 0.3, "z", 14)
    # warm lamp on a pole beside the table (findable from far away)
    mbld.rod(M["timberdk"], (tx - 1.6, ty + 0.6, 0.0), (tx - 1.6, ty + 0.6, 3.2), 0.05, 0.05, 5)
    mbld.finish()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=(0, 0, 0))
    lamp = bpy.context.active_object
    lamp.name = "dress_lamp"
    lm = bpy.data.materials.new("dress_lamp_m")
    lm.use_nodes = True
    nd = lm.node_tree.nodes
    for n in list(nd):
        nd.remove(n)
    em = nd.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.62, 0.18, 1)
    em.inputs["Strength"].default_value = 5.0
    out = nd.new("ShaderNodeOutputMaterial")
    lm.node_tree.links.new(em.outputs["Emission"], out.inputs["Surface"])
    lamp.data.materials.append(lm)
    lamp.parent = R
    lamp.location = (tx - 1.6, ty + 0.6, 3.4)
    A['lamp'] = lamp



def make_glow_and_fill(A):
    """a big warm glow sphere above Eiffel's table (scaled up at the start so the eye finds him; the set's own beacon is sub-pixel) and a warm
    fill light on the table front / Eiffel for the landing."""
    import bpy
    R = CO.root()
    m = A["marks"][MARK]
    pos = (m[0] / CO.SC * CO.SC, m[1], m[2])                                  # marks are world D: keep them as they are
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
    gl = bpy.context.active_object
    gl.name = "bz_glow"
    lm = bpy.data.materials.new("bz_glow_m")
    lm.use_nodes = True
    nd = lm.node_tree.nodes
    for n in list(nd):
        nd.remove(n)
    em = nd.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.58, 0.10, 1)
    em.inputs["Strength"].default_value = 2.2
    out = nd.new("ShaderNodeOutputMaterial")
    lm.node_tree.links.new(em.outputs["Emission"], out.inputs["Surface"])
    gl.data.materials.append(lm)
    gl.visible_shadow = False
    gl.location = (pos[0], pos[1], pos[2] + 5.5 * CO.SC)                      # 5.5 m above the ground at his table
    bpy.ops.object.light_add(type="POINT", location=(pos[0] - 3.0, pos[1] - 6.0, pos[2] + 4.5))
    fill = bpy.context.active_object
    fill.name = "bz_fill"
    fill.data.color = (1.0, 0.78, 0.55)
    fill.data.energy = 4000.0
    fill.data.shadow_soft_size = 3.0
    gp = bpy.data.materials.get("gravelp")                                      # the pale gravel patches read as white domes: make them dirt-coloured
    if gp is not None and gp.use_nodes:
        for n in gp.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                n.inputs["Base Color"].default_value = (0.62, 0.38, 0.22, 1)
            for i in n.inputs:
                if i.type == "RGBA" and n.type in ("MIX", "VALTORGB") and hasattr(i, "default_value"):
                    i.default_value = (0.58, 0.36, 0.21, 1)
    fb = bpy.data.materials.get("flag_b")                                      # the flag's blue renders pure black in shade: lift it to a real blue
    if fb is not None and fb.use_nodes:
        for n in fb.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                n.inputs["Base Color"].default_value = (0.10, 0.22, 0.70, 1)
            for i in n.inputs:
                if i.type == "RGBA" and n.type in ("MIX", "VALTORGB") and hasattr(i, "default_value"):
                    i.default_value = (0.10, 0.24, 0.72, 1)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0, location=(0, 0, 0))
    sh = bpy.context.active_object
    sh.name = "bz_shaft"
    sm = bpy.data.materials.new("bz_shaft_m")
    sm.use_nodes = True
    nd2 = sm.node_tree.nodes
    for n in list(nd2):
        nd2.remove(n)
    e2 = nd2.new("ShaderNodeEmission")
    e2.inputs["Color"].default_value = (1.0, 0.72, 0.35, 1)
    e2.inputs["Strength"].default_value = 4.0
    tr = nd2.new("ShaderNodeBsdfTransparent")
    mx = nd2.new("ShaderNodeMixShader")
    mx.inputs[0].default_value = 0.45
    o2 = nd2.new("ShaderNodeOutputMaterial")
    sm.node_tree.links.new(tr.outputs[0], mx.inputs[1])
    sm.node_tree.links.new(e2.outputs[0], mx.inputs[2])
    sm.node_tree.links.new(mx.outputs[0], o2.inputs["Surface"])
    sh.data.materials.append(sm)
    sh.visible_shadow = False
    sh.location = (pos[0], pos[1], pos[2] + 2.0)
    bpy.ops.object.light_add(type="POINT", location=(0, 0, 0))
    up = bpy.context.active_object
    up.name = "bz_up"
    up.data.color = (1.0, 0.72, 0.45)
    up.data.energy = 0.0
    up.data.shadow_soft_size = 4.0
    A["bz_glow"], A["bz_fill"], A["bz_shaft"], A["bz_up"] = gl, fill, sh, up


HIDE_SCATTER = ("pnoink_white", "pm_timber", "pm_timberdk", "pm_metal", "pf_coal", "pf_soot", "pf_rivet", "pf_metal", "pf_stonedk", "pm_coal", "pm_soot", "pm_rivet", "pm_metal", "pm_stonedk", "pn_coal", "pn_soot", "pn_rivet", "pn_stonedk")   # the small near-black scatter that reads as debris


V2_HIDE = ("pm_redlead", "pm_crimson", "pf_redlead", "pf_crimson", "pnoink_redleadlt", "pm_dark")      # v2: lying girders / crates / bits that hovered (z 2-3 above the dirt)


def v2_fix_scene(T):
    """v2 (client: nothing floats): hide the floating girder chunks, give the white canopy 4 thick legs to the ground, ground-darken the pier slab
    with a contact blob, and tag everything for ground_check."""
    import bpy, bmesh
    from mathutils import Vector
    for n in V2_HIDE:
        ob = bpy.data.objects.get(n)
        if ob is not None:
            ob.hide_render = True
    M = CO.STATE["M"]
    def box(name, cx, cy, z0, z1, hw, mat):
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            v.co = Vector((cx + v.co.x * 2 * hw, cy + v.co.y * 2 * hw, z0 + (v.co.z + 0.5) * (z1 - z0)))
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        ob.data.materials.append(mat)
        ob["gc_role"] = "prop"
        return ob
    for i, (x, y) in enumerate(((66.5, -152.7), (74.9, -152.7), (66.5, -145.9), (74.9, -145.9))):
        box("canopy_leg_%d" % i, x, y, 0.0, 6.25, 0.28, M["timberdk"])
    for n in ("pnoink_canvasw", "pnoink_crimson", "pn_tablewood", "beacon_beacon_g", "bz_glow", "bz_shaft", "bz_up", "bz_fill"):
        ob = bpy.data.objects.get(n)
        if ob is not None:
            ob["gc_role"] = "skip"
    # contact blobs: canopy (under the roof, soft) and pier foot ring
    def blob(name, cx, cy, w, d, op):
        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(cx, cy, 0.06))
        ob = bpy.context.active_object
        ob.name = name
        ob.scale = (w, d, 1.0)
        m = bpy.data.materials.new(name + "_m")
        m.use_nodes = True
        nd = m.node_tree.nodes
        for n in list(nd):
            nd.remove(n)
        tr = nd.new("ShaderNodeBsdfTransparent")
        bk = nd.new("ShaderNodeBsdfDiffuse")
        bk.inputs["Color"].default_value = (0.05, 0.04, 0.06, 1)
        tc = nd.new("ShaderNodeTexCoord")
        gr = nd.new("ShaderNodeTexGradient")
        gr.gradient_type = "SPHERICAL"
        mp = nd.new("ShaderNodeMapping")
        mp.inputs["Location"].default_value = (-0.5, -0.5, 0)
        cr = nd.new("ShaderNodeMapRange")
        cr.inputs["From Min"].default_value = 0.0
        cr.inputs["From Max"].default_value = 0.5
        cr.inputs["To Min"].default_value = op
        cr.inputs["To Max"].default_value = 0.0
        cr.clamp = True
        mx = nd.new("ShaderNodeMixShader")
        o = nd.new("ShaderNodeOutputMaterial")
        L = m.node_tree.links
        L.new(tc.outputs["UV"], mp.inputs["Vector"]); L.new(mp.outputs["Vector"], gr.inputs["Vector"])
        L.new(gr.outputs["Fac"], cr.inputs["Value"]); L.new(cr.outputs["Result"], mx.inputs[0])
        L.new(tr.outputs[0], mx.inputs[1]); L.new(bk.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], o.inputs["Surface"])
        ob.data.materials.append(m)
        ob.visible_shadow = False
        ob["gc_role"] = "shadow"
    blob("canopy_gcshadow", 70.7, -149.3, 14.0, 11.0, 0.55)
    for nm in ("leg_a", "leg_b", "leg_c"):                       # scaffold platforms under the riveters (they stood on nothing)
        mk = T.A["marks"][nm]
        d = box("plankdeck_" + nm, mk[0] + 0.8, mk[1], mk[2] - 0.35, mk[2], 1.0, M["plank"])
        for v in d.data.vertices:
            v.co.x = mk[0] + 0.8 + (v.co.x - (mk[0] + 0.8)) * 3.6
            v.co.y = mk[1] + (v.co.y - mk[1]) * 1.6
        d["gc_role"] = "ground"


def trap(u, a=0.32):
    """eased trapezoid 0..1 (C1; accelerates over a, cruises, decelerates over a): peak speed 1/(1-a) x mean, lower than smoothstep's 1.5-1.9x"""
    u = clamp(u, 0.0, 1.0)
    k = 1.0 / (1.0 - a)
    if u < a:
        return k * u * u / (2.0 * a)
    if u > 1.0 - a:
        return 1.0 - k * (1.0 - u) ** 2 / (2.0 * a)
    return k * (u - a / 2.0)


def smoother(u):
    u = clamp(u, 0.0, 1.0)
    return u * u * u * (u * (u * 6 - 15) + 10)


class ZoomPath(C.CamPath):
    """BIGZOOM: spherical path about Eiffel's body: distance D0 -> D1 (geometric), elevation EL0 -> EL1, azimuth AZ0 -> AZ1, all on one
    smootherstep over g 178..268 (ease in/out), then a slow drift (push 5 %/s, azimuth -3 deg/s) so it never parks."""

    def __init__(self, A):
        m = Vector(A["marks"][MARK])
        self.subj = m + Vector((0.0, 0.0, 1.7))
        C.CamPath.__init__(self, self.subj + Vector((1, 0, 0)), self.subj, GF, G_LAST, push=0, decay=0.0)

    KEYS = ((GF, 620.0), (G0, 560.0), (203, 39.0), (G_LAND, D1))     # camera distance to Eiffel (D): ~10 px figure at g 178, 64 px (5 %) at g 196, medium (~540 px) at g 300

    def lnd(self, g):
        ks = self.KEYS
        g = clamp(g, ks[0][0], ks[-1][0])
        for (ga, da), (gb, db) in zip(ks, ks[1:]):
            if g <= gb:
                u = (g - ga) / float(gb - ga)
                return math.log(da) + (math.log(db) - math.log(da)) * u
        return math.log(ks[-1][1])

    @staticmethod
    def lens(p):
        """22 mm until p 0.55, then eased to the 62 mm of site_bigzoom_land (Eiffel head ~178 px)"""
        return 22.0 + 40.0 * smoother((p - 0.55) / 0.45)

    @staticmethod
    def shift(p):
        """lens shift_y: +0.37 (site_bigzoom_start: picture pushed down, sky band on top) -> 0.08 (mid) -> 0 at the landing"""
        return 0.20 * (1.0 - smoother(p / 0.6))

    def prog(self, g):
        """smoothed log-distance (13-frame box) -> progress 0..1 of the BIGZOOM"""
        l = sum(self.lnd(g + k) for k in range(-6, 7)) / 13.0
        return clamp((math.log(self.KEYS[0][1]) - l) / (math.log(self.KEYS[0][1]) - math.log(D1)), 0.0, 1.0), l

    def state(self, g):
        p, l = self.prog(g)
        tau = max(0.0, (g - G_LAND) / 30.0)
        d = math.exp(l) * (1.0 - 0.10 * tau) * self.lens(p) / 22.0          # d_eff x lens/22: the figure keeps the same on-screen size as with a 22 mm lens
        el = lerp(EL0, EL1, p)
        az = lerp(AZ0, AZ1, p) - 9.0 * tau
        return d, el, az, 0.0

    def at(self, g):
        d, el, az, tilt = self.state(g)
        e, a = math.radians(el), math.radians(az)
        off = Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e))) * d
        loc = self.subj + off
        p = self.prog(g)[0]
        tgt = self.subj.lerp(SITE_CTR, 0.75 * math.exp(-7.0 * p))          # at the start the aim is between Eiffel and the middle of the site (legs around him), then it closes on Eiffel
        fwd = (tgt - loc).normalized()
        r = Vector((fwd.y, -fwd.x, 0.0)).normalized()
        from mathutils import Matrix
        aim = Matrix.Rotation(math.radians(tilt), 3, r) @ fwd
        return loc, loc + aim * d

    def tilt(self, g):
        return self.state(g)[3]


LEG_FWD = -2.0                                 # m: the leg camera starts this much nearer the foot than the preset (smaller sacks)
LIFT = float(os.environ.get('LIFTV', 60.0))                                    # D: the camera lifts over the yard / pier while it travels (clears the stone block)


class TravelPath(ZoomPath):
    """ZoomPath (BIGZOOM to the table, drift parked after 0.6 s) then, from G_TRAVEL, a blend of position AND aim to the front-left-leg
    camera (site_leg_low moved LEG_FWD m nearer): crane lift over the pier, aim pans ~135 deg, pitch 14 -> 36 deg + a +9 deg SNAP on
    'สูงที่สุดในโลก' (g 344-359).  Moving on both ends (10 % linear in the blend)."""

    def __init__(self, A):
        ZoomPath.__init__(self, A)
        c = A["cams"]["site_leg_low"]
        l, k = Vector(c["loc"]), Vector(c["look_at"])
        h = k - l
        h.z = 0.0
        self.h = h.normalized()
        self.locC = l + self.h * (LEG_FWD * CO.SC)

    def at(self, g):
        from mathutils import Matrix
        la, ka = ZoomPath.at(self, min(g, G_LAST) if g <= G_TRAVEL else G_TRAVEL)
        if g <= G_TRAVEL:
            return la, ka
        u = clamp((g - G_TRAVEL) / float(G_LAST - G_TRAVEL), 0.0, 1.0)
        wm = os.environ.get("WMODE", "trap45")
        w = {"trap": lambda: trap(u), "front": lambda: smoother(u ** 0.75), "trap45": lambda: trap(u, float(os.environ.get("TA", 0.5))), "ss": lambda: smoother(u)}[wm]()      # v2: one smooth eased crane (no fast blend, no shake)
        pitch = lerp(8.0, 22.0, w) + 6.0 * smoother((g - SNAP[0]) / float(SNAP[1] - SNAP[0]))
        dC = self.h * math.cos(math.radians(pitch)) + Vector((0, 0, math.sin(math.radians(pitch))))
        dA = (ka - la).normalized()
        loc = la.lerp(self.locC, w) + Vector((0, 0, LIFT * math.sin(math.pi * w)))
        d = (dA * (1.0 - w) + dC * w).normalized()
        return loc, loc + d * 20.0

    def tilt(self, g):
        return 0.0


def cam_path(A):
    return TravelPath(A)


def cam_path_static():
    return cam_path(dict(marks={MARK: CO.W((50.7, -71.3, 0.0))}, cams={"site_leg_low": dict(loc=CO.W((-60.0, -82.0, 1.4)), look_at=CO.W((-52.0, -58.0, 14.0)))}))


EIF_A = cast20.STORY20["eiffel_blueprint"][1]
EIF_B = cast20.STORY20["eiffel_point_up"][1]


def pose_of(g):
    u = u_of(g, *RAISE) * (1.0 - u_of(g, 316, 326))                    # arm up g 266-274, held, down g 316-326 (hand on hip, proud)
    p = dict(puppet.lerp_pose("eiffel", EIF_A, EIF_B, u))
    p["expr"] = "determined" if g < G_SWAP else "proud"
    p["yaw"] = lerp(0.35, 0.45, u)
    p["lean"] = lerp(0.0, -3.0, u) + 1.2 * math.sin(g * 0.21)
    p["squash"] = (1.0, 1.0 + 0.010 * math.sin(g * 0.3))
    p["head_roll"] = 2.0 * math.sin(g * 0.17) + 3.0 * ez(u)
    p["blink"] = blink(g, [G_SWAP - 1, 300])
    p["t"] = g / 30.0
    return p


RIV = [("rv_a", "riveter_hammer", (28.0, -75.0), False), ("rv_b", "riveter_tongs", (42.0, -76.0), True), ("rv_c", "riveter_forge", (24.0, -80.0), False)]


def riv_pose(kind, g, k):
    ph = g * 0.7 + k * 1.9
    if kind == "riveter_hammer":
        a, b = cast20.STORY20["riveter_hammer_work"][1], cast20.STORY20["riveter_hammer_hit"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph), 0, 1) ** 2
    elif kind == "riveter_tongs":
        a, b = cast20.STORY20["riveter_tongs_work"][1], cast20.STORY20["riveter_tongs_throw"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph * 0.5), 0, 1)
    else:
        a, b = cast20.STORY20["riveter_forge_work"][1], cast20.STORY20["riveter_forge_lift"][1]
        u = clamp(0.5 - 0.5 * math.cos(ph * 0.4), 0, 1)
    p = dict(puppet.lerp_pose(kind, a, b, u))
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.3 + k))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s03")
        bc = C.bpy.data.objects.get("beacon_beacon_g")                # v2: the beacon column (top z 13.3) was taken for ground: Eiffel stood 12.7 D in the air
        if bc is not None:
            bc.hide_viewport = True
            C.bpy.context.view_layer.update()
        mk0 = self.A["marks"][MARK]
        mx, my = mk0[0] - 2.4, mk0[1] - 6.4                          # v2: in front of the plan table (camera side), not behind / inside it
        self.A["marks"][MARK] = (mx, my, C.ground_z(mx, my, top=6.0))
        if bc is not None:
            bc.hide_viewport = False
        for ob in C.bpy.data.objects:                               # the preset's near-black FG slabs (anchored to the preset camera): camera-invisible
            if ob.name in ("fg_redlead_sh", "fg_dark_sh", "fg_metal_sh", "fg_timber_sh") or ob.name.startswith(("derricks_", "swinggirder")):
                ob.visible_camera = False
            if ob.name in HIDE_SCATTER or ob.name.startswith("pnoink_flag"):
                ob.hide_render = True                                  # removed entirely (no cast shadow blobs either)
        v2_fix_scene(self)
        self.cam.data.clip_end = 6000.0
        self.smoke, self.gravel = C.bpy.data.objects.get("pnoink_smokep"), C.bpy.data.objects.get("pn_gravelp")
        make_glow_and_fill(self.A)
        self.path = cam_path(self.A)
        self.key_cam(bf(GF), *self.path.at(GF))
        self.scene.frame_set(bf(GF))
        self.eif = self.actors["eif"] = C.make_actor("eif", "eiffel", os.path.join(WORK, "sprites"), contact=dict(width=1.4, depth=0.6, opacity=0.8),
                                                     cam=self.cam)
        self.riv = []
        for name, cast, xy, mirror in RIV:
            a = C.make_actor(name, cast, os.path.join(WORK, "sprites"), contact=dict(width=1.2, depth=0.5, opacity=0.8), cam=self.cam)
            self.actors[name] = a
            mk = C.on_ground(CO.W((xy[0], xy[1], 0.0)))
            self.riv.append((a, cast, mk, mirror, 1.0))
        for name, cast, mark, mirror in (("rl_a", "riveter_hammer", "leg_a", False), ("rl_b", "riveter_tongs", "leg_b", True), ("rl_c", "riveter_forge", "leg_c", False), ("rl_d", "riveter_forge", "leg_a", True), ("rl_e", "riveter_hammer", "leg_b", False), ("rl_f", "riveter_tongs", "leg_c", True)):
            a = C.make_actor(name, cast, os.path.join(WORK, "sprites"), contact=False, cam=self.cam)       # on a deck: no ground decal
            self.actors[name] = a
            mk3 = list(self.A["marks"][mark])
            if name in ("rl_d", "rl_e", "rl_f"):
                mk3[0] += 1.6                                   # second worker on the same platform
            zz = C.ground_z(mk3[0], mk3[1], top=mk3[2] + 0.5)            # v2: stand ON the deck / beam under the mark (no hovering riveters)
            if name in ("rl_d", "rl_e", "rl_f"):
                mk3[2] -= 0.23                                  # their poses carry the feet ~0.23 D higher in the card: sink onto the plank deck
            self.riv.append((a, cast, tuple(mk3), mirror, 2.4))                           # x2.4: reads on the platforms

    def pose(self, gs):
        mark = self.A["marks"][MARK]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.eif, f, mark)
            for a, cast, mk, mirror, sc in self.riv:
                C.place(a, f, mk, scale=sc)
            d_m = self.path.state(g)[0] / CO.SC                                  # camera distance in metres
            p = self.path.prog(g)[0]
            gk = clamp(self.path.state(g)[0] * 12.0 / 782.0, 0.0, 70.0) * (1.0 - smoother((p - 0.40) / 0.25)) * (1.0 - smoother((g - 176) / 14.0))   # glow radius ~ 7 px on screen while far, gone well before the landing
            self.A["bz_glow"].scale = (max(gk, 1e-3),) * 3
            self.A["bz_glow"].keyframe_insert("scale", frame=f)
            fade = 1.0 - smoother((p - 0.40) / 0.25)
            wsh = 1e-3                                                          # the shaft is dropped (the warm glow alone is findable)
            _unused = max(self.path.state(g)[0] * 3.0 / 782.0 * fade, 1e-3)          # a soft vertical light shaft ~3 px wide, ~90 px tall while far
            hsh = 1e-3
            self.A["bz_shaft"].scale = (wsh, wsh, hsh)
            self.A["bz_shaft"].location = (self.A["bz_shaft"].location[0], self.A["bz_shaft"].location[1], self.A["marks"][MARK][2] + hsh * 0.5)
            self.A["bz_shaft"].keyframe_insert("scale", frame=f)
            self.A["bz_shaft"].keyframe_insert("location", frame=f)
            lc = self.path.at(g)[0]
            self.A["bz_up"].location = (lc[0], lc[1], lc[2] + 2.5)
            self.A["bz_up"].data.energy = 9000.0 * smoother((g - 322) / 40.0) + 18000.0 * smoother((g - 345) / 20.0)       # warm up-light into the deck undersides during the crane-up
            self.A["bz_up"].keyframe_insert("location", frame=f)
            self.A["bz_up"].data.keyframe_insert("energy", frame=f)
            for ob, hid in ((self.smoke, g >= 340), (self.gravel, g <= 215)):          # source-less smoke puffs g 340+, the pale gravel disc g <= 215
                if ob is not None:
                    ob.hide_render = bool(hid)
                    ob.keyframe_insert("hide_render", frame=f)
            self.cam.data.lens = self.path.lens(p)
            self.cam.data.shift_y = self.path.shift(p) + 0.10 * smoother((p - 0.55) / 0.45) * (1.0 - smoother((g - 312) / 60.0))      # v2: figure lower in the frame at the landing (less bare dirt)
            self.cam.data.keyframe_insert("lens", frame=f)
            self.cam.data.keyframe_insert("shift_y", frame=f)
            fe = smoother((p - 0.7) / 0.3)
            self.A["bz_fill"].data.energy = 4000.0 * fe
            self.A["bz_fill"].data.keyframe_insert("energy", frame=f)
            self.key_set(f, set_beacon=bool(p < 0.22))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.eif.pose(f, pose_of(g), camera=self.cam)
            for i, (a, cast, mk, mirror, sc) in enumerate(self.riv):
                p = riv_pose(cast, g, i)
                if mirror:
                    p["mirror"] = True
                a.pose(f, p, camera=self.cam)
        self.sprites_for([(self.eif, PPD)] + [(a, 160) for a, _, _, _, _ in self.riv], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = cam_path_static().report(GS[:-1])
        for r in rows[::5]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (max 6)" % worst)
        sys.exit(0)
    if cmd == "hue":
        gs = [int(v) for v in sys.argv[2:]]
        Tk = Take("final"); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], os.path.join(WORK, "hue"))[0]
            print(g, json.dumps(C.hue_frame(st["path"])), flush=True)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
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
