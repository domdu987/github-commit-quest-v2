"""bc_mat.py -- procedural Cycles materials for the blocky cast (no downloaded textures; the only images are the
code-drawn face decals, the star-of-life patch and the ID card).

Every mask is computed in REST space (the mesh attribute 'rest', metres from the soles, the figure facing -Y), so
dirt, blood and drips stay on the cloth when the limbs move:
  dirt   = height falloff (boots, hems) + a knee band, broken by noise, plus all-over mottling
  blood  = splats placed by code (centre, radius, drip length) with noisy edges, drips that run down, fine specks
  tears  = code-placed holes painted as skin + blood rim (zombie shirt / slacks)
  wet    = darker, glossier base, a clear coat and voronoi rain droplets (bumped, mirror-like)
Reflective tape is a retro-reflector: a glossy lobe whose normal is the view vector, so lights near the camera are
sent straight back into the lens (the tape flares under camera-side lights and stays grey otherwise).
Black stays black (base <= 0.03 linear, wet gloss is a clear coat, not a lighter base); orange is mixed in linear
with multiplicative grime only, so it keeps its hue and saturation.
"""
import os, math
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))


class NB:
    """tiny node builder."""

    def __init__(self, mat):
        mat.use_nodes = True
        self.nt = mat.node_tree; self.N = self.nt.nodes; self.Lk = self.nt.links
        for n in list(self.N): self.N.remove(n)
        self.out = self.N.new("ShaderNodeOutputMaterial")

    def link(self, a, b):
        self.Lk.new(a, b)

    def _in(self, sock, x):
        if x is None: return
        if isinstance(x, (int, float)): sock.default_value = x
        elif isinstance(x, (tuple, list)):
            v = tuple(x)
            if len(sock.default_value) == 4 and len(v) == 3: v = v + (1.0,)
            sock.default_value = v
        else: self.Lk.new(x, sock)

    def node(self, t, **props):
        n = self.N.new(t)
        for k, v in props.items(): setattr(n, k, v)
        return n

    def math(self, op, a, b=None, c=None, clamp=False):
        n = self.node("ShaderNodeMath", operation=op, use_clamp=clamp)
        self._in(n.inputs[0], a)
        if b is not None: self._in(n.inputs[1], b)
        if c is not None: self._in(n.inputs[2], c)
        return n.outputs[0]

    def vmath(self, op, a, b=None, sc=None):
        n = self.node("ShaderNodeVectorMath", operation=op)
        self._in(n.inputs[0], a)
        if b is not None: self._in(n.inputs[1], b)
        if sc is not None: self._in(n.inputs["Scale"], sc)
        return n.outputs["Value"] if op in ("LENGTH", "DOT_PRODUCT", "DISTANCE") else n.outputs["Vector"]

    def mix(self, f, a, b, blend="MIX"):
        n = self.node("ShaderNodeMix", data_type="RGBA", blend_type=blend)
        self._in(n.inputs[0], f); self._in(n.inputs[6], a); self._in(n.inputs[7], b)
        return n.outputs[2]

    def mixf(self, f, a, b):
        n = self.node("ShaderNodeMix", data_type="FLOAT")
        self._in(n.inputs[0], f); self._in(n.inputs[2], a); self._in(n.inputs[3], b)
        return n.outputs[0]

    def sep(self, v):
        n = self.node("ShaderNodeSeparateXYZ"); self._in(n.inputs[0], v)
        return n.outputs[0], n.outputs[1], n.outputs[2]

    def comb(self, x, y, z):
        n = self.node("ShaderNodeCombineXYZ")
        for i, a in enumerate((x, y, z)): self._in(n.inputs[i], a)
        return n.outputs[0]

    def noise(self, v, scale, detail=2.0, rough=0.5, w=None):
        n = self.node("ShaderNodeTexNoise")
        self._in(n.inputs["Vector"], v); n.inputs["Scale"].default_value = scale
        n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough
        return n.outputs["Fac"]

    def voronoi(self, v, scale, feature="F1", rand=1.0):
        n = self.node("ShaderNodeTexVoronoi", feature=feature)
        self._in(n.inputs["Vector"], v); n.inputs["Scale"].default_value = scale
        n.inputs["Randomness"].default_value = rand
        return n.outputs["Distance"], n.outputs["Color"]

    def ss(self, x, a, b):
        """smoothstep from a (0) to b (1); a > b inverts."""
        n = self.node("ShaderNodeMapRange", interpolation_type="SMOOTHSTEP", clamp=True)
        self._in(n.inputs["Value"], x)
        if a > b:
            n.inputs["From Min"].default_value = b; n.inputs["From Max"].default_value = a
            n.inputs["To Min"].default_value = 1.0; n.inputs["To Max"].default_value = 0.0
        else:
            n.inputs["From Min"].default_value = a; n.inputs["From Max"].default_value = b
        return n.outputs["Result"]

    def rest(self):
        if not hasattr(self, "_rest"):
            a = self.node("ShaderNodeAttribute", attribute_type="GEOMETRY", attribute_name="rest")
            self._rest = a.outputs["Vector"]
        return self._rest

    def attr(self, name):
        a = self.node("ShaderNodeAttribute", attribute_type="GEOMETRY", attribute_name=name)
        return a.outputs["Fac"]

    def bump(self, h, strength, dist=0.002, normal=None):
        n = self.node("ShaderNodeBump")
        self._in(n.inputs["Height"], h); n.inputs["Strength"].default_value = strength
        n.inputs["Distance"].default_value = dist
        if normal is not None: self._in(n.inputs["Normal"], normal)
        return n.outputs["Normal"]

    def principled(self, **kw):
        b = self.node("ShaderNodeBsdfPrincipled")
        for k, v in kw.items():
            self._in(b.inputs[k], v)
        return b


