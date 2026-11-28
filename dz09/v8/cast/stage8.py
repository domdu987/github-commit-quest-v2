"""stage8.py -- bpy side of the v8 cast: drawn layers on parallel cards, lit by the scene through pseudo-normal maps.

    import stage8 as S
    a = S.Actor8("kong", spec="kong", height=2.86)        # height in BU (1 BU = 0.6 m): the soles-to-hair-top size
    a.place((x, y, 0), facing_deg)                         # 0 faces -Y (v6 convention), +90 faces +X
    a.pose(dict(expr="determined", arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3)), camera=cam)
    a.set_shadow_light(light_obj)                          # the light whose shadow the proxy casts (others: no proxy shadow)
    a.head_world(), a.foot_world("L"), a.objects, a.root

Card shader (node group DZ8_card, shared): base = the drawn colour (sRGB) ->
    lit = mix(Diffuse(base, N), Toon(base, N, size 0.5, smooth 0.10), TOON)       (real scene lights + shadows)
    + Emission(base * AMB_TINT * AMB)                                             (flat-colour floor, lavender)
    + wet: Glossy(0.22) * 0.06                                                    (kong_wet / crew_wet)
    alpha-cut with Transparent.  N comes from the layer's pseudo-normal map (tangent space, inflated silhouette).
    Everything is multiplied by the base colour, so black ink and hair stay black.
Cards: visible to camera, diffuse and glossy (wet-road reflections), not to shadow rays.  A hidden proxy card with
the flat silhouette casts the actor's cast shadow; it is moved downstream of the shadow light so it never shades the
actor's own cards, and shadow linking stops it blocking other lights.  A soft contact/AO decal sits under the feet.
"""
import os, sys, math, hashlib
import numpy as np
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import draw8, raster8

PPD = 200
GAP = 0.05             # layer spacing in D
COLL = "CAST8"
VIEW_EDGES = (20.0, 52.0)  # camera-relative yaw (deg) where the front / q / side drawings swap
PROXY_TILT = 24.0       # deg the shadow proxy leans away from its light about the sole line
MODE = "flat"           # default staging mode: "flat" (reference E: camera-facing undistorted paper puppets) or "round" (v8 pass 1)
# flat look (see spec/refE_chars.md): colour = base * (AMB * TINT  +  DIR * scene light on the flat card  +  BACK * light from behind)
FLAT = dict(AMB=0.23, TINT=(0.30, 0.45, 1.0), DIR=0.20, BACK=0.10, NSTR=0.0, INK_LUM=0.014, INK_MIN=0.25,
            GLOW=0.20, GLOW_COL=(0.70, 0.82, 1.0), GLOW_R=0.16, PITCH=1.0, PITCH_MAX=40.0, GAP=0.03, SELF_R=0.45, EXPO=1.0)
FLAT_DEFAULT = dict(FLAT)
TUNE = dict(AMB=0.32, AMB_TINT=(0.80, 0.80, 0.98), TOON=0.35, NSTR=1.0, WET=0.035, INK_LUM=0.035, INK_MIN=0.35)


def _coll():
    c = bpy.data.collections.get(COLL)
    if c is None:
        c = bpy.data.collections.new(COLL)
        bpy.context.scene.collection.children.link(c)
    return c


def _img(path, noncolor=False):
    nm = os.path.basename(path)
    im = bpy.data.images.get(nm)
    if im is None:
        im = bpy.data.images.load(path)
        im.name = nm
        if noncolor:
            im.colorspace_settings.name = "Non-Color"
        im.alpha_mode = "STRAIGHT"
    return im


