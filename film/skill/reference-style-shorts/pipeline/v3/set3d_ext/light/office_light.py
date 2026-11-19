#!/usr/bin/env python3
"""office_light.py : the two extra lights of the office (shot plan build step 8, presets only), as an EXTENSION of
v3/set3d/office3d.py.  It imports office3d and changes the scene office3d.build() made; office3d.py is not edited.

    import office3d as S, office_light as OL
    A = S.build("INTERIOR_DAY")            # the reviewed set, office_day
    OL.apply("office_grey")                # next morning: dull drizzle day (shots 17-22)
    OL.apply("office_storm")               # shot 25: office_grey darkened, lightning-ready
    OL.flash(1.0, frame=f)                 # lightning: the key pulsed (keyed CONSTANT), OL.lightning(f) keys a 3-frame pulse
    OL.set_rain(drizzle=1.0, lash=0.0, frame=None)   # the animated rain card on the window
    OL.apply("office_day")                 # back to the reviewed INTERIOR_DAY, bit-identical

What apply() changes (nothing is rebuilt, no object of SET is moved; actors and cameras are untouched):
  1. the ambient of every lit material (office3d mat_lit: emission = (art x SHADE x shade_mul + LIFT) x F), per surface;
  2. the key sun: colour, energy, angle, and whether the room shell (walls, window, ceiling, beams, lamps) casts shadows:
     in office_grey and office_storm it does not, so there is no window patch, while actors and furniture still throw soft
     contact shadows (the shell casts again on the frames of a lightning flash);
  3. the sky card behind the window (grey overcast / storm texture with the same roofline), the bulbs and the banker lamp;
  4. the window rain card (LIGHT_EXT collection) and a second sun `olt_flash` from the key direction for lightning;
  5. the grade (spec/grade_compositor.py rebuilt with the preset's offset, slope, power, saturation and bloom);
  6. the actor cards' tint (office_storm only), on cards present at the time of the call (see tint_cards()).
office3d.STATE['P'] gets the preset's shade and lift, so materials made later with office3d.mat_lit match the light;
call apply() again after adding props or actors if they need the per-surface tint or the card tint.
CLI: python3 office_light.py stills <preset> [outdir]  (no actors, every camera, 360x640)"""
import os, sys, math
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, 'set3d'), os.path.join(PROJ, 'spec')):
    if p not in sys.path: sys.path.insert(0, p)
import office3d as S                                       # noqa: E402

TEX = os.path.join(HERE, 'tex')
RAIN_FRAMES = 96                                           # length of the rain loop (gen_tex.py), 3.2 s
EXT = 'LIGHT_EXT'                                          # collection of this module's objects

