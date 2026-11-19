#!/usr/bin/env python3
"""telegraph.py : set of film 16 ("ไอ้บ้าลวด", Samuel Morse's telegraph line, Maryland / Washington 1825-1845) as a real 3D Blender set (bpy 5.x, Cycles CPU).
Three locations, one per process (the preset picks the location, default light, camera and set state):

    import telegraph as TG
    A = TG.build('line', 'line_close', light='DAY')        # LINE   : line_close line_wide line_rail line_trench line_trench_high line_trench_end trench_cut line_road line_wagon
    A = TG.build('studio', 'studio_wide')                  # STUDIO : studio_wide studio_easel studio_door studio_window
    A = TG.build('chamber', 'chamber_table', light='NIGHT')# CHAMBER: chamber_wide_high chamber_low chamber_table
    cam = TG.make_camera(A['cam'])                         # 22 mm, DOF OFF, far clip 2000
    TG.set_poles('bottle', 16); TG.set_trench(0.5, frame=n); TG.set_pulse(0.3, frame=n); TG.set_rain(True, frame=n) ...   (see API.md)

World: 1 unit = 1 D (head), Z up, adults ~3.2 D. LINE: the road / rail / pole line runs along world +x (the sb1 camera looks along +x), ground z = 0.
Authoring frame = styleboard/sb.py (metres) converted by telegraph_kit.W: D = 1.85 * metres (and a -90 deg turn about z for the LINE).
NO depth of field anywhere. NO text anywhere. Built on the client-approved style board (styleboard/sb.py), kit in telegraph_kit.py.
CLI: python3 telegraph.py final|stills [preset[:LIGHT]...]   |   python3 telegraph.py digest <preset>"""
import os, sys, math, json, time, random, hashlib
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import telegraph_kit as K                                  # noqa: E402
from telegraph_kit import MB, mat, mat_emit, hexc, lin, W, Wd, SC, FR, MATS, rnd, frame_mat   # noqa: E402
import tg_line as LN                                       # noqa: E402
WORK = os.path.join(HERE, 'telegraph_work')
STATE = {}

# ----------------------------------------------------------------------------- lights
SKYPOS = [0.0, 0.47, 0.53, 0.62, 0.74, 0.88, 1.0]       # smooth gradient: no hard horizon arc even when the camera pitches
def kdir(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

_L = dict(sun_angle=1.0, exposure=0.0, sat=1.08, wet=0.0, cloud_k=1.0, hill_k=1.0, fill=0.0, win=0.0, candle=0.0, lamp=0.0)
LINE_LIGHTS = dict(
    DAY=dict(_L, key=(1.0, 0.85, 0.63, 14.0), az=150, el=24, sky_k=0.85, amb=('#3e58ff', 2.2),
             sky=['#8a92d8', '#efc698', '#f3d3a8', '#cdc8d8', '#8db0ec', '#5a86e0', '#3a5acb'], hills=['#9a9ad2', '#8aa0d8', '#7ea4d6'], cloud=('#ffeacc', '#7c84d8')),
    DUSK=dict(_L, key=(1.0, 0.55, 0.3, 27.0), az=150, el=12, sun_angle=1.3, sky_k=0.95, amb=('#3a62ff', 2.9),
              sky=['#4a52b8', '#e6905a', '#f0a876', '#b8a4c0', '#6a86d8', '#3e58c0', '#262c98'], hills=['#7a78b8', '#6e7cc0', '#6a84c8'], cloud=('#ffc89a', '#6a72c4')),
    RAIN=dict(_L, key=(0.8, 0.82, 1.0, 2.4), az=150, el=32, sun_angle=16.0, sky_k=0.8, amb=('#6068ff', 3.3), wet=1.0, exposure=-0.1, cloud_k=0.8,
              sky=['#6a78b4', '#c4b4b0', '#c8c0c8', '#aab4d0', '#8a9ccc', '#6a80c0', '#4a62ac'], hills=['#7a82b8', '#6e7ab4', '#6a7cb4'], cloud=('#b8bad8', '#7e86c4')),
    AFTER_RAIN=dict(_L, key=(1.0, 0.85, 0.63, 9.0), az=-125, el=24, sun_angle=0.8, sky_k=1.0, amb=('#3a4cff', 2.2), wet=0.9,
                    sky=['#5a6cc4', '#f0b488', '#f4c8a0', '#b0a8d0', '#7488d0', '#4a64c4', '#2a3fa8'], hills=['#8a8ac8', '#7a96d2', '#7aa0d4'], cloud=('#ffe2bc', '#6c78d4')),
)
STUDIO_LIGHTS = dict(
    DAY=dict(_L, key=(1.0, 0.82, 0.55, 16.0), az=-24, el=34, sun_angle=1.2, sky_k=1.0, amb=('#4a56ff', 2.6), fill=0.55, win=1.2, exposure=-0.25,
             sky=['#8a92d8', '#f4c890', '#f8dcb0', '#d4cce0', '#a8c6f0', '#5a86e4', '#3a5acc'], hills=['#9a9ad2', '#8aa0d8', '#7ea4d6'], cloud=('#fff0dc', '#a8a4dc')),
)
CHAMBER_LIGHTS = dict(
    DAY=dict(_L, key=(1.0, 0.85, 0.63, 15.0), az=-22, el=15, sky_k=1.0, exposure=0.55, fill=1.0, win=1.9, candle=1.0, lamp=1.0, shafts=1.0, amb=('#5a60ff', 1.0),
             sky=['#8a92d8', '#f4c890', '#f8dcb0', '#d4cce0', '#a8c6f0', '#5a86e4', '#3a5acc'], hills=['#9a9ad2', '#8aa0d8', '#7ea4d6'], cloud=('#fff0dc', '#a8a4dc')),
    NIGHT=dict(_L, key=(0.4, 0.5, 1.0, 1.0), az=-22, el=32, sun_angle=2.5, sky_k=0.4, exposure=-0.7, fill=0.0, win=0.12, candle=2.6, lamp=2.4, nightc=1.0, shafts=0.0, amb=('#2a2eff', 0.2), sat=1.06,
               sky=['#1c2060', '#2c3478', '#3a4488', '#323c84', '#262e78', '#1a2268', '#101658'], hills=['#262c6a', '#222866', '#1e2462'], cloud=('#4a5090', '#2a3070')),
)
LIGHTS = dict(line=LINE_LIGHTS, studio=STUDIO_LIGHTS, chamber=CHAMBER_LIGHTS)
LOC_LIGHTS = {k: list(v) for k, v in LIGHTS.items()}
LIGHT_KEYS = ['DAY', 'DUSK', 'RAIN', 'AFTER_RAIN', 'NIGHT']

def _lerpP(a, b, k):
    out = {}
    for key, va in a.items():
        vb = b.get(key, va)
        if isinstance(va, (int, float)) and not isinstance(va, bool): out[key] = va + (vb - va) * k
        elif isinstance(va, tuple) and va and isinstance(va[0], (int, float)): out[key] = tuple(x + (y - x) * k for x, y in zip(va, vb))
        elif isinstance(va, tuple) and isinstance(va[0], str):     # (hex, number) or (hex, hex)
            out[key] = tuple(_mixhex(x, y, k) if str(x).startswith('#') else x + (y - x) * k for x, y in zip(va, vb))
        elif isinstance(va, list) and va and isinstance(va[0], str): out[key] = [_mixhex(x, y, k) for x, y in zip(va, vb)]
        else: out[key] = va
    return out
def _mixhex(a, b, k):
    ca, cb = hexc(a), hexc(b); return tuple(ca[i] + (cb[i] - ca[i]) * k for i in range(3)) + (1.0,)
def _col(c): return hexc(c) if isinstance(c, str) else tuple(c)

# ----------------------------------------------------------------------------- keying helpers
def _fc_interp(idb, path, frame, interp):
    ad = idb.animation_data
    if not ad or not ad.action: return
    try:
        from bpy_extras import anim_utils
    except Exception: anim_utils = None
    for fc in _fcurves(idb):
        if fc.data_path == path or fc.data_path.startswith(path):
            for kp in fc.keyframe_points:
                if abs(kp.co[0] - frame) < 1e-3: kp.interpolation = interp
def _fcurves(idb):
    ad = idb.animation_data; out = []
    if not ad or not ad.action: return out
    act = ad.action
    try:
        for layer in act.layers:
            for strip in layer.strips:
                for cb in strip.channelbags: out += list(cb.fcurves)
    except Exception: pass
    if not out and hasattr(act, 'fcurves'): out = list(act.fcurves)
    return out
def _key(idb, path, frame, interp='LINEAR', index=-1):
    idb.keyframe_insert(path, frame=frame, index=index)
    for fc in _fcurves(idb):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co[0] - frame) < 1e-3: kp.interpolation = interp
