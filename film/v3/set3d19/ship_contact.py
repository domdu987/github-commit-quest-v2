#!/usr/bin/env python3
"""ship_contact.py : standalone tester of the SHIP location (h19_ship.py).  One final 720x1280 tile per preset x light (grey 3 D placeholder cards at the marks,
cyan line at y 880), ship_contact.jpg, ship_cost.txt (CPU s of the render call per tile, 2 threads), ship_hue.txt (cast-shadow hue 225-265, magenta <= 10 %).
usage:  python3 ship_contact.py [draft] [--only preset[:LIGHT],...] [--nohue]      (draft = 360x640 quick look)"""
import os, sys, math, time, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import bpy
from mathutils import Vector
from PIL import Image, ImageDraw, ImageFont
import h19_kit as K
import h19_ship as SH

WORK = os.path.join(HERE, 'ship_work'); FINAL = os.path.join(WORK, 'final')
LIGHTS = SH.LIGHT_NAMES
PRESETS = SH.PRESET_NAMES
D3 = 3.0

def card(name, loc, face_to, root=None):
    import bmesh
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0, matrix=__import__('mathutils').Matrix.Diagonal((1.0, 0.05, D3, 1.0)) @ __import__('mathutils').Matrix.Translation((0, 0, 0.5)))
    bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=8, radius=0.5, matrix=__import__('mathutils').Matrix.Translation((0, 0, D3 * 0.9)) @ __import__('mathutils').Matrix.Diagonal((0.5, 0.06, 0.5, 1.0)))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    m = K.mat('card_grey', '#9a9ca8'); me.materials.append(m)
    ob = bpy.data.objects.new('actor_' + name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = loc; v = Vector(face_to) - Vector(loc); ob.rotation_euler = (0, 0, math.atan2(v.x, -v.y))
    if root is not None:
        bpy.context.view_layer.update(); ob.parent = root; ob.matrix_parent_inverse = root.matrix_world.inverted()
    return ob

def render_tile(preset, light, quality, out_png, hue=True):
    bpy.ops.wm.read_factory_settings(use_empty=True); K.MATS.clear(); K.STATE.clear()
    t0 = time.time(); A = SH.build_ship(None, preset, light); tb = time.time() - t0
    sc = bpy.context.scene
    K.setup_render(sc, quality)
    try: K.setup_grade(sc, K.STATE.get('grade_sat', 1.08))
    except Exception as e: print('grade skipped', e)
    cam = K.make_camera(A['cams'][A['cam']])
    for nm, p in A['marks'].items():
        ob = bpy.data.objects.get('mark_' + nm)
        card(nm, p, cam.location, ob.parent if ob is not None else None)
    if light == 'STORM_DUSK' and preset == 'ship_rocks': SH.set_rain(True)
    wall, cpu = K.render(out_png)
    res = dict(preset=preset, light=light, build=round(tb, 1), wall=round(wall, 1), cpu=round(cpu, 1))
    if hue and quality == 'final':
        try: res['hue'] = K.measure_hue(out_png)
        except Exception as e: res['hue'] = dict(err=str(e))
    return res

def finish_png(png, quality):
    im = Image.open(png).convert('RGB'); d = ImageDraw.Draw(im); y = 880 if quality == 'final' else 440
    d.line([(0, y), (im.width, y)], fill=(0, 255, 255), width=2 if quality == 'final' else 1); im.save(png)

def main():
    args = sys.argv[1:]; draft = 'draft' in args; hue = '--nohue' not in args
    only = None
    if '--only' in args: only = args[args.index('--only') + 1].split(',')
    q = 'preview' if draft else 'final'
    os.makedirs(FINAL, exist_ok=True)
    combos = [(p, l) for p in PRESETS for l in LIGHTS]
    if only: combos = [(p, l) for (p, l) in combos if p in only or ('%s:%s' % (p, l)) in only]
    results = []
    for (p, l) in combos:
        out = os.path.join(FINAL, '%s_%s%s.png' % (p, l, '_draft' if draft else ''))
        r = render_tile(p, l, q, out, hue); finish_png(out, q); results.append(r); print(json.dumps(r), flush=True)
    jf = os.path.join(WORK, 'results%s.json' % ('_draft' if draft else ''))
    old = {}
    if os.path.exists(jf):
        try: old = {(x['preset'], x['light']): x for x in json.load(open(jf))}
        except Exception: old = {}
    for r in results: old[(r['preset'], r['light'])] = r
    allr = [old[(p, l)] for p in PRESETS for l in LIGHTS if (p, l) in old]
    json.dump(allr, open(jf, 'w'), indent=1)
    if draft: contact(allr, draft=True); return
    # ---- reports
    with open(os.path.join(HERE, 'ship_cost.txt'), 'w') as f:
        f.write('SHIP final 720x1280, Cycles CPU, %d spp + OIDN, 2 threads; CPU s of the render call (scene build separate, once per process); limit 40\n' % K.STATE.get('samples', 12) if False else 'SHIP final 720x1280, Cycles CPU, 12 spp + OIDN (direct light, no diffuse bounce), 2 threads. CPU s of the render call (user+sys of the process); limit 40. build = scene build seconds (once per process).\n')
        for r in allr: f.write('%-12s %-11s render cpu %5.1f s  wall %5.1f s  build %4.1f s  %s\n' % (r['preset'], r['light'], r['cpu'], r['wall'], r['build'], 'OK' if r['cpu'] <= 40 else 'OVER'))
        f.write('max cpu %.1f s\n' % max(r['cpu'] for r in allr))
    with open(os.path.join(HERE, 'ship_hue.txt'), 'w') as f:
        f.write('SHIP hue report: cast-shadow pixels from a sun-only render (method of styleboard/hue_check.py). target shade hue 225-265, magenta <= 10 %.\n')
        for r in allr:
            h = r.get('hue') or {}
            f.write('%-12s %-11s shade hue %s  median %s  in-band %s %%  magenta %s %%  cast px %s %%  %s\n' % (r['preset'], r['light'], h.get('shade_hue'), h.get('median'), h.get('in_band'), h.get('magenta'), h.get('cast_pct'), 'OK' if h.get('ok') else ('n/a (few shade pixels)' if h.get('shade_hue') is None and h.get('magenta', 0) <= 10 else 'OUT')))
    contact(allr, draft=False)

def contact(allr, draft=False):
    tw, th = (288, 512) if not draft else (270, 480)
    cols = len(LIGHTS); rows = len(PRESETS)
    pad = 8; lab = 22
    W = cols * (tw + pad) + pad; H = rows * (th + lab + pad) + pad
    im = Image.new('RGB', (W, H), (24, 24, 28)); d = ImageDraw.Draw(im)
    for ri, p in enumerate(PRESETS):
        for ci, l in enumerate(LIGHTS):
            f = os.path.join(FINAL, '%s_%s%s.png' % (p, l, '_draft' if draft else ''))
            x = pad + ci * (tw + pad); y = pad + ri * (th + lab + pad)
            if os.path.exists(f):
                t = Image.open(f).convert('RGB').resize((tw, th), Image.LANCZOS); im.paste(t, (x, y))
            r = [a for a in allr if a['preset'] == p and a['light'] == l]
            d.text((x + 2, y + th + 4), '%s  %s%s' % (p, l, ('  %.0fs' % r[0]['cpu']) if r else ''), fill=(220, 220, 230))
    im.save(os.path.join(HERE, 'ship_contact%s.jpg' % ('_draft' if draft else '')), quality=90)

if __name__ == '__main__':
    main()
