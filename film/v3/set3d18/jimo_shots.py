"""jimo_shots.py : the shot table of film 18 (film18/shot_plan.md): one named camera per shot s01..s26 (start pose + the move: eased push / pull 6-10 % of the framing per second,
lateral slide in px/s, snaps, whips), the light, the set state at the shot's middle, foreground prop, stand marks for the 2D puppets (world points), herd layouts.
Pure python (no bpy).  Camera conventions: loc / look_at in world D, lens in mm (36 mm sensor on the 1280 px side; 720x1280 portrait: horizontal half FOV = atan(10.125 / lens))."""
import math
from collections import OrderedDict

HEIGHT = dict(tiandan=3.0, general=3.4, soldier=3.2, townsfolk=3.0, child=2.0, envoy=3.0, ox=2.6, qi_soldier=3.2)
DEFAULT = dict(
    jimo_in=dict(loc=(0.0, 36.0, 2.6), look_at=(0.0, 4.0, 8.0), lens=22),
    jimo_out=dict(loc=(-6.0, -56.0, 9.5), look_at=(3.0, 0.0, 17.6), lens=20),
    yan_camp=dict(loc=(0.0, -112.0, 3.3), look_at=(0.0, 0.0, 11.0), lens=16.5),
    vista=dict(loc=(40.0, -250.0, 150.0), look_at=(0.0, 60.0, 0.0), lens=22),
)
SHOTS = OrderedDict()
def CRENEL_GAPS(*xs):
    """Centre x of the nearest crenel gap (merlons every 3.4 D from x -94, 2.0 wide) for each wanted x: cards on the wall walk stand IN a gap of the parapet."""
    out = []
    for x in xs:
        k = round((x + 91.3) / 3.4); out.append(round(-91.3 + 3.4 * k, 2))
    return out

def _v(a): return tuple(float(x) for x in a)
def _fwd(c):
    d = (c['look_at'][0] - c['loc'][0], c['look_at'][1] - c['loc'][1]); n = math.hypot(*d) or 1.0; return d[0] / n, d[1] / n
def ahead(c, dist, lat=0.0, z=0.0):
    """Ground point `dist` D ahead of the camera along its horizontal heading and `lat` D to the right (lat < 0 left), at height z."""
    fx, fy = _fwd(c); rx, ry = fy, -fx
    return (round(c['loc'][0] + fx * dist + rx * lat, 2), round(c['loc'][1] + fy * dist + ry * lat, 2), z)
def face(mark, c):
    """Yaw (deg, about z) that turns a card whose front faces -y at yaw 0 toward the camera start position."""
    dx, dy = c['loc'][0] - mark[0], c['loc'][1] - mark[1]; return round(math.degrees(math.atan2(dx, -dy)), 1)

def shot(n, f0, f1, loc, light, cam, move, state='', fg=None, note='', marks=None, sun=None):
    SHOTS['s%02d' % n] = dict(n=n, f0=f0, f1=f1, frames=f1 - f0, dur=(f1 - f0) / 30.0, loc=loc, light=light, cam=cam, move=move, state=state, fg=fg, note=note, marks=marks or (lambda c: {}), sun=sun)

def C(loc, look, lens=22): return dict(loc=_v(loc), look_at=_v(look), lens=float(lens))

# ---- helpers for marks
def pts(c, items):
    """items: role -> [(dist, lat[, z])] -> {role: [(x, y, z, yaw)]}"""
    out = {}
    for role, lst in items.items():
        out[role] = []
        for it in lst:
            p = ahead(c, it[0], it[1], it[2] if len(it) > 2 else 0.0); out[role].append(p + (face(p, c),))
    return out