def card_group():
    g = bpy.data.node_groups.get("DZ8_card")
    if g:
        return g
    g = bpy.data.node_groups.new("DZ8_card", "ShaderNodeTree")
    I = g.interface
    I.new_socket("Color", in_out="INPUT", socket_type="NodeSocketColor")
    I.new_socket("Alpha", in_out="INPUT", socket_type="NodeSocketFloat")
    I.new_socket("NormalTex", in_out="INPUT", socket_type="NodeSocketColor")
    I.new_socket("Wet", in_out="INPUT", socket_type="NodeSocketFloat")
    I.new_socket("Shader", in_out="OUTPUT", socket_type="NodeSocketShader")
    N, L = g.nodes, g.links.new
    gi = N.new("NodeGroupInput")
    go = N.new("NodeGroupOutput")
    nm = N.new("ShaderNodeNormalMap"); nm.space = "TANGENT"; nm.uv_map = "UVMap"; nm.name = "nmap"
    nm.inputs["Strength"].default_value = TUNE["NSTR"]
    L(gi.outputs["NormalTex"], nm.inputs["Color"])
    # review fix: ink stays ink.  Under the strong warm practicals (S06 key) black hair/brows (#1d1d1d, 0.012 linear)
    # graded to brown 90,60,40.  The lit (not the ambient) colour of near-black paint is scaled down by
    # clamp(lum / INK_LUM, INK_MIN, 1): the hair/ink/vest blacks keep about a third of the light, every other colour is untouched.
    bw = N.new("ShaderNodeRGBToBW"); L(gi.outputs["Color"], bw.inputs[0])
    dv = N.new("ShaderNodeMath"); dv.operation = "DIVIDE"; L(bw.outputs[0], dv.inputs[0]); dv.inputs[1].default_value = TUNE["INK_LUM"]
    dv.name = "ink_lum"
    cl = N.new("ShaderNodeClamp"); L(dv.outputs[0], cl.inputs[0]); cl.inputs["Min"].default_value = TUNE["INK_MIN"]; cl.inputs["Max"].default_value = 1.0
    cl.name = "ink_min"
    ik = N.new("ShaderNodeMix"); ik.data_type = "RGBA"; ik.blend_type = "MULTIPLY"; ik.inputs[0].default_value = 1.0
    L(gi.outputs["Color"], ik.inputs[6]); L(cl.outputs[0], ik.inputs[7])
    lit_col = ik.outputs[2]
    dif = N.new("ShaderNodeBsdfDiffuse")
    L(lit_col, dif.inputs["Color"]); L(nm.outputs[0], dif.inputs["Normal"])
    toon = N.new("ShaderNodeBsdfToon"); toon.component = "DIFFUSE"
    toon.inputs["Size"].default_value = 0.5; toon.inputs["Smooth"].default_value = 0.10
    L(lit_col, toon.inputs["Color"]); L(nm.outputs[0], toon.inputs["Normal"])
    mx = N.new("ShaderNodeMixShader"); mx.name = "toon_mix"; mx.inputs[0].default_value = TUNE["TOON"]
    L(dif.outputs[0], mx.inputs[1]); L(toon.outputs[0], mx.inputs[2])
    # ambient flat floor: emission = base * tint * AMB
    mul = N.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs[0].default_value = 1.0
    mul.name = "amb_tint"
    L(gi.outputs["Color"], mul.inputs[6]); mul.inputs[7].default_value = TUNE["AMB_TINT"] + (1.0,)
    em = N.new("ShaderNodeEmission"); em.name = "amb"; em.inputs["Strength"].default_value = TUNE["AMB"]
    L(mul.outputs[2], em.inputs["Color"])
    ad = N.new("ShaderNodeAddShader"); L(mx.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1])
    gl = N.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.32; L(nm.outputs[0], gl.inputs["Normal"])
    wm = N.new("ShaderNodeMath"); wm.operation = "MULTIPLY"; L(gi.outputs["Wet"], wm.inputs[0]); wm.inputs[1].default_value = TUNE["WET"]
    wm.name = "wet_k"
    cw = N.new("ShaderNodeCombineColor"); L(wm.outputs[0], cw.inputs[0]); L(wm.outputs[0], cw.inputs[1]); L(wm.outputs[0], cw.inputs[2])
    # review fix: the wet gloss was added untinted, so black hair and ink took tan/white highlights (S06 hair top
    # up to rgb 194,159,115: the moon disc reflected in the gloss).  The gloss is multiplied by the drawn colour,
    # so ink/hair (0.012 linear) keep about 1 % of it and white skin all of it.
    gt = N.new("ShaderNodeMix"); gt.data_type = "RGBA"; gt.blend_type = "MIX"; gt.inputs[0].default_value = 1.0
    gt.inputs[6].default_value = (0.3, 0.3, 0.3, 1.0); L(gi.outputs["Color"], gt.inputs[7])
    gm = N.new("ShaderNodeMix"); gm.data_type = "RGBA"; gm.blend_type = "MULTIPLY"; gm.inputs[0].default_value = 1.0
    L(gt.outputs[2], gm.inputs[6]); L(cw.outputs[0], gm.inputs[7])
    L(gm.outputs[2], gl.inputs["Color"])
    ad2 = N.new("ShaderNodeAddShader"); L(ad.outputs[0], ad2.inputs[0]); L(gl.outputs[0], ad2.inputs[1])
    tr = N.new("ShaderNodeBsdfTransparent")
    cut = N.new("ShaderNodeMixShader"); L(gi.outputs["Alpha"], cut.inputs[0]); L(tr.outputs[0], cut.inputs[1]); L(ad2.outputs[0], cut.inputs[2])
    L(cut.outputs[0], go.inputs["Shader"])
    return g