# ------------------------------------------------------------------------------------------------- masks
def blood_mask(nb, spots, H=1.8, specks=0.0, speck_zone=None):
    """spots: list of (centre xyz m, radius m, drip m).  -> float socket 0..1."""
    P = nb.rest()
    acc = None
    edge = nb.noise(P, 52.0, 4.0, 0.70)
    for (c, r, drip) in spots:
        D = nb.vmath("SUBTRACT", P, tuple(c))
        dx, dy, dz = nb.sep(D)
        below = nb.math("LESS_THAN", dz, 0.0)
        k = nb.mixf(below, 1.0, r / (r + drip) if drip > 0 else 1.0)
        dzs = nb.math("MULTIPLY", dz, k)
        # drips: thin vertical runs below the splat
        dist = nb.vmath("LENGTH", nb.comb(dx, dy, dzs))
        dist = nb.math("MULTIPLY_ADD", nb.math("SUBTRACT", edge, 0.5), r * 1.5, dist)
        m = nb.ss(dist, r, r * 0.55)
        if drip > 0:
            stripes = nb.noise(nb.comb(nb.math("MULTIPLY", dx, 1.0), nb.math("MULTIPLY", dy, 1.0), 0.0), 60.0 / max(r, 0.02) * 0.02, 1.0, 0.5)
            st = nb.ss(stripes, 0.56, 0.66)
            m = nb.math("MULTIPLY", m, nb.mixf(below, 1.0, nb.math("MAXIMUM", st, nb.ss(dist, r * 0.7, r * 0.3))))
        acc = m if acc is None else nb.math("MAXIMUM", acc, m)
    if specks > 0:
        d, _ = nb.voronoi(P, 140.0)
        sp = nb.ss(d, 0.16, 0.10)
        zone = nb.ss(nb.noise(P, 4.0, 2.0), 0.48, 0.62)
        sp = nb.math("MULTIPLY", nb.math("MULTIPLY", sp, zone), specks)
        acc = sp if acc is None else nb.math("MAXIMUM", acc, sp)
    return acc


def dirt_mask(nb, H, low=0.16, knee=None, amount=1.0, mottle=0.0, mottle_scale=9.0):
    P = nb.rest()
    x, y, z = nb.sep(P)
    n1 = nb.noise(P, 7.0, 4.0, 0.6)
    h = nb.ss(z, low * H, 0.0)                                   # 1 at the soles -> 0 at low*H
    if knee:
        kz = nb.math("ABSOLUTE", nb.math("SUBTRACT", z, knee * H))
        front = nb.ss(y, 0.0, -0.08 * H)                         # knees: the front of the leg
        h = nb.math("MAXIMUM", h, nb.math("MULTIPLY", nb.ss(kz, 0.06 * H, 0.0), nb.math("MULTIPLY", front, 0.8)))
    m = nb.math("MULTIPLY", h, nb.ss(n1, 0.30, 0.62))
    if mottle > 0:
        n2 = nb.noise(P, mottle_scale, 6.0, 0.62)
        mt = nb.math("MULTIPLY", nb.ss(n2, 0.52, 0.66), mottle)
        m = nb.math("MAXIMUM", m, mt)
    return nb.math("MULTIPLY", m, amount, clamp=True)


