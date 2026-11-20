#!/usr/bin/env python3
"""Hue rows (v3/tools/hue_report.stats) + SHADE HUE (chroma-weighted circular mean hue of shaded pixels, rule 240-260) + the night-brightness
rules of the film-18 brief: middle-band luma (0-255) 70..130 and dark share (V < 0.25) under 0.35. usage: python3 jimo_hue.py <png ...>"""
import sys, os, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import hue_report as H

def shade_hue(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255; im = np.concatenate([im[:212], im[240:]])
    r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60
    sel = (mx > 0.10) & (mx < 0.55) & (s > 0.2) & (b >= r); w = (s * mx)[sel]
    if w.sum() == 0: return float('nan'), 0.0
    a = np.radians(h[sel]); m = math.degrees(math.atan2((np.sin(a) * w).sum(), (np.cos(a) * w).sum())) % 360
    return m, float(sel.mean())

def luma(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float); y = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
    mid = y[107:213]                                                                  # middle third of the height
    v = im.max(-1) / 255
    return float(y.mean()), float(mid.mean()), float((v < 0.25).mean())

def report(fs):
    out = []
    print(f"{'still':14s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark | shade hue (n)  luma  midband  dark<0.25")
    for f in fs:
        h, s, v, dk = H.stats([f]); sh, fr = shade_hue(f); lm, lmid, dkv = luma(f)
        print(f"{os.path.basename(f)[:-4]:14s} " + " ".join(f"{h[n]:6.1f}" for n in H.NAMES) + f"  {s:.2f} {v:.2f} {dk:.2f} | {sh:6.1f} ({fr:.2f}) {lm:6.1f} {lmid:7.1f}  {dkv:.2f}  " + ('ok' if 240 <= sh <= 260 else 'SHADE-OUT') + (' ' if 70 <= lmid <= 130 else ' MID-OUT') + (' ' if dkv < 0.35 else ' DARK-OUT'))
        out.append(dict(file=os.path.basename(f), hue={n: round(h[n], 1) for n in H.NAMES}, sat=round(s, 3), val=round(v, 3), dark_v025=round(dkv, 3), shade_hue=round(sh, 1), shaded_frac=round(fr, 3),
                        luma_mean=round(lm, 1), luma_mid=round(lmid, 1)))
    return out

if __name__ == '__main__' and not (len(sys.argv) > 1 and sys.argv[1] == 'rows'): report(sys.argv[1:])

# ----------------------------------------------------------------------------- production rows (one per contact tile): hue families, shade hue, brightness, caption band, wall edge density and wall hue
import json
from PIL import ImageDraw

def _gray(im): return (0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]) / 255.0

def edge_density(png, polys, thr=0.22):
    """Share of wall-region pixels with a strong edge: grayscale, 1 px box blur, Sobel gradient magnitude > thr x 0.5 (0..1 luma), 1-px thinned by keeping local maxima along x or y
    (a Canny-like count without hysteresis: calibrated so that the style board's board_1 wall reads 0.048)."""
    im = np.asarray(Image.open(png).convert('RGB'), dtype=float); g = _gray(im)
    k = np.ones((3, 3)) / 9.0; gp = np.pad(g, 1, mode='edge'); gb = sum(gp[i:i + g.shape[0], j:j + g.shape[1]] * k[i, j] for i in range(3) for j in range(3))
    gx = np.zeros_like(gb); gy = np.zeros_like(gb); gx[:, 1:-1] = gb[:, 2:] - gb[:, :-2]; gy[1:-1, :] = gb[2:, :] - gb[:-2, :]; mag = np.hypot(gx, gy)
    mx = (mag >= np.roll(mag, 1, 1)) & (mag >= np.roll(mag, -1, 1)) | (mag >= np.roll(mag, 1, 0)) & (mag >= np.roll(mag, -1, 0))
    e = (mag > thr * 0.5) & mx
    m = Image.new('L', (g.shape[1], g.shape[0]), 0); d = ImageDraw.Draw(m)
    for p in polys: d.polygon([tuple(q) for q in p], fill=255)
    m = np.asarray(m) > 0
    if m.sum() < 400: return float('nan'), 0
    return float(e[m].mean()), int(m.sum())

