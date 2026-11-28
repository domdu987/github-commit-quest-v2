#!/usr/bin/env python3
"""prove.py : the light review of office_light.py.  Writes everything to proof/.

    python3 prove.py stills [scale]     # 3 presets x 5 cameras, two stage actors (hero, boss), 12 samples, 2 threads -> proof/stills/
    python3 prove.py strips             # flash strip (office_storm, eye_two_shot), rain card at 4 times (grey, storm) -> proof/strips/
    python3 prove.py identity           # office_day after grey -> storm -> day is bit-identical to a fresh build -> proof/identity.json
    python3 prove.py timing [threads]   # final 720x1280 12-sample frames per preset (eye_two_shot, two actors) -> proof/timing.json
    python3 prove.py measure            # head fill / ink, wall ring luminance, hue_report rows -> proof/measure.json (no bpy needed for the hue part)
    python3 prove.py sheets             # proof/compare.jpg, proof/flash_strip.jpg, proof/rain_strip.jpg"""
import os, sys, json, time, math, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE)); PROJ = os.path.dirname(V3)
OUT = os.path.join(HERE, 'proof')
CAMS = ['eye_two_shot', 'low_medium', 'insert_rake', 'high_two_shot', 'wide_high']
PRESETS = ['office_day', 'office_grey', 'office_storm']
REFS = {'eye_two_shot': 'b/t07.0', 'low_medium': 'a/t27.5', 'insert_rake': 'a/t32.0', 'high_two_shot': 'b/t24.5', 'wide_high': 'b/t18.5'}


def _bpy_setup():
    for p in (HERE, os.path.join(V3, 'stage'), os.path.join(V3, 'set3d')):
        if p not in sys.path: sys.path.insert(0, p)
    import bpy  # noqa
    import office_light as OL
    import actors, sprites, render  # noqa
    return bpy, OL, OL.S, actors, sprites, render


def staging(cam):
    """two stage actors: hero and chief.  Two-shot cameras: chief far at boss_mark, hero near at near_mark (the hook's take-B
    staging, turned to face the chief); low_medium: both at the wall; insert_rake: no actors (the map insert)."""
    if cam == 'insert_rake': return None
    if cam == 'low_medium': return dict(hero=((-0.55, -0.42, 0.0), False), boss=((1.30, -0.42, 0.0), False))
    return dict(hero=((2.6, -1.95, 0.0), True), boss=((1.30, -0.42, 0.0), False))


HERO_POSE = dict(yaw=0.6, expr='sad', arm_l='down', arm_r='down', legs='stand', head_roll=-4.0)
BOSS_POSE = dict(yaw=-0.5, expr='smug', arm_r='hip', arm_l='down', legs='stand', head_roll=-4.0)


