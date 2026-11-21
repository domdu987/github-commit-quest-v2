#!/usr/bin/env python3
"""ghost_shot_table.py : the SHOTS rows (see ghost_shots.py for the move model).  Local coordinates of each location."""
from ghost_shots import shot, C, M_

# ============================================================================= FIELDS (dawn)
# S01 BIGZOOM 1: extreme wide bird's-eye (column < 5 % of the frame height) -> descend + push along the lane past the poplars -> medium on the
# lead tank (col0 at (-18, -20), heading SSW, towed by a jeep), a soldier on its rear deck waves the column on.
shot(1, 0.00, 4.00, 'FIELDS', 'DAWN', C((-3, -118, 1693), (-3, 30, 0), 24),
     dict(path=[(0.0, C((-3, -118, 1693), (-3, 30, 0), 24)),
                (0.42, C((-110, -200, 230), (-10, 0, 0), 24)),
                (0.78, C((-62, -76, 24), (-17, -17, 1.5), 24)),
                (1.0, C((-32.5, -31.0, 5.6), (-19.0, -20.5, 3.2), 24))]),
     note='BIGZOOM 1: extreme wide high over the patchwork, descend + push along the lane past two poplars, end medium on the lead tank',
     marks=dict(rider=[M_(-2.9, 0.4, pose='wave', z=3.3, parent='col0')],
                walkers=[M_(-23.6, -17.0, pose='wave'), M_(-19.0, -4.0, pose='stand')]),
     state='column=0')

# ============================================================================= LANE (morning / day); ghost_lane.py has the layout
import math
def _fr(o, yaw, x, y):
    a = math.radians(yaw); return (round(o[0] + x * math.cos(a) - y * math.sin(a), 2), round(o[1] + x * math.sin(a) + y * math.cos(a), 2))
HERO = (-1.128, 16.949); HY = -36.0
LIFT = (-5.0, -30.0); LY = 92.0
LIFTERS = [_fr(LIFT, LY, x, y) for (x, y) in ((2.7, 1.95), (-2.6, 1.95), (2.7, -1.95), (-2.6, -1.95))]
PUMPMAN = (-9.0, 20.0)
CREW = dict(pumpman=[M_(*PUMPMAN, ph='pumpman', pose='pump')], clipboard=[M_(0.2, 8.4, ph='clipboard')], soundman=[M_(4.6, 13.0, ph='soundman', pose='carry')],
            painter=[M_(9.4, 21.4, ph='painter', pose='polish')])

# S02 low hero along the decoy row (field0..3, x -26, barrels up 30 deg), side-track right; one polishes field0's barrel, one salutes
shot(2, 4.00, 8.40, 'LANE', 'MORNING', C((-20.2, -47.5, 1.2), (-25.5, -19.0, 4.0), 22), dict(push=0.06, slide=40, sdist=14.0),
     note='LOW hero angle along the row of tanks, barrels up; side-tracking slide', fg=('crate', ('cam', 1.9, -0.9), 30, 0.8, 'crate_b'),
     marks=dict(polisher=[M_(-18.6, -30.4, pose='polish')], saluter=[M_(-19.4, -21.0, pose='salute')], soldier=[M_(-20.0, -4.0), M_(-34.0, -18.0, pose='carry')]))
# S03 medium on the hero tank, quick push-in on the pin: the pricker stands under the barrel tip, it drapes onto his helmet (set_deflate 0 -> 1)
shot(3, 8.40, 11.90, 'LANE', 'MORNING', C((8.8, 1.2, 2.7), (3.0, 12.8, 2.3), 26), dict(push=0.10, slide=-30),
     note='medium, quick push-in on the pin; the tank deflates, the barrel droops onto his helmet', fg=('jerrycan', ('cam', 1.6, 0.75), 60, 1.0),
     marks=dict(pricker=[M_(4.4, 11.2, pose='point')], pumpman=CREW['pumpman'], clipboard=[M_(-3.4, 10.2, ph='clipboard')]), state='deflate=0.5')