def droplets(nb, scale=150.0):
    """rain beads: (mask, height)."""
    P = nb.rest()
    d, c = nb.voronoi(P, scale)
    sz = nb.math("MULTIPLY_ADD", nb.sep(c)[0], 0.22, 0.16)       # bead radius in cell units, varied
    m = nb.math("LESS_THAN", d, sz)
    hgt = nb.math("MULTIPLY", m, nb.math("SUBTRACT", 1.0, nb.math("DIVIDE", d, sz), clamp=True))
    keep = nb.ss(nb.noise(P, 3.0, 1.0), 0.40, 0.55)               # patches: not a uniform grid of beads
    return nb.math("MULTIPLY", m, keep), nb.math("MULTIPLY", hgt, keep)


# ------------------------------------------------------------------------------------------------- materials
def _mat(name):
    m = bpy.data.materials.get(name)
    if m is not None:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name)
    return m


def cloth(name, base, rough=0.62, H=1.8, weave=0.0045, weave_k=0.25, sheen=0.25, dirt=None, dirt_col=(0.055, 0.035, 0.018),
          blood=None, wet=0.0, tears=None, tear_skin=(0.30, 0.31, 0.25), stripe=None, panel_v=None, tee=None, drops=150.0):
    """fabric: base linear RGB; dirt = dict(low, knee, amount, mottle); blood = dict(spots, specks); tears = spots list."""
    m = _mat(name); nb = NB(m)
    P = nb.rest()
    col = base
    # weave: two crossed fine waves + fibre noise
    wx = nb.node("ShaderNodeTexWave", wave_type="BANDS", bands_direction="X"); nb.link(P, wx.inputs["Vector"]); wx.inputs["Scale"].default_value = 1.0 / weave / 6.28 * 6.28 / 10
    wx.inputs["Scale"].default_value = 1.0 / weave * 0.1
    wz = nb.node("ShaderNodeTexWave", wave_type="BANDS", bands_direction="Z"); nb.link(P, wz.inputs["Vector"]); wz.inputs["Scale"].default_value = 1.0 / weave * 0.1
    wv = nb.math("MULTIPLY", wx.outputs["Fac"], wz.outputs["Fac"])
    fib = nb.noise(P, 260.0, 2.0, 0.5)
    hgt = nb.math("MULTIPLY_ADD", fib, 0.4, wv)
    # colour variation
    cv = nb.noise(P, 3.5, 3.0, 0.55)
    col = nb.mix(nb.math("MULTIPLY", nb.math("SUBTRACT", cv, 0.5), 0.5, clamp=False), col, tuple(c * 0.80 for c in base), "MIX")
    if tee is not None:                                          # the dark inner tee in the open neck (a V at the top front)
        x, y, z = nb.sep(P)
        zt, half, depth = tee["z_top"], tee["half"], tee["depth"]
        vmask = nb.math("LESS_THAN", nb.math("ABSOLUTE", x), nb.math("MULTIPLY", nb.math("SUBTRACT", z, zt - depth, clamp=False), half / depth))
        front = nb.math("LESS_THAN", y, -tee["y_front"])
        vm = nb.math("MULTIPLY", vmask, front)
        col = nb.mix(vm, col, tee["col"])
    if panel_v is not None:                                      # zip / placket line down the front
        x, y, z = nb.sep(P)
        ln = nb.math("MULTIPLY", nb.ss(nb.math("ABSOLUTE", nb.math("SUBTRACT", x, panel_v.get("x", 0.0))), 0.006, 0.002), nb.math("LESS_THAN", y, -panel_v["y_front"]))
        ln = nb.math("MULTIPLY", ln, nb.math("LESS_THAN", z, panel_v.get("z_top", 9.0)))
        col = nb.mix(nb.math("MULTIPLY", ln, 0.85), col, panel_v.get("col", (0.03, 0.02, 0.015)))
    rough_s = rough
    if dirt:
        dm = dirt_mask(nb, H, **dirt)
        col = nb.mix(nb.math("MULTIPLY", dm, 0.85), col, nb.mix(0.5, col, dirt_col, "MULTIPLY"))
        col = nb.mix(nb.math("MULTIPLY", dm, 0.35), col, dirt_col)
        rough_s = nb.math("MULTIPLY_ADD", dm, 0.15, rough)
    if tears:
        tm = blood_mask(nb, tears, H)
        rim = nb.math("SUBTRACT", blood_mask(nb, [(c, r * 1.35, 0) for c, r, d in tears], H), tm, clamp=True)
        col = nb.mix(tm, col, tuple(c * 0.45 for c in tear_skin))
        col = nb.mix(nb.math("MULTIPLY", rim, 0.85), col, (0.07, 0.008, 0.006))
        hgt = nb.math("SUBTRACT", hgt, nb.math("MULTIPLY", tm, 3.0))
    bm = None
    if blood:
        bm = blood_mask(nb, blood["spots"], H, blood.get("specks", 0.0))
        bcol = nb.mix(nb.noise(P, 30.0, 2.0), (0.16, 0.006, 0.008), (0.08, 0.004, 0.005))
        col = nb.mix(bm, col, bcol)
        rough_s = nb.mixf(bm, rough_s, 0.32)
    if stripe:
        pass
    # wetness
    coat_w = 0.0; coat_n = None
    nrm = nb.bump(hgt, weave_k, 0.0015)
    if wet > 0:
        col = nb.mix(wet * 0.55, col, nb.mix(1.0, col, (0.62, 0.62, 0.62), "MULTIPLY"))   # wet cloth is darker
        dark = max(base) < 0.05
        rough_s = nb.mixf(wet * (0.30 if dark else 0.55), rough_s, 0.34 if dark else 0.28)
        dm_, dh = droplets(nb, drops)
        coat_w = nb.math("MULTIPLY_ADD", dm_, (0.6 if dark else 1.0) * wet, (0.10 if dark else 0.30) * wet)
        coat_n = nb.bump(dh, 0.9, 0.003)
        nrm = nb.bump(dh, 0.5, 0.003, normal=nrm)
    b = nb.principled(**{"Base Color": col, "Roughness": rough_s, "Sheen Weight": sheen, "Sheen Roughness": 0.5, "Normal": nrm,
                         "Specular IOR Level": 0.25 if max(base) < 0.05 else 0.45})
    if wet > 0:
        nb._in(b.inputs["Coat Weight"], coat_w); b.inputs["Coat Roughness"].default_value = 0.06
        nb._in(b.inputs["Coat Normal"], coat_n)
    nb.link(b.outputs[0], nb.out.inputs[0])
    return m