DAY = S.PRESETS['INTERIOR_DAY']
# ---------------------------------------------------------------------------------------------------- the presets
# shade, lift: the flat ambient and dark lift of the light model (office3d API.md section 5), replacing INTERIOR_DAY's.
# surf: an extra per-surface multiplier of the ambient (on top of the set's own shade_mul), by material-name keyword.
# key: the sun's scene-linear colour x energy (INTERIOR_DAY 2.30, 1.65, 0.74); key_shell=False: the room shell does not
#   block it (no window patch, a flat daylight wash from the window side); sun_angle: penumbra of what still blocks it.
# sky: (texture, strength) of the window card; bulb: strength of the pendant bulbs (slit of the banker lamp = 0.6 x);
# rain: (drizzle, lash) levels of the rain card; flash_energy: key multiple the lightning sun reaches at flash(1).
# grade: spec/grade_compositor.py parameters; card_tint: multiplier of the actor cards' colour.
PRESETS = {
    'office_day': dict(shade=DAY['shade'], lift=DAY['lift'], surf={}, kgain={}, key=DAY['key'], key_shell=True, sun_angle=DAY['sun_angle'],
                       sky=(None, DAY['sky']), bulb=DAY['bulb'], rain=(0.0, 0.0), flash_energy=0.0,
                       grade=dict(offset=DAY['grade_offset'], saturation=DAY['grade_saturation'], slope=(1.000, 0.985, 0.970), power=(1.0, 1.0, 1.0),
                                  bloom_size=DAY['bloom_size'], bloom_strength=0.5),
                       card_tint=(1.0, 1.0, 1.0)),
    'office_grey': dict(
        shade=(0.20, 0.23, 0.41), lift=(0.002, 0.005, 0.014),
        surf=dict(map=(1.60, 1.48, 1.18), wallpaper=(0.92, 1.0, 1.08), frieze=(1.10, 0.95, 0.80), wainscot=(1.30, 1.50, 0.60), planks=(1.45, 1.12, 0.72), rug=(1.10, 1.0, 0.88),
                  ceiling=(1.15, 1.45, 0.55), beam=(1.20, 1.45, 0.55), paper=(1.35, 1.30, 1.10), calendar=(1.35, 1.30, 1.10), sign=(1.2, 1.15, 1.05),
                  warm_flat=(1.30, 1.50, 0.60), flat_c8301c=(2.0, 0.35, 0.3)),
        kgain=dict(wallpaper=0.60, frieze=0.70, flat_c8301c=1.8),
        key=(0.66, 0.58, 0.50), key_shell=False, sun_angle=3.0,
        sky=('sky_grey.png', 1.0), bulb=8.0, rain=(1.0, 0.0), flash_energy=0.0,
        grade=dict(offset=(0.003, 0.004, 0.008), saturation=0.96, slope=(1.005, 1.005, 1.02), power=(1.02, 1.01, 1.0), bloom_size=0.08, bloom_strength=0.65),
        card_tint=(1.0, 1.0, 1.0)),
    'office_storm': dict(
        shade=(0.068, 0.082, 0.165), lift=(0.003, 0.003, 0.007),
        surf=dict(map=(1.60, 1.48, 1.18), wallpaper=(1.12, 0.92, 0.62), frieze=(1.15, 1.10, 0.55), wainscot=(1.30, 1.50, 0.60), planks=(1.40, 1.25, 0.65),
                  ceiling=(1.15, 1.45, 0.55), beam=(1.15, 1.55, 0.50), paper=(1.35, 1.30, 1.10), calendar=(1.35, 1.30, 1.10), sign=(1.2, 1.15, 1.05),
                  warm_flat=(1.25, 1.60, 0.55), rug=(1.15, 1.0, 0.85), flat_c8301c=(2.8, 0.35, 0.3)),
        kgain=dict(wallpaper=0.70, frieze=0.75, flat_c8301c=4.5),
        key=(0.12, 0.13, 0.19), key_shell=False, sun_angle=3.0,
        sky=("sky_storm.png", 1.0), bulb=12.0, rain=(0.35, 1.0), flash_energy=3.2,
        grade=dict(offset=(0.003, 0.003, 0.006), saturation=1.0, slope=(1.0, 0.99, 0.99), power=(1.02, 1.01, 1.0), bloom_size=0.08, bloom_strength=0.7),
        card_tint=(0.86, 0.86, 0.95)),
}
FLASH_COLOR = (0.82, 0.88, 1.0)                            # blue-white lightning
FLASH_ANGLE = 1.2                                          # degrees: the window bars print fairly sharp in the flash
FLASH_SKY = 2.2                                            # the sky card brightens by this factor x flash
FLASH_RAIN = 1.5
SHELL = ('walls', 'wall_relief', 'window', 'ceiling', 'beams', 'pendants', 'pendant_bulbs')   # never shadow the office_grey key
RAIN_RECT = dict(x=S.XW + 0.095, y0=S.WIN['y0'], y1=S.WIN['y1'], z0=S.WIN['z0'], z1=S.WIN['z1'])  # inside the frame depth (3.84..3.95), cut by the bars

_ST = {}                                                   # module state: preset, objects