class Rig:
    def __init__(self, sprite_dir):
        self.bpy, self.OL, self.S, self.actors, self.sprites, self.render = _bpy_setup()
        bpy, S = self.bpy, self.S
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.A = S.build('INTERIOR_DAY'); self.sc = sc = bpy.context.scene
        sc.render.use_persistent_data = False; sc.cycles.transparent_max_bounces = 12; S.set_track(1.0, 0.0)
        self.cam = S.make_camera(self.A['cams']['eye_two_shot'], name='cam'); self.cam.data.clip_start = 0.02
        self.hero = self.actors.Actor('hero', 'hero'); self.boss = self.actors.Actor('boss', 'boss')
        self.hero.build(self.sprites.DEFAULT_CANVAS['hero'], sprite_dir, contact=True)
        self.boss.build(self.sprites.DEFAULT_CANVAS['boss'], sprite_dir, contact=True)
        self.hero.head_flip = self.boss.head_flip = True
        self.frame = 0

    def set_cam(self, name, frame):
        """one Blender frame per camera so every staging has its own keyed placement and sprite."""
        S, bpy = self.S, self.bpy
        st = staging(name); cs = self.A['cams'][name]
        self.camrig_key(frame, cs)
        if st is None:
            for a in (self.hero, self.boss): a.place(frame, (0.0, 20.0, -50.0))      # parked far outside the room
        else:
            self.hero.place(frame, st['hero'][0], flip=st['hero'][1]); self.boss.place(frame, st['boss'][0], flip=st['boss'][1])
        self.sc.frame_set(frame)
        self.hero.pose(frame, HERO_POSE, camera=self.cam); self.boss.pose(frame, BOSS_POSE, camera=self.cam)
        return st

    def camrig_key(self, frame, cs):
        import camrig
        camrig.key_camera(frame, cs['loc'], cs['look_at'], cam=self.cam, interp='CONSTANT')

    def sprites_out(self, frames):
        self.hero.render_sprites(256, frames=frames); self.boss.render_sprites(256, frames=frames)

    def heads(self, frame):
        out = {}
        for nm, a in (('hero', self.hero), ('boss', self.boss)):
            x, y, d = self.actors.local_to_screen(a, self.cam, (0.0, 0.0), frame)
            out[nm] = dict(center=(x, y), D_px=782.2 / d, depth=d)
        return out

    def _alpha(self, ob, loc, fi, dg, frame):
        """alpha of the actor sprite of `frame` at a hit point of its card (the card shows an image sequence)."""
        import numpy as np
        from PIL import Image
        from mathutils.interpolate import poly_3d_calc
        a = self.hero if ob.name.startswith('hero') else self.boss
        key = (a.name, frame); cache = self.__dict__.setdefault('_acache', {})
        if key not in cache: cache[key] = np.asarray(Image.open(a.sprite_path(frame)).convert('RGBA'))[:, :, 3].astype(np.float32) / 255
        A = cache[key]; me = ob.evaluated_get(dg).data; poly = me.polygons[fi]; uvl = me.uv_layers.active.data
        co = [ob.matrix_world @ me.vertices[v].co for v in poly.vertices]; w = poly_3d_calc(co, loc)
        u = sum(wi * uvl[li].uv.x for wi, li in zip(w, poly.loop_indices)); v = sum(wi * uvl[li].uv.y for wi, li in zip(w, poly.loop_indices))
        if not (0 <= u <= 1 and 0 <= v <= 1): return 0.0
        return float(A[min(A.shape[0] - 1, int((1 - v) * A.shape[0])), min(A.shape[1] - 1, int(u * A.shape[1]))])

    def actor_mask(self, frame, pts):
        """for screen points (x, y) in 720x1280 units: True where the first opaque hit is an actor card."""
        from mathutils import Vector
        bpy, S = self.bpy, self.S
        self.sc.frame_set(frame); self.actors.sync_all(self.sc, self.cam)
        dg = bpy.context.evaluated_depsgraph_get(); M = self.cam.matrix_world; o0 = M.to_translation(); R = M.to_3x3()
        res = []
        for (x, y) in pts:
            d = (R @ Vector(((x - 360.0) / 782.2, -(y - 640.0) / 782.2, -1.0))).normalized(); o = o0.copy(); hit_actor = False
            for _ in range(12):
                hit, loc, nrm, fi, ob, mw = self.sc.ray_cast(dg, o, d, distance=80.0)
                if not hit: break
                src = ob.original
                if src.name.endswith(('_shadow', '_contact')) or not src.visible_camera or src.hide_render: o = loc + d * 1e-4; continue
                if src.name.endswith('_card'):
                    if self._alpha(src, loc, fi, dg, frame) < 0.5: o = loc + d * 1e-4; continue
                    hit_actor = True
                break
            res.append(hit_actor)
        return res


def cmd_stills(scale=1.0, samples=12):
    sd = os.path.join(OUT, 'sprites'); os.makedirs(os.path.join(OUT, 'stills'), exist_ok=True)
    R = Rig(sd); bpy, S, OL = R.bpy, R.S, R.OL
    meta = {}
    for i, c in enumerate(CAMS): R.set_cam(c, i + 1)
    R.sprites_out(list(range(1, len(CAMS) + 1)))
    for i, c in enumerate(CAMS): meta[c] = dict(frame=i + 1, heads=R.heads(i + 1) if staging(c) else {})
    json.dump(meta, open(os.path.join(OUT, 'stills', 'staging.json'), 'w'), indent=1)
    R.sc.cycles.samples = samples
    for pr in PRESETS:
        OL.apply(pr); OL.tint_cards()
        for i, c in enumerate(CAMS):
            out = os.path.join(OUT, 'stills')
            res = R.render.render_frames([i + 1], out, scale=scale, threads=2, scene=R.sc, camera=R.cam, prefix='tmp_', verbose=False)
            os.replace(os.path.join(out, 'tmp_%04d.png' % (i + 1)), os.path.join(out, '%s_%s.png' % (pr, c)))
            print(pr, c, '%.1f s' % res[0]['wall'], flush=True)


