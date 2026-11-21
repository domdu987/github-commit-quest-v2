#!/usr/bin/env python3
"""Take s13 = shot 13 (27.957-28.922, film g 839..867, no handle in (punch-in cut), handle 7 out): office, office_day.
The punch-in on the Thai label 'ทางด่วนพายุ' being pinned above the arrow head of the red line. Camera label_insert (props
extension; on the axis of shot 12, raked 12 deg from below-left): a 4-frame punch-in that lands on the setup with white speed
lines over the first 6 frames, held close, a 2-frame shake (0.45 deg) on the slap, then an eased drift push of about 5 %/s.
The chief's hand (a hand card, the take-A method of s11) slaps the label (nickname_label art of the paper registry, hi-res) onto
the map at 28.00, slides up to its top edge and thumbs the red pin home at 28.25; the label rocks 4 deg for 2 frames and its
lower-right corner curls. No faces. The red line is the hand-drawn track as it is now (line 1, smudge halo 3).
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]"""
import os, sys, math
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(DIR), 's10'))
import otake as O                                       # noqa: E402
import numpy as np                                      # noqa: E402
gf, gb, smooth, smoother, lerp = O.gf, O.gb, O.smooth, O.smoother, O.lerp
import acting as AC                                     # noqa: E402,F401
import office3d as S                                    # noqa: E402
import office_props as X                                # noqa: E402

TAKE, SHOTS, VERSION, HI_MAP = 's13', [13], 1, False
G0, G1 = gb(27.957), gb(28.922)                         # 839, 868
H_IN, H_OUT = 0, 7                                      # punch-in cut in; dissolve 11 f out (5.5 + 2 -> 7)
TRANSITION_IN = dict(type='punch_in', frames=0, note='punch-in cut with white speed lines over the first 6 frames')
R0, R1 = G0 - H_IN, G1 + H_OUT                          # 839, 875

SLAP = gf(28.00)                                        # 843
PIN = gf(28.25)                                         # 851
SPEED_LINES = 6

# ----------------------------------------------------------------------------- the label, registered on the hand-drawn track
MAP_Y = S.MAP_Y
LR = dict(x0=-0.45, x1=0.70, z0=3.10, z1=3.44)          # office3d label_rect (A['label_rect']); the props module hangs the label there
LB_PIN = X.LB_PIN
LW, LH = X.LABEL_W, X.LABEL_H
TILT = 4.0


def arrow_head():
    """tip of the red line and its LOCAL heading (unit, map plane x/z), from the set API (track_point of the hand-drawn track)."""
    a, b = np.array(S.track_point(0.97)), np.array(S.track_point(1.0))
    d = b - a
    return b, np.array([d[0], d[2]]) / math.hypot(d[0], d[2])


def label_registration():
    """where the arrow head's own heading, extended past N.Y., meets the label's bottom edge, against the label's bottom centre."""
    tip, h = arrow_head()
    th = math.radians(-TILT)
    piv = np.array([LR['x0'] + LB_PIN[0], LR['z1'] - LB_PIN[1]])
    def wpt(lx, lz):                                     # label-local (x right from the pin, z up) -> map x/z (rotation about y)
        return piv + np.array([lx * math.cos(th) + lz * math.sin(th), -lx * math.sin(th) + lz * math.cos(th)])
    bl, br = wpt(-LB_PIN[0], LB_PIN[1] - LH), wpt(LW - LB_PIN[0], LB_PIN[1] - LH)
    # intersect tip + s h with the bottom edge bl + v (br - bl)
    A = np.array([[h[0], -(br - bl)[0]], [h[1], -(br - bl)[1]]])
    s, v = np.linalg.solve(A, bl - np.array([tip[0], tip[2]]))
    hit = np.array([tip[0], tip[2]]) + s * h
    return dict(tip=(round(float(tip[0]), 4), round(float(tip[2]), 4)), heading_deg_from_up=round(math.degrees(math.atan2(h[0], h[1])), 2),
                gap_D=round(float(s), 3), hit_x=round(float(hit[0]), 4), hit_frac_of_width=round(float(v), 3),
                bottom_centre_x=round(float((bl[0] + br[0]) / 2), 4), offset_D=round(float(hit[0] - (bl[0] + br[0]) / 2), 4))