# S04 high crane down over the work area
shot(4, 11.90, 16.20, 'LANE', 'MORNING', C((3.0, -12.0, 23.0), (3.0, 17.0, 0.0), 22), dict(end=C((3.5, -2.0, 12.5), (3.0, 18.0, 0.5), 22)),
     note='high crane down over the work area: painter, sound man, designer, pump man', fg=None, marks=CREW, state='jeep=0')
# S05 pull back and up from the sign to the decoy field filling with tanks (a dozen men among them)
_F = [(-26.0 - 16.0 * r, -32.0 + 18.5 * i + (r % 2) * 6.0) for r in range(3) for i in range(4)]
shot(5, 16.20, 20.55, 'LANE', 'MORNING', C((-10.5, 20.0, 4.0), (-15.0, 27.2, 4.4), 24), dict(end=C((2.0, -4.0, 15.0), (-34.0, 6.0, 0.0), 22)),
     note='pull back and up past the 23rd HQ SPECIAL TROOPS sign: a dozen men vs a field filling with rubber tanks', fg=None,
     marks=dict(crew=[M_(x + 3.6, y - 3.2, pose=('pump' if i % 3 == 0 else 'carry' if i % 3 == 1 else 'stand')) for i, (x, y) in enumerate(_F)]))
# S06 OTS from behind the crew toward the jeep pulling up; the Major laughs in the passenger seat
shot(6, 20.60, 23.20, 'LANE', 'MORNING', C((1.6, 16.4, 4.6), (6.4, 1.0, 0.6), 24), dict(zoom_rate=0.07, slide=-25, sdist=12.0),
     note='medium-wide OTS from behind the crew toward the jeep (set_jeep 0.55 -> 1)',
     marks=dict(crew=[M_(5.1, 10.2, ph='clipboard'), M_(2.4, 7.8, ph='soldier')], major=[M_(-0.3, -0.75, ph='major', pose='sit', z=2.1, parent='jeep')],
                driver=[M_(-0.3, 0.75, ph='driver', pose='sit', z=2.1, parent='jeep')]), state='jeep=0.8,deflate=1')
# S07 low angle on the Major (out of the jeep) pointing at the flat tank, slow push, crew small behind
shot(7, 23.20, 27.40, 'LANE', 'MORNING', C((2.2, -3.8, 1.05), (4.8, 8.6, 3.7), 24), dict(push=0.07, slide=-30),
     note='LOW angle on the Major, slow push, crew small behind; he points at the deflated tank and talks', fg=('toolbox', ('cam', 1.5, -0.7), 30, 1.3),
     marks=dict(major=[M_(5.6, 6.0, ph='major', pose='point')], crew=[M_(-2.6, 11.0), M_(1.6, 12.2, ph='clipboard'), M_(-6.0, 13.4, ph='pumpman')],
                driver=[M_(-0.3, 0.75, ph='driver', pose='sit', z=2.1, parent='jeep')]), state='jeep=1,deflate=1')
# S08 wide high pull back: the driver chalks BALLOON ARMY on a crate (set_chalk 0 -> 1); the crew droops
shot(8, 27.40, 30.20, 'LANE', 'MORNING', C((11.8, -8.6, 8.0), (6.6, 5.4, 1.6), 22), dict(push=-0.08, slide=30, rise=0.8, sdist=12.0),
     note='wide high, pull back; the driver chalks BALLOON ARMY on a crate; crew droop', fg=('post', ('cam', 2.0, 1.1), 0, 1.4),
     marks=dict(driver=[M_(12.6, 0.6, ph='driver', pose='point')], major=[M_(6.4, 5.4, ph='major', pose='stand')],
                crew=[M_(-0.6, 9.6), M_(2.2, 10.8, ph='clipboard'), M_(-3.2, 12.0, ph='pumpman')]), state='jeep=1,deflate=1,chalk=0.6')

