"""EP.3-4 sets of ช่างเชื่อมสายฟ้า remake (bpy 5.3, Cycles CPU), same toon light model as hosp3d / soi3d.
layout 'nursery': the community hospital's newborn room (ห้องเด็กอ่อน) built on the hosp3d ward shell (windows, blinds, ceiling, nurse
  station) with three incubators across the room (y = INC_Y) instead of beds, bassinets along the walls, the nursery sign.
layout 'ctrl'   : the hospital's power room: concrete box x -2.6..2.6, y 0..6, ceiling 3.0; four switchboards on the far wall, the dead
  generator, the main feeder cable dropping from the ceiling to a breaker with its end hanging free, a puddle, a door (near-left) to the rain.
Presets: 'dark' (storm night, power out: blue window light + red emergency lamp), 'lit' (power back, storm night outside), 'morning' (sun).
    import nurs3d; A = nurs3d.build('dark', layout='nursery'); nurs3d.set_incubator(i, 0..1); nurs3d.set_power(on)
CLI: python3 nurs3d.py stills <preset> <layout> [L]  -> out_nurs/<layout>_<preset>.png"""
import os, sys, math, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import office3d as S
import hosp3d as H
import tex_hosp, tex_props
MB = S.MB
OUT = os.path.join(HERE, 'out_nurs')
DAY = dict(H.PRESETS['day'])
PRESETS = {
    'morning': dict(DAY),
    'dark': dict(DAY, shade=(0.050, 0.055, 0.135), key=(0.30, 0.40, 0.80), lift=(0.004, 0.004, 0.012), key_dir=(-0.78, -0.26, -0.40), sun_angle=1.5,
                 tubes=0.0, ext=0.035, screens=0.4, monitor=0.0, shafts=0.0, gain=0.5, grade_saturation=1.1, grade_offset=(0.002, 0.002, 0.008)),
    'lit': dict(DAY, shade=(0.17, 0.165, 0.33), key=(1.25, 1.18, 1.05), lift=(0.010, 0.010, 0.022), key_dir=(0.15, 0.25, -1.0), sun_angle=8.0,
                tubes=2.4, ext=0.05, shafts=0.0, gain=0.45),
}
INC_X = (-1.75, 0.0, 1.75); INC_Y = 4.2
A = {}; INC = []; POWER = {}

def _sun(P, lc):
    sd = bpy.data.lights.new('key_sun', 'SUN'); kmax = max(P['key']); sd.energy = math.pi * kmax; sd.color = tuple(c / kmax for c in P['key'])
    sd.angle = math.radians(P['sun_angle']); sd.use_shadow = True; so = bpy.data.objects.new('key_sun', sd); lc.objects.link(so)
    so.rotation_euler = Vector(P['key_dir']).normalized().to_track_quat('-Z', 'Y').to_euler(); return so

def _world(scene):
    w = bpy.data.worlds.new('nurs_world'); scene.world = w; w.use_nodes = True; bg = w.node_tree.nodes.get('Background')
    if bg: bg.inputs['Color'].default_value = (0.01, 0.01, 0.03, 1); bg.inputs['Strength'].default_value = 0.0
    w.cycles.sampling_method = 'NONE'

def _point(lc, name, loc, color, energy, size=0.2):
    ld = bpy.data.lights.new(name, 'POINT'); ld.energy = energy; ld.color = color; ld.shadow_soft_size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; lc.objects.link(ob); return ob

