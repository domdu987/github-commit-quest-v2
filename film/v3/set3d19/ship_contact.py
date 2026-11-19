#!/usr/bin/env python3
"""ship_contact.py : the SHIP tiles (single source with make_contact.py: same H.build -> make_camera -> stage_placeholders -> render -> measure_hue pipeline).
One final 720x1280 tile per preset x light with placeholder actors (h19.stage_placeholders) at the deck / shore marks, cyan line at y 880.
Writes ship_contact.jpg, ship_cost.txt (CPU s of the render call, 2 threads), ship_hue.txt (cast-shadow hue from a sun-only render), ship_heads.txt (head y per preset).
usage:  python3 ship_contact.py [draft] [--only preset[:LIGHT],...] [--nohue] [--sheet]      (draft = 360x640 quick look, no reports)"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import bpy
from PIL import Image, ImageDraw
import h19 as H
import h19_kit as K

WORK = os.path.join(HERE, 'ship_work'); FINAL = os.path.join(WORK, 'final')
LIGHTS = ['NOON', 'DAY', 'STORM_DUSK']
PRESETS = ['ship_hero', 'ship_aerial', 'ship_deck', 'ship_rail', 'ship_rocks', 'ship_coast']
HOOKS = dict(ship_hero="H.set_sea(0.0); H.set_roll(0.0)", ship_aerial="H.set_sea(0.0)", ship_deck="H.set_sea(0.0); H.set_roll(0.0)", ship_rail="H.set_sea(0.0); H.set_roll(0.0)",
             ship_rocks="H.set_sea(0.0)", ship_coast="H.set_sea(0.0)", ship_shore="H.set_sea(0.0)")

def render_tile(preset, light, quality, out_png, hue=True, hooks=None):
    """the one pipeline (also used by make_contact.py for its S tiles). returns dict(cpu, wall, heads, hue, samples)"""
    A = H.build(preset, light=light); sc = bpy.context.scene
    H.setup_render(sc, quality)
    cs = A['cam']; cam = H.make_camera(cs)
    exec(HOOKS.get(preset, '') if hooks is None else hooks, dict(H=H, bpy=bpy))
    if light == 'STORM_DUSK' and preset == 'ship_rocks': H.set_rain(True)
    H.stage_placeholders(A['cam_name'], cs['loc']); bpy.context.view_layer.update(); hp = H.head_pixels(A['cam_name'])
    wall, cpu = H.render(out_png)
    res = dict(preset=preset, light=light, wall=round(wall, 1), cpu=round(cpu, 1), samples=sc.cycles.samples, heads=hp)
    if hue and quality == 'final':
        lamps = [o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'POINT']
        lampm = [o for o in bpy.data.objects if o.type == 'MESH' and any(m is not None and m.name.startswith('lamp') for m in o.data.materials)]
        try:
            if lamps or lampm:                           # lantern pools are warm by design: measure the sun / sky shade hue with the lamps (lights and glowing lantern meshes) off, 6 spp re-render, not counted in the cost
                en = [o.data.energy for o in lamps]; hv = [o.hide_render for o in lampm]; cy = sc.cycles; s0 = cy.samples
                for o in lamps: o.data.energy = 0.0
                for o in lampm: o.hide_render = True
                cy.samples = 6; tmp = out_png[:-4] + '_nolamp.png'; H.render(tmp); cy.samples = s0
                res['hue'] = H.measure_hue(tmp); res['hue']['lamps_off'] = True; os.remove(tmp)
                for o, e in zip(lamps, en): o.data.energy = e
                for o, v in zip(lampm, hv): o.hide_render = v
            else: res['hue'] = H.measure_hue(out_png)
        except Exception as e: res['hue'] = dict(err=str(e))
    return res

def finish_png_img(im, quality='final'):
    d = ImageDraw.Draw(im); y = 880 if quality == 'final' else 440
    d.line([(0, y), (im.width, y)], fill=(0, 255, 255), width=2 if quality == 'final' else 1)

def finish_png(png, quality):
    im = Image.open(png).convert('RGB'); d = ImageDraw.Draw(im); y = 880 if quality == 'final' else 440
    d.line([(0, y), (im.width, y)], fill=(0, 255, 255), width=2 if quality == 'final' else 1); im.save(png)

def main():
    args = sys.argv[1:]; draft = 'draft' in args; hue = '--nohue' not in args
    only = args[args.index('--only') + 1].split(',') if '--only' in args else None
    q = 'preview' if draft else 'final'; os.makedirs(FINAL, exist_ok=True)
    combos = [(p, l) for p in PRESETS for l in LIGHTS]
    if only: combos = [(p, l) for (p, l) in combos if p in only or ('%s:%s' % (p, l)) in only]
    if '--sheet' in args: combos = []
    results = []
    for (p, l) in combos:
        out = os.path.join(FINAL, '%s_%s%s.png' % (p, l, '_draft' if draft else ''))
        r = render_tile(p, l, q, out, hue); (finish_png(out, q) if draft else None); results.append(r); print(json.dumps(r), flush=True)
        for pr in ('ship_',):
            pass
    jf = os.path.join(WORK, 'results%s.json' % ('_draft' if draft else ''))
    old = {}
    if os.path.exists(jf):
        try: old = {(x['preset'], x['light']): x for x in json.load(open(jf))}
        except Exception: old = {}
    for r in results: old[(r['preset'], r['light'])] = r
    allr = [old[(p, l)] for p in PRESETS for l in LIGHTS if (p, l) in old]
    json.dump(allr, open(jf, 'w'), indent=1)
    if draft: contact(allr, draft=True); return
    reports(allr); contact(allr, draft=False)

def reports(allr):
    mx = max(r['cpu'] for r in allr)
    with open(os.path.join(HERE, 'ship_cost.txt'), 'w') as f:
        f.write('SHIP final 720x1280, Cycles CPU, 12 spp + OIDN, 2 threads, one process at a time. CPU s of the render call (user+sys); limit 40 (ship_deck 38). Same pipeline as make_contact.py (ship_contact.render_tile).\n')
        for r in allr:
            lim = 38 if r['preset'] == 'ship_deck' else 40
            f.write('%-12s %-11s render cpu %5.1f s  wall %5.1f s  %d spp  %s\n' % (r['preset'], r['light'], r['cpu'], r['wall'], r['samples'], 'OK' if r['cpu'] <= lim else 'OVER'))
        f.write('max cpu %.1f s\n' % mx)
    with open(os.path.join(HERE, 'ship_hue.txt'), 'w') as f:
        f.write('SHIP hue: cast-shadow pixels from a sun-only render (K.measure_hue; real cast shadows: masts, sails, rails, hull on the water). target shade hue 225-265, magenta <= 10 %.\n')
        for r in allr:
            h = r.get('hue') or {}
            f.write('%-12s %-11s shade hue %s  median %s  in-band %s %%  magenta %s %%  cast px %s %%  %s\n' % (r['preset'], r['light'], h.get('shade_hue'), h.get('median'), h.get('in_band'), h.get('magenta'), h.get('cast_pct'), 'OK' if h.get('ok') else ('n/a few shadow px' if h.get('shade_hue') is None and h.get('magenta', 99) <= 10 else 'OUT')))
    with open(os.path.join(HERE, 'ship_heads.txt'), 'w') as f:
        f.write('SHIP head positions at 720x1280: role, mark (D), head centre y, head px, chin y, feet y, head x. Target head y 450-760, chin < 880.\n')
        for r in allr:
            hs = r.get('heads') or []
            ys = [a[2] for a in hs]
            f.write('%-12s %-11s %s\n' % (r['preset'], r['light'], ('head y %s | ' % ys if ys else 'no actors | ') + '; '.join('%s y%d x%d chin%d' % (a[0], a[2], a[6], a[4]) for a in hs)))

def contact(allr, draft=False):
    tw, th = (288, 512) if not draft else (270, 480)
    cols = len(LIGHTS); rows = len(PRESETS); pad = 8; lab = 22
    W = cols * (tw + pad) + pad; Hh = rows * (th + lab + pad) + pad
    im = Image.new('RGB', (W, Hh), (24, 24, 28)); d = ImageDraw.Draw(im)
    for ri, p in enumerate(PRESETS):
        for ci, l in enumerate(LIGHTS):
            f = os.path.join(FINAL, '%s_%s%s.png' % (p, l, '_draft' if draft else ''))
            x = pad + ci * (tw + pad); y = pad + ri * (th + lab + pad)
            if os.path.exists(f):
                t = Image.open(f).convert('RGB')
                if not draft: finish_png_img(t)          # cyan y-880 guide only on the contact-sheet copy
                im.paste(t.resize((tw, th), Image.LANCZOS), (x, y))
            r = [a for a in allr if a['preset'] == p and a['light'] == l]
            d.text((x + 2, y + th + 4), '%s  %s%s' % (p, l, ('  %.0fs' % r[0]['cpu']) if r else ''), fill=(220, 220, 230))
    im.save(os.path.join(HERE, 'ship_contact%s.jpg' % ('_draft' if draft else '')), quality=90)

if __name__ == '__main__':
    main()