def solid(name, base, rough=0.5, metal=0.0, coat=0.0, coat_rough=0.1, wet=0.0, H=1.8, dirt=None, dirt_col=(0.09, 0.06, 0.035), noise_bump=0.15,
          blood=None, drops=150.0, emission=None):
    """leather, plastic, webbing, metal, hair."""
    m = _mat(name); nb = NB(m)
    P = nb.rest()
    col = base
    cv = nb.noise(P, 6.0, 3.0, 0.55)
    col = nb.mix(nb.math("MULTIPLY", nb.math("SUBTRACT", cv, 0.5), 0.6), col, tuple(c * 0.7 for c in base))
    hgt = nb.noise(P, 180.0, 2.0, 0.5)
    rough_s = rough
    if dirt:
        dm = dirt_mask(nb, H, **dirt)
        col = nb.mix(dm, col, dirt_col)
        rough_s = nb.mixf(dm, rough, 0.85 if wet <= 0 else 0.45)
        hgt = nb.math("MULTIPLY_ADD", dm, nb.noise(P, 60.0, 3.0), hgt)
    if blood:
        bm = blood_mask(nb, blood["spots"], H, blood.get("specks", 0.0))
        col = nb.mix(bm, col, (0.13, 0.005, 0.007))
        rough_s = nb.mixf(bm, rough_s, 0.3)
    nrm = nb.bump(hgt, noise_bump, 0.002)
    coat_w = coat; coat_n = None
    if wet > 0:
        dark = max(base) < 0.05                                   # black stays black: a thinner wet film on black kit
        rough_s = nb.mixf(wet * (0.35 if dark else 0.6), rough_s, max(0.18 if dark else 0.12, rough * 0.4))
        dm_, dh = droplets(nb, drops)
        coat_w = nb.math("MULTIPLY_ADD", dm_, wet * (0.6 if dark else 1.0), max(coat, (0.18 if dark else 0.45) * wet))
        coat_n = nb.bump(dh, 0.9, 0.003)
    b = nb.principled(**{"Base Color": col, "Roughness": rough_s, "Metallic": metal, "Normal": nrm,
                         "Specular IOR Level": 0.25 if (max(base) < 0.05 and metal == 0) else 0.5})   # black kit: less sky in its sheen
    nb._in(b.inputs["Coat Weight"], coat_w); b.inputs["Coat Roughness"].default_value = coat_rough
    if coat_n is not None: nb._in(b.inputs["Coat Normal"], coat_n)
    if emission:
        nb._in(b.inputs["Emission Color"], emission[0]); b.inputs["Emission Strength"].default_value = emission[1]
    nb.link(b.outputs[0], nb.out.inputs[0])
    return m


