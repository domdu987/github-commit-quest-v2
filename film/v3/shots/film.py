#!/usr/bin/env python3
"""film.py -- the first 5 s of the film staged in the 3D office (bpy 5.3, Cycles CPU): two takes, three shots.

    take "A"  g 0 .. g3-1    ONE continuous camera move: raking low insert on the pencil (shot 1), a fast pull-out that swings
                             round the hero (the framing change centred on g2), low-angle medium, snap on the jab (shot 2),
                             whip-off to the right
    take "B"  g g3 .. N-1    whip-on, high-angle two-shot staged in depth: the chief rubs the track out at the wall, the hero
                             at near_mark goes wide-eyed, snap push onto his face (shot 3)

Every beat frame comes from timing.load() (the Thai timing file).  g = 0-based output frame; Blender frame = g + 1.

    import film
    F = film.Film(take="A", quality="draft")      # builds the set, camera and actors of that take, keys camera + track
    F.pose(frames)                                # poses + sprites for those output frames
    F.render(frames, out_dir, scale=0.5, threads=2, samples=8)
"""
import math, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
PROJ = os.path.dirname(V3)
for p in (HERE, os.path.join(V3, "stage"), os.path.join(V3, "set3d"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import office3d as S                                    # noqa: E402  (v3/set3d)
import actors, camrig, render, sprites                  # noqa: E402  (v3/stage)
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402  (v2/shots/anim.py, read-only)
import timing                                           # noqa: E402

TMP = os.path.join(V3, "tmp", "shots")
T = timing.load()
N = T["N"]; G2 = T["g2"]; G3 = T["g3"]; G_JAB = T["g_jab"]; G_TOUCH = T["g_touch"]; G_LAST = T["g_last"]
G_DONE = min(T["g_done"], G_LAST + 13)   # last rubbing stroke: under the last phrase, as the snap push lands on the hero
                                         # (after the push the chief's body hides the track, so the rubbing must read before)

# ----------------------------------------------------------------------------- beat frames derived from the timing
G_LAND = 7                               # the pencil point touches the storm symbol
SNAP1 = (8, 19)                          # snap push onto the pencil
PULL = (G2 - 6, G2 + 8)                  # the pull-out that turns the insert into the low-angle medium (centre about G2 + 1)
SHADOW_SWAP = PULL[0] + 4                # from this frame on the hero's shadow comes from the light-facing proxy
GATHER = (G_JAB - 5, G_JAB - 3)          # he draws back ...
SNAP2 = (G_JAB - 3, G_JAB + 7)           # ... jabs (lands on G_JAB) and the camera snaps in
TURN = (G_JAB + 2, G_JAB + 9)            # head turns to the viewer
WHIP_OFF = (G3 - 4, G3 - 1)              # whip pan to the right, cut on G3
WHIP_ON = (G3, G3 + 6)                   # shot 3 arrives still panning, brakes
SHOCK = G_LAST - 1                       # closed frame of the hero's blink: determined -> wide-eyed
SNAP3 = (SHOCK, SHOCK + 12)              # snap push onto his face
STROKE = 5                               # one rubbing stroke every 5 frames
TAKES = {"A": (0, G3 - 1), "B": (G3, N - 1)}


def bf(g):
    return int(g) + 1


# ----------------------------------------------------------------------------- story state
def line_at(g):
    """how much of the red track is drawn (0..1)."""
    return keys(g, [(G_LAND, 0.0, "quad_in"), (G_LAND + 6, 0.07, "lin"), (PULL[0] + 3, 0.75, "cubic_out"),
                    (GATHER[0], 0.92, "hold"), (GATHER[1], 0.92, "cubic_in"), (G_JAB, 1.0, "hold")])


def erase_at(g):
    """fraction rubbed out from the New York end: starts when the eraser touches, 0.60 by the last phrase, done at G_DONE."""
    return keys(g, [(G_TOUCH, 0.0, "sine"), (G_LAST, 0.60, "sine"), (G_DONE, 1.0, "hold")])


def track_w(u):
    return Vector(S.track_point(u))


# ----------------------------------------------------------------------------- take A: hero at the map, one camera move
HERO_A = (-0.80, -0.72, 0.0)             # feet.  Left of the track; his card can swing between "through the pencil point"
                                         # (insert, yaw about 34 deg) and camera-facing (medium) without entering the wall
TOUCH_GAP = 0.012                        # D between the pencil point and the map while drawing (insert)
L2 = Vector((-0.30, -0.35, 2.42))        # look-at of the low-angle medium
L3 = Vector((-0.34, -0.35, 2.10))        # look-at after the snap on the jab
INSERT_OX = 0.17                         # world-x offset of the insert's look point from the pencil point on g 0..SNAP1[0]
                                         # (was -0.14: the hero's head cut into the left edge of the frame)
REACH_MAX = 1.30                         # the drawing arm may stretch this far (the puppet's own limit) to keep the point on the line


def reveal_e(g):
    """0 in the insert, 1 once the pull-out has revealed the hero."""
    return ease((g - PULL[0]) / float(PULL[1] - PULL[0]), "sine")


def tip_a(g):
    """world point of the pencil point (insert: TOUCH_GAP in front of the growing end of the track)."""
    p = track_w(line_at(g))
    e_in = 1.0 - ease(g / float(G_LAND), "cubic_out")
    gap = TOUCH_GAP * (1.0 - reveal_e(g))
    return p + Vector((-0.50 * e_in, -gap - 0.34 * e_in, -0.30 * e_in))


def cam_a(g):
    """(loc, look_at) of take A.  Spherical keys about the look point: distance, view yaw (clockwise from +y), pitch."""
    # dist, yaw, pitch, look offset x, look offset z (from the pencil point), weight of the fixed look point
    k = keys(g, [(0, (2.22, -39.0, 13.0, INSERT_OX, 0.34, 0.0), "quad_out"),
                 (SNAP1[0], (2.08, -38.0, 13.5, INSERT_OX, 0.31, 0.0), "quint"),
                 (SNAP1[1], (1.42, -34.0, 17.0, -0.12, 0.13, 0.0), "sine"),
                 (PULL[0], (1.30, -22.0, 23.0, -0.10, 0.07, 0.0), "sine"),
                 (PULL[1], (4.78, 8.0, 15.2, -0.10, 0.07, 1.0), "sine"),      # far and low enough for the pendant lamp at
                 (SNAP2[0], (4.60, 9.5, 15.4, 0, 0, 1.0), "quint"),           # (0.4, -2.6, 4.27) to hang into the top right;
                                                                              # x stays right of -1.05: clear of the desk corner
                 (SNAP2[1], (3.40, 10.0, 15.8, 0, 0, 2.0), "sine"),
                 (WHIP_OFF[1], (3.32, 9.2, 15.9, 0, 0, 2.0), "hold")])
    dist, yaw, pitch, ox, oz, w = k
    look_tip = track_w(line_at(g)) + Vector((ox, 0.0, oz))
    if w <= 1.0:
        look = look_tip.lerp(L2, w)
    else:
        look = L2.lerp(L3, w - 1.0)
    pan = 34.0 * ease((g - WHIP_OFF[0]) / float(WHIP_OFF[1] + 1 - WHIP_OFF[0]), "quad_in")      # whip-off: accelerating pan to the right
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(yr) * math.cos(pr), math.cos(yr) * math.cos(pr), math.sin(pr)))
    loc = look - d * dist
    if pan:
        v = look - loc
        a = math.radians(-pan)                                    # clockwise seen from above = toward +x
        look = loc + Vector((v.x * math.cos(a) - v.y * math.sin(a), v.x * math.sin(a) + v.y * math.cos(a), v.z))
    return loc, look


