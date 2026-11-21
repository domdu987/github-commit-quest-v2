"""mc.py : shared helpers of takes s20, s21, s22 (the mechanism on the wall map after shot 19; office_grey, no characters).
Same scene, same camera grammar (pose = target, distance, direction, up, roll; snaps blend those) and same resumable render loop
as film/s19/shot.py.  Each take's shot.py defines G0, G1, H_IN, H_OUT, cam_setup(g), state(g), CUES and calls mc.main()."""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d_ext', 'mech'))
import bpy                                            # noqa: E402
from mathutils import Vector                          # noqa: E402

LIGHT, WALL_H = 'office_grey', 0.50

def gf(x): return int(round((x + 0.1) * 30))
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def smooth(a, b, g): x = clamp((g - a) / float(b - a)); return x * x * (3 - 2 * x)
def smoother(x): x = clamp(x); return x * x * x * (x * (6 * x - 15) + 10)
def lin(a, b, g): return clamp((g - a) / float(b - a))
def snap_e(g, a, b):
    x = clamp((g - a) / float(b - a)); return smoother(1 - (1 - x) ** 1.35)
def hsh(g, s=0):
    x = math.sin(g * 12.9898 + s * 78.233) * 43758.5453; return x - math.floor(x)

_M = {}
def scene(scale=1.0, samples=12):
    import office_mech as M
    S, X = M.S, M.X
    import office_light as OL
    A = S.build('INTERIOR_DAY'); PA = X.build(A, hi_map=True); MA = M.build(A, PA, wall_height=WALL_H); OL.apply(LIGHT)
    sc = bpy.context.scene; S.setup_render(sc, 'final'); sc.cycles.samples = samples; sc.render.resolution_percentage = int(round(scale * 100))
    sc.render.threads_mode = 'FIXED'; sc.render.threads = 2
    S.set_track(1, 0); [X.set_ghost(i, 1.0, 0.35) for i in range(1, 7)]; X.set_label(1.0)
    X.set_chalk(1.0, crumble=1.0, alpha=0.45)                       # as shot 19 leaves it
    _M.update(bpy=bpy, M=M, S=S, X=X, OL=OL, A=A, PA=PA, MA=MA, sc=sc)
    return _M

def base_state():
    """The map at the end of shot 19: both walls locked, lane lit (glow 0.2), compass, both pictograms."""
    M = _M['M']
    for sd in 'EW': M.set_wall(sd, rise=4, slide=1, lock=1, fade=1.0, pulse=0.0)
    M.set_lane(1.0, red=0.0, fuse=0.0, alpha=1.0, glow=0.22)
    M.set_compass(show=1.0, scale=0.8)
    for sd in 'EW':
        M.set_picto(sd, show=1.0, scale=0.5, s=0.22, h=0.30, yaw_deg=22.0 if sd == 'E' else 60.0, tilt_deg=0.0 if sd == 'E' else 35.0)
    M.set_spinner_fx(ring=0.0, drop=0.0)
    M.set_speed_sign(show=0); M.set_wind(0.0, amount=0); M.set_wake(0, 0, 0)
    for i in (1, 2, 3): M.set_ghost_spinner(i, 0.0, show=0)
    M.set_shell(0.0)

# ----------------------------------------------------------------------------- camera poses
def pose(setup):
    loc, look = Vector(setup['loc']), Vector(setup['look_at']); d = loc - look
    up = Vector(setup['up']) if setup.get('up') else None
    return dict(t=look, d=d.length, v=d.normalized(), up=up, roll=setup.get('roll', 0.0))

def upv(p):
    if p['up'] is not None: return p['up']
    f = -p['v']; r = f.cross(Vector((0, 0, 1))).normalized(); return r.cross(f).normalized()

def blend(a, b, e):
    t = a['t'].lerp(b['t'], e); d = a['d'] * (b['d'] / a['d']) ** e; v = a['v'].lerp(b['v'], e).normalized()
    up = upv(a).lerp(upv(b), e).normalized(); roll = a['roll'] + (b['roll'] - a['roll']) * e
    return dict(t=t, d=d, v=v, up=up, roll=roll)

def setup_of(p, jitter=None, lens=22.0):
    loc = p['t'] + p['d'] * p['v']; look = p['t'] + (jitter if jitter is not None else Vector((0, 0, 0)))
    return dict(loc=tuple(loc), look_at=tuple(look), lens=lens, up=tuple(upv(p)), roll=p['roll'])

def raw(loc, look, up):
    return dict(t=Vector(look), d=(Vector(loc) - Vector(look)).length, v=(Vector(loc) - Vector(look)).normalized(), up=Vector(up) if up else None, roll=0.0)

# ----------------------------------------------------------------------------- numbers
def project(p):
    from bpy_extras.object_utils import world_to_camera_view
    sc = _M['sc']; co = world_to_camera_view(sc, sc.camera, Vector(p)); return co.x * 720, (1 - co.y) * 1280, co.z