# ============================================================== JIMO_IN
shot(1, 0, 78, 'jimo_in', 'NIGHT', C((-14, 26, 2.5), (4, 8, 4.2), 24), dict(push=0.08, slide=40),
     fg=('lantern', 'right'), note='lantern-lit ox yard, eye, push 8 %/s, slide right; Tian Dan dresses an ox, a row of dressed oxen along the wall behind',
     marks=lambda c: dict(tiandan=[(-4.1, 16.8, 0.0, 0.0)], ox=[(-1.2, 15.2, 0.0, 165.0, 1.0)] + [(x, 7.4 + 0.5 * (k % 2), 0.0, 180.0, 1.0) for k, x in enumerate((-15.0, -9.5, -4.0, 1.5, 7.0, 12.5))]))
shot(2, 78, 156, 'jimo_in', 'NIGHT', C((-28, 11.5, 1.2), (12, 10.5, 3.0), 20), dict(push=-0.07, slide=0),
     fg=('pick_baskets', 'left'), note='low 1.2 D along the ring lane, pull-out reveals dozens of dressed oxen filling the lane (herd helper)',
     marks=lambda c: dict(tiandan=[(-24.5, 10.2, 0.0, 0.0)], ox=[(-21.8, 8.4, 0.0, 180.0, 1.0)], herd=herd(34, (-21, 10.6), (30, 10.6), 6.0, 5, yaw=180.0)))
shot(5, 384, 459, 'jimo_in', 'DUSK', C((-69.5, 18.5, 2.6), (-76.5, 22.5, 2.8), 24), dict(push=0.08, slide=0), sun=325.0,
     fg=('counter', 'right'), note='market lane, the clerk stall at (-77, 22) faces +x; Tian Dan behind the counter, townsfolk hand him a sash',
     marks=lambda c: dict(tiandan=[(-76.0, 22.0, 0.0, 90.0)], townsfolk=[(-75.2, 20.6, 0.0, 130.0), (-75.2, 23.8, 0.0, 230.0), (-76.0, 25.6, 0.0, 200.0)], child=[(-76.8, 24.6, 0.0, 190.0)]))
shot(6, 459, 531, 'jimo_in', 'DUSK', C((84, 9.0, 2.4), (72, 22.0, 2.6), 22), dict(push=0.0, slide=-40), sun=320.0,
     fg=None, note='eye, slides left 40 px/s along the ring lane in front of the house gates (x 58 / 74 / 89, y 23); townsfolk lead oxen out of the gates; ten oxen at "สิบตัว"',
     marks=lambda c: dict(tiandan=[(76.0, 12.5, 0.0, 180.0)], townsfolk=[(58.0, 19.5, 0.0, 180.0), (74.0, 19.5, 0.0, 180.0), (86.0, 19.5, 0.0, 180.0), (66.0, 11.0, 0.0, 180.0)],
                          herd=herd(10, (60, 15.0), (93, 16.0), 3.0, 6, yaw=190.0)))
shot(7, 531, 597, 'jimo_in', 'DUSK', C((0, 46, 20), (0, 14, 0), 20), dict(push=-0.05, slide=0, moves=[dict(t=0.55, d=1.6, dur=7)]), sun=80.0,
     fg=None, note='high 4-5 D from the north end of the yard, pull-out with a snap x1.6 on "พันกว่าตัว": the whole quarter packed with oxen (herd helper ~200 + silhouettes)',
     marks=lambda c: dict(herd=herd(170, (-28, 13.5), (28, 26.0), 12.0, 7, yaw=-20.0), herd_pen=herd(40, (-15, 36.0), (15, 36.0), 8.0, 17, yaw=-60.0), herd_far=herd(60, (-34, 8.4), (34, 8.4), 3.0, 8, yaw=0.0) + herd(40, (52, 21), (94, 22), 9.0, 9, yaw=30.0)))
