#!/usr/bin/env python3
"""otake.py -- shared runner for the office_day takes s04, s05, s07 (one worker; lives in s04/, imported by s05/s07).

A take module (sNN/shot.py) defines:
    TAKE, SHOTS, G0, G1 (exclusive), H_IN, H_OUT, TRANSITION_IN, TRANSITION_OUT, LIGHT, SET
    cam(g) -> (loc Vector, look Vector)
    keys(T)            key every prop state for every rendered frame (X setters with frame = g + 1)
    ACTORS             list of dict(name, cast, canvas (None = default), shadow ('proxy' | 'card'), contact)
    perform(T, g)      -> {actor name: None (hidden) | dict(feet, pose, hands, yaw_fixed, ppd, flip)}
    map_hi(g) -> bool  6000 px map for this frame
    CUES = [(clock_s, dur, kind, label)]

Commands (python3 shot.py <cmd> ...):
    probe a:b[:s]      staging numbers, no rendering
    still a:b[:s]      360x640 drafts, 6 samples -> work/draft/
    final              12 samples, 720x1280, resumable -> raw/ (+ raw/meta), then layers, post, meta, cues, contact
    layers | post | contact | deliver
"""
import json, math, os, sys, time, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
V3 = os.path.join(PROJ, 'v3')
for p in (os.path.join(V3, 'acting'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d'), os.path.join(V3, 'set3d_ext', 'props'),
          os.path.join(PROJ, 'v2', 'shots')):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.path.append(os.path.join(V3, 'shots'))           # post.py (streak maths) last, so its timing/film never shadow ours

import bpy                                            # noqa: E402
from mathutils import Vector                          # noqa: E402
import acting                                         # noqa: E402,F401  (registers cast + drawings)
import office3d as S                                  # noqa: E402
import office_props as X                              # noqa: E402
import actors, camrig, render, sprites                # noqa: E402
import post as POST                                   # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402,F401


def gf(clock):
    """film frame of an in-shot event at narration clock `clock` (s)."""
    return int(round((clock + 0.1) * 30))


def bf(g):
    return int(g) + 1


def parse(spec, r0, r1):
    if spec in (None, '', 'all'):
        return list(range(r0, r1))
    out = []
    for part in spec.split(','):
        bits = [int(b) for b in part.split(':')]
        if len(bits) == 1:
            out.append(bits[0])
        else:
            st = bits[2] if len(bits) > 2 else 1
            out += list(range(bits[0], bits[1] + 1, st))
    return [g for g in out if r0 <= g < r1]


class Take(object):
    def __init__(self, M, verbose=True):
        self.M = M
        self.dir = os.path.dirname(os.path.abspath(M.__file__))
        self.R0, self.R1 = M.G0 - M.H_IN, M.G1 + M.H_OUT
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = sc = bpy.context.scene
        self.A = S.build('INTERIOR_DAY')
        self.PA = X.build(self.A, hi_map=False)
        X.reset()
        S.set_track(0.0, 0.0)
        sc.render.use_persistent_data = False
        sc.cycles.transparent_max_bounces = 12
        sc.frame_start, sc.frame_end = 1, 2000
        self.cam = camrig.make_camera(sc, name='cam_' + M.TAKE)
        self.cam.data.clip_start = 0.02
        for g in range(self.R0, self.R1):
            loc, look = M.cam(g)
            camrig.key_camera(bf(g), loc, look, cam=self.cam, interp='LINEAR', easing='AUTO')
        self.actors = {}
        self.sprite_dir = os.path.join(self.dir, 'work', 'sprites')
        for spec in getattr(M, 'ACTORS', []):
            a = actors.Actor(spec['name'], spec['cast'])
            canvas = spec.get('canvas') or sprites.DEFAULT_CANVAS[spec['cast']]
            a.build(canvas, self.sprite_dir, shadow=spec.get('shadow', 'proxy'), contact=spec.get('contact'))
            a.head_flip = True
            S.no_bounce(a.card)
            self.actors[spec['name']] = a
        M.keys(self)
        self.perf = {}
        self.info = {}
        self.anch = {}
        self._hi = None
        if verbose:
            print('otake: %s built in %.1f s (render g %d..%d)' % (M.TAKE, time.time() - t0, self.R0, self.R1 - 1), flush=True)

    # ------------------------------------------------------------------ per frame
    def perform(self, g):
        if g not in self.perf:
            self.perf[g] = self.M.perform(self, g) if hasattr(self.M, 'perform') else {}
        return self.perf[g]

    def apply(self, g):
        hi = bool(self.M.map_hi(g)) if hasattr(self.M, 'map_hi') else False
        if hi != self._hi:
            X.set_map_res(hi)
            self._hi = hi
        P = self.perform(g)
        for name, a in self.actors.items():
            p = P.get(name)
            vis = p is not None
            a.card.hide_render = not vis
            if a.proxy is not None:
                a.proxy.hide_render = not vis
            if getattr(a, 'contact', None) is not None:
                a.contact.hide_render = not vis
            if vis:
                a.yaw_fixed = p.get('yaw_fixed')

    def on_frame(self, f):
        self.apply(f - 1)

    def pose(self, frames, verbose=False):
        cam, sc = self.cam, self.scene
        for g in frames:
            f = bf(g)
            P = self.perform(g)
            for name, a in self.actors.items():
                p = P.get(name)
                if p is None:
                    continue
                a.place(f, tuple(p['feet']), scale=p.get('scale', 1.0), flip=p.get('flip', False))
        for g in frames:
            f = bf(g)
            sc.frame_set(f)
            self.apply(g)
            P = self.perform(g)
            for name, a in self.actors.items():
                p = P.get(name)
                if p is None:
                    continue
                hands = p.get('hands')
                kw = {}
                if p.get('upper_k') is not None:
                    kw['upper_k'] = p['upper_k']
                pose, info = a.pose(f, p['pose'], hands=hands, camera=cam, **kw)
                if hands:
                    for side, e in info.items():
                        if 'reached' in e:
                            e['screen'] = actors.local_to_screen(a, cam, e['reached'], f)[:2]
                            tw = hands[side].get('tip') if hands[side].get('tip') is not None else hands[side].get('hand')
                            if tw is not None and len(tw) == 3:
                                e['want'] = render.world_to_screen(cam, Vector(tw), f)[:2]
                self.info.setdefault(g, {})[name] = info
        for name, a in self.actors.items():
            groups = {}
            for g in frames:
                p = self.perform(g).get(name)
                if p is None:
                    continue
                groups.setdefault(int(p.get('ppd', 256)), []).append(g)
            for ppd, gl in groups.items():
                res = a.render_sprites(ppd, frames=[bf(g) for g in gl], verbose=verbose)
                for g, r in zip(gl, res):
                    self.anch.setdefault(g, {})[name] = r['anchors']
                    if r.get('clipped'):
                        print('otake: WARNING sprite of %s clipped on g %d' % (name, g), flush=True)

    # ------------------------------------------------------------------ numbers
    def report(self, g):
        f = bf(g)
        cam = self.cam
        self.scene.frame_set(f)
        self.apply(g)
        loc, look = self.M.cam(g)
        v = Vector(look) - Vector(loc)
        out = dict(g=g, t_film=round(g / 30.0, 3), cam=[round(c, 3) for c in loc], cam_height=round(loc[2], 3),
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 2),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 2),
                   map_dist=round(-Vector(loc).y + S.MAP_Y if False else -(Vector(loc).y - S.MAP_Y), 3), heads={}, reg={})
        P = self.perform(g)
        for name, a in self.actors.items():
            if P.get(name) is None:
                continue
            an = self.anch.get(g, {}).get(name)
            if not an or P[name].get('no_head'):
                continue
            feet = a.feet.get(f)
            hx, hy = an['head']
            c = actors.local_to_screen(a, cam, (hx, hy), f, feet)
            l = actors.local_to_screen(a, cam, (hx - 0.5, hy), f, feet)
            r = actors.local_to_screen(a, cam, (hx + 0.5, hy), f, feet)
            out['heads'][name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1), depth=round(c[2], 3))
        for name, info in self.info.get(g, {}).items():
            for side, e in info.items():
                if 'screen' in e and 'want' in e:
                    out['reg'][name] = dict(px=round(math.hypot(e['screen'][0] - e['want'][0], e['screen'][1] - e['want'][1]), 3),
                                            solve_err_D=round(e['error'], 5), tip=[round(e['screen'][0], 1), round(e['screen'][1], 1)])
        if hasattr(self.M, 'report_extra'):
            out.update(self.M.report_extra(self, g))
        return out

    # ------------------------------------------------------------------ render
    def render(self, frames, out_dir, scale=1.0, samples=12, threads=2, resumable=True, verbose=True):
        meta = os.path.join(out_dir, 'meta')
        os.makedirs(meta, exist_ok=True)
        png = lambda g: os.path.join(out_dir, 'f_%04d.png' % bf(g))
        js = lambda g: os.path.join(meta, 'g_%04d.json' % g)
        todo = []
        for g in frames:
            done = False
            if resumable and os.path.exists(png(g)) and os.path.exists(js(g)):
                try:
                    m = json.load(open(js(g)))
                    done = m.get('scale') == scale and m.get('samples') == samples and m.get('version') == getattr(self.M, 'VERSION', 1)
                except Exception:
                    done = False
            if not done:
                for p in (png(g), js(g)):
                    if os.path.exists(p):
                        os.remove(p)
                todo.append(g)
        print('otake: %s render %d frames (%d finished) -> %s' % (self.M.TAKE, len(todo), len(frames) - len(todo), out_dir), flush=True)
        if not todo:
            return
        self.pose(todo)
        self.scene.cycles.samples = samples
        for g in todo:
            st = render.render_frames([bf(g)], out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam,
                                      on_frame=self.on_frame, verbose=False)[0]
            rep = self.report(g)
            rep.update(wall=round(st['wall'], 2), cpu=round(st['cpu'], 2), scale=scale, samples=samples, threads=threads,
                       retried=st.get('retried'), still_wrong=st.get('still_wrong'), version=getattr(self.M, 'VERSION', 1))
            tmp = js(g) + '.tmp'
            json.dump(rep, open(tmp, 'w'))
            os.replace(tmp, js(g))
            if verbose:
                print('g %d  %.1f s wall  %.1f s cpu%s' % (g, st['wall'], st['cpu'], '  RETRIED' if st.get('retried') else ''), flush=True)

    def layers(self, frames, raw, samples=12, threads=2):
        """plate (actors hidden from the camera, shadows kept) and matte (actors only, set as holdout) of streaked frames
        with an actor in view; resumable."""
        sc = self.scene
        plate, matte = os.path.join(raw, 'plate'), os.path.join(raw, 'matte')
        todo = [g for g in frames if not (os.path.exists(os.path.join(plate, 'f_%04d.png' % bf(g))) and
                                          os.path.exists(os.path.join(matte, 'f_%04d.png' % bf(g))))]
        if not todo:
            return
        self.pose(todo)
        cards = [a.card for a in self.actors.values()]
        decals = [a.contact for a in self.actors.values() if getattr(a, 'contact', None) is not None]
        set_obs = [ob for ob in sc.objects if ob not in cards and ob.type in ('MESH', 'CURVE') and not ob.name.endswith('_shadow')]
        for g in todo:
            f = bf(g)
            sc.cycles.samples = samples
            vis_cam = {}

            def hide_cards(fr, _g=g):
                self.apply(_g)
                for c in cards:
                    vis_cam[c.name] = c.visible_camera
                    c.visible_camera = False
            render.render_frames([f], plate, threads=threads, scene=sc, camera=self.cam, on_frame=hide_cards, verbose=False, check=False)
            for c in cards:
                c.visible_camera = True
            keep = (sc.render.film_transparent, sc.render.image_settings.color_mode, sc.render.use_compositing, sc.cycles.samples)
            sc.render.film_transparent = True; sc.render.image_settings.color_mode = 'RGBA'; sc.render.use_compositing = False; sc.cycles.samples = 4
            hold = [(ob, ob.is_holdout) for ob in set_obs]
            for ob, _ in hold:
                ob.is_holdout = True
            hid = [(d, d.hide_render) for d in decals]
            render.render_frames([f], matte, threads=threads, scene=sc, camera=self.cam, on_frame=self.on_frame, verbose=False, check=False)
            for ob, v in hold:
                ob.is_holdout = v
            for d, v in hid:
                d.hide_render = v
            sc.render.film_transparent, sc.render.image_settings.color_mode, sc.render.use_compositing, sc.cycles.samples = keep
            print('layers g %d' % g, flush=True)


