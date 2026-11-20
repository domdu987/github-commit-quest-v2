"""make_contact.py : contact.jpg = one 720x1280 FINAL (placeholder actors at the stand points) per camera / light / hook state (SITE + TOWER here, CAFE + RESTO from int20.TILES), label UNDER each tile,
cyan line at y 880, plus per-tile cost, head pixels, luma bands + hue shares (hue_report.txt) and the render cost (cost_report.txt).
usage:  python3 make_contact.py run [name ...]      render the missing tiles (WORKERS processes, 2 threads each) then the sheet
        python3 make_contact.py tile NAME            render one tile (final/NAME.png + .json)
        python3 make_contact.py sheet                contact.jpg + contact_small.jpg + hue_report.txt + cost_report.txt from final/*.json
        python3 make_contact.py list                 tile names
int20.TILES (optional, interior builder): [(name, preset, light, hooks_code, label, camera_name_or_None[, extras_code])], hooks_code is exec'd after build with S (set3d20), A, bpy in scope."""
import os, sys, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FINAL = os.path.join(HERE, 'work', 'final'); os.makedirs(FINAL, exist_ok=True)
WORKERS = int(os.environ.get('WORKERS', '2'))
CR = "S.project((%.3f, %.3f, %.3f))"
TILES = [   # name, preset, light, hooks, label, camera (None = preset camera), extras
    ('S01_site_wide_stage0', 'site_wide', 'DAY', '', 'site_wide / DAY stage 0 (high crane start)', None, "site_extras(A)"),
    ('S02_site_wide_end', 'site_wide', 'DAY', '', 'site_wide_end / DAY stage 0 (crane down)', 'site_wide_end', ""),
    ('S03_site_table', 'site_table', 'DAY', '', 'site_table / DAY (Eiffel at the plan table)', None, ""),
    ('S04_site_leg_low', 'site_leg_low', 'DAY', '', 'site_leg_low / DAY (tilt up the scaffolded leg)', None, ""),
    ('S05_site_fence', 'site_fence', 'DAY', '', 'site_fence / DAY (Parisians at the fence)', None, ""),
    ('S06_site_girders', 'site_girders', 'DAY', 'S.crane_swing(0.5)', 'site_girders / DAY stage 1 (crane swing 0.5)', None, ""),
    ('S07_site_rivet', 'site_rivet', 'DAY', 'S.spark(3, t0=0); S.rivet_toss(0.5)', 'site_rivet / DAY stage 1 (spark + rivet toss hooks)', None, ""),
    ('S08_site_rise_snap1', 'site_rise', 'DAY', 'S.set_stage(1)', 'site_rise snap 1 (stage 1)', 'site_rise_snap1', ""),
    ('S09_site_rise_snap2', 'site_rise', 'DAY', 'S.set_stage(2)', 'site_rise snap 2 (stage 2)', 'site_rise_snap2', ""),
    ('S10_site_rise_snap3', 'site_rise', 'DAY', 'S.set_stage(3)', 'site_rise snap 3 (stage 3, finished spire)', 'site_rise_snap3', ""),
    ('S11_site_bigzoom_start', 'site_bigzoom_start', 'DAY', '', 'site_bigzoom_start / DAY stage 0 (extreme wide, 47 deg down, shift +0.37)', None, ""),
    ('S12_site_bigzoom_mid', 'site_bigzoom_start', 'DAY', '', 'site_bigzoom_mid / DAY stage 0 (over the roofs and scaffolds)', 'site_bigzoom_mid', ""),
    ('S13_site_bigzoom_land', 'site_bigzoom_start', 'DAY', '', 'site_bigzoom_land / DAY stage 0 (medium on Eiffel at the plan table, 40 mm)', 'site_bigzoom_land', ""),
    ('T01_tower_low_DAY', 'tower_low', 'DAY', '', 'tower_low / DAY 1889 (shot 1)', None, ""),
    ('T02_tower_fair_DAY', 'tower_fair', 'DAY', '', 'tower_fair / DAY 1889 (shots 15)', None, ""),
    ('T03_tower_fair_1910', 'tower_fair', 'DAY', 'S.set_year(1910); S.set_crowd(2)', 'tower_fair / DAY 1910 (shot 23)', None, ""),
    ('T04_tower_dusk_DUSK', 'tower_dusk', 'DUSK', '', 'tower_dusk / DUSK 1909 (shot 18)', None, "tower_extras(A)"),
    ('T05_tower_dusk_NIGHT', 'tower_dusk', 'NIGHT', '', 'tower_dusk / NIGHT 1909 (shot 22)', None, ""),
    ('T06_tower_dusk_summit', 'tower_dusk_summit', 'DUSK', '', 'tower_dusk_summit / DUSK (start on the summit, wires)', None, ""),
    ('T07_tower_dusk_summit_end', 'tower_dusk_summit', 'DUSK', '', 'tower_dusk_summit_end / DUSK (whip-tilt end: the hut)', 'tower_dusk_summit_end', ""),
    ('T08_tower_hut', 'tower_hut', 'DUSK', 'S.spark_gap(False)', 'tower_hut / DUSK (inside the hut, gap off)', None, ""),
    ('T09_tower_hut_spark', 'tower_hut', 'DUSK', 'S.spark_gap(True)', 'tower_hut / DUSK (spark_gap on)', None, ""),
    ('T10_tower_night_wide', 'tower_night_wide', 'NIGHT', 'S.signal_rings(0.45); S.wire_glow(0.9)', 'tower_night_wide / NIGHT (rings 0.45, wire_glow 0.9)', None, ""),
    ('T11_tower_night_summit', 'tower_night_wide', 'NIGHT', 'S.signal_rings(0.2); S.wire_glow(0.5)', 'tower_night_summit / NIGHT (whip pull-out start)', 'tower_night_summit', ""),
    ('T12_tower_window_pull', 'tower_window_pull', 'DAY', '', 'tower_window_pull / DAY 1889 (start at the lit window)', None, ""),
    ('T13_tower_window_end', 'tower_window_pull', 'DAY', 'bpy.context.scene.view_settings.exposure = -0.55', 'tower_window_end / DAY 1889 (crash pull-out end)', 'tower_window_end', ""),
    ('T15_tower_window_in', 'tower_window_pull', 'DAY', '', 'tower_window_in / DAY 1889 (landing pose of the zoom, 55 mm through the clear pane)', 'tower_window_in', ""),
    ('T14_tower_dusk_chars', 'tower_dusk', 'DUSK', '', 'tower_dusk_chars / DUSK 1909 (shot 18 staging camera)', 'tower_dusk_chars', ""),
]
def interior_tiles():
    try:
        import int20
        return list(getattr(int20, 'TILES', []))
    except Exception as e:
        return []