def label_state(g):
    """(show, dx, away, scale, swing, curl, flutter, pin, pin_out) of frame g."""
    if g <= SLAP:
        a = ((g - R0) / float(SLAP - R0)) ** 2           # accelerating into the slap
        return 1.0, 0.30 * (1 - a), 0.22 * (1 - a), 1.10 - 0.10 * a, -3.0 * (1 - a), 0.0, 0.0, 0.0, 0.0
    sw = {SLAP + 1: 4.0, SLAP + 2: -2.0, SLAP + 3: 0.8}.get(g, 0.0)      # rocks 4 deg for 2 frames, settles
    sc = 1.0 - 0.03 * (g == SLAP + 1)
    curl = 0.55 * smooth(SLAP + 3, SLAP + 10, g)
    fl = 0.25 * math.sin((g - SLAP) * 0.9) * (1 - smooth(SLAP, SLAP + 9, g)) + 0.04 * math.sin(g * 0.37)
    pin = 1.0 if g >= PIN - 4 else 0.0
    pin_out = 0.04 * (1 - smooth(PIN - 2, PIN, g)) if pin else 0.0
    return 1.0, 0.0, 0.0, sc, sw, curl, max(0.0, fl), pin, pin_out


def label_root(g):
    show, dx, away, sc, sw, curl, fl, pin, pin_out = label_state(g)
    return np.array([LR['x0'] + LB_PIN[0] + dx, MAP_Y - 0.004 - away, LR['z1'] - LB_PIN[1]]), math.radians(-(TILT + sw)), sc


def label_world(g, lx, ly, lz):
    """world point of label-local (lx right of the pin, ly toward the room negative, lz up) at frame g (Blender rot about y)."""
    loc, th, sc = label_root(g)
    x, z = lx * sc, lz * sc
    return loc + np.array([x * math.cos(th) + z * math.sin(th), ly * sc, -x * math.sin(th) + z * math.cos(th)])


def props(g, f):
    S.set_track(1.0, 0.0, frame=f)
    X.set_chalk(1.0, frame=f)
    for i in range(1, 7):
        X.set_ghost(i, 1.0, frame=f)
    X.set_tick(1.0, frame=f)
    a, w = X.spinner_angle(g / 30.0)
    X.set_spinner(u=0.0, angle=a, wobble=w, frame=f)
    X.set_smudge(3.0, frame=f)
    X.set_crumbs(1.0, frame=f)
    X.set_ruler(0.0, frame=f)
    show, dx, away, sc, sw, curl, fl, pin, pin_out = label_state(g)
    X.set_label(show=show, tilt_deg=TILT, swing_deg=sw, away=away, scale=sc, curl=curl, flutter=fl, pin=pin, pin_out=pin_out,
                res='hi', frame=f)
    root = X.STATE['objects']['label_root']               # the hand carries the label in from the right: x offset on the same key
    root.location.x = LR['x0'] + LB_PIN[0] + dx
    root.keyframe_insert('location', frame=f)


# ----------------------------------------------------------------------------- camera
LAB_C = np.array([(LR['x0'] + LR['x1']) / 2, MAP_Y, (LR['z0'] + LR['z1']) / 2])


def _aim(target, dist, yaw_deg, pitch_deg, look_shift):
    y, p = math.radians(yaw_deg), math.radians(pitch_deg)
    loc = target + dist * np.array([-math.sin(y) * math.cos(p), -math.cos(y) * math.cos(p), -math.sin(p)])
    return loc, target + np.array(look_shift)


LI = _aim(LAB_C, 1.84, 12.0, 12.0, (0, 0, -0.40))       # label_insert of the props module: (-0.249, -1.811, 2.887) -> (0.125, -0.05, 2.87)


def cam(g):
    loc0, look = LI
    if g <= G0 + 4:                                      # punch-in: lands from 1.30 x the distance in 4 frames (ease out)
        u = 1 - (1 - min(1.0, (g - G0) / 4.0)) ** 3
        k = 1.30 + (1.0 - 1.30) * u
    else:                                                # drift push about 5 %/s, eased in
        s = (g - (G0 + 4)) / 30.0
        k = 1.0 - 0.05 * (s - 0.25 * (1 - math.exp(-s / 0.25)))
    loc = look + (loc0 - look) * k
    fw, r, up = O.cam_basis(loc, look, None)
    roll = {SLAP: 0.45, SLAP + 1: -0.30}.get(g, 0.0)     # the 2-frame shake on the slap
    rr = math.radians(roll)
    upv = up * math.cos(rr) + r * math.sin(rr)
    return tuple(loc), tuple(look), tuple(upv), 22.0


# ----------------------------------------------------------------------------- the chief's hand (hand card, s11 method)
HS = 1.5


