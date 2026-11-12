"""Compositor grade for the 'color_light_post' spec. Blender 5.3 (bpy module), CPU compositor.

    import grade_compositor as G
    G.build(scene)                         # Render Layers -> grade -> output
    G.build(scene, image=bpy_image)        # grade an existing image (compositor-only run, no 3D render)

All parameters are in PRESET; values were validated with compositor-only runs (see
color_light_post.md, section 'Validation runs'). Node properties are sockets in 5.x, and several
sockets share a name (Color Balance), so those are addressed by index.
"""
import bpy

PRESET = dict(
    bloom_type='Bloom',            # 'Bloom' (fast, 0.1 s/frame at 720x1280 on CPU)
    bloom_threshold=1.0,           # scene-linear; only emitters / blown sun patches are above 1
    bloom_size=0.05,               # tight halo: 10 % radius = core radius + ~20 px at 720 px width
    bloom_strength=0.5,
    bloom_tint=(1.0, 0.92, 0.80, 1.0),
    offset=(0.0075, 0.0035, 0.0095),   # ASC-CDL offset: black renders #150919 (luma 0.05), plum
    slope=(1.000, 0.985, 0.970),       # warm-cream highlights
    power=(1.00, 1.00, 1.00),
    saturation=1.12,
    vignette_strength=0.04,        # linear corner multiplier = 1 - strength; reference shows 0-5 % only
    vignette_size=(0.80, 0.80),    # ellipse size as fraction of frame
    vignette_blur=260,             # px at 720x1280
)

def _n(ng, idname, x, y=0):
    n = ng.nodes.new(idname); n.location = (x, y); return n

def build(scene, image=None, preset=None):
    p = dict(PRESET); p.update(preset or {})
    ng = bpy.data.node_groups.new('GradeCLP', 'CompositorNodeTree')
    ng.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    if image is None:
        src = _n(ng, 'CompositorNodeRLayers', -900); src.scene = scene
    else:
        src = _n(ng, 'CompositorNodeImage', -900); src.image = image
    # 1 bloom
    gl = _n(ng, 'CompositorNodeGlare', -700)
    gl.inputs['Type'].default_value = p['bloom_type']
    gl.inputs['Quality'].default_value = 'High'
    gl.inputs['Threshold'].default_value = p['bloom_threshold']
    gl.inputs['Smoothness'].default_value = 0.1
    gl.inputs['Size'].default_value = p['bloom_size']
    gl.inputs['Strength'].default_value = p['bloom_strength']
    gl.inputs['Saturation'].default_value = 1.0
    gl.inputs['Tint'].default_value = p['bloom_tint']
    # 2 colour balance, ASC-CDL: out = (in * slope + offset) ** power
    cb = _n(ng, 'CompositorNodeColorBalance', -500)
    cb.inputs['Type'].default_value = 'Offset/Power/Slope (ASC-CDL)'
    cb.inputs[9].default_value = 0.0                      # Offset basis (float)
    cb.inputs[10].default_value = (*p['offset'], 1.0)      # Offset colour
    cb.inputs[11].default_value = 1.0                     # Power (float)
    cb.inputs[12].default_value = (*p['power'], 1.0)       # Power colour
    cb.inputs[13].default_value = 1.0                     # Slope (float)
    cb.inputs[14].default_value = (*p['slope'], 1.0)       # Slope colour
    # 3 saturation
    hs = _n(ng, 'CompositorNodeHueSat', -300)
    hs.inputs['Saturation'].default_value = p['saturation']
    # 4 vignette: blurred ellipse -> remap to [1-strength, 1] -> multiply
    el = _n(ng, 'CompositorNodeEllipseMask', -700, -400)
    el.inputs['Size'].default_value = p['vignette_size']
    bl = _n(ng, 'CompositorNodeBlur', -500, -400)
    bl.inputs['Type'].default_value = 'Gaussian'
    bl.inputs['Size'].default_value = (p['vignette_blur'], p['vignette_blur'])
    bl.inputs['Extend Bounds'].default_value = False
    ma = _n(ng, 'ShaderNodeMath', -300, -400); ma.operation = 'MULTIPLY_ADD'
    ma.inputs[1].default_value = p['vignette_strength']
    ma.inputs[2].default_value = 1.0 - p['vignette_strength']
    mx = _n(ng, 'ShaderNodeMix', -100); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
    mx.inputs[0].default_value = 1.0
    out = _n(ng, 'NodeGroupOutput', 100)
    L = ng.links.new
    L(src.outputs['Image'], gl.inputs['Image'])
    L(gl.outputs['Image'], cb.inputs['Image'])
    L(cb.outputs['Image'], hs.inputs['Image'])
    L(el.outputs['Mask'], bl.inputs['Image'])
    L(bl.outputs['Image'], ma.inputs[0])
    L(hs.outputs['Image'], mx.inputs[6])     # A (colour)
    L(ma.outputs[0], mx.inputs[7])           # B (colour), float is promoted
    L(mx.outputs[2], out.inputs[0])          # Result (colour)
    scene.compositing_node_group = ng
    scene.render.compositor_device = 'CPU'
    return ng
