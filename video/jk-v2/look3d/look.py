"""Look test in the real-3D plaza: EP.2 climax (m09 + m10, 13.2 s): extreme wide -> crane in, low angle on Ken, crowd, hero close-up, sword to the throat.
usage: python3 look.py sprites | render [a:b] [--draft] | frames"""
import os, sys, json, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30; DUR = 13.18; N = int(round(DUR * FPS)); PORT = 8775
SPR = os.path.join(HERE, 'spr'); RAW = os.path.join(HERE, 'raw')
C = (0.0, -4.6)
KEN = (-1.0, -4.6, 0.0); HERO = (0.89, -4.6, 0.0)
PAIR_DX = 650   # rig px from Ken's feet to the hero's feet: the blade tip (jkKenLSA, arm -73) lands on the kneeling hero's throat
EAR = """document.querySelectorAll('#'+AID+' .jkEar').forEach(function(e){ tl.set(e,{opacity:1},0); for(var k=0;k<60;k++){ tl.set(e,{opacity:0.45},k*0.3+0.15); tl.set(e,{opacity:1},k*0.3+0.3);} });"""
PRE = "Rig.MODES.kneelHands = (u, o) => { const j = Math.sin(u * 37) * 1.4; return { ...Rig.MODES.kneelUp(u, o), uaF: -150 + j, faF: -25, uaB: -150 - j, faB: -25 }; };"
CROWD = [('jkMan2', -4.2, -2.6), ('jkWom1', -2.6, -1.9), ('jkMan3', -0.9, -1.5), ('jkAunt', 1.3, -1.6), ('jkMan1', 3.0, -2.0), ('jkMan3', 4.5, -2.8),
         ('jkWom1', -5.4, -4.6), ('jkMan1', 5.5, -4.8), ('jkMan3', -5.0, -6.8), ('jkAunt', 5.2, -7.0), ('jkMan2', -3.4, -8.6), ('jkWom1', 3.2, -8.8)]
def crowd_track(i):
    calm = ['idle', 'idle', 'point', 'idle', 'raise', 'idle'][i % 6]
    return [{'t': 0, 'mode': 'idle', 'eyes': 'wide', 'mouth': 'o'}, {'t': 1.9 + 0.13 * (i % 4), 'mode': 'laugh' if i % 3 == 0 else 'idle', 'eyes': 'happy' if i % 3 == 0 else 'wide', 'mouth': 'laugh' if i % 3 == 0 else 'o'},
            {'t': 5.25 + 0.07 * (i % 5), 'mode': 'point' if i % 2 else 'idle', 'eyes': 'angry', 'mouth': 'frown'}]
SHOTS = [  # (start, end, camera keys [(t, loc, look, lens, ease)], ppx for leads, ppx crowd)
    ('S1', 0.0, 3.0, [(0.0, (5, -27, 18), (0, -4.5, 1.0), 22), (0.35, (4.8, -26.6, 17.7), (0, -4.5, 1.0), 22, 'l'), (3.0, (1.4, -12.5, 3.2), (-0.1, -4.4, 1.3), 30, 's')], 0.7, 0.45),
    ('S2', 3.0, 5.2, [(3.0, (-0.25, -6.7, 0.32), (-1.0, -4.6, 1.75), 23), (5.2, (0.15, -6.35, 0.38), (-0.9, -4.6, 1.85), 25, 'l')], 1.8, 0.8),
    ('S3', 5.2, 6.48, [(5.2, (0.6, -6.4, 1.75), (-2.6, -2.0, 1.55), 26), (6.48, (0.9, -6.1, 1.7), (-2.2, -2.0, 1.55), 27, 'l')], 1.2, 1.1),
    ('S4', 6.48, 9.42, [(6.48, (1.15, -7.6, 1.55), (0.9, -4.6, 1.35), 34), (9.42, (1.05, -7.0, 1.5), (0.9, -4.6, 1.3), 42, 'o')], 2.2, 0.9),
    ('S5', 9.42, DUR, [(9.42, (-0.1, -9.6, 1.05), (-0.05, -4.6, 0.95), 28), (10.15, (-0.05, -9.2, 1.05), (-0.05, -4.6, 0.95), 28, 'l'),
                      (10.75, (0.35, -6.9, 0.95), (0.45, -4.6, 0.86), 30, 'q'), (DUR, (0.4, -6.6, 0.93), (0.48, -4.6, 0.86), 31, 'l')], 2.0, 0.7),
]
def shot_of(t):
    for s in SHOTS:
        if s[1] <= t < s[2]: return s
    return SHOTS[-1]