def all_tiles(): return TILES + interior_tiles()
def by_name(n): return {t[0]: t for t in all_tiles()}[n]

def site_extras(A, S, bpy):
    """SITE numbers at site_wide: crane height px, scaffold height / leg height, worker px"""
    import kit20 as K, core20 as C
    out = {}
    sx, sy = 1, -1; z = K.S_TOPS[0]; px, py = sx * (K.tw(z) - K.th(z) * 0.2), sy * (K.tw(z) - K.th(z) * 0.2)
    a = S.project(C.W((px, py, z))); b = S.project(C.W((px, py, z + 19.0)))
    out['crane_px'] = abs(a[1] - b[1]); out['scaffold_over_leg'] = round(36.0 / z, 2)
    hp = S.head_pixels(A['cam_name']); body = [abs(h[5] - (h[2] - h[3] / 2.0)) for h in hp]
    out['workers'] = len(hp); out['workers_body_px'] = [int(b_) for b_ in body]; out['workers_ge60'] = int(sum(1 for b_ in body if b_ >= 60))
    return out
def tower_extras(A, S, bpy):
    return {}

def do_tiles(names):
    """tiles that share (preset, light) are rendered by ONE process: build once, then per tile: hooks, camera, staging, render, stats"""
    import bpy, set3d20 as S, core20 as C, hue20
    t0 = by_name(names[0]); A = S.build(t0[1], t0[2]); sc = bpy.context.scene; S.setup_render(sc, 'final')
    for name in names:
        t = by_name(name); nm_, preset, light, hooks, label, camname = t[:6]; extras = t[6] if len(t) > 6 else ''
        exec(hooks, dict(S=S, A=A, bpy=bpy, C=C))
        cn = camname or A['cam_name']; cs = A['cams'][cn]; S.make_camera(cs)
        cn_s = cn if cn in A.get('staging', {}) and A['staging'][cn] else A['cam_name'] if (cn not in A.get('staging', {})) else cn
        S.stage_placeholders(A, cn_s, cs['loc']); bpy.context.view_layer.update(); hp = S.head_pixels(cn_s)
        png = os.path.join(FINAL, name + '.png'); w, c = S.render(png)
        ex = {}
        if extras:
            try: ex = eval(extras, dict(site_extras=lambda A_: site_extras(A_, S, bpy), tower_extras=lambda A_: tower_extras(A_, S, bpy), A=A))
            except Exception as e: ex = dict(extras_error=str(e))
        stats = image_stats(png); stats.update(sky_share(sc, png))
        try: hue = hue20.measure(png)
        except Exception as e: hue = dict(shade_hue=None, magenta=0.0, ok=True, cast_pct=0.0, in_band=None, error=str(e))
        json.dump(dict(name=name, label=label, preset=preset, light=light, cam=cn, wall=round(w, 1), cpu=round(c, 1), samples=sc.cycles.samples, heads=hp, hue=hue, stats=stats, extras=ex, load=os.getloadavg()[0]), open(os.path.join(FINAL, name + '.json'), 'w'))
        print('%s: %.1f s wall, %.1f s cpu, heads %s, hue %s' % (name, w, c, hp, hue), flush=True)

