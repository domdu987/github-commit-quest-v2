"""Toon light model for PRACTICAL lights (point / spot / area), shared by room3d.py and the soi 'evening' preset (soi3d.py).

office3d.mat_lit makes every face that sees the ONE sun take the full key by dividing the diffuse colour by the cosine to the sun.
That trick only works for one fixed direction. Here the key is a Toon BSDF (diffuse, size ~1): Cycles evaluates it per light, so a
face turned toward a bulb, a tube or the moon gets that light's full (distance-attenuated) intensity whatever its angle; cast
shadows stay ray traced. Measured (bpy 5.3): Toon size 1 = 1/(2 pi), i.e. half of Lambert at normal incidence, so the colour is
art x gain x 2 and

    pixel = art x gain x K x visibility + (art x SHADE x shade_mul + LIFT) x F          (same as mat_lit, F = form / falloff term)
    K of a point or spot light of power W at distance d:  K = W / (4 pi^2 d^2)   ->  W = K d^2 4 pi^2
    K of an area light on its axis:                        K = W / (pi^2 d^2)      ->  W = K d^2 pi^2
    K of a sun of strength s:                              K = s / pi

Switching: every practical light and every emissive term (bulb glass, lit windows, signs) is registered here, so
set_lights(False) turns the whole set dark in one call (same camera, same frame), and set_lights(True) brings it back.
"""
import math
import bpy
from mathutils import Vector
import office3d as S

REG = dict(lights=[], emit=[], amb=[])           # filled by the set builders; cleared by reset()
STATE = dict(on=True)

def reset():
    for k in REG: REG[k].clear()
    STATE['on'] = True

def lin(h): return S.hex_lin(h)