def _keysock(sock, value, frame, interp='LINEAR'):
    sock.default_value = value
    if frame is not None:
        sock.keyframe_insert('default_value', frame=frame)
        idb = sock.id_data
        for fc in _fcurves(idb):
            if 'default_value' in fc.data_path:
                for kp in fc.keyframe_points:
                    if abs(kp.co[0] - frame) < 1e-3: kp.interpolation = interp
def _setv(ob, vis, frame=None):
    ob.hide_render = not vis
    if frame is not None:
        _key(ob, 'hide_render', frame, 'CONSTANT')
def _show(objs, vis, frame=None):
    for o in (objs if isinstance(objs, (list, tuple)) else [objs]): _setv(o, vis, frame)
def _keyxf(ob, frame, loc=True, rot=False, scl=False, interp='LINEAR'):
    if loc: _key(ob, 'location', frame, interp)
    if rot: _key(ob, 'rotation_euler', frame, interp)
    if scl: _key(ob, 'scale', frame, interp)

def clear_keys():
    """Drop every key the hooks inserted (objects, lamps, materials, node groups, world, scene), so plain set_* calls hold again.
    Keeps drivers: only keyed actions are removed."""
    for idb in list(bpy.data.objects) + list(bpy.data.lights) + list(bpy.data.cameras):
        ad = idb.animation_data
        if ad and ad.action: ad.action = None
    for coll in (bpy.data.materials, bpy.data.node_groups, bpy.data.worlds):
        for m in coll:
            nt = getattr(m, 'node_tree', None) if coll is not bpy.data.node_groups else m
            if nt is not None and nt.animation_data: nt.animation_data_clear()
    sc = bpy.context.scene
    for idb in (sc, sc.view_settings):
        if getattr(idb, 'animation_data', None): idb.animation_data_clear()

# ----------------------------------------------------------------------------- sky world, sun, light application
def _sky_world():
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); cr.name = 'skyramp'; L(sp.outputs['Z'], cr.inputs[0]); bg.name = 'skybg'
    cr.color_ramp.elements[0].position = SKYPOS[0]
    for pos in SKYPOS[1:-1]: cr.color_ramp.elements.new(pos)
    cr.color_ramp.elements[-1].position = SKYPOS[-1]
    L(cr.outputs[0], bg.inputs['Color'])
    lp = N('ShaderNodeLightPath'); b2 = N('ShaderNodeBackground'); b2.name = 'ambbg'; mx = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx.inputs[0]); L(b2.outputs[0], mx.inputs[1]); L(bg.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    STATE['world'] = w

def apply_P(P, frame=None):
    """Apply a light parameter dict: sun, sky ramp, ambient, hills, clouds, exposure, wet. frame=n keys everything (LINEAR)."""
    sc = bpy.context.scene; ks = STATE['sun']; d = ks.data; k = P['key']
    kd = Vector(kdir(P['az'], P['el'])); kdw = Wd(kd)
    d.color = k[:3]; d.energy = k[3]; d.angle = math.radians(P['sun_angle'])
    ks.rotation_euler = (-kdw).to_track_quat('Z', 'Y').to_euler()
    nt = STATE['world'].node_tree; cr = nt.nodes['skyramp']
    for el, c in zip(cr.color_ramp.elements, P['sky']): el.color = _col(c)
    nt.nodes['skybg'].inputs['Strength'].default_value = P['sky_k']
    nt.nodes['ambbg'].inputs['Color'].default_value = _col(P['amb'][0]); nt.nodes['ambbg'].inputs['Strength'].default_value = P['amb'][1]
    for m, c in zip(STATE.get('hill_mats', []), P['hills']):
        e = m.node_tree.nodes['Emission']; e.inputs['Color'].default_value = _col(c); e.inputs['Strength'].default_value = P['hill_k']
    cm = STATE.get('cloud_mat')
    if cm is not None:
        cm.node_tree.nodes['cmix'].inputs[7].default_value = _col(P['cloud'][0]); cm.node_tree.nodes['cmix'].inputs[6].default_value = _col(P['cloud'][1])
        cm.node_tree.nodes['cem'].inputs['Strength'].default_value = P['cloud_k']; cm.node_tree.nodes['cdot'].inputs[1].default_value = (-kdw.x, -kdw.y, -kdw.z)
    sc.view_settings.exposure = P['exposure']
    for o in STATE.get('shafts', []): o.hide_render = P.get('shafts', 0.0) <= 0.0
    for grp, base in STATE.get('lamps', {}).items():
        kk = P.get(grp, 0.0)
        for l, e in base: l.data.energy = e * kk
    if frame is not None:
        ks.keyframe_insert('rotation_euler', frame=frame); d.keyframe_insert('color', frame=frame); d.keyframe_insert('energy', frame=frame); d.keyframe_insert('angle', frame=frame)
        for el in cr.color_ramp.elements: pass
        for i in range(len(SKYPOS)): cr.id_data.keyframe_insert('nodes["skyramp"].color_ramp.elements[%d].color' % i, frame=frame)
        for nm, sk in (('skybg', 'Strength'), ('ambbg', 'Strength'), ('ambbg', 'Color')): nt.keyframe_insert('nodes["%s"].inputs["%s"].default_value' % (nm, sk), frame=frame) if False else nt.nodes[nm].inputs[sk].keyframe_insert('default_value', frame=frame)
        for m in STATE.get('hill_mats', []): m.node_tree.nodes['Emission'].inputs['Color'].keyframe_insert('default_value', frame=frame)
        if cm is not None:
            for i_ in (6, 7): cm.node_tree.nodes['cmix'].inputs[i_].keyframe_insert('default_value', frame=frame)
        sc.view_settings.keyframe_insert('exposure', frame=frame)
        for grp, base in STATE.get('lamps', {}).items():
            for l, e in base: l.data.keyframe_insert('energy', frame=frame)
    STATE['P'] = P

def apply_light(name, frame=None, wet=True):
    """Switch the whole light (sun, sky, ambient, hills, clouds, exposure; wetness too when wet=True). Keyed when frame is given."""
    P = dict(LIGHTS[STATE['loc']][name]); STATE['light'] = name; apply_P(P, frame)
    if wet: set_wet(P['wet'], frame)
    return P

def set_light_mix(a, b, k, frame=None):
    """Blend two lights of this location (k 0 = a, 1 = b), e.g. set_light_mix('DAY', 'DUSK', 0.6, frame=n) for the DAY -> DUSK snaps. Keyed when frame is given."""
    LL = LIGHTS[STATE['loc']]; P = _lerpP(LL[a], LL[b], k); apply_P(P, frame); set_wet(P['wet'], frame); return P

def set_wet(k, frame=None):
    """Wetness 0..1 of every wettable material (poles, wood, road, ground, grass...): darker, glossier. Puddles appear above 0.35."""
    g = bpy.data.node_groups.get('TG_WET')
    if g is not None: _keysock(g.nodes['wet'].outputs[0], float(k), frame)
    for p in STATE.get('puddles', []): _setv(p, k > 0.35, frame)

# ----------------------------------------------------------------------------- shared scene hooks created lazily
def _emit_mat(name, hexcol, k, alpha=1.0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k
    if alpha < 1.0:
        tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); mx.inputs[0].default_value = alpha; L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    else: L(em.outputs[0], out.inputs['Surface'])
    MATS[name] = m; return m

# ----------------------------------------------------------------------------- build
LOC_OF = {}
def build(location=None, preset=None, light=None, clear=True, dress=True):
    """Build a location for a preset (PRESETS): scene reset, light, world, render settings, grade and the preset's set state.
    Returns the anchors dict (API.md); A['cam'] is the preset camera (make it with telegraph.make_camera)."""
    preset = preset or {'line': 'line_wide', 'studio': 'studio_wide', 'chamber': 'chamber_wide_high', None: 'line_wide'}[location]
    assert preset in PRESETS, 'preset %s is not one of %s' % (preset, list(PRESETS))
    PR = PRESETS[preset]; loc = PR['loc']; lkey = light or PR['light']
    assert lkey in LOC_LIGHTS[loc], 'light %s: %s has %s' % (lkey, loc, LOC_LIGHTS[loc])
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True)
    MATS.clear(); STATE.clear(); STATE.update(loc=loc, preset=preset, light=lkey)
    FR['rot'] = -math.pi / 2 if loc == 'line' else 0.0
    sc = bpy.context.scene; P = dict(LIGHTS[loc][lkey])
    _sky_world()
    d = bpy.data.lights.new('key', 'SUN'); ks = bpy.data.objects.new('key', d); sc.collection.objects.link(ks); STATE['sun'] = ks; STATE['lamps'] = {}
    if loc == 'line':
        LN.build_line(STATE, P)
        if dress and preset in FG:
            cl, lk = CAMS_M[PR['cam']]; STATE['fg'] = LN.fg_dress(STATE, STATE['M'], cl, lk, FG[preset], seed=31 + len(preset))
    elif loc == 'studio':
        import tg_studio as SD; SD.build_studio(STATE, P)
        if dress and preset in STUDIO_FG:
            cl, lk = CAMS_M[PR['cam']]; STATE['fg'] = SD.fg_dress(STATE, STATE['M'], cl, lk, STUDIO_FG[preset])
    else:
        import tg_chamber as CH; CH.build_chamber(STATE, P)
        if dress and preset == 'chamber_low': CH.fg_desk(STATE, *CAMS_M['chamber_low'])
    # shared hook objects (puddles, rain, sparks, pulse) are made by the location builders / lazily
    setup_render(sc, 'final'); setup_grade(sc, P)
    apply_P(P); set_wet(P['wet'])
    STATE['marks'] = {}; _marks(loc)
    apply_preset_state(preset)
    A = anchors(); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    """final 720x1280 (preview 360x640), Cycles CPU, few samples + OpenImageDenoise, direct light + sky/ambient (line / studio: no diffuse bounce; chamber: 2)."""
    r = scene.render; c = scene.cycles; r.engine = 'CYCLES'; c.device = 'CPU'
    r.resolution_x, r.resolution_y = 720, 1280; r.resolution_percentage = 100 if quality in ('final', 'hq') else 50
    c.samples = {'final': FINAL_SAMPLES.get(STATE.get('loc'), 12), 'hq': 24}.get(quality, 6)
    c.use_denoising = True; c.denoiser = 'OPENIMAGEDENOISE'; c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; c.denoising_prefilter = 'FAST'
    c.use_adaptive_sampling = False
    ind = STATE.get('loc') != 'line'
    c.max_bounces = 2; c.diffuse_bounces = 0; c.glossy_bounces = 1; c.transmission_bounces = 0; c.transparent_max_bounces = 8
    c.use_light_tree = False; c.filter_width = 1.2; r.threads_mode = 'FIXED'; r.threads = 2
    scene.view_settings.view_transform = 'Standard'; scene.view_settings.look = 'None'
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.film_transparent = False
    c.use_fast_gi = False