shot(16, 1205, 1309, 'jimo_in', 'NIGHT', C((50, 16, 2.6), (30, 4, 2.2), 22), dict(push=0.0, slide=-40), state='h6',
     fg=('pick_baskets', 'left'), note='low inside the wall base, slides left along the wall (x 50 -> 25): the holes open one after another (set_holes 0 -> 12, hole order from x 41 down); townsfolk dig between the holes',
     marks=lambda c: dict(townsfolk=[(HOLES[i] + 2.75, 7.4, 0.0, 180.0) for i in (11, 10, 9, 8, 7, 6)], child=[(HOLES[8] + 2.75, 9.2, 0.0, 180.0)]))
shot(17, 1309, 1388, 'jimo_in', 'NIGHT', C((-9, 16.5, 2.6), (-27, 5.5, 2.4), 22), dict(push=0.08, slide=0), state='h12',
     fg=('reeds', 'left'), note='eye medium, push 8 %/s; reed bundles soaked from a jar are tied to the tails; oxen lined up nose-first at the holes (marks face the wall)',
     marks=lambda c: dict(ox=[(HOLES[i], 8.4, 0.0, -90.0, 1.0) for i in (0, 1, 2, 3, 4, 5)], townsfolk=[(HOLES[i] + 1.8, 11.5, 0.0, 200.0) for i in (1, 3, 4)], tiandan=[(HOLES[2] - 2.2, 12.0, 0.0, 160.0)]))
shot(18, 1388, 1427, 'jimo_in', 'NIGHT', C((-1, 15.5, 2.4), (-22, 5.5, 4.0), 22), dict(push=0.10, slide=0, moves=[dict(t=0.5, d=0.8, dur=6)]), state='h12',
     fg=None, note='eye, quick push-in: Tian Dan raises a torch, tails light in a ripple (flame_card on each ox card)',
     marks=lambda c: dict(tiandan=[(-6.8, 12.6, 0.0, 120.0)], ox=[(HOLES[i], 8.4, 0.0, -90.0, 1.0) for i in (0, 1, 2, 3, 4, 5)]))
HOLES = [-41.0 + 5.5 * k for k in range(6)] + [13.5 + 5.5 * k for k in range(6)]

# ============================================================== JIMO_OUT
shot(12, 944, 1003, 'jimo_out', 'DUSK', C((-14, -42, 1.7), (2, -12, 4.6), 24), dict(push=0.0, slide=40), state='g0.15',
     fg=('wheel', 'left'), note='eye low, slides right; the gate opens a crack (set_gate 0.15); the envoy bows on the bridge; old folk and women stand on the wall walk (z 16, no soldiers)',
     marks=lambda c: dict(envoy=[(0.2, -29.0, 0.0, 180.0)], townsfolk=[(x, -2.2, 16.0, 180.0) for x in CRENEL_GAPS(-14, -10, -6.5, 6.5, 10, 14)], child=[(CRENEL_GAPS(-16.5)[0], -2.2, 16.0, 180.0)]))
shot(19, 1427, 1515, 'jimo_out', 'NIGHT', C((6, -32, 1.5), (30, -5, 3.4), 18), dict(push=0.0, slide=0, moves=[dict(t=0.9, pan=-85, dur=6)]), state='h12,g0.3',
     fg=None, note='low wide at the wall base, WHIP pan at the end to follow the herd; oxen burst out of the 12 holes (x 13.5..41 at y -5), cross the dry ditch / bridge and the field toward the camp',
     marks=lambda c: dict(ox=[(HOLES[i], -7.2, 0.0, -100.0, 1.0) for i in range(6, 12)], herd=herd(40, (27, -10), (34, -58), 16.0, 19, yaw=-98.0), qi_soldier=herd(30, (27, 6), (27, -6), 30.0, 20)))
shot(20, 1515, 1596, 'jimo_out', 'NIGHT', C((22, -56, 1.7), (-2, -92, 3.0), 20), dict(push=0.07, slide=0), state='h12',
     fg=None, note='low, tracking beside the herd, push 7 %/s; the herd charges toward the Yan camp (far camp at y -150..-215); oxen never turn back',
     marks=lambda c: dict(herd=herd(36, (15, -62), (-3, -108), 14.0, 21, yaw=-108.0)))