def _basis(g):
    c = cam(g)
    fw, r, u = O.cam_basis(c[0], c[1], None)
    fh = np.array([fw[0], fw[1], 0.0]); fh /= np.linalg.norm(fh)
    rh = np.array([r[0], r[1], 0.0]); rh /= np.linalg.norm(rh)
    return np.asarray(c[0]), fh, rh


PALM = (0.36, -0.012, -0.16)                            # label-local: the palm on the right half of the strip
THUMB = (0.0, -0.030, 0.0)                              # label-local: on the pin head (pin_out added)
SLIDE = (SLAP + 2, PIN - 3)                             # 845 - 848 the hand slides up to the pin
AWAY = (PIN + 2, PIN + 8)                               # 853 - 859 the hand leaves to the upper right


def hand_tip(g):
    _, _, _, _, _, _, _, pin, pin_out = label_state(g)
    loc, fh, rh = _basis(g)
    palm = label_world(g, *PALM)
    thumb = label_world(g, THUMB[0], THUMB[1] - pin_out, THUMB[2])
    if g <= SLIDE[0]:
        p = palm
    else:
        p = lerp(palm, thumb, smoother((g - SLIDE[0]) / float(SLIDE[1] - SLIDE[0]))) if g < SLIDE[1] else thumb
        p = np.asarray(p) + np.array([0.0, -0.05, 0.06]) * math.sin(math.pi * min(1.0, max(0.0, (g - SLIDE[0]) / float(SLIDE[1] - SLIDE[0]))))
    away = smooth(AWAY[0], AWAY[1], g)
    return np.asarray(p) + (rh * 0.9 + np.array([0, 0, 0.45])) * away


def hand_place(g):
    loc, fh, rh = _basis(g)
    t = hand_tip(g)
    k = smooth(SLIDE[0], SLIDE[1], g)                    # the shoulder rises with the hand: level for the slap, above for the pin
    L0, D0, L1, D1 = [float(v) for v in os.environ.get('S13_HAND', '1.85 0.05 1.9 0.30').split()]
    lateral, drop = L0 + (L1 - L0) * k, D0 + (D1 - D0) * k
    f = t - fh * 0.05 + rh * lateral
    f = np.array([f[0], f[1], t[2] + drop - 2.44 * HS])
    return tuple(float(x) for x in f), False, HS


def hand_pose(g):
    p = dict(yaw=-0.5, expr='smug', arm_r='hip', arm_l='hip', legs='stand')
    k = smooth(SLIDE[0], SLIDE[1], g)
    shape = 'open' if k < 0.5 else 'point'
    return p, {'l': {'hand': tuple(float(x) for x in hand_tip(g)), 'stretch': float(os.environ.get('S13_STRETCH', '1.30')), 'bend': -0.35, 'shape': shape}}


ACTORS = [
    dict(name='bossH13', cast='boss', canvas=(-1.9375, -3.625, 0.5, -1.25), contact=False, shadow=None,
         place=hand_place, pose=hand_pose, ppd=512, hidden=lambda g: g > AWAY[1]),
]

NOTES = [
    "Camera: label_insert of the props module, (-0.249, -1.811, 2.887) -> (0.125, -0.05, 2.87), 22 mm: 1.84 D from the label, raked 12 deg from below-left (the module's note: at 1.1 D the 1.15 D label would be about 820 px wide; 1.84 D keeps the planned 480 px). Punch-in: the take opens at 1.30 x the distance and lands on the setup in 4 frames (cubic ease-out); 2-frame shake on the slap (roll 0.45 then -0.30 deg, g 843-844); then a drift push easing in to 5 %/s.",
    "Speed lines: 46 white radial wedges (2D, deterministic, centred on the label) over the first 6 frames g 839-844, fading out and retreating outward, drawn by this take's post on top of the streaked frames.",
    "Label: nickname_label of the paper registry at 2400 px (set_label res 'hi'), hung by the props module on label_rect from its pin LB_PIN, tilt 4 deg. It flies in with the hand (0.30 D from the right, 0.22 D off the wall, scale 1.10, accelerating) and slaps flat at g 843 (28.00), rocks +4 / -2 deg for 2 frames, the lower-right corner curls (0 -> 0.55 over g 846-853) and flutters slightly. The red pin appears under the thumb at g 847 and is thumbed home g 849-851 (28.25).",
    "Registration on the hand-drawn track (set API track_point): the arrow head is track_point(1.0) = (0.0623, 2.6197); its local heading (track_point(0.97) -> track_point(1.0)) leans 5.6 deg east of up. Extended past N.Y., that heading meets the label's bottom edge 0.486 D above the tip at x 0.110, 47 % along the label's width; the label's bottom centre is at x 0.145, so the label sits centred over the end of the line within 0.036 D (about 15 px in this framing). The label keeps the shared label_rect position so that shots 17-25 match.",
    "The chief's hand is a hand card (s11's take-A method: the chief's puppet at scale 1.5 facing the lens, 0.05 D in front of the target, body and head outside the frame at the right). Its BARE hand is pinned with a world 'hand' target (palm on the label's right half for the slap, then on the pin head for the thumb). The shared runner reports registration only for prop tips, so this take measures the bare hand the same way (projected hand anchor against the projected world target). The card casts no shadow; the chief's body is not in the scene, so his hat does not shadow the label (the props module measured 17 % at boss_mark).",
    "No faces: the hand card's head lies beyond the right or top edge in every frame (checked on the frames)."]


