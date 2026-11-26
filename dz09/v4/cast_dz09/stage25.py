"""stage25.py -- 2.5D puppets in a Blender (bpy 5.3, Cycles) scene.

Each actor is an Empty (the floor point under the feet) carrying one card per drawn layer (pack, far arm, far leg,
torso, head, face, hair, near arm, props ...).  The cards are parallel, `gap` D apart along the card normal, so a
moving camera sees real parallax between body parts.  Every card is EMISSION ONLY (never lit by Cycles) but its
emission colour is the drawing passed through a small toon model that reads the scene lights:

    colour = fill                                   where the pseudo-normal faces the key light
           = mix(fill * 0.55, SHADE_RGB, 0.35)      in the one shade band (blue-violet, hue ~245) away from it
           + sum_i  light_i * att_i * (rim * edge-band facing light i  +  wash * card facing light i)
           + wet glints (Blinn half-vector step, sparse noise mask) when the cast is wet

The pseudo-normal is computed from each layer's silhouette (raster25.normal_map), so the head gets the crescent of
the v2 rule and the sleeves and trouser legs get a round band, while the inside of every shape stays flat.
Lights are read from Blender objects by `sync_lights()` (one shared node group, so all actors agree).
Shadows: the layer cards do not cast shadows (that would stack them); one hidden proxy card with the flat
silhouette casts them, turned to face the chosen shadow light; a soft contact decal sits under the feet.

    import stage25 as st
    st.setup_render(scene, 360, 640, samples=16, denoise=True)
    a = st.Actor25("kong", "kong", gap=0.05, ppd=160, mode="25d")      # or mode="flat" (one emission card, v3 style)
    a.place((0, 0, 0), facing_deg=0)          # facing: the direction the character's front points (deg about Z, 0 = -Y)
    st.sync_lights(key="Moon", rims=["Beacon", "Sodium"], shadow="Sodium")
    a.pose({"expr": "determined", "arm_l": "hold", "prop_l": {"type": "cutter", "bars": 3}}, camera=scene.camera)
    bpy.ops.render.render(write_still=True)
"""
import math, os, sys
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import draw25d, raster25

SHADE_RGB = (0.50, 0.50, 0.78)       # shade multiplier: blue-violet (a white fill shades to hue ~240), keeps darks dark
GROUP = "DZ25_toon"
N_RIM = 3
YAW_RANGE_DEG = 60.0                 # rel yaw of +/-60 deg maps to drawing yaw +/-1: front < 18 deg, 3/4 18-48, side > 48 (review: was 35, which showed a full profile at a 28 deg camera offset; the ref/c puppets stay frontal/3-4 under orbits)

# ----------------------------------------------------------------------------------------------- render setup
def setup_render(scene, w=360, h=640, samples=16, denoise=True, threads=4):
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.render.threads_mode = "FIXED"
    scene.render.threads = threads
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.resolution_percentage = 100
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = bool(denoise)
    if denoise:
        scene.cycles.denoiser = "OPENIMAGEDENOISE"
    scene.cycles.max_bounces = 4
    scene.cycles.diffuse_bounces = 1
    scene.cycles.glossy_bounces = 2
    scene.cycles.transmission_bounces = 0
    scene.cycles.volume_bounces = 0
    scene.cycles.transparent_max_bounces = 48       # up to ~14 stacked layer cards + rain streaks
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    try:
        scene.render.use_motion_blur = False
    except Exception:
        pass


