#!/usr/bin/env python3
"""b1.py -- film 21 segment B1 (g 159..298 + 3 handle frames 299..301): "คืออย่างนี้นะ สกอตแลนด์ เจ็ดร้อยกว่าปีก่อน".
High over the valley, the camera glides south over the river, banks left and swoops DOWN into the English camp, passes the "ENGLISH CAMP" sign, banners and
smoke shafts, and lands EXACTLY at P_CAMP (the camp_wide camera) at g 298 as the knights parade (narration 7.74 = g 235 'ทัพอังกฤษ', 8.29 'มีอัศวินม้าเกราะ').
    python3 b1.py path_draft                       10 fps 360x640 draft of the path (no cast) -> work/pd/*.png
    python3 b1.py probe <g list>                   camera + heads numbers
    python3 b1.py stills <g list> <out_dir> [scale] [samples]
    python3 b1.py final <g list> [samples]         raw/g_%04d.png (resumable)
"""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c21 as C
import numpy as np
from mathutils import Vector
K, cast21, bpy, actors, camrig, sprites = C.K, C.cast21, C.bpy, C.actors, C.camrig, C.sprites
S21 = cast21.STORY21
SC = C.SC

G0, G1, GH = 159, 298, 301          # first g, P_CAMP landing, last handle frame
PRESETS = ['camp_wide', 'valley_wide']      # camp_wide FIRST: the ENGLISH CAMP sign faces the first preset's camera (P_CAMP)


def keys():
    ext_loc, ext_look = (-62.0, -85.0, 14.5), (28.0, -43.0, 2.0)          # beyond P_CAMP: the move continues up and forward (NE), for the 3 handle frames
    return [(159, (-112, 300, 195), (-86, -85, 0), 22.0),
            (192, (-108, 120, 125), (-80, -115, 2), 22.0),
            (222, (-100, -14, 70), (-60, -100, 4), 22.0),
            (250, (-102, -92, 28), (-36, -90, 6), 22.0),
            (276, (-94, -108, 18.5), (-6, -72, 3), 22.0),
            (298, 'P_CAMP'),
            (310, ext_loc, ext_look, 22.0)]


def cam_at(g):
    return K.cam_path(None, keys(), g)


def hooks(g):
    t = g / 30.0
    K.set_flutter(t); K.set_smoke(t); K.set_flow(t)


def idle(g, k=0, lean=1.2, roll=1.5):
    return dict(lean=lean * math.sin(g * 0.071 + k * 1.7), head_roll=roll * math.sin(g * 0.053 + k * 2.3), blink=C.blink_at(g, 84 + 7 * k, 11 * k))


class Member(object):
    def __init__(self, actor, xyz_fn, base, k, fn=None, riding=False, walk=None):
        self.a, self.xyz_fn, self.base, self.k, self.fn, self.riding, self.walk = actor, xyz_fn, base, k, fn, riding, walk