def cmd_strips():
    sd = os.path.join(OUT, 'sprites'); od = os.path.join(OUT, 'strips'); os.makedirs(od, exist_ok=True)
    R = Rig(sd); S, OL = R.S, R.OL
    R.set_cam('eye_two_shot', 1); R.sprites_out([1])
    R.sc.cycles.samples = 12
    OL.apply('office_storm'); OL.tint_cards()
    # lightning: the default 3-frame pulse keyed on Blender frames 2..4, 0 on frame 5; frames 1..6 rendered as a strip
    for f in range(2, 7): R.set_cam('eye_two_shot', f)
    R.sprites_out(list(range(2, 7)))
    OL.flash(0.0, 1); OL.lightning(2)
    for f in range(1, 7):
        R.render.render_frames([f], od, scale=0.5, threads=2, scene=R.sc, camera=R.cam, prefix='tmp_', verbose=False)
        os.replace(os.path.join(od, 'tmp_%04d.png' % f), os.path.join(od, 'flash_%d.png' % f)); print('flash', f, OL.state()['flash'], flush=True)
    # rain on the window at 4 times of the loop (frames 1, 25, 49, 73), grey and storm, from a camera at the window
    OL.flash(0.0, 1); OL._clear_keys(OL._ctl(), 'flash'); OL.flash(0.0)
    win = dict(loc=(1.3, -4.75, 2.45), look_at=(3.8, -4.6, 2.7), lens=22)
    for f in (1, 25, 49, 73):
        import camrig
        camrig.key_camera(100 + f, win['loc'], win['look_at'], cam=R.cam, interp='CONSTANT')
        for a in (R.hero, R.boss): a.place(100 + f, (0.0, 20.0, -50.0)); a.pose(100 + f, HERO_POSE if a is R.hero else BOSS_POSE, camera=R.cam)
    R.sprites_out([101, 125, 149, 173])
    for pr in ('office_grey', 'office_storm'):
        OL.apply(pr)
        for f in (1, 25, 49, 73):
            R.render.render_frames([100 + f], od, scale=0.5, threads=2, scene=R.sc, camera=R.cam, prefix='tmp_', verbose=False)
            os.replace(os.path.join(od, 'tmp_%04d.png' % (100 + f)), os.path.join(od, 'rain_%s_%02d.png' % (pr, f))); print('rain', pr, f, flush=True)


def cmd_identity():
    """office_day rendered after a fresh build, and again after grey -> storm (with a flash and rain keyed) -> day."""
    import numpy as np
    from PIL import Image
    bpy, OL, S, actors, sprites, render = _bpy_setup()
    od = os.path.join(OUT, 'identity'); os.makedirs(od, exist_ok=True)
    A = S.build('INTERIOR_DAY'); sc = bpy.context.scene; S.setup_render(sc, 'preview'); sc.render.threads = 2; S.set_track(1.0, 0.0)
    res = {}
    for c in ('eye_two_shot', 'insert_rake'):
        S.make_camera(A['cams'][c]); S.render(os.path.join(od, 'fresh_%s.png' % c))
    OL.apply('office_grey'); OL.apply('office_storm'); OL.flash(0.7); OL.set_rain(1, 1); OL.apply('office_day')
    for c in ('eye_two_shot', 'insert_rake'):
        S.make_camera(A['cams'][c]); S.render(os.path.join(od, 'after_%s.png' % c))
        a = np.asarray(Image.open(os.path.join(od, 'fresh_%s.png' % c)), np.int16); b = np.asarray(Image.open(os.path.join(od, 'after_%s.png' % c)), np.int16)
        res[c] = dict(max_abs_diff=int(np.abs(a - b).max()), mean_abs_diff=float(np.abs(a - b).mean()))
    json.dump(res, open(os.path.join(OUT, 'identity.json'), 'w'), indent=1); print(res)