FINAL_SAMPLES = dict(line=7, studio=6, chamber=6)

def setup_grade(scene, P):
    """film-wide mild saturation (the board's grade: sat 1.08), no recolour: compositor from spec/grade_compositor."""
    sys.path.insert(0, os.path.join(PROJ, 'spec'))
    import warnings, grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        G.build(scene, preset=dict(vignette_strength=0.0, bloom_strength=0.0, offset=(0.0, 0.0, 0.0), saturation=float(P.get('sat', 1.08))))
    scene.render.use_compositing = True

def apply_dof(*a, **k):
    """Client rule: no depth of field at all (kept for API symmetry)."""
    return None

def make_camera(setup, name='cam', scene=None):
    """22 mm / 36 mm sensor camera from {loc, look_at, lens[, roll]}: DOF OFF, clip 0.05..2000; becomes the scene camera."""
    scene = scene or bpy.context.scene
    ob = bpy.data.objects.get(name)
    if ob is None:
        cd = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cd); scene.collection.objects.link(ob)
    cd = ob.data; cd.lens = setup.get('lens', 22); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.clip_start = 0.05; cd.clip_end = 2000; cd.dof.use_dof = False
    ob.location = setup['loc']; ob.rotation_euler = (Vector(setup['look_at']) - Vector(setup['loc'])).to_track_quat('-Z', 'Y').to_euler()
    if setup.get('roll'): ob.rotation_euler.rotate_axis('Z', math.radians(setup['roll']))
    scene.camera = ob; STATE['cam'] = ob; _rain_follow(); return ob

def render(path, scene=None):
    scene = scene or bpy.context.scene; scene.render.filepath = path
    t0 = time.time(); c0 = os.times(); bpy.ops.render.render(write_still=True); c1 = os.times()
    return time.time() - t0, (c1.user - c0.user) + (c1.system - c0.system)

# ----------------------------------------------------------------------------- cameras / marks / presets
def _cam(loc, look, lens=22.0, roll=0.0):
    return dict(loc=tuple(round(v, 3) for v in W(loc)), look_at=tuple(round(v, 3) for v in W(look)), lens=lens, **({'roll': roll} if roll else {}))

def _pm(x, y, z=0.0): return tuple(round(v, 3) for v in W((x, y, z)))