shot(23, 1742, 1807, 'jimo_out', 'NIGHT', C((-31, 0.6, 21.5), (-2, 0.6, 16.5), 22), dict(push=-0.07, slide=0), state='h12',
     fg=('torch', 'right'), note='high over the wall top, pull-out; fg torch; old men, women and kids beat bronze pots on the walk (walk centre y 0.4, z 16)',
     marks=lambda c: dict(townsfolk=[(x, 0.4 + 1.3 * (-1) ** k, 16.0, 180.0) for k, x in enumerate((-21.5, -17, -12.5, -8, -3.5, 1))], child=[(-19.2, 0.3, 16.0, 180.0), (-10.2, 0.3, 16.0, 180.0)]))
shot(26, 1958, 2112, 'jimo_out', 'DAWN', C((2.5, -84, 1.5), (0.5, -70, 2.6), 24), dict(push=-0.06, slide=0, moves=[dict(t=0.72, d=0.82, dur=10)]), sun=262.0,
     fg=None, note='low, long tracking pull in front of the running general (he runs -y toward home along the road toward the camera), push-in at the end; dragon oxen trot after him with smoking tails',
     marks=lambda c: dict(general=[(0.8, -77.0, 0.0, 0.0)], ox=[(-1.8, -71.0, 0.0, -90.0, 1.0), (3.2, -69.0, 0.0, -90.0, 1.0), (-0.6, -66.5, 0.0, -90.0, 1.0), (4.0, -63.5, 0.0, -90.0, 1.0)], road=[(0.0, -30.0, 0.0, 0.0), (0.0, -150.0, 0.0, 0.0)]))
# ============================================================== YAN_CAMP
shot(8, 597, 674, 'yan_camp', 'DUSK', C((1.5, -59, 2.4), (-4, -47.5, 4.8), 22), dict(push=0.08, slide=0),
     fg=('spear_rack', 'left'), note='eye, push 8 %/s, the general on the rampart (marks.rampart, z 2.6) looks at Jimo, bursts out laughing; fg spear rack',
     marks=lambda c: dict(general=[(-4.0, -47.5, 2.6, face((-4.0, -47.5), c))], soldier=[(3.6, -48.5, 2.6, face((3.6, -48.5), c)), (-9.0, -48.5, 2.6, face((-9.0, -48.5), c))]))
shot(9, 674, 737, 'yan_camp', 'DUSK', C((-7, -99, 2.8), (-3.5, -90.5, 4.2), 24), dict(push=0.09, slide=0),
     fg=None, note='QUOTE 1a medium (camera on the far side of the general, looking +y toward the camp and Jimo; the table is the fg), push 9 %/s; the general arms wide, soldiers behind him laugh',
     marks=lambda c: dict(general=[(-3.5, -90.5, 0.0, face((-3.5, -90.5), c))], soldier=[(-8.2, -85.0, 0.0, 0.0), (0.8, -84.2, 0.0, 0.0), (-3.8, -81.5, 0.0, 0.0)]))
shot(10, 737, 853, 'yan_camp', 'DUSK', C((-1.5, -96.5, 3.1), (-3.5, -90.5, 3.0), 26), dict(push=0.10, slide=-25),
     fg=None, note='QUOTE 1b medium-close (reverse angle, the camp behind him), push 10 %/s then a slight slide; thumb at his chest, chin up',
     marks=lambda c: dict(general=[(-3.5, -90.5, 0.0, face((-3.5, -90.5), c))], soldier=[(-8.0, -85.0, 0.0, 0.0), (0.8, -84.0, 0.0, 0.0)]))
