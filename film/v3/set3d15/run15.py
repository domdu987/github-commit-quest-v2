#!/usr/bin/env python3
"""run15.py : CLI. python3 run15.py stills [shots] | final [shots] | contact   (shots: 1,2,5-9 ...). Output in work/."""
import os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import set15 as F
import set15_shots as SH
HERE = F.HERE; WORK = F.WORK
def parse(a):
    out = []
    for tok in a.split(','):
        if '-' in tok: x, y = tok.split('-'); out += list(range(int(x), int(y) + 1))
        elif tok: out.append(int(tok))
    return out
def render_shot(n, quality='final', outdir=None, actors=True, light=None, which='a'):
    sd = F.SHOTS[n]; lt = light or sd['light']
    if (F.STATE.get('loc'), F.STATE.get('light')) != (sd['loc'], lt) or True:
        A = F.build(sd['loc'], lt)
    sc = bpy.context.scene; F.setup_render(sc, quality)
    cam = SH.setup_shot(n)
    F.crowd_mode(sd.get('crowd', 'hush' if 24 <= n <= 30 else 'normal')) if sd['loc'] == 'B' else None
    sc.frame_set(int(round(sd['t0'] * 30)) if which == 'a' else int(round(sd['t1'] * 30)))
    if actors: F.stage_placeholders(n, tuple(cam.location))
    bpy.context.view_layer.update(); hp = F.head_pixels(n)
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, 'shot%02d_%s_%s.png' % (n, sd['loc'], lt)); w, c = F.T.render(path)
    return path, w, c, hp
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; shots = parse(sys.argv[2]) if len(sys.argv) > 2 else sorted(F.SHOTS)
    if cmd == 'day16':
        p, w, c, hp = render_shot(16, 'final', light='DAY'); print(p, w, c)
    elif cmd in ('stills', 'final'):
        log = []
        for n in shots:
            p, w, c, hp = render_shot(n, 'final' if cmd == 'final' else 'preview')
            print('%s shot %d: %.1f s wall, %.1f s cpu, heads %s' % (cmd, n, w, c, hp), flush=True); log.append((n, w, c, hp))
    elif cmd == 'contact':
        from PIL import Image, ImageDraw, ImageFont
        W, H, LB, C = 720, 1280, 56, 6; fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
        paths = []; log = []
        for n in shots:
            p, w, c, hp = render_shot(n, 'final'); paths.append((n, p)); log.append('shot %02d %s %s wall %.1f cpu %.1f heads %s' % (n, F.SHOTS[n]['loc'], F.SHOTS[n]['light'], w, c, hp)); print(log[-1], flush=True)
        open(os.path.join(WORK, 'final_log_%s.txt' % (sys.argv[3] if len(sys.argv) > 3 else 'all')), 'w').write('\n'.join(log) + '\n')
    elif cmd == 'sheet':
        from PIL import Image, ImageDraw, ImageFont
        W, H, LB, C = 720, 1280, 56, 6; fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
        items = []
        for n in sorted(F.SHOTS):
            import glob
            for g in sorted(glob.glob(os.path.join(WORK, 'final', 'shot%02d_*.png' % n))): items.append((n, g))
        rows = (len(items) + C - 1) // C; Sh = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(Sh)
        for i, (n, pth) in enumerate(items):
            im = Image.open(pth).convert('RGB'); x, y = (i % C) * W, (i // C) * (H + LB); Sh.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2)
            sd = F.SHOTS[n]; lt = os.path.basename(pth).split('_')[2][:-4]; d.text((x + 12, y + H + 11), 'shot %d  %s %s' % (n, sd['loc'], lt), fill=(235, 235, 235), font=fnt)
        Sh.save(os.path.join(HERE, 'contact.jpg'), quality=88); Sh.resize((Sh.width // 3, Sh.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_small.jpg'), quality=88); print(Sh.size, len(items))
    else: print(__doc__)