def view_yaw(loc, look):
    return math.degrees(math.atan2(look[0] - loc[0], look[1] - loc[1]))


def card_yaw_a(g):
    """yaw_fixed of the hero's card in take A (degrees), None = camera-facing.  Insert: the card passes through the pencil
    point and the feet, so the pencil really touches the map and its shadow meets it; pull-out: turns to face the camera."""
    e = reveal_e(g)
    if e >= 1.0:
        return None
    t = tip_a(g)
    touch = math.degrees(math.atan2(t.y - HERO_A[1], t.x - HERO_A[0]))
    loc, look = cam_a(g)
    return touch + (-view_yaw(loc, look) - touch) * e


def hero_a(g):
    """pose and hand spec of the hero in take A."""
    turn = ease((g - TURN[0]) / float(TURN[1] - TURN[0]), "sine")
    j = G_JAB
    lean = keys(g, [(PULL[0], -13.0, "sine"), (PULL[1], -5.0, "sine"), (j - 9, -4.0, "sine"), (GATHER[1], -8.0, "back_out"),
                    (j + 1, 4.0, "sine"), (j + 10, 0.0, "hold")])
    roll = keys(g, [(PULL[0], 4.0, "sine"), (PULL[1], 7.0, "sine"), (j - 8, 12.0, "sine"), (GATHER[1], 8.0, "back_out"),
                    (j + 1, 16.0, "sine"), (TURN[1], -9.0, "hold")])
    crouch = pulse(g, GATHER[0], GATHER[1], j, 0.07)
    sq = pulse(g, GATHER[0], GATHER[1], j - 1, 1.0)
    st_ = pulse(g, GATHER[1], j, j + 6, 1.0, "cubic_in")
    squash = (1.0 + 0.025 * sq - 0.02 * st_, 1.0 - 0.03 * sq + 0.03 * st_)
    yaw = 0.55 + (-0.10 - 0.55) * turn
    pitch = -0.4 + 0.35 * turn
    hdx = 0.05 * pulse(g, GATHER[1], j + 1, j + 9, 1.0, "cubic_in")
    pose = dict(yaw=yaw, pitch=pitch, head_roll=roll, lean=lean, head_dx=hdx, squash=squash, expr="determined",
                blink=blink(g, [PULL[1] + 1, TURN[0] + 2]), gaze=(0.85 * (1 - turn), -0.45 * (1 - turn)), arm_l="hip",
                legs=dict(preset="stand", crouch=crouch),
                arm_r=dict(preset="reach_up", stretch=1.22 - 0.10 * reveal_e(g), bend=-0.28, sharp=0.15))
    away = ease((g - (j + 2)) / 8.0, "sine")
    e_in = 1.0 - ease(g / float(G_LAND), "cubic_out")
    rise = clamp(line_at(g) / 0.75)
    ang = (-22.0 - 30.0 * rise) * (1.0 - reveal_e(g)) + (-58.0) * reveal_e(g) - 8.0 * e_in \
        + 2.0 * math.sin(g * 0.45) * (1 - e_in) * (1.0 - reveal_e(g)) + 4.0 * pulse(g, GATHER[0], GATHER[1], j, 1.0) - 26.0 * away
    return pose, ang, away