# S11 side tracking with the two cyclists along the low hedge (foreground), baguette in the basket
shot(11, 39.70, 42.80, 'LANE', 'DAY', C((7.4, -88.0, 3.0), (-6.4, -81.0, 2.5), 24), dict(end=C((7.6, -75.6, 3.0), (-6.2, -68.6, 2.5), 24)),
     note='side tracking with the two cyclists along the hedgerow (foreground hedge); they ride 4 D/s', fg=None,
     marks=dict(cyclist_a=[M_(-7.6, -83.0, ph='cyclist_a', pose='ride', yaw=None)], cyclist_b=[M_(-6.0, -86.0, ph='cyclist_b', pose='ride')]))
# S12 BIGZOOM 2: close on the cyclists' faces -> pull back and up: four soldiers hold the tank over their heads
shot(12, 42.80, 45.60, 'LANE', 'DAY', C((-4.0, -40.2, 3.5), (-6.0, -45.6, 3.2), 24),
     dict(path=[(0.0, C((-4.0, -40.2, 3.5), (-6.0, -45.6, 3.2), 24)), (0.5, C((0.5, -46.0, 5.0), (-6.0, -40.5, 3.4), 23)),
                (1.0, C((5.5, -59.0, 7.4), (-6.0, -37.0, 3.8), 22))]),
     note='BIGZOOM 2 / reveal: from close on the cyclists pull back and up wide: 4 soldiers lift the tank over their heads (set_lift 1); cyclists brake',
     marks=dict(cyclist_a=[M_(-7.0, -45.2, ph='cyclist_a', pose='brake')], cyclist_b=[M_(-4.6, -47.6, ph='cyclist_b', pose='brake')],
                lifters=[M_(x, y, pose='lift') for (x, y) in LIFTERS]), state='lift=1')
# S13 medium two-shot in depth, quick push on the front lifter's dry smile
shot(13, 45.60, 50.10, 'LANE', 'DAY', C((-11.8, -55.0, 3.4), (-5.6, -33.5, 4.4), 26), dict(zoom_rate=0.08, slide=20, sdist=12.0),
     note='medium two-shot in depth; quick push on the soldier with the tank overhead; one cyclist falls off gently', fg=('hay', ('cam', 2.2, -1.3), 40, 0.7),
     marks=dict(cyclist_a=[M_(-12.5, -46.3, ph='cyclist_a', pose='stand')], cyclist_b=[M_(-11.4, -47.8, ph='cyclist_b', pose='stand')],
                lifters=[M_(x, y, pose='lift') for (x, y) in LIFTERS]), state='lift=1')

# S19 ending: wide -> medium push, ends on the Major on his crate blowing balloons; the pile; crew grin; the last balloon loops away
shot(19, 66.00, 70.30, 'LANE', 'DAY', C((13.6, -7.0, 5.6), (12.4, 9.8, 2.4), 22), dict(push=0.10, slide=-25),
     note='wide -> medium push, ends on the Major; huge balloon pile (set_pile); last balloon escapes (set_loose_balloon)', fg=('crate', ('cam', 1.8, 1.0), 20, 0.8, 'crate_a'),
     marks=dict(major=[M_(11.0, 8.6, ph='major', pose='blow')], crew=[M_(6.2, 11.8, pose='wave'), M_(8.0, 15.6), M_(17.8, 6.2, ph='clipboard')]), state='pile=0.85,jeep=0')

def _sm(a, b, x): x = max(0.0, min(1.0, (x - a) / (b - a))); return x * x * (3 - 2 * x)
def _a03(GH, t): GH.set_deflate(_sm(0.25, 0.85, t))
def _a05(GH, t):
    for i in range(12): GH.set_inflate('field%d' % i, 0.15 + 0.85 * _sm(0.05 * i, 0.45 + 0.05 * i, t))