# ---------------------------------------------------------------------- streak / post (numpy only, no Blender scene needed)
def cam_tuple(M):
    return lambda g: tuple(tuple(v) for v in M.cam(g))


def streak_plan(M):
    """[(g, speed)] of frames faster than post.STREAK_MIN (the hook's rule) and whether an actor is in that frame."""
    R0, R1 = M.G0 - M.H_IN, M.G1 + M.H_OUT
    fn = cam_tuple(M)
    out = []
    for g in range(R0, R1):
        M1, sp = POST.camera_motion(fn, g, R0, R1 - 1)
        out.append((g, sp, M1))
    return out


def do_post(M, raw, frames_dir, actor_frames=()):
    os.makedirs(frames_dir, exist_ok=True)
    from PIL import Image
    log = []
    for g, sp, M1 in streak_plan(M):
        src = os.path.join(raw, 'f_%04d.png' % bf(g))
        dst = os.path.join(frames_dir, 'g_%04d.png' % g)
        if not os.path.exists(src):
            raise SystemExit('missing raw frame ' + src)
        row = dict(g=g, corner_speed_px=round(sp, 2), streaked=False)
        if sp >= POST.STREAK_MIN:
            im = Image.open(src).convert('RGB')
            pl = os.path.join(raw, 'plate', 'f_%04d.png' % bf(g)); mt = os.path.join(raw, 'matte', 'f_%04d.png' % bf(g))
            if g in actor_frames and os.path.exists(pl) and os.path.exists(mt):
                POST.over(POST.streak(Image.open(pl).convert('RGB'), M1, sp), im, Image.open(mt)).save(dst)
                row['streaked'] = 'plate'
            else:
                POST.streak(im, M1, sp).save(dst)
                row['streaked'] = 'whole'
        else:
            shutil.copyfile(src, dst)
        log.append(row)
    return log


