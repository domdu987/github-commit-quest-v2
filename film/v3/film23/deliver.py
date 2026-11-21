#!/usr/bin/env python3
"""deliver.py <sNN> -- build take.mkv, meta.json, cues.json, contact.jpg, QA_AUTO.md / phone_sheet.jpg (qa_auto), QA_JITTER.txt, numbers.json from <sNN>/raw.
Per-take constants are in TAKES.  python3 deliver.py s18 [--no-encode]"""
import os, sys, json, subprocess, glob, math, shutil
import numpy as np
from PIL import Image, ImageDraw
V3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PROJ = os.path.dirname(V3)
sys.path.insert(0, os.path.join(V3, 'set3d23'))
HERE = os.path.dirname(os.path.abspath(__file__))
T = {  # shot, g0, g1 (planned), n (rendered body frames - 1), handle, transition_in, location, light
 's01': dict(shot='S01', g0=0, g1=120, n=150, handle=0, tin=dict(type='open', frames=0), loc='FIELDS', light='DAWN'),
 's14': dict(shot='S14', g0=1506, g1=1626, n=150, handle=10, tin=dict(type='dissolve', frames=17), loc='RHINE', light='NIGHT_R'),
 's15': dict(shot='S15', g0=1629, g1=1728, n=124, handle=7, tin=dict(type='dissolve', frames=11), loc='RHINE', light='NIGHT_R'),
 's16': dict(shot='S16', g0=1728, g1=1827, n=124, handle=0, tin=dict(type='cut', frames=0), loc='RHINE', light='NIGHT_R'),
 's17': dict(shot='S17', g0=1827, g1=1905, n=98, handle=7, tin=dict(type='dissolve', frames=11), loc='RHINE', light='NIGHT_R'),
 's18': dict(shot='S18', g0=1905, g1=1980, n=94, handle=9, tin=dict(type='dissolve', frames=13), loc='RHINE', light='PREDAWN'),
}
CUES = {
 's01': [(0, 150, 'dawn countryside, Normandy 1944: birds, a light breeze, far-off diesel rumble growing as the column nears', 'ambience'), (45, 150, 'tank column rolling on the lane: engines, tracks clanking, a jeep tow chain jingling', 'foley'), (100, 150, 'soldier on the lead tank waves: cloth flap, a cheerful shout far away', 'foley')],
 's14': [(0, 160, 'Rhine at night, March 1945: slow water, a cold wind, distant artillery thump far off', 'ambience'), (20, 160, 'crates dropped on the bank, canvas rustle, boots on gravel from the unloading trucks', 'foley')],
 's15': [(0, 131, 'night camp by the river: hand pumps wheezing, rubber hissing as the tanks fill, low murmur', 'ambience'), (10, 131, 'pump handles creaking in a steady stroke, air hissing into the rubber', 'foley')],
 's16': [(0, 125, 'sound truck booming a recorded tank column across the water, with static radio chatter from the tent', 'foley'), (0, 125, 'night camp ambience: lantern hiss, river lap', 'ambience')],
 's17': [(0, 105, 'far-bank night, quiet wind; binocular strap creak, a muttered gasp', 'ambience'), (57, 75, 'sausage drops on the ground: soft thud', 'prop')],
 's18': [(0, 103, 'pre-dawn Rhine: quiet water, paddles dipping softly, boards creaking under tiptoeing boots', 'foley'), (0, 103, 'bird calls starting, a hushed dog whine', 'ambience')],
}

def sh(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)