def wall_hue(png, polys):
    """Share of wall-region pixels (mid value) with hue 230-255 (moon shade), 20-45 (ochre fire-lit), and the magenta/rose share (300-350)."""
    im = np.asarray(Image.open(png).convert('RGB'), dtype=float) / 255
    m = Image.new('L', (im.shape[1], im.shape[0]), 0); d = ImageDraw.Draw(m)
    for p in polys: d.polygon([tuple(q) for q in p], fill=255)
    m = np.asarray(m) > 0
    if m.sum() < 400: return None
    r, g, b = im[..., 0][m], im[..., 1][m], im[..., 2][m]; mx = im.max(-1)[m]; mn = im.min(-1)[m]; dd = mx - mn; s = dd / np.maximum(mx, 1e-9)
    hr = ((g - b) / np.maximum(dd, 1e-9)) % 6; hg = (b - r) / np.maximum(dd, 1e-9) + 2; hb = (r - g) / np.maximum(dd, 1e-9) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60; ok = s > 0.12
    n = max(1, ok.sum())
    return dict(blue230_255=float(((h >= 230) & (h <= 255) & ok).sum() / n), ochre20_45=float(((h >= 20) & (h <= 45) & ok).sum() / n), rose300_350=float(((h >= 300) & (h <= 350) & ok).sum() / n))

def caption_band(png):
    im = np.asarray(Image.open(png).convert('RGB'), dtype=float)[880:950]; y = _gray(im); v = im.max(-1) / 255
    return float(y.mean() * 255), int((v > 0.7).sum())

def production_rows(fdir, out):
    sys.path.insert(0, HERE); import jimo_shots as S
    lines = []; names = H.NAMES; hdr = "%-4s %-9s %-5s " % ('shot', 'loc', 'light') + " ".join("%6s" % n[:6] for n in names) + "   sat  val dark | shade  frac   luma  mid  dark25 | cap_mean cap_bright | wall_edge wall_blue wall_ochre wall_rose | s_cpu"
    lines.append(hdr); allrows = []
    for k, sh in S.SHOTS.items():
        png = os.path.join(fdir, k + '.png')
        if not os.path.exists(png): continue
        h, s, v, dk = H.stats([png]); sh_h, fr = shade_hue(png); lm, lmid, dkv = luma(png); cm, cb = caption_band(png)
        mj = os.path.join(fdir, k + '.json'); meta = json.load(open(mj)) if os.path.exists(mj) else {}; polys = meta.get('wall', [])
        ed = edge_density(png, polys) if polys else (float('nan'), 0); wh = wall_hue(png, polys) if polys else None
        lg = os.path.join(os.path.dirname(fdir), 'final_log.txt'); cpu = ''
        for ln in open(lg).read().split('\n') if os.path.exists(lg) else []:
            if ln.startswith('final %s' % k) or ln.startswith('final %s_' % k): cpu = ln.split(',')[1].strip().split()[0]
        lines.append("%-4s %-9s %-5s " % (k, sh['loc'], sh['light']) + " ".join("%6.1f" % h[n] for n in names) + "  %.2f %.2f %.2f | %6.1f %5.2f %6.1f %4.0f %5.2f | %7.1f %9d | %9.3f %9s %10s %9s | %s" % (
            s, v, dk, sh_h, fr, lm, lmid, dkv, cm, cb, ed[0], ('%.2f' % wh['blue230_255']) if wh else '-', ('%.2f' % wh['ochre20_45']) if wh else '-', ('%.2f' % wh['rose300_350']) if wh else '-', cpu))
        allrows.append(dict(shot=k, magenta=round(h['magenta'], 1), edge=ed[0], cap_mean=cm, cap_bright=cb, wall=wh))
    open(out, 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines)); return allrows

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'rows':
    production_rows(os.path.join(HERE, 'set_work', 'final'), os.path.join(HERE, 'set_work', 'hue_rows.txt'))