def flat_group():
    """DZ8_flat: the reference-E card.  No rounding (geometric card normal; NSTR 0), an even emissive fill tinted by the
    scene (AMB * TINT), plus the real scene lights on the flat card (DIR, front) and through it (BACK, translucent), so
    set shadows and light pools still cut across the drawing as flat shapes.  Ink stays black (everything is
    multiplied by the drawn colour and near-black paint keeps only INK_MIN of the direct light)."""
    g = bpy.data.node_groups.get("DZ8_flat")
    if g:
        return g
    g = bpy.data.node_groups.new("DZ8_flat", "ShaderNodeTree")
    I = g.interface
    I.new_socket("Color", in_out="INPUT", socket_type="NodeSocketColor")
    I.new_socket("Alpha", in_out="INPUT", socket_type="NodeSocketFloat")
    I.new_socket("NormalTex", in_out="INPUT", socket_type="NodeSocketColor")
    I.new_socket("Wet", in_out="INPUT", socket_type="NodeSocketFloat")
    I.new_socket("Shader", in_out="OUTPUT", socket_type="NodeSocketShader")
    N, L = g.nodes, g.links.new
    gi = N.new("NodeGroupInput"); go = N.new("NodeGroupOutput")
    nm = N.new("ShaderNodeNormalMap"); nm.space = "TANGENT"; nm.uv_map = "UVMap"; nm.name = "nmap"
    nm.inputs["Strength"].default_value = FLAT["NSTR"]
    L(gi.outputs["NormalTex"], nm.inputs["Color"])
    bw = N.new("ShaderNodeRGBToBW"); L(gi.outputs["Color"], bw.inputs[0])
    dv = N.new("ShaderNodeMath"); dv.operation = "DIVIDE"; dv.name = "ink_lum"; L(bw.outputs[0], dv.inputs[0]); dv.inputs[1].default_value = FLAT["INK_LUM"]
    cl = N.new("ShaderNodeClamp"); cl.name = "ink_min"; L(dv.outputs[0], cl.inputs[0]); cl.inputs["Min"].default_value = FLAT["INK_MIN"]; cl.inputs["Max"].default_value = 1.0
    ik = N.new("ShaderNodeMix"); ik.data_type = "RGBA"; ik.blend_type = "MULTIPLY"; ik.inputs[0].default_value = 1.0
    L(gi.outputs["Color"], ik.inputs[6]); L(cl.outputs[0], ik.inputs[7])
    def gain(name, v):
        m = N.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = "MULTIPLY"; m.inputs[0].default_value = 1.0; m.name = name
        L(ik.outputs[2], m.inputs[6]); m.inputs[7].default_value = (v, v, v, 1.0)
        return m
    gd = gain("dir_k", FLAT["DIR"]); gb = gain("back_k", FLAT["BACK"])
    dif = N.new("ShaderNodeBsdfDiffuse"); L(gd.outputs[2], dif.inputs["Color"]); L(nm.outputs[0], dif.inputs["Normal"])
    trl = N.new("ShaderNodeBsdfTranslucent"); L(gb.outputs[2], trl.inputs["Color"])
    a1 = N.new("ShaderNodeAddShader"); L(dif.outputs[0], a1.inputs[0]); L(trl.outputs[0], a1.inputs[1])
    mul = N.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs[0].default_value = 1.0; mul.name = "amb_tint"
    L(gi.outputs["Color"], mul.inputs[6]); mul.inputs[7].default_value = tuple(FLAT["TINT"]) + (1.0,)
    em = N.new("ShaderNodeEmission"); em.name = "amb"; em.inputs["Strength"].default_value = FLAT["AMB"] / max(FLAT["EXPO"], 1e-3)
    L(mul.outputs[2], em.inputs["Color"])
    a2 = N.new("ShaderNodeAddShader"); L(a1.outputs[0], a2.inputs[0]); L(em.outputs[0], a2.inputs[1])
    tr = N.new("ShaderNodeBsdfTransparent")
    cut = N.new("ShaderNodeMixShader"); L(gi.outputs["Alpha"], cut.inputs[0]); L(tr.outputs[0], cut.inputs[1]); L(a2.outputs[0], cut.inputs[2])
    L(cut.outputs[0], go.inputs["Shader"])
    return g


def tune_flat(**kw):
    """change the shared flat look: AMB, TINT (scene-light tint of the even fill), DIR / BACK (share of real scene
    light from the front / from behind), NSTR (0 = no rounding), INK_MIN, GLOW, GLOW_COL, GLOW_R (D), PITCH, PITCH_MAX,
    SELF_R.  Call per shot to match the scene (e.g. warm TINT inside a lamp pool)."""
    FLAT.update(kw)
    n = flat_group().nodes
    n["amb"].inputs["Strength"].default_value = FLAT["AMB"] / max(FLAT["EXPO"], 1e-3)
    n["amb_tint"].inputs[7].default_value = tuple(FLAT["TINT"]) + (1.0,)
    for k, nm_ in (("DIR", "dir_k"), ("BACK", "back_k")):
        n[nm_].inputs[7].default_value = (FLAT[k],) * 3 + (1.0,)
    n["nmap"].inputs["Strength"].default_value = FLAT["NSTR"]
    n["ink_min"].inputs["Min"].default_value = FLAT["INK_MIN"]
    n["ink_lum"].inputs[1].default_value = FLAT["INK_LUM"]
    for m in bpy.data.materials:
        if m.name.endswith("_glow_m") and m.node_tree and "glow" in m.node_tree.nodes and not m.get("own"):
            m.node_tree.nodes["glow"].inputs["Strength"].default_value = FLAT["GLOW"] / max(FLAT["EXPO"], 1e-3)