def actors_in(shot):
    """[(name, job spec without frames, world pos, flip-free scale)]"""
    nm = shot[0]; L = []
    if nm != 'S5':
        L.append(('hero', dict(who='jkYouBag', canvas=[-460, -980, 460, 140], track=[{'t': 0, 'mode': 'raise', 'eyes': 'wide', 'mouth': 'scream'}, {'t': 6.48, 'mode': 'idle', 'eyes': 'sad', 'mouth': 'pout', 'sweat': True}], flip=True, extra=EAR), HERO, 1.0))
        L.append(('ken', dict(who='jkKen', canvas=[-380, -820, 640, 140], track=[{'t': 0, 'mode': 'point', 'eyes': 'happy', 'mouth': 'laugh'}, {'t': 1.69, 'mode': 'point', 'eyes': 'wide', 'mouth': 'laugh'}, {'t': 5.2, 'mode': 'point', 'eyes': 'angry', 'mouth': 'frown'}],
                          talk=[[1.8, 5.1, 'o']], flip=False), KEN, 0.95))
    else:
        L.append(('pair', dict(canvas=[-520, -900, 1250, 140], actors=[
            dict(who='jkKenLSA', dx=0, flip=False, track=[{'t': 0, 'mode': 'lunge', 'opts': {'arm': -118}, 'eyes': 'angry', 'mouth': 'scream'}, {'t': 10.2, 'mode': 'lunge', 'opts': {'arm': -73}, 'blend': 0.16, 'eyes': 'angry', 'mouth': 'frown'}]),
            dict(who='jkYou', dx=PAIR_DX, flip=True, track=[{'t': 0, 'mode': 'kneelHands', 'eyes': 'wide', 'mouth': 'scream'}])], extraAid='x1'), KEN, 0.95))
    for i, (who, x, y) in enumerate(CROWD):
        L.append((f'c{i}', dict(who=who, canvas=[-330, -800, 420, 120], track=crowd_track(i), flip=x > 0), (x, y, 0.0), 0.92))
    return L

def frames_of(shot): return [g for g in range(N) if shot[1] <= g / FPS < shot[2]]

def cmd_sprites():
    jobs = []
    for sh in SHOTS:
        fr = frames_of(sh)
        for (nm, spec, pos, sc) in actors_in(sh):
            ppx = (sh[3] if not nm.startswith('c') else sh[4])
            d = os.path.join(SPR, nm); os.makedirs(d, exist_ok=True)
            j = dict(id=f'{nm}_{sh[0]}', dur=DUR + 1, ppx=ppx, pre=PRE, frames=[dict(t=g / FPS, out=os.path.join(d, f'{g:04d}.png')) for g in fr])
            j.update({k: v for k, v in spec.items() if k not in ('talk', 'extraAid', 'extra')})
            if 'talk' in spec: j['track'] = j['track']; j['actors'] = [dict(who=spec['who'], track=spec['track'], flip=False)]; j['actors'][0]['track'] = spec['track']
            ex = spec.get('extra'); aid_sfx = spec.get('extraAid', '')
            if nm == 'pair': ex = EAR; aid_sfx = 'x1'
            if ex: j['extra'] = "var AID = aid + '" + aid_sfx + "'; " + ex
            if 'talk' in spec: j['talkTrack'] = spec['talk']
            jobs.append(j)
    # talk: rig tracks carry .talk as a property of the array; pass through 'talk' on the actor
    for j in jobs:
        if 'talkTrack' in j:
            j['actors'][0]['talk'] = j.pop('talkTrack')
    if ONLY: jobs = [j for j in jobs if any(j['id'].startswith(o) for o in ONLY)]
    jp = os.path.join(HERE, 'look_jobs.json' if not ONLY else 'look_jobs_part.json'); json.dump(jobs, open(jp, 'w'))
    r = subprocess.run(['node', os.path.join(HERE, 'sprites.cjs'), str(PORT), jp], capture_output=True, text=True)
    print(r.stderr[-2000:]); print('sprites done', len(jobs))

def cmd_render(rng=None, draft=False):
    import bpy, stage3d as G
    A = G.T.build(); scene = bpy.context.scene
    scene.cycles.samples = 6 if draft else 12; scene.render.resolution_percentage = 50 if draft else 100
    scene.render.threads_mode = 'FIXED'; scene.render.threads = 4
    coll = G.S._coll('ACTORS', scene); cards = {}
    cam = G.S.make_camera(dict(loc=(0, -10, 2), look_at=(0, 0, 1.5), lens=22), name='cam')
    out = RAW + ('_draft' if draft else ''); os.makedirs(out, exist_ok=True)
    a, b = (0, N) if not rng else map(int, rng.split(':'))
    import time
    for g in range(a, b):
        t = g / FPS; sh = shot_of(t); loc, look, lens = G.cam_at(SHOTS_KEYS[sh[0]], t)
        G.place_cam(cam, loc, look, lens)
        vis = set()
        for (nm, spec, pos, sc) in actors_in(sh):
            png = os.path.join(SPR, nm, f'{g:04d}.png')
            if nm not in cards: cards[nm] = G.Card(nm, spec['canvas'], coll)
            cards[nm].set(pos, loc, png, sc); vis.add(nm)
        for nm, c in cards.items():
            if nm not in vis: c.set(None, None, None, hidden=True)
        scene.render.filepath = os.path.join(out, f'f_{g:04d}.png'); t0 = time.time(); bpy.ops.render.render(write_still=True)
        print(f'frame {g} {sh[0]} {time.time() - t0:.1f}s', flush=True)

ONLY = [a for a in sys.argv[2:] if not a.startswith('-')] if len(sys.argv) > 1 and sys.argv[1] == 'sprites' else []
SHOTS_KEYS = {s[0]: s[3] for s in SHOTS}
# normalise: (name, start, end, ppx_lead, ppx_crowd) for actors/frames, keys in SHOTS_KEYS
SHOTS = [(s[0], s[1], s[2], s[4], s[5]) for s in SHOTS]

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'sprites': cmd_sprites()
    elif c == 'render': cmd_render(sys.argv[2] if len(sys.argv) > 2 and ':' in sys.argv[2] else None, '--draft' in sys.argv)