def groups_of(names):
    g = {}
    order = []
    for n in names:
        t = by_name(n); k = (t[1], t[2])
        if k not in g: g[k] = []; order.append(k)
        g[k].append(n)
    return [g[k] for k in order]

def image_stats(png):
    import numpy as np
    from PIL import Image
    im = Image.open(png).convert('RGB'); a = np.asarray(im, dtype=np.float32) / 255.0; L = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) * 255; H, W_ = L.shape
    hsv = np.asarray(im.convert('HSV'), dtype=np.float32); h = hsv[..., 0] * 360 / 255; s = hsv[..., 1] / 255; v = hsv[..., 2] / 255
    ch = (s > 0.25) & (v > 0.1); nch = max(1, ch.sum())
    red = ch & ((h >= 345) | (h <= 30)); blue = ch & (h >= 190) & (h <= 265); mag = ch & (h >= 290) & (h < 345)
    return dict(top8=round(float(L[:H // 8].mean()), 1), mid=round(float(L[3 * H // 8:5 * H // 8].mean()), 1), bot8=round(float(L[7 * H // 8:].mean()), 1), v95=round(float((v > 0.95).mean()), 3), dark=round(float((v < 0.25).mean()), 3),
                sat=round(float(s.mean()), 2), red=round(float(red.sum() / nch * 100), 1), blue=round(float(blue.sum() / nch * 100), 1), magenta_ch=round(float(mag.sum() / nch * 100), 1), luma_p1=round(float(np.percentile(L, 1)), 1))

def sky_share(sc, png):
    """share of the frame that is open sky: alpha of a cheap transparent render, once without and once with the clouds"""
    import bpy, numpy as np
    from PIL import Image
    r = sc.render; cy = sc.cycles; sv = dict(pct=r.resolution_percentage, fp=r.filepath, ft=r.film_transparent, cm=r.image_settings.color_mode, comp=r.use_compositing, den=cy.use_denoising, sm=cy.samples)
    r.resolution_percentage = 20; r.film_transparent = True; r.image_settings.color_mode = 'RGBA'; r.use_compositing = False; cy.use_denoising = False; cy.samples = 1
    res = {}
    for tag, hide in (('sky_open', True), ('sky_noclouds_hidden', False)):
        cl = [o for o in bpy.data.objects if o.name.startswith(('clouds', 'stars'))]
        for o in cl: o.hide_render = hide
        p = png[:-4] + '_a.png'; r.filepath = p; bpy.ops.render.render(write_still=True); a = np.asarray(Image.open(p).convert('RGBA'))[..., 3]; os.remove(p)
        res['sky_with_clouds' if hide is False else 'sky_without_clouds'] = round(float((a < 128).mean() * 100), 1)
        for o in cl: o.hide_render = False
    r.resolution_percentage = sv['pct']; r.filepath = sv['fp']; r.film_transparent = sv['ft']; r.image_settings.color_mode = sv['cm']; r.use_compositing = sv['comp']; cy.use_denoising = sv['den']; cy.samples = sv['sm']
    return res

def sheet():
    from PIL import Image, ImageDraw, ImageFont
    W, H, LB, Cn = 720, 1280, 84, 6
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 25); F2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    have = [t for t in all_tiles() if os.path.exists(os.path.join(FINAL, t[0] + '.png')) and os.path.exists(os.path.join(FINAL, t[0] + '.json'))]; rows = (len(have) + Cn - 1) // Cn
    S = Image.new('RGB', (W * Cn, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S); lines = []; cost = []
    for i, t in enumerate(have):
        js = json.load(open(os.path.join(FINAL, t[0] + '.json'))); im = Image.open(os.path.join(FINAL, t[0] + '.png')).convert('RGB'); x, y = (i % Cn) * W, (i // Cn) * (H + LB)
        S.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2)
        h = js['hue']; st = js['stats']; hs = 'shade hue %s mag %.1f%%' % (h.get('shade_hue'), h.get('magenta', 0))
        d.text((x + 10, y + H + 4), t[4][:62], fill=(235, 235, 235), font=F)
        d.text((x + 10, y + H + 34), '%s | luma %s/%s/%s | %.0f cpu s' % (hs, st['top8'], st['mid'], st['bot8'], js['cpu']), fill=(170, 210, 255), font=F2)
        if 'sky_without_clouds' in st: d.text((x + 10, y + H + 58), 'sky open %.0f%% (%.0f%% with clouds counted as sky) | v>.95 %.1f%%' % (st['sky_without_clouds'], st['sky_with_clouds'], st['v95'] * 100), fill=(200, 200, 170), font=F2)
        interior = t[1].startswith(('cafe_', 'resto_'))
        lines.append('%-26s %-6s shade-hue(cast px) %-6s median %-6s in 225-265 %-6s cast %5.1f%% | magenta(frame) %5.2f%% | luma top/mid/bottom-eighth %s/%s/%s | V>.95 %.3f dark %.3f sat %s | chroma share red %s blue %s magenta %s | sky open %s%% (clouds as sky %s%%) | %s%s' % (
            t[0], t[2], h.get('shade_hue'), h.get('median'), h.get('in_band'), h.get('cast_pct', 0), h.get('magenta', 0), st['top8'], st['mid'], st['bot8'], st['v95'], st['dark'], st['sat'], st['red'], st['blue'], st['magenta_ch'],
            st.get('sky_without_clouds', '-'), st.get('sky_with_clouds', '-'), ('OK' if h.get('ok') else ('warm interior shade (see QA note)' if interior else 'CHECK')), (' | ' + json.dumps(js['extras'])) if js.get('extras') else ''))
        cost.append('%-26s %6.1f cpu s  %6.1f wall s  %d spp  heads(role, y, px, chin, feet) %s' % (t[0], js['cpu'], js['wall'], js['samples'], [(a[0], a[2], a[3], a[4], a[5]) for a in js['heads']]))
    S.save(os.path.join(HERE, 'contact.jpg'), quality=86); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_small.jpg'), quality=86)
    open(os.path.join(HERE, 'hue_report.txt'), 'w').write('hue per tile: cast-shadow hue (method of styleboard/hue_check.py; outdoors band 225-265, client shade 240-260), magenta share of the frame (limit 10 %), luma bands, chroma shares, open sky share\n' + '\n'.join(lines) + '\n')
    open(os.path.join(HERE, 'cost_report.txt'), 'w').write('CPU seconds of the final 720x1280 render call per tile (%d worker process(es), 2 threads each; the one-off build per process is 10-40 s and not counted)\n' % WORKERS + '\n'.join(cost) + '\n')
    print(S.size, len(have)); print('\n'.join(lines)); print('\n'.join(cost))

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sheet'; args = sys.argv[2:]
    if cmd == 'tile': do_tiles(args)
    elif cmd == 'list': print('\n'.join(t[0] for t in all_tiles()))
    elif cmd == 'run':
        names = args or [t[0] for t in all_tiles()]; force = os.environ.get('FORCE')
        todo = [n for n in names if force or not os.path.exists(os.path.join(FINAL, n + '.json'))]
        procs = []; q = groups_of(todo)
        while q or procs:
            procs = [p for p in procs if p.poll() is None]
            while q and len(procs) < WORKERS:
                n = q.pop(0); print('start', n, flush=True); procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), 'tile'] + n, stdout=open(os.path.join(FINAL, n[0] + '.log'), 'w'), stderr=subprocess.STDOUT))
            time.sleep(2)
        sheet()
    else: sheet()