# ---------------------------------------------------------------------------------------------------- helpers
def _lit_nodes(m):
    """(shade mix node, lift node) of an office3d.mat_lit material, else None."""
    if not m.node_tree: return None
    nt = m.node_tree; ms = lf = None
    if not any(n.bl_idname == 'ShaderNodeBsdfDiffuse' for n in nt.nodes): return None
    for n in nt.nodes:
        if n.bl_idname == 'ShaderNodeMix' and n.data_type == 'RGBA' and n.blend_type == 'MULTIPLY':
            for l in n.outputs[2].links:
                if l.to_node.bl_idname == 'ShaderNodeVectorMath' and l.to_node.operation == 'ADD': ms, lf = n, l.to_node
    return (ms, lf) if ms else None


def _albedo(m):
    """linear albedo of a flat (untextured) lit material, None for a textured one."""
    nt = m.node_tree
    if any(n.bl_idname == 'ShaderNodeTexImage' for n in nt.nodes): return None
    for n in nt.nodes:
        if n.bl_idname == 'ShaderNodeVectorMath' and n.operation == 'SCALE' and not n.inputs[0].is_linked and n.inputs['Scale'].is_linked:
            return tuple(n.inputs[0].default_value)
    return None


def _match(k, name):
    """preset keys: 'map' matches the textured material tex_map, 'flat_c8301c' a flat colour (the red track and pencils)."""
    return (k in name) if k.startswith('flat_') else (('tex_' + k) in name)


def _surf_key(m, surf):
    """per-surface ambient multiplier: by material-name keyword, else 'warm_flat' for untextured red-brown woods."""
    for k, v in surf.items():
        if k != 'warm_flat' and _match(k, m.name): return tuple(v)
    a = _albedo(m)
    if a is not None and 'warm_flat' in surf:
        import colorsys
        h, sat, v = colorsys.rgb_to_hsv(*[c ** (1 / 2.2) for c in a])
        if (h < 45 / 360 or h > 350 / 360) and sat > 0.35 and v < 0.75: return tuple(surf['warm_flat'])
    return (1.0, 1.0, 1.0)


def _coll():
    sc = bpy.context.scene; c = bpy.data.collections.get(EXT)
    if c is None: c = bpy.data.collections.new(EXT)
    if c.name not in [k.name for k in sc.collection.children]: sc.collection.children.link(c)
    return c


def _ctl():
    """control empty with the animatable properties flash, drizzle, lash (drivers read them)."""
    ob = bpy.data.objects.get('olt_ctl')
    if ob is None:
        ob = bpy.data.objects.new('olt_ctl', None); _coll().objects.link(ob); ob.hide_render = True
        for k in ('flash', 'drizzle', 'lash', 'sky_base', 'flash_energy', 'rain_gain'): ob[k] = 0.0
    return ob


def _driver(idblock, path, expr, names, index=-1):
    try: idblock.driver_remove(path, index)
    except TypeError: pass
    fc = idblock.driver_add(path, index) if index >= 0 else idblock.driver_add(path)
    d = fc.driver; d.type = 'SCRIPTED'
    for v in list(d.variables): d.variables.remove(v)
    for vn in names:
        v = d.variables.new(); v.name = vn; v.type = 'SINGLE_PROP'; v.targets[0].id = _ctl(); v.targets[0].data_path = '["%s"]' % vn
    d.expression = expr
    return fc


def _seq_image(kind):
    path = os.path.join(TEX, 'rain_' + kind, 'r_0001.png')
    if not os.path.exists(path): raise FileNotFoundError(path + ' (run gen_tex.py)')
    im = bpy.data.images.load(path, check_existing=True); im.source = 'SEQUENCE'
    return im


