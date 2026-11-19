#!/usr/bin/env python3
"""film 17 set contact sheet. usage (from this folder):
   python3 make_contact.py render [final|draft] [samples]   render every tile in TILES into contact_work/<mode>/ (one process per tile, skips existing; FORCE=1 re-renders)
   python3 make_contact.py sheet [final|draft]               contact.jpg (6 columns, 720x1280 tiles, label strip under each, cyan line at y 880) + contact_small.jpg (1/3)
   python3 make_contact.py hue [final|draft]                 hue.md: hue_report families + shade hue + black point + vivid blue + head-ring luma + render time per tile
"""
import sys, os, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
TILES = [('measure_wide', 'DAY_INT'), ('measure_chair', 'DAY_INT'), ('measure_high', 'DAY_INT'), ('measure_door', 'DAY_INT'), ('measure_low', 'DAY_INT'),
         ('records_aisle', 'DAY_INT'), ('records_low', 'DAY_INT'), ('records_desk', 'DAY_INT'), ('records_ladder', 'DAY_INT'),
         ('drawer_big', 'DAY_INT'), ('drawer_box', 'DAY_INT'), ('card_hero', 'DAY_INT'),
         ('street_wide', 'DUSK_EXT'), ('street_wagon', 'DUSK_EXT'),
         ('measure_wide', 'EVENING_INT'), ('measure_chair', 'EVENING_INT'), ('records_aisle', 'EVENING_INT'), ('records_desk', 'EVENING_INT'), ('card_hero', 'EVENING_INT'), ('street_wide', 'DAY_INT')]
def name(t): return '%s__%s' % t
def render(mode='final', samples=None):
    d = os.path.join(HERE, 'contact_work', mode); os.makedirs(d, exist_ok=True)
    for t in TILES:
        out = os.path.join(d, name(t) + '.png')
        if os.path.exists(out) and not os.environ.get('FORCE'): continue
        cmd = [sys.executable, os.path.join(HERE, 'bertillon.py'), 'render', t[0], t[1], out, mode] + ([str(samples)] if samples else [])
        t0 = time.time(); r = subprocess.run(cmd, capture_output=True, text=True); print(name(t), '%.0fs' % (time.time() - t0), (r.stdout.strip().splitlines() or [r.stderr[-300:]])[-1], flush=True)
def sheet(mode='final'):
    from PIL import Image, ImageDraw, ImageFont
    d = os.path.join(HERE, 'contact_work', mode); W, H, LB, C = 720, 1280, 78, 6
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26); F2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    rows = (len(TILES) + C - 1) // C; S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); dr = ImageDraw.Draw(S)
    for i, t in enumerate(TILES):
        f = os.path.join(d, name(t) + '.png')
        if not os.path.exists(f): continue
        im = Image.open(f).convert('RGB').resize((W, H)); x, y = (i % C) * W, (i // C) * (H + LB); S.paste(im, (x, y)); dr.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2)
        j = json.load(open(f + '.json')) if os.path.exists(f + '.json') else {}
        dr.text((x + 12, y + H + 8), '%s  [%s]' % (t[0], t[1]), fill=(240, 240, 240), font=F); dr.text((x + 12, y + H + 44), '%.0f s render, %s samples, %s tris' % (j.get('render_s', 0), j.get('samples', '?'), j.get('tris', '?')), fill=(170, 170, 180), font=F2)
    S.save(os.path.join(HERE, 'contact.jpg'), quality=88); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_small.jpg'), quality=88); print(S.size, len(TILES))
def hue(mode='final'):
    sys.path.insert(0, HERE); import bertillon_hue as BH
    d = os.path.join(HERE, 'contact_work', mode); L = ['# film 17 set3d17: colour numbers per frame (%s, 720x1280, placeholders at the stand points)' % mode, '',
        'Bands: shade hue 240-260; black point (luma p1) 0.08-0.12; blue share 14-30 %; magenta <= 10 %; vivid blue (S>0.6, H200-245) < 1.5 %; head-ring luma about 95-165. The street (exterior, dusk) may leave the hue band.',
        '', '| tile | red | orange | blue | magenta | shade hue | p1 | vivid % | dim 240-260 % | dim 0-45 % | val | dark | head ring luma (median) | render s | verdict |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for t in TILES:
        f = os.path.join(d, name(t) + '.png')
        if not os.path.exists(f): continue
        st = BH.frame_stats(f); bad = BH.check(st); j = json.load(open(f + '.json')) if os.path.exists(f + '.json') else {}; ring = j.get('ring', {})
        rl = ', '.join('%s %d' % (k, round(v['luma'])) for k, v in ring.items()) or '-'
        fm = st['fam']; L.append('| %s [%s] | %.1f | %.1f | %.1f | %.1f | %.1f | %.3f | %.1f | %.0f | %.0f | %.2f | %.2f | %s | %.0f | %s |' % (t[0], t[1], fm['red'], fm['orange'], fm['blue'], fm['magenta'], st['shade'], st['p1'], st['vivid'] * 100, st['dim_blue'] * 100, st['dim_warm'] * 100, st['val'], st['dark'], rl, j.get('render_s', 0), 'ok' if not bad else 'OUT: ' + ','.join(bad)))
    open(os.path.join(HERE, 'hue.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sheet'; mode = sys.argv[2] if len(sys.argv) > 2 else 'final'
    if cmd == 'render': render(mode, int(sys.argv[3]) if len(sys.argv) > 3 else None)
    elif cmd == 'sheet': sheet(mode)
    elif cmd == 'hue': hue(mode)