def cmd_timing(threads=4, n=3):
    sd = os.path.join(OUT, 'sprites'); od = os.path.join(OUT, 'timing'); os.makedirs(od, exist_ok=True)
    R = Rig(sd); OL = R.OL
    for f in range(1, n + 2): R.set_cam('eye_two_shot', f)
    R.sprites_out(list(range(1, n + 2)))
    import camrig
    for f in range(1, n + 2):
        cs = R.A['cams']['eye_two_shot']; loc = (cs['loc'][0] + 0.02 * f, cs['loc'][1], cs['loc'][2])
        camrig.key_camera(f, loc, cs['look_at'], cam=R.cam, interp='CONSTANT')
    R.sc.cycles.samples = 12; out = {}
    for pr in PRESETS:
        OL.apply(pr); OL.tint_cards()
        if pr == 'office_storm': OL.flash(0.0)
        rs = []
        for f in range(1, n + 2):
            l0 = os.getloadavg()[0]
            r = R.render.render_frames([f], od, scale=1.0, threads=threads, scene=R.sc, camera=R.cam, prefix=pr + '_', verbose=False)[0]
            rs.append(dict(frame=f, wall=round(r['wall'], 2), cpu=round(r['cpu'], 2), load1=round(l0, 2)))
            print(pr, rs[-1], flush=True)
        steady = rs[1:]
        out[pr] = dict(frames=rs, median_wall=sorted(x['wall'] for x in steady)[len(steady) // 2], median_cpu=sorted(x['cpu'] for x in steady)[len(steady) // 2],
                       threads=threads, samples=12, resolution='720x1280')
    json.dump(out, open(os.path.join(OUT, 'timing_%dt.json' % threads), 'w'), indent=1)


def cmd_measure():
    import numpy as np
    from PIL import Image
    meta = json.load(open(os.path.join(OUT, 'stills', 'staging.json')))
    res = dict(heads={}, hue={})
    need_mask = any(meta[c]['heads'] for c in CAMS)
    R = None
    if need_mask:
        R = Rig(os.path.join(OUT, 'sprites'))
        for i, c in enumerate(CAMS): R.set_cam(c, i + 1)
    lum = lambda p: p @ np.array([0.2126, 0.7152, 0.0722])
    for c in CAMS:
        hd = meta[c]['heads']
        if not hd: continue
        f = meta[c]['frame']; yy, xx = np.mgrid[0:1280, 0:720]
        masks = {}
        for nm, h in hd.items():
            cx, cy = h['center']; D = h['D_px']; rr = np.hypot(xx + 0.5 - cx, yy + 0.5 - cy)
            ring = (rr > 0.62 * D) & (rr < 0.95 * D) & (xx % 2 == 0) & (yy % 2 == 0)
            pts = list(zip((xx[ring] + 0.5).tolist(), (yy[ring] + 0.5).tolist()))
            act = np.array(R.actor_mask(f, pts)); masks[nm] = (ring, act)
        for pr in PRESETS:
            a = np.asarray(Image.open(os.path.join(OUT, 'stills', '%s_%s.png' % (pr, c))).convert('RGB'), float) / 255
            for nm, h in hd.items():
                cx, cy = h['center']; D = h['D_px']; rr = np.hypot(xx + 0.5 - cx, yy + 0.5 - cy)
                disc = rr < 0.46 * D; px = a[disc]; Y = lum(px); fill = np.median(px[Y > np.percentile(Y, 55)], axis=0)
                band = (rr > 0.40 * D) & (rr < 0.53 * D); pb = a[band]; Yb = lum(pb); ink = np.median(pb[Yb < np.percentile(Yb, 12)], axis=0)
                ring, act = masks[nm]; wall = a[ring][~act]
                wl = float(np.median(lum(wall)) * 255) if len(wall) > 30 else None
                import colorsys
                hh, ss, vv = colorsys.rgb_to_hsv(*fill)
                res['heads'].setdefault(pr, {}).setdefault(c, {})[nm] = dict(D_px=round(D, 1), center=[round(cx), round(cy)], fill='#%02x%02x%02x' % tuple(int(round(x * 255)) for x in fill),
                                                                            fill_V=round(vv, 3), fill_S=round(ss, 3), ink='#%02x%02x%02x' % tuple(int(round(x * 255)) for x in ink),
                                                                            wall_luma_ring=None if wl is None else round(wl, 1), ring_px_wall=int((~act).sum()), ring_px_actor=int(act.sum()))
                # is the head the brightest large shape? share of non-actor pixels in the frame brighter than the head fill's luma
                res['heads'][pr][c][nm]['frame_px_brighter_than_fill'] = round(float((lum(a.reshape(-1, 3)) > lum(fill) - 0.02).mean()), 4)
    hr = os.path.join(V3, 'tools', 'hue_report.py')
    for pr in PRESETS:
        r = subprocess.run(['python3', hr, os.path.join(OUT, 'stills', pr + '_*.png')], capture_output=True, text=True).stdout.strip().splitlines()
        res['hue'][pr] = r[-1]
    res['hue']['header'] = subprocess.run(['python3', hr, os.path.join(OUT, 'stills', 'office_day_*.png')], capture_output=True, text=True).stdout.strip().splitlines()[0]
    json.dump(res, open(os.path.join(OUT, 'measure.json'), 'w'), indent=1, ensure_ascii=False)
    for pr in PRESETS: print(res['hue'][pr])
    for pr, v in res['heads'].items():
        for c, hs in v.items():
            for nm, h in hs.items(): print(pr, c, nm, h)


def cmd_sheets():
    from PIL import Image, ImageDraw, ImageFont
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
    except Exception: font = ImageFont.load_default()
    def sheet(rows, out, w=240):
        h = int(w * 16 / 9); st = 22; cols = max(len(r) for r in rows)
        G = Image.new('RGB', (cols * w, len(rows) * (h + st)), (18, 18, 22)); d = ImageDraw.Draw(G)
        for j, r in enumerate(rows):
            for i, (lab, p) in enumerate(r):
                x, y = i * w, j * (h + st)
                if p and os.path.exists(p): G.paste(Image.open(p).convert('RGB').resize((w, h)), (x, y + st))
                d.text((x + 4, y + 3), lab, fill=(255, 255, 255), font=font)
        G.save(out, quality=88); print(out)
    ref = lambda k: os.path.join(PROJ, 'ref', k + '.jpg')
    rows = [[('ref ' + REFS[c], ref(REFS[c]))] + [(pr.replace('office_', '') + ' ' + c, os.path.join(OUT, 'stills', '%s_%s.png' % (pr, c))) for pr in PRESETS] for c in CAMS]
    sheet(rows, os.path.join(OUT, 'compare.jpg'))
    # transposed: one row per preset (easier to read the whole mood)
    rows = [[(pr.replace('office_', '') + ' ' + c, os.path.join(OUT, 'stills', '%s_%s.png' % (pr, c))) for c in CAMS] for pr in PRESETS]
    sheet(rows, os.path.join(OUT, 'compare_by_preset.jpg'), w=216)
    sheet([[('frame %d flash %s' % (f, {1: '0', 2: '1.0', 3: '0.35', 4: '0.8', 5: '0', 6: '0'}[f]), os.path.join(OUT, 'strips', 'flash_%d.png' % f)) for f in range(1, 7)]],
          os.path.join(OUT, 'flash_strip.jpg'), w=240)
    sheet([[('%s f%d' % (pr.replace('office_', ''), f), os.path.join(OUT, 'strips', 'rain_%s_%02d.png' % (pr, f))) for f in (1, 25, 49, 73)] for pr in ('office_grey', 'office_storm')],
          os.path.join(OUT, 'rain_strip.jpg'), w=270)


if __name__ == '__main__':
    a = sys.argv[1:]; cmd = a[0] if a else ''
    if cmd == 'stills': cmd_stills(float(a[1]) if len(a) > 1 else 1.0)
    elif cmd == 'strips': cmd_strips()
    elif cmd == 'identity': cmd_identity()
    elif cmd == 'timing': cmd_timing(int(a[1]) if len(a) > 1 else 4)
    elif cmd == 'measure': cmd_measure()
    elif cmd == 'sheets': cmd_sheets()
    else: print(__doc__)
