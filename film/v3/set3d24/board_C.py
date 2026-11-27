#!/usr/bin/env python3
"""board_C.py : the LOOK C lighting / look board (LIGHT_SPEC.md) with the REAL cast24 cards (film24/common.py + the film24 shot takes).

    python3 board_C.py tile <name> [samples 12]     one tile (one process, 2 threads) -> joseon_work/board_C/<name>.png + <name>.json
    python3 board_C.py all [samples 12]             every tile, one process after another (never two renders at once)
    python3 board_C.py sheet                        board_C.jpg + board_C_small.jpg (labelled, with the LIGHT_SPEC metrics)

Every card gets the look C warm rim (J.card_rim via common.story).  Env JOSEON_LOOK=C is set here."""
import os, sys, json, time, math, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'joseon_work', 'board_C')
F24 = os.path.join(os.path.dirname(HERE), 'film24')
# name: (label, kind, arg)
TILES = [
    ('hero_yard', '4  hero_yard (Yi at its foot)', 'custom', None),
    ('hero_orbit', '14  hero_orbit', 'custom', None),
    ('cannon_close', '13b  cannon_close (broadside)', 'custom', None),
    ('hit_close', '13c  hit_close (mid-explosion)', 'custom', None),
    ('roof_low', '1  roof_low relit (s01 cast)', 'take', ('s01', 1)),
    ('flag_deck', '5  flag_deck (s05 cast)', 'take', ('s05', 5)),
    ('flag_deck_crew', '7  flag_deck_crew (s07 cast)', 'take', ('s07', 7)),
    ('reveal_top', '13  reveal_top aerial U (s13)', 'take', ('s13', 13)),
    ('shore', '15  shore (s15 cast)', 'take', ('s15', 15)),
]
F = 40


def _rim_story(C, J):
    orig = C.story
    def story(name):
        c, p = orig(name)
        return c, J.card_rim(p)
    C.story = story


def tile(name, samples):
    os.environ['JOSEON_LOOK'] = 'C'
    sys.path.insert(0, F24)
    import common as C
    J = C.J
    _rim_story(C, J)
    label, kind, arg = [(l, k, a) for n, l, k, a in TILES if n == name][0]
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    if kind == 'take':
        mod, shot = arg
        spec = importlib.util.spec_from_file_location('shot_' + mod, os.path.join(F24, mod, 'shot.py'))
        M = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(M)
        a, b = (getattr(M, 'RANGES', None) or M.RANGE)[shot]
        g = (a + b) // 2
        Tk = M.Take(shot)
        Tk.pose(shot, [g])
        rep = Tk.report(shot, g)
        st = Tk.render(shot, [g], OUT, scale=C.RES_PCT, samples=samples)[0]
    else:
        Tk = C.Take(name)
        sd = os.path.join(OUT, 'sprites_' + name)
        A = Tk.A
        jobs = []
        if name == 'hero_yard':
            Tk.key_set(F, spikes=3, ports=0, dragon_smoke=0.45)
            yi = Tk.actors['yi'] = C.make_actor('yi', 'yi24', sd)
            C.place(yi, F, A['marks']['yi_hero'])
            _, p = C.story('yi24_stand_arms_behind')
            p['gaze'] = (-0.6, -0.6)
            p['mirror'] = True
            Tk.scene.frame_set(F)
            yi.pose(F, p, camera=Tk.cam)
            jobs.append((yi, 128))
        elif name == 'hero_orbit':
            Tk.key_set(F, spikes=3, ports=1, dragon_smoke=0.8)
        elif name == 'cannon_close':
            Tk.key_set(F, spikes=3, ports=1, dragon_smoke=0.0)
            J.set_broadside(0.62, F)
        elif name == 'hit_close':
            t = 0.35
            J.set_hit_explosion(t, F)
            for i, (cast, st_) in enumerate((('ashi_a24', 'ashi_a24_step_back'), ('ashi_b24', 'ashi_b24_peer_worried'))):
                a_ = Tk.actors['ashi%d' % i] = C.make_actor('ashi%d' % i, cast, sd, contact=False)
                tj = 0.30 + 0.12 * i
                C.place(a_, F, tuple(J.jump_arc(i, tj)))
                J.set_jump_splash(i, tj, F)
                _, p = C.story(st_)
                p['mirror'] = bool(i)
                Tk.scene.frame_set(F)
                a_.pose(F, p, camera=Tk.cam)
                jobs.append((a_, 128))
        if jobs:
            Tk.sprites_for(jobs, [F])
        Tk.scene.frame_set(F)
        rep = dict(heads=C.head_report(Tk, F), feet=C.feet_report(Tk, F))
        st = C.Take.render(Tk, [F], OUT, scale=C.RES_PCT, samples=samples)[0]
    dst = os.path.join(OUT, name + '.png')
    os.replace(st['path'], dst)
    sys.path.insert(0, HERE)
    import look_metrics
    m = look_metrics.metrics(dst)
    info = dict(name=name, label=label, wall=round(st['wall'], 1), cpu=round(st['cpu'], 1), samples=samples, total_wall=round(time.time() - t0, 1), metrics=m, report=rep)
    json.dump(info, open(os.path.join(OUT, name + '.json'), 'w'), indent=1, default=str)
    print('tile %s: %.1f s wall, %.1f s cpu  %s' % (name, st['wall'], st['cpu'], m), flush=True)


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    W, H, cols = 720, 1280, 5
    names = [n for n, *_ in TILES if os.path.exists(os.path.join(OUT, n + '.png'))]
    rows = (len(names) + cols - 1) // cols
    bar = 120
    im = Image.new('RGB', (cols * W, rows * (H + bar)), (24, 24, 30))
    d = ImageDraw.Draw(im)
    try:
        fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    except Exception:
        fnt = fs = ImageFont.load_default()
    for i, n in enumerate(names):
        x, y = (i % cols) * W, (i // cols) * (H + bar)
        im.paste(Image.open(os.path.join(OUT, n + '.png')).convert('RGB').resize((W, H)), (x, y))
        info = json.load(open(os.path.join(OUT, n + '.json')))
        m = info['metrics']
        d.text((x + 14, y + H + 10), [l for n_, l, *_ in TILES if n_ == n][0], fill=(240, 236, 228), font=fnt)
        d.text((x + 14, y + H + 50), 'sat %.2f  warm %d%%  cool %d%%  other %d%%  shadow %d%%' % (m['sat'], 100 * m['warm'], 100 * m['cool'], 100 * m['other'], 100 * m['shadow']), fill=(200, 196, 210), font=fs)
        d.text((x + 14, y + H + 80), '%d samples  %.0f s cpu (%.0f s on 4 cores)' % (info['samples'], info['cpu'], info['cpu'] / 4.0), fill=(170, 170, 185), font=fs)
    im.save(os.path.join(HERE, 'board_C.jpg'), quality=88)
    im.resize((im.width // 3, im.height // 3)).save(os.path.join(HERE, 'board_C_small.jpg'), quality=85)
    print('sheet: %d tiles' % len(names))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'tile':
        tile(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 12)
    elif cmd == 'all':
        smp = sys.argv[2] if len(sys.argv) > 2 else '12'
        for n, *_ in TILES:
            r = subprocess.run([sys.executable, os.path.abspath(__file__), 'tile', n, smp], capture_output=True, text=True)
            print('\n'.join(l for l in (r.stdout + r.stderr).splitlines() if l.startswith(('tile', 'Traceback', '  File', 'Error')) or 'Error' in l), flush=True)
        sheet()
    elif cmd == 'sheet':
        sheet()