def set_mode(mode):
    """default staging mode of Actor8 instances created afterwards: "flat" (film default) or "round"."""
    global MODE
    assert mode in ("flat", "round")
    MODE = mode


def _glow_material(name, path):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); N, L = nt.nodes, nt.links.new
    out = N.new("ShaderNodeOutputMaterial")
    uv = N.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    tc = N.new("ShaderNodeTexImage"); tc.name = "col"; tc.image = _img(path); tc.extension = "CLIP"; L(uv.outputs[0], tc.inputs[0])
    col = N.new("ShaderNodeRGB"); col.name = "glow_col"; col.outputs[0].default_value = tuple(FLAT["GLOW_COL"]) + (1.0,)
    mx = N.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs[0].default_value = 1.0
    L(col.outputs[0], mx.inputs[6]); L(tc.outputs["Alpha"], mx.inputs[7])
    em = N.new("ShaderNodeEmission"); em.name = "glow"; em.inputs["Strength"].default_value = FLAT["GLOW"] / max(FLAT["EXPO"], 1e-3); L(mx.outputs[2], em.inputs["Color"])
    tr = N.new("ShaderNodeBsdfTransparent")
    ad = N.new("ShaderNodeAddShader"); L(tr.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1])
    L(ad.outputs[0], out.inputs[0])
    return m


def _glow_png(flat_path, ppd, pad_px):
    """soft halo of the whole silhouette (white, alpha = halo): a tight core hugging the outline + a wide falloff."""
    import cv2
    from PIL import Image
    key = hashlib.sha1(("glow|%s|%d|%d|%.3f" % (flat_path, ppd, pad_px, FLAT["GLOW_R"])).encode()).hexdigest()[:24]
    out = os.path.join(raster8.CACHE, key + "_g.png")
    if os.path.exists(out):
        return out
    al = np.asarray(Image.open(flat_path).convert("RGBA"))[..., 3].astype(np.float32) / 255.0
    al = np.pad(al, pad_px)
    r = max(1.0, FLAT["GLOW_R"] * ppd)
    wide = cv2.GaussianBlur(al, (0, 0), r)
    core = cv2.GaussianBlur(al, (0, 0), max(0.8, r * 0.28))
    h = np.clip(0.55 * np.clip(wide * 1.6, 0, 1) + 0.45 * np.clip(core * 1.5, 0, 1), 0, 1)
    im = np.zeros(al.shape + (4,), np.uint8); im[..., :3] = 255; im[..., 3] = (h * 255).round()
    Image.fromarray(im).save(out)
    return out


def tune(**kw):
    """change the shared card look: AMB (flat floor), TOON (terminator share), NSTR (normal strength), WET."""
    TUNE.update(kw)
    g = card_group()
    n = g.nodes
    n["amb"].inputs["Strength"].default_value = TUNE["AMB"]
    n["amb_tint"].inputs[7].default_value = tuple(TUNE["AMB_TINT"]) + (1.0,)
    n["toon_mix"].inputs[0].default_value = TUNE["TOON"]
    n["nmap"].inputs["Strength"].default_value = TUNE["NSTR"]
    n["wet_k"].inputs[1].default_value = TUNE["WET"]


def card_material(name, cpath, npath, wet, mode="round"):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links.new
    out = N.new("ShaderNodeOutputMaterial")
    uv = N.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    tc = N.new("ShaderNodeTexImage"); tc.name = "col"; tc.image = _img(cpath); tc.interpolation = "Linear"; tc.extension = "CLIP"
    tn = N.new("ShaderNodeTexImage"); tn.name = "nrm"; tn.image = _img(npath, True); tn.interpolation = "Linear"; tn.extension = "EXTEND"
    L(uv.outputs[0], tc.inputs[0]); L(uv.outputs[0], tn.inputs[0])
    gr = N.new("ShaderNodeGroup"); gr.node_tree = flat_group() if mode == "flat" else card_group()
    L(tc.outputs["Color"], gr.inputs["Color"]); L(tc.outputs["Alpha"], gr.inputs["Alpha"]); L(tn.outputs["Color"], gr.inputs["NormalTex"])
    gr.inputs["Wet"].default_value = 1.0 if wet else 0.0
    L(gr.outputs[0], out.inputs[0])
    m.blend_method = "HASHED" if hasattr(m, "blend_method") else None
    return m