# ----------------------------------------------------------------------------------------------- shader group
def _ng_new():
    ng = bpy.data.node_groups.new(GROUP, "ShaderNodeTree")
    it = ng.interface
    it.new_socket("Color", in_out="INPUT", socket_type="NodeSocketColor")
    it.new_socket("Alpha", in_out="INPUT", socket_type="NodeSocketFloat")
    it.new_socket("Normal", in_out="INPUT", socket_type="NodeSocketVector")
    it.new_socket("Shade", in_out="INPUT", socket_type="NodeSocketFloat")
    it.new_socket("Wet", in_out="INPUT", socket_type="NodeSocketFloat")
    it.new_socket("Rim", in_out="INPUT", socket_type="NodeSocketFloat")
    it.new_socket("Shader", in_out="OUTPUT", socket_type="NodeSocketShader")
    N = ng.nodes
    Lk = ng.links
    gi = N.new("NodeGroupInput")
    go = N.new("NodeGroupOutput")
    geo = N.new("ShaderNodeNewGeometry")

    def node(t, name=None, **kw):
        n = N.new(t)
        if name:
            n.name = n.label = name
        for k, v in kw.items():
            setattr(n, k, v)
        return n

    def inp(n, i, v):
        if hasattr(v, "is_output") or hasattr(v, "links"):
            Lk.new(v, n.inputs[i])
        else:
            n.inputs[i].default_value = v

    def vm(op, a, b=None, s=None):
        n = node("ShaderNodeVectorMath", operation=op)
        inp(n, 0, a)
        if b is not None:
            inp(n, 1, b)
        if s is not None:
            inp(n, 3, s)
        return n.outputs["Value"] if op in ("DOT_PRODUCT", "LENGTH", "DISTANCE") else n.outputs["Vector"]

    def m(op, a, b=None, clamp=False):
        n = node("ShaderNodeMath", operation=op, use_clamp=clamp)
        inp(n, 0, a)
        if b is not None:
            inp(n, 1, b)
        return n.outputs[0]

    def mr(x, a, b, smooth=True):
        n = node("ShaderNodeMapRange", interpolation_type="SMOOTHSTEP" if smooth else "LINEAR", clamp=True)
        inp(n, 0, x)
        n.inputs[1].default_value, n.inputs[2].default_value = a, b
        n.inputs[3].default_value, n.inputs[4].default_value = 0.0, 1.0
        return n.outputs[0]

    def val(name, v):
        n = node("ShaderNodeValue", name)
        n.outputs[0].default_value = v
        return n.outputs[0]

    def xyz(name, v):
        n = node("ShaderNodeCombineXYZ", name)
        for i in range(3):
            n.inputs[i].default_value = v[i]
        return n.outputs[0]

    base = gi.outputs["Color"]
    Nn = vm("NORMALIZE", gi.outputs["Normal"])
    Nc = geo.outputs["Normal"]
    V = geo.outputs["Incoming"]
    P = geo.outputs["Position"]
    # ---- toon key
    Lkey = vm("NORMALIZE", xyz("key_dir", (0.3, -0.5, 0.8)))
    lit = vm("DOT_PRODUCT", Nn, Lkey)
    thr = val("toon_thr", 0.05)
    toon = mr(m("SUBTRACT", lit, thr), -0.03, 0.03)
    toonf = m("SUBTRACT", 1.0, m("MULTIPLY", gi.outputs["Shade"], m("SUBTRACT", 1.0, toon)))
    shade_k = val("shade_k", 0.55)
    shade_col = xyz("shade_rgb", SHADE_RGB)
    sc2 = vm("ADD", vm("SCALE", vm("MULTIPLY", base, shade_col), s=m("DIVIDE", shade_k, 0.55)),
             xyz("shade_lift", (0.004, 0.004, 0.012)))
    col = vm("ADD", sc2, vm("SCALE", vm("SUBTRACT", base, sc2), s=toonf))
    edge = m("SUBTRACT", 1.0, vm("DOT_PRODUCT", Nn, Nc))
    edge_band = mr(edge, 0.03, 0.10)
    rim_amt = m("MULTIPLY", val("rim_amt", 1.0), gi.outputs["Rim"])
    wash_amt = val("wash_amt", 0.25)
    glint_amt = val("glint_amt", 1.5)
    # sparse glint mask (wet)
    tc = node("ShaderNodeTexCoord")
    nz = node("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 18.0
    nz.inputs["Detail"].default_value = 1.0
    Lk.new(tc.outputs["Object"], nz.inputs["Vector"])
    gmask = m("MULTIPLY", mr(nz.outputs["Fac"], 0.60, 0.66), gi.outputs["Wet"])
    acc = col
    # albedo factor for rim / wash: fill * alb_k + alb_floor (ink ~0.04, white 1.0)
    alb = vm("ADD", vm("SCALE", base, s=val("alb_k", 0.96)), xyz("alb_floor", (0.04, 0.04, 0.05)))
    # key glint
    Hk = vm("NORMALIZE", vm("ADD", Lkey, V))
    gk = m("MULTIPLY", mr(vm("DOT_PRODUCT", Nn, Hk), 0.975, 0.99), gmask)
    keycol = xyz("key_col", (0.6, 0.7, 1.0))
    acc = vm("ADD", acc, vm("SCALE", keycol, s=m("MULTIPLY", gk, glint_amt)))
    for i in range(N_RIM):
        Pi = xyz("rim%d_pos" % i, (0, 0, -1000))
        Ci = xyz("rim%d_col" % i, (0, 0, 0))
        Ri = val("rim%d_rad" % i, 6.0)
        d = vm("SUBTRACT", Pi, P)
        dist = vm("LENGTH", d)
        Li = vm("NORMALIZE", d)
        att = m("DIVIDE", 1.0, m("ADD", 1.0, m("POWER", m("DIVIDE", dist, Ri), 2.0)))
        face = mr(vm("DOT_PRODUCT", Nn, Li), 0.10, 0.28)
        rim = m("MULTIPLY", m("MULTIPLY", face, edge_band), rim_amt)
        wash = m("MULTIPLY", m("MAXIMUM", vm("DOT_PRODUCT", Nc, Li), 0.0), wash_amt)
        Hi = vm("NORMALIZE", vm("ADD", Li, V))
        gl = m("MULTIPLY", m("MULTIPLY", mr(vm("DOT_PRODUCT", Nn, Hi), 0.97, 0.99), gmask), glint_amt)
        # rim + wash are light reflected by the drawn surface, so they scale with its fill (albedo): black ink,
        # hair and trousers stay black instead of turning into red / brown stripes (review fix); glints stay white.
        kr = m("MULTIPLY", m("ADD", rim, wash), att)
        acc = vm("ADD", acc, vm("MULTIPLY", vm("SCALE", Ci, s=kr), alb))
        acc = vm("ADD", acc, vm("SCALE", Ci, s=m("MULTIPLY", gl, att)))
    expo = val("exposure", 1.0)
    acc = vm("SCALE", acc, s=expo)
    em = node("ShaderNodeEmission")
    Lk.new(acc, em.inputs["Color"])
    em.inputs["Strength"].default_value = 1.0
    tr = node("ShaderNodeBsdfTransparent")
    mx = node("ShaderNodeMixShader")
    Lk.new(gi.outputs["Alpha"], mx.inputs[0])
    Lk.new(tr.outputs[0], mx.inputs[1])
    Lk.new(em.outputs[0], mx.inputs[2])
    Lk.new(mx.outputs[0], go.inputs["Shader"])
    return ng


def toon_group():
    ng = bpy.data.node_groups.get(GROUP)
    return ng or _ng_new()


def set_toon(**kw):
    """exposure, rim_amt, wash_amt, glint_amt, shade_k, toon_thr"""
    ng = toon_group()
    for k, v in kw.items():
        ng.nodes[k].outputs[0].default_value = v


def _set_xyz(ng, name, v):
    n = ng.nodes[name]
    for i in range(3):
        n.inputs[i].default_value = float(v[i])


def sync_lights(key=None, rims=(), shadow=None, rim_gain=1.0, radius=None):
    """copy light objects into the shared toon group.  key: a SUN (its -Z axis) or a point light (direction from
    the scene centre).  rims: up to 3 point/spot/area lights, colour x energy normalised.  shadow: the light the
    shadow proxies of the actors face (default: key)."""
    ng = toon_group()
    if key:
        ob = bpy.data.objects[key]
        if ob.data.type == "SUN":
            d = ob.matrix_world.to_3x3() @ Vector((0, 0, 1))
        else:
            d = (ob.matrix_world.translation - Vector((0, 0, 1.5))).normalized()
        _set_xyz(ng, "key_dir", d)
        _set_xyz(ng, "key_col", tuple(ob.data.color))
    for i in range(N_RIM):
        if i < len(rims):
            ob = bpy.data.objects[rims[i]]
            c = ob.data.color
            e = rim_gain * ob.get("rim_gain", 1.0)
            _set_xyz(ng, "rim%d_pos" % i, ob.matrix_world.translation)
            _set_xyz(ng, "rim%d_col" % i, (c[0] * e, c[1] * e, c[2] * e))
            ng.nodes["rim%d_rad" % i].outputs[0].default_value = float(ob.get("rim_radius", radius or 6.0))
        else:
            _set_xyz(ng, "rim%d_col" % i, (0, 0, 0))
    global _SHADOW_LIGHT
    _SHADOW_LIGHT = shadow or key


_SHADOW_LIGHT = None


# ----------------------------------------------------------------------------------------------- materials
def _img(path, colorspace="sRGB"):
    im = bpy.data.images.get(os.path.basename(path) + "|" + colorspace)
    if im is None or im.filepath != path:
        im = bpy.data.images.load(path, check_existing=False)
        im.name = os.path.basename(path) + "|" + colorspace
        im.colorspace_settings.name = colorspace
        im.alpha_mode = "STRAIGHT"
    return im


def _card_material(name, flat=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.cycles.emission_sampling = "NONE"
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.name = "color"
    tex.interpolation = "Linear"
    tex.extension = "CLIP"
    if flat:
        em = nt.nodes.new("ShaderNodeEmission")
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(tex.outputs["Color"], em.inputs["Color"])
        nt.links.new(tex.outputs["Alpha"], mx.inputs[0])
        nt.links.new(tr.outputs[0], mx.inputs[1])
        nt.links.new(em.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs["Surface"])
        return m
    ntex = nt.nodes.new("ShaderNodeTexImage")
    ntex.name = "normal"
    ntex.interpolation = "Linear"
    ntex.extension = "EXTEND"
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.space = "TANGENT"
    nm.uv_map = "UVMap"
    g = nt.nodes.new("ShaderNodeGroup")
    g.node_tree = toon_group()
    g.name = "toon"
    nt.links.new(ntex.outputs["Color"], nm.inputs["Color"])
    nt.links.new(tex.outputs["Color"], g.inputs["Color"])
    nt.links.new(tex.outputs["Alpha"], g.inputs["Alpha"])
    nt.links.new(nm.outputs["Normal"], g.inputs["Normal"])
    g.inputs["Shade"].default_value = 1.0
    g.inputs["Wet"].default_value = 0.0
    g.inputs["Rim"].default_value = 1.0
    nt.links.new(g.outputs["Shader"], out.inputs["Surface"])
    return m


def _plane(name, x0, x1, z0, z1, mat, parent):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for i, (u, v) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[i].uv = (u, v)
    me.update()
    # face normal must point to local -Y (the front); vertices above give +Y? flip if needed
    if me.polygons[0].normal.y > 0:
        me.flip_normals()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = parent
    return ob


# ----------------------------------------------------------------------------------------------- the actor
SLOTS = ["pack", "hairback", "arm_r", "arm_l", "prop_r", "prop_l", "leg_r", "leg_l", "torso", "head", "face", "hair"]


class Actor25(object):
    def __init__(self, name, cast, gap=0.05, ppd=160, canvas=(-2.0, -1.25, 2.0, 3.25), mode="25d", follow=0.5,
                 sprite_dir=None, contact=True, normal_radius=0.15):
        self.normal_radius = normal_radius
        self.name, self.cast, self.gap, self.ppd, self.canvas, self.mode, self.follow = name, cast, gap, ppd, canvas, mode, follow
        self.dir = sprite_dir or os.path.join(HERE, "tmp", "sprites", name)
        os.makedirs(self.dir, exist_ok=True)
        self.root = bpy.data.objects.new(name, None)
        bpy.context.scene.collection.objects.link(self.root)
        self.facing = 0.0
        self.view = None
        self.cards = {}
        x0, y0, x1, y1 = canvas
        self.pivot = bpy.data.objects.new(name + "_pivot", None)       # rotates toward the camera by `follow`
        bpy.context.scene.collection.objects.link(self.pivot)
        self.pivot.parent = self.root
        if mode == "flat":
            m = _card_material(name + "_flat", flat=True)
            self.cards["flat"] = _plane(name + "_flat", x0, x1, -y1, -y0, m, self.pivot)
            self.cards["flat"].visible_shadow = False
        else:
            for s in SLOTS:
                m = _card_material("%s_%s" % (name, s))
                ob = _plane("%s_%s" % (name, s), x0, x1, -y1, -y0, m, self.pivot)
                ob.visible_shadow = False
                self.cards[s] = ob
        # shadow proxy: flat silhouette, invisible to the camera, casts the shadow
        pm = bpy.data.materials.new(name + "_proxy")
        pm.use_nodes = True
        nt = pm.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        o = nt.nodes.new("ShaderNodeOutputMaterial")
        t = nt.nodes.new("ShaderNodeTexImage")
        t.name = "color"
        d = nt.nodes.new("ShaderNodeBsdfDiffuse")
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(t.outputs["Alpha"], mx.inputs[0])
        nt.links.new(tr.outputs[0], mx.inputs[1])
        nt.links.new(d.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], o.inputs["Surface"])
        self.proxy_root = bpy.data.objects.new(name + "_proxyroot", None)
        bpy.context.scene.collection.objects.link(self.proxy_root)
        self.proxy_root.parent = self.root
        self.proxy = _plane(name + "_proxy", x0, x1, -y1, -y0, pm, self.proxy_root)
        for a in ("visible_camera", "visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter"):
            setattr(self.proxy, a, False)
        self.proxy.visible_shadow = True
        # contact shadow decal
        self.contact = None
        if contact:
            cm = bpy.data.materials.new(name + "_contact")
            cm.use_nodes = True
            cm.cycles.emission_sampling = "NONE"
            nt = cm.node_tree
            for n in list(nt.nodes):
                nt.nodes.remove(n)
            o = nt.nodes.new("ShaderNodeOutputMaterial")
            tc = nt.nodes.new("ShaderNodeTexCoord")
            gr = nt.nodes.new("ShaderNodeTexGradient")
            gr.gradient_type = "SPHERICAL"
            mp = nt.nodes.new("ShaderNodeMapRange")
            mp.inputs[1].default_value, mp.inputs[2].default_value = 0.0, 1.0
            mp.inputs[3].default_value, mp.inputs[4].default_value = 0.0, 0.85
            mp.interpolation_type = "SMOOTHSTEP"
            em = nt.nodes.new("ShaderNodeEmission")
            em.inputs["Color"].default_value = (0.004, 0.004, 0.012, 1)
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            mx = nt.nodes.new("ShaderNodeMixShader")
            nt.links.new(tc.outputs["Object"], gr.inputs["Vector"])
            nt.links.new(gr.outputs["Fac"], mp.inputs[0])
            nt.links.new(mp.outputs[0], mx.inputs[0])
            nt.links.new(tr.outputs[0], mx.inputs[1])
            nt.links.new(em.outputs[0], mx.inputs[2])
            nt.links.new(mx.outputs[0], o.inputs["Surface"])
            me = bpy.data.meshes.new(name + "_contact")
            me.from_pydata([(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)], [], [(0, 1, 2, 3)])
            me.materials.append(cm)
            ob = bpy.data.objects.new(name + "_contact", me)
            bpy.context.scene.collection.objects.link(ob)
            ob.parent = self.root
            ob.location = (0, 0, 0.004)
            ob.scale = (0.75, 0.42, 1)
            ob.visible_shadow = False
            self.contact = ob
        self.last = None

    # -------------------------------------------------------------------------------------------
    def place(self, loc, facing_deg=0.0):
        self.root.location = loc
        self.facing = facing_deg

    def rel_yaw(self, camera):
        """drawing yaw in degrees: + when the character faces screen-right as seen from the camera."""
        a = math.radians(self.facing)
        f = Vector((math.sin(a), -math.cos(a), 0.0))           # front vector (facing 0 = toward -Y)
        t = camera.matrix_world.translation - self.root.matrix_world.translation
        t.z = 0
        t.normalize()
        right = Vector((-t.y, t.x, 0.0))                       # camera's right as seen looking at the actor
        return math.degrees(math.atan2(f.dot(right), f.dot(t))), t

    def pose(self, pose, camera=None, extra_yaw_deg=0.0, view_lock=None):
        P = dict(pose or {})
        rel, t = (0.0, None)
        if camera is not None:
            rel, t = self.rel_yaw(camera)
        rel += extra_yaw_deg + P.pop("yaw_deg", 0.0)
        y = max(-1.2, min(1.2, rel / YAW_RANGE_DEG))
        # view with hysteresis (0.04 of drawing yaw)
        e0, e1 = draw25d.VIEW_EDGES
        a = abs(y)
        v = "front" if a < e0 else "q" if a < e1 else "side"
        if self.view and v != self.view:
            vv = self.view
            lo, hi = {"front": (0, e0), "q": (e0, e1), "side": (e1, 9)}[vv]
            if lo - 0.04 <= a <= hi + 0.04:
                v = vv
        if self.mode == "flat":                       # the v3-style sticker: one drawing, card turned to the camera
            v = view_lock or "front"
            y = 0.0 if v == "front" else y
        elif view_lock:
            v = view_lock
        self.view = v
        P["yaw"] = y
        P["view"] = v
        P.setdefault("uid", self.name)
        fig = draw25d.build(self.cast, P)
        self.last = fig
        fx, fy = fig["feet"]
        # pivot: turn the card stack part of the way toward the camera (follow), about the feet
        fol = 1.0 if self.mode == "flat" else self.follow
        piv = math.radians(self.facing - fol * rel)
        self.pivot.rotation_euler = (0, 0, piv)
        wet = 1.0 if draw25d.CAST25[self.cast].get("wet") else 0.0
        if self.mode == "flat":
            p = os.path.join(self.dir, "flat.png")
            raster25.flat_png(fig, self.canvas, self.ppd, p)
            p2 = os.path.join(self.dir, "flat_%s.png" % raster25.hashlib.sha1(open(p, "rb").read()).hexdigest()[:12])
            if not os.path.exists(p2):
                os.link(p, p2)
            c = self.cards["flat"]
            c.data.materials[0].node_tree.nodes["color"].image = _img(p2)
            _fit_card(c, p2, self.canvas)
            c.location = (-fx, 0, fy)
            layers = {"flat": None}
        else:
            res = raster25.layer_pngs(fig, self.canvas, self.ppd, os.path.join(self.dir, "_tmp"), tag="L",
                                      normal_radius_D=self.normal_radius)
            for s, ob in self.cards.items():
                if s not in res:
                    ob.hide_render = True
                    continue
                r = res[s]
                ob.hide_render = False
                # unique file per drawing (Blender caches images by path)
                cp = _uniq(r["color"])
                npth = _uniq(r["normal"])
                nt = ob.data.materials[0].node_tree
                nt.nodes["color"].image = _img(cp)
                nt.nodes["normal"].image = _img(npth, "Non-Color")
                _fit_card(ob, cp, self.canvas)
                nt.nodes["toon"].inputs["Shade"].default_value = r["shade"]
                nt.nodes["toon"].inputs["Rim"].default_value = r.get("rim", 1.0)
                nt.nodes["toon"].inputs["Wet"].default_value = wet if r["kind"] != "face" else 0.0
                ob.location = (-fx, -r["z"] * self.gap, fy)
        # shadow proxy faces the shadow light (about the feet), keeps the flat silhouette
        pp = os.path.join(self.dir, "proxy.png")
        raster25.flat_png(fig, self.canvas, max(64, self.ppd // 2), pp)
        pp2 = _uniq(pp)
        self.proxy.data.materials[0].node_tree.nodes["color"].image = _img(pp2)
        _fit_card(self.proxy, pp2, self.canvas)
        self.proxy.location = (-fx, 0, fy)
        ang = self.facing
        if _SHADOW_LIGHT and _SHADOW_LIGHT in bpy.data.objects:
            L = bpy.data.objects[_SHADOW_LIGHT]
            if L.data.type == "SUN":
                d = L.matrix_world.to_3x3() @ Vector((0, 0, 1))
            else:
                d = L.matrix_world.translation - self.root.matrix_world.translation
            ang = math.degrees(math.atan2(-d.x, d.y)) + 180.0
            # face the light, but never more than 70 degrees away from the visible card
            dv = (ang - (self.facing - self.follow * rel) + 180) % 360 - 180
            if abs(dv) > 90:
                dv = dv - math.copysign(180, dv)
            ang = (self.facing - self.follow * rel) + max(-70, min(70, dv))
        self.proxy_root.rotation_euler = (0, 0, math.radians(ang))
        return fig

    def screen_points(self, scene, camera, names=("head", "hand_l", "hand_r", "feet")):
        """world -> pixel of anchors of the last pose, using the card each anchor lives on."""
        from bpy_extras.object_utils import world_to_camera_view
        fig = self.last
        bpy.context.view_layer.update()
        out = {}
        slot = {"head": "head", "hand_l": "arm_l", "hand_r": "arm_r", "feet": "torso", "shoulder_l": "arm_l",
                "shoulder_r": "arm_r", "hip": "torso", "mouth": "face"}
        for n in names:
            x, y = fig["anchors"][n]
            card = self.cards.get(slot.get(n, "torso")) or self.cards.get("flat")
            w = card.matrix_world @ Vector((x, 0, -y))
            c = world_to_camera_view(scene, camera, w)
            out[n] = (c.x * scene.render.resolution_x, (1 - c.y) * scene.render.resolution_y)
        return out


_UQ = {}
_BBOX = {}


def _fit_card(ob, png, canvas, pad=3):
    """shrink a card's quad (and its UVs) to the opaque part of its sprite (review fix).  Every layer used to be a
    full-canvas quad, so each camera ray through the character's 4 x 4.5 D box crossed up to 13 transparent quads;
    cropping removes most of those transparent hits and so most of the 2.5D render overhead."""
    bb = _BBOX.get(png)
    if bb is None:
        from PIL import Image
        im = Image.open(png)
        W, H = im.size
        a = im.getchannel("A") if "A" in im.getbands() else None
        box = a.point(lambda v: 255 if v > 2 else 0).getbbox() if a is not None else None
        if box is None:
            bb = (0.0, 0.0, 0.001, 0.001)          # empty layer: a speck (the card is effectively gone)
        else:
            l, t, r, b = box
            l, t, r, b = max(0, l - pad), max(0, t - pad), min(W, r + pad), min(H, b + pad)
            bb = (l / W, 1.0 - b / H, r / W, 1.0 - t / H)
        _BBOX[png] = bb
    u0, v0, u1, v1 = bb
    x0, y0, x1, y1 = canvas
    X0, X1 = x0 + u0 * (x1 - x0), x0 + u1 * (x1 - x0)
    Z0, Z1 = -y1 + v0 * (y1 - y0), -y1 + v1 * (y1 - y0)
    me = ob.data
    vs = me.vertices
    uvl = me.uv_layers["UVMap"].data
    # vertex i keeps its corner role: find corners by their current sign in x and z
    xs = [v.co.x for v in vs]
    zs = [v.co.z for v in vs]
    xm, zm = (max(xs) + min(xs)) / 2, (max(zs) + min(zs)) / 2
    hi = {}
    for v in vs:
        hx, hz = v.co.x > xm, v.co.z > zm
        hi[v.index] = (hx, hz)
        v.co.x, v.co.z = (X1 if hx else X0), (Z1 if hz else Z0)
    for li, loop in enumerate(me.loops):
        hx, hz = hi[loop.vertex_index]               # (float32 coords: compare corner flags, never floats)
        uvl[li].uv = (u1 if hx else u0, v1 if hz else v0)
    me.update()


def _uniq(path):
    """hard-link a sprite to a file named by its content hash so Blender never reuses a stale image."""
    import hashlib
    h = hashlib.sha1(open(path, "rb").read()).hexdigest()[:14]
    d = os.path.join(os.path.dirname(path), "_u")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, h + ".png")
    if not os.path.exists(p):
        os.link(path, p)
    return p