shot(11, 853, 944, 'yan_camp', 'DUSK', C((-1, -73, 2.6), (5.5, -86, 2.2), 22), dict(push=-0.07, slide=0, moves=[dict(t=0.55, d=0.78, dur=8)]), sun=100.0,
     fg=('jar', 'left'), note='wide eye, pull-out 7 %/s with a push-in on "ไอ้เสมียนวัว" (30.64 s); soldiers round the fire at (5.5, -85) mock-moo, finger horns',
     marks=lambda c: dict(soldier=[(2.5, -81.5, 0.0, 0.0), (8.5, -82.0, 0.0, 0.0), (9.8, -86.5, 0.0, 0.0), (2.0, -87.5, 0.0, 0.0), (5.5, -89.5, 0.0, 0.0), (-1.0, -84.0, 0.0, 0.0)], general=[(-2.5, -92.0, 0.0, 0.0)]))
shot(13, 1003, 1071, 'yan_camp', 'NIGHT', C((0, -54, 12.0), (2, -86, 2.0), 20), dict(push=-0.06, slide=0), state='pt1',
     fg=None, note='wide high, pull-out 6 %/s; the camp party (set_party 1): cheering-crowd marks round the fires, cups, a sentry drops his spear and joins in',
     marks=lambda c: dict(party_crowd=PARTY, sentry=[(-14.0, -76.0, 0.0, 180.0)]))
shot(14, 1071, 1136, 'yan_camp', 'NIGHT', C((-9, -106, 2.8), (-4.3, -96.2, 4.4), 24), dict(push=0.09, slide=0), state='pt1',
     fg=('jar', 'right'), note='QUOTE 2a medium (reverse angle: the party fires, tents and crowd behind him), push 9 %/s; the general raises his cup and laughs, bounce; fg wine jar',
     marks=lambda c: dict(general=[(-4.3, -96.2, 0.0, face((-4.3, -96.2), c))], soldier=[(-9.2, -90.8, 0.0, 0.0), (1.2, -90.0, 0.0, 0.0)],
                          party_crowd=[(6.5, -85.0, 0.0, 0.0), (9.5, -80.5, 0.0, 0.0), (2.0, -78.0, 0.0, 0.0), (-3.0, -74.5, 0.0, 0.0), (-9.0, -72.0, 0.0, 0.0), (8.0, -74.0, 0.0, 0.0)]))
shot(15, 1136, 1205, 'yan_camp', 'NIGHT', C((-1.5, -103, 3.1), (-4.3, -96.2, 3.0), 26), dict(push=0.10, slide=0), state='pt1',
     fg=None, note='QUOTE 2b medium-close (reverse angle), push 10 %/s; he mimes carving, licks his lips, the cup tilts',
     marks=lambda c: dict(general=[(-4.3, -96.2, 0.0, face((-4.3, -96.2), c))], soldier=[(-9.0, -91.0, 0.0, 0.0)], party_crowd=[(6.0, -86.0, 0.0, 0.0), (9.5, -81.0, 0.0, 0.0), (2.0, -79.0, 0.0, 0.0)]))
shot(21, 1596, 1683, 'yan_camp', 'NIGHT', C((0, -58, 2.2), (0, -8, 4.0), 22), dict(push=0.03, slide=0, moves=[dict(t=0.45, d=0.67, dur=6)]),
     fg=None, note='eye from the Yan side at the palisade gap (x +-6): a wall of glowing red dragon monsters comes out of the dark field (y -38 .. -6); SNAP push x1.5; soldiers\' jaws drop, cups fall',
     marks=lambda c: dict(soldier=[(-3.0, -51.5, 0.0, 0.0), (3.5, -49.5, 0.0, 0.0), (0.2, -47.0, 0.0, 0.0)], herd=herd(60, (0, -8), (0, -37), 10.0, 21, yaw=-90.0)))
shot(22, 1683, 1742, 'yan_camp', 'NIGHT', C((-2, -52, 1.6), (0.5, -45, 2.0), 26), dict(push=0.09, slide=0),
     fg=None, note='close-medium on ONE ox in full flare (blades, silk, flame tail) with a frozen terrified soldier',
     marks=lambda c: dict(ox=[(0.4, -46.5, 0.0, -60.0, 1.0)], soldier=[(-1.4, -47.0, 0.0, 0.0)]))