def _quad(name, coll):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)], [], [(0, 1, 2, 3)])
    me.uv_layers.new(name="UVMap")
    uvl = me.uv_layers["UVMap"].data
    for i, uv in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uvl[i].uv = uv
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def _set_quad(ob, box, sc, y):
    """box (x0, y0, x1, y1) in figure D (y down) -> quad in the pivot's local XZ plane at depth y."""
    x0, y0, x1, y1 = box
    me = ob.data
    v = [(x0 * sc, y, -y1 * sc), (x1 * sc, y, -y1 * sc), (x1 * sc, y, -y0 * sc), (x0 * sc, y, -y0 * sc)]
    for i, p in enumerate(v):
        me.vertices[i].co = p
    me.update()


def _contact_material():
    m = bpy.data.materials.get("dz8_contact")
    if m:
        return m
    m = bpy.data.materials.new("dz8_contact")
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); N, L = nt.nodes, nt.links.new
    out = N.new("ShaderNodeOutputMaterial")
    tc = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ"); L(tc.outputs["Generated"], sep.inputs[0])
    # radial falloff from the decal centre (generated coords 0..1)
    vm = N.new("ShaderNodeVectorMath"); vm.operation = "SUBTRACT"; L(tc.outputs["Generated"], vm.inputs[0]); vm.inputs[1].default_value = (0.5, 0.5, 0.5)
    mul = N.new("ShaderNodeVectorMath"); mul.operation = "MULTIPLY"; L(vm.outputs[0], mul.inputs[0]); mul.inputs[1].default_value = (2, 2, 0)
    lnn = N.new("ShaderNodeVectorMath"); lnn.operation = "LENGTH"; L(mul.outputs[0], lnn.inputs[0])
    rp = N.new("ShaderNodeValToRGB"); L(lnn.outputs["Value"], rp.inputs[0])
    e = rp.color_ramp.elements
    e[0].position = 0.0; e[0].color = (0.85, 0.85, 0.85, 1); e[1].position = 1.0; e[1].color = (0, 0, 0, 1)
    rp.color_ramp.interpolation = "EASE"
    tr = N.new("ShaderNodeBsdfTransparent")
    df = N.new("ShaderNodeBsdfDiffuse"); df.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1)
    mx = N.new("ShaderNodeMixShader"); L(rp.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(df.outputs[0], mx.inputs[2])
    L(mx.outputs[0], out.inputs[0])
    return m


def _proxy_material(name, cpath):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear(); N, L = nt.nodes, nt.links.new
    out = N.new("ShaderNodeOutputMaterial")
    tc = N.new("ShaderNodeTexImage"); tc.name = "col"; tc.image = _img(cpath); tc.extension = "CLIP"
    uv = N.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"; L(uv.outputs[0], tc.inputs[0])
    tr = N.new("ShaderNodeBsdfTransparent"); df = N.new("ShaderNodeBsdfDiffuse")
    # no self-shadow (flat mode): a shadow ray that STARTS above the ground inside the actor's own column (radius
    # self_r BU around the proxy origin) passes through.  origin = hit position + incoming * ray length.
    geo = N.new("ShaderNodeNewGeometry"); lp = N.new("ShaderNodeLightPath"); oi = N.new("ShaderNodeObjectInfo")
    sc_ = N.new("ShaderNodeVectorMath"); sc_.operation = "SCALE"; L(geo.outputs["Incoming"], sc_.inputs[0]); L(lp.outputs["Ray Length"], sc_.inputs["Scale"])
    org = N.new("ShaderNodeVectorMath"); org.operation = "ADD"; L(geo.outputs["Position"], org.inputs[0]); L(sc_.outputs[0], org.inputs[1])
    rel = N.new("ShaderNodeVectorMath"); rel.operation = "SUBTRACT"; L(org.outputs[0], rel.inputs[0]); L(oi.outputs["Location"], rel.inputs[1])
    sp = N.new("ShaderNodeSeparateXYZ"); L(rel.outputs[0], sp.inputs[0])
    flat_ = N.new("ShaderNodeCombineXYZ"); L(sp.outputs["X"], flat_.inputs["X"]); L(sp.outputs["Y"], flat_.inputs["Y"])
    hl = N.new("ShaderNodeVectorMath"); hl.operation = "LENGTH"; L(flat_.outputs[0], hl.inputs[0])
    near = N.new("ShaderNodeMath"); near.operation = "LESS_THAN"; near.name = "self_r"; L(hl.outputs["Value"], near.inputs[0]); near.inputs[1].default_value = 0.0
    up = N.new("ShaderNodeMath"); up.operation = "GREATER_THAN"; up.name = "self_z"; L(sp.outputs["Z"], up.inputs[0]); up.inputs[1].default_value = 0.05
    both = N.new("ShaderNodeMath"); both.operation = "MULTIPLY"; L(near.outputs[0], both.inputs[0]); L(up.outputs[0], both.inputs[1])
    keep = N.new("ShaderNodeMath"); keep.operation = "SUBTRACT"; keep.inputs[0].default_value = 1.0; L(both.outputs[0], keep.inputs[1])
    al = N.new("ShaderNodeMath"); al.operation = "MULTIPLY"; L(tc.outputs["Alpha"], al.inputs[0]); L(keep.outputs[0], al.inputs[1])
    mx = N.new("ShaderNodeMixShader"); L(al.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(df.outputs[0], mx.inputs[2])
    L(mx.outputs[0], out.inputs[0])
    return m


def view_for(rel_deg):
    a = abs(rel_deg)
    if a < VIEW_EDGES[0]:
        return "front"
    if a < VIEW_EDGES[1]:
        return "q"
    if a < 128.0:
        return "side"
    return "back"


class Actor8:
    def __init__(self, name, spec="kong", height=2.86, ppd=PPD, gap=None, follow=1.0, pass_index=2, contact=True, mode=None):
        self.name = name
        self.mode = mode or MODE
        if gap is None:
            gap = FLAT["GAP"] if self.mode == "flat" else GAP
        self.pitch_anchor = 0.0                    # flat mode: height fraction the pitch turns about (0 = the soles: feet stay planted; ~0.6 for a seated actor)
        self.pitch_override = None                 # degrees, or None = follow the camera
        self.glow = None
        self.glow_color = None                     # None = FLAT["GLOW_COL"]; set per actor/shot with set_glow()
        self.glow_strength = None
        self.height = height
        self.spec = draw8.get_spec(spec)
        tot = self.spec["legs"] + self.spec["torso"] + 1.0 + self.spec["hair"]["top"]
        self.sc = height / tot                      # BU per D
        self.ppd, self.gap, self.follow = ppd, gap, follow
        self.coll = _coll()
        self.root = bpy.data.objects.new(name + "_root", None)
        self.coll.objects.link(self.root)
        self.pivot = bpy.data.objects.new(name + "_pivot", None)
        self.coll.objects.link(self.pivot)
        self.pivot.parent = self.root
        self.cards = {}
        self.fig = None
        self.facing = 0.0
        self.pass_index = pass_index
        self.proxy = _quad(name + "_proxy", self.coll)
        self.proxy.parent = self.root
        for a in ("visible_camera", "visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter"):
            setattr(self.proxy, a, False)
        self.proxy.visible_shadow = True
        self.contact = None
        if contact:
            bpy.ops.mesh.primitive_plane_add(size=1.0)
            c = bpy.context.active_object
            for cl in list(c.users_collection):
                cl.objects.unlink(c)
            self.coll.objects.link(c)
            c.name = name + "_contact"
            c.data.materials.append(_contact_material())
            c.parent = self.root
            c.location = (0, 0, 0.004)
            c.visible_shadow = False
            c.visible_glossy = False
            self.contact = c
        self.shadow_light = None
        self.walk_lock = None                      # walking: card plane locked to the motion direction
        self.view_override = None
        self.last_pose = {}

    # ----------------------------------------------------------------------------------------- placement
    def place(self, loc, facing_deg=0.0):
        self.root.location = loc
        self.facing = facing_deg
        self.root.rotation_euler = (0, 0, math.radians(facing_deg))

    @property
    def objects(self):
        return [c for c in self.cards.values()] + [self.proxy] + ([self.contact] if self.contact else []) + ([self.glow] if self.glow else [])

    def set_pass_index(self, i):
        self.pass_index = i
        for o in self.objects:
            o.pass_index = i

    def hide(self, h=True):
        for o in self.objects:
            o.hide_render = h

    def _cam_rel(self, camera):
        """camera direction relative to the actor's facing, in degrees (+ = camera on the actor's left side,
        i.e. the actor is seen facing screen-left... see s below)."""
        if camera is None:
            return 0.0
        bpy.context.view_layer.update()
        p = self.root.matrix_world.translation
        c = camera.matrix_world.translation
        d = Vector((c.x - p.x, c.y - p.y))
        if d.length < 1e-6:
            return 0.0
        ang_cam = math.degrees(math.atan2(d.x, -d.y))     # same convention as facing: 0 = toward -Y
        rel = (ang_cam - self.facing + 180) % 360 - 180
        return rel

    # ----------------------------------------------------------------------------------------- pose
    def pose(self, pose, camera=None, view=None):
        pose = dict(pose)
        rel = self._cam_rel(camera) if camera is not None else 0.0
        v = view or self.view_override or pose.get("view") or view_for(rel)
        # rel > 0: the camera sits toward the actor's facing-left -> the actor turns screen-right?  The actor faces
        # facing_deg; a camera at +rel (counter-clockwise) sees the actor's front turned to screen-LEFT... worked out:
        # camera at rel=+90 looks at the actor's left side: the actor faces screen-right.
        s = -1 if rel > 0.5 else 1
        if "s" in pose:
            s = pose["s"]
        pose["view"] = v
        pose["s"] = s
        self.last_pose = pose
        fig = draw8.build(self.spec, pose)
        self.fig = fig
        cv = draw8.canvas_for(self.spec)
        tag = self.name
        L = raster8.layer_pngs(fig, cv, self.ppd, os.path.join(HERE, "tmp", "layers"), tag)
        self.layers = L
        # pivot: cards turn toward the camera by `follow` (stills), or stay in the motion plane (walks)
        pitch = 0.0
        if self.walk_lock is not None:
            yaw_p = self.walk_lock
        else:
            yaw_p = rel * (1.0 if self.mode == "flat" else self.follow)
            # the drawing already shows the turn: face the camera, keep the cards' plane square to it
        if self.mode == "flat":
            # reference E: the drawing is never skewed.  The card is pitched until it is parallel to the sensor
            # (camera looking down -> the card leans back), about the sole line so the feet stay planted.
            if self.pitch_override is not None:
                pitch = self.pitch_override
            elif camera is not None:
                fz = (camera.matrix_world.to_3x3() @ Vector((0, 0, -1))).z
                pitch = math.degrees(math.asin(max(-1.0, min(1.0, -fz)))) * FLAT["PITCH"]
            pitch = max(-FLAT["PITCH_MAX"], min(FLAT["PITCH_MAX"], pitch))
        self.pitch = pitch
        self.pivot.rotation_euler = (-math.radians(pitch), 0, math.radians(yaw_p))
        if pitch and self.pitch_anchor:
            c = Vector((0, 0, self.pitch_anchor * self.height))
            self.pivot.location = c - (self.pivot.rotation_euler.to_matrix() @ c)
        else:
            self.pivot.location = (0, 0, 0)
        used = set()
        for nm, info in L.items():
            used.add(nm)
            ob = self.cards.get(nm)
            if ob is None:
                ob = _quad("%s_%s" % (self.name, nm), self.coll)
                ob.parent = self.pivot
                ob.visible_shadow = False
                ob.pass_index = self.pass_index
                self.cards[nm] = ob
            mname = "%s_%s_m" % (self.name, nm)
            m = bpy.data.materials.get(mname)
            if m is None:
                m = card_material(mname, info["color"], info["normal"], self.spec.get("wet", False), self.mode)
                ob.data.materials.clear(); ob.data.materials.append(m)
            else:
                m.node_tree.nodes["col"].image = _img(info["color"])
                m.node_tree.nodes["nrm"].image = _img(info["normal"], True)
            _set_quad(ob, info["box"], self.sc, -info["z"] * self.gap * self.sc)
            ob.hide_render = False
        for nm, ob in self.cards.items():
            if nm not in used:
                ob.hide_render = True
        # shadow proxy: the flat composite silhouette
        svg, W, H = draw8.doc(draw8.flat_svg(fig), cv, max(60, self.ppd // 3))
        fp = raster8.png(svg, W, H)
        pm = bpy.data.materials.get(self.name + "_proxy_m")
        if pm is None:
            pm = _proxy_material(self.name + "_proxy_m", fp)
            self.proxy.data.materials.append(pm)
        else:
            pm.node_tree.nodes["col"].image = _img(fp)
        _set_quad(self.proxy, cv, self.sc, 0.0)
        pm.node_tree.nodes["self_r"].inputs[1].default_value = FLAT["SELF_R"] * self.height if self.mode == "flat" else 0.0
        self._place_proxy()
        if self.mode == "flat":
            ppd_g = max(60, self.ppd // 3)
            pad = int(round(FLAT["GLOW_R"] * 2.6 * ppd_g))
            gp = _glow_png(fp, ppd_g, pad)
            if self.glow is None:
                self.glow = _quad(self.name + "_glow", self.coll)
                self.glow.parent = self.pivot
                for a in ("visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter", "visible_shadow"):
                    setattr(self.glow, a, False)
                self.glow.pass_index = self.pass_index
                gm = _glow_material(self.name + "_glow_m", gp)
                self.glow.data.materials.append(gm)
                self._apply_glow()
            else:
                self.glow.data.materials[0].node_tree.nodes["col"].image = _img(gp)
            pd = pad / ppd_g
            zmin = min(i["z"] for i in L.values()) if L else 0.0
            _set_quad(self.glow, (cv[0] - pd, cv[1] - pd, cv[2] + pd, cv[3] + pd), self.sc, -(zmin - 2.0) * self.gap * self.sc)
        if self.contact:
            fx = [fig["anchors"].get("foot_R"), fig["anchors"].get("foot_L")]
            fx = [p for p in fx if p]
            w = (max(p[0] for p in fx) - min(p[0] for p in fx) + 1.1) * self.sc if fx else 1.2 * self.sc
            self.contact.scale = (w * 1.05, 0.75 * self.sc, 1)
            self.contact.rotation_euler = (0, 0, math.radians(yaw_p))
        return fig

    def set_glow(self, color=None, strength=None):
        """flat mode: the soft halo/rim behind the figure.  color None = FLAT["GLOW_COL"], strength None = FLAT["GLOW"]
        (0 switches it off).  Use the colour of the light behind the actor (warm lamp, cool moon)."""
        self.glow_color, self.glow_strength = color, strength
        self._apply_glow()

    def _apply_glow(self):
        if self.glow is None:
            return
        m = self.glow.data.materials[0]; n = m.node_tree.nodes
        n["glow_col"].outputs[0].default_value = tuple(self.glow_color or FLAT["GLOW_COL"]) + (1.0,)
        n["glow"].inputs["Strength"].default_value = (FLAT["GLOW"] if self.glow_strength is None else self.glow_strength) / max(FLAT["EXPO"], 1e-3)
        m["own"] = self.glow_strength is not None

    def set_shadow_light(self, light):
        self.shadow_light = light
        self._place_proxy()

    def _place_proxy(self):
        """turn the proxy to face the shadow light (horizontally) and move it downstream of the light so the
        actor's own cards are never inside its shadow."""
        L = self.shadow_light
        try:
            if L is not None: L.name
        except ReferenceError:                       # the light was deleted (e.g. a rebuilt work lamp)
            L = self.shadow_light = None
        bpy.context.view_layer.update()
        p = self.root.matrix_world.translation
        if L is None:
            self.proxy.rotation_euler = (0, 0, self.pivot.rotation_euler[2])
            self.proxy.location = (0, 0, 0)
            return
        if L.data.type == "SUN":
            d = L.matrix_world.to_3x3() @ Vector((0, 0, -1))
        else:
            d = p + Vector((0, 0, 1.5 * self.sc)) - L.matrix_world.translation
        dh = Vector((d.x, d.y, 0))
        if dh.length < 1e-4:
            dh = Vector((0, 1e-3, 0))
        dh.normalize()
        # local (root) frame
        inv = self.root.matrix_world.to_3x3().inverted()
        dl = inv @ dh
        yaw = math.degrees(math.atan2(-dl.x, dl.y))        # quad normal is -Y local: face the light
        # review fix: the proxy used to be shifted 0.35 D downstream, so its shadow started 14 cm away from the soles
        # (a detached shadow).  Now its sole line stays ON the soles and the card leans away from the light about
        # that line: at the feet the shadow is attached, above the boots the proxy is behind the card stack
        # (0.25 D at 0.6 D height), so it still never shades the actor's own upper cards.
        self.proxy.rotation_euler = (-math.radians(PROXY_TILT), 0, math.radians(yaw))
        self.proxy.location = (0, 0, 0)

    # ----------------------------------------------------------------------------------------- queries
    def world_of(self, pt_D, layer_z=0.0):
        """figure point (x, y-down, D) on the card plane at depth layer_z -> world."""
        bpy.context.view_layer.update()
        loc = Vector((pt_D[0] * self.sc, -layer_z * self.gap * self.sc, -pt_D[1] * self.sc))
        return self.pivot.matrix_world @ loc

    def sole_world(self, layer):
        """measured on the drawn sprite: centre of the lowest 3 opaque pixel rows of a leg layer -> world."""
        from PIL import Image
        info = self.layers[layer]
        al = np.asarray(Image.open(info["color"]))[..., 3]
        ys, xs = np.nonzero(al > 128)
        ymax = ys.max()
        sel = ys >= ymax - 2
        px, py = xs[sel].mean(), ys[sel].mean()
        x0, y0, x1, y1 = info["box"]
        H, W = al.shape
        pt = (x0 + (px + 0.5) / W * (x1 - x0), y0 + (py + 0.5) / H * (y1 - y0))
        return self.world_of(pt, info["z"])

    def head_world(self):
        return self.world_of(self.fig["anchors"]["head"], 1.0)

    def foot_world(self, side):
        return self.world_of(self.fig["anchors"]["foot_" + side], -1.0)


def shadow_link(actors, key_light):
    """proxies cast shadows from key_light only: every other light gets a blocker collection that excludes them."""
    cname = "CAST8_proxies"
    c = bpy.data.collections.get(cname) or bpy.data.collections.new(cname)
    for a in actors:
        if a.proxy.name not in c.objects:
            c.objects.link(a.proxy)
    for ob in bpy.data.objects:
        if ob.type != "LIGHT" or ob == key_light:
            continue
        try:
            ob.light_linking.blocker_collection = c
            for co in c.collection_objects:
                co.light_linking.link_state = "EXCLUDE"
        except Exception as e:                       # older API
            print("shadow_link:", e)
    for a in actors:
        a.set_shadow_light(key_light)