REST_A = (0.60, 0.12)                    # puppet-local: where the pencil point rests beside his head after the jab


# ----------------------------------------------------------------------------- take B: two-shot in depth
HERO_B = tuple(S.NEAR_MARK)              # (2.6, -1.95, 0): the near actor
BOSS_Y = -0.50


def boss_x(g):
    er = erase_at(g)
    return keys(g, [(G3, 1.36, "cubic_out"), (G_TOUCH - 4, 1.12, "hold")]) - 0.10 * er


def done_e(g):
    return ease((g - G_DONE) / 9.0, "sine")


def eraser_b(g):
    """world target of the eraser face and its angle."""
    er = erase_at(g)
    keep = 1.0 - er
    done = done_e(g)
    u = min(1.0, keep + 0.05)
    p = track_w(u)
    p2 = track_w(max(0.0, u - 0.02))
    t = (p - p2); t.y = 0.0
    if t.length < 1e-6:
        t = Vector((0.0, 0.0, 1.0))
    t.normalize()
    n = Vector((t.z, 0.0, -t.x))                                 # in-plane normal of the track
    ph = (g - G_TOUCH) * 2 * math.pi / STROKE
    on = clamp((g - G_TOUCH + 1) / 2.0)
    amp = 0.06 * (1 - done) * on
    tip = p + n * (amp * math.sin(ph)) + t * (0.02 * math.cos(ph) * on)
    # before the touch: the eraser comes down from beside his shoulder
    appr = 1.0 - ease((g - (G3 + 4)) / float(G_TOUCH - (G3 + 4)), "sine")
    tip = tip + Vector((0.62, 0.0, -0.10)) * appr + Vector((0.0, 0.0, 0.14)) * math.sin(math.pi * appr) * 0.6
    lift = Vector((0.50, 0.0, -0.42))                            # after the last stroke he takes the eraser away
    tip = tip + lift * done + Vector((0.0, 0.0, 0.08)) * math.sin(math.pi * done)
    ang = -140.0 + 9.0 * math.sin(ph) * (1 - done) * on + 22.0 * done + 14.0 * appr
    return tip, ang