shot(24, 1807, 1882, 'yan_camp', 'NIGHT', C((-34, -44, 15.0), (-4, -82, 2.0), 20), dict(push=0.05, slide=50), state='ro0.5',
     fg=None, note='wide high, slide 50 px/s + push; rout (set_rout 0 -> 1): tents fold, soldiers flee, pots and helmets fly, a chariot rolls away empty; nobody hurt',
     marks=lambda c: dict(soldier=[ahead(c, d, l) + (200.0,) for (d, l) in ((27, -9), (31, 4), (34, -5), (38, 10), (42, -12), (46, 2), (33, -14), (50, 9))]))
PARTY = [(-6.0, -92.0, 0.0, 200.0), (-2.0, -93.0, 0.0, 210.0), (1.5, -90.0, 0.0, 190.0), (8.5, -80.0, 0.0, 180.0), (3.0, -80.0, 0.0, 190.0), (-4.0, -76.0, 0.0, 200.0), (-8.0, -77.0, 0.0, 190.0),
         (7.0, -74.0, 0.0, 180.0), (11.0, -79.0, 0.0, 200.0), (2.0, -98.5, 0.0, 190.0), (-3.0, -104.0, 0.0, 200.0), (6.0, -91.0, 0.0, 180.0), (9.5, -88.0, 0.0, 170.0), (-10.0, -86.0, 0.0, 210.0)]

# ============================================================== VISTA
shot(3, 156, 297, 'vista', 'DUSK', C((70, -215, 105), (0, 70, -10), 20), dict(push=0.06, slide=-40), state='pn0.5',
     fg=None, note='establishing high, push 6 %/s, slide left; the black Yan pennants pop over the towns one by one (set_pennants 0 -> 1 on 7.32-9.89 s)', marks=lambda c: dict())
shot(4, 297, 384, 'vista', 'DUSK', C((52, -150, 80), (28, -30, 6), 22), dict(push=0.07, slide=0), state='pn1',
     fg=None, note='high, push-in toward the near lit town Jimo (marks.jimo) on "จี๋โม่" (11.91 s); two towns stay lit (Jimo near, Ju far)', marks=lambda c: dict())
shot(25, 1882, 1958, 'vista', 'DAWN', C((-50, -215, 105), (0, 80, -10), 20), dict(push=0.06, slide=0), state='pn1,qr0.5',
     fg=None, note='establishing high, push 6 %/s; the Qi banners return over the towns one by one (set_qi_return 0 -> 1), warm dawn', marks=lambda c: dict())

SHOTS_SORTED = OrderedDict(sorted(SHOTS.items(), key=lambda kv: kv[1]['n']))
SHOTS.clear(); SHOTS.update(SHOTS_SORTED)

# ============================================================== camera motion
def hfov_half(lens): return math.atan(10.125 / lens)

def _norm(a): n = math.sqrt(sum(x * x for x in a)); return tuple(x / n for x in a)
def _add(a, b): return tuple(x + y for x, y in zip(a, b))
def _mul(a, k): return tuple(x * k for x in a)
def _sub(a, b): return tuple(x - y for x, y in zip(a, b))
def _smooth(t): t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)