# ----------------------------------------------------------------------------- materials
def mat_toon(name, P, color='#808080', image=None, gain=1.0, shade_mul=1.0, alpha=False, form=None, glow=None, glow_strength=0.0,
             glow_tint=(1.0, 1.0, 1.0), glow_off=0.0, size=0.92, smooth=0.08, falloff=None, interp='Linear', amb_off=None, lambert=0.0):
    """Ambient (emission, node 'AMB') + Toon key (node 'KEY'). glow: optional emission mask texture (path) x glow_strength
    (node 'GLOW', registered for set_lights: off value glow_off). amb_off: ambient multiplier while the lights are off (registered).
    falloff = (axis, origin, length, amount): ambient falls by `amount` over `length` along the axis (rooms: darker corners).
    lambert = 0..1: share of the key that keeps the cosine (Diffuse BSDF). 0 = pure toon (orientation-free); a room lit by one bulb
    reads better with ~0.6 (walls fall off with the angle to the bulb, the ceiling does not blow out). Same K at normal incidence."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = S._tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); geo = nt.nodes.new('ShaderNodeNewGeometry')
    key = nt.nodes.new('ShaderNodeBsdfToon'); key.name = 'KEY'; key.component = 'DIFFUSE'
    key.inputs['Size'].default_value = size; key.inputs['Smooth'].default_value = smooth
    emi = nt.nodes.new('ShaderNodeEmission'); emi.name = 'AMB'; emi.inputs['Strength'].default_value = 1.0
    ms = nt.nodes.new('ShaderNodeMix'); ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0
    sm = tuple(shade_mul) if isinstance(shade_mul, (tuple, list)) else (shade_mul,) * 3
    ms.inputs[7].default_value = (*[s * k for s, k in zip(P['shade'], sm)], 1.0)
    kc = nt.nodes.new('ShaderNodeVectorMath'); kc.operation = 'SCALE'; kc.inputs['Scale'].default_value = 2.0 * gain * (1.0 - lambert)
    tex = None
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = S._img(image); tex.interpolation = interp
        L(tex.outputs['Color'], ms.inputs[6]); L(tex.outputs['Color'], kc.inputs[0])
    else:
        col = (*lin(color), 1.0); ms.inputs[6].default_value = col; kc.inputs[0].default_value = col[:3]
    L(kc.outputs['Vector'], key.inputs['Color']); keyout = key.outputs['BSDF']
    if lambert > 0:
        lb = nt.nodes.new('ShaderNodeBsdfDiffuse'); lb.name = 'KEY_L'; lb.inputs['Roughness'].default_value = 0.0
        lc_ = nt.nodes.new('ShaderNodeVectorMath'); lc_.operation = 'SCALE'; lc_.inputs['Scale'].default_value = gain * lambert
        if tex is not None: L(tex.outputs['Color'], lc_.inputs[0])
        else: lc_.inputs[0].default_value = lin(color)
        L(lc_.outputs['Vector'], lb.inputs['Color']); ka = nt.nodes.new('ShaderNodeAddShader'); L(key.outputs['BSDF'], ka.inputs[0]); L(lb.outputs['BSDF'], ka.inputs[1]); keyout = ka.outputs['Shader']
    lf = nt.nodes.new('ShaderNodeVectorMath'); lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P.get('lift', (0, 0, 0))); L(ms.outputs[2], lf.inputs[0])
    fac = None
    if form and any(abs(x) > 1e-6 for x in form):
        fd = nt.nodes.new('ShaderNodeVectorMath'); fd.operation = 'DOT_PRODUCT'; fd.inputs[1].default_value = tuple(form); L(geo.outputs['True Normal'], fd.inputs[0])
        fa = nt.nodes.new('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fd.outputs['Value'], fa.inputs[0]); fac = fa.outputs[0]
    if falloff:
        ax, org, length, amount = falloff
        pd = nt.nodes.new('ShaderNodeVectorMath'); pd.operation = 'SUBTRACT'; pd.inputs[1].default_value = tuple(org); L(geo.outputs['Position'], pd.inputs[0])
        pl = nt.nodes.new('ShaderNodeVectorMath'); pl.operation = 'DOT_PRODUCT'; pl.inputs[1].default_value = tuple(Vector(ax).normalized() / length); L(pd.outputs['Vector'], pl.inputs[0])
        pc = nt.nodes.new('ShaderNodeMath'); pc.operation = 'MULTIPLY_ADD'; pc.use_clamp = True; pc.inputs[1].default_value = -amount; pc.inputs[2].default_value = 1.0
        L(pl.outputs['Value'], pc.inputs[0])
        if fac is not None:
            pm = nt.nodes.new('ShaderNodeMath'); pm.operation = 'MULTIPLY'; L(fac, pm.inputs[0]); L(pc.outputs[0], pm.inputs[1]); fac = pm.outputs[0]
        else: fac = pc.outputs[0]
    if fac is not None:
        fs = nt.nodes.new('ShaderNodeVectorMath'); fs.operation = 'SCALE'; L(lf.outputs['Vector'], fs.inputs[0]); L(fac, fs.inputs['Scale']); L(fs.outputs['Vector'], emi.inputs['Color'])
    else: L(lf.outputs['Vector'], emi.inputs['Color'])
    add = nt.nodes.new('ShaderNodeAddShader'); L(keyout, add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1]); last = add.outputs['Shader']
    if glow is not None:
        gt = nt.nodes.new('ShaderNodeTexImage'); gt.image = S._img(glow) if isinstance(glow, str) else glow
        ge = nt.nodes.new('ShaderNodeEmission'); ge.name = 'GLOW'; ge.inputs['Strength'].default_value = glow_strength
        if tuple(glow_tint) != (1.0, 1.0, 1.0):
            gm = nt.nodes.new('ShaderNodeVectorMath'); gm.operation = 'MULTIPLY'; gm.inputs[1].default_value = tuple(glow_tint); L(gt.outputs['Color'], gm.inputs[0]); L(gm.outputs[0], ge.inputs['Color'])
        else: L(gt.outputs['Color'], ge.inputs['Color'])
        ga = nt.nodes.new('ShaderNodeAddShader'); L(last, ga.inputs[0]); L(ge.outputs[0], ga.inputs[1]); last = ga.outputs['Shader']
        REG['emit'].append((ge.inputs['Strength'], glow_strength, glow_off))
    if amb_off is not None: REG['amb'].append((emi.inputs['Strength'], 1.0, amb_off))
    if alpha and tex is not None:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(tex.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def mat_glow(name, color='#ffffff', strength=1.0, image=None, off=0.0, off_color=None, alpha=False):
    """Practical emitter surface (bulb glass, tube, neon, lit sign face, backdrop window). Registered: off -> strength `off`
    (and colour `off_color` if given, e.g. a dead tube reads grey). Never sampled as a light (the real lights do the lighting)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = S._tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission'); emi.name = 'GLOW'; emi.inputs['Strength'].default_value = strength
    tex = None
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = S._img(image); L(tex.outputs['Color'], emi.inputs['Color'])
    else: emi.inputs['Color'].default_value = (*lin(color), 1.0)
    last = emi.outputs['Emission']
    if alpha and tex is not None:
        tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
        L(tex.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    REG['emit'].append((emi.inputs['Strength'], strength, off))
    if off_color is not None and tex is None: REG['emit'].append((emi.inputs['Color'], (*lin(color), 1.0), (*lin(off_color), 1.0)))
    return m

def mat_additive(name, color, strength, image=None, off=0.0):
    """Transparent + emission seen by the camera only (light haze, glare cards). Registered for set_lights."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = S._tree(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); em = nt.nodes.new('ShaderNodeEmission'); em.name = 'GLOW'
    em.inputs['Color'].default_value = (*lin(color), 1); lp = nt.nodes.new('ShaderNodeLightPath'); mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
    L(lp.outputs['Is Camera Ray'], mul.inputs[0]); mul.inputs[1].default_value = strength
    if image:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = S._img(image); m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'
        L(tex.outputs['Alpha'], m2.inputs[0]); L(mul.outputs[0], m2.inputs[1]); L(m2.outputs[0], em.inputs['Strength'])
    else: L(mul.outputs[0], em.inputs['Strength'])
    ad = nt.nodes.new('ShaderNodeAddShader'); L(tr.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1]); L(ad.outputs[0], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    REG['emit'].append((mul.inputs[1], strength, off))
    return m

# ----------------------------------------------------------------------------- lights
def _light(coll, name, kind, loc, color, power, radius=0.02, direction=None, practical=True):
    ld = bpy.data.lights.new(name, kind); ld.energy = power; ld.color = lin(color) if isinstance(color, str) else color
    ld.use_shadow = True
    if kind in ('POINT', 'SPOT'): ld.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, ld); coll.objects.link(ob); ob.location = loc
    if direction is not None: ob.rotation_euler = Vector(direction).normalized().to_track_quat('-Z', 'Y').to_euler()
    try: ob.visible_camera = False
    except AttributeError: pass
    if practical: REG['lights'].append(ob)
    return ob

def point(coll, name, loc, color, K, d, radius=0.02, practical=True):
    """Point light giving key K at distance d (see module doc)."""
    return _light(coll, name, 'POINT', loc, color, K * d * d * 4 * math.pi ** 2, radius, None, practical)

def spot(coll, name, loc, direction, color, K, d, angle_deg=70, blend=0.25, radius=0.03, practical=True):
    ob = _light(coll, name, 'SPOT', loc, color, K * d * d * 4 * math.pi ** 2, radius, direction, practical)
    ob.data.spot_size = math.radians(angle_deg); ob.data.spot_blend = blend; ob.data.show_cone = False
    return ob

def area(coll, name, loc, direction, color, K, d, size=1.2, size_y=0.08, practical=True, spread=180.0):
    ob = _light(coll, name, 'AREA', loc, color, K * d * d * math.pi ** 2, 0.0, direction, practical)
    ob.data.shape = 'RECTANGLE'; ob.data.size = size; ob.data.size_y = size_y
    try: ob.data.spread = math.radians(spread)
    except AttributeError: pass
    return ob

def sun(coll, name, direction, color_k, angle_deg=0.5):
    """Sun with toon key color_k (linear rgb K); not practical (stays on with set_lights(False))."""
    kmax = max(color_k); ld = bpy.data.lights.new(name, 'SUN'); ld.energy = math.pi * kmax; ld.color = tuple(c / kmax for c in color_k)
    ld.angle = math.radians(angle_deg); ld.use_shadow = True
    ob = bpy.data.objects.new(name, ld); coll.objects.link(ob); ob.rotation_euler = Vector(direction).normalized().to_track_quat('-Z', 'Y').to_euler()
    return ob

# ----------------------------------------------------------------------------- switch
def set_lights(on=True):
    """Every registered practical light and emissive term on (True) or off (False). Returns the number of switched items."""
    on = bool(on); n = 0
    for ob in REG['lights']:
        try: ob.hide_render = not on; ob.hide_viewport = not on; n += 1
        except ReferenceError: pass
    for sock, v_on, v_off in REG['emit'] + REG['amb']:
        try: sock.default_value = v_on if on else v_off; n += 1
        except ReferenceError: pass
    STATE['on'] = on
    return n

def lights_on(): return STATE['on']