def contact_sheet(M, frames_dir, out, n=16, cols=4, label=''):
    from PIL import Image, ImageDraw
    R0, R1 = M.G0 - M.H_IN, M.G1 + M.H_OUT
    gs = [int(round(R0 + i * (R1 - 1 - R0) / float(n - 1))) for i in range(n)]
    w, h, strip = 240, 427, 22
    W = Image.new('RGB', (cols * w, ((n + cols - 1) // cols) * (h + strip)), (20, 20, 24))
    d = ImageDraw.Draw(W)
    for i, g in enumerate(gs):
        p = os.path.join(frames_dir, 'g_%04d.png' % g)
        if not os.path.exists(p):
            p = os.path.join(frames_dir, 'f_%04d.png' % bf(g))
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert('RGB').resize((w, h))
        x, y = (i % cols) * w, (i // cols) * (h + strip)
        W.paste(im, (x, y + strip))
        tag = 'g %d  t %.2f s%s' % (g, g / 30.0, ('  (handle)' if g < M.G0 or g >= M.G1 else ''))
        d.text((x + 4, y + 5), tag, fill=(235, 235, 235))
    W.save(out, quality=88)
    return gs


def write_cues(M, path):
    ev = []
    for clock, dur, kind, label in M.CUES:
        t = round(clock + 0.1, 3)
        ev.append(dict(time=t, duration=dur, frame=int(round(t * 30)), end_frame=int(round((t + dur) * 30)), kind=kind, label=label, clock=clock))
    json.dump(dict(fps=30, time_base='film seconds (narration clock + 0.100); frame g starts at g / 30', take=M.TAKE, events=ev),
              open(path, 'w'), indent=1, ensure_ascii=False)


def write_meta(M, path, extra=None):
    d = dict(take=M.TAKE, shots=M.SHOTS, g0=M.G0, g1=M.G1, handle_in=M.H_IN, handle_out=M.H_OUT, transition_in=M.TRANSITION_IN,
             transition_out=getattr(M, 'TRANSITION_OUT', None), set='office', light=M.LIGHT, samples=12, frames_dir='frames',
             first_rendered=M.G0 - M.H_IN, last_rendered=M.G1 + M.H_OUT - 1, resolution=[720, 1280], fps=30)
    if extra:
        d.update(extra)
    json.dump(d, open(path, 'w'), indent=1, ensure_ascii=False)


# ---------------------------------------------------------------------- command line
def main(M, argv):
    cmd = argv[0] if argv else 'probe'
    d = os.path.dirname(os.path.abspath(M.__file__))
    R0, R1 = M.G0 - M.H_IN, M.G1 + M.H_OUT
    raw = os.path.join(d, 'raw')
    if cmd == 'probe':
        T = Take(M)
        gs = parse(argv[1] if len(argv) > 1 else '%d:%d:6' % (R0, R1 - 1), R0, R1)
        T.pose(gs)
        rows = [T.report(g) for g in gs]
        for r in rows:
            print(json.dumps(r))
        json.dump(rows, open(os.path.join(d, 'work', 'probe.json'), 'w'), indent=0)
    elif cmd == 'still':
        T = Take(M)
        gs = parse(argv[1] if len(argv) > 1 else '%d:%d:6' % (R0, R1 - 1), R0, R1)
        out = os.path.join(d, 'work', 'draft')
        T.render(gs, out, scale=0.5, samples=int(argv[2]) if len(argv) > 2 else 6, threads=2)
    elif cmd == 'final':
        T = Take(M)
        T.render(list(range(R0, R1)), raw, scale=1.0, samples=12, threads=2)
        af = actor_streak_frames(M, T)
        if af:
            T.layers(af, raw)
        json.dump(sorted(af), open(os.path.join(d, 'work', 'actor_streak_frames.json'), 'w'))
        deliver(M, d)
    elif cmd == 'deliver':
        deliver(M, d)
    elif cmd == 'contact':
        contact_sheet(M, argv[1], argv[2])
    else:
        raise SystemExit('unknown command ' + cmd)


def actor_streak_frames(M, T):
    out = []
    for g, sp, M1 in streak_plan(M):
        if sp >= POST.STREAK_MIN and any(v is not None for v in T.perform(g).values()):
            if hasattr(M, 'plate_ok') and not M.plate_ok(T, g):
                continue
            out.append(g)
    return out


def deliver(M, d):
    raw = os.path.join(d, 'raw')
    p = os.path.join(d, 'work', 'actor_streak_frames.json')
    af = set(json.load(open(p))) if os.path.exists(p) else set()
    log = do_post(M, raw, os.path.join(d, 'frames'), af)
    json.dump(log, open(os.path.join(d, 'work', 'post_log.json'), 'w'), indent=0)
    write_cues(M, os.path.join(d, 'cues.json'))
    write_meta(M, os.path.join(d, 'meta.json'), getattr(M, 'META_EXTRA', None))
    contact_sheet(M, os.path.join(d, 'frames'), os.path.join(d, 'contact.jpg'))
    print('deliver: %s post %d frames, streaked whole %s, plate %s' % (M.TAKE, len(log), [r['g'] for r in log if r['streaked'] == 'whole'],
                                                                        [r['g'] for r in log if r['streaked'] == 'plate']), flush=True)


# ---------------------------------------------------------------------- hand inserts (shots 5, 7): the take-A method
def arm_rig(cast, pose, side, hand_w, shoulder_w, cam_loc):
    """Card for a hand reaching into an insert: the card is the vertical plane through the hand point and the shoulder
    point (world), so the arm is drawn where a real arm would be and the hand (or prop tip) really meets its target.
    Returns (feet world point, yaw_fixed degrees, info).  The figure's local +x runs from the hand toward the shoulder
    (left arm reaching to the figure's left); info['facing'] = cos of the angle between the card normal and the view."""
    import puppet as P
    fig = P.figure(cast, pose, 'rig')
    a = fig['anchors']
    fx, fy = a['feet'][0], fig['feet_y']
    shx, shy = a['shoulder_' + side]
    H, Sh = Vector(hand_w), Vector(shoulder_w)
    Xd = Vector((Sh.x - H.x, Sh.y - H.y, 0.0))
    if side == 'r':
        Xd = -Xd
    Xd.normalize()
    Z = Vector((0.0, 0.0, 1.0))
    Y = Z.cross(Xd)                                   # card normal, away from the camera
    view = (H - Vector(cam_loc)).normalized()
    facing = Y.dot(view)
    # feet so that the shoulder anchor lands on Sh: world = o + X*(lx - fx) - Z*(ly - fy)
    o = Sh - Xd * (shx - fx) + Z * (shy - fy)
    return tuple(o), math.degrees(math.atan2(Xd.y, Xd.x)), dict(facing=round(facing, 3), reach=round((Sh - H).length, 3))


def arm_canvas(x0=-2.25, x1=-0.80, y0=-1.4, y1=1.8, feet_y=2.871):
    """feet-relative sprite canvas around a left arm reaching left (head and hat excluded: x1 < -0.8)."""
    g = 1 / 16.0
    return (math.floor(x0 / g) * g, math.floor((y0 - feet_y) / g) * g, math.ceil(x1 / g) * g, math.ceil((y1 - feet_y) / g) * g)


def qa_motion(M):
    """corner speed per frame (post.camera_motion on the true camera), moves, static runs (< 0.25 px/frame) and constant-speed
    runs (speed changing < 2 % per frame while moving > 1 px/frame) of a take."""
    import numpy as np
    pl = streak_plan(M)
    sp = np.array([s for g, s, m in pl]); gs = [g for g, s, m in pl]

    def runs(flags):
        out, s = [], None
        for i, f in enumerate(flags):
            if f and s is None:
                s = i
            if (not f) and s is not None:
                out.append((gs[s], gs[i - 1])); s = None
        if s is not None:
            out.append((gs[s], gs[-1]))
        return out
    static = [r for r in runs(sp < 0.25) if r[1] - r[0] + 1 > 6]
    rel = np.abs(np.diff(sp)) / np.maximum(sp[:-1], 1e-6)
    lin = [r for r in runs(list((rel < 0.02) & (sp[:-1] > 1.0)) + [False]) if r[1] - r[0] + 1 >= 6]
    moves = []
    for a, b in runs(sp > 12.0):
        seg = [s for g, s, m in pl if a <= g <= b]
        moves.append(dict(start=a, end=b, peak=round(max(seg), 1), t0=round(a / 30.0, 2), t1=round((b + 1) / 30.0, 2)))
    return dict(speed=[round(float(s), 1) for s in sp], g=gs, static_over6=static, linear_runs=lin, moves=moves,
                streaked=[g for g, s, m in pl if s >= POST.STREAK_MIN])
