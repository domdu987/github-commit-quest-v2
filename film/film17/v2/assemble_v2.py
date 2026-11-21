"""Film 17 v2: assemble the 2052 film frames from the render-team parts and apply the conform luma trim.

usage: python3 assemble_v2.py <parts_root> <out_frames_dir> [--report trim.json]
  <parts_root>/<part>/take.mkv (or take.mkv.partaa/ab) + meta.json, as fetched by fetch_v2.sh.
Writes <out_frames_dir>/f_%04d.png (f = film g, 0..2051) for conform17.py (FRAMES=<dir>).

Trim (takes.md "Luma trim at conform"): pure RGB multiply k per frame. The metric is the qa_stats2 luma
(the mean of R, G and B at 90x160). k only pulls a frame back into its take's target band:
  k = hi/L if L > hi, lo/L if L < lo, else 1
k is clamped to [KMIN, 1.12] (KMIN = 0.85, or 0.82 for T6) and smoothed with a 15-frame moving average.
The smoothing never crosses a hard cut. A multiply leaves the qa_stats2 sat/vivid unchanged.
"""
import sys, os, json, subprocess, glob
import numpy as np
from PIL import Image

N = 2052
CUTS = [0, 336, 651, 850, 1045, 1377, 1675, 1695, 1868, N]   # shot starts; 1675 = P2 hard cut (takes.md)
# take ranges used in the film (by the hard cuts) -> target band and trim floor
TAKES = [  # (take, g0, g1 incl, lo, hi, kmin)
    ('T1', 0, 335, 95, 112, 0.85), ('T2', 336, 650, 95, 110, 0.85), ('T3', 651, 849, 95, 110, 0.85),
    ('T4', 850, 1044, 95, 110, 0.85), ('T5', 1045, 1376, 90, 108, 0.85), ('T6', 1377, 1694, 95, 112, 0.82),
    ('T7', 1695, 1867, 88, 105, 0.85), ('T8', 1868, 2051, 95, 110, 0.85)]
# which part supplies which film frames (split parts join frame-exact)
PARTS = [('T1a', 0, 190), ('T1b', 191, 335), ('T2a', 336, 493), ('T2b', 494, 650), ('T3', 651, 750), ('T3b', 751, 849),
         ('T4', 850, 1044), ('T5a', 1045, 1210), ('T5b', 1211, 1296), ('T5b2', 1297, 1376), ('T6a', 1377, 1452),
         ('T6a2', 1453, 1535), ('T6b', 1536, 1694), ('T7', 1695, 1867), ('T8', 1868, 2051)]
KMAX = 1.12


def luma(a):
    im = Image.fromarray(a).resize((90, 160), Image.BILINEAR)
    return float(np.asarray(im, dtype=np.float32).mean())


def decode(part_dir, tmp):
    mk = os.path.join(part_dir, 'take.mkv')
    if not os.path.exists(mk):
        pieces = sorted(glob.glob(mk + '.part*'))
        assert pieces, 'no take in ' + part_dir
        with open(os.path.join(tmp, 'take.mkv'), 'wb') as o:
            for p in pieces: o.write(open(p, 'rb').read())
        mk = os.path.join(tmp, 'take.mkv')
    meta = json.load(open(os.path.join(part_dir, 'meta.json')))
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mk, os.path.join(tmp, 'd_%05d.png')], check=True)
    files = sorted(glob.glob(os.path.join(tmp, 'd_*.png')))
    return int(meta['first_g']), files


def main():
    root, out = sys.argv[1], sys.argv[2]
    rep = sys.argv[sys.argv.index('--report') + 1] if '--report' in sys.argv else None
    os.makedirs(out, exist_ok=True)
    src = [None] * N
    for part, g0, g1 in PARTS:
        tmp = os.path.join(out, '_dec_' + part)
        first, files = decode(os.path.join(root, part), tmp)
        for g in range(g0, g1 + 1):
            i = g - first
            assert 0 <= i < len(files), f'{part}: g{g} not in its take (first_g {first}, {len(files)} frames)'
            src[g] = files[i]
    L = np.array([luma(np.asarray(Image.open(f).convert('RGB'))) for f in src])
    k = np.ones(N)
    for t, g0, g1, lo, hi, kmin in TAKES:
        for g in range(g0, g1 + 1):
            k[g] = hi / L[g] if L[g] > hi else (lo / L[g] if L[g] < lo else 1.0)
            k[g] = min(KMAX, max(kmin, k[g]))
    ks = k.copy()
    for a, b in zip(CUTS[:-1], CUTS[1:]):              # smooth inside each shot only
        seg = k[a:b]; w = min(15, len(seg))
        pad = np.pad(seg, (w // 2, w - 1 - w // 2), mode='edge')
        ks[a:b] = np.convolve(pad, np.ones(w) / w, mode='valid')
    for g in range(N):
        a = np.asarray(Image.open(src[g]).convert('RGB'), dtype=np.float32)
        Image.fromarray(np.clip(a * ks[g] + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(out, 'f_%04d.png' % g))
    after = L * ks
    summ = {t: {'before': round(float(L[g0:g1 + 1].mean()), 1), 'after': round(float(after[g0:g1 + 1].mean()), 1),
                'k_min': round(float(ks[g0:g1 + 1].min()), 3), 'k_max': round(float(ks[g0:g1 + 1].max()), 3)}
            for t, g0, g1, *_ in TAKES}
    summ['film'] = {'before': round(float(L.mean()), 1), 'after': round(float(after.mean()), 1)}
    print(json.dumps(summ, indent=1))
    if rep: json.dump({'summary': summ, 'k': [round(float(x), 4) for x in ks], 'luma_before': [round(float(x), 2) for x in L]}, open(rep, 'w'))
    for d in glob.glob(os.path.join(out, '_dec_*')):
        subprocess.run(['rm', '-rf', d])


if __name__ == '__main__':
    main()
