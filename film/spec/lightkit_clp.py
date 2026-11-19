"""Lighting / material kit for the 'color_light_post' spec (Blender 5.3 bpy module, Cycles CPU).

Model (scene-linear, Standard view transform, exposure 0):
    displayed = albedo * (A + K * n.l * visibility)        for environment surfaces
    A = flat ambient colour, injected as EMISSION (albedo * A) -> noise-free, exactly tinted shadows
    K = key (sun) irradiance factor on a surface facing it; sun.energy = pi * max(K) / 1.0
    characters = unlit emission cut-outs (camera rays only) that still block the sun -> hard cast shadows
All numbers come from color_light_post.md. API calls below were executed in Blender 5.3.0 (no render).
"""
import bpy, math

def hex_lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

# Character artwork constants (compositor-checked: head displays #fcf7f6, ink #322032 after the default grade).
HEAD_ARTWORK = '#fcfafa'
INK = '#2b1e2a'
# Optional per-shot multiply tints for characters (clip B behaviour); clip A uses (1, 1, 1) everywhere.
HEAD_TINTS = {'none': (1.0, 1.0, 1.0), 'night_lilac': (0.97, 0.76, 0.98), 'night_pink': (0.99, 0.70, 0.82),
              'warm_interior': (0.98, 0.80, 0.74)}

# A = ambient factor (linear RGB), K = key factor (linear RGB) on a surface facing the key.
# 'head' is the head fill AS DISPLAYED in the reference for that treatment (a target, not an input).
PRESETS = {
    # office with a hard sun shaft through the window; model: clip A t32.5/t34.5 + clip B hall shade ratio
    'INTERIOR_DAY':   dict(A=(0.42, 0.40, 0.56), K=(0.70, 0.54, 0.15), elev=38, az=-55, angle=1.5,
                           head='#fbf7f5', sky=('#4a78cd', '#5e92e5', '#92b7e7')),
    # lamp-lit evening / storm office; model: clip A t27.5, clip B t22-23 (lamps are the key, no sun)
    'INTERIOR_LAMP':  dict(A=(0.20, 0.16, 0.30), K=(0.0, 0.0, 0.0), elev=0, az=0, angle=1.5,
                           head='#fbf4ee', sky=('#1e2e7b', '#1748ae', '#4c4f90'),
                           lamp_color=(1.0, 0.69, 0.31), lamp_gain=0.9),
    'EXTERIOR_NOON':  dict(A=(0.10, 0.21, 0.79), K=(0.90, 0.79, 0.21), elev=50, az=-55, angle=1.5,
                           head='#fcf8f6', sky=('#386ec9', '#5e92e5', '#92b7e7')),
    'LATE_AFTERNOON': dict(A=(0.20, 0.45, 0.95), K=(0.85, 0.50, 0.10), elev=20, az=-70, angle=1.5,
                           head='#faf9f5', sky=('#4d7dd0', '#6ea0e8', '#83aee3')),
    'SUNSET':         dict(A=(0.35, 0.25, 0.45), K=(0.80, 0.44, 0.20), elev=8, az=-80, angle=2.5,
                           head='#fff5f3', sky=('#bdb0b8', '#eee4cf', '#f2d8ab')),
    'NIGHT':          dict(A=(0.12, 0.13, 0.45), K=(0.33, 0.35, 0.75), elev=45, az=-55, angle=1.5,
                           head='#fbdaf7', sky=('#1a3b92', '#1748ae', '#204c8f')),
}

def setup_render(scene, samples=24):
    scene.render.engine = 'CYCLES'
    c = scene.cycles
    c.device = 'CPU'; c.samples = samples; c.use_adaptive_sampling = True; c.use_denoising = True
    # direct light only for diffuse: the emission ambient must not be counted again as bounce light
    c.max_bounces = 1; c.diffuse_bounces = 0; c.glossy_bounces = 1
    c.transmission_bounces = 0; c.volume_bounces = 0; c.transparent_max_bounces = 8
    c.caustics_reflective = False; c.caustics_refractive = False
    c.sample_clamp_indirect = 3.0
    vs = scene.view_settings
    vs.view_transform = 'Standard'; vs.look = 'None'; vs.exposure = 0.0; vs.gamma = 1.0
    scene.display_settings.display_device = 'sRGB'
    scene.render.film_transparent = False

def _nt(mat):
    try: mat.use_nodes = True
    except Exception: pass
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt

def env_material(name, albedo_hex, A, image=None, ao=False, gloss=0.0):
    """Diffuse(albedo) + Emission(albedo * A). `image` (bpy image, sRGB) replaces the flat albedo."""
    m = bpy.data.materials.new(name); nt = _nt(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 1.0
    emi = nt.nodes.new('ShaderNodeEmission'); emi.inputs['Strength'].default_value = 1.0
    add = nt.nodes.new('ShaderNodeAddShader')
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs[0].default_value = 1.0
    mul.inputs[7].default_value = (*A, 1.0)                      # B = ambient colour
    if image is not None:
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = image
        L(tex.outputs['Color'], dif.inputs['Color']); L(tex.outputs['Color'], mul.inputs[6])
    else:
        col = (*hex_lin(albedo_hex), 1.0)
        dif.inputs['Color'].default_value = col; mul.inputs[6].default_value = col
    src = mul.outputs[2]
    if ao:                                                        # optional contact darkening of the ambient
        aon = nt.nodes.new('ShaderNodeAmbientOcclusion'); aon.samples = 8; aon.inputs['Distance'].default_value = 0.5
        m2 = nt.nodes.new('ShaderNodeMix'); m2.data_type = 'RGBA'; m2.blend_type = 'MULTIPLY'; m2.inputs[0].default_value = 0.6
        L(src, m2.inputs[6]); L(aon.outputs['AO'], m2.inputs[7]); src = m2.outputs[2]
    L(src, emi.inputs['Color'])
    L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1])
    last = add.outputs['Shader']
    if gloss > 0:
        gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.25
        mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = gloss
        L(last, mx.inputs[1]); L(gl.outputs['BSDF'], mx.inputs[2]); last = mx.outputs['Shader']
    L(last, out.inputs['Surface'])
    return m

def emissive_material(name, hex_color, strength=8.0):
    """Lamp bulbs, flames, sun-lit window panes: strength > 1 is what the bloom threshold (1.0) catches."""
    m = bpy.data.materials.new(name); nt = _nt(m)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission')
    emi.inputs['Color'].default_value = (*hex_lin(hex_color), 1.0); emi.inputs['Strength'].default_value = strength
    nt.links.new(emi.outputs['Emission'], out.inputs['Surface'])
    return m

def character_material(name, image, tint=(1.0, 1.0, 1.0)):
    """Unlit cut-out: shows the drawn colours exactly, emits only towards the camera, blocks the sun."""
    m = bpy.data.materials.new(name); nt = _nt(m); L = nt.links.new
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = image
    lp = nt.nodes.new('ShaderNodeLightPath')
    tin = nt.nodes.new('ShaderNodeMix'); tin.data_type = 'RGBA'; tin.blend_type = 'MULTIPLY'
    tin.inputs[0].default_value = 1.0; tin.inputs[7].default_value = (*tint, 1.0)
    emi = nt.nodes.new('ShaderNodeEmission')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader')
    L(tex.outputs['Color'], tin.inputs[6]); L(tin.outputs[2], emi.inputs['Color'])
    L(lp.outputs['Is Camera Ray'], emi.inputs['Strength'])
    L(tex.outputs['Alpha'], mix.inputs['Fac']); L(tr.outputs['BSDF'], mix.inputs[1]); L(emi.outputs['Emission'], mix.inputs[2])
    L(mix.outputs['Shader'], out.inputs['Surface'])
    return m

def add_sun(scene, K, elev_deg, az_deg, angle_deg=1.5, name='key_sun'):
    """K = linear RGB irradiance factor on a surface facing the sun. az 0 = light travelling +Y, -90 = travelling +X."""
    k = max(K)
    if k <= 0: return None
    d = bpy.data.lights.new(name, 'SUN')
    d.color = tuple(x / k for x in K); d.energy = math.pi * k; d.angle = math.radians(angle_deg)
    o = bpy.data.objects.new(name, d); scene.collection.objects.link(o)
    o.rotation_euler = (math.radians(90 - elev_deg), 0.0, math.radians(az_deg))
    return o

def add_lamp(scene, location, color, gain, distance, name='lamp', radius=0.05):
    """Point light giving `gain` (x albedo) on a facing surface at `distance` metres: P = gain * 4 * pi^2 * d^2."""
    d = bpy.data.lights.new(name, 'POINT'); d.color = color
    d.energy = gain * 4.0 * math.pi ** 2 * distance ** 2; d.shadow_soft_size = radius
    o = bpy.data.objects.new(name, d); scene.collection.objects.link(o); o.location = location
    return o

def set_world(scene, hex_color='#000000', strength=0.0):
    w = bpy.data.worlds.new('W_clp'); scene.world = w
    try: w.use_nodes = True
    except Exception: pass
    bg = w.node_tree.nodes.get('Background')
    bg.inputs[0].default_value = (*hex_lin(hex_color), 1.0); bg.inputs[1].default_value = strength
    return w

def apply_preset(scene, name):
    p = PRESETS[name]
    setup_render(scene)
    set_world(scene, '#000000', 0.0)          # ambient lives in the materials, not in the world
    sun = add_sun(scene, p['K'], p['elev'], p['az'], p['angle'])
    return p, sun