def boss_b(g):
    er = erase_at(g)
    done = done_e(g)
    arr = ease((g - G3) / float(G_TOUCH - 4 - G3), "cubic_out")
    pose = dict(yaw=-0.5 + 0.80 * done, head_roll=keys(g, [(G3, -4.0, "sine"), (G_TOUCH, -8.0, "sine"), (G_LAST, -13.0, "sine"),
                                                          (G_DONE, -13.0, "sine"), (G_DONE + 9, 8.0, "hold")]),
                lean=-2.0 * arr - 8.0 * er + 7.0 * done, expr="smug", blink=blink(g, [G_TOUCH - 9, G_DONE + 3]),
                gaze=(-0.7 + 1.3 * done, 0.5 * er * (1 - done)),
                legs=dict(preset="stand", crouch=0.07 * er * (1 - 0.7 * done), stride=0.5 * (1 - arr)),
                arm_r="hip", arm_l=dict(preset="rub", stretch=1.18, bend=-0.5))
    return pose


def hero_b(g):
    """the hero at near_mark.  Posed as if facing right; place(flip=True) mirrors him to face the chief at screen-left."""
    shocked = g >= SHOCK
    sq = pulse(g, SHOCK - 1, SHOCK + 1, SHOCK + 5, 1.0)
    rec = ease((g - SHOCK) / 6.0, "cubic_out") if shocked else 0.0
    pose = dict(yaw=0.62, pitch=-0.15 - 0.2 * rec, head_roll=-7.0 - 3.0 * rec, lean=2.0 - 5.0 * rec,
                squash=(1.0 + 0.014 * sq, 1.0 - 0.014 * sq),
                expr="shocked" if shocked else "determined", blink=blink(g, [G3 + 9, SHOCK - 1, min(N - 6, SHOCK + 30)]),
                gaze=(0.9, -0.15), fx=(["sweat"] if shocked else []),
                arm_l="down", arm_r=dict(hand=(0.50, 0.54 - 0.10 * rec), bend=-0.6, sharp=0.3),
                prop_r=dict(type="pencil", angle=-76.0 - 10.0 * rec), legs="stand")
    return pose


CAM_TWO = (Vector((2.10, -5.25, 3.70)), Vector((1.53, -0.95, 2.05)))       # high-angle two-shot (3.7 D up, -21 deg)
CAM_FACE = (Vector((2.46, -4.60, 3.32)), Vector((2.01, -1.60, 2.20)))      # after the snap onto the hero's face