def main(name, encode=True):
    cfg = T[name]; D = os.path.join(HERE, name); raw = os.path.join(D, 'raw')
    first_g = cfg['g0'] - cfg['handle']; n_frames = cfg['handle'] + cfg['n'] + 1; last_g = first_g + n_frames - 1
    files = [os.path.join(raw, 'g_%04d.png' % g) for g in range(first_g, last_g + 1)]
    miss = [f for f in files if not os.path.exists(f)]
    assert not miss, 'missing %d frames, e.g. %s' % (len(miss), miss[:3])
    rows = [json.load(open(f[:-4] + '.json')) for f in files]
    mkv = os.path.join(D, 'take.mkv')
    if encode:
        r = sh(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(first_g), '-i', os.path.join(raw, 'g_%04d.png'), '-frames:v', str(n_frames),
                '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', mkv]); print(r.stderr[-500:])
    size = os.path.getsize(mkv)
    parts = []
    if size > 45 * 1024 * 1024:
        for p in glob.glob(mkv + '.part_*'): os.remove(p)
        sh(['split', '-b', '40M', mkv, mkv + '.part_']); os.remove(mkv); parts = sorted(os.path.basename(p) for p in glob.glob(mkv + '.part_*'))
        mkv_an = os.path.join(D, 'work', 'take_full.mkv'); os.makedirs(os.path.dirname(mkv_an), exist_ok=True)
        with open(mkv_an, 'wb') as o:
            for p in parts: o.write(open(os.path.join(D, p), 'rb').read())
    else: mkv_an = mkv
    # QA_AUTO + phone sheet, jitter
    r = sh([sys.executable, os.path.join(PROJ, 'qa_auto.py'), mkv_an, '--first_g', str(first_g), '--out', D]); print(r.stdout[-1500:], r.stderr[-500:])
    rj = sh([sys.executable, os.path.join(PROJ, 'qa_jitter.py'), mkv_an]); open(os.path.join(D, 'QA_JITTER.txt'), 'w').write(rj.stdout + rj.stderr); print(rj.stdout)
    # frame-diff, luma, hue, heads, water
    g90 = [np.asarray(Image.open(f).convert('L').resize((90, 160), Image.BILINEAR), dtype=np.float32) for f in files]
    body0 = cfg['handle']; diffs = np.array([np.abs(g90[i + 1] - g90[i]).mean() for i in range(body0, len(g90) - 1)])
    lum = [float(np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float).mean()) for f in files[::5]]
    import ghost_hue as GHUE
    idx = [0, len(files) // 2, len(files) - 1]; hues = {}
    for i in idx:
        sh_, fr = GHUE.shade_hue(files[i]); hues[str(first_g + i)] = dict(shade_hue=round(sh_, 1), share=round(fr, 3))
    heads = {}; maxhead = 0.0
    for r_, g in zip(rows, range(first_g, last_g + 1)):
        for k, v in r_.get('heads', {}).items():
            maxhead = max(maxhead, v['y']); heads[k] = max(heads.get(k, 0), v['y'])
    wall = [r_['wall'] for r_ in rows]; cpu = [r_['cpu'] for r_ in rows]
    water = [r_['water_frac'] for r_ in rows if 'water_frac' in r_]
    nums = dict(take=name, first_g=first_g, n_frames=n_frames, diff_median=round(float(np.median(diffs)), 2), diff_p90=round(float(np.percentile(diffs, 90)), 2),
                diff_min=round(float(diffs.min()), 2), luma_min=round(min(lum), 1), luma_max=round(max(lum), 1), luma_mean=round(float(np.mean(lum)), 1),
                shade_hue=hues, max_head_centre_y=round(maxhead, 1), head_y_by_card={k: round(v, 1) for k, v in heads.items()},
                water_frac_range=[round(min(water), 3), round(max(water), 3)] if water else None,
                s_per_frame_wall=round(float(np.mean(wall)), 2), s_per_frame_cpu=round(float(np.mean(cpu)), 2), jitter=rj.stdout.strip().splitlines()[-1] if rj.stdout.strip() else '')
    json.dump(nums, open(os.path.join(D, 'numbers.json'), 'w'), indent=1); print(json.dumps(nums, indent=1))
    # contact sheet: every 5th frame (6 fps), 180x320 tiles, cyan line at y 880
    sel = list(range(0, len(files), 5)); cols = 10; rowsn = int(math.ceil(len(sel) / cols)); W, H = 180, 320
    sheet = Image.new('RGB', (cols * W, rowsn * H), (0, 0, 0)); dr = ImageDraw.Draw(sheet)
    for k, i in enumerate(sel):
        im = Image.open(files[i]).convert('RGB').resize((W, H), Image.LANCZOS); x, y = (k % cols) * W, (k // cols) * H; sheet.paste(im, (x, y))
        dr.line([x, y + int(880 / 4), x + W, y + int(880 / 4)], fill=(0, 255, 255), width=1); dr.text((x + 3, y + 3), 'g%d' % (first_g + i), fill=(255, 255, 255))
    sheet.save(os.path.join(D, 'contact.jpg'), quality=88)
    # meta / cues
    meta = dict(take=name, film=23, shots=[cfg['shot']], g0=cfg['g0'], g1=cfg['g1'], g1_render=cfg['g0'] + cfg['n'], first_g=first_g, n_frames=n_frames,
                handle_in=cfg['handle'], handle_out=0, transition_in=cfg['tin'], location=cfg['loc'], light=cfg['light'], samples=12, resolution=[720, 1280], fps=30, threads=2,
                s_per_frame_wall_mean=nums['s_per_frame_wall'], s_per_frame_cpu_mean=nums['s_per_frame_cpu'], dof='none',
                timing='ESTIMATE (timing_EST.json): rendered planned length x 1.25 (the camera move and the action continue through the tail)',
                mkv_parts=parts or None)
    json.dump(meta, open(os.path.join(D, 'meta.json'), 'w'), indent=1)
    cues = [dict(time=round((first_g + a) / 30.0, 3), duration=round((b - a) / 30.0, 3), frame=first_g + a, end_frame=first_g + b, kind=k, label=l) for a, b, l, k in CUES[name]]
    json.dump(dict(take=name, fps=30, note='time = film seconds (g / 30) on the ESTIMATED clock', cues=cues), open(os.path.join(D, 'cues.json'), 'w'), indent=1)
    print('delivered', name, size, parts)

if __name__ == '__main__':
    main(sys.argv[1], encode='--no-encode' not in sys.argv)