class World(object):
    def __init__(self, quality='final', samples=32, threads=2):
        t0 = time.time()
        self.A = K.build_world(PRESETS, fg=['camp_wide'])
        self.pr = K.PRESETS['camp_wide']
        n = 0
        for o in bpy.data.objects:                      # the set's own 3D parade (boxy riders) is replaced by the cast cards
            if o.name.startswith('parade'):
                o.hide_render = True; o.hide_viewport = True; n += 1
        sc = self.scene = bpy.context.scene
        self.quality, self.samples = quality, samples
        K.setup_render(sc, quality, samples)
        sc.render.threads_mode = 'FIXED'; sc.render.threads = threads; sc.render.use_persistent_data = False
        sc.cycles.denoising_prefilter = 'FAST'
        sc.frame_start, sc.frame_end = 1, 9000
        self.cam = camrig.make_camera(sc, name='cam_b1', lens=22.0)
        self.cam.data.clip_start = 0.05; self.cam.data.clip_end = 9000.0; self.cam.data.dof.use_dof = False
        K.setup_render(sc, quality, samples); sc.render.threads_mode = 'FIXED'; sc.render.threads = threads
        self.actors = {}; self.cast = []; self.res = {}
        self.sprite_dir = os.path.join(HERE, 'work', 'sprites')
        self.stage()
        print('world built in %.1f s (parade hidden %d)' % (time.time() - t0, n), flush=True)

    def ground(self, x, y):
        return float(K.ground(x, y))

    def add_actor(self, name, cast):
        a = actors.Actor(name, cast)
        a.build(sprites.DEFAULT_CANVAS[cast], self.sprite_dir, contact=True, shadow='proxy')
        a.head_flip = False
        self.actors[name] = a
        return a

    def stage(self):
        pr = self.pr
        left = (-0.439, 0.898)                           # screen-left at P_CAMP = toward the bridge
        riders = [("r1", "knight_a_mtd", "knight_a_mounted", 31.0, 420, "red"), ("r2", "knight_b_mtd", "knight_b_mounted", 35.0, 340, "red"),
                  ("r3", "knight_a_open_mtd", "knight_a_mounted", 39.0, 270, "gold"), ("r4", "knight_b_great_mtd", "knight_b_mounted", 43.0, 200, "red"),
                  ("r5", "knight_a_mtd", "knight_a_mounted", 47.0, 130, "red"), ("r6", "knight_b_mtd", "knight_b_mounted", 34.0, 470, "gold"),
                  ("r7", "knight_a_open_mtd", "knight_a_mounted", 37.0, 560, "red"), ("r8", "knight_b_great_mtd", "knight_b_mounted", 41.0, 600, "red"),
                  ("r9", "knight_a_mtd", "knight_a_mounted", 45.0, 520, "gold"), ("r10", "knight_b_mtd", "knight_b_mounted", 50.0, 450, "red")]
        for i, (nm, cast_, base, d, xp, cap) in enumerate(riders):
            x0, y0 = K.at_px(pr, d, xp)
            def xyz(g, x0=x0, y0=y0):
                t = (g - G1) / 30.0
                x, y = x0 + left[0] * 1.35 * t, y0 + left[1] * 1.35 * t
                return (x, y, self.ground(x, y))
            self.cast.append(Member(self.add_actor(nm, cast_), xyz, base, i, fn=(lambda p, cap=cap: dict(p, mode21='walk', horse21=cap, mirror=True)), riding=True))
        foot = [("f1", "footman_a", 50.0, 110, 0), ("f2", "footman_b", 53.0, 190, 1), ("f3", "footman_a", 47.0, 330, 2), ("f4", "footman_b", 55.0, 440, 3),
                ("f5", "footman_a", 51.0, 540, 1), ("f6", "footman_a", 58.0, 610, 2), ("f7", "footman_b", 36.0, 600, 0), ("f8", "footman_a", 33.0, 70, 3),
                ("f9", "footman_a", 41.0, 670, 2), ("f10", "footman_b", 44.0, 380, 1), ("f11", "footman_a", 39.0, 150, 2), ("f12", "footman_b", 46.0, 290, 3)]
        for i, (nm, cast_, d, xp, v) in enumerate(foot):
            x, y = K.at_px(pr, d, xp); z = self.ground(x, y)
            self.cast.append(Member(self.add_actor(nm, cast_), (lambda g, p=(x, y, z): p), cast_ + "_stand", 10 + i,
                                    fn=(lambda p, v=v, i=i: dict(p, mirror=bool(i % 2)))))
        # walkers: a file of footmen marching along the camp lane toward the bridge (spears up), walk cycle
        for i in range(6):
            cast_ = ("footman_a", "footman_b")[i % 2]
            d = 36.0 + 3.0 * i; xp = 90 + 95 * i
            x0, y0 = K.at_px(pr, d, xp)
            def xyz(g, x0=x0, y0=y0):
                t = (g - G1) / 30.0
                x, y = x0 + left[0] * 1.5 * t, y0 + left[1] * 1.5 * t
                return (x, y, self.ground(x, y))
            self.cast.append(Member(self.add_actor("w%d" % (i + 1), cast_), xyz, None, 30 + i, fn=None, walk=cast_))

    def key_cam(self, f, loc, look, lens):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp='LINEAR', easing='AUTO')

    def pose(self, gs):
        for g in gs:
            r = cam_at(g); self.key_cam(C.bf(g), r['loc'], r['look'], r['lens'])
        for g in gs:
            f = C.bf(g); self.scene.frame_set(f)
            for m in self.cast:
                m.a.place(f, m.xyz_fn(g), scale=SC)
                if m.walk:
                    p = dict(cast21.walk_spear(m.walk, ((g + 7 * m.k) / 28.0) % 1.0, -1, 'march'))
                elif m.riding:
                    p = dict(S21[m.base][1]); p.update(gait=((g + 9 * m.k) / 40.0) % 1.0, t=((g + 13 * m.k) / 70.0) % 1.0, blink=C.blink_at(g, 90 + 5 * m.k, 13 * m.k), lean=0.8 * math.sin(g * 0.09 + m.k))
                else:
                    p = dict(S21[m.base][1]); p.update(idle(g, m.k))
                if m.fn:
                    p = m.fn(p)
                for kk in ('prop_r', 'prop_l'):
                    if isinstance(p.get(kk), dict) and p[kk].get('type') == 'spear21':
                        p[kk] = dict(p[kk], scale=1.1)
                m.a.pose(f, K.with_rim(p), camera=self.cam)
        fr = [C.bf(g) for g in gs]
        for a in self.actors.values():
            ff = [f for f in fr if f in a.poses]
            for f, r in zip(ff, a.render_sprites(256, frames=ff)):
                self.res[(a.name, f)] = r

    def head(self, name, f):
        a = self.actors[name]; self.scene.frame_set(f); bpy.context.view_layer.update()
        r = self.res.get((name, f))
        if not r: return None
        hx, hy = r['anchors']['head']; c = actors.local_to_screen(a, self.cam, (hx, hy), f, a.feet.get(f))
        k = 720.0 / self.scene.render.resolution_x
        return round(c[0] * k), round(c[1] * k)

    def render_frame(self, g, out_png, pct=100):
        f = C.bf(g); sc = self.scene
        sc.frame_set(f)
        hooks(g)
        r_ = cam_at(g)                             # sets STATE['vivid'] (and the K camera); the render camera is the stage camera
        v_ = list(r_['vivid']) + [1.0] * (3 - len(r_['vivid']))
        w_ = max(0.0, min(1.0, min((g - 192) / 22.0, (272 - g) / 27.0)))      # the steep mid-dive (g ~205-250) looks into the shade: lift it so it is not murky
        K.STATE['vivid'] = (v_[0] + (1.5 - v_[0]) * w_, v_[1], v_[2] + (1.32 - v_[2]) * w_)
        actors.sync_all(sc, self.cam); sc.camera = self.cam
        sc.render.filepath = out_png; sc.render.resolution_percentage = pct
        t0 = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t0
        if pct == 100: K.grade(out_png)
        return dt