def pose_at(shot_or_name, t):
    """Camera pose {loc, look_at, lens} at t = 0..1 of the shot (eased push/pull + slide, then the snaps / whips of `move['moves']`)."""
    sh = SHOTS[shot_or_name] if isinstance(shot_or_name, str) else shot_or_name; c = sh['cam']; mv = sh['move']; dur = sh['dur']
    loc, look = c['loc'], c['look_at']; d = _sub(look, loc); d0 = math.sqrt(sum(x * x for x in d)); u = _norm(d); e = _smooth(t)
    push = mv.get('push', 0.0); delta = max(-0.9 * d0, min(0.6 * d0, push * dur * d0)) * e
    hx, hy = _norm((d[0], d[1], 0.0))[:2]; right = (hy, -hx, 0.0)
    shift = mv.get('slide', 0.0) * dur / 720.0 * 2 * d0 * math.tan(hfov_half(c['lens'])) * e
    loc2 = _add(_add(loc, _mul(u, delta)), _mul(right, shift)); look2 = _add(look, _mul(right, shift))
    for m in mv.get('moves', ()):                                          # snaps / whips
        k = _smooth((t - m['t']) / max(1e-6, m['dur'] / max(1, sh['frames'])))
        if k <= 0: continue
        if 'd' in m:                                                        # new distance factor (d < 1 push in, > 1 pull out)
            dd = _sub(look2, loc2); L = math.sqrt(sum(x * x for x in dd)); loc2 = _sub(look2, _mul(_norm(dd), L * (1 + (m['d'] - 1) * k)))
        if 'pan' in m:
            dd = _sub(look2, loc2); a = math.radians(m['pan']) * k; ca, sa = math.cos(a), math.sin(a)
            look2 = _add(loc2, (dd[0] * ca - dd[1] * sa, dd[0] * sa + dd[1] * ca, dd[2]))
    return dict(loc=tuple(round(x, 3) for x in loc2), look_at=tuple(round(x, 3) for x in look2), lens=c['lens'])

def cams_for(location, light=None):
    out = {'wide': dict(DEFAULT[location])}
    for k, sh in SHOTS.items():
        if sh['loc'] == location:
            out[k] = dict(sh['cam'], start=pose_at(sh, 0.0), mid=pose_at(sh, 0.5), end=pose_at(sh, 1.0), light=sh['light'], frames=sh['frames'], f0=sh['f0'], f1=sh['f1'], note=sh['note'], fg=sh['fg'])
    return out

def preset_cam(preset, location, light):
    if preset in SHOTS: return dict(pose_at(SHOTS[preset], 0.0))
    return dict(DEFAULT[location])

# ============================================================== herd layouts (ox cards): N marks along a lane / field
def herd(n, a, b, width=6.0, seed=1, jitter=0.35, yaw=None):
    """N stand marks for ox cards along the lane / field from point a to point b (x, y) with a lateral spread `width` (D): rows staggered, jittered, the card yaw following the direction a->b
    (the cards face +x at yaw 0 for a side view; `yaw` in degrees about z = direction of travel; pass yaw= to override). Returns [(x, y, z, yaw_deg, scale)] sorted far to near.
    Spacing keeps oxen about 3.6 D apart along the lane and 3 D across; for n beyond what fits, the rows deepen (the spread grows), never overlap more than 25 %."""
    import random
    r = random.Random(seed); ax, ay = a; bx, by = b; L = math.hypot(bx - ax, by - ay) or 1.0; ux, uy = (bx - ax) / L, (by - ay) / L; px, py = -uy, ux
    ang = math.degrees(math.atan2(uy, ux)) if yaw is None else yaw
    rows = max(1, int(width / 3.0)); cols = int(math.ceil(n / rows)); step = L / max(1, cols - 1) if cols > 1 else 0.0; out = []; k = 0
    for ci in range(cols):
        for ri in range(rows):
            if k >= n: break
            along = ci * step + r.uniform(-jitter, jitter) * step * 0.5 + (0.5 * step if ri % 2 else 0.0) * 0.5
            lat = (ri - (rows - 1) / 2) * (width / max(1, rows)) + r.uniform(-jitter, jitter) * 1.0
            x = ax + ux * along + px * lat; y = ay + uy * along + py * lat
            out.append((round(x, 2), round(y, 2), 0.0, round(ang + r.uniform(-6, 6), 1), round(r.uniform(0.93, 1.07), 2))); k += 1
    out.sort(key=lambda m: -m[1]); return out

def marks_for(name):
    sh = SHOTS[name]; return sh['marks'](sh['cam'])
