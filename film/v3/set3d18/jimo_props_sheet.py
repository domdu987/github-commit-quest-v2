"""jimo_props_sheet.py : 360x640 night props sheet (reed bundle, 3 pots, helmet, chariot upright and tumbled) -> set_work/props_r8/props_sheet.png
    python3 jimo_props_sheet.py [light]"""
import sys, os, math
import jimo as J
from mathutils import Vector as V
import bpy
OUT = os.path.join(J.WORK, 'props_r8'); os.makedirs(OUT, exist_ok=True)

def scene(light='NIGHT'):
    A = J.build('yan_camp', 'yan_camp', light)
    SET = J.STATE['SET']; keep = ('sky', 'dome')
    for ob in list(SET.objects):
        mo = [o for o, off in J.STATE.get('moon_objs', [])]
        if ob not in mo and not any(k in ob.name for k in keep): bpy.data.objects.remove(ob, do_unlink=True)
    for ob in list(J.STATE['LIGHTS'].objects):
        if ob.type == 'LIGHT' and ob.data.type == 'POINT': bpy.data.objects.remove(ob, do_unlink=True)
    for k in ('fires', 'flame_cards', 'torches'): J.STATE[k] = []
    M = J.STATE['M']; mb = J.Banks()('g'); J.flat(mb, V((-60, -60, 0)), V((120, 0, 0)), V((0, 120, 0)), M['bank'], (-60 / 8, -60 / 8, 60 / 8, 60 / 8)); ob = mb.obj('sheet_ground', SET); J.no_bounce(ob)
    li = bpy.data.lights.new('warm', 'POINT'); li.energy = 5000; li.color = (1.0, 0.62, 0.3); li.shadow_soft_size = 0.6
    lo = bpy.data.objects.new('warm', li); J.STATE['LIGHTS'].objects.link(lo); lo.location = (-3.0, -7.0, 6.0)
    return A

def clear():
    for ob in list(J.STATE['SET'].objects):
        if ob.name.startswith('prop_'): bpy.data.objects.remove(ob, do_unlink=True)
    for ob in list(bpy.data.objects):
        if ob.name.startswith('prop_') and ob.type == 'EMPTY': bpy.data.objects.remove(ob, do_unlink=True)
    J.STATE['props'] = []; J.STATE['chariots'] = []

def shot(name, loc, look, lens, light='NIGHT', draft=False):
    cam = J.make_camera(dict(loc=loc, look_at=look, lens=lens)); sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 360, 640; sc.render.resolution_percentage = 100; sc.cycles.samples = 24
    bpy.context.view_layer.update(); w, c = J.T.render(os.path.join(OUT, name + '.png')); print(name, round(w, 1), 's'); return os.path.join(OUT, name + '.png')

if __name__ == '__main__':
    light = sys.argv[1] if len(sys.argv) > 1 else 'NIGHT'
    scene(light); P = J
    which = sys.argv[2] if len(sys.argv) > 2 else 'ab'
    if 'a' in which:
        P.prop_reed_bundle((-1.5, -3.2, 0.34), (0, 0, 0.35))
        P.prop_helmet((1.7, -3.0, 0.0), (0, 0, -0.5), scale=1.0)
        for i, k in enumerate(('jar', 'bowl', 'pot')): P.prop_pot((-2.0 + 2.1 * i, 0.4, 0.0), (0, 0, 0.4 * i), kind=k)
        shot('props_a', (0.0, -8.5, 5.2), (0.0, -0.8, 0.5), 30, light)
    if 'b' in which:
        clear()
        P.prop_chariot((-1.0, -1.5, 0), (0, 0, 0.35), 0.0, scale=0.5)
        P.prop_chariot((-2.0, 4.5, 0), (0, 0, 0.25), 0.8, scale=0.5)
        shot('props_b', (0.0, -9.5, 7.5), (-0.6, 1.4, 0.5), 30, light)
    if 'c' in which:
        clear()
        P.prop_helmet((-0.9, 0.0, 0.0), (0, 0, 3.6)); P.prop_helmet((0.9, 0.2, 0.0), (0, 0, 0.5)); 
        shot('props_c', (0.0, -4.5, 1.6), (0.0, 0.0, 0.5), 30, light)
    from PIL import Image
    tiles = [Image.open(os.path.join(OUT, 'props_%s.png' % k)).convert('RGB') for k in 'abc' if os.path.exists(os.path.join(OUT, 'props_%s.png' % k))]
    sh = Image.new('RGB', (360 * len(tiles) + 8 * (len(tiles) - 1), 640), (16, 16, 24))
    for i, im in enumerate(tiles): sh.paste(im, (i * 368, 0))
    sh.save(os.path.join(OUT, 'props_sheet.png')); print('sheet', os.path.join(OUT, 'props_sheet.png'))