CREEP = 0.22                             # share of every take-B camera segment that is travelled at constant speed, so the
                                         # camera never parks at a key: a "hold" still creeps, as in the reference


def cam_b(g):
    ks = [(G3, tuple(CAM_TWO[0] + Vector((0.10, -0.62, 0.10))) + tuple(CAM_TWO[1] + Vector((-0.06, 0, 0.0))), "cubic_out"),
          (G3 + 14, tuple(CAM_TWO[0]) + tuple(CAM_TWO[1]), "sine"),
          (SNAP3[0], tuple(CAM_TWO[0] + Vector((0.20, 0.26, -0.03))) + tuple(CAM_TWO[1] + Vector((0.05, 0, 0.02))), "quint"),
          (SNAP3[1], tuple(CAM_FACE[0]) + tuple(CAM_FACE[1]), "quad_out"),
          (N - 1, tuple(CAM_FACE[0] + Vector((0.07, 0.20, -0.02))) + tuple(CAM_FACE[1] + Vector((0.02, 0, 0.0))), "hold")]
    k = lerp(keys(g, ks), keys(g, [(f, v, "lin") for f, v, e in ks]), CREEP)
    loc, look = Vector(k[:3]), Vector(k[3:])
    pan = -30.0 * (1.0 - ease((g - WHIP_ON[0] + 1) / float(WHIP_ON[1] - WHIP_ON[0] + 1), "quart_out"))   # still panning right, braking
    if pan:
        v = look - loc
        a = math.radians(-pan)
        look = loc + Vector((v.x * math.cos(a) - v.y * math.sin(a), v.x * math.sin(a) + v.y * math.cos(a), v.z))
    return loc, look


# ----------------------------------------------------------------------------- the film object
class HeroA(actors.Actor):
    """the take-A hero: while yaw_fixed steers the visible card (insert), the shadow proxy still stands stage-front."""
    def _proxy_yaw(self, scene, card_yaw=0.0):
        keep, self.yaw_fixed = self.yaw_fixed, None
        try:
            return super()._proxy_yaw(scene, 0.0)
        finally:
            self.yaw_fixed = keep


def scale_ratio_at(actor, cam, frame, world_point):
    """horizontal / vertical on-screen scale of the actor's card where the sight line to `world_point` meets it."""
    o, x, y, z, s = actors.card_state(actor, cam, frame)
    c = cam.matrix_world.to_translation()
    d = Vector(world_point) - c
    hit = c + d * ((o - c).dot(y) / d.dot(y))
    e = 0.05
    px = lambda v: Vector(render.world_to_screen(cam, v)[:2])
    return (px(hit + x * e) - px(hit - x * e)).length / max((px(hit + z * e) - px(hit - z * e)).length, 1e-9)


