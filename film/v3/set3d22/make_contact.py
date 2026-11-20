#!/usr/bin/env python3
"""make_contact.py: render the contact stills of builder A's shots (one process per frame: one location per process), then build
contact_sheet.jpg (labelled sNN start/mid/end + stats), contact_phone.jpg (360x640 tiles), hue_rows.txt, contact/stats.json.
    python3 make_contact.py [shots...]      e.g. s01 s02   (default: all of A's shots)   --sheet-only  only rebuild the sheets"""
import os, sys, json, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
A_SHOTS = ['s01', 's02', 's04', 's05', 's06', 's07', 's08', 's15']
BIGZOOM = ('s02', 's15')
def frames_for(sh):
    return ['start', 'mid', 'end'] if sh in BIGZOOM else ['start', 'end']
def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]; shots = a or A_SHOTS
    os.makedirs(os.path.join(HERE, 'contact'), exist_ok=True); tims = json.load(open(os.path.join(HERE, 'contact', 'timing.json'))) if os.path.exists(os.path.join(HERE, 'contact', 'timing.json')) else {}
    if '--sheet-only' not in sys.argv:
        for sh in shots:
            for w in frames_for(sh):
                while subprocess.run("pgrep -f 'beck.py (shot|still|board)|bpy|blender|render_' >/dev/null", shell=True).returncode == 0: time.sleep(0.25)
                t0 = time.time(); r = subprocess.run([sys.executable, os.path.join(HERE, 'beck.py'), 'shot', sh, w], capture_output=True, text=True)
                dt = time.time() - t0; line = [l for l in r.stdout.splitlines() if 'frame' in l]; print(sh, w, '%.1fs' % dt, line[-1] if line else r.stderr[-300:], flush=True)
                tims['%s_%s' % (sh, w)] = round(dt, 1)
        json.dump(tims, open(os.path.join(HERE, 'contact', 'timing.json'), 'w'), indent=1)
    sheet(tims)
def sheet(tims):
    from PIL import Image, ImageDraw, ImageFont
    import stats as ST
    tiles = []
    for sh in A_SHOTS:
        for w in frames_for(sh):
            p = os.path.join(HERE, 'contact', '%s_%s.png' % (sh, w))
            if os.path.exists(p): tiles.append((sh, w, p))
    ft = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
    cols = 6; W, H = 360, 640; LAB = 56; rows = (len(tiles) + cols - 1) // cols
    im = Image.new('RGB', (cols * (W + 8), rows * (H + LAB + 8)), '#10102a'); d = ImageDraw.Draw(im); ph = Image.new('RGB', (cols * W, rows * H), '#10102a'); st_all = {}; hue = []
    for i, (sh, w, p) in enumerate(tiles):
        r, c = divmod(i, cols); full = Image.open(p).convert('RGB'); t = full.resize((W, H), Image.LANCZOS); s = ST.stats(p)
        full2 = full.copy(); ImageDraw.Draw(full2).line((0, 880, 720, 880), fill=(0, 255, 255), width=3); full2.save(p.replace('.png', '_line.png'))
        t2 = full2.resize((W, H), Image.LANCZOS); x, y = c * (W + 8), r * (H + LAB + 8)
        im.paste(t2, (x, y)); d.text((x + 6, y + H + 4), '%s %s' % (sh, w), font=ft, fill='white')
        d.text((x + 6, y + H + 34), 'sat %.2f luma %.0f vivid %.0f%% hue %.0f' % (s['sat'], s['luma'], s['vivid'], s['shade_hue']), font=fs, fill=(170, 200, 255))
        ph.paste(t, (c * W, r * H)); st_all['%s_%s' % (sh, w)] = s
        hue.append('%s %-5s sat %.3f luma %5.1f vivid %5.1f%% shade_hue %5.1f shade_frac %4.1f%%' % (sh, w, s['sat'], s['luma'], s['vivid'], s['shade_hue'], s['shade_frac']))
    im.save(os.path.join(HERE, 'contact_sheet.jpg'), quality=90); ph.save(os.path.join(HERE, 'contact_phone.jpg'), quality=90)
    open(os.path.join(HERE, 'hue_rows.txt'), 'w').write('\n'.join(hue) + '\n'); json.dump(dict(stats=st_all, timing=tims), open(os.path.join(HERE, 'contact', 'stats.json'), 'w'), indent=1)
    print('\n'.join(hue))
if __name__ == '__main__': main()
