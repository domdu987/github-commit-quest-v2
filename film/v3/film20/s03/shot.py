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
G_TRAVEL = 280                                 # the camera leaves Eiffel (after the point has landed)
G_MOST = C.cap_g("สูงที่สุดในโลก")                # 346: snap up
SNAP = (G_MOST - 2, G_MOST + 13)
GS = list(range(GF, G_LAST + 1))
G_WORD = C.cap_g("วิศวกรไอเฟล")                   # 268
G_LAND = G_WORD                                # the zoom lands on the medium at the word
RAISE = (G_WORD - 2, G_WORD + 6)               # arm rises to the point
G_SWAP = G_WORD + 2
PRESET, LIGHT, MARK = "site_table", "DAY", "eiffel_table"
PPD = 256
D0, D1 = 400.0, 4.6                            # camera distance to Eiffel (D): extreme wide -> medium
EL0, EL1 = 52.0, 7.0                           # elevation (deg): high over Paris -> low
AZ0, AZ1 = 228.0, 221.0                        # azimuth from the table (deg, 225 = the preset camera's side)
SITE_CTR = CO.W((0.0, -30.0, 25.0))            # the middle of the four legs (D) the far start looks at
TILT1 = 13.0                                   # aim tilts UP by the end so the leg + scaffold fill the background



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
    em.inputs["Strength"].default_value = 18.0
    out = nd.new("ShaderNodeOutputMaterial")
    lm.node_tree.links.new(em.outputs["Emission"], out.inputs["Surface"])
    lamp.data.materials.append(lm)
    lamp.parent = R
    lamp.location = (tx - 1.6, ty + 0.6, 3.4)
    A['lamp'] = lamp


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

    def state(self, g):
        u = clamp((g - GF) / float(G_LAND - GF), 0.0, 1.0)
        s = 0.10 * u + 0.90 * smoother(u)          # ease in/out, but already moving on frame 0 (never parked)
        tau = max(0.0, (g - G_LAND) / 30.0)
        d = D0 * (D1 / D0) ** s * (1.0 - 0.10 * tau)
        el = lerp(EL0, EL1, s)
        az = lerp(AZ0, AZ1, s) - 9.0 * tau
        return d, el, az, lerp(0.0, TILT1, s)

    def at(self, g):
        d, el, az, tilt = self.state(g)
        e, a = math.radians(el), math.radians(az)
        off = Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e))) * d
        loc = self.subj + off
        u0 = clamp((g - GF) / float(G_LAND - GF), 0.0, 1.0)
        tgt = self.subj.lerp(SITE_CTR, (1.0 - smoother(u0)) ** 1.5)          # at the start the aim is the middle of the site (all 4 legs), then it closes on Eiffel
        fwd = (tgt - loc).normalized()
        r = Vector((fwd.y, -fwd.x, 0.0)).normalized()
        from mathutils import Matrix
        aim = Matrix.Rotation(math.radians(tilt), 3, r) @ fwd
        return loc, loc + aim * d

    def tilt(self, g):
        return self.state(g)[3]


LEG_FWD = 5.0                                  # m: the leg camera starts this much nearer the foot than the preset (smaller sacks)
LIFT = 14.0                                    # D: the camera lifts over the yard / pier while it travels (clears the stone block)


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
        w = 0.06 * u + 0.94 * smoother(u ** 0.55)        # leaves Eiffel quickly (no half-body lingering at the frame edge)
        pitch = lerp(10.0, 36.0, u) + 9.0 * C.snap_u(g, SNAP[0], SNAP[1], 1.7)
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
    u = u_of(g, *RAISE) * (1.0 - u_of(g, 292, 302))                    # arm up g 266-274, held, down g 292-302 (hand on hip, proud)
    p = dict(puppet.lerp_pose("eiffel", EIF_A, EIF_B, u))
    p["expr"] = "determined" if g < G_SWAP else "proud"
    p["yaw"] = lerp(0.35, 0.45, u)
    p["lean"] = lerp(0.0, -3.0, u) + 1.2 * math.sin(g * 0.21)
    p["squash"] = (1.0, 1.0 + 0.010 * math.sin(g * 0.3))
    p["head_roll"] = 2.0 * math.sin(g * 0.17) + 3.0 * ez(u)
    p["blink"] = blink(g, [G_SWAP - 1, 300])
    p["t"] = g / 30.0
    return p


RIV = [("rv_a", "riveter_hammer", (41.5, -68.6), False), ("rv_b", "riveter_tongs", (57.5, -69.4), True), ("rv_c", "riveter_forge", (35.0, -69.2), False)]


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
        self.A["marks"][MARK] = C.on_ground(self.A["marks"][MARK])
        for ob in C.bpy.data.objects:                               # the preset's near-black FG slabs (anchored to the preset camera): camera-invisible
            if ob.name in ("fg_redlead_sh", "fg_dark_sh", "fg_metal_sh", "fg_timber_sh") or ob.name.startswith(("derricks_", "swinggirder")):
                ob.visible_camera = False
        self.cam.data.clip_end = 6000.0
        dress(self.A)
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
        for name, cast, mark, mirror in (("rl_a", "riveter_hammer", "leg_a", False), ("rl_b", "riveter_tongs", "leg_b", True), ("rl_c", "riveter_forge", "leg_c", False)):
            a = C.make_actor(name, cast, os.path.join(WORK, "sprites"), contact=False, cam=self.cam)       # on a deck: no ground decal
            self.actors[name] = a
            self.riv.append((a, cast, tuple(self.A["marks"][mark]), mirror, 2.4))                           # x2.4: reads on the platforms

    def pose(self, gs):
        mark = self.A["marks"][MARK]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.eif, f, mark)
            for a, cast, mk, mirror, sc in self.riv:
                C.place(a, f, mk, scale=sc)
            lk = 1.0 + 6.0 * (1.0 - smoother((g - GF) / float(G_LAND - GF)))        # the warm lamp is big when we are far (findable), normal at the landing
            self.A["lamp"].scale = (lk, lk, lk)
            self.A["lamp"].keyframe_insert("scale", frame=f)
            self.key_set(f)
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