def _marks(loc):
    m = STATE['marks']
    if loc == 'line':
        px = LN.px; wy, wx_ = LN.WAGON[1], LN.WAGON[0]; kx, ky = LN.KEYCRATE; pl = LN.PLAT
        yaw = math.pi / 2 + 0.06
        def wl(lx, ly=0.0, z=0.0): return (wx_ - ly * math.sin(yaw) + lx * math.cos(yaw), wy + lx * math.sin(yaw) + ly * math.cos(yaw) * 1.0, z)
        rg = LN.rung(12)
        m.update(morse_ladder=_pm(*rg), morse_ladder_foot=_pm(px(4.0) + 1.6, 2.2, 0.0), morse_wide=_pm(px(4.0) - 0.7, 0.4, 0.0), morse_wire=_pm(-3.0, 24.0, 0.0), morse_rail=_pm(-4.6, 21.0, 0.0),
                 morse_pole=_pm(px(13.0) + 1.1, 12.0, 0.0), morse_ladder3=_pm(px(31.0) + 0.5, 30.5, 3.3),
                 morse_key=_pm(kx + 0.6, ky + 1.1, 0.0), worker_key_a=_pm(kx - 0.9, ky + 1.2, 0.0), worker_key_b=_pm(kx + 2.0, ky + 1.4, 0.0), worker_key_c=_pm(kx + 0.0, ky + 2.2, 0.0),
                 morse_wagon_key=_pm(*wl(-1.6, 0.0, 1.0)), worker_wagon=_pm(wx_ + 1.4, wy - 2.6, 0.0), morse_wagon_bed=_pm(*wl(0.5, 0.0, 1.0)), morse_bottle=_pm(*wl(0.5, 0.0, 1.0)))
        for i, y in enumerate((44.0, 49.0, 54.0, 59.0)): m['platform_%s' % 'abcd'[i]] = _pm(pl[0] - 1.3 - 0.4 * (i % 2), y, 1.0)
        m.update(pit_ground=_pm(LN.PIT[0], LN.PIT[1], 0.0))
        m.update(plough_marks(0.5)); m.update(buggy_marks(36.0))
    elif loc == 'studio':
        import tg_studio as SD; m.update({k: _pm(*v) for k, v in SD.MARKS.items()})
    else:
        import tg_chamber as CH; m.update({k: _pm(*v) for k, v in CH.MARKS.items()}); m.update({k: _pm(*v) for k, v in CH.congress_marks(STATE).items()})

def plough_marks(k):
    """world marks that follow the plough front at furrow fraction k (0..1): mules ahead, Cornell behind the handles, workers and Morse behind"""
    y = LN.Y0 + k * (LN.Y1 - LN.Y0); xt = LN.xc(y) + 2.3
    return dict(plough=_pm(xt, y, 0.0), mule_a=_pm(xt - 0.95, y + 5.2, 0.0), mule_b=_pm(xt + 0.45, y + 6.6, 0.0), cornell=_pm(xt - 1.3, y - 1.6, 0.0),
                worker_a=_pm(xt + 1.6, y - 3.2, 0.0), worker_b=_pm(xt - 1.6, y - 4.6, 0.0), morse_trench=_pm(xt + 1.9, y - 5.8, 0.0))

def buggy_marks(y):
    x = LN.xc(y)
    return dict(mocker_buggy=_pm(x + 0.0, y - 0.35, 0.95), mule_buggy=_pm(x, y + 3.9, 0.0))

HEIGHT = dict(morse=3.2, mocker=3.1, cornell=3.3, worker=3.1, messenger=3.0, clerk=3.0, congress=3.2)