def inc_mats(i):
    scr = H.screen_mat('inc_screen_%d' % i, tex_props.os.path.join(HERE, 'props_tex', 'incub_off.png'), 1.6)
    heat = S.mat_emit('INC_heat_%d' % i, '#ffb060', strength=0.0)
    glow = bpy.data.materials.new('INC_glow_%d' % i); glow.use_nodes = True; nt = glow.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    L = nt.links.new; out = nt.nodes.new('ShaderNodeOutputMaterial'); emi = nt.nodes.new('ShaderNodeEmission'); emi.name = 'GLOW'; tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    mx = nt.nodes.new('ShaderNodeMixShader'); mx.name = 'MIX'; mx.inputs['Fac'].default_value = 0.1
    emi.inputs['Color'].default_value = (*S.hex_lin('#bfe6ff'), 1); emi.inputs['Strength'].default_value = 0.5
    L(tr.outputs['BSDF'], mx.inputs[1]); L(emi.outputs['Emission'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface']); glow.cycles.emission_sampling = 'NONE'
    return scr, heat, glow

def incubator(coll, i, c):
    """Infant incubator on its cart, centred at c (floor), facing -y. The hood is acrylic (camera-transparent glow)."""
    x, y = c[0], c[1]; mb = MB(); flat = H.flat; scr, heat, glow = inc_mats(i)
    cream, grey, dark = flat('#ece6d6', 0.85), flat('#b8bec6', 0.85), flat('#2a2c32')
    mb.box((x - 0.45, y - 0.28, 0.16), (x + 0.45, y + 0.28, 0.74), cream, mats={'front': flat('#e2dccb', 0.85)})
    for dz in (0.34, 0.54): mb.box((x - 0.42, y - 0.285, dz), (x + 0.42, y - 0.28, dz + 0.012), grey)                      # drawer lines
    mb.box((x - 0.4, y - 0.24, 0.05), (x + 0.4, y + 0.24, 0.16), grey)
    for dx in (-0.36, 0.36):
        for dy in (-0.2, 0.2): mb.sphere((x + dx, y + dy, 0.05), 0.05, dark, 8, 5)
    mb.box((x - 0.44, y - 0.27, 0.74), (x + 0.44, y + 0.27, 0.80), grey)
    mb.box((x - 0.38, y - 0.2, 0.80), (x + 0.38, y + 0.2, 0.86), flat('#f8f6f0', 0.85))                                    # mattress
    # control head on a post at the right end: screen + knobs
    mb.box((x + 0.45, y - 0.08, 0.6), (x + 0.53, y + 0.08, 1.35), grey); mb.box((x + 0.36, y - 0.16, 1.3), (x + 0.62, y + 0.16, 1.52), cream)
    mb.quad((x + 0.39, y - 0.165, 1.33), (0.2, 0, 0), (0, 0, 0.16), scr)
    mb.box((x - 0.34, y - 0.05, 1.27), (x + 0.3, y + 0.05, 1.3), heat)                                                       # warmer bar under the lid
    mb.frustum((x - 0.38, y, 1.275), (x + 0.36, y, 1.275), 0.012, 0.012, grey, seg=6)
    ob = mb.obj('incubator_%d' % i, coll); S.no_bounce(ob)
    hm = MB(); x0, x1, y0, y1, z0, z1 = x - 0.42, x + 0.42, y - 0.25, y + 0.25, 0.80, 1.24
    hm.box((x0, y0, z0), (x1, y1, z1), glow)
    ob2 = hm.obj('inc_hood_%d' % i, coll); ob2.visible_shadow = False; S.no_bounce(ob2)
    fm = MB(); fr = flat('#f4f4f2', 0.9)                                                                                       # hood edges + arm ports
    for (a, b) in (((x0, y0, z1), (x1, y0, z1)), ((x0, y1, z1), (x1, y1, z1)), ((x0, y0, z1), (x0, y1, z1)), ((x1, y0, z1), (x1, y1, z1)),
                   ((x0, y0, z0), (x0, y0, z1)), ((x1, y0, z0), (x1, y0, z1)), ((x0, y1, z0), (x0, y1, z1)), ((x1, y1, z0), (x1, y1, z1))):
        fm.frustum(a, b, 0.012, 0.012, fr, seg=6)
    for dx in (-0.2, 0.2):
        cc = Vector((x + dx, y0 - 0.002, 1.02)); pts = [cc + Vector((0.075 * math.cos(2 * math.pi * k / 16), 0, 0.075 * math.sin(2 * math.pi * k / 16))) for k in range(17)]
        for p, q in zip(pts[:-1], pts[1:]): fm.frustum(tuple(p), tuple(q), 0.012, 0.012, fr, seg=5)
    fm.obj('inc_frame_%d' % i, coll); INC.append(dict(scr=scr, heat=heat, glow=glow, baby=(x - 0.05, y, 0.86)))

def set_incubator(i, level):
    """0 dead and cold (red LOW, no warmer), 1 warm (green 36.8, warmer glow, hood tinted warm)."""
    d = INC[i]; tex = d['scr'].node_tree.nodes['SCREEN_TEX']
    tex.image = bpy.data.images.load(os.path.join(HERE, 'props_tex', 'incub_on.png' if level > 0.5 else 'incub_off.png'), check_existing=True)
    d['heat'].node_tree.nodes['Emission'].inputs['Strength'].default_value = 6.0 * level
    g = d['glow'].node_tree.nodes; g['GLOW'].inputs['Color'].default_value = (*S.hex_lin('#ffd9a8' if level > 0.5 else '#bfe6ff'), 1)
    g['GLOW'].inputs['Strength'].default_value = 0.5 + 1.6 * level; g['MIX'].inputs['Fac'].default_value = 0.1 + 0.08 * level

def bassinet(mb, c, flat):
    x, y = c; mb.box((x - 0.3, y - 0.22, 0.6), (x + 0.3, y + 0.22, 0.95), H.flat('#f0eadc', 0.85)); mb.box((x - 0.26, y - 0.18, 0.95), (x + 0.26, y + 0.18, 0.97), H.flat('#bfe0f8', 0.85))
    for dx in (-0.25, 0.25): mb.frustum((x + dx, y, 0.0), (x + dx, y, 0.6), 0.02, 0.02, H.flat('#b8bec6', 0.85), seg=6)
    mb.box((x - 0.3, y - 0.05, 0.0), (x + 0.3, y + 0.05, 0.04), H.flat('#b8bec6', 0.85))

def build_nursery(preset, scene):
    P = H.P; P.clear(); P.update(PRESETS[preset]); S.STATE.clear(); S.STATE['P'] = P; H.M.clear(); H.A.clear(); H._MEAN.clear()
    H.TX.clear(); H.TX.update(tex_hosp.build_all()); tex_props.build_all()
    coll = S._coll('SET', scene); S._wipe(coll); lc = S._coll('LIGHTS', scene); S._wipe(lc)
    H.materials(); r = random.Random(20261115)
    G = dict(coll=coll, room=MB(), alpha=MB(), blinds=MB(), beds=MB(), props=MB(), curtains=MB())
    H.room(G)
    for s in (-1, 1):
        for k, wy in enumerate(H.WIN_Y): H.blinds(G, s, wy, [1.0, 1.4, 1.0, 1.25, 1.6][k] if s < 0 else 2.2, 30 if s < 0 else 6)
    H.rails(G); H.ceiling_stuff(G); A['station'] = H.station(G, r)
    for k, (bx, by) in enumerate(((-2.9, 7.0), (-2.9, 8.6), (2.9, 7.0), (2.9, 8.6), (-2.9, 1.6), (2.9, 1.6))): bassinet(G['props'], (bx, by), H.flat)
    for nm in ('room', 'alpha', 'blinds', 'beds', 'props', 'curtains'): G[nm].obj('hosp_' + nm, coll)
    for ob in coll.objects: S.no_bounce(ob)
    INC.clear()
    for i, x in enumerate(INC_X): incubator(coll, i, (x, INC_Y))
    sign = MB(); sign.quad((-1.45, 14.86, 2.5), (2.9, 0, 0), (0, 0, 0.725), S.mat_lit('NS_sign', image=os.path.join(HERE, 'props_tex', 'nurs_sign.png'), gain=0.9 * P['gain'] * 2, shade_mul=1.2, form=(0, 0, 0.2)))
    sign.obj('nurs_sign', coll)
    for ob in coll.objects: S.no_bounce(ob)
    for nm in ('hosp_tubes',):
        if nm in bpy.data.objects: bpy.data.objects[nm].visible_shadow = False
    _sun(P, lc); _world(scene)
    if preset == 'dark':
        POWER['emerg'] = _point(lc, 'emerg', (0.0, 14.6, 3.2), (1.0, 0.2, 0.15), 120.0, 0.3)
        mb = MB(); mb.box((-0.25, 14.85, 3.05), (0.25, 14.98, 3.25), S.mat_emit('NS_emerg', '#ff3a2a', strength=6.0)); mb.obj('emerg_lamp', coll)
    for i in range(3): set_incubator(i, 0.0 if preset == 'dark' else 1.0)
    A.update(incubators=[dict(index=i, center=(x, INC_Y, 0.0), baby=INC[i]['baby'], screen=(x + 0.49, INC_Y - 0.17, 1.41)) for i, x in enumerate(INC_X)],
             nurse_mark=(2.8, 4.6, 0.0), hero_mark=(0.0, 2.6, 0.0), door_mark=(0.0, -1.6, 0.0), wall_poster=(-3.47, 3.0, 1.5),
             key_dir=tuple(Vector(P['key_dir']).normalized()), room=dict(x=(-H.XW, H.XW), y=(H.Y0, H.Y1), ceiling=H.HC))
    return A

# ----------------------------------------------------------------------------- the power room
def build_ctrl(preset, scene):
    P = dict(PRESETS[preset])
    if preset == 'lit': P.update(key=(0.5, 0.48, 0.45), shade=(0.12, 0.12, 0.2))
    S.STATE.clear(); S.STATE['P'] = P; H.P.clear(); H.P.update(P); tex_props.build_all()
    coll = S._coll('SET', scene); S._wipe(coll); lc = S._coll('LIGHTS', scene); S._wipe(lc)
    TXP = lambda k: os.path.join(HERE, 'props_tex', k + '.png')
    def lit(n, img=None, color='#808080', gain=1.0, shade=1.0): return S.mat_lit('CT_' + n, color=color, image=img and TXP(img), gain=gain * P['gain'] * 1.6, shade_mul=shade, form=(0.05, 0.0, 0.2))
    X0, X1, Y0, Y1, HC = -2.6, 2.6, 0.0, 6.0, 3.0; mb = MB(); conc = lit('conc', color='#8f948e'); floor = lit('floor', color='#6c706c'); ceil = lit('ceil', color='#7c807c', shade=0.8)
    mb.box((X0 - 0.2, Y0 - 0.2, -0.1), (X1 + 0.2, Y1 + 0.2, 0.0), floor)
    mb.box((X0 - 0.2, Y1, 0), (X1 + 0.2, Y1 + 0.2, HC), conc); mb.box((X0 - 0.2, Y0, 0), (X0, Y1, HC), conc); mb.box((X1, Y0, 0), (X1 + 0.2, Y1, HC), conc)
    mb.box((X0 - 0.2, Y0 - 0.2, HC), (X1 + 0.2, Y1 + 0.2, HC + 0.1), ceil)
    mb.box((X0, Y0 - 0.2, 0), (-1.0, Y0, HC), conc); mb.box((0.0, Y0 - 0.2, 0), (X1, Y0, HC), conc); mb.box((-1.0, Y0 - 0.2, 2.2), (0.0, Y0, HC), conc)   # near wall + doorway x -1..0
    mb.box((X0, Y1 - 0.02, 0.0), (X1, Y1, 0.12), lit('skirt', color='#4a4e4a'))
    # four switchboards on the far wall: each shows one quarter of the panel artwork
    pan = TXP('ctrl_panel'); pm = S.mat_lit('CT_panel', image=pan, gain=P['gain'] * 1.7, shade_mul=1.1, form=(0.05, 0.0, 0.2)); side = lit('cab', color='#8a948c')
    for k in range(4):
        x = -2.2 + k * 1.1; mb.box((x, Y1 - 0.55, 0.05), (x + 1.0, Y1 - 0.02, 2.2), side)
        mb.quad((x, Y1 - 0.552, 0.05), (1.0, 0, 0), (0, 0, 2.15), pm, uv=(k / 4, 0, (k + 1) / 4, 1))
    gm = S.mat_lit('CT_gen', image=TXP('ctrl_gen'), gain=P['gain'] * 1.7, form=(0.05, 0, 0.2))            # dead generator on the right wall
    mb.box((1.6, 1.4, 0.0), (2.5, 3.4, 1.4), lit('genbody', color='#3c6e48'), mats={'left': gm}); mb.frustum((2.0, 3.0, 1.4), (2.0, 3.0, 2.2), 0.08, 0.08, lit('exh', color='#4a4a4e'), seg=10)
    mb.quad((-0.95, Y0 - 0.21, 2.25), (0.9, 0, 0), (0, 0, 0.45), S.mat_lit('CT_sign', image=TXP('ctrl_sign'), gain=P['gain'] * 1.8, form=(0, 0, 0.2)))   # outside sign (seen from the corridor)
    # the main feeder: conduit across the ceiling, down the left wall to a breaker box, its cable end hanging free
    cm = lit('cable', color='#1c1c20'); yel = lit('tray', color='#c8a030')
    mb.box((X0 + 0.05, 0.4, HC - 0.25), (X0 + 0.45, Y1 - 0.1, HC - 0.2), yel)
    mb.box((X0 + 0.02, 2.3, 1.0), (X0 + 0.42, 3.3, 2.1), lit('brk', color='#9aa29c'), mats={'right': lit('brkf', color='#b8beb6')})
    for k in range(3): mb.frustum((X0 + 0.15 + k * 0.1, 2.8, 2.1), (X0 + 0.15 + k * 0.1, 2.8, HC - 0.22), 0.035, 0.035, cm, seg=8)
    end = Vector((X0 + 0.9, 2.55, 1.15)); pts = [Vector((X0 + 0.42, 2.6, 1.35)), Vector((X0 + 0.65, 2.58, 1.05)), Vector((X0 + 0.8, 2.56, 1.0)), end]
    for a, b in zip(pts[:-1], pts[1:]): mb.frustum(tuple(a), tuple(b), 0.045, 0.045, cm, seg=10)
    mb.frustum(tuple(end), tuple(end + Vector((0.12, -0.02, 0.05))), 0.03, 0.03, lit('cu', color='#e08a40'), seg=8)
    # puddle (from the leak) on the floor
    pud = S.mat_emit('CT_puddle', '#1a2848', strength=0.55); r = random.Random(7)
    pts2 = [Vector((0.2 + (1.0 + 0.25 * r.uniform(-1, 1)) * math.cos(2 * math.pi * k / 20), 2.4 + (0.75 + 0.2 * r.uniform(-1, 1)) * math.sin(2 * math.pi * k / 20), 0.004)) for k in range(20)]
    mb.face(pts2, pud); hl = S.mat_emit('CT_puddle_hl', '#9ec4ff', strength=1.4)
    for k in range(4): a = Vector((0.0 + 0.25 * k, 2.1 + 0.15 * k, 0.006)); mb.face([a, a + Vector((0.35, 0.05, 0)), a + Vector((0.35, 0.09, 0)), a + Vector((0, 0.04, 0))], hl)
    mb.frustum((0.6, 2.6, HC), (0.6, 2.6, HC - 0.02), 0.1, 0.1, lit('stain', color='#4a4e4a'), seg=10)
    # fluorescent fittings + emergency lamp
    tube_m = S.mat_emit('CT_tube', '#f2f8ff', strength=3.0 if preset != 'dark' else 0.0)
    for y in (1.5, 4.0): mb.box((-0.7, y - 0.06, HC - 0.08), (0.7, y + 0.06, HC - 0.02), lit('fit', color='#d8dcd8')); mb.box((-0.65, y - 0.03, HC - 0.1), (0.65, y + 0.03, HC - 0.08), tube_m)
    mb.box((1.4, Y1 - 0.15, 2.5), (1.8, Y1 - 0.02, 2.7), S.mat_emit('CT_emerg', '#ff3a2a', strength=6.0 if preset == 'dark' else 0.6))
    ob = mb.obj('ctrl_room', coll); S.no_bounce(ob)
    _sun(P, lc); _world(scene)
    if preset == 'dark':
        POWER['emerg'] = _point(lc, 'emerg', (1.6, Y1 - 0.6, 2.4), (1.0, 0.18, 0.12), 160.0, 0.2)
        POWER['door'] = _point(lc, 'door_blue', (-0.5, -1.2, 2.0), (0.55, 0.7, 1.0), 120.0, 0.6)
    else:
        for k, y in enumerate((1.5, 4.0)): _point(lc, 'tube%d' % k, (0.0, y, HC - 0.3), (0.95, 0.98, 1.0), 45.0, 0.6)
    A.update(hero_mark=(-1.2, 2.5, 0.0), cable_end=tuple(end), door_mark=(-0.5, -0.3, 0.0), kim_door=(-0.5, -0.9, 0.0), puddle=(0.2, 2.4, 0.0),
             key_dir=tuple(Vector(P['key_dir']).normalized()), room=dict(x=(X0, X1), y=(Y0, Y1), ceiling=HC))
    return A

def build(preset='dark', layout='nursery', clear=True):
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene; A.clear(); POWER.clear()
    out = build_nursery(preset, scene) if layout == 'nursery' else build_ctrl(preset, scene)
    S.setup_render(scene, 'fast'); scene.cycles.samples = 12; scene.render.use_persistent_data = False; S.setup_grade(scene, bloom=True)
    scene.cycles.transparent_max_bounces = 12
    return out

def set_power(on=True):
    if 'emerg' in POWER: POWER['emerg'].data.energy = 0.0 if on else 140.0

if __name__ == '__main__':
    import time
    a = sys.argv[1:]; preset = a[1] if len(a) > 1 else 'dark'; layout = a[2] if len(a) > 2 else 'nursery'; land = 'L' in a[3:]
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); AA = build(preset, layout); scene = bpy.context.scene
    scene.render.resolution_x, scene.render.resolution_y = (1280, 720) if land else (720, 1280)
    if os.environ.get('LT_PREVIEW'): scene.render.resolution_percentage = 50; scene.cycles.samples = 8
    cams = dict(nursery=[dict(loc=(0.0, -1.2, 1.7), look_at=(0.0, 6.0, 0.9), lens=20), dict(loc=(-0.9, 2.9, 1.35), look_at=(0.0, 4.2, 1.0), lens=24)],
                ctrl=[dict(loc=(0.6, 0.4, 1.7), look_at=(-0.4, 5.0, 1.1), lens=18), dict(loc=(1.2, 1.2, 1.4), look_at=(-1.6, 2.6, 1.1), lens=22)])[layout]
    for k, c in enumerate(cams):
        cam = S.make_camera(c, name='cam%d' % k)
        if land: cam.data.sensor_fit = 'VERTICAL'; cam.data.sensor_height = 36.0 * 720 / 1280 * 1.15
        scene.camera = cam; scene.render.filepath = os.path.join(OUT, f'{layout}_{preset}_{k}.png'); bpy.ops.render.render(write_still=True)
    json.dump(AA, open(os.path.join(OUT, f'anchors_{layout}.json'), 'w'), indent=1, default=list)
    print('done', round(time.time() - t0, 1))