def skin(name, base, H=1.8, sss=0.12, wet=0.0, blood=None, grime=0.0, face=None, eyes_glow=0.0, drops=170.0):
    """plastic toy skin: slight subsurface, a thin coat, fine noise; face = dict(w, h, img, emit) maps the decal
    onto the head's front face (object coordinates, origin at the head centre, front = -Y)."""
    m = _mat(name); nb = NB(m)
    P = nb.rest()
    cv = nb.noise(P, 9.0, 3.0, 0.5)
    col = nb.mix(nb.math("MULTIPLY", nb.math("SUBTRACT", cv, 0.5), 0.35), base, tuple(c * 0.86 for c in base))
    if grime > 0:
        g = nb.ss(nb.noise(P, 14.0, 5.0, 0.62), 0.5, 0.7)
        col = nb.mix(nb.math("MULTIPLY", g, grime), col, nb.mix(1.0, col, (0.55, 0.52, 0.42), "MULTIPLY"))
    if blood:
        bm = blood_mask(nb, blood["spots"], H, blood.get("specks", 0.0))
        col = nb.mix(bm, col, (0.15, 0.006, 0.008))
    hgt = nb.noise(P, 420.0, 2.0, 0.5)
    rough = 0.42
    img_emit = None
    if face is not None:
        tc = nb.node("ShaderNodeTexCoord")
        x, y, z = nb.sep(tc.outputs["Object"])
        u = nb.math("MULTIPLY_ADD", x, 1.0 / face["w"], 0.5)
        v = nb.math("MULTIPLY_ADD", nb.math("SUBTRACT", z, face.get("zc", 0.0)), 1.0 / face["h"], 0.5)
        uv = nb.comb(u, v, 0.0)
        im = nb.node("ShaderNodeTexImage", extension="CLIP", interpolation="Cubic"); im.name = "face_col"
        im.image = bpy.data.images.load(face["img"], check_existing=True)
        nb.link(uv, im.inputs["Vector"])
        nx, ny, nz = nb.sep(tc.outputs["Normal"])
        front = nb.ss(ny, -0.55, -0.80)
        a = nb.math("MULTIPLY", im.outputs["Alpha"], front)
        col = nb.mix(a, col, im.outputs["Color"])
        rough = nb.mixf(a, 0.42, 0.30)
        hgt = nb.math("MULTIPLY_ADD", a, -0.6, hgt)
        if face.get("emit"):
            ie = nb.node("ShaderNodeTexImage", extension="CLIP"); ie.name = "face_emit"
            ie.image = bpy.data.images.load(face["emit"], check_existing=True)
            ie.image.colorspace_settings.name = "Non-Color"
            nb.link(uv, ie.inputs["Vector"])
            img_emit = nb.math("MULTIPLY", ie.outputs["Color"], front)
    nrm = nb.bump(hgt, 0.05, 0.001)
    coat = 0.25; coat_n = None
    if wet > 0:
        dm_, dh = droplets(nb, drops)
        coat = nb.math("MULTIPLY_ADD", dm_, wet, 0.35 * wet + 0.2)
        coat_n = nb.bump(dh, 0.8, 0.002)
    b = nb.principled(**{"Base Color": col, "Roughness": rough, "Subsurface Weight": sss, "Subsurface Radius": (1.0, 0.45, 0.25),
                         "Subsurface Scale": 0.012, "Normal": nrm, "Specular IOR Level": 0.5})
    nb._in(b.inputs["Coat Weight"], coat); b.inputs["Coat Roughness"].default_value = 0.22
    if coat_n is not None: nb._in(b.inputs["Coat Normal"], coat_n)
    if img_emit is not None and eyes_glow > 0:
        b.inputs["Emission Color"].default_value = (0.92, 0.97, 1.0, 1.0)
        es = nb.node("ShaderNodeValue"); es.name = "eye_glow"; es.outputs[0].default_value = eyes_glow
        nb._in(b.inputs["Emission Strength"], nb.math("MULTIPLY", img_emit, es.outputs[0]))
    nb.link(b.outputs[0], nb.out.inputs[0])
    return m