def main():
    cmd = sys.argv[1]
    if cmd == 'path_draft':
        W = World('draft', 8, 4)
        out = os.path.join(HERE, 'work', 'pd'); os.makedirs(out, exist_ok=True)
        gs = list(range(G0, GH + 1, 3))
        W.pose(gs)
        for g in gs:
            dt = W.render_frame(g, os.path.join(out, 'pd_%04d.png' % g))
            print(g, '%.1fs' % dt, flush=True)
        return
    gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= GH]
    if cmd == 'probe':
        W = World('draft', 6, 4); W.pose(gs)
        for g in gs:
            r = cam_at(g); print(g, [round(float(v), 1) for v in r['loc']], {m.a.name: W.head(m.a.name, C.bf(g)) for m in W.cast if m.a.name[0] in 'rf'}, flush=True)
    elif cmd == 'stills':
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 8
        os.makedirs(out, exist_ok=True)
        W = World('draft' if scale < 1 else 'final', samples); W.pose(gs)
        for g in gs:
            dt = W.render_frame(g, os.path.join(out, 'b1_%04d.png' % g)); print('g', g, '%.1fs' % dt, flush=True)
    elif cmd == 'final':
        samples = int(sys.argv[3]) if len(sys.argv) > 3 else 32
        out = os.path.join(HERE, 'raw'); os.makedirs(out, exist_ok=True)
        todo = []
        for g in gs:
            png, js = os.path.join(out, 'g_%04d.png' % g), os.path.join(out, 'g_%04d.json' % g)
            if os.path.exists(png) and os.path.exists(js) and json.load(open(js)).get('samples') == samples: continue
            todo.append(g)
        print('final: %d to render, %d done' % (len(todo), len(gs) - len(todo)), flush=True)
        if not todo: return
        W = World('final', samples); W.pose(todo)
        for g in todo:
            png = os.path.join(out, 'g_%04d.png' % g)
            dt = W.render_frame(g, png + '.tmp.png'); os.replace(png + '.tmp.png', png)
            r = cam_at(g)
            json.dump(dict(g=g, samples=samples, wall=round(dt, 1), cam=[round(float(v), 3) for v in r['loc']], look=[round(float(v), 3) for v in r['look']], vivid=[round(float(v), 3) for v in r['vivid']],
                           heads={m.a.name: W.head(m.a.name, C.bf(g)) for m in W.cast}), open(png[:-4] + '.json', 'w'))
            print('g', g, '%.1f s' % dt, flush=True)


if __name__ == '__main__':
    main()