class Film(object):
    def __init__(self, take, sprite_dir=None, verbose=True):
        self.take = take
        self.g0, self.g1 = TAKES[take]
        self.sprite_dir = sprite_dir or os.path.join(TMP, "sprites_" + take)
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = S.build("INTERIOR_DAY")
        scene.render.use_persistent_data = False        # stage review: saves nothing, risks stale sprites
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, N
        self.cam = camrig.make_camera(scene, name="cam" + take)
        self.cam.data.clip_start = 0.02
        self.info = {}
        self.anch = {}
        self.cam_fn = cam_a if take == "A" else cam_b
        for g in range(self.g0, self.g1 + 1):
            loc, look = self.cam_fn(g)
            camrig.key_camera(bf(g), loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            S.set_track(line_at(g) if take == "A" else 1.0, erase_at(g) if take == "B" else 0.0, frame=bf(g))
        if take == "A":
            self.hero = h = HeroA("heroA", "hero")
            self.canvas_h = sprites.DEFAULT_CANVAS["hero"]
            h.build(self.canvas_h, self.sprite_dir, contact=True)
            h.head_flip = True                           # key light from screen-right: thick ink side and crescent to the left
            S.no_bounce(h.card)
            for g in range(self.g0, self.g1 + 1):
                h.place(bf(g), HERO_A)
            self.actors = [h]
            self.ppd = {"heroA": lambda g: 800 if g < PULL[0] + 5 else 480}      # insert: the arm is 300 to 1100 px per D on screen
        else:
            self.hero = h = actors.Actor("heroB", "hero")
            self.boss = b = actors.Actor("bossB", "boss")
            h.build(sprites.DEFAULT_CANVAS["hero"], self.sprite_dir, contact=True)
            b.build(sprites.DEFAULT_CANVAS["boss"], self.sprite_dir, contact=True)
            h.head_flip = b.head_flip = True
            S.no_bounce(h.card); S.no_bounce(b.card)
            for g in range(self.g0, self.g1 + 1):
                h.place(bf(g), HERO_B, flip=True)
                b.place(bf(g), (boss_x(g), BOSS_Y, 0.0))
            self.actors = [h, b]
            self.ppd = {"heroB": 480, "bossB": 288}
        if verbose:
            print("film: take %s built in %.1f s (frames g %d..%d)" % (take, time.time() - t0, self.g0, self.g1), flush=True)

    # ------------------------------------------------------------------ per-frame state that is not keyed
    def apply(self, g):
        """set everything of output frame g that lives in Python attributes (card yaw, which object casts the shadow)."""
        if self.take == "A":
            h = self.hero
            h.yaw_fixed = card_yaw_a(g)
            insert = g < SHADOW_SWAP
            h.card.visible_shadow = insert               # insert: the card itself casts (the pencil's shadow meets its point)
            h.proxy.hide_render = insert

    def on_frame(self, f):
        self.apply(f - 1)

    # ------------------------------------------------------------------ poses
    def pose(self, frames=None, verbose=False):
        frames = [g for g in (range(self.g0, self.g1 + 1) if frames is None else frames) if self.g0 <= g <= self.g1]
        cam = self.cam
        for g in frames:
            f = bf(g)
            self.apply(g)
            if self.take == "A":
                h = self.hero
                pose, ang, away = hero_a(g)
                tw = tip_a(g)
                e = reveal_e(g)
                feet = sprites.feet_of("hero", pose)
                self.scene.frame_set(f)
                k_head = actors.upper_stretch(h, cam, f, pose)
                k_hand = max(1.0, min(1.6, scale_ratio_at(h, cam, f, tw)))
                k = round(k_hand + (k_head - k_hand) * e, 3)
                h.upper_k[f] = k
                tgt = actors.world_to_local(h, cam, tw, f, feet=feet)
                if away > 0.0:
                    tgt = (tgt[0] + (REST_A[0] - tgt[0]) * away, tgt[1] + (REST_A[1] - tgt[1]) * away - 0.10 * math.sin(math.pi * away))
                st0 = float(pose["arm_r"].get("stretch", 1.0))
                st = st0
                while True:
                    p, info = h.pose(f, pose, hands={"r": {"tip": tgt, "prop": "pencil", "angle": ang, "stretch": st}},
                                     camera=cam, upper_k=k)
                    if info["r"]["error"] < 0.002 or st >= REACH_MAX:
                        break
                    st = min(REACH_MAX, st + 0.04)
                info["r"]["stretch"] = st
                hit = actors.local_to_world(h, info["r"]["reached"], f, feet, cam)
                c = cam.matrix_world.to_translation()
                info["r"]["clear"] = (tw - c).length - (hit - c).length
                info["r"]["screen"] = actors.local_to_screen(h, cam, info["r"]["reached"], f, feet)[:2]
                info["r"]["want"] = render.world_to_screen(cam, tw, f)[:2]
                self.info[g] = dict(hero=info, k=k, away=away)
            else:
                h, b = self.hero, self.boss
                h.pose(f, hero_b(g), camera=cam)
                tip, ang = eraser_b(g)
                p, info = b.pose(f, boss_b(g), hands={"l": {"tip": tuple(tip), "prop": "eraser", "angle": ang}}, camera=cam)
                info["l"]["screen"] = actors.local_to_screen(b, cam, info["l"]["reached"], f)[:2]
                info["l"]["want"] = render.world_to_screen(cam, tip, f)[:2]
                self.info[g] = dict(boss=info)
        res = {}
        for a in self.actors:
            ppd = self.ppd[a.name]
            groups = {}
            for g in frames:
                groups.setdefault(ppd(g) if callable(ppd) else ppd, []).append(g)
            got = {}
            for p, gl in groups.items():
                for g, r in zip(gl, a.render_sprites(p, frames=[bf(g) for g in gl], verbose=verbose)):
                    got[g] = r
            res[a.name] = [got[g] for g in frames]
            for g, r in zip(frames, res[a.name]):
                self.anch.setdefault(g, {})[a.name] = r["anchors"]
                if r.get("clipped"):
                    print("film: WARNING sprite of %s clipped on g %d" % (a.name, g), flush=True)
        return res

    # ------------------------------------------------------------------ measurements (no rendering)
    def report(self, g):
        """camera and staging numbers of output frame g (after pose()): camera position, height, pitch, yaw; for every actor
        the head centre and head width on screen (720x1280 px, y from the top); registration of the pinned prop."""
        f = bf(g)
        cam = self.cam
        self.scene.frame_set(f)
        self.apply(g)
        loc, look = self.cam_fn(g)
        v = look - loc
        out = dict(g=g, cam=[round(c, 4) for c in loc], cam_height=round(loc.z, 3),
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 2), yaw=round(view_yaw(loc, look), 2), heads={})
        for a in self.actors:
            an = self.anch.get(g, {}).get(a.name)
            if not an:
                continue
            feet = a.feet.get(f)
            hx, hy = an["head"]
            c = actors.local_to_screen(a, cam, (hx, hy), f, feet)
            l = actors.local_to_screen(a, cam, (hx - 0.5, hy), f, feet)
            r = actors.local_to_screen(a, cam, (hx + 0.5, hy), f, feet)
            t = actors.local_to_screen(a, cam, (hx, hy - 0.5), f, feet)
            b = actors.local_to_screen(a, cam, (hx, hy + 0.5), f, feet)
            out["heads"][a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1),
                                        h=round(math.hypot(b[0] - t[0], b[1] - t[1]), 1), depth=round(c[2], 3))
        inf = self.info.get(g, {})
        for who in ("hero", "boss"):
            d = inf.get(who)
            if isinstance(d, dict):
                for side, e in d.items():
                    if "screen" in e:
                        out["reg"] = dict(who=who, px=round(math.hypot(e["screen"][0] - e["want"][0], e["screen"][1] - e["want"][1]), 3),
                                          solve_err_D=round(e["error"], 5), tip=[round(e["screen"][0], 1), round(e["screen"][1], 1)],
                                          want=[round(e["want"][0], 1), round(e["want"][1], 1)])
        out["line"] = round(line_at(g) if self.take == "A" else 1.0, 4)
        out["erase"] = round(erase_at(g) if self.take == "B" else 0.0, 4)
        return out

    # ------------------------------------------------------------------ render
    def render(self, frames, out_dir, scale=1.0, threads=4, samples=16, skip_existing=False, verbose=True):
        frames = [g for g in frames if self.g0 <= g <= self.g1]
        if skip_existing:
            frames = [g for g in frames if not os.path.exists(os.path.join(out_dir, "f_%04d.png" % bf(g)))]
        if not frames:
            return []
        self.scene.cycles.samples = samples
        return render.render_frames([bf(g) for g in frames], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, on_frame=self.on_frame, verbose=verbose)