def _import_tower():
    p = os.path.join(PROJ, 'v3', 'set3d2')
    if p not in sys.path: sys.path.insert(0, p)
    import tower as T
    T.PH.update(
        morse=('beach_man', dict(yaw=0.25, expr='happy', arm_l='down', arm_r='down', legs='stand'), HEIGHT['morse']),
        mocker=('boss', dict(yaw=0.3, head_roll=-4, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), HEIGHT['mocker']),
        cornell=('senior_a', dict(yaw=0.3, expr='determined', arm_l='down', arm_r='down', legs='stand'), HEIGHT['cornell']),
        worker=('senior_b', dict(yaw=-0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['worker']),
        messenger=('beach_kid', dict(yaw=-0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['messenger']),
        clerk=('senior_a', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['clerk']),
        congress=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['congress']))
    return T

def placeholder_actor(role, mark, face_to=None, tilt=0.0, name=None, ppd=256):
    """Stand-in card (tower.placeholder_actor) scaled to HEIGHT[role], standing at `mark` (x, y, ground z), facing `face_to`."""
    T = _import_tower(); return T.placeholder_actor(role, tuple(mark), face_to=face_to, tilt=tilt, name=name, ppd=ppd)

def _clear_actors():
    for o in list(bpy.context.scene.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)

def mule_card(mark, face_to=None, name='actor_mule', size=5.6):
    """placeholder mule (side-view card 5.6 x 3.7 D, facing +x) standing at `mark`, turned to face the camera (yaw only)"""
    import telegraph_tex as TX
    p = os.path.join(TX.OUT, 'mule_v1.png')
    if not os.path.exists(p): TX.mule(p)
    img = bpy.data.images.load(p, check_existing=True); m = bpy.data.materials.new(name + '_m'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tx = N('ShaderNodeTexImage'); tx.image = img; em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(tx.outputs['Color'], em.inputs['Color']); em.inputs['Strength'].default_value = 0.9; L(tx.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    w, h = size, size * 460 / 700
    me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2, 0, 0), (w / 2, 0, 0), (w / 2, 0, h), (-w / 2, 0, h)], [], [(0, 1, 2, 3)]); me.update(); uv = me.uv_layers.new(name='UVMap')
    for li, c in zip(range(4), ((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[li].uv = c
    me.materials.append(m); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.location = tuple(mark); ob.visible_shadow = False
    if face_to is not None:
        d = Vector(face_to) - Vector(mark); ob.rotation_euler = (0, 0, math.atan2(d.x, -d.y))
    return ob

def stage_placeholders(A, cam_name, cam_loc):
    _clear_actors(); out = []
    for i, (role, mk) in enumerate(_staging(cam_name)):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        if role == 'mule': out.append(mule_card(mk, cam_loc, 'actor_mule_%d' % i)); continue
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

def _staging(cam_name):
    return [(role, tuple(STATE['marks'][mk]) if isinstance(mk, str) else tuple(mk)) for role, mk in STAGING.get(cam_name, [])]

def head_pixels(cam_name):
    """[(role, mark, head_centre_y_px, head_px, chin_y_px, feet_y_px, head_x_px)] at 720x1280 (caption rule: chin < 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for i, (role, mk) in enumerate(_staging(cam_name)):
        if role == 'mule': continue
        h = HEIGHT[role]; m = Vector(mk); top, hc, bot = m + Vector((0, 0, h)), m + Vector((0, 0, h - 0.5)), m + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot)); f = world_to_camera_view(sc, cam, m)
        out.append((role, tuple(round(v, 2) for v in mk), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280), round(p.x * 720)))
    return out

def project(world_pt):
    """(x_px, y_px) of a world point in the scene camera (720x1280, y from the top)"""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; p = world_to_camera_view(sc, sc.camera, Vector(world_pt)); return round(p.x * 720), round((1 - p.y) * 1280)

CAMS_M = dict(
    # LINE (sb-frame metres): (loc, look)
    line_wide=((-0.2, -6.0, 1.9), (1.6, 30.0, 2.9)),
    line_close=((2.9, 0.7, 1.2), (4.6, 3.9, 3.7)),
    bottle_macro=((3.5, 2.0, 4.6), (4.35, 4.0, 5.7)),
    line_rail=((-14.5, 12.0, 1.4), (2.0, 17.0, 2.9)),
    line_station=((3.0, 33.0, 1.6), (-10.5, 52.0, 2.4)),
    line_trench=((-0.6, 27.2, 1.0), (3.4, 33.5, 1.6)),
    line_trench_high=((-2.0, 16.0, 4.5), (3.6, 34.0, 0.8)),
    line_trench_snap1=((-1.0, 8.0, 2.2), (3.3, 25.0, 1.0)),
    line_trench_snap2=((-1.5, 22.0, 4.2), (3.3, 41.0, 0.8)),
    line_trench_snap3=((-2.0, 34.0, 7.5), (3.3, 58.0, 0.4)),
    line_trench_end=((0.6, 60.0, 1.8), (3.8, 65.0, 1.0)),
    trench_cut=((52.3, 11.1, 0.1), (52.0, 13.3, -0.85)),
    line_road=((6.4, 32.6, 1.0), (1.0, 36.0, 1.8)),
    line_wagon=((1.8, 65.0, 2.9), (-1.9, 70.0, 1.4)),
    # STUDIO
    studio_wide=((-3.3, -2.2, 3.0), (1.0, 4.6, 0.6)),
    studio_easel=((-0.2, -0.6, 1.5), (-0.2, 3.6, 0.95)),
    studio_door=((-2.0, 0.3, 1.5), (3.2, 3.4, 1.0)),
    studio_window=((-0.5, 0.8, 1.5), (-0.8, 6.9, 1.5)),
    # CHAMBER
    chamber_wide_high=((0.0, -5.0, 8.0), (0.0, 14.0, -1.0)),
    chamber_low=((-3.0, 8.6, 1.05), (-5.27, 12.27, 0.55)),
    chamber_table=((0.1, -0.3, 1.5), (0.1, 5.6, 1.15)),
    chamber_table_night=((-0.95, -0.4, 1.45), (0.3, 13.0, 0.9)),
)
EXTRA_CAMS = {'line': ['line_station', 'line_trench_snap1', 'line_trench_snap2', 'line_trench_snap3'], 'studio': [], 'chamber': ['chamber_table_night']}
LIGHT_CAM = {('chamber_table', 'NIGHT'): 'chamber_table_night'}
CAM_NOTES = dict(
    line_close='low angle up the hero pole 1 (hook): the oversize inverted green bottle on the peg, the wire wrapped round the glass, the ladder LEANING on the pole with Morse on a rung, 3 blades in FG',
    bottle_macro='macro on the glass neck of pole 1 (shot 24): park the pulse bead on the glass with set_pulse(TG.pulse_s_at_pole(1))',
    line_wide='sb1: dirt road with the poles marching to the horizon, wheat, fences, the train far left, farm',
    line_rail='from the far side of the track: the loco side-on in the mid-ground (wheels, rods, steam chain), the pole line + wire behind it for the pulse race',
    line_station='from the road toward the station platform beyond the track (shot 27): train puffing in, 4 platform marks',
    line_trench='low alongside the furrow: plough, 2 mules, Cornell + workers, the pipe unrolling from the reel',
    line_trench_high='higher view down the furrow',
    line_trench_snap1='snap 1 of 3 (shot 14): set_trench(0.3)', line_trench_snap2='snap 2 of 3: set_trench(0.6)', line_trench_snap3='snap 3 of 3: set_trench(0.9)',
    line_trench_end='crate with the big test key + register and a wire coil at the furrow end, the wagon behind',
    trench_cut='cut face of damp soil strata with the lead pipe split open: torn cloth, copper wire, blue sparks leaking down the face',
    line_road='low from the pole side to the road: green buggy, mocker seated, mule in the shafts',
    line_wagon='raised view onto the wagon: the crate of 18 empty green bottles, spool, key crate; Morse on the bed',
    studio_wide='from the front-left corner: tall window with the road and fields, the easel, canvases, busts (crane down from the window light)',
    studio_easel='easel with the unfinished general, side table with paint jars + the oval wife portrait + the letter, jars in FG',
    studio_door='toward the door on the right wall (messenger), the stool and the easel',
    studio_window='toward the tall window: road to the horizon; coil + magnet on the sill',
    chamber_wide_high='high from the front: table with the telegraph, tiers of walnut desks with congressmen, the speaker door-screen, soft sun shafts (DAY) or candle pools (NIGHT)',
    chamber_low='desk height in front of the mocker desk: inkwell + quill in FG, the mocker big behind his desk',
    chamber_table='eye level at the front table: Morse, the mocker and the clerk behind it, telegraph coils, key and tape register',
    chamber_table_night='NIGHT start pose (auto for chamber_table / NIGHT): mocker on his stool at the left third, tape pile, the lit door-screen far behind with Morse in the doorway',
)
CONG = ['cong_%d' % i for i in range(1, 15)]
STAGING = dict(
    line_close=[('morse', 'morse_ladder')], bottle_macro=[], line_wide=[('morse', 'morse_wide')], line_rail=[('morse', 'morse_rail')],
    line_station=[('congress', 'platform_a'), ('worker', 'platform_b'), ('clerk', 'platform_c'), ('messenger', 'platform_d')],
    line_trench=[('mule', 'mule_a'), ('mule', 'mule_b'), ('cornell', 'cornell'), ('worker', 'worker_a'), ('morse', 'morse_trench')],
    line_trench_high=[('mule', 'mule_a'), ('mule', 'mule_b'), ('cornell', 'cornell'), ('worker', 'worker_a')],
    line_trench_snap1=[('mule', 'mule_a'), ('mule', 'mule_b'), ('cornell', 'cornell')], line_trench_snap2=[('mule', 'mule_a'), ('mule', 'mule_b'), ('cornell', 'cornell')], line_trench_snap3=[('mule', 'mule_a'), ('mule', 'mule_b')],
    line_trench_end=[('morse', 'morse_key'), ('worker', 'worker_key_a'), ('worker', 'worker_key_b')],
    trench_cut=[], line_road=[('mocker', 'mocker_buggy'), ('mule', 'mule_buggy')], line_wagon=[('morse', 'morse_wagon_bed')],
    studio_wide=[('morse', 'morse_easel')], studio_easel=[('morse', 'morse_easel')], studio_door=[('messenger', 'messenger_door'), ('morse', 'morse_door')], studio_window=[('morse', 'morse_window')],
    chamber_wide_high=[('morse', 'morse_table')] + [('congress', c) for c in CONG], chamber_low=[('mocker', 'mocker_desk')],
    chamber_table=[('morse', 'morse_table'), ('mocker', 'mocker_table'), ('clerk', 'clerk_table')],
    chamber_table_night=[('mocker', 'mocker_stool'), ('morse', 'morse_door')],
)
_LN = dict(poles=('bottle', 17))
PRESETS = dict(
    line_close=dict(loc='line', light='AFTER_RAIN', cam='line_close', state=dict(poles=('bottle', 17), trench=0.0, pipe=0.0, train=None)),
    bottle_macro=dict(loc='line', light='AFTER_RAIN', cam='bottle_macro', state=dict(poles=('bottle', 17), trench=0.0, pipe=0.0, train=None, pulse=('pole', 1))),
    line_wide=dict(loc='line', light='DAY', cam='line_wide', state=dict(poles=('bottle', 17), trench=0.0, pipe=0.0, train='home')),
    line_rail=dict(loc='line', light='DAY', cam='line_rail', state=dict(poles=('bottle', 17), trench=0.0, pipe=0.0, train=31.5, pulse=('y', 9.5))),
    line_trench=dict(loc='line', light='DAY', cam='line_trench', state=dict(poles=('none', 0), trench=0.5, pipe=0.45, train=None)),
    line_trench_high=dict(loc='line', light='DAY', cam='line_trench_high', state=dict(poles=('none', 0), trench=0.7, pipe=0.6, train=None)),
    line_trench_end=dict(loc='line', light='DUSK', cam='line_trench_end', state=dict(poles=('none', 0), trench=1.0, pipe=1.0, train=None)),
    trench_cut=dict(loc='line', light='DUSK', cam='trench_cut', state=dict(poles=('none', 0), trench=1.0, pipe=1.0, train=None, leak=('pipe', 1.0))),
    line_road=dict(loc='line', light='DUSK', cam='line_road', state=dict(poles=('none', 0), trench=1.0, pipe=1.0, train=None, buggy=36.0 * SC)),
    line_wagon=dict(loc='line', light='AFTER_RAIN', cam='line_wagon', state=dict(poles=('bottle', 17), trench=1.0, pipe=1.0, train=None)),
    studio_wide=dict(loc='studio', light='DAY', cam='studio_wide', state=dict(palette=False, door=0.0)),
    studio_easel=dict(loc='studio', light='DAY', cam='studio_easel', state=dict(palette=False, door=0.0)),
    studio_door=dict(loc='studio', light='DAY', cam='studio_door', state=dict(palette=False, door=0.35)),
    studio_window=dict(loc='studio', light='DAY', cam='studio_window', state=dict(palette=False, door=0.0)),
    chamber_wide_high=dict(loc='chamber', light='DAY', cam='chamber_wide_high', state=dict(tape=0.0, click=0, moneybag=False, mailsacks=False)),
    chamber_low=dict(loc='chamber', light='DAY', cam='chamber_low', state=dict(tape=0.0, click=0, moneybag=False, mailsacks=False, shafts=False)),
    chamber_table=dict(loc='chamber', light='DAY', cam='chamber_table', state=dict(tape=0.45, click=0, moneybag=False, mailsacks=False, shafts=False)),
)
LOC_PRESETS = {}
STUDIO_FG = dict(studio_wide=[('canvases', -0.8, 1.0), ('brushpot', 0.9, 1.2)], studio_easel=[('jars', -0.55, 1.05), ('brushpot', 0.5, 1.3)], studio_door=[('jars', 0.8, 1.1), ('canvases', -0.9, 1.4)], studio_window=[('jars', -0.8, 1.1), ('brushpot', 0.7, 1.4)])
FG = dict(   # foreground dressing (1-2 D from the lens): kind, metres right of the camera, metres ahead; kept to the sides, calm below y 880
    line_wide=[('grass', 0, 2.4, 45), ('crate', -1.4, 1.2), ('spool', 1.7, 2.0)],
    line_close=[('blades', 0, 0, [(-0.9, 0.8, 1.15), (0.85, 1.0, 1.35), (1.25, 0.9, 1.0)])],
    bottle_macro=[],
    line_rail=[('grass', 0, 3.0, 40), ('crate', -1.5, 1.6), ('coil', 1.5, 1.9)],
    line_station=[('crate', -1.4, 1.4), ('grass', 0, 2.6, 30)],
    line_trench=[('grass', 0, 2.4, 40), ('crate', -1.7, 1.4), ('shovel', 1.3, 1.5)],
    line_trench_high=[('grass', 0, 3.0, 30)], line_trench_snap1=[('grass', 0, 3.0, 30)], line_trench_snap2=[], line_trench_snap3=[],
    line_trench_end=[('coil', -1.6, 1.3), ('crate', 1.7, 1.5), ('grass', 0, 2.2, 30)],
    line_road=[('grass', 0, 2.4, 40), ('crate', -1.6, 1.4)],
    line_wagon=[('bottles', -1.5, 1.3), ('grass', 0, 2.0, 30)],
)

def apply_preset_state(preset):
    st = PRESETS[preset].get('state', {}); loc = PRESETS[preset]['loc']
    if loc == 'line':
        s, n = st.get('poles', ('bottle', LN.NPOLE)); set_poles(s, n); set_trench(st.get('trench', 1.0)); set_pipe(st.get('pipe', 1.0)); set_ladder(True, 0); set_ladder(preset in ('line_wide', 'line_rail', 'line_station'), 3)
        set_rain(st.get('rain', False)); set_leak('pipe', 0.0); set_leak('pole', 0.0); set_pulse(-1); set_buggy(st.get('buggy', None)); set_train(st.get('train', None))
        if st.get('leak'): set_leak(*st['leak'])
        pu = st.get('pulse')
        if pu:
            if pu[0] == 'pole': set_pulse(pulse_s_at_pole(pu[1]))
            elif pu[0] == 'y': set_pulse(pulse_s_at_y(pu[1]))
            else: set_pulse(pu)
    elif loc == 'studio':
        import tg_studio as SD; SD.apply_state(STATE, st)
    else:
        import tg_chamber as CH; CH.apply_state(STATE, st)

def pulse_s_at_pole(i):
    """pulse parameter s that puts the bead on the glass of pole i (the closed bottom, where the wire is wrapped)"""
    pts, cum = STATE['wire_pts']['bottle']; k = LN.POLES_Y[i]
    j = min(range(len(pts)), key=lambda q: abs(pts[q][1] - k) + abs(pts[q][2] - (LN.POLE_H + 0.01 + LN.BOT_TOP * LN.BS + 0.03)) * 0.01)
    return cum[j] / cum[-1]

def pulse_s_at_y(y_m):
    """pulse parameter s that puts the bead on the wire at sb-frame y (metres along the line)"""
    pts, cum = STATE['wire_pts']['bottle']; j = min(range(len(pts)), key=lambda q: abs(pts[q][1] - y_m)); return cum[j] / cum[-1]

def _cams(loc):
    return {k: _cam(*v) for k, v in CAMS_M.items() if k in LOC_PRESETS[loc] or k in EXTRA_CAMS.get(loc, [])}

def anchors():
    P = STATE['P']; loc = STATE['loc']; PR = PRESETS[STATE['preset']]
    cams = _cams(loc)
    kd = Wd(kdir(P['az'], P['el']))
    return dict(location=loc, preset=STATE['preset'], light=STATE['light'], cams=cams, cam=dict(cams[LIGHT_CAM.get((STATE['preset'], STATE['light']), PR['cam'])]), cam_name=LIGHT_CAM.get((STATE['preset'], STATE['light']), PR['cam']), cam_notes={k: CAM_NOTES.get(k, '') for k in cams},
                render=dict(samples_final=FINAL_SAMPLES.get(loc), resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), key_dir=tuple(round(v, 4) for v in kd),
                sun_elevation_deg=P['el'], heights=dict(HEIGHT), marks=dict(STATE.get('marks', {})), staging={k: [(r, STATE['marks'][m] if isinstance(m, str) else m) for r, m in STAGING.get(k, [])] for k in cams},
                floor_z=0.0, lights=[o.name for o in bpy.data.objects if o.type == 'LIGHT'])

# ============================================================================= LINE hooks
def _line_only():
    assert STATE['loc'] == 'line', 'this hook belongs to the LINE location'

def set_poles(state='bottle', count=None, frame=None):
    """state 'none' | 'bare' (wire hung straight on the wood) | 'bottle' (pole-top peg + inverted bottle neck); count = poles standing, counted from the camera end (0..16)."""
    _line_only(); n = LN.NPOLE if count is None else int(count); STATE['pole_state'] = (state, n)
    for i, p in enumerate(STATE['poles']):
        on = state != 'none' and i < n
        _show(p['body'], on, frame); _show(p['peg'], on and state == 'bottle', frame)
    for i in range(LN.NPOLE - 1):
        a = state != 'none' and i + 1 < n
        for o in STATE['spans_bottle'][i]: _setv(o, a and state == 'bottle', frame)
        for o in STATE['spans_bare'][i]: _setv(o, a and state == 'bare', frame)
    for lad in STATE.get('ladder', []): pass

def set_ladder(on=True, pole=0, frame=None):
    """show / hide the ladder leaning on pole 0 (hero ladder, near line_close) or pole 3"""
    _line_only(); idx = {0: 0, 3: 1}[pole]; _show(STATE['ladder'][idx], bool(on), frame)

def set_trench(k, plough=None, frame=None):
    """furrow length k 0..1 (y 2..62 m beside the road); the plough stands at its front (plough=None), a float 0..1 puts it elsewhere, False hides it.
    plough_marks(k) gives the mule / Cornell marks. Keyed when frame is given."""
    _line_only(); k = float(k); g = bpy.data.node_groups.get('TG_CLIP_TRENCH'); y = LN.Y0 + k * (LN.Y1 - LN.Y0)
    if g is not None: _keysock(g.nodes['clip'].outputs[0], y * SC, frame)
    pr = STATE['plough_root']; pk = k if plough in (None, True) else plough
    vis = plough is not False and 0.0 < (pk if pk is not False else 0) < 1.0
    yp = LN.Y0 + float(pk if pk else 0) * (LN.Y1 - LN.Y0); pr.location = W((LN.xc(yp) + 2.3, yp, 0.0)); _show([pr] + list(pr.children), vis, frame)
    if frame is not None: _keyxf(pr, frame)
    STATE['trench_k'] = k; STATE['marks'].update(plough_marks(k))

def set_pipe(k, frame=None):
    """lead pipe laid in the furrow, length k 0..1 (same y range as the furrow); the pipe reel + cart stand at its front while k < 1"""
    _line_only(); k = float(k); g = bpy.data.node_groups.get('TG_CLIP_PIPE'); y = LN.Y0 + k * (LN.Y1 - LN.Y0)
    if g is not None: _keysock(g.nodes['clip'].outputs[0], y * SC, frame)
    rr = STATE['reel_root']; rr.location = W((LN.xc(y) + 3.9, y + 1.3, 0.0)); _show([rr] + list(rr.children), 0.0 < k < 1.0, frame)
    if frame is not None: _keyxf(rr, frame)
    STATE['pipe_k'] = k

def set_buggy(x, frame=None):
    """open 1840s buggy on the road (heading +x), centred at world x (D) along the line, or None to hide it. The mule is a cast card (buggy_marks)."""
    _line_only()
    if 'buggy' not in STATE:
        if x is None: return
        _make_buggy()
    b = STATE['buggy']
    if x is None: _show([b['root']] + list(b['root'].children_recursive), False, frame); return
    y = x / SC if abs(x) > 400 else x                    # metres accepted too for small numbers is NOT supported: x is world D
    y = x / SC
    xr = LN.xc(y); b['root'].location = W((xr, y, 0.0))
    _show([b['root']] + list(b['root'].children_recursive), True, frame)
    for o, r in b['wheels']:
        o.rotation_euler = (0, y / r, 0)
        if frame is not None: _key(o, 'rotation_euler', frame)
    if frame is not None: _key(b['root'], 'location', frame)
    STATE['buggy_y'] = y; STATE['marks'].update(buggy_marks(y))

def _make_buggy():
    M = STATE['M']; root = bpy.data.objects.new('buggy_root', None); bpy.context.scene.collection.objects.link(root)
    mb = MB('buggy'); mb.T = frame_mat() @ Matrix.Translation((0, 0, 0)); LN.buggy(mb, M, None)
    for o in mb.finish(): o.parent = root
    ws = []
    for (ay, r) in ((-0.7, 0.55), (0.8, 0.42)):
        for sx in (-1, 1):
            o = LN.wheel_obj(M, 'bwheel', (sx * 0.78, ay, r * 1.0), r, spokes=12, wide=0.05, hub=0.06)
            o.location = W((sx * 0.78, ay, r)); o.parent = root; ws.append((o, r))
    STATE['buggy'] = dict(root=root, wheels=ws)

def set_train(x, frame=None, speed=None):
    """1840s train on the rail: x = world x (D) of the loco's front buffer (the train runs toward -x, i.e. toward the sb1 camera); None hides it.
    Wheels roll, connecting rods turn, smoke puffs billow and trail (speed D/s is taken from the previous call when omitted). Key it on every frame."""
    _line_only(); T = STATE['train']; root = T['root']
    objs = [root] + list(root.children_recursive) + T['puffs']
    if x is None: _show(objs, False, frame); return
    if isinstance(x, str): x = T['front0']
    _show(objs, True, frame)
    dx = x - T['front0']; root.location = (dx, 0, 0)
    s_m = -dx / SC                                           # metres travelled toward -x ... positive when moving toward -x relative to start (sign: loco starts at front0)
    ang = lambda r: s_m / r
    for o, r in T['wheels']:
        o.rotation_euler = (0, -ang(r), 0)
        if frame is not None: _key(o, 'rotation_euler', frame)
    th = -ang(T['drive_r'])
    for i, (o, base, sy) in enumerate(T['rods']):
        cr = T['crank'] * SC; o.location = base + Vector((cr * (math.cos(th) - 1.0), 0.0, -cr * math.sin(th)))
        if frame is not None: _key(o, 'location', frame)
    if frame is not None: _key(root, 'location', frame)
    t = (frame if frame is not None else bpy.context.scene.frame_current) / 30.0
    hist = T.get('hist'); v = speed
    if v is None:
        v = 0.0
        if hist and frame is not None and frame != hist[0]: v = (hist[1] - x) / ((frame - hist[0]) / 30.0)
        elif hist: v = hist[2]
    if frame is not None: T['hist'] = (frame, x, v)
    fun = W(T['funnel'][:]) + Vector((dx, 0, 0)); life = 4.2
    for i, o in enumerate(T['puffs']):
        a = (t * 0.45 + i / len(T['puffs'])) % 1.0
        pos = fun + Vector((abs(v) * a * life * 0.9 + 8.5 * SC * a, 1.2 * SC * a, 11.0 * SC * a ** 0.9))
        r_m = (1.0 - 0.78 * a) * min(1.0, a / 0.04) * (1.0 - max(0.0, (a - 0.94) / 0.06))        # a chain of puffs that SHRINK away from the funnel
        o.location = pos; o.scale = (max(r_m, 0.002),) * 3
        if frame is not None: _key(o, 'location', frame); _key(o, 'scale', frame)

def _rain_follow(frame=None):
    """put the rain volume under the camera, turned with its heading (computed from the camera pose at `frame`; key it per frame for moving cameras)"""
    R = STATE.get('rain'); cam = STATE.get('cam')
    if R is None or cam is None: return
    sc = bpy.context.scene
    if frame is not None: sc.frame_set(int(frame))
    bpy.context.view_layer.update(); f = cam.matrix_world.to_3x3() @ Vector((0, 0, -1)); f.z = 0
    if f.length < 1e-4: f = cam.matrix_world.to_3x3() @ Vector((0, 1, 0)); f.z = 0
    th = math.atan2(-f.x, f.y); root = R['root']; root.location = (cam.matrix_world.translation.x, cam.matrix_world.translation.y, 0.0); root.rotation_euler = (0, 0, th)
    if frame is not None: _key(root, 'location', frame); _key(root, 'rotation_euler', frame)

def set_rain(on=True, frame=None):
    """rain streaks over the whole frame (geometry, three depth layers that follow the camera and fall every frame). on: bool or 0..1 (fraction of layers). Key per frame."""
    _line_only()
    if 'rain' not in STATE and not on: return
    if 'rain' not in STATE: _make_rain()
    R = STATE['rain']; lvl = float(on); n_on = 0 if lvl <= 0 else (3 if lvl >= 0.99 else max(1, int(round(lvl * 3))))
    t = (frame if frame is not None else bpy.context.scene.frame_current)
    for i, (lay, v, Lp) in enumerate(R['layers']):
        _setv(lay, i < n_on, frame)
        lay.location.z = -((t * v) % Lp)
        if frame is not None: _key(lay, 'location', frame)
    _rain_follow(frame)

def _make_rain():
    sc = bpy.context.scene; root = bpy.data.objects.new('rain_root', None); sc.collection.objects.link(root)
    m = _emit_mat('rain', '#dfe8ff', 1.8, 0.4); layers = []
    spec = [('near', 150, 0.7, 3.2, 1.0, 0.012, 15.0), ('mid', 520, 3.0, 9.0, 0.8, 0.012, 15.0), ('far', 900, 8.0, 26.0, 1.0, 0.026, 15.0)]
    for nm, n, d0, d1, ln, r_, Lp in spec:
        mb = MB('rain_' + nm); mb.T = Matrix.Identity(4); rs = rnd(100 + len(layers))
        for rep in (0, 1):
            for i in range(n):
                d = rs.uniform(d0, d1); lat = rs.uniform(-0.62, 0.62) * d; z = rs.uniform(-1.0, Lp) + rep * Lp
                a = (lat, d, z); b = (lat + 0.1 * ln, d, z + ln)
                mb.rod(m, tuple(c * SC for c in a), tuple(c * SC for c in b), r_ * SC * 0.5, r_ * SC * 0.5, 3, caps=False)
        ob = mb.finish()[0]; ob.visible_shadow = False; ob.parent = root; ob.visible_glossy = False
        layers.append((ob, 0.33 * SC, Lp * SC))
    STATE['rain'] = dict(root=root, layers=layers)

def set_leak(where='pipe', intensity=1.0, frame=None):
    """small blue spark beads leaking: where 'pipe' (the pit pipe in trench_cut, from the torn cloth into the soil) | 'pole' (down the wet wood of poles 0 and 1);
    intensity 0..1 (0 hides). Phase follows the frame, so key it on every frame."""
    _line_only(); S = STATE.setdefault('sparks', {})
    if where not in S:
        if intensity <= 0: return
        S[where] = _make_sparks(where)
    sp = S[where]; t = (frame if frame is not None else bpy.context.scene.frame_current) / 30.0; it = float(intensity)
    for j, o in enumerate(sp['objs']):
        core, halo, fn = o
        if it <= 0: _show([core, halo], False, frame); continue
        u = (t * sp['rate'] + j / len(sp['objs']) + sp['ph'][j]) % 1.0; p, s_, vis = fn(j, u, t)
        vis = vis and it > 0.01; _show([core, halo], vis, frame)
        core.location = halo.location = p; core.scale = (s_ * (0.5 + 0.5 * it),) * 3; halo.scale = (s_ * 2.2 * (0.4 + 0.6 * it),) * 3
        if frame is not None: _keyxf(core, frame, True, False, True); _keyxf(halo, frame, True, False, True)

def _make_sparks(where):
    M = STATE['M']; core_m = _emit_mat('sparkcore', '#c8e8ff', 30.0); halo_m = _emit_mat('sparkhalo', '#4a8cff', 6.0, 0.35); rr = rnd(55); objs = []; ph = []
    n = 18 if where == 'pipe' else 12
    for j in range(n):
        for nm, m_ in (('c', core_m), ('h', halo_m)):
            mb = MB('spk_%s%d%s' % (where, j, nm)); mb.T = Matrix.Identity(4); mb.ell(m_, (0, 0, 0), ((0.026 if where == 'pole' else 0.05) * SC,) * 3, (10, 6)); o = mb.finish()[0]; o.visible_shadow = False
            if nm == 'c': core = o
            else: halo = o
        ph.append(rr.random());
        objs.append([core, halo, None])
    if where == 'pipe':
        pit = STATE['pit']; cx, cy = pit['c']; fy = pit['face_y']; z0 = pit['z0']; x0, x1 = pit['w']
        def fn(j, u, t, cx=cx, fy=fy, z0=z0, x0=x0, x1=x1):
            sg = -1 if j % 2 else 1; xs = x0 + 0.2 + (x1 - x0 - 0.4) * ((j * 0.37) % 1.0)
            p = W((xs + sg * 0.5 * u * u + 0.05 * math.sin(9 * u + j), fy - 0.2 - 0.05 * u, z0 + 0.12 - 1.05 * u + 0.1 * math.sin(5 * u + j)))
            return p, 1.0 - 0.45 * u, u < 0.93
        rate = 0.45
    else:
        def fn(j, u, t):
            pi = 1 + j % 2; y = LN.POLES_Y[pi]; x = LN.px(y) + 0.03; z = LN.POLE_H * (1.0 - u) ** 1.0
            rad = 0.14 - (0.14 - 0.085) * z / LN.POLE_H + 0.035; a = j * 1.1 + 7.0 * u
            return W((x + rad * math.cos(a), y + rad * math.sin(a), z)), 1.0, z > 0.12
        rate = 0.3
    for j, o in enumerate(objs): o[2] = fn
    return dict(objs=[tuple(o) for o in objs], rate=rate, ph=ph)

def set_pulse(s, frame=None):
    """glowing bead + short trail travelling along the wire: s 0..1 over the whole line (over every bottle neck in 'bottle' state); s < 0 hides it."""
    _line_only()
    if 'pulse' not in STATE:
        if s < 0: return
        _make_pulse()
    Pz = STATE['pulse']; st = STATE.get('pole_state', ('bottle', LN.NPOLE))[0]; st = st if st in ('bottle', 'bare') else 'bottle'
    pts, cum = STATE['wire_pts'][st]; tot = cum[-1]
    for k, (core, halo, lag) in enumerate(Pz):
        ss = s - lag
        if s < 0 or ss < 0 or ss > 1: _show([core, halo], False, frame); continue
        d = ss * tot; i = int(np.searchsorted(cum, d)); i = max(1, min(i, len(cum) - 1)); u = (d - cum[i - 1]) / max(1e-6, cum[i] - cum[i - 1])
        p = Vector(pts[i - 1]).lerp(Vector(pts[i]), u); pw = W(p); _show([core, halo], True, frame)
        core.location = halo.location = pw; sc_ = 1.0 - 0.09 * k; core.scale = (sc_,) * 3; halo.scale = (sc_,) * 3
        if frame is not None: _keyxf(core, frame, True, False, True); _keyxf(halo, frame, True, False, True)

def _glow_mat(name, hexcol, k, power=1.6):
    """soft glow: emission whose opacity is 1 at the centre and falls to 0 at the silhouette"""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    em.inputs['Color'].default_value = hexc(hexcol); em.inputs['Strength'].default_value = k
    L(K.cos_facing(nt, power), mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface']); MATS[name] = m; return m

def _make_pulse():
    core_m = _emit_mat('pulsecore', '#fff6d0', 90.0); halo_m = _glow_mat('pulsehalo', '#ffd890', 3.2, 3.0); halo2_m = _glow_mat('pulsehalo2', '#78b8ff', 2.0, 3.0); L = []
    for k in range(10):
        r = 0.032 * (1.0 - 0.07 * k) * SC
        mb = MB('pulse_c%d' % k); mb.T = Matrix.Identity(4); mb.ell(core_m, (0, 0, 0), (r,) * 3, (12, 8)); c = mb.finish()[0]
        mb = MB('pulse_h%d' % k); mb.T = Matrix.Identity(4); mb.ell(halo_m if k < 4 else halo2_m, (0, 0, 0), (r * 5.0,) * 3, (14, 10)); h = mb.finish()[0]
        for o in (c, h): o.visible_shadow = False; o.visible_glossy = False
        L.append((c, h, 0.0036 * k))
    STATE['pulse'] = L

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_render(specs=None, quality='final', outdir=None, actors=True):
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for spec in (specs or list(PRESETS)):
        parts = spec.split(':'); pr = parts[0]; lt = parts[1] if len(parts) > 1 and parts[1] else None
        A = build(None, pr, light=lt); sc = bpy.context.scene; setup_render(sc, quality)
        nm = A['cam_name']; cs = A['cams'][nm]; make_camera(cs)
        if actors: stage_placeholders(A, nm, cs['loc'])
        bpy.context.view_layer.update(); hp = head_pixels(nm); tag = '%s_%s' % (pr, A['light'])
        w, c = render(os.path.join(outdir, tag + '.png')); res[tag] = (round(w, 1), round(c, 1), hp)
        print('%s %s: %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, tag, w, c, _load()), flush=True)
    return res

LOC_PRESETS.update({l: [k for k, v in PRESETS.items() if v['loc'] == l] for l in ('line', 'studio', 'chamber')})
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('final', 'stills'): cli_render(arg or None, 'final' if cmd == 'final' else 'preview')
    else: print(__doc__)