def set_face(mat, col_path, emit_path=None, glow=None):
    nt = mat.node_tree
    n = nt.nodes.get("face_col")
    if n is not None and (n.image is None or n.image.filepath != col_path):
        n.image = bpy.data.images.load(col_path, check_existing=True)
    e = nt.nodes.get("face_emit")
    if e is not None and emit_path and (e.image is None or e.image.filepath != emit_path):
        e.image = bpy.data.images.load(emit_path, check_existing=True); e.image.colorspace_settings.name = "Non-Color"
    if glow is not None and nt.nodes.get("eye_glow"):
        nt.nodes["eye_glow"].outputs[0].default_value = glow


def tape(name, wet=0.0, gain=1.7, silver=(0.36, 0.37, 0.38), yellow=(0.86, 0.60, 0.010), edge=0.26):
    """retro-reflective band: yellow edges, silver centre (attribute 'tapev' = 0..1 across the band)."""
    m = _mat(name); nb = NB(m)
    v = nb.attr("tapev")
    e = nb.math("MAXIMUM", nb.ss(v, edge, edge - 0.03), nb.ss(v, 1 - edge, 1 - edge + 0.03))
    col = nb.mix(e, silver, yellow)
    P = nb.rest()
    grime = nb.ss(nb.noise(P, 10.0, 4.0, 0.6), 0.55, 0.72)
    col = nb.mix(nb.math("MULTIPLY", grime, 0.6), col, nb.mix(1.0, col, (0.35, 0.3, 0.25), "MULTIPLY"))
    # micro-prism texture: a fine cell bump on the silver
    d, _ = nb.voronoi(P, 900.0)
    base = nb.principled(**{"Base Color": col, "Roughness": 0.45, "Normal": nb.bump(d, 0.06, 0.0005)})
    geo = nb.node("ShaderNodeNewGeometry")
    rr = nb.node("ShaderNodeBsdfGlossy", distribution="GGX")
    rr.inputs["Roughness"].default_value = 0.26
    nb.link(geo.outputs["Incoming"], rr.inputs["Normal"])
    rcol = nb.mix(e, tuple(c * gain * 1.15 for c in silver), tuple(c * gain for c in yellow))
    rcol = nb.mix(nb.math("MULTIPLY", grime, 0.6), rcol, nb.mix(1.0, rcol, (0.35, 0.3, 0.25), "MULTIPLY"))
    nb._in(rr.inputs["Color"], rcol)
    add = nb.node("ShaderNodeAddShader")
    nb.link(base.outputs[0], add.inputs[0]); nb.link(rr.outputs[0], add.inputs[1])
    if wet > 0:
        base.inputs["Coat Weight"].default_value = 0.5 * wet; base.inputs["Coat Roughness"].default_value = 0.05
    nb.link(add.outputs[0], nb.out.inputs[0])
    return m


def image_mat(name, path, rough=0.4, wet=0.0, emission=0.0, uv=True):
    """a printed surface (patch, ID card) read through the mesh UVs."""
    m = _mat(name); nb = NB(m)
    im = nb.node("ShaderNodeTexImage", extension="CLIP"); im.image = bpy.data.images.load(path, check_existing=True)
    if uv:
        u = nb.node("ShaderNodeUVMap"); u.uv_map = "UVMap"; nb.link(u.outputs[0], im.inputs["Vector"])
    b = nb.principled(**{"Base Color": im.outputs["Color"], "Roughness": rough})
    if wet > 0:
        b.inputs["Coat Weight"].default_value = 0.6 * wet; b.inputs["Coat Roughness"].default_value = 0.05
    if emission > 0:
        nb._in(b.inputs["Emission Color"], im.outputs["Color"]); b.inputs["Emission Strength"].default_value = emission
    nb.link(b.outputs[0], nb.out.inputs[0])
    return m


def emit(name, col, strength):
    m = _mat(name); nb = NB(m)
    e = nb.node("ShaderNodeEmission"); e.inputs["Color"].default_value = tuple(col) + (1.0,); e.inputs["Strength"].default_value = strength
    nb.link(e.outputs[0], nb.out.inputs[0])
    return m