def _a06(GH, t): GH.set_jeep(0.55 + 0.45 * _sm(0.0, 0.8, t))
def _a08(GH, t): GH.set_chalk(_sm(0.1, 0.9, t))
def _a12(GH, t): GH.set_lift(_sm(0.1, 0.6, t))
def _a19(GH, t): GH.set_pile(0.7 + 0.3 * _sm(0.0, 1.0, t)); GH.set_loose_balloon(_sm(0.85, 1.25, t))
def _a11(GH, t):
    for ob in GH.STATE['cards']:
        if ob['role'].startswith('cyclist'):
            if 'y0' not in ob.keys(): ob['y0'] = ob.location.y
            ob.location.y = ob['y0'] + 4.0 * t * 3.1
def _a01(GH, t): GH.set_column(1.0 * 4.0 * t)
ACTION = dict(S01=_a01, S11=_a11, S03=_a03, S05=_a05, S06=_a06, S08=_a08, S12=_a12, S19=_a19)

# ============================================================================= CAMP (night); ghost_camp.py has the layout
# S09 crane from the tank rows down to the sound truck, push toward the horn; the sound man at the desk, the record spins
shot(9, 30.20, 35.00, 'CAMP', 'NIGHT', C((-24.0, -2.0, 15.0), (-6.0, 22.0, 2.0), 22), dict(path=[(0.0, C((-24.0, -2.0, 15.0), (-6.0, 22.0, 2.0), 22)), (0.5, C((-14.0, -27.0, 9.0), (-8.0, -4.0, 3.0), 22)), (1.0, C((3.0, -24.0, 4.2), (-7.6, -9.8, 4.8), 22))]),
     note='crane from the tank rows to the sound truck, push toward the horn; sound man flips switches, record spins (spin_record); moon rim on the tanks',
     fg=('lantern', ('camend', 2.0, 1.2), 0, 1.6),
     marks=dict(soundman=[M_(-1.9, -16.6, ph='soundman', pose='point')], guard=[M_(-10.6, -1.6), M_(4.0, 2.0, pose='carry')]))
# S10 side-tracking from the radio tent out to the second truck: the painter stencils a new badge on its bumper by a lantern
shot(10, 35.00, 39.70, 'CAMP', 'NIGHT', C((0.2, -18.2, 3.0), (1.6, -4.6, 2.4), 24), dict(end=C((7.6, -19.6, 3.0), (10.2, -8.0, 2.2), 24)),
     note='side tracking through the radio tent and out to a truck; radio man chatters into the handset; painter stencils a division badge on a bumper',
     fg=('crate', ('cam', 1.9, -1.0), 10, 0.8, 'crate_c'),
     marks=dict(radioman=[M_(1.2, -4.6, ph='radioman', pose='sit')], painter=[M_(8.4, -9.8, ph='painter', pose='polish')], soldier=[M_(4.8, -9.0, pose='carry')]))
def _a09(GH, t): GH.set_record(936.0 * t * 4.8 * 1.25 / 1.25)
ACTION['S09'] = _a09

# ============================================================================= RHINE (night, March 1945); ghost_rhine.py has the layout
# S14 extreme wide high over the river, slow descend; the 'RHINE' sign on the bank; soldiers unload crates of folded rubber from two trucks
shot(14, 50.20, 54.20, 'RHINE', 'NIGHT_R', C((-128.0, -268.0, 74.0), (-30.0, -96.0, -2.0), 22), dict(end=C((-94.0, -226.0, 26.0), (-38.0, -132.0, 0.0), 22)),
     note='extreme wide high over the river, slow descend; caption-safe RHINE sign on the bank; soldiers unload crates from trucks',
     marks=dict(unloaders=[M_(-73.6, -181.4, pose='carry'), M_(-75.8, -183.2, pose='carry'), M_(-88.0, -177.2, pose='carry'), M_(-86.2, -179.6)]))