def motion(shot, gs):
    M = _M['M']
    pts = [M.world(a, 0, h, u=u) for u in (-0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1) for a in (-0.5, -0.2, 0.0, 0.2, 0.5) for h in (0.0, 0.3)]
    pts += [(x, -0.05, z) for x in (-2.0, -1.0, 0.0, 1.0, 2.0) for z in (1.0, 2.0, 3.0, 4.0)]
    prev = None; sp = []
    for g in gs:
        shot.apply(g); P = [project(p) for p in pts]
        if prev is not None:
            d = [math.hypot(x[0] - y[0], x[1] - y[1]) for x, y in zip(P, prev) if x[2] > 0.05 and y[2] > 0.05 and -200 < x[0] < 920 and -200 < x[1] < 1480]
            sp.append((g, round(max(d), 2) if d else 0.0))
        prev = P
    return sp

def runs(sp, still=0.3, tol=0.06, minlen=7):
    """Static runs (< still px/f) and linear runs (speed within tol relative over minlen frames)."""
    st = []; ln = []; k = 0
    for i, (g, v) in enumerate(sp):
        if v < still: k += 1
        else:
            if k >= 6: st.append((g - k, k))
            k = 0
    i = 0
    while i < len(sp) - 1:
        j = i
        while j + 1 < len(sp) and sp[j + 1][1] > still and abs(sp[j + 1][1] - sp[i][1]) <= tol * max(sp[i][1], 1e-6) and abs(sp[j + 1][1] - sp[j][1]) <= 0.02 * max(sp[j][1], 1e-6) + 0.02:
            j += 1
        if j - i + 1 >= minlen: ln.append((sp[i][0], j - i + 1))
        i = j + 1
    return st, ln

# ----------------------------------------------------------------------------- render
def render_frames(shot, gs, out, scale, samples, meta_dir):
    _ = scene(scale, samples); S = _['S']; os.makedirs(out, exist_ok=True); os.makedirs(meta_dir, exist_ok=True)
    for g in gs:
        png = os.path.join(out, 'g_%04d.png' % g); js = os.path.join(meta_dir, 'g_%04d.json' % g)
        if os.path.exists(png) and os.path.exists(js): continue
        if os.path.exists(png): os.remove(png)
        shot.apply(g); tmp = os.path.join(out, '.tmp_%04d.png' % g)
        t0 = time.time(); c0 = time.process_time(); S.render(tmp); wall = time.time() - t0; cpu = time.process_time() - c0
        os.replace(tmp, png)
        json.dump(dict(g=g, wall_s=round(wall, 2), cpu_s=round(cpu, 2), load=os.getloadavg()[0], scale=scale, samples=samples,
                       cam=shot.cam_setup(g)), open(js, 'w'))
        print('g %d  %.1f s' % (g, wall), flush=True)

def write_cues(shot):
    cues = [dict(t=round(t + 0.1, 3), clock=t, g=gf(t), dur=d, kind=k, label=l) for t, d, k, l in shot.CUES]
    json.dump(dict(take=shot.TAKE, time='film seconds (narration clock + 0.100)', cues=cues), open(os.path.join(shot.DIR, 'cues.json'), 'w'), indent=1, ensure_ascii=False)

def main(shot):
    R0, R1 = shot.G0 - shot.H_IN, shot.G1 + shot.H_OUT
    def parse(spec):
        if not spec: return list(range(R0, R1))
        p = [int(x) for x in spec.split(':')]; return list(range(p[0], p[1], p[2] if len(p) > 2 else 1))
    a = sys.argv[1:]; cmd = a[0] if a else 'probe'; D = shot.DIR
    if cmd == 'probe':
        scene(0.5, 4); gs = parse(a[1] if len(a) > 1 else None); st = int(a[2]) if len(a) > 2 else 6
        for g in gs[::st]: print(json.dumps(shot.probe_frame(g)))
    elif cmd == 'motion':
        scene(0.5, 4); sp = motion(shot, parse(None)); st, ln = runs(sp)
        json.dump(dict(speed=sp, static=st, linear=ln), open(os.path.join(D, 'work', 'motion.json'), 'w'))
        print(' '.join('%d:%.1f' % x for x in sp)); print('static', st); print('linear', ln)
    elif cmd == 'still':
        gs = [int(x) for x in a[1].split(',')]; dr = 'draft' in a
        render_frames(shot, gs, os.path.join(D, 'work', 'still'), 0.5 if dr else 1.0, 6 if dr else 12, os.path.join(D, 'work', 'still', 'meta'))
    elif cmd == 'draft':
        render_frames(shot, parse(a[1] if len(a) > 1 else None), os.path.join(D, 'work', 'draft'), 0.5, 6, os.path.join(D, 'work', 'draft', 'meta'))
    elif cmd == 'render':
        render_frames(shot, parse(a[1] if len(a) > 1 else None), os.path.join(D, 'frames'), 1.0, 12, os.path.join(D, 'work', 'meta'))
    elif cmd == 'cues': write_cues(shot)
