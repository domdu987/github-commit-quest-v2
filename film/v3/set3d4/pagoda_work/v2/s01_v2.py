#!/usr/bin/env python3
"""s01_v2.py : the five s01 shots (cameras, staging and poses of v3/film4/s01/shot.py, cast4 actors) re-rendered on the v2 set,
with the set's depth of field; compare2.jpg = per shot  new | old s01 frame | reference.
    python3 s01_v2.py [shots e.g. 1,2,3,4,5] [scale 1.0] [samples 12]"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); SET = os.path.dirname(os.path.dirname(HERE)); V3 = os.path.dirname(SET); PROJ = os.path.dirname(V3)
S01 = os.path.join(V3, 'film4', 's01'); sys.path.insert(0, S01)
import shot as S                                   # noqa: E402 (imports cast4, bpy, the v2 pagoda set)
import pagoda as G                                 # noqa: E402
S.build_dressing = lambda: []                      # the set carries the dressing now (v2); shot.py's would double it
PAIRS = [(1, 20, 1), (2, 60, 3), (3, 95, 5), (4, 166, 7), (5, 230, 31)]
OUT = os.path.join(HERE, 's01')

def dof_for(Tk, shot):
    from mathutils import Vector
    if shot in (1, 4): return Tk.kenta.card, (3.5 if shot == 1 else 6.0)
    if shot == 2: return (0.2, -0.62, G.FOOT_Z + 0.5), 6.0
    if shot == 3: return (-3.6, -3.4, 6.0), 7.0
    return None, None

if __name__ == '__main__':
    shots = [int(s) for s in (sys.argv[1] if len(sys.argv) > 1 else '1,2,3,4,5').split(',')]
    scale = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0; samples = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    os.makedirs(OUT, exist_ok=True)
    Tk = S.Take(quality='final'); log = {}
    for shot, g, _ in PAIRS:
        if shot not in shots: continue
        Tk.pose(shot, [g]); Tk.scene.frame_set(S.bf(shot, g)); Tk.scene.camera = Tk.cam
        foc, fs = dof_for(Tk, shot); G.setup_dof(Tk.scene, foc, fs, cam=Tk.cam)
        st = Tk.render(shot, [g], OUT, scale=scale, samples=samples)[0]
        dst = os.path.join(OUT, 's%d_g%04d.png' % (shot, g)); os.replace(st['path'], dst)
        log[shot] = dict(wall=round(st['wall'], 1), cpu=round(st['cpu'], 1)); print('shot %d g %d: %.1f s wall, %.1f s cpu' % (shot, g, st['wall'], st['cpu']), flush=True)
    lp = os.path.join(OUT, 'log.json'); old = json.load(open(lp)) if os.path.exists(lp) else {}
    old.update({str(k): v for k, v in log.items()}); json.dump(old, open(lp, 'w'), indent=1)
    from PIL import Image, ImageDraw
    w, h, lab, gap = 360, 640, 22, 14
    C = Image.new('RGB', (len(PAIRS) * (3 * w + gap) - gap, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C); x = 0
    for shot, g, tref in PAIRS:
        new = os.path.join(OUT, 's%d_g%04d.png' % (shot, g))
        for k, (pth, txt, col) in enumerate(((new, 'v2 shot %d g %d' % (shot, g), (160, 255, 160)), (os.path.join(S01, 'frames', 'g_%04d.png' % g), 'old s01 g %d' % g, (255, 255, 255)),
                                            (os.path.join(PROJ, 'ref', 'a', 't%04d.jpg' % tref), 'ref a t%04d' % tref, (255, 220, 160)))):
            if os.path.exists(pth): C.paste(Image.open(pth).convert('RGB').resize((w, h), Image.LANCZOS), (x + k * w, lab))
            dr.text((x + k * w + 4, 5), txt, fill=col)
        x += 3 * w + gap
    C.save(os.path.join(SET, 'compare2.jpg'), quality=90); print('compare2.jpg written')
