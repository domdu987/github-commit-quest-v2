"""jimo_cards.py : real 2D cast cards for the contact sheet / drafts (round 2). Rasterises cast18 figures (people poses, the dragon / plain ox) to transparent PNGs with the same
Playwright raster path the cast uses (puppet._raster -> raster.js), cached in set_work/cards/. Pure python (no bpy).
    card('ox', state='dragon', view='three_quarter', gait='gallop', phase=2, flame=1)  -> dict(path, w, h, x0, feet)   (w, h, x0 in D (x0 = left edge relative to the feet x), feet = image row of the soles in D from the top)
    card('person', pose='general_laugh')"""
import os, sys, hashlib, json
HERE = os.path.dirname(os.path.abspath(__file__)); CARDS = os.path.join(HERE, 'set_work', 'cards')
CAST = os.path.join(os.path.dirname(HERE), 'cast18')
PXD_P, PXD_O = 130, 120                                   # px per D for people / oxen
_C = {}

def _cast():
    if 'cast' not in _C:
        if CAST not in sys.path: sys.path.insert(0, CAST)
        import cast18, puppet as P
        _C['cast'] = cast18; _C['P'] = P
    return _C['cast'], _C['P']

def _write(svg_body, bb, feet_y, D, name):
    cast, P = _cast(); x0, y0, x1, y1 = bb; W = int((x1 - x0) * D) + 8; H = int((y1 - y0) * D) + 8
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d"><g transform="translate(%.2f %.2f) scale(%d)">%s</g></svg>' % (W, H, 4 - x0 * D, 4 - y0 * D, D, svg_body)
    os.makedirs(CARDS, exist_ok=True); sp = os.path.join(CARDS, name + '.svg'); out = os.path.join(CARDS, name + '.png')
    open(sp, 'w').write(svg); P._raster(sp, out, W, H, 1)
    try: os.remove(sp)
    except OSError: pass
    return dict(path=out, w=W / D, h=H / D, x0=x0 - 4.0 / D, feet=(feet_y - y0) + 4.0 / D, top=-(y0 - 4.0 / D), D=D)

def card(kind, **k):
    key = kind + '_' + '_'.join('%s%s' % (a, k[a]) for a in sorted(k)); name = hashlib.md5(key.encode()).hexdigest()[:10] + '_' + kind
    mp = os.path.join(CARDS, name + '.json')
    if os.path.exists(mp) and os.path.exists(os.path.join(CARDS, name + '.png')): return json.load(open(mp))
    cast, P = _cast()
    if kind == 'ox':
        f = cast.ox_figure(state=k.get('state', 'dragon'), view=k.get('view', 'three_quarter'), gait=k.get('gait', 'stand'), phase=k.get('phase', 0) / 8.0, flame=k.get('flame', -1), blades=True, reed=(True if k.get('reed') else None), uid='c%s' % name[:6])
        m = _write(f['svg'], f['bbox'], 0.0, PXD_O, name); m['kind'] = 'ox'
    else:
        c, pose = cast.STORY18[k['pose']]; f = P.figure(c, dict(pose), 'p%s' % name[:6]); a = f['anchors']
        m = _write(f['svg'], f['bbox'], f['feet_y'], PXD_P, name); m['kind'] = 'person'; m['height'] = f['feet_y'] - a['head_top'][1]; m['x0'] = f['bbox'][0] - 4.0 / PXD_P
    json.dump(m, open(mp, 'w')); return m

if __name__ == '__main__':
    m = card('ox', state='dragon', view='three_quarter', gait='gallop', phase=1, flame=1); print(m)
    print(card('person', pose='general_laugh'))