# S15 crane up over the rows inflating in lantern light; pump crews
shot(15, 54.30, 57.60, 'RHINE', 'NIGHT_R', C((-52.0, -162.0, 2.6), (-84.0, -112.0, 2.8), 22), dict(end=C((-40.0, -152.0, 18.0), (-92.0, -96.0, 0.0), 22)),
     note='crane up over rows inflating in lantern light (set_inflate decoyN staggered); pump crews',
     fg=('reeds', ('cam', 1.7, 0.9), 0, 0.9),
     marks=dict(pumpcrew=[M_(-62.0 + 1.5, -131.0 + 6.0, ph='pumpman', pose='pump'), M_(-72.0 + 1.5, -125.0 + 6.0, ph='pumpman', pose='pump'), M_(-88.0 + 1.5, -131.0 + 6.0, ph='pumpman', pose='pump'),
                          M_(-98.0 + 1.5, -106.0 + 6.0), M_(-114.0 + 1.5, -112.0 + 6.0, pose='carry')]))
# S16 push along the sound truck and the radio tent; crates stencilled 30th INF DIV / 79th INF DIV
shot(16, 57.60, 60.90, 'RHINE', 'NIGHT_R', C((-45.5, -104.0, 4.5), (-60.0, -58.0, 2.5), 22), dict(push=0.07, slide=30, sdist=20.0),
     note='push along the sound truck and the radio tent; 30th / 79th INF DIV crates; sound truck booming (spin_record), radio chatter',
     fg=('lantern', ('cam', 1.9, -1.2), 0, 0.8),
     marks=dict(soundman=[M_(-55.0, -80.6, ph='soundman', pose='point')], radioman=[M_(-51.6, -36.6, ph='radioman', pose='sit')], soldier=[M_(-53.0, -55.0, pose='carry')]))
# S17 OTS from behind the German observers across the river to the glowing balloon field
shot(17, 60.90, 63.50, 'RHINE', 'NIGHT_R', C((69.0, -53.6, 3.8), (-90.0, -104.0, 0.5), 24), dict(zoom_rate=0.08, slide=-25, sdist=10.0),
     note='OTS from behind the German observers (binoculars, a telescope) across the river to the glowing decoy field; one drops his sausage', fg=('sandbags', ('cam', 1.8, -0.9), 90, 0.9, 3),
     marks=dict(observers=[M_(58.4, -59.0, ph='german', pose='look'), M_(59.6, -61.6, ph='german', pose='point'), M_(61.2, -58.6, ph='german', pose='stand')]))
# S18 pre-dawn blue: wide slow pan along the boats and the pontoon bridge; soldiers paddle, tiptoe, a dog in a boat
shot(18, 63.50, 66.00, 'RHINE', 'PREDAWN', C((-37.5, 334.0, 3.2), (-2.0, 350.0, -0.2), 22), dict(end=C((-36.5, 337.0, 3.1), (16.0, 360.0, -0.2), 24)),
     note='wide, slow pan along the assault boats / pontoon crossing in blue pre-dawn shadow (set_boats 0.3 -> 0.6)', fg=('reeds', ('cam', 1.8, -1.0), 0, 1.0),
     marks=dict(**{'boat%d' % i: [M_(x, 0.0, pose='paddle', z=-0.76, parent='boat%d' % i) for x in (-1.5, 0.0, 1.3)] for i in range(5)},
                dog=[M_(1.95, 0.0, ph='dog', pose='stand', z=-0.76, parent='boat2')], tiptoe=[M_(-40.0, 382.0, z=0.52, pose='carry'), M_(-33.0, 382.6, z=0.52)]))
def _a15(GH, t):
    for i in range(42): GH.set_inflate('decoy%d' % i, 0.2 + 0.8 * _sm(0.08 * (i % 7) - 0.1 + 0.05 * (i // 7), 0.5 + 0.08 * (i % 7) + 0.05 * (i // 7), t))
def _a18(GH, t): GH.set_boats(0.3 + 0.3 * t / 1.25)
ACTION.update(S15=_a15, S18=_a18)