# the runner reports registration for prop tips only; the chief's bare hand ('hand' target) is measured here the same way
_orig_pose = O.Take.pose


def _pose_with_hand_reg(self, frames, verbose=False):
    _orig_pose(self, frames, verbose)
    A, R = self.actors_mod, self.R
    for g in [x for x in frames if self.r0 <= x < self.r1]:
        f = g + 1
        self.scene.frame_set(f); self.apply(g)
        for a in self.actors:
            if a.card.hide_render:
                continue
            pose, hands = a._spec['pose'](g)
            if not hands:
                continue
            p, info = a.pose(f, pose, hands=hands, camera=self.cam)
            reg = {}
            for side, h in hands.items():
                e = info.get(side)
                if e and 'hand' in h:
                    sc = A.local_to_screen(a, self.cam, e['reached'], f)[:2]
                    w = R.world_to_screen(self.cam, self.Vector(h['hand']), f)[:2]
                    reg[side] = dict(px=round(math.hypot(sc[0] - w[0], sc[1] - w[1]), 3), err_D=round(e['error'], 5),
                                     clearance=round(e.get('clearance', 0.0), 4), screen=[round(sc[0], 1), round(sc[1], 1)])
            self.info.setdefault(g, {})[a.name] = reg


O.Take.pose = _pose_with_hand_reg

CUES = [
    (27.93, 0.2, 'whump', 'punch-in whump (speed lines)'),
    (27.96, 0.64, 'walla', 'laughter tail ducking out'),
    (28.00, 0.15, 'slap', 'paper slap (the label hits the map)'),
    (28.25, 0.15, 'thunk', 'pin thunk (thumbed home)'),
    (28.30, 0.5, 'music', 'muted trumpet wah-wah'),
]


def speed_lines(frames_dir):
    """white radial speed lines over the first SPEED_LINES frames of the take (2D, deterministic), fading out."""
    from PIL import Image, ImageDraw
    rng = np.random.RandomState(13)
    n = 46
    ang = np.sort(rng.uniform(0, 2 * math.pi, n))
    r_in = rng.uniform(0.50, 0.78, n)
    wid = rng.uniform(3.0, 9.0, n)
    cx, cy, R = 360.0, 470.0, 1500.0
    for i in range(SPEED_LINES):
        g = G0 + i
        p = os.path.join(frames_dir, 'g_%04d.png' % g)
        im = Image.open(p).convert('RGB')
        a = (1 - i / float(SPEED_LINES)) ** 1.3
        ov = Image.new('L', im.size, 0); d = ImageDraw.Draw(ov)
        grow = 1.0 + 0.06 * i                                # the inner ends retreat outward as the lines fade
        for t, ri, w in zip(ang, r_in, wid):
            r0 = ri * grow * 700.0
            c, s = math.cos(t), math.sin(t)
            p0 = (cx + c * r0, cy + s * r0); n0 = (-s, c)
            p1 = (cx + c * R, cy + s * R)
            poly = [(p0[0], p0[1]), (p1[0] + n0[0] * w * 2.2, p1[1] + n0[1] * w * 2.2), (p1[0] - n0[0] * w * 2.2, p1[1] - n0[1] * w * 2.2)]
            d.polygon(poly, fill=int(235 * a))
        white = Image.new('RGB', im.size, (255, 252, 246))
        Image.composite(white, im, ov).save(p)
    print('speed lines on g %d..%d' % (G0, G0 + SPEED_LINES - 1))


if __name__ == '__main__':
    argv = sys.argv[1:]
    if argv and argv[0] == 'post':
        O.cmd_post(sys.modules[__name__])
        speed_lines(os.path.join(DIR, 'frames'))
    elif argv and argv[0] == 'reg':
        print(label_registration())
    else:
        O.run(sys.modules[__name__], argv)