def _rain_material():
    name = 'OLT_rain'
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    L = nt.links.new; out = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    last = tr.outputs['BSDF']
    for kind in ('drizzle', 'lash'):
        tex = nt.nodes.new('ShaderNodeTexImage'); tex.name = 'rain_' + kind; tex.image = _seq_image(kind); tex.extension = 'REPEAT'; tex.interpolation = 'Linear'
        iu = tex.image_user; iu.frame_duration = RAIN_FRAMES; iu.frame_start = 1; iu.frame_offset = 0; iu.use_cyclic = True; iu.use_auto_refresh = True
        emi = nt.nodes.new('ShaderNodeEmission'); emi.name = 'emi_' + kind; L(tex.outputs['Color'], emi.inputs['Color'])
        lv = nt.nodes.new('ShaderNodeValue'); lv.name = 'lvl_' + kind
        mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.use_clamp = True; L(tex.outputs['Alpha'], mul.inputs[0]); L(lv.outputs[0], mul.inputs[1])
        mx = nt.nodes.new('ShaderNodeMixShader'); L(mul.outputs[0], mx.inputs['Fac']); L(last, mx.inputs[1]); L(emi.outputs['Emission'], mx.inputs[2])
        last = mx.outputs['Shader']
    L(last, out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    nt2 = m.node_tree
    _driver(nt2.nodes['lvl_drizzle'].outputs[0], 'default_value', 'drizzle', ['drizzle'])
    _driver(nt2.nodes['lvl_lash'].outputs[0], 'default_value', 'lash', ['lash'])
    for kind in ('drizzle', 'lash'):
        _driver(nt2.nodes['emi_' + kind].inputs['Strength'], 'default_value', 'rain_gain*(1+%g*flash)' % FLASH_RAIN, ['rain_gain', 'flash'])
    return m


def _rain_card():
    ob = bpy.data.objects.get('olt_rain')
    if ob is not None: return ob
    R = RAIN_RECT; me = bpy.data.meshes.new('olt_rain')
    # seen from the room (looking +x) screen-right is -y: u runs from y1 to y0, v up; the face normal is -x (into the room)
    me.from_pydata([(R['x'], R['y1'], R['z0']), (R['x'], R['y0'], R['z0']), (R['x'], R['y0'], R['z1']), (R['x'], R['y1'], R['z1'])], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
    me.materials.append(_rain_material())
    ob = bpy.data.objects.new('olt_rain', me); _coll().objects.link(ob); ob.visible_shadow = False; S.no_bounce(ob)
    return ob


def _flash_sun():
    ob = bpy.data.objects.get('olt_flash')
    if ob is not None: return ob
    d = bpy.data.lights.new('olt_flash', 'SUN'); d.color = FLASH_COLOR; d.energy = 0.0; d.angle = math.radians(FLASH_ANGLE)
    ob = bpy.data.objects.new('olt_flash', d); _coll().objects.link(ob)
    kd = S.Vector(S.STATE['P']['key_dir']).normalized(); ob.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); ob.location = (S.XW + 3, -5, 6.2)
    _driver(d, 'energy', 'flash*flash_energy*%g' % (math.pi * max(DAY['key'])), ['flash', 'flash_energy'])
    # the flash must not be the light the actors' shadow proxies follow ("first visible SUN"): keep it after key_sun
    return ob


def _shell_objs():
    return [o for o in (S.STATE['objects'].get(nm) or bpy.data.objects.get(nm) for nm in SHELL) if o is not None]


def _clear_obj_keys(ob, path):
    for fc in S._fcurves(ob):
        if fc.data_path == path: fc.keyframe_points.clear()


def _shell_shadows(on, frame=None):
    """The room shell (walls, window, ceiling, beams, lamps) casts shadows (on=True: the reviewed behaviour, a window patch)
    or not (on=False: no patch, the key becomes a flat wash from the window side; actors and furniture still shadow it).
    Ray visibility, not light linking: light linking cost 30 percent more per frame (measured, API.md).  The bulbs keep their
    own setting (never a shadow caster).  frame=N keys it (a boolean key holds until the next one)."""
    sh0 = _ST.setdefault('shadow0', {o.name: o.visible_shadow for o in _shell_objs()})
    for o in _shell_objs():
        o.visible_shadow = bool(on) and sh0.get(o.name, True)
        if frame is not None: o.keyframe_insert('visible_shadow', frame=frame)


def _sky_material(texname, strength):
    if texname is None: return bpy.data.materials.get(_ST['sky_day'])
    name = 'OLT_sky_' + texname.split('.')[0]
    m = bpy.data.materials.get(name)
    if m is None:
        m = S.mat_emit(name, image=os.path.join(TEX, texname), strength=strength)
    return m


def _grade(g):
    import grade_compositor as G
    import warnings
    sc = bpy.context.scene
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    gp = dict(vignette_strength=0.0, bloom_strength=g['bloom_strength'], bloom_size=g['bloom_size'], offset=tuple(g['offset']),
              saturation=float(g['saturation']), slope=tuple(g['slope']), power=tuple(g['power']))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore'); G.build(sc, preset=gp)
    sc.render.use_compositing = True


def _is_card_material(m):
    if not m or not m.node_tree: return False
    ids = {n.bl_idname for n in m.node_tree.nodes}
    return 'ShaderNodeTexImage' in ids and 'ShaderNodeEmission' in ids and 'ShaderNodeBsdfTransparent' in ids and 'ShaderNodeBsdfDiffuse' not in ids


def tint_cards(rgb=None):
    """Multiply the colour of every actor card in the scene (stage actors '<name>_card', office3d placeholders 'actor_*')
    by rgb (default: the current preset's card_tint).  Idempotent; (1, 1, 1) restores the untinted card exactly."""
    rgb = tuple(rgb or PRESETS[_ST.get('preset', 'office_day')]['card_tint']); n = 0
    for ob in bpy.context.scene.objects:
        if not (ob.name.endswith('_card') or ob.name.startswith('actor_')) or ob.type != 'MESH': continue
        for sl in ob.material_slots:
            m = sl.material
            if not _is_card_material(m): continue
            nt = m.node_tree; emi = next(x for x in nt.nodes if x.bl_idname == 'ShaderNodeEmission')
            tn = nt.nodes.get('olt_tint')
            if tn is None:
                src = emi.inputs['Color'].links[0].from_socket if emi.inputs['Color'].links else None
                if src is None: continue
                tn = nt.nodes.new('ShaderNodeMix'); tn.name = 'olt_tint'; tn.data_type = 'RGBA'; tn.blend_type = 'MULTIPLY'; tn.inputs[0].default_value = 1.0
                nt.links.new(src, tn.inputs[6]); nt.links.new(tn.outputs[2], emi.inputs['Color'])
            tn.inputs[7].default_value = (*rgb, 1.0); n += 1
    return n


# ---------------------------------------------------------------------------------------------------- public API
def apply(preset):
    """Switch the built office to one of PRESETS ('office_day', 'office_grey', 'office_storm'). Needs office3d.build() first
    (any time after it; call it again after another office3d.build())."""
    if 'P' not in S.STATE or 'objects' not in S.STATE: raise RuntimeError('office3d.build() first')
    if preset not in PRESETS: raise KeyError(preset)
    Q = PRESETS[preset]; P = S.STATE['P']
    if _ST.get('build_id') != id(S.STATE['objects']):         # a new office3d.build(): forget the old bookkeeping
        _ST.clear(); _ST['build_id'] = id(S.STATE['objects'])
        _ST['sky_day'] = S.STATE['objects']['sky'].data.materials[0].name
        _ST['P0'] = dict(shade=tuple(P['shade']), lift=tuple(P.get('lift', (0, 0, 0))))
    cur = _ST.get('cur', _ST['P0'])
    # 1. ambient of every lit material: B = shade x sm x surf.  sm (the set's own shade_mul) is recovered once per material
    for m in bpy.data.materials:
        nn = _lit_nodes(m)
        if nn is None: continue
        ms, lf = nn
        if 'olt_sm' not in m:
            b = ms.inputs[7].default_value; m['olt_sm'] = [b[i] / max(cur['shade'][i], 1e-9) / m.get('olt_surf', (1, 1, 1))[i] for i in range(3)]
        sm = m['olt_sm']; sf = _surf_key(m, Q['surf']); m['olt_surf'] = list(sf)
        ms.inputs[7].default_value = (*[Q['shade'][i] * sm[i] * sf[i] for i in range(3)], 1.0)
        lf.inputs[1].default_value = tuple(Q['lift'])
        dv = next((n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeMath' and n.operation == 'DIVIDE'), None)
        if dv is not None:
            if 'olt_g0' not in m: m['olt_g0'] = dv.inputs[0].default_value
            kg = next((v for k, v in Q.get('kgain', {}).items() if _match(k, m.name)), 1.0)
            dv.inputs[0].default_value = m['olt_g0'] * kg
    P['shade'] = tuple(Q['shade']); P['lift'] = tuple(Q['lift']); _ST['cur'] = dict(shade=tuple(Q['shade']), lift=tuple(Q['lift']))
    # 2. key sun
    sun = S.STATE.get('sun')
    if sun is not None:
        k = max(Q['key']); sun.data.color = tuple(x / k for x in Q['key']); sun.data.energy = math.pi * k; sun.data.angle = math.radians(Q['sun_angle'])
        sun.light_linking.blocker_collection = None
        for o in _shell_objs(): _clear_obj_keys(o, 'visible_shadow')
        _shell_shadows(Q['key_shell'])
    # 3. sky card, bulbs, banker lamp
    sky = S.STATE['objects']['sky']; sm_ = _sky_material(Q['sky'][0], Q['sky'][1]); sky.data.materials[0] = sm_
    if Q['sky'][0] is not None:
        emi = next(n for n in sm_.node_tree.nodes if n.bl_idname == 'ShaderNodeEmission')
        _driver(emi.inputs['Strength'], 'default_value', 'sky_base*(1+%g*flash)' % FLASH_SKY, ['sky_base', 'flash'])
    for m in bpy.data.materials:
        if '_emit_' not in m.name or not m.node_tree: continue
        emi = next((n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeEmission'), None)
        if emi is None: continue
        if 'olt_s0' not in m: m['olt_s0'] = emi.inputs['Strength'].default_value
        emi.inputs['Strength'].default_value = m['olt_s0'] * Q['bulb'] / DAY['bulb']
    # 4. rain card, flash sun, controls
    ctl = _ctl(); ctl['sky_base'] = float(Q['sky'][1]); ctl['flash_energy'] = float(Q['flash_energy']); ctl['rain_gain'] = 0.9 if preset == 'office_grey' else 0.55
    rain = _rain_card(); fl = _flash_sun()
    on = Q['rain'] != (0.0, 0.0); rain.hide_render = not on
    set_rain(*Q['rain'])
    _clear_keys(ctl, 'flash'); _clear_obj_keys(fl, 'hide_render'); ctl['flash'] = 0.0; fl.hide_render = True
    # 5. grade, 6. cards
    _grade(Q['grade'])
    _touch()
    _ST['preset'] = preset; S.STATE['light'] = preset
    tint_cards(Q['card_tint'])
    for o in _coll().objects:
        if o.type == 'MESH': S.no_bounce(o)          # never on the flash sun: a light hidden from diffuse rays lights nothing
    return dict(preset=preset, shade=Q['shade'], lift=Q['lift'], key=Q['key'], sun_angle=Q['sun_angle'], key_shell=Q['key_shell'],
                sky=Q['sky'], bulb=Q['bulb'], rain=Q['rain'], flash_energy=Q['flash_energy'], grade=Q['grade'], card_tint=Q['card_tint'])


def _clear_keys(ob, prop):
    for fc in S._fcurves(ob):
        if fc.data_path == '["%s"]' % prop: fc.keyframe_points.clear()


def _key(ob, prop, frame, interp):
    ob.keyframe_insert('["%s"]' % prop, frame=frame)
    for fc in S._fcurves(ob):
        if fc.data_path == '["%s"]' % prop:
            for kp in fc.keyframe_points: kp.interpolation = interp


def set_rain(drizzle=1.0, lash=0.0, frame=None, phase=None):
    """Rain on the window card: drizzle (beads and drops sliding down in stick-slip steps with wet trails) and lash
    (wind-driven streaks, dense drops), each 0..1.  frame=N keys both (LINEAR between keys).  phase: offset of the 96-frame
    loop in frames (two shots that must not repeat the same water can use different phases)."""
    ctl = _ctl(); ctl['drizzle'] = float(drizzle); ctl['lash'] = float(lash)
    if frame is not None: _key(ctl, 'drizzle', frame, 'LINEAR'); _key(ctl, 'lash', frame, 'LINEAR')
    if phase is not None:
        for n in _rain_material().node_tree.nodes:
            if n.bl_idname == 'ShaderNodeTexImage': n.image_user.frame_offset = int(phase)
    _touch()
    ob = bpy.data.objects.get('olt_rain')
    if ob is not None and (drizzle > 0 or lash > 0 or frame is not None): ob.hide_render = False


def flash(amount, frame=None):
    """Lightning: a blue-white sun from the key direction (1.2 degrees) at amount x flash_energy x the INTERIOR_DAY key,
    the sky card brightened x(1 + 2.2 amount), the rain lit.  While amount > 0 the room shell casts shadows again, so the
    flash prints the window and its bars on the floor and the map wall; at amount 0 the flash sun is hidden (no cost).
    frame=N keys all of it at frame N (CONSTANT: it holds until the next key, so key 0 after the flash; lightning() does
    both).  The keys stay until the next apply().  flash_energy is 0 in office_day and office_grey: set_flash_energy() there."""
    ctl = _ctl(); ctl['flash'] = float(amount); fl = _flash_sun(); on = amount > 0 and ctl['flash_energy'] > 0
    fl.hide_render = not on
    if frame is not None:
        _key(ctl, 'flash', frame, 'CONSTANT'); fl.keyframe_insert('hide_render', frame=frame)
    if not PRESETS[_ST.get('preset', 'office_day')]['key_shell']: _shell_shadows(on, frame)
    _touch()


def lightning(frame, pattern=(1.0, 0.35, 0.8)):
    """Key a lightning pulse: pattern[i] on frame + i (CONSTANT), 0 on frame + len(pattern). Default: 3 frames, a double strike."""
    for i, a in enumerate(pattern): flash(a, frame + i)
    flash(0.0, frame + len(pattern))


def _touch():
    """a property set from Python does not tag the depsgraph: tag the control and every driven datablock."""
    _ctl().update_tag()
    for idb in [bpy.data.lights.get('olt_flash'), bpy.data.materials.get('OLT_rain')] + [m for m in bpy.data.materials if m.name.startswith('OLT_sky_')]:
        if idb is not None: idb.update_tag()
    bpy.context.view_layer.update()


def set_flash_energy(e):
    """key multiple the flash reaches at flash(1) (office_storm 3.2); lets office_day or office_grey have lightning too."""
    _ctl()['flash_energy'] = float(e); _touch()


def state():
    ctl = bpy.data.objects.get('olt_ctl')
    return dict(preset=_ST.get('preset'), flash=ctl['flash'] if ctl else 0.0, drizzle=ctl['drizzle'] if ctl else 0.0, lash=ctl['lash'] if ctl else 0.0)


# ---------------------------------------------------------------------------------------------------- CLI
def cli_stills(preset, outdir):
    A = S.build('INTERIOR_DAY'); sc = bpy.context.scene; S.setup_render(sc, 'preview'); sc.render.threads = 2; S.set_track(1.0, 0.0)
    apply(preset); os.makedirs(outdir, exist_ok=True)
    for nm, cs in A['cams'].items():
        S.make_camera(cs); w, c = S.render(os.path.join(outdir, '%s_%s.png' % (preset, nm))); print(nm, '%.1f s' % w, flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'stills': cli_stills(a[1] if len(a) > 1 else 'office_grey', a[2] if len(a) > 2 else os.path.join(HERE, 'work', 'stills'))
    else: print(__doc__)
