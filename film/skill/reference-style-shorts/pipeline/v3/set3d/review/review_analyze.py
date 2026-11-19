#!/usr/bin/env python3
"""review_analyze.py : measurements on the reviewer's passes (no bpy).
  light <dir> <cam>   per-surface shadow/lit ratio, hue shift and cast-shadow edge width from the on / off / unshadowed passes
"""
import sys, os, json
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmeasure as M

def lin(a): return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)

def visibility(d, cam):
    on = M.load(f'{d}/{cam}_on.png'); off = M.load(f'{d}/{cam}_off.png'); un = M.load(f'{d}/{cam}_unshadowed.png')
    lon, loff, lun = lin(on).sum(2), lin(off).sum(2), lin(un).sum(2); den = lun - loff
    v = np.clip((lon - loff) / np.maximum(den, 1e-4), 0, 1); sunny = den > 0.03          # sunny = the key would reach this surface if nothing stood in the way
    return on, off, un, v, sunny

def edge_widths(v, sunny, ids_full=None, names=None, only=None):
    """10-90 percent widths (px) of v across the v = 0.5 contour, measured along the local normal."""
    vs = cv2.GaussianBlur(v.astype(np.float32), (0, 0), 1.0); gx = cv2.Sobel(vs, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(vs, cv2.CV_32F, 0, 1, ksize=3)
    cs, _ = cv2.findContours((v > 0.5).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE); H, W = v.shape; out = []
    sun_e = cv2.erode(sunny.astype(np.uint8), np.ones((41, 41), np.uint8)) > 0             # stay well inside one sunny surface
    for c in cs:
        if len(c) < 40: continue
        for k in range(0, len(c), 6):
            x, y = c[k, 0]
            if not (24 < x < W - 24 and 24 < y < H - 24) or not sun_e[y, x]: continue
            g = np.array([gx[y, x], gy[y, x]], float); n = np.linalg.norm(g)
            if n < 1e-3: continue
            g /= n; t = np.arange(-22, 22.01, 0.25); xs = (x + t * g[0]).astype(np.float32).reshape(-1, 1); ys = (y + t * g[1]).astype(np.float32).reshape(-1, 1)
            p = cv2.remap(v.astype(np.float32), xs, ys, cv2.INTER_LINEAR).ravel()
            if p[:12].mean() > 0.08 or p[-12:].mean() < 0.92: continue                    # needs clean plateaus on both sides (a single edge)
            i9 = int(np.argmax(p >= 0.9)); i1 = i9
            while i1 > 0 and p[i1] > 0.1: i1 -= 1
            w = (i9 - i1) * 0.25
            if only is not None and ids_full is not None and names[ids_full[y, x]] not in only: continue
            out.append((w, x, y))
    return out

def light(d, cam, verbose=True):
    on, off, un, v, sunny = visibility(d, cam); g = M.load(f'{d}/{cam}_graded.png')
    z = np.load(f'{d}/{cam}_ids.npz', allow_pickle=True); ids = z['ids']; names = list(z['names']); ids_full = cv2.resize(ids, (720, 1280), interpolation=cv2.INTER_NEAREST)
    Yon, Yoff = M.luma(on), M.luma(off); rows = []
    lit = sunny & (v > 0.97); cast = sunny & (v < 0.03)
    groups = dict(floor=['floor'], rug=['rug'], map=['map_paper'], wallpaper=['wall_z1'], wainscot=['wall_z0', 'wall_relief'], ALL=None)
    res = {}
    for gname, members in groups.items():
        m = np.ones(ids_full.shape, bool) if members is None else np.isin(ids_full, [names.index(n) for n in members if n in names])
        ml, mc = m & lit, m & cast
        if ml.sum() < 400: continue
        r = Yoff[ml] / np.maximum(Yon[ml], 1e-3); rl = lin(off)[ml].dot((0.2126, 0.7152, 0.0722)) / np.maximum(lin(on)[ml].dot((0.2126, 0.7152, 0.0722)), 1e-4)
        row = dict(n_lit=int(ml.sum()), n_cast=int(mc.sum()), ratio_display=[float(np.percentile(r, q)) for q in (10, 50, 90)], ratio_linear=float(np.median(rl)))
        L = np.median(g[ml], axis=0); row['lit'] = M.hexs(L); row['hue_lit'] = M.hsv(L)[0]
        Ssame = np.median(off[ml], axis=0)                                                 # the same pixels with the key off (ungraded)
        row['v_ratio'] = float(np.median(off[ml].max(1) / np.maximum(on[ml].max(1), 1e-3)))
        if mc.sum() > 200:
            C = np.median(g[mc], axis=0); row['cast'] = M.hexs(C); row['hue_cast'] = M.hsv(C)[0]; row['sat_cast'] = M.hsv(C)[1]; row['ratio_region_display'] = float(M.luma(C) / M.luma(L))
        res[gname] = row
    ew = edge_widths(v, sunny); w = np.array([e[0] for e in ew]) if ew else np.array([0.0])
    res['edge_width_px'] = dict(n=len(ew), p10=float(np.percentile(w, 10)), median=float(np.median(w)), p90=float(np.percentile(w, 90)), max=float(w.max()))
    res['sunny_share'] = float(sunny.mean()); res['lit_share'] = float(lit.mean()); res['cast_shadow_share'] = float(cast.mean())
    cv2.imwrite(f'{d}/{cam}_vis.png', (v * 255).astype(np.uint8))
    if verbose:
        print('==', cam)
        for k, r in res.items():
            if isinstance(r, dict) and 'ratio_display' in r:
                print('  %-10s shadow/lit display p10 %.3f med %.3f p90 %.3f | linear %.3f | V %.2f | lit %s hue %3.0f -> cast %s hue %s S %s | region ratio %s' % (k, *r['ratio_display'], r['ratio_linear'], r['v_ratio'], r['lit'], r['hue_lit'], r.get('cast'), '%3.0f' % r['hue_cast'] if 'cast' in r else '-', '%.2f' % r['sat_cast'] if 'cast' in r else '-', '%.3f' % r['ratio_region_display'] if 'cast' in r else '-'))
        print('  edge width px', {k: round(x, 2) for k, x in res['edge_width_px'].items()}, '| sunny %.3f lit %.3f cast shadow %.3f of frame' % (res['sunny_share'], res['lit_share'], res['cast_shadow_share']))
    return res

if __name__ == '__main__':
    if sys.argv[1] == 'light':
        r = light(sys.argv[2], sys.argv[3]); json.dump(r, open(f'{sys.argv[2]}/{sys.argv[3]}_light.json', 'w'), indent=1)

# ----------------------------------------------------------------------------- bloom, heads, parallax, anchors
def _in(p, m=0): return m < p[0] < 720 - m and m < p[1] < 1280 - m and p[2] > 0

def bloom(d, cam, verbose=True):
    b = M.load(f'{d}/{cam}_bloom.png'); nb = M.load(f'{d}/{cam}_nobloom.png'); A = json.load(open(f'{d}/{cam}_anchors.json')); diff = np.abs(b - nb).max(2); res = dict(lamps=[], heads=[])
    yy, xx = np.mgrid[0:1280, 0:720]
    for i, p in enumerate(A['lamps']):
        if not _in(p, -40): continue
        r_b = 0.2 * 782.2 / p[2]; h = M.halo(b, (p[0], p[1]), r_max=int(r_b + 70))
        rr = np.hypot(xx - p[0], yy - p[1])
        # radius beyond which the bloom adds less than 2 levels / less than 10 percent of its peak outside the core
        prof = np.array([diff[(rr >= k) & (rr < k + 1)].mean() if ((rr >= k) & (rr < k + 1)).any() else 0 for k in range(int(r_b + 70))])
        core = int(round(r_b)); pk = prof[core:core + 4].max() if len(prof) > core + 4 else 0
        r10 = next((k for k in range(core, len(prof)) if prof[k] < 0.1 * pk), len(prof)); r2 = next((k for k in range(core, len(prof)) if prof[k] < 2 / 255), len(prof))
        res['lamps'].append(dict(lamp=i, px=[round(p[0]), round(p[1])], bulb_radius_px=r_b, core_px=h['core'], halo_10pct_px=h['halo'], bloom_added_peak=float(pk), bloom_r10_beyond_core=r10 - core, bloom_r2levels_beyond_core=r2 - core))
    for nm, hd in A['heads'].items():
        c = hd['center']; D = hd['D_px']
        if not _in(c): continue
        rr = np.hypot(xx - c[0], yy - c[1]); ring = (rr > 0.5 * D + 2) & (rr < 0.5 * D + 26); disc = rr < 0.22 * D
        res['heads'].append(dict(actor=nm, D_px=D, bloom_added_in_ring_mean_levels=float(diff[ring].mean() * 255), bloom_added_in_ring_max_levels=float(diff[ring].max() * 255), bloom_added_on_head_max_levels=float(diff[disc].max() * 255),
                                 fill_bloom=M.hexs(np.median(b[disc], axis=0)), fill_nobloom=M.hexs(np.median(nb[disc], axis=0))))
    if verbose:
        print('== bloom', cam)
        for r in res['lamps']: print('  lamp', {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
        for r in res['heads']: print('  head', {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
    return res

def heads(img_path, anchors, ids=None, names=None, verbose=True):
    """Head fill, ink and crescent as displayed; luminance of the set in a ring around each head (actor pixels excluded when ids are given)."""
    a = M.load(img_path); yy, xx = np.mgrid[0:1280, 0:720]; out = []
    for nm, hd in anchors['heads'].items():
        c = hd['center']; D = hd['D_px']
        if not _in(c): continue
        rr = np.hypot(xx - c[0], yy - c[1]); disc = rr < 0.46 * D; px = a[disc]; Y = M.luma(px)
        fill = np.median(px[Y > np.percentile(Y, 55)], axis=0)                      # the dominant bright value = the fill
        band = (rr > 0.40 * D) & (rr < 0.53 * D); pb = a[band]; Yb = M.luma(pb); ink = np.median(pb[Yb < np.percentile(Yb, 12)], axis=0)
        ring = (rr > 0.62 * D) & (rr < 0.95 * D)
        if ids is not None:
            act = np.isin(ids, [i for i, n in enumerate(names) if n.startswith('actor_')]); ring &= ~act
        wl = float(np.median(M.luma(a[ring])) * 255) if ring.sum() > 50 else None
        h, s, v = M.hsv(fill); out.append(dict(actor=nm, D_px=round(D, 1), center=[round(c[0]), round(c[1])], fill=M.hexs(fill), fill_V=round(v, 3), fill_S=round(s, 3), ink=M.hexs(ink), wall_luma_ring=wl))
    if verbose:
        for o in out: print('  head', o)
    return out

def parallax(d, cam, verbose=True):
    J = json.load(open(f'{d}/{cam}_parallax.json')); a0 = cv2.imread(f'{d}/{cam}_p0.png'); a1 = cv2.imread(f'{d}/{cam}_p1.png'); g0 = cv2.cvtColor(a0, cv2.COLOR_BGR2GRAY); g1 = cv2.cvtColor(a1, cv2.COLOR_BGR2GRAY)
    pts = {}
    for k in ('map_center', 'map_ny', 'hero_mark', 'boss_mark', 'near_mark'): pts[k] = (J['p0'][k], J['p1'][k])
    for i, (p, q) in enumerate(zip(J['p0']['lamps'], J['p1']['lamps'])): pts['lamp%d' % i] = (p, q)
    for nm in J['p0']['heads']: pts['head_' + nm] = (J['p0']['heads'][nm]['center'], J['p1']['heads'][nm]['center'])
    rows = []
    for k, (p, q) in pts.items():
        if not (_in(p, 36) and _in(q, 36)): continue
        x, y = int(round(p[0])), int(round(p[1])); t = g0[y - 30:y + 31, x - 30:x + 31]; r = cv2.matchTemplate(g1, t, cv2.TM_CCOEFF_NORMED)
        # search near the predicted place only (repeating wallpaper would match anywhere)
        px_, py_ = int(round(q[0])) - 30, int(round(q[1])) - 30; x0, x1, y0, y1 = max(0, px_ - 25), min(r.shape[1], px_ + 26), max(0, py_ - 25), min(r.shape[0], py_ + 26)
        sub = r[y0:y1, x0:x1]; j, i = np.unravel_index(np.argmax(sub), sub.shape); mx = x0 + i + 30; my = y0 + j + 30
        rows.append(dict(anchor=k, depth=round(p[2], 2), predicted_shift=[round(q[0] - p[0], 1), round(q[1] - p[1], 1)], measured_shift=[int(mx - x), int(my - y)], ncc=round(float(sub.max()), 3)))
    # can one 2D similarity (zoom + pan + roll) explain the pair?
    orb = cv2.ORB_create(4000); k0, d0 = orb.detectAndCompute(g0, None); k1, d1 = orb.detectAndCompute(g1, None)
    m = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d0, d1); P0 = np.float32([k0[x.queryIdx].pt for x in m]); P1 = np.float32([k1[x.trainIdx].pt for x in m])
    Mt, inl = cv2.estimateAffinePartial2D(P0, P1, method=cv2.RANSAC, ransacReprojThreshold=3.0); F, inlF = cv2.findFundamentalMat(P0, P1, cv2.FM_RANSAC, 1.5, 0.99)
    res = dict(rows=rows, matches=len(m), similarity_inlier_ratio=float(inl.mean()), fundamental_inlier_ratio=float(inlF.mean()) if inlF is not None else None,
               shift_range_px=[min(abs(r['predicted_shift'][0]) for r in rows), max(abs(r['predicted_shift'][0]) for r in rows)])
    if verbose:
        print('== parallax', cam, '(camera moved 0.5 D to its right)')
        for r in rows: print('  ', r)
        print('   ORB matches %d: one 2D similarity explains %.0f%% of them (3 px), a fundamental matrix %.0f%%' % (len(m), 100 * res['similarity_inlier_ratio'], 100 * (res['fundamental_inlier_ratio'] or 0)))
    return res

def overlay(img_path, A, out, title=''):
    """Draw the projected anchors on a render: track polyline, N.Y. rect, marks, poles with predicted shadow tips, head-shadow predictions, VPs and horizon."""
    im = cv2.imread(img_path); c = lambda p: (int(round(p[0])), int(round(p[1])))
    tr = [c(p) for p in A['map_track']]
    for p in tr[::4]: cv2.circle(im, p, 3, (255, 255, 0), 1, cv2.LINE_AA)
    cv2.circle(im, c(A['map_storm']), 9, (0, 255, 0), 2, cv2.LINE_AA); cv2.putText(im, 'map_storm', (c(A['map_storm'])[0] + 10, c(A['map_storm'])[1] + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.circle(im, c(A['map_ny']), 9, (0, 255, 255), 2, cv2.LINE_AA); cv2.putText(im, 'map_ny', (c(A['map_ny'])[0] + 10, c(A['map_ny'])[1] - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.polylines(im, [np.int32([c(p) for p in A['ny_label_rect']])], True, (255, 0, 255), 1, cv2.LINE_AA); cv2.polylines(im, [np.int32([c(p) for p in A['map_rect']])], True, (0, 255, 0), 1, cv2.LINE_AA)
    for k, col in (('hero_mark', (255, 128, 0)), ('boss_mark', (0, 128, 255)), ('near_mark', (0, 0, 255))):
        pl = A['poles'][k]
        if pl['base'][2] <= 0: continue
        cv2.drawMarker(im, c(pl['base']), col, cv2.MARKER_CROSS, 18, 2, cv2.LINE_AA); cv2.putText(im, k, (c(pl['base'])[0] + 8, c(pl['base'])[1] + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, col, 1, cv2.LINE_AA)
        cv2.line(im, c(pl['base']), c(pl['top']), col, 1, cv2.LINE_AA); cv2.arrowedLine(im, c(pl['top']), c(pl['shadow_tip']), (255, 255, 255), 1, cv2.LINE_AA, tipLength=0.12)
    for nm, hd in A.get('heads', {}).items():
        if hd['center'][2] > 0:
            cv2.circle(im, c(hd['center']), int(hd['D_px'] / 2), (0, 255, 0), 1, cv2.LINE_AA)
            s = hd['shadow_on_map_plane']; cv2.circle(im, c(s), max(4, int(782.2 / s[2] / 2)), (255, 255, 255), 1, cv2.LINE_AA); cv2.arrowedLine(im, c(hd['center']), c(s), (255, 255, 255), 1, cv2.LINE_AA, tipLength=0.08)
    ci = A['cam']
    if ci.get('horizon_y') is not None and 0 <= ci['horizon_y'] < 1280: cv2.line(im, (0, int(ci['horizon_y'])), (720, int(ci['horizon_y'])), (0, 200, 255), 1, cv2.LINE_AA); cv2.putText(im, 'horizon', (6, int(ci['horizon_y']) - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1, cv2.LINE_AA)
    v = ci.get('vp_y')
    if v and v[2] > 0:
        cv2.drawMarker(im, c(v), (0, 200, 255), cv2.MARKER_TILTED_CROSS, 22, 2, cv2.LINE_AA)
        for fx in (-3.0, -1.2, 1.2, 3.0): pass
    cv2.putText(im, title, (6, 1270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imwrite(out, im); return out

if __name__ == '__main__' and sys.argv[1] in ('bloom', 'parallax', 'heads'):
    if sys.argv[1] == 'bloom': json.dump(bloom(sys.argv[2], sys.argv[3]), open(f'{sys.argv[2]}/{sys.argv[3]}_bloomres.json', 'w'), indent=1)
    if sys.argv[1] == 'parallax': json.dump(parallax(sys.argv[2], sys.argv[3]), open(f'{sys.argv[2]}/{sys.argv[3]}_parallaxres.json', 'w'), indent=1)
    if sys.argv[1] == 'heads':
        d, cam = sys.argv[2], sys.argv[3]; z = np.load(f'{d}/{cam}_ids.npz', allow_pickle=True); ids = cv2.resize(z['ids'], (720, 1280), interpolation=cv2.INTER_NEAREST)
        json.dump(heads(f'{d}/{cam}_graded.png', json.load(open(f'{d}/{cam}_anchors.json')), ids, list(z['names'])), open(f'{d}/{cam}_heads.json', 'w'), indent=1)

def measured_vp(img_path, predicted=None, band=None, iters=4000, seed=1):
    """Dominant vanishing point of the straight lines in a render (Canny + probabilistic Hough + RANSAC over line pairs).
    band = (y0, y1) restricts the lines to image rows (e.g. the floor). Returns (x, y, inliers, lines)."""
    im = cv2.imread(img_path); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); ed = cv2.Canny(g, 50, 130)
    if band: ed[:band[0]] = 0; ed[band[1]:] = 0
    ls = cv2.HoughLinesP(ed, 1, np.pi / 360, 60, minLineLength=70, maxLineGap=6)
    if ls is None: return None
    L = []
    for x1, y1, x2, y2 in ls.reshape(-1, 4):
        a = np.degrees(np.arctan2(y2 - y1, x2 - x1)) % 180
        if a < 8 or a > 172 or abs(a - 90) < 2: continue          # horizontals and exact verticals carry no information about this point
        l = np.cross([x1, y1, 1.0], [x2, y2, 1.0]); L.append(l / np.hypot(l[0], l[1]))
    L = np.array(L); rng = np.random.RandomState(seed); best = (0, None)
    for _ in range(iters):
        i, j = rng.randint(0, len(L), 2)
        p = np.cross(L[i], L[j])
        if abs(p[2]) < 1e-9: continue
        p = p / p[2]; d = np.abs(L @ p); n = int((d < 2.5).sum())
        if n > best[0]: best = (n, p)
    n, p = best; inl = np.abs(L @ p) < 2.5; A = L[inl][:, :2]; b = -L[inl][:, 2]; q = np.linalg.lstsq(A, b, rcond=None)[0]
    return float(q[0]), float(q[1]), int(inl.sum()), len(L)

if __name__ == '__main__' and sys.argv[1] == 'vp':
    d = sys.argv[2]; J = json.load(open(f'{d}/cams.json'))
    for cam, band in (('eye_two_shot', (880, 1280)), ('high_two_shot', (700, 1280)), ('low_medium', (0, 330)), ('desk_fg', (900, 1280)), ('wide_high', (700, 1280)), ('high_steep', (560, 1280)), ('low_rake', (0, 420))):
        r = measured_vp(f'{d}/staged_{cam}.png', band=band); v = J[cam]['cam']['vp_y']
        print('%-14s vanishing point measured on the render (%6.0f, %6.0f) from %3d of %3d lines in rows %s | from the camera matrix (%6.0f, %6.0f) | difference %5.1f px' % (cam, r[0], r[1], r[2], r[3], band, v[0], v[1], np.hypot(r[0] - v[0], r[1] - v[1])))
