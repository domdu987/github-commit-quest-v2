"""T5a local override (director fix list): 5b OTS push to the inspector, lights up. Import after prefecture17; call apply()."""
import sys, math
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d17')
import prefecture17 as P
from mathutils import Vector
_orig_path = P.path_take
G_A, G_B = 1196, 1211          # blend back to the prepared path over g1196-1210; g1211 == prepared
MY_KEYS = [                    # inspector at (15.4, 15.0): %H = 1.66*fpx/(d*1280)
    P._k(1100, (15.0, 30.8, 3.6), (15.9, 27.6, 1.7), 22.0),               # = prepared key g1100 (over Bertillon's shoulder)
    P._k(1118, (16.5, 29.7, 2.9), (15.4, 17.0, 1.9), 45.0),
    P._k(1135, (17.5, 26.9, 3.5), (15.4, 15.0, 1.75), 96.0),
    P._k(1160, (17.8, 22.6, 3.2), (15.4, 15.0, 1.7), 78.0),
    P._k(1196, (18.6, 18.0, 2.2), (15.4, 15.0, 1.7), 44.0, hold=True)]
def _mine_frames(): return P.cam_path([dict(k) for k in MY_KEYS], 1100, G_B)
def path_t5():
    base = _orig_path('T5'); mine = {f['g']: f for f in _mine_frames()}; out = []
    for f in base:
        g = f['g']
        if g < 1100 or g >= G_B and False: out.append(f); continue
        if g >= G_B: out.append(f); continue
        m = mine[g]
        if g > G_A:
            u = (g - G_A) / (G_B - G_A); u = u * u * (3 - 2 * u)
            loc = tuple((1 - u) * a + u * b for a, b in zip(m['loc'], f['loc'])); look = tuple((1 - u) * a + u * b for a, b in zip(m['look'], f['look']))
            lens = math.exp((1 - u) * math.log(m['lens']) + u * math.log(f['lens']))
            q = P._lookrot(loc, look); out.append(dict(g=g, loc=loc, look=look, rot=tuple(q), lens=lens))
        else: out.append(m)
    # quaternion sign continuity
    import mathutils; prev = None
    for f in out:
        q = mathutils.Quaternion(f['rot'])
        if prev is not None and q.dot(prev) < 0: q.negate(); f['rot'] = tuple(q)
        prev = q
    return out
def apply():
    P.path_take = lambda take: path_t5() if take == 'T5' else _orig_path(take)
    L = P.K.LIGHTS['ARCHIVE_NIGHT']; L.update(fill_w=230, lamp_k=1.0, gasolier_k=0.7)
if __name__ == '__main__':
    apply(); fr = P.path_take('T5'); T = P.TAKES['T5']['cast']; byname = {c['name']: c for c in T}
    pr = 0
    for f in fr:
        g = f['g']
        if g < 1100 or g > 1215: continue
        i = [x['g'] for x in fr].index(g); sp = (Vector(fr[min(i+1, len(fr)-1)]['loc']) - Vector(fr[max(i-1, 0)]['loc'])).length * 15
        ins = P.anchor_frac(f, P.cast_pos(byname['inspector'], g), P.HCAST['inspector'])
        if g in (1111, 1128, 1135, 1150, 1160, 1190, 1196, 1203, 1211) or sp > 6: print(g, 'speed %.1f' % sp, 'insp %%H %.1f in=%s d=%.1f' % (ins[0]*100, ins[1], ins[2]), 'lens %.1f' % f['lens'])
